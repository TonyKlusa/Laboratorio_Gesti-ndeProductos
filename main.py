from sgp import (
    ProductoAlimenticio,
    ProductoElectronico,
    GestionProductos,
)

def mostrar_menu():
    print("========== Menú de Gestión de Productos ==========")
    print("1: Agregar un producto electrónico")


def agregar_producto(gestion, tipo_producto):
    try:
        codigo_producto = input('Ingrese código del producto: ')
        producto = input('Ingrese el producto: ')
        precio = float(input(f'Ingrese el precio de {producto} : '))
        cantidad_stock = int(input(f'Ingrese el stock de {producto} : '))
        marca = input(f'Ingrese la marca del {producto} : ')
        modelo = input(f'Ingrese el modelo del {producto} : ')
        peso = input(f'Ingrese el peso del {producto} : ') #peso no está disponible porque Productos alimenticios no se carga. 

        producto= ProductoElectronico(codigo_producto, producto, precio, cantidad_stock, marca, modelo)
        gestion.crear_producto(producto)

    except ValueError as e:
        print(f'Error:{e}')
    except Exception as e:
        print(f'Error inesperado')


def buscar_producto_por_codigo(gestion):
    pass

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
        mostrar_menu()
        opcion = input('Seleccione una opción:') 
        if opcion == '1':
            agregar_producto(gestion_productos,opcion)
        else:
            print('Opción no válida')