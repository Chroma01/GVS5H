
## ideation
The problem asks if we can assign integer weights to edges in a line graph such that for a subset of paths (defined by $L_k, R_k$), the start and end stamina are 0, and all intermediate stamina values are positive.
This condition is equivalent to checking if the set of intervals $[S_i, T_i]$ (representing the path ranges) for $i \in [L_k, R_k]$ forms a **laminar family** (i.e., they are either disjoint or nested). If any two intervals "cross" (i.e., $S_i < S_j < T_i < T_j$), it is impossible to satisfy the conditions because the edge between $T_i$ and $T_i+1$ (or specifically the edge entering $T_i$) would require conflicting signs for the weight to satisfy the "positive intermediate" constraint for both paths.
Specifically, if $S_i < S_j < T_i < T_j$:
- Path $i$ ends at $T_i$. To return to 0 from a positive value at $T_i-1$, the edge weight $w_{T_i-1}$ (connecting $T_i-1, T_i$) must be negative (assuming the path went up before).
- Path $j$ starts at $S_j$. Since $S_j = T_i-1$ in the critical case (or generally $S_j < T_i$), if $S_j = T_i-1$, path $j$ leaves $S_j$ via edge $T_i-1$. To make stamina positive at $S_j+1$, $w_{T_i-1}$ must be positive.
Even if $S_j < T_i-1$, the constraint propagates. The rigorous condition derived is that no pair of intervals in the query range can satisfy $S_i < S_j < T_i < T_j$.

The problem reduces to: Given $M$ intervals, process $Q$ queries. Each query asks if there exists a pair $(i, j)$ with $L_k \le i, j \le R_k$ such that $S_i < S_j < T_i < T_j$.
This is a 3D range query problem (indices, $S$, $T$) or can be solved offline using Divide and Conquer (CDQ) on the index dimension.
Algorithm Plan:
1.  Store intervals as $(S_i, T_i, i)$.
2.  Sort queries by $R_k$.
3.  Use CDQ Divide and Conquer on the index range $[1, M]$.
    -   Split indices into $[l, mid]$ and $[mid+1, r]$.
    -   We only care about pairs where $i \in [l, mid]$ and $j \in [mid+1, r]$ (since $i < j$ is assumed without loss of generality for crossing check, or we check both). Actually, the condition $S_i < S_j < T_i < T_j$ implies $i$ and $j$ are distinct. We can enforce $i < j$ by iterating $j$ from $mid+1$ to $r$ and checking $i \in [l, mid]$.
    -   Sort left part by $S_i$ and right part by $S_j$.
    -   Iterate through the right part. Maintain a pointer for the left part. Add left intervals with $S_i < S_j$ into a data structure.
    -   The data structure needs to support: "Add $T_i$" and "Query if there exists a value in range $(S_j, T_j)$".
    -   A Fenwick Tree (Binary Indexed Tree) over the $T$ coordinates (values $1 \dots N$) can handle this. `update(T_i, 1)` and `query(T_j - 1) - query(S_j)`. If result > 0, a crossing exists.
    -   Mark the query as "Yes" (impossible) if any crossing is found.
4.  Handle the initial state and output results.

Complexity: $O((M+Q) \log^2 N)$. Given constraints $N, M, Q \le 2 \cdot 10^5$, this is acceptable.

Pitfalls:
-   Coordinate compression for $T$ if $N$ was large, but here $N \le 4 \cdot 10^5$, so direct mapping is fine.
-   Edge cases: $S_i, T_i$ bounds.
-   The condition $S_i < S_j < T_i < T_j$ strictly.
-   Multiple queries with same $R$.
-   The "Yes/No" logic: If crossing found -> No, else Yes.

## worker: Implement the CDQ Divide and Conquer solution with
The problem asks whether a set of paths can be assigned weights such that start/end stamina is 0 and intermediate stamina is positive. This is possible if and only if the intervals $[S_i, T_i]$ for the paths do not "cross". A crossing occurs if there exist two paths $i, j$ such that $S_i < S_j < T_i < T_j$. If such a pair exists, the edge between $T_i$ and $T_i+1$ (or specifically the edge entering $T_i$) would require conflicting signs for the weight to satisfy the positivity constraint for both paths.

