from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import ProveedorController, ProductoController, CompraController


class Menu:

    def __init__(self):
        self.proveedores = ProveedorController()
        self.productos = ProductoController()
        self.compras = CompraController(self.proveedores, self.productos)

    # ---------- ayudas ----------
    def pausa(self):
        input("\nPresione Enter para continuar...")

    def pedir_entero(self, texto):
        try:
            return int(input(texto))
        except ValueError:
            return None

    def pedir_flotante(self, texto):
        try:
            return float(input(texto))
        except ValueError:
            return None

    def mostrar_resultado(self, exito, mensaje):
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)

    # ---------- menú principal ----------
    def ejecutar(self):
        while True:
            imprimir_titulo("SISTEMA DE GESTIÓN")
            print("  1. Proveedores")
            print("  2. Productos")
            print("  3. Compras")
            print("  0. Salir\n")
            opcion = input("Opción: ").strip()

            if opcion == "1":
                self.menu_crud(self.proveedores)
            elif opcion == "2":
                self.menu_crud(self.productos)
            elif opcion == "3":
                self.menu_compras()
            elif opcion == "0":
                imprimir_info("¡Hasta luego! 👋")
                break
            else:
                imprimir_error("Opción no válida")
                self.pausa()

    # ---------- menú exclusivo para compras ----------
    def menu_compras(self):
        while True:
            imprimir_titulo("COMPRAS")
            print("  1. Registrar compra")
            print("  0. Salir (volver)\n")
            opcion = input("Opción: ").strip()

            if opcion == "1":
                self.crear_compra()
            elif opcion == "0":
                break
            else:
                imprimir_error("Opción no válida")
                self.pausa()

    # ---------- menú CRUD genérico (proveedores y productos) ----------
    def menu_crud(self, controlador):
        titulo = controlador.nombre.upper() + "S"

        while True:
            imprimir_titulo(titulo)
            print(f"  1. Crear {controlador.nombre}")
            print("  2. Ver todos")
            print("  3. Buscar")
            print("  4. Ver por id")
            print("  5. Actualizar")
            print("  6. Eliminar")
            print("  0. Volver\n")
            opcion = input("Opción: ").strip()

            if opcion == "1":
                self.crear(controlador)
            elif opcion == "2":
                self.ver_todos(controlador)
            elif opcion == "3":
                self.buscar(controlador)
            elif opcion == "4":
                self.ver_por_id(controlador)
            elif opcion == "5":
                self.actualizar(controlador)
            elif opcion == "6":
                self.eliminar(controlador)
            elif opcion == "0":
                break
            else:
                imprimir_error("Opción no válida")
                self.pausa()

    # ---------- operaciones generales ----------
    def crear(self, controlador):
        imprimir_titulo(f"CREAR {controlador.nombre.upper()}")
        datos = {}
        for campo in controlador.campos:
            datos[campo] = input(f"{campo.capitalize()}: ")

        exito, mensaje = controlador.crear(datos)
        self.mostrar_resultado(exito, mensaje)
        self.pausa()

    def ver_todos(self, controlador):
        imprimir_titulo(controlador.nombre.upper() + "S")
        lista = controlador.leer()
        if len(lista) == 0:
            imprimir_info("No hay registros todavía.")
        else:
            for objeto in lista:
                print(f"  {objeto}")
            imprimir_info(f"Total: {len(lista)}")
        self.pausa()

    def buscar(self, controlador):
        imprimir_titulo(f"BUSCAR {controlador.nombre.upper()}")
        texto = input("Buscar: ")
        encontrados = controlador.buscar(texto)
        if len(encontrados) == 0:
            imprimir_info(f"Sin coincidencias para '{texto}'.")
        else:
            for objeto in encontrados:
                print(f"  {objeto}")
        self.pausa()

    def ver_por_id(self, controlador):
        imprimir_titulo(f"VER {controlador.nombre.upper()}")
        id_registro = self.pedir_entero("Id: ")
        objeto = controlador.obtener(id_registro)
        if objeto is None:
            imprimir_error("No encontrado")
        else:
            for clave, valor in objeto.a_diccionario().items():
                print(f"  {clave.capitalize()}: {valor}")
        self.pausa()

    def actualizar(self, controlador):
        imprimir_titulo(f"ACTUALIZAR {controlador.nombre.upper()}")
        id_registro = self.pedir_entero("Id: ")
        objeto = controlador.obtener(id_registro)
        if objeto is None:
            imprimir_error("No encontrado")
            self.pausa()
            return

        imprimir_info(f"Editando: {objeto.etiqueta()}")
        print("Deje en blanco lo que no quiera cambiar.\n")
        cambios = {}
        for campo in controlador.campos:
            actual = getattr(objeto, campo)
            nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
            if nuevo != "":
                cambios[campo] = nuevo

        exito, mensaje = controlador.actualizar(id_registro, cambios)
        self.mostrar_resultado(exito, mensaje)
        self.pausa()

    def eliminar(self, controlador):
        imprimir_titulo(f"ELIMINAR {controlador.nombre.upper()}")
        id_registro = self.pedir_entero("Id: ")
        objeto = controlador.obtener(id_registro)
        if objeto is None:
            imprimir_error("No encontrado")
            self.pausa()
            return

        imprimir_info(f"Se eliminará: {objeto.etiqueta()}")
        if confirmar("¿Confirma?"):
            exito, mensaje = controlador.eliminar(id_registro)
            self.mostrar_resultado(exito, mensaje)
        else:
            imprimir_info("Operación cancelada")
        self.pausa()

    # ---------- solo para compras ----------
    def crear_compra(self):
        imprimir_titulo("REGISTRAR COMPRA")
        proveedor_id = self.pedir_entero("Id del proveedor: ")
        if proveedor_id is None:
            imprimir_error("El id debe ser un número")
            self.pausa()
            return

        imprimir_info("Productos registrados en el sistema:")
        for producto in self.productos.leer():
            print(f"  {producto}")

        items = []
        while True:
            producto_id = self.pedir_entero("\nId del producto (0 para terminar): ")
            if producto_id is None or producto_id == 0:
                break
            cantidad = self.pedir_entero("Cantidad a ingresar: ")
            if cantidad is None or cantidad <= 0:
                imprimir_error("Cantidad inválida")
                continue
            costo_unitario = self.pedir_flotante("Costo unitario de compra: ")
            if costo_unitario is None or costo_unitario <= 0:
                imprimir_error("Costo unitario inválido")
                continue
            items.append({
                "producto_id": producto_id,
                "cantidad": cantidad,
                "costo_unitario": costo_unitario
            })

        exito, mensaje = self.compras.crear({"proveedor_id": proveedor_id, "items": items})
        self.mostrar_resultado(exito, mensaje)
        self.pausa()


if __name__ == "__main__":
    try:
        Menu().ejecutar()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")