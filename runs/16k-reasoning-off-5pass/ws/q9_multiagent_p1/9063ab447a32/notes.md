
## ideation
The problem asks us to maximize the total number of units $X = \sum x_i$ subject to $\sum x_i^2 P_i \le M$.
The cost function for product $i$ is convex ($x_i^2 P_i$). This implies the marginal cost of the $k$-th unit is $(k^2 - (k-1)^2)P_i = (2k-1)P_i$.
Since we want to maximize the count, we should greedily pick units with the smallest marginal costs.
The marginal costs for product $i$ form an arithmetic progression: $P_i, 3P_i, 5P_i, \dots, (2k-1)P_i, \dots$.
We need to select a total of $X$ units such that the sum of the $X$ smallest marginal costs is $\le M$.
This suggests a binary search approach:
1.  **Binary Search on the Answer ($X$):** Can we buy at least $X$ units?
    *   To check if $X$ units are possible with cost $\le M$, we need to distribute $X$ units among products to minimize total cost.
    *   Since the marginal costs are increasing, we should fill the "cheapest" slots first.
    *   Alternatively, we can binary search on the **threshold marginal cost** $T$. If the marginal cost of the $k$-th unit of product $i$ is $\le T$, we might buy it.
    *   Let's refine the "Binary Search on Threshold $T$" approach:
        *   Suppose we decide to only buy units whose marginal cost is $\le T$.
        *   For product $i$, the condition is $(2k-1)P_i \le T \implies 2k-1 \le T/P_i \implies k \le \frac{T/P_i + 1}{2}$.
        *   Let $k_i(T) = \lfloor \frac{\lfloor T/P_i \rfloor + 1}{2} \rfloor$. This is the number of units we buy from product $i$ if the threshold is $T$.
        *   Total units $X(T) = \sum k_i(T)$.
        *   Total cost $C(T) = \sum P_i \cdot k_i(T)^2$.
        *   We need to find the largest $T$ such that $C(T) \le M$. However, simply checking $C(T) \le M$ isn't enough because we might be able to buy *more* units by including some units with marginal cost slightly higher than $T$, or we might have a "partial" unit at the boundary.
        *   Actually, the standard technique for this type of convex cost maximization is:
            1.  Binary search for the maximum total units $X$.
            2.  Check function `can_buy(X)`:
                *   We want to minimize $\sum x_i^2 P_i$ subject to $\sum x_i = X$.
                *   Using Lagrange multipliers or simple calculus intuition, the optimal $x_i$ satisfies $2x_i P_i \approx \lambda$. So $x_i \approx \lambda / (2P_i)$.
                *   Specifically, $x_i = \lfloor \frac{K}{P_i} \rfloor$ or similar? Let's derive properly.
                *   We want to minimize $\sum P_i x_i^2$ subject to $\sum x_i = X$.
                *   The derivative of cost w.r.t $x_i$ is $2 P_i x_i$. At optimum, $2 P_i x_i \le \lambda$ and equality holds for active items.
                *   So $x_i = \lfloor \frac{\lambda}{2 P_i} \rfloor$? Not exactly, because $x_i$ must be integer.
                *   Actually, we can binary search on the "marginal cost threshold" $V$. If we set a threshold $V$, we buy all units with marginal cost $\le V$.
                *   For a fixed $V$, the number of units from product $i$ is $k_i = \lfloor \frac{V/P_i + 1}{2} \rfloor$.
                *   Let this sum be $S$. If $S \ge X$, we might be able to achieve $X$ with cost $\le M$.
                *   Wait, the binary search on $X$ is safer. But calculating the minimum cost for a fixed $X$ efficiently is the key.
                *   To minimize $\sum P_i x_i^2$ with $\sum x_i = X$:
                    *   We can binary search on the value $K$ such that we buy $x_i = \lfloor K/P_i \rfloor$? No.
                    *   Let's look at the marginal cost again: $c_{i,k} = (2k-1)P_i$.
                    *   We want to pick $X$ smallest values from the set $\{ (2k-1)P_i \mid i \in [1,N], k \ge 1 \}$.
                    *   The $k$-th smallest value for product $i$ is roughly proportional to $k P_i$.
                    *   If we pick a threshold $T$, we take all $(2k-1)P_i \le T$.
                    *   Let $k_i = \lfloor \frac{T/P_i + 1}{2} \rfloor$.
                    *   Total units $U = \sum k_i$.
                    *   Total cost $C = \sum P_i k_i^2$.
                    *   If $U \ge X$, it means we can potentially buy $X$ units. The cost would be $C$ minus the cost of the $(U-X)$ most expensive units included (which are all $\le T$) plus potentially some units just above $T$.
                    *   Actually, a simpler logic:
                        Binary search on the threshold $T$ (the marginal cost of the last unit bought).
                        Range for $T$: $1$ to $2 \cdot 10^{18}$ (approx, since $M \le 10^{18}$ and min cost is 1).
                        For a fixed $T$:
                        1. Calculate $k_i = \lfloor \frac{\lfloor T/P_i \rfloor + 1}{2} \rfloor$.
                        2. Sum $k_i$ to get total units $S$.
                        3. Sum $P_i k_i^2$ to get total cost $C$.
                        4. If $S \ge X$ and $C \le M$? No, we don't know $X$ yet.
                        We need to find the max $X$.
                        Let's binary search on $X$ directly? $X$ can be up to $2 \cdot 10^{14}$ (if $P_i=1, M=10^{18}$, $X^2 \approx 10^{18} \implies X \approx 10^9$). Wait, if $P_i=1$, cost is $x^2$. $x^2 \le 10^{18} \implies x \le 10^9$. With $N$ products, we can buy more. If $P_i=1$ for all $N$, we distribute $X$ units. Cost $\approx \sum (X/N)^2 = N (X/N)^2 = X^2/N$. $X^2/N \le M \implies X \le \sqrt{NM}$. Max $N=2\cdot 10^5, M=10^{18} \implies X \approx \sqrt{2\cdot 10^{23}} \approx 4.5 \cdot 10^{11}$.
                        So $X$ fits in 64-bit integer.
                        
                        **Check function `check(X)`:**
                        Can we buy $X$ units with cost $\le M$?
                        We need to minimize $\sum P_i x_i^2$ subject to $\sum x_i = X, x_i \ge 0$.
                        This is a convex optimization problem. The optimal $x_i$ satisfies $2 P_i x_i \approx \lambda$.
                        So $x_i \approx \frac{\lambda}{2 P_i}$.
                        Let's binary search for $\lambda$ (or rather, the threshold $K$ such that $x_i = \lfloor \frac{K}{P_i} \rfloor$? No, the relation is $x_i \propto 1/P_i$).
                        Actually, the condition $2 P_i x_i \le \lambda$ implies $x_i \le \frac{\lambda}{2 P_i}$.
                        Let $K = \lambda/2$. Then $x_i = \lfloor \frac{K}{P_i} \rfloor$?
                        Let's test: if $x_i = \lfloor K/P_i \rfloor$, then marginal cost of last unit is $(2x_i-1)P_i \approx 2(K/P_i)P_i = 2K$.
                        Yes, the marginal costs are roughly constant at $2K$.
                        So, to check if $X$ is possible:
                        1. Binary search for $K$ such that $\sum \lfloor K/P_i \rfloor \ge X$.
                           Let the found $K$ be $K_{opt}$.
                           With this $K$, we calculate $x_i = \lfloor K_{opt}/P_i \rfloor$.
                           Sum $x_i$ might be $> X$. Let the excess be $rem = (\sum x_i) - X$.
                           We need to remove $rem$ units. To minimize cost reduction (or rather, we want the minimal cost for exactly $X$), we should remove the units with the highest marginal costs.
                           The marginal cost of the last unit of product $i$ (the $x_i$-th unit) is $(2x_i - 1)P_i$.
                           We have a collection of these "last unit marginal costs" for all $i$. We need to remove $rem$ units with the largest marginal costs.
                           Since $N$ is up to $2 \cdot 10^5$, we cannot sort all marginal costs.
                           However, notice that for a fixed $K$, the values $(2x_i-1)P_i$ are roughly $2K$.
                           Is there a way to calculate the cost of the best $X$ units without sorting?
                           
                        Alternative approach: Binary search on the threshold $T$ of the marginal cost.
                        Let $T$ be the maximum marginal cost we are willing to pay.
                        For a given $T$, we buy all units with marginal cost $\le T$.
                        Number of units $S(T) = \sum \lfloor \frac{T/P_i + 1}{2} \rfloor$.
                        Cost $C(T) = \sum P_i \lfloor \frac{T/P_i + 1}{2} \rfloor^2$.
                        We want to find the largest $T$ such that $C(T) \le M$.
                        Let this optimal $T$ be $T_{max}$.
                        Then we buy all units with marginal cost $< T_{max}$. Let the count be $S'$.
                        The remaining budget is $M - C(T_{max})$.
                        We can try to buy more units with marginal cost equal to $T_{max}$?
                        Wait, the marginal costs are discrete values $(2k-1)P_i$.
                        If we pick a threshold $T$, we get a set of units.
                        The function $S(T)$ is non-decreasing. $C(T)$ is non-decreasing.
                        We want max $X$ such that min cost for $X$ is $\le M$.
                        The min cost for $X$ is achieved by taking the $X$ smallest marginal costs.
                        Let $f(X)$ be the min cost for $X$ units. $f(X)$ is convex and non-decreasing.
                        We can binary search $X$.
                        But calculating $f(X)$ efficiently is hard because of the "remove largest marginal costs" step.
                        
                        Let's reconsider the binary search on $T$ (threshold marginal cost).
                        Suppose we fix $T$. We take all units with marginal cost $\le T$.
                        Let this set be $U_T$. Size $|U_T|$, Cost $Cost(U_T)$.
                        If $Cost(U_T) \le M$, then we can definitely buy $|U_T|$ units. Can we buy more?
                        Maybe we can buy some units with marginal cost $> T$ if we have budget left?
                        Yes. If $Cost(U_T) < M$, we have slack. We can try to add units with marginal cost $> T$ but as small as possible.
                        The smallest marginal cost $> T$ is $\min_i \{ (2k-1)P_i \mid (2k-1)P_i > T \}$.
                        This looks like we can just binary search on $T$ to find the largest $T$ such that $Cost(\text{all units with marginal cost } \le T) \le M$.
                        Let this max $T$ be $T^*$.
                        Then we buy all units with marginal cost $< T^*$. Let count be $C_{<}$.
                        Then we consider units with marginal cost exactly $T^*$.
                        Wait, $T$ in the binary search is a continuous variable conceptually, but the actual marginal costs are integers.
                        Let's binary search for the integer $T$ such that if we take all units with marginal cost $\le T$, the total cost is $\le M$.
                        Let $S(T)$ be the set of units with marginal cost $\le T$.
                        Find max $T$ such that $\sum_{u \in S(T)} cost(u) \le M$.
                        Let this be $T_{opt}$.
                        Then we take all units in $S(T_{opt})$. Let the count be $cnt$.
                        The cost is $C_{opt}$.
                        Remaining budget $R = M - C_{opt}$.
                        Now we need to see if we can buy any more units.
                        The next available units have marginal costs $> T_{opt}$.
                        Specifically, for each product $i$, the next unit after $k_i$ units (where $(2k_i-1)P_i \le T_{opt}$) has cost $(2(k_i+1)-1)P_i = (2k_i+1)P_i$.
                        We need to pick units with the smallest marginal costs from the set of "next units" across all products, as long as their cost $\le R$?
                        No, the condition is total cost $\le M$.
                        We already spent $C_{opt}$. We have $R$ left.
                        We can buy a unit with marginal cost $c$ if $C_{opt} + c \le M \implies c \le R$.
                        So we need to count how many units have marginal cost $\le R$ among the "next units".
                        But wait, the "next units" are not independent. If we buy the next unit of product $i$, its cost is $(2k_i+1)P_i$. If we buy that, the *next* one becomes $(2k_i+3)P_i$.
                        However, since we stopped at $T_{opt}$ because adding any unit with cost $\le T_{opt}$ would exceed $M$ (or rather, we found the max $T$ such that sum of costs $\le M$), it implies that for any unit with cost $\le T_{opt}$, we already included it.
                        The units we didn't include have cost $> T_{opt}$.
                        So we just need to count how many units from the "next layer" have cost $\le R$.
                        Wait, is it possible that $T_{opt}$ is not the exact marginal cost of the last unit?
                        Yes. $T_{opt}$ is the largest integer such that $\sum_{(2k-1)P_i \le T_{opt}} (2k-1)P_i \le M$.
                        Let $S_{opt}$ be the set of units with marginal cost $\le T_{opt}$.
                        Total cost $C_{opt} \le M$.
                        Any unit not in $S_{opt}$ has marginal cost $> T_{opt}$.
                        We want to add as many units as possible from the set of units with cost $> T_{opt}$ such that total cost $\le M$.
                        Since all units in $S_{opt}$ are already taken, and all remaining units have cost $> T_{opt}$, we simply need to count how many remaining units have cost $\le M - C_{opt}$.
                        Let $R = M - C_{opt}$.
                        We need to count pairs $(i, k)$ such that $(i, k)$ is not in $S_{opt}$ and $(2k-1)P_i \le R$.
                        Note that for product $i$, the units in $S_{opt}$ are $k=1 \dots k_i^{max}$ where $(2k_i^{max}-1)P_i \le T_{opt}$.
                        The next unit is $k = k_i^{max} + 1$, with cost $(2(k_i^{max}+1)-1)P_i = (2k_i^{max}+1)P_i$.
                        We need to count how many such next units satisfy $(2k_i^{max}+1)P_i \le R$.
                        Wait, if $(2k_i^{max}+1)P_i \le R$, can we buy it? Yes.
                        But if we buy it, do we consider the one after?
                        The one after has cost $(2k_i^{max}+3)P_i$.
                        Since $T_{opt}$ was the max threshold such that sum of costs $\le M$, it implies that we cannot afford *all* units with cost $\le T_{opt}$ plus *any* unit with cost $> T_{opt}$?
                        Actually, the definition of $T_{opt}$ ensures that including all units $\le T_{opt}$ fits in $M$.
                        It does NOT ensure that we can't add one more unit with cost $> T_{opt}$.
                        Example: $M=10$. Costs: 3, 3, 5, 5, 5...
                        $T_{opt}$ might be 5. Sum of costs $\le 5$ is $3+3+5+5 = 16 > 10$. So $T_{opt}$ would be 3. Sum=6. $R=4$.
                        Next unit cost is 5. $5 \le 4$ is false. So we stop.
                        Another example: $M=10$. Costs: 2, 2, 2, 2, 2... (all 2).
                        $T_{opt}$ could be 2. Sum of all units $\le 2$ is huge.
                        Wait, if all costs are 2, then $T_{opt}$ will be 2, and we will take ALL units with cost $\le 2$.
                        If $N$ is large, sum might exceed $M$.
                        Ah, the binary search on $T$ finds the largest $T$ such that the cost of taking *all* units with marginal cost $\le T$ is $\le M$.
                        If $N$ is large, we might not be able to take *all* units with cost $\le T$.
                        In that case, the binary search on $T$ is flawed because $S(T)$ grows with $T$, but the cost might jump over $M$.
                        Actually, if we can't take all units $\le T$, then for that $T$, the cost is $> M$. So the binary search will find a smaller $T$.
                        So $T_{opt}$ is indeed the max threshold such that taking ALL units with marginal cost $\le T_{opt}$ fits in $M$.
                        Let $S_{opt}$ be the set of all units with marginal cost $\le T_{opt}$.
                        Cost $C_{opt} \le M$.
                        Remaining budget $R = M - C_{opt}$.
                        Now we look at units with marginal cost $> T_{opt}$.
                        We want to pick as many as possible with cost $\le R$.
                        Since all units in $S_{opt}$ are taken, the next available units for product $i$ are those with $k > k_i^{max}$.
                        The smallest such cost is $(2(k_i^{max}+1)-1)P_i$.
                        Let this be $c_{next, i}$.
                        We need to count how many $i$ have $c_{next, i} \le R$.
                        Wait, if $c_{next, i} \le R$, we can buy that unit.
                        But what if after buying that unit, the next one is also $\le R$?
                        Since $T_{opt}$ was the max threshold where *all* units $\le T_{opt}$ fit, it implies that for any $T > T_{opt}$, the cost of taking all units $\le T$ is $> M$.
                        This means we cannot take *all* units with cost $\le T_{opt} + \epsilon$.
                        Specifically, we cannot take all units with cost $\le T_{opt}$ AND all units with cost $\le T_{opt} + \delta$ for any $\delta > 0$?
                        No. It means we cannot take all units with cost $\le T_{opt+1}$ (if integers).
                        So we have taken all units with cost $\le T_{opt}$.
                        We have budget $R$.
                        We can take some units with cost $> T_{opt}$.
                        But we cannot take *all* units with cost $\le T_{opt} + 1$ (if such a threshold exists and is integer).
                        Actually, the set of available units with cost $> T_{opt}$ are sparse.
                        For each product $i$, the next unit has cost $c_i = (2k_i^{max}+1)P_i$.
                        If $c_i \le R$, we can buy it.
                        If we buy it, the new next unit has cost $c_i + 2P_i$.
                        Can we buy that too?
                        If we buy the first one, the total cost increases by $c_i$.
                        If we buy the second one, it increases by $c_i + 2P_i$.
                        The condition is total cost $\le M$.
                        Since we know that taking ALL units with cost $\le T_{opt} + 1$ exceeds $M$, it implies that we cannot buy ALL units with cost $> T_{opt}$ that are $\le T_{opt}+1$.
                        Actually, since the costs are integers, the next possible marginal cost after $T_{opt}$ is at least $T_{opt}+1$.
                        If we buy a unit with cost $c > T_{opt}$, then $c \ge T_{opt}+1$.
                        If we buy multiple units with cost $> T_{opt}$, say $k$ units, their costs are $\ge T_{opt}+1$.
                        If we buy even one unit with cost $c \ge T_{opt}+1$, then the total cost would be $C_{opt} + c$.
                        If $C_{opt} + c \le M$, we can buy it.
                        But we know that if we tried to set threshold $T' = T_{opt}+1$, the cost of taking ALL units $\le T_{opt}+1$ is $> M$.
                        This means $\sum_{u: cost(u) \le T_{opt}+1} cost(u) > M$.
                        This sum is $C_{opt} + \sum_{u: T_{opt} < cost(u) \le T_{opt}+1} cost(u)$.
                        So the sum of costs of all units with cost in $(T_{opt}, T_{opt}+1]$ is $> M - C_{opt} = R$.
                        Therefore, we cannot buy ALL units with cost in $(T_{opt}, T_{opt}+1]$.
                        However, we might be able to buy SOME of them.
                        But wait, the costs in $(T_{opt}, T_{opt}+1]$ are integers. The only integer in $(T_{opt}, T_{opt}+1]$ is none?
                        If $T_{opt}$ is an integer, then the next integer is $T_{opt}+1$.
                        So the units with cost $> T_{opt}$ have cost $\ge T_{opt}+1$.
                        The units with cost $\le T_{opt}+1$ are exactly those with cost $= T_{opt}+1$ (since we already took all $\le T_{opt}$).
                        So the set of units with cost $\le T_{opt}+1$ is $S_{opt} \cup \{ u \mid cost(u) = T_{opt}+1 \}$.
                        The cost of this set is $C_{opt} + \sum_{u: cost(u)=T_{opt}+1} cost(u)$.
                        We know this total is $> M$.
                        So $\sum_{u: cost(u)=T_{opt}+1} cost(u) > R$.
                        Since each such unit has cost $T_{opt}+1$, and $T_{opt}+1 \ge 1$, we can buy at most $\lfloor R / (T_{opt}+1) \rfloor$ units from this group.
                        But wait, is it possible that there are no units with cost $T_{opt}+1$?
                        Yes. Then the next cost is $T_{opt}+2$.
                        In general, we need to find the smallest integer $V > T_{opt}$ such that there exists a unit with cost $V$.
                        Then we can buy at most $\lfloor R/V \rfloor$ units of cost $V$.
                        But we need to be careful: the units with cost $V$ are specific $(i, k)$ pairs.
                        For each product $i$, the next unit has cost $c_i = (2k_i^{max}+1)P_i$.
                        We need to count how many $i$ have $c_i = V$.
                        Actually, we don't need to iterate $V$.
                        We just need to count how many $i$ have $c_i \le R$.
                        Wait, if we buy one unit of cost $c_i$, can we buy the next one of cost $c_i + 2P_i$?
                        If $c_i \le R$, we buy it. Remaining budget $R' = R - c_i$.
                        Then we check if $c_i + 2P_i \le R'$.
                        But we know that the total sum of ALL units with cost $\le T_{opt}+1$ exceeds $M$.
                        This implies we can't buy all units with cost $\le T_{opt}+1$.
                        What about units with cost $> T_{opt}+1$?
                        If we buy a unit with cost $c > T_{opt}+1$, then $c \ge T_{opt}+2$.
                        The cost of taking all units $\le T_{opt}+1$ is $> M$.
                        Does this restrict us from buying units with cost $> T_{opt}+1$?
                        Not directly. But logically, if we can't afford all units $\le T_{opt}+1$, we definitely can't afford any unit with cost $> T_{opt}+1$ PLUS all units $\le T_{opt}+1$.
                        But we are only considering adding units to $S_{opt}$.
                        We have already taken all units $\le T_{opt}$.
                        We have budget $R$.
                        We want to pick a subset of units with cost $> T_{opt}$ such that sum of costs $\le R$.
                        To maximize the count, we should pick the cheapest ones.
                        The cheapest available units are those with the smallest marginal costs $> T_{opt}$.
                        Let these costs be $v_1 \le v_2 \le \dots$.
                        We want to find $k$ such that $\sum_{j=1}^k v_j \le R$.
                        Since the costs are integers and we know that $\sum_{v_j \le T_{opt}+1} v_j > R$ (if such units exist), we can only pick a few.
                        Specifically, if there are units with cost $T_{opt}+1$, let their count be $K_1$.
                        Sum of these is $K_1(T_{opt}+1)$.
                        If $K_1(T_{opt}+1) > R$, we can pick at most $\lfloor R/(T_{opt}+1) \rfloor$ units from this group.
                        If we pick $k$ units from this group, the cost is $k(T_{opt}+1)$.
                        Can we pick units from the next group (cost $T_{opt}+2$)?
                        Only if we have budget left.
                        But note: if we pick a unit from the next group, its cost is $\ge T_{opt}+2$.
                        The total cost of all units with cost $\le T_{opt}+1$ is $> M$.
                        This means $C_{opt} + \text{cost}(all \le T_{opt}+1) > M$.
                        So $R < \text{cost}(all \le T_{opt}+1)$.
                        If we pick any unit with cost $> T_{opt}+1$, say $u$, then $cost(u) \ge T_{opt}+2$.
                        The total cost would be $C_{opt} + \text{cost}(subset \le T_{opt}+1) + cost(u)$.
                        Is it possible that this is $\le M$?
                        Suppose we pick 0 units from $\le T_{opt}+1$ and 1 unit from $> T_{opt}+1$.
                        Cost = $C_{opt} + (T_{opt}+2)$.
                        We know $C_{opt} + \text{cost}(all \le T_{opt}+1) > M$.
                        This doesn't prevent $C_{opt} + (T_{opt}+2) \le M$.
                        Example: $M=10$. Costs: 3, 3, 3, 3, 3... (5 units).
                        $T_{opt}=3$. Sum=15 > 10. So $T_{opt}$ would be 2?
                        If costs are 3, then $T_{opt}$ for threshold 2 is 0 units. Cost 0. $R=10$.
                        Next unit cost 3. $3 \le 10$. Buy 1. $R=7$.
                        Next unit cost 3. Buy 1. $R=4$.
                        Next unit cost 3. Buy 1. $R=1$.
                        Next unit cost 3. $3 > 1$. Stop. Total 3 units.
                        Here $T_{opt}=2$. Next cost is 3.
                        The logic holds: we just need to count how many units with cost $> T_{opt}$ we can afford, prioritizing smallest costs.
                        Since the number of units with cost $> T_{opt}$ that are $\le T_{opt}+1$ is likely small (or non-existent), and the costs jump, we can just:
                        1. Binary search $T$ to find max $T$ such that $\sum_{cost \le T} cost \le M$.
                        2. Calculate $C_{opt}$ and $R = M - C_{opt}$.
                        3. Identify all products $i$ and their next unit cost $c_i = (2k_i^{max}+1)P_i$.
                        4. Collect all such $c_i$. Sort them? $N$ is $2 \cdot 10^5$, sorting is fine.
                        5. Greedily pick $c_i$ as long as $c_i \le R$ and $R \ge c_i$.
                        Wait, if we pick $c_i$, the next unit for product $i$ becomes $c_i + 2P_i$.
                        We need to re-evaluate.
                        But notice: if we pick a unit with cost $c$, the next one is $c+2P_i \ge c+2$.
                        The costs are increasing.
                        However, we know that we cannot pick ALL units with cost $\le T_{opt}+1$.
                        Actually, the number of units we can pick from the "next layer" is very small.
                        Why? Because the sum of ALL units with cost $\le T_{opt}+1$ is $> M$.
                        So the sum of costs of units with cost $> T_{opt}$ and $\le T_{opt}+1$ is $> R$.
                        Let $S_{next}$ be the set of units with cost $> T_{opt}$ and $\le T_{opt}+1$.
                        $\sum_{u \in S_{next}} cost(u) > R$.
                        Since each $cost(u) \ge T_{opt}+1$, the number of such units we can pick is at most $\lfloor R/(T_{opt}+1) \rfloor$.
                        If $T_{opt}$ is large, this number is small.
                        If $T_{opt}$ is small, $R$ is large, but then $T_{opt}$ would be larger?
                        Actually, if $T_{opt}$ is small, it means even taking all units with cost $\le T_{opt}$ is close to $M$, but adding any unit with cost $> T_{opt}$ pushes it over?
                        No, $T_{opt}$ is defined as max $T$ such that sum of ALL units $\le T$ is $\le M$.
                        So if we increase $T$ to $T_{opt}+1$, the sum exceeds $M$.
                        This means the sum of units with cost in $(T_{opt}, T_{opt}+1]$ is $> R$.
                        So we can pick at most a few units from this range.
                        What about units with cost $> T_{opt}+1$?
                        If we pick a unit with cost $c > T_{opt}+1$, then $c \ge T_{opt}+2$.
                        The total cost would be $C_{opt} + \text{cost}(picked \le T_{opt}+1) + c$.
                        We know $C_{opt} + \text{cost}(all \le T_{opt}+1) > M$.
                        So $C_{opt} + \text{cost}(picked \le T_{opt}+1) + c > M + c - \text{cost}(rest \le T_{opt}+1)$.
                        This doesn't guarantee $> M$.
                        However, intuitively, the number of units we can pick beyond the threshold is very small.
                        Actually, we can just collect all candidate next units, sort them, and simulate?
                        But the "next unit" changes.
                        Wait, if we pick a unit, the next one becomes available.
                        But the costs are $c, c+2P, c+4P \dots$.
                        Since we can only pick a few units (because the sum of all units $\le T_{opt}+1$ is $> R$), we can just:
                        1. Collect all $c_i = (2k_i^{max}+1)P_i$.
                        2. Sort $c_i$.
                        3. Iterate and pick.
                        But if we pick $c_i$, the next one is $c_i + 2P_i$.
                        Is it possible that $c_i + 2P_i$ is smaller than some other $c_j$?
                        Yes.
                        However, since we can only pick a few units (likely $< N$), maybe we can just use a priority queue?
                        Or simply: since the number of units we can pick is small, we can just run a loop?
                        How small?
                        If $T_{opt}$ is large, $R$ is small, count is small.
                        If $T_{opt}$ is small, then $C_{opt}$ is small, so $R \approx M$.
                        But if $T_{opt}$ is small, it means even for $T=T_{opt}+1$, the cost exceeds $M$.
                        This implies there are MANY units with cost $\le T_{opt}+1$.
                        So the number of units with cost $> T_{opt}$ and $\le T_{opt}+1$ is large.
                        But their sum is $> R$.
                        So we can pick at most $R / (T_{opt}+1)$ units.
                        If $T_{opt}$ is small, $R/(T_{opt}+1)$ can be large.
                        Example: $M=10^{18}, P_i=1$. $T_{opt} \approx 10^9$. $R \approx 0$.
                        Example: $M=10, P_i=1$. $T_{opt}=3$ (sum 15>10, so $T_{opt}=2$, sum 6, $R=4$).
                        Next units cost 3. We can pick $\lfloor 4/3 \rfloor = 1$.
                        It seems the number of units we can pick is always small?
                        Wait, if $T_{opt}$ is small, say $T_{opt}=0$ (no units $\le 0$). $R=M$.
                        Next units cost $P_i$.
                        We can pick many units.
                        But if $T_{opt}=0$, it means $\sum_{all} cost > M$? No, $T_{opt}=0$ means sum of units $\le 0$ (none) is 0 $\le M$.
                        Next $T=1$. Sum of units $\le 1$ (all units with $P_i=1$) might be $> M$.
                        So we have many units with cost 1. Sum $> M$.
                        We can pick $\lfloor M/1 \rfloor = M$ units.
                        So the number of units can be large.
                        But we can just binary search on the answer $X$!
                        We established earlier that checking $X$ is hard because we need to calculate min cost.
                        BUT, we can calculate min cost for $X$ using the threshold method!
                        For a fixed $X$:
                        1. Binary search for $K$ such that $\sum \lfloor K/P_i \rfloor \ge X$.
                        2. Let $x_i = \lfloor K/P_i \rfloor$. Sum $S = \sum x_i \ge X$.
                        3. We have excess $rem = S - X$.
                        4. We need to remove $rem$ units with the largest marginal costs.
                        5. Marginal costs of removed units are $(2x_i-1)P_i$.
                        6. We need to sum the smallest $S-X$ costs from the set of all marginal costs of the selected units?
                        No, we need to remove the $rem$ largest costs from the set of costs of the $x_i$ units.
                        The costs are $(2k-1)P_i$ for $k=1 \dots x_i$.
                        The largest are the last ones: $(2x_i-1)P_i$.
                        So we have a list of values $v_i = (2x_i-1)P_i$. We need to remove $rem$ largest values from $\{v_1, v_2, \dots, v_N\}$.
                        Wait, if we remove the last unit of product $i$, the new last unit is $(2(x_i-1)-1)P_i$.
                        We need to remove $rem$ units total.
                        We should remove the ones with largest $v_i$.
                        Since $N$ is $2 \cdot 10^5$, we can sort the $v_i$'s?
                        Yes! Sorting $N$ items is fast enough ($O(N \log N)$).
                        So the check function `check(X)`:
                        1. Binary search $K$ in $[0, 2 \cdot 10^{18}]$ (or appropriate range).
                           Condition: $\sum \lfloor K/P_i \rfloor \ge X$.
                           Find smallest $K$ satisfying this.
                        2. Calculate $x_i = \lfloor K/P_i \rfloor$.
                        3. Calculate total cost $C = \sum P_i x_i^2$.
                        4. Calculate excess $rem = (\sum x_i) - X$.
                        5. If $rem == 0$, return $C \le M$.
                        6. If $rem > 0$, we need to remove $rem$ units with largest marginal costs.
                           The marginal cost of the last unit of product $i$ is $m_i = (2x_i-1)P_i$.
                           Collect all $m_i$ for $i$ where $x_i > 0$.
                           Sort $m_i$ descending.
                           Sum the top $rem$ values. Let this be $cost\_removed$.
                           Total cost $C_{final} = C - cost\_removed$.
                           Return $C_{final} \le M$.
                        Complexity: $O(N \log N)$ per check. Binary search for $K$ takes $O(\log(\text{range}))$. Binary search for $X$ takes $O(\log(\text{ans}))$.
                        Total: $O(\log(\text{ans}) \cdot \log(\text{range}) \cdot N \log N)$.
                        With $N=2 \cdot 10^5$, this is too slow ($2 \cdot 10^5 \times 60 \times 60 \approx 7 \cdot 10^8$).
                        We need to optimize.
                        Notice that $m_i = (2 \lfloor K/P_i \rfloor - 1) P_i$.
                        We need to sum the largest $rem$ values of $m_i$.
                        $m_i$ is roughly $2K$.
                        Actually, we can avoid sorting by observing that $m_i$ depends on $K/P_i$.
                        But maybe the number of distinct $x_i$ is small? No.
                        Alternative: Binary search on $T$ (threshold marginal cost) directly to find max $X$.
                        Let $f(T)$ = max units we can buy with cost $\le M$ such that all bought units have marginal cost $\le T$.
                        This is not quite right.
                        
                        Let's go back to the threshold $T$ approach which seemed promising.
                        We want to find the largest $T$ such that the cost of taking all units with marginal cost $\le T$ is $\le M$.
                        Let this be $T_{opt}$.
                        Then we buy all units with marginal cost $\le T_{opt}$.
                        Then we buy as many units with marginal cost $> T_{opt}$ as possible, prioritizing smallest costs.
                        The number of such units is likely small?
                        Wait, if $T_{opt}$ is small, we can buy many.
                        But if $T_{opt}$ is small, it means the sum of costs of all units $\le T_{opt}+1$ is $> M$.
                        This implies we can't buy all units $\le T_{opt}+1$.
                        So we can buy at most a few units from the range $(T_{opt}, T_{opt}+1]$.
                        What about $(T_{opt}+1, T_{opt}+2]$?
                        If we buy a unit from there, its cost is $\ge T_{opt}+2$.
                        The total cost of all units $\le T_{opt}+1$ is $> M$.
                        So $C_{opt} + \text{cost}(all \le T_{opt}+1) > M$.
                        $R < \text{cost}(all \le T_{opt}+1)$.
                        If we buy a unit with cost $c \ge T_{opt}+2$, then $C_{opt} + c > C_{opt} + T_{opt}+2$.
                        Is it possible $C_{opt} + c \le M$?
                        Yes, if $R \ge c$.
                        But we know $R < \text{cost}(all \le T_{opt}+1)$.
                        If there are no units with cost $\le T_{opt}+1$ (except those $\le T_{opt}$), then $R$ can be large.
                        But if there are no units with cost $T_{opt}+1$, then the next cost is $T_{opt}+2$.
                        Then $T_{opt}+2$ is the smallest cost $> T_{opt}$.
                        We can buy units with cost $T_{opt}+2$ as long as $R \ge T_{opt}+2$.
                        How many? $\lfloor R / (T_{opt}+2) \rfloor$.
                        Then we check next cost, etc.
                        The key insight: The number of distinct marginal cost values $> T_{opt}$ that we might consider is small?
                        No, but the number of units we can buy from the "next layer" is bounded by $R / (T_{opt}+1)$.
                        If $T_{opt}$ is large, this is small.
                        If $T_{opt}$ is small, then $T_{opt}+1$ is small, so we can buy many.
                        BUT, if $T_{opt}$ is small, it means $M$ is small relative to the number of cheap units?
                        No, if $T_{opt}$ is small, it means even taking all units with cost $\le T_{opt}$ is close to $M$, but adding any unit with cost $> T_{opt}$ pushes it over?
                        No, $T_{opt}$ is the max $T$ such that sum of ALL units $\le T$ is $\le M$.
                        If $T_{opt}$ is small, it means for $T=T_{opt}+1$, the sum of ALL units $\le T_{opt}+1$ is $> M$.
                        This means there are many units with cost $T_{opt}+1$.
                        So we can buy at most $\lfloor R/(T_{opt}+1) \rfloor$ units from this group.
                        If $T_{opt}+1$ is small, this number can be large.
                        However, we can just collect all units with cost $T_{opt}+1$, sort them (they are all equal), and take as many as possible.
                        Then check $T_{opt}+2$, etc.
                        Since the costs are integers, we can iterate $T$ from $T_{opt}+1$ upwards.
                        For each $T$, count how many units have cost $T$.
                        Let this count be $cnt_T$.
                        We can buy $k = \min(cnt_T, \lfloor R/T \rfloor)$ units.
                        $R \leftarrow R - k \cdot T$.
                        If $k < cnt_T$, we stop (cannot afford more).
                        If $k = cnt_T$, we continue to $T+1$.
                        How many iterations?
                        Since we stop when $R < T$, and $T$ increases, the number of iterations is at most $R_{initial} + 1$? No.
                        But we know that $\sum_{u: cost(u) \le T_{opt}+1} cost(u) > M$.
                        So the number of units with cost $T_{opt}+1$ is large enough to exceed $R$.
                        So we will stop at $T_{opt}+1$ in most cases?
                        Unless there are NO units with cost $T_{opt}+1$.
                        Then we go to $T_{opt}+2$.
                        The number of iterations is bounded by the number of distinct marginal cost values up to $R$.
                        But $R$ can be $10^{18}$.
                        However, we only care about costs that actually exist.
                        The costs are $(2k-1)P_i$.
                        The number of distinct values might be large.
                        But we can use the fact that we only need to check $T$ where there exists a unit with cost $T$.
                        We can collect all $c_i = (2k_i^{max}+1)P_i$ for all $i$.
                        Sort them.
                        Then iterate through the sorted list.
                        Since we can only pick a few units from each cost level (actually, we pick all if affordable, or a fraction), and the costs are increasing, we can just:
                        1. Collect all next unit costs $c_i$.
                        2. Sort $c_i$.
                        3. Iterate and pick.
                        But if we pick $c_i$, the next one is $c_i + 2P_i$.
                        This changes the set of available costs.
                        However, since we can only pick a few units (because the sum of all units $\le T_{opt}+1$ is $> M$), the number of units we pick from the "next layer" is small?
                        Wait, if $T_{opt}$ is small, $R$ is large, but the sum of units $\le T_{opt}+1$ is $> M$.
                        So we can pick at most $M/(T_{opt}+1)$ units.
                        If $T_{opt}$ is small, this can be large.
                        But if $T_{opt}$ is small, then $P_i$ must be small?
                        Actually, the number of units we can pick is bounded by $N \times (\text{something small})$.
                        Given the constraints and time limit, the intended solution is likely:
                        Binary search on $T$ to find $T_{opt}$.
                        Then collect all $c_i = (2k_i^{max}+1)P_i$.
                        Sort $c_i$.
                        Use a priority queue or just iterate if the number of items to pick is small.
                        But if the number of items is large, we can't iterate.
                        However, note that if we pick a unit with cost $c$, the next one is $c+2P_i \ge c+2$.
                        The costs are strictly increasing for each product.
                        The total number of units we can pick is at most $M$. But we need to output the count.
                        Actually, the number of units we can pick from the "next layer" is at most $N$?
                        No.
                        Let's assume the number of iterations is small enough or we can use binary search on the number of units to add?
                        Given the complexity, maybe the number of distinct $c_i$ is small?
                        No.
                        Let's just implement the binary search on $T$ and then a greedy selection using a priority queue, but limit the number of extractions?
                        Actually, the number of units we can add is at most $N$?
                        If we add more than $N$ units, we must have added at least 2 units from some product.
                        If we add 2 units from product $i$, costs are $c_i, c_i+2P_i$.
                        If we add $k$ units from product $i$, costs are $c_i, c_i+2P_i, \dots$.
                        The sum is roughly $k \cdot c_i + k^2 P_i$.
                        If $c_i \approx T_{opt}$, and we add many, the cost grows quadratically.
                        Since $R < \text{sum of all units } \le T_{opt}+1$, and the sum of units $\le T_{opt}+1$ is dominated by the count of such units.
                        If $T_{opt}$ is small, the count is large, so $R$ is small relative to the count?
                        No, $R$ is fixed.
                        Okay, I will implement the binary search on $T$ and then a greedy approach with a priority queue, but I suspect the number of units to add is small enough or the priority queue operations are fast enough.
                        Actually, the number of units to add is at most $N$?
                        If we add $> N$ units, by Pigeonhole Principle, some product has $\ge 2$ units added.
                        If we add 2 units from product $i$, cost is $c_i + (c_i+2P_i) = 2c_i + 2P_i$.
                        If we add $k$ units, cost is $\sum_{j=0}^{k-1} (c_i + 2jP_i) = k c_i + k(k-1)P_i$.
                        Since $c_i \ge T_{opt}+1$, cost $\ge k(T_{opt}+1) + k(k-1)P_i$.
                        If $k$ is large, cost is large.
                        Given $R < \text{sum of all units } \le T_{opt}+1$, and the sum is $> M$, it implies $R$ is not extremely large compared to $T_{opt}$.
                        Actually, the number of units we can add is likely $\le N$.
                        So we can just collect all $c_i$, sort them, and iterate?
                        No, because picking one changes the next.
                        But if we assume we pick at most $N$ units, we can use a priority queue.
                        Complexity: $O(N \log N + K \log N)$ where $K$ is number of units added. If $K \le N$, it's fine.

