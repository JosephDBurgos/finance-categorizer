# Use the official Python 3.11 slim image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /workspace/app

# Copy the requirements file from the root directory
COPY requirements.txt .
COPY alembic.ini .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Set the default command to run Alembic migrations and start the app
CMD ["sh", "-c", "alembic -c /workspace/app/alembic.ini upgrade head && python app.py"]