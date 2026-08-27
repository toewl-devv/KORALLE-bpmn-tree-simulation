# BPMN Process Simulation
This repository is for simulating the process within a BPMN (Business Process Model and Notation) diagram.
A simple example is found below to get you started, or read further to understand more.

## Example usage
```python
# main.py (example)
#
# first we need to import the necessary files:
import tree_simulation

# then we can simply make Simulation object:
simulation = tree_simulation.Simulation("complexdiagram.bpmn", timescale=3)
simulation.simulate()
```

## BPMN Diagram Constraints:
* Each node must belong to exactly **one** layer.
* There must be exactly **one** root node and **one** node for which it's depth is equal to the height of the diagram.
* A node may not have more than one parent.
* The text inside of a task must be in the form `name;t;var;capacity;failchance` where:
    * `t` $\geq 0$ is the time in seconds which the task will run for in the simulation, 
    * `var` $\geq 0$ is the variance of the time taken (set to 0 for exact given time), 
    * `capacity` $> 0$ is the maximum number of processes which may run the same task at once, and
    * `failchance` $\in [0,1]$ is the probability that the task fails causing it to restart immediately.
  
* Should the time be too long for a simulation, you can instead input the time in minutes, or hours etc. for the sake of the simulation.

## Detailed Usage
First we must import the tree simulation library:
```py
import tree_simulation as ts
```
To create a simulation, we create an instance of the Simulation class:
```py
my_simulation = ts.Simulation("complexdiagram.bpmn")
```
We can optionally give a value for the time scale (default 1):
```py
my_simulation = ts.Simulation("complexdiagram.bpmn", timescale=3)
```
In this case, the simulation will run three times faster than usual when we start it.

Now we can use other commands.
## Features of `Simulation`
##### `simulate(n=1, t=0.0)`
Runs the entire simulation for the given BPMN file. The current timestep is displayed at the top and currently active tasks are marked with an asterisk *.

`n` specifies the number of processes to run (default 1) and `t` specifies the time which the simulation should wait between starting consecutive processes (default 0).

At the end of the simulation, a report of how the simulation went is shown.
> TODO: make the report more insightful

> [!NOTE]
> A simulation ran with the exact same input values may not always result in the same output, this is because the time it takes for tasks to run is randomised according to a normally distributed variable with mean and variance given in the BPMN diagram (see [constraints](#BPMN-Diagram-Constaints:)).
##### `print_timestep(timestep, n=1, t=0.0)`
Prints one point in time (timestep) of the full simulation. The given value `timestep` must be non-negative and less than the maximum timestep value.

`print_timestep` assumes tasks take their mean amount of time every time with no randomness.

##### `get_max_time(n=1, t=0.0)`
Returns the maximum timestep reached in a simulation.

`get_max_time` assumes tasks take their mean amount of time every time with no randomness.

# Roadmap

