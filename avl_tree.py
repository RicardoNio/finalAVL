from exceptions import DuplicateKeyError, KeyNotFoundError
class AVLNode:
    def __init__(self, key, value):
        self.key = key          # El ID o Clave Principal
        self.value = value      # El objeto JSON (diccionario)
        self.left = None
        self.right = None
        self.height = 1         # Altura para el balanceo

class AVLTree:
    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_right(self, y):
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
        if not root or root.key == key:
            return root
        
        if key < root.key:
            return self.search(root.left, key)
        return self.search(root.right, key)

    def get_min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self.get_min_value_node(node.left)

    def delete(self, root, key):
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
        """Devuelve una lista de todos los objetos (útil para guardar en JSON)"""
        if root:
            self.inorder_list(root.left, result)
            result.append(root.value)
            self.inorder_list(root.right, result)

    def get_structure_dict(self, root):
        """
        Retorna la estructura completa del árbol en un formato de diccionario jerárquico.
        Muy útil para que la interfaz gráfica sepa cómo dibujar las conexiones.
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