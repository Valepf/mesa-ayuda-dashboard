# Mesa de Ayuda · Panel de tickets

Panel desarrollado por **Valeria García** con **Python, Streamlit y pandas** para visualizar solicitudes de soporte, prioridades y tiempos de atención. Admite datos de demostración, archivos CSV/Excel y lectura de Google Sheets mediante OAuth.

## Recorrido de un ticket

Un formulario en n8n recibe la consulta, un clasificador con IA identifica la categoría y el flujo registra el ticket en Google Sheets. Este panel consulta la planilla y permite analizar los resultados.

**Formulario → n8n + IA → Google Sheets → Panel Streamlit**

El flujo de automatización se mantiene en [ai-support-ticket-automation-n8n](https://github.com/Valepf/ai-support-ticket-automation-n8n). Este repositorio contiene el panel; no ejecuta el clasificador ni escribe en Sheets.

## Funcionalidades

- Demostración con 90 tickets ficticios, sin cuenta de Google.
- Filtros por fechas, estado, categoría, prioridad y canal; búsqueda por ID.
- Indicadores de pendientes, respuesta y resolución; gráficos y exportación CSV.
- Avisos de tickets pendientes de prioridad alta, urgente o crítica.
- Importación CSV y Excel (pestaña `Tickets`); validación de fechas, IDs y tiempos.
- Lectura privada de Google Sheets con permiso de solo lectura.
- Reconocimiento de las columnas en español utilizadas por el flujo n8n.

## Inicio rápido en Windows

Se necesita Python 3.11 o posterior. Descargá y extraé el repositorio en una carpeta.

1. Ejecutá `1_INSTALAR.bat` para crear `.venv` e instalar dependencias.
2. Ejecutá `3_ABRIR_PANEL.bat` para abrir el panel en modo **Demostración**.

No hace falta activar el entorno virtual. Dejá la terminal abierta mientras usás el panel.

### Conectar Google Sheets

Seguí [CONECTAR_GOOGLE_SHEETS.md](CONECTAR_GOOGLE_SHEETS.md). Copiá `config.example.json` como `config.local.json` y configurá tu planilla. Guardá las credenciales OAuth de escritorio como `credentials.json` junto a `app.py`, ejecutá `2_CONECTAR_GOOGLE.bat` y seleccioná **Google Sheets** en el panel.

### Inicio desde terminal

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

En Linux/macOS usá `python3 -m venv .venv` y `.venv/bin/python`.

## Formatos de entrada

El CSV estándar usa `ticket_id`, `created_at`, `category`, `priority`, `status`, `first_response_hours`, `resolution_hours` y `channel`.

El formato n8n usa `Fecha`, `Categoria`, `Estado` y `Prioridad`. Se admiten columnas adicionales, pero `Nombre` y `Mensaje` no se muestran ni exportan desde el panel. Si falta `ticket_id`, se generan IDs provisionales por fila: cambian al reordenar la fuente.

Los tiempos ausentes se muestran sin dato y se excluyen del promedio. No se calculan tiempos reales si el flujo no los registra. Las fechas con zona horaria se convierten a hora argentina. Los IDs duplicados se rechazan.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m unittest discover -p "test_*.py"
```

Incluye pruebas de normalización y configuración. El modo demo no requiere credenciales. La autenticación real requiere una cuenta autorizada del usuario.

## Privacidad y alcance

El repositorio incluye únicamente datos ficticios. `.gitignore` excluye credenciales, tokens, configuración privada y entornos virtuales. No subas tickets reales ni archivos de sesión.

El inicio de sesión OAuth está pensado para ejecutar el panel en la computadora del usuario. Publicar el código en GitHub no aloja una aplicación web: un despliegue multiusuario requiere adaptar la autenticación y el control de acceso.
