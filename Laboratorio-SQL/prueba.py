import mysql.connector
from mysql.connector import Error
from decouple import config

def conectar_bd():
    try:
        connection = mysql.connector.connect(
            host=config('DB_HOST', default='localhost'),
            database=config('DB_DATABASE'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            port=config('DB_PORT', default=3306)
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def cargar_producto(codigo_producto, nombre_producto, precio, cantidad_stock, marca, tipo_producto, modelo=None, peso=None):
    connection = conectar_bd()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Verificar si el código del producto ya existe
            cursor.execute('SELECT codigo_producto FROM productos WHERE codigo_producto = %s', (codigo_producto,))
            if cursor.fetchone():
                print(f'Error: Ya existe un producto con el código {codigo_producto}.')
                return
            
            # Insertar producto en la tabla productos
            query_producto = '''
                INSERT INTO productos (codigo_producto, producto, precio, cantidad_stock, marca)
                VALUES (%s, %s, %s, %s, %s)
            '''
            cursor.execute(query_producto, (codigo_producto, nombre_producto, precio, cantidad_stock, marca))

            # Insertar en la tabla específica según el tipo de producto
            if tipo_producto == 'electronic':
                if modelo is None:
                    print('Error: Se requiere un modelo para productos electrónicos.')
                    return
                query_electronico = '''
                    INSERT INTO productoselectronicos (codigo_producto, modelo)
                    VALUES (%s, %s)
                '''
                cursor.execute(query_electronico, (codigo_producto, modelo))
            elif tipo_producto == 'alimenticio':
                if peso is None:
                    print('Error: Se requiere un peso para productos alimenticios.')
                    return
                query_alimenticio = '''
                    INSERT INTO productosalimenticios (codigo_producto, peso)
                    VALUES (%s, %s)
                '''
                cursor.execute(query_alimenticio, (codigo_producto, peso))
            else:
                print('Error: Tipo de producto no válido.')
                return
            
            connection.commit()
            print(f'Producto {nombre_producto} con código {codigo_producto} ha sido agregado exitosamente.')
        except Error as e:
            print(f"Error al cargar el producto: {e}")
        finally:
            cursor.close()
            connection.close()
            print("La conexión MySQL ha sido cerrada.")

if __name__ == "__main__":
    # Ejemplo de uso
    cargar_producto(
        codigo_producto='623456',
        nombre_producto='Laptop',
        precio=1200.00,
        cantidad_stock=10,
        marca='Dell',
        tipo_producto='electronic',
        modelo='XPS 15'
    )
