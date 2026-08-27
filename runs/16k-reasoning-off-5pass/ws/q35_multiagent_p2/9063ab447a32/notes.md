
## ideation
The core difficulty lies in efficiently computing the minimum cost to buy exactly $X$ units for a given $X$ during a binary search. A naive simulation or priority queue approach is too slow because $X$ can be up to $10^{18}$. 

The key insight is that the cost function $k^2 P_i$ is convex. The marginal cost of the $(k+1)$-th unit of product $i$ is $(2k+1)P_i$. To minimize total cost for a fixed total count $X$, we should greedily pick the units with the smallest marginal costs. This is equivalent to finding a threshold $\lambda$ such that we buy unit $k$ of product $i$ if its marginal cost $(2k-1)P_i \le \lambda$ (for the $k$-th unit, index starting at 1). More precisely, if we decide to buy $k_i$ units of product $i$, the condition for optimality is roughly that the marginal cost of the last unit bought is less than or equal to the marginal cost of the first unit not bought. 

Specifically, for a given threshold $T$, we can determine how many units $k_i$ to buy for each product $i$ such that the marginal cost of the $k_i$-th unit is $\le T$ and the $(k_i+1)$-th is $> T$. The marginal cost of the $j$-th unit is $(2j-1)P_i$. So we want $(2k_i-1)P_i \le T \implies 2k_i - 1 \le T/P_i \implies k_i \le \frac{T/P_i + 1}{2}$. Thus, $k_i = \max(0, \lfloor \frac{T + P_i}{2 P_i} \rfloor)$. Note: if $T < P_i$, then even the first unit has marginal cost $P_i > T$, so $k_i=0$. The formula $\lfloor \frac{T + P_i}{2 P_i} \rfloor$ works correctly for $T < P_i$ yielding 0 if $T < P_i$? Let's check: if $T=0, P_i=4$, $\lfloor 4/8 \rfloor = 0$. If $T=3, P_i=4$, $\lfloor 7/8 \rfloor = 0$. If $T=4, P_i=4$, $\lfloor 8/8 \rfloor = 1$. Correct.

So, for a fixed $T$, total units $S(T) = \sum_{i=1}^N \max(0, \lfloor \frac{T + P_i}{2 P_i} \rfloor)$. This function $S(T)$ is non-decreasing with $T$. We can binary search for the smallest $T$ such that $S(T) \ge X$. Let this be $T^*$. Then the minimum cost to buy at least $X$ units is computed using $k_i = \lfloor \frac{T^* + P_i}{2 P_i} \rfloor$. However, $S(T^*)$ might be greater than $X$. We need to adjust. Specifically, we buy $k_i$ units for all $i$, sum is $S$. If $S > X$, we need to remove $S-X$ units. The units to remove are those with the largest marginal costs among the bought units. The marginal cost of the $k_i$-th unit is $(2k_i-1)P_i$. We can sort the products by this marginal cost and remove units from the ones with the highest marginal cost until the total count is $X$. Since $N$ is up to $2 \times 10^5$, sorting is feasible.

Wait, there's a simpler way. Binary search on $X$ directly? No, computing min cost for fixed $X$ is hard. But we can binary search on $T$ to find the max $X$ such that min cost $\le M$. Actually, the problem asks for max $X$ such that min cost $\le M$. The min cost for a given $X$ is a convex function of $X$. We can binary search on $X$. For a fixed $X$, we find the optimal distribution. The optimal distribution corresponds to a threshold $T$ such that $\sum k_i = X$. We can find $T$ by binary search. Then compute cost. This inner binary search for $T$ takes $O(N \log (\text{max } T))$. Max $T$ can be around $2 \cdot 10^{18} \cdot 2 \cdot 10^9 \approx 4 \cdot 10^{27}$? No. Max units per product is $10^{18}$. Marginal cost $\approx 2 \cdot 10^{18} \cdot 2 \cdot 10^9 = 4 \cdot 10^{27}$. So $T$ can be large. Binary search on $T$ takes $\log(10^{27}) \approx 90$ steps. Total complexity $O(N \log (\text{max } X) \log (\text{max } T))$. With $N=2 \cdot 10^5$, this is roughly $2 \cdot 10^5 \cdot 60 \cdot 90 \approx 10^9$, which might be too slow for Python.

