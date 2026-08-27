
## ideation
The core difficulty is efficiently determining which houses lie on each segment of Santa's path. Since $N$ and $M$ are up to $2 \times 10^5$, a naive $O(N \cdot M)$ check is too slow. We need a faster way to query houses on axis-aligned segments.

Key observations:
1. Moves are strictly horizontal or vertical.
2. A house $(X_i, Y_i)$ is on a horizontal move from $(x_1, y)$ to $(x_2, y)$ if $Y_i = y$ and $X_i$ is between $\min(x_1, x_2)$ and $\max(x_1, x_2)$.
3. Similarly for vertical moves.

Approach:
1. Preprocess houses into two dictionaries:
   - `by_y`: maps Y-coordinate to a sorted list of X-coordinates of houses at that Y.
   - `by_x`: maps X-coordinate to a sorted list of Y-coordinates of houses at that X.
2. Also maintain a set `visited` to track distinct houses already counted.
3. For each move:
   - Determine the segment (start and end points).
   - If horizontal: look up `by_y[y]` and use binary search to find houses with X in the range $[\min(x_{start}, x_{end}), \max(x_{start}, x_{end})]$. For each such house, if not in `visited`, add it and increment count.
   - If vertical: look up `by_x[x]` and use binary search to find houses with Y in the range $[\min(y_{start}, y_{end}), \max(y_{start}, y_{end})]$. Similarly mark visited.
4. Important: A house might be encountered multiple times. We only count it once. Using a set ensures this.
5. Edge case: The starting point is not a house (per constraints). But during moves, we might pass through a house. We need to check if the house lies on the segment including endpoints.

Pitfalls:
- Large coordinates: Use 64-bit integers (Python handles this automatically).
- Efficiency: Binary search per move is $O(\log N)$, and we process each house at most once across all moves (since we skip visited houses). However, we still need to iterate through all houses on a segment. In the worst case, if many houses are on one segment, it could be slow. But note: each house is added to `visited` at most once. So the total number of successful checks (where we add to visited) is $N$. The number of failed checks (house already visited) could be large. To avoid TLE, we should not iterate over already visited houses repeatedly.

Better approach for efficiency:
- Instead of iterating over all houses on a segment and checking if visited, we can remove visited houses from the data structures. But removing from a sorted list is expensive.
- Alternative: Use a set for visited houses, and when querying, we still iterate. But if many houses are already visited, we might do redundant work.
- However, note that each house is on only one horizontal line and one vertical line. Once visited, it's marked. The issue is if we query a segment that has many already-visited houses.
- To mitigate: We can use the fact that we only care about unvisited houses. But the data structure doesn't support efficient removal.
- Another idea: Since each house is visited at most once, the total number of "successful" visits is $N$. The total number of "unsuccessful" checks (house already visited) could be large if we're not careful. But in practice, if we just iterate and check the set, the worst case is $O(N \cdot M)$ if every move checks all houses. That's bad.

Wait, let's reconsider: The number of houses on a segment can be large, but each house is only added to `visited` once. However, we might check the same visited house multiple times. To avoid this, we can remove houses from the dictionaries once they are visited. But removing from a sorted list is $O(N)$ per removal, which is too slow.

Alternative efficient approach:
- Use a set for visited houses.
- For each segment, use binary search to find the range of houses.
- Iterate through the houses in that range. For each house, if not visited, mark it and increment count. If visited, skip.
- The problem is that if a segment has many visited houses, we still iterate over them.

But note: Each house is on only one horizontal line and one vertical line. Once it's visited, it's marked. The total number of times we encounter a visited house is bounded by the number of segments that pass through it. In the worst case, a house could be on many segments? No, because Santa's path is a sequence of moves. A house is at a fixed point. It can be on at most two segments (the horizontal and vertical segments that pass through it). But actually, Santa might pass through the same house multiple times via different segments? No, because once visited, we skip. But we still check it.

Actually, the worst-case scenario: Suppose all houses are on the x-axis, and Santa makes many horizontal moves along the x-axis. Each move would check all houses. That's $O(N \cdot M)$, which is too slow.

We need a better way. Idea: Remove visited houses from the data structure. But as noted, removal from sorted list is expensive.

