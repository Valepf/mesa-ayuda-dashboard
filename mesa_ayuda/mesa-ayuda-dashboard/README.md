# Panel de seguimiento de tickets

Aplicación de portfolio hecha con **Python, Streamlit y pandas**. Permite explorar métricas de una mesa de ayuda usando datos ficticios o un CSV propio.

## Qué muestra

- Total de tickets, pendientes, resueltos y porcentaje de resolución.
- Promedio de horas hasta la primera respuesta y hasta la resolución.
- Actividad diaria, categorías y estados.
- Filtros por período, estado y categoría.
- Descarga de los resultados filtrados en CSV.

## Ejecutar en Windows

1. Instalá Python 3.10 o superior.
2. Abrí una terminal dentro de esta carpeta.
3. Creá y activá un entorno virtual:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

4. Instalá las dependencias y ejecutá la app:

   ```powershell
   py -m pip install -r requirements.txt
   py -m streamlit run app.py
   ```

Streamlit abrirá el panel en el navegador. Para detenerlo, presioná `Ctrl+C` en la terminal.

## CSV para conectar datos

Desde la barra lateral se puede cargar otro CSV. Debe tener estos encabezados:

| Columna | Descripción | Ejemplo |
|---|---|---|
| `ticket_id` | Identificador único | `TK-1042` |
| `created_at` | Fecha y hora de creación | `2026-10-10 09:30:00` |
| `category` | Tipo de consulta | `Acceso` |
| `priority` | Prioridad asignada | `Alta` |
| `status` | Estado actual | `Pendiente`, `En proceso`, `Resuelto` |
| `first_response_hours` | Horas hasta la primera respuesta | `1.5` |
| `resolution_hours` | Horas hasta la resolución; vacío si sigue abierto | `4.0` |
| `channel` | Canal de ingreso | `Formulario` |

La app arranca con `data/tickets_demo.csv`, que contiene registros inventados. Para integrarlo con el sistema de n8n, se puede mapear la salida del flujo a estas columnas y exportarla como CSV. No incluyas datos personales o reales en una versión pública del portfolio.

## Idea para presentarlo en el portfolio

> Construí un dashboard interactivo para analizar tickets de soporte. Procesa archivos CSV, filtra por período, estado y categoría, calcula indicadores de atención y permite exportar los resultados. El proyecto demuestra Python, análisis de datos e integración potencial con un flujo de automatización en n8n.
