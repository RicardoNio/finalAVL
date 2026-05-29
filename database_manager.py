from avl_tree import AVLTree
from models import Record
import persistence
from exceptions import (
    ValidationError, 
    DuplicateKeyError, 
    KeyNotFoundError, 
    DatabaseCorruptionError
)

class DatabaseManager:
    """Gestor principal de la base de datos basada en un árbol AVL y persistencia en JSON.

    Esta clase maneja la carga, escritura, actualización, búsqueda y eliminación
    de registros, manteniendo la estructura en memoria sincronizada con un archivo físico.

    Attributes:
        tree (AVLTree): Instancia del árbol AVL utilizado para organizar los datos.
        root (Node o None): Nodo raíz del árbol AVL en memoria.
        file_path (str): Ruta del archivo JSON utilizado para la persistencia.
    """
    def __init__(self, file_path):
        """Inicializa el gestor de la base de datos.

        Configura las estructuras de datos iniciales y arranca el proceso de carga 
        para construir el árbol AVL desde el archivo de almacenamiento.

        Args:
            file_path (str): Ruta al archivo JSON donde se almacenan los datos.
        """
        self.tree = AVLTree()
        self.root = None
        self.file_path = file_path
        # Al iniciar, cargamos los datos y construimos el árbol
        self._load_initial_data()

    def _load_initial_data(self):
        """Lee el JSON y reconstruye el árbol AVL en memoria con validaciones de integridad.

        Carga los registros en bruto utilizando el módulo de persistencia, valida su 
        formato de manera estricta y los inserta secuencialmente en el árbol AVL.

        Raises:
            DatabaseCorruptionError: Si un elemento en el JSON no es un diccionario, 
                si carece de la clave 'id', o si ocurre un fallo al leer los datos base.
        """
        try:
            raw_data = persistence.load_all(self.file_path)
            for item in raw_data:
                # Validar que cada elemento sea un objeto/diccionario
                if not isinstance(item, dict):
                    raise DatabaseCorruptionError(
                        "El archivo JSON contiene elementos con un formato de objeto inválido."
                    )
                
                # Validar que exista la clave primaria obligatoria
                if 'id' not in item or item['id'] is None:
                    raise DatabaseCorruptionError(
                        "Se encontró un registro en el archivo sin la clave obligatoria 'id'."
                    )
                
                # Convertimos el diccionario a nuestra estructura Record
                # Hacemos una copia para no alterar el diccionario original al usar pop()
                item_copy = item.copy()
                record = Record.from_dict(item_copy)
                
                # Construimos el árbol AVL
                self.root = self.tree.insert(self.root, record.id, record)
                
            print(f"Sincronización inicial completada con éxito. {len(raw_data)} registros cargados.")
            
        except DatabaseCorruptionError as e:
            # Re-lanzamos para que main.py pueda decidir cómo actuar
            raise e
        except Exception as e:
            raise DatabaseCorruptionError(
                f"No se pudo inicializar la base de datos debido a un error de lectura: {e}"
            )

    def _sync_to_disk(self):
        """Extrae de manera ordenada los objetos del árbol y los vuelca en el archivo.

        Utiliza un recorrido inorden del árbol AVL para obtener todos los registros 
        ordenados numéricamente por su ID, los convierte a diccionarios estándar y 
        sobrescribe el archivo JSON físico.
        """
        all_records = []
        # Obtenemos todos los objetos Record ordenados mediante recorrido Inorden
        self.tree.inorder_list(self.root, all_records)
        
        # Convertimos los objetos Record de vuelta a diccionarios estándar
        json_ready_data = [record.to_dict() for record in all_records]
        persistence.save_all(self.file_path, json_ready_data)

    def save_record(self, obj):
        """Inserta un nuevo registro en la base de datos.
        
        Lanza DuplicateKeyError si el ID ya existe. Efectúa comprobaciones de tipo 
        y de existencia estructural antes de incluir el nuevo registro en el árbol AVL 
        y luego sincroniza con el disco.

        Args:
            obj (dict): Diccionario que contiene la información del nuevo registro.

        Raises:
            ValidationError: Si 'obj' no es un diccionario, si no posee un 'id', o 
                si el 'id' no es un número entero.
            DuplicateKeyError: Lanza desde la lógica de inserción si el ID ya existe.
        """
        if not isinstance(obj, dict):
            raise ValidationError("Los datos del registro deben representarse como un diccionario.")

        if 'id' not in obj or obj['id'] is None:
            raise ValidationError("Error de Integridad: El registro debe contener un atributo 'id'.")
        
        if not isinstance(obj['id'], int):
            raise ValidationError("Error de Tipo: El 'id' debe ser un número entero.")

        # Copiamos para proteger los datos originales de efectos colaterales
        obj_copy = obj.copy()
        record = Record.from_dict(obj_copy)

        # La inserción lanzará DuplicateKeyError desde avl_tree.py si ya existe
        self.root = self.tree.insert(self.root, record.id, record)
        self._sync_to_disk()

    def update_record(self, obj):
        """Modifica un registro existente.
        
        Lanza KeyNotFoundError si el ID no existe. Busca el nodo en el árbol, 
        reemplaza sus atributos con el nuevo objeto provisto y actualiza el disco.

        Args:
            obj (dict): Diccionario con los datos a actualizar. Debe contener un 'id'.

        Raises:
            ValidationError: Si el diccionario no contiene la clave 'id'.
            KeyNotFoundError: Si el 'id' no se logra encontrar dentro del árbol.
        """
        if 'id' not in obj or obj['id'] is None:
            raise ValidationError("Error de Integridad: Se requiere un 'id' para actualizar el registro.")
        
        key = obj['id']
        node = self.tree.search(self.root, key)
        
        if not node:
            raise KeyNotFoundError(f"Error de Actualización: El ID {key} no existe en la base de datos.")
        
        # Reemplazamos el valor anterior por el nuevo objeto Record
        obj_copy = obj.copy()
        node.value = Record.from_dict(obj_copy)
        self._sync_to_disk()

    def find_by_id(self, key):
        """Búsqueda eficiente O(log n) que retorna un diccionario clásico.

        Navega rápidamente a través del árbol AVL apoyándose en el identificador entero.

        Args:
            key (int): El ID principal del registro objetivo.

        Returns:
            dict: El registro hallado convertido a un formato estándar de diccionario.

        Raises:
            ValidationError: Si el valor de 'key' no es de tipo numérico (entero).
            KeyNotFoundError: Si la búsqueda no obtiene un resultado para el ID dado.
        """
        if not isinstance(key, int):
            raise ValidationError("El ID de búsqueda debe ser un entero.")
            
        node = self.tree.search(self.root, key)
        if not node:
            raise KeyNotFoundError(f"Búsqueda fallida: El ID {key} no está registrado.")
            
        return node.value.to_dict()

    def find_by_criteria(self, field, value):
        """Búsqueda lineal O(n) que filtra coincidencias basadas en un campo y su valor.
        
        Es insensible a mayúsculas/minúsculas para strings. Itera en orden sobre todos 
        los registros disponibles verificando la existencia del campo y emparejando el valor.

        Args:
            field (str): Nombre del atributo o campo a evaluar.
            value (Any): Valor específico buscado. Se convierte a string para la comparación.

        Returns:
            list[dict]: Lista que contiene todos los registros (diccionarios) 
                que cumplen con el criterio dado.
        """
        all_records = []
        self.tree.inorder_list(self.root, all_records)
        
        results = []
        for record in all_records:
            record_dict = record.to_dict()
            if field in record_dict:
                # Comparamos convirtiendo a texto plano en minúsculas para mayor flexibilidad
                curr_val = str(record_dict[field]).strip().lower()
                target_val = str(value).strip().lower()
                if curr_val == target_val:
                    results.append(record_dict)
        return results

    def delete_record(self, key):
        """Elimina un nodo usando la clave primaria y actualiza el archivo JSON.

        Ejecuta el borrado balanceado dentro del árbol AVL y procede a la 
        sincronización final con el archivo de persistencia en disco.

        Args:
            key (int): ID correspondiente al registro que desea eliminarse.

        Raises:
            ValidationError: Si la clave especificada no es un número entero.
        """
        if not isinstance(key, int):
            raise ValidationError("El ID para eliminación debe ser un número entero.")

        # delete() de avl_tree.py lanzará KeyNotFoundError si la clave no existe
        self.root = self.tree.delete(self.root, key)
        self._sync_to_disk()

    def get_all_sorted(self):
        """Devuelve todos los elementos ordenados ascendentemente según su clave.

        Recorre la integridad del árbol inorden y formatea los resultados a una 
        estructura de datos primitiva en Python.

        Returns:
            list[dict]: Una lista que contiene todos los diccionarios almacenados 
                en la base de datos, estructurados en orden numérico por su ID.
        """
        all_records = []
        self.tree.inorder_list(self.root, all_records)
        return [record.to_dict() for record in all_records]