The problem asks for the sum of the K-th power of all contiguous subarray sums. Since $K$ is small ($K \le 10$) and $N$ is up to $2 \times 10^5$, an $O(N \cdot K)$ or $O(N \log N)$ solution is required. We can expand the term $(\sum A_i)^K$ using the Multinomial Theorem, which expresses the sum as a linear combination of products of powers of individual elements. Specifically, $\sum_{l \le r} (\sum_{i=l}^r A_i)^K = \sum_{l \le r} \sum_{c_1 + \dots + c_N = K, \text{support} \subseteq [l,r]} \frac{K!}{c_1! \dots c_N!} \prod A_i^{c_i}$. However, a more direct combinatorial approach involves iterating over the number of times each element $A_i$ appears in the subarray sum. For a fixed element $A_i$, if it appears $c_i$ times in a subarray $[l, r]$, it contributes to the term $A_i^{c_i}$. The total sum can be rewritten by considering the contribution of each element's power to the total sum. A standard technique for this specific constraint ($K$ small) is to use the identity $(\sum x_i)^K = \sum_{j=0}^K \binom{K}{j} (\sum x_i)^j (\sum x_i)^{K-j}$? No, that's not helpful.
Actually, the most efficient approach for small $K$ is to expand $(\sum_{i=l}^r A_i)^K$ using the multinomial expansion: $\sum_{c_1+\dots+c_N=K} \frac{K!}{c_1!\dots c_N!} \prod A_i^{c_i}$. The condition $l \le i \le r$ means that for a specific configuration of counts $c_i$, the subarray $[l, r]$ must cover all indices $i$ where $c_i > 0$. Let $L = \min \{i \mid c_i > 0\}$ and $R = \max \{i \mid c_i > 0\}$. The number of subarrays $[l, r]$ containing exactly the set of indices with $c_i > 0$ and no others is $(L-1) \times (N-R+1)$? No, that's for fixed sets.
Let's refine: We iterate over all possible "active" segments of indices. But that's too slow.
Alternative approach: Use the linearity of expectation or simply expand the power.
$(\sum_{i=l}^r A_i)^K = \sum_{i_1, \dots, i_K \in [l, r]} A_{i_1} \dots A_{i_K}$.
We need to sum this over all $1 \le l \le r \le N$.
Total Sum = $\sum_{l \le r} \sum_{i_1, \dots, i_K \in [l, r]} \prod_{j=1}^K A_{i_j}$.
Swap sums: $\sum_{i_1, \dots, i_K} (\prod_{j=1}^K A_{i_j}) \times (\text{number of pairs } (l, r) \text{ such that } [l, r] \text{ contains all } i_1, \dots, i_K)$.
For a fixed tuple $(i_1, \dots, i_K)$, let $min\_idx = \min(i_1, \dots, i_K)$ and $max\_idx = \max(i_1, \dots, i_K)$. The condition $[l, r] \supseteq \{i_1, \dots, i_K\}$ is equivalent to $l \le min\_idx$ and $r \ge max\_idx$.
The number of such pairs $(l, r)$ is $min\_idx \times (N - max\_idx + 1)$.
So the answer is $\sum_{i_1, \dots, i_K} (\prod A_{i_j}) \cdot min\_idx \cdot (N - max\_idx + 1)$.
Since $K$ is small, we can group terms by the values of $min\_idx$ and $max\_idx$.
Let $L = min\_idx$ and $R = max\_idx$. We need to sum $\prod A_{i_j}$ over all tuples where $\min(i) = L$ and $\max(i) = R$.
This can be computed by iterating over all pairs $(L, R)$ with $1 \le L \le R \le N$.
For a fixed pair $(L, R)$, we need the sum of products of $K$ elements chosen from indices $L \dots R$, such that at least one element is at $L$ and at least one is at $R$.
Let $S(L, R)$ be the sum of products of $K$ elements from the range $[L, R]$.
The sum we want for fixed $L, R$ is $S(L, R) - (\text{sums where } L \text{ is not used}) - (\text{sums where } R \text{ is not used}) + (\text{sums where neither } L \text{ nor } R \text{ is used})$.
Actually, it's easier:
Sum over $[L, R]$ with $\min=L, \max=R$ = (Sum over $[L, R]$) - (Sum over $[L+1, R]$) - (Sum over $[L, R-1]$) + (Sum over $[L+1, R-1]$).
Let $DP[len][k]$ be the sum of products of $k$ elements from a prefix of length $len$. This looks like we can compute prefix sums of these DP values.
Let $P[i][k]$ be the sum of $\prod_{j=1}^m A_{idx_j}$ for all sequences of length $m$ (where $m \le k$? No, exactly $k$) chosen from the first $i$ elements.
Actually, the standard DP for "sum of products of $k$ elements from a set" is:
Let $dp[i][j]$ = sum of products of $j$ elements chosen from $A_1 \dots A_i$.
$dp[i][j] = dp[i-1][j] + A_i \times dp[i-1][j-1]$.
Base case: $dp[i][0] = 1$ (empty product).
Then for a range $[L, R]$, we can't easily get the sum of products of $k$ elements from $A_L \dots A_R$ using just prefix DPs because the DP state depends on the specific values, not just the count.
Wait, the operation is linear. The sum of products of $k$ elements from a set $\{x_1, \dots, x_m\}$ is the coefficient of $z^k$ in $\prod_{i=1}^m (1 + x_i z)$.
So, let $Poly_i(z) = \prod_{j=1}^i (1 + A_j z)$. Then the sum of products of $k$ elements from $A_1 \dots A_i$ is the coefficient of $z^k$ in $Poly_i(z)$.
Let $C[i][k]$ be the coefficient of $z^k$ in $\prod_{j=1}^i (1 + A_j z)$.
Then $C[i][k] = C[i-1][k] + A_i \cdot C[i-1][k-1]$.
This can be precomputed for all $i, k$ in $O(NK)$.
Now, how to get the sum for range $[L, R]$?
The generating function for range $[L, R]$ is $Q_{L,R}(z) = \frac{\prod_{j=1}^R (1 + A_j z)}{\prod_{j=1}^{L-1} (1 + A_j z)} = \frac{Poly_R(z)}{Poly_{L-1}(z)}$.
We need the coefficient of $z^K$ in $Q_{L,R}(z)$.
Since $K$ is small, we can perform polynomial division or simply compute the coefficients iteratively.
However, doing this for every pair $(L, R)$ is $O(N^2 K)$, which is too slow ($4 \times 10^{10}$).
We need a faster way.
Let's reconsider the formula: $\sum_{L \le R} min\_idx \cdot (N - max\_idx + 1) \times [z^K] \frac{Poly_R(z)}{Poly_{L-1}(z)}$.
This looks complicated to optimize directly.
Is there a simpler expansion?
$(\sum_{i=l}^r A_i)^K = \sum_{j=0}^K \binom{K}{j} (\sum_{i=l}^r A_i)^j (\sum_{i=l}^r A_i)^{K-j}$? No.
Let's go back to: $\sum_{l \le r} (\sum_{i=l}^r A_i)^K = \sum_{l \le r} \sum_{i_1, \dots, i_K \in [l, r]} \prod A_{i_j}$.
We grouped by $L = \min(i)$ and $R = \max(i)$.
Count = $L \times (N - R + 1)$.
Term = $\sum_{i_1, \dots, i_K \in [L, R], \min=L, \max=R} \prod A_{i_j}$.
Let $S(L, R, K)$ be the sum of products of $K$ elements from $A_L \dots A_R$.
We know $S(L, R, K) = [z^K] \frac{Poly_R(z)}{Poly_{L-1}(z)}$.
We need $\sum_{L \le R} L(N-R+1) \times ([z^K] \frac{Poly_R(z)}{Poly_{L-1}(z)})$.
This still requires iterating $L, R$.
Wait, maybe we can iterate over $L$ and $R$ differently?
Actually, notice that $K$ is very small.
Can we rewrite the sum?
$\sum_{L \le R} L(N-R+1) \sum_{i_1, \dots, i_K \in [L, R], \min=L, \max=R} \prod A_{i_j}$.
This is equivalent to:
$\sum_{i_1, \dots, i_K} (\prod A_{i_j}) \times (\min(i) \times (N - \max(i) + 1))$.
Let's fix the set of indices $\{i_1, \dots, i_K\}$. Let $u = \min(i)$ and $v = \max(i)$.
Contribution is $(\prod A_{i_j}) \cdot u \cdot (N - v + 1)$.
We can iterate over all possible values of $u$ and $v$ ($1 \le u \le v \le N$).
For fixed $u, v$, we need the sum of products of $K$ elements from the range $[u, v]$ such that at least one element is $u$ and at least one is $v$.
Let $T(u, v)$ be the sum of products of $K$ elements from $A_u \dots A_v$.
Let $T(u, v, \text{no } u)$ be the sum of products of $K$ elements from $A_{u+1} \dots A_v$.
Let $T(u, v, \text{no } v)$ be the sum of products of $K$ elements from $A_u \dots A_{v-1}$.
Let $T(u, v, \text{no } u, \text{no } v)$ be the sum of products of $K$ elements from $A_{u+1} \dots A_{v-1}$.
Then the required sum for fixed $u, v$ is $T(u, v) - T(u, v, \text{no } u) - T(u, v, \text{no } v) + T(u, v, \text{no } u, \text{no } v)$.
Note that $T(u, v, \text{no } u) = T(u+1, v)$, $T(u, v, \text{no } v) = T(u, v-1)$, and $T(u, v, \text{no } u, \text{no } v) = T(u+1, v-1)$.
So we need $\sum_{u \le v} u(N-v+1) \times (T(u, v) - T(u+1, v) - T(u, v-1) + T(u+1, v-1))$.
This simplifies to a sum over $u, v$ of $T(u, v)$ weighted by some coefficient.
Coefficient for $T(u, v)$:
From $u(N-v+1) \times T(u, v)$: $u(N-v+1)$.
From $-T(u+1, v)$: When the term is $T(u+1, v)$, it appears in the sum when the outer loop is $u' = u$ (giving $-u(N-v+1)$) and when $u' = u+1$ (giving $+(u+1)(N-v+1)$).
Wait, let's expand the double sum properly.
Sum = $\sum_{u=1}^N \sum_{v=u}^N u(N-v+1) [ T(u,v) - T(u+1,v) - T(u,v-1) + T(u+1,v-1) ]$.
Let's collect coefficients for each $T(x, y)$.
$T(x, y)$ appears when:
1. $u=x, v=y$: term is $+x(N-y+1)$.
2. $u=x-1, v=y$: term is $-(x-1)(N-y+1)$.
3. $u=x, v=y+1$: term is $-x(N-(y+1)+1) = -x(N-y)$.
4. $u=x-1, v=y+1$: term is $+(x-1)(N-(y+1)+1) = +(x-1)(N-y)$.
So Coeff$(x, y) = x(N-y+1) - (x-1)(N-y+1) - x(N-y) + (x-1)(N-y)$.
Simplify:
$= (N-y+1)(x - (x-1)) + (N-y)(-(x) + (x-1))$
$= (N-y+1)(1) + (N-y)(-1)$
$= N - y + 1 - N + y = 1$.
Wow! The coefficient is always 1.
So the total answer is simply $\sum_{1 \le u \le v \le N} T(u, v)$.
Where $T(u, v)$ is the sum of products of $K$ elements from the subarray $A_u \dots A_v$.
This is a massive simplification.
We just need to compute $\sum_{1 \le u \le v \le N} [z^K] \frac{Poly_v(z)}{Poly_{u-1}(z)}$.
Let $G_v(z) = Poly_v(z) = \prod_{i=1}^v (1 + A_i z)$.
We need $\sum_{1 \le u \le v \le N} [z^K] (G_v(z) / G_{u-1}(z))$.
Let $H_v(z) = \sum_{u=1}^v G_v(z) / G_{u-1}(z)$.
Then the answer is $\sum_{v=1}^N [z^K] H_v(z)$.
How to compute $H_v(z)$ efficiently?
$H_v(z) = \frac{G_v(z)}{G_0(z)} + \frac{G_v(z)}{G_1(z)} + \dots + \frac{G_v(z)}{G_{v-1}(z)}$.
Note that $G_v(z) = G_{v-1}(z) \cdot (1 + A_v z)$.
So $\frac{G_v(z)}{G_{u-1}(z)} = \frac{G_{v-1}(z) (1 + A_v z)}{G_{u-1}(z)} = (1 + A_v z) \frac{G_{v-1}(z)}{G_{u-1}(z)}$.
Thus, $H_v(z) = (1 + A_v z) \sum_{u=1}^{v-1} \frac{G_{v-1}(z)}{G_{u-1}(z)} + \frac{G_v(z)}{G_0(z)}$.
Wait, the sum index for $H_{v-1}$ is $u=1 \dots v-1$.
$H_{v-1}(z) = \sum_{u=1}^{v-1} \frac{G_{v-1}(z)}{G_{u-1}(z)}$.
So $H_v(z) = (1 + A_v z) H_{v-1}(z) + (1 + A_v z) \frac{G_{v-1}(z)}{G_0(z)}$?
No, the last term in $H_v$ corresponds to $u=v$, which is $\frac{G_v(z)}{G_{v-1}(z)} = 1 + A_v z$.
The terms for $u < v$ are $(1 + A_v z) \frac{G_{v-1}(z)}{G_{u-1}(z)}$.
So $H_v(z) = (1 + A_v z) \left( H_{v-1}(z) + \frac{G_{v-1}(z)}{G_{v-1}(z)} \right)$? No.
$H_{v-1}(z) = \sum_{u=1}^{v-1} \frac{G_{v-1}(z)}{G_{u-1}(z)}$.
The sum part of $H_v$ for $u=1 \dots v-1$ is $(1+A_v z) \sum_{u=1}^{v-1} \frac{G_{v-1}(z)}{G_{u-1}(z)} = (1+A_v z) H_{v-1}(z)$.
The term for $u=v$ is $\frac{G_v(z)}{G_{v-1}(z)} = 1 + A_v z$.
So $H_v(z) = (1 + A_v z) (H_{v-1}(z) + 1)$.
Base case: $H_0(z) = 0$ (empty sum).
$H_1(z) = (1 + A_1 z)(0 + 1) = 1 + A_1 z$.
$H_2(z) = (1 + A_2 z)(H_1(z) + 1) = (1 + A_2 z)(2 + A_1 z)$.
This recurrence is $O(K)$ per step if we maintain the polynomial coefficients up to degree $K$.
Total complexity $O(NK)$.
Algorithm:
1. Initialize an array `dp` of size $K+1$ representing $H_{current}(z)$. Initially all 0.
2. Loop $i$ from 1 to $N$:
   a. Create `new_dp` initialized to 0.
   b. We need to compute $(1 + A_i z) \times (H_{i-1}(z) + 1)$.
      Let $P(z) = H_{i-1}(z) + 1$. So $P[0] = 1 + H_{i-1}[0]$, $P[k] = H_{i-1}[k]$ for $k \ge 1$.
      Then `new_dp` is the product of $(1 + A_i z)$ and $P(z)$, truncated to degree $K$.
      `new_dp[0] = P[0]`
      `new_dp[k] = P[k] + A_i * P[k-1]` for $k \ge 1$.
   c. Update `dp = new_dp`.
   d. Add `dp[K]` to the total answer.
