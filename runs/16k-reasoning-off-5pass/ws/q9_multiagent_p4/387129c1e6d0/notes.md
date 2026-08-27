
## ideation
**Core Difficulty:**
1.  **Efficiency:** $N, M \le 2 \times 10^5$. A naive $O(N)$ check per move results in $O(NM)$, which is too slow ($4 \times 10^{10}$ operations). We need something closer to $O((N+M) \log N)$.
2.  **Coordinate Range:** Coordinates can be up to $10^9$ and move distances up to $10^9$, so the final position can exceed $2^{31}-1$. Python handles large integers automatically, but we must ensure no overflow logic is applied (unlike C++/Java).
3.  **Segment Intersection:** We need to efficiently query if any house lies on a line segment defined by $(x_1, y_1)$ to $(x_2, y_2)$. Since moves are axis-aligned, this simplifies to checking if a house has the same coordinate on one axis and falls within the range on the other.
4.  **Distinct Counting:** We need to count unique houses visited. Using a set of house indices (or coordinates) is necessary.

**Candidate Approaches:**
1.  **Sorting + Binary Search (Bisect):**
    *   Store houses in two lists:
        *   `houses_by_x`: Sorted by X, then Y.
        *   `houses_by_y`: Sorted by Y, then X.
    *   For a horizontal move (changing X, Y fixed):
        *   Filter houses with $Y = \text{current } Y$.
        *   Use `bisect_left` and `bisect_right` on `houses_by_x` to find the range of houses with X in $[\min(x_1, x_2), \max(x_1, x_2)]$.
        *   Iterate through this small range (worst case $O(N)$ per move if all houses are on the line, but average case depends on distribution; however, worst-case input could still be bad if many houses lie on the path).
        *   *Wait*, worst case: All $N$ houses are on the line $Y=0$. Moving from $-10^9$ to $10^9$ visits all $N$. Next move visits all again. Total $O(NM)$. This approach fails if many houses are collinear.
    *   *Correction*: The problem asks for the number of *distinct* houses. If we process moves sequentially, we might re-scan the same houses.
    *   **Optimization:** Instead of scanning ranges repeatedly, can we mark houses as "visited"?
        *   If we simply iterate the range found by bisect, and the range contains $K$ houses, we do $O(K)$ work. If $K$ is large and repeated, we TLE.
        *   However, once a house is visited, we don't need to count it again. But we still need to *find* it to mark it.
        *   Is there a way to avoid re-scanning?
        *   Actually, the constraints allow $O(N \log N + M \log N + \text{total visits})$. If total visits is high, we fail.
        *   **Crucial Observation:** The total number of *distinct* houses is at most $N$. If we can efficiently find *unvisited* houses on the segment, we are good.
        *   But finding unvisited houses on a segment is hard without complex data structures (Segment Tree / Fenwick Tree over coordinates).
        *   Let's re-read the constraints and typical competitive programming patterns for this specific problem (likely AtCoder ABC 213 D or similar).
        *   Actually, usually in these problems, the test cases aren't constructed to hit the worst-case $O(NM)$ with naive bisect unless there's a specific trick. But we should aim for better.
        *   **Alternative Idea:** Since we only care about distinct houses, maybe we can process the moves differently? No, the path is fixed.
        *   **Re-evaluating the "Bad Case":** If all houses are on a single line, and we traverse that line back and forth.
            *   Move 1: Traverse full line. Visit all $N$. Mark all as visited.
            *   Move 2: Traverse full line. Bisect finds $N$ houses. We check each. If we check `visited` flag, we stop early? No, we still have to iterate to find the first unvisited one or just skip.
            *   If we iterate all $N$ every time, it's $O(NM)$.
            *   **Solution:** Use a data structure to maintain the set of *unvisited* houses on each line (or coordinate).
            *   Since coordinates are large, we can't use a direct array. We can use a `set` for each unique X and each unique Y containing the list of Y-coordinates (for vertical lines) or X-coordinates (for horizontal lines) of unvisited houses.
            *   In Python, `set` doesn't support range deletion efficiently.
            *   However, `sortedcontainers` isn't available. We must use standard library.
            *   **Standard Library Limitation:** Without `sortedcontainers`, implementing a balanced BST or Segment Tree is verbose.
            *   **Is $O(NM)$ really the intended worst case?** If the problem is from a contest like AtCoder, usually $N, M \le 2 \cdot 10^5$ implies $O((N+M)\log N)$ or $O((N+M)\sqrt{N})$.
            *   Let's reconsider the "Bad Case". If all houses are on $Y=0$, and we move $L$ then $R$.
                *   Move L: Scan all $N$. Mark all visited.
                *   Move R: Scan all $N$. All marked.
                *   Total time $2N$. Wait, scanning $N$ items takes $O(N)$. Doing it $M$ times is $O(NM)$.
                *   We need to skip visited houses.
                *   We can maintain for each $Y$ coordinate, a list of $X$ coordinates of unvisited houses. Since we need to query by range, we need a structure that supports "find elements in range $[L, R]$" and "delete elements".
                *   In Python, we can simulate this by storing the unvisited houses in a `set` for each $Y$. But `set` doesn't support range queries.
                *   **Wait**, maybe the number of houses on any specific line isn't that large in typical test cases, OR the problem allows $O(N \log N + M \log N + \text{output})$?
                *   Actually, there is a simpler observation: We only need to count distinct houses.
                *   If we use a `set` to store visited house indices.
                *   For each move, we get a range of potential houses. We iterate them. If a house is not in `visited`, add to `visited`.
                *   To avoid iterating visited houses repeatedly, we need to efficiently jump over them.
                *   **Idea:** For each unique $Y$, keep a sorted list of $X$'s of houses on that line. Also keep a pointer or a set of "active" segments?
                *   Actually, the most robust way without external libs:
                    *   Group houses by $X$ and by $Y$.
                    *   For a move on line $Y=y$, we get a range $[x_{min}, x_{max}]$.
                    *   We need to find all houses in this range that are not yet visited.
                    *   We can maintain for each $Y$, a `set` of unvisited $X$'s? No, range query on set is slow.
                    *   **Wait**, is it possible that the sum of lengths of segments visited is small? No.
                    *   **Let's look at the constraints again.** $N, M \le 2 \cdot 10^5$.
                    *   Maybe the intended solution relies on the fact that we only care about the *count*.
                    *   **Hypothesis:** The test cases are weak, or there's a property I'm missing.
                    *   **Actually**, there is a known technique for this: **Coordinate Compression + Segment Tree**.
                        *   Compress all $X$ and $Y$ coordinates that appear in the houses.
                        *   Build a Segment Tree over the compressed X-coordinates. Each node stores the count of unvisited houses in that range (or a flag if any exist).
                        *   Query: Find range $[x_{min}, x_{max}]$ on line $Y=y$.
                        *   Traverse the segment tree to find unvisited houses in that range.
                        *   Mark them as visited (update tree to 0).
                        *   Complexity: $O(M \log N + N \log N)$.
                        *   This is the correct approach for strict time limits.
                        *   Implementation details:
                            1. Collect all unique $X$ coordinates of houses. Sort and map to ranks $0..K$.
                            2. Build a Segment Tree (or Fenwick Tree if we only need counts, but we need to *find* and *remove* specific items to avoid re-scanning).
                            3. Actually, we need to *iterate* and remove. A Segment Tree can support "find first unvisited in range", then "remove", then "find next". This is $O(\text{num\_visited} \times \log N)$.
                            4. Total complexity: $O(M \log N + (\text{total distinct houses}) \log N) = O((N+M) \log N)$.
                            5. This handles the "all houses on one line" case perfectly.

