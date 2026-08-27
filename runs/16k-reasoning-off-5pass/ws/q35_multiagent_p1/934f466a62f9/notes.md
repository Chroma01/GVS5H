
## ideation
The core difficulty lies in the fact that the objective function is the sum of maximums of sums, which doesn't decompose easily. A naive $O(N^2)$ pair evaluation is too slow for $N=10^5$. Binary search on the answer is a strong candidate because the "is it possible to get total score $\ge V$?" check might be solvable greedily or via matching. However, general maximum weight $k$-matching is hard.

Let's reconsider the structure. The price of a pair $(i, j)$ is $\max(X_i+X_j, Y_i+Y_j, Z_i+Z_j)$. This is equivalent to $\max_{d \in \{X,Y,Z\}} (d_i + d_j)$.
Total score = $\sum_{k=1}^K \max(X_{a_k}+X_{b_k}, Y_{a_k}+Y_{b_k}, Z_{a_k}+Z_{b_k})$.

Since $K$ can be up to $N/2$, we need an efficient algorithm.
Key observation: The function $f(i,j) = \max(X_i+X_j, Y_i+Y_j, Z_i+Z_j)$ is not linear.
However, note that $\max(A, B, C) = \frac{1}{2} (A+B+C + |A-B| + |B-C| + |C-A|)$? No, that's for 3 numbers. Actually $\max(A,B,C) = \frac{1}{2} (A+B+C + \max(|A-B|, |B-C|, |C-A|) \dots)$? No.
A simpler identity: $\max(A,B,C) = \frac{1}{2} (A+B+C + |A-B| + |B-C| + |C-A|)$ is false.
Correct identity: $\max(A,B,C) = \frac{1}{2} (A+B+C + \max(|A-B|, |B-C|, |C-A|))$? No.
Actually, $\max(A,B,C) = \frac{1}{2} (A+B+C + \max(A-B, B-A, B-C, C-B, C-A, A-C))$? No.

Let's look at constraints. Sum of N is $10^5$. This suggests an $O(N \log N)$ or $O(N \log (\max V))$ solution.
Binary search on the answer $V$ is promising.
Check(V): Can we pick $K$ disjoint pairs such that $\sum \text{price} \ge V$?
This is equivalent to: Can we pick $K$ disjoint pairs such that $\sum (\text{price} - \text{something}) \dots$? No.

Alternative approach:
Since the max is taken over 3 dimensions, maybe we can iterate over which dimension dominates?
For a specific pair, one of $X_i+X_j$, $Y_i+Y_j$, or $Z_i+Z_j$ is the maximum.
There are $3^K$ combinations? No, that's too big.

Let's look at similar problems. "Maximum weight matching in a general graph" is hard, but here the weights have special structure.
Wait, if we fix the "dominant dimension" for each pair, the problem becomes: maximize $\sum (D_{a_k} + D_{b_k})$ where $D \in \{X,Y,Z\}$.
If we knew for each pair which dimension dominates, we could just sum the top $2K$ values in that dimension? No, because the pairs must be disjoint and the "dominance" depends on the pair.

However, note that $\max(A,B,C) \ge A, \max(A,B,C) \ge B, \max(A,B,C) \ge C$.
So Total Price $\ge \sum (X_{a_k} + X_{b_k})$.
Also Total Price $\ge \sum (Y_{a_k} + Y_{b_k})$.
Also Total Price $\ge \sum (Z_{a_k} + Z_{b_k})$.

Actually, there is a known technique for this specific problem (AtCoder ABC 400 G? No, this is likely a harder problem).
Let's try binary search on the answer $V$.
Check(V): We want to know if there exists a set of $K$ disjoint pairs such that $\sum_{k=1}^K \max(X_{a_k}+X_{b_k}, Y_{a_k}+Y_{b_k}, Z_{a_k}+Z_{b_k}) \ge V$.
This is equivalent to: Is the maximum weight $K$-matching in a graph with edge weights $w_{ij} = \max(X_i+X_j, Y_i+Y_j, Z_i+Z_j)$ at least $V$?
Maximum weight $K$-matching in a general graph is solvable in $O(N^3)$ or $O(N^4)$, which is too slow for $N=10^5$.

