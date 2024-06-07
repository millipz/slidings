# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Set the environment variables
ENV DATABASE_URL=postgresql://postgres:password@db:5432/mydb
ENV PYTHONPATH=/

# Expose the port the app will run on
EXPOSE 8000

# Start the application with Uvicorn
CMD ["uvicorn", "src.pontoon:app", "--host", "0.0.0.0", "--port", "8000"]