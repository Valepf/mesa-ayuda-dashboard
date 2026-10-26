# Conectar Google Sheets

1. En tu proyecto de Google Cloud, habilitá la API de Google Sheets y configurá Google Auth Platform. Para una app externa en pruebas, agregá tu correo como usuario de prueba.
2. Creá un cliente OAuth de tipo **Aplicación de escritorio** y descargá el JSON al crearlo. Guardalo como `credentials.json` junto a `app.py` (sin repetir `.json`).
3. Copiá `config.example.json` como `config.local.json`. Reemplazá `TU_ID_DE_PLANILLA` por el ID de tu hoja: la parte entre `/d/` y `/edit` en su enlace. Configurá `worksheet` con el nombre exacto de la pestaña, por ejemplo `Tickets`.
4. Ejecutá `1_INSTALAR.bat` y luego `2_CONECTAR_GOOGLE.bat`. Elegí una cuenta con acceso a la hoja. La autorización solicita solo lectura de Sheets y guarda `token.json` localmente.
5. Ejecutá `3_ABRIR_PANEL.bat`, elegí Google Sheets y pulsá Actualizar.

También se admiten las variables de entorno `GOOGLE_SHEET_ID` y `GOOGLE_SHEET_TAB`, que prevalecen sobre el archivo local.

## Problemas frecuentes

- Falta credentials.json: comprobá su nombre exacto y ubicación junto a app.py.
- Falta token.json o sesión vencida: ejecutá de nuevo 2_CONECTAR_GOOGLE.bat.
- Acceso bloqueado durante el inicio de sesión: comprobá el correo en Usuarios de prueba.
- No se puede leer la hoja: verificá API habilitada, cuenta autorizada, ID y pestaña.
- n8n lee pero no guarda: revisá por separado su credencial con permisos de escritura, acceso de Editor, protecciones y almacenamiento disponible en la cuenta propietaria. El panel solo lee; su autorización no configura n8n.

No publiques credentials.json, token.json ni config.local.json. Este procedimiento es para uso local, no para un servidor compartido.
