## Example usage
```python
# main.py (example)
#
# first we need to import the necessary files:
import bpmn_tree_structure
import bpmn_parser
import tree_simulation

# then we can simply make Simulation object:
simulation = tree_simulation.Simulation("diagram.bpmn", timescale=3)
simulation.simulate()
```

## BPMN Diagram Constraints:
* Each node must belong to exactly **one** layer.
* There must be exactly **one** root node and **one** node for which it's depth is equal to the height of the diagram.
* A node may not have more than one parent.
* The text inside of a task must be in the form `name;t;var` where `t` is the time in seconds which the task will run for in the simulation, and `var` is the variance of the time taken.
* It follows that neither `t` nor `var` may be negative.
  
  Should the time be too long for a simulation, you can instead input the time in minutes, or hours etc. for the sake of the simulation.
