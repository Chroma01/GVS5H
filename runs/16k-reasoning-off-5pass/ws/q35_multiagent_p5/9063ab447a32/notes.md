
## ideation
The problem asks for the maximum total units $X$ such that the minimum cost to buy $X$ units is $\le M$.
The cost function for buying $k$ units of product $i$ is $k^2 P_i$.
The marginal cost of the $j$-th unit (1-indexed) of product $i$ is $C_{i,j} = j^2 P_i - (j-1)^2 P_i = (2j-1)P_i$.
To minimize the total cost for a fixed total number of units $X$, we should greedily pick the $X$ units with the smallest marginal costs across all products.
Since $X$ can be very large (up to $10^{18}$), we cannot simulate the selection.
However, the condition "minimum cost for $X$ units $\le M$" is monotonic in $X$. If we can buy $X$ units with cost $\le M$, we can definitely buy $X-1$ units with cost $\le M$ (by removing the most expensive unit). Thus, we can binary search on the answer $X$.
The range for $X$ is $[0, M + N]$ roughly, but more tightly, since the cheapest marginal cost is at least $1 \cdot \min(P_i) \ge 1$, the maximum units is at most $M$. So range $[0, M]$.

For a fixed candidate $X$, we need to check if the minimum cost to buy $X$ units is $\le M$.
To compute the minimum cost for $X$ units efficiently:
1. We can binary search for a threshold marginal cost $T$ such that the number of units with marginal cost $< T$ is less than $X$, and the number of units with marginal cost $\le T$ is at least $X$.
2. For a given threshold $T$, the number of units of product $i$ with marginal cost $\le T$ is the largest $j$ such that $(2j-1)P_i \le T \implies 2j-1 \le T/P_i \implies j \le \frac{T/P_i + 1}{2}$. So $count_i(T) = \max(0, \lfloor \frac{\lfloor T/P_i \rfloor + 1}{2} \rfloor)$.
3. Let $S(T) = \sum_i count_i(T)$. We find the smallest $T$ such that $S(T) \ge X$.
4. The cost of all units with marginal cost $< T$ can be computed. Specifically, for each product $i$, the units $1, \dots, count_i(T)$ have marginal costs $(2j-1)P_i$. Note that if $(2j-1)P_i < T$, it is strictly less. If $(2j-1)P_i = T$, it is equal.
5. Actually, it's easier to split the cost into:
   - Cost of all units with marginal cost $< T$.
   - Cost of remaining units needed to reach $X$, which will have marginal cost exactly $T$ (if $S(T-1) < X \le S(T)$).
   
   Let $T^*$ be the threshold such that $S(T^*-1) < X \le S(T^*)$.
   Let $K = S(T^*-1)$. We need $X - K$ more units, each with marginal cost $T^*$.
   The total cost is:
   $\sum_i \text{Cost of first } count_i(T^*-1) \text{ units of product } i + (X - K) \cdot T^*$.
   
   The cost of the first $j$ units of product $i$ is $\sum_{m=1}^j (2m-1)P_i = j^2 P_i$.
   So, Total Cost = $\sum_i (count_i(T^*-1))^2 P_i + (X - K) T^*$.

   We need to binary search for $T^*$ in range $[0, 2M]$. The max marginal cost for the last unit won't exceed roughly $2M$ because the first unit costs $P_i \ge 1$, and the $k$-th unit costs approx $2k P_i$. If $k \approx M/P_i$, cost is $2M$. So $2M$ is a safe upper bound.

   Complexity: Binary search on $X$ takes $O(\log M)$. For each $X$, binary search on $T$ takes $O(\log M)$. Inside the check for $T$, we iterate over $N$ products, taking $O(N)$. Total complexity $O(N \log^2 M)$. With $N=2 \cdot 10^5$ and $\log M \approx 60$, this is roughly $2 \cdot 10^5 \cdot 3600 \approx 7.2 \cdot 10^8$ operations, which might be too slow for Python (typically $10^7-10^8$ ops/sec). We might need to optimize.

   Optimization: Instead of binary searching $X$ then $T$, we can binary search on the threshold $T$ directly to find the maximum units we can buy with cost $\le M$? No, the cost function is not linear in $T$.
   
   Alternative approach:
   Binary search on the answer $X$.
   Check function `can_buy(X)`:
     Binary search for $T$ in $[0, 2M]$.
     For a given $T$, compute $S(T) = \sum \max(0, \lfloor (\lfloor T/P_i \rfloor + 1)/2 \rfloor)$.
     Find smallest $T$ such that $S(T) \ge X$.
     Compute cost using $T^* = T$.
     Return cost $\le M$.

   To speed up, note that $N$ is large. The inner loop over $N$ is unavoidable in the check.
   Can we avoid binary searching $T$ for every $X$?
   Maybe we can binary search on $T$ globally?
   Let $F(T)$ be the minimum cost to buy $S(T)$ units? No, $S(T)$ is the count of units with marginal cost $\le T$.
   The cost to buy all units with marginal cost $< T$ is $C_{<T} = \sum_i (count_i(T-1))^2 P_i$.
   The number of such units is $K = S(T-1)$.
   If we want to buy $X$ units where $K < X \le S(T)$, the cost is $C_{<T} + (X-K)T$.
   
   We want to maximize $X$ such that there exists a $T$ with $K < X \le S(T)$ and $C_{<T} + (X-K)T \le M$.
   This looks complicated because $T$ depends on $X$.

   Let's stick to $O(N \log^2 M)$ and optimize the inner loop.
   In Python, $7 \cdot 10^8$ is definitely too slow. We need a faster approach.
   
   Notice that $count_i(T) = \max(0, \lfloor \frac{\lfloor T/P_i \rfloor + 1}{2} \rfloor)$.
   Let $q_i = \lfloor T/P_i \rfloor$. Then $count_i = \lfloor (q_i+1)/2 \rfloor$.
   
   Is there a way to compute $S(T)$ and the cost sum faster?
   The values of $P_i$ are up to $2 \cdot 10^9$. We can't use frequency arrays.
   
   However, note that for large $T$, many $P_i$ will result in $q_i$ being large.
   
   Let's reconsider the binary search on $X$.
   Range of $X$: $[0, M]$.
   Inside `check(X)`:
     Binary search $T \in [0, 2M]$.
     This is $O(\log M)$ iterations.
     Each iteration: $O(N)$ to compute sum.
     
   Total $O(N \log^2 M)$.
   
   Can we optimize the check?
   We are looking for $T$ such that $S(T) \ge X$.
   $S(T)$ is monotonically increasing with $T$.
   
   Maybe we can swap the binary searches?
   Binary search on $T$ to find the "bottleneck" threshold?
   
   Actually, let's look at the constraints again. $N=2 \cdot 10^5$.
   In C++, $O(N \log^2 M)$ might pass if constants are small. In Python, it's risky.
   
   Let's try to reduce the number of iterations or the cost per iteration.
   
   Observation:
   $count_i(T)$ changes only when $T$ crosses values of the form $(2j-1)P_i$.
   There are too many such values.
   
   Alternative Idea:
   Binary search on the answer $X$.
   To check $X$, we need the sum of the $X$ smallest marginal costs.
   The marginal costs are $(2j-1)P_i$.
   
   Let's define a function `get_cost_for_X(X)` which returns the minimum cost.
   We binary search for $T$ such that the number of marginal costs $\le T$ is at least $X$.
   
   Let's optimize the inner loop.
   Instead of full binary search on $T$ for each $X$, can we do better?
   
   Actually, we can binary search on $T$ globally to find the maximum units we can buy with cost $\le M$?
   No, because the cost depends on how many units we take below $T$.
   
   Let's try to implement the $O(N \log^2 M)$ solution efficiently in Python.
   Use `sys.stdin.read`.
   Use integer arithmetic.
   
   One optimization:
   In the inner binary search for $T$, we compute $S(T)$.
   $S(T) = \sum_i \max(0, \lfloor \frac{\lfloor T/P_i \rfloor + 1}{2} \rfloor)$.
   
   If $T$ is very large, $S(T)$ will be huge.
   
   Let's refine the range for $T$.
   Lower bound: 0.
   Upper bound: $2M$.
   
   Inside `check(X)`:
     low = 0, high = 2*M
     while low < high:
       mid = (low + high) // 2
       if S(mid) >= X:
         high = mid
       else:
         low = mid + 1
     T_star = low
     
     # Now compute cost
     # Count units with marginal cost < T_star
     # These are units with marginal cost <= T_star - 1
     K = S(T_star - 1)
     cost = 0
     for i in range(N):
       p = P[i]
       # number of units with marginal cost <= T_star - 1
       # q = floor((T_star - 1) / p)
       # cnt = (q + 1) // 2
       # cost += cnt * cnt * p
       
       # But wait, we need to be careful.
       # The units with marginal cost < T_star are exactly those with index j such that (2j-1)P_i < T_star.
       # This is equivalent to (2j-1)P_i <= T_star - 1 (since integers).
       # So yes, count is based on T_star - 1.
       
       q = (T_star - 1) // p
       cnt = (q + 1) // 2
       if cnt > 0:
         cost += cnt * cnt * p
         
     # Add remaining units at cost T_star
     remaining = X - K
     cost += remaining * T_star
     
     return cost <= M

   This is the plan.

