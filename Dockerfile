FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make port 8080 available to the world outside this container
ENV PORT=8080

# Run the application
CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT}