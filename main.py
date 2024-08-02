import os
import platform
import time

from sgp import (
    ProductoAlimenticio,
    ProductoElectronico,
    GestionProductos,
)

def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo / windows es diferente a los demas'''
    if platform.system() == 'Windows': #windows 
        os.system('cls')
    else:
        os.system('clear') # Para Linux/Unix/MacOs

def mostrar_menu():
    print("========== Menú de Gestión de Productos ==========")
    print("1: Agregar un producto electrónico")
    print("2: Agregar un producto alimenticio")
    print("3: Buscar producto por código")

#Pra evitar cargar todos los datos, quier primero verificar el codigo del producto

#Para cargar productos
def agregar_producto(gestion, tipo_producto):
    try:
        codigo_producto = input('Ingrese código del producto: ')
        producto = input('Ingrese el producto: ')
        precio = float(input(f'Ingrese el precio de {producto} : '))
        cantidad_stock = int(input(f'Ingrese el stock de {producto} : '))
        marca = input(f'Ingrese la marca del {producto} : ')
        #modelo = input(f'Ingrese el modelo del {producto} : ')
        #peso = input(f'Ingrese el peso del {producto} : ')  

        if tipo_producto == '1':
            modelo = input(f'Ingrese el modelo del {producto} : ')
            producto= ProductoElectronico(codigo_producto, producto, precio, cantidad_stock, marca, modelo)
        elif tipo_producto == '2':
            peso = int(input(f'Ingrese el peso del {producto} : ')) 
            producto= ProductoAlimenticio(codigo_producto, producto, precio, cantidad_stock, marca, peso)
        else:
            print('Opción inválida')
            return
        
        gestion.crear_producto(producto)
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Error:{e}')
    except Exception as e:
        print(f'Error inesperado')


def buscar_producto_por_codigo(gestion):
    codigo_producto = input('Ingrese el código del producto buscar: ')
    gestion.leer_producto(codigo_producto)
    input('Presione enter para continuar...')

def actualizar_stock_producto(gestion):
    pass

def eliminar_producto_por_codigo(gestion):
    pass

def mostrar_todos_los_productos(gestion):
    pass

if __name__ == "__main__":
    archivo_productos='productos_db.json'
    gestion_productos=GestionProductos(archivo_productos)
    
    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción:') 
        
        if opcion == '1' or opcion == '2':
            agregar_producto(gestion_productos,opcion)
        elif opcion == '3':
            buscar_producto_por_codigo(gestion_productos)
        else:
            print('Opción no válida')