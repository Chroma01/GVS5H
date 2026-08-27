
## ideation
<your analysis>
The problem requires simulating Santa's movement and counting distinct houses visited.
1.  **Movement Simulation**: We must track Santa's current coordinates $(x, y)$ after each of the $M$ moves. Since $M$ is up to $2 \times 10^5$, we can simulate this step-by-step in $O(M)$ time.
2.  **Collision Detection**: For each move, we traverse a line segment. We need to identify all houses lying on this segment.
    *   If the move is horizontal (constant $y$), we need to find houses with $y$-coordinate equal to the current $y$ and $x$-coordinate within the range $[\min(x_{start}, x_{end}), \max(x_{start}, x_{end})]$.
    *   If the move is vertical (constant $x$), we need to find houses with $x$-coordinate equal to the current $x$ and $y$-coordinate within the range $[\min(y_{start}, y_{end}), \max(y_{start}, y_{end})]$.
    *   To do this efficiently, we can store houses in two dictionaries: `houses_by_x` (mapping $x \to$ sorted list of $y$'s) and `houses_by_y` (mapping $y \to$ sorted list of $x$'s).
    *   Using binary search (`bisect`), we can find the range of indices in these sorted lists that fall within the segment in $O(\log N)$ time.
3.  **Counting Distinct Houses**: The problem requires counting *distinct* houses. A house might be visited multiple times.
    *   Naive approach: Maintain a global set of visited houses. For each segment, iterate through the houses found by binary search and add them to the set.
    *   **Pitfall**: In the worst case, if a line contains $O(N)$ houses and we traverse it $O(M)$ times, the total time becomes $O(N \cdot M)$, which is too slow ($4 \times 10^{10}$ operations).
    *   **Optimization**: We need to skip already visited houses. We can use a Disjoint Set Union (DSU) (or Union-Find) structure for each line (each $x$ or $y$ coordinate).
        *   For a specific line (e.g., $x=c$), let the sorted list of $y$-coordinates be $L$. We maintain a DSU structure where `parent[i]` points to the next unvisited index in $L$.
        *   Initially, `parent[i] = i`. When a house at index $i$ is visited, we union $i$ with $i+1$, effectively making `find(i)` return the next unvisited index.
        *   When processing a segment on a line, we find the range $[L, R]$ of indices. We start at $L$ and repeatedly call `find` to get the next unvisited index. If the index is within $[L, R]$, we count the house and union it with the next. If `find` returns an index $> R$, we stop.
        *   This ensures each house is processed (counted) exactly once. The amortized complexity of DSU operations is nearly constant ($\alpha(N)$).
4.  **Complexity**:
    *   Sorting houses: $O(N \log N)$.
    *   Simulating moves and binary searching: $O(M \log N)$.
    *   DSU operations: $O(N \alpha(N))$.
    *   Total Time: $O((N+M) \log N)$. This fits well within the time limit for $N, M \le 2 \times 10^5$.
    *   Space: $O(N)$ to store houses and DSU structures.
5.  **Constraints**: Coordinates can be large ($10^9$) and sums can exceed $2^{31}-1$, but Python handles large integers automatically.

## worker: Write the Python code implementing the described a
- **Algorithm**: The solution simulates Santa's movement step-by-step. For each move (horizontal or vertical), it identifies the segment traversed.
- **Efficiency**: To avoid $O(N \cdot M)$ complexity, houses are stored in sorted lists keyed by their x and y coordinates. Binary search (`bisect`) locates the relevant houses on the current segment in $O(\log N)$.
- **Distinct Counting**: A Disjoint Set Union (DSU) structure is used for each line (each unique x or y coordinate). The DSU tracks the next unvisited house index. When a house is visited, it is "unioned" with the next one, effectively skipping it in future queries. This ensures each house is processed exactly once, leading to an amortized complexity of nearly linear time relative to the number of houses visited.
- **Data Structures**:
  - `houses_by_x`: Dict mapping $x \to$ sorted list of $y$'s.
  - `houses_by_y`: Dict mapping $y \to$ sorted list of $x$'s.
  - `parent_x`, `parent_y`: Dictionaries mapping coordinate $\to$ list of DSU parents for the indices in the corresponding sorted lists.
- **Edge Cases**: Handles large coordinates (Python handles arbitrary precision integers), empty sets of houses on a line, and moves that don't pass through any houses.

## worker: Run the code against Sample 1 and Sample 2 to veri
1.  **Algorithm Verification**: The code implements the Disjoint Set Union (DSU) approach to efficiently count distinct houses visited.
    *   **Sorting & Indexing**: Houses are grouped by X and Y coordinates and sorted. This allows $O(\log N)$ range queries using `bisect`.
    *   **DSU for Skipping**: For each line (constant X or Y), a DSU structure tracks the next unvisited house index. When a house is visited, it is unioned with the next index, effectively skipping it in future queries. This ensures each house is processed exactly once, reducing the complexity from $O(N \cdot M)$ to $O((N+M) \log N + N \alpha(N))$.
    *   **Iterative Find**: An iterative `find` function is used to prevent recursion depth issues, although `sys.setrecursionlimit` was also increased as a safeguard.
2.  **Sample 1 Check**:
    *   Start: (3, 2). Houses: (2,2), (3,3), (2,1).
    *   L 2: Move (3,2) -> (1,2). Range x=[1,3], y=2. House (2,2) found. Count=1.
    *   D 1: Move (1,2) -> (1,1). Range y=[1,2], x=1. No houses.
    *   R 1: Move (1,1) -> (2,1). Range x=[1,2], y=1. House (2,1) found. Count=2.
    *   U 2: Move (2,1) -> (2,3). Range y=[1,3], x=2. House (2,2) is in range but already visited (skipped by DSU). House (3,3) is not on x=2.
    *   Final: (2,3), Count=2. Matches sample output.
3.  **Sample 2 Check**:
    *   Start: (0,0). House: (1,1).
    *   R 1e9: Move (0,0) -> (1e9, 0). y=0. House is at y=1. No intersection.
    *   R 1e9: Move (1e9,0) -> (2e9, 0). No intersection.
    *   R 1e9: Move (2e9,0) -> (3e9, 0). No intersection.
    *   Final: (3000000000, 0), Count=0. Matches sample output.
4.  **Overflow**: Python handles large integers automatically, so sums like $3 \times 10^9$ are safe.
