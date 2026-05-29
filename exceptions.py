class DatabaseError(Exception):
    """Clase base para excepciones del gestor de base de datos.

    Esta excepción hereda de la clase `Exception` nativa de Python y 
    sirve como jerarquía raíz. Permite a los desarrolladores capturar 
    cualquier error genérico de la base de datos con un solo bloque `except`.
    """
    # La instrucción 'pass' indica que la clase no requiere lógica ni atributos 
    # adicionales más allá de la funcionalidad base heredada de Exception.
    pass

class DuplicateKeyError(DatabaseError):
    """Se lanza cuando se intenta insertar un ID que ya existe.

    Hereda de `DatabaseError`. Es útil para prevenir la sobrescritura 
    accidental de registros, garantizando la integridad de claves únicas
    dentro de la estructura de datos subyacente.
    """
    # Se utiliza 'pass' porque el comportamiento y la recepción del mensaje 
    # de error por defecto provistos por la clase base son suficientes.
    pass

class KeyNotFoundError(DatabaseError):
    """Se lanza cuando no se encuentra un ID para eliminar o buscar.

    Hereda de `DatabaseError`. Se dispara principalmente durante operaciones 
    de lectura, actualización o borrado cuando el identificador solicitado 
    no está registrado en el sistema.
    """
    # No se requiere implementación adicional, permitiendo que la clase actúe
    # únicamente como una etiqueta semántica de error.
    pass

class DatabaseCorruptionError(DatabaseError):
    """Se lanza cuando el archivo JSON tiene un formato inválido.

    Hereda de `DatabaseError`. Advierte que el archivo físico de 
    almacenamiento está vacío, corrupto o ha sido alterado externamente, 
    impidiendo su deserialización correcta.
    """
    # Se usa 'pass' para evitar errores de sintaxis en Python al definir 
    # una clase que no añade métodos ni variables nuevas.
    pass

class ValidationError(DatabaseError):
    """Se lanza cuando los datos no cumplen con el esquema (ej. falta el ID).

    Hereda de `DatabaseError`. Actúa como una barrera de seguridad previa 
    a las operaciones de escritura, verificando que los diccionarios o 
    datos de entrada posean la estructura requerida.
    """
    # Mantiene la simplicidad de la clase, delegando la gestión y el 
    # almacenamiento del mensaje de error a la clase padre (Exception).
    pass