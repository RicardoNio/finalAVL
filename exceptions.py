class DatabaseError(Exception):
    """Clase base para excepciones del gestor de base de datos."""
    pass

class DuplicateKeyError(DatabaseError):
    """Se lanza cuando se intenta insertar un ID que ya existe."""
    pass

class KeyNotFoundError(DatabaseError):
    """Se lanza cuando no se encuentra un ID para eliminar o buscar."""
    pass

class DatabaseCorruptionError(DatabaseError):
    """Se lanza cuando el archivo JSON tiene un formato inválido."""
    pass

class ValidationError(DatabaseError):
    """Se lanza cuando los datos no cumplen con el esquema (ej. falta el ID)."""
    pass