Let's reconsider. We can binary search on the answer $X$. The range of $X$ is $[0, 10^{18} \cdot N]$? No, max units is limited by $M$. If $P_i=1$, max units is $\sqrt{M} \approx 10^9$. If $P_i$ are large, units are fewer. So $X$ is at most $10^9 \cdot N$? No, if all $P_i=1$, and $M=10^{18}$, we can buy $10^9$ units total? No, if we buy $k$ units of one product, cost $k^2$. If we distribute, say $k_i$, sum $k_i^2 \le M$. Max sum $k_i$ is when all $k_i$ are equal? No, to maximize sum $k_i$ subject to $\sum k_i^2 P_i \le M$, we should put all mass on the smallest $P_i$. So max $X \approx \sqrt{M / \min(P_i)}$. With $P_i \ge 1$, max $X \le 10^9$. So $X$ is in $[0, 10^9]$. This is small!

So, binary search on $X \in [0, 10^9]$. For a fixed $X$, we need to compute min cost. To compute min cost for fixed $X$:
1. Find threshold $T$ such that $\sum_{i} \lfloor \frac{T + P_i}{2 P_i} \rfloor = X$. We can binary search $T$. Range for $T$: $[0, 2 \cdot 10^9 \cdot 10^9] = 2 \cdot 10^{18}$. Actually, max marginal cost is for $k=10^9, P=2\cdot 10^9 \implies 2 \cdot 10^9 \cdot 2 \cdot 10^9 = 4 \cdot 10^{18}$. So $T \in [0, 4 \cdot 10^{18}]$.
2. Binary search for $T$ takes $\log(4 \cdot 10^{18}) \approx 62$ steps.
3. In each step, compute sum over $N$ items: $O(N)$.
4. Total per $X$: $62 \cdot N$.
5. Binary search for $X$ takes $\log(10^9) \approx 30$ steps.
6. Total complexity: $30 \cdot 62 \cdot N \approx 1860 \cdot 2 \cdot 10^5 \approx 3.7 \cdot 10^8$. This is borderline for Python (1-2 seconds usually allows $10^7-10^8$ ops). It might be too slow.

Can we optimize? Notice that the function $S(T) = \sum \lfloor \frac{T + P_i}{2 P_i} \rfloor$ is piecewise linear. We can compute it faster? Not easily.

Alternative: Binary search on $T$ directly to find the max $X$ such that min cost $\le M$. But we want max $X$. The min cost for a given $T$ is $C(T) = \sum k_i^2 P_i$. This is increasing in $T$. We can binary search on $T$ to find the max $T$ such that $C(T) \le M$. Then $X = S(T)$. But $S(T)$ might jump. We need the max $X$ such that min cost $\le M$. The min cost for a given $X$ is convex. The max $X$ is such that min cost $(X) \le M$. 

Actually, the mapping from $T$ to $X$ and Cost is monotonic. As $T$ increases, $X$ increases and Cost increases. So we can binary search on $T$ to find the largest $T$ such that the cost of the distribution defined by $T$ is $\le M$. Let this be $T^*$. Then $X^* = S(T^*)$. But is this the max $X$? Yes, because any distribution with total units $X > X^*$ would require a higher threshold $T > T^*$, which would imply a higher cost. However, there's a catch: for a fixed $T$, the distribution is unique and minimizes cost for that specific count $S(T)$. But we might be able to achieve count $S(T)+1$ with cost $\le M$? No, because the marginal cost of the next unit is $> T$, and the current last unit has marginal cost $\le T$. The cost increase is significant. 

Actually, the standard approach is: Binary search on $X$. For each $X$, compute min cost. If min cost $\le M$, try larger $X$. Else, try smaller. This is robust.

To speed up, note that $N$ is large. We can precompute nothing? The inner loop is simple arithmetic. In Python, $3.7 \cdot 10^8$ simple integer operations might take 10-20 seconds. We need a faster method.

Observation: The function $S(T)$ can be computed in $O(N)$. Is there a way to avoid binary searching $T$ for every $X$? 
We can binary search on $T$ directly to find the max $T$ such that the cost is $\le M$. Let $T_{max}$ be this value. Then $X = S(T_{max})$. But we must check if we can add more units without exceeding $M$. The next unit to add would be one of the products with the smallest marginal cost among those not yet bought. The marginal cost of the $(k_i+1)$-th unit is $(2k_i+1)P_i$. We can compute these for all $i$ with $k_i = \lfloor \frac{T_{max} + P_i}{2 P_i} \rfloor$. Sort these marginal costs. The smallest one is the cost to add the next unit. If current cost + smallest marginal cost $\le M$, then we can add it. We can add multiple units? Yes, but we must add them in order of increasing marginal cost. This becomes a knapsack-like problem but with convex costs. However, since we are at the boundary, we can just add units one by one? No, too many.

