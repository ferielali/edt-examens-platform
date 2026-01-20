FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variable for Python path
ENV PYTHONPATH=/app

# Default port
ENV PORT=8000

# Expose port
EXPOSE 8000

# Start command - using shell form for variable expansion
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
