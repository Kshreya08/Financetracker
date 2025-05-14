# Use official Python image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy backend code
COPY ./backend /app/backend

# Copy frontend code
COPY ./frontend /app/frontend

# Set environment variables (for Flask)
ENV FLASK_APP=backend/app.py

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "backend/app.py"]
