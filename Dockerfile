FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make port 7860 available (Hugging Face default)
ENV PORT=7860

# Run the application
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT}
