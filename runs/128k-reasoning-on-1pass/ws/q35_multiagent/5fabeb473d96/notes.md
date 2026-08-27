
## ideation


## worker: Read input values $N, Q$ and the sequence $A$.
The problem asks for the sum of distances between $u$ and $v$ over all valid trees $T(P)$. The total number of trees is $(N-1)!$.
By linearity of expectation (or summing over edges), the total distance is $\sum_{x=2}^N A_x \cdot C_x(u, v)$, where $C_x(u, v)$ is the number of trees where edge $E_x$ (connecting $x$ to $P_x$) is on the path between $u$ and $v$.
Let $p_x = C_x(u, v) / (N-1)!$ be the probability that $E_x$ is on the path.
For $u < v$, the probabilities $p_x$ are derived as:
1. $x < u$: $p_x = \frac{2}{x(x+1)}$.
2. $x = u$: $p_x = \frac{u-1}{u}$.
3. $u < x < v$: $p_x = \frac{1}{x}$.
4. $x = v$: $p_x = 1$.
5. $x > v$: $p_x = 0$.

We compute the sum $\sum A_x p_x$ efficiently using prefix sums.
$S_1[i] = \sum_{x=2}^i A_x/x$.
$S_2[i] = \sum_{x=2}^i A_x \frac{2}{x(x+1)}$.
The answer for a query $(u, v)$ is $(N-1)! \times (\text{sum of relevant terms})$.
All calculations are done modulo 998244353.
Complexity is $O(N + Q)$ due to precomputation and $O(1)$ per query.
