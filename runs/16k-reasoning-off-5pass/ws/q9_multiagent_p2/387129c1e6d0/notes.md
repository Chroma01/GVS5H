
## ideation
**Core Difficulty**:
The problem asks us to count distinct houses lying on line segments traversed by Santa. The constraints are $N, M \le 2 \times 10^5$, and coordinates can be large ($\pm 10^9$). A naive simulation checking every point on every segment is $O(M \cdot \max(C_i))$, which is too slow. We need an efficient way to query "how many houses are on the segment from $(x_1, y_1)$ to $(x_2, y_2)$" and mark them as visited. Since we need the count of *distinct* houses, we must avoid double-counting if a house is passed multiple times.

**Candidate Approaches**:
1.  **Hash Sets per Coordinate**:
    - Store houses in four dictionaries: `houses_x[y]` = set of x-coordinates, and `houses_y[x]` = set of y-coordinates.
    - For a vertical move (changing Y from $y_{start}$ to $y_{end}$ at fixed $x$):
        - Look up `houses_y[x]`.
        - Find the range of y-coordinates in this set that fall within $[\min(y_{start}, y_{end}), \max(y_{start}, y_{end})]$.
        - Add these houses to a global `visited` set.
    - For a horizontal move (changing X from $x_{start}$ to $x_{end}$ at fixed $y$):
        - Look up `houses_x[y]`.
        - Find the range of x-coordinates in this set that fall within $[\min(x_{start}, x_{end}), \max(x_{start}, x_{end})]$.
        - Add these houses to the global `visited` set.
    - **Complexity**: If we use a hash set for `houses_x` and `houses_y`, finding the range takes $O(K)$ where $K$ is the number of houses in that range. In the worst case (all houses on one line), this is $O(N)$ per move, leading to $O(N \cdot M)$ total, which is too slow.
    - **Optimization**: Use sorted lists (or trees) for the coordinates to allow binary search ($O(\log N)$) to find the start and end indices of the range, then iterate only through the houses in that range. However, if many moves cover the same dense line, iterating is still costly.
    - **Better Optimization**: Since we only care about the *count* of distinct houses, we can maintain a global set of visited house IDs (or coordinates). The issue remains the iteration time.
    - **Wait, is iteration unavoidable?** Yes, if a segment passes through 1000 houses, we must process them to mark them as visited. The total complexity would be proportional to the total number of house-passings. If the test cases are constructed such that Santa passes through $O(N)$ houses $M$ times, this fails. However, usually in such problems, the sum of houses passed is bounded or the test cases aren't worst-case adversarial against a simple sweep-line. But strictly speaking, worst-case $O(N \cdot M)$ exists.
    - **Alternative**: Use a Segment Tree or Fenwick Tree? No, coordinates are large. Coordinate compression is possible but 2D range queries on lines are tricky.
    - **Re-evaluating the "Distinct" constraint**: The problem asks for the number of distinct houses. If we simply add the coordinates of houses found in the current segment to a global `set`, the insertion is $O(1)$ on average. The bottleneck is *finding* which houses are in the segment.
    - **Is there a faster way to count without iterating?** Only if we can query "count of points in range" without listing them. But we need to mark them as visited for future queries. If a house is already visited, we don't need to do anything, but we still need to know *which* houses are in the range to check if they are new.
    - **Actually**, the standard solution for this specific type of problem (AtCoder ABC 299 D? No, looks like ABC 299 C or similar difficulty) often relies on the fact that while $N, M$ are large, the total number of *distinct* houses passed might not be the bottleneck if we use efficient range queries.
    - **Wait, let's look at the constraints again.** $N, M \le 2 \cdot 10^5$. If we have a line with $10^5$ houses and we traverse it $10^5$ times, we do $10^{10}$ operations. This suggests we need something faster than iterating.
    - **Is it possible the problem guarantees no overlapping dense lines?** No.
    - **Is there a data structure that supports "mark all in range as visited"?** A DSU (Disjoint Set Union) on the sorted array of houses on a line?
        - For a specific line (e.g., $x=c$), we have a sorted list of y-coordinates: $y_1, y_2, \dots, y_k$.
        - When we traverse $[y_a, y_b]$, we want to mark all $y_i \in [y_a, y_b]$ as visited.
        - We can use DSU to skip visited segments. When we visit a range, we union the indices. The next time we query the same range, we jump over the unioned components.
        - This technique (DSU on array indices) ensures that each element is processed (visited) at most once (or a few times).
        - **Algorithm**:
            1. Group houses by X and Y. For each unique X, store a sorted list of Ys. For each unique Y, store a sorted list of Xs.
            2. Maintain a global `visited` set of house coordinates (or IDs).
            3. For each move:
               - Identify the line (fixed X or fixed Y) and the range.
               - Find the index range $[L, R]$ in the sorted list for that line using `bisect`.
               - Iterate from $L$ to $R$. For each index $i$:
                 - If house $i$ is not visited:
                   - Mark as visited, increment count.
                   - Union $i$ with $i+1$ (if $i+1 \le R$) in the DSU structure for this line to skip next time?
                   - Actually, standard DSU optimization: `find(i)` gives the next unvisited index. We jump to `find(i)`.
                   - If `find(i)` is within $[L, R]$, we process it. If it's outside, we stop.
            4. This ensures total complexity is $O((N + M) \alpha(N))$ or similar, because each house is "processed" (added to visited set) once, and the DSU operations are nearly constant. The cost of finding the initial range is $O(M \log N)$.

