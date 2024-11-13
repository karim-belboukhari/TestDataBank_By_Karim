import mysql.connector
from mysql.connector import Error

def insert_data_entry(connection, data, environment):
    try:
        cursor = connection.cursor()
        sql = """
        INSERT INTO data_entries (data, environment, tags, comment)
        VALUES (%s, %s, %s, %s)
        """
        tags = data.get('tags', None)
        comment = data.get('comment', None)
        data_json = str(data)
        
        cursor.execute(sql, (data_json, environment, tags, comment))
        connection.commit()
        print("Data inserted successfully!")
    except Error as e:
        print(f"Error: '{e}'")
