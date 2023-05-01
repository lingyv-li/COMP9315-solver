from typing import Optional
import treelib

class Node:
    def __init__(self, parent: Optional['Node'], keys, pages, is_leaf=True):
        self.parent = parent
        self.keys: list = keys
        self.pages: list = pages
        self.is_leaf = is_leaf

    def is_full(self):
        return len(self.keys) == C

    def visualize(self, parent_id, description: str, tree: treelib.Tree):
        id = str(parent_id)+description
        tree.create_node(description, id, parent_id)  # create root node
        if self.is_leaf:
            for i, key in enumerate(self.keys):
                tree.create_node(str(key), str(key), parent=id)
        else:
            for i, key in enumerate(self.keys):
                if i == 0:
                    child_description = f" "
                else:
                    child_description = f"{self.keys[i-1]}"
                self.pages[i].visualize(id, child_description, tree)
            self.pages[-1].visualize(id, f"{self.keys[-1]}", tree)


class Tree:
    def __init__(self, root: Node):
        self.root = root

    def visualize(self):
        viz_tree = treelib.Tree()
        self.root.visualize(None, "root", viz_tree)
        viz_tree.show(sorting=False)

    def find(self, k):
        return self.search(k, self.root)

    def search(self, k, node):
        if (node.is_leaf):
            return node
        keys = node.keys
        pages = node.pages
        if (k <= keys[0]):
            return self.search(k, pages[0])
        for i in range(len(keys)-1):
            if (keys[i] < k <= keys[i+1]):
                return self.search(k, pages[i+1])
        if (k > keys[-1]):
            return self.search(k, pages[-1])

    def range(self, Lo, Hi):
        node = self.search(Lo, self.root)
        pages = []
        while node and node.keys[-1] < Hi:
            for i, key in enumerate(node.keys):
                if Lo <= key <= Hi:
                    pages.append(node.pages[i])
            node = node.pages[-1] if node.pages else None
        return pages

    def insert(self, k):
        leaf_node = self.find(k)
        is_full = leaf_node.is_full()
        leaf_node.keys.append(k)
        leaf_node.keys.sort()
        if is_full:
            self.split_and_promote(leaf_node)
            leaf_node = self.find(k)

    def split_and_promote(self, node):
        middle_index = len(node.keys) // 2
        middle_key = node.keys[middle_index]
        left_node = Node(parent=node.parent, keys=node.keys[:middle_index], pages=node.pages[:middle_index+1], is_leaf=node.is_leaf)
        right_node = Node(parent=node.parent, keys=node.keys[middle_index+1:], pages=node.pages[middle_index+1:], is_leaf=node.is_leaf)
        if node.parent is None:
            new_parent = Node(parent=None, keys=[middle_key], pages=[left_node, right_node], is_leaf=False)
            self.root = new_parent
            left_node.parent = new_parent
            right_node.parent = new_parent
        else:
            node_index = node.parent.pages.index(node)
            node.parent.keys.insert(node_index, middle_key)
            node.parent.pages[node_index] = left_node
            node.parent.pages.insert(node_index+1, right_node)
            left_node.parent = node.parent
            right_node.parent = node.parent
            if node.parent.is_full():
                self.split_and_promote(node.parent)

if __name__ == '__main__':
    C = 4  # max number of keys per node

    # Example from exercise 5
    tree = Tree(Node(parent=None, keys=[], pages=[], is_leaf=True))
    for val in [100, 50, 80, 200, 20, 65, 150, 110, 75, 10, 180]:
        tree.insert(val)
        tree.visualize()