**Pitfalls:**
1.  **Coordinate Compression:** Must handle negative coordinates.
2.  **Segment Tree Implementation:** Python recursion limit or overhead. Iterative segment tree is preferred.
3.  **Horizontal vs Vertical:** Need two structures?
    *   Actually, we can just use one structure if we process moves? No, moves are dynamic.
    *   We need to query based on fixed coordinate.
    *   Approach A: Two Segment Trees. One for X-coordinates (to handle vertical moves), one for Y-coordinates (to handle horizontal moves).
        *   Tree X: Keys are unique $X_i$. Values indicate if house at $(X_i, Y_i)$ is visited. Wait, multiple houses can have same $X$.
        *   So, Tree X should store a list of $Y$'s for each $X$, sorted. And we need to mark specific $Y$'s as visited.
        *   This gets complicated.
    *   Approach B (Simpler): Just store houses in a list sorted by X, and a list sorted by Y.
        *   For a vertical move (fixed X, range Y):
            *   Look at the list of houses with this specific X.
            *   We need to find houses in Y-range $[y_{min}, y_{max}]$ that are unvisited.
            *   We can maintain for each unique X, a Segment Tree (or similar) over the Y-coordinates of houses at that X.
            *   Since total houses is $N$, the sum of sizes of these trees is $N$.
            *   Similarly for horizontal moves: For each unique Y, maintain a structure over X-coordinates.
        *   This is $O(N \log N)$ build + $O(M \log N + \text{visits} \log N)$.
        *   Given Python's overhead, building $N$ small trees might be slow if many unique X/Y.
        *   **Alternative:** Just use a global Segment Tree on compressed coordinates?
            *   We need to query "houses at $X=x$ with $Y \in [y1, y2]$".
            *   This is a 2D range query problem (points in a rectangle).
            *   But the rectangle is degenerate (width 0 or height 0).
            *   We can treat this as: Query points with $X=x$ and $y \in [y1, y2]$.
            *   We can solve this by sorting queries and processing offline? No, we need online updates (marking visited).
            *   **Best Approach for Python:**
                *   Group houses by X. For each X, store a sorted list of (Y, original_index).
                *   For each group, we need to efficiently find and remove items in a range.
                *   Since the groups are independent, we can just use a `bisect` to find the start/end of the range in the list.
                *   Then iterate from start to end. If a house is visited, skip. If not, mark visited and add to count.
                *   **Problem:** If we have 1000 houses on line X=0, and we traverse it 1000 times.
                    *   First traversal: Visits 1000. $O(1000)$.
                    *   Second traversal: Bisect finds 1000. We iterate 1000. Check `visited`. Skip. $O(1000)$.
                    *   Total $O(N \times M)$.
                *   **Fix:** We need to skip visited items efficiently.
                *   Inside the list for a specific X, we can maintain a pointer or use a data structure to jump over visited items.
                *   Since we only delete, we can use a `set` of unvisited indices for that X? No, we need range.
                *   **Wait**, if we use a `set` of unvisited indices for a specific X, we can't do range queries efficiently in Python without a library.
                *   **Is there a simpler trick?**
                *   What if we just accept that we iterate?
                *   Actually, the problem statement says "Find the point... and the number of distinct houses".
                *   Maybe the number of *moves* that actually pass through houses is small? No.
                *   Let's reconsider the **Segment Tree** approach. It is the only one guaranteeing $O((N+M)\log N)$.
                *   **Implementation Plan for Segment Tree:**
                    1.  Collect all unique X coordinates. Sort them -> `unique_x`. Map $x \to idx$.
                    2.  For each unique $x$, we have a list of houses $(y, id)$. Sort by $y$.
                    3.  We need to query: Given $x$ and range $[y_1, y_2]$, find all unvisited houses.
                    4.  This is equivalent to: In the list of houses for $x$, find indices in the sorted $y$-list that fall in $[y_1, y_2]$ and are unvisited.
                    5.  We can maintain for each $x$, a Segment Tree (or Fenwick) over the *indices* of the sorted $y$-list.
                    6.  The Segment Tree stores 1 if the house is unvisited, 0 if visited.
                    7.  Query: Sum in range $[L, R]$. If sum > 0, we need to find the positions.
                    8.  We can implement a "find k-th" or "find first 1 in range" on the segment tree.
                    9.  Since Python is slow, building $N$ segment trees (one for each unique X) is overhead.
                    10. **Optimization:** Notice that we only need to handle vertical moves (fixed X) and horizontal moves (fixed Y).
                        *   We can have two maps: `trees_x` (map X -> SegmentTree over Y-ranks) and `trees_y` (map Y -> SegmentTree over X-ranks).
                        *   Total nodes in all trees = $N$.
                        *   Building $N$ small trees is fine.
                        *   Query: $O(\log (\text{count at X}))$.
                        *   Update: $O(\log (\text{count at X}))$.
                        *   This is optimal.

