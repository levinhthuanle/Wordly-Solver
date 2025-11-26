FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY Requirements.txt .
RUN pip install --no-cache-dir -r Requirements.txt

# Copy application files
COPY main.py .
COPY words.txt .
COPY algorithms/ ./algorithms/
COPY history/ ./history/

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
