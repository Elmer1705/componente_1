def imprimir_titulo(texto):
    print("\n" + "=" * 50)
    print(f"  {texto}")
    print("=" * 50)

def imprimir_exito(mensaje):
    print(f"[✓] {mensaje}")

def imprimir_error(mensaje):
    print(f"[✗] Error: {mensaje}")

def imprimir_info(mensaje):
    print(f"[i] {mensaje}")

def confirmar(pregunta):
    resp = input(f"{pregunta} (s/n): ").strip().lower()
    return resp in ("s", "si", "sí", "y", "yes")