"""Consulta privada sin escrituras, sin compartir ni publicar la planilla."""
import pandas as pd
import json
import os

def sheet_settings(base_dir):
    path = base_dir / 'config.local.json'
    config = json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else {}
    sheet_id = os.getenv('GOOGLE_SHEET_ID') or config.get('spreadsheet_id', '')
    tab = os.getenv('GOOGLE_SHEET_TAB') or config.get('worksheet', 'Tickets')
    if not isinstance(sheet_id, str) or not sheet_id.strip() or sheet_id == 'TU_ID_DE_PLANILLA':
        raise ValueError('Configurá spreadsheet_id en config.local.json. Ver CONECTAR_GOOGLE_SHEETS.md.')
    if not isinstance(tab, str) or not tab.strip():
        raise ValueError('Configurá worksheet con el nombre de la pestaña.')
    return sheet_id.strip(), tab.strip()

def read_sheet(base_dir):
    sheet_id, tab = sheet_settings(base_dir)
    try:
        import gspread
        from google_login import load_credentials
        client = gspread.authorize(load_credentials(base_dir))
        client.set_timeout(20)
        rows = client.open_by_key(sheet_id).worksheet(tab).get_all_values()
    except ImportError:
        raise ValueError('Instalá las dependencias actualizadas de requirements.txt.') from None
    except ValueError:
        raise
    except Exception:
        raise ValueError('No se pudo leer Google Sheets. Revisá la conexión, la API de Google Sheets y que la cuenta elegida pueda abrir la planilla Tickets Soporte IA.') from None
    if not rows:
        raise ValueError('La pestaña Tickets está vacía; necesita encabezados.')
    headers = rows[0]
    if len(headers) != len(set(headers)):
        raise ValueError('La hoja tiene encabezados repetidos.')
    return pd.DataFrame(rows[1:], columns=headers)