Actually, the binary search on $X$ is the most straightforward. Let's optimize the inner loop.
The inner loop computes $S(T)$ and Cost$(T)$.
We can combine the binary search for $X$ and the binary search for $T$? No.

Let's stick to binary search on $X$. To make it faster in Python, we can use `sys.stdin.read` and efficient loops. We can also prune: if $M$ is small, $X$ is small.

Another idea: The optimal $k_i$ are roughly $C / P_i$. We can estimate $T$ and refine. But binary search is safe.

Let's implement binary search on $X$. Range $[0, 10^9]$.
For a given $X$, we binary search $T$ in $[0, 4 \cdot 10^{18}]$.
Find smallest $T$ such that $S(T) \ge X$.
Then compute cost for this $T$. But $S(T)$ might be $> X$. We need to remove $S(T)-X$ units. The units to remove are those with the largest marginal costs. We can compute the marginal cost of the last unit bought for each product: $mc_i = (2k_i-1)P_i$. Sort these. Remove the ones with largest $mc_i$. This adds $O(N \log N)$ per check, which is too slow.

Better: For a fixed $X$, we want the distribution that minimizes cost. This distribution corresponds to a threshold $T$ such that $\sum k_i = X$. If we find $T$ such that $S(T) = X$, we are done. If $S(T)$ jumps over $X$, it means there is no $T$ that gives exactly $X$ units with the "clean" threshold rule? No, the threshold rule gives a specific set of units. The set of all possible "optimal" distributions for some $X$ are those defined by thresholds. Any $X$ can be achieved by a threshold distribution? No. For example, if we have one product, $S(T)$ takes values $0, 1, 2, \dots$. For multiple products, $S(T)$ is the sum. It is possible that $S(T)$ skips some values? No, because as $T$ increases continuously, $k_i$ increases by 1 at specific points. So $S(T)$ increases by 1 at each event. So for any $X$, there is a $T$ such that $S(T)=X$. We just need to find the smallest $T$ such that $S(T) \ge X$. Then $S(T)$ will be exactly $X$ if we define the events carefully? Actually, at the exact value of $T$ where a marginal cost equals $T$, the floor function might behave. We should use $k_i = \lfloor \frac{T + P_i - 1}{2 P_i} \rfloor + 1$? No.

Let's use the definition: Buy unit $j$ of product $i$ if $(2j-1)P_i \le T$. Then $j \le \frac{T/P_i + 1}{2}$. So $k_i = \lfloor \frac{T + P_i}{2 P_i} \rfloor$.
This $k_i$ is the number of units bought.
We binary search for the smallest $T$ such that $\sum k_i \ge X$.
Let this be $T^*$. Then $\sum k_i \ge X$. Let $S = \sum k_i$.
If $S == X$, compute cost.
If $S > X$, we have bought too many units. We need to remove $S-X$ units. The units we bought are all units $j$ such that $(2j-1)P_i \le T^*$. The units to remove are those with the largest marginal costs. The marginal cost of the $k_i$-th unit is $(2k_i-1)P_i$. We can compute these for all $i$, sort them, and remove the ones with the highest marginal costs. This is $O(N \log N)$. With $N=2 \cdot 10^5$, $\log N \approx 18$. $30 \cdot 62 \cdot 18 \cdot N \approx 6 \cdot 10^9$ ops. Too slow.

We need a faster way to handle the "remove units" part.
Notice that we only need to remove a few units? No, $S-X$ can be large.
However, note that $S(T)$ is the sum of floors. The difference $S(T) - X$ is usually small? No.

