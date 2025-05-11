# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt from the local backend directory into the container
COPY backend/requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the react app into the container
COPY myApp /app/frontend

# build the react app
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Move the react build to Djangos static folder
WORKDIR /app
RUN mkdir -p /app/staticfiles
RUN cp -r /app/frontend/build/* /app/staticfiles/


# Copy the rest of the Django project (local backend directory) into the container
COPY backend /app/

# Expose port 8000 for the Django development server
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]