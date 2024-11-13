import subprocess
import sys
import os
import platform
import getpass
import mysql

MYSQL_ROOT_PASSWORD = 'root_password' 
DB_NAME = 'test_data_bank'
TABLE_NAME = 'data_entries'

def install_mysql():
    """Installs MySQL server if not installed."""
    system = platform.system()

    if system == "Windows":
        print("This script can help guide you through installing MySQL on Windows.")
        print("You can download the MySQL Installer from: https://dev.mysql.com/downloads/installer/")
        print("After installation, run this script again to complete the database setup.")
        sys.exit(1)

    try:
        print("Checking MySQL installation...")
        subprocess.run(['mysql', '--version'], check=True)
        print("MySQL is already installed.")
    except subprocess.CalledProcessError:
        print("MySQL is not installed. Installing MySQL...")

        if system == "Darwin": 
            subprocess.run(['brew', 'install', 'mysql'], check=True)
        elif system == "Linux": 
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'mysql-server'], check=True)
        else:
            print("Unsupported system for automatic MySQL installation.")
            sys.exit(1)

def set_mysql_root_password():
    """Prompt user to set MySQL root password."""
    print("MySQL root password is required for setup.")
    password = getpass.getpass("Enter a new MySQL root password (or press Enter to use the default): ")

    if not password:
        password = 'default_password'

    return password

def create_database():
    """Creates a MySQL database and table."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=set_mysql_root_password()
        )

        if connection.is_connected():
            print("Connected to MySQL server.")
            cursor = connection.cursor()

            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
            print(f"Database '{DB_NAME}' created or already exists.")

            cursor.execute(f"USE {DB_NAME};")

            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    tags VARCHAR(255),
                    comment TEXT,
                    environment VARCHAR(255)
                );
            """)
            print(f"Table '{TABLE_NAME}' created or already exists.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def main():
    """Main function to install MySQL and set up the database and tables."""
    install_mysql()
    create_database()

if __name__ == "__main__":
    main()
