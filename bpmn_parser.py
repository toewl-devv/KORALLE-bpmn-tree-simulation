'''
    This file contains the methods needed to parse the BPMN file and
    turn it into a tree using bpmn_tree_structure.py.
    The methods will check that a clean BPMN file is given, and if the
    file is not clean, an error will be given.
'''

import xml.etree.ElementTree as ET
from pathlib import Path

import bpmn_tree_structure as ts

def check_values(child_time, child_variance, child_capacity, child_failchance):
    if child_time < 0:
        raise ValueError(f"task time must be non-negative ({child_time} given)")
    if child_variance < 0:
        raise ValueError(f"task time variance must be non-negative ({child_variance} given)")
    if child_capacity <= 0:
        raise ValueError(f"task capacity must non-zero positive ({child_capacity} given)")
    if not (0 <= child_failchance <= 1):
        raise ValueError(f"task failure chance out of range [0,1] ({child_failchance} given)")

def check_file(file_name):
    path = Path(file_name)

    if path.suffix != ".bpmn":
        raise ValueError("file must end with .bpmn")

    if not path.is_file():
        raise ValueError("file not found")

class BpmnFile:
    def __init__(self, file_name):
        # raise an error if the file is invalid
        check_file(file_name)
        
        # tree is a ElementTree object which makes it easy to read the xml file
        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse(file_name, parser=parser)
        
        if tree is None:
            raise Exception("no tree found in bpmn file")
        # root <==> <definitions/> for a BPMN file
        root = tree.getroot()
        if root.tag.startswith("{"):
            namespace = root.tag[root.tag.find("{") + 1 : root.tag.find("}")]
        else:
            raise Exception("no namespace found in BPMN file")

        ns = {"bpmn" : namespace}
        process = root.find("bpmn:process", ns)

        if process is None:
            raise Exception("no process element found in bpmn")
        
        self.process = process
        self.tree = tree
        self.root = root


    def get_tree_structure(self):
        process_nodes = []

        for child in self.process:
            if child.tag.endswith("sequenceFlow"):
                continue

            # Only tasks have names. If the "name" attribute exists,
            # split it via ";". Otherwise, use the child.tag.
            temp_name = child.get("name")

            if temp_name:
                try:
                    child_name, time, variance, capacity, failchance = temp_name.split(";")
                    child_time = float(time)
                    child_variance = float(variance)
                    child_capacity = int(capacity)
                    child_failchance = float(failchance)

                except ValueError:
                    raise ValueError(
                        f'Invalid task format: "{temp_name}". Expected "name;time;variance;capacity,failchance"'
                    )
            else:
                child_name = child.tag.split("}")[-1]
                child_time = 1.0
                child_variance = 0.0
                child_capacity = 1
                child_failchance = 0.0

            # check for value errors
            check_values(child_time, child_variance, child_capacity, child_failchance)

            child_id = child.get("id") or ""

            process_nodes.append(
                    ts.TreeNode(child_name,
                                child_id,
                                child.tag, 
                                child_time, 
                                child_variance, 
                                child_capacity,
                                child_failchance
                    )
            )

        nodes_by_id = {node.id: node for node in process_nodes}

        for child in self.process:
            if not child.tag.endswith("sequenceFlow"):
                continue

            flow_parent = nodes_by_id.get(child.get("sourceRef"))
            flow_child = nodes_by_id.get(child.get("targetRef"))

            if flow_parent is None or flow_child is None:
                raise Exception("sequenceFlow references an unknown node")

            flow_parent.add_child(flow_child)

        # Find the BPMN root
        roots = [node for node in process_nodes if node.is_root()]

        if len(roots) == 0:
            raise Exception("no root was found in the BPMN file")

        if len(roots) > 1:
            raise Exception("more than one root was found in the BPMN file")

        bpmn_tree = ts.Tree(roots[0])

        # Find the unique deepest node
        max_depth = bpmn_tree.get_height()

        deepest_nodes = [
            node for node in process_nodes
            if node.get_depth() == max_depth
        ]

        if len(deepest_nodes) != 1:
            raise ValueError("more than one node exists at maximum depth")

        last_node = deepest_nodes[0]

        # Add artificial start and end nodes
        # Recall this in the form name, id, type, time, variance, capacity
        start = ts.TreeNode("start", "startnode", "start", 0.0, 0.0, 9999, 0.0)
        end = ts.TreeNode("end", "endnode", "end", 0.0, 0.0, 9999, 0.0)

        start.add_child(bpmn_tree.root)
        last_node.add_child(end)

        return ts.Tree(start)
