# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt first to leverage Docker caching
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Change the working directory to src
WORKDIR /app/src

# Expose the port on which Flask will run
EXPOSE 5000

# Define environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

# Command to run the Flask app
#for dev: CMD ["flask", "run", "--host=0.0.0.0"]
#for prod
CMD ["gunicorn", "src.app:app", "--bind", "0.0.0.0:5000"]