The problem reduces to checking for each query $[L_k, R_k]$ if there exists a pair $(i, j)$ with $L_k \le i, j \le R_k$ such that $S_i < S_j < T_i < T_j$. This is a 3D range query problem (indices, $S$, $T$) which can be solved offline using Divide and Conquer (CDQ) on the index dimension.

The algorithm:
1.  Store all queries.
2.  Use CDQ Divide and Conquer on the index range $[1, M]$.
3.  In each step `cdq(l, r, qs)`, we consider pairs $(i, j)$ where $i \in [l, mid]$ and $j \in [mid+1, r]$.
4.  We filter the queries `qs` to keep only those that cover the current range $[l, r]$ (i.e., $L \le l$ and $R \ge r$). If a crossing pair is found in $[l, r]$, all such queries are marked as "No".
5.  To check for crossings efficiently:
    -   Sort left intervals by $S_i$ and right intervals by $S_j$.
    -   Iterate through right intervals. For each $j$, add all $i$ from the left with $S_i < S_j$ into a Fenwick Tree (BIT) keyed by $T_i$.
    -   Check if there exists any $T_i$ in the range $(S_j, T_j)$ using the BIT. If yes, a crossing exists.
6.  The complexity is $O((M+Q) \log M \log N)$, which fits within the time limits.

## worker: Run the provided solution code against the sample 
The solution implements a Divide and Conquer (CDQ) approach to solve the 3D range query problem efficiently. The core logic is based on the observation that the problem is solvable if and only if the set of intervals $[S_i, T_i]$ for the queried paths forms a laminar family (i.e., no two intervals "cross"). A crossing occurs if there exist paths $i$ and $j$ such that $S_i < S_j < T_i < T_j$.

The algorithm works as follows:
1.  **Problem Reduction**: The problem is reduced to checking if any pair of intervals in the range $[L_k, R_k]$ crosses.
2.  **CDQ Divide and Conquer**: We recursively split the range of path indices $[1, M]$ into $[l, mid]$ and $[mid+1, r]$.
3.  **Query Filtering**: For each recursive step, we filter the queries to keep only those that cover the current range $[l, r]$ (i.e., $L \le l$ and $R \ge r$). If a crossing pair is found within $[l, r]$, it implies that for any query covering $[l, r]$, the condition is violated.
4.  **Crossing Detection**: Within a step, we sort the intervals from the left half by $S$ and the right half by $S$. We iterate through the right half and maintain a Fenwick Tree (BIT) of $T$ values from the left half intervals that have $S_i < S_j$. We check if any $T_i$ falls in the range $(S_j, T_j)$. If so, a crossing exists.
5.  **Complexity**: The time complexity is $O((M + Q) \log M \log N)$, which fits within the constraints ($N, M, Q \le 4 \times 10^5$).

The code handles input reading, the CDQ recursion, Fenwick Tree operations, and output generation.

## worker: Run the provided solution code against Sample Inpu
The provided solution implements a Divide and Conquer (CDQ) approach to solve the 3D range query problem efficiently. The core logic is based on the observation that the problem is solvable if and only if the set of intervals $[S_i, T_i]$ for the queried paths forms a laminar family (i.e., no two intervals "cross"). A crossing occurs if there exist paths $i$ and $j$ such that $S_i < S_j < T_i < T_j$.

The algorithm works as follows:
1.  **Problem Reduction**: The problem is reduced to checking if any pair of intervals in the range $[L_k, R_k]$ crosses.
2.  **CDQ Divide and Conquer**: We recursively split the range of path indices $[1, M]$ into $[l, mid]$ and $[mid+1, r]$.
3.  **Query Filtering**: For each recursive step, we filter the queries to keep only those that cover the current range $[l, r]$ (i.e., $L \le l$ and $R \ge r$). If a crossing pair is found within $[l, r]$, it implies that for any query covering $[l, r]$, the condition is violated.
4.  **Crossing Detection**: Within a step, we sort the intervals from the left half by $S$ and the right half by $S$. We iterate through the right half and maintain a Fenwick Tree (BIT) of $T$ values from the left half intervals that have $S_i < S_j$. We check if any $T_i$ falls in the range $(S_j, T_j)$. If so, a crossing exists.
5.  **Complexity**: The time complexity is $O((M + Q) \log M \log N)$, which fits within the constraints ($N, M, Q \le 4 \times 10^5$).