## worker: Implement the solution in Python using coordinate 
The solution implements the DSU (Disjoint Set Union) optimization on the sorted lists of houses for each coordinate line.
1.  **Data Structures**:
    -   `houses_by_x`: Dictionary mapping x-coordinate to a sorted list of y-coordinates of houses on that vertical line.
    -   `houses_by_y`: Dictionary mapping y-coordinate to a sorted list of x-coordinates of houses on that horizontal line.
    -   `dsu_x` / `dsu_y`: Dictionaries mapping coordinate to a DSU parent array. The parent array for a line of size $K$ has size $K+1$. `parent[i]` stores the next unvisited index $\ge i$.
    -   `visited`: A set of tuples `(x, y)` to track distinct houses passed.
2.  **Algorithm**:
    -   For each move, determine the fixed coordinate (x or y) and the range of the other coordinate.
    -   Use `bisect_left` and `bisect_right` to find the index range `[l, r]` in the sorted list corresponding to the segment.
    -   Use the DSU `find` operation to jump over already visited houses. If `find(l)` returns an index $> r$, no new houses are in this segment.
    -   If a house at `list[idx]` is found (unvisited), add it to the `visited` set, increment the count, and perform `union(idx, idx+1)` to mark it as visited for future queries.
    -   Update the current position after each move.
3.  **Complexity**:
    -   Sorting houses: $O(N \log N)$.
    -   Processing moves: $O(M \log N)$ for binary searches.
    -   DSU operations: Each house is visited and unioned at most once. Total DSU operations are nearly linear in the number of houses passed, bounded by $O(N \alpha(N))$.
    -   Overall Time Complexity: $O(N \log N + M \log N + N \alpha(N))$, which fits well within the limits.
    -   Space Complexity: $O(N)$ to store the lists and DSU structures.

## worker: Run the code against the provided sample inputs to
The solution implements a DSU (Disjoint Set Union) optimization on the sorted lists of houses for each coordinate line (vertical and horizontal).
1.  **Data Structures**:
    -   `houses_by_x`: Dictionary mapping x-coordinate to a sorted list of y-coordinates.
    -   `houses_by_y`: Dictionary mapping y-coordinate to a sorted list of x-coordinates.
    -   `dsu_x` / `dsu_y`: Dictionaries mapping coordinate to a DSU parent array. The parent array for a line of size $K$ has size $K+1$. `parent[i]` stores the next unvisited index $\ge i$.
    -   `visited`: A set of tuples `(x, y)` to track distinct houses passed.
2.  **Algorithm**:
    -   For each move, determine the fixed coordinate (x or y) and the range of the other coordinate.
    -   Use `bisect_left` and `bisect_right` to find the index range `[l, r]` in the sorted list corresponding to the segment.
    -   Use the DSU `find` operation to jump over already visited houses. If `find(l)` returns an index $> r$, no new houses are in this segment.
    -   If a house at `list[idx]` is found (unvisited), add it to the `visited` set, increment the count, and perform `union(idx, idx+1)` to mark it as visited for future queries.
    -   Update the current position after each move.
3.  **Complexity**:
    -   Sorting houses: $O(N \log N)$.
    -   Processing moves: $O(M \log N)$ for binary searches.
    -   DSU operations: Each house is visited and unioned at most once. Total DSU operations are nearly linear in the number of houses passed, bounded by $O(N \alpha(N))$.
    -   Overall Time Complexity: $O(N \log N + M \log N + N \alpha(N))$, which fits well within the limits.
    -   Space Complexity: $O(N)$ to store the lists and DSU structures.

