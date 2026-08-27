
## ideation
The core difficulty lies in efficiently finding houses along the path segments given the large coordinate space ($10^9$) and the constraints on $N$ and $M$ ($2 \times 10^5$). A naive check of all houses for each move would be $O(NM)$, which is too slow.

**Candidate Approaches:**
1.  **Coordinate Compression + 2D Structure**: Compress coordinates and use a 2D data structure (e.g., 2D Segment Tree). This is complex to implement and may have high constant factors.
2.  **Spatial Indexing (KD-Tree/Quadtree)**: Query points in a rectangle. Overhead might be significant, and worst-case performance can be poor.
3.  **Sorting + Binary Search + DSU (Recommended)**:
    *   Store houses in two dictionaries: `houses_by_y` (mapping $y \to$ sorted list of $x$'s) and `houses_by_x` (mapping $x \to$ sorted list of $y$'s).
    *   For each move, use binary search (`bisect`) to find the range of indices in the sorted list that fall within the move's segment.
    *   Use a Disjoint Set Union (DSU) structure for each line to skip houses that have already been visited on that specific line. This ensures each house is processed at most twice (once for its horizontal line, once for its vertical line).
    *   Maintain a global boolean array or set to track distinct houses visited across all moves.

**Pitfalls:**
*   **Double Counting**: A house lies on exactly one horizontal line and one vertical line. It might be encountered during a horizontal move and again during a vertical move. A global visited tracker is necessary.
*   **DSU Logic**: The DSU must efficiently return the *next unvisited* index. Standard DSU `union` needs to be adapted to link an index to the next one (`parent[i] = find(i+1)`).
*   **Binary Search on Tuples**: If storing `(x, id)` tuples, `bisect` cannot directly compare with an integer coordinate. We need separate lists of coordinates or a custom key.
*   **Memory**: Storing lists for each unique coordinate can be memory-intensive, but $O(N)$ is acceptable.
*   **Recursion Depth**: Recursive `find` in DSU might hit recursion limits; iterative implementation is safer.

## worker: Parse input using `sys.stdin.read` and build `hous
The solution uses a combination of sorting, binary search, and Disjoint Set Union (DSU) to efficiently process the moves.
1.  **Data Organization**: Houses are stored in dictionaries `houses_by_y` and `houses_by_x`, mapping coordinates to sorted lists of house IDs and their coordinates. This allows efficient range queries.
2.  **Binary Search**: For each move, `bisect_left` and `bisect_right` are used to find the range of indices in the sorted lists that fall within the move's segment.
3.  **DSU for Skipping**: A DSU structure is maintained for each line (horizontal or vertical). When a house is visited, it is unioned with the next index in the list. This allows the algorithm to skip already visited houses in $O(\alpha(N))$ time, ensuring each house is processed at most twice (once for horizontal, once for vertical).
4.  **Complexity**: Sorting takes $O(N \log N)$. Each move takes $O(\log N)$ for binary search and nearly constant time for DSU operations. Total time complexity is $O(N \log N + M \log N)$, which fits within the constraints.
5.  **Edge Cases**: Large coordinates are handled by Python's arbitrary-precision integers. The DSU handles boundaries correctly by including an extra element in the parent array.