Alternative: Use a balanced BST or a data structure that supports efficient deletion and range queries. In Python, we don't have a built-in one. But we can use a set for visited houses and hope that the test cases are not worst-case? No, we need to be efficient.

Another idea: Instead of storing sorted lists, we can use a dictionary that maps coordinate to a set of houses, but then range queries are not efficient.

Wait, note that for a horizontal move at y, we only care about houses at that y. We can store for each y, a sorted list of x's. When we visit a house, we can mark it as visited. But to avoid iterating over visited houses, we can use a pointer or something? Not straightforward.

Alternatively, we can use a segment tree or Fenwick tree? But the coordinates are large.

But note: The number of distinct y-coordinates that have houses is at most N. Similarly for x. We can compress coordinates? But the moves are arbitrary.

Actually, the key is: each house is visited at most once. The total number of "successful" visits is N. The total number of "unsuccessful" checks (visiting a house that is already visited) is the problem. How many times can a house be checked without being visited? Only when it is on a segment but already visited. Since a house is at a fixed point, it can be on at most two segments in the entire path? No, because Santa might pass through the same point multiple times. But once visited, we skip. However, we still check it.

But note: The path is continuous. A house is at a specific point. It can be on multiple segments only if Santa passes through that point multiple times. But each time he passes through, we check the house. However, after the first time, it's marked visited, and we skip. But we still do the binary search and iterate over the houses in the range. The iteration might include many visited houses.

To avoid iterating over visited houses, we can remove them from the sorted list. But removal is expensive.

Alternative: Use a set for visited houses, and for each segment, we do a binary search to get the range, and then we iterate. But we can break early? No.

Another idea: Instead of storing all houses, we can store the houses in a way that allows efficient removal. In Python, we can use a list and mark as removed, but then the list becomes sparse. Or we can use a balanced BST via a third-party library, but we can't.

Wait, there's a simpler observation: The total number of houses is N. Each house is checked at most a constant number of times? No, as argued, it could be checked many times.

But note: For a given horizontal line y, the houses are stored in a sorted list. When we do a query for a segment on that line, we get a range of indices. We then iterate over the houses in that range. If a house is already visited, we skip. But if many houses in the range are already visited, we still iterate.

However, each house is visited only once. So the total number of "successful" iterations (where we add to visited) is N. The total number of "unsuccessful" iterations is the number of times we check a house that is already visited. How many times can a house be checked? It depends on how many segments pass through it. In the worst case, a house could be on O(M) segments? Actually, no: because the path is a sequence of moves, and a house is at a fixed point. The house is on a segment if the segment covers that point. Since the path is continuous, the house can be on at most two segments that are adjacent? Not necessarily: Santa might go back and forth.

Example: Houses at (0,0). Santa starts at (-1,0), moves R to (1,0) -> passes (0,0). Then moves L to (-1,0) -> passes (0,0) again. Then R to (1,0) again. So the house (0,0) is checked in every move. If there are M moves, and all moves are along the same line, then we check the house M times. And if there are N houses all on the same line, and we make M moves along that line, then total checks are O(N*M), which is 4e10, too slow.

So we must avoid checking already visited houses.

Solution: Remove visited houses from the data structure. But how to do it efficiently?

For a sorted list, removal is O(N) per removal. Total O(N^2) worst-case, which is 4e10, too slow.

Alternative: Use a set for visited houses, and for each segment, we do a binary search to get the range, and then we iterate. But we can skip visited houses quickly? No, we still have to iterate.

Another idea: Instead of storing the houses in sorted lists, we can store them in a dictionary that maps (x,y) to a boolean, but then range queries are not efficient.

Wait, we can use the following: For each horizontal line y, we have a sorted list of x's. We also maintain a set of visited houses. When we query a segment on y, we get the range of x's. We then iterate over the houses in that range. For each house, if not visited, we mark it and remove it from the sorted list? But removal from a list is O(N).

But note: We can use a linked list? Not in Python.

Alternatively, we can use a balanced BST. In Python, we don't have one in the standard library. But we can use a skip list or something? Not practical.

Another idea: Use a Fenwick tree or segment tree over the compressed coordinates. But the coordinates are large, so we need to compress. However, the moves are arbitrary, so the segments might not align with the house coordinates.

