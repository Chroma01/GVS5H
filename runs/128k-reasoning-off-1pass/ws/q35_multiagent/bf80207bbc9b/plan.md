The key observation is that since W is small (up to 18), we can iterate over all possible subsets of columns to flip using Operation Y. There are $2^W$ such subsets. For each fixed configuration of column flips, the state of each row becomes fixed relative to the column flips. Specifically, for a row $i$, if we decide whether to flip it (Operation X) or not, the resulting row vector is determined. To minimize the sum of 1s, for each row independently, we should choose to flip it or not based on which choice yields fewer 1s in that row after the column flips have been applied. We precompute the "cost" of each row pattern: for each possible column-flip mask, we calculate the minimum 1s in that row by either keeping it as-is or flipping it. We then sum these minimums across all rows for each column-flip mask and take the global minimum. The complexity will be $O(H \cdot 2^W)$, which is feasible since $H \le 2 \cdot 10^5$ and $W \le 18$ ($2^{18} \approx 2.6 \cdot 10^5$, so total operations $\approx 5 \cdot 10^{10}$ might be too slow in Python). 

Wait, $H \cdot 2^W$ is too large for Python. We need a more efficient approach. Notice that flipping a row is equivalent to XORing the row with all 1s. Let $R_i$ be the integer representation of row $i$. Let $M$ be the mask of columns flipped by Operation Y. After column flips, row $i$ becomes $R_i \oplus M$. Then we can optionally flip the entire row, which means we can choose between $R_i \oplus M$ and $(R_i \oplus M) \oplus (2^W - 1)$. The number of 1s in a bitmask $B$ is `popcount(B)`. So for each row $i$ and mask $M$, the cost is $\min(\text{popcount}(R_i \oplus M), \text{popcount}((R_i \oplus M) \oplus (2^W-1)))$. 

To speed this up, we can group identical rows. Let `count[v]` be the number of rows with value $v$. Then the total cost for a mask $M$ is $\sum_{v=0}^{2^W-1} \text{count}[v] \cdot \min(\text{popcount}(v \oplus M), \text{popcount}((v \oplus M) \oplus (2^W-1)))$. This is still $O(2^W \cdot 2^W)$ if done naively, which is $2^{36}$, too slow.

However, note that $\min(\text{popcount}(A), \text{popcount}(A \oplus \text{ALL\_ONES}))$ depends only on the popcount of $A$ and $W$. Specifically, if $A$ has $k$ ones, then $A \oplus \text{ALL\_ONES}$ has $W-k$ ones. So the cost for a transformed row value $T = v \oplus M$ is $\min(\text{popcount}(T), W - \text{popcount}(T))$. 

Let $f(T) = \min(\text{popcount}(T), W - \text{popcount}(T))$. We need to compute $\sum_{v} \text{count}[v] \cdot f(v \oplus M)$ for each $M$. This is a convolution-like structure. Since $W$ is small, we can use Fast Walsh-Hadamard Transform (FWHT) or simply iterate. But $2^W$ is up to $2^{18}$. Iterating over all $M$ and all $v$ is $2^{36}$. 

Alternative: Since $H$ is large but $W$ is small, the number of distinct row patterns is at most $\min(H, 2^W)$. Let $U$ be the set of unique row values present. $|U| \le 2^W$. We can iterate over all $M \in [0, 2^W-1]$ and for each $M$, iterate over all unique $v \in U$. The complexity is $O(2^W \cdot \min(H, 2^W))$. In the worst case, this is $2^{18} \cdot 2^{18} = 2^{36}$, which is too slow.

Let's re-evaluate. We want $\min_M \sum_i \min(\text{popcount}(R_i \oplus M), W - \text{popcount}(R_i \oplus M))$.
Let $g(M) = \sum_i \min(\text{popcount}(R_i \oplus M), W - \text{popcount}(R_i \oplus M))$.
We can precompute `cnt[k][p]` = number of rows $i$ such that $\text{popcount}(R_i) = k$ and ... no, the interaction is via XOR.

Actually, $2^{18}$ iterations for $M$ is fine if the inner loop is fast. The inner loop sums over $H$ rows. $H \cdot 2^W \approx 2 \cdot 10^5 \cdot 2.6 \cdot 10^5 \approx 5 \cdot 10^{10}$, which is too slow for Python (and likely C++).

We need to use the fact that we can group identical rows. Let `freq[v]` be the frequency of row value `v`. The number of unique values is at most $2^W$. But also at most $H$.
The sum is $\sum_{v} \text{freq}[v] \cdot f(v \oplus M)$.
This is equivalent to a convolution if we define appropriate functions, but $f$ is not linear.

However, note that $f(T)$ only depends on $\text{popcount}(T)$. Let $h[k] = \min(k, W-k)$. Then $f(T) = h[\text{popcount}(T)]$.
So we need $\sum_v \text{freq}[v] \cdot h[\text{popcount}(v \oplus M)]$.

Let's define an array $A$ of size $2^W$ where $A[v] = \text{freq}[v]$.
We want to compute for each $M$: $S[M] = \sum_v A[v] \cdot h[\text{popcount}(v \oplus M)]$.
This can be rewritten as $S[M] = \sum_v A[v] \cdot h[\text{popcount}(v \oplus M)]$.
Let $B[k] = \sum_{v: \text{popcount}(v)=k} A[v]$. This groups rows by their popcount. But $v \oplus M$'s popcount depends on the specific bits of $v$ and $M$, not just the popcount of $v$. So this grouping doesn't directly help with the XOR.

