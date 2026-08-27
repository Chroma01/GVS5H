
## ideation
The core difficulty lies in efficiently checking if a total of $K$ units can be purchased with cost $\le M$. Since the cost function $\sum k_i^2 P_i$ is convex, the minimum cost for a fixed total $K$ is achieved when the marginal costs of adding the last unit to each product are as balanced as possible. Specifically, for a product $i$ with $k_i$ units, the marginal cost of the $j$-th unit is $P_i \cdot ((j)^2 - (j-1)^2) = P_i(2j-1)$.

We can binary search for the answer $K$ in the range $[0, 2 \cdot 10^9]$ (since max units from one product with $P=1$ and $M=10^{18}$ is $10^9$, and spreading across products doesn't increase the max possible count beyond roughly this order, actually slightly more but bounded by $\sum \sqrt{M/P_i}$ which is at most $N \sqrt{M}$ but practically limited by the fact that we want to minimize cost, so we focus on cheap products. A safe upper bound is $2 \cdot 10^9$ or even $10^9 + N$ is too small? Let's check: if all $P_i=1$, min cost for $K$ units is when $k_i \approx K/N$. Cost $\approx N (K/N)^2 = K^2/N$. So $K^2/N \le M \implies K \le \sqrt{MN}$. With $M=10^{18}, N=2\cdot 10^5$, $K \le \sqrt{2 \cdot 10^{23}} \approx 4.5 \cdot 10^{11}$. So the upper bound for binary search should be around $10^{12}$ or $2 \cdot 10^{12}$ to be safe.

For a fixed $K$, we need to find the minimum cost. This can be done by binary searching for a "marginal cost threshold" $\lambda$. For a given $\lambda$, the maximum number of units $k_i$ we can buy from product $i$ such that the marginal cost of the last unit is $\le \lambda$ is $k_i = \lfloor \frac{\lambda/P_i + 1}{2} \rfloor$. We sum these $k_i$ to get total units $U(\lambda)$. We want $U(\lambda) \ge K$. We can find the smallest $\lambda$ such that $U(\lambda) \ge K$. Then the cost is calculated based on these $k_i$ values. Note that we might have "spare" units if $U(\lambda) > K$, but since we want the minimum cost for *exactly* $K$ (or at most $K$? No, we want max units for cost $\le M$, so for a fixed $K$, we check if min cost $\le M$), we should take exactly $K$ units. The optimal strategy for exactly $K$ units is to take the $K$ cheapest marginal costs. The threshold method gives us the set of units with marginal cost $\le \lambda$. If the count is greater than $K$, we remove the most expensive ones among those selected (which are those with marginal cost closest to $\lambda$).

Algorithm for `check(K)`:
1. Binary search for $\lambda$ such that $\sum_i \lfloor \frac{\lambda/P_i + 1}{2} \rfloor \ge K$. Let this count be $C$.
2. Calculate the cost of buying $k_i = \lfloor \frac{\lambda/P_i + 1}{2} \rfloor$ units for each product.
3. If $C > K$, we have bought too many units. We need to remove $C - K$ units. These should be the units with the highest marginal cost among the selected ones. The marginal cost of the $j$-th unit of product $i$ is $P_i(2j-1)$. The selected units for product $i$ are $1, \dots, k_i$. The most expensive one is $k_i$-th unit with cost $P_i(2k_i-1)$. We can collect all these marginal costs, sort them, and subtract the largest $C-K$ costs from the total. However, sorting is $O(N \log N)$ which might be slow if done inside the binary search for $K$.
4. Optimization: Instead of full sort, we can use the fact that we are binary searching $\lambda$. Or, we can use a priority queue approach? No, $N$ is large.
5. Alternative for `check(K)`: Use the property that the optimal $k_i$ are close to each other in terms of marginal cost. We can binary search $\lambda$ in range $[0, 2 \cdot 10^{18}]$ (since max marginal cost can be around $2 \cdot 10^9 \cdot 2 \cdot 10^9 \approx 4 \cdot 10^{18}$? No, max $k_i \approx 10^9$, $P_i \approx 10^9$, marginal cost $\approx 2 \cdot 10^{18}$).
   - For a fixed $\lambda$, compute $k_i = \max(0, \lfloor \frac{\lambda/P_i + 1}{2} \rfloor)$.
   - Sum $k_i$ to get $S$.
   - If $S < K$, we need higher $\lambda$.
   - If $S \ge K$, we can compute the cost. But we need exactly $K$.
   - The cost for $k_i$ units is $\sum k_i^2 P_i$.
   - If $S > K$, we need to subtract the cost of the $S-K$ most expensive marginal units. The marginal cost of the last unit of product $i$ is $m_i = P_i(2k_i-1)$. We need to subtract the sum of the largest $S-K$ values from the set $\{m_i \mid i=1\dots N\}$.
   - To do this efficiently without sorting, we can binary search for a cutoff value $\mu$ within the marginal costs of the selected units. But this is complex.

Let's refine the check:
We want to find min cost for exactly $K$.
The marginal costs are $P_i, 3P_i, 5P_i, \dots$.
We can binary search for a threshold $\lambda$ such that the number of units with marginal cost $< \lambda$ is less than $K$, and with marginal cost $\le \lambda$ is at least $K$.
Let $k_i$ be the number of units of product $i$ with marginal cost $< \lambda$. i.e., $P_i(2j-1) < \lambda \Rightarrow 2j-1 < \lambda/P_i \Rightarrow j < (\lambda/P_i + 1)/2$. So $k_i = \lfloor \frac{\lambda - 1}{2 P_i} + 0.5 \rfloor$? No.
Condition: $P_i(2j-1) < \lambda \iff 2j-1 < \lambda/P_i \iff 2j < \lambda/P_i + 1 \iff j < \frac{\lambda/P_i + 1}{2}$.
So $k_i = \lfloor \frac{\lambda/P_i + 1}{2} - \epsilon \rfloor = \lfloor \frac{\lambda - 1}{2 P_i} + 0.5 \rfloor$? Let's stick to integer arithmetic.
$k_i = \lfloor \frac{\lambda - 1}{2 P_i} \rfloor + 1$ if $\lambda > P_i$?
Actually, simpler: $k_i$ is the largest integer such that $P_i(2k_i-1) < \lambda$.
$2k_i - 1 < \lambda/P_i \Rightarrow 2k_i < \lambda/P_i + 1 \Rightarrow k_i \le \lfloor \frac{\lambda/P_i + 1 - \epsilon}{2} \rfloor$.
In integer arithmetic: $k_i = (\lambda - 1) // (2 * P_i) + 1$ if $\lambda > P_i$ else 0.
Let $S = \sum k_i$.
If $S \ge K$, then the optimal solution includes all units with marginal cost $< \lambda$, and possibly some with marginal cost $= \lambda$.
The cost of these $S$ units is $\sum_{i} k_i^2 P_i$.
We have $S - K$ extra units. These are the ones with marginal cost $= \lambda$ (if any) or the largest marginal costs among those $< \lambda$? No, the threshold $\lambda$ separates the set.
Actually, it's easier to binary search for $\lambda$ such that the number of units with marginal cost $\le \lambda$ is $\ge K$.
Let $k_i(\lambda)$ be the max units with marginal cost $\le \lambda$.
$k_i(\lambda) = \lfloor \frac{\lambda/P_i + 1}{2} \rfloor$.
Let $S(\lambda) = \sum k_i(\lambda)$.
Find smallest $\lambda$ such that $S(\lambda) \ge K$.
Then the cost is $\sum k_i(\lambda)^2 P_i$ minus the cost of the $S(\lambda) - K$ most expensive units among the selected ones.
The selected units for product $i$ have marginal costs $P_i, 3P_i, \dots, P_i(2k_i-1)$.
The most expensive ones are at the end.
We can collect the marginal costs of the last unit of each product: $m_i = P_i(2k_i-1)$.
We need to remove $R = S(\lambda) - K$ units. These should be the ones with the largest marginal costs.
Since we only removed the "top" units, we can sort the $m_i$ values? $N=2 \cdot 10^5$, sorting is fast enough inside a binary search that runs $\approx 60$ times? $60 \cdot 2 \cdot 10^5 \log(2 \cdot 10^5) \approx 60 \cdot 3.6 \cdot 10^6 \approx 2 \cdot 10^8$ operations. This might be too slow for 2 seconds.

We need a faster way to subtract the largest $R$ marginal costs.
We can use a selection algorithm or binary search on the value of the marginal cost to subtract.
Let's binary search for a value $\mu$ such that the number of selected units with marginal cost $> \mu$ is at least $R$, and with marginal cost $\ge \mu$ is at most $R$?
Actually, we can just binary search for $\mu$ such that $\sum_i \max(0, k_i - \text{count of units in } i \text{ with cost } \le \mu) = R$? No.
We want to remove $R$ units with the highest marginal costs.
The marginal costs of the last $j$ units of product $i$ are $P_i(2(k_i-j+1)-1), \dots, P_i(2k_i-1)$.
This is getting complicated.

Alternative: Use a priority queue to simulate the process? No, $K$ is large.

Let's reconsider the binary search on $K$.
Range $[0, 2 \cdot 10^{12}]$.
Inside `check(K)`:
1. Binary search $\lambda$ in $[0, 2 \cdot 10^{18}]$.
   - Compute $k_i = \lfloor \frac{\lambda/P_i + 1}{2} \rfloor$.
   - Sum $S = \sum k_i$.
   - If $S \ge K$, store $\lambda$ and try smaller.
   - Else, try larger.
   - Let $\lambda^*$ be the smallest $\lambda$ with $S \ge K$.
2. Calculate total cost for $k_i(\lambda^*)$ units.
3. Calculate $R = S - K$.
4. We need to subtract the sum of the $R$ largest marginal costs among the selected units.
   - The marginal costs of the selected units for product $i$ are $P_i, 3P_i, \dots, P_i(2k_i-1)$.
   - We can collect all $m_i = P_i(2k_i-1)$ and sort them? Too slow.
   - Instead, binary search for a threshold $\mu$ such that the number of selected units with marginal cost $> \mu$ is $\le R$ and with marginal cost $\ge \mu$ is $\ge R$.
   - Let $cnt(\mu)$ be the number of selected units with marginal cost $> \mu$.
   - $cnt(\mu) = \sum_i \max(0, k_i - \lfloor \frac{\mu/P_i + 1}{2} \rfloor)$.
   - Binary search $\mu$ in $[0, \lambda^*]$.
   - Find $\mu$ such that $cnt(\mu) \le R$ and $cnt(\mu-1) > R$? Or similar.
   - Let $R_{high}$ be the number of units with marginal cost $> \mu$. We must remove all of them.
   - Let $R_{mid}$ be the number of units with marginal cost $= \mu$. We remove some of them.
   - The cost to subtract is:
     - Sum of marginal costs of all units with cost $> \mu$.
     - Plus $(R - R_{high}) \times \mu$.
   - Sum of marginal costs of units with cost $> \mu$ for product $i$:
     - Let $k_i' = \lfloor \frac{\mu/P_i + 1}{2} \rfloor$. This is the number of units with cost $\le \mu$.
     - The units with cost $> \mu$ are indices $k_i'+1$ to $k_i$.
     - Their marginal costs are $P_i(2(k_i'+1)-1), \dots, P_i(2k_i-1)$.
     - Sum $= P_i \sum_{j=k_i'+1}^{k_i} (2j-1) = P_i (k_i^2 - (k_i')^2)$.
   - So, subtract $\sum_i P_i (k_i^2 - (k_i')^2) + (R - R_{high}) \mu$.

This approach is $O(N \log (\text{max\_cost}) \cdot \log (\text{max\_cost}))$ per check, and we do this for $\log (\text{max\_K})$ checks.
Total complexity: $O(N \log^2 M \log K)$. With $N=2 \cdot 10^5$, $\log M \approx 60$, $\log K \approx 40$. $2 \cdot 10^5 \cdot 3600 \cdot 40 \approx 2.8 \cdot 10^{10}$, too slow.

We need a faster check.
Notice that the function $S(\lambda)$ is monotonic.
We can find $\lambda^*$ in $O(N \log M)$.
Then we need to find $\mu$ in $O(N \log M)$.
Total per check: $O(N \log M)$.
Total overall: $O(N \log M \log K)$.
$2 \cdot 10^5 \cdot 60 \cdot 40 \approx 4.8 \cdot 10^8$. This is acceptable for 2 seconds in C++, maybe tight in Python.

Let's implement this.

## worker: Implement the solution in Python.
The problem asks for the maximum number of units $K$ that can be bought with total cost $\le M$. The cost function $\sum k_i^2 P_i$ is convex, so the minimum cost for a fixed $K$ is achieved when the marginal costs of adding the last unit to each product are as balanced as possible.

We binary search for the answer $K$ in the range $[0, 2 \cdot 10^{12}]$. The upper bound is derived from the worst-case scenario where all $P_i=1$, leading to $K \approx \sqrt{MN} \approx 4.5 \cdot 10^{11}$.

For a fixed $K$, we check if the minimum cost is $\le M$. This is done by:
1. Binary searching for a marginal cost threshold $\lambda$ such that the total number of units with marginal cost $\le \lambda$ is at least $K$. This gives us a set of candidate units.
2. If the total number of candidate units $S$ is greater than $K$, we need to remove $R = S - K$ units. These should be the ones with the highest marginal costs.
3. We binary search for a value $\mu$ to determine which units to remove. Specifically, we find the largest $\mu$ such that the number of selected units with marginal cost $> \mu$ is $\le R$.
4. We subtract the sum of the marginal costs of all units with cost $> \mu$, and then subtract $(R - \text{count}) \times \mu$ for the remaining units.
5. The marginal cost of the $j$-th unit of product $i$ is $P_i(2j-1)$. The sum of marginal costs for units from index $a$ to $b$ is $P_i(b^2 - (a-1)^2)$.

The complexity is $O(N \log M \log K)$, which is acceptable for $N=2 \cdot 10^5$.
