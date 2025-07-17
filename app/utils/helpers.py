# utils.py
from typing import List, Dict

def query_to_dict_list(cursor) -> list[dict]:
    """
    Convierte los resultados de un cursor en una lista de diccionarios.
    Las claves del diccionario son los nombres de las columnas en minúscula.
    Limpia los espacios en blanco de los valores string.
    """
    columns = [col[0].lower() for col in cursor.description]
    results = []

    for row in cursor.fetchall():
        row_dict = {}
        for col_name, value in zip(columns, row):
            if isinstance(value, str):
                row_dict[col_name] = value.strip()
            else:
                row_dict[col_name] = value
        results.append(row_dict)

    return results
