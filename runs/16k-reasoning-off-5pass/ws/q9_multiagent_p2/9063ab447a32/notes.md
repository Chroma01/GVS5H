
## ideation
**Core Difficulty**: The problem requires maximizing the total units bought under a budget $M$ with a non-linear cost function ($k^2 P_i$). The cost function is convex, meaning the marginal cost of buying the $k$-th unit of product $i$ is $(2k-1)P_i$, which increases with $k$. This suggests a greedy strategy: always buy the unit with the lowest current marginal cost. However, simulating this unit-by-unit is too slow ($M$ up to $10^{18}$ implies up to $10^9$ units).

**Candidate Approaches**:
1.  **Binary Search on Answer ($K$)**:
    *   We can binary search for the maximum total number of units $K$ we can buy. The range for $K$ is roughly $[0, 2 \cdot 10^9]$ (since min $P_i=1$ and $M=10^{18}$, max units $\approx \sqrt{10^{18}} = 10^9$).
    *   **Check Function (`can_buy(K)`)**: Given a target count $K$, find the minimum cost to buy exactly $K$ units.
        *   This sub-problem is also convex. We need to distribute $K$ units among products to minimize $\sum x_i^2 P_i$.
        *   The optimal distribution corresponds to a threshold marginal cost $V$. We buy all units with marginal cost $< V$, and some units with marginal cost $= V$.
        *   We can binary search for $V$ such that the total count of units with marginal cost $\le V$ is at least $K$.
        *   Once $V$ is found, calculate the exact cost: Sum of costs for all units with marginal cost $< V$, plus $(K - \text{count}_{<V}) \times V$.
        *   Compare this minimum cost with $M$.

2.  **Direct Binary Search on Marginal Cost Threshold**:
    *   Instead of binary searching $K$ then $V$, we can binary search directly on the marginal cost threshold $V$.
    *   For a fixed $V$, calculate the total units $S(V) = \sum \lfloor \frac{V + P_i}{2P_i} \rfloor$ and the total cost $C(V)$.
    *   We want the largest $V$ such that the cost to buy all units with marginal cost $\le V$ is $\le M$.
    *   Let this optimal threshold be $V_{opt}$. The total units will be $S(V_{opt})$. However, we might have "extra" units with marginal cost exactly $V_{opt}$ that we can't afford fully if we strictly follow the cost constraint, or rather, we can buy *all* units with marginal cost $< V_{opt}$, and then as many units with marginal cost $V_{opt}$ as the remaining budget allows.
    *   This approach seems more direct.
        *   Range for $V$: $[0, 2 \cdot 10^{18}]$ (since max marginal cost is roughly $2 \cdot 10^9 \cdot 2 \cdot 10^9 \approx 4 \cdot 10^{18}$).
        *   For a mid $V$:
            *   Calculate $count = \sum \lfloor \frac{V + P_i}{2P_i} \rfloor$.
            *   Calculate $cost = \sum \text{cost}(x_i)$ where $x_i = \lfloor \frac{V + P_i}{2P_i} \rfloor$.
            *   If $cost \le M$: This $V$ is achievable. We can potentially buy more units with marginal cost $V$. Specifically, we bought $count$ units. The "last" layer of units for each product has marginal cost $V$. We can buy up to $N$ such units (one per product type) if we increase the count? No, the marginal cost is constant $V$ for the specific unit index.
            *   Actually, if $cost \le M$, we can definitely buy $count$ units. Can we buy more? The next unit for product $i$ would have marginal cost $V + 2P_i > V$. So if we increase the count beyond $count$, the marginal cost jumps.
            *   Wait, the definition of $x_i = \lfloor \frac{V + P_i}{2P_i} \rfloor$ means the $x_i$-th unit has cost $(2x_i-1)P_i \le V$. The $(x_i+1)$-th unit has cost $(2x_i+1)P_i > V$.
            *   So if we find the largest $V$ such that the cost of buying all units with marginal cost $\le V$ is $\le M$, let this be $V^*$.
            *   Then we buy all units with marginal cost $< V^*$. Let this count be $C_{<}$.
            *   We have remaining budget $M - \text{cost}_{<}$.
            *   We can buy additional units with marginal cost $V^*$. How many? For each product $i$, the unit with marginal cost $V^*$ is available (since we included it in the $V^*$ check). Wait, if we include it in the sum for $V^*$, we already paid for it.
            *   Let's refine:
                1. Binary search for max $V$ such that Cost(units with marginal cost $\le V$) $\le M$.
                2. Let this max $V$ be $V_{max}$.
                3. Calculate total units bought with marginal cost $\le V_{max}$. Let this be $Total$.
                4. Is it possible to buy more? The next unit for any product has marginal cost $> V_{max}$. Since $V_{max}$ is the *maximum* threshold satisfying the budget, any unit with cost $> V_{max}$ would push the total cost over $M$ (assuming we already bought all $\le V_{max}$).
                5. Therefore, the answer is simply the count of units with marginal cost $\le V_{max}$.
                6. Wait, edge case: What if Cost(units $\le V_{max}$) $\le M$, but we could buy *some* units with cost $> V_{max}$? No, because if we could buy a unit with cost $C > V_{max}$, then the set of units with cost $\le C$ would also satisfy the budget (since $C$ is just one more unit), contradicting that $V_{max}$ is the maximum threshold.
                7. So the strategy is: Binary Search $V$. Find max $V$ where $\sum \text{cost}(x_i) \le M$ with $x_i = \lfloor \frac{V+P_i}{2P_i} \rfloor$. The answer is $\sum x_i$.

