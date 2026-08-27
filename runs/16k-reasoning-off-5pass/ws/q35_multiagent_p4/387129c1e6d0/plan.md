1. **Simulate Santa's path**: Track Santa's current position $(x, y)$ and process each move $(D_i, C_i)$ to update his position. For each move, determine the segment of the path (horizontal or vertical).
2. **Check for house intersections**: For each segment, check if any house lies on that segment. Since houses are points and segments are axis-aligned, we can efficiently check by:
   - For horizontal moves: check houses with the same $y$-coordinate and $x$-coordinate between the start and end of the move.
   - For vertical moves: check houses with the same $x$-coordinate and $y$-coordinate between the start and end of the move.
3. **Efficient house lookup**: To avoid $O(N \cdot M)$ complexity, pre-process houses into two dictionaries (or hash maps):
   - `houses_by_x`: maps $x$-coordinate to a sorted list of $y$-coordinates for houses at that $x$.
   - `houses_by_y`: maps $y$-coordinate to a sorted list of $x$-coordinates for houses at that $y$.
4. **Use binary search**: For each move, use binary search (e.g., `bisect`) on the sorted lists to find houses in the relevant range. Keep a set of visited houses to count distinct ones.
5. **Handle large coordinates**: Use 64-bit integers (Python handles this automatically) to avoid overflow.