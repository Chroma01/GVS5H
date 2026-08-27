
## ideation
The problem asks for the minimum cost to sort a permutation using adjacent swaps where swapping elements at indices $i$ and $i+1$ (1-based) costs $i$.

Key Insight:
1.  **Boundary Swaps**: Consider the boundary between position $k$ and $k+1$. Any element that starts in the left part ($1 \dots k$) but belongs in the right part ($k+1 \dots N$) must cross this boundary to the right. Similarly, any element that starts in the right part but belongs in the left part must cross to the left.
2.  **Net Flow**: Let $S_{start}$ be the set of values initially at positions $1 \dots k$, and $S_{target}$ be the set of values that should end at positions $1 \dots k$ (which is simply $\{1, 2, \dots, k\}$).
3.  **Number of Crossings**: The number of elements that need to move from left to right across the boundary $k$ is $|S_{start} \setminus S_{target}|$. The number of elements that need to move from right to left is $|S_{target} \setminus S_{start}|$. These two quantities are equal. Let this count be $C_k$.
4.  **Cost Calculation**: Each crossing of the boundary between $k$ and $k+1$ corresponds to exactly one swap operation at index $k$. Since we want to minimize cost, we should perform the necessary swaps. The minimum number of swaps across boundary $k$ is exactly $C_k$. Why? Because each swap across this boundary changes the "balance" of elements on the left side by 1. To get from the initial configuration to the target configuration, we need exactly $C_k$ net transfers. Since swaps are the only way to transfer, and we can't "undo" progress efficiently without paying more, the minimum number of swaps across boundary $k$ is $C_k$.
5.  **Total Cost**: The total cost is the sum over all boundaries $k=1$ to $N-1$ of (number of swaps across boundary $k$) $\times$ (cost per swap at $k$).
    $$ \text{Total Cost} = \sum_{k=1}^{N-1} C_k \times k $$
    where $C_k$ is the number of elements in the first $k$ positions of the initial permutation that are greater than $k$. Alternatively, $C_k = k - (\text{number of elements in the first } k \text{ positions that are } \le k)$.

Algorithm:
1.  Read $N$ and the permutation $P$.
2.  We need to compute $C_k$ for each $k$ from $1$ to $N-1$.
3.  $C_k$ is the count of $P_i$ such that $1 \le i \le k$ and $P_i > k$.
4.  This can be computed efficiently. Let's define an array or use a Fenwick tree / Binary Indexed Tree (BIT) or simply iterate if $O(N^2)$ is too slow? $N \le 2 \times 10^5$, so $O(N^2)$ is too slow.
5.  We can compute the number of elements $\le k$ in the first $k$ positions. Let this be $M_k$. Then $C_k = k - M_k$.
6.  How to compute $M_k$ for all $k$?
    $M_k$ is the count of $i \in \{1, \dots, k\}$ such that $P_i \le k$.
    This looks like a 2D range query or can be solved with a sweep-line.
    Alternatively, notice that $C_k$ is the number of inversions involving a specific boundary? No.
    Let's use a BIT. We can iterate $k$ from $1$ to $N$.
    We want to count how many numbers in $P[1 \dots k]$ are $\le k$.
    This is equivalent to: Count pairs $(i, P_i)$ such that $i \le k$ and $P_i \le k$.
    This is a standard problem. We can process queries offline or online.
    Actually, we can just iterate $k$ from $1$ to $N-1$.
    Let's maintain a data structure that stores the positions of the numbers we've seen.
    Wait, simpler:
    $C_k = \sum_{i=1}^k [P_i > k]$.
    We can compute this for all $k$ using a Fenwick Tree (BIT) over the values $1 \dots N$.
    Iterate $i$ from $1$ to $N$:
    - Add $P_i$ to the BIT at position $P_i$.
    - After adding $P_i$, the BIT contains all $P_j$ for $j \le i$.
    - For a specific $k=i$, we want to count how many $P_j$ ($j \le k$) are $> k$.
    - Total elements in BIT is $k$.
    - Number of elements $\le k$ in BIT is `query(k)`.
    - So $C_k = k - \text{query}(k)$.
    - Add $C_k \times k$ to the total cost.
    
    This approach is $O(N \log N)$.

Pitfalls:
- 1-based indexing for costs and positions.
- Large numbers: Cost can exceed $2^{31}-1$, so use 64-bit integers.
- The loop for $k$ goes up to $N-1$.

## worker: <empty>
The problem asks for the minimum cost to sort a permutation using adjacent swaps where swapping elements at 1-based indices $i$ and $i+1$ costs $i$.

The key insight is to consider the "flow" of elements across each boundary between position $k$ and $k+1$. Let $C_k$ be the number of elements that start in the first $k$ positions but belong in the last $N-k$ positions (i.e., their target position is $> k$). Equivalently, $C_k$ is the number of elements in the first $k$ positions of the initial permutation that have a value greater than $k$.

Each such element must cross the boundary between $k$ and $k+1$ exactly once (moving right). Similarly, elements that start in the last $N-k$ positions but belong in the first $k$ positions (values $\le k$) must cross the boundary to the left. The number of such elements is also $C_k$. The minimum number of swaps across the boundary $k$ is exactly $C_k$. Since each swap across this boundary costs $k$, the total cost contributed by this boundary is $C_k \times k$.

The total minimum cost is the sum over all boundaries $k=1$ to $N-1$ of $C_k \times k$.

To compute $C_k$ efficiently for all $k$:
$C_k = k - (\text{number of elements in } P[0 \dots k-1] \text{ that are } \le k)$.

We can use a Fenwick Tree (BIT) to maintain the counts of values seen so far. As we iterate $k$ from $1$ to $N-1$:
1. Add the value $P[k-1]$ (the $k$-th element) to the BIT.
2. Query the BIT to find how many values $\le k$ have been added.
3. Compute $C_k = k - \text{query}(k)$.
4. Add $C_k \times k$ to the total cost.

This approach runs in $O(N \log N)$ time, which is efficient for $N \le 2 \times 10^5$.
