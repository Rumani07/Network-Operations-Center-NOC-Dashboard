# Use an official lightweight Python runtime
FROM python:3.12-slim

# Set environment variables to optimize Python behavior inside the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app



# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django project code
COPY . .

# Expose port 8000 to allow network traffic to the container
EXPOSE 8000

# Run migrations, collect static files, and start Gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn network_project.wsgi:application --bind 0.0.0.0:8000"]
