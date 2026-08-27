
## ideation
The core difficulty lies in efficiently determining which houses lie on the path segments Santa traverses. A naive check against all $N$ houses for each of the $M$ moves would result in $O(N \cdot M)$ complexity, which is too slow given the constraints ($N, M \le 2 \times 10^5$).

The key insight is that Santa's movements are strictly axis-aligned (horizontal or vertical). Therefore, for any given move:
1. If it's horizontal (L/R), Santa stays at a constant $y$-coordinate and varies $x$. We only need to check houses that have that specific $y$-coordinate and an $x$-coordinate within the range of the move.
2. If it's vertical (U/D), Santa stays at a constant $x$-coordinate and varies $y$. We only need to check houses that have that specific $x$-coordinate and a $y$-coordinate within the range of the move.

To implement this efficiently:
1. Pre-process the houses into two hash maps:
   - `houses_by_y`: Maps a $y$-coordinate to a sorted list of $x$-coordinates of houses at that $y$.
   - `houses_by_x`: Maps an $x$-coordinate to a sorted list of $y$-coordinates of houses at that $x$.
2. For each move, determine the direction and range.
3. Use binary search (`bisect_left` and `bisect_right`) on the corresponding sorted list to find all houses within the segment's range.
4. Maintain a set of visited house indices (or coordinates) to count distinct houses. Note that we must ensure we don't double-count a house if it's visited multiple times. Since the problem asks for the number of *distinct* houses, using a set is appropriate.
5. Be careful with coordinate ranges: the segment includes both endpoints. The binary search should find all points $P$ such that $\min(x_{start}, x_{end}) \le P.x \le \max(x_{start}, x_{end})$ (for horizontal) or similarly for vertical.

Pitfalls to avoid:
- **Overflow**: Coordinates can be up to $10^9$ and moves up to $10^9$, so final positions can exceed $2^{31}-1$. Python handles large integers automatically, so this is not an issue in Python, but worth noting for other languages.
- **Double counting**: Using a set of house identifiers (e.g., tuples of coordinates) ensures each house is counted only once.
- **Efficiency**: Using hash maps for lookup and binary search for range queries ensures that each move is processed in $O(\log N)$ time on average (plus the time to iterate over found houses, but each house is added to the set at most once, so the total iteration cost over all moves is bounded by $O(N)$). Thus, the overall complexity is $O(N \log N + M \log N)$.

## worker: [todo] **Task 1**: Read input and store houses in 
The solution efficiently simulates Santa's path and checks for house intersections using pre-processed data structures. 

1. **Data Structures**: 
   - `houses_by_x`: Maps each x-coordinate to a sorted list of y-coordinates of houses at that x.
   - `houses_by_y`: Maps each y-coordinate to a sorted list of x-coordinates of houses at that y.
   - `visited_houses`: A set to store tuples of (x, y) for houses that have been passed or arrived at, ensuring distinct counting.

2. **Algorithm**:
   - For each move, determine the direction and the range of the segment.
   - Depending on the direction (horizontal or vertical), use the corresponding dictionary to find houses within the segment's range.
   - Use binary search (`bisect_left` and `bisect_right`) to efficiently find all houses in the range.
   - Add found houses to the `visited_houses` set.

3. **Complexity**:
   - Pre-processing houses: $O(N \log N)$ due to sorting.
   - Each move: $O(\log N)$ for binary search plus $O(K)$ where $K$ is the number of houses found in the range. Since each house is added to the set at most once, the total cost of adding to the set over all moves is $O(N)$. Thus, the overall complexity is $O(N \log N + M \log N)$.

4. **Edge Cases**:
   - Large coordinates are handled by Python's arbitrary-precision integers.
   - No house at the starting position is guaranteed by constraints.
   - Houses may be visited multiple times, but the set ensures distinct counting.
