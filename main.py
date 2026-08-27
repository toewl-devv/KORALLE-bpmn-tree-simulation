import simulation

file_name = "complexdiagram.bpmn"

simulation = simulation.Simulation(file_name, n=6, t=1.0, timescale=10)
input("Press <enter> to start simulation")
simulation.simulate(visualise=True)
print(simulation.results.node_times_spent_waiting)
