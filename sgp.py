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

import json
class Producto:
    def __init__(self, codigo_producto, producto, precio, cantidad_stock):
        self.__codigo_producto = self.validar_codigo_producto(codigo_producto)
        self.__producto = producto
        self.__precio = precio
        self.__cantidad_stock = self.validar_cantidad_stock(cantidad_stock)
            
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
    
    @cantidad_stock.setter
    def cantidad_stock(self, nuevo_stock):
        self.__cantidad_stock = self.validar_cantidad_stock(nuevo_stock)


    def to_dict(self):
        return {
            "codigo_producto": self.codigo_producto,
            "producto": self.producto,
            "precio": self.precio,
            "cantidad_stock": self.cantidad_stock,
        }
    
    def __str__(self):
        return f"{self.producto} {self.codigo_producto}"
   
# Para ISBN-13: Multiplica alternativamente cada dígito por 1 y 3, comenzando por el primer dígito.Suma todos los resultados.
# Divide la suma por 10. El dígito de control es el número que debes añadir a la suma para que sea un múltiplo de 10.
# Si la suma ya es múltiplo de 10, el dígito de control es 0. Sería interesante calcularlo para revisar.Si tengo tiempo lo hago

    def validar_codigo_producto(self, codigo_producto):
        try:
            codigo_producto_num = int(codigo_producto)
            if len(str(codigo_producto)) != [13]:
                raise ValueError("El código del producto debe tener 13 dígitos. ")
        except ValueError:
            raise ValueError("El código del producto debe ser un número y estar compuesto por 13 dígitos.")
    
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
        super().__init__(codigo_producto, producto, precio, cantidad_stock)
        #Mapeo los atributos que agrego ala subclase
        self.__marca = marca
        self.__modelo = modelo

    @property
    def marca(self):
        return self.__marca
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
        super().__init__(codigo_producto, producto, precio, cantidad_stock)
        #Mapeo los atributos que agrego ala subclase
        self.__marca = marca
        self.__modelo = peso

    @property
    def marca(self):
        return self.__marca

    def to_dict(self):
        data = super().to_dict()
        data["marca"] = self.marca
        return data

    def __str__(self):
        return f"{super().__str__()} - marca: {self.marca}"
    
    @property
    def peso(self):
        return self.peso

    def to_dict(self):
        data = super().to_dict()
        data["peso"] = self.peso
        return data

    def __str__(self):
        return f"{super().__str__()} - peso: {self.peso}"

class GestionProductos:
    def __init__(self, archivo):
        self.archivo = archivo
    #Traigo los datos para leerlos
    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del {self.archivo}: {error}')
        #Si sale todo bien, retorna los datos
        else:
            return datos
    
    #Para guardar
    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4) #Son los espacios dentro del json ára facilitar su lectura: 4 es el más utilizado
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')
    

    #Para crear producto
    def crear_producto(self, producto):
        datos = self.leer_datos()
        codigo_producto = Producto.codigo_producto
        if not str(codigo_producto) in datos.keys():
            datos[codigo_producto] = Producto.to_dict()
            self.guardar_datos(datos)
            print(f"Se agregó el producto {Producto.producto} {Producto.codigo_producto} a la base de datos.")


    
    

