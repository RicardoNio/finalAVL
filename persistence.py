import json
import os
from exceptions import DatabaseCorruptionError

def ensure_data_directory(file_path):
    """Asegura que la carpeta donde se guardará el archivo exista."""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def save_all(file_path, data_list):
    """
    Guarda una lista de diccionarios en un archivo JSON.
    data_list: Viene del método inorder_list del árbol AVL.
    """
    try:
        ensure_data_directory(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            # indent=4 para que el archivo sea legible por humanos
            json.dump(data_list, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar los datos: {e}")
        return False

def load_all(file_path):
    """
    Lee el archivo JSON y devuelve una lista de diccionarios.
    Si el archivo no existe, devuelve una lista vacía.
    """
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Si el archivo está vacío o corrupto
        raise DatabaseCorruptionError(f"El archivo {file_path} tiene un formato inválido.")
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return []