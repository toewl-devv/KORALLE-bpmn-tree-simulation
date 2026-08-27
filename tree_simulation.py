'''
This file contains the main simulation code. Using a Tree object, it will run
through the objects the same way one would run through a BPMN diagram.
The simulation will use the times provided in the BPMN file to make the simulation more realistic.
Times will also be slightly randomised to account for IRL random error. '''

from time import sleep
from copy import deepcopy
import numpy as np
import random

import bpmn_parser
import makecolors as mc

def clear():
    print("\033[2J\033[H", end="")

class Simulation:
    def __init__(self, file_name, timescale:float=1):
        if timescale <= 0:
            raise ValueError("timescale must be positive")
        bpmn_xml = bpmn_parser.BpmnFile(file_name)
        process_tree = bpmn_xml.get_tree_structure()
        self.tree = process_tree
        self.timescale = timescale

    def step(self, current_running_nodes, ends, simulated_trees):
        finished_nodes = [[] for _ in current_running_nodes]

        # Count how many processes are currently on each node
        occupied = {}

        for process in current_running_nodes:
            for running_node in process:
                occupied[running_node.id] = occupied.get(running_node.id, 0) + 1

        for i, process in enumerate(current_running_nodes):
            for node in process:
                if node == ends[i][0]:
                    pass

                elif node.time_left <= 0:
                    # Check whether every child has available capacity
                    if random.random() < node.failure_chance:
                        node.time_left = node.time_needed
                        self.tree.get_node(node.id).failures += 1
                    else:
                        if all(
                            occupied.get(child.id, 0) < child.max_capacity
                            for child in node.children
                        ):
                            finished_nodes[i].append(node)

                            # Reserve one slot on every child
                            for child in node.children:
                                occupied[child.id] = occupied.get(child.id, 0) + 1
                        else:
                            simulated_trees[i].time_spent_waiting += 1

                else:
                    node.time_left -= 1

            for node in finished_nodes[i]:
                process.remove(node)
                process.extend(node.children)


    def print_timestep(self, timestep: int, n=1, t=0.0):
        if not (0 < timestep < self.get_total_time()):
            raise ValueError("timestep out of range")
        simulated_trees = [deepcopy(self.tree) for _ in range(n)]

        for tree in simulated_trees:
            tree.reset_time_lefts(randomise=False)
        current_running_nodes = [[tree.root] for tree in simulated_trees]

        # Make each one start t later:
        for i, nodes in enumerate(current_running_nodes):
            nodes[0].time_left += t*i
        
        # Start simulation
        time_steps = 0
        ends = [[tree.get_node("endnode")] for tree in simulated_trees]
        while current_running_nodes != ends:
            if time_steps == timestep:
                # print the tree w many processes
                print("Time step:", time_steps)
                self.tree.print_tree_processes(current_running_nodes, n)
                break
            self.step(current_running_nodes, ends, simulated_trees)
            time_steps += 1

    def get_total_time(self, n=1, t=0.0):
        simulated_trees = [deepcopy(self.tree) for _ in range(n)]
        for tree in simulated_trees:
            tree.reset_time_lefts(randomise=False)
        current_running_nodes = [[tree.root] for tree in simulated_trees]

        # Make each one start t later:
        for i, nodes in enumerate(current_running_nodes):
            nodes[0].time_left += t*i
        
        # Start simulation
        time_steps = 0
        ends = [[tree.get_node("endnode")] for tree in simulated_trees]
        while current_running_nodes != ends:
            self.step(current_running_nodes, ends, simulated_trees)
            time_steps += 1

        return time_steps

    def simulate(self, n=1, t=0.0):
        simulated_trees = [deepcopy(self.tree) for _ in range(n)]
        for tree in simulated_trees:
            tree.reset_time_lefts()
        current_running_nodes = [[tree.root] for tree in simulated_trees]

        # Make each one start t later:
        for i, nodes in enumerate(current_running_nodes):
            nodes[0].time_left += t*i
        
        # Start simulation
        time_steps = 0
        ends = [[tree.get_node("endnode")] for tree in simulated_trees]
        while True:
            # print the tree w many processes
            clear()
            print("Time step:", time_steps)
            self.tree.print_tree_processes(current_running_nodes, n)
            
            if current_running_nodes == ends:
                break

            self.step(current_running_nodes, ends, simulated_trees)
            time_steps += 1

            sleep(1.0 / self.timescale)
        
        # simulation ended

        sleep(2)
        clear()

        # print simulation report

        tree_lines, report_lines = self.print_tree_report()
        tree_width = max(len(line) for line in tree_lines) + 4
        
        for line, fails in zip(tree_lines, report_lines):
            print(line + " "*(tree_width-len(line)) + f"{fails}")

        print("\nTimesteps spent waiting:")
        for process, tree in enumerate(simulated_trees):
            print(mc.highlight_process(f"{process + 1}: {tree.time_spent_waiting}", process))

        input("press <enter> to quit")

    def print_tree_report(self, node=None, level=0, prefix="├──"):
        if node is None:
            node = self.tree.root

        output_lines = []
        report_lines = []

        indent = "│ " * level
        output_lines.append(f"{indent}{prefix}{node.name}")
        report_lines.append(f"{node.failures}")

        for i, child in enumerate(node.children):
            is_last = i == len(node.children) - 1
            child_prefix = "└──" if is_last else "├──"

            child_output, child_report = self.print_tree_report(
                child, level + 1, child_prefix
            )

            output_lines.extend(child_output)
            report_lines.extend(child_report)

        return output_lines, report_lines


