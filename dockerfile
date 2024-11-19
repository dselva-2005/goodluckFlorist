FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run Uvicorn
CMD ["uvicorn", "myshop.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