## worker: Run the provided sample inputs to verify correctne
The code implements the solution using a Disjoint Set Union (DSU) optimization on the sorted lists of houses for each coordinate line.
1.  **Data Structures**:
    -   `houses_by_x` and `houses_by_y`: Dictionaries mapping coordinates to sorted lists of the other coordinate.
    -   `dsu_x` and `dsu_y`: Dictionaries mapping coordinates to DSU parent arrays. The parent array for a line of size $K$ has size $K+1$. `parent[i]` stores the next unvisited index $\ge i$.
    -   `visited`: A set of tuples `(x, y)` to track distinct houses passed (though the count is incremented directly, the set ensures we don't double count if logic were different, but here the DSU logic inherently prevents re-processing).
2.  **Algorithm**:
    -   For each move, determine the fixed coordinate and the range of the other coordinate.
    -   Use `bisect_left` and `bisect_right` to find the index range `[l, r]` in the sorted list corresponding to the segment.
    -   Use the DSU `find` operation to jump over already visited houses. If `find(l)` returns an index $> r$, no new houses are in this segment.
    -   If a house at `list[idx]` is found (unvisited), increment the count, and perform `union(idx, idx+1)` to mark it as visited for future queries.
    -   Update the current position after each move.
3.  **Complexity**:
    -   Sorting houses: $O(N \log N)$.
    -   Processing moves: $O(M \log N)$ for binary searches.
    -   DSU operations: Each house is visited and unioned at most once. Total DSU operations are nearly linear in the number of houses passed, bounded by $O(N \alpha(N))$.
    -   Overall Time Complexity: $O(N \log N + M \log N + N \alpha(N))$, which fits well within the limits.
    -   Space Complexity: $O(N)$ to store the lists and DSU structures.

## worker: Run the code against Sample Input 1 and Sample Inp
The code implements the solution using a Disjoint Set Union (DSU) optimization on the sorted lists of houses for each coordinate line.
1.  **Data Structures**:
    -   `houses_by_x` and `houses_by_y`: Dictionaries mapping coordinates to sorted lists of the other coordinate.
    -   `dsu_x` and `dsu_y`: Dictionaries mapping coordinates to DSU parent arrays. The parent array for a line of size $K$ has size $K+1$. `parent[i]` stores the next unvisited index $\ge i$.
    -   `visited`: A set of tuples `(x, y)` to track distinct houses passed (though the count is incremented directly, the set ensures we don't double count if logic were different, but here the DSU logic inherently prevents re-processing).
2.  **Algorithm**:
    -   For each move, determine the fixed coordinate and the range of the other coordinate.
    -   Use `bisect_left` and `bisect_right` to find the index range `[l, r]` in the sorted list corresponding to the segment.
    -   Use the DSU `find` operation to jump over already visited houses. If `find(l)` returns an index $> r$, no new houses are in this segment.
    -   If a house at `list[idx]` is found (unvisited), increment the count, and perform `union(idx, idx+1)` to mark it as visited for future queries.
    -   Update the current position after each move.
3.  **Complexity**:
    -   Sorting houses: $O(N \log N)$.
    -   Processing moves: $O(M \log N)$ for binary searches.
    -   DSU operations: Each house is visited and unioned at most once. Total DSU operations are nearly linear in the number of houses passed, bounded by $O(N \alpha(N))$.
    -   Overall Time Complexity: $O(N \log N + M \log N + N \alpha(N))$, which fits well within the limits.
    -   Space Complexity: $O(N)$ to store the lists and DSU structures.

## worker: finalize
The solution implements a Disjoint Set Union (DSU) optimization on the sorted lists of houses for each coordinate line (vertical and horizontal).
1.  **Data Structures**:
    -   `houses_by_x` and `houses_by_y`: Dictionaries mapping coordinates to sorted lists of the other coordinate.
    -   `dsu_x` and `dsu_y`: Dictionaries mapping coordinates to DSU parent arrays. The parent array for a line of size $K$ has size $K+1$. `parent[i]` stores the next unvisited index $\ge i$.
    -   `visited`: A set of tuples `(x, y)` to track distinct houses passed.
2.  **Algorithm**:
    -   For each move, determine the fixed coordinate and the range of the other coordinate.
    -   Use `bisect_left` and `bisect_right` to find the index range `[l, r]` in the sorted list corresponding to the segment.
    -   Use the DSU `find` operation to jump over already visited houses. If `find(l)` returns an index $> r$, no new houses are in this segment.
    -   If a house at `list[idx]` is found (unvisited), increment the count, and perform `union(idx, idx+1)` to mark it as visited for future queries.
    -   Update the current position after each move.
3.  **Complexity**:
    -   Sorting houses: $O(N \log N)$.
    -   Processing moves: $O(M \log N)$ for binary searches.
    -   DSU operations: Each house is visited and unioned at most once. Total DSU operations are nearly linear in the number of houses passed, bounded by $O(N \alpha(N))$.
    -   Overall Time Complexity: $O(N \log N + M \log N + N \alpha(N))$, which fits well within the limits.
    -   Space Complexity: $O(N)$ to store the lists and DSU structures.
