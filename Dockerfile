# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
#TODO copy more selectively what is needed for run or test containers i.e. Dockerfile is now in container.
COPY . /app
⌈
# Install any needed packages specified in requirements.txt
# If you don't have a requirements.txt, you can remove this line
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt