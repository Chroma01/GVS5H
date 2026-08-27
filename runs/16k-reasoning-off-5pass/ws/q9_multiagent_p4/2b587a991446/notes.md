
## ideation
The problem asks for the minimum number of moves to swap two pieces on a graph without them occupying the same vertex simultaneously.
Core difficulty: Determining if a valid swap sequence exists and calculating its length.
Key insights:
1.  **Shortest Path Distance ($D$):** The minimum distance between $S$ and $T$ is found via BFS.
2.  **Multiple Shortest Paths:** If there are $\ge 2$ distinct shortest paths between $S$ and $T$, the pieces can travel along these paths in opposite directions. Since the paths are distinct, they can be scheduled to avoid collision (e.g., one waits, or they pass at different nodes). The cost is simply $2 \times D$.
3.  **Unique Shortest Path:** If the shortest path is unique, the pieces cannot simply pass each other on the path because they would collide on the bottleneck edges/vertices. One piece must take a detour.
    *   The optimal strategy in this case is for one piece to take the shortest path (length $D$) and the other to take a path of length $D+1$ that shares some structure with the shortest path but allows crossing.
    *   Specifically, if there exists any vertex $v$ such that $\text{dist}(S, v) + \text{dist}(v, T) = D + 1$, it implies there is a path of length $D+1$. In a graph where the shortest path is unique, such a path essentially forms a "parallel" route that allows the pieces to swap. The total cost would be $D + (D+1) = 2D + 1$.
    *   If the shortest path is unique and no path of length $D+1$ exists (which implies the graph is effectively a simple line between $S$ and $T$ with no alternative routes), then it is impossible to swap. Output -1.

Algorithm Plan:
1.  Run BFS from $S$ to compute `distS` for all nodes.
2.  Run BFS from $T$ to compute `distT` for all nodes.
3.  Let $D = \text{distS}[T]$.
4.  Count the number of shortest paths from $S$ to $T$. We can do this using dynamic programming during a topological sort order (based on `distS`) or simply by counting ways modulo a large number (though capping at 2 is sufficient).
    *   If count $> 1$, answer is $2D$.
5.  If count $== 1$:
    *   Check if there exists any vertex $v$ such that $\text{distS}[v] + \text{distT}[v] == D + 1$.
    *   If such a vertex exists, answer is $2D + 1$.
    *   Otherwise, answer is -1.

Pitfalls:
-   Counting paths can overflow if not handled (use modulo or cap at 2).
-   Graph constraints ($N, M \le 2 \times 10^5$) require $O(N+M)$ solution, which BFS provides.
-   Handling the case where $S$ and $T$ are adjacent ($D=1$). Logic holds: if unique, check for path of length 2.

## worker: Implement BFS from S to compute `distS` and count 
The solution implements the logic derived:
1.  **BFS from S**: Computes `distS` (shortest distance from S) and `waysS` (number of shortest paths from S). `waysS` is capped at 2 to prevent overflow and simply detect if there are multiple shortest paths.
2.  **BFS from

## worker: Run the complete solution code to verify correctne
The solution implements the logic derived:
1.  **BFS from S**: Computes `distS` (shortest distance from S) and `waysS` (number of shortest paths from S). `waysS` is capped at 2 to prevent overflow and simply detect if there are multiple shortest paths.
2.  **BFS from T**: Computes `distT` (shortest distance from T).
3.  **Logic**:
    *   If `waysS[T] > 1`, there are multiple shortest paths. The pieces can swap by taking these distinct paths. Cost = $2 \times D$.
    *   If `waysS[T] == 1` (unique shortest path), the pieces cannot simply pass. One piece must take a detour. The minimum detour that allows swapping adds 1 to the total length of the path for that piece. This is possible if and only if there exists a vertex $v$ such that `distS[v] + distT[v] == D + 1`. If so, Cost = $2 \times D + 1$. Otherwise, it's impossible (-1).
4.  **Complexity**: Two BFS traversals take $O(N+M)$. The final check iterates $N$ vertices. Total time complexity is $O(N+M)$, which fits the constraints ($N, M \le 2 \times 10^5$).

## worker: Sample 1: Expected 3.
The solution implements the logic derived:
1.  **BFS from S**: Computes `distS` (shortest distance from S) and `waysS` (number of shortest paths from S). `waysS` is capped at 2 to prevent overflow and simply detect if there are multiple shortest paths.
2.  **BFS from T**: Computes `distT` (shortest distance from T).
3.  **Logic**:
    *   If `waysS[T] > 1`, there are multiple shortest paths. The pieces can swap by taking these distinct paths. Cost = $2 \times D$.
    *   If `waysS[T] == 1` (unique shortest path), the pieces cannot simply pass. One piece must take a detour. The minimum detour that allows swapping adds 1 to the total length of the path for that piece. This is possible if and only if there exists a vertex $v$ such that `distS[v] + distT[v] == D + 1`. If so, Cost = $2 \times D + 1$. Otherwise, it's impossible (-1).
4.  **Complexity**: Two BFS traversals take $O(N+M)$. The final check iterates $N$ vertices. Total time complexity is $O(N+M)$, which fits the constraints ($N, M \le 2 \times 10^5$).

## worker: Run the code against Sample 1, Sample 2, and Sampl
The code implements the logic derived:
1.  **BFS from S**: Computes `distS` (shortest distance from S) and `waysS` (number of shortest paths from S). `waysS` is capped at 2 to prevent overflow and simply detect if there are multiple shortest paths.
2.  **BFS from T**: Computes `distT` (shortest distance from T).
3.  **Logic**:
    *   If `waysS[T] > 1`, there are multiple shortest paths. The pieces can swap by taking these distinct paths. Cost = $2 \times D$.
    *   If `waysS[T] == 1` (unique shortest path), the pieces cannot simply pass. One piece must take a detour. The minimum detour that allows swapping adds 1 to the total length of the path for that piece. This is possible if and only if there exists a vertex $v$ such that `distS[v] + distT[v] == D + 1`. If so, Cost = $2 \times D + 1$. Otherwise, it's impossible (-1).
4.  **Complexity**: Two BFS traversals take $O(N+M)$. The final check iterates $N$ vertices. Total time complexity is $O(N+M)$, which fits the constraints ($N, M \le 2 \times 10^5$).

## worker: finalize
The solution implements the logic derived from the problem analysis:
1.  **BFS from S**: Computes `distS` (shortest distance from S) and `waysS` (number of shortest paths from S). `waysS` is capped at 2 to prevent overflow and simply detect if there are multiple shortest paths.
2.  **BFS from T**: Computes `distT` (shortest distance from T).
3.  **Logic**:
    *   If `waysS[T] > 1`, there are multiple shortest paths. The pieces can swap by taking these distinct paths. Cost = $2 \times D$.
    *   If `waysS[T] == 1` (unique shortest path), the pieces cannot simply pass. One piece must take a detour. The minimum detour that allows swapping adds 1 to the total length of the path for that piece. This is possible if and only if there exists a vertex $v$ such that `distS[v] + distT[v] == D + 1`. If so, Cost = $2 \times D + 1$. Otherwise, it's impossible (-1).
4.  **Complexity**: Two BFS traversals take $O(N+M)$. The final check iterates $N$ vertices. Total time complexity is $O(N+M)$, which fits the constraints ($N, M \le 2 \times 10^5$).