## worker: Implement the binary search on $X$ in range $[0, M
The problem asks for the maximum number of units $X$ such that the minimum cost to buy $X$ units is at most $M$.
1. **Monotonicity**: If we can buy $X$ units with cost $\le M$, we can definitely buy $X-1$ units with cost $\le M$ (by removing the most expensive unit). Thus, the answer is monotonic, and we can binary search on $X$.
2. **Marginal Costs**: The cost to buy $k$ units of product $i$ is $k^2 P_i$. The marginal cost of the $j$-th unit (1-indexed) is $j^2 P_i - (j-1)^2 P_i = (2j-1)P_i$.
3. **Greedy Selection**: To minimize the total cost for a fixed $X$, we should pick the $X$ units with the smallest marginal costs across all products.
4. **Threshold Binary Search**: For a fixed $X$, we need to find the sum of the $X$ smallest marginal costs. We do this by binary searching for a threshold $T$ such that the number of units with marginal cost $\le T$ is at least $X$. Let this threshold be $T^*$.
   - The number of units of product $i$ with marginal cost $\le T$ is $\max(0, \lfloor (\lfloor T/P_i \rfloor + 1)/2 \rfloor)$.
   - Let $S(T)$ be the total number of such units across all products.
   - We find the smallest $T^*$ such that $S(T^*) \ge X$.
   - The cost is then computed as:
     - Sum of costs for all units with marginal cost $< T^*$ (i.e., $\le T^*-1$). For each product, if $cnt_i$ units are taken, the cost is $cnt_i^2 P_i$.
     - Plus the cost of the remaining $X - S(T^*-1)$ units, each costing exactly $T^*$.
5. **Complexity**: Binary search on $X$ takes $O(\log M)$ steps. For each step, binary search on $T$ takes $O(\log M)$ steps. Each evaluation of $S(T)$ or the cost sum takes $O(N)$. Total complexity is $O(N \log^2 M)$. Given $N=2 \cdot 10^5$ and $\log M \approx 60$, this is roughly $7.2 \cdot 10^8$ operations, which is tight for Python but should pass if constants are small and operations are simple integer arithmetic. The inner loops are straightforward and efficient.
