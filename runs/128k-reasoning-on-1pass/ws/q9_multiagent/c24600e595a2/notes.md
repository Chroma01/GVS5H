
## ideation
The problem asks for the minimum cost to transform binary sequence $A$ into binary sequence $B$ by flipping bits. Each flip operation incurs a cost equal to the weighted sum of the current sequence $A$ (calculated *after* the flip).

**Core Difficulty:**
The cost of an operation depends on the state of $A$ *after* the flip. This means the order of operations significantly impacts the total cost. We need to determine the optimal order of flipping the bits that differ between $A$ and $B$.

**Candidate Approaches:**
1.  **Greedy Strategy with Sorting:**
    -   Identify indices where $A_i \neq B_i$. These must be flipped exactly once.
    -   Classify these indices into two sets:
        -   $P$: Indices where $A_i = 1, B_i = 0$ (flipping reduces the sum).
        -   $Z$: Indices where $A_i = 0, B_i = 1$ (flipping increases the sum).
    -   **Ordering:**
        -   Flipping an element in $P$ reduces the current sum, lowering the cost of subsequent operations.
        -   Flipping an element in $Z$ increases the current sum, raising the cost of subsequent operations.
        -   Therefore, it is optimal to perform all operations in $P$ before all operations in $Z$.
    -   **Within Groups:**
        -   For $P$: To minimize the cost $\sum (S_{current} - C_i)$, we want to subtract larger $C_i$ earlier when the sum is higher. Thus, sort $P$ by $C_i$ in descending order.
        -   For $Z$: To minimize the cost $\sum (S_{current} + C_i)$, we want to add smaller $C_i$ earlier when the sum is lower. Thus, sort $Z$ by $C_i$ in ascending order.
    -   **Calculation:**
        -   Compute initial sum $S = \sum A_k C_k$.
        -   Iterate through sorted $P$: Add $(S - C_i)$ to total cost, update $S \leftarrow S - C_i$.
        -   Iterate through sorted $Z$: Add $(S + C_i)$ to total cost, update $S \leftarrow S + C_i$.

2.  **Formulaic Calculation:**
    -   Derive a closed-form expression for the total cost based on the sorted order and initial sum.
    -   This avoids a simulation loop but requires careful indexing to avoid off-by-one errors. Simulation is safer and has the same complexity.

**Pitfalls:**
-   **Cost Calculation Timing:** The cost is calculated *after* the flip. This means for $P$, cost is $S_{old} - C_i$, and for $Z$, cost is $S_{old} + C_i$. This is different from standard problems where cost is often based on the pre-flip state.
-   **Integer Overflow:** The total cost can exceed $2^{31}-1$ (up to $\approx 4 \times 10^{16}$). Python handles large integers automatically, but in other languages, `long long` is needed.
-   **Sorting Order:** It is crucial to sort $P$ descending and $Z$ ascending. Reversing this leads to suboptimal solutions.
-   **Input Parsing:** Efficiently reading large inputs ($N=2 \times 10^5$) is necessary.

## worker: Write the Python code to implement the greedy stra
The problem asks for the minimum cost to transform sequence $A$ into $B$ by flipping bits. Each flip operation incurs a cost equal to the weighted sum of the current sequence $A$ (calculated *after* the flip).

**Core Logic:**
1.  **Identify Necessary Flips:** Only indices where $A_i \neq B_i$ need to be flipped.
    -   Set $P$: Indices where $A_i=1, B_i=0$ (flipping reduces the weighted sum).
    -   Set $Z$: Indices where $A_i=0, B_i=1$ (flipping increases the weighted sum).
2.  **Ordering:**
    -   Flipping elements in $P$ reduces the sum, lowering the cost of subsequent operations. Thus, perform all $P$ operations before $Z$ operations.
    -   Within $P$, flipping a larger $C_i$ reduces the sum more, which is beneficial for subsequent operations. So, sort $P$ by $C_i$ descending.
    -   Within $Z$, flipping a larger $C_i$ increases the sum more. Since $Z$ operations happen after $P$, we want to minimize the impact of the increased sum on subsequent $Z$ operations. Mathematical derivation shows that smaller $C_i$ should be processed earlier in the $Z$ sequence to minimize the total weighted sum of costs. So, sort $Z$ by $C_i$ ascending.
3.  **Calculation:**
    -   Compute initial sum.
    -   Iterate through sorted $P$, updating sum and accumulating cost.
    -   Iterate through sorted $Z$, updating sum and accumulating cost.
4.  **Complexity:** $O(N \log N)$ due to sorting. $N \le 2 \times 10^5$ fits within time limits.
