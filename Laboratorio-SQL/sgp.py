'''
Desafío 1: Sistema de Gestión de Productos
Objetivo: Desarrollar un sistema para manejar productos en un inventario.

Requisitos:

Crear una clase base Producto con atributos como producto, precio, cantidad en stock, etc.
Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos
y métodos específicos.
Implementar operaciones CRUD para gestionar productos del inventario.
Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
Persistir los datos en archivo JSON.'''

import mysql.connector
from mysql.connector import Error
import decouple
from decouple import config


class Producto:
    def __init__(self, codigo_producto, producto, precio, cantidad_stock, marca):
        self.__codigo_producto = self.validar_codigo_producto(codigo_producto)
        self.__producto = producto
        self.__precio = precio
        self.__cantidad_stock = self.validar_cantidad_stock(cantidad_stock)
        self.__marca = marca
            
    @property
    def codigo_producto(self):
        return self.__codigo_producto

    @property
    def producto(self):
        return self.__producto.capitalize()

    @property
    def precio(self):
        return self.__precio

    @property
    def cantidad_stock(self):
        return self.__cantidad_stock

    @property
    def marca(self):
        return self.__marca
    
    @cantidad_stock.setter
    def cantidad_stock(self, nuevo_stock):
        self.__cantidad_stock = self.validar_cantidad_stock(nuevo_stock)


    def to_dict(self):
        return {
            "codigo_producto": self.codigo_producto,
            "producto": self.producto,
            "precio": self.precio,
            "cantidad_stock": self.cantidad_stock,
            "marca": self.marca
        }
    
    def __str__(self):
        return f"{self.producto} {self.codigo_producto}"
    
    def validar_codigo_producto(self, codigo_producto):
        try:
            codigo_producto_num = int(codigo_producto)
            if len(str(codigo_producto)) == 6:
                return codigo_producto_num
            else:
                raise ValueError("El código del producto debe tener 6 dígitos. ")
        except ValueError:
            raise ValueError("El código del producto debe ser un número y estar compuesto por 6 dígitos.")

    def validar_cantidad_stock(self, cantidad_stock):
        try:
            cantidad_stock_num = float(cantidad_stock)
            if cantidad_stock_num <= 0:
                raise ValueError("El stock debe ser numérico positivo.")
            return cantidad_stock_num
        except ValueError:
            raise ValueError("El stock debe ser un número válido.")
        
#Desarrollo las subclases que pide la consigna


class ProductoElectronico(Producto):
    def __init__(self, codigo_producto, producto, precio, cantidad_stock, marca, modelo):
        super().__init__(codigo_producto, producto, precio, cantidad_stock, marca)
        #Mapeo los atributos que agrego ala subclase
        self.__modelo = modelo

#Ej. de polimorfismo.El mismo metodo, según de donde lo ejecutemos responde de una manera u otra.
    def to_dict(self):
        data = super().to_dict()
        data["marca"] = self.marca
        return data

    def __str__(self):
        return f"{super().__str__()} - marca: {self.marca}"
    
    @property
    def modelo(self):
        return self.__modelo

    def to_dict(self):
        data = super().to_dict()
        data["modelo"] = self.modelo
        return data

    def __str__(self):
        return f"{super().__str__()} - modelo: {self.modelo}"

class ProductoAlimenticio(Producto):
    def __init__(self, codigo_producto, producto, precio, cantidad_stock, marca, peso):
        super().__init__(codigo_producto, producto, precio, cantidad_stock, marca)
        #Mapeo los atributos que agrego ala subclase
        self.__peso = peso

    @property
    def peso(self):
        return self.__peso

    def to_dict(self):
        data = super().to_dict()
        data["peso"] = self.peso
        return data

    def __str__(self):
        return f"{super().__str__()} - peso: {self.peso}"

class GestionProductos:
    def __init__(self):
        self.host = config('DB_HOST')
        self.database = config('DB_DATABASE')
        self.usuario = config('DB_USER')
        self.password =config('DB_PASSWORD')
        self.port = config('DB_PORT')
    
    def connect(self):
        '''Establecer una conexión con la base de datos'''
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.usuario,  
                password=self.password,
                port=self.port
                )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f'Error al conectar a la BD') #acá podria hacer un manejo de errores
            return None
#######################
    #Traigo los datos para leerlos
        '''    def leer_datos(self):
                try:
                    connection = self.connect()
                    if connection:
                        with connection.cursor() as cursor:
                            # Verificar si el codigo ya existe
                            cursor.execute('SELECT codigo_producto FROM productos WHERE codigo_producto = %s', (producto.codigo_producto,))
                            if cursor.fetchone():
                                print(f' Datos leidos con éxito. Producto {producto.producto} encontrado')
                                return
                
                except Exception as error:
                    raise Exception(f'Error al leer datos del {self.archivo}: {error}')
                #Si sale todo bien, retorna los datos
                finally:
                    if connection.is_connected:
                        connection.close()
                
            #Para guardar
            def guardar_datos(self, datos):'''
        '''        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4) #Son los espacios dentro del json ára facilitar su lectura: 4 es el más utilizado
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')'''
        pass