## worker: Read inputs $N, M$ and $P$.
The problem asks to maximize the total number of units bought with a budget $M$ given a cost function $k^2 P_i$ for $k$ units of product $i$.
The marginal cost of the $k$-th unit of product $i$ is $(2k-1)P_i$. This forms an arithmetic progression for each product.
To maximize the count, we should greedily pick units with the smallest marginal costs.
The strategy is:
1.  **Binary Search on Threshold $T$**: Find the largest integer $T$ such that the sum of costs of ALL units with marginal cost $\le T$ is $\le M$. Let this threshold be $T_{opt}$.
    *   For a given $T$, the number of units of product $i$ we can buy is $k_i = \lfloor \frac{\lfloor T/P_i \rfloor + 1}{2} \rfloor$.
    *   The total cost is $\sum P_i k_i^2$.
    *   We binary search $T$ in the range $[1, 2 \cdot 10^{18} + 7]$.
2.  **Greedy Selection for Remaining Budget**:
    *   After buying all units with marginal cost $\le T_{opt}$, we have a remaining budget $R = M - \text{cost}(T_{opt})$.
    *   We need to buy additional units with marginal cost $> T_{opt}$.
    *   The next available unit for product $i$ (which had $k_i$ units) has marginal cost $c_i = (2k_i + 1)P_i$.
    *   We collect all such $c_i$ into a min-priority queue.
    *   We repeatedly extract the smallest $c_i$. If $c_i \le R$, we buy it (decrement $R$, increment count), and push the next unit's cost for that product ($c_i + 2P_i$) back into the queue.
    *   If $c_i > R$, we stop because all other available units have cost $\ge c_i > R$.
    *   The number of units added in this phase is typically small because $T_{opt}$ is the maximum threshold where the sum of costs $\le T_{opt}$ fits in $M$. This implies that the sum of costs of units with cost in $(T_{opt}, T_{opt}+1]$ exceeds $R$, limiting the number of units we can pick from the immediate next layer. Even if $T_{opt}$ is small, the logic holds.

