# Description: Dockerfile for building the production image of the Django application
# Two stage build to reduce the size of the final image by not including the build dependencies
# and only including the runtime dependencies

# Stage 1: Base build stage
FROM python:3.13-slim AS builder

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Install dependencies first for caching benefit
RUN pip install --upgrade pip 
COPY requirements.txt /app/ 
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.13-slim

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser . .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000 

# Make entry file executable
RUN mkdir -p /app/logs && chmod -R 777 /app/logs
RUN mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles
RUN chmod +x  /app/entrypoint.prod.sh

# Start the application using Gunicorn
CMD ["/app/entrypoint.prod.sh"]
