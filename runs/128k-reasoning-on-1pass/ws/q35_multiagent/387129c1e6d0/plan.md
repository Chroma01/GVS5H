1.  **Input Parsing**: Read all input efficiently using `sys.stdin.read().split()`. Parse $N, M, S_x, S_y$ and the house coordinates.
2.  **Data Organization**: Store houses in two dictionaries: `houses_by_y` mapping $y \to$ sorted list of $x$'s, and `houses_by_x` mapping $x \to$ sorted list of $y$'s. This allows efficient range queries for horizontal and vertical moves.
3.  **DSU Initialization**: For each list in the dictionaries, initialize a Disjoint Set Union (DSU) structure. The DSU will help skip houses that have already been visited on a specific line, ensuring each house is processed at most twice (once for horizontal, once for vertical).
4.  **Simulation**: Simulate Santa's movement step by step. For each move:
    *   Determine the segment (horizontal or vertical).
    *   Use binary search (`bisect_left`) to find the starting index of houses within the segment's range.
    *   Use the DSU to iterate through unvisited houses in the range. Add them to a `visited` set and union the current index with the next to mark it as visited.
    *   Update Santa's position.
5.  **Output**: Print the final coordinates and the size of the `visited` set.