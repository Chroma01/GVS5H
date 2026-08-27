
## ideation
The problem asks for the minimum number of vertices to delete from a tree to obtain a "Snowflake Tree" as an induced subgraph. A Snowflake Tree consists of a center vertex connected to x "blue" vertices, each of which is connected to the center and to exactly y "leaf" vertices, with no other connections.

The core difficulty is efficiently finding the largest induced subgraph that is a Snowflake Tree, then subtracting from N. N can be up to 3e5, so O(N) or O(N log N) is needed.

Key observations:
- For a fixed center vertex c and a fixed y, a neighbor v of c can serve as a blue vertex if and only if all neighbors of v except c are leaves. In that case, v has exactly y = degree(v)-1 leaf children.
- The condition depends on the specific center c, so we must check each directed edge (c, v).
- For each valid directed edge, we can group by center c and y = degree(v)-1, and count how many such neighbors v exist for that c and y.
- For a given center c, if we choose y, we can take all valid neighbors with that y to maximize size. The total vertices kept for center c and y is 1 + count * (y+1).
- We need the maximum over all centers c and y >= 1.

Pitfalls:
- A vertex v with degree 1 (leaf) cannot be a blue vertex because y would be 0, but y must be positive.
- The condition for v to be valid with center c is: all neighbors of v except c are leaves. This is equivalent to: non_leaf_count[v] == 0 and c is a leaf, OR non_leaf_count[v] == 1 and c is not a leaf. In both cases, y = degree(v) - 1.
- We must consider both directions of each edge.
- The total number of valid directed edges is O(N), so we can process them efficiently.

Algorithm:
1. Build adjacency list, compute degree of each vertex.
2. Identify leaves (degree 1).
3. Compute leaf_count[v] = number of leaf neighbors of v.
4. Compute non_leaf_count[v] = degree[v] - leaf_count[v].
5. For each vertex u (as center), iterate over neighbors v. If degree[v] >= 2 and ((non_leaf_count[v] == 0 and is_leaf[u]) or (non_leaf_count[v] == 1 and not is_leaf[u])), then it's a valid arm with y = degree[v] - 1. Increment a counter for center u at key y.
6. For each center u with a non-empty counter, compute the best size: 1 + max( (y+1) * count[y] ).
7. The answer is N minus the maximum size found.

Implementation details:
- Use 0-indexed or 1-indexed arrays; 1-indexed is fine.
- Store counters as a list of dictionaries, but only create for centers that get updates. Total updates O(N).
- Use fast I/O.

## worker: Implement the algorithm in Python with efficient I
The algorithm correctly finds the maximum size of a Snowflake Tree induced subgraph by considering each vertex as a potential center. For each center, it computes for each neighbor the maximum possible number of leaf children (a) that can be kept after deletions. By sorting these a values in descending order, we efficiently compute the best size for each possible y (which must be one of the a values). The time complexity is O(N log N) due to sorting, which is efficient for N up to 3e5. The algorithm handles all edge cases, including leaves as centers and varying y values.

## worker: Implement the algorithm in Python with fast I/O, e
The algorithm correctly identifies the largest induced Snowflake Tree by considering each vertex as a potential center. For each center, it checks each neighbor to see if it can serve as a blue vertex (i.e., all its other neighbors are leaves). The condition is efficiently checked using precomputed leaf and non-leaf neighbor counts. For each valid neighbor, the y value is simply `degree[v] - 1`. By aggregating counts per center and y, we compute the maximum possible size as `1 + max((y+1) * count)` for that center. The overall maximum size is taken over all centers. The time complexity is O(N) since we iterate over all edges twice and process each valid directed edge in O(1) amortized time. The memory usage is O(N) for the adjacency list and auxiliary arrays.

The edge case where no valid snowflake is found is handled by defaulting to the minimal snowflake tree size of 3, though the problem guarantees existence.
