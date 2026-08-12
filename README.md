## Example usage
```python
# main.py
#
# first we need to import the necessary files:
import bpmn_tree_structure
import bpmn_parser
import tree_simulation

# then we can simply make Simulation object:
simulation = tree_simulation.Simulation("diagram.bpmn", timescale=3)
simulation.simulate()
```
A (slightly) more sophisticated example is found in [`main.py`](main.py).

## BPMN Diagram Constraints:
* Each node must belong to exactly **one** layer.
* There must be exactly **one** root node and **one** node for which it's depth is equal to the height of the diagram.
* A node may not have more than one parent.
* The text inside of a task must be in the form `name;t` where `t` is the time in seconds which the task will run for in the simulation.
  
  Should the time be too long for a simulation, you can instead input the time in minutes, or hours etc. for the sake of the simulation.
