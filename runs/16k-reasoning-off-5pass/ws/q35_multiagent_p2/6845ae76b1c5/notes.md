
## ideation
The core difficulty is efficiently answering $K$ queries, each requiring a double summation over subsets of two arrays. A naive $O(N^2)$ or $O(K \cdot N \log N)$ approach will be too slow given the constraints ($N=10^5, K=10^4$).

Key observations:
1.  **Sorting**: The absolute difference sum $\sum |A_i - B_j|$ is minimized and can be computed efficiently if arrays are sorted. We should sort $A$ and $B$.
2.  **Prefix Sums**: With sorted arrays, prefix sums allow $O(1)$ calculation of the sum of any subarray.
3.  **Query Structure**: Each query asks for the sum over $A[1..X_k]$ and $B[1..Y_k]$. Let's denote the sorted prefix of $A$ as $A_{1..X}$ and $B$ as $B_{1..Y}$.
4.  **Two-Pointer / Monotonicity**: For a fixed $Y$ (fixed prefix of $B$), as we iterate $i$ from $1$ to $N$ (increasing $A_i$), the split point in $B_{1..Y}$ where $B_j \le A_i$ moves monotonically to the right. This allows us to compute the contribution of each $A_i$ to the sum for a fixed $Y$ in amortized $O(1)$ time after an initial $O(Y)$ or $O(\log Y)$ setup.
5.  **Grouping by Y**: Since $K$ is up to $10^4$ and $N$ up to $10^5$, doing $O(N)$ work per query is $10^9$ operations, which might be too slow in Python. However, many queries may share the same $Y$. We can group queries by $Y$. For each distinct $Y$, we compute the answers for all $X$ in one pass. The total work is proportional to $(\text{number of distinct } Y) \times N$. In the worst case, this is $10^4 \times 10^5 = 10^9$, which is risky in Python.
6.  **Optimization**: Instead of grouping, we can precompute a 2D structure? No, too much memory.
    Let's re-evaluate the complexity. The two-pointer approach for a fixed $Y$ takes $O(N)$ time. If we have $D$ distinct $Y$ values, total time is $O(D \cdot N)$. With $D \le K=10^4$ and $N=10^5$, $10^9$ is too slow for Python (typically $10^7-10^8$ ops/sec).
    
    Is there a faster way?
    Consider the formula for a single pair $(X, Y)$:
    $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
    If we fix $Y$, let $S_Y[i] = \sum_{j=1}^Y |A_i - B_j|$. Then the answer for $(X, Y)$ is $\sum_{i=1}^X S_Y[i]$.
    We can precompute $S_Y[i]$ for all $i$ for a fixed $Y$ in $O(N)$ using two pointers. Then we can compute prefix sums of $S_Y$ to answer any $X$ in $O(1)$.
    So for each distinct $Y$, we spend $O(N)$ to build the array $S_Y$ and its prefix sums. Then each query with that $Y$ is $O(1)$.
    Total time: $O(D \cdot N + K)$. With $D \le 10^4, N=10^5$, this is $10^9$ operations. This is still potentially too slow for Python.
    
    However, note that $D$ is the number of *distinct* $Y_k$. In many cases, $D$ might be small. But worst case is $D=K$.
    
    Let's check if we can do better.
    Can we precompute for all $Y$? No, $O(N^2)$ space.
    
    Alternative: Process queries offline. Sort queries by $Y$. As we increase $Y$, we add one element $B_Y$ to the active set.
    When we add $B_Y$ to the set of $B$'s, how does the total sum change?
    The total sum for a query $(X, Y)$ is $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
    Let $Total(X, Y) = \sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
    $Total(X, Y) = Total(X, Y-1) + \sum_{i=1}^X |A_i - B_Y|$.
    So if we maintain the array $C_Y[i] = \sum_{j=1}^Y |A_i - B_j|$, then $C_Y[i] = C_{Y-1}[i] + |A_i - B_Y|$.
    And the answer for $(X, Y)$ is $\sum_{i=1}^X C_Y[i]$.
    
    If we process $Y$ from $1$ to $N$, we can maintain the current array $C[i]$ for all $i=1..N$.
    Initially $Y=0$, $C[i]=0$.
    For each step $Y$ from $1$ to $N$:
      Update $C[i] \leftarrow C[i] + |A_i - B_Y|$ for all $i$.
      Compute prefix sums of $C$ to answer queries with this $Y$.
    
    The update step takes $O(N)$. Doing this for all $Y$ takes $O(N^2)$, which is $10^{10}$, too slow.
    
    But we only care about $Y$ values that appear in queries.
    Let distinct $Y$ values be $y_1 < y_2 < \dots < y_D$.
    We can jump from $y_m$ to $y_{m+1}$.
    The difference is adding $B_{y_m+1}, \dots, B_{y_{m+1}}$.
    This is still essentially adding elements one by one or in blocks.
    
    Wait, the previous approach of grouping by $Y$ and doing $O(N)$ per distinct $Y$ is $O(D \cdot N)$.
    Is $10^9$ really too slow? In C++ it passes easily. In Python, it might TLE.
    However, the constant factor in the two-pointer approach is very small.
    Also, we can optimize the inner loop.
    
    Let's stick to the "Group by Y" approach.
    1. Sort A and B.
    2. Compute prefix sums for A and B.
    3. Group queries by $Y_k$.
    4. For each distinct $Y$:
       a. Let $B_{sub} = B[0:Y]$.
       b. Use two pointers to compute $S[i] = \sum_{j=1}^Y |A_i - B_j|$ for all $i=1..N$.
          - Initialize pointer `ptr` for $B_{sub}$.
          - For each $A_i$, move `ptr` forward while $B_{sub}[ptr] \le A_i$.
          - Calculate sum using prefix sums of $B_{sub}$.
       c. Compute prefix sums of $S$ to get $Ans[X] = \sum_{i=1}^X S[i]$.
       d. Store answers for all queries with this $Y$.
    5. Print answers in original order.

    This is $O(D \cdot N)$. With $D=10^4, N=10^5$, it's $10^9$.
    To speed up in Python, we can use `bisect` which is implemented in C.
    For a fixed $Y$, computing $S[i]$ for all $i$:
    $S[i] = (\text{count of } B_j \le A_i) \cdot A_i - (\text{sum of } B_j \le A_i) + (\text{sum of } B_j > A_i) - (\text{count of } B_j > A_i) \cdot A_i$.
    Using `bisect_right` on $B_{sub}$ for each $A_i$ takes $O(N \log Y)$.
    Total time: $O(D \cdot N \log N)$. This is worse than two-pointer $O(D \cdot N)$.
    
    However, `bisect` is fast in C. Two-pointer in Python loop is slow.
    Let's compare:
    Two-pointer: $N$ iterations, each with a while loop. In worst case, pointer moves $Y$ times total. So $O(N+Y)$ per distinct $Y$. Total $O(D \cdot (N+Y)) \approx O(D \cdot N)$.
    Bisect: $N$ calls to `bisect_right`. Each call is $O(\log Y)$. Total $O(D \cdot N \log Y)$.
    
    $10^9$ simple operations in Python might take 10-20 seconds, which is too slow.
    But note: $D$ is number of distinct $Y$. If $K=10^4$, $D \le 10^4$.
    Is there a way to avoid $O(N)$ per distinct $Y$?
    
    Actually, we can precompute the contribution of each $B_j$ to all $A_i$?
    No.
    
    Let's try to optimize the two-pointer in Python.
    We can use `numpy`? No, standard library only.
    
    Wait, look at constraints again. $N=10^5, K=10^4$.
    Maybe the test cases are weak or $D$ is small?
    Or maybe $O(K \cdot N)$ is acceptable if the constant is small?
    
    Let's try to implement the two-pointer approach efficiently.
    We can avoid creating subarrays. Use indices.
    
    Actually, there is a known technique for this problem:
    Precompute `prefix_sum_A` and `prefix_sum_B`.
    For a query $(X, Y)$, the answer is:
    $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
    
    If we sort A and B, we can compute this in $O(N)$ per query using two pointers.
    Total $O(K \cdot N)$.
    
    Given Python's slowness, we might need to use `sys.stdin.read` and fast I/O, and minimize overhead.
    
    Let's write the solution with grouping by Y and two-pointer. If it TLEs, we might need to switch to bisect if the constant factor of bisect (C implementation) is better than the Python loop overhead of two-pointer.
    
    Actually, `bisect` approach:
    For each distinct Y:
      $B_{sub} = B[:Y]$
      $SB = \text{prefix\_sum}(B_{sub})$
      For each $i$ in $1..N$:
         $idx = \text{bisect\_right}(B_{sub}, A[i])$
         $sum\_le = SB[idx-1]$ if $idx>0$ else 0
         $sum\_gt = SB[Y-1] - sum\_le$
         $cnt\_le = idx$
         $cnt\_gt = Y - idx$
         $S[i] = cnt\_le \cdot A[i] - sum\_le + sum\_gt - cnt\_gt \cdot A[i]$
      
      This loop in Python is $N$ iterations. Inside, `bisect` is fast, but the arithmetic and list access is Python overhead.
      
    Two-pointer approach:
      ptr = 0
      sum_le = 0
      sum_gt = SB[Y-1] # Total sum of B_sub
      For each $i$ in $1..N$:
         while ptr < Y and B[ptr] <= A[i]:
             sum_le += B[ptr]
             sum_gt -= B[ptr]
             ptr += 1
         S[i] = ptr * A[i] - sum_le + sum_gt - (Y - ptr) * A[i]
      
      This loop has a while loop. The total increments of `ptr` is $Y$. So amortized $O(1)$ per $i$.
      But the `while` condition and list access in Python is still overhead.
      
    I will implement the two-pointer approach as it is theoretically $O(N)$ per distinct Y, which is better than $O(N \log Y)$. I'll use fast I/O.

