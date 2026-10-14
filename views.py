from abc import ABC, abstractmethod

from models import Cliente, Proveedor, Producto, Compra
from shared.json_manager import GestorJSON


# =====================================================================
# CLASE BASE (ABSTRACTA)
# =====================================================================
class CrudBase(ABC):

    @abstractmethod
    def leer(self):
        pass

    @abstractmethod
    def buscar(self, texto):
        pass

    @abstractmethod
    def siguiente(self):
        pass

    @abstractmethod
    def crear(self, datos):
        pass

    @abstractmethod
    def actualizar(self, id_registro, datos):
        pass

    @abstractmethod
    def eliminar(self, id_registro):
        pass


# =====================================================================
# CONTROLADOR DE CLIENTES
# =====================================================================
class ClienteController(CrudBase):

    def __init__(self, archivo="data/clientes.json"):
        self.nombre = "cliente"
        self.campos = Cliente.CAMPOS
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Cliente.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for cliente in self.lista:
            datos.append(cliente.a_diccionario())
        self.gestor.guardar(datos)

    def obtener(self, id_cliente):
        for cliente in self.lista:
            if cliente.id == id_cliente:
                return cliente
        return None

    def leer(self):
        return self.lista

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for cliente in self.lista:
            if (texto in cliente.nombre.lower()
                    or texto in cliente.apellido.lower()
                    or texto in cliente.email
                    or texto in cliente.telefono
                    or texto in cliente.ciudad.lower()):
                encontrados.append(cliente)
        return encontrados

    def siguiente(self):
        mayor = 0
        for cliente in self.lista:
            if cliente.id > mayor:
                mayor = cliente.id
        return mayor + 1

    def crear(self, datos):
        email = str(datos.get("email", "")).strip().lower()
        for cliente in self.lista:
            if cliente.email == email:
                return False, "Ese email ya está registrado"

        try:
            cliente = Cliente(self.siguiente(),
                              datos.get("nombre", ""),
                              datos.get("apellido", ""),
                              datos.get("email", ""),
                              datos.get("telefono", ""),
                              datos.get("ciudad", ""))
        except ValueError as error:
            return False, str(error)

        self.lista.append(cliente)
        self.guardar()
        return True, f"Cliente creado: {cliente.etiqueta()}"

    def actualizar(self, id_cliente, datos):
        if not datos:
            return False, "No se indicó ningún cambio"

        cliente = self.obtener(id_cliente)
        if cliente is None:
            return False, f"No existe cliente con id {id_cliente}"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            for otro in self.lista:
                if otro.email == email and otro.id != id_cliente:
                    return False, "Ese email ya está registrado"

        try:
            nuevo = Cliente(cliente.id,
                            datos.get("nombre", cliente.nombre),
                            datos.get("apellido", cliente.apellido),
                            datos.get("email", cliente.email),
                            datos.get("telefono", cliente.telefono),
                            datos.get("ciudad", cliente.ciudad))
        except ValueError as error:
            return False, str(error)

        posicion = self.lista.index(cliente)
        self.lista[posicion] = nuevo
        self.guardar()
        return True, f"Cliente {id_cliente} actualizado"

    def eliminar(self, id_cliente):
        cliente = self.obtener(id_cliente)
        if cliente is None:
            return False, f"No existe cliente con id {id_cliente}"

        self.lista.remove(cliente)
        self.guardar()
        return True, f"Cliente {id_cliente} eliminado"


