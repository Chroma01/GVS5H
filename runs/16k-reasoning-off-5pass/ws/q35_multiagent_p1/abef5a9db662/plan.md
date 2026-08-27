The key observation is that the rating change in each contest depends on whether the current rating falls within $[L_i, R_i]$. Since the rating only increases, we can model the final rating as $X + \text{total\_increase}(X)$, where $\text{total\_increase}(X)$ is the number of contests $i$ such that the rating at the time of contest $i$ is in $[L_i, R_i]$. However, the rating at contest $i$ depends on previous increases, making direct simulation per query too slow ($O(NQ)$).

Instead, we can use a difference array (or sweep-line) approach. Notice that for a fixed initial rating $X$, the rating after $k$ contests is $X + f_k(X)$, where $f_k(X)$ is the number of increases in the first $k$ contests. The condition for contest $i$ to increase the rating is $L_i \leq X + f_{i-1}(X) \leq R_i$. This is complex because $f_{i-1}(X)$ depends on $X$.

A better approach: Since the maximum rating is bounded ($5 \times 10^5$), we can precompute the answer for all possible initial ratings $X \in [1, 5 \times 10^5]$. We simulate the process for all $X$ simultaneously. We maintain an array `rating` of size $500002$ where `rating[x]` is the current rating of someone who started with $x$. Initially, `rating[x] = x`. For each contest $i$, we iterate over all $x$ and check if `rating[x]` is in $[L_i, R_i]$. If so, increment `rating[x]`. However, this is $O(N \cdot \max\_R)$ which is $2 \times 10^5 \times 5 \times 10^5 = 10^{11}$, too slow.

Alternative: Use a segment tree or Fenwick tree to track which initial ratings $X$ are currently in a range. But the ranges shift.

Actually, note that the function $g(X) = \text{final rating for initial } X$ is non-decreasing. Moreover, the increase is the count of $i$ such that $L_i \leq \text{rating at step } i \leq R_i$. 

Let's use the fact that the maximum rating is $5 \times 10^5$. We can process the contests and maintain for each possible current rating value, how many initial ratings $X$ have that current rating. But this is still complex.

Correct efficient approach: 
We can compute the answer for all $X$ by processing the contests and using a difference array on the "increase" count. Let $A[X]$ be the total increase for initial rating $X$. Initially $A[X] = 0$. For each contest $i$, we want to add 1 to $A[X]$ for all $X$ such that the current rating of $X$ (which is $X + A[X]$ before contest $i$) is in $[L_i, R_i]$. This is a range update on $X$ but the condition is on $X + A[X]$, which is not a simple range.

However, we can use a segment tree with lazy propagation to maintain the values $X + A[X]$ and support range queries. But updates are not range-based in $X$.

Actually, there's a simpler insight: The final rating for initial $X$ is $X + \sum_{i=1}^N [L_i \leq X + \text{increases before } i \leq R_i]$. 

Given the constraints, we can use a **sweep-line with a Fenwick tree** or **segment tree** to count for each $X$ how many contests apply. But the dependency is sequential.

Let's reconsider: Since $N, Q$ are large and ratings are up to $5 \times 10^5$, we can precompute the answer for all $X \in [1, 500000]$ by simulating all contests but using a **difference array technique on the "current rating distribution"**. 

Actually, we can process each contest and update a data structure that tells us for each initial $X$, whether it gets a point. We can use a **segment tree** where each leaf $X$ stores the current rating of initial $X$. For each contest $[L, R]$, we want to find all $X$ such that current rating of $X$ is in $[L, R]$ and increment their rating. This is a "range set" or "range increment" but on a non-contiguous set of $X$. 

This is a known problem. The solution is to use a **DSU (Disjoint Set Union)** or **linked list** to skip over ratings that are not in the range. Specifically, we can maintain for each rating value $v$, the next rating value $> v$ that is "active". But here, multiple $X$ can map to the same current rating.

Standard solution: Use a **segment tree** that supports:
1. Query: Find all $X$ such that current rating is in $[L, R]$.
2. Update: Increment current rating for those $X$.

But this is still complex. 

Simpler: Since the maximum rating is $5 \times 10^5$, we can use a **difference array** on the "number of times a rating value $v$ is incremented". Let $cnt[v]$ be the number of initial ratings $X$ that have current rating $v$. Initially, $cnt[v] = 1$ if $v \in [1, 500000]$, else 0. For each contest $[L, R]$, the number of people who get incremented is $\sum_{v=L}^R cnt[v]$. Then, we need to move these people from rating $v$ to $v+1$. This is a shift operation. We can use a **Fenwick tree** to maintain $cnt$ and support range sum and point updates. But shifting is $O(N \cdot \max\_R)$ if done naively.

However, we can use a **lazy propagation segment tree** to handle the shifts. Or, we can use a **difference array** for the shifts. 

Actually, the standard solution for this problem is to use a **segment tree with lazy propagation** where each node stores the minimum and maximum current rating in its range, and we recursively update. But this is $O(N \log (\max\_R))$.

Given the time, I'll implement the **DSU-based skipping** method:
- Maintain an array `next_rating[v]` which points to the next rating value $> v$ that has at least one person. Initially, `next_rating[v] = v+1` for all $v$.
- Also maintain `cnt[v]` = number of people with current rating $v$.
- For each contest $[L, R]$:
  - Start from $v = L$.
  - While $v \leq R$:
    - If `cnt[v] > 0`, then all `cnt[v]` people get incremented. So, `cnt[v+1] += cnt[v]`, `cnt[v] = 0`.
    - Use DSU to jump to the next non-empty rating: `v = find(v)`.
    - But we need to update the DSU structure when `cnt[v]` becomes 0.

This is $O(N \cdot \alpha(\max\_R))$ which is efficient.