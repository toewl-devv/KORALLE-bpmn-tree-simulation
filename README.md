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
simulation.simulate(visualise=True)
```

![examplevideo](media/video.mov)

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
import simulation
```
To create a simulation, we create an instance of the Simulation class:
```py
my_simulation = simulation.Simulation("complexdiagram.bpmn")
```
We can optionally give values for the time scale (default 1), and a value for the number of processes `n` to run at once (default 1) along with the staggering time `t` between the processes (default 0):
```py
my_simulation = simulation.Simulation("complexdiagram.bpmn", n=6, t=1.0, timescale=3)
```
In this case, the simulation will run three times faster than usual when we start it.

Now we can use other commands.
## Features of `Simulation`
### The `Simulation` Object
Upon creating a simulation, can access several parameters about it.
#### Attributes
##### `self.tree`
The `Tree` object which is created from the given BPMN diagram. This object has its own functions tied to it too.
##### `self.timescale`
The given timescale, `1.0` if no timescale is given.
##### `self.processes`
The given number of processes `n`, `1` if no value is given.
##### `self.stagger`
The given staggering time of processes `t`, `0.0` if no value is given.
##### `self.results`
The [`results` object](#The-results-Object) contains data about the simulation which is filled in after the simulation is run with [`simulate()`](#simulate(visual=False)).

#### `simulate(visualise=False)`
Runs a simulation of the current `Simulation` object. If `visualise` is true, a tree representation of the BPMN file will be shown. Currently active nodes will represented by a number of asterisks `*` corresponding to the number of processes currently running that node.

> [!NOTE]
> A simulation ran with the exact same input values may not always result in the same output, this is because the time it takes for tasks to run is randomised according to a normally distributed variable with mean and variance given in the BPMN diagram (see [constraints](#BPMN-Diagram-Constaints)).

> [!NOTE]
> If `visualise` is set to `True`, the console will be cleared before showing the simulation!

### The `results` Object
#### Attributes
##### `self.failures`
A dictionary of each node ID and how many times that node failed during the simulation.
##### `self.time_steps_taken`
The total time steps which the simulation took to finish.
##### `self.node_times_spent_waiting`
A dictionary of each node ID and how many time steps it spent waiting to move on to the next node (this value is incremented every time the node is finished but it cannot move to the next node because it's capacity is full).
##### `self.event_log`
A list of dictionaries with data about the simulation.
> [!TIP]
> Use the `pandas` library if you plan on using the event log.

# Roadmap