## worker: Implement the solution in Python using the "Binary
The problem asks to maximize the total number of units purchased given a budget $M$ and a cost function where buying $k$ units of product $i$ costs $k^2 P_i$. The marginal cost of the $k$-th unit of product $i$ is $(2k-1)P_i$. Since the marginal cost is increasing with $k$, the optimal strategy is to greedily purchase units with the lowest marginal costs.

This structure allows us to binary search on the marginal cost threshold $V$. If we set a threshold $V$, we can determine how many units of each product we can afford such that the marginal cost of the last unit purchased is $\le V$. Specifically, for product $i$, we buy $x_i = \lfloor \frac{V + P_i}{2P_i} \rfloor$ units. The total cost for this configuration is $\sum x_i^2 P_i$.

The algorithm proceeds as follows:
1.  **Binary Search for $V$**: We search for the maximum integer $V$ such that the total cost of buying all units with marginal cost $\le V$ is less than or equal to $M$. The range for $V$ is $[0, 2 \cdot 10^{18}]$.
2.  **Calculate Units**: Once the optimal $V$ (let's call it $V_{opt}$) is found, the maximum number of units we can buy is simply the sum of $x_i$ calculated using $V_{opt}$. This is because $V_{opt}$ is the largest threshold satisfying the budget, meaning we cannot afford any unit with marginal cost $> V_{opt}$ (otherwise the cost for the set including that unit would exceed $M$, or we could have increased $V$).
3.  **Complexity**: The binary search takes $O(\log(\text{MaxV}))$ steps. Inside each step, we iterate over $N$ products. Thus, the time complexity is $O(N \log(\text{MaxV}))$, which fits well within the limits ($N \le 2 \cdot 10^5$, MaxV $\approx 10^{18}$).

Edge cases handled:
-   $V < P_i$: The formula correctly yields 0 units.
-   Large $M$: Python handles arbitrarily large integers, so overflow is not an issue.
-   $M$ is small: The binary search will naturally converge to a small $V$.

## worker: Run the code against the provided sample inputs to
The solution implements a binary search on the marginal cost threshold $V$.
1.  **Problem Analysis**: The cost function $k^2 P_i$ is convex. The marginal cost of the $k$-th unit is $(2k-1)P_i$. To maximize units for a budget $M$, we should greedily pick units with the lowest marginal costs.
2.  **Binary Search Strategy**: Instead of simulating the greedy process (which is too slow for $M=10^{18}$), we binary search for the maximum marginal cost $V$ such that the total cost of buying all units with marginal cost $\le V$ is $\le M$.
3.  **Check Function**: For a candidate $V$, the number of units $x_i$ of product $i$ satisfying $(2x_i-1)P_i \le V$ is $x_i = \lfloor \frac{V+P_i}{2P_i} \rfloor$. The total cost is $\sum x_i^2 P_i$. If this sum is $\le M$, $V$ is feasible.
4.  **Complexity**: The binary search runs in $O(\log(\text{MaxV}))$ steps. Each step iterates over $N$ products. Total time complexity is $O(N \log M)$, which fits within the time limit for $N=2 \cdot 10^5$ and $M=10^{18}$.
5.  **Correctness**: The optimal solution corresponds to buying all units with marginal cost strictly less than some threshold $V^*$, and some units with marginal cost equal to $V^*$. The binary search finds the largest $V$ where the cost of *all* units with marginal cost $\le V$ is within budget. Since the cost function is strictly increasing with the number of units, if we can afford all units $\le V$, we can definitely afford the subset of those units. The count of units for this $V$ is the maximum possible because any unit with marginal cost $> V$ would require increasing the threshold, which we proved is not possible within budget $M$.

## worker: Run the provided sample inputs to verify correctne
The solution implements a binary search on the marginal cost threshold $V$.
1.  **Problem Analysis**: The cost function $k^2 P_i$ is convex. The marginal cost of the $k$-th unit of product $i$ is $(2k-1)P_i$. To maximize units for a budget $M$, we should greedily pick units with the lowest marginal costs.
2.  **Binary Search Strategy**: Instead of simulating the greedy process (which is too slow for $M=10^{18}$), we binary search for the maximum marginal cost $V$ such that the total cost of buying all units with marginal cost $\le V$ is $\le M$.
3.  **Check Function**: For a candidate $V$, the number of units $x_i$ of product $i$ satisfying $(2x_i-1)P_i \le V$ is $x_i = \lfloor \frac{V+P_i}{2P_i} \rfloor$. The total cost is $\sum x_i^2 P_i$. If this sum is $\le M$, $V$ is feasible.
4.  **Complexity**: The binary search runs in $O(\log(\text{MaxV}))$ steps. Each step iterates over $N$ products. Total time complexity is $O(N \log M)$, which fits within the time limit for $N=2 \cdot 10^5$ and $M=10^{18}$.
5.  **Correctness**: The optimal solution corresponds to buying all units with marginal cost strictly less than some threshold $V^*$, and some units with marginal cost equal to $V^*$. The binary search finds the largest $V$ where the cost of *all* units with marginal cost $\le V$ is within budget. Since the cost function is strictly increasing with the number of units, if we can afford all units $\le V$, we can definitely afford the subset of those units. The count of units for this $V$ is the maximum possible because any unit with marginal cost $> V$ would require increasing the threshold, which we proved is not possible within budget $M$.

## worker: finalize
The solution uses a binary search on the marginal cost threshold $V$.
1.  **Marginal Cost Analysis**: The cost function $k^2 P_i$ is convex. The marginal cost of the $k$-th unit is $(2k-1)P_i$. To maximize units for a fixed budget, we should greedily pick units with the lowest marginal costs.
2.  **Binary Search on $V$**: Instead of simulating the greedy process (which is too slow for $M=10^{18}$), we binary search for the maximum integer $V$ such that the total cost of buying *all* units with marginal cost $\le V$ is $\le M$.
3.  **Check Function**: For a candidate $V$, the number of units $x_i$ of product $i$ satisfying $(2x_i-1)P_i \le V$ is $x_i = \lfloor \frac{V+P_i}{2P_i} \rfloor$. The total cost is $\sum x_i^2 P_i$. If this sum is $\le M$, $V$ is feasible.
4.  **Complexity**: The binary search runs in $O(\log(\text{MaxV}))$ steps. Each step iterates over $N$ products. Total time complexity is $O(N \log M)$, which fits within the time limit for $N=2 \cdot 10^5$ and $M=10^{18}$.
5.  **Correctness**: The optimal solution corresponds to buying all units with marginal cost strictly less than some threshold $V^*$, and some units with marginal cost equal to $V^*$. The binary search finds the largest $V$ where the cost of *all* units with marginal cost $\le V$ is within budget. Since the cost function is strictly increasing with the number of units, if we can afford all units $\le V$, we can definitely afford the subset of those units. The count of units for this $V$ is the maximum possible because any unit with marginal cost $> V$ would require increasing the threshold, which we proved is not possible within budget $M$.
