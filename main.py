import simulation
file_name = "complexdiagram.bpmn"

simulation = simulation.Simulation(file_name, n=6, t=1.0, timescale=10)
simulation.simulate(visualise=True)
