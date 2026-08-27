
## ideation
**Core Difficulty:**
The problem asks for the sum of absolute differences $|A_i - B_j|$ over a sub-rectangle of indices $1 \le i \le X_k$ and $1 \le j \le Y_k$. A naive calculation for each query takes $O(X_k \cdot Y_k)$, which is too slow ($O(N^2)$ worst case). We need an approach that leverages the structure of the absolute difference function.

**Key Insight:**
The absolute difference $|a - b|$ can be rewritten based on the relative order of $a$ and $b$:
- If $a \le b$, then $|a - b| = b - a$.
- If $a > b$, then $|a - b| = a - b$.

By sorting arrays $A$ and $B$, we can efficiently determine the split point where elements of $A$ are less than or equal to elements of $B$.
Let the sorted arrays be $A'$ and $B'$. For a query $(X, Y)$:
1. Consider the subset $A_{sub} = \{A'_1, \dots, A'_X\}$ and $B_{sub} = \{B'_1, \dots, B'_Y\}$.
2. Find the index $p$ in $B_{sub}$ such that all $A'_i$ (for $i \le p$) are $\le B'_j$ (for $j \ge p+1$)? No, the split is better viewed as: for a specific $A'_i$, find how many $B'_j$ are smaller/larger.
Actually, a more robust approach for the sum over a rectangle:
Sort $A$ and $B$.
For a query $(X, Y)$, we are summing $|A_i - B_j|$ for $i \in [1, X]$ and $j \in [1, Y]$.
Since $A$ and $B$ are sorted, the condition $A_i \le B_j$ defines a region in the $(i, j)$ grid. However, since we are summing over a fixed rectangular prefix, the "split" isn't a diagonal line across the whole grid, but rather we can iterate or binary search.
Wait, simply sorting $A$ and $B$ allows us to use the property:
$\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j| = \sum_{i=1}^X \left( \sum_{j=1}^Y |A_i - B_j| \right)$.
For a fixed $A_i$, the term $\sum_{j=1}^Y |A_i - B_j|$ can be computed in $O(\log N)$ or $O(1)$ if we precompute prefix sums of $B$.
Specifically, find the largest index $k$ in $B$ (within $1 \dots Y$) such that $B_k \le A_i$.
- Elements $B_1 \dots B_k$ are $\le A_i$: contribution is $\sum (A_i - B_j) = k \cdot A_i - \text{prefix\_sum\_B}[k]$.
- Elements $B_{k+1} \dots B_Y$ are $> A_i$: contribution is $\sum (B_j - A_i) = (\text{prefix\_sum\_B}[Y] - \text{prefix\_sum\_B}[k]) - (Y - k) \cdot A_i$.
Summing this over all $i=1 \dots X$ gives the answer.
Complexity: Sorting takes $O(N \log N)$. Precomputing prefix sums takes $O(N)$. Each query takes $O(X \log N)$ if we iterate $i$, or $O(\log N)$ if we can aggregate.
Wait, iterating $i$ from $1$ to $X$ makes the query $O(X \log N)$. With $X \approx N$ and $K=10^4$, total ops $\approx 10^4 \times 10^5 \approx 10^9$, which might be TLE (Time Limit Exceeded) for Python (usually $\sim 10^8$ ops/sec).
We need to optimize the query to $O(\log N)$ or $O(1)$.