Wait, $W \le 18$ is small enough for $O(3^W)$? No.
Is there a property we can exploit?
Note that $h[k] = \min(k, W-k)$.
Let's just implement the $O(H \cdot 2^W)$ solution in C++? No, must be Python.
In Python, $5 \cdot 10^{10}$ is impossible.

Let's look at constraints again. $W \le 18$.
Maybe we can iterate over $M$ and use bit-level parallelism or precomputed popcounts?
Precomputing popcounts for all $0 \dots 2^W-1$ takes $O(2^W)$.
Then for each $M$, we iterate over all unique row values $v$.
Number of unique row values is at most $\min(H, 2^W)$.
If $H$ is very large, many rows are duplicates.
Worst case: $H = 2^W$, all distinct. Then we do $2^W \cdot 2^W = 2^{36}$ ops.

There must be a better way.
Let's consider the contribution of each bit position? No, the min function couples the bits.

Actually, let's look at similar problems. This is equivalent to finding a mask $M$ and row flips to minimize 1s.
This is equivalent to: for each row, we can choose to flip it or not. Let $r_i \in \{0, 1\}$ be the choice to flip row $i$. Let $c_j \in \{0, 1\}$ be the choice to flip column $j$.
The final value at $(i,j)$ is $A_{i,j} \oplus c_j \oplus r_i$.
We want to minimize $\sum_{i,j} (A_{i,j} \oplus c_j \oplus r_i)$.

This is a minimum cut problem or can be solved with FWHT?
Let's try FWHT.
Let $U$ be the matrix of values. We want to choose row vector $R$ and column vector $C$ to minimize $\sum_{i,j} (A_{i,j} \oplus C_j \oplus R_i)$.
This is not a standard convolution.

However, note that $W$ is small. We can iterate over all $2^W$ column masks $M$.
For a fixed $M$, the problem reduces to: for each row $i$, we have a target pattern $T_i = R_i \oplus M$. We can flip $T_i$ to $T_i \oplus \text{ALL}$. We want to minimize the sum of popcounts.
This part is easy: for each row, cost is $\min(\text{popcount}(T_i), W - \text{popcount}(T_i))$.
The bottleneck is computing this sum for all $M$.

Let $F[M] = \sum_{i=1}^H \min(\text{popcount}(R_i \oplus M), W - \text{popcount}(R_i \oplus M))$.
Let $g(v) = \min(\text{popcount}(v), W - \text{popcount}(v))$.
$F[M] = \sum_{v=0}^{2^W-1} \text{freq}[v] \cdot g(v \oplus M)$.
This is a convolution of `freq` and `g` under XOR?
No, $g(v \oplus M)$ is not $g(v) * g(M)$. It is a correlation.
Specifically, $F[M] = (\text{freq} \star g)[M]$ where $\star$ is XOR correlation.
XOR convolution can be computed using FWHT in $O(W 2^W)$.
Recall that FWHT allows us to compute $C[k] = \sum_{i \oplus j = k} A[i] B[j]$.
Here we have $\sum_v \text{freq}[v] g(v \oplus M)$. Let $u = v \oplus M$, then $v = u \oplus M$.
Sum becomes $\sum_u \text{freq}[u \oplus M] g(u)$.
This is exactly the XOR convolution of `freq` and `g` evaluated at $M$?
Let $H = \text{freq} * g$ (XOR convolution). Then $H[M] = \sum_{u \oplus v = M} \text{freq}[u] g(v)$.
This is not the same as $\sum_u \text{freq}[u \oplus M] g(u)$.
Note that $\sum_u \text{freq}[u \oplus M] g(u) = \sum_v \text{freq}[v] g(v \oplus M)$.
Let's check if this is a convolution.
Let $A = \text{freq}$, $B = g$.
We want $S[M] = \sum_v A[v] B[v \oplus M]$.
Let $k = v \oplus M \implies v = k \oplus M$.
$S[M] = \sum_k A[k \oplus M] B[k]$.
This is the cross-correlation. For XOR, correlation is related to convolution.
Specifically, if we define $\tilde{A}[x] = A[x]$, then $S = A \star B$.
FWHT has the property: $\text{FWHT}(A \star B) = \text{FWHT}(A) \cdot \text{FWHT}(B)$?
Actually, $\text{FWHT}(A * B) = \text{FWHT}(A) \cdot \text{FWHT}(B)$ pointwise.
And $A \star B$ (correlation) is $A * \tilde{B}$ where $\tilde{B}[x] = B[-x]$? In XOR group, $-x = x$. So $\tilde{B} = B$.
So $S[M] = \sum_v A[v] B[v \oplus M]$.
Let's verify with small example.
$A=[a0, a1], B=[b0, b1]$.
$S[0] = A[0]B[0] + A[1]B[1]$.
$S[1] = A[1]B[0] + A[0]B[1]$.
Convolution $C = A * B$:
$C[0] = A[0]B[0] + A[1]B[1]$.
$C[1] = A[0]B[1] + A[1]B[0]$.
So $S = C$. The correlation under XOR is the same as convolution because the group is its own inverse and abelian.
So yes, $F = \text{freq} * g$ (XOR convolution).

Algorithm:
1. Compute `freq` array of size $2^W$, where `freq[v]` is the count of rows with value `v`.
2. Compute `g` array of size $2^W$, where `g[v] = min(popcount(v), W - popcount(v))`.
3. Compute FWHT of `freq` and `g`.
4. Pointwise multiply the transformed arrays.
5. Compute inverse FWHT to get `F`.
6. The answer is $\min_M F[M]$.

Complexity: $O(W 2^W + H)$. With $W=18$, $2^{18} = 262144$, $W 2^W \approx 4.7 \cdot 10^6$, which is very fast in Python.