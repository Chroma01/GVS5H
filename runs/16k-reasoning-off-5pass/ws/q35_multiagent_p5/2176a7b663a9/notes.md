
## ideation
The core difficulty lies in efficiently determining connectivity and minimum weight paths in a graph with $O(N^2)$ potential edges. The key insight is that the graph's structure is determined by the geometric arrangement of intervals. Specifically, two intervals are connected if they are disjoint. This implies that if we sort intervals by their left endpoints, connectivity is largely determined by whether the "gap" between the rightmost endpoint of a left-group and the leftmost endpoint of a right-group is non-empty.

1.  **Component Identification**: We can determine connected components by sorting intervals by their left endpoints ($L_i$). We iterate through the sorted intervals, maintaining the maximum right endpoint ($max\_R$) seen so far. If the current interval's $L_i$ is greater than $max\_R$, it means there is a gap between the previous set of intervals and the current one. This indicates a new connected component. All intervals in a contiguous range of the sorted list that don't have such a gap belong to the same component.
2.  **Minimum Weight Path Logic**:
    *   If $s$ and $t$ are in different components, the answer is -1.
    *   If they are in the same component:
        *   Check if they are directly connected. Two intervals $[L_s, R_s]$ and $[L_t, R_t]$ are disjoint (and thus directly connected) if $R_s < L_t$ or $R_t < L_s$.
        *   If directly connected, the minimum weight path is simply $W_s + W_t$.
        *   If not directly connected, any path must go through at least one intermediate node. The optimal path will be $s \to k \to t$ where $k$ is a node in the same component that is disjoint from both $s$ and $t$. To minimize weight, we should pick the node $k$ with the minimum weight in the component. However, we must ensure such a $k$ exists that is disjoint from both.
        *   Actually, a stronger property holds: In a connected component of this specific graph (complement of interval overlap graph), if two nodes are not directly connected, they are connected via a "hub". The best hub is the node with the global minimum weight in the component, *provided* it is disjoint from both $s$ and $t$. If the global minimum node overlaps with $s$ or $t$, we might need the next best. But wait, is it always possible to go through the global min?
        *   Let's refine: The graph is the complement of the interval intersection graph. The connected components of the interval intersection graph are well-defined. The complement graph's connectivity is related.
        *   Actually, a simpler observation for the complement graph: If the union of intervals in a component is "dense" (no large gaps), the component is likely a clique or close to it. If there are gaps, the component splits.
        *   Correct approach for min weight:
            *   Find the component ID for $s$ and $t$. If different, return -1.
            *   Check direct connection: `disjoint(s, t)`. If yes, ans = $W_s + W_t$.
            *   If not directly connected, we need a path of length 2 (3 vertices). The best such path is $s \to k \to t$. We need a $k$ such that $k$ is disjoint from $s$ AND $k$ is disjoint from $t$. To minimize $W_s + W_k + W_t$, we need the minimum $W_k$ among all such valid $k$.
            *   Is it sufficient to just take the global minimum weight node in the component? Not necessarily, because the global min node might overlap with $s$ or $t$.
            *   However, note that if $s$ and $t$ are not directly connected, they overlap. If the component has more than 2 nodes, there likely exists a node disjoint from both.
            *   Actually, we can precompute for each component the minimum weight node. Let $min\_W$ be the minimum weight in the component. Let $idx\_min$ be its index.
            *   If $idx\_min$ is disjoint from $s$ and $t$, then the answer is $W_s + W_{min} + W_t$.
            *   If $idx\_min$ overlaps with $s$ or $t$, we need the next best. But checking all nodes is too slow.
            *   Alternative: The graph is very dense. If $s$ and $t$ are not directly connected, they are "close". The best intermediate node is likely one that is "far" from them.
            *   Actually, we can observe that if the component size is large, the probability that the global min is disjoint from both is high. But we need a deterministic answer.
            *   Let's reconsider the structure. The connected components of the *overlap* graph are intervals of the sorted array. The complement graph connects nodes that are "far apart" in the sorted order.
            *   Key realization: If $s$ and $t$ are in the same component, and not directly connected, then there exists a node $k$ in the component such that $k$ is disjoint from $s$ and $k$ is disjoint from $t$? Not always. But if the component is connected, the diameter is small.
            *   Actually, a known result for this problem (often seen in competitive programming): The minimum weight path between $s$ and $t$ in this graph is $\min(W_s + W_t, W_s + W_{min\_comp} + W_t)$ if they are not directly connected? No, if they are not directly connected, the direct edge doesn't exist. So we must use an intermediate. The best intermediate is the one with min weight that is disjoint from both.
            *   However, if the global min node $m$ is disjoint from $s$, and disjoint from $t$, then $W_s + W_m + W_t$ is a candidate.
            *   What if $m$ overlaps $s$? Then we can't use $m$ as the intermediate for $s \to m \to t$. But maybe $s \to m$ is not an edge.
            *   Let's check if $s$ and $t$ are directly connected. If yes, ans = $W_s + W_t$.
            *   If no, we look for the best $k$. The best $k$ is the one with min weight in the component that is disjoint from $s$ and $t$.
            *   Since $N$ is large, we cannot check all $k$.
            *   Insight: The nodes disjoint from $s$ are those with $R_k < L_s$ or $L_k > R_s$. In the sorted order, these are prefixes and suffixes.
            *   We can precompute the minimum weight in the prefix and suffix of the component's sorted interval list.
            *   So, for a component, we have the sorted intervals. We can build a Segment Tree or just prefix/suffix min arrays for the weights in the sorted order of the component.
            *   For a query $(s, t)$:
                1. Check if same component. If not, -1.
                2. Check if directly connected. If yes, $W_s + W_t$.
                3. If not, find min weight node in the component that is disjoint from $s$ and $t$.
                   - Disjoint from $s$: $R_k < L_s$ or $L_k > R_s$.
                   - Disjoint from $t$: $R_k < L_t$ or $L_k > R_t$.
                   - So $k$ must satisfy: $(R_k < L_s \lor L_k > R_s) \land (R_k < L_t \lor L_k > R_t)$.
                   - This breaks into 4 cases:
                     a) $R_k < \min(L_s, L_t)$
                     b) $L_k > \max(R_s, R_t)$
                     c) $R_k < L_s \land L_k > R_t$
                     d) $L_k > R_s \land R_k < L_t$ (Impossible if $L_s \le R_s$ and $L_t \le R_t$ and intervals are valid, unless $R_t < L_s$ which is case a/b essentially? No, case c and d are for "crossing" gaps. But if $s$ and $t$ overlap, then $L_s \le R_t$ and $L_t \le R_s$. So $R_k < L_s$ and $L_k > R_t$ implies $R_k < L_s \le R_t < L_k$, so $R_k < L_k$, which is valid. This corresponds to a gap between $s$ and $t$ if they are ordered? No, if they overlap, there is no single gap between them. But there could be a gap elsewhere in the component.)
                   - Actually, since the component is contiguous in the sorted order, the nodes disjoint from $s$ are a prefix (small $R$) and a suffix (large $L$). Same for $t$.
                   - The intersection of "disjoint from $s$" and "disjoint from $t$" will be a prefix, a suffix, or potentially two middle segments if the "disjoint" regions overlap in the middle? No, disjoint from $s$ is $(-\infty, L_s) \cup (R_s, \infty)$ in terms of position? No, it's based on interval values.
                   - In the sorted array (by $L$), the condition $R_k < X$ defines a prefix. The condition $L_k > Y$ defines a suffix.
                   - So, the set of valid $k$ is the union of:
                     1. Prefix where $R_k < \min(L_s, L_t)$
                     2. Suffix where $L_k > \max(R_s, R_t)$
                     3. Prefix where $R_k < L_s$ AND Suffix where $L_k > R_t$? No, this is not a contiguous segment in the sorted array necessarily.
                     4. However, note that if $s$ and $t$ overlap, then $\min(L_s, L_t) \le \max(R_s, R_t)$.
                     5. The condition "disjoint from $s$ AND disjoint from $t$" is equivalent to:
                        - $R_k < \min(L_s, L_t)$ OR
                        - $L_k > \max(R_s, R_t)$ OR
                        - ($R_k < L_s$ AND $L_k > R_t$) OR
                        - ($R_k < L_t$ AND $L_k > R_s$)
                     6. The last two cases represent a "middle" gap. But in a sorted list by $L$, if $L_k > R_t$ and $R_k < L_s$, this implies $L_k > R_t \ge L_t$ and $R_k < L_s$. This requires a gap between $t$ and $s$ if $t$ is to the left of $s$?
                     7. Actually, we can just query the minimum weight in the component for indices satisfying these conditions. Since the conditions define prefixes and suffixes of the sorted component array, we can use prefix-min and suffix-min arrays.
                     8. What about the "middle" cases? If $s$ and $t$ overlap, can there be a $k$ such that $R_k < L_s$ and $L_k > R_t$? This implies $L_k > R_t \ge L_t$ and $R_k < L_s$. If $L_t \le R_t < L_s$, then $t$ is to the left of $s$. Then $k$ is to the right of $t$ and left of $s$? No, $L_k > R_t$ means $k$ starts after $t$ ends. $R_k < L_s$ means $k$ ends before $s$ starts. So $k$ is in the gap between $t$ and $s$. This is a valid interval. Is it possible? Yes. But in the sorted order, such a $k$ would be between $t$ and $s$.
                     9. However, if the component is connected, there are no gaps in the "union of intervals" sense that split the component. But individual intervals can exist in gaps.
                     10. Crucially, if such a $k$ exists, it must be in the component. And we can find the min weight in the range of indices corresponding to this gap?
                     11. This is getting complicated. Let's simplify.
                     12. Most cases: The best $k$ is either in the prefix (small $R$) or suffix (large $L$). The "middle" cases are rare or covered by the fact that if a gap exists between $s$ and $t$, the nodes in that gap are disjoint from both.
                     13. We can precompute for each component:
                         - `pref_min[i]`: min weight in `comp[0...i]`
                         - `suff_min[i]`: min weight in `comp[i...end]`
                     14. For a query, we identify the range of indices in the sorted component that satisfy $R_k < \min(L_s, L_t)$. This is a prefix. We take `pref_min` at the last index of this prefix.
                     15. Similarly for $L_k > \max(R_s, R_t)$, this is a suffix. We take `suff_min` at the first index.
                     16. For the middle cases: If $L_s > R_t$, then the gap between $t$ and $s$ contains indices. We can find the range of indices in the component that fall in $(R_t, L_s)$. But wait, if $L_s > R_t$, then $s$ and $t$ are disjoint! So we would have taken the direct edge case.
                     17. Therefore, if $s$ and $t$ are NOT directly connected, they overlap. This means $L_s \le R_t$ and $L_t \le R_s$.
                     18. In this case, the conditions $R_k < L_s$ and $L_k > R_t$ imply $R_k < L_s \le R_t < L_k$, so $R_k < L_k$, which is fine, but it requires $L_k > R_t \ge L_t$ and $R_k < L_s$. This means $k$ is to the right of $t$ and to the left of $s$? No, $L_k > R_t$ means $k$ starts after $t$ ends. $R_k < L_s$ means $k$ ends before $s$ starts. This implies $t$ is to the left of $k$ and $k$ is to the left of $s$. So $t, k, s$ are ordered. But if $t$ and $s$ overlap, can there be a $k$ between them? Yes, if the overlap is partial and there's a gap? No, if they overlap, their union is connected. But $k$ could be in a gap if the component has "holes".
                     19. However, if $s$ and $t$ overlap, then $\min(L_s, L_t) \le \max(R_s, R_t)$. The condition $R_k < \min(L_s, L_t)$ is a prefix. The condition $L_k > \max(R_s, R_t)$ is a suffix.
                     20. What about $R_k < L_s$ and $L_k > R_t$? This requires $L_s > R_t$. But if $s$ and $t$ overlap, we don't necessarily have $L_s > R_t$. We have $L_s \le R_t$ OR $L_t \le R_s$.
                     21. If $L_s \le R_t$ and $L_t \le R_s$, then the interval $[L_s, R_s]$ and $[L_t, R_t]$ overlap.
                     22. The condition for $k$ to be disjoint from both is:
                         - $R_k < \min(L_s, L_t)$ OR
                         - $L_k > \max(R_s, R_t)$ OR
                         - ($R_k < L_s$ AND $L_k > R_t$) -> This implies $L_s > R_t$.
                         - ($R_k < L_t$ AND $L_k > R_s$) -> This implies $L_t > R_s$.
                     23. If $s$ and $t$ overlap, then it is NOT the case that ($L_s > R_t$ AND $L_t > R_s$). It is possible that $L_s > R_t$ is false, or $L_t > R_s$ is false.
                     24. If $L_s > R_t$, then $s$ is to the right of $t$. But if they overlap, this is impossible? No, if $L_s > R_t$, then $s$ starts after $t$ ends, so they are disjoint.
                     25. Therefore, if $s$ and $t$ are NOT directly connected, they overlap, which implies $L_s \le R_t$ AND $L_t \le R_s$.
                     26. This means $L_s \ngtr R_t$ and $L_t \ngtr R_s$.
                     27. Consequently, the conditions ($R_k < L_s$ AND $L_k > R_t$) and ($R_k < L_t$ AND $L_k > R_s$) are IMPOSSIBLE to satisfy simultaneously with the overlap constraint?
                         - If $L_s \le R_t$, then $L_k > R_t \implies L_k > L_s$. And $R_k < L_s$. So $R_k < L_s \le R_t < L_k$. This is a valid interval $k$ that lies in the gap between $s$ and $t$? No, $s$ and $t$ overlap. There is no gap between them that contains an interval disjoint from both?
                         - Example: $s=[1,5], t=[4,8]$. Overlap.
                         - $k$ disjoint from $s$: $R_k < 1$ or $L_k > 5$.
                         - $k$ disjoint from $t$: $R_k < 4$ or $L_k > 8$.
                         - Intersection:
                           - $R_k < 1$ (Prefix)
                           - $L_k > 8$ (Suffix)
                           - $R_k < 1$ AND $L_k > 8$ (Impossible)
                           - $R_k < 4$ AND $L_k > 5$ -> $R_k < 4$ and $L_k > 5$. This implies $L_k > 5 > R_k$, so $L_k > R_k$, valid. This corresponds to intervals in the gap $(5, 4)$? No, gap is empty? No, $5 < 4$ is false. Wait. $R_k < 4$ and $L_k > 5$. This requires $L_k > 5$ and $R_k < 4$. This is impossible for a valid interval ($L \le R$).
                     28. So, if $s$ and $t$ overlap, the only valid $k$ are those in the prefix ($R_k < \min(L_s, L_t)$) or suffix ($L_k > \max(R_s, R_t)$).
                     29. Therefore, we only need to check the prefix min and suffix min of the component.

