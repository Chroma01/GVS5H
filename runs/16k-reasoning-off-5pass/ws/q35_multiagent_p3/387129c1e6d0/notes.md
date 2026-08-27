
## ideation
- The core difficulty is efficiently checking which houses lie on the line segments Santa travels, given the constraints ($N, M \le 2 \times 10^5$). A naive $O(N \cdot M)$ check is too slow.
- Since all moves are axis-aligned (horizontal or vertical), we can preprocess the houses into two data structures:
  1. `houses_by_y`: A dictionary mapping y-coordinate to a sorted list of x-coordinates.
  2. `houses_by_x`: A dictionary mapping x-coordinate to a sorted list of y-coordinates.
- For each move, we determine the segment. If it's horizontal (same y), we look up `houses_by_y[y]` and use binary search (`bisect`) to find houses with x-coordinates in the range `[min(x_start, x_end), max(x_start, x_end)]`.
- If it's vertical (same x), we look up `houses_by_x[x]` and use binary search to find houses with y-coordinates in the range `[min(y_start, y_end), max(y_start, y_end)]`.
- We maintain a set of visited house coordinates to count distinct houses.
- Pitfalls:
  - Coordinate values can be very large (up to $10^9$ or more after moves), so we must use 64-bit integers. Python handles this automatically.
  - Be careful with the range inclusion: the segment includes both endpoints.
  - The problem states "passed through or arrived at", so if Santa lands exactly on a house, it counts.
  - The initial position is not a house, but subsequent positions might be.
  - We need to ensure we don't double-count houses if they are visited multiple times. Using a set of coordinates handles this.
  - The number of houses on a segment can be large, but we only need to add them to the set. The total number of additions to the set is bounded by $N$, so the overall complexity will be dominated by the binary searches and set operations, which is $O(M \log N + N \log N)$ due to sorting.

## worker: [todo] **Task 1**: Read input values N, M, Sx, Sy,
The solution efficiently handles the problem by preprocessing house locations into two dictionaries: `by_y` mapping y-coordinates to sorted lists of x-coordinates, and `by_x` mapping x-coordinates to sorted lists of y-coordinates. This allows for $O(\log N)$ range queries using binary search (`bisect_left` and `bisect_right`) for each move.

For each move, Santa travels along an axis-aligned segment. Depending on the direction (U, D, L, R), we query the appropriate dictionary to find all houses lying on that segment. The coordinates of these houses are added to a set to ensure distinct counting.

The time complexity is $O(N \log N + M \log N)$ due to sorting the house coordinates and performing binary searches for each of the $M$ moves. The space complexity is $O(N)$ to store the house coordinates. Python's arbitrary-precision integers handle the large coordinate values without overflow issues.
