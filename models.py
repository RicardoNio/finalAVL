class Record:
    """
    Representa un objeto dentro de nuestra base de datos.
    Esto ayuda a validar que todos los objetos tengan al menos un ID.
    """
    def __init__(self, id, data=None):
        self.id = id
        # 'attributes' guardará el resto de la información (nombre, precio, etc.)
        self.attributes = data if data else {}

    def to_dict(self):
        """Convierte el objeto a un diccionario para guardarlo en JSON."""
        # Unimos el ID con el resto de atributos en un solo diccionario
        return {"id": self.id, **self.attributes}

    @staticmethod
    def from_dict(data_dict):
        """Crea una instancia de Record a partir de un diccionario (cargado de JSON)."""
        record_id = data_dict.pop("id")
        return Record(record_id, data_dict)

    def __repr__(self):
        return f"Record(id={self.id}, data={self.attributes})"