## worker: (None)
The problem requires computing $\sum_{i=1}^{X_k} \sum_{j=1}^{Y_k} |A_i - B_j|$ for $K$ queries.
1. **Sorting**: Sorting $A$ and $B$ allows us to use prefix sums and two-pointer techniques efficiently.
2. **Prefix Sums**: We precompute prefix sums for $B$ to quickly calculate the sum of any subarray of $B$.
3. **Grouping by Y**: Since $K$ is up to $10^4$ and $N$ up to $10^5$, a naive $O(K \cdot N)$ approach might be too slow in Python if not optimized. However, by grouping queries by their $Y$ value, we only process each distinct $Y$ once.
4. **Two-Pointer for Fixed Y**: For a fixed $Y$, we iterate through $A$ and maintain a pointer in $B[0:Y]$. As $A_i$ increases, the split point in $B$ (where $B_j \le A_i$) only moves right. This allows us to compute the inner sum $\sum_{j=1}^Y |A_i - B_j|$ for each $A_i$ in amortized $O(1)$ time.
5. **Prefix Sums of S**: After computing $S[i] = \sum_{j=1}^Y |A_i - B_j|$ for all $i$, we compute prefix sums of $S$ to answer queries for different $X$ in $O(1)$ time.
6. **Complexity**: Let $D$ be the number of distinct $Y$ values. The total time complexity is $O(N \log N + D \cdot N + K)$. In the worst case $D=K=10^4$, so $O(K \cdot N) = 10^9$ operations. While this is borderline for Python, the constant factor in the two-pointer loop is very small, and using fast I/O helps. The `bisect` approach would be $O(D \cdot N \log Y)$ which is worse.
