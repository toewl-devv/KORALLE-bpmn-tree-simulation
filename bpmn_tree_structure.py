'''
    This file contains the TreeNode and Tree classes. These classes give
    functionality to our tree structure, including standard tree functions
    and other functions which will aid in simulation. E.g. get_children_at_depth()
'''

from collections import Counter
import numpy as np

import makecolors as mc

class TreeNode():
    def __init__(self, 
                 task_name,
                 task_id,
                 task_type, 
                 task_time_needed, 
                 task_time_variance, 
                 task_max_capacity
                 ):
        self.name: str = task_name
        self.id: str = task_id
        self.type: str = task_type
        self.time_needed: float = task_time_needed
        self.children: list[TreeNode] = []
        self.parent: TreeNode | None = None
        self.time_left = self.time_needed
        self.time_variance = task_time_variance
        self.max_capacity = task_max_capacity

    def add_child(self, child_node):
        if child_node is None:
            raise ValueError("Child cannot be None")
        child_node.parent = self
        self.children.append(child_node)

    def remove_child(self, child_node):
        if child_node not in self.children:
            raise ValueError("the given child is not a child of this node")

        self.children.remove(child_node)
        child_node.parent = None

    def is_leaf(self):
        return len(self.children) == 0

    def is_root(self):
        return self.parent is None

    def get_depth(self):
        if self.parent is None:
            return 0
        return self.parent.get_depth() + 1


class Tree:
    def __init__(self, root_node):
        self.root: TreeNode = root_node
        self.time_spent_waiting = 0

    def reset_time_lefts(self, randomise=True):
        for node in self.get_nodes():
            # Randomise the time given according to mean and variance given,
            # and ensure it isn't negative
            if randomise:
                node.time_left = np.rint(
                        max(0, 
                            np.random.normal(node.time_needed, np.sqrt(node.time_variance))
                            )
                        )
            else:
                node.time_left = node.time_needed 
 
    def get_root(self):
        return self.root

    def get_size(self):
        return self._count_nodes(self.root)

    def _count_nodes(self, node):
        if node is None:
            return 0
        count = 1
        for child in node.children:
            count += self._count_nodes(child)
        return count

    def get_height(self):
        return self._get_height(self.root)

    def _get_height(self, node):
        if node is None:
            return -1
        if node.is_leaf():
            return 0

        max_child_height = 0
        for child in node.children:
            child_height = self._get_height(child)
            max_child_height = max(max_child_height, child_height)
        return max_child_height + 1

    def get_node(self, node_id):
        return self._get_node(self.root, node_id)

    def _get_node(self, node, node_id):
        if node is None:
            return None
        if node.id == node_id:
            return node
        for child in node.children:
            results = self._get_node(child, node_id)
            if results:
                return results
        return None

    def get_nodes(self):
        nodes = []
        self._get_nodes(self.root, nodes)
        return nodes

    def _get_nodes(self, node, nodes):
        if node is None:
            return

        nodes.append(node)
        for child in node.children:
            self._get_nodes(child, nodes)

    def print_tree(self, node=None, level=0, prefix="├──"):
        if node is None:
            node = self.root

        indent = "│ "*level
        print(f'{indent}{prefix}{node.name}')
        for i, child in enumerate(node.children):
            is_last = i == len(node.children) - 1
            child_prefix = "└──" if is_last else "├──"
            self.print_tree(child, level+1, child_prefix)

    def print_tree_highlight_nodes(self, current_nodes, node=None, level=0, prefix="`--"):
        if node is None:
            node = self.root

        indent = "| " * level

        if node in current_nodes:
            print(f'{indent}{prefix}{mc.highlight(f" {node.name} ")} ')
        else:
            print(f'{indent}{prefix}{mc.non_highlight(f" {node.name} ")} ')

        for i, child in enumerate(node.children):
            is_last = i == len(node.children) - 1
            child_prefix = "`--" if is_last else "|--"
            self.print_tree_highlight_nodes(current_nodes, child, level + 1, child_prefix)

    def print_tree_processes(
        self, current_running_nodes, n, node=None, level=0, prefix="`--",
        process_counts=None
    ):
        if node is None:
            node = self.root

        # processes is the list of process numbers (indices) which are running
        # the node we are printing
        processes = [
            i
            for i, process in enumerate(current_running_nodes)
            if any(running_node.id == node.id for running_node in process)
        ]

        # colour in the stars depending which process is running
        stars = "".join(mc.highlight_process("*", process) for process in processes)

        # the indent to the whole tree is enough space to show all processes (length n)
        process_area = stars + " " * (n-len(processes))
        indent = "| " * level

        # print ther line and call the next line(s) to print
        print(f"{process_area}{indent}{prefix} {node.name}")

        for i, child in enumerate(node.children):
            is_last = i == len(node.children) - 1
            child_prefix = "`--" if is_last else "|--"

            self.print_tree_processes(
                current_running_nodes,
                n,
                child,
                level + 1,
                child_prefix,
                process_counts
            )