Alternative: Binary search on $T$ to find the max $T$ such that the cost is $\le M$.
Let $T_{opt}$ be the largest $T$ such that Cost$(T) \le M$.
Then $X = S(T_{opt})$.
Is it possible that we can buy more units with cost $\le M$?
The next unit to buy would have marginal cost $> T_{opt}$. The cost would increase by at least the smallest such marginal cost. If Cost$(T_{opt}) + \text{min next marginal cost} \le M$, then we can buy more.
So, after finding $T_{opt}$, we compute the marginal costs of the next unit for each product: $mc_i = (2k_i+1)P_i$. Sort these. Add them one by one to the cost and count until we exceed $M$. This is efficient because the number of additional units is small? Not necessarily. If $M$ is very large, we might add many units. But if $M$ is large, $T_{opt}$ is large, and we are near the limit. The number of units we can add is limited by the remaining budget. The marginal costs increase. We can add units until the cost exceeds $M$. This loop might be long.

However, note that the total number of units is at most $10^9$. The binary search on $T$ gives us a base. The "add units" part might be slow if we do it one by one.

Let's go back to binary search on $X$. It is the most standard.
To speed up the inner loop, we can avoid sorting.
For a fixed $X$, we find $T$ such that $S(T) \approx X$.
Actually, we can binary search on $T$ to find the exact distribution for $X$.
The key is that we don't need to sort if we can compute the cost directly.
But we established that $S(T)$ might not equal $X$.

Let's try a different perspective.
The problem is equivalent to: Minimize $\sum k_i^2 P_i$ subject to $\sum k_i = X$.
This is a resource allocation problem with convex costs.
The optimal solution satisfies $2 k_i P_i \approx \lambda$.
We can binary search on $\lambda$.
For a given $\lambda$, $k_i = \lfloor \frac{\lambda}{2 P_i} \rfloor$ or similar.
Let's use $k_i = \lfloor \frac{\lambda + P_i}{2 P_i} \rfloor$ as before.
This is the same as $T = \lambda$.

I will implement binary search on $X$ with the inner binary search on $T$. To handle the $S > X$ case efficiently, I will note that $S(T)$ is very close to $X$. In fact, $S(T)$ is the smallest value $\ge X$. The difference $S(T) - X$ is less than $N$? No. It can be up to $N$. Because $S(T)$ increases by at most $N$ when $T$ crosses a threshold? No, it increases by 1 at each event. The events are distinct. So $S(T)$ takes all integer values. So there exists a $T$ such that $S(T) = X$. We just need to find the largest $T$ such that $S(T) \le X$? No, we need the $T$ that gives exactly $X$.
Since $S(T)$ is non-decreasing and increases by 1 at each step, we can find $T$ such that $S(T) = X$ by binary searching for the largest $T$ such that $S(T) \le X$. Then $S(T)$ will be $X$ if we are lucky? No, $S(T)$ is a step function. The value $X$ is achieved at a range of $T$. We can pick any $T$ in that range. The cost is constant for that range? No, the cost depends on the $k_i$, which are constant for that range. So yes, the cost is constant.
So, for a fixed $X$, we binary search for the largest $T$ such that $S(T) \le X$. Let this be $T^*$. Then $S(T^*) = X$ (since $S$ takes all values). Then we compute the cost for $T^*$. This avoids the removal step!
This is the key. $S(T)$ takes all integer values from 0 to infinity. So for any $X$, there is a $T$ such that $S(T)=X$. We find the largest such $T$. Then the cost is computed directly.

Complexity: Binary search on $X$ (30 steps) * Binary search on $T$ (60 steps) * $O(N)$ per step.
$30 \cdot 60 \cdot 2 \cdot 10^5 = 3.6 \cdot 10^8$. This is heavy for Python.
Can we reduce the range of $T$?
Max $T$ is $4 \cdot 10^{18}$. $\log_2(4 \cdot 10^{18}) \approx 62$.
Can we reduce the range of $X$?
Max $X$ is $10^9$. $\log_2(10^9) \approx 30$.
Total operations: $30 \cdot 62 \cdot 2 \cdot 10^5 \approx 3.7 \cdot 10^8$.
In Python, this might TLE. We need to optimize the inner loop.
The inner loop is:
```python
def count_units(T, P):
    s = 0
    for p in P:
        s += (T + p) // (2 * p)
    return s
```
This loop is in Python. $2 \cdot 10^5$ iterations. 62*30 = 1860 calls. Total $3.7 \cdot 10^8$ iterations.
This is likely too slow for Python (1-2 sec limit).

We need a faster way to compute $S(T)$.
$S(T) = \sum \lfloor \frac{T + P_i}{2 P_i} \rfloor = \sum \lfloor \frac{T}{2 P_i} + \frac{1}{2} \rfloor$.
This doesn't simplify easily.

