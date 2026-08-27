
## ideation
The problem asks for the sum of $f(L, R)$ over all subarrays.
Key Insight:
1.  **Characterization of $f(L, R)$**: The value $f(L, R)$ represents the minimum number of operations to erase the subarray $A[L \dots R]$. The operation allows erasing a contiguous segment of the *current* blackboard if the values in that segment "cover" the segment (i.e., every position in the segment has a value present in the segment).
    This process is equivalent to decomposing the subarray into the minimum number of "primitive" segments. A segment $[L, R]$ is primitive if it cannot be split into $[L, k]$ and $[k+1, R]$ such that the set of values in the left part is disjoint from the set of values in the right part.
    Therefore, $f(L, R) = (R - L + 1) - \sum_{k=L}^{R-1} I(\text{cut at } k)$, where $I(\text{cut at } k)$ is 1 if the set of values in $A[L \dots k]$ is disjoint from the set of values in $A[k+1 \dots R]$.

2.  **Summation Transformation**:
    We need to compute $\sum_{L=1}^N \sum_{R=L}^N f(L, R)$.
    Let $Total = \sum_{L=1}^N \sum_{R=L}^N (R - L + 1)$. This is easy to compute in $O(1)$ or $O(N)$.
    Let $Cuts = \sum_{L=1}^N \sum_{R=L}^N \sum_{k=L}^{R-1} I(S(L, k) \cap S(k+1, R) = \emptyset)$.
    Swapping the order of summation for $Cuts$:
    $Cuts = \sum_{k=1}^{N-1} \sum_{L=1}^{k} \sum_{R=k+1}^{N} I(S(L, k) \cap S(k+1, R) = \emptyset)$.

3.  **Evaluating the Inner Sum**:
    For a fixed $k$ and $L$, the condition $S(L, k) \cap S(k+1, R) = \emptyset$ means that no value present in $A[L \dots k]$ appears in $A[k+1 \dots R]$.
    Let $Val_L = S(L, k)$. The condition holds for $R$ if $A[k+1 \dots R]$ contains no value from $Val_L$.
    Let $NextPos(v, k+1)$ be the first occurrence of value $v$ in $A$ at an index $> k$.
    Then, for a fixed $L$, the valid $R$'s are those such that $R < \min_{v \in Val_L} NextPos(v, k+1)$.
    Let $Limit(L, k) = \min_{v \in S(L, k)} NextPos(v, k+1)$. If $Val_L$ is empty, limit is $\infty$.
    The number of valid $R$'s is $\max(0, Limit(L, k) - (k + 1))$.

