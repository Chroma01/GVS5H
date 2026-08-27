1. **Understand f(L,R)**: The operation allows us to erase a contiguous range of *positions* on the blackboard if every value in that position range appears at least once. However, the key insight is that this process is equivalent to finding the minimum number of "groups" we can partition the subarray into, where each group consists of values that can be erased together. Actually, a better interpretation: The operation erases all occurrences of values that are present in positions `l` through `r`. This is complex. Let's re-read carefully.
   
   Actually, there's a known result for this type of problem. The minimum number of operations to erase the array is equal to the number of "connected components" of values if we consider the interval [L,R] and the values present. More precisely, if we look at the set of distinct values in A[L..R], say S, and we consider the first and last occurrence of each value in S within A[L..R], the problem reduces to finding the minimum number of intervals needed to cover these occurrences such that each interval contains all values it "claims". 
   
   A simpler characterization: `f(L,R)` is the number of times we must split the subarray. It turns out that `f(L,R)` is equal to the number of "connected components" in the following sense: Consider the values in A[L..R]. Two positions are in the same component if they are connected via shared values. Specifically, if we define a graph where nodes are indices in [L,R] and edges connect indices that share the same value, then `f(L,R)` is the number of connected components? No, because one operation can erase multiple disjoint sets of indices if they form a contiguous block of positions.
   
   Let's look at the example: `1, 3, 1, 4`. 
   - Op 1: erase positions 1-1 (value 1). Remaining: `3, 1, 4` at original positions 2,3,4? No, the blackboard shrinks. The problem says "erase all integers from l through r that are on the blackboard". The blackboard is a sequence. If we erase positions 1 to 1, we remove the first element. The blackboard becomes `3, 1, 4`. Then we choose l=2, r=3 (values 3 and 4? No, positions 2 and 3 in the *current* blackboard are 1 and 4. Wait. The example says: "Choose (l,r)=(3,4) and erase all occurrences of 3 and 4". This implies the indices refer to the *original* positions or the current blackboard? "Write ... on the blackboard in order". "Choose integers l, r ... erase all integers from l through r that are on the blackboard". This usually means positions in the current blackboard.
   
   However, there is a well-known competitive programming problem with this exact statement. The answer `f(L,R)` is equal to the number of distinct values in A[L..R] minus the number of "merges" we can perform. Actually, it is known that `f(L,R)` is the number of connected components of the interval graph defined by the values. 
   
   **Key Insight**: `f(L,R)` is equal to the number of "blocks" if we merge overlapping intervals of value occurrences. For each value `v` present in `A[L..R]`, let `first(v)` and `last(v)` be its first and last occurrence in `A[L..R]`. We have a set of intervals `[first(v), last(v)]`. The minimum number of operations is the number of connected components of the union of these intervals.
   
   Let's verify with `1, 3, 1, 4` (L=1, R=4).
   Values: 1 (pos 1,3), 3 (pos 2), 4 (pos 4).
   Intervals: `[1,3]` for 1, `[2,2]` for 3, `[4,4]` for 4.
   Union of `[1,3]` and `[2,2]` is `[1,3]`. `[4,4]` is separate.
   Components: `[1,3]` and `[4,4]`. Count = 2. Matches `f(1,4)=2`.
   
   So the problem reduces to: For each subarray `A[L..R]`, compute the number of connected components of the union of intervals `[first_occurrence(v), last_occurrence(v)]` for all distinct `v` in `A[L..R]`.
   
   We need to sum this over all `L,R`.
   
   We can iterate `R` from 1 to N and maintain the state for all `L`. As we increase `R`, we add `A[R]`. This updates the interval for `A[R]` (if it existed before, the interval extends; if not, a new interval starts). We need to efficiently update the number of connected components.
   
   The number of connected components of a set of intervals can be computed as: `(# of intervals) - (# of overlaps/merges)`. Or more simply, if we sort the intervals, the number of components is `1 + sum(1 if interval i doesn't overlap with previous)`.
   
   Alternatively, `f(L,R) = (number of distinct values in A[L..R]) - (number of pairs of adjacent values in the sorted-by-start-time interval list that merge)`. This is tricky.
   
   Better approach: The number of connected components is `K`. We can maintain the set of active intervals for the current `R` as `L` varies. As `L` decreases, we add more values. This seems hard to do for all `L`.
   
   Let's fix `R` and vary `L`. As `L` goes from `R` down to 1, we add `A[L]`. If `A[L]` has been seen before in `A[L+1..R]`, its interval extends to the left. This might merge two existing components or extend one.
   
   We can use a Disjoint Set Union (DSU) or a segment tree to maintain the components. However, since we are summing over all `L`, we can use a sweep-line.
   
   Actually, there is a simpler formula:
   `f(L,R) = 1 + sum_{v in distinct(A[L..R]), v != A[L]} I(v's interval starts after L and merges with something)`? No.
   
   Let's use the property: `f(L,R) = (number of distinct values) - (number of merges)`.
   A merge happens when a new interval overlaps with an existing component.
   
   We can iterate `R` from 1 to N. We maintain an array `comp_count[L]` which stores `f(L,R)`.
   When moving from `R` to `R+1`, we introduce `A[R+1]`.
   Let `prev = last_pos[A[R+1]]`.
   If `prev` is undefined, we start a new interval `[R+1, R+1]`. This increases the number of distinct values by 1. Does it increase components? It adds a new interval. If this interval doesn't overlap with any existing interval for a given `L`, it adds 1 to the component count. But for small `L`, it might overlap.
   
   This is complex. Given the constraints and problem type, a known solution involves maintaining the "next occurrence" and using a segment tree to track the number of components.
   
   Specifically, `f(L,R)` can be computed by tracking the "rightmost" end of the current component.
   
   Let's try a different angle. The number of connected components of intervals `[l_v, r_v]` is equal to the number of indices `i` in `[L,R]` such that `i` is the start of a new component. An index `i` starts a new component if `A[i]` is the first occurrence of that value in the current set of intervals AND it doesn't overlap with the previous component.
   
   Actually, `f(L,R)` is equal to the number of `i` in `[L,R]` such that `A[i]` has not appeared in `A[L..i-1]` OR its previous occurrence was not connected to the current component.
   
   Standard solution:
   1. Precompute `prev[i]` = previous occurrence of `A[i]`, and `next[i]` = next occurrence.
   2. For a fixed `R`, as we decrease `L`, we add `A[L]`.
   3. We can maintain the answer for all `L` using a segment tree.
   
   Let `ans[L]` be `f(L,R)`. When we move `R` to `R+1`:
   - Let `v = A[R+1]`.
   - Let `p = prev_occurrence[v]` (the last index `< R+1` where `v` appeared).
   - If `p` exists, the interval for `v` was `[p, R]` (effectively, or rather, the component containing `p` now extends to `R+1`).
   - The new interval is `[R+1, R+1]` but it connects to the component containing `p`.
   - If the component containing `p` already extends to some `R_max`, it now extends to `R+1`.
   - This might merge two components if there was a gap? No, intervals are defined by first and last.
   
   Actually, the number of components decreases by 1 if the new element `A[R+1]` connects two previously disjoint components, or increases by 0 if it extends an existing component, or increases by 1 if it starts a new isolated component.
   
   Wait, if `A[R+1]` is a new value, it starts a new interval `[R+1, R+1]`. This adds 1 to the distinct count. It forms a new component unless it overlaps with an existing one. It overlaps if there is a value `u` in `A[L..R]` such that `first(u) <= R+1 <= last(u)`. Since `last(u) <= R`, this is only possible if `first(u) <= R+1` which is always true for `L <= first(u)`. But the interval for `u` is `[first(u), last(u)]`. It overlaps with `[R+1, R+1]` only if `last(u) >= R+1`, which is false since `last(u) <= R`. So a new value always starts a new component?
   
   NO. The intervals are `[first(v), last(v)]` within `A[L..R]`.
   If we add `A[R+1]`, and `v` was already present, its interval becomes `[first(v), R+1]`. This might merge with other intervals that overlap with `[first(v), R+1]`.
   
   Correct Logic:
   Maintain for each `L` the set of intervals.
   Instead, maintain the number of components.
   `f(L,R) = f(L,R-1) + delta`.
   
   Let's use the property: `f(L,R)` is the number of `i` in `[L,R]` such that `A[i]` is the first occurrence of `A[i]` in `A[L..R]` AND `A[i]` is not "connected" to the previous component.
   
   Given the complexity, I will delegate the implementation of the sweep-line with a segment tree to the workers.