# =====================================================================
# CONTROLADOR DE PROVEEDORES
# =====================================================================
class ProveedorController(CrudBase):

    def __init__(self, archivo="data/proveedores.json"):
        self.nombre = "proveedor"
        self.campos = Proveedor.CAMPOS
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Proveedor.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for proveedor in self.lista:
            datos.append(proveedor.a_diccionario())
        self.gestor.guardar(datos)

    def obtener(self, id_proveedor):
        for proveedor in self.lista:
            if proveedor.id == id_proveedor:
                return proveedor
        return None

    def leer(self):
        return self.lista

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for proveedor in self.lista:
            if (texto in proveedor.nombre.lower()
                    or texto in proveedor.apellido.lower()
                    or texto in proveedor.email
                    or texto in proveedor.ruc
                    or texto in proveedor.empresa.lower()):
                encontrados.append(proveedor)
        return encontrados

    def siguiente(self):
        mayor = 0
        for proveedor in self.lista:
            if proveedor.id > mayor:
                mayor = proveedor.id
        return mayor + 1

    def crear(self, datos):
        ruc = str(datos.get("ruc", "")).strip()
        for proveedor in self.lista:
            if proveedor.ruc == ruc:
                return False, "Ese RUC ya está registrado"

        try:
            proveedor = Proveedor(self.siguiente(),
                                  datos.get("nombre", ""),
                                  datos.get("apellido", ""),
                                  datos.get("email", ""),
                                  ruc,
                                  datos.get("empresa", ""))
        except ValueError as error:
            return False, str(error)

        self.lista.append(proveedor)
        self.guardar()
        return True, f"Proveedor creado: {proveedor.etiqueta()}"

    def actualizar(self, id_proveedor, datos):
        if not datos:
            return False, "No se indicó ningún cambio"

        proveedor = self.obtener(id_proveedor)
        if proveedor is None:
            return False, f"No existe proveedor con id {id_proveedor}"

        if "ruc" in datos:
            ruc = str(datos["ruc"]).strip()
            for otro in self.lista:
                if otro.ruc == ruc and otro.id != id_proveedor:
                    return False, "Ese RUC ya está registrado"

        try:
            nuevo = Proveedor(proveedor.id,
                              datos.get("nombre", proveedor.nombre),
                              datos.get("apellido", proveedor.apellido),
                              datos.get("email", proveedor.email),
                              datos.get("ruc", proveedor.ruc),
                              datos.get("empresa", proveedor.empresa))
        except ValueError as error:
            return False, str(error)

        posicion = self.lista.index(proveedor)
        self.lista[posicion] = nuevo
        self.guardar()
        return True, f"Proveedor {id_proveedor} actualizado"

    def eliminar(self, id_proveedor):
        proveedor = self.obtener(id_proveedor)
        if proveedor is None:
            return False, f"No existe proveedor con id {id_proveedor}"

        self.lista.remove(proveedor)
        self.guardar()
        return True, f"Proveedor {id_proveedor} eliminado"


# =====================================================================
# CONTROLADOR DE PRODUCTOS
# =====================================================================
class ProductoController(CrudBase):

    def __init__(self, archivo="data/productos.json"):
        self.nombre = "producto"
        self.campos = Producto.CAMPOS
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Producto.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for producto in self.lista:
            datos.append(producto.a_diccionario())
        self.gestor.guardar(datos)

    def obtener(self, id_producto):
        for producto in self.lista:
            if producto.id == id_producto:
                return producto
        return None

    def leer(self):
        return self.lista

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for producto in self.lista:
            if texto in producto.nombre.lower():
                encontrados.append(producto)
        return encontrados

    def siguiente(self):
        mayor = 0
        for producto in self.lista:
            if producto.id > mayor:
                mayor = producto.id
        return mayor + 1

    def crear(self, datos):
        nombre = str(datos.get("nombre", "")).strip().title()
        for producto in self.lista:
            if producto.nombre == nombre:
                return False, f"Ya existe un producto llamado {nombre}"

        stock = datos.get("stock", "")
        if str(stock).strip() == "":
            stock = 0

        try:
            producto = Producto(self.siguiente(), nombre, datos.get("precio", ""), stock)
        except ValueError as error:
            return False, str(error)

        self.lista.append(producto)
        self.guardar()
        return True, f"Producto creado: {producto.etiqueta()}"

    def actualizar(self, id_producto, datos):
        if not datos:
            return False, "No se indicó ningún cambio"

        producto = self.obtener(id_producto)
        if producto is None:
            return False, f"No existe producto con id {id_producto}"

        if "nombre" in datos:
            nombre = str(datos["nombre"]).strip().title()
            for otro in self.lista:
                if otro.nombre == nombre and otro.id != id_producto:
                    return False, f"Ya existe un producto llamado {nombre}"

        try:
            nuevo = Producto(producto.id,
                             datos.get("nombre", producto.nombre),
                             datos.get("precio", producto.precio),
                             datos.get("stock", producto.stock))
        except ValueError as error:
            return False, str(error)

        posicion = self.lista.index(producto)
        self.lista[posicion] = nuevo
        self.guardar()
        return True, f"Producto {id_producto} actualizado"

    def eliminar(self, id_producto):
        producto = self.obtener(id_producto)
        if producto is None:
            return False, f"No existe producto con id {id_producto}"

        self.lista.remove(producto)
        self.guardar()
        return True, f"Producto {id_producto} eliminado"

    def con_stock_bajo(self, minimo=5):
        bajos = []
        for producto in self.lista:
            if producto.stock <= minimo:
                bajos.append(producto)
        return bajos


