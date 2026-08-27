
## ideation
The core difficulty lies in determining the minimum number of swaps required at each specific index $i$ (between position $i$ and $i+1$). 

1.  **Cost Structure**: The cost of a swap at index $i$ is $i$. The total cost is $\sum_{i=1}^{N-1} i \times (\text{number of swaps at index } i)$.
2.  **Invariant/Flow Argument**: Consider the boundary between index $i$ and $i+1$. In the final sorted array, the elements at positions $1, \dots, i$ must be exactly the values $\{1, 2, \dots, i\}$.
    *   Let $S_i$ be the set of values currently at positions $1, \dots, i$.
    *   Let $T_i$ be the set of values currently at positions $i+1, \dots, N$.
    *   For the array to be sorted, all values in $\{1, \dots, i\}$ must end up in the left part, and all values in $\{i+1, \dots, N\}$ must end up in the right part.
    *   Any value $v \in S_i$ such that $v > i$ must eventually move to the right of the boundary (from left to right).
    *   Any value $v \in T_i$ such that $v \le i$ must eventually move to the left of the boundary (from right to left).
    *   The number of elements moving left-to-right across the boundary must equal the number of elements moving right-to-left to maintain the count of $i$ elements on the left.
    *   Specifically, the number of elements in $S_i$ that are greater than $i$ is exactly equal to the number of elements in $T_i$ that are less than or equal to $i$. Let this count be $C_i$.
    *   Therefore, exactly $C_i$ swaps must occur across the boundary between $i$ and $i+1$. It is a known result in sorting networks/adjacent swap problems that the minimum number of swaps across a cut is determined by this net flow. Since we want to minimize cost, and the cost per swap is fixed for a given index, we just need the minimum number of swaps, which is $C_i$.
3.  **Algorithm**:
    *   For each $i$ from $1$ to $N-1$:
        *   Count how many elements in $P[0 \dots i-1]$ (0-indexed) are greater than $i$ (1-indexed value). Note: The problem uses 1-based indexing for costs and values. $P$ is a permutation of $1 \dots N$.
        *   Actually, simpler: $C_i$ is the number of elements in the prefix $P[1 \dots i]$ that are $> i$.
    *   Sum $i \times C_i$ for all $i$.
4.  **Efficiency**: A naive calculation for each $i$ would be $O(N^2)$. With $N=2 \times 10^5$, we need $O(N \log N)$ or $O(N)$.
    *   We can compute $C_i$ efficiently.
    *   $C_i = (\text{count of elements in } P[1 \dots i] > i)$.
    *   Let's define an array `is_large` where `is_large[k] = 1` if $P[k] > i$ else $0$. But $i$ changes.
    *   Alternative view: $C_i$ is the number of inversions between the set of indices $\{1, \dots, i\}$ and values $\{i+1, \dots, N\}$? No.
    *   Let's use a Fenwick Tree (Binary Indexed Tree) or Segment Tree.
    *   We iterate $i$ from $1$ to $N$. We want to count elements in the prefix $P[1 \dots i]$ that are $> i$.
    *   This is equivalent to: (Total elements in prefix) - (Elements in prefix $\le i$).
    *   Total elements in prefix is $i$.
    *   So $C_i = i - (\text{count of elements in } P[1 \dots i] \text{ that are } \le i)$.
    *   We can maintain a data structure that stores the values seen so far. As we iterate $i$ from $1$ to $N$:
        *   Add $P[i]$ to the data structure.
        *   Query the number of elements in the data structure that are $\le i$.
        *   $C_i = i - \text{query}(i)$.
        *   Add $i \times C_i$ to the total cost.
    *   This approach is $O(N \log N)$.

## worker: (None)
The problem asks for the minimum cost to sort a permutation where swapping adjacent elements at indices $i$ and $i+1$ costs $i$. 

The key insight is that the minimum number of swaps that must occur across the boundary between position $i$ and $i+1$ is determined by the "flow" of elements across that boundary. In the sorted array, the first $i$ positions must contain the values $\{1, 2, \dots, i\}$. 

Let $S_i$ be the set of values currently at positions $1, \dots, i$. Any value in $S_i$ that is greater than $i$ must eventually move to the right of the boundary. Similarly, any value not in $S_i$ (i.e., in positions $i+1, \dots, N$) that is less than or equal to $i$ must move to the left. The number of such values moving right-to-left equals the number of values in $S_i$ greater than $i$. Let this count be $C_i$. 

Thus, exactly $C_i$ swaps must occur across the boundary between $i$ and $i+1$. The total cost is $\sum_{i=1}^{N-1} i \times C_i$.

To compute $C_i$ efficiently:
$C_i = i - (\text{number of elements in } P[1 \dots i] \text{ that are } \le i)$.

We iterate $i$ from $1$ to $N-1$. At each step, we add $P[i]$ (the $i$-th element, 1-based) to a data structure. We then query the number of elements seen so far that are $\le i$. A Fenwick Tree (BIT) allows us to do this in $O(\log N)$ time per step, leading to an overall $O(N \log N)$ solution.
