# Use an official Python runtime as a parent image
FROM python:3.12-bookworm

# Set the working directory
WORKDIR /app

# Copy the application files into the container
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV TERM=xterm-256color

# Command to run the application
CMD ["python", "barista.py"]