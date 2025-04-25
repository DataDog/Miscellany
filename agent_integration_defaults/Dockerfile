FROM python:3.13-slim

# Install dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Clone the integrations-core repo
RUN git clone https://github.com/DataDog/integrations-core.git

# Set the working directory to the cloned repo
COPY src/requirements.txt /src/requirements.txt
RUN pip3 install --no-cache-dir -r /src/requirements.txt

# Copy the Python script into the container
COPY /src /app

# Run the script
CMD ["python", "collect_configs.py"]