But note: We only care about the houses. The segments are defined by the moves. We can compress the x-coordinates of the houses and the y-coordinates of the houses. But the segments might cover ranges that don't include any houses, but we only care about houses.

Actually, we can do this:
- Collect all x-coordinates of houses and all y-coordinates of houses.
- Compress them to ranks.
- Build a 2D structure? But 2D is complex.

Alternatively, we can use the following efficient method:
- For each horizontal line y, we have a sorted list of x's. We also maintain a pointer for each line that indicates the next unvisited house? But the queries are arbitrary ranges.

This is tricky.

Let me think of a different approach: Instead of iterating over houses on the segment, we can use the fact that the total number of houses is N. We can store the houses in a set for O(1) lookup, but then how to find houses on a segment? We need to iterate over possible houses.

But the segment might cover a large area. We cannot iterate over all houses.

So we must use the sorted lists for range queries.

To avoid the O(N*M) worst-case, we need to ensure that each house is checked only a constant number of times. How? By removing it from the data structure once visited.

But removal from a sorted list is expensive. However, we can use a lazy removal: mark the house as visited, and when we iterate, we skip visited houses. But then we still iterate over them.

But note: The total number of houses is N. The total number of "successful" checks is N. The total number of "unsuccessful" checks is the number of times we check a visited house. If we can bound the number of unsuccessful checks, we are good.

In the worst case, as argued, it can be O(N*M). So we must remove.

How to remove efficiently? We can use a balanced BST. In Python, we can use the `sortedcontainers` library, but it's not available. So we have to use standard library.

Another idea: Use a set for visited houses, and for each segment, we do a binary search to get the range of indices in the sorted list. Then, we can iterate over the indices, and for each index, if the house is not visited, we mark it and remove it from the sorted list. But removal from a list by index is O(N) because it shifts elements.

Total time for removals: O(N^2) in worst-case, which is 4e10, too slow.

We need a data structure that supports:
- Range query: get all elements in [L, R].
- Delete an element.
- And we want the total time for all operations to be O((N+M) log N) or something.

This is challenging.

Alternative approach: Instead of storing houses in sorted lists per line, we can store all houses in a single 2D grid? But coordinates are large.

Or, we can use a KD-tree? But building a KD-tree is O(N log N), and query is O(sqrt(N)) per query, total O(M sqrt(N)), which for 2e5 is about 2e5 * 450 = 9e7, which might be acceptable in Pyton? But implementing a KD-tree is complex and might be slow in Python.

Given the constraints and the fact that this is a competitive programming problem, there must be a simpler way.

Let me read the constraints again: N, M up to 2e5. Coordinates up to 1e9.

Another idea: Use a set for visited houses. For each segment, we do a binary search to find the range of houses. Then, we iterate over the houses in that range. But instead of iterating over all, we can use the fact that the houses are sorted, and we can skip visited ones by using a pointer? But the queries are arbitrary.

Wait, here's a key insight: Each house is visited at most once. The total number of times we encounter a house (whether visited or not) is the number of segments that cover it. But a house is at a specific point. It is covered by a segment if the segment passes through that point. How many segments can pass through a given point? In the worst case, O(M). So total checks could be O(N*M).

But note: The path is continuous. A house is on a segment if the segment covers the house's coordinates. For a horizontal move at y, the house must have Y_i = y. So for a given house, it is only relevant for horizontal moves at its y-coordinate and vertical moves at its x-coordinate. So for a house at (x_i, y_i), it is only checked during:
- Horizontal moves that are at y_i and cover x_i.
- Vertical moves that are at x_i and cover y_i.

How many such moves can there be? In the worst case, all M moves could be at the same y_i or x_i. So still O(M) per house.

So total checks O(N*M).

This is not acceptable.

We must remove visited houses from the data structure.

How to do it efficiently in Python with standard library?

We can use a dictionary that maps y to a sorted list of x's. When we visit a house, we remove it from the sorted list. But removal from a sorted list is O(N) per removal.

Total time for removals: O(N^2). With N=2e5, N^2=4e10, which is too slow.

So we need a different data structure.

Idea: Use a balanced BST. In Python, we can simulate a balanced BST using a skip list or a red-black tree, but it's complex.

Alternatively, we can use a Fenwick tree or segment tree over the compressed coordinates for each line.

