from datetime import date, datetime

def to_date_iso(v):
    if not v:
        return None
    if isinstance(v, datetime):
        return v.date().isoformat()
    if isinstance(v, date):
        return v.isoformat()
    if isinstance(v, str):
        # Por si tu driver devuelve 'YYYY-MM-DD'
        try:
            return date.fromisoformat(v).isoformat()
        except ValueError:
            return v  # o None, según prefieras
    return None