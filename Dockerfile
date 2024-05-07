FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    wget \
    xfonts-75dpi \
    xfonts-base

# Download wkhtmltopdf from the provided link
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb

# Install wkhtmltopdf
# Ensure that missing dependencies are automatically installed
RUN dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb; apt-get install -f -y

# Clean up unnecessary files and clear the apt cache to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /wkhtmltox_0.12.6-1.buster_amd64.deb

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8000

# Define the command to run the application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]