#########################
   
    #Para crear producto
    def crear_producto(self, producto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Verificar si el codigo ya existe
                    cursor.execute('SELECT codigo_producto FROM productos WHERE codigo_producto = %s', (producto.codigo_producto,))
                    if cursor.fetchone():
                        print(f'Error: Ya existe un producto con producto con ')
                        return
                    
                    # Insertar producto dependiendo del tipo
                    if isinstance(producto, ProductoAlimenticio):
                        query = '''
                        INSERT INTO Productos (codigo_producto, producto, cantidad_stock, precio, marca)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.codigo_producto, producto.producto, producto.cantidad_stock, producto.precio, producto.marca))
                        query = '''
                        INSERT INTO productosalimenticios (codigo_producto, peso)
                        VALUES (%s, %s)
                        '''
                        cursor.execute(query, (producto.codigo_producto, producto.peso))
                    elif isinstance(producto, ProductoElectronico):
                        query = '''
                        INSERT INTO productos (codigo_producto, producto, cantidad_stock, precio, marca)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.codigo_producto, producto.producto, producto.cantidad_stock, producto.precio, producto.marca))
                        query = '''
                        INSERT INTO productoselectronicos (codigo_producto, modelo)
                        VALUES (%s, %s)
                        '''
                        cursor.execute(query, (producto.codigo_producto, producto.modelo))
                    connection.commit()
                    print(f'Producto {producto.producto} creado correctamente')
        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')

    
    def actualizar_producto(self, codigo_producto, actualiza_cantidad_stock):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Verificar si el código del producto existe
                    cursor.execute('SELECT producto FROM productos WHERE codigo_producto = %s', (codigo_producto,))
                    producto = cursor.fetchone()

                    if producto:
                        # Validar el nuevo valor de stock
                        if not isinstance(actualiza_cantidad_stock, int) or actualiza_cantidad_stock < 0:
                            print('Error: La cantidad de stock debe ser un número entero positivo.')
                            return

                        # Actualizar el stock del producto
                        cursor.execute('UPDATE productos SET cantidad_stock = %s WHERE codigo_producto = %s',
                                    (actualiza_cantidad_stock, codigo_producto))
                        connection.commit()
                        print(f'Stock actualizado para el producto {producto[0]} con código {codigo_producto}')
                    else:
                        print(f'No se encontró producto con código: {codigo_producto}')
        except Exception as e:
            print(f'Error al actualizar el producto: {e}')

       
    def eliminar_producto(self, codigo_producto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Verificar si el producto existe
                    cursor.execute('SELECT producto FROM productos WHERE codigo_producto = %s', (codigo_producto,))
                    producto = cursor.fetchone()

                    if producto:
                        # Eliminar registros relacionados en productoselectronicos y productosalimenticios
                        cursor.execute('DELETE FROM productoselectronicos WHERE codigo_producto = %s', (codigo_producto,))
                        cursor.execute('DELETE FROM productosalimenticios WHERE codigo_producto = %s', (codigo_producto,))
                        connection.commit()
                        # Eliminar el producto de la tabla productos
                        cursor.execute('DELETE FROM productos WHERE codigo_producto = %s', (codigo_producto,))
                        connection.commit()
                        print(f'Producto {producto[0]} con código {codigo_producto} eliminado correctamente.')
                    else:
                        print(f'No se encontró producto con código: {codigo_producto}')

        except Exception as error:
            print(f'Error inesperado al eliminar producto: {error}')

    


    def leer_datos(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Verificar si el codigo ya existe
                    cursor.execute('SELECT codigo_producto FROM productos WHERE codigo_producto = %s', (producto.codigo_producto,))
                    if cursor.fetchone():
                        print(f' Datos leidos con éxito. Producto {producto.producto} encontrado')
                        return
           
        except Exception as error:
            raise Exception(f'Error al leer datos del {self.archivo}: {error}')
        #Si sale todo bien, retorna los datos
        finally:
            if connection.is_connected:
                connection.close()
          
    #Para guardar
    def guardar_datos(self, datos):
        '''        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4) #Son los espacios dentro del json ára facilitar su lectura: 4 es el más utilizado
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')'''
        pass
#########################
   
    def buscar_producto(self, codigo_producto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Buscar el producto por su código
                    cursor.execute('SELECT producto, cantidad_stock FROM productos WHERE codigo_producto = %s', (codigo_producto,))
                    producto = cursor.fetchone()

                    if producto:
                        print(f'Producto: {producto[0]} con stock: {producto[1]}')
                    else:
                        print(f'No se encontró producto con código: {codigo_producto}')

        except Exception as error:
            print(f'Error inesperado al buscar producto: {error}')

    
    

