## Problem:
Finding the shortest path from a starting position to a destination on a given map that may contain obstacles.

## Intuition:
This algorithm operates similarly to other pathfinding algorithms—using a queue of tiles to check, a list of already checked tiles, and a selection process for the best move—but it runs simultaneously from both the start and the destination, drastically reducing the number of tiles that need to be checked. The path is reconstructed once the two waves meet and establish a meeting point. It works best in scenarios where movement costs are not a factor, as the identified meeting point serves as the reference for calculating the optimal path segments, rather than the path being calculated in its entirety from start to finish.

## Example use cases:
- Scenarios where movement geometry matters, but movement costs do not
- Finding paths in mazes consisting only of open space and walls
- Social networks: finding the shortest chain of connections between two individuals
