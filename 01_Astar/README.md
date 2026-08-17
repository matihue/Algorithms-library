## Problem:
Finding the shortest paths from a starting position to a target based on specific maps.

## Intuition:
A queue-based algorithm that examines neighboring cells and records the cost for each cell based on the sum of the path cost traveled so far and the distance to the target. If a cell is revisited, the stored cost is updated only if the new path cost is lower than the previously recorded one. Once the path to the target has been fully explored, the optimal route can be reconstructed by backtracking using a parent dictionary.

## Example applications:
- AI in games (e.g., finding the shortest path to a food source),
- route planning in navigation apps,
- robot movement within a specific space,
- pathfinding in mazes and on maps.
