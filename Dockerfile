FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code (including app/main.py and app/models_weights/)
COPY . .

# Expose port and run uvicorn using Render's dynamic PORT environment variable
EXPOSE 8000
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"