"""Validación compartida por el panel y futuras importaciones de n8n."""
import pandas as pd

COLUMNS = ['ticket_id', 'created_at', 'category', 'priority', 'status',
           'first_response_hours', 'resolution_hours', 'channel']

def normalize(data):
    data = data.copy()
    data.columns = data.columns.str.strip().str.lower()
    notices = []
    if {'fecha', 'categoria', 'estado', 'prioridad'}.issubset(data.columns):
        data = data.rename(columns={'fecha':'created_at','categoria':'category','estado':'status','prioridad':'priority'})
        if 'ticket_id' not in data:
            data['ticket_id'] = [f'FILA-{i+2}' for i in range(len(data))]
            notices.append('IDs provisionales según fila de origen. Pueden cambiar al ordenar o borrar filas en Sheets.')
        for field in ['first_response_hours','resolution_hours']:
            if field not in data: data[field] = float('nan')
        if 'channel' not in data: data['channel'] = 'Formulario'
        notices.append('Formato n8n detectado. Los tiempos no registrados aparecen sin dato. Nombre y Mensaje no se incluyen en el panel.')
    missing = set(COLUMNS) - set(data.columns)
    if missing:
        raise ValueError('Faltan columnas: ' + ', '.join(sorted(missing)))
    warnings = notices
    data = data[COLUMNS].copy()
    data['ticket_id'] = data.ticket_id.fillna('').astype(str).str.strip()
    def parse_date(value):
        try:
            stamp = pd.Timestamp(value)
            if pd.isna(stamp): return pd.NaT
            if stamp.tzinfo is not None:
                stamp = stamp.tz_convert('America/Argentina/Buenos_Aires').tz_localize(None)
            return stamp
        except (ValueError, TypeError, OverflowError):
            return pd.NaT
    data['created_at'] = pd.to_datetime(data.created_at.map(parse_date), errors='coerce')
    for col in ['category', 'priority', 'status', 'channel']:
        data[col] = data[col].fillna('').astype(str).str.strip().replace('', 'Sin especificar')
    for col in ['priority','status']:
        data[col] = data[col].str.capitalize()
    for col in ['first_response_hours','resolution_hours']:
        original = data[col]
        numeric = pd.to_numeric(original, errors='coerce')
        bad = ((original.notna() & original.astype(str).str.strip().ne('') & numeric.isna()) | numeric.lt(0))
        if bad.any(): warnings.append(f'{int(bad.sum())} valores inválidos en {col}; se muestran sin dato.')
        data[col] = numeric.mask(numeric.lt(0))
    invalid = data.created_at.isna() | data.ticket_id.eq('')
    if invalid.any(): warnings.append(f'{int(invalid.sum())} filas omitidas por fecha o ID inválidos.')
    data = data.loc[~invalid].copy()
    duplicates = data.ticket_id.duplicated(keep='first')
    if duplicates.any():
        raise ValueError('Hay IDs de ticket repetidos. Cada ticket debe tener un ID único.')
    return data, warnings

def date_bounds(selection):
    if isinstance(selection, (tuple,list)):
        return (selection[0], selection[-1]) if selection else (None,None)
    return selection, selection
