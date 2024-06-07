# Use the official Python base image with version 3.10.12
FROM python:3.10.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container at /app
COPY . .

# Expose port 5000 to allow external access to the application
EXPOSE 5000

# Run the Flask server with --host=0.0.0.0 to make it externally accessible
CMD ["flask", "run", "--host=0.0.0.0"]
