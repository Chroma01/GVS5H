
## ideation
The core difficulty is efficiently checking if a total of $K$ units can be purchased with cost $\le M$.
1.  **Binary Search on Answer**: The maximum total units $K$ is bounded. Since min $P_i \ge 1$, max $K \approx \sqrt{M} \le 10^9$. We can binary search for the maximum $K$ in range $[0, 2 \cdot 10^9]$.
2.  **Feasibility Check for Fixed $K$**: For a fixed $K$, we need to minimize $\sum k_i^2 P_i$ subject to $\sum k_i = K$.
    *   The cost function is convex. The optimal distribution satisfies $2 k_i P_i \approx \lambda$ (Lagrange multiplier). Thus, $k_i \approx \frac{\lambda}{2 P_i}$.
    *   Let $x_i = k_i$. We want to find non-negative integers $x_i$ such that $\sum x_i = K$ and $\sum x_i^2 P_i$ is minimized.
    *   This is equivalent to finding a threshold $\lambda$ such that if we set $x_i(\lambda) = \lfloor \frac{\lambda}{2 P_i} \rfloor$ (or similar continuous approximation rounded down), the sum $\sum x_i(\lambda)$ is close to $K$.
    *   Specifically, let's define a function $f(\lambda) = \sum_{i=1}^N \lfloor \frac{\lambda}{2 P_i} \rfloor$. This function is non-decreasing with $\lambda$.
    *   We can binary search for the smallest $\lambda$ such that $f(\lambda) \ge K$. Let this be $\lambda^*$.
    *   The "base" allocation is $k_i = \lfloor \frac{\lambda^*}{2 P_i} \rfloor$. Let $S = \sum k_i$. If $S < K$, we have some remaining units $R = K - S$ to distribute.
    *   The remaining units should be assigned to products where the *marginal cost* of adding one more unit is smallest. The marginal cost of the $(k_i+1)$-th unit for product $i$ is $(k_i+1)^2 P_i - k_i^2 P_i = (2k_i+1)P_i$.
    *   So, we calculate the marginal cost for each product for the next unit, sort them (or use a selection algorithm), and assign the remaining $R$ units to the products with the smallest marginal costs.
    *   Finally, check if the total cost $\le M$.

3.  **Optimization**:
    *   Binary searching $\lambda$ takes $O(N \log (\text{max\_lambda}))$. Max $\lambda \approx 2 P_i \sqrt{K} \approx 2 \cdot 2\cdot 10^9 \cdot 10^9 = 4 \cdot 10^{18}$, so $\log \lambda \approx 60$.
    *   Calculating sum and marginal costs takes $O(N)$.
    *   Sorting marginal costs for the remainder takes $O(N \log N)$ or $O(N)$ with `nth_element`/quickselect if we only need the sum of the smallest $R$. Since $N=2 \cdot 10^5$, $O(N \log N)$ is acceptable inside the outer binary search?
    *   Outer binary search runs $\approx 60$ times. Inner check is $O(N \log N)$. Total complexity $O(60 \cdot N \log N) \approx 60 \cdot 2 \cdot 10^5 \cdot 18 \approx 2 \cdot 10^8$ operations. This might be tight for Python.
    *   Can we optimize the inner check?
        *   We don't need to sort fully. We just need the sum of the smallest $R$ marginal costs. We can use `numpy.partition` or `quickselect` to find the threshold marginal cost and sum the rest. This reduces the inner check to $O(N)$.
        *   Total complexity $O(60 \cdot N)$, which is $\approx 1.2 \cdot 10^7$, very fast in Python.

4.  **Pitfalls**:
    *   Integer overflow: Costs can exceed $2^{63}-1$? $M \le 10^{18}$, so we only care if cost $\le 10^{18}$. Intermediate calculations like $\lambda^2$ might overflow 64-bit integers if not careful, but Python handles large integers automatically.
    *   Precision: Using floating point for $\lambda$ binary search might be risky. Better to use integer binary search for $\lambda$.
    *   Edge case: $K=0$.

## worker: (None)
The problem asks to maximize the total number of units $K = \sum k_i$ subject to $\sum k_i^2 P_i \le M$.
1.  **Binary Search on Answer**: The maximum possible $K$ is bounded by $\sqrt{M}$ (since min $P_i \ge 1$). With $M \le 10^{18}$, $K \le 10^9$. We binary search for the largest $K$ such that the minimum cost to buy $K$ units is $\le M$.
2.  **Feasibility Check**: For a fixed $K$, we need to minimize $\sum k_i^2 P_i$ subject to $\sum k_i = K$.
    *   The cost function is convex. The optimal real-valued allocation satisfies $2 k_i P_i = \lambda$, so $k_i = \lambda / (2 P_i)$.
    *   For integer allocations, we find the smallest integer $\lambda$ such that $\sum \lfloor \lambda / (2 P_i) \rfloor \ge K$. Let this be $\lambda^*$.
    *   The base allocation is $k_i = \lfloor \lambda^* / (2 P_i) \rfloor$. Let $S = \sum k_i$.
    *   If $S = K$, we compute the cost and check.
    *   If $S > K$, we have $S - K$ excess units. We remove units with the largest marginal savings. The marginal saving of removing the $j$-th unit from product $i$ is $(2j - 1) P_i$. Since $S - K \le N$ (due to the floor function property), we can use a max-heap to efficiently remove the top $S - K$ units.
    *   If $S < K$, we have $K - S$ missing units. We add units with the smallest marginal costs. The marginal cost of adding the $(k_i+1)$-th unit is $(2k_i + 1) P_i$. We use a min-heap to add the cheapest $K - S$ units.
3.  **Complexity**:
    *   Outer binary search: $O(\log (\sqrt{M})) = O(\log M) \approx 60$ iterations.
    *   Inner check:
        *   Finding $\lambda^*$: $O(N \log (\text{max\_lambda})) \approx O(N \cdot 60)$.
        *   Heap operations: $O(N \log N)$ for building the heap and $O(K_{diff} \log N)$ for adjustments. Since $K_{diff} \le N$, this is $O(N \log N)$.
    *   Total complexity: $O(\log M \cdot (N \log M + N \log N))$. With $N=2 \cdot 10^5$, this is roughly $60 \cdot (2 \cdot 10^5 \cdot 60 + 2 \cdot 10^5 \cdot 18) \approx 60 \cdot 1.56 \cdot 10^7 \approx 10^9$ operations. This might be tight in Python.
    *   Optimization: The inner binary search for $\lambda$ can be optimized. Notice that $f(\lambda) = \sum \lfloor \lambda / (2 P_i) \rfloor$ is monotonic. We can also observe that the optimal $\lambda$ is roughly $2 P_{avg} \sqrt{K}$. However, the current approach is correct and likely fast enough given the constraints and typical time limits for Python if implemented efficiently. The heap operations are only on $N$ elements, and $N \log N$ is small.
