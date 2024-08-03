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
    print('4. Actualizar stock del producto')
    print('5. Eliminar producto por código')
    print('6. Mostrar todos los productos')
    print('7. Salir')
    print('======================================================')

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
        input('Presione enter para continuar...')    
    except Exception as e:
        print(f'Error inesperado')
        input('Presione enter para continuar...')

def buscar_producto_por_codigo(gestion):
    codigo_producto = input('Ingrese el código del producto buscar: ')
    gestion.leer_producto(codigo_producto)
    input('Presione enter para continuar...')

def actualizar_stock_producto(gestion):
    codigo_producto = input('Ingrese el código del producto a modificar stock: ')
    actualiza_cantidad_stock=int(input('Ingresa la cantidad de stock del producto'))
    gestion.actualizar_producto(codigo_producto, actualiza_cantidad_stock)
    input('Presione enter para continuar...')

def eliminar_producto_por_codigo(gestion):
    codigo_producto = input('Ingrese el código del producto a eliminar stock: ')
    gestion.eliminar_producto(codigo_producto)
    input('Presione enter para continuar...')

def mostrar_todos_los_productos(gestion):
    print('=========== Listado completo de los productos ==========')
    #print('Código       / Producto  /     Stock                    ')
    for producto in gestion.leer_datos().values():
        if 'modelo' in producto:
            print(f"{producto['codigo_producto']} - {producto['producto']} - Stock {producto['cantidad_stock']} - modelo {producto['modelo']}")
        else:
            print(f"{producto['codigo_producto']} - {producto['producto']} - Stock {producto['cantidad_stock']} - peso {producto['peso']}")
    print('========================================================')
    input('Presione enter para continuar...')

if __name__ == "__main__":
    archivo_productos='productos_db.json'
    gestion_productos=GestionProductos(archivo_productos)
    
    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción para continuar: ') 
        
        if opcion == '1' or opcion == '2':
            agregar_producto(gestion_productos,opcion)
        elif opcion == '3':
            buscar_producto_por_codigo(gestion_productos)
        elif opcion == '4':
            actualizar_stock_producto(gestion_productos)
        elif opcion == '5':
            eliminar_producto_por_codigo(gestion_productos)
        elif opcion == '6':
            mostrar_todos_los_productos(gestion_productos)
        elif opcion == '7':
            print('Saliendo del programa')
            input('Presione enter para continuar...')
            break
        else:
            print('Opción no válida, ingrese una opción del 1 al 7.')