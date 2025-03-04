# Use an official lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY s3_proxy.py requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Expose the API port
EXPOSE 5001

# Run the application
CMD ["python", "s3_proxy.py"]
