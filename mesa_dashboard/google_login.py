"""Autorización local de Google Sheets, con permiso de solo lectura."""
from pathlib import Path
import json

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def load_credentials(base_dir):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    path = base_dir / 'token.json'
    if not path.exists():
        raise ValueError('Primero ejecutá: python google_login.py')
    try:
        creds = Credentials.from_authorized_user_file(str(path), SCOPES)
        if not creds.valid and creds.refresh_token:
            creds.refresh(Request())
            path.write_text(creds.to_json(), encoding='utf-8')
        if not creds.valid:
            raise ValueError()
        return creds
    except Exception:
        raise ValueError('La sesión de Google venció o no es válida. Ejecutá: python google_login.py') from None


def main():
    from google_auth_oauthlib.flow import InstalledAppFlow
    base = Path(__file__).resolve().parent
    path = base / 'credentials.json'
    if not path.exists():
        raise ValueError('Guardá credentials.json junto a app.py y volvé a intentarlo.')
    info = json.loads(path.read_text(encoding='utf-8-sig'))
    if 'installed' not in info:
        raise ValueError('El JSON debe ser de un cliente OAuth de tipo Aplicación de escritorio.')
    flow = InstalledAppFlow.from_client_config(info, SCOPES)
    creds = flow.run_local_server(
        host='localhost', port=0, timeout_seconds=180, prompt='consent',
        authorization_prompt_message='Abrí este enlace si el navegador no se abre: {url}',
        success_message='Conexión autorizada. Podés cerrar esta pestaña y volver a la terminal.',
    )
    (base / 'token.json').write_text(creds.to_json(), encoding='utf-8')
    print('Listo. Ahora ejecutá: python -m streamlit run app.py')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Inicio de sesión cancelado. Podés volver a intentarlo.')
    except Exception as error:
        if isinstance(error, ValueError):
            print(str(error))
        else:
            print('No se completó el inicio de sesión. Revisá el mensaje del navegador y volvé a ejecutar python google_login.py.')
        raise SystemExit(1)
