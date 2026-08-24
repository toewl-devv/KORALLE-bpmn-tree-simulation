'''
This file contains the main simulation code. Using a Tree object, it will run
through the objects the same way one would run through a BPMN diagram.
The simulation will use the times provided in the BPMN file to make the simulation more realistic.
Times will also be slightly randomised to account for IRL random error. '''

from time import sleep
import numpy as np

import bpmn_parser

class Simulation:
    def __init__(self, fileName, timescale:float=1):
        if timescale <= 0:
            raise ValueError("timecale must be positive")
        bpmn_xml = bpmn_parser.BPMNfile(fileName)
        process_tree = bpmn_xml.get_tree_structure()
        self.tree = process_tree
        self.timescale = timescale

    def reset_time_lefts(self, randomise=True):
        for node in self.tree.get_nodes():
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
   
    def step(self, current_running_nodes, end):
        finished_nodes = []
        for node in current_running_nodes:
            if node == end:
                pass
            elif node.time_left <= 0:
                finished_nodes.append(node)
            else:
                node.time_left -= 1

        for node in finished_nodes:
            current_running_nodes.remove(node)
            current_running_nodes.extend(node.children)

    def print_timestep(self, timestep: int):
        self.reset_time_lefts()
        simulated_tree = self.tree
        current_running_nodes = [simulated_tree.root]
        time_steps = 0
        end = simulated_tree.get_node("endnode")
        while current_running_nodes != [end]:
            self.step(current_running_nodes, end)
            if time_steps == timestep:
                print("Timestep:", time_steps)
                simulated_tree.print_tree_highlight_nodes(current_running_nodes)
                break
            time_steps += 1

    def get_total_time(self):
        self.reset_time_lefts(randomise=False)
        current_running_nodes = [self.tree.root]
        time_steps = 0
        end = self.tree.get_node("endnode")
        while current_running_nodes != [end]:
            self.step(current_running_nodes, end)
            time_steps += 1

        return time_steps


    def simulate(self):
        self.reset_time_lefts()
        simulated_tree = self.tree
        current_running_nodes = [simulated_tree.root]
        time_steps = 0
        end = simulated_tree.get_node("endnode")
        while current_running_nodes != [end]:
            self.step(current_running_nodes, end)
            # clear screen then print the tree
            clear()
            print("Timestep:", time_steps)
            simulated_tree.print_tree_highlight_nodes(current_running_nodes)
            time_steps += 1
            sleep(1.0 / self.timescale)

def clear():
    print("\033[2J\033[H", end="")

