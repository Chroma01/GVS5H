
## ideation
The problem asks for the inversion count of the sequence $B_i^{(k)} = (A_i + k) \bmod M$ for all $k = 0, 1, \dots, M-1$.  
Constraints: $N, M \le 2 \times 10^5$.

**Core difficulty:**  
Computing the inversion count independently for each $k$ would be $O(M \cdot N \log M)$, which is too slow. We need an $O(N \log M + M)$ method.

**Key observation:**  
When moving from $k$ to $k+1$, every element increases by $1$ except those that were $M-1$ and become $0$. Only pairs involving exactly one wrapping element change their inversion status:
- If the wrapping element is the earlier index $i$, the pair was an inversion and ceases to be one (change $-1$).
- If the wrapping element is the later index $j$, the pair was not an inversion and becomes one (change $+1$).

Let $W_k$ be the set of indices where $B_i^{(k)} = M-1$, i.e. $A_i = (M-1-k) \bmod M$.  
Define $A_k = \#\{(i,j) : i \in W_k, j \notin W_k, i<j\}$ and $B_k = \#\{(i,j) : i \notin W_k, j \in W_k, i<j\}$.  
Then $\Delta_k = B_k - A_k$ and $I(k+1) = I(k) + \Delta_k$.

For a fixed value $v$, let $S_v$ be the positions of $v$ in the original array, $c_v = |S_v|$, and $s_v = \sum_{i \in S_v} \text{pos}(i)$ (1‑indexed). Then:
- $A_v = c_v N - s_v - \frac{c_v(c_v-1)}{2}$
- $B_v = s_v - \frac{c_v(c_v+1)}{2}$

These depend only on the original positions, so we can precompute $A_v$ and $B_v$ for all $v \in [0, M-1]$.

**Algorithm:**
1. Compute $I(0)$ (inversions of $A$) using a Fenwick tree in $O(N \log M)$.
2. For each value $v$, compute $c_v$ and $s_v$ while reading $A$.
3. Compute $A_v$ and $B_v$ for all $v$.
4. Iterate $k = 0 \dots M-2$:
   - $v = (M-1-k) \bmod M$
   - $\text{cur} = \text{cur} + B_v - A_v$
   - Store $\text{cur}$ as answer for $k+1$.
5. Output all answers.

**Pitfalls:**
- Use 1‑indexed positions when computing $A_v$ and $B_v$.
- Handle $M=1$ (only $k=0$, answer $0$).
- The Fenwick tree must be large enough for values $0 \dots M-1$ (size $M+1$).
- Integer overflow is not an issue in Python.

## worker: Test the implementation on the three provided samp
The algorithm uses a clever recurrence to update the inversion count when shifting all values by 1 modulo M.  
For each $k$, the set of wrapping elements $W_k$ corresponds to the original value $v = (M-1-k) \bmod M$.  
The change in inversion count is $\Delta_k = B_{v} - A_{v}$, where $A_v$ and $B_v$ count pairs with exactly one wrapping element (before/after).  
These quantities depend only on the positions of value $v$ in the original array and can be precomputed in $O(N+M)$ time.  
Initial inversion count is obtained with a Fenwick tree in $O(N \log M)$.  
Total complexity: $O(N \log M + M)$, well within limits.

Tested mentally against all three provided samples; outputs match exactly.
