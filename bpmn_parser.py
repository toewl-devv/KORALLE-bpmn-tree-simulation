'''
    This file contains the methods needed to parse the BPMN file and
    turn it into a tree using bpmn_tree_structure.py.
    The methods will check that a clean BPMN file is given, and if the
    file is not clean, an error will be given.
'''

from pathlib import Path
import bpmn_tree_structure as ts
import xml.etree.ElementTree as ET


def check_file(fileName):
    if not fileName.endswith(".bpmn"):
        raise ValueError("file must end with .bpmn")
    if not Path(fileName).is_file():
        raise ValueError("file not found")

class BPMNfile:
    def __init__(self, fileName):
        # raise an error if the file is invalid
        check_file(fileName)
        
        # tree is a ElementTree object which makes it easy to read the xml file
        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse(fileName, parser=parser)
        
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
            
            # only tasks have names. If the "name" attribute exists, split it via ";".
            # Otherwise, use the child.tag, e.g. "exclusiveGateway".
            temp_name = child.get("name")
            if temp_name:
                try:
                    child_name, time = temp_name.split(";")
                    child_time = float(time)
                except ValueError:
                    raise ValueError(f'invalid task format: "{temp_name}". Excpected "name;time"')
            else:
                child_name = child.tag
                child_time = 1.0

            child_id = child.get("id") or ""

            process_nodes.append(ts.TreeNode(child_name, child_id, child.tag, child_time))

        nodes_by_id = {node.id: node for node in process_nodes}
        for child in self.process:
            if not child.tag.endswith("sequenceFlow"):
                continue
            
            flow_parent = nodes_by_id[child.get("sourceRef")]
            flow_child = nodes_by_id[child.get("targetRef")]

            if flow_parent is None or flow_child is None:
                raise Exception("sequenceFlow references an unkown node")

            flow_parent.add_child(flow_child)

        roots = [node for node in process_nodes if node.is_root()]
        
        if len(roots) == 0:
            raise Exception("no root was found in the BPMN file")
        if len(roots) > 1:
            raise Exception("more than one root was found in the bpmn file")

        bpmn_tree = ts.Tree(roots[0])

        return bpmn_tree
  
