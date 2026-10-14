import json
import os

class GestorJSON:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        carpeta = os.path.dirname(ruta_archivo)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta, exist_ok=True)
        if not os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, "w", encoding="utf-8") as f:
                json.dump([], f)

    def leer(self):
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def guardar(self, datos):
        with open(self.ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)