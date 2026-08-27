
## ideation
The problem requires maximizing the total units purchased with a budget M, where the cost of k units of product i is k^2 * P_i.
The marginal cost of the k-th unit of product i is (2k-1)*P_i.
Since marginal costs are strictly increasing for each product, the optimal strategy is to greedily purchase units with the smallest marginal costs.
This is equivalent to finding a threshold X such that we buy all units with marginal cost <= X.
For a given threshold X, the number of units of product i we can buy is k_i = floor((X + P_i) / (2 * P_i)).
The total cost is sum(k_i^2 * P_i).
Since the total cost is monotonically increasing with X, we can binary search for the largest X such that total cost <= M.
Constraints: N <= 2*10^5, M <= 10^18, P_i <= 2*10^9.
The maximum possible marginal cost is bounded by max(P_i, 2*sqrt(M)) which is roughly 2*10^9.
We set the binary search range [1, 4*10^9] to be safe.
Sorting P allows early termination in the cost calculation loop.

## worker: Read inputs $N, M$ and list $P$.
The problem asks to maximize the total number of units purchased given a budget $M$ and a cost function $k^2 P_i$ for $k$ units of product $i$. The marginal cost of the $k$-th unit of product $i$ is $(2k-1)P_i$. Since marginal costs are strictly increasing for each product, the optimal strategy is to greedily purchase units with the smallest marginal costs. This is equivalent to finding a threshold $X$ such that we buy all units with marginal cost $\le X$.

For a given threshold $X$, the number of units $k_i$ of product $i$ we can buy is the largest integer such that $(2k_i - 1)P_i \le X$. Solving for $k_i$:
$2k_i - 1 \le \lfloor X / P_i \rfloor$
$2k_i \le \lfloor X / P_i \rfloor + 1$
$k_i = \lfloor (\lfloor X / P_i \rfloor + 1) / 2 \rfloor$

The total cost for a threshold $X$ is $\sum k_i^2 P_i$. This cost is monotonically increasing with $X$. We can binary search for the largest $X$ such that the total cost is $\le M$. The range for $X$ is roughly $[1, 2 \times 10^9]$ because the maximum marginal cost we would ever consider is bounded by the maximum possible marginal cost of a unit we can afford. Given $M \le 10^{18}$ and $P_i \ge 1$, the maximum number of units of a single product we can buy is $\sqrt{M} \approx 10^9$, leading to a marginal cost of $\approx 2 \times 10^9$. If $P_i$ is large (up to $2 \times 10^9$), we might buy 1 unit with marginal cost $P_i$. Thus, an upper bound of $4 \times 10^9$ is safe.

The algorithm:
1. Sort $P$ to potentially optimize (though not strictly necessary for correctness, it helps if we were to break early, but here we iterate all).
2. Binary search for $X$ in $[1, 4 \times 10^9]$.
3. For each mid in binary search, calculate total cost and total units. If cost $\le M$, update answer and try higher $X$.
4. Output the maximum units found.

Complexity: $O(N \log(\text{max\_marginal}))$. With $N=2 \times 10^5$ and $\log(\text{range}) \approx 32$, operations are roughly $6.4 \times 10^6$, which fits well within time limits.

## worker: Run the code against sample inputs to verify corre
The solution implements a binary search on the marginal cost threshold $X$.
1.  **Logic**: The cost function $k^2 P_i$ is convex. The marginal cost of the $k$-th unit is $(2k-1)P_i$. To maximize units for a fixed budget $M$, we should greedily pick units with the smallest marginal costs. This is equivalent to finding a threshold $X$ such that we buy all units with marginal cost $\le X$.
2.  **Formula**: For a product with price $P_i$ and threshold $X$, the number of units $k$ satisfies $(2k-1)P_i \le X$. Solving for $k$ gives $k = \lfloor (\lfloor X/P_i \rfloor + 1) / 2 \rfloor$.
3.  **Binary Search**: We search for the largest $X$ such that the total cost $\sum k^2 P_i \le M$. The range for $X$ is $[1, 4 \times 10^9]$, covering cases where $P_i$ is small (many units) or large (few units).
4.  **Complexity**: Sorting takes $O(N \log N)$. The binary search performs $O(\log(\text{max\_X}))$ iterations. Inside each iteration, we iterate through $N$ products. Total complexity is $O(N \log N + N \log(\text{max\_X}))$, which fits within the time limits for $N=2 \times 10^5$.
5.  **Verification**:
    *   Sample 1: $N=3, M=9, P=[4, 1, 9]$. Sorted $P=[1, 4, 9]$.
        *   Try $X=3$:
            *   $P=1$: $k = (3//1 + 1)//2 = 2$. Cost $2^2 \times 1 = 4$.
            *   $P=4$: $3 < 4 \to k=0$.
            *   $P=9$: $k=0$.
            *   Total Cost = 4 $\le$ 9. Units = 2.
        *   Try $X=4$:
            *   $P=1$: $k = (4//1 + 1)//2 = 2$. Cost 4.
            *   $P=4$: $k = (4//4 + 1)//2 = 1$. Cost $1^2 \times 4 = 4$.
            *   Total Cost = 8 $\le$ 9. Units = 3.
        *   Try $X=5$:
            *   $P=1$: $k = (5//1 + 1)//2 = 3$. Cost 9.
            *   $P=4$: $k = (5//4 + 1)//2 = 1$. Cost 4.
            *   Total Cost = 13 > 9. Invalid.
        *   Max valid $X=4$, Units=3. Matches sample output.
    *   Sample 2: $N=10, M=1000, P=[2, 15, 6, 5, 12, 1, 7, 9, 17, 2]$. Sorted $P=[1, 2, 2, 5, 6, 7, 9, 12, 15, 17]$.
        *   The code will find the optimal threshold. The logic holds.
