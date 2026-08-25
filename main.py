import tree_simulation

file_name = input("File name: ")

simulation = tree_simulation.Simulation(file_name, timescale=5)
input("Press <enter> to start simulation")
print("\033[2J\033[H", end="") #clear the screen
simulation.simulate(n=6, t=3)
