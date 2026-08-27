This problem requires determining if we can cover the entire range $[1, N]$ using a subset of the given operations, where each operation covers either a specific interval $[L_i, R_i]$ or its complement. Since $N$ is large ($10^6$), we cannot simulate the array directly. Instead, we can model this as a set cover problem on intervals or use a greedy approach with a segment tree/coordinate compression to track uncovered positions. However, given the constraints and the nature of "complement" operations, a more efficient approach involves checking if the union of selected intervals covers $[1, N]$. We can iterate through the operations, treating them as potential covers. A key insight is that if we select an operation of type 2, it covers everything outside $[L_i, R_i]$. This suggests we can model the problem as finding a minimum set of operations such that their union is $[1, N]$. We can use a greedy strategy: maintain the current covered range $[1, R_{curr}]$. If $R_{curr} < N$, we look for an operation that starts at or before $R_{curr} + 1$ and extends as far right as possible. If we pick a type 2 operation, it covers $[1, L_i-1]$ and $[R_i+1, N]$. This complicates the simple greedy. A better approach is to consider the gaps. Initially, the gap is $[1, N]$. We need to cover all points. We can use a segment tree over the coordinates $1 \dots N+1$ to manage coverage. For each operation, we decide whether to include it based on whether it helps cover the leftmost uncovered point. Since we want to minimize cost, we prefer type 0 (cost 0) if it doesn't help, but we must pick operations to cover gaps. Actually, the problem asks for *any* valid assignment minimizing cost. We can formulate this as: for each operation, do we use it? If we use type 1, we cover $[L, R]$. If type 2, we cover $[1, L-1] \cup [R+1, N]$. We need the union to be $[1, N]$. This is equivalent to: the set of points NOT covered by type 1 operations must be covered by type 2 operations, and vice versa? No.
Let's reframe: We need $\bigcup_{i \in S_1} [L_i, R_i] \cup \bigcup_{j \in S_2} ([1, N] \setminus [L_j, R_j]) = [1, N]$.
This is equivalent to saying that for every point $p \in [1, N]$, either $p$ is in some $[L_i, R_i]$ (with $i \in S_1$) OR $p$ is not in some $[L_j, R_j]$ (with $j \in S_2$).
This looks like a 2-SAT or a flow problem, but simpler: we can process from left to right. Let `last_covered` be the rightmost point covered so far. Initially 0. We need to cover `last_covered + 1`. We find all operations that can cover `last_covered + 1`.
- Type 1: $[L, R]$ covers $p$ if $L \le p \le R$.
- Type 2: $[1, L-1] \cup [R+1, N]$ covers $p$ if $p < L$ or $p > R$.
If we pick a Type 1 operation covering $p$, it extends coverage to $\max(\text{current}, R)$.
If we pick a Type 2 operation covering $p$, it covers everything up to $L-1$ and everything from $R+1$ to $N$. This might jump over gaps.
Actually, the optimal strategy is likely greedy with backtracking or simply checking feasibility first. But since we need minimum cost, and costs are uniform (1 for non-zero), we just need the minimum number of non-zero operations.
Algorithm:
1. Identify the set of "critical" points that must be covered.
2. Use a greedy approach: find the first uncovered point $p$. Find all operations that cover $p$. Among those, pick the one that covers the largest range extending to the right (or effectively covers the most "future" gaps).
   - If we pick Type 1 $[L, R]$ where $L \le p \le R$, new covered range becomes $[1, \max(\text{prev\_end}, R)]$? No, Type 1 only covers $[L, R]$. It doesn't cover $[1, L-1]$.
   - If we pick Type 2 $[L, R]$, it covers $[1, L-1]$ and $[R+1, N]$.
