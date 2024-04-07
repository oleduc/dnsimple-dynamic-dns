import os
import shutil
import time
import requests
import yaml
import logging
from typing import List, Dict, Any, Callable
from dnsimple import Client
from dnsimple.struct import ZoneRecordUpdateInput

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def collect_pages(api_call: Callable[[int], Any]) -> List[Any]:
    """Collects paginated results from a given API call."""
    results = []
    current_page = 1
    total_pages = 1
    current_response = None

    while not current_response or current_response.pagination.current_page <= total_pages:
        try:
            current_response = api_call(current_page)
            total_pages = current_response.pagination.total_pages
            current_page += 1
            results.extend(current_response.data)
        except Exception as e:
            logging.error(f"API call failed: {e}")
            break

    return results


def get_current_external_ip(ip_service_url: str) -> str:
    """Fetches the current public IP address."""
    try:
        public_ip_response = requests.get(ip_service_url)
        public_ip_response.raise_for_status()  # Raises an exception for 4XX/5XX errors
        return public_ip_response.text
    except requests.RequestException as e:
        raise Exception('Failed to fetch public IP.') from e


def get_current_config_zone(config: Dict[str, Any], zone_name: str) -> Dict[str, Any]:
    """Finds the configuration for the specified DNS zone."""
    filtered_config_zones = [config_zone for config_zone in config['zones'] if config_zone['name'] == zone_name]
    if len(filtered_config_zones) != 1:
        raise Exception(f"Expected exactly one zone configuration for {zone_name}, found {len(filtered_config_zones)}.")

    return filtered_config_zones[0]


def update_dns_records(config: Dict[str, Any]):
    """Updates DNS records based on the current public IP and specified configuration."""
    public_ip = get_current_external_ip(config['ip_service_url'])

    dnsimple_client = Client(access_token=config['api_token'])
    zones = collect_pages(lambda page: dnsimple_client.zones.list_zones(config['account_id'], page=page))

    for zone in zones:
        try:
            configured_zone = get_current_config_zone(config, zone.name)
        except Exception as e:
            logging.warning(e)
            continue

        records = collect_pages(
            lambda page: dnsimple_client.zones.list_records(config['account_id'], zone.name, page=page))

        for record in records:
            config_records = [config_record for config_record in configured_zone['records']
                              if config_record['name'] == record.name and record.type == 'A']
            if len(config_records) != 1:
                continue

            try:
                response = dnsimple_client.zones.update_record(
                    config['account_id'],
                    zone.name,
                    record.id,
                    ZoneRecordUpdateInput(content=public_ip)
                )
                if response.http_response.status_code == 200:
                    logging.info(f"Updated DNS record for {record.name}.{zone.name} to IP {public_ip}.")
                else:
                    logging.error(f"Failed to update DNS record for {record.name}.{zone.name}.")
            except Exception as e:
                logging.error(f"Exception updating DNS record for {record.name}.{zone.name}: {e}")


def load_or_initialize_config():
    config_path = '/config/config.yml'
    example_config_path = 'example_config.yml'

    # Check if the config file exists
    if not os.path.exists(config_path):
        logging.warning(
            f"No config.yml found in {config_path}. Creating one from the example config. PLEASE EDIT THIS FILE WITH YOUR SETTINGS.")
        shutil.copy(example_config_path, config_path)

        with open(example_config_path, 'r') as file:
            example_config = file.read()
            print("\nExample config.yml content:\n")
            print(
                example_config)

        raise SystemExit("Please configure config.yml in /config directory and restart the script.")

    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def main():
    config = load_or_initialize_config()

    try:
        while True:
            update_dns_records(config)
            time.sleep(config['update_frequency_seconds'] * 60)
    except KeyboardInterrupt:
        logging.info("Script terminated by user.")


main()