**Refined Plan:**
1.  Read input. Store houses as `(x, y, id)`.
2.  Group houses by X: `by_x[x] = list of (y, id)`. Sort each list by Y.
3.  Group houses by Y: `by_y[y] = list of (x, id)`. Sort each list by X.
4.  For each group in `by_x`:
    *   Create a Segment Tree (or Fenwick Tree with "find next" logic) over the indices $0..len-1$.
    *   Initialize with 1s (all unvisited).
    *   Store the tree in a dictionary/list keyed by X.
    *   *Wait*, implementing a full Segment Tree in Python for every group might be heavy on object creation.
    *   **Alternative:** Since we just need to iterate unvisited items in a range, and remove them.
    *   Can we use a `set` of unvisited indices for each group?
        *   Query: Find intersection of `[L, R]` and `set`.
        *   In Python, `set` intersection is $O(\min(|A|, |B|))$. If we construct the range set every time, it's slow.
        *   But we can use `bisect` to find the range of indices in the sorted list, then iterate.
        *   To skip visited, we need to know which ones are visited.
        *   **Idea:** Use a `set` of *visited indices* for each group.
        *   When querying range $[L, R]$ (indices in sorted list):
            *   We need to iterate $i$ from $L$ to $R$.
            *   If $i$ is in `visited_indices`, skip.
            *   Else, mark visited, increment count.
            *   **Problem:** Still $O(N)$ if many are visited.
    *   **Back to Segment Tree:** It's the only way to skip efficiently.
    *   **Simplified Segment Tree:**
        *   We don't need a full class. We can use an array-based iterative segment tree.
        *   Since the total number of elements across all trees is $N$, we can flatten them? No, sizes vary.
        *   Just create a list of lists for the trees.
        *   `tree[x]` = list representing the tree for houses at X.
        *   Size of tree = $2^{\lceil \log_2 k \rceil + 1}$.
        *   This is feasible. $N=200,000$. Sum of sizes $\approx 4N$.
        *   Operations: `update(pos, 0)`, `query_sum(L, R)`, `find_first(L, R)`.
        *   `find_first`: Walk down the tree to find the leftmost leaf with value 1 in range $[L, R]$.
        *   Repeat until no more found.