## worker: Implement the component identification by sorting 
1.  **Component Identification**: The graph's connected components are determined by sorting intervals by their left endpoints ($L_i$). A new component starts when the current interval's $L_i$ is strictly greater than the maximum $R_i$ of all previous intervals in the sorted order. This is because if $L_i > \max(R_{prev})$, there is a gap, and no interval in the previous set can be disjoint from an interval in the current set (and vice versa) in a way that connects the two sets into a single component in the complement graph.
2.  **Direct Connection**: Two vertices $s$ and $t$ are directly connected if their intervals are disjoint, i.e., $R_s < L_t$ or $R_t < L_s$. If so, the minimum weight path is simply $W_s + W_t$.
3.  **Indirect Connection**: If $s$ and $t$ are in the same component but not directly connected, they must overlap. The minimum weight path will be of the form $s \to k \to t$. The weight is $W_s + W_k + W_t$. To minimize this, we need the minimum weight $W_k$ among all nodes $k$ in the same component that are disjoint from both $s$ and $t$.
4.  **Finding Optimal $k$**: A node $k$ is disjoint from both $s$ and $t$ if:
    *   $R_k < \min(L_s, L_t)$ (k is to the left of both)
    *   OR $L_k > \max(R_s, R_t)$ (k is to the right of both)
    *   (Other cases like $k$ being between $s$ and $t$ are impossible if $s$ and $t$ overlap, as shown in the reasoning).
5.  **Efficient Querying**:
    *   For each component, we maintain two sorted structures:
        *   Nodes sorted by $R_i$ with a prefix-min array of weights. This allows us to quickly find the minimum weight node with $R_k < X$ using binary search.
        *   Nodes sorted by $L_i$ with a suffix-min array of weights. This allows us to quickly find the minimum weight node with $L_k > Y$ using binary search.
    *   For each query, we perform two binary searches to find the best candidate $k$ from the "left" and "right" sets, and take the minimum weight.
