# dnsimple-dynamic-dns
## Description
This project provides a dynamic DNS updater script that automatically updates DNS records on DNSimple based on the current external IP address of the host it's running on. Designed to run in a Docker or Podman container for easy deployment, it ensures that your DNS records always point to the correct IP address, which is especially useful for home servers, IoT devices, or any instance where the IP address may change frequently.
Prerequisites

 - Docker or Podman
 - Docker Compose (optional, for convenience)
 - Python 3.9 or later (if running outside of Docker)

## Getting Started
1. Clone the Repository

To get started, clone this repository to your local machine:
sh
```
git clone https://github.com/oleduc/dnsimple-dynamic-dns.git
cd dnsimple-dynamic-dns
```

2. Configuration

Before running the script, you need to set up your configuration:
 - Navigate to the config directory within the cloned repository.
 - If there is no config.yml present, copy the provided example_config.yml to config.yml.
 - Edit config.yml with your DNSimple API token, account ID, and specify the DNS zones and records you wish to automatically update.

Important: The script requires a properly configured config.yml file to function correctly.

3. Build and Run with Docker

To build the Docker image, execute:
sh
```
docker build -t dnsimple-dynamic-dns .
```

To run the Docker container and mount the config directory:
sh
```
docker run -d -v $(pwd)/config:/config dnsimple-dynamic-dns
```

4. Using Docker Compose

For convenience, you can use Docker Compose to manage the build and run process:
sh
```
docker-compose up --build -d
```

To stop the service:
sh
```
docker-compose down
```

## Customizing the Script
The script can be customized by modifying the config.yml file. For advanced customizations, you may also edit the Python script to add or modify functionality. Please ensure you're familiar with Python and the DNSimple API before making any changes.

## Troubleshooting
If you encounter issues, first verify that your config.yml file is correctly configured with your DNSimple credentials and target DNS records. Ensure that the Docker container has network access and can reach the DNSimple API and the external IP address resolution service.

## Contributing
Contributions to dnsimple-dynamic-dns are welcome! If you have improvements or bug fixes, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is open-source and available under the MIT License.