However, note that we are binary searching on $X$. The values of $T$ we check are correlated.
But we can't easily reuse.

Let's try to binary search on $T$ directly to find the max $T$ such that Cost$(T) \le M$.
Then $X = S(T)$.
This is one binary search on $T$ (60 steps) * $O(N)$ per step.
Total $60 \cdot 2 \cdot 10^5 = 1.2 \cdot 10^7$. This is very fast!
Then, we have a base $X_0 = S(T_{max})$ and Cost $C_0 \le M$.
We need to see if we can add more units.
The next units to add are those with the smallest marginal costs among the ones not yet bought.
Marginal cost of next unit for product $i$ is $(2k_i+1)P_i$.
We compute these for all $i$. Sort them.
Add them one by one to the cost and count, until we exceed $M$.
How many units can we add?
The marginal costs are at least $T_{max}$. The remaining budget is $M - C_0$.
The number of units we can add is at most $(M - C_0) / T_{max}$.
If $T_{max}$ is large, this number is small.
If $T_{max}$ is small, then $M$ must be large relative to $T_{max}$.
But if $T_{max}$ is small, then $X_0$ is small.
The total number of units is at most $10^9$.
The sorting takes $O(N \log N)$.
The adding loop: if we add $K$ units, it takes $O(K)$.
Is $K$ small?
In the worst case, $T_{max}$ is small, say 1. Then we might add $10^9$ units. This is too slow.
But if $T_{max}$ is small, it means $P_i$ are small or $X$ is small.
If $P_i=1$, $T_{max} \approx 2 \sqrt{M}$. Then $K$ is small?
No, if $P_i=1$, $k_i \approx \sqrt{M}$. $T \approx 2 \sqrt{M}$.
The next marginal cost is $2 \sqrt{M} + 1$.
The remaining budget is small?
Actually, if we find $T_{max}$ such that Cost$(T_{max}) \le M$, then $T_{max}$ is close to the optimal threshold. The cost is very close to $M$. The remaining budget is small compared to the marginal cost of the next unit? Not necessarily.
However, note that the marginal costs increase. We can add units in batches?
No, the marginal costs are different for each product.

But wait, if $T_{max}$ is small, then $X_0$ is small. The total units $X$ is at most $10^9$.
If $X_0$ is small, and we add $K$ units, $K$ is at most $10^9$.
Sorting $N$ items is $2 \cdot 10^5 \log(2 \cdot 10^5) \approx 3.6 \cdot 10^6$.
If $K$ is large, we can't iterate.

However, observe that if $T_{max}$ is small, then the marginal costs are small. The number of units we can add is limited by the budget.
If the budget is large, $T_{max}$ would be large.
There is a trade-off.
Actually, the number of units we add is at most $N$? No.
But note that after adding one unit to a product, its marginal cost increases.
We can use a priority queue to add units one by one.
But if we add $10^9$ units, it's too slow.

