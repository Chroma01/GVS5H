
## ideation
The problem asks for the minimum cost to sort a permutation where swapping adjacent elements at indices $i$ and $i+1$ costs $i$.
The key insight is that the number of times a swap must occur between index $i$ and $i+1$ is determined by how many elements need to cross this boundary. Specifically, if we consider the set of values $\{1, 2, \ldots, i\}$, these values must eventually occupy the first $i$ positions in the sorted array. If there are $k$ values from this set currently located at indices $> i$, then exactly $k$ swaps must occur across the boundary $(i, i+1)$ to move these values to the left. Conversely, there are $i-k$ values from the set $\{1, \ldots, i\}$ currently at indices $\le i$, meaning there are $i-k$ values from $\{i+1, \ldots, N\}$ at indices $\le i$. The number of swaps is the number of elements crossing from right to left (or left to right), which is equal to the number of elements in the prefix $P[1 \dots i]$ that are greater than $i$. Let this count be $L_i$.
The total cost is $\sum_{i=1}^{N-1} i \times L_i$.
To compute $L_i$ efficiently for all $i$, we can iterate $i$ from 1 to $N-1$. At each step, we maintain a data structure (like a Fenwick Tree or Binary Indexed Tree) that stores the presence of elements seen so far in the prefix.
$L_i$ is the count of elements in $P[1 \dots i]$ that are $> i$.
This can be calculated as: $L_i = i - (\text{count of elements in } P[1 \dots i] \text{ that are } \le i)$.
The term $(\text{count of elements in } P[1 \dots i] \text{ that are } \le i)$ can be obtained by querying the Fenwick Tree for the prefix sum up to $i$ after inserting $P_i$.
The algorithm runs in $O(N \log N)$ time, which fits within the constraints ($N \le 2 \times 10^5$).

Pitfalls:
- Off-by-one errors in 1-based vs 0-based indexing. The problem uses 1-based indexing for costs.
- Incorrectly calculating the number of swaps. It's crucial to realize it's based on the set of values $\{1, \dots, i\}$ crossing the boundary.
- Using a naive $O(N^2)$ approach will TLE.

## worker: Implement the solution based on the provided logic
The solution relies on the key insight that the minimum cost to sort the permutation is the sum over all boundaries $i$ (from $1$ to $N-1$) of $i \times L_i$, where $L_i$ is the number of elements in the prefix $P[1 \dots i]$ that are greater than $i$. This $L_i$ represents the number of swaps that must occur between index $i$ and $i+1$ to ensure that the set of values $\{1, \dots, i\}$ ends up in the first $i$ positions.

To compute $L_i$ efficiently for all $i$, we use a Fenwick Tree (Binary Indexed Tree). As we iterate $i$ from $1$ to $N-1$:
1. We add the current element $P_i$ (using 1-based indexing for logic, so $P[i-1]$ in 0-based array) to the Fenwick Tree.
2. We query the Fenwick Tree to find the number of elements in the current prefix that are $\le i$.
3. We calculate $L_i = i - \text{query}(i)$.
4. We add $i \times L_i$ to the total cost.

This approach runs in $O(N \log N)$ time due to the Fenwick Tree operations, which is efficient enough for $N \le 2 \times 10^5$.
