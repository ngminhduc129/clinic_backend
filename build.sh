#!/usr/bin/env bash
# Thoát ngay nếu có lỗi
set -o errexit

# Cập nhật và cài đặt ODBC Driver cho SQL Server (Bản 18)
if ! [[ "18.04 20.04 22.04" == *"$(lsb_release -rs)"* ]]; then
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
    apt-get update
    ACCEPT_EULA=Y apt-get install -y msodbcsql18
fi

# Cài đặt các thư viện Python
pip install -r requirements.txt