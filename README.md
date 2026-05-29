# Proyecto-Final-CS1 Gestor de Bases de Datos No Relacional con Indexación AVL


Este proyecto consiste en un prototipo funcional de un Gestor de Bases de Datos No Relacionales (documental) desarrollado en Python. Permite almacenar, consultar, actualizar y eliminar objetos en formato JSON de manera persistente en disco.

Para optimizar el rendimiento de las operaciones de búsqueda por clave primaria, se implementó desde cero un **Árbol AVL** (árbol binario de búsqueda auto-balanceado) que mantiene un índice en memoria.

---

## 🚀 Características del Proyecto

- **Estructura Documental (No Relacional):** Los registros se manipulan como diccionarios flexibles de atributos bajo un formato compatible con JSON.
- **Indexación Eficiente ($O(\log n)$):** Inserciones, búsquedas por clave primaria y eliminaciones optimizadas gracias al balanceo estricto del Árbol AVL.
- **Persistencia Síncrona:** El estado de la base de datos se mantiene en disco en archivos `.json` planos, actualizándose de manera consistente tras cada operación de escritura.
- **Robustez y Seguridad:** Jerarquía de excepciones personalizadas para capturar y mitigar fallos como claves duplicadas, registros inexistentes o corrupción del archivo físico.
- **Arquitectura desacoplada:** Separación clara entre la estructura de datos, la lógica del negocio (el gestor), los modelos y la interfaz de usuario.

---

## Estructura del Proyecto

```text
DB_Manager/
│
├── app.py                  # GUI
├── database_manager.py     # Orquestador del sistema (conecta el árbol y los archivos)
├── avl_tree.py             # Algoritmo de balanceo y rotaciones del Árbol AVL
├── models.py               # Definición del Record y el nodo AVLNode
├── persistence.py          # Serialización y lectura de datos JSON en disco
├── exceptions.py           # Jerarquía de errores del sistema
├── .gitignore              # Configuración para evitar subir caché y datos locales
├── README.md               # Documentación general del proyecto
└── data/                   # Carpeta que aloja el archivo físico de datos
    └── database.json       # Base de datos en texto plano

```

## Requisitos e Instalación
### Prerequisitos 
-Python 3.8 o superior
-flask
-flask-cors
```bash
pip install -r requirements.txt
```

### Configuración inicial

- 1. Clonar el repositorio
- 2. Abra una terminal en la raiz del proyecto
- 3. Cree el directorio para datos fisicos

``` bash
mkdir data
```

## Instrucciones de uso
Para iniciar ejecute
```bash
python app.py
```
### Flujo de Operaciones soportadas
1. Crear registro: Permite ingresar un ID entero único y agregar atributos (nombre, categoría, precio).
2. Modificar registro: Si el ID existe, permite modificar los atributos en memoria y actualiza el archivo JSON.
3. Buscar por ID: Recupera los datos en tiempo logarítmico utilizando el índice AVL.
4. Buscar por criterio: Realiza un escaneo lineal (O(n)) en los atributos no indexados (por ejemplo, buscar por categoría).
5. Eliminar registro: Remueve el nodo del árbol, balancea la estructura si es necesario y sincroniza el cambio en el archivo de texto.
## Estructura de Datos (AVL)

Para este gestor se seleccionó el Árbol AVL como estructura de indexación debido a su estricto criterio de balanceo (la diferencia de alturas entre subárboles nunca es mayor a 1).

### Complejidad Algoritmica Comparativa:

|Operación   |   Busqueda por ID  |  Búsqueda por Criterios|
| Insersión  |    O(log(n))       |    -           
| Búsqueda   |    O(log(n))       |     O(n)
| Eliminación|    O(log(n))       |    -

A diferencia de un árbol binario de búsqueda estándar, el AVL evita el peor de los casos O(n)que ocurre cuando las inserciones se realizan en orden secuencial, previniendo que el árbol se degenere en una lista enlazada.

## Colaboradores
[Tomás Palomá Suárez 20251020163]
[Estiven Ricardo Niño Niño 20251020176]