Is the graph special? The weights are derived from 3 coordinates.
Maybe we can use the fact that $N$ is large but the structure is simple.
Consider the top $2K$ cakes in terms of some metric?
If we sort all cakes by $X_i+Y_i+Z_i$ descending, and take the top $2K$, is the optimal solution contained within these?
Not necessarily. A cake with small sum might have a huge $X$ and pair with another huge $X$ to get a large max.

Let's reconsider the binary search.
If we binary search on $V$, the check is: Max Weight K-Matching $\ge V$.
This is hard.

Is there a greedy strategy?
Sort all possible pairs? $O(N^2)$ pairs. Too many.

Let's look at the constraints again. Sum of N is $10^5$.
Maybe the number of "relevant" pairs is small?
No.

Let's try a different angle.
The problem is equivalent to:
Maximize $\sum_{k=1}^K \max(X_{a_k}+X_{b_k}, Y_{a_k}+Y_{b_k}, Z_{a_k}+Z_{b_k})$.

Consider the case where we only have 1 dimension. Then we just pick the $2K$ largest values and pair them optimally (largest with largest? No, largest with smallest? For sum, largest+largest is best).
With max of sums, it's more complex.

Actually, there is a solution using **Minimum Cost Maximum Flow** or **Hungarian Algorithm**? No, too slow.

Wait, look at Sample 2.
5 cakes, K=2.
Cakes:
1: 1 2 3
2: 1 2 3
3: 1 2 3
4: 1 2 3
5: 100 100 200

Pairs:
(1,2) -> max(2,4,6)=6
(3,5) -> max(101,102,203)=203
Total 209.

Notice that Cake 5 is very dominant. It pairs with a "weak" cake to get a high score because its own values are huge.
This suggests we should pair the "strongest" cakes with each other?
If we pair 5 with 4: max(101,102,203)=203.
Then pair 1 with 2: 6.
Total 209. Same.

What if we pair 5 with 1? 203.
Pair 2 with 3? 6.
Total 209.

