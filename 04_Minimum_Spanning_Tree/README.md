## Problem:
Finding the minimum total cost required to connect all vertices in a weighted graph without creating unnecessary cycles.

## Intuition:
The idea of this algorithm is relatively simple.
We start from an arbitrary vertex and mark it as reached. Then, among all edges connecting the currently reached vertices to vertices that have not been reached yet, we choose the edge with the smallest weight.
The newly reached vertex is added to the set of visited vertices and the process is repeated.
At every step, the algorithm searches for the cheapest possible connection between the already constructed part of the graph and one of the remaining vertices.
The process finishes when every vertex has been reached.
The result is a tree connecting all vertices while minimizing the total sum of edge weights.

## Example use cases:

Minimum Spanning Trees can be useful whenever multiple locations or objects need to be connected while keeping the total connection cost as small as possible.

- Network infrastructure – connecting buildings, computers or network nodes while minimizing the total amount of cable required.
- Road planning – finding a low-cost set of roads that connects multiple locations.
-  Electrical grids – connecting multiple points while minimizing the total length or cost of power lines.
-   Pipeline networks – designing a basic network connecting multiple locations with minimal construction cost.
-   Clustering and data analysis – MSTs can be used to reveal structure in data and help separate groups based on distances between points.