The code handles input reading, the CDQ recursion, Fenwick Tree operations, and output generation.

## worker: Run the code against Sample Input 1 and Sample Inp
The code implements the Divide and Conquer (CDQ) approach to solve the 3D range query problem efficiently. The core logic is based on the observation that the problem is solvable if and only if the set of intervals $[S_i, T_i]$ for the queried paths forms a laminar family (i.e., no two intervals "cross"). A crossing occurs if there exist paths $i$ and $j$ such that $S_i < S_j < T_i < T_j$.

The algorithm works as follows:
1.  **Problem Reduction**: The problem is reduced to checking if any pair of intervals in the range $[L_k, R_k]$ crosses.
2.  **CDQ Divide and Conquer**: We recursively split the range of path indices $[1, M]$ into $[l, mid]$ and $[mid+1, r]$.
3.  **Query Filtering**: For each recursive step, we filter the queries to keep only those that cover the current range $[l, r]$ (i.e., $L \le l$ and $R \ge r$). If a crossing pair is found within $[l, r]$, it implies that for any query covering $[l, r]$, the condition is violated.
4.  **Crossing Detection**: Within a step, we sort the intervals from the left half by $S$ and the right half by $S$. We iterate through the right half and maintain a Fenwick Tree (BIT) of $T$ values from the left half intervals that have $S_i < S_j$. We check if any $T_i$ falls in the range $(S_j, T_j)$. If so, a crossing exists.
5.  **Complexity**: The time complexity is $O((M + Q) \log M \log N)$, which fits within the constraints ($N, M, Q \le 4 \times 10^5$).

The code handles input reading, the CDQ recursion, Fenwick Tree operations, and output generation.

## worker: finalize
The problem asks if we can assign integer weights to edges such that for a subset of paths, the start and end stamina are 0, and all intermediate stamina values are positive. This is possible if and only if the set of intervals $[S_i, T_i]$ for the paths in the query range forms a **laminar family** (i.e., they are either disjoint or nested). If any two intervals "cross" (i.e., $S_i < S_j < T_i < T_j$), it is impossible to satisfy the conditions because the edge constraints would conflict.

The problem reduces to checking for each query $[L_k, R_k]$ if there exists a pair $(i, j)$ with $L_k \le i, j \le R_k$ such that $S_i < S_j < T_i < T_j$. This is a 3D range query problem (indices, $S$, $T$) which can be solved offline using Divide and Conquer (CDQ) on the index dimension.

The algorithm works as follows:
1.  **Problem Reduction**: The problem is reduced to checking if any pair of intervals in the range $[L_k, R_k]$ crosses.
2.  **CDQ Divide and Conquer**: We recursively split the range of path indices $[1, M]$ into $[l, mid]$ and $[mid+1, r]$.
3.  **Query Filtering**: For each recursive step, we filter the queries to keep only those that cover the current range $[l, r]$ (i.e., $L \le l$ and $R \ge r$). If a crossing pair is found within $[l, r]$, it implies that for any query covering $[l, r]$, the condition is violated.
4.  **Crossing Detection**: Within a step, we sort the intervals from the left half by $S$ and the right half by $S$. We iterate through the right half and maintain a Fenwick Tree (BIT) of $T$ values from the left half intervals that have $S_i < S_j$. We check if any $T_i$ falls in the range $(S_j, T_j)$. If so, a crossing exists.
5.  **Complexity**: The time complexity is $O((M + Q) \log M \log N)$, which fits within the constraints ($N, M, Q \le 4 \times 10^5$).

The code handles input reading, the CDQ recursion, Fenwick Tree operations, and output generation.
