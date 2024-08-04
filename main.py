import os
import platform
from datetime import datetime

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

        # Pra evitar cargar todos los datos, quier primero verificar el codigo del producto
        if gestion.leer_producto(codigo_producto):
            print(f'Error: El código {codigo_producto} ya existe. Intente con otro código.')
            input('Presione enter para continuar...')
            return  
        
        # si el código no existe sigue por aca
        nombre_producto = input('Ingrese el nombre del producto: ')
        precio = float(input(f'Ingrese el precio de {nombre_producto}: '))
        cantidad_stock = int(input(f'Ingrese el stock de {nombre_producto}: '))
        marca = input(f'Ingrese la marca del {nombre_producto}: ')

        if tipo_producto == '1':
            modelo = input(f'Ingrese el modelo del {nombre_producto}: ')
            producto = ProductoElectronico(codigo_producto, nombre_producto, precio, cantidad_stock, marca, modelo)
        elif tipo_producto == '2':
            peso = int(input(f'Ingrese el peso del {nombre_producto}: '))
            producto = ProductoAlimenticio(codigo_producto, nombre_producto, precio, cantidad_stock, marca, peso)
        else:
            print('Opción inválida')
            return
        
        gestion.crear_producto(producto)
        print('Producto agregado exitosamente.')
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Error: {e}')
        input('Presione enter para continuar...')
    except Exception as e:
        print(f'Error inesperado: {e}')
        input('Presione enter para continuar...')

def buscar_producto_por_codigo(gestion):
    codigo_producto = input('Ingrese el código del producto buscar: ')
    gestion.buscar_producto_por_codigo(codigo_producto)
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
    limpiar_pantalla()
    print('=========== Listado completo de los productos ==========')

    productos_electronicos = []
    productos_alimenticios = []

    for producto in gestion.leer_datos().values():
        if 'modelo' in producto:
            producto_str = f"{producto['codigo_producto']} - {producto['producto']} - Stock {producto['cantidad_stock']} - modelo {producto['modelo']}"
            productos_electronicos.append(producto_str)
        else:
            producto_str = f"{producto['codigo_producto']} - {producto['producto']} - Stock {producto['cantidad_stock']} - peso {producto['peso']}"
            productos_alimenticios.append(producto_str)

    # Imprimir productos con modelo
    print('Productos Electrónicos:')
    print('\n'.join(productos_electronicos))
    print('========================================================')

    # Imprimir productos sin modelo
    print('Productos Alimenticios:')
    print('\n'.join(productos_alimenticios))
    print('========================================================')
    
    opcion_guardar = input('¿Desea guardar los productos en un archivo de texto? (s/n): ').lower()
    if opcion_guardar == 's':
        # Generar nombre del archivo con fecha y hora
        fecha_hora_actual = datetime.now().strftime('%Y%m%d-%H%M')
        nombre_archivo = f"{fecha_hora_actual}_listado_de_productos.txt"
        
        with open(nombre_archivo, 'w') as archivo_txt:
            archivo_txt.write('=========== Listado completo de los productos ==========\n')
            archivo_txt.write('=========== Productos electronicos =========== ==========\n')
            archivo_txt.write('\n'.join(productos_electronicos))
            archivo_txt.write('\n========================================================\n')
            archivo_txt.write('=========== Productos alimenticios =======================\n')
            archivo_txt.write('\n'.join(productos_alimenticios))
            archivo_txt.write('\n========================================================\n')

        
        print(f'Productos guardados en {nombre_archivo}')
    
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