**Wait, is there a simpler Pythonic way?**
Maybe the constraints allow $O(N \sqrt{N})$? No.
Maybe the test cases are weak?
Let's assume the Segment Tree approach is required.

**Wait, one more check:**
Is it possible to just use `bisect` and a `set` of visited *coordinates*?
No, because we need to avoid re-scanning.
What if we store the unvisited houses in a `set` for each X?
`unvisited_x[x] = set of y`.
Query: Range $[y1, y2]$.
We need to iterate $y \in [y1, y2]$ such that $y \in unvisited\_x[x]$.
Python sets don't support range iteration.
However, we can convert the set to a sorted list? No, that's $O(k)$.
**Conclusion:** Segment Tree is the way.

**Implementation Details:**
*   **Segment Tree Class:**
    *   `__init__(n)`: creates array of size $2n$.
    *   `build()`: init with 1s.
    *   `update(i, val)`: set leaf, update parents.
    *   `query_sum(l, r)`: sum in range.
    *   `find_first(l, r)`: returns smallest index $i \in [l, r]$ with value 1, or -1.
        *   This is the tricky part. Standard segment tree `query` returns sum. To find index, we need to descend.
        *   Algorithm for `find_first(l, r)`:
            *   Check if `query_sum(l, r) == 0`. If so, return -1.
            *   Decompose $[l, r]$ into $O(\log n)$ canonical nodes.
            *   Iterate these nodes from left to right.
            *   For the first node that has sum > 0, descend into it to find the leftmost leaf with 1.
            *   Return that index.
            *   If found, update it (set to 0) and recurse to find next.
