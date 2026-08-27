
## ideation
The problem asks for the minimum cost to transform binary sequence $A$ into $B$ by flipping bits. The cost of a flip operation at index $i$ is the sum of $A_k \cdot C_k$ for all $k$ *after* the flip of $A_i$.
Key observations:
1. We only need to flip indices where $A_i \neq B_i$. Let this set be $M$.
2. Indices where $A_i = B_i$ never change, but they contribute to the cost of every operation performed. If there are $K = |M|$ operations, a static index $i$ with $A_i=1$ contributes $K \cdot C_i$ to the total cost.
3. For indices in $M$, the value changes from $A_i$ to $B_i$. The cost contribution of $C_i$ depends on the order of operations. Specifically, if we flip index $i$ at step $t$ (1-indexed), $A_i$ is $1$ for steps $1, \dots, t$ (since the flip happens first, then cost is calculated, so the value used in cost is the new value) and $0$ for subsequent steps? Wait, let's re-verify the cost definition.
   - Operation: Flip $A_i$, then pay $\sum A_k C_k$.
   - If $A_i$ was $1$ and becomes $0$: The cost includes $0 \cdot C_i$. Before this operation, it contributed $1 \cdot C_i$ in previous operations.
   - If $A_i$ was $0$ and becomes $1$: The cost includes $1 \cdot C_i$. Before this operation, it contributed $0 \cdot C_i$.
   
   Let's refine the contribution logic:
   Total Cost = $\sum_{\text{ops } t} \sum_{k} A_k^{(t)} C_k = \sum_{k} C_k \sum_{t} A_k^{(t)}$.
   - If $k \notin M$: $A_k$ is constant. Sum is $K \cdot A_k$. Cost: $K \cdot A_k C_k$.
   - If $k \in M$: $A_k$ starts at $A_k$, flips to $B_k$ at step $t_k$.
     - For $t < t_k$: $A_k^{(t)} = A_k$.
     - For $t \ge t_k$: $A_k^{(t)} = B_k$ (since the flip happened at $t_k$, the value at $t_k$ is $B_k$).
     - Sum of values = $A_k \cdot (t_k - 1) + B_k \cdot (K - t_k + 1)$.
     - Contribution: $C_k [ A_k(t_k - 1) + B_k(K - t_k + 1) ]$.
   
   We need to minimize this sum by choosing the permutation of flips (values of $t_k$).
   Let's analyze the coefficient of $t_k$:
   Term = $C_k [ t_k(A_k - B_k) + (B_k(K+1) - A_k) ]$.
   - If $A_k = 1, B_k = 0$: Coeff of $t_k$ is $C_k(1-0) = C_k > 0$. To minimize, we want $t_k$ as **small** as possible. (Flip early).
   - If $A_k = 0, B_k = 1$: Coeff of $t_k$ is $C_k(0-1) = -C_k < 0$. To minimize, we want $t_k$ as **large** as possible. (Flip late).
   
   Strategy:
   1. Identify all indices $i$ where $A_i \neq B_i$.
   2. Separate them into two groups:
      - Group 1 ($1 \to 0$): Indices where $A_i=1, B_i=0$. Sort them by $C_i$? No, the coefficient is linear in $t_k$. The specific value of $t_k$ matters, but since all $1 \to 0$ flips want small $t$ and all $0 \to 1$ flips want large $t$, the optimal strategy is simply: **Perform all $1 \to 0$ flips first, then all $0 \to 1$ flips**. The relative order within Group 1 doesn't matter for the $t_k$ term because they all get the smallest available $t$'s ($1, 2, \dots, |G1|$), and the constant term doesn't depend on order. Same for Group 2.
      - Wait, does the relative order within Group 1 matter?
        Sum for $G1$: $\sum_{j \in G1} C_j [ t_j(1) + \text{const} ]$. We assign $t_j \in \{1, \dots, |G1|\}$. To minimize $\sum C_j t_j$, we should assign larger $t_j$ to smaller $C_j$? Yes, rearrangement inequality.
        Similarly for $G2$ ($0 \to 1$), coefficient is $-C_j$. We assign $t_j \in \{|G1|+1, \dots, K\}$. To minimize $\sum -C_j t_j = -\sum C_j t_j$, we want to maximize $\sum C_j t_j$. So assign larger $t_j$ to larger $C_j$.
   
   Revised Strategy:
   1. Calculate base cost from static indices ($k \notin M$): $K \cdot \sum_{k \notin M, A_k=1} C_k$.
   2. For dynamic indices ($k \in M$):
      - Split into $S_{10}$ ($1 \to 0$) and $S_{01}$ ($0 \to 1$).
      - Let $K_1 = |S_{10}|$, $K_2 = |S_{01}|$. Total $K = K_1 + K_2$.
      - For $S_{10}$: We need to assign times $1, \dots, K_1$. Cost part: $\sum_{j \in S_{10}} C_j [ t_j - 1 + \text{const} ] = \sum C_j t_j - \sum C_j + \dots$
        Actually, let's just compute the sum directly:
        Cost = $\sum_{j \in S_{10}} C_j [ A_j(t_j-1) + B_j(K-t_j+1) ]$.
        With $A_j=1, B_j=0$: $C_j [ t_j - 1 + 0 ] = C_j(t_j - 1)$.
        We need to minimize $\sum_{j \in S_{10}} C_j t_j$. Optimal: Sort $S_{10}$ by $C_j$ ascending, assign $t=1, 2, \dots$.
      - For $S_{01}$: $A_j=0, B_j=1$. Cost part: $C_j [ 0 + 1(K-t_j+1) ] = C_j(K - t_j + 1)$.
        We need to minimize $\sum_{j \in S_{01}} C_j (K+1) - \sum C_j t_j$. This is equivalent to maximizing $\sum C_j t_j$.
        Optimal: Sort $S_{01}$ by $C_j$ descending, assign $t=K_1+1, \dots, K$.
   
   Wait, is the "relative order" necessary?
   Let's re-read the problem carefully. "Print the minimum total cost".
   Usually in such problems, if the cost function is separable like this, sorting is required.
   Let's double check the logic.
   Total Cost = $\sum_{k \notin M} K A_k C_k + \sum_{j \in S_{10}} C_j (t_j - 1) + \sum_{j \in S_{01}} C_j (K - t_j + 1)$.
   (Note: The constant terms $B_j(K+1) - A_j$ were simplified in the previous step. Let's re-derive carefully).
   
   Re-derivation:
   Contribution of $j \in M$: $C_j \times (\text{sum of } A_j \text{ over } t=1..K)$.
   $A_j$ is $A_j$ for $t < t_j$, and $B_j$ for $t \ge t_j$.
   Sum = $A_j(t_j - 1) + B_j(K - t_j + 1)$.
   
   Case $1 \to 0$ ($A_j=1, B_j=0$):
   Sum = $1 \cdot (t_j - 1) + 0 = t_j - 1$.
   Total contribution = $\sum_{j \in S_{10}} C_j (t_j - 1) = \sum C_j t_j - \sum C_j$.
   To minimize, minimize $\sum C_j t_j$.
   Available $t_j \in \{1, \dots, K_1\}$.
   By rearrangement inequality, pair smallest $C_j$ with smallest $t_j$ (1).
   So sort $S_{10}$ by $C_j$ ascending.
   
   Case $0 \to 1$ ($A_j=0, B_j=1$):
   Sum = $0 + 1 \cdot (K - t_j + 1) = K - t_j + 1$.
   Total contribution = $\sum_{j \in S_{01}} C_j (K + 1 - t_j) = (K+1)\sum C_j - \sum C_j t_j$.
   To minimize, maximize $\sum C_j t_j$.
   Available $t_j \in \{K_1+1, \dots, K\}$.
   Pair largest $C_j$ with largest $t_j$.
   So sort $S_{01}$ by $C_j$ descending.
   
   Algorithm:
   1. Read inputs.
   2. Identify $M = \{i \mid A_i \neq B_i\}$. Let $K = |M|$.
   3. Calculate static cost: $K \times \sum_{i \notin M, A_i=1} C_i$.
   4. Collect $C_i$ for $i \in S_{10}$ ($A_i=1, B_i=0$). Sort ascending.
   5. Collect $C_i$ for $i \in S_{01}$ ($A_i=0, B_i=1$). Sort descending.
   6. Calculate dynamic cost:
      - For $S_{10}$: $\sum_{k=0}^{K_1-1} C_{sorted}[k] \times (k)$. (Since $t = k+1$, $t-1 = k$).
      - For $S_{01}$: $\sum_{k=0}^{K_2-1} C_{sorted}[k] \times (K - (K_1 + k))$. (Since $t = K_1 + k + 1$, term is $K - t + 1 = K - (K_1+k+1) + 1 = K - K_1 - k$).
   7. Sum static + dynamic.

   Complexity: $O(N \log N)$ due to sorting. $N \le 2 \times 10^5$, feasible.

## worker: Implement the solution in Python using the derived
The solution implements the derived optimal strategy:
1.  **Static Indices**: Indices where $A_i = B_i$ do not change. If $A_i=1$, they contribute $C_i$ to the cost of every operation performed. The total number of operations is $K$ (the count of mismatches). Thus, their total contribution is $K \times \sum C_i$.
2.  **Dynamic Indices**: Indices where $A_i \neq B_i$ must be flipped exactly once.
    *   **Group $1 \to 0$**: Flipping such an index reduces its value from 1 to 0. The cost contribution depends on when it is flipped. To minimize the total cost, we should flip these as early as possible. Furthermore, among these, indices with smaller $C_i$ should be flipped earlier to minimize the sum $\sum C_i \times t$. Hence, we sort $C_i$ values for this group in ascending order.
    *   **Group $0 \to 1$**: Flipping such an index increases its value from 0 to 1. To minimize cost, we should flip these as late as possible. Among these, indices with larger $C_i$ should be flipped later (larger $t$) to maximize the reduction in cost (since the term is $C_i \times (K - t + 1)$). Hence, we sort $C_i$ values for this group in descending order.
3.  **Ordering**: All $1 \to 0$ flips are performed before all $0 \to 1$ flips. This is optimal because $1 \to 0$ flips want small $t$ and $0 \to 1$ flips want large $t$.
4.  **Complexity**: The algorithm involves a single pass to categorize indices ($O(N)$) and sorting two lists of size at most $N$ ($O(N \log N)$). This fits well within the time limits for $N \le 2 \times 10^5$.
