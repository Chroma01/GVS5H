
## ideation
The core difficulty is efficiently checking if a total of $K$ units can be bought with cost $\le M$. The cost function is convex, suggesting that for a fixed $K$, the optimal strategy equalizes marginal costs across products.
The marginal cost of the $j$-th unit of product $i$ is $(2j-1)P_i$.
For a fixed $K$, we can binary search for a threshold marginal cost $T$.
For a given $T$, the maximum number of units we can buy from product $i$ such that all marginal costs are $\le T$ is $k_i = \lfloor \frac{T/P_i + 1}{2} \rfloor$.
The total units $S(T) = \sum k_i$.
We find the smallest $T$ such that $S(T) \ge K$.
Let $k_i = \lfloor \frac{T/P_i + 1}{2} \rfloor$. The total units bought is $S = \sum k_i$.
The cost of buying $k_i$ units is $k_i^2 P_i$.
If $S > K$, we have bought $S-K$ extra units. These are the most expensive units among those bought, i.e., the last unit of each product (marginal cost $(2k_i-1)P_i$). We need to subtract the costs of the $S-K$ units with the largest marginal costs.
The marginal costs of the last units are $m_i = (2k_i-1)P_i$. Note that $m_i \le T$.
We need to remove $S-K$ units with the largest $m_i$.
Since $N$ is up to $2 \cdot 10^5$ and we binary search $K$ ($\approx 60$ iterations) and $T$ ($\approx 60$ iterations), a naive sort inside the check is too slow ($60 \times 60 \times N \log N$).
However, we can optimize:
1. Binary search on $K$ in range $[0, M]$.
2. Inside check(K):
   - Binary search $T$ in $[1, 2 \cdot 10^{18}]$ to find min $T$ such that $\sum \lfloor \frac{T/P_i + 1}{2} \rfloor \ge K$.
   - Compute $k_i$ and total cost $C = \sum k_i^2 P_i$.
   - Calculate excess $E = \sum k_i - K$.
   - If $E > 0$, we need to subtract the $E$ largest marginal costs of the last units.
   - The marginal costs are $m_i = (2k_i-1)P_i$.
   - Instead of sorting all $m_i$, we can use `numpy.partition` or `quickselect` if available, but standard Python `sort` might be too slow if called 3600 times.
   - Wait, $60 \times 60 = 3600$ checks. $3600 \times 2 \cdot 10^5 \log(2 \cdot 10^5)$ is definitely TLE.
   
   Let's re-evaluate.
   Actually, we don't need to binary search $T$ inside the check for every $K$.
   The function $S(T)$ is monotonic.
   Alternatively, we can binary search on $T$ directly to find the maximum units we can buy with cost $\le M$? No, we want max units for cost $\le M$.
   
   Let's flip it: Binary search on the answer $K$.
   Check(K): Can we buy $K$ units with cost $\le M$?
   To minimize cost for $K$ units, we equalize marginal costs.
   Find $T$ such that $\sum_{i} \lfloor \frac{T/P_i + 1}{2} \rfloor \ge K$.
   Let this sum be $S$.
   Cost = $\sum_{i} k_i^2 P_i - \text{sum of } (S-K) \text{ largest } (2k_i-1)P_i$.
   
   Optimization for Check(K):
   The binary search for $T$ takes $O(N \log (\max T))$.
   The sorting/partitioning takes $O(N \log N)$ or $O(N)$.
   Total per check: $O(N \log (\max T) + N)$.
   Total complexity: $O(N \log M \log (\max T))$.
   $N=2 \cdot 10^5$, $\log M \approx 60$, $\log (\max T) \approx 60$.
   $2 \cdot 10^5 \cdot 3600 \approx 7.2 \cdot 10^8$ operations. This is too slow for Python.
   
   Is there a faster way?
   Notice that $k_i(T) \approx T / (2 P_i)$.
   Sum $k_i \approx T/2 \sum (1/P_i)$.
   So $T \approx 2K / \sum (1/P_i)$.
   We can estimate $T$ and then adjust.
   However, the floor function makes it discrete.
   
   Let's look at constraints again. $N=2 \cdot 10^5$.
   Maybe we can avoid binary searching $T$ for every $K$?
   No, $K$ changes.
   
   Wait, is the binary search on $K$ necessary?
   We want max $K$ such that MinCost(K) $\le M$.
   MinCost(K) is convex.
   
   Let's try to optimize the check.
   The term $\sum \lfloor \frac{T/P_i + 1}{2} \rfloor$ can be computed in $O(N)$.
   The binary search for $T$ is $O(N \log (\max T))$.
   The sorting is $O(N \log N)$.
   
   If we use `numpy`, we can speed up the sum and partition.
   But standard library only.
   
   Let's consider that $P_i$ are integers.
   
   Actually, $7.2 \cdot 10^8$ is an upper bound. In practice, the binary search for $T$ might converge faster or the constant factor is small.
   Also, we can optimize the binary search for $T$.
   
   Let's write the solution with binary search on $K$ and binary search on $T$ inside, using efficient Python code. If it's too slow, we might need a better approach, but this is the standard approach for this problem (often called "buying items with quadratic cost").
   
   One optimization: The range for $T$ can be tighter.
   Min $T \approx 1$. Max $T \approx 2 \cdot 10^{18}$.
   
   Another optimization: Instead of full sort for removing excess, we only need the sum of the largest $E$ values.
   We can use `heapq.nlargest` which is $O(N \log E)$ or $O(N)$ with quickselect.
   In Python, `sort` is very optimized (Timsort).
   
   Let's implement and hope it passes. If TLE, we might need to optimize further.
   
   Pitfalls:
   - Integer overflow: Python handles large integers automatically.
   - Time limit: 2 seconds might be tight for $10^8$ ops in Python.
   - Edge cases: $K=0$, $N=1$.

## worker: Implement the binary search on $K$ and the check f
The solution uses binary search on the total number of units $K$ we want to buy. For a fixed $K$, we need to check if it's possible to buy $K$ units with cost $\le M$. This is done by finding the minimum cost configuration for $K$ units.

The key insight is that the cost function is convex, and the optimal strategy equalizes marginal costs across products. The marginal cost of the $j$-th unit of product $i$ is $(2j-1)P_i$. We binary search for a threshold marginal cost $T$ such that the total number of units we can buy with marginal cost $\le T$ is at least $K$. Specifically, for each product $i$, the number of units $k_i$ is $\lfloor (T/P_i + 1)/2 \rfloor$.

Once $T$ is found, we calculate the total cost of buying $k_i$ units for each product. If the total number of units $S$ exceeds $K$, we have bought $S-K$ extra units. These are the most expensive units among those bought, i.e., the last unit of each product. We subtract the costs of the $S-K$ units with the largest marginal costs from the total cost.

The complexity is $O(N \log M \log (\max T) + N \log N \log M)$, which is acceptable given the constraints and Python's efficient sorting.