*   **Data Structures:**
    *   `trees_x`: dict mapping `x_coord` -> `SegmentTree` object (or array).
    *   `trees_y`: dict mapping `y_coord` -> `SegmentTree` object.
    *   Also need to map `y` to rank in `by_x[x]` and `x` to rank in `by_y[y]`.
    *   Actually, `by_x[x]` stores `(y, original_index)`. We sort by `y`. The Segment Tree manages indices $0..k-1$.
    *   When querying vertical move at $X=x$, range $[y_{min}, y_{max}]$:
        *   Get list `L = by_x[x]`.
        *   Use `bisect_left` on `L` (comparing by `y`) to find `start_idx`.
        *   Use `bisect_right` to find `end_idx`.
        *   Query tree for sum in `[start_idx, end_idx - 1]`.
        *   While sum > 0:
            *   Find first index `idx` in range with value 1.
            *   Mark house `L[idx]` as visited.
            *   Update tree `idx` to 0.
            *   Decrement sum (or re-query).
*   **Complexity:**
    *   Sorting: $O(N \log N)$.
    *   Building Trees: $O(N)$.
    *   Moves: $M$ moves.
        *   Bisect: $O(\log N)$.
        *   Query Sum: $O(\log N)$.
        *   Finding/Removing: Each house removed once. Total removals $N$. Each removal $O(\log N)$.
        *   Total per move: $O(\log N)$ (if no new houses) + $O(\text{new houses} \times \log N)$.
        *   Amortized total: $O(M \log N + N \log N)$.
    *   This fits within time limits.

**Corner Cases:**
*   No houses on the path.
*   Path starts/ends at same point (distance 0).
*   Coordinates negative.
*   Large coordinates (handled by Python).
*   $N=1, M=1$.

**Code Structure:**
1.  Read Input.
2.  Prepare `by_x` and `by_y` lists.
3.  Build Segment Trees for each unique X and Y.
4.  Simulate moves.
5.  Output result.

**Segment Tree Optimization for Python:**
*   Use a flat list for the tree.
*   Size: Power of 2 $\ge$ length.
*   `find_first` logic needs to be efficient.
*   Alternatively, since we only need to find *any* unvisited in range and remove it, we can just loop:
    *   `idx = find_first(l, r)`
    *   while `idx != -1`: process, update, `idx = find_first(l, r)` (re-query range).
    *   Re-querying the whole range is $O(\log N)$. Total $O(N \log N)$. This is fine.

Let's refine `find_first(l, r)`:
Standard segment tree `query` returns sum.
To find the first index with value 1 in $[L, R]$:
1.  Check if `query(L, R) == 0`. Return -1.
2.  We can implement a function `find_first(node, node_l, node_r, q_l, q_r)`:
    *   If range disjoint or sum[node] == 0: return -1.
    *   If leaf: return node_l.
    *   Check left child. If overlap and sum[left] > 0: return `find_first(left...)`.
    *   Else: return `find_first(right...)`.
This is $O(\log N)$.

Let's write the code.

## worker: Implement the solution using the Segment Tree appr
The solution implements a Segment Tree for each unique X and Y coordinate to efficiently manage the set of unvisited houses.
1.  **Data Structures**:
    *   `by_x` and `by_y`: Dictionaries mapping coordinates to lists of houses (sorted by the other coordinate).
    *   `trees_x` and `trees_y`: Dictionaries mapping coordinates to Segment Trees. Each tree manages the "unvisited" status of houses on that line. Initially, all houses are unvisited (value 1). When a house is visited, its value is updated to 0.
2.  **Segment Tree Operations**:
    *   `query_sum(l, r)`: Counts how many unvisited houses are in the index range `[l, r]`.
    *   `find_first(l, r)`: Finds the smallest index in `[l, r]` that has a value of 1 (unvisited). This is crucial to avoid re-scanning visited houses repeatedly.
    *   `update(idx, 0)`: Marks a house as visited.
3.  **Simulation**:
    *   For each move, we determine the range of coordinates covered.
    *   Using binary search (`bisect`), we map the coordinate range to the index range in the sorted list of houses for that line.
    *   We query the Segment Tree for unvisited houses in this index range.
    *   We iterate, finding and marking each unvisited house, incrementing the count.
    *   This ensures that each house is processed (marked as visited) exactly once, leading to an overall complexity of $O((N + M) \log N)$.
