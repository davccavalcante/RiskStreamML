# Use a lightweight Python base image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code to the container
COPY . .

# Create output and log directories if they don't exist
RUN mkdir -p data output logs hdfs_simulation hdfs_simulation/user hdfs_simulation/user/data

# Command to run the application when the container is started
CMD ["python", "run.py"]
