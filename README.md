
# Min Cost algorithms

A python implementation of min cost maximum flow algorithms. 

The implemented algorithms are:

1. **Successive shortest path**
2. **Cycle cancelling**
3. **Primal-Dual**

The program loads a graph from file, runs the algorithms and prints to output the **computed graph structure with flow value for each edge** and **total cost**. If the graph is not admissible for a solution it detects it and stops the algorithm. The program is intended to work with directed _NetworkX_ graphs with properties: capacity, flow, bValue

## How to run
It is recommended to create a python virtual environment either using `conda` or `pyenv`

These are the required steps to run the program from the working directory: 

1. Install required dependencies

    `pip install requirements.txt`


2. Run the code with:

    `python main.py --graph graph_filename.txt`

## Graph files

Graph files are plain-text files stored in the `graphs/` subfolder (pass only the file name to `--graph` while running `main.py`). Fields on each line are separated by a single space (the separator used by `main.py`). The format is parsed by `load_directed_graph` in `loadFromFile.py`.

### Structure

1. **Line 1 – node header**: the keyword `nodes` followed by a list of names of each node's properties, e.g. `nodes bValue`.
2. **Line 2 – edge header**: the keyword `edges` followed by a list of names of each edge's properties, e.g. `edges capacity cost`.
3. **Remaining lines** – The following lines of the file represent the nodes and edges of the file. One node or edge per line:
   - Node: `n <label> <property values...>`, one value for each node property in the header.
   `label` is the an associated string that uniquely identifies a node in a graph
   - Edge: `e <from_node_label> <to_node_label> <property values...>`, one value for each edge property in the header. Edges are directed.

If the first two lines are not in this format, the file is rejected. Lines that do not start with `n`/`e` or have the wrong number of values are silently skipped. All values are read as strings.

### Example

```
nodes bValue
edges capacity cost
n s 10
n a 0
n t -10
e s a 10 2
e a t 10 3
```