**Optimization Strategy:**
Notice that the split point $k$ (where $B_k \le A_i < B_{k+1}$) depends on $A_i$. As $i$ increases, $A_i$ increases, so the split point $k$ in $B$ also non-decreases.
However, we are summing over $i \in [1, X]$. The split point varies for each $i$.
Can we precompute answers?
The constraints are $N=10^5, K=10^4$.
If we sort $A$ and $B$, let's reconsider the formula:
Total Sum = $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
This can be decomposed into:
$\sum_{i=1}^X \sum_{j=1}^Y (B_j - A_i) \cdot \mathbb{I}(B_j \ge A_i) + \sum_{i=1}^X \sum_{j=1}^Y (A_i - B_j) \cdot \mathbb{I}(A_i > B_j)$.
Let's fix the split based on the values.
Actually, there is a known technique for this specific problem (often found in competitive programming contexts like AtCoder).
Sort $A$ and $B$.
Precompute prefix sums of $A$ and $B$.
For a query $(X, Y)$:
We need to sum $|A_i - B_j|$ for $i \le X, j \le Y$.
The critical observation is that we can't easily separate the sums without knowing the relative order.
But notice: The set of pairs is a rectangle.
Let's try to calculate:
$S = \sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
We can iterate over the "split" index in $B$ for the entire range $1..X$? No, the split depends on $A_i$.
However, since $A$ is sorted, as $i$ goes $1 \to X$, $A_i$ increases. The index $k_i$ in $B$ such that $B_k \le A_i < B_{k+1}$ is non-decreasing.
But $k_i$ is bounded by $Y$.
So for a fixed query $(X, Y)$, we can find the transition points.
Actually, maybe $O(X \log N)$ is acceptable? $10^4 \times 10^5 = 10^9$. In C++ maybe, in Python definitely risky.
Is there an $O(1)$ or $O(\log N)$ per query solution?
Yes.
Let's define a function $f(i, j) = \sum_{u=1}^i \sum_{v=1}^j |A_u - B_v|$.
We want $f(X, Y)$.
Can we express $f(X, Y)$ using prefix sums of $A$ and $B$ and some precomputed values?
Consider the contribution of each $A_i$ and $B_j$.
$\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j| = \sum_{i=1}^X \left( \sum_{j=1}^Y |A_i - B_j| \right)$.
Let $g(i, Y) = \sum_{j=1}^Y |A_i - B_j|$.
Since $B$ is sorted, for a fixed $A_i$, we find $k = \text{bisect\_right}(B, A_i) - 1$. But we are limited to $j \le Y$. So effective $k = \min(Y-1, \text{bisect\_right}(B, A_i) - 1)$.
Then $g(i, Y) = (k+1)A_i - P_B[k+1] + (P_B[Y] - P_B[k+1]) - (Y - (k+1))A_i$.
Simplifying: $g(i, Y) = (2(k+1) - Y)A_i + (P_B[Y] - 2P_B[k+1])$.
Here $k$ depends on $i$. Since $k$ is non-decreasing with $i$, we can't simply sum coefficients unless we group $i$'s by their $k$ value.
The values of $k$ change only when $A_i$ crosses a value in $B$.
There are at most $N$ such changes.
But $K$ is up to $10^4$. We cannot iterate all changes per query.
Wait, $N=10^5, K=10^4$.
Maybe $O(N \log N + K \log N)$ is possible?
How?
Notice that the "split" index $k$ for $A_i$ in $B$ is just `bisect_right(B, A_i)`.
Let $idx_i = \text{bisect\_right}(B, A_i)$. This is the count of elements in $B$ strictly less than $A_i$? No, `bisect_right` returns insertion point after all elements $\le A_i$. So elements $0 \dots idx_i-1$ are $\le A_i$.
Let $c_i = idx_i$. Then for $j < c_i$, $|A_i - B_j| = A_i - B_j$. For $j \ge c_i$, $|A_i - B_j| = B_j - A_i$.
But we only sum $j$ up to $Y$.
So for a fixed $i$, the split in the range $[1, Y]$ is at $k = \min(Y, c_i)$.
If $c_i \le Y$: split is at $c_i$. Terms $1..c_i$ are $A_i - B_j$, terms $c_i+1..Y$ are $B_j - A_i$.
If $c_i > Y$: all terms $1..Y$ are $A_i - B_j$.
If $c_i = 0$: all terms $1..Y$ are $B_j - A_i$.