4.  **Complexity**:
    *   Sorting: $O(N \log N)$.
    *   Building Trees: $O(N)$.
    *   Moves: $M$ moves. Each move involves binary search ($O(\log N)$) and potentially updating visited houses. Since each house is updated once, the total update cost is $O(N \log N)$. The query cost per move is $O(\log N)$. Total: $O((N + M) \log N)$.
5.  **Edge Cases**:
    *   No houses on the path: `query_sum` returns 0, loop doesn't run.
    *   Large coordinates: Handled by Python's arbitrary precision integers.
    *   Negative coordinates: Handled correctly by sorting and bisect.

## worker: Implement the Segment Tree logic within the `solve
The solution implements a Segment Tree for each unique X and Y coordinate to efficiently manage the set of unvisited houses.
1.  **Data Structures**:
    *   `by_x` and `by_y`: Dictionaries mapping coordinates to lists of houses (sorted by the other coordinate).
    *   `trees_x` and `trees_y`: Dictionaries mapping coordinates to Segment Trees. Each tree manages the "unvisited" status of houses on that line. Initially, all houses are unvisited (value 1). When a house is visited, its value is updated to 0.
2.  **Segment Tree Operations**:
    *   `query_sum(l, r)`: Counts how many unvisited houses are in the index range `[l, r]`.
    *   `find_first(l, r)`: Finds the smallest index in `[l, r]` that has a value of 1 (unvisited). This is crucial to avoid re-scanning visited houses repeatedly.
    *   `update(idx, 0)`: Marks a house as visited.
3.  **Simulation**:
    *   For each move, we determine the range of coordinates covered.
    *   Using binary search (`bisect`), we map the coordinate range to the index range in the sorted list of houses for that line.
    *   We query the Segment Tree for unvisited houses in this index range.
    *   We iterate, finding and marking each unvisited house, incrementing the count.
    *   This ensures that each house is processed (marked as visited) exactly once, leading to an overall complexity of $O((N + M) \log N)$.
4.  **Complexity**:
    *   Sorting: $O(N \log N)$.
    *   Building Trees: $O(N)$.
    *   Moves: $M$ moves. Each move involves binary search ($O(\log N)$) and potentially updating visited houses. Since each house is updated once, the total update cost is $O(N \log N)$. The query cost per move is $O(\log N)$. Total: $O((N + M) \log N)$.
5.  **Edge Cases**:
    *   No houses on the path: `query_sum` returns 0, loop doesn't run.
    *   Large coordinates: Handled by Python's arbitrary precision integers.
    *   Negative coordinates: Handled correctly by sorting and bisect.

## worker: Verify the solution against Sample 1 and Sample 2,
The solution implements a Segment Tree for each unique X and Y coordinate to efficiently manage the set of unvisited houses.
1.  **Data Structures**:
    *   `by_x` and `by_y`: Dictionaries mapping coordinates to lists of houses (sorted by the other coordinate).
    *   `trees_x` and `trees_y`: Dictionaries mapping coordinates to Segment Trees. Each tree manages the "unvisited" status of houses on that line. Initially, all houses are unvisited (value 1). When a house is visited, its value is updated to 0.
2.  **Segment Tree Operations**:
    *   `query_sum(l, r)`: Counts how many unvisited houses are in the index range `[l, r]`.
    *   `find_first(l, r)`: Finds the smallest index in `[l, r]` that has a value of 1 (unvisited). This is crucial to avoid re-scanning visited houses repeatedly.
    *   `update(idx, 0)`: Marks a house as visited.
3.  **Simulation**:
    *   For each move, we determine the range of coordinates covered.
    *   Using binary search (`bisect`), we map the coordinate range to the index range in the sorted list of houses for that line.
    *   We query the Segment Tree for unvisited houses in this index range.
    *   We iterate, finding and marking each unvisited house, incrementing the count.
    *   This ensures that each house is processed (marked as visited) exactly once, leading to an overall complexity of $O((N + M) \log N)$.
4.  **Complexity**:
    *   Sorting: $O(N \log N)$.
    *   Building Trees: $O(N)$.
    *   Moves: $M$ moves. Each move involves binary search ($O(\log N)$) and potentially updating visited houses. Since each house is updated once, the total update cost is $O(N \log N)$. The query cost per move is $O(\log N)$. Total: $O((N + M) \log N)$.
