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
        try:
            datos = self.leer_datos()
            codigo_producto = producto.codigo_producto
            if not str(codigo_producto) in datos.keys():
                datos[codigo_producto] = producto.to_dict()
                self.guardar_datos(datos)
                print(f"Se agregó el producto {producto.producto} a la base de datos.")
            else:
                # Si el producto ya existe, quero qu eme diga que producto es, para saber si ya esta cargado. 
                producto_existente = datos[str(codigo_producto)]["producto"]
                print(f"El código del producto ingresado ya existe en la base de datos y está relacionado con el producto '{producto_existente}'.")
        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')
    
    #Para leer producto
    def leer_producto(self, codigo_producto):
        try:
            datos = self.leer_datos()
            if codigo_producto in datos:
                producto_data = datos[codigo_producto]
                if 'modelo' in producto_data:
                    return ProductoElectronico(**producto_data)
                else:
                    return ProductoAlimenticio(**producto_data)
            else:
                return None  # No se encontró el producto

        except Exception as e:
            print(f'Error al leer producto: {e}')
            return None
    
    def buscar_producto_por_codigo(self, codigo_producto):
        producto = self.leer_producto(codigo_producto)
        if producto:
            print(f'Producto encontrado: {producto}')
        else:
            print(f'No se encontró producto con código {codigo_producto}')
    
    def actualizar_producto(self, codigo_producto, actualiza_cantidad_stock):
        try:
            datos = self.leer_datos()
            if str(codigo_producto) in datos.keys():
                 datos[codigo_producto]['cantidad_stock'] = actualiza_cantidad_stock #deberia hacer validaciones aca tbn?
                 self.guardar_datos(datos)
                 nombre_producto = datos[codigo_producto]['producto']
                 print(f'Stock actualizado para el producto {nombre_producto} con código {codigo_producto}')
            else:
                print(f'No se encontró producto con codigo:{codigo_producto} ')
        except Exception as e:
            print(f'Error al actualizar el producto: {e}')

    def eliminar_producto(self, codigo_producto):
        try:
            datos = self.leer_datos()
            if str(codigo_producto) in datos.keys():
                 nombre_producto = datos[codigo_producto]['producto']
                 del datos[codigo_producto]
                 self.guardar_datos(datos)
                 print(f'Base de datos actualizada. Se ha eliminado el producto {nombre_producto} con código {codigo_producto}')
            else:
                print(f'No se encontró producto con codigo:{codigo_producto} ')
        except Exception as e:
            print(f'Error al eliminar el producto: {e}')
    



    
    