This implies the covered set is not necessarily an interval. It can be a union of intervals.
However, notice that if we use a Type 2 operation, we cover the "outside". If we use Type 1, we cover the "inside".
Let's reverse the thinking: What points are *not* covered?
Initially, all points are uncovered.
We need to select a set of operations such that every point is covered by at least one selected operation.
This is a Set Cover problem where the universe is $[1, N]$ and sets are defined by the operations. Since $N$ is large, we can't run standard set cover.
But the sets have a specific structure.
Type 1 sets are intervals. Type 2 sets are complements of intervals.
Key Observation: If we select a Type 2 operation $(L, R)$, it covers $[1, L-1]$ and $[R+1, N]$. If we select a Type 1 operation $(L, R)$, it covers $[L, R]$.
Consider the gaps between selected Type 1 operations. Any point in a gap must be covered by a Type 2 operation.
Also, points covered by Type 2 operations might be covered by Type 1 operations too.
Let's try a greedy strategy from left to right.
Let `covered` be a boolean array (or a set of intervals) representing covered points.
Find the smallest uncovered index `p`.
If no such `p` exists, we are done.
Otherwise, we must pick an operation covering `p`.
Candidates:
1. Type 1: $(L, R)$ such that $L \le p \le R$.
2. Type 2: $(L, R)$ such that $p < L$ or $p > R$.
We want to pick one that maximizes the "progress".
Since Type 2 covers a prefix and a suffix, picking one might cover `p` and also cover everything up to $L-1$ and everything from $R+1$ to $N$.
If we pick Type 2, we cover $[1, L-1]$ and $[R+1, N]$. The only potential gap left is $(L-1, R+1)$ excluding the point $p$ itself? No, $p$ is in the gap if $L \le p \le R$. Wait, Type 2 covers $p$ if $p \notin [L, R]$. So if $p$ is uncovered, and we pick Type 2 $(L, R)$, then $p \notin [L, R]$. So either $p < L$ or $p > R$.
If $p < L$, then Type 2 covers $[1, L-1]$, which includes $p$ and everything up to $L-1$.
If $p > R$, then Type 2 covers $[R+1, N]$, which includes $p$ and everything from $R+1$ to $N$.
So, if we pick Type 2, we effectively fill a prefix or a suffix.
If we pick Type 1, we fill an interval containing $p$.
This looks like we can maintain the set of uncovered intervals. Initially $\{[1, N]\}$.
While there are uncovered intervals:
  Pick the leftmost uncovered interval $[a, b]$. Let $p = a$.
  We need to cover $p$.
  Options:
  - Pick Type 1 $(L, R)$ with $L \le p \le R$. This covers $[L, R]$. The new uncovered set is the union of $[a, b] \setminus [L, R]$ and other intervals. Since $a \le p \le R$, the part $[a, \min(b, R)]$ is covered. The remaining part of this interval is $[\min(b, R)+1, b]$ (if any).
  - Pick Type 2 $(L, R)$ with $p < L$ or $p > R$.
    - If $p < L$, then $[a, L-1]$ is covered. The remaining part is $[L, b]$.
    - If $p > R$, then $[R+1, b]$ is covered. The remaining part is $[a, R]$.
  We want to minimize the number of operations. This is equivalent to finding the minimum set cover.
  Given the structure, maybe we can just greedily pick the operation that covers the largest contiguous segment starting from $p$?
  Actually, since Type 2 operations cover disjoint parts (prefix/suffix), they are very powerful.
  Let's refine the greedy:
  Always look at the leftmost uncovered point $p$.
  Find all operations that cover $p$.
  Among them, choose the one that covers the largest range of *consecutive* points starting from $p$ to the right?
  Not necessarily consecutive, but extending the covered region as much as possible to the right.
  However, Type 2 might cover $[1, L-1]$ (which includes $p$) and $[R+1, N]$. If we pick this, the gap $[L, R]$ remains uncovered (unless covered by others).
  If we pick Type 1 $[L, R]$ containing $p$, it covers $[L, R]$.
  
  Let's try a different perspective.
  Total cost = number of non-zero ops.
  We can iterate $i$ from 1 to $M$. For each, decide op type.
  This is hard.
  
  Alternative: Coordinate compression + Segment Tree.
  Points of interest are $L_i, R_i+1$.
  We can maintain the coverage count on segments.
  But we need to *select* operations.
  
  Let's reconsider the "leftmost uncovered" greedy.
  Let `uncovered` be a list of disjoint intervals. Initially `[(1, N)]`.
  While `uncovered` is not empty:
    Take the first interval `[l, r]`. Let `p = l`.
    We need to cover `p`.
    Candidates:
      1. Type 1: $(L, R)$ where $L \le p \le R$.
         Effect: Covers $[L, R]$.
         Intersection with `[l, r]`: $[\max(l, L), \min(r, R)]$.
         Since $L \le p \le R$ and $p=l$, the intersection is $[l, \min(r, R)]$.
         The remaining part of `[l, r]` is $[\min(r, R)+1, r]$.
         We want to maximize the extension to the right, i.e., maximize $\min(r, R)$.
      2. Type 2: $(L, R)$ where $p < L$ or $p > R$.
         Case A: $p < L$. Covers $[1, L-1]$.
         Intersection with `[l, r]`: $[l, \min(r, L-1)]$.
         Remaining: $[\min(r, L-1)+1, r]$.
         We want to maximize $\min(r, L-1)$, i.e., maximize $L-1$ (so maximize $L$).
         Note: This also covers $[R+1, N]$, which might merge with other intervals or cover the whole right side.
         Case B: $p > R$. Covers $[R+1, N]$.
         Intersection with `[l, r]`: $[\max(l, R+1), r]$.
         Since $p=l > R$, $\max(l, R+1) = l$.
         So it covers $[l, r]$ completely? Yes, if $R < l$.
         Wait, if $p > R$, then $[R+1, N]$ covers $[l, r]$ entirely because $l \ge p > R$.
         So if there exists a Type 2 with $R < p$, we can cover `[l, r]` completely with 1 op.
         This is extremely powerful. If we have any Type 2 with $R < l$, we can finish the current interval `[l, r]` (and potentially cover everything to the right of $R$).
         
  Refined Greedy Strategy:
  Maintain a set of uncovered intervals. Initially `{[1, N]}`.
  Loop:
    Pick the leftmost uncovered interval `[l, r]`.
    Check if there is any Type 2 operation with $R_i < l$.
      If yes, pick the one with the largest $R_i$ (to cover as much as possible to the right, though any $R_i < l$ covers `[l, r]` fully).
      Actually, if we pick such a Type 2, it covers $[R_i+1, N]$. Since $R_i < l$, it covers $[l, N]$.
      So `[l, r]` is fully covered. And everything to the right of $R_i$ is covered.
      This might merge with other intervals.
      If we find such an operation, we should probably use it because it's very efficient (covers a suffix).
      But wait, does it cover the prefix $[1, R_i]$? No, it covers $[1, R_i-1]$? No, Type 2 covers $[1, L_i-1] \cup [R_i+1, N]$.
      If $R_i < l$, then $[R_i+1, N]$ covers $[l, N]$. The gap $[l, R_i]$? No, $R_i < l$, so the gap is $[1, R_i]$? No.
      The operation covers $[1, L_i-1]$ and $[R_i+1, N]$.
      The point $l$ is covered if $l \le L_i-1$ or $l \ge R_i+1$.
      If $R_i < l$, then $l \ge R_i+1$, so $l$ is covered.
      The interval `[l, r]` is covered.
      Does it help with other intervals? It covers $[R_i+1, N]$. This covers everything to the right of $R_i$.
      So if we have an uncovered interval `[l, r]` and we find a Type 2 with $R_i < l$, we can cover `[l, r]` and potentially merge it with the right side.
      However, we also need to cover the left side $[1, R_i]$? No, the operation covers $[1, L_i-1]$. If $L_i$ is small, it covers a prefix.
      
    Let's simplify.
    We need to cover $[1, N]$.
    We can maintain the current set of covered points.
    Since $N$ is large, we maintain a list of uncovered intervals.
    Algorithm:
    1. `uncovered` = `[(1, N)]`
    2. `ans` = array of 0s.
    3. While `uncovered` is not empty:
       a. Let `[l, r]` be the first interval in `uncovered`.
       b. Find best operation to cover `l`.
          Candidates:
          - Type 1: $(L, R)$ with $L \le l \le R$.
            Benefit: Covers $[l, \min(r, R)]$. Remaining: $[\min(r, R)+1, r]$.
            Score: $\min(r, R)$. (Maximize this).
          - Type 2: $(L, R)$ with $l < L$ or $l > R$.
            If $l > R$: Covers $[l, r]$ completely (since $l \ge R+1$).
              Benefit: Covers $[l, r]$. Remaining: empty.
              Score: $\infty$ (or just flag as "full cover").
            If $l < L$: Covers $[l, \min(r, L-1)]$. Remaining: $[\min(r, L-1)+1, r]$.
              Benefit: $\min(r, L-1)$.
              Score: $\min(r, L-1)$.
       c. Select the operation with the highest score.
          - If there's a Type 2 with $R < l$ (full cover), pick it.
          - Else, pick the one that maximizes the right endpoint of the covered segment within `[l, r]`.
          - If multiple, pick any (maybe prefer Type 2 if it covers more globally? But locally greedy should work).
       d. Apply the operation:
          - Mark `ans[i]` = type.
          - Update `uncovered`: remove the covered part of `[l, r]` and split if necessary.
          - Also, if the operation was Type 2 with $R < l$, it covers $[R+1, N]$. This might cover other intervals in `uncovered` that are to the right of $R$. We need to update `uncovered` to remove any interval that overlaps with $[R+1, N]$ (or $[1, L-1]$).
          - Similarly for Type 1, it only covers $[L, R]$.
          - For Type 2 with $l < L$, it covers $[1, L-1]$. This might cover intervals to the left of $l$? But `uncovered` is sorted, and we process left to right. If there are intervals to the left of `l`, they should have been processed already?
            Wait, if we pick a Type 2 that covers $[1, L-1]$ where $L-1 \ge l$, then it covers `l` and everything before it. But we are processing the *leftmost* uncovered interval. So there are no uncovered intervals to the left of `l`.
            However, if we pick a Type 2 with $l < L$, it covers $[1, L-1]$. This covers `l` and extends left. But since `l` is the leftmost uncovered, everything $< l$ is already covered. So the only new coverage is up to $L-1$.
            But wait, if we pick Type 2 with $l < L$, we cover $[l, L-1]$. The rest of `[l, r]` is $[L, r]$.
            Is it possible that this Type 2 covers some interval to the right? No, it covers $[R+1, N]$. If $R+1 \le r$, it covers the right part of `[l, r]`?
            No, if $l < L$, then $l \le L-1$. The condition for covering $p$ is $p < L$ or $p > R$.
            For $p \in [l, r]$, if $p < L$, it is covered.
            If $p > R$, it is covered.
            So the covered part of `[l, r]` is $[l, \min(r, L-1)] \cup [\max(l, R+1), r]$.
            Since $l < L$, the first part is $[l, \min(r, L-1)]$.
            The second part exists if $R+1 \le r$.
            So we might cover two disjoint parts of `[l, r]`.
            This complicates the "remaining" logic.
            
    Given the complexity of updating intervals, and the constraints, maybe there's a simpler property.
    Actually, the problem is small enough for a greedy with a segment tree or just careful interval management.
    But let's look at the constraints again. $N=10^6, M=2 \cdot 10^5$.
    An $O(M \log M)$ or $O(N)$ solution is needed.
    
    Let's try a simpler greedy:
    Iterate $i$ from 1 to $N$. If $i$ is uncovered, find an operation covering $i$ that extends the furthest to the right.
    But "extends to the right" is tricky with Type 2.
    However, note that if we use a Type 2 operation, we cover a suffix $[R+1, N]$. If we use it when we are at $i$, and $i > R$, we cover everything from $i$ to $N$. That's optimal.
    So, if there is any Type 2 with $R < i$, we should use it immediately?
    Yes, because it covers $[i, N]$.
    What if there are multiple? Any one works to cover $[i, N]$. We can pick the one that also covers a prefix $[1, L-1]$? No, we just need to cover $i$.
    But we want to minimize total ops. If we pick one, we cover $[i, N]$. Done with the right side.
    What about the left side? We still need to cover $[1, i-1]$.
    So the strategy:
    1. Find the first uncovered $i$.
    2. Check if there is a Type 2 with $R < i$.
       If yes, pick one (any, say the one with largest $L$ to maximize prefix coverage? Or just any).
       This covers $[i, N]$. Now we only need to cover $[1, i-1]$.
       But wait, the Type 2 also covers $[1, L-1]$. So it might cover some of $[1, i-1]$.
       So we should pick the Type 2 that maximizes $L-1$ (to cover the most of the left side).
       So: if exists Type 2 with $R < i$, pick the one with max $L$.
       Update covered range: $[1, L-1] \cup [i, N]$.
       The new uncovered part is $[L, i-1]$.
       If $L > i-1$, we are done.
       Else, set $i = L$.
    3. If no Type 2 with $R < i$, we must use Type 1 or Type 2 with $R \ge i$.
       If we use Type 2 with $R \ge i$, then $i \le R$. For $i$ to be covered, we need $i < L$.
       So we need Type 2 with $L > i$.
       If we pick such a Type 2, it covers $[1, L-1]$. Since $i < L$, $i$ is covered.
       It also covers $[R+1, N]$.
       So it covers $[1, L-1] \cup [R+1, N]$.
       The gap is $[L, R]$.
       Since $i < L$, the gap starts after $i$.
       So we cover $[i, L-1]$. The next uncovered is $L$.
       We want to maximize $L-1$, so maximize $L$.
       So: if exists Type 2 with $L > i$, pick the one with max $L$.
       Update covered: $[1, L-1] \cup [R+1, N]$.
       Next uncovered: $L$.
    4. If no Type 2 helps (either $R < i$ or $L > i$), we must use Type 1.
       We need Type 1 with $L \le i \le R$.
       We want to extend as far right as possible. Maximize $R$.
       Pick Type 1 with max $R$.
       Update covered: $[i, R]$.
       Next uncovered: $R+1$.
    
    This greedy strategy seems sound:
    At each step, find the first uncovered $i$.
    Try to cover $i$ using a Type 2 that covers a suffix starting at or before $i$ (i.e., $R < i$). This covers $[i, N]$. Among these, pick max $L$ to cover as much of $[1, i-1]$ as possible.
    If not possible, try Type 2 that covers a prefix ending after $i$ (i.e., $L > i$). This covers $[i, L-1]$. Pick max $L$.
    If not possible, use Type 1 covering $i$. Pick max $R$.
    
    Wait, is it possible that using a Type 1 now is better than a Type 2 later?
    Suppose we have $i$.
    Option A: Type 2 with $R < i$. Covers $[i, N]$ and $[1, L-1]$. Cost 1.
    Option B: Type 1 with $L \le i \le R$. Covers $[i, R]$. Cost 1.
    If we pick A, we cover $[i, N]$. We are left with $[L, i-1]$.
    If we pick B, we cover $[i, R]$. We are left with $[R+1, N]$ and potentially $[1, i-1]$ (if not covered by other ops).
    Clearly A is better because it covers the entire suffix $[i, N]$.
    So the priority should be:
    1. Type 2 with $R < i$ (covers suffix). Maximize $L$.
    2. Type 2 with $L > i$ (covers prefix up to $L-1$). Maximize $L$.
    3. Type 1 with $L \le i \le R$ (covers interval). Maximize $R$.
    
    Is there a case where picking a Type 2 with $L > i$ is worse than a Type 1?
    Type 2 with $L > i$ covers $[i, L-1]$. Type 1 covers $[i, R]$.
    If $L-1 < R$, Type 1 is better.
    So we should compare the "reach" of Type 2 (max $L-1$) vs Type 1 (max $R$).
    Actually, Type 2 with $L > i$ also covers $[R+1, N]$.
    So Type 2 covers $[i, L-1] \cup [R+1, N]$.
    Type 1 covers $[i, R]$.
    If we pick Type 2, we cover the suffix $[R+1, N]$. This is huge.
    So Type 2 with $L > i$ is very strong if $R$ is large.
    But we need to cover $i$.
    If we have a Type 2 with $R < i$, it covers $[i, N]$. This is definitely the best.
    If not, we have to cover $i$ with something that starts $\le i$.
    Candidates:
    - Type 1: $[L, R]$ with $L \le i \le R$.
    - Type 2: $[L, R]$ with $i < L$. (Covers $[i, L-1]$ and $[R+1, N]$).
    
    Comparison:
    Type 1 covers $[i, R]$.
    Type 2 covers $[i, L-1]$ and $[R+1, N]$.
    If $R_{type2} \ge i$, then $[R+1, N]$ is covered.
    The gap is $[L, R_{type2}]$.
    If we pick Type 1, the gap is $[R+1, N]$.
    So Type 2 is better if $[L, R_{type2}]$ is smaller than $[R+1, N]$?
    Actually, Type 2 covers the suffix $[R+1, N]$. Type 1 does not.
    So Type 2 is generally better if it exists, unless $L-1$ is very small and $R$ is very large?
    But Type 2 covers $[R+1, N]$. If $R$ is large, $[R+1, N]$ is small.
    If $R$ is small, $[R+1, N]$ is large.
    So Type 2 is good if $R$ is small (covers large suffix) or if $L$ is large (covers large prefix).
    Actually, the condition $i < L$ means $L \ge i+1$.
    The covered part is $[i, L-1]$.
    If we have a Type 1 with $R$ very large, it covers $[i, N]$.
    If we have a Type 2 with $R$ very small, it covers $[i, L-1]$ and $[R+1, N]$.
    If $R < i$, we already handled it.
    So assume $R \ge i$.
    Then Type 2 covers $[i, L-1]$ and $[R+1, N]$.
    Type 1 covers $[i, R]$.
    If $L-1 \ge R$, then Type 2 covers $[i, R]$ and $[R+1, N]$, i.e., $[i, N]$.
    So if $L-1 \ge R$, Type 2 is better.
    If $L-1 < R$, Type 2 covers $[i, L-1] \cup [R+1, N]$. Gap $[L, R]$.
    Type 1 covers $[i, R]$. Gap $[R+1, N]$.
    Which gap is smaller?
    Length of gap Type 2: $R - L + 1$.
    Length of gap Type 1: $N - R$.
    We prefer Type 2 if $R - L + 1 < N - R \iff 2R - L + 1 < N$.
    But we don't know $N$ relative to gaps? We know $N$.
    So we can compare the "remaining uncovered" length.
    However, the greedy step-by-step might be simpler:
    Just maintain the set of uncovered intervals.
    At each step, find the leftmost uncovered $i$.
    Find all operations that cover $i$.
    For each, calculate the new set of uncovered intervals.
    Pick the one that results in the smallest total length of uncovered intervals? Or the one that leaves the leftmost uncovered point as large as possible?
    Since we process left to right, maximizing the new leftmost uncovered point is the standard greedy for interval covering.
    Let's check if "maximize new leftmost uncovered" works.
    Current uncovered starts at $i$.
    Type 1 $[L, R]$ ($L \le i \le R$): New start is $\max(i, L) + \text{something}$? No, it covers $[i, R]$. New start is $R+1$.
    Type 2 $[L, R]$ ($i < L$): Covers $[i, L-1]$. New start is $L$. (Also covers $[R+1, N]$, but that's to the right).
    Type 2 $[L, R]$ ($R < i$): Covers $[i, N]$. New start is $N+1$ (done).
    
    So we want to maximize the new start point.
    Candidates:
    - Type 2 with $R < i$: New start $N+1$. (Best)
    - Type 2 with $L > i$: New start $L$.
    - Type 1 with $L \le i \le R$: New start $R+1$.
    
    So we compare:
    1. Max $L$ among Type 2 with $L > i$.
    2. Max $R+1$ among Type 1 with $L \le i \le R$.
    3. If any Type 2 with $R < i$ exists, pick that (effectively $N+1$).
    
    Wait, Type 2 with $L > i$ also covers $[R+1, N]$. Does this affect the "leftmost uncovered"?
    The leftmost uncovered becomes $L$. The part $[R+1, N]$ is covered, but since $L \le R+1$ (usually), the leftmost is still $L$.
    Unless $L > R+1$? No, $L \le R$.
    So the leftmost uncovered is determined by the rightmost point covered in the prefix.
    So the metric "maximize new leftmost uncovered" works perfectly.
    
    Algorithm:
    1. `uncovered_start` = 1.
    2. `ans` = [0]*M.
    3. While `uncovered_start` <= N:
       a. Find best op to cover `uncovered_start`.
          - `best_val` = -1, `best_idx` = -1, `best_type` = -1.
          - Check Type 2 with $R < uncovered\_start$:
             If exists, pick the one with max $L$.
             If found, `best_val` = N+1, `best_idx` = that op, `best_type` = 2.
          - Else, check Type 2 with $L > uncovered\_start$:
             Find max $L$. Let this be `max_L`.
             If `max_L` > `best_val`: `best_val` = `max_L`, `best_idx` = that op, `best_type` = 2.
          - Else, check Type 1 with $L \le uncovered\_start \le R$:
             Find max $R$. Let this be `max_R`.
             If `max_R + 1` > `best_val`: `best_val` = `max_R + 1`, `best_idx` = that op, `best_type` = 1.
       b. If no op found, return -1.
       c. Set `ans[op_idx]` = `best_type`.
       d. `uncovered_start` = `best_val`.
    4. Output result.
    
    Complexity:
    We iterate at most $N$ times? No, we jump.
    But we need to query efficiently.
    We can pre-sort operations.
    - List of Type 1: sorted by $L$.
    - List of Type 2: sorted by $L$ and $R$.
    Since $N$ is up to $10^6$, we can't iterate all ops.
    We need to query:
    - Max $L$ for Type 2 with $L > X$. (Suffix max).
    - Max $R$ for Type 1 with $L \le X \le R$. (Range max).
    - Max $L$ for Type 2 with $R < X$. (Prefix max).
    
    We can use Segment Trees or just arrays if we compress coordinates?
    Actually, since we only care about the values, we can precompute:
    - `max_L_type2_suffix[x]` = max $L$ for Type 2 with $L \ge x$.
    - `max_R_type1_range[x]` = max $R$ for Type 1 with $L \le x$ and $R \ge x$.
    - `max_L_type2_prefix[x]` = max $L$ for Type 2 with $R < x$.
    
    We can compute these arrays in $O(N + M)$.
    Steps:
    1. Initialize arrays of size $N+2$ with -1.
    2. For Type 1 ops: update `max_R_type1_range`?
       We need max $R$ for a given $x$ such that $L \le x \le R$.
       This is equivalent to: for a fixed $x$, consider all Type 1 with $L \le x$. Among those, we need $R \ge x$.
       We can store Type 1 ops in a list sorted by $L$.
       Or use a segment tree over $L$.
       Actually, simpler:
       Create an array `best_R_for_L` where `best_R_for_L[l]` = max $R$ for Type 1 with start $l$.
       Then for a query $x$, we want $\max \{ R \mid L \le x, R \ge x \}$.
       This is hard to do in $O(1)$ without more structure.
       But note: we only query at specific points `uncovered_start`.
       We can use a Segment Tree over the range $[1, N]$.
       Leaves represent positions.
       For Type 1 $(L, R)$: update range $[L, R]$ with value $R$? No.
       We want to query: max $R$ such that $L \le x \le R$.
       This is equivalent to: max $R$ among all Type 1 with $L \le x$ and $R \ge x$.
       We can maintain a segment tree where at index $L$, we store $R$.
       Query: max in range $[1, x]$. Let this be $M_R$.
       Then we need to check if $M_R \ge x$.
       If yes, then $M_R$ is a candidate.
       So:
       - Build a segment tree over $[1, N]$. Initialize with -1.
       - For each Type 1 $(L, R)$, update position $L$ with $R$ (maximize).
       - Query `max_R` = query_max(1, x).
       - If `max_R` >= x, then candidate is `max_R`.
       
    For Type 2:
    - We need max $L$ for $L > x$.
      Build segment tree over $[1, N]$. At index $L$, store $L$? No, we want max $L$.
      Just store $L$ at $L$. Query max in $[x+1, N]$.
    - We need max $L$ for $R < x$.
      Build segment tree over $[1, N]$. At index $R$, store $L$.
      Query max in $[1, x-1]$.
      
    So we need 3 segment trees (or one with different updates).
    Since $N=10^6$, $O(N)$ build and $O(\log N)$ per step.
    Number of steps? In worst case, we might cover 1 point at a time?
    But we always jump to at least $R+1$ or $L$.
    Is it possible to have $O(N)$ steps? Yes, if we cover 1 point each time.
    Then total time $O(N \log N)$. Acceptable.
    
    Implementation details:
    - Read N, M.
    - Store Type 1 ops: list of $(L, R)$.
    - Store Type 2 ops: list of $(L, R)$.
    - Build SegTree1 (for Type 1): size N+1. Update at $L$ with $R$. Query max in $[1, x]$.
    - Build SegTree2 (for Type 2 suffix): size N+1. Update at $L$ with $L$. Query max in $[x+1, N]$.
    - Build SegTree3 (for Type 2 prefix): size N+1. Update at $R$ with $L$. Query max in $[1, x-1]$.
    - Loop while `curr <= N`.
      - Query Type 2 prefix: `cand2_prefix = query3(1, curr-1)`. If valid, `val = cand2_prefix`.
      - Query Type 2 suffix: `cand2_suffix = query2(curr+1, N)`. If valid, `val = cand2_suffix`.
      - Query Type 1: `cand1 = query1(1, curr)`. If `cand1 >= curr`, `val = cand1 + 1`.
      - Pick max `val`.
      - If no candidate, -1.
      - Record op.
      - `curr = val`.
    
    Wait, for Type 2 prefix, we want max $L$ among Type 2 with $R < curr$.
    The query is max $L$ in range $[1, curr-1]$ of the tree storing $L$ at $R$.
    Correct.
    
    One edge case: multiple ops with same $L$ or $R$. We just need the index.
    We can store `(val, index)` in the segment tree.
    
    Final check on logic:
    - Type 2 with $R < curr$: covers $[curr, N]$. New start $N+1$.
      We want max $L$ to cover as much of $[1, curr-1]$ as possible?
      Actually, the greedy metric is "maximize new start".
      For Type 2 with $R < curr$, new start is $N+1$.
      For Type 2 with $L > curr$, new start is $L$.
      For Type 1, new start is $R+1$.
      So we compare $N+1$, $L$, $R+1$.
      $N+1$ is always the best.
      So if any Type 2 with $R < curr$ exists, we pick the one with max $L$?
      Wait, if we have multiple Type 2 with $R < curr$, they all give new start $N+1$.
      Does the choice of $L$ matter for future steps?
      No, because we jump to $N+1$ and stop.
      So any Type 2 with $R < curr$ is sufficient to finish.
      But we need to output the specific op.
      So if multiple, pick any? Or the one with max $L$?
      It doesn't matter for correctness, but let's pick max $L$ to be consistent.
      
    Wait, what if we have Type 2 with $R < curr$ AND Type 2 with $L > curr$?
    Type 2 with $R < curr$ gives $N+1$. Type 2 with $L > curr$ gives $L$.
    $N+1 > L$. So we prefer $R < curr$.
    
    So the priority is:
    1. Type 2 with $R < curr$. (Any, pick max $L$).
    2. Type 2 with $L > curr$. (Pick max $L$).
    3. Type 1 with $L \le curr \le R$. (Pick max $R$).
    
    This matches the logic.