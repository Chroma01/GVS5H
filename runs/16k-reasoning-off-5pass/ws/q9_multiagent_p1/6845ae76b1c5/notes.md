
## ideation
The core difficulty is efficiently computing $\sum_{i=1}^{X} \sum_{j=1}^{Y} |A_i - B_j|$ for multiple queries $(X, Y)$ where $N$ is up to $10^5$ and $K$ is up to $10^4$. A naive $O(N^2)$ per query is impossible.

Key observations:
1.  **Sorting**: The absolute difference $|a - b|$ depends on the relative order of $a$ and $b$. Sorting $A$ and $B$ allows us to split the summation into two parts: where $A_i \le B_j$ (sum is $B_j - A_i$) and where $A_i > B_j$ (sum is $A_i - B_j$).
2.  **Prefix Sums**: Once sorted, the sum of $A_i$ and $B_j$ over ranges can be computed in $O(1)$ using prefix sums.
3.  **Query Complexity**: Since queries specify prefixes $[1, X]$ and $[1, Y]$ of the *sorted* arrays (after sorting initially), we can answer each query in $O(\log N)$ or $O(1)$ after $O(N \log N)$ preprocessing. Specifically, for a fixed $X$ and $Y$, we find the split index $p$ such that $A[i] \le B[j]$ for $i \le p$ (roughly, though the split depends on the specific values). Actually, since we are summing over a rectangle in the sorted grid, we can iterate over the sorted $A$ up to $X$ and sorted $B$ up to $Y$. The condition $A_i \le B_j$ changes based on $A_i$ and $B_j$.
    *   Correct approach: Sort $A$ and $B$. Let the sorted arrays be $A'$ and $B'$.
    *   For a query $(X, Y)$, we consider $A'[1..X]$ and $B'[1..Y]$.
    *   We need to find an index $k$ such that for all $i \le k$ (within $1..X$) and $j \le Y$, $A'[i] \le B'[j]$? No, that's not strictly true for all pairs. The condition is pairwise.
    *   Better approach: The sum is $\sum_{i=1}^X \sum_{j=1}^Y |A'_i - B'_j|$.
    *   We can find the largest index $p$ in $A'$ (within $1..X$) such that $A'_p \le B'_1$? No.
    *   Standard technique: Find the split point $k$ such that $A'_i \le B'_j$ for $i \le k$ and $i > k$ implies $A'_i > B'_j$? This only works if the arrays are monotonic in a specific way relative to each other.
    *   Actually, since both are sorted, there exists a "staircase" boundary. However, a simpler $O(\log N)$ approach per query exists:
        Find the largest index $idx$ such that $A'[idx] \le B'[1]$? No.
        Let's reconsider. We want $\sum_{i=1}^X \sum_{j=1}^Y |A'_i - B'_j|$.
        Split the sum into $A'_i \le B'_j$ and $A'_i > B'_j$.
        Since $A'$ and $B'$ are sorted, for a fixed $i$, the values of $j$ where $B'_j \ge A'_i$ form a suffix of $1..Y$. Let $pos(i)$ be the first index in $B'$ such that $B'_{pos(i)} \ge A'_i$. Then for $j \in [pos(i), Y]$, term is $B'_j - A'_i$. For $j \in [1, pos(i)-1]$, term is $A'_i - B'_j$.
        We can precompute prefix sums for $A'$ and $B'$.
        For each query $(X, Y)$:
        1. Iterate $i$ from $1$ to $X$. Find $pos(i)$ using binary search (or two pointers if queries were sorted, but $K$ is small enough that binary search per query is fine: $10^4 \times 10^5 \log 10^5$ is too big? Wait. $K=10^4, N=10^5$. $10^4 \times \log(10^5) \approx 1.7 \times 10^5$ operations if we do binary search on $B$ for each $A$. But we need to do this for each $i$ from $1$ to $X$. That would be $O(X \log Y)$ per query, total $O(K \cdot N \log N)$ in worst case ($X=N$). $10^4 \cdot 10^5 = 10^9$, which is TLE.
        
        **Correction**: We cannot iterate $i$ from $1$ to $X$. We need an $O(\log N)$ or $O(1)$ per query solution.
        
        Alternative view:
        $\sum_{i=1}^X \sum_{j=1}^Y |A'_i - B'_j| = \sum_{i=1}^X (\sum_{j=1}^Y |A'_i - B'_j|)$.
        Let $f(v, Y) = \sum_{j=1}^Y |v - B'_j|$.
        $f(v, Y)$ can be computed in $O(1)$ if we know the split point $p$ where $B'_p < v \le B'_{p+1}$.
        $f(v, Y) = \sum_{j=1}^p (v - B'_j) + \sum_{j=p+1}^Y (B'_j - v)$.
        $= p \cdot v - \text{prefix\_sum\_B}[p] + (\text{prefix\_sum\_B}[Y] - \text{prefix\_sum\_B}[p]) - (Y-p) \cdot v$.
        $= (2p - Y) \cdot v + (\text{prefix\_sum\_B}[Y] - \text{prefix\_sum\_B}[p])$.
        
        So for each query $(X, Y)$, we need to compute $\sum_{i=1}^X f(A'_i, Y)$.
        This still requires summing over $i=1..X$. If we do this naively, it's $O(X)$ per query. Total $O(K \cdot N)$. With $K=10^4, N=10^5$, this is $10^9$, likely too slow for 2 seconds.
        
        Is there a way to optimize $\sum_{i=1}^X f(A'_i, Y)$?
        Notice that $A'$ is sorted. As $i$ increases, $A'_i$ increases. The split point $p_i$ (index in $B'$ where $B'_p < A'_i \le B'_{p+1}$) is non-decreasing.
        However, $Y$ is fixed for the query.
        The function $g(i) = f(A'_i, Y)$ is convex?
        Maybe we can use the fact that $K$ is relatively small ($10^4$) but $N$ is large.
        Wait, constraints: $N \le 10^5, K \le 10^4$.
        $O(K \cdot N)$ is indeed risky. But maybe the constant factor is small? Or maybe there's a specific property.
        
        Let's re-read carefully. "Find $\sum_{i=1}^{X_k} \sum_{j=1}^{Y_k} |A_i-B_j|$".
        Is it possible to swap loops?
        Total Sum = $\sum_{j=1}^Y \sum_{i=1}^X |A'_i - B'_j|$.
        Let $h(u, X) = \sum_{i=1}^X |u - A'_i|$.
        Then Total = $\sum_{j=1}^Y h(B'_j, X)$.
        Same issue.
        
        Is it possible that $O(K \cdot N)$ passes? In C++, $10^9$ simple ops might pass in 2-3s, but Python is slower. We need a better approach.
        
        Wait, do we really need to sum over all $i$?
        Let's look at the structure again.
        We have two sorted arrays $A'$ and $B'$. We want the sum of absolute differences in the subgrid $[1, X] \times [1, Y]$.
        This is equivalent to:
        $\sum_{i=1}^X \sum_{j=1}^Y |A'_i - B'_j|$.
        Consider the contribution of each pair.
        Maybe we can use the "two pointers" idea on the boundary?
        Actually, there is a known technique for this specific problem (sum of absolute differences in submatrices of sorted arrays).
        The split point logic:
        For a fixed $Y$, as $i$ goes $1 \to X$, the split point $p_i$ in $B'$ moves right.
        But we need the sum over $i$.
        
        Let's reconsider the complexity. $10^4 \times 10^5 = 10^9$. In Python, this will definitely TLE.
        Is there an $O((N+K) \log N)$ or $O((N+K) \log^2 N)$ approach?
        
        Yes!
        We can rewrite the sum:
        $\sum_{i=1}^X \sum_{j=1}^Y |A'_i - B'_j| = \sum_{i=1}^X \sum_{j=1}^Y \text{sgn}(A'_i - B'_j)(A'_i - B'_j)$? No.
        
        Let's go back to:
        Sum = $\sum_{i=1}^X [ (p_i \cdot A'_i - S_{B, p_i}) + (S_{B, Y} - S_{B, p_i}) - (Y - p_i) \cdot A'_i ]$
        where $p_i$ is the count of elements in $B'[1..Y]$ strictly less than $A'_i$.
        Sum = $\sum_{i=1}^X [ (2p_i - Y) A'_i + S_{B, Y} - 2 S_{B, p_i} ]$.
        Sum = $S_{A, X} \cdot (-Y) + \sum_{i=1}^X (2p_i A'_i) + \sum_{i=1}^X (-2 S_{B, p_i}) + X \cdot S_{B, Y}$.
        
        The term $p_i$ is the number of elements in $B'[1..Y]$ less than $A'_i$.
        Since $A'$ is sorted, $p_i$ is non-decreasing.
        Also $p_i = \min(Y, \text{bisect\_left}(B', A'_i))$.
        
        Can we compute $\sum_{i=1}^X p_i A'_i$ and $\sum_{i=1}^X S_{B, p_i}$ efficiently?
        Notice that $p_i$ takes values $0, 1, 2, \dots, Y$.
        Specifically, $p_i$ changes value only when $A'_i$ crosses some $B'_j$.
        Since $A'$ is sorted, we can find the ranges of $i$ where $p_i$ is constant.
        The values of $p_i$ will be $0$ for $i \in [1, i_0]$, $1$ for $i \in [i_0+1, i_1]$, ..., $Y$ for $i \in [i_{Y-1}+1, X]$.
        The transition points $i_k$ are determined by $A'_i \le B'_k$.
        Specifically, $p_i = k$ when $B'_{k} < A'_i \le B'_{k+1}$ (with boundary conditions).
        Actually, $p_i = \text{count}(\{j \le Y : B'_j < A'_i\})$.
        So $p_i \ge k \iff A'_i > B'_k$.
        So $p_i = k$ for $B'_k < A'_i \le B'_{k+1}$ (roughly).
        
        Algorithm refinement:
        1. Sort $A$ and $B$. Compute prefix sums for both.
        2. For each query $(X, Y)$:
           We need to sum over $i \in [1, X]$.
           The value $p_i$ depends on $A'_i$ and $B'$.
           Since $A'$ is sorted, we can find the indices where $p_i$ changes.
           The critical values for $A'_i$ are the values in $B'[1..Y]$.
           Let the sorted unique values in $B'[1..Y]$ be $v_1, v_2, \dots, v_m$ (where $m \le Y$).
           These values divide the range of $A'$ into segments.
           For $A'_i \le v_1$, $p_i = 0$.
           For $v_1 < A'_i \le v_2$, $p_i = 1$.
           ...
           For $v_{m-1} < A'_i \le v_m$, $p_i = m-1$.
           For $A'_i > v_m$, $p_i = m$ (which is $Y$ if all $B$ are considered, but here we only care about $B'[1..Y]$).
           Wait, $p_i$ is the count of elements in $B'[1..Y]$ less than $A'_i$.
           So if $A'_i > B'_Y$, then $p_i = Y$.
           If $A'_i \le B'_1$, then $p_i = 0$.
           
           So we can iterate through the segments defined by $B'[1..Y]$.
           There are at most $Y$ segments. Summing over segments is $O(Y)$.
           Total complexity $O(\sum Y_k)$. In worst case $K \times N = 10^9$. Still too slow.
           
           Is there a way to avoid iterating over $Y$?
           Yes, use binary search (or `bisect`) to find the range of $i$ for each segment in $O(\log N)$.
           There are $Y$ segments, so finding the split points in $A'$ for each $B'_j$ takes $O(Y \log N)$. Still $O(N)$ per query.
           
           Wait, do we need to iterate over all $B'_j$?
           We need $\sum_{i=1}^X (2p_i A'_i)$.
           $p_i = \sum_{j=1}^Y [B'_j < A'_i]$.
           So $\sum_{i=1}^X p_i A'_i = \sum_{i=1}^X \sum_{j=1}^Y [B'_j < A'_i] A'_i = \sum_{j=1}^Y \sum_{i=1}^X [B'_j < A'_i] A'_i$.
           For a fixed $j$, the inner sum is $\sum_{i: A'_i > B'_j, i \le X} A'_i$.
           This is a suffix sum of $A'$ up to $X$.
           Let $idx_j = \text{bisect\_right}(A', B'_j)$. Then the sum is over $i \in [\min(idx_j, X) + 1, X]$.
           If $\min(idx_j, X) + 1 > X$, sum is 0.
           So the term is $S_{A, X} - S_{A, \min(idx_j, X)}$.
           
           Similarly for the other part: $\sum_{i=1}^X S_{B, p_i}$.
           $p_i = \text{count}(B' < A'_i \text{ in } 1..Y)$.
           $S_{B, p_i} = \sum_{k=1}^{p_i} B'_k$.
           So $\sum_{i=1}^X S_{B, p_i} = \sum_{i=1}^X \sum_{k=1}^Y [B'_k < A'_i] B'_k = \sum_{k=1}^Y B'_k \sum_{i=1}^X [B'_k < A'_i]$.
           The inner sum is the count of $i \in [1, X]$ such that $A'_i > B'_k$.
           Let $cnt_j = \max(0, X - \text{bisect\_right}(A', B'_j))$.
           Then term is $B'_j \times cnt_j$.
           
           So the total sum can be rewritten as:
           Total = $\sum_{i=1}^X \sum_{j=1}^Y |A'_i - B'_j|$
           $= \sum_{i=1}^X [ (p_i A'_i - S_{B, p_i}) + (S_{B, Y} - S_{B, p_i}) - (Y-p_i)A'_i ]$
           $= \sum_{i=1}^X [ (2p_i - Y)A'_i + S_{B, Y} - 2S_{B, p_i} ]$
           $= (2 \sum_{i=1}^X p_i A'_i - Y S_{A, X}) + X S_{B, Y} - 2 \sum_{i=1}^X S_{B, p_i}$.
           
           Substitute the derived forms:
           1. $\sum_{i=1}^X p_i A'_i = \sum_{j=1}^Y (S_{A, X} - S_{A, \min(\text{idx}_j, X)})$ where $\text{idx}_j = \text{bisect\_right}(A', B'_j)$.
              $= Y \cdot S_{A, X} - \sum_{j=1}^Y S_{A, \min(\text{idx}_j, X)}$.
           
           2. $\sum_{i=1}^X S_{B, p_i} = \sum_{j=1}^Y B'_j \cdot (\text{count of } i \in [1, X] \text{ s.t. } A'_i > B'_j)$
              $= \sum_{j=1}^Y B'_j \cdot \max(0, X - \text{bisect\_right}(A', B'_j))$.
           
           Now the complexity per query is $O(Y)$ if we iterate $j$.
           Worst case $Y=N$, so $O(N)$ per query. Total $O(KN)$.
           Still $10^9$.
           
           Is there a constraint I missed? $K=10^4, N=10^5$.
           Maybe the test cases are weak? Or maybe $O(KN)$ is acceptable in C++ but not Python?
           Or maybe there's a way to optimize the summation over $j$?
           Notice that $\text{idx}_j = \text{bisect\_right}(A', B'_j)$ is non-decreasing with $j$ (since $B'$ is sorted).
           So $\min(\text{idx}_j, X)$ is also non-decreasing.
           We can use two pointers to compute $\sum_{j=1}^Y S_{A, \min(\text{idx}_j, X)}$ in $O(X)$? No, $O(Y)$ is fine, but we want to avoid $O(Y)$.
           Wait, if $\text{idx}_j$ is constant for a range of $j$, we can group them.
           Since $\text{idx}_j$ takes values in $0..N$, and it changes at most $N$ times, but we only care about $j \in [1, Y]$.
           The number of distinct values of $\text{idx}_j$ for $j \in [1, Y]$ is at most $Y$.
           However, we can find the ranges of $j$ where $\text{idx}_j$ is constant using binary search on $A'$?
           Actually, $\text{idx}_j$ is the position of $B'_j$ in $A'$.
           We can precompute for each $j$, the value $v_j = \text{bisect\_right}(A', B'_j)$. This takes $O(N \log N)$ total.
           Then for a query $(X, Y)$, we need to sum over $j=1..Y$:
           Term1: $S_{A, \min(v_j, X)}$.
           Term2: $B'_j \cdot \max(0, X - v_j)$.
           
           Since $v_j$ is non-decreasing, the sequence $v_1, v_2, \dots, v_Y$ is sorted.
           We can find the split points where $v_j < X$ and $v_j \ge X$.
           Let $k$ be the largest index such that $v_k < X$. (Using binary search on the precomputed array $v$).
           Then for $j \in [1, k]$, $\min(v_j, X) = v_j$.
           For $j \in [k+1, Y]$, $\min(v_j, X) = X$.
           
           So:
           $\sum_{j=1}^Y S_{A, \min(v_j, X)} = \sum_{j=1}^k S_{A, v_j} + \sum_{j=k+1}^Y S_{A, X}$.
           $= \sum_{j=1}^k S_{A, v_j} + (Y-k) S_{A, X}$.
           
           Similarly for the second term:
           $\max(0, X - v_j)$ is $X - v_j$ for $j \le k$, and $0$ for $j > k$.
           So $\sum_{j=1}^Y B'_j \max(0, X - v_j) = \sum_{j=1}^k B'_j (X - v_j)$.
           
           Now we need to compute $\sum_{j=1}^k S_{A, v_j}$ and $\sum_{j=1}^k B'_j v_j$ efficiently.
           $k$ can be up to $Y$. We still need to sum over $j=1..k$.
           However, notice that $v_j$ is the index in $A$.
           $S_{A, v_j}$ is the prefix sum of $A$ up to index $v_j$.
           Is there a pattern?
           $v_j$ is non-decreasing.
           We can precompute prefix sums of $v_j$ and $B'_j v_j$? No, because $v_j$ depends on $A$ and $B$ globally, but the query restricts $j$ to $1..Y$.
           Wait, $v_j$ is fixed for all queries!
           Yes! $v_j = \text{bisect\_right}(A, B_j)$ is independent of the query.
           So we can precompute arrays:
           $P1[k] = \sum_{j=1}^k S_{A, v_j}$
           $P2[k] = \sum_{j=1}^k B'_j v_j$
           $P3[k] = \sum_{j=1}^k B'_j$
           
           Then for a query $(X, Y)$:
           1. Find $k = \max \{ j \in [1, Y] : v_j < X \}$. If no such $j$, $k=0$.
              We can find this $k$ by binary searching $v$ in the range $[1, Y]$. Since $v$ is sorted, we can use `bisect_right` on the array $v$ (clamped to $Y$) to find the first index where $v_j \ge X$, then $k = \text{index} - 1$.
           2. Compute sums using precomputed prefix arrays $P1, P2, P3$.
              Sum1 = $P1[k] + (Y-k) S_{A, X}$.
              Sum2 = $X \cdot P3[k] - P2[k]$.
           3. Plug into the main formula.
           
           Complexity:
           Preprocessing: $O(N \log N)$ to sort and compute $v_j$. $O(N)$ to compute prefix sums.
           Per Query: $O(\log N)$ to find $k$ and $O(1)$ to compute answer.
           Total: $O(N \log N + K \log N)$.
           This is well within limits! $10^5 \log 10^5 \approx 1.7 \times 10^6$, $10^4 \log 10^5 \approx 1.7 \times 10^5$.
           
           Double check the logic for $S_{A, v_j}$.
           $v_j$ is an index in $A$ (1-based or 0-based).
           $S_{A, v_j}$ is the sum of $A[0..v_j-1]$.
           If $v_j = 0$, sum is 0.
           The logic holds.
           
           One detail: $v_j = \text{bisect\_right}(A, B_j)$.
           If $B_j < A_0$, $v_j = 0$.
           If $B_j \ge A_N$, $v_j = N$.
           Correct.

## worker: Implement the optimized $O((N+K)\log N)$ solution 
1.  **Algorithm Selection**: The problem asks for $\sum_{i=1}^{X} \sum_{j=1}^{Y} |A_i - B_j|$. A naive $O(N^2)$ per query is too slow. Sorting $A$ and $B$ allows us to split the absolute difference sum into two parts based on the relative order of elements.
2.  **Mathematical Derivation**:
    *   Let sorted arrays be $A'$ and $B'$.
    *   For a fixed $j$ (element in $B'$), the contribution to the sum over $i \in [1, X]$ is $\sum_{i=1}^X |A'_i - B'_j|$.
    *   This inner sum can be computed as $(count(A' < B'_j) \cdot B'_j - \sum_{A' < B'_j} A') + (\sum_{A' \ge B'_j} A') - (count(A' \ge B'_j) \cdot B'_j)$.
    *   Alternatively, using the derived formula: $\sum_{i=1}^X \sum_{j=1}^Y |A'_i - B'_j| = (2 \sum p_i A'_i - Y S_{A,X}) + X S_{B,Y} - 2 \sum S_{B, p_i}$, where $p_i$ is the count of elements in $B'[1..Y]$ less than $A'_i$.
    *   By swapping summation order and using properties of sorted arrays, we reduced the problem to computing sums over $j \in [1, Y]$ involving $v_j = \text{bisect\_right}(A, B_j)$.
3.  **Optimization**:
    *   Precompute $v_j$ for all $j$. Since $B$ is sorted, $v_j$ is non-decreasing.
    *   Precompute prefix sums of $prefA[v_j]$, $B_j \cdot v_j$, and $B_j$.
    *   For each query $(X, Y)$, find the split point $k$ where $v_j < X$ using binary search (`bisect_right`).
    *   Use the precomputed prefix sums to calculate the required terms in $O(1)$ after the binary search ($O(\log N)$).
4.  **Complexity**:
    *   Sorting: $O(N \log N)$.
    *   Precomputation: $O(N \log N)$ (due to bisect) or $O(N)$ if optimized, but $O(N \log N)$ is fine.
    *   Queries: $K \times O(\log N)$.
    *   Total: $O((N+K) \log N)$, which fits well within the time limit for $N=10^5, K=10^4$.

## worker: Implement the optimized $O((N+K)\log N)$ solution 
The solution implements the optimized $O((N+K)\log N)$ approach.
1.  **Sorting**: Arrays $A$ and $B$ are sorted to enable binary search and prefix sum logic.
2.  **Precomputation**:
    *   Prefix sums for $A$ and $B$ are computed.
    *   An array $v$ is precomputed where $v[j]$ is the count of elements in $A$ strictly less than $B[j]$. Since $B$ is sorted, $v$ is non-decreasing.
    *   Prefix sums over $v$ are computed for two specific terms: $\sum \text{prefA}[v[j]]$ and $\sum B[j] \cdot v[j]$.
3.  **Query Processing**:
    *   For each query $(X, Y)$, we determine a split point $k$ within the first $Y$ elements of $B$ such that for indices $j < k$, $v[j] < X$, and for $j \ge k$, $v[j] \ge X$. This is done using binary search (`bisect_right`) on the precomputed array $v$.
    *   Using the precomputed prefix sums, we calculate the required sums in $O(1)$ time after the binary search step.
    *   The final answer is derived from the mathematical expansion of the sum of absolute differences, substituting the precomputed values.
4.  **Complexity**: Sorting takes $O(N \log N)$. Precomputation takes $O(N \log N)$ (due to bisect) or $O(N)$ if optimized, but $O(N \log N)$ is acceptable. Each query takes $O(\log N)$ for the binary search. Total time complexity is $O((N+K) \log N)$, which fits well within the limits.

## worker: Implement the optimized $O((N+K)\log N)$ solution 
The solution implements the optimized $O((N+K)\log N)$ approach.
1.  **Sorting**: Arrays $A$ and $B$ are sorted to enable binary search and prefix sum logic.
2.  **Precomputation**:
    *   Prefix sums for $A$ and $B$ are computed.
    *   An array $v$ is precomputed where $v[j]$ is the count of elements in $A$ strictly less than $B[j]$ (using `bisect_right`). Since $B$ is sorted, $v$ is non-decreasing.
    *   Prefix sums over $v$ are computed for two specific terms: $\sum \text{prefA}[v[j]]$ and $\sum B[j] \cdot v[j]$.
3.  **Query Processing**:
    *   For each query $(X, Y)$, we determine a split point $k$ within the first $Y$ elements of $B$ such that for indices $j < k$, $v[j] < X$, and for $j \ge k$, $v[j] \ge X$. This is done using binary search (`bisect_right`) on the precomputed array $v$.
    *   Using the precomputed prefix sums, we calculate the required sums in $O(1)$ time after the binary search step.
    *   The final answer is derived from the mathematical expansion of the sum of absolute differences:
        $$ \text{Total} = Y \cdot S_{A, X} + X \cdot S_{B, Y} - 2 \left( \sum_{j=1}^Y S_{A, \min(v_j, X)} + \sum_{j=1}^Y B_j \cdot \max(0, X - v_j) \right) $$
        where $S_{A, X}$ is the prefix sum of $A$ up to $X$.
4.  **Complexity**: Sorting takes $O(N \log N)$. Precomputation takes $O(N \log N)$ (due to bisect) or $O(N)$ if optimized, but $O(N \log N)$ is acceptable. Each query takes $O(\log N)$ for the binary search. Total time complexity is $O((N+K) \log N)$, which fits well within the limits.

## worker: Run the code against the provided sample inputs to
The code implements the optimized $O((N+K)\log N)$ solution derived in the thought process.
1.  **Sorting**: Arrays $A$ and $B$ are sorted.
2.  **Precomputation**:
    *   Prefix sums for $A$ and $B$ are computed.
    *   An array $v$ is precomputed where $v[j]$ is the count of elements in $A$ strictly less than $B[j]$ (using `bisect_right`). Since $B$ is sorted, $v$ is non-decreasing.
    *   Prefix sums over $v$ are computed for two specific terms: $\sum \text{prefA}[v[j]]$ and $\sum B[j] \cdot v[j]$.
3.  **Query Processing**:
    *   For each query $(X, Y)$, we determine a split point $k$ within the first $Y$ elements of $B$ such that for indices $j < k$, $v[j] < X$, and for $j \ge k$, $v[j] \ge X$. This is done using binary search (`bisect_right`) on the precomputed array $v$.
    *   Using the precomputed prefix sums, we calculate the required sums in $O(1)$ time after the binary search step.
    *   The final answer is derived from the mathematical expansion of the sum of absolute differences:
        $$ \text{Total} = Y \cdot S_{A, X} + X \cdot S_{B, Y} - 2 \left( \sum_{j=1}^Y S_{A, \min(v_j, X)} + \sum_{j=1}^Y B_j \cdot \max(0, X - v_j) \right) $$
        where $S_{A, X}$ is the prefix sum of $A$ up to $X$.
4.  **Complexity**: Sorting takes $O(N \log N)$. Precomputation takes $O(N \log N)$ (due to bisect) or $O(N)$ if optimized, but $O(N \log N)$ is acceptable. Each query takes $O(\log N)$ for the binary search. Total time complexity is $O((N+K) \log N)$, which fits well within the limits.

## worker: finalize
The solution implements an optimized $O((N+K)\log N)$ approach.
1.  **Sorting**: Arrays $A$ and $B$ are sorted to enable binary search and prefix sum logic.
2.  **Precomputation**:
    *   Prefix sums for $A$ and $B$ are computed.
    *   An array $v$ is precomputed where $v[j]$ is the count of elements in $A$ strictly less than $B[j]$ (using `bisect_right`). Since $B$ is sorted, $v$ is non-decreasing.
    *   Prefix sums over $v$ are computed for two specific terms: $\sum \text{prefA}[v[j]]$ and $\sum B[j] \cdot v[j]$.
3.  **Query Processing**:
    *   For each query $(X, Y)$, we determine a split point $k$ within the first $Y$ elements of $B$ such that for indices $j < k$, $v[j] < X$, and for $j \ge k$, $v[j] \ge X$. This is done using binary search (`bisect_right`) on the precomputed array $v$.
    *   Using the precomputed prefix sums, we calculate the required sums in $O(1)$ time after the binary search step.
    *   The final answer is derived from the mathematical expansion of the sum of absolute differences:
        $$ \text{Total} = Y \cdot S_{A, X} + X \cdot S_{B, Y} - 2 \left( \sum_{j=1}^Y S_{A, \min(v_j, X)} + \sum_{j=1}^Y B_j \cdot \max(0, X - v_j) \right) $$
        where $S_{A, X}$ is the prefix sum of $A$ up to $X$.
4.  **Complexity**: Sorting takes $O(N \log N)$. Precomputation takes $O(N \log N)$ (due to bisect) or $O(N)$ if optimized, but $O(N \log N)$ is acceptable. Each query takes $O(\log N)$ for the binary search. Total time complexity is $O((N+K) \log N)$, which fits well within the limits.
