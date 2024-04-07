# Use an official Python runtime as a parent image, based on Alpine
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Create the directory where the configuration file will be located
RUN mkdir /config

# Inform Docker that the container expects a volume to be mounted at /config
VOLUME /config

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ensure your application uses the configuration file from /config, adjust accordingly
# For example, your application might need to be informed about the config path via an environment variable or command-line argument

# Run script.py when the container launches, assuming script.py is adjusted to use /config/config.yaml
CMD ["python", "./main.py"]