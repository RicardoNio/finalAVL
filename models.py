class Record:
    """Representa un objeto dentro de nuestra base de datos.
    
    Esto ayuda a validar que todos los objetos tengan al menos un ID.

    Attributes:
        id (int o str): El identificador único asignado al registro.
        attributes (dict): Diccionario que contiene la carga útil o atributos 
            adicionales del registro.
    """
    def __init__(self, id, data=None):
        """Inicializa una nueva instancia de la clase Record.

        Args:
            id (int o str): Identificador único que representará este registro.
            data (dict, opcional): Diccionario con los datos del registro. 
                Por defecto es None.
        """
        # Asigna el identificador único proporcionado a la instancia
        self.id = id
        
        # 'attributes' guardará el resto de la información (nombre, precio, etc.)
        # Si 'data' es None, se asigna un diccionario vacío para prevenir errores futuros de tipo TypeError
        self.attributes = data if data else {}

    def to_dict(self):
        """Convierte el objeto a un diccionario para guardarlo en JSON.

        Returns:
            dict: Un diccionario plano que incluye la clave 'id' junto con
                todos los atributos adicionales desempaquetados.
        """
        # Unimos el ID con el resto de atributos en un solo diccionario
        # Se utiliza el operador (**) para desempaquetar el contenido de self.attributes
        return {"id": self.id, **self.attributes}

    @staticmethod
    def from_dict(data_dict):
        """Crea una instancia de Record a partir de un diccionario (cargado de JSON).

        Args:
            data_dict (dict): Diccionario deserializado desde un archivo JSON. 
                Debe contener obligatoriamente la clave 'id'.

        Returns:
            Record: Una nueva instancia de esta misma clase con los datos reconstruidos.
        """
        # pop('id') extrae y elimina la clave 'id' de data_dict, aislando este valor
        record_id = data_dict.pop("id")
        
        # El diccionario restante (sin el ID) se pasa como el argumento 'data' para los atributos
        return Record(record_id, data_dict)

    def __repr__(self):
        """Genera una representación formal del objeto en formato de texto.

        Returns:
            str: Cadena representativa que facilita la lectura durante la depuración,
                mostrando el estado actual de las propiedades del objeto.
        """
        # Devuelve un string formateado (f-string) útil para imprimir directamente el objeto en consola
        return f"Record(id={self.id}, data={self.attributes})"