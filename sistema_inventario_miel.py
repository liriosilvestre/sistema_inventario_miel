import csv
import json
import os
from datetime import datetime

ARCHIVO_JSON = "inventario_miel.json"
ARCHIVO_CSV = "historial_movimientos.csv"

# Límites para alertas de inventario bajo
MINIMO_GRANEL_LITROS = 100.0
MINIMO_ENVASES = 20

# --- 1. FUNCIONES DE PERSISTENCIA (JSON Y CSV) ---

def obtener_estructura_inicial():
    """
    Devuelve la estructura base del inventario con todos los contadores en cero.
    """
    return {
        "miel_granel_litros": 0.0,
        "inversion_total": 0.0,
        "ingresos_totales": 0.0,
        "productos": {
            "1_litro": {
                "nombre": "Envase 1 Litro",
                "stock": 0,
                "precio_venta": 250.0,
                "costo_envase": 10.0,
                "litros_por_unidad": 1.0
            },
            "medio_litro": {
                "nombre": "Envase 1/2 Litro",
                "stock": 0,
                "precio_venta": 140.0,
                "costo_envase": 6.0,
                "litros_por_unidad": 0.5
            }
        }
    }

def cargar_datos():
    """
    Carga el estado del inventario desde JSON o crea uno nuevo en cero si no existe.
    """
    if os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return obtener_estructura_inicial()

def guardar_json(datos):
    """
    Guarda el estado actual del inventario en el archivo JSON.
    """
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def registrar_historial_csv(tipo_movimiento, detalle, cantidad, monto):
    """
    Agrega una fila con fecha y hora al archivo CSV (compatible con Excel).
    """
    archivo_nuevo = not os.path.exists(ARCHIVO_CSV)
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ARCHIVO_CSV, mode="a", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.writer(archivo)
        if archivo_nuevo:
            escritor.writerow(["Fecha y Hora", "Movimiento", "Detalle", "Cantidad", "Monto ($)"])
        escritor.writerow([fecha_hora, tipo_movimiento, detalle, cantidad, f"{monto:.2f}"])

# --- 2. FUNCIONES DE VISUALIZACIÓN Y ALERTAS ---

def verificar_alertas_stock(datos):
    """
    Revisa los niveles de inventario y muestra advertencias si están por debajo del mínimo.
    """
    alertas = []

    if datos["miel_granel_litros"] < MINIMO_GRANEL_LITROS:
        alertas.append(f"ALERTA: Miel a granel baja ({datos['miel_granel_litros']:.1f} L). Mínimo: {MINIMO_GRANEL_LITROS} L.")

    for prod in datos["productos"].values():
        if prod["stock"] < MINIMO_ENVASES:
            alertas.append(f"ALERTA: Stock bajo en '{prod['nombre']}' ({prod['stock']} uds). Mínimo: {MINIMO_ENVASES} uds.")

    if alertas:
        print("\n" + "!" * 56)
        for alerta in alertas:
            print(alerta)
        print("!" * 56)

def mostrar_reporte_financiero(datos):
    """
    Muestra el inventario físico, la ganancia neta y activa las alertas de stock.
    """
    ganancia_neta = datos["ingresos_totales"] - datos["inversion_total"]
    p1 = datos["productos"]["1_litro"]
    p2 = datos["productos"]["medio_litro"]

    print("\n" + "=" * 56)
    print("            REPORTE DE INVENTARIO Y FINANZAS")
    print("=" * 56)
    print(f"Miel a granel disponible : {datos['miel_granel_litros']:.1f} litros")
    print(f"Stock {p1['nombre']:<18} : {p1['stock']} uds (${p1['precio_venta']} c/u)")
    print(f"Stock {p2['nombre']:<18} : {p2['stock']} uds (${p2['precio_venta']} c/u)")
    print("-" * 56)
    print(f"Ingresos por ventas      : ${datos['ingresos_totales']:,.2f}")
    print(f"Inversión / Costos       : ${datos['inversion_total']:,.2f}")
    print(f"GANANCIA NETA ACTUAL     : ${ganancia_neta:,.2f}")
    print("=" * 56)

    verificar_alertas_stock(datos)

def mostrar_historial_pantalla():
    """
    Lee el archivo CSV e imprime en pantalla la tabla completa de movimientos registrados.
    """
    if not os.path.exists(ARCHIVO_CSV):
        print("\n[Info] Aún no hay movimientos registrados en el historial.")
        return

    print("\n" + "=" * 82)
    print("                         HISTORIAL DE MOVIMIENTOS")
    print("=" * 82)

    with open(ARCHIVO_CSV, mode="r", encoding="utf-8-sig") as archivo:
        lector = csv.reader(archivo)
        for indice, fila in enumerate(lector):
            if len(fila) == 5:
                print(f"{fila[0]:<20} | {fila[1]:<14} | {fila[2]:<24} | {fila[3]:<5} | ${fila[4]}")
                if indice == 0:
                    print("-" * 82)

    print("=" * 82)

# --- 3. FUNCIONES DE OPERACIONES ---

