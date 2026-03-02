FROM python:3.12-slim

# Cài đặt các công cụ cần thiết để cài Driver SQL Server
RUN apt-get update && apt-get install -y \
    curl apt-transport-https gnupg2 unixodbc-dev g++ \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Chạy app
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
