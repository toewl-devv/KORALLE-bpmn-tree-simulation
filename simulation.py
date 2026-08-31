from time import sleep
from copy import deepcopy
import numpy as np
import random

import bpmn_parser
import makecolors as mc

def clear():
    print("\033[2J\033[H", end="")

class Simulation():
    def __init__(self, file_name, n=1, t=0.0, timescale=1.0):
        if timescale <= 0:
            raise ValueError("timescale must be positive")
        if n < 1:
            raise ValueError("n must be >= 1")
        if t < 0.0:
            raise ValueError("t must be >= 0.0f")
        
        bpmn_xml = bpmn_parser.BpmnFile(file_name)
        process_tree = bpmn_xml.get_tree_structure()

        self.tree = process_tree
        self.timescale = timescale
        self.processes = n
        self.stagger = t
        self.results = self.Results(self.tree)

    class Results():
        def __init__(self, tree):
            self.failures = {node.id: 0 for node in tree.get_nodes()}
            self.time_steps_taken = 0
            self.node_times_spent_waiting = {node.id: 0 for node in tree.get_nodes()}
            self.event_log = []

    def _step_simulation(self, current_running_nodes, simulated_trees, ends, time=None):
        finished_nodes = [[] for _ in current_running_nodes]

        # Count how many processes are currently on each node
        occupied = {}

        for process in current_running_nodes:
            for running_node in process:
                occupied[running_node.id] = occupied.get(running_node.id, 0) + 1

        for i, (process, tree, end, finished) in enumerate(zip(current_running_nodes, 
                                                simulated_trees, 
                                                ends, 
                                                finished_nodes)):
            for node in process:
                if node == end[0]:
                    pass
                elif node.time_left <= 0:
                    # does it fail at the end?
                    if random.random() < node.failure_chance:
                        node.time_left = node.time_needed
                        self.results.failures[node.id] += 1
                        self.results.event_log.append(
                                {"time": time, "process": i, "node": node.name, "event": "failure"}
                                )
                    else:
                        if all(
                                occupied.get(child.id, 0) < child.max_capacity
                                for child in node.children
                                ):
                            finished.append(node)
                            if time:
                                self.results.event_log.append(
                                        {"time": time, "process": i, "node": node.name, "event": "end"}
                                        )

                            # reserve one slot on every child
                            for child in node.children:
                                occupied[child.id] = occupied.get(child.id, 0) + 1
                        else:
                            tree.time_spent_waiting += 1
                            self.results.node_times_spent_waiting[node.id] += 1
                else:
                    node.time_left -= 1
            for node in finished:
                process.remove(node)
                process.extend(node.children)
                for child in node.children:
                    self.results.event_log.append(
                            {"time": time, "process": i, "node": child.name, "event": "start"}
                            )

    def simulate(self, visualise=False):
        simulated_trees = [deepcopy(self.tree) for _ in range(self.processes)]

        for tree in simulated_trees:
            tree.reset_time_lefts() # randomise for each tree
        
        current_running_nodes = [[tree.root] for tree in simulated_trees]

        # make each process start self.stagger timesteps later
        for i, nodes in enumerate(current_running_nodes):
            nodes[0].time_left += self.stagger*i

        # start simulating!
        time_step = 0
        ends = [[tree.get_node("endnode")] for tree in simulated_trees]
        while True:
            if visualise:
                # print the tree with many processes
                clear()
                print("Time step:", time_step)
                self.tree.print_tree_processes(current_running_nodes, self.processes)
                sleep(1.0 / self.timescale)

            if current_running_nodes == ends:
                break

            self._step_simulation(current_running_nodes, simulated_trees, ends, time=time_step+1)
            time_step += 1

        # the loop is broken when all processes have reached the end
        self.results.time_steps_taken = time_step

