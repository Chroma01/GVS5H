
## ideation
The core difficulty lies in efficiently determining which houses lie on the line segments traversed by Santa. A naive check of all $N$ houses for each of the $M$ moves results in $O(NM)$ complexity, which is too slow given $N, M \le 2 \times 10^5$.

The key insight is that the moves are axis-aligned.
- Horizontal moves (L/R) keep $Y$ constant and vary $X$. We only need to check houses with that specific $Y$ coordinate.
- Vertical moves (U/D) keep $X$ constant and vary $Y$. We only need to check houses with that specific $X$ coordinate.

By organizing the houses into two hash maps:
1. `houses_by_y`: Maps a $Y$-coordinate to a set of $X$-coordinates of houses at that $Y$.
2. `houses_by_x`: Maps an $X$-coordinate to a set of $Y$-coordinates of houses at that $X$.

For each move, we can look up the relevant map in $O(1)$ average time. Then, we iterate through the candidate houses in that set. However, simply iterating through the set might still be slow if many houses share the same coordinate and are never visited, or if we repeatedly check the same unvisited houses.

To optimize, we can remove visited houses from the sets. Since each house is visited at most once, the total number of removals across all moves is $O(N)$. The cost of checking a house is $O(1)$. If a house is not on the current segment, we leave it in the set. But wait, if we don't remove it, we might check it again in a future move along the same line.

Actually, a better approach is:
- For a horizontal move at $Y=y$ from $x_1$ to $x_2$, look up `houses_by_y[y]`.
- Iterate through the $X$ values in this set. If an $X$ is within $[\min(x_1, x_2), \max(x_1, x_2)]$ and the house hasn't been visited, mark it as visited and remove it from both `houses_by_y[y]` and `houses_by_x[X]`.
- If an $X$ is not within the range, we cannot remove it because it might be visited in a future move along the same $Y$ line.

This approach ensures that each house is removed at most once. The total time complexity will be $O(N + M)$ on average, assuming hash map operations are $O(1)$. We must be careful with large coordinates (Python handles large integers automatically) and ensure we use sets for $O(1)$ lookups and removals.

Pitfalls:
- Forgetting to remove houses from both dictionaries when they are visited.
- Not handling the case where a house is at the starting or ending point of a move (the problem says "passed through or arrived at", so endpoints count).
- Overflow issues (mitigated by Python's arbitrary-precision integers).
- The initial position $(S_x, S_y)$ is not a house, so we don't need to check it initially.

## worker: [todo] Parse the input: read N, M, Sx, Sy, the lis
The solution efficiently tracks Santa's movement and counts distinct houses visited by using two hash maps (`houses_by_x` and `houses_by_y`) to quickly locate potential houses on each axis-aligned segment. When a house is found on a segment and hasn't been visited before, it is marked as visited, counted, and removed from both hash maps. This ensures that each house is processed at most once, leading to an overall time complexity of $O(N + M)$ on average, which is optimal for the given constraints. Python's arbitrary-precision integers handle the large coordinate values without overflow issues.