5.  **Edge Cases**:
    *   No houses on the path: `query_sum` returns 0, loop doesn't run.
    *   Large coordinates: Handled by Python's arbitrary precision integers.
    *   Negative coordinates: Handled correctly by sorting and bisect.

## worker: Run the code against Sample 1 and Sample 2 to veri
The code implements the solution using a Segment Tree for each unique X and Y coordinate to efficiently manage the set of unvisited houses.
1.  **Data Structures**:
    *   `by_x` and `by_y`: Dictionaries mapping coordinates to lists of houses (sorted by the other coordinate).
    *   `trees_x` and `trees_y`: Dictionaries mapping coordinates to Segment Trees. Each tree manages the "unvisited" status of houses on that line. Initially, all houses are unvisited (value 1). When a house is visited, its value is updated to 0.
2.  **Segment Tree Operations**:
    *   `query_sum(l, r)`: Counts how many unvisited houses are in the index range `[l, r]`.
    *   `find_first(l, r)`: Finds the smallest index in `[l, r]` that has a value of 1 (unvisited). This is crucial to avoid re-scanning visited houses repeatedly.
    *   `update(idx, 0)`: Marks a house as visited.
3.  **Simulation**:
    *   For each move, we determine the range of coordinates covered.
    *   Using binary search (`bisect`), we map the coordinate range to the index range in the sorted list of houses for that line.
    *   We query the Segment Tree for unvisited houses in this index range.
    *   We iterate, finding and marking each unvisited house, incrementing the count.
    *   This ensures that each house is processed (marked as visited) exactly once, leading to an overall complexity of $O((N + M) \log N)$.
4.  **Complexity**:
    *   Sorting: $O(N \log N)$.
    *   Building Trees: $O(N)$.
    *   Moves: $M$ moves. Each move involves binary search ($O(\log N)$) and potentially updating visited houses. Since each house is updated once, the total update cost is $O(N \log N)$. The query cost per move is $O(\log N)$. Total: $O((N + M) \log N)$.
5.  **Edge Cases**:
    *   No houses on the path: `query_sum` returns 0, loop doesn't run.
    *   Large coordinates: Handled by Python's arbitrary precision integers.
    *   Negative coordinates: Handled correctly by sorting and bisect.

## worker: finalize
The solution implements a Segment Tree for each unique X and Y coordinate to efficiently manage the set of unvisited houses.
1.  **Data Structures**:
    *   `by_x` and `by_y`: Dictionaries mapping coordinates to lists of houses (sorted by the other coordinate).
    *   `trees_x` and `trees_y`: Dictionaries mapping coordinates to Segment Trees. Each tree manages the "unvisited" status of houses on that line. Initially, all houses are unvisited (value 1). When a house is visited, its value is updated to 0.
2.  **Segment Tree Operations**:
    *   `query_sum(l, r)`: Counts how many unvisited houses are in the index range `[l, r]`.
    *   `find_first(l, r)`: Finds the smallest index in `[l, r]` that has a value of 1 (unvisited). This is crucial to avoid re-scanning visited houses repeatedly.
    *   `update(idx, 0)`: Marks a house as visited.
3.  **Simulation**:
    *   For each move, we determine the range of coordinates covered.
    *   Using binary search (`bisect`), we map the coordinate range to the index range in the sorted list of houses for that line.
    *   We query the Segment Tree for unvisited houses in this index range.
    *   We iterate, finding and marking each unvisited house, incrementing the count.
    *   This ensures that each house is processed (marked as visited) exactly once, leading to an overall complexity of $O((N + M) \log N)$.
4.  **Complexity**:
    *   Sorting: $O(N \log N)$.
    *   Building Trees: $O(N)$.
    *   Moves: $M$ moves. Each move involves binary search ($O(\log N)$) and potentially updating visited houses. Since each house is updated once, the total update cost is $O(N \log N)$. The query cost per move is $O(\log N)$. Total: $O((N + M) \log N)$.
5.  **Edge Cases**:
    *   No houses on the path: `query_sum` returns 0, loop doesn't run.
    *   Large coordinates: Handled by Python's arbitrary precision integers.
    *   Negative coordinates: Handled correctly by sorting and bisect.
