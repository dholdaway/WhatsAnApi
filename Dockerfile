# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install FastAPI + Uvicorn
RUN pip install fastapi uvicorn python-multipart

# Copy app files
COPY main.py /app/
COPY static /app/static
COPY images /app/images

# Expose the default FastAPI port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