3. Print total answer modulo 998244353.

Let's double check the logic.
We derived Answer = $\sum_{1 \le u \le v \le N} T(u, v)$.
$T(u, v) = [z^K] \frac{Poly_v(z)}{Poly_{u-1}(z)}$.
$H_v(z) = \sum_{u=1}^v \frac{Poly_v(z)}{Poly_{u-1}(z)}$.
Recurrence: $H_v(z) = (1 + A_v z) H_{v-1}(z) + (1 + A_v z)$.
Wait, $H_{v-1}(z) = \sum_{u=1}^{v-1} \frac{Poly_{v-1}(z)}{Poly_{u-1}(z)}$.
$\frac{Poly_v(z)}{Poly_{u-1}(z)} = \frac{Poly_{v-1}(z)(1+A_v z)}{Poly_{u-1}(z)} = (1+A_v z) \frac{Poly_{v-1}(z)}{Poly_{u-1}(z)}$.
Summing over $u=1 \dots v-1$: $(1+A_v z) H_{v-1}(z)$.
Plus the term $u=v$: $\frac{Poly_v(z)}{Poly_{v-1}(z)} = 1 + A_v z$.
So $H_v(z) = (1+A_v z) (H_{v-1}(z) + 1)$.
Yes, the recurrence is correct.
The base case $H_0(z) = 0$.
$i=1$: $H_1 = (1+A_1 z)(1) = 1+A_1 z$.
$i=2$: $H_2 = (1+A_2 z)(1+A_1 z + 1) = (1+A_2 z)(2+A_1 z)$.
Correct.

Implementation details:
- Modulo arithmetic for all additions and multiplications.
- Array size $K+1$.
- Input reading.
- Output.