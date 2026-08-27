
## ideation
The problem asks us to maximize the total number of units bought given a budget $M$ and cost functions $k^2 P_i$ for $k$ units of product $i$. The cost function is convex, which implies that to minimize the cost for a fixed total number of units, we should distribute the units such that the marginal costs are balanced. The marginal cost of buying the $k$-th unit of product $i$ is $(2k-1)P_i$.

We can binary search for the maximum possible marginal cost threshold $T$. If we set a threshold $T$, we buy the $k$-th unit of product $i$ if its marginal cost $(2k-1)P_i \le T$. This gives us a specific number of units $x_i$ for each product, where $x_i = \lfloor \frac{T + P_i}{2 P_i} \rfloor$. The total cost for this distribution is $\sum x_i^2 P_i$. Since the cost is monotonically increasing with $T$, we can binary search for the largest $T$ such that the total cost is at most $M$. The answer will be the total number of units $\sum x_i$ for this optimal $T$.

Key optimizations for Python:
1. Sort $P$ to allow skipping products where $P_i > T$ (since $x_i=0$ in that case).
2. Precompute denominators $2P_i$ to avoid repeated multiplication.
3. Use `bisect` to quickly find the range of relevant products.
4. The upper bound for $T$ can be estimated. With $M=10^{18}$ and max $P_i=2 \cdot 10^9$, the maximum marginal cost is around $10^{14}$, so a bound of $2 \cdot 10^{14}$ is safe.
