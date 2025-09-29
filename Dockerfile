# Use an official Python runtime as a parent image
FROM python:3.9

# Install ffmpeg, which is a dependency for moviepy
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code to the working directory
COPY . .

# Set the default command to run when the container starts
CMD ["python", "main.py"]