# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory
WORKDIR /app

# Accept build arguments
ARG APP_HOST
ARG APP_PORT

# Set environment variables
ENV APP_HOST=${APP_HOST}
ENV APP_PORT=${APP_PORT}

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application into the container
COPY . .

# Expose the port
EXPOSE ${APP_PORT}

# Use a shell command to run the FastAPI server with substituted environment variables
CMD ["sh", "-c", "uvicorn server:app --host ${APP_HOST} --port ${APP_PORT}"]