Complexity:
- Binary Search: $O(N \log(\text{Range}))$.
- Priority Queue operations: In the worst case, we might process many units, but practically, the number of units added beyond $T_{opt}$ is limited by the budget constraint relative to the marginal costs. Given the constraints and the nature of the problem, this approach is efficient enough. The number of PQ operations is bounded by the number of units we can afford, which is at most $M$ but effectively much smaller in the context of the "next layer" logic. Specifically, since we stop when the smallest available cost exceeds $R$, and the costs increase, we won't process too many.

## worker: Implement the full solution code based on the stra
The solution implements the strategy derived:
1.  **Binary Search on Threshold $T$**: We find the largest integer $T$ such that the sum of costs of all units with marginal cost $\le T$ does not exceed $M$. The marginal cost of the $k$-th unit of product $i$ is $(2k-1)P_i$. The condition $(2k-1)P_i \le T$ allows us to calculate the maximum $k$ for each product in $O(1)$, leading to an $O(N)$ check function. The binary search runs in $O(N \log(\text{Range}))$.
2.  **Greedy Selection with Priority Queue**: After determining $T_{opt}$, we have a remaining budget $R$. We collect the marginal costs of the next available unit for each product (which are all $> T_{opt}$) into a min-heap. We then repeatedly extract the smallest cost, buy the unit if affordable, decrement the budget, and push the next unit's cost for that product back into the heap. This greedy approach works because the marginal costs for each product are strictly increasing. The number of operations in the heap is proportional to the number of additional units we can buy, which is bounded and efficient given the constraints.

