import mysql.connector
from mysql.connector import Error
from decouple import config

def conectar_bd():
    try:
        # Conectarse a la base de datos utilizando las variables de entorno
        connection = mysql.connector.connect(
            host=config('DB_HOST', default='localhost'),
            database=config('DB_DATABASE'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            port=config('DB_PORT', default=3306)
        )
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print(f"Conectado a MySQL Server versión {db_Info}")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"Conectado a la base de datos {record}")

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("La conexión MySQL ha sido cerrada.")

if __name__ == "__main__":
    conectar_bd()
