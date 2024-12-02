# Lightweight Python image
FROM python:3.12-slim
# Installing dependencies for mysqlclient > 2.2
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*
# Set the working directory
WORKDIR /po_django
# Copy the requirements file
COPY requirements.txt requirements.txt
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the project code
COPY . .
# Expose the port for Django
EXPOSE 8000
# Command to run the Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]