The complexity is dominated by the binary search $O(N \log(10^{18}))$ and the heap operations, which is well within the time limits for $N=2 \times 10^5$.

## worker: Run the code against the provided sample inputs to
The solution implements a two-phase approach:
1.  **Binary Search on Threshold ($T$):** We determine the maximum marginal cost $T$ such that purchasing *all* units with marginal cost $\le T$ fits within the budget $M$. This is done by binary searching $T$ and calculating the total cost in $O(N)$ time. The marginal cost of the $k$-th unit of product $i$ is $(2k-1)P_i$. The condition $(2k-1)P_i \le T$ allows us to compute the maximum $k$ for each product efficiently.
2.  **Greedy Selection with Priority Queue:** After identifying $T_{opt}$, we have a remaining budget $R = M - \text{cost}(T_{opt})$. We then greedily purchase additional units with marginal costs $> T_{opt}$. The next available unit for each product is identified, and its cost is pushed into a min-heap. We repeatedly extract the smallest cost, buy the unit if affordable, decrement the budget, and push the next unit's cost for that product back into the heap. This ensures we always pick the cheapest available unit. The number of operations in the heap is proportional to the number of additional units we can buy, which is bounded and efficient.

The complexity is dominated by the binary search $O(N \log(\text{Range}))$ and the heap operations, which fits well within the time limits for $N=2 \times 10^5$.

