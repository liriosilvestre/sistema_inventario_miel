# 🍯 Sistema de Control de Inventario y Finanzas: Miel de Abeja

Aplicación interactiva desarrollada en **Python** para gestionar el ciclo completo de comercialización de miel de abeja: desde la adquisición de materia prima a granel, pasando por el envasado en presentaciones comerciales, hasta el control de ventas, cálculo de rentabilidad y emisión de alertas preventivas.

---

## 🎯 Características Principales

* **Gestión de Materia Prima:** Convierte automáticamente las compras por tonelada (1,000 kg) a litros disponibles (aprox. **704 litros** por tonelada, considerando una densidad promedio de 1.42 kg/L).
* **Control de Envasado y Stock:** Descuenta miel a granel y actualiza el inventario de botellas listas para la venta en dos presentaciones:
  * **Envase de 1 Litro:** Precio de venta **$250.00 MXN** (costo estimado de envase/etiqueta: $10.00 MXN).
  * **Envase de 1/2 Litro:** Precio de venta **$140.00 MXN** (costo estimado de envase/etiqueta: $6.00 MXN).
* **Cálculo de Ganancia Neta:** Registra la inversión en materia prima e insumos para calcular en tiempo real la utilidad real (`Ingresos - Inversión`).
* **Alertas de Stock Mínimo:** Notifica automáticamente en consola cuando la miel a granel baja de **100 litros** o cuando quedan menos de **20 botellas** de alguna presentación.
* **Persistencia Dual (JSON y CSV):**
  * `inventario_miel.json`: Respalda el estado actual del inventario y finanzas.
  * `historial_movimientos.csv`: Genera una bitácora cronológica con fecha y hora, lista para abrirse en **Microsoft Excel** o **Power BI**.

---

## 🛠️ Arquitectura y Buenas Prácticas

El código fue estructurado siguiendo estándares de desarrollo limpio y mantenible:
* **Modularización (`def`):** Lógica dividida en funciones independientes y reutilizables.
* **Separación de Responsabilidades:** Cada función cumple una única tarea (persistencia, alertas, cálculo operativo o interfaz de consola).
* **Documentación Interna (`docstrings`):** Cada función incluye su descripción detallada de propósito y comportamiento.
* **Validación de Entradas:** Uso de bloques `try-except` para evitar interrupciones ante datos inválidos del usuario.

---

## 🚀 Cómo Ejecutar el Proyecto

1. Asegúrate de tener instalado **Python 3.8** o superior.
2. Descarga o clona este repositorio en tu equipo:
   ```bash
   git clone https://github.com
   ```
3. Entra a la carpeta del proyecto y ejecuta el archivo principal:
   ```bash
   python sistema_inventario_miel.py
   ```
4. Navega por el menú interactivo ingresando el número de la opción deseada (`1` a `7`).

---

## 📊 Ejemplo de Flujo Operativo

1. **Compra inicial:** Registro de 1 tonelada a $55,000.00 MXN (+704.0 L disponibles).
2. **Envasado:** Llenado de 300 botellas de 1 L y 400 botellas de 1/2 L.
3. **Ventas:** Registro de salidas de producto y activación automática de alertas de reabastecimiento.
4. **Reporte Financiero:** Visualización de ingresos totales, costos acumulados y ganancia neta.