We need to sum this over $i=1 \dots X$.
The term $c_i$ changes values.
However, note that $c_i$ is determined by $A_i$.
Since we have many queries, maybe we can precompute something?
Actually, the constraints $N=10^5, K=10^4$ suggest that $O(K \cdot \log N)$ or $O(K \cdot \sqrt N)$ or $O(K \cdot N)$ is wrong. $O(K \cdot N)$ is $10^9$. $O(K \log N)$ is $1.4 \times 10^5$, very fast.
Is it possible to answer in $O(\log N)$?
Let's look at the structure again.
We are summing over a rectangle $[1, X] \times [1, Y]$.
Let's define a 2D array $D[i][j] = |A_i - B_j|$. We want sum of submatrix.
But $D$ is not arbitrary; it has structure.
Actually, there is a simpler way.
Sort $A$ and $B$.
The total sum $\sum_{i=1}^N \sum_{j=1}^N |A_i - B_j|$ is easy.
But we have limits $X, Y$.
Let's consider the contribution of each $A_i$ to the sum.
Contribution of $A_i$ is $\sum_{j=1}^Y |A_i - B_j|$.
As established, this is $(2 \cdot \text{count}(B_j \le A_i) - Y) A_i + \text{const}(B, Y, \text{count})$.
Let $cnt_i = \text{count}(j \in [1, Y] : B_j \le A_i)$.
Then term is $(2 cnt_i - Y) A_i + (P_B[Y] - 2 P_B[cnt_i])$.
We need $\sum_{i=1}^X (2 cnt_i - Y) A_i + \sum_{i=1}^X (P_B[Y] - 2 P_B[cnt_i])$.
$= 2 \sum_{i=1}^X cnt_i A_i - Y \sum_{i=1}^X A_i + X P_B[Y] - 2 \sum_{i=1}^X P_B[cnt_i]$.
Here $cnt_i = \min(Y, \text{bisect\_right}(B, A_i))$.
The problem is calculating $\sum cnt_i A_i$ and $\sum P_B[cnt_i]$ efficiently.
Since $cnt_i$ is non-decreasing with $i$, we can find the ranges of $i$ where $cnt_i$ is constant.
The values of $cnt_i$ change only when $A_i$ crosses a value in $B$.
Specifically, $cnt_i = k$ when $B_k \le A_i < B_{k+1}$ (with boundary conditions).
The indices $i$ where this happens form intervals.
Since $A$ is sorted, we can binary search for the transition points of $cnt_i$ within $1 \dots X$.
The transition points are the indices $i$ where $A_i \ge B_1, A_i \ge B_2, \dots$.
Actually, $cnt_i = k$ means $A_i \ge B_k$ and $A_i < B_{k+1}$ (roughly).
So for a fixed $Y$, the sequence $cnt_1, cnt_2, \dots, cnt_X$ will look like $0, 0, \dots, 0, 1, 1, \dots, 1, 2, \dots, Y, Y, \dots$.
The boundaries are determined by comparing $A_i$ with $B_1, B_2, \dots, B_Y$.
There are at most $Y$ such boundaries. Since $Y \le N$, this could be $O(N)$ boundaries.
However, we only care about boundaries that fall within $1 \dots X$.
So we need to find how many $A_i$'s are $\ge B_1$, how many are $\ge B_2$, etc., up to $B_Y$.
This is equivalent to finding the rank of each $B_k$ in $A$.
Let $pos_k$ be the index in $A$ such that $A_{pos_k} \ge B_k$. (Using 1-based indexing, $pos_k = \text{bisect\_left}(A, B_k) + 1$? No, we want count of $A_i < B_k$).
Let $L_k = \text{bisect\_right}(A, B_k)$. This is the number of elements in $A$ strictly less than $B_k$? No, $\le B_k$.
Wait, $cnt_i = \min(Y, \text{bisect\_right}(B, A_i))$.
Let $R_i = \text{bisect\_right}(B, A_i)$. This is the number of elements in $B$ that are $\le A_i$.
$cnt_i = \min(Y, R_i)$.
We need to sum over $i=1 \dots X$.
The value of $R_i$ changes when $A_i$ passes a value in $B$.
The distinct values of $R_i$ are $0, 1, \dots, Y$.
The transition from $R_i = k$ to $R_i = k+1$ happens when $A_i$ exceeds $B_k$.
Let $idx_k$ be the smallest index $i$ such that $A_i > B_k$. Then for $i < idx_k$, $R_i \le k$.
Actually, $R_i = k \iff B_k \le A_i < B_{k+1}$.
So the range of $i$ where $R_i = k$ is $[ \text{bisect\_right}(B, \text{prev}) + 1, \text{bisect\_right}(B, \text{curr}) ]$.
More simply:
Let $p_k = \text{bisect\_right}(A, B_k)$. This is the count of elements in $A$ that are $\le B_k$.
Then for $i \in [p_{k-1}+1, p_k]$, we have $A_i > B_{k-1}$ and $A_i \le B_k$.
Thus $R_i = k$ (assuming $B$ is sorted and distinct, handling duplicates carefully).
Actually, $R_i = \text{bisect\_right}(B, A_i)$.
If $A_i \le B_k$, then $R_i \le k$.
If $A_i > B_k$, then $R_i > k$.
So $R_i = k$ corresponds to $B_{k-1} < A_i \le B_k$ (with $B_0 = -\infty, B_{Y+1} = \infty$).
The indices $i$ satisfying this are $i \in ( \text{bisect\_right}(A, B_{k-1}), \text{bisect\_right}(A, B_k) ]$.
Let $start_k = \text{bisect\_right}(A, B_{k-1}) + 1$ and $end_k = \text{bisect\_right}(A, B_k)$.
For $i \in [start_k, end_k]$, $R_i = k$.
We are interested in $i \in [1, X]$.
So for each $k \in [1, Y]$, the contribution is for $i \in [\max(1, start_k), \min(X, end_k)]$.
Let this interval be $[l_k, r_k]$. If $l_k \le r_k$, we add $(r_k - l_k + 1)$ terms where $cnt_i = k$.
For these terms, $cnt_i = k$.
Contribution to sum:
$\sum_{i=l_k}^{r_k} [ (2k - Y) A_i + (P_B[Y] - 2 P_B[k]) ]$
$= (2k - Y) \sum_{i=l_k}^{r_k} A_i + (r_k - l_k + 1) (P_B[Y] - 2 P_B[k])$.
We can compute $\sum A_i$ in $O(1)$ using prefix sums of $A$.
So the algorithm is:
1. Sort $A$ and $B$.
2. Compute prefix sums for $A$ and $B$.
3. For each query $(X, Y)$:
   - Iterate $k$ from $1$ to $Y$.
   - Determine range $[l_k, r_k]$ of $i$'s where $cnt_i = k$.
   - Add to total.
