import tree_simulation

file_name = "complexdiagram.bpmn"

simulation = tree_simulation.Simulation(file_name, timescale=10)
input("Press <enter> to start simulation")
print("\033[2J\033[H", end="") #clear the screen
simulation.simulate(n=6, t=3)