def registrar_compra_tonelada(datos, toneladas, costo_por_tonelada):
    """
    Suma miel a granel en litros, registra el gasto y guarda en JSON y CSV.
    """
    litros_nuevos = toneladas * 704.0
    gasto = toneladas * costo_por_tonelada
    datos["miel_granel_litros"] += litros_nuevos
    datos["inversion_total"] += gasto

    guardar_json(datos)
    registrar_historial_csv("COMPRA GRANEL", f"{toneladas} ton ({litros_nuevos:.1f} L)", toneladas, -gasto)
    print(f"\n[OK] Compra registrada: +{litros_nuevos:.1f} L a granel. Costo: ${gasto:,.2f}")

def envasar_miel(datos, clave_prod, cantidad):
    """
    Descuenta miel a granel, aumenta botellas listas y registra el costo de empaque.
    """
    producto = datos["productos"][clave_prod]
    litros_requeridos = cantidad * producto["litros_por_unidad"]

    if datos["miel_granel_litros"] >= litros_requeridos:
        datos["miel_granel_litros"] -= litros_requeridos
        producto["stock"] += cantidad
        costo_empaque = cantidad * producto["costo_envase"]
        datos["inversion_total"] += costo_empaque

        guardar_json(datos)
        registrar_historial_csv("ENVASADO", producto["nombre"], cantidad, -costo_empaque)
        print(f"\n[OK] Se envasaron {cantidad} uds de '{producto['nombre']}'. Costo envases: ${costo_empaque:,.2f}")
        verificar_alertas_stock(datos)
    else:
        print(f"\n[Error] Miel insuficiente. Solo tienes {datos['miel_granel_litros']:.1f} L a granel.")

def registrar_venta(datos, clave_prod, cantidad):
    """
    Descuenta unidades vendidas del stock, suma ingresos y actualiza JSON y CSV.
    """
    producto = datos["productos"][clave_prod]

    if producto["stock"] >= cantidad:
        producto["stock"] -= cantidad
        ingreso = cantidad * producto["precio_venta"]
        datos["ingresos_totales"] += ingreso

        guardar_json(datos)
        registrar_historial_csv("VENTA", producto["nombre"], cantidad, ingreso)
        print(f"\n[OK] Venta registrada: {cantidad} x {producto['nombre']} = +${ingreso:,.2f}")
        verificar_alertas_stock(datos)
    else:
        print(f"\n[Error] Stock insuficiente. Solo hay {producto['stock']} botellas listas.")

def reiniciar_sistema_a_cero():
    """
    Restablece el archivo JSON a cero y limpia el historial CSV previa confirmación.
    """
    confirmar = input("\n¿Estás seguro de borrar TODO el historial y volver a cero? (s/n): ").strip().lower()
    if confirmar == "s":
        datos_limpios = obtener_estructura_inicial()
        guardar_json(datos_limpios)
        if os.path.exists(ARCHIVO_CSV):
            os.remove(ARCHIVO_CSV)
        print("\n[OK] Sistema reiniciado a cero. Se limpiaron JSON y CSV.")
        return datos_limpios
    else:
        print("\nOperación cancelada. Tus datos siguen intactos.")
        return cargar_datos()

# --- 4. MENÚ INTERACTIVO ---

def seleccionar_presentacion():
    """
    Muestra las opciones de envase y devuelve la clave seleccionada.
    """
    print("\nSelecciona la presentación:")
    print("1. Envase de 1 Litro ($250)")
    print("2. Envase de 1/2 Litro ($140)")
    opcion = input("Opción (1 o 2): ").strip()

    if opcion == "1":
        return "1_litro"
    elif opcion == "2":
        return "medio_litro"
    print("[Error] Opción no válida.")
    return None

def ejecutar_sistema():
    """
    Ejecuta el ciclo principal del menú interactivo para gestionar el inventario.
    """
    datos = cargar_datos()

    while True:
        print("\n--- SISTEMA DE INVENTARIO: MIEL DE ABEJA ---")
        print("1. Ver reporte financiero y alertas de stock")
        print("2. Registrar compra de miel a granel (Toneladas)")
        print("3. Envasar miel (Granel -> Botellas)")
        print("4. Registrar venta")
        print("5. Ver historial de movimientos en pantalla")
        print("6. Reiniciar todos los datos a cero")
        print("7. Salir")

        opcion = input("\nElige una opción (1-7): ").strip()

        try:
            if opcion == "1":
                mostrar_reporte_financiero(datos)

            elif opcion == "2":
                ton = float(input("¿Cuántas toneladas compraste? (Ej. 1): "))
                costo = float(input("¿Costo por tonelada en pesos? (Ej. 55000): "))
                if ton > 0 and costo >= 0:
                    registrar_compra_tonelada(datos, ton, costo)
                else:
                    print("[Error] Ingresa valores mayores a cero.")

            elif opcion == "3":
                clave = seleccionar_presentacion()
                if clave:
                    cant = int(input("¿Cuántas botellas vas a envasar?: "))
                    if cant > 0:
                        envasar_miel(datos, clave, cant)
                    else:
                        print("[Error] La cantidad debe ser mayor a cero.")

            elif opcion == "4":
                clave = seleccionar_presentacion()
                if clave:
                    cant = int(input("¿Cuántas botellas vendiste?: "))
                    if cant > 0:
                        registrar_venta(datos, clave, cant)
                    else:
                        print("[Error] La cantidad debe ser mayor a cero.")

            elif opcion == "5":
                mostrar_historial_pantalla()

