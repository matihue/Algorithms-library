## Problem:
Finding the shortest paths from a starting position to a destination based on specific maps.

## Intuition:
The algorithm closely resembles A*, but it examines significantly more tiles and spreads more widely across the map; this occurs because it does not account for the estimated distance to the target. The `demonstration.png` file shows that while the primary route remains the same, the number of tiles checked differs from that of the A* algorithm (a detailed explanation of the mechanism is provided in the `readme.txt` file within the `01_Astar` folder).

## Example use case:
- Similar to A*, it offers an efficient approach when the specific destination is not initially known.
- It is used when paths to multiple destinations—rather than just one—need to be found; instead of running A* multiple times, Dijkstra’s algorithm is run once to explore the area and determine routes to several targets.