4.  **Efficient Calculation**:
    $Limit(L, k) = \min(Limit(L+1, k), NextPos(A[L], k+1))$.
    Note that $NextPos(A[L], k+1)$ is simply the next occurrence of $A[L]$ after index $L$, which we can precompute as `nxt[L]`.
    So, $Limit(L, k) = \min_{j=L}^{k} nxt[j]$.
    We need to compute $\sum_{k=1}^{N-1} \sum_{L=1}^{k} \max(0, \min_{j=L}^{k} nxt[j] - k - 1)$.
    
    This can be computed efficiently. For each $k$, we want to sum over $L \le k$.
    Let $m_j = nxt[j]$. We need $\sum_{L=1}^{k} \max(0, \min_{j=L}^{k} m_j - k - 1)$.
    As $L$ decreases from $k$ to 1, the minimum $\min_{j=L}^{k} m_j$ is non-decreasing.
    We can use a monotonic stack to maintain the "next smaller element" structure.
    Specifically, for each $k$, we can determine the ranges of $L$ where the minimum is determined by a specific $m_j$.
    
    However, a simpler $O(N)$ or $O(N \log N)$ approach:
    Iterate $k$ from 1 to $N-1$. Maintain a data structure that allows querying the sum of $\max(0, \min_{j=L}^{k} m_j - k - 1)$.
    Alternatively, iterate $L$ from $N$ down to 1.
    For a fixed $L$, as $k$ increases from $L$ to $N-1$, $M(L, k) = \min_{j=L}^{k} m_j$ is non-increasing.
    We can maintain the current minimum and sum. But this is $O(N^2)$.
    
    Given constraints $N \le 3 \times 10^5$, $O(N^2)$ is too slow.
    We need to compute $Cuts$ in $O(N \log N)$ or $O(N)$.
    
    Let's use the property:
    $Cuts = \sum_{k=1}^{N-1} \sum_{L=1}^{k} \max(0, M(L, k) - k - 1)$.
    For a fixed $k$, let $g_k(L) = M(L, k)$.
    $g_k(L) = \min(m_L, g_k(L+1))$.
    
    We can use a segment tree or a stack to manage the values $m_j$.
    Actually, we can process this by iterating $k$ and maintaining a stack of indices $j$ such that $m_j$ are increasing.
    For each $k$, we push $k$ onto the stack, popping elements larger than $m_k$.
    The stack stores indices $idx_1 < idx_2 < \dots < idx_p = k$ with $m_{idx_1} < m_{idx_2} < \dots < m_{idx_p}$.
    For any $L \in (idx_{i-1}, idx_i]$, the minimum $\min_{j=L}^{k} m_j$ is $m_{idx_i}$.
    So for a fixed $k$, the sum over $L$ is:
    $\sum_{i=1}^{p} \sum_{L=idx_{i-1}+1}^{idx_i} \max(0, m_{idx_i} - k - 1)$.
    The inner sum is $(idx_i - idx_{i-1}) \times \max(0, m_{idx_i} - k - 1)$.
    
    This allows computing the contribution of each $k$ in $O(\text{stack size})$. Total time $O(N)$.

## worker: (None)
1.  **Problem Analysis**: The function $f(L, R)$ counts the minimum operations to erase a subarray. This is equivalent to the number of "primitive" segments in the decomposition of the subarray. A cut exists at $k$ ($L \le k < R$) if the set of values in $A[L \dots k]$ is disjoint from the set of values in $A[k+1 \dots R]$.
2.  **Formula Derivation**:
    $f(L, R) = (R - L + 1) - \sum_{k=L}^{R-1} I(\text{cut at } k)$.
    Summing over all $L, R$:
    $\sum f(L, R) = \sum (R - L + 1) - \sum_{k} \sum_{L \le k} \sum_{R > k} I(\text{cut at } k)$.
3.  **Cut Condition**: A cut at $k$ for a given $L$ exists for $R$ if $A[k+1 \dots R]$ contains no value from $A[L \dots k]$. This means $R$ must be less than the first occurrence of any value in $A[L \dots k]$ after index $k$.
    Let $Limit(L, k) = \min_{j=L}^{k} nxt[j]$, where $nxt[j]$ is the next occurrence of $A[j]$ after $j$.
    The number of valid $R$'s for a fixed $L, k$ is $\max(0, Limit(L, k) - (k + 1))$.
4.  **Efficient Calculation**:
    We need to compute $\sum_{k=0}^{N-2} \sum_{L=0}^{k} \max(0, \min_{j=L}^{k} nxt[j] - k - 1)$.
    For a fixed $k$, as $L$ decreases, the minimum $\min_{j=L}^{k} nxt[j]$ changes only at specific points. We can use a monotonic stack to maintain the indices $j$ where $nxt[j]$ is a new minimum when scanning from $k$ down to 0.
    The stack stores indices $idx_0 < idx_1 < \dots < idx_p = k$ with increasing $nxt$ values.
    For $L \in (idx_{i-1}, idx_i]$, the minimum is $nxt[idx_i]$.
    The contribution is $(idx_i - idx_{i-1}) \times \max(0, nxt[idx_i] - k - 1)$.
    This allows computing the total cuts in $O(N)$ time.
5.  **Complexity**: Precomputing `nxt` takes $O(N)$. The main loop runs $N$ times, and each index is pushed and popped from the stack at most once, so the inner while loop and the final summation over the stack take amortized $O(1)$ per $k$. Total time complexity is $O(N)$. Space complexity is $O(N)$.
