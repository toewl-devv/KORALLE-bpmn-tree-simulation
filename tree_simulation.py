'''
This file contains the main simulation code. Using a Tree object, it will run
through the objects the same way one would run through a BPMN diagram.
The simulation will use the times provided in the BPMN file to make the simulation more realistic.
Times will also be slightly randomised to account for IRL random error. '''

import bpmn_parser
import bpmn_tree_structure
import os
from time import sleep
from collections import deque
import numpy as np

class Simulation:
    def __init__(self, fileName, timescale:float=1):
        bpmn_xml = bpmn_parser.BPMNfile(fileName)
        process_tree = bpmn_xml.get_tree_structure()
        self.tree = process_tree
        self.timescale = timescale
    
    def print_timestep(self, timestep: int):
        simulated_tree = self.tree
        current_running_nodes = [simulated_tree.root]
        time_steps = 0
        end = simulated_tree.get_node("endnode")
        while current_running_nodes != [end]:
            for node in current_running_nodes:
                if node == end:
                    pass
                elif node.time_left <= 0:
                    current_running_nodes.remove(node)
                    for child in node.children:
                        current_running_nodes.append(child)
                else:
                    node.time_left -= 1
            if time_steps == timestep:
                print("Timestep:", time_steps)
                simulated_tree.print_tree_highlight_nodes(current_running_nodes)
                break
            time_steps += 1




    def reset_time_lefts(self):
        for node in self.tree.get_nodes():
            # Randomise the time given according to mean and variance given
            randomised_time = np.random.normal(node.time_needed, np.sqrt(node.time_variance))
            node.time_left = np.rint(randomised_time)



    def get_total_time(self):
        current_running_nodes = [self.tree.root]
        time_steps = 0
        end = self.tree.get_node("endnode")
        while current_running_nodes != [end]:
            for node in current_running_nodes:
                if node == end:
                    pass
                elif node.time_left <= 0:
                    current_running_nodes.remove(node)
                    for child in node.children:
                        current_running_nodes.append(child)
                else:
                    node.time_left -= 1
            time_steps += 1

        return time_steps


    def simulate(self):
        self.reset_time_lefts()
        if self.timescale <= 0:
            raise ValueError("timescale must be a positive number")

        simulated_tree = self.tree
        current_running_nodes = [simulated_tree.root]
        time_steps = 0
        end = simulated_tree.get_node("endnode")
        while current_running_nodes != [end]:
            for node in current_running_nodes:
                if node == end:
                    pass
                elif node.time_left <= 0:
                    current_running_nodes.remove(node)
                    for child in node.children:
                        current_running_nodes.append(child)
                else:
                    node.time_left -= 1

            # clear screen then print the stuff :D
            clear()
            print("Timestep:", time_steps)
            simulated_tree.print_tree_highlight_nodes(current_running_nodes)
            time_steps += 1
            sleep(1.0 / self.timescale)

def clear():
    print("\033[2J\033[H", end="")

