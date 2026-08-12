'''
    This file is here to run the entire process. The pipeline is:
        +-----------------+
        |   BPMN file     |
        |      |          |
        |      V          |
        | Tree structure  |
        |      |          |
        |      V          | 
        |   Simulation    |
        +-----------------+
    The final simulation is displayed here.
'''

import bpmn_tree_structure
import bpmn_parser
import tree_simulation
import os

file_name = input("File name: ")

simulation = tree_simulation.Simulation(file_name, timescale=3)
input("Press <enter> to start simulation")
os.system('clear')
simulation.simulate()
