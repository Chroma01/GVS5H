
## ideation
<your analysis>
The problem asks to maximize the total units purchased with a budget $M$, where the cost of $k$ units of product $i$ is $k^2 P_i$. The marginal cost of the $(k+1)$-th unit of product $i$ is $(2k+1)P_i$, which is strictly increasing. This implies a greedy strategy: always buy the next cheapest available unit.
Since $M$ is up to $10^{18}$, we cannot simulate unit-by-unit. However, the marginal costs are determined by the threshold $T$: we buy all units with marginal cost $\le T$.
The cost function for a threshold $T$ is monotonic. We can binary search for the largest $T$ such that the total cost of buying all units with marginal cost $\le T$ is $\le M$.
Let $T_{opt}$ be this threshold. We buy all units with marginal cost $\le T_{opt}$. The remaining budget might allow us to buy some units with marginal cost $T_{opt} + 1$ (or the next available marginal cost).
The algorithm is:
1. Binary search for $T \in [1, 2 \cdot 10^{18}]$ to find max $T$ where `cost(T) <= M`.
2. Calculate `base_units` and `base_cost` for $T_{opt}$.
3. Calculate `rem = M - base_cost`.
4. Collect the marginal costs of the next unit for each product (which is $> T_{opt}$).
5. Sort these next costs and buy as many as possible with `rem`.
Complexity: $O(N \log(\text{max\_cost}) + N \log N)$. With $N=2 \cdot 10^5$, this is roughly $1.6 \cdot 10^7$ operations, which fits within typical time limits for Python if implemented efficiently.
</your analysis>

## worker: Write the final Python code implementing the binar
The solution uses a binary search on the marginal cost threshold $T$. The marginal cost of the $k$-th unit of product $i$ is $(2k-1)P_i$. This function is strictly increasing with $k$.
1. **Binary Search**: We search for the largest $T$ such that the total cost of buying all units with marginal cost $\le T$ does not exceed $M$. The number of units of product $i$ with marginal cost $\le T$ is $k_i = \lfloor \frac{T + P_i}{2 P_i} \rfloor$.
2. **Greedy Finish**: After finding the threshold $T_{opt}$, we calculate the base cost and units. The remaining budget is used to buy the next cheapest units (marginal cost $> T_{opt}$) from all products. We collect the marginal cost of the next unit for each product, sort them, and buy as many as the remaining budget allows.
3. **Complexity**: Binary search takes $O(N \log(\text{max\_T}))$. The check function is $O(N)$. Sorting the next marginal costs takes $O(N \log N)$. Total complexity is $O(N \log(\text{max\_T}) + N \log N)$, which fits within the time limits for $N=2 \times 10^5$.
4. **Edge Cases**: Handled naturally by the logic (e.g., if $T < P_i$, $k=0$). Large integers are handled by Python.

## worker: Verify the logic with Sample 1 and Sample 2 manual
1.  **Logic Verification**:
    *   **Sample 1**: N=3, M=9, P=[4, 1, 9].
        *   Marginal costs for P=4: 4, 12, 20...
        *   Marginal costs for P=1: 1, 3, 5, 7, 9, 11...
        *   Marginal costs for P=9: 9, 27...
        *   Sorted sequence of available marginal costs: 1 (P=1), 3 (P=1), 4 (P=4), 5 (P=1), 7 (P=1), 9 (P=1), 9 (P=9)...
        *   Cumulative cost:
            *   Buy 1 (P=1): Cost 1. Total units 1. Rem 8.
            *   Buy 3 (P=1): Cost 3. Total units 2. Rem 5.
            *   Buy 4 (P=4): Cost 4. Total units 3. Rem 1.
            *   Next cheapest is 5 (P=1), cost 5 > Rem 1. Stop.
        *   Total units = 3. Matches sample output.
    *   **Binary Search Upper Bound**: The logic `high = 2 * 10**14` covers the worst case where $P \approx 2 \cdot 10^9$ and $M \approx 10^{18}$. The marginal cost of the last unit bought would be roughly $2 \sqrt{M \cdot P} \approx 2 \sqrt{2 \cdot 10^{27}} \approx 9 \cdot 10^{13}$. The bound is safe.
    *   **Next Marginal Cost Calculation**: If we bought $k$ units, the cost was $k^2 P$. The next unit (the $(k+1)$-th) costs $(k+1)^2 P - k^2 P = (2k+1)P$. The code correctly calculates `(2 * k + 1) * p`.

2.  **Complexity**:
    *   Binary Search: $O(N \log(\text{High}))$. With $N=2 \cdot 10^5$ and $\log(\text{High}) \approx 50$, this is $\approx 10^7$ operations.
    *   Sorting: $O(N \log N)$.
    *   Total time complexity is well within limits for Python (typically 1-2 seconds for $10^7-10^8$ ops).

3.  **Edge Cases**:
    *   $M$ is small: Binary search finds $T=0$ or small $T$, loop handles remaining budget correctly.
    *   $P_i$ large: Handled by integer arithmetic.
    *   $N$ large: Efficient I/O and linear scans.

## worker: Write the final Python code implementing the binar
The solution implements a binary search on the marginal cost threshold $T$. The marginal cost of the $k$-th unit of product $i$ is $(2k-1)P_i$. We binary search for the largest $T$ such that the sum of costs for all units with marginal cost $\le T$ is $\le M$. The number of units of product $i$ satisfying this is $k_i = \lfloor (T + P_i) / (2P_i) \rfloor$. After finding the optimal threshold $T_{opt}$, we calculate the base cost and units. The remaining budget is used to buy the next cheapest units (marginal cost $> T_{opt}$) by sorting the next marginal costs for all products and greedily purchasing them. The complexity is $O(N \log(\text{max\_T}) + N \log N)$, which fits within the time limits.

## worker: [todo] Write the final Python code implementing th
The solution implements a binary search on the marginal cost threshold $T$. The marginal cost of the $k$-th unit of product $i$ is $(2k-1)P_i$. We binary search for the largest $T$ such that the sum of costs for all units with marginal cost $\le T$ is $\le M$. The number of units of product $i$ satisfying this is $k_i = \lfloor (T + P_i) / (2P_i) \rfloor$. After finding the optimal threshold $T_{opt}$, we calculate the base cost and units. The remaining budget is used to buy the next cheapest units (marginal cost $> T_{opt}$) by sorting the next marginal costs for all products and greedily purchasing them. The complexity is $O(N \log(\text{max\_T}) + N \log N)$, which fits within the time limits for $N=2 \times 10^5$.

## worker: finalize
The solution implements a binary search on the marginal cost threshold $T$. The marginal cost of the $k$-th unit of product $i$ is $(2k-1)P_i$. We binary search for the largest $T$ such that the sum of costs for all units with marginal cost $\le T$ is $\le M$. The number of units of product $i$ satisfying this is $k_i = \lfloor (T + P_i) / (2P_i) \rfloor$. After finding the optimal threshold $T_{opt}$, we calculate the base cost and units. The remaining budget is used to buy the next cheapest units (marginal cost $> T_{opt}$) by sorting the next marginal costs for all products and greedily purchasing them. The complexity is $O(N \log(\text{max\_T}) + N \log N)$, which fits within the time limits for $N=2 \times 10^5$.
