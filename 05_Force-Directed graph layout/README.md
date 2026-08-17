## Problem
Arrange a given graph in a way that makes it as readable and visually structured as possible.

## Intuition

This algorithm works similarly to a physical simulation. Instead of directly calculating the final positions of all nodes, it repeatedly applies several different forces that gradually move the graph toward a better layout.

The algorithm combines four main forces:

- Distance correction force – moves connected nodes so that the distance between them is as close as possible to the desired edge length.
- Crossing reduction force – detects intersecting edges and moves their endpoints in directions that can help reduce the number of crossings.
- Node repulsion force – based on Coulomb's law. Nodes repel each other as if they were particles with the same electrical charge, which prevents the graph from collapsing into a small area.
- Node-edge repulsion force – pushes nodes away from nearby edges that they are not connected to, improving overall readability.

The final layout is evaluated using a score. A lower score represents a better graph.

The score is based mainly on:
- average error between desired and actual edge lengths,
- number of edge crossings,
- penalties for nodes being too close to unrelated edges.

The user can modify the weights of these components, allowing the algorithm to prioritize different properties. For example, a larger crossing weight makes the optimizer prefer layouts with fewer edge intersections, while a larger distance weight gives more importance to preserving the desired edge lengths.

The algorithm does not guarantee a perfect layout. Different forces can compete with each other, and the optimization can converge to different local solutions depending on the initial node positions.


## Planarity

- It is worth noting that NOT every graph can be drawn without edge crossings.

- Some graphs are non-planar, which means that there is no possible arrangement of their vertices in a two-dimensional plane that results in zero edge crossings.

- Because of this, for some graphs the theoretical minimum number of crossings is greater than zero, regardless of how well the optimizer performs.
