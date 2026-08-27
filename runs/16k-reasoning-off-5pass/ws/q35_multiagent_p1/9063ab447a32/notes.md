
## ideation
The problem asks for the maximum total units $T$ such that the minimum cost to buy $T$ units is at most $M$.
The cost function for product $i$ with $k_i$ units is $k_i^2 P_i$. The marginal cost of the $k$-th unit of product $i$ is $(2k-1)P_i$.
To minimize the total cost for a fixed total number of units $T$, we should greedily pick units with the smallest marginal costs. This is a classic "water-filling" or threshold problem.
We can binary search on the answer $T$ (the total number of units). The range for $T$ is $[0, M]$ because the minimum cost for 1 unit is $1^2 \cdot \min(P_i) \ge 1$, so we can buy at most $M$ units. A tighter upper bound is $M$ (since each unit costs at least 1).
For a fixed $T$, we need to check if the minimum cost to buy $T$ units is $\le M$.
To find the minimum cost for $T$ units:
1. We determine a threshold marginal cost $X$ such that the total number of units with marginal cost $\le X$ is at least $T$, and the total number of units with marginal cost $\le X-1$ is less than $T$.
2. The number of units of product $i$ with marginal cost $\le X$ is $k_i(X) = \lfloor \frac{X + P_i}{2 P_i} \rfloor$. Note: If $X < P_i$, this formula gives 0, which is correct because the first unit has marginal cost $P_i$.
3. We binary search for $X$ in the range $[1, 2 \cdot 10^{18}]$ (since max marginal cost can be around $2 \cdot M \cdot \max(P_i)$? No, max marginal cost for a unit is bounded. If we buy $T$ units, the max marginal cost is roughly $2 \cdot T \cdot \max(P_i)$? Actually, since $T \le M$ and $P_i \le 2 \cdot 10^9$, the threshold $X$ can be up to $2 \cdot 10^{18} \cdot 2 \cdot 10^9$? No. The max units is $M$. The max marginal cost for the last unit is roughly $2 \cdot M \cdot \min(P_i)$? No.
   Let's bound $X$. The maximum possible units is $M$. The worst case is one product with $P_i=1$. Then $k^2 \le M \implies k \le \sqrt{M} = 10^9$. Marginal cost $\approx 2 \cdot 10^9$.
   If we have many products, say $N$ products with $P_i=1$, and we buy $T$ units. The marginal costs are $1, 1, ..., 1$ ($N$ times), then $3, 3, ..., 3$ ($N$ times), etc.
   The threshold $X$ will be around $2 \cdot \frac{T}{N}$. Since $T \le M = 10^{18}$ and $N \ge 1$, $X$ can be up to $2 \cdot 10^{18}$.
   So binary search range for $X$ is $[1, 2 \cdot 10^{18}]$.
4. Once we find the smallest $X$ such that $\sum k_i(X) \ge T$, let $S_{prev} = \sum k_i(X-1)$.
   The number of units we take with marginal cost strictly less than $X$ is $S_{prev}$.
   The number of units we take with marginal cost exactly $X$ is $rem = T - S_{prev}$.
   The total cost is $\sum_{i} \text{cost}_i(k_i(X-1)) + rem \cdot X$.
   We check if this cost $\le M$.

Pitfalls:
- Overflow: Costs and sums can exceed $2^{63}-1$. Python handles large integers automatically, so this is fine.
- Binary search bounds: Ensure the range for $T$ and $X$ is sufficient.
- Correctness of $k_i(X)$ formula: Derived as $\lfloor \frac{X + P_i}{2 P_i} \rfloor$.
- The check function must be monotonic: If $T$ is feasible, any $T' < T$ is feasible.

## worker: <none>
The problem asks for the maximum total number of units $T$ that can be bought with a budget $M$. The cost function for product $i$ is $k_i^2 P_i$, which is convex. The marginal cost of the $k$-th unit of product $i$ is $(2k-1)P_i$. To minimize the total cost for a fixed $T$, we should greedily select units with the smallest marginal costs.

We binary search on the answer $T$ (total units). The range is $[0, M]$ because each unit costs at least 1 yen.
For a fixed $T$, we determine the minimum cost to buy $T$ units:
1.  Find a threshold marginal cost $X$ such that the total number of units with marginal cost $\le X$ is at least $T$, and the total number of units with marginal cost $\le X-1$ is less than $T$.
2.  The number of units of product $i$ with marginal cost $\le X$ is $k_i(X) = \lfloor \frac{X + P_i}{2 P_i} \rfloor$.
3.  We binary search for $X$ in a large range $[1, 2 \cdot 10^{18}]$.
4.  Let $S_{prev} = \sum k_i(X-1)$. The number of units we take with marginal cost strictly less than $X$ is $S_{prev}$.
5.  The remaining $rem = T - S_{prev}$ units are taken from the pool of units with marginal cost exactly $X$. Since they all have the same marginal cost $X$, their contribution to the total cost is $rem \cdot X$.
6.  The total cost is $\sum k_i(X-1)^2 P_i + rem \cdot X$.
7.  If this cost is $\le M$, then $T$ is feasible.

Complexity:
- Binary search on $T$: $O(\log M)$ iterations.
- Inside each iteration, binary search on $X$: $O(\log (\text{max\_X}))$ iterations.
- Inside each $X$ search, we compute `count_units` and `calculate_cost` in $O(N)$.
- Total complexity: $O(N \log M \log (\text{max\_X}))$. With $N=2 \cdot 10^5$, $M=10^{18}$, this is roughly $2 \cdot 10^5 \cdot 60 \cdot 60 \approx 7.2 \cdot 10^8$ operations, which might be tight for Python. However, the constant factors are small, and the ranges are often smaller. We can optimize by noting that `count_units` and `calculate_cost` are monotonic and can be computed efficiently. Given Python's speed, this might TLE. Let's re-evaluate.

Optimization:
The inner binary search for $X$ can be optimized. Notice that `count_units(X)` is a sum of floor functions. We can't easily vectorize it, but $N$ is up to $2 \cdot 10^5$. $60 \times 60 \times 2 \cdot 10^5$ is too slow.
Wait, the outer binary search is on $T$. The inner binary search is on $X$.
Is there a way to avoid the inner binary search?
Actually, we can binary search on $X$ directly to find the maximum $T$ such that cost $\le M$? No, the relationship between $T$ and cost is not linear.
However, note that for a fixed $X$, the cost is a function of $T$.
Let's reconsider the complexity. $N=2 \cdot 10^5$. $\log M \approx 60$. $\log (\text{max\_X}) \approx 60$. $60 \times 60 \times 2 \cdot 10^5 = 7.2 \cdot 10^8$. This is definitely too slow for Python (and likely C++).

We need a more efficient check.
Notice that `count_units(X)` and `calculate_cost(X)` can be computed in $O(N)$.
Can we reduce the number of iterations?
The outer binary search is on $T$. The inner is on $X$.
Actually, we can binary search on $X$ directly to find the maximum $T$ such that the cost is $\le M$?
No, because for a fixed $X$, the cost is not a simple function of $T$.
However, we can observe that the function $f(T) = \text{min\_cost}(T)$ is convex and increasing.
We want max $T$ such that $f(T) \le M$.
The check function `check(T)` involves finding $X$ such that $\sum k_i(X) \ge T$.
This is equivalent to finding the inverse of the cumulative count function.

Let's optimize the inner part.
Instead of binary searching $X$ for each $T$, we can note that as $T$ increases, $X$ increases.
But the outer binary search jumps around.

Alternative approach:
Binary search on $X$ directly?
If we fix $X$, we can calculate the total units $S(X) = \sum k_i(X)$ and the total cost $C(X) = \sum k_i(X)^2 P_i$.
This gives us a point $(S(X), C(X))$ on the "efficient frontier".
However, $S(X)$ is a step function. The true minimum cost for $T$ units is a piecewise linear convex function connecting these points.
Specifically, for $T$ between $S(X-1)$ and $S(X)$, the cost is $C(X-1) + (T - S(X-1)) \cdot X$.
So, for a fixed $X$, we know the cost for all $T \in [S(X-1)+1, S(X)]$.
We can binary search on $X$ to find the largest $X$ such that the cost for $S(X)$ units is $\le M$?
No, because the max units might be in the middle of an interval.
But we can binary search on $X$ to find the largest $X$ such that $C(X) \le M$.
Let this be $X^*$.
Then the maximum units we can buy is at least $S(X^*)$.
But we might be able to buy more units with marginal cost $X^*+1$ if the budget allows.
Actually, the cost function is:
$Cost(T) = C(X-1) + (T - S(X-1)) \cdot X$ for $S(X-1) < T \le S(X)$.
We want max $T$ such that $Cost(T) \le M$.
We can binary search on $X$ to find the interval where $M$ falls.
Find the largest $X$ such that $C(X) \le M$. Let this be $X_{max}$.
Then we know $S(X_{max})$ units cost $\le M$.
Can we buy more? Yes, up to $S(X_{max}+1)$ units, with marginal cost $X_{max}+1$.
The cost for $T$ units in this range is $C(X_{max}) + (T - S(X_{max})) \cdot (X_{max}+1)$.
We set this $\le M$ and solve for $T$.
$T = S(X_{max}) + \lfloor \frac{M - C(X_{max})}{X_{max}+1} \rfloor$.
We must ensure $T \le S(X_{max}+1)$.

So the algorithm is:
1. Binary search on $X$ to find the largest $X$ such that $C(X) \le M$.
   Range for $X$: $[1, 2 \cdot 10^{18}]$.
2. Let $X^*$ be this value.
3. Calculate $S(X^*)$ and $C(X^*)$.
4. Calculate remaining budget $rem\_budget = M - C(X^*)$.
5. The next marginal cost is $X^* + 1$.
6. We can buy $add = \lfloor rem\_budget / (X^* + 1) \rfloor$ more units.
7. The total units is $S(X^*) + add$.
8. However, we must cap this at $S(X^*+1)$? No, because if $add$ is large, it means we can buy units with marginal cost $X^*+2$, etc.
   Wait, the formula $Cost(T) = C(X) + (T - S(X)) \cdot (X+1)$ is only valid for $T \le S(X+1)$.
   If $add$ is such that $S(X^*) + add > S(X^*+1)$, then we have bought all units with marginal cost $\le X^*+1$, and we still have budget.
   This implies $C(X^*+1) \le M$, which contradicts that $X^*$ is the largest $X$ with $C(X) \le M$.
   Therefore, $add$ will always be such that $S(X^*) + add \le S(X^*+1)$.
   Proof: If $S(X^*) + add > S(X^*+1)$, then $rem\_budget \ge (S(X^*+1) - S(X^*)) \cdot (X^*+1)$.
   Then $C(X^*+1) = C(X^*) + (S(X^*+1) - S(X^*)) \cdot (X^*+1) \le C(X^*) + rem\_budget = M$.
   This would mean $X^*+1$ is also a valid $X$, contradicting maximality of $X^*$.
   So the answer is simply $S(X^*) + \lfloor \frac{M - C(X^*)}{X^* + 1} \rfloor$.

Complexity: $O(N \log (\text{max\_X}))$. $2 \cdot 10^5 \cdot 60 \approx 1.2 \cdot 10^7$. This is very fast.
