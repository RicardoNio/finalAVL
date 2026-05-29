from exceptions import DuplicateKeyError, KeyNotFoundError

class AVLNode:
    """Representa un nodo individual dentro de un árbol AVL.

    Attributes:
        key (int): Identificador principal utilizado para ordenar el árbol.
        value (Any): Carga útil de datos asociada a la clave (generalmente un objeto Record).
        left (AVLNode o None): Referencia al hijo izquierdo del nodo.
        right (AVLNode o None): Referencia al hijo derecho del nodo.
        height (int): Altura del nodo en el árbol, usada para calcular el factor de balanceo.
    """
    def __init__(self, key, value):
        """Inicializa un nuevo nodo para el árbol AVL.

        Args:
            key (int): Clave única que identificará al nodo.
            value (Any): Objeto o diccionario con la información del registro.
        """
        self.key = key          # El ID o Clave Principal
        self.value = value      # El objeto JSON (diccionario)
        self.left = None
        self.right = None
        self.height = 1         # Altura para el balanceo

class AVLTree:
    """Estructura de datos de Árbol Binario de Búsqueda Auto-balanceable (AVL).

    Proporciona operaciones de inserción, búsqueda y eliminación con un 
    rendimiento garantizado de O(log n) manteniendo el árbol estrictamente balanceado.
    """
    def get_height(self, node):
        """Obtiene la altura de un nodo específico.

        Args:
            node (AVLNode o None): El nodo a evaluar.

        Returns:
            int: La altura del nodo. Retorna 0 si el nodo es nulo (None).
        """
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        """Calcula el factor de balance de un nodo.

        El factor de balance es la diferencia entre la altura del subárbol 
        izquierdo y la altura del subárbol derecho.

        Args:
            node (AVLNode o None): El nodo a evaluar.

        Returns:
            int: El factor de balance. Un valor fuera del rango [-1, 1] 
                indica que el árbol necesita rebalanceo.
        """
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_right(self, y):
        """Realiza una rotación simple a la derecha sobre el nodo dado.

        Args:
            y (AVLNode): El nodo sobre el cual se realiza la rotación (raíz desbalanceada).

        Returns:
            AVLNode: La nueva raíz del subárbol después de la rotación.
        """
        x = y.left
        T2 = x.right
        # Rotación
        x.right = y
        y.left = T2
        # Actualizar alturas
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def rotate_left(self, x):
        """Realiza una rotación simple a la izquierda sobre el nodo dado.

        Args:
            x (AVLNode): El nodo sobre el cual se realiza la rotación (raíz desbalanceada).

        Returns:
            AVLNode: La nueva raíz del subárbol después de la rotación.
        """
        y = x.right
        T2 = y.left
        # Rotación
        y.left = x
        x.right = T2
        # Actualizar alturas
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, root, key, value):
        """Inserta un nuevo nodo en el árbol AVL y lo rebalancea si es necesario.

        Args:
            root (AVLNode o None): Nodo raíz actual del subárbol.
            key (int): Clave única a insertar.
            value (Any): Carga útil asociada a la clave.

        Returns:
            AVLNode: La nueva raíz del subárbol tras la inserción y posible rebalanceo.

        Raises:
            DuplicateKeyError: Si se intenta insertar una clave que ya existe en el árbol.
        """
        # 1. Inserción normal de BST
        if not root:
            return AVLNode(key, value)
        
        if key < root.key:
            root.left = self.insert(root.left, key, value)
        elif key > root.key:
            root.right = self.insert(root.right, key, value)
        else:
            # Si la clave ya existe, actualizamos el valor (Update)
            raise DuplicateKeyError(f"El ID {key} ya existe. No se permiten duplicados.")
            return root

        # 2. Actualizar altura del nodo ancestro
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # 3. Obtener factor de balance para ver si se desbalanceó
        balance = self.get_balance(root)

        # Caso Izquierda-Izquierda
        if balance > 1 and key < root.left.key:
            return self.rotate_right(root)

        # Caso Derecha-Derecha
        if balance < -1 and key > root.right.key:
            return self.rotate_left(root)

        # Caso Izquierda-Derecha
        if balance > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Caso Derecha-Izquierda
        if balance < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def search(self, root, key):
        """Busca un nodo en el árbol AVL usando su clave.

        Args:
            root (AVLNode o None): El nodo raíz desde donde empezar a buscar.
            key (int): La clave a buscar.

        Returns:
            AVLNode o None: El nodo encontrado, o None si la clave no existe en el árbol.
        """
        if not root or root.key == key:
            return root
        
        if key < root.key:
            return self.search(root.left, key)
        return self.search(root.right, key)

    def get_min_value_node(self, node):
        """Encuentra el nodo con el valor de clave más pequeño en un subárbol.

        Este nodo siempre se encontrará recorriendo el camino izquierdo hasta el final.

        Args:
            node (AVLNode): La raíz del subárbol donde se buscará el mínimo.

        Returns:
            AVLNode: El nodo con la clave mínima encontrada.
        """
        if node is None or node.left is None:
            return node
        return self.get_min_value_node(node.left)

    def delete(self, root, key):
        """Elimina un nodo del árbol AVL y asegura que se mantenga balanceado.

        Args:
            root (AVLNode o None): El nodo raíz del subárbol.
            key (int): La clave del nodo que se desea eliminar.

        Returns:
            AVLNode o None: La nueva raíz del subárbol tras el borrado y rebalanceo.

        Raises:
            KeyNotFoundError: Si el árbol es recorrido completamente sin encontrar la clave.
        """
        # 1. Eliminación estándar de BST
        if not root:
            raise KeyNotFoundError(f"El ID {key} no se encontró para eliminar.")

        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # Nodo con un solo hijo o sin hijos
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            # Nodo con dos hijos: obtener el sucesor (mínimo en el subárbol derecho)
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.value = temp.value
            root.right = self.delete(root.right, temp.key)

        if root is None:
            return root

        # 2. Actualizar altura
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # 3. Rebalancear
        balance = self.get_balance(root)

        # Caso Izquierda-Izquierda
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.rotate_right(root)

        # Caso Izquierda-Derecha
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Caso Derecha-Derecha
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.rotate_left(root)

        # Caso Derecha-Izquierda
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def inorder_list(self, root, result):
        """Devuelve una lista de todos los objetos (útil para guardar en JSON).

        Realiza un recorrido inorden (Izquierda -> Raíz -> Derecha) de manera recursiva,
        lo que garantiza que los elementos se almacenen de forma ordenada según su clave.

        Args:
            root (AVLNode o None): El nodo en evaluación durante la recursión.
            result (list): Lista que se irá poblando con los valores de los nodos.
        """
        if root:
            self.inorder_list(root.left, result)
            result.append(root.value)
            self.inorder_list(root.right, result)

    def get_structure_dict(self, root):
        """Retorna la estructura completa del árbol en un formato de diccionario jerárquico.
        
        Muy útil para que la interfaz gráfica sepa cómo dibujar las conexiones.
        Convierte recursivamente los nodos a una representación pura basada en 
        diccionarios anidados.

        Args:
            root (AVLNode o None): El nodo actual a convertir en diccionario.

        Returns:
            dict o None: Diccionario con la información estructural del nodo
                y sus hijos, o None si el nodo actual está vacío.
        """
        if not root:
            return None
        
        return {
            "key": root.key,
            "height": root.height,
            "balance": self.get_balance(root),
            "left": self.get_structure_dict(root.left),
            "right": self.get_structure_dict(root.right)
        }