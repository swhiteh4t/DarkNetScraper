from collections import deque

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = deque()

class QueueTree:
    def __init__(self, root_value):
        self.root = TreeNode(root_value)

    def add_child(self, parent_value, child_value):
        parent_node = self.find_node(parent_value, self.root)
        if parent_node:
            child_node = TreeNode(child_value)
            parent_node.children.append(child_node)
        else:
            print(f"Parent node with value {parent_value} not found.")

    def find_node(self, value, current_node):
        if current_node is None:
            return None
        if current_node.value == value:
            return current_node
        for child in current_node.children:
            result = self.find_node(value, child)
            if result:
                return result
        return None

    def print_tree(self):
        self._print_tree(self.root, 0)

    def _print_tree(self, current_node, level):
        if current_node is not None:
            print("  " * level + str(current_node.value))
            for child in current_node.children:
                self._print_tree(child, level + 1)

# Example usage:
if __name__ == "__main__":
    tree = QueueTree("Root")
    tree.add_child("Root", "Child1")
    tree.add_child("Root", "Child2")
    tree.add_child("Child1", "Grandchild1")
    tree.add_child("Child1", "Grandchild2")
    tree.add_child("Child2", "Grandchild3")
    tree.add_child("Child2", "Grandchild4")

    tree.print_tree()
