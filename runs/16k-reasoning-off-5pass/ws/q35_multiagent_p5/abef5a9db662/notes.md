
## ideation
The core difficulty lies in efficiently simulating the rating changes for $Q$ queries without running an $O(N \cdot Q)$ simulation. The key insight is that the final rating function $f(X)$ (final rating given start $X$) is non-decreasing with respect to $X$. This monotonicity allows us to determine, for each contest, the range of starting ratings $[A_i, B_i]$ that will trigger an increase in that specific contest.

We can maintain the state of the rating for all possible starting values $X \in [1, 500000]$ simultaneously. Let $h(X)$ be the current rating after processing some contests, given a start of $X$. Initially $h(X) = X$.
For each contest $[L_i, R_i]$, we need to find the interval of starting ratings $[A_i, B_i]$ such that if we start at $X \in [A_i, B_i]$, the current rating $h(X)$ falls within $[L_i, R_i]$. Because $h(X)$ is non-decreasing, this set of $X$ forms a contiguous interval.
1. Find smallest $A_i$ such that $h(A_i) \ge L_i$.
2. Find largest $B_i$ such that $h(B_i) \le R_i$.
3. For all $X \in [A_i, B_i]$, the rating increases by 1. So we update $h(X) \leftarrow h(X) + 1$ for $X$ in this range.

To implement this efficiently:
- We use a Binary Indexed Tree (BIT) or Fenwick Tree to handle range updates (adding 1 to a range) and point queries (getting the current value of $h(X)$).
- Since the initial values are $h(X) = X$, we can store the *difference* $d(X) = h(X) - X$ in the BIT. Initially $d(X) = 0$.
- The actual value $h(X)$ is then $X + \text{BIT.query}(X)$.
- To find $A_i$ and $B_i$, we perform binary search over the domain $[1, M]$ (where $M=500000$). For a candidate $X$, we compute $h(X)$ using the BIT and compare with $L_i$ or $R_i$.
- Range update on $[A_i, B_i]$ is done in $O(\log M)$ using the BIT.
- Total complexity: $O(N \log M \cdot \log M)$ or $O(N \log M)$ if binary search is optimized. Given constraints $N, M \le 5 \cdot 10^5$, this is feasible.

Pitfalls:
- The range for binary search is only for initial ratings $X \in [1, 500000]$. The current ratings $h(X)$ can exceed 500000, but we only care about which initial $X$ leads to a valid current rating.
- Ensure binary search boundaries are correct (inclusive/exclusive).
- The BIT needs to support range updates and point queries. This can be done with a standard BIT by updating `val[l] += 1` and `val[r+1] -= 1`, and querying prefix sums.

## worker: none
The problem requires determining the final rating for multiple starting values after a sequence of conditional increments. A direct simulation for each query is too slow ($O(NQ)$).

Key Insight:
Let $h(X)$ be the rating after processing some contests, given a starting rating $X$. The function $h(X)$ is non-decreasing with respect to $X$. This is because if you start with a higher rating, you will always have a rating greater than or equal to the one starting with a lower rating at any step (since increments are +1 and conditions are intervals).

For each contest $i$ with range $[L_i, R_i]$, we want to find the set of starting ratings $X$ such that the current rating $h_{i-1}(X)$ falls within $[L_i, R_i]$. Due to monotonicity, this set of $X$ values forms a contiguous interval $[A_i, B_i]$.
- $A_i$ is the smallest $X$ such that $h_{i-1}(X) \ge L_i$.
- $B_i$ is the largest $X$ such that $h_{i-1}(X) \le R_i$.

For all $X \in [A_i, B_i]$, the rating increases by 1. So we update $h_i(X) = h_{i-1}(X) + 1$ for $X$ in this range.

Algorithm:
1. Maintain the function $h(X)$ for $X \in [1, 500000]$. Initially $h(X) = X$.
2. Use a Binary Indexed Tree (BIT) to store the differences $d(X) = h(X) - X$. Initially $d(X) = 0$.
3. For each contest:
   - Use binary search on $X \in [1, 500000]$ to find $A_i$ and $B_i$. The value $h(X)$ is computed as $X + \text{BIT.query}(X)$.
   - If $A_i \le B_i$, perform a range update on the BIT: add 1 to $d(X)$ for $X \in [A_i, B_i]$. This is done by `bit_add(A_i, 1)` and `bit_add(B_i + 1, -1)`.
4. For each query $X$, the answer is $X + \text{BIT.query}(X)$.

Complexity:
- Each contest involves two binary searches, each taking $O(\log M \cdot \log M)$ or $O(\log M)$ depending on implementation. With a BIT, point query is $O(\log M)$, so binary search is $O(\log^2 M)$. Range update is $O(\log M)$.
- Total time: $O(N \log^2 M + Q \log M)$. With $N, Q, M \le 5 \cdot 10^5$, this is efficient enough.