Complexity: $O(Y)$ per query. Worst case $O(N)$. Total $O(K \cdot N)$. Still too slow ($10^9$).

**Wait, is there a faster way?**
Notice that we are summing over $k=1 \dots Y$.
The ranges $[start_k, end_k]$ partition the array $A$.
We are intersecting these partitions with $[1, X]$.
This looks like we are summing over a 2D range in a transformed space?
Actually, let's reverse the thinking.
We want $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
This is equal to $\sum_{i=1}^X \sum_{j=1}^Y \max(A_i, B_j) - \min(A_i, B_j)$.
$= \sum_{i=1}^X \sum_{j=1}^Y \max(A_i, B_j) - \sum_{i=1}^X \sum_{j=1}^Y \min(A_i, B_j)$.
Let's focus on $S_{max}(X, Y) = \sum_{i=1}^X \sum_{j=1}^Y \max(A_i, B_j)$.
$\max(A_i, B_j) = A_i + B_j - \min(A_i, B_j)$.
So $S_{max} = X \cdot P_B[Y] + Y \cdot P_A[X] - S_{min}(X, Y)$.
Then Total $= S_{max} - S_{min} = X P_B[Y] + Y P_A[X] - 2 S_{min}(X, Y)$.
So we just need to compute $S_{min}(X, Y) = \sum_{i=1}^X \sum_{j=1}^Y \min(A_i, B_j)$.
$\min(A_i, B_j)$ is $B_j$ if $B_j \le A_i$, else $A_i$.
This is the same structure as before.
$S_{min}(X, Y) = \sum_{i=1}^X \left( \sum_{j=1}^Y \min(A_i, B_j) \right)$.
For a fixed $i$, let $k = \min(Y, \text{bisect\_right}(B, A_i))$.
Inner sum = $\sum_{j=1}^k B_j + \sum_{j=k+1}^Y A_i = P_B[k] + (Y-k)A_i$.
So $S_{min}(X, Y) = \sum_{i=1}^X (P_B[\min(Y, R_i)] + (Y - \min(Y, R_i)) A_i)$.
Where $R_i = \text{bisect\_right}(B, A_i)$.
Again, $R_i$ is non-decreasing.
The values of $R_i$ change at most $Y$ times (or $N$ times).
But we can optimize the summation.
We need $\sum_{i=1}^X P_B[\min(Y, R_i)] + Y \sum_{i=1}^X A_i - \sum_{i=1}^X \min(Y, R_i) A_i$.
The term $\sum \min(Y, R_i) A_i$ is the hard part.
However, note that $R_i$ takes values in $0 \dots N$.
But we only care about $R_i$ up to $Y$.
If $R_i \ge Y$, then $\min(Y, R_i) = Y$.
If $R_i < Y$, then $\min(Y, R_i) = R_i$.
So split the sum into $i$ where $R_i \ge Y$ and $i$ where $R_i < Y$.
Condition $R_i \ge Y \iff \text{bisect\_right}(B, A_i) \ge Y \iff A_i \ge B_Y$.
Let $idx = \text{bisect\_left}(A, B_Y)$. (First index where $A_i \ge B_Y$).
For $i \ge idx$, $R_i \ge Y$, so $\min(Y, R_i) = Y$.
For $i < idx$, $R_i < Y$ (assuming $B_Y$ is the $Y$-th element, actually $B_Y$ is the element at index $Y$ in 1-based, so $B[Y-1]$ in 0-based. `bisect_right` returns count. If $A_i \ge B_Y$, then count $\ge Y$).
So for $i \in [idx, X]$, term is $Y \cdot A_i$.
For $i \in [1, \min(X, idx-1)]$, term is $R_i \cdot A_i$.
Now we need to sum $R_i \cdot A_i$ for $i < idx$.
$R_i$ is the number of elements in $B$ less than or equal to $A_i$.
$R_i = \text{bisect\_right}(B, A_i)$.
Since $i < idx$, $A_i < B_Y$. Thus $R_i \le Y$.
Also $R_i$ is non-decreasing.
The values of $R_i$ are constant between the elements of $B$.
Specifically, $R_i = k$ for $A_i \in (B_{k-1}, B_k]$.
The range of $i$ for a given $k$ is $[ \text{bisect\_right}(A, B_{k-1}), \text{bisect\_right}(A, B_k) ]$.
Let $L_k = \text{bisect\_right}(A, B_{k-1})$ and $R_k = \text{bisect\_right}(A, B_k)$.
We need to sum $k \cdot A_i$ for $i \in [1, \min(X, idx-1)]$ intersected with $[L_k, R_k]$.
This is summing $k \cdot A_i$ over intervals.
The intervals $[L_k, R_k]$ for $k=1 \dots Y$ partition the range $[1, \text{count}(A < B_Y)]$.
We can iterate $k$ from $1$ to $Y$.
But $Y$ can be $10^5$. $K=10^4$. $O(K \cdot Y)$ is too slow.
We need to avoid iterating $k$.
Notice that we are summing $k \cdot A_i$ where $k = R_i$.
This is $\sum_{i=1}^M R_i A_i$ where $M = \min(X, idx-1)$.
$R_i$ is a step function.
Can we precompute this?
We have $K$ queries. $X, Y$ vary.
This looks like a 2D range sum problem or something solvable with persistent segment trees or offline processing.
Given the constraints and problem type (AtCoder style), maybe offline processing with a sweep-line or Fenwick tree is intended.
Sort queries by $Y$? Or $X$?
Actually, the constraints $N, K$ are somewhat balanced. $N=10^5, K=10^4$.
Maybe $O((N+K) \log N)$ is required.
Let's reconsider the offline approach.
We want to compute $S = \sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
This is equivalent to summing over all pairs $(i, j)$ with $i \le X, j \le Y$.
Let's place points $(i, j)$ in a grid. We want sum of $|A_i - B_j|$ in rectangle $[1, X] \times [1, Y]$.
The value $|A_i - B_j|$ depends on $i, j$.
But $A$ and $B$ are sorted.
The condition $A_i \le B_j$ defines a region below a curve in the grid.
The curve is $j \approx \text{bisect}(B, A_i)$.
Since $A$ and $B$ are sorted, the boundary is monotonic.
We can use the fact that the boundary is a step function.
The "steps" are at indices where $A_i$ crosses $B_j$.
There are $N$ such steps.
We can process queries offline.
Sort queries by $Y$?
If we fix $Y$, we want $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$.
As $Y$ increases, we add a new row $B_Y$ to the sum.
New contribution: $\sum_{i=1}^X |A_i - B_Y|$.
This can be computed in $O(\log N)$ using binary search on $A$.
So if we process queries sorted by $Y$, we can maintain the current sum for all $i$.
But we need the sum for specific $X$.
We can maintain an array $S_i = \sum_{j=1}^{current\_Y} |A_i - B_j|$.
When $Y$ increments to $Y+1$, update $S_i \leftarrow S_i + |A_i - B_{Y+1}|$ for all $i$.
Then answer query $(X, Y)$ as $\sum_{i=1}^X S_i$.
This is a range add, range sum problem.
Update: Add $|A_i - B_{new}|$ to $S_i$ for all $i=1 \dots N$.
Query: Sum $S_i$ for $i=1 \dots X$.
The update is "add value $v_i$ to range $[1, N]$".
$v_i = |A_i - B_{new}|$.
Since $A$ is sorted, $|A_i - B_{new}|$ is:
- $B_{new} - A_i$ for $A_i \le B_{new}$
- $A_i - B_{new}$ for $A_i > B_{new}$
So the update is:
- Add $(B_{new} - A_i)$ to $S_i$ for $i \in [1, p]$ where $A_p \le B_{new}$.
  This is: Add $p \cdot B_{new} - \sum_{i=1}^p A_i$.
  This is a range add of constant? No, range add of linear function.
  $S_i \leftarrow S_i + B_{new} - A_i$.
  We can maintain two Fenwick trees (or segment trees):
  1. One for the constant part added to $S_i$.
  2. One for the $-A_i$ part (which is just adding $-1$ to coefficient of $A_i$, but $A_i$ is fixed).
  Actually, simpler:
  $S_i$ is a value. We add $C$ to $S_i$ for $i \in [1, p]$ and add $-A_i$ to $S_i$ for $i \in [1, p]$.
  Wait, $S_i \leftarrow S_i + (B_{new} - A_i)$.
  This is: Add $B_{new}$ to $S_i$ for $i \in [1, p]$.
  And add $-A_i$ to $S_i$ for $i \in [1, p]$.
  The second part is not a constant add. It depends on $i$.
  However, we can maintain $S_i$ as a sum of terms.
  $S_i = \sum_{j=1}^Y |A_i - B_j|$.
  We need $\sum_{i=1}^X S_i$.
  Let's decompose $|A_i - B_j| = \max(A_i, B_j) - \min(A_i, B_j)$.
  Total Sum = $\sum_{i=1}^X \sum_{j=1}^Y \max(A_i, B_j) - \sum_{i=1}^X \sum_{j=1}^Y \min(A_i, B_j)$.
  Let's handle $\sum \max$.
  $\sum_{i=1}^X \sum_{j=1}^Y \max(A_i, B_j) = \sum_{i=1}^X \left( \sum_{j=1}^Y \max(A_i, B_j) \right)$.
  For fixed $i$, $\sum \max = \sum_{j: B_j \le A_i} A_i + \sum_{j: B_j > A_i} B_j$.
  This is $A_i \cdot (\text{count}) + (P_B[Y] - P_B[\text{count}])$.
  This leads back to the same formula.

  **Offline Approach with Fenwick Tree:**
  We can compute the answer for all queries offline.
  Sort queries by $Y$.
  Iterate $Y$ from $1$ to $N$.
  Maintain a data structure that supports:
  - Add a new $B_j$ (update the function $f(i) = |A_i - B_j|$).
  - Query $\sum_{i=1}^X f(i)$.
  
  When adding $B_j$:
  Find $p$ such that $A_p \le B_j < A_{p+1}$.
  For $i \le p$: $|A_i - B_j| = B_j - A_i$.
  For $i > p$: $|A_i - B_j| = A_i - B_j$.
  We need to add this to our accumulator for each $i$.
  Let $D_i$ be the current sum $\sum_{k=1}^{current\_Y} |A_i - B_k|$.
  Update:
  For $i \in [1, p]$: $D_i \leftarrow D_i + B_j - A_i$.
  For $i \in [p+1, N]$: $D_i \leftarrow D_i + A_i - B_j$.
  
  We need to support:
  1. Range add: Add constant $C$ to $D_i$ for $i \in [L, R]$.
  2. Range add: Add $-A_i$ to $D_i$ for $i \in [L, R]$. (This is tricky, $A_i$ varies).
  3. Range add: Add $A_i$ to $D_i$ for $i \in [L, R]$.
  4. Range add: Add constant $C$ to $D_i$ for $i \in [L, R]$.
  
  Actually, we can maintain $D_i$ as a sum of two components:
  $D_i = \text{Base}_i + \text{Coeff}_i \cdot A_i$.
  Initially 0.
  Update for $B_j$:
  - For $i \in [1, p]$: Add $B_j - A_i = B_j + (-1) \cdot A_i$.
    So $\text{Base}_i \leftarrow \text{Base}_i + B_j$, $\text{Coeff}_i \leftarrow \text{Coeff}_i - 1$.
  - For $i \in [p+1, N]$: Add $A_i - B_j = (-B_j) + (1) \cdot A_i$.
    So $\text{Base}_i \leftarrow \text{Base}_i - B_j$, $\text{Coeff}_i \leftarrow \text{Coeff}_i + 1$.
  
  We need a data structure that supports:
  - Range add to $\text{Base}$.
  - Range add to $\text{Coeff}$.
  - Range sum of $(\text{Base}_i + \text{Coeff}_i \cdot A_i)$.
  
  This can be done with two Fenwick Trees (or Segment Trees):
  - BIT1 for $\text{Base}$. Supports range add, point query? No, we need range sum.
    Standard BIT supports point update, prefix sum.
    We need range add, prefix sum.
    Range add $[L, R]$ with $v$, prefix sum $[1, X]$.
    This is standard: Use a BIT to store differences.
    Update: `add(L, v)`, `add(R+1, -v)`.
    Query: `query(X)`.
    This gives $\sum_{i=1}^X \text{Base}_i$.
  - BIT2 for $\text{Coeff}$. Same logic. Gives $\sum_{i=1}^X \text{Coeff}_i$.
  
  Then the answer for query $X$ is:
  $\sum_{i=1}^X \text{Base}_i + A_i \cdot \text{Coeff}_i$? No.
  We need $\sum_{i=1}^X (\text{Base}_i + \text{Coeff}_i \cdot A_i) = \sum \text{Base}_i + \sum (\text{Coeff}_i \cdot A_i)$.
  The second term $\sum \text{Coeff}_i \cdot A_i$ is not separable if $\text{Coeff}_i$ is just a scalar.
  Wait, $\text{Coeff}_i$ is constant in the range updates?
  Yes, in the range $[1, p]$, we add $-1$ to all $\text{Coeff}_i$.
  So $\text{Coeff}_i$ is a step function.
  But $A_i$ is not constant.
  So we cannot simply sum $\text{Coeff}_i$ and multiply by something.
  We need a data structure that supports:
  - Range add to coefficients $c_i$.
  - Query $\sum_{i=1}^X c_i \cdot A_i$.
  
  This is a "Range Add, Range Weighted Sum" problem.
  Since $A_i$ is fixed (sorted), we can use a Segment Tree where each node stores:
  - Sum of $A_i$ in range.
  - Sum of $1$ (count) in range.
  - Lazy tag for adding to $c_i$.
  When updating range $[L, R]$ with $+v$:
  - `lazy += v`
  - `sum_weighted += v * sum_A_in_range`
  - `sum_count += v * count_in_range` (if we also track sum of $c_i$).
  
  Yes! A Segment Tree with lazy propagation can solve this.
  Operations:
  1. Range add $v$ to $c_i$ for $i \in [L, R]$.
     Update: `tree[node].lazy += v`, `tree[node].sum_A_weighted += v * tree[node].sum_A`, `tree[node].sum_c += v * tree[node].count`.
  2. Query prefix sum of $(c_i + b_i)$ where $b_i$ is the base part.
     We can maintain two Segment Trees:
     - ST1: Tracks $c_i$ (coefficients). Supports range add, query $\sum c_i A_i$.
     - ST2: Tracks $b_i$ (base constants). Supports range add, query $\sum b_i$.
  
  Complexity: $O(N \log N)$ build, $O(N \log N)$ updates (one per $B_j$), $O(K \log N)$ queries.
  Total time: $O((N+K) \log N)$. This fits well within limits.
  
  **Algorithm Plan:**
  1. Read input, sort $A$ and $B$.
  2. Store queries with original indices. Sort queries by $Y$.
  3. Initialize Segment Trees:
     - `ST_base`: Range add, Range sum. (Standard lazy segment tree).
     - `ST_coeff`: Range add, Range weighted sum (by $A_i$).
       Node stores: `sum_A` (sum of $A_i$ in range), `sum_val` (sum of $c_i A_i$), `lazy`.
       Update $[L, R]$ with $v$:
         `lazy += v`
         `sum_val += v * sum_A`
  4. Iterate $j$ from $1$ to $N$ (processing $B_j$):
     - Find split point $p$ in $A$ such that $A_p \le B_j < A_{p+1}$. (Using `bisect`).
       Note: $p$ is the count of elements $\le B_j$. So indices $1 \dots p$ get $B_j - A_i$.
       Indices $p+1 \dots N$ get $A_i - B_j$.
     - Update `ST_base`:
       - Range $[1, p]$: add $B_j$.
       - Range $[p+1, N]$: add $-B_j$.
     - Update `ST_coeff`:
       - Range $[1, p]$: add $-1$ (since term is $-A_i$).
       - Range $[p+1, N]$: add $1$ (since term is $+A_i$).
     - Answer all queries with $Y == j$.
       For query $(X, Y)$:
         $Ans = \text{query\_base}(X) + \text{query\_coeff\_weighted}(X)$.
         Store result.
  5. Print results in original order.

  **Corner Cases:**
  - $p=0$ (all $A_i > B_j$): Only update $[1, N]$ with $-B_j$ and $+1$.
  - $p=N$ (all $A_i \le B_j$): Only update $[1, N]$ with $B_j$ and $-1$.
  - $X=0$? Constraints say $X \ge 1$.
  - $A_i, B_j$ up to $2 \cdot 10^8$, sums can exceed $2^{31}-1$, use 64-bit integers.

  **Implementation Details:**
  - Segment Tree size $4N$.
  - `ST_base` is simpler.
  - `ST_coeff` needs `sum_A` precomputed for each node (static, can be built once).
  - Python recursion limit might be an issue for deep trees ($N=10^5$), use iterative or increase limit. Iterative is safer/faster.