Let's check the constraints. $M \le 10^{18}$.
If $P_i=1$, max units is $10^9$.
If we use the binary search on $T$ method, we get $X_0$.
Then we add units.
If $X_0$ is close to $10^9$, then we add few units.
If $X_0$ is small, then $M$ is small or $P_i$ are large.
If $P_i$ are large, $X_0$ is small.
If $P_i=1$, $X_0 \approx 10^9$.
So in most cases, $X_0$ is close to the answer.
The number of units to add is small.
Why? Because the marginal cost of the next unit is at least $T_{max}$.
The cost of $X_0$ units is $C_0$.
$M - C_0 < \text{marginal cost of next unit} \times 1$? No.
But $T_{max}$ is the largest threshold such that cost $\le M$.
This implies that for $T_{max} + \epsilon$, the cost would exceed $M$.
The cost function is continuous in a sense.
The jump in cost when moving from $T_{max}$ to the next threshold is the cost of the next unit.
So $M - C_0$ is less than the cost of the next unit? No, it's less than the cost of the next unit PLUS the cost of subsequent units? No.
Actually, $C(T)$ is the cost for $S(T)$ units.
If we increase $T$ slightly, $S(T)$ stays same, cost stays same.
When $T$ crosses a marginal cost, $S(T)$ increases by 1, and cost increases by that marginal cost.
So, if $C(T_{max}) \le M$ and $C(T_{max}+\epsilon) > M$, it means that the next unit's cost is $> M - C(T_{max})$.
So we can add at most 0 units? No, we can add units if their marginal cost is $\le M - C(T_{max})$.
But the next unit has marginal cost $> T_{max}$? No, the next unit has marginal cost equal to the next threshold.
Let $T_{next}$ be the next threshold. The marginal cost is $T_{next}$.
If $C(T_{max}) + T_{next} \le M$, we can add it.
So we add units as long as their marginal cost $\le M - C_{current}$.
Since the marginal costs are increasing, we can add a sequence of units.
The number of units we add is the number of marginal costs $\le M - C_{current}$.
Since the marginal costs are at least $T_{max}$, the number of units is at most $(M - C_{current}) / T_{max}$.
If $T_{max}$ is large, this is small.
If $T_{max}$ is small, then $M$ must be large for $X$ to be large.
But if $T_{max}$ is small, then $X_0$ is small.
The total units $X$ is at most $10^9$.
If $X_0$ is small, say $10^5$, and we add $10^9$ units, it's slow.
But if $X_0$ is small, then $T_{max}$ is small.
If $T_{max}$ is small, then $P_i$ are small or $X_0$ is small.
If $P_i=1$, $T_{max} \approx 2 \sqrt{M}$.
If $M=10^{18}$, $T_{max} \approx 2 \cdot 10^9$.
Then the number of units to add is $(M - C_0) / T_{max}$.
$C_0 \approx M$. So $M - C_0$ is small.
So the number of units to add is small.
This heuristic suggests that the number of units to add is small.
So we can use a priority queue to add units one by one.

Plan:
1. Binary search on $T \in [0, 4 \cdot 10^{18}]$ to find the largest $T$ such that Cost$(T) \le M$.
   - Compute $k_i = \lfloor \frac{T + P_i}{2 P_i} \rfloor$.
   - Compute $S = \sum k_i$ and $C = \sum k_i^2 P_i$.
   - If $C \le M$, store $T$ and move right. Else move left.
2. Let $T_{opt}$ be the found $T$. Compute $k_i$ and $C_0, X_0$.
3. Compute the marginal cost of the next unit for each product: $mc_i = (2k_i+1)P_i$.
4. Use a min-heap to extract the smallest $mc_i$.
5. While heap is not empty and $C_0 + mc \le M$:
   - Pop smallest $mc$.
   - $C_0 += mc$.
   - $X_0 += 1$.
   - Update $k_i$ for that product, compute new $mc_i = (2k_i+1)P_i$, push to heap.
6. Print $X_0$.

This should be efficient. The binary search is $O(N \log (\text{max } T))$. The heap operations: each unit added is one pop and one push. The number of units added is small.

## worker: (none)
1. **Binary Search on Threshold T**: The problem is to maximize total units $X$ such that the minimum cost to buy $X$ units is $\le M$. The minimum cost for a fixed distribution is achieved when the marginal costs of all bought units are less than or equal to the marginal costs of all unbought units. This defines a threshold $T$. For a given $T$, the number of units $k_i$ of product $i$ is determined by $(2k_i-1)P_i \le T \implies k_i = \lfloor \frac{T + P_i}{2P_i} \rfloor$.
2. **Monotonicity**: The total cost $C(T) = \sum k_i^2 P_i$ is non-decreasing with $T$. We binary search for the largest $T$ such that $C(T) \le M$. This gives a base number of units $X_0$ and cost $C_0$.
3. **Greedy Addition**: After finding the optimal threshold $T$, we might be able to buy more units. The next available units are those with the smallest marginal costs among the unbought ones. The marginal cost of the $(k_i+1)$-th unit is $(2k_i+1)P_i$. We use a min-heap to efficiently extract the cheapest next unit, buy it, update the state, and push the next marginal cost for that product. This continues until we can no longer afford the cheapest next unit.
4. **Complexity**:
   - Binary search on $T$: Range is $[0, 4 \cdot 10^{18}]$, so $\approx 62$ iterations. Each iteration takes $O(N)$. Total: $O(N \log (\text{max } T))$.
   - Heap operations: Each unit added involves a heap pop and push ($O(\log N)$). The number of units added is typically small because the marginal costs increase rapidly. In the worst case, if many units are added, the heap operations dominate, but given the convexity and budget constraint, this is efficient enough.
   - Overall complexity is well within limits for $N=2 \cdot 10^5$ and $M=10^{18}$.