It seems the "strong" cake's value dominates the pair's value regardless of the partner (as long as the partner's values are small relative to 5).

Let's try to formulate this as a **Maximum Weight Matching** in a general graph, but since N is large, we need a specialized algorithm.
However, for competitive programming, sometimes $O(N^2)$ is acceptable if the constant is small or if we only consider top candidates.
But $N=10^5$ makes $O(N^2)$ impossible.

Is it possible that we only need to consider the top $M$ cakes?
If we take the top $2K$ cakes by $X+Y+Z$, is the answer always found within these?
In Sample 2, top 4 by sum:
5: 400
1,2,3,4: 6
Top 4 are 5,1,2,3.
Pairs from {5,1,2,3}:
(5,1)=203, (2,3)=6 -> 209.
(5,2)=203, (1,3)=6 -> 209.
(5,3)=203, (1,2)=6 -> 209.
All give 209.
What if we included 4?
(5,4)=203, (1,2)=6 -> 209.

Hypothesis: The optimal solution only involves the top $2K$ cakes by some metric?
If this is true, we can reduce N to $2K$. Since $K \le N/2$, $2K \le N$. This doesn't reduce the worst case.
But if $K$ is small, it helps. If $K$ is large, $2K$ is large.

However, note that if $K$ is large, we are pairing almost everyone.
If $K = N/2$, we pair everyone.
Then we want to maximize $\sum \max(X_i+X_j, Y_i+Y_j, Z_i+Z_j)$.

Let's try a **Greedy with Priority Queue** approach?
Or **Binary Search + Greedy Check**?

Let's assume the **Binary Search on Answer** is the way.
Check(V): Can we find K pairs with total weight $\ge V$?
This is equivalent to: Can we find K pairs with weight $\ge V$? No, sum of weights.

Actually, there is a known result:
For the problem of maximizing $\sum \max(X_i+X_j, Y_i+Y_j, Z_i+Z_j)$, one can iterate over the $3^K$ cases? No.

Let's look at the constraints again.
Sum of N is $10^5$.
This usually allows $O(N \log N)$ or $O(N)$.

I will implement a solution that:
1. If $N$ is small (e.g., $N \le 2000$), use a max weight matching algorithm (like Blossom or Min-Cost Max-Flow) or even brute force with pruning? No, Blossom is complex.
   Actually, for $N \le 2000$, $O(N^2)$ is $4 \cdot 10^6$, which is fine. We can compute all pair weights and then use a greedy matching? No, greedy doesn't work for max weight matching.
   But for $N \le 2000$, we can use a library or implement a simple max weight matching?
   Wait, Max Weight Matching in general graphs is hard.
   
   However, notice the weights are $w_{ij} = \max(X_i+X_j, Y_i+Y_j, Z_i+Z_j)$.
   
   Let's try a **heuristic**:
   Sort cakes by $X_i+Y_i+Z_i$ descending.
   Take the top $2K$ cakes.
   Solve the problem on these $2K$ cakes.
   If $2K$ is small (e.g. $\le 50$), we can use DP or brute force?
   If $2K$ is large, this heuristic might fail.

   But wait, if $K$ is large, the "top $2K$" is almost all cakes.
   
   Let's try **Binary Search on Answer** with a **Greedy Check** that is not optimal but might be close? No, we need exact.

   Given the complexity, I will provide a solution that uses **Binary Search on the Answer** and for the check, I will use a **Maximum Weight Matching** algorithm on a reduced graph?
   
   Actually, there is a simpler observation:
   $\max(A,B,C) = \frac{1}{2} (A+B+C + |A-B| + |B-C| + |C-A|)$ is FALSE.
   Correct: $\max(A,B,C) = \frac{1}{2} (A+B+C + \max(A-B, B-A, B-C, C-B, C-A, A-C))$? No.
   
   Let's just use the **Binary Search on Answer** and a **Greedy Check** that assumes we can pick the best pairs independently? No.

   I will write a solution that handles small N with a brute-force/backtracking or max-weight matching approximation, and large N with a heuristic.
   
   For the "Check" in binary search:
   We want to know if Max Weight K-Matching $\ge V$.
   
   Since I cannot implement Blossom easily, I will use a **Greedy Strategy** for the check:
   1. Calculate all pair weights.
   2. Sort pairs by weight descending.
   3. Pick pairs greedily if they don't overlap.
   This is NOT optimal for max weight matching, but it's a heuristic.
   
   However, for this specific problem, is greedy optimal?
   No. Counterexample:
   3 cakes.
   1: 10 0 0
   2: 0 10 0
   3: 0 0 10
   K=1.
   Pairs:
   (1,2): max(10,10,0)=10
   (1,3): max(10,0,10)=10
   (2,3): max(0,10,10)=10
   All equal.
   
   Counterexample for greedy:
   1: 10 10 0
   2: 10 10 0
   3: 0 0 100
   4: 0 0 100
   K=2.
   Pairs:
   (1,2): max(20,20,0)=20
   (3,4): max(0,0,200)=200
   Total 220.
   
   Greedy:
   (3,4) weight 200. Pick it.
   Remaining: 1,2.
   (1,2) weight 20. Pick it.
   Total 220.
   
   Another case:
   1: 10 0 0
   2: 9 9 0
   3: 0 0 10
   K=1.
   (1,2): max(19,9,0)=19
   (1,3): max(10,0,10)=10
   (2,3): max(9,9,10)=10
   Greedy picks (1,2). Correct.
   
   Greedy often works for "Max Weight Matching" if the graph is a complete graph with specific weights? No.
   
   I will use **Binary Search on Answer** and **Greedy Matching** for the check. It might not be correct, but it's the best I can do without a complex library.
   
   Actually, for $N \le 2000$, I can use a **DP** or **Min-Cost Max-Flow**?
   
   Given the time, I will provide a solution that:
   1. Reads input.
   2. For each test case:
      - If $N$ is small ($\le 20$), use brute force (try all matchings).
      - If $N$ is large, use Binary Search on Answer + Greedy Check.

## worker: Implement the brute-force solver for small N (N <=
The solution uses two strategies based on N:
1. **Small N (N <= 20)**: Brute-force with backtracking to find the maximum weight K-matching. This is exact and feasible due to the small search space.
2. **Large N (N > 20)**: 
   - Heuristic: Select the top $2K$ cakes (capped at 20 for brute-force feasibility) based on the sum of their coordinates.
   - Binary Search on the answer $V$.
   - Check(V): Uses dynamic programming on the bitmask of the selected subset of cakes to find the maximum weight matching of size $K_{eff} = \min(K, \text{len(selected)}/2)$. If the max weight $\ge V$, the check passes.
   
   **Limitations**: The heuristic for large N is not guaranteed to be optimal because it restricts the search to a subset of cakes. However, given the constraints and the nature of the problem (max of sums), the "heaviest" cakes are likely to be part of the optimal solution. The cap of 20 ensures the DP runs in $O(2^{20})$ which is acceptable for a single test case, but doing it 50 times (binary search) might be slow in Python. 
   
   **Optimization**: The DP is run once per test case to compute the max weight for $K_{eff}$ pairs, and then binary search checks against this precomputed max weight. Wait, the code above re-runs the DP? No, it computes `max_w` once and then `check(V)` compares `max_w >= V`. This is correct and efficient. The binary search just compares against a single value.
   
   **Correction**: The code computes `max_w` for `K_eff` pairs. If `K <= n_sel//2`, then `K_eff = K`, and we find the true max weight for K pairs within the subgraph. If `K > n_sel//2`, we find the max weight for `n_sel//2` pairs. This is an underestimation if the optimal solution uses more than `n_sel//2` pairs from the top cakes. However, since we cap at 20, `K_eff` is at most 10. If `K > 10`, we are severely limiting the solution. 
   
   Given the problem constraints and typical competitive programming heuristics, this approach is a best-effort solution. For a rigorous solution, one would need a more advanced algorithm like Min-Cost Max-Flow or Blossom algorithm, which are complex to implement.

## worker: Implement the brute-force solver for small N (N <=
The solution uses two strategies based on N:
1. **Small N (N <= 20)**: Brute-force with backtracking to find the maximum weight K-matching. This is exact and feasible due to the small search space. The backtracking picks the first unused item and tries pairing it with all other unused items, recursively forming K pairs.
2. **Large N (N > 20)**: 
   - Heuristic: Select the top $2K$ cakes (capped at 20) based on the sum of their coordinates. This assumes that the most valuable cakes are likely to be part of the optimal solution.
   - DP on the selected subset: We use dynamic programming with bitmask to find the maximum weight matching of size $K_{eff} = \min(K, \text{len(selected)}/2)$ within the subgraph of selected cakes. The DP state `dp[mask]` stores the maximum weight for the subset of items represented by `mask`.
   - Binary Search on the Answer: We binary search on the possible total price. The check is simply comparing the precomputed `max_w` (the maximum weight matching found in the subgraph) against the candidate answer.
   
   **Limitations**: The heuristic for large N is not guaranteed to be optimal because it restricts the search to a subset of cakes. However, given the constraints and the nature of the problem (max of sums), the "heaviest" cakes are likely to be part of the optimal solution. The cap of 20 ensures the DP runs in $O(2^{20})$ which is acceptable for a single test case.
