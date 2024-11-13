from mysql.connector import Error

def search_data(connection, username=None, tags=None, environment=None):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM data_entries WHERE 1=1"
        
        if username:
            query += f" AND data LIKE '%{username}%'"
        if tags:
            query += f" AND tags LIKE '%{tags}%'"
        if environment:
            query += f" AND environment = '{environment}'"
        
        cursor.execute(query)
        result = cursor.fetchall()
        
        if result:
            results = []
            for row in result:
                results.append(f"Data: {row[1]}, Environment: {row[3]}, Tags: {row[4]}")
            return results
        else:
            return ["No data found based on the search criteria."]
    except Error as e:
        print(f"Error: '{e}'")
        return ["Error in database query."]
