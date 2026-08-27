
## ideation
The core difficulty lies in efficiently determining which houses lie on the line segments traversed by Santa Claus. A naive approach of checking every house against every segment is $O(N \cdot M)$, which is too slow given the constraints ($N, M \le 2 \times 10^5$).

The key insight is that since each house is counted at most once, we can optimize by removing visited houses from our data structure. We can group houses by their coordinates:
- For vertical movements (U/D), the path is a vertical line segment with constant $X$. We group houses by their $X$-coordinate. For each vertical segment, we look up the list of houses with that specific $X$ and check which ones have a $Y$-coordinate within the segment's range.
- For horizontal movements (L/R), the path is a horizontal line segment with constant $Y$. We group houses by their $Y$-coordinate. For each horizontal segment, we look up the list of houses with that specific $Y$ and check which ones have an $X$-coordinate within the segment's range.

By storing these lists as sorted arrays (or using a structure that allows efficient range queries and deletions), we can use binary search (`bisect`) to find the range of houses on the segment. Once found, we mark them as visited and remove them from the list to ensure they aren't counted again. Since each house is removed at most once, the total cost for removals is $O(N)$. The cost for binary searches across all segments is $O(M \log N)$. Thus, the total time complexity is $O((N + M) \log N)$, which fits within the time limits.

Pitfalls to avoid:
1. **Coordinate Range**: Coordinates can be large ($10^9$), so we cannot use a 2D array. Dictionary-based grouping is necessary.
2. **Integer Overflow**: Final coordinates can exceed $2^{31}-1$, so we must use 64-bit integers. Python handles this automatically, but it's a consideration for other languages.
3. **Segment Direction**: Moves can be negative (e.g., L, D). We must correctly determine the min and max bounds for the range check regardless of direction.
4. **Efficiency of Removal**: Removing elements from a Python list is $O(K)$ where $K$ is the number of elements removed. Since each element is removed once, the amortized cost is acceptable. Using `bisect` to find indices and then slicing/deleting is efficient.

## worker: [todo] **Task 1**: Read input and store houses in 
The solution efficiently tracks Santa's path and counts distinct houses visited by using coordinate-based grouping and binary search. 

1. **Data Structures**: 
   - `houses_by_x`: Dictionary mapping X-coordinate to a sorted list of Y-coordinates of houses at that X. Used for vertical segments (U/D moves).
   - `houses_by_y`: Dictionary mapping Y-coordinate to a sorted list of X-coordinates of houses at that Y. Used for horizontal segments (L/R moves).
   - `visited_houses`: A set to keep track of houses already counted, ensuring each house is only counted once.

2. **Algorithm**:
   - For each move, determine the line segment (horizontal or vertical).
   - Use `bisect_left` and `bisect_right` to find the range of houses in the relevant sorted list that lie within the segment's bounds.
   - If any houses are found, they are marked as visited, the count is incremented, and they are removed from the sorted list. This removal is crucial for efficiency: since each house is removed at most once, the total cost of removals across all operations is $O(N)$. The cost of binary searches is $O(M \log N)$.
   - Update Santa's current position after each move.

3. **Complexity**: 
   - Preprocessing: $O(N \log N)$ to sort the lists.
   - Processing moves: $O(M \log N)$ for binary searches.
   - House removals: $O(N)$ amortized since each house is removed once.
   - Total Time Complexity: $O((N + M) \log N)$.
   - Space Complexity: $O(N)$ to store the houses.

4. **Edge Cases**:
   - Large coordinates: Python handles large integers automatically.
   - No houses on a segment: The bisect indices will indicate an empty range, and no action is taken.
   - Houses at endpoints: The inclusive range check `[y_min, y_max]` correctly includes endpoints.
