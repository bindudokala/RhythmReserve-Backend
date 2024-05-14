# Use the official Python 3.11 image as a parent image
FROM python:3.11.1-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
# Since requirements.txt is at the root of your project, just copy it directly.
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the rest of your Django project
# This assumes that Dockerfile is in the same directory as manage.py.
COPY ./RhythmReserve .

# Expose the port the app runs on
EXPOSE 8000

# Run the application with Uvicorn
CMD ["uvicorn", "RhythmReserve.asgi:application", "--host", "0.0.0.0", "--port", "8000"]