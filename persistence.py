import json
import os
from exceptions import DatabaseCorruptionError

def ensure_data_directory(file_path):
    """Asegura que la carpeta donde se guardará el archivo exista.

    Si el directorio intermedio en la ruta provista no existe, se crea
    de manera recursiva.

    Args:
        file_path (str): Ruta completa del archivo que se planea escribir.

    Returns:
        None
    """
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def save_all(file_path, data_list):
    """Guarda una lista de diccionarios en un archivo JSON de forma segura.

    Si los directorios del destino no existen, intenta crearlos. En caso de 
    error durante el guardado, este se captura y se reporta en consola.

    Args:
        file_path (str): Ruta de destino para el archivo JSON.
        data_list (list[dict]): Lista de diccionarios que se van a serializar.
            Comúnmente proviene del método `inorder_list` de un árbol AVL.

    Returns:
        bool: True si el archivo fue guardado con éxito, False en caso contrario.
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
    """Lee el archivo JSON provisto y devuelve una lista de diccionarios.

    Verifica la existencia del archivo antes de proceder a su lectura. Si el 
    archivo posee errores de formato JSON, se lanza una excepción de corrupción.

    Args:
        file_path (str): Ruta del archivo JSON que se desea leer.

    Returns:
        list[dict]: Lista de diccionarios leída del archivo JSON. Retorna una 
            lista vacía si el archivo no existe o si ocurre un error inesperado.

    Raises:
        DatabaseCorruptionError: Si el archivo existe pero su contenido no puede 
            ser decodificado como un JSON válido.
    """
    # Valida la existencia física del archivo para prevenir errores de lectura (FileNotFoundError)
    if not os.path.exists(file_path):
        # Retorna una estructura vacía si no hay registros previos, asumiendo un estado inicial limpio
        return []
    
    try:
        # Abre el archivo en modo de solo lectura, usando UTF-8 para garantizar soporte de caracteres especiales
        with open(file_path, 'r', encoding='utf-8') as f:
            # Deserializa la cadena de texto con formato JSON de vuelta a objetos nativos de Python
            return json.load(f)
    except json.JSONDecodeError:
        # Si el archivo está vacío o corrupto
        # Lanza una excepción personalizada detallando el fallo estructural del JSON
        raise DatabaseCorruptionError(f"El archivo {file_path} tiene un formato inválido.")
    except Exception as e:
        # Captura errores imprevistos (por ejemplo: falta de permisos de lectura del sistema operativo)
        print(f"Error al cargar los datos: {e}")
        # Retorna una lista vacía de manera controlada para que la ejecución del programa no se interrumpa
        return []