For each horizontal line y, we have a set of x-coordinates. We can compress the x-coordinates for that line. Then, build a Fenwick tree or segment tree for that line to support range queries and point deletion.

But there are up to N lines. Building a Fenwick tree for each line: the total size is N, so it's feasible.

Steps:
1. Group houses by y-coordinate. For each y, collect the x-coordinates and sort them. Also, compress these x-coordinates to ranks 0,1,2,...,k-1 for that y.
2. For each y, build a Fenwick tree (or segment tree) that supports:
   - Query: count of houses in [L, R] (but we need the actual houses, not just count).
   - Actually, we need to retrieve the houses in the range. But Fenwick tree is for sums. We can use a segment tree that stores the list of houses? But then deletion is still expensive.

Alternatively, we can use a segment tree that stores the minimum and maximum, but that doesn't help for retrieval.

Another idea: Use a set for each line, but then range queries are not efficient.

This is getting complicated.

Let me search for similar problems. This is a classic problem: "count points on a path" with axis-aligned moves.

Standard solution: Use a dictionary mapping y to a sorted list of x's, and similarly for x to y's. Then, for each move, use binary search to find the range, and iterate. To avoid TLE, remove visited houses from the sorted list. But removal from a list is O(N).

However, note that the total number of removals is N. The total time for removals is sum over removals of the cost. If we use a linked list, removal is O(1), but then binary search is not possible.

So we need a data structure that supports binary search and O(log N) deletion. A balanced BST does that.

In Python, we can use the `bisect` module for binary search, and for deletion, we can use a balanced BST from a third-party library, but we can't.

So what to do?

Perhaps the test cases are not worst-case. Or perhaps there is a different approach.

Another idea: Instead of removing, we can use a set for visited houses, and for each segment, we do a binary search to get the range of indices in the sorted list. Then, we iterate over the indices, and for each index, if the house is not visited, we mark it and also mark it for removal. But then we have to remove it from the sorted list, which is O(N).

But if we do lazy removal: after processing all moves, we can clean up, but during the moves, we still iterate.

Perhaps we can use a different strategy: Process the moves in order, and for each move, we only consider houses that are not visited. But how to quickly find unvisited houses in a range?

We can use a DSU-like structure or a linked list of unvisited houses for each line.

For each horizontal line y, we have a sorted list of x's. We also maintain a doubly linked list of the unvisited houses on that line. When we visit a house, we remove it from the linked list. Then, for a range query, we can traverse the linked list within the range. But the linked list is sorted by x, so we can find the start of the range using binary search on the x-coordinates, and then traverse the linked list until we go out of range.

The cost per house visited is O(1) for removal from the linked list. The cost for traversal is proportional to the number of unvisited houses in the range. Since each house is visited once, the total traversal cost over all moves is O(N). The cost for binary search per move is O(log N). So total time O(M log N + N), which is acceptable.

How to implement:
- For each y, we have:
  - `xs`: a sorted list of x-coordinates of houses at y.
  - `linked_list`: a doubly linked list of the houses at y, sorted by x. Each node has `x`, `prev`, `next`, and `visited` flag (or we remove it).
  - Also, we need to quickly find the node in the linked list that corresponds to the start of the range. We can do a binary search on `xs` to find the index of the first x >= L, and then we need a way to get the node at that index. So we can store an array of nodes for each y, indexed by the rank in `xs`.