# =====================================================================
# CONTROLADOR DE COMPRAS
# =====================================================================
class CompraController(CrudBase):

    def __init__(self, proveedores, productos, archivo="data/compras.json"):
        self.nombre = "compra"
        self.campos = Compra.CAMPOS
        self.gestor = GestorJSON(archivo)

        self.proveedores = proveedores
        self.productos = productos

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Compra.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for compra in self.lista:
            datos.append(compra.a_diccionario())
        self.gestor.guardar(datos)

    def obtener(self, id_compra):
        for compra in self.lista:
            if compra.id == id_compra:
                return compra
        return None

    def leer(self):
        return self.lista

    def buscar(self, texto):
        texto = texto.strip()
        encontrados = []
        if texto == "":
            return encontrados

        for compra in self.lista:
            if texto in compra.fecha:
                encontrados.append(compra)
        return encontrados

    def siguiente(self):
        mayor = 0
        for compra in self.lista:
            if compra.id > mayor:
                mayor = compra.id
        return mayor + 1

    def crear(self, datos):
        # datos = {"proveedor_id": 1, "items": [{"producto_id": 2, "cantidad": 5, "costo_unitario": 12.50}, ...]}
        try:
            proveedor_id = int(datos.get("proveedor_id", 0))
        except (TypeError, ValueError):
            return False, "El proveedor_id debe ser un número"

        if self.proveedores.obtener(proveedor_id) is None:
            return False, f"No existe un proveedor con id {proveedor_id}"

        items = datos.get("items", [])
        if len(items) == 0:
            return False, "La compra debe tener al menos un producto"

        ids_vistos = []
        for item in items:
            producto = self.productos.obtener(item["producto_id"])
            if producto is None:
                return False, f"No existe producto con id {item['producto_id']}"
            if producto.id in ids_vistos:
                return False, f"El producto {producto.nombre} está repetido en la compra"
            ids_vistos.append(producto.id)

        try:
            compra = Compra(self.siguiente(), proveedor_id, datos.get("fecha", ""))
            for item in items:
                producto = self.productos.obtener(item["producto_id"])
                compra.agregar_detalle(producto, item["cantidad"], item["costo_unitario"])
                producto.aumentar_stock(item["cantidad"])
        except ValueError as error:
            return False, str(error)

        self.productos.guardar()
        self.lista.append(compra)
        self.guardar()
        return True, f"Compra {compra.id} registrada por ${compra.total:.2f}"

    def actualizar(self, id_compra, datos):
        return False, "Las compras registradas no se pueden modificar"

    def eliminar(self, id_compra):
        compra = self.obtener(id_compra)
        if compra is None:
            return False, f"No existe compra con id {id_compra}"

        self.lista.remove(compra)
        self.guardar()
        return True, f"Compra {id_compra} eliminada"

    def comprobante(self, id_compra):
        compra = self.obtener(id_compra)
        if compra is None:
            return None

        proveedor = self.proveedores.obtener(compra.proveedor_id)
        if proveedor is None:
            nombre_prov = "Eliminado"
            ruc = "N/A"
        else:
            nombre_prov = f"{proveedor.nombre_completo} ({proveedor.empresa})"
            ruc = proveedor.ruc

        texto = f"COMPROBANTE DE COMPRA #{compra.id}   Fecha: {compra.fecha}\n"
        texto += f"Proveedor: {nombre_prov} | RUC: {ruc}\n"
        texto += "-" * 55 + "\n"
        for detalle in compra.detalles:
            texto += f"  {detalle}\n"
        texto += "-" * 55 + "\n"
        texto += f"  TOTAL: ${compra.total:.2f}  ({compra.cantidad_items} ítems)"
        return texto