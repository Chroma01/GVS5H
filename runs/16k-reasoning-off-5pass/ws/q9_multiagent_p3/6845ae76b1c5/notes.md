
## ideation
**Core Difficulty**:
The problem asks for the sum of $|A_i - B_j|$ over a subgrid defined by indices $1 \dots X_k$ and $1 \dots Y_k$. A naive solution would iterate $O(X_k \cdot Y_k)$ per query, leading to $O(N^2 K)$ in the worst case, which is too slow ($10^{13}$ operations). We need a solution that preprocesses the data to answer each query efficiently (ideally $O(1)$ or $O(\log N)$).

**Key Insight**:
The absolute difference $|a - b|$ can be rewritten based on the relative order of $a$ and $b$:
- If $a \ge b$, $|a - b| = a - b$.
- If $a < b$, $|a - b| = b - a$.

Therefore, $\sum |A_i - B_j| = \sum_{A_i \ge B_j} (A_i - B_j) + \sum_{A_i < B_j} (B_j - A_i)$.
This can be split into:
$\sum_{A_i \ge B_j} A_i - \sum_{A_i \ge B_j} B_j + \sum_{A_i < B_j} B_j - \sum_{A_i < B_j} A_i$.

**Candidate Approaches**:
1.  **Sorting + Prefix Sums (Optimal)**:
    - Sort both arrays $A$ and $B$.
    - Precompute prefix sums for sorted $A$ and sorted $B$.
    - For a query $(X, Y)$, we are summing over the first $X$ elements of original $A$ and first $Y$ elements of original $B$.
    - *Wait*: The query restricts to the *first* $X$ elements of the *original* sequences, not the sorted ones. Sorting destroys the index mapping required by the query constraints ($A_1 \dots A_X$).
    - **Correction**: The query is on specific prefixes of the *original* arrays. We cannot simply sort and take the first $X$ elements because the set $\{A_1, \dots, A_X\}$ is not necessarily the $X$ smallest elements.
    - **Revised Strategy**:
        - The set of values involved in a query is fixed: $S_A = \{A_1, \dots, A_X\}$ and $S_B = \{B_1, \dots, B_Y\}$.
        - We need to compute $\sum_{a \in S_A} \sum_{b \in S_B} |a - b|$.
        - This is equivalent to: $\sum_{a \in S_A} (\sum_{b \in S_B, b \le a} (a-b) + \sum_{b \in S_B, b > a} (b-a))$.
        - Let's sort the specific subset $S_A$ and $S_B$ for each query? No, sorting takes $O(N \log N)$ per query, total $O(K N \log N) \approx 10^9$, might be TLE.
        - Better: Pre-sort the entire arrays $A$ and $B$. But the query is on prefixes of the *unsorted* arrays.
        - Actually, we can pre-calculate the sorted version of the whole array $A$ and $B$. But the query selects a subset of indices.
        - Let's reconsider the structure. We have $K$ queries. Each query defines a subset of $A$ (first $X$) and a subset of $B$ (first $Y$).
        - Since $K$ is up to $10^4$ and $N$ up to $10^5$, an $O(N)$ per query is $10^9$, likely too slow. We need something faster, like $O(\log N)$ or $O(1)$.
        - Is there a way to use the sorted global arrays?
        - Let $A'$ be sorted $A$, $B'$ be sorted $B$.
        - The sum is $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
        - This looks like we need to count how many $B_j$'s are $\le A_i$ and how many are $> A_i$.
        - Since the sets $S_A$ and $S_B$ change per query, we can't easily use global prefix sums unless we can quickly query "sum of elements in $A[1..X]$ that are $\le V$" and "count of elements in $A[1..X]$ that are $\le V$".
        - This is a classic **2D Range Sum** problem (or rather, orthogonal range counting/summing).
        - Points are $(index, value)$. We want to sum values in a rectangle $[1, X] \times [0, V]$ and count points in $[1, X] \times [0, V]$.
        - Since coordinates are static, we can use **Merge Sort Tree** or **Persistent Segment Tree** or simply **Offline Processing with Fenwick Tree (BIT)**.
        - **Offline Approach**:
            1. Sort queries by $X$.
            2. Iterate $x$ from $1$ to $N$. Add $A_x$ to a data structure.
            3. For queries with current $X$, we need to query the data structure for sums involving $B$.
            4. Wait, the query involves a specific subset of $B$ ($B[1..Y]$) as well.
            5. We need $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
            6. Split: $\sum_{i=1}^X \left( \sum_{j=1}^Y [B_j \le A_i] (A_i - B_j) + \sum_{j=1}^Y [B_j > A_i] (B_j - A_i) \right)$.
            7. This equals: $\sum_{i=1}^X \left( [B_j \le A_i] \cdot A_i - [B_j \le A_i] \cdot B_j + [B_j > A_i] \cdot B_j - [B_j > A_i] \cdot A_i \right)$.
            8. Group by $A_i$:
               - Term 1: $A_i \times (\text{count of } B_j \in \{B_1..B_Y\} \text{ s.t. } B_j \le A_i)$
               - Term 2: $- (\text{sum of } B_j \in \{B_1..B_Y\} \text{ s.t. } B_j \le A_i)$
               - Term 3: $+ (\text{sum of } B_j \in \{B_1..B_Y\} \text{ s.t. } B_j > A_i)$
               - Term 4: $- A_i \times (\text{count of } B_j \in \{B_1..B_Y\} \text{ s.t. } B_j > A_i)$
            9. Notice that Terms 1 and 4 depend on $A_i$ and the count of $B$'s. Terms 2 and 3 depend on the sum of $B$'s.
            10. Let $C(V, Y) = \text{count of } \{B_1..B_Y\} \le V$.
            11. Let $S(V, Y) = \text{sum of } \{B_1..B_Y\} \le V$.
            12. Then contribution of $A_i$ is: $A_i \cdot C(A_i, Y) - S(A_i, Y) + (S_{total}(Y) - S(A_i, Y)) - A_i \cdot (Y - C(A_i, Y))$.
            13. Simplify: $A_i (2 C(A_i, Y) - Y) + S_{total}(Y) - 2 S(A_i, Y)$.
            14. Total Answer for $(X, Y) = \sum_{i=1}^X [ A_i (2 C(A_i, Y) - Y) + S_{total}(Y) - 2 S(A_i, Y) ]$.
            15. This still requires calculating $C(A_i, Y)$ and $S(A_i, Y)$ for each $i \in 1..X$. If we do this naively, it's $O(X \log N)$ or $O(X)$ per query. Total $O(NK)$ worst case. Too slow.

    **Alternative Idea**:
    Can we swap the loops?
    Total Sum = $\sum_{j=1}^Y \sum_{i=1}^X |A_i - B_j|$.
    For a fixed $B_j$, we need $\sum_{i=1}^X |A_i - B_j|$.
    This is the sum of distances from $B_j$ to the first $X$ elements of $A$.
    Let $f(X, V) = \sum_{i=1}^X |A_i - V|$.
    We need $\sum_{j=1}^Y f(X, B_j)$.
    $f(X, V) = \sum_{i=1}^X (V - A_i)$ if $A_i \le V$ else $(A_i - V)$.
    $f(X, V) = V \cdot \text{count}(A_1..A_X \le V) - \text{sum}(A_1..A_X \le V) + \text{sum}(A_1..A_X > V) - V \cdot \text{count}(A_1..A_X > V)$.
    Let $cntA(X, V)$ be count of $A_i \le V$ in first $X$, $sumA(X, V)$ be sum.
    $f(X, V) = V \cdot cntA(X, V) - sumA(X, V) + (SumA(X) - sumA(X, V)) - V \cdot (X - cntA(X, V))$.
    $f(X, V) = V(2 cntA(X, V) - X) + SumA(X) - 2 sumA(X, V)$.
    So Answer = $\sum_{j=1}^Y [ B_j(2 cntA(X, B_j) - X) + SumA(X) - 2 sumA(X, B_j) ]$.
    $= 2 cntA(X, \cdot) \cdot B_j - X B_j + SumA(X) - 2 sumA(X, B_j)$.
    This requires evaluating $cntA(X, B_j)$ and $sumA(X, B_j)$ for each $j=1..Y$.
    This is still $O(Y \log N)$ per query. Total $O(NK)$.

    **Is $O(NK)$ acceptable?**
    $N=10^5, K=10^4 \implies 10^9$. In Python, this will definitely TLE (Time Limit Exceeded). We need something closer to $O((N+K) \log N)$ or $O((N+K) \sqrt N)$.

    **Re-evaluating the constraints and problem type**:
    Usually, if $N, K$ are large, we need offline processing with a data structure that supports updates and range queries.
    The term $cntA(X, V)$ is the number of elements in $A[1..X]$ that are $\le V$.
    The term $sumA(X, V)$ is the sum of elements in $A[1..X]$ that are $\le V$.
    This is exactly a **2D range sum** problem:
    - Points: $(i, A_i)$ for $i=1..N$.
    - Query: Count/Sum points in rectangle $[1, X] \times [0, V]$.
    
    We have $K$ queries of the form $(X, Y)$.
    The answer is $\sum_{j=1}^Y f(X, B_j)$.
    This looks like we can't easily separate $X$ and $Y$ because $f(X, B_j)$ depends on both.
    However, notice the symmetry.
    Total Sum = $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
    Let's try to compute this using **offline processing with a Fenwick Tree (BIT)**.