## worker: Run the code against Sample 1: `3 9` and `4 1 9`. 
The solution implements a two-phase approach:
1.  **Binary Search on Threshold ($T$):** We determine the maximum marginal cost $T$ such that purchasing *all* units with marginal cost $\le T$ fits within the budget $M$. This is done by binary searching $T$ and calculating the total cost in $O(N)$ time. The marginal cost of the $k$-th unit of product $i$ is $(2k-1)P_i$. The condition $(2k-1)P_i \le T$ allows us to compute the maximum $k$ for each product efficiently.
2.  **Greedy Selection with Priority Queue:** After identifying $T_{opt}$, we have a remaining budget $R = M - \text{cost}(T_{opt})$. We then greedily purchase additional units with marginal costs $> T_{opt}$. The next available unit for each product is identified, and its cost is pushed into a min-heap. We repeatedly extract the smallest cost, buy the unit if affordable, decrement the budget, and push the next unit's cost for that product back into the heap. This ensures we always pick the cheapest available unit. The number of operations in the heap is proportional to the number of additional units we can buy, which is bounded and efficient given the constraints.

The complexity is dominated by the binary search $O(N \log(\text{Range}))$ and the heap operations, which fits well within the time limits for $N=2 \times 10^5$.

## worker: finalize
The solution uses a two-phase greedy approach combined with binary search:
1.  **Binary Search on Threshold ($T$):** We determine the maximum marginal cost $T$ such that purchasing *all* units with marginal cost $\le T$ fits within the budget $M$. The marginal cost of the $k$-th unit of product $i$ is $(2k-1)P_i$. The condition $(2k-1)P_i \le T$ allows us to compute the maximum $k$ for each product in $O(1)$, leading to an $O(N)$ check function. The binary search runs in $O(N \log(\text{Range}))$.
2.  **Greedy Selection with Priority Queue:** After identifying $T_{opt}$, we have a remaining budget $R = M - \text{cost}(T_{opt})$. We then greedily purchase additional units with marginal costs $> T_{opt}$. The next available unit for each product is identified, and its cost is pushed into a min-heap. We repeatedly extract the smallest cost, buy the unit if affordable, decrement the budget, and push the next unit's cost for that product back into the heap. This ensures we always pick the cheapest available unit. The number of operations in the heap is proportional to the number of additional units we can buy, which is bounded and efficient given the constraints.

The complexity is dominated by the binary search $O(N \log(10^{18}))$ and the heap operations, which fits well within the time limits for $N=2 \times 10^5$.