## worker: finalize
1.  **Algorithm Selection**: The problem requires calculating $\sum_{i=1}^X \sum_{j=1}^Y |A_i - B_j|$. A naive $O(N^2)$ or even $O(N)$ per query is too slow given $N=10^5$ and $K=10^4$.
2.  **Offline Processing**: By sorting queries by $Y$, we can incrementally add elements of $B$ to our data structure. When moving from $Y$ to $Y+1$, we add the term $|A_i - B_{Y+1}|$ for all $i$.
3.  **Decomposition**: $|A_i - B_j| = \max(A_i, B_j) - \min(A_i, B_j)$. Alternatively, we can directly model the update:
    - If $A_i \le B_j$, contribution is $B_j - A_i$.
    - If $A_i > B_j$, contribution is $A_i - B_j$.
    This can be rewritten as:
    - Base part: Add $B_j$ (if $A_i \le B_j$) or $-B_j$ (if $A_i > B_j$).
    - Coeff part: Add $-1 \cdot A_i$ (if $A_i \le B_j$) or $+1 \cdot A_i$ (if $A_i > B_j$).
4.  **Data Structures**:
    - **Base Part**: Requires Range Add, Range Sum. Implemented using a Binary Indexed Tree (BIT) supporting range updates and prefix sums.
    - **Coeff Part**: Requires Range Add to coefficients, and Range Weighted Sum (sum of $c_i \cdot A_i$). Implemented using a Segment Tree with Lazy Propagation. Since $A$ is static and sorted, we precompute sum of $A$ in ranges to update the weighted sum efficiently during lazy propagation.
5.  **Complexity**:
    - Sorting $A, B$: $O(N \log N)$.
    - Sorting Queries: $O(K \log K)$.
    - Processing: $N$ updates to data structures ($O(N \log N)$) and $K$ queries ($O(K \log N)$).
    - Total Time: $O((N+K) \log N)$, which fits within the time limit.
6.  **Edge Cases**: Handled via `bisect_right` for split points and careful range management in BIT/SegTree (0-based vs 1-based).