Steps for a horizontal move at y from x1 to x2 (assume x1 <= x2):
- If there are no houses at y, skip.
- Otherwise, get the sorted list `xs` for y.
- Use bisect_left to find the index `i` of the first x >= min(x1,x2).
- Use bisect_right to find the index `j` of the last x <= max(x1,x2) (actually, bisect_right returns the insertion point, so the range of indices is [i, j-1]).
- Then, starting from the node at index `i` in the linked list array, traverse the linked list until we go beyond x2 or until the node is None.
- For each node in the range that is not visited (but we remove it when visited, so we only see unvisited ones), mark it as visited, add to the global visited set, increment count, and remove it from the linked list (and also from the array? but we don't need the array anymore for this node).

But when we remove a node from the linked list, we update the prev and next pointers. And we also need to remove it from the array? Not necessary, because we are traversing via the linked list, and we start from the node at index `i`, but if that node is removed, then the linked list is broken.

So we need to ensure that the linked list is up-to-date. When we remove a node, we update the linked list, but the array of nodes remains, and the node might be removed. So when we start at index `i`, the node at that index might have been removed. So we need to skip removed nodes.

This is messy.

Alternative: Instead of an array of nodes, we can store for each house a pointer to its node in the linked list. And for the linked list, we have a dummy head or something.

But then, to find the start of the range, we do a binary search on the `xs` list to get the index, and then get the node from the array. But if that node has been removed, then the linked list from that node might not be valid because its prev or next might be None or point to removed nodes.

So we need a way to find the first unvisited node in the range.

This is complicated.

Given the time, and since this is a thought process, I'll go with the following plan, hoping that the test cases are not worst-case, or that the constant factor is small:

- Use two dictionaries: `by_y` and `by_x`, mapping coordinate to a sorted list of the other coordinate.
- Use a set `visited` for visited houses.
- For each move, determine the segment.
- For horizontal move at y from x1 to x2:
  - If y not in `by_y`, skip.
  - Else, get the list `L = by_y[y]`.
  - Use bisect_left to find the start index: `i = bisect.bisect_left(L, min(x1,x2))`
  - Use bisect_right to find the end index: `j = bisect.bisect_right(L, max(x1,x2))`
  - Then, for k in range(i, j):
      - x = L[k]
      - if (x,y) not in visited:
          - add (x,y) to visited
          - increment count
          - # Note: we do not remove from L, because removal is expensive.
- Similarly for vertical moves.

This is O(N) per move in the worst-case, leading to O(N*M) total, which is 4e10, too slow.

But perhaps in practice, the number of houses on a segment is small. Or the test cases are weak.

However, the problem constraints say N, M up to 2e5, so we must have an efficient solution.

After research, I recall that in competitive programming, for this type of problem, the intended solution is to use the sorted lists and remove visited houses, and the total time is O((N+M) log N) if removal is O(log N). But in Python, with lists, removal is O(N).

So for Python, we might need to use a different approach.

Another idea: Use a set for visited houses, and for each segment, we do a binary search to get the range, and then we iterate. But we can use the fact that the houses are sorted, and we can skip visited houses by using a pointer that advances. But the queries are not monotonic.

Perhaps we can process the moves in a way that we only check each house once. But the path is given in order.

I think the best shot is to use the sorted lists and hope that the test cases are not worst-case. Or use a balanced BST simulation.

Since this is a thought process, I'll outline the code with the sorted lists and set, and hope for the best. If it TLEs, then we need a better method.

But the problem says "do not directly test on the sample inputs", so we must submit correct code.

Given the constraints, I think the intended solution in C++ would use `std::set` for each line, which supports O(log N) deletion and range queries. In Python, we don't have that.

So for Python, we might need to use a different strategy.

Let me try this: Instead of storing the houses in sorted lists per line, we can store all houses in a single list, and use a 2D grid? No.

Another idea: Use a dictionary that maps (x,y) to a boolean, and then for each segment, we iterate over the possible houses? But the segment might cover a large area.

This is not feasible.

Perhaps the number of houses on any segment is small on average.

I think for the sake of completing, I'll implement the sorted list approach with set, and hope that the test cases are not worst-case. Or perhaps the constant factor is small.

But let's calculate: In the worst-case, if all houses are on the x-axis, and we make M moves along the x-axis, then each move checks all N houses. Total 2e5 * 2e5 = 4e10 checks, which in Python might take 100 seconds, but the time limit is usually 2 seconds. So it will TLE.

Therefore, we must remove visited houses.

How to remove efficiently? We can use a linked list for each line, and for binary search, we can use the sorted list of x's, but when we remove a house, we remove it from the linked list, and also from the sorted list? But removing from sorted list is O(N).

But if we use a linked list, we can't do binary search.

So we need a data structure that supports both.

I recall that in Python, we can use a balanced BST by using the `sortedcontainers` library, but it's not available.

So perhaps we can use a Fenwick tree for each line to mark visited houses, and then for range query, we can use binary search on the Fenwick tree to find the next unvisited house.

For each horizontal line y, we have a list of x's. We compress the x's to ranks. Then, we build a Fenwick tree that supports:
- Point update: set a position to 1 (visited) or 0 (unvisited). Initially all 0.
- Query: find the next unvisited house in [L, R].

But Fenwick tree is for sums. We can use it to find the k-th unvisited house, but we need all unvisited houses in [L, R].

We can do: while there is an unvisited house in [L, R], find the first one, process it, mark it visited, and repeat.

The cost per house visited is O(log N) for the Fenwick tree operations. The total cost for all houses is O(N log N). The cost for the moves: for each move, we do a binary search to find the range, and then we repeatedly query for the next unvisited house in the range. The number of times we query is proportional to the number of unvisited houses in the range, which is at most the number of houses in the range, but since we remove them, the total over all moves is O(N log N) for the queries.

Additionally, for each move, we do a binary search on the x-coordinates to find the range of ranks, which is O(log N).

So total time O((M + N) log N), which is acceptable.

Implementation for one line (y-coordinate fixed):
- Let `xs` be the sorted list of x-coordinates of houses at y.
- Let `n = len(xs)`.
- Create an array `fenw` of size n+1 for Fenwick tree, initialized to 0.
- Also, we need to map x-coordinate to rank. We can use a dictionary or bisect.

For a horizontal move at y from x1 to x2 (assume x1 <= x2):
- If no houses at y, skip.
- Find the rank range: 
  - `left_rank = bisect.bisect_left(xs, x1)`
  - `right_rank = bisect.bisect_right(xs, x2) - 1`  # because bisect_right returns the first index > x2, so the last index <= x2 is right_rank = bisect_right-1.
  - If left_rank > right_rank, skip.
- Then, while there is an unvisited house in [left_rank, right_rank]:
  - Find the smallest rank `r` in [left_rank, right_rank] such that the house is unvisited.
    - How? We can use the Fenwick tree to find the first unvisited house in [left_rank, right_rank].
    - We can do a binary search on the Fenwick tree for the first index in [left_rank, right_rank] with value 0 (unvisited).
    - Or, we can use the Fenwick tree to compute the number of visited houses in [left_rank, r-1], and find the smallest r such that the number of unvisited in [left_rank, r] >= 1.
    - Specifically, the number of unvisited in [left_rank, r] = (r - left_rank + 1) - (query(r) - query(left_rank-1)), where query(i) is the number of visited houses in [0, i].
    - We want the smallest r >= left_rank such that the number of unvisited in [left_rank, r] >= 1.
    - This is equivalent to: find the smallest r >= left_rank such that query(r) - query(left_rank-1) < (r - left_rank + 1).
    - But this is not monotonic in a simple way.

Alternatively, we can store the Fenwick tree for the visited status, and then use a separate structure to find the next unvisited.

A better way: Use a DSU or a linked list of unvisited houses for the ranks.

For the ranks on a line, we can maintain a set of unvisited ranks. But then range query is not efficient.

Given the complexity, and since this is a thought process, I'll implement the Fenwick tree approach for finding the next unvisited house.

For a fixed line with sorted x's of length n:
- Fenwick tree `fenw` of size n+1, where `fenw[i]` stores the number of visited houses in the first i ranks (1-indexed).
- To find the first unvisited house in [L, R] (ranks), we can do a binary search over the ranks in [L, R] for the first rank r such that the number of visited houses in [L, r] < (r - L + 1).

But this binary search is O(log^2 n) per query.

Total time O(M log^2 N + N log N), which is acceptable for N,M=2e5.

Steps for a move on a line with sorted x's `xs` of length n, and Fenwick tree `fenw` (1-indexed, size n+1):
- Let `L = bisect.bisect_left(xs, x_min)`  # x_min = min(x1,x2)
- Let `R = bisect.bisect_right(xs, x_max) - 1`  # x_max = max(x1,x2)
- If L > R, skip.
- While L <= R:
  - Find the smallest rank `r` in [L, R] such that the house at rank `r` is unvisited.
    - How? We can binary search for `r` in [L, R]:
      - low = L, high = R
      - while low <= high:
          - mid = (low+high)//2
          - visited_count = query_fenw(mid) - query_fenw(L-1)  # number of visited in [L, mid]
          - unvisited_count = (mid - L + 1) - visited_count
          - if unvisited_count > 0:
              - then there is an unvisited in [L, mid], so try left: high = mid-1, and remember mid as candidate.
          - else:
              - low = mid+1
      - If no unvisited found, break.
      - Otherwise, let `r` be the candidate (the smallest mid such that unvisited_count>0).
  - Now, the house at rank `r` is unvisited. Mark it as visited:
      - Update Fenwick tree: add 1 at position r.
      - Get the x-coordinate: `x = xs[r]`
      - The house is (x, y) for horizontal move.
      - If not in global visited set, add it and increment count.
      - But note: we are using the Fenwick tree to track visited for this line, so we don't need the global set for this line? But we need the global set to avoid double-counting if the same house is on both a horizontal and vertical move? No, a house is at a specific (x,y), so it is only on one horizontal line and one vertical line. But when we visit it via a horizontal move, we mark it in the horizontal line's Fenwick tree, and also in the vertical line's Fenwick tree? No, we only have one Fenwick tree per line.

Actually, a house is only on one horizontal line (its y-coordinate) and one vertical line (its x-coordinate). When we visit it via a horizontal move, we only need to mark it in the horizontal line's data structure. Similarly for vertical. But the global visited set is to ensure that we don't count the same house twice. However, since a house is only on one horizontal line and one vertical line, and we only visit it once (because after first visit, it's marked), we can use the Fenwick tree for that line to indicate it's visited, and then we don't need a global set? But wait, the house might be visited via a horizontal move and then later via a vertical move? No, because after the first visit, it's marked, so when we encounter it again, we skip.

But in our approach, for a horizontal move, we only consider the horizontal line's Fenwick tree. When we visit a house, we mark it in the horizontal line's Fenwick tree. Then, when a vertical move comes along the same house's x-coordinate, we will see that the house is not in the vertical line's data structure? No, the vertical line's data structure is separate.

Actually, the house is stored in both `by_y` and `by_x`. So when we visit it via a horizontal move, we mark it in the horizontal line's Fenwick tree, but not in the vertical line's. Then, when a vertical move comes, we will see the house in the vertical line's sorted list, and it will be unvisited in the vertical line's Fenwick tree, so we might visit it again.

So we need a global visited set to avoid double-counting.

So plan:
- Global set `visited_houses` for houses that have been counted.
- For each horizontal line y, we have:
  - `xs`: sorted list of x-coordinates.
  - `fenw`: Fenwick tree for visited status on this line (initially all 0).
  - `n = len(xs)`
- Similarly for vertical lines.

For a horizontal move at y from x1 to x2:
- If y not in `by_y`, skip.
- Get `xs = by_y[y]`, `fenw = fenw_by_y[y]`, `n = len(xs)`.
- Find rank range [L, R] as above.
- While L <= R:
  - Binary search for the smallest r in [L, R] such that the house at r is unvisited (i.e., the number of visited in [L, r] < (r - L + 1)).
  - If not found, break.
  - Let r be that rank.
  - Mark r as visited in `fenw`: update_fenw(r, 1).
  - Get x = xs[r].
  - House = (x, y).
  - If house not in `visited_houses`:
      - Add to `visited_houses`.
      - Increment count.
  - Set L = r + 1  # because we've processed r, and we want to continue from r+1. But note: there might be unvisited houses after r, so we set L = r+1 and continue the while loop.

Similarly for vertical moves.

This ensures that each house is processed at most once per line, and the total work is O(N log^2 N) for all moves, which is acceptable.

Let's implement this.

Note: Fenwick tree is 1-indexed.

Fenwick tree functions:
- `update(i, delta)`: add delta to index i (1-indexed).
- `query(i)`: sum from 1 to i.

For a range [L, R] in 0-indexed ranks, we convert to 1-indexed: L1 = L+1, R1 = R+1.

In the binary search for the first unvisited in [L, R] (0-indexed ranks), we consider ranks from L to R.

Let `low = L`, `high = R`.
`ans = -1`
While `low <= high`:
  `mid = (low+high)//2`
  # Number of visited in [L, mid] (0-indexed) = query_fenw(mid+1) - query_fenw(L)  [because query_fenw(i) is sum from 1 to i, so for 0-indexed rank r, the Fenwick index is r+1]
  `visited_count = fenw_query(mid+1) - fenw_query(L)`  # because L is 0-indexed, so Fenwick index for L is L+1, but query_fenw(L) is sum from 1 to L, which corresponds to ranks 0 to L-1. We want sum from rank L to mid.
  # Actually, the number of visited in ranks [L, mid] (0-indexed) is:
  #   = (number of visited in [0, mid]) - (number of visited in [0, L-1])
  #   = fenw_query(mid+1) - fenw_query(L)   [because fenw_query(i) is sum of first i ranks (0-indexed ranks 0 to i-1)]
  # So yes.
  `unvisited_count = (mid - L + 1) - visited_count`
  If `unvisited_count > 0`:
      `ans = mid`
      `high = mid - 1`
  Else:
      `low = mid + 1`

If `ans == -1`, break.

Then, process rank `ans`.

This should work.

Let's code accordingly.

Steps:
1. Read input.
2. Store houses in `by_y` and `by_x`:
   - `by_y`: dict mapping y to sorted list of x's.
   - `by_x`: dict mapping x to sorted list of y's.
3. For each y in `by_y`, create a Fenwick tree (list of zeros) of size len(xs)+1.
4. Similarly for `by_x`.
5. Initialize `visited_houses = set()`, `count = 0`.
6. Current position = (Sx, Sy).
7. For each move:
   - Update current position to new position.
   - Determine the segment: from (old_x, old_y) to (new_x, new_y).
   - If horizontal (same y):
        - y = old_y
        - x1, x2 = old_x, new_x
        - If y in `by_y`:
            - xs = by_y[y]
            - fenw = fenw_by_y[y]
            - n = len(xs)
            - L = bisect.bisect_left(xs, min(x1,x2))
            - R = bisect.bisect_right(xs, max(x1,x2)) - 1
            - If L <= R:
                - While L <= R:
                    - Binary search for first unvisited rank r in [L, R] as above.
                    - If not found, break.
                    - Mark r as visited in fenw: update_fenw(r+1, 1)
                    - x = xs[r]
                    - house = (x, y)
                    - If house not in visited_houses:
                        - visited_houses.add(house)
                        - count += 1
                    - L = r + 1
   - Similarly for vertical.
8. Print final position and count.

Note: The move is from (x,y) to (x',y'). We need to consider the segment between them. The houses on the segment are those with the same y (for horizontal) and x between min(x,x') and max(x,x').

Also, the starting point is not a house, and the ending point of a move might be a house, which is included.

Let's implement.

We'll create a Fenwick tree class or functions.

Since there are many lines, we'll store the Fenwick trees in dictionaries.

Let's code accordingly.

Note: The coordinates can be negative, but the Fenwick tree is over the ranks (indices), so it's fine.

Let's write the code.

## worker: Implement the solution using Fenwick trees for eff
The solution uses Fenwick trees (Binary Indexed Trees) to efficiently manage and query visited houses on each horizontal and vertical line. Here's the breakdown:

1. **Preprocessing**: Houses are grouped by their y-coordinates (for horizontal moves) and x-coordinates (for vertical moves). Each group is sorted to enable binary search.

2. **Fenwick Trees**: For each line (horizontal or vertical), a Fenwick tree is created to track which houses have been visited. The Fenwick tree supports:
   - `update(i, delta)`: Mark a house as visited (add 1 to its position).
   - `query(i)`: Count the number of visited houses in the range [1, i].

3. **Processing Moves**: For each move:
   - **Horizontal Move**: Determine the range of x-coordinates covered. Use binary search to find the corresponding ranks in the sorted list of x-coordinates for that y. Then, use another binary search over the Fenwick tree to find the first unvisited house in that rank range. Once found, mark it as visited, check if it's already counted globally, and update the count. Continue to the next unvisited house in the range.
   - **Vertical Move**: Similar to horizontal, but using y-coordinates and the corresponding Fenwick tree.

4. **Efficiency**: Each house is visited at most once. The binary search for the first unvisited house in a range takes O(log² N) time per query due to the nested binary search. With N houses and M moves, the total time complexity is O((N + M) log² N), which is efficient enough for the given constraints (N, M ≤ 2×10⁵).

5. **Global Visited Set**: A set `visited_houses` ensures that each house is counted only once, even if it's encountered multiple times during the path.
