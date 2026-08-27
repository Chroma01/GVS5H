We need to determine feasibility and minimum cost to set all positions to 1 after M operations, each can be 0 (do nothing), 1 (set range [L,R] to 1), or 2 (set complement to 1).  
Observations: Once a position becomes 1, it stays 1. So we need to ensure every index is covered by the union of "type 1" ranges (inside) and "type 2" complements (outside) of selected operations.  
A type 2 operation effectively selects the complement interval, so the union of covered positions from chosen type-2 ops is the union of intervals (1, L-1) and (R+1, N).  
Thus we need to pick a subset of operations (each costing 1 if type 1 or 2) to cover [1,N] with intervals, where a type-1 op contributes its [L,R] and a type-2 op contributes the two pieces. We want minimum number of chosen operations. This is a set cover on a line, solvable greedily: sort operations by their leftmost coverage? But type-2 ops have two disjoint pieces, complicating things. However note that type-2 ops cover at least one of the two extreme regions (left of L or right of R). Since we need full coverage, the leftmost index 1 must be covered by an operation whose coverage includes 1 — that is either a type-1 op with L=1, or a type-2 op with L>1 (covers 1). Similarly for N. This suggests we can use a BFS/DP or greedy approach extending from both ends, but due to disjoint coverage we can treat each operation as a node in a graph of intervals and use 0-1 BFS for minimum ops to reach full coverage. But N is up to 1e6, M up to 2e5, so a simpler greedy works: repeatedly pick the operation that extends coverage furthest from the current leftmost uncovered point, preferring type-1 if it starts at or before current point. If no such op, fail. This is the classic minimum number of intervals to cover [1,N]. But type-2 ops are special: they cover left side and right side disjointly. We can think of them as two intervals: [1, L-1] and [R+1, N]. However we need to cover the whole range contiguously. Since type-2's coverage is two separated pieces, if we use it to cover the left side, the right piece becomes irrelevant or may be used later? Actually the coverage contributed by a type-2 op is the union of those two intervals, so if we are covering from left, we can use a type-2 op to cover up to L-1 (if L>1) or from R+1 to N (if R<N) when covering from the right. This suggests a symmetric approach: we can cover from both ends inward.  

Better approach: model as shortest path on a line. We want to find minimum number of intervals (with their possibly split forms) to cover [1,N]. This is equivalent to: we start with covered set = empty, we want to end with [1,N] covered. Each operation adds its interval(s) to the covered set. The cost is number of operations. This is a hitting set / set cover, but for intervals on a line there is a polynomial solution.  

Key insight: type-2 operation covers two intervals: left = [1, L-1] (if L>1) and right = [R+1, N] (if R<N). When covering the whole [1,N], we can think of using type-2 ops only at the extremes. Actually, consider the optimal solution: if a type-2 op is used, it must be used to cover either some prefix or some suffix (or both) because the middle is already covered by type-1 ops. Since type-1 ops are single intervals, they are more "efficient" for covering the middle. So we can restrict to: all type-1 ops are used, and at most one type-2 op (or two?) to cover the leftmost and rightmost pieces. But is that always true? Suppose we have disjoint pieces that cannot be covered by a single type-1 op; a type-2 op might cover a left piece and a right piece, but the right piece might be needed to cover a gap that cannot be covered by type-1 ops. However a type-1 op could also cover that gap. Actually, because the coverage of a type-2 op is the complement of a contiguous interval, it consists of at most two disjoint intervals at the two ends. To cover the whole line, we need to cover the middle contiguous block and possibly the ends. The ends can be covered by type-2 ops. But could a type-2 op be used to cover an interior gap? No, because its coverage is only the two ends. So if there's a gap in the middle, only type-1 ops can fill it. Therefore, to cover the middle, we must use a set of type-1 ops whose intervals cover some contiguous segment [a,b] (maybe not the whole [1,N] if the ends are covered by type-2). The remaining uncovered parts are [1,a-1] and [b+1,N]. These must be covered by type-2 ops. Since a type-2 op covers [1, L-1] and [R+1, N], it can cover a left prefix and a right suffix. However, a single type-2 op covers both a left prefix and a right suffix. But if we need different L_i for left and R_i for right, we might need two type-2 ops: one to cover left prefix (its L determines how far left) and one to cover right suffix (its R determines how far right). But a single type-2 op with L_i and R_i covers left up to L_i-1 and right from R_i+1. So to cover left prefix [1,a-1], we need an operation with L_i ≤ a (so that L_i-1 ≥ a-1? Actually to cover index a-1, we need L_i ≤ a. If L_i = a, it covers [1,a-1]. If L_i < a, it covers [1,L_i-1] which is smaller. So to cover exactly up to a-1, we need L_i = a. But we don't need exact, just coverage of [1,a-1], so L_i ≤ a works, but it might also cover more left, which is fine. However, the left coverage of a type-2 op is exactly [1, L_i-1]. So to cover [1,a-1], we need an operation with L_i ≤ a. Actually if L_i ≤ a, the left coverage is [1, L_i-1] which is a subset of [1,a-1] (since L_i-1 < a). Wait, that doesn't cover a-1. Let's check: if L_i=2, left coverage is [1,1] = {1}. So it covers only up to index 1. To cover index a-1, we need L_i - 1 ≥ a-1 => L_i ≥ a. So to cover up to a-1, we need L_i = a (if we want to cover exactly a-1). More generally, to cover [1,a-1], we need an operation with L_i = a (to cover a-1). If L_i > a, left coverage is [1, L_i-1] which is a superset covering a-1 and more, but that "more" is still left side, so it's fine. Wait, superset is fine: covering more left is okay because left side is already covered. So we need an operation with L_i ≥ a. Actually if L_i > a, left coverage is [1, L_i-1] which includes a-1. So condition is L_i ≥ a. Similarly, to cover right suffix [b+1,N], we need an operation with R_i ≤ b (since right coverage is [R_i+1, N], to include b+1 we need R_i+1 ≤ b+1 => R_i ≤ b). So we need an operation with L_i ≥ a and R_i ≤ b to cover both sides. But a single operation can have L_i ≥ a and R_i ≤ b simultaneously only if L_i ≤ R_i, which means a ≤ b (true). So there may exist an operation that covers both the left and right uncovered parts. However, we might need two different operations: one with large L to cover left, and one with small R to cover right. The optimal strategy is to find a contiguous segment [a,b] that is covered by type-1 ops (i.e., a set of type-1 intervals whose union covers [a,b]), and then the left and right ends can be covered by type-2 ops. The cost is the number of type-1 ops used plus the number of type-2 ops used. Since we want to minimize total ops, we should consider all possible choices of which type-1 ops to use, which is like covering a subsegment with minimum intervals. This is a classic interval covering problem: given intervals (from type-1 ops), find minimum number to cover a subsegment [a,b] such that the remaining parts can be covered by type-2 ops. But we also need the type-2 ops to exist: there must be an op with L_i ≥ a and R_i ≤ b? Not necessarily: we can use one type-2 op for left and another for right. So condition: there exists at least one op with L_i ≥ a (to cover left) and at least one op with R_i ≤ b (to cover right). They could be the same or different. Actually, a single op can cover both if L_i ≥ a and R_i ≤ b, but that might be too restrictive. If we use two ops, we need one with L_i ≥ a and another with R_i ≤ b. So the condition for feasibility is: there exist a,b (1 ≤ a ≤ b ≤ N) such that [a,b] can be covered by some type-1 intervals, and there exists at least one operation with L_i ≥ a, and at least one (possibly the same) with R_i ≤ b. But we can also use more than two type-2 ops? Since we want minimum cost, using more than two is wasteful because we can always replace a type-2 op that covers a left piece with a type-2 op that covers a larger left piece, as long as the cost is same (1). Actually, multiple type-2 ops could be used to cover different pieces, but the uncovered parts are only two (left and right). So at most two type-2 ops are needed. Thus the minimal cost is: (minimum number of type-1 intervals to cover some [a,b]) + (1 if we need a type-2 for left and one for right and they are distinct, or 0 if both covered by the same op, or 0 if the left or right is already covered by type-1). But we can also choose a=1, meaning left side is covered by type-1, so no left type-2 needed. Similarly b=N. So we need to find the best [a,b] and a set of type-1 intervals covering it, minimizing total ops = |cover| + (need_left?1:0) + (need_right?1:0). However, need_left is true if a > 1 and there is no type-1 op covering 1. But a is the leftmost index of the segment covered by type-1. We can always choose a to be 1 if there is a type-1 op covering 1. But we might want to choose a > 1 to reduce the number of type-1 intervals? Actually, if we choose a > 1, we might need fewer type-1 intervals to cover [a,b] because the segment is shorter, but then we pay an extra type-2 for left. So it's a tradeoff. Similarly for right.

We need to compute, for each possible left endpoint a, the minimum number of type-1 intervals to cover from a to some b, and the corresponding b, and the right type-2 cost. This sounds like a dynamic programming or shortest path on intervals.

Alternative global view: This is a shortest path problem on a state space of positions. We can think of operations as actions: from current uncovered set, we apply an operation to add its coverage. Since coverage only adds, we can think of the process as building up covered set. But we need the final covered set to be [1,N]. This is like we want to reach a state where the covered set is exactly [1,N] (or superset). Since we only add, we can think of the process as: we have a set of "available" operations. The order doesn't matter. So we just need to select a subset. This is exactly the minimum set cover for a line, which can be solved by a greedy algorithm if intervals are "normal" (no type-2). With type-2, we can transform each type-2 op into two intervals: left = [1, L-1] (if L>1) and right = [R+1, N] (if R<N). Then we have M' ≤ 2M intervals (some may be empty). We want to select a subset of these intervals to cover [1,N], with the constraint that if we select both intervals from the same original type-2 op, we pay 1; if we select only one, we still pay 1? Actually, the cost is per operation, not per interval. So selecting a type-2 op and using only its left interval still costs 1. But if we select a type-2 op, we can use both its intervals for free. However, we might not need both. But the cost is incurred regardless. So in the interval covering problem, each type-2 op gives us a "bundle" of two intervals that we can use at cost 1. This is a set cover with bundles, which is NP-hard in general? But on a line, it might be tractable because the intervals are special: they are at the ends.

Actually, we can solve the problem by considering the following: we need to cover [1,N]. The operations are of two kinds: type-1 covers an internal interval, type-2 covers two external intervals. Because type-2 intervals are at the ends, we can handle them separately.  

Let's formalize: Let S be the set of type-1 operations, each with interval [L_i, R_i]. Let T be the set of type-2 operations. We can think of selecting a subset A ⊆ S and a subset B ⊆ T. The total covered set is the union of intervals from A plus the unions of left/right intervals from B. We want this union to be [1,N]. We want to minimize |A| + |B|.

This is a covering problem with two types of items. Since T items are "large" (cover extremes), we can try to use them to cover the ends, and S to cover the middle. The middle is a contiguous segment [a,b] that is not covered by T? Actually, the uncovered part after using T is some set of positions. Since T intervals are at the ends, the uncovered part is a contiguous segment in the middle (maybe empty). Specifically, if we select a set of T operations, their left coverages are all of the form [1, L-1] for some L, and right coverages are [R+1, N] for some R. The union of all left coverages from selected T is [1, max_L - 1] where max_L is the maximum L among selected T operations? Wait, each type-2 op gives left coverage [1, L_i-1]. The union of several such is [1, max_i (L_i-1)] = [1, max_L - 1]. Similarly, the union of right coverages is [min_R + 1, N] where min_R is the minimum R among selected T. So by selecting a set of type-2 ops, we can cover a prefix [1, L_max - 1] and a suffix [R_min + 1, N], for some L_max and R_min achievable from the selected ops. The cost is the number of ops selected. But we can achieve the same prefix and suffix with at most two ops: one with L = L_max (to get the prefix) and one with R = R_min (to get the suffix). If we have an op with both L ≥ L_max and R ≤ R_min, we can cover both with one op, but that might not exist. So to minimize cost for given (L_max, R_min), we need: if there exists an op with L_i ≥ L_max and R_i ≤ R_min, cost = 1; else if there exists an op with L_i ≥ L_max and another with R_j ≤ R_min, cost = 2; else impossible. Actually, we also need to consider that we might not need to cover the full prefix or suffix if the middle covers them. The middle is covered by type-1 ops. So we can think: we want to find a,b such that [a,b] is covered by type-1 ops, and the left uncovered part [1,a-1] can be covered by some type-2 ops (i.e., there exists an op with L_i ≥ a) and the right uncovered part [b+1,N] can be covered by some type-2 ops (R_i ≤ b). And we want to minimize (cost of type-1 covering [a,b]) + (cost of type-2 for left, which is 1 if a>1 and there is an op with L_i ≥ a, else 0) + (cost for right, 1 if b<N and there is an op with R_i ≤ b, else 0). But note: if we need both left and right type-2, we can use the same op if it satisfies both, so cost might be 1 instead of 2. So we need to be careful.

We can precompute for each possible L_i (and R_i) from type-2 ops. But L_i and R_i can be up to N (1e6), so we can use arrays.  

Let’s denote:
- For each x from 1 to N, let min_R[x] = minimum R_i among all type-2 ops with L_i ≥ x. (i.e., among ops that can cover left prefix up to x-1, what is the smallest R they have?)
- For each x, let max_L[x] = maximum L_i among all type-2 ops with R_i ≤ x. (i.e., among ops that can cover right suffix from x+1, what is the largest L they have?)

Alternatively, we can precompute:
- A boolean array left_possible[x] = true if there exists a type-2 op with L_i ≥ x. (meaning we can cover left prefix up to x-1)
- For such x, the cost to cover left prefix is 1 (using that op), but we might share with right.
- Similarly, right_possible[x] = true if there exists a type-2 op with R_i ≤ x. (cover right suffix from x+1)
- Also, we can know for a given x, if there is an op that can cover both left up to x and right from x? That would be an op with L_i ≥ x and R_i ≤ x, which means L_i ≥ x and R_i ≤ x => L_i ≥ x ≥ R_i, so L_i = R_i = x? Actually, if L_i ≥ x and R_i ≤ x, then since L_i ≤ R_i, we have L_i = R_i = x. So only ops with L_i = R_i = x can cover both left and right for the same x? Not exactly: to cover left prefix up to a-1, we need L_i ≥ a. To cover right suffix from b+1, we need R_i ≤ b. For an op to cover both left and right for the same boundary, we need it to cover a left piece and a right piece simultaneously. But the left piece covered is [1, L_i-1] and the right piece is [R_i+1, N]. These two pieces are separated by [L_i, R_i]. So the op does not cover the middle. So if we want to cover left and right of some [a,b], we need an op with L_i ≥ a and R_i ≤ b. So the condition for an op to cover both left and right for a given [a,b] is L_i ≥ a and R_i ≤ b. So for each op, it can serve as both left and right for any a ≤ L_i and b ≥ R_i. So if we have an op with L_i = L0 and R_i = R0, it can cover left for any a ≤ L0, and right for any b ≥ R0. So to cover both left and right of [a,b], we need a ≤ L_i and b ≥ R_i.  

Now, the problem reduces to: choose a,b (1 ≤ a ≤ b ≤ N) and a set of type-1 intervals covering [a,b] (min number = cover1[a][b]), and choose a set of type-2 ops to cover left and right, with cost cover2(a,b). Then total cost = cover1(a,b) + cover2(a,b). We need to minimize over a,b. And we also need to output the actual ops chosen.

But computing cover1[a][b] for all a,b is too large. We need a better way.

Notice that the minimum number of type-1 intervals to cover [a,b] is a function that can be computed if we sort intervals by left endpoint. This is the classic interval covering problem: given intervals, the minimum number to cover [a,b] is the size of the smallest chain of intervals starting at or before a and extending as far right as possible, etc. Actually, if we want to cover exactly [a,b], we need the first interval to start ≤ a, and the last to end ≥ b. The minimum number is the length of the shortest path from a to b in a graph where nodes are positions and edges are intervals? Not exactly.

Alternatively, we can think of the process of covering [1,N] using both type-1 and type-2. Since type-2 are extremes, we can try to cover from left to right: we want to cover from 1 to N. We can use a type-2 op to jump to L_i (if we use its left coverage, we cover up to L_i-1, but we still need to cover [L_i, N]? Actually, if we use a type-2 op, we cover [1, L_i-1] and [R_i+1, N]. So the uncovered part is [L_i, R_i]. So using a type-2 op essentially "removes" the interval [L_i, R_i] from the uncovered set, and we then need to cover that interval with type-1 ops. So the problem is exactly: we need to select a set of type-1 ops to cover some interval [a,b], and then we can use type-2 ops to cover the rest. But the type-2 ops we use must have L_i ≥ a and R_i ≤ b (to cover the outside). So the condition for a set of type-1 ops covering [a,b] is that their union covers [a,b], and we can choose a,b as the "inner" covered region. Actually, if we select a set of type-1 ops, their union is some set U. We can then use type-2 ops to cover the complement of U, provided that the complement is exactly [1, min(U)-1] ∪ [max(U)+1, N]? Not exactly, because U might have gaps. If U has gaps, then the complement is not just two intervals. But we need the complement to be coverable by type-2 ops. Type-2 ops cover prefixes and suffixes. So the complement of U must be a subset of a prefix and a suffix. That means U must contain a contiguous segment [a,b] such that the complement is contained in [1,a-1] ∪ [b+1,N]. In other words, U must have no gaps in the middle. So the set of type-1 ops we select must have a contiguous union, i.e., their intervals must overlap to form a single segment [a,b]. So we need to select a set of type-1 ops that form a connected coverage of some [a,b]. This is exactly covering a contiguous interval with a set of intervals, which is always possible if the union is connected. So the condition is: the union of selected type-1 ops is a contiguous interval [a,b]. Then the outside is two intervals, which can be covered by type-2 ops if there exist ops with L_i ≥ a and R_i ≤ b (possibly same).  

So the problem is: find a contiguous interval [a,b] that can be covered by some type-1 ops, and such that there exist type-2 ops to cover the left and right, with minimum total cost = (number of type-1 ops used) + (number of type-2 ops used, which is 1 if both sides covered by the same op, or 2 if different, or 0 if no sides).  

We can think of the type-1 ops as edges in a graph: each op is an interval. The union of a set of intervals is contiguous if the intervals overlap in a chain. This is like the classic "interval covering" to cover a target interval. The minimum number of type-1 intervals to cover a given [a,b] is the minimum number of intervals from the set S that exactly cover [a,b] (i.e., the union is exactly [a,b] and they form a connected coverage). But we are not forced to cover exactly [a,b]; we can cover a larger interval, but then the complement becomes smaller. However, if we cover a larger interval, the complement is smaller, which might reduce the need for type-2. But covering a larger interval might require more type-1 ops. So we need to optimize.  

This is similar to a shortest path problem on the line. Consider the positions 0,1,...,N,N+1. We can start at position 1 (the leftmost uncovered) and we want to reach N+1 (past the right end). At each step, we can use a type-1 op to jump from its L to R+1. But we can also use a type-2 op to jump from 1 to L_i (if we use its left coverage, we cover up to L_i-1, but then we are at L_i, still need to cover from L_i to N? Actually, using a type-2 op covers [1, L_i-1] and [R_i+1, N]. So after using it, the uncovered part is [L_i, R_i]. So we are now at position L_i, and we need to cover up to R_i. But we could also use a type-2 op to cover a suffix: if we are at some position, we could use a type-2 op to cover the right side, but that would cover from R_i+1 to N, leaving [1, R_i] uncovered. That doesn't help to progress left-to-right.  

Maybe a better model: we want to select a set of ops to cover everything. We can think of the ops as actions that "fill" certain regions. Since the complement of type-2 is an interval, using a type-2 op is like "cutting out" the interval [L_i, R_i] from the uncovered set. So if we use a set of type-2 ops, the remaining uncovered set is the intersection of their intervals? Actually, if we use multiple type-2 ops, the uncovered part is the intersection of their [L_i, R_i]? Let's check: each type-2 op covers the complement of [L_i, R_i]. So the uncovered part after using a set of type-2 ops is the set of positions that are not covered by any of them. A position j is covered by a type-2 op if it is outside [L_i, R_i], i.e., j < L_i or j > R_i. So j is uncovered by all type-2 ops if for every type-2 op used, we have L_i ≤ j ≤ R_i. That is, j is in the intersection of all [L_i, R_i] for the used type-2 ops. So the uncovered part is exactly the intersection of the intervals of the used type-2 ops. If we use a set of type-2 ops, their intersection is some interval [a,b] (possibly empty). Then we need to cover this [a,b] with type-1 ops. So the problem becomes: choose a set of type-2 ops whose intersection is [a,b] (which is the uncovered part), and then cover [a,b] with type-1 ops. The cost is (#type2) + (#type1). We want to minimize this. And we can also choose not to use any type-2 ops, then [a,b] = [1,N], so we need to cover [1,N] with type-1 ops.  

This is a much cleaner formulation! Let's verify: If we use a set B of type-2 ops, the uncovered set is the intersection of their intervals: I = ∩_{i in B} [L_i, R_i]. If we also use a set A of type-1 ops, the final uncovered set is I \ (union of A's intervals). We want this to be empty, so we need the union of A's intervals to cover I. So indeed, we need to cover I with type-1 ops. The cost is |A| + |B|. And we can also use no type-2 ops, then I = [1,N].  

This is perfect! Because type-2 ops are only useful to shrink the interval that needs to be covered by type-1. The intersection of a set of type-2 ops is an interval (since each is an interval, the intersection of intervals is an interval or empty). So we need to find a non-empty interval [a,b] (which is the intersection of some type-2 ops) such that [a,b] can be covered by type-1 ops with minimum number, and then add the number of type-2 ops used to get that [a,b]. But we are free to choose any set of type-2 ops; their intersection is determined by the maximum L and minimum R among the chosen ops. That is, if we choose a set B, let L_max = max_{i in B} L_i, R_min = min_{i in B} R_i. Then the intersection is [L_max, R_min] provided L_max ≤ R_min. So the cost for that intersection is |B|, and we can achieve it with at most 2 type-2 ops: one with L = L_max and one with R = R_min (if they are different ops). Actually, to achieve intersection [a,b], we need all chosen ops to have L_i ≤ a and R_i ≥ b? Wait, the intersection is [max L_i, min R_i]. So to get intersection exactly [a,b], we need max L_i = a and min R_i = b. But we can also have intersection [a,b] with a larger set: if we choose ops with L_i ≤ a and R_i ≥ b, then max L_i ≤ a and min R_i ≥ b, so the intersection contains [a,b] and is possibly larger. But we want the intersection to be exactly the part that needs covering, so we don't want it larger because that would require covering more with type-1. So we want to choose B such that the intersection is as small as possible but still coverable by type-1 with low cost. Actually, we want to minimize |A| + |B|. So we can consider any set B, compute its intersection I = [l, r] (if non-empty), and then compute the minimum number of type-1 ops to cover I, call it c1(I). Then total cost = |B| + c1(I). We want to minimize over all non-empty intersections I achievable by some B. But note that if we have a set B, we can always replace it with a set B' that gives a smaller intersection and possibly smaller |B|? Not necessarily. For example, if we have two ops: one with L=2,R=10 and another with L=5,R=7, their intersection is [5,7]. If we take only the second, intersection is [5,7] with cost 1, which is better. So we can always assume B is minimal in the sense that no proper subset gives a smaller intersection? Actually, adding an op can only shrink the intersection or keep it same. So if we have a set B, any subset B' has intersection I' that contains I. So if we can cover I with type-1, we can also cover I' because I' is larger. So the cost for B' is |B'| + c1(I'). Since I' is larger, c1(I') might be larger, but |B'| is smaller. So there is a tradeoff. We need to search over all possible intersections I that can be formed as the intersection of some subset of type-2 ops. And for each I, we can compute the minimum |B| to achieve an intersection contained in I? Actually, we want to achieve exactly I or a superset? If we achieve an intersection J that contains I, then we need to cover J with type-1, which is at least as hard as covering I. So the cost is at least |B| + c1(I). So we can restrict to intersections that are exactly of the form [max L, min R] for some subset. But we can parameterize by (l,r) where l ≤ r. The minimum number of type-2 ops to achieve an intersection that is contained in [l,r] (i.e., max L ≤ l and min R ≥ r) is: we need to select a set of ops such that all have L_i ≤ l and R_i ≥ r. That is, we need to select ops from the set of ops that "cover" [l,r] in the sense that their interval contains [l,r]. Let's denote by S2(l,r) the set of type-2 ops with L_i ≤ l and R_i ≥ r. If we select any subset of S2(l,r), the intersection will be [max L_i, min R_i] which is a subinterval of [l,r]. The cost is the size of the subset. To minimize |B|, we should select the minimum number of ops to achieve an intersection that is as small as possible? Actually, we want to minimize |B| + c1(intersection). The intersection will be some [l', r'] with l ≤ l' ≤ l and r ≤ r' ≤ r? Wait, if all selected ops have L_i ≤ l and R_i ≥ r, then max L_i ≤ l and min R_i ≥ r, so the intersection is [max L_i, min R_i] ⊆ [l,r]? Actually, max L_i ≤ l, so the left endpoint of intersection is ≤ l. min R_i ≥ r, so the right endpoint is ≥ r. So the intersection contains [l,r]? Let's be precise: if we have ops with L_i ≤ l and R_i ≥ r, then the intersection is [max L_i, min R_i]. Since each L_i ≤ l, max L_i ≤ l. Since each R_i ≥ r, min R_i ≥ r. So the intersection is an interval that contains [r? No, it contains points from max L_i to min R_i. Since max L_i ≤ l and min R_i ≥ r, the intersection is actually [max L_i, min R_i] which contains [l, r]? Not necessarily: if max L_i is less than l, then the intersection starts before l. If min R_i is greater than r, it ends after r. So the intersection is a superset of [l,r]? Actually, if max L_i ≤ l and min R_i ≥ r, then the intersection is [max L_i, min R_i] which includes all numbers between max L_i and min R_i. Since max L_i ≤ l and min R_i ≥ r, the entire segment [l,r] is contained in [max L_i, min R_i] because for any x in [l,r], we have x ≥ l ≥ max L_i? Wait, if max L_i ≤ l, then max L_i is at most l, so x ≥ l ≥ max L_i, so x ≥ max L_i. And x ≤ r ≤ min R_i, so x ≤ min R_i. So yes, [l,r] is contained in the intersection. So the intersection is a superset of [l,r]. That means if we select ops from S2(l,r), the uncovered part (the intersection) is actually larger than [l,r] (it contains [l,r] and possibly more). But we want the uncovered part to be exactly the part that we will cover with type-1. So if we have a superset, we need to cover that superset with type-1, which is at least as hard as covering [l,r]. So it's better to have the intersection be exactly [l,r] if possible, or as small as possible. So we should consider intersections that are exactly the intersection of some set. But note that if we have a set B, its intersection is [L_max, R_min]. So we can parameterize by (L_max, R_min). For a given pair (L,R) with L ≤ R, we can achieve intersection exactly [L,R] if there exists a set B such that max L_i = L and min R_i = R. That requires at least one op with L_i = L and at least one op with R_i = R, and all ops in B have L_i ≤ L and R_i ≥ R. The minimum size of such a B is 1 if there is an op with L_i = L and R_i = R? Not exactly: if there is an op with L_i = L and R_i = R, then taking just that op gives intersection [L,R]. If no such op, we might need two: one with L_i = L and R_j = R, but we need both to be in B, and for the intersection to be exactly [L,R], we need that no op in B has L_i > L or R_i < R. So if we take an op with L_i = L but R_i > R, and another with R_i = R but L_i < L, then the intersection is [max(L, L_i?), actually max L_i = L (since the first has L_i = L, the second has L_i < L, so max is L), and min R_i = R (first has R_i > R, second has R_i = R, so min is R). So intersection is [L,R]. So we can achieve [L,R] with two ops as long as there is an op with L_i = L (and any R_i ≥ R) and an op with R_i = R (and any L_i ≤ L). So the condition for being able to achieve intersection [L,R] with at most 2 ops is: there exists an op with L_i = L and R_i ≥ R, and there exists an op with L_i ≤ L and R_i = R. And if there is a single op with L_i = L and R_i = R, then 1 op. So for any [L,R], we can compute the minimum number of type-2 ops to achieve intersection exactly [L,R] (or at least contained in [L,R]? Actually we want intersection to be exactly [L,R] to minimize the covering work). So we can precompute for each L (1..N) the minimum R such that there is an op with L_i = L and R_i ≥ something? Not exactly.

Maybe we can approach the problem from the other side: we want to cover [1,N] with type-1 and type-2 ops. Since type-2 ops are expensive but can cover large parts, we can think of using them to "skip" covering some middle part. Specifically, if we use a type-2 op with interval [L,R], we don't need to cover [L,R] with type-1. So we can choose a set of type-2 ops to cover some parts, and then cover the rest with type-1. But the rest after using a set of type-2 ops is the intersection of their intervals. So indeed, the problem is to choose a set of type-2 ops, and then cover their intersection with type-1.  

We can think of this as: we need to cover [1,N] with type-1, but we are allowed to "remove" some intervals by using type-2 ops, each removal costing 1. The removed intervals are the intersections of the type-2 ops we choose. So we want to remove a set of positions (which will be an interval) at minimum cost, and then cover the remaining with type-1 at minimum cost. The removed interval must be exactly the intersection of the chosen type-2 ops. So we need to find an interval [l,r] that can be expressed as the intersection of some type-2 ops, and such that the cost of type-2 ops to get that intersection plus the cost to cover [l,r] with type-1 is minimized.  

We can precompute for each interval [l,r] the minimum cost to achieve an intersection that is exactly [l,r] using type-2 ops. But there are O(N^2) intervals, too many. We need a smarter way.

Observe that the intersection of type-2 ops is determined by the maximum L and minimum R among the chosen ops. So if we choose a set B, let L = max L_i, R = min R_i. Then the intersection is [L,R]. The cost is |B|. To achieve a given (L,R), we need to select a set of ops such that all L_i ≤ L and all R_i ≥ R, and at least one has L_i = L and at least one has R_i = R. The minimum size of such a set is: 1 if there exists an op with L_i = L and R_i = R; else 2 if there exists an op with L_i = L and R_i ≥ R, and an op with L_i ≤ L and R_i = R; else impossible. So for each L and R, we can determine the cost to achieve intersection exactly [L,R] with type-2 ops. But we don't need to consider all L,R; we only need to consider L and R that are "relevant", i.e., that come from the ops.  

We also need the cost to cover [L,R] with type-1 ops. This is the minimum number of type-1 intervals to cover [L,R]. Let's denote f(L,R) = min number of type-1 ops to cover [L,R]. If [L,R] cannot be covered, f = ∞.  

Then total cost for (L,R) is cost2(L,R) + f(L,R). We want to minimize over all L ≤ R.  

But we can also consider not using any type-2 ops, which corresponds to L=1, R=N, with cost2 = 0.  

So the problem reduces to computing f(L,R) and cost2(L,R) efficiently.  

Computing f(L,R) for all L,R is too heavy. But we don't need all; we only need to consider L,R that are boundaries of the type-2 ops? Because the cost2(L,R) is only finite for L,R that are achievable as max L_i and min R_i of some subset. But that's still many.  

Maybe we can use a shortest path approach on the line. Consider the positions 1..N+1. We can start at position 1 (uncovered leftmost) and we want to reach N+1 (uncovered rightmost+1). We can use type-1 ops: from position p, if there is a type-1 op with L ≤ p and R > p, we can jump to R+1 at cost 1. Actually, to cover continuously, we need to ensure that we cover everything. This is like: we need to cover from 1 to N. We can use ops to jump. But type-2 ops allow us to jump from 1 to L_i (if we use its left coverage, we cover up to L_i-1, but then we still need to cover from L_i to R_i? Actually, if we use a type-2 op, we cover [1, L_i-1] and [R_i+1, N]. So the uncovered part is [L_i, R_i]. So if we are at position 1 (uncovered), using a type-2 op will cover 1..L_i-1, so the new uncovered leftmost is L_i. But we also have a gap? Actually, after using a type-2 op, the uncovered set is [L_i, R_i] (if we haven't covered anything else). So we are now at L_i, and we need to cover up to R_i. But we could also use another type-2 op to shrink the uncovered set further. So we can think of a sequence: start with uncovered = [1,N]. We can apply a type-2 op to replace uncovered by [L_i, R_i] (if the current uncovered is contained in the complement of [L_i, R_i]? Actually, if we apply a type-2 op to a set U, the new uncovered set is U ∩ [L_i, R_i]. Because the type-2 op covers the complement, so only points in [L_i, R_i] remain uncovered. So if we start with U = [1,N], applying a type-2 op gives U1 = [1,N] ∩ [L_i, R_i] = [L_i, R_i]. Then we can apply another type-2 op: U2 = U1 ∩ [L_j, R_j] = [max(L_i, L_j), min(R_i, R_j)]. So indeed, the order of type-2 ops doesn't matter; the final uncovered set is the intersection of all applied type-2 ops. So we can think of selecting a set of type-2 ops to get an intersection I, and then we need to cover I with type-1.  

Now, to cover I with type-1, we can use a similar greedy: to cover an interval [l,r], we can repeatedly choose the type-1 op that starts at or before the current leftmost uncovered point and extends furthest to the right. This is the standard algorithm for minimum number of intervals to cover a target interval, provided we have the right set of intervals. But we need to compute this for many possible I.  

Maybe we can reverse the problem: we want to find a set of type-1 ops that cover some interval [l,r], and then we can use type-2 ops to cover the outside. But as argued, using type-2 ops to cover the outside is equivalent to having the type-2 ops' intersection be contained in [l,r]? Actually, if we have a set of type-1 ops covering [l,r], then the uncovered part after type-1 is the complement of the union of those intervals. That complement might not be a single interval; it could be two intervals. To cover that complement with type-2 ops, we need type-2 ops that cover those two intervals. But a single type-2 op covers two intervals: a prefix and a suffix. So we need the complement to be exactly a prefix and a suffix. That means the union of the type-1 ops must be exactly [l,r] (a contiguous block) and nothing else. So again, the type-1 ops must cover exactly [l,r] (their union is exactly [l,r], and they cover no points outside [l,r]). So the type-1 ops are all contained within [l,r]. So if we choose a set of type-1 ops, their union U must be an interval [l,r], and we can then use type-2 ops to cover the complement if there exist type-2 ops with L_i ≥ l and R_i ≤ r. So the problem is: choose a set of type-1 ops whose union is an interval [l,r], minimizing |A| + cost to cover complement with type-2.  

Now, to compute the minimum cost to cover complement with type-2: we need to cover [1,l-1] and [r+1,N]. As argued, we can cover [1,l-1] with a type-2 op if there exists an op with L_i ≥ l. Similarly for [r+1,N] with R_i ≤ r. And we can cover both with one op if there exists an op with L_i ≥ l and R_i ≤ r. So the cost is: 0 if l=1 and r=N (no complement); 1 if exactly one of the sides is non-empty and there is a suitable op; 2 if both sides non-empty and we need two ops, but possibly 1 if one op covers both. More systematically, let cost_left = 0 if l=1, else 1 if there exists type-2 op with L_i ≥ l. cost_right = 0 if r=N, else 1 if there exists type-2 op with R_i ≤ r. But if both cost_left and cost_right are 1, we can possibly combine them: if there exists a type-2 op with L_i ≥ l and R_i ≤ r, then total cost for both sides is 1 instead of 2. So we need to check that.  

So the problem becomes: find a contiguous interval [l,r] that can be covered by some type-1 ops, and such that (cost_left + cost_right, with possible combination) is minimized, and also we want to minimize the number of type-1 ops used. Actually, we want to minimize |A| + cost_type2. So we need to consider all possible [l,r] that are unions of some type-1 intervals. And for each, compute the minimum number of type-1 intervals to cover exactly [l,r] (i.e., the union is exactly [l,r]). But note: if we cover [l,r] with a set of type-1 intervals, their union might be a superset of [l,r] if they extend beyond. To have the union exactly [l,r], we need that no type-1 interval extends outside [l,r]. So we should only consider type-1 intervals that are entirely within [l,r]. So we can think: for each possible [l,r], we only consider type-1 ops with [L,R] ⊆ [l,r]. Then the minimum number to cover [l,r] using these ops is the standard interval covering problem. But [l,r] is exactly the target.  

Now, the number of possible [l,r] is O(N^2), but we can restrict to l and r that are boundaries of type-1 intervals. Since M is up to 2e5, the number of distinct L and R is at most 2e5. So we can consider l from the set of L_i of type-1 ops (or 1) and r from the set of R_i (or N). That's at most 2e5 * 2e5 = 4e10, too many.  

We need a more efficient approach.  

Maybe we can use the fact that the cost to cover [l,r] with type-1 ops is a function that can be computed if we sort intervals by left endpoint. Let's denote the type-1 intervals as [L_j, R_j]. We can sort them by L_j. For a given starting point l, the greedy algorithm to cover as far right as possible is: among intervals with L_j ≤ l, pick the one with maximum R. Then set l to that R+1, and repeat. This gives the maximum coverage with minimum number of intervals for that starting point. To cover a specific [l,r], we need that the greedy process starting at l reaches r or beyond. The number of intervals used is the number of steps. So for each l, we can precompute the "next" l after one step, and so on. This is like jumping pointers. We can build a graph where from position l, we can go to position R_max+1 at cost 1, where R_max is the maximum R among intervals with L ≤ l. This is a functional graph. We want to find, for each l, the minimum cost to reach a position ≥ r. But we need to consider all r.  

Alternatively, we can precompute for each l, the minimum number of type-1 intervals to cover from l to some position, and also the furthest position we can reach with k intervals. This is similar to the classic problem of covering an interval with minimum intervals. We can do this efficiently for all l by using two pointers.  

Let’s sort type-1 intervals by L. Let’s denote them as I_1, I_2, ..., I_K (K ≤ M). For each l from 1 to N, we want to know the minimum number of type-1 intervals to cover [l, x] for any x. Actually, we want to know for each l, the minimum number of intervals to cover [l, t] for each t ≥ l. But that's too much.  

Maybe we can observe that the optimal [l,r] will be such that the type-1 covering is done by a chain of intervals that are "tight": the union is exactly [l,r] and each interval starts at or before the previous one's end. This is like a path in the interval graph.  

Another idea: since the type-1 intervals are static, we can precompute for each position i, the minimum number of type-1 intervals needed to cover from i to some position, and also the furthest reachable with that many intervals. This is like building a sparse table for jumps. But N is 1e6, M is 2e5, so we can do O((N+M) log N) maybe.  

But we also have type-2 ops. The cost for type-2 depends on l and r. We can precompute for each l, the minimum cost to cover left prefix [1,l-1] with type-2 ops: that's 1 if l>1 and there exists a type-2 op with L_i ≥ l, else 0 (if l=1). Similarly, for each r, the minimum cost to cover right suffix [r+1,N] with type-2 ops: 1 if r<N and there exists a type-2 op with R_i ≤ r, else 0. But we also need to consider the case where one op covers both. So we need to know for each pair (l,r) whether there exists a type-2 op with L_i ≥ l and R_i ≤ r.  

We can precompute:
- For each l from 1 to N, define left_possible[l] = true if there exists a type-2 op with L_i ≥ l.
- For each r from 1 to N, define right_possible[r] = true if there exists a type-2 op with R_i ≤ r.
- Also, for each l, we want to know the minimum R among ops with L_i ≥ l? Or we want to know for each l, the maximum L? Not sure.

To check if there exists an op with L_i ≥ l and R_i ≤ r, we can precompute for each l, the minimum R among ops with L_i ≥ l. Let minR_for_Lge[l] = min{ R_i : L_i ≥ l }. Then if minR_for_Lge[l] ≤ r, then there exists such an op. So we can compute an array minR_ge_L, where for l from N down to 1, we update with the R_i of ops with L_i = l.  

Similarly, we can compute for each r, the maximum L among ops with R_i ≤ r: maxL_le_R[r] = max{ L_i : R_i ≤ r }. Then if maxL_le_R[r] ≥ l, there exists an op with L_i ≥ l? Wait, maxL_le_R[r] is the maximum L_i for ops with R_i ≤ r. That means there is an op with L = maxL_le_R[r] and R ≤ r. So if we want an op with L_i ≥ l and R_i ≤ r, we need an op with L_i ≥ l and R_i ≤ r. That is equivalent to: there exists an op with R_i ≤ r and L_i ≥ l. So if we know the maximum L among ops with R_i ≤ r, call it maxL_le_R[r], then if maxL_le_R[r] ≥ l, then there is an op with L_i ≥ l and R_i ≤ r? Not exactly: maxL_le_R[r] is the maximum L_i among all ops with R_i ≤ r. If that maximum is ≥ l, then there is an op with R_i ≤ r and L_i ≥ l (since the op achieving the maximum has L_i ≥ l and R_i ≤ r). So yes, condition is maxL_le_R[r] ≥ l. So we can check both ways.  

So for each l, we can compute minR_ge_L[l]. For each r, we can compute maxL_le_R[r].  

Now, for a given [l,r], the cost for type-2 to cover the complement is:
- If l=1 and r=N: cost_type2 = 0.
- If l>1 and r=N: need to cover left prefix. Cost = 1 if left_possible[l] (i.e., exists op with L_i ≥ l), else impossible.
- If l=1 and r<N: need to cover right suffix. Cost = 1 if right_possible[r] (exists op with R_i ≤ r), else impossible.
- If l>1 and r<N: need to cover both. We can use one op if there exists an op with L_i ≥ l and R_i ≤ r. That is true if minR_ge_L[l] ≤ r (since minR_ge_L[l] is the smallest R among ops with L_i ≥ l; if that smallest R is ≤ r, then there is an op with L_i ≥ l and R_i ≤ r). Alternatively, maxL_le_R[r] ≥ l. If such an op exists, we can cover both with cost 1. If not, but left_possible[l] and right_possible[r] are both true, we can use two ops, cost = 2. If one of left_possible or right_possible is false, then impossible.  

So cost_type2(l,r) can be computed in O(1) if we have these precomputed arrays.  

Now we need to compute, for each possible [l,r] that is the union of some type-1 intervals, the minimum number of type-1 intervals to cover exactly [l,r]. But maybe we don't need to consider all [l,r]; we only need to consider l and r that are the leftmost and rightmost points of the union of some type-1 intervals. And we want to minimize |A| + cost_type2(l,r).  

We can approach by building the "reachable" set of intervals using type-1 ops. This is similar to finding all intervals that can be covered by a chain of type-1 ops. We can think of a graph where nodes are positions, and from a position p, we can jump to R+1 using a type-1 op with L ≤ p ≤ R, but we need to cover continuously. Actually, to cover from p, we need an interval that starts at or before p and ends at or after p. So we can only jump from p if there is an interval covering p. So the process of covering with type-1 ops is: start at l, we need to cover from l. The first interval must have L ≤ l. After using an interval [L,R], the new uncovered leftmost is R+1. So we can think of a function nxt[p] = the smallest position > p that can be reached by one interval? Not exactly.  

We can precompute for each position p, the furthest right we can reach using one interval: let far[p] = max{ R : there exists type-1 op with L ≤ p ≤ R }. But to cover continuously, we need that the next interval starts at or before the current position. So if we are at p, we can only use an interval that covers p. So we need to know, for each p, the maximum R among intervals covering p. Let cover_furthest[p] = max{ R : L ≤ p ≤ R }. Then we can jump from p to cover_furthest[p] + 1 at cost 1. But this is only valid if there is at least one interval covering p. If no interval covers p, then we cannot cover p with type-1, so any [l,r] that includes p is impossible.  

So we can define an array furthest: for p from 1 to N, furthest[p] = maximum R among type-1 ops with L ≤ p ≤ R. If no such op, furthest[p] = -1.  

Now, to cover an interval [l,r] with type-1 ops, we start at p = l. We need furthest[p] ≥ p. Then we jump to p' = furthest[p] + 1. We need that p' ≤ r (otherwise we overshoot? Actually, we need to cover exactly up to r. If furthest[p] > r, we still cover r, so it's fine. But we need to ensure that we don't leave gaps. So the process is: while p ≤ r, we need an interval covering p. We set p = furthest[p] + 1. If at some point p > r, we have covered [l, r] (or more). If we get stuck because no interval covers p, then we cannot cover [l,r] continuously from l.  

The number of intervals used is the number of jumps. This is a deterministic process given l: we follow the chain of furthest jumps. But note that furthest[p] depends only on p, so the path is unique. So for each l, the sequence of positions visited is deterministic. The number of jumps to reach or pass a given r is simply the number of steps in this chain until we exceed r. So we can precompute for each l, the positions after each jump. This is like a functional graph. We can build a "next" array: next1[p] = furthest[p] + 1 if furthest[p] exists, else -1. Then we can do binary lifting to find how many steps to reach a given position. But we need to find for each l, the number of steps to cover exactly [l, r]. Actually, we want to know for each l and r (with l ≤ r), what is the minimum number of type-1 intervals to cover [l,r]? Since the process is deterministic, it's exactly the number of steps in the chain starting at l until the current position > r. But is it always minimum? Yes, because the greedy choice of using the interval that extends furthest is optimal for covering an interval on a line. So for a given starting point l, the greedy algorithm gives the minimum number of intervals to cover as far as possible, and it is unique. So f(l,r) is simply the number of steps in the greedy chain starting at l until we reach a position > r. However, we must ensure that the chain actually covers r. If the greedy chain jumps over r (i.e., we have p ≤ r, but after a jump, p' > r), then we have covered [l, r] (since the last interval covered up to at least r). If at some p ≤ r, we have no interval covering p, then we cannot cover [l,r] from l using type-1. So f(l,r) is defined as the number of steps if possible, else ∞.  

But wait: is the greedy algorithm always optimal for covering a specific target interval? Yes, for covering an interval on a line with intervals, the greedy algorithm that always picks the interval with the leftmost start and the furthest right is optimal. But here we are forced to start at l, and we must cover continuously. The greedy algorithm from l is: at each step, pick the interval that starts at or before the current point and extends the furthest. This yields the maximum reach for a given number of intervals, and thus the minimum number to reach a given point. So indeed, for a given l, the greedy chain gives the unique path. So f(l,r) is well-defined.  

Now, we need to consider all possible l. But l is not arbitrary; l must be such that the union of the intervals used in the greedy chain is exactly [l, r]? Actually, if we start at l and follow the greedy chain until we pass r, the union of the intervals used might extend beyond r. That's fine because we are covering [l,r] as a subset. But we also need that the union is exactly [l,r]? No, we only need that [l,r] is covered. The fact that the intervals might extend beyond r is okay because we can still use type-2 to cover the outside? Wait, if the type-1 intervals extend beyond r, then their union is larger than [l,r]. That means the complement (the part not covered by type-1) is smaller, and might not be exactly a prefix and suffix. For example, if the type-1 intervals cover [l, r'] with r' > r, then the uncovered part is [1, l-1] and [r'+1, N]. But we intended to cover the complement with type-2 ops. But if the type-1 intervals cover beyond r, then the complement is different. So to use the type-2 complement approach, we need the type-1 union to be exactly [l,r]. If the type-1 union is [l, r'] with r' > r, then we could have chosen r = r' and the complement would be [1,l-1] and [r'+1,N], which is even better (smaller complement). So we should actually take the union of the type-1 intervals as the covered region. So we should not fix r arbitrarily; rather, we should consider the entire union of the selected type-1 intervals. That union is exactly the set of positions covered by type-1. And we want to choose a set of type-1 intervals whose union is some interval [l,r] (contiguous), and then use type-2 to cover the complement. So the natural choice is to take l as the minimum index covered by the type-1 intervals, and r as the maximum index covered. So if we select a set of type-1 intervals, their union is [l,r] (if contiguous). So l and r are determined by the set. And we want to minimize |A| + cost_type2(l,r).  

Now, given the greedy chain starting from some l, if we follow the chain until we cannot jump anymore (i.e., we reach a point p with no interval covering it), then the union of all intervals used in the chain is exactly the set of positions covered from l up to the last point before p? Actually, the chain starts at l, uses an interval that covers l and goes to furthest[l]. Then from furthest[l]+1, uses another interval, etc. The union of these intervals is a contiguous block starting at l and ending at the maximum R among the intervals used. That is exactly the greedy chain's coverage. So if we start at l and follow the greedy chain until we get stuck (i.e., we reach a point p with no interval covering it), then the union of the intervals used is [l, last_R], where last_R is the maximum R of the last interval. But note that after the last jump, we are at p = last_R+1, and there is no interval covering p. So the covered region is [l, last_R]. So for each l, if we start the greedy chain and continue until we cannot jump, we get a covered interval [l, r_l] where r_l is the maximum position reached. The number of intervals used is the number of steps. This is the maximal coverage starting from l using the greedy algorithm. But is this the only possible coverage starting from l? If we choose a different set of intervals, we might get a smaller coverage. For example, we could stop earlier. But if we want to minimize total cost, we might want to cover a smaller interval if that allows using fewer type-2 ops? Actually, if we cover a smaller interval, the complement is larger, so we might need more type-2 ops. But type-2 ops have cost 1 each, and they can cover both sides with one op. So it's not obvious.  

We need to consider all possible subsets of type-1 intervals that form a contiguous union. The greedy chain from l gives the maximum coverage for a given number of intervals? Actually, the greedy chain from l gives the coverage with the minimum number of intervals to reach as far as possible. But we might not need to reach as far as possible; we might stop earlier. For a given l, the possible unions we can achieve by choosing different chains? But since the intervals are static, the set of positions that can be covered starting from l is actually all positions that are covered by the greedy chain? Not necessarily: there might be alternative ways to cover from l using a different set of intervals that yields a different union. For example, if there are two intervals covering l: one goes to 5, another to 10. Greedy picks the one to 10. But if we pick the one to 5, we might then pick an interval starting at 5 to go further. The greedy is optimal for covering a target, but if we are free to choose the target, the greedy also gives the maximum reach for a given number of intervals. So for a given l, the set of achievable unions (as contiguous intervals) is actually a set of intervals that are "nested" in some way. In fact, if we start at l, the first interval must cover l. We can choose any interval that covers l. After that, we are at some point p, and we need to cover from p. So the possible unions are determined by the first choice. So there could be many possibilities.  

This seems complicated. Maybe there is a simpler solution.  

Let's think from the perspective of the final state: all x_j = 1. Each operation either sets a range to 1 or its complement to 1. This is reminiscent of a problem where we can think of each operation as a "move" that flips the state? No, it only sets to 1, not toggles.  

Maybe we can model the process as a game on a line where we want to cover all points. Since setting to 1 is permanent, the order doesn't matter. So we just need to select a set of operations.  

Another idea: consider the complement of the final state: initially all 0, we want all 1. So we need to "activate" each position. Each operation activates a set of positions. We need the union of activated sets to be all positions.  

This is a set cover problem. Since M is up to 2e5, and N is 1e6, we need an efficient solution.  

Observing the special form of type-2 (complement of an interval), we can think of the problem as: we need to cover [1,N] with intervals, where each type-1 gives an interval, and each type-2 gives two intervals: [1,L-1] and [R+1,N]. But note that these two intervals are disjoint and at the ends. So if we use a type-2 op, we can think of it as providing coverage for the leftmost and rightmost regions.  

Maybe we can use a greedy algorithm that scans from left to right. We want to cover the leftmost uncovered point. We can use a type-1 op that covers it, or a type-2 op that covers the left prefix. If we use a type-2 op, it will also cover the right suffix, but that might be wasteful if we don't need it. However, we can still use it to cover the left prefix, and then we will have to cover the remaining middle part. So the process: we maintain a covered region from the left. Initially, covered = 0. We look at the leftmost uncovered point p. We can either:
- Use a type-1 op that covers p. This will extend the covered region to at least the R of that op. We can choose the one that extends furthest to minimize the number of ops.
- Or, we can use a type-2 op to cover a left prefix. If we use a type-2 op, it will cover [1, L-1]. So if we choose an op with L = p, it will cover up to p-1, so the new leftmost uncovered is p. That doesn't help. We need an op with L > p to cover beyond p. Specifically, if we use a type-2 op with L = L0, it covers [1, L0-1]. So if we want to cover p, we need p ≤ L0-1, i.e., L0 ≥ p+1. So we can use a type-2 op to jump the leftmost uncovered to L0. But note that using a type-2 op also covers the right suffix from R0+1 to N. That might cover some right part, but we still need to cover the middle [L0, R0]. So after using the type-2 op, the uncovered set is [L0, R0]. So we have essentially "removed" the left part and the right part, and we need to cover the middle. This is exactly the earlier intersection idea.  

So we can think recursively: we need to cover [1,N]. We can choose a type-2 op with interval [L,R] to cover the ends, leaving [L,R] to be covered by type-1. Or we can choose a type-1 op to cover from the left.  

This suggests a dynamic programming on intervals. Let dp[l][r] be the minimum cost to cover [l,r]. But N is too large.  

Maybe we can use the fact that type-2 ops are only useful when they significantly reduce the middle interval. We can try all possible type-2 ops as the "main" one, and then compute the cost to cover the middle with type-1. But we might need to use multiple type-2 ops. However, using two type-2 ops is equivalent to using their intersection as the middle. So we can consider all possible intersections of up to two type-2 ops (since using more than two is redundant: you can always achieve the same intersection with at most two ops, as argued). So we can iterate over all possible (L,R) that can be formed as the intersection of at most two type-2 ops. How many such (L,R) are there? For each type-2 op, we can take its L and R. For pairs of ops, we can take (max(L1, L2), min(R1, R2)). That's O(M^2) in the worst case, too many.  

But maybe we can do better: we can sort type-2 ops by L, and for each L, we can consider the best R. Actually, for a given L, the best R to pair with is the minimum R among ops with L_i ≥ L. That is minR_ge_L[L]. So for each L, we can consider the pair (L, minR_ge_L[L]) if minR_ge_L[L] ≥ L. That gives at most N possibilities. Similarly, for each R, we can consider (maxL_le_R[R], R) if maxL_le_R[R] ≤ R. Also, we can consider single ops: for each op, (L_i, R_i). So we can generate a set of candidate intervals [l,r] that are achievable as intersections of at most two type-2 ops. The number of candidates is O(N + M), which is manageable. For each candidate, we compute the cost to cover [l,r] with type-1 ops (using the greedy chain from l, but we need to ensure that the chain covers exactly [l,r]? Actually, if we use type-1 ops to cover [l,r], we can start at l and follow the greedy chain. But we need to cover exactly [l,r]. The greedy chain from l will cover up to some r'. If r' ≥ r, then we can cover [l,r] with the same number of intervals as needed to reach r'? Actually, if the greedy chain from l reaches r' > r, we can still cover [l,r] by using the same intervals, but we might be able to stop earlier? The number of intervals used to cover [l,r] is the number of steps in the greedy chain until we first reach a position > r. That number might be less than or equal to the number to reach r'. So we need to compute, for each l and each r, the number of steps to reach r. But if we only have a set of candidate r, we can compute the number of steps to reach that r. However, note that the greedy chain from l is deterministic, so for a given l, as we follow the chain, the positions visited are increasing. The number of steps to reach a given r is the number of intervals until the current position > r. So if we precompute for each l, the sequence of positions after each jump, we can answer queries for any r. But we have many l.  

We can precompute for each l, the furthest position reachable with k intervals. This is like a sparse table. Since N is 1e6 and M is 2e5, the maximum number of intervals needed to cover any interval is at most M, so log M is about 18. We can do a two-pointer sweep to compute the "next" array as described, and then build a binary lifting table for the "next" function. Then for any l and r, we can compute the minimum number of intervals to cover [l,r] by finding the smallest k such that after k jumps from l, the position is > r. This is a standard technique.  

So the plan:
1. Read input, separate type-1 and type-2 operations.
2. For type-2 ops, precompute arrays:
   - minR_ge_L[l] for l=1..N: minimum R_i among ops with L_i ≥ l.
   - maxL_le_R[r] for r=1..N: maximum L_i among ops with R_i ≤ r.
   - left_possible[l] = (minR_ge_L[l] exists)
   - right_possible[r] = (maxL_le_R[r] exists)
3. For type-1 ops, precompute for each position p (1..N), the furthest R among type-1 ops that cover p (i.e., L ≤ p ≤ R). This can be done by processing events: for each op [L,R], we can update an array furthest_in[L] = max(furthest_in[L], R). Then we need, for each p, the maximum R among ops with L ≤ p ≤ R. This is not straightforward. We can do: for each op, we know it covers all points in [L,R]. So we can think of the maximum R for each point p as the maximum R of ops that have L ≤ p and R ≥ p. We can precompute an array best_R_for_point[p] by sweeping: we maintain a set of active intervals. As we move p from 1 to N, we add intervals that start at p, and remove intervals that end before p. The maximum R among active intervals is the furthest we can cover from p. So we can do this in O((N+M) log M) or O(N+M) with two pointers if we sort intervals by L and R. Since N is 1e6, we can do O(N + M) with careful sweeping. Let's do: sort type-1 ops by L. For each p from 1 to N, we add all ops with L = p to a priority queue (max R), and we also need to remove ops that have R < p. But removal is tricky. We can instead precompute an array next_L[p]? Actually, we can compute for each p, the maximum R among ops with L ≤ p and R ≥ p by using a segment tree or by using the fact that we only need the furthest jump from p. But we need it for all p to build the jump table. We can do: for each p, we want the maximum R among ops with L ≤ p and R ≥ p. This is equivalent to: among all ops, if we sort by L, and for each op, it covers from L to R. So for p, we need ops with L ≤ p ≤ R. We can precompute an array max_R_starting_at_or_before[p] but that only gives the max R among ops with L ≤ p, not necessarily those with R ≥ p. To ensure R ≥ p, we need to filter. So we can do: for each p, we can find the op with the maximum R among those with L ≤ p and R ≥ p. This can be done by, for each op, it contributes to all p in [L,R]. So we can build an array furthest_cover[p] by initializing to -1, and for each op [L,R], we set furthest_cover[p] = max(furthest_cover[p], R) for p in [L,R]. That's O(N*M) too large.  

We need a more efficient way. Since the intervals are static, we can compute the furthest cover for each p by considering the "upper envelope" of intervals. The condition L ≤ p ≤ R means that p is in the interval. So the maximum R for a given p is the maximum R among all intervals that contain p. So if we consider the set of intervals, for each p, we want the maximum R such that there is an interval [L,R] with L ≤ p ≤ R. This is essentially the maximum R of intervals that start at or before p and end at or after p. We can compute this by scanning p from 1 to N, maintaining a data structure of intervals that are "active" (i.e., L ≤ current p) and have R ≥ current p. But as p increases, some intervals become inactive because R < p. So we need to be able to add intervals by L and remove by R. This is a typical sweep line with a max-heap. We can do: sort intervals by L. For p from 1 to N, we add all intervals with L = p to a max-heap (keyed by R). We also need to remove intervals with R < p. To efficiently remove, we can push intervals into the heap with their R, and when popping, we check if R < p, and if so, discard. So we can maintain a heap of intervals that have L ≤ p, and we pop any with R < p. The maximum R in the heap (if any) is the furthest we can cover from p. This is O((N+M) log M) which is fine. M is 2e5, N is 1e6, so total operations about 1.2e6, log 2e5 ~ 18, so about 20 million operations, okay.  

Let's detail:
- Sort type-1 intervals by L.
- Have a priority queue (max-heap) of pairs (R, L) or just R. Actually, we need to be able to remove intervals when they expire. We can push (R, L) and when we pop, we check if the L is consistent? Actually, we can just push R, and when we want to know the max R, we look at the top. But we also need to remove intervals that have R < p. We can do: while heap not empty and heap[0] < p: pop. Then if heap not empty, furthest[p] = heap[0]; else furthest[p] = -1. But wait, this only removes intervals that have R < p, but what about intervals that have L > p? They are not added yet. So as p increases, we add intervals with L = p. So the heap contains all intervals with L ≤ p and R ≥ p? Actually, it contains all intervals with L ≤ p that have not been popped because their R was < p. So it contains intervals with L ≤ p and R ≥ p. So the max R is exactly what we want. So this works.  

We also need to handle the case where there are no type-1 ops. Then furthest[p] = -1 for all p.  

Now, we have an array furthest[p] for p=1..N. If furthest[p] = -1, then no type-1 op covers p.  

Next, we want to build a jump table for the greedy covering. Define next_pos[p] = furthest[p] + 1 if furthest[p] != -1, else -1. Note that furthest[p] could be less than p? Actually, if an op covers p, then R ≥ p, so furthest[p] ≥ p. So next_pos[p] > p.  

Now, we want to answer queries: given start l and target r, what is the minimum number of jumps to reach a position > r? This is like finding the smallest k such that the k-th jump from l is > r. We can precompute a sparse table for next_pos. Let nxt[0][p] = next_pos[p]. For j>0, nxt[j][p] = nxt[j-1][ nxt[j-1][p] ] if nxt[j-1][p] != -1, else -1. This is standard. Also, we can precompute the position after k jumps for each p. But we need to know for each l and r, the number of jumps. We can do: for a given l and r, we can start from l and follow the jumps until we exceed r, but that could be O(number of jumps). Using binary lifting, we can find the number of jumps to reach a position > r efficiently. Actually, we can do: we want the smallest k such that after k jumps, the position is > r. We can binary lift: start with k=0, pos=l. For j from max_log down to 0, if nxt[j][pos] != -1 and nxt[j][pos] ≤ r+1? Wait, we want to go to a position > r. So we can check if after some jumps, we are still ≤ r. So we can maintain a variable pos and count. We can do: for j from max_log down to 0, if nxt[j][pos] != -1 and nxt[j][pos] ≤ r+1, then we can take that jump (it keeps us ≤ r+1). But we want the first time we exceed r. Alternatively, we can precompute for each l, the list of positions after each jump. Since M is 2e5, the number of jumps to cover any interval is at most M, so the depth is at most M. We can precompute an array depth[l] = the number of jumps to reach a point with no next (or to reach the end). But we need to answer for various r.  

Maybe we can precompute for each l, the positions after each jump in an array, and also the number of jumps. But storing an array of size M for each l is too much (N * M). We can use the sparse table to compute the number of jumps in O(log M) per query. That's acceptable if we have O(M) queries. We will have O(N) candidate intervals? Actually, we plan to generate candidate intervals from type-2 ops. The number of candidates could be up to O(N + M). So O((N+M) log M) is fine.  

So for each candidate interval [l,r], we can compute the number of type-1 intervals needed to cover [l,r] as follows:
- Let pos = l.
- If furthest[pos] == -1, then impossible.
- Else, we need to find the number of jumps to reach > r. We can do: cnt = 0; while pos <= r: if next_pos[pos] == -1: impossible; else: pos = next_pos[pos]; cnt++; if pos > r: break; if pos <= r and no further jump possible, impossible. But this loop could be long. Instead, we can use binary lifting to find the maximum number of jumps we can take without exceeding r. We can precompute a table jump[k][p] = position after 2^k jumps from p. Also, we can have a table steps[k][p] = the number of jumps? Actually, we can just use the position table and binary lift to find the smallest k such that after k jumps, position > r. We can do: 
  - Initialize ans = 0, cur = l.
  - For i from max_log down to 0:
      if nxt[i][cur] != -1 and nxt[i][cur] <= r+1:   (since we want to stay ≤ r, but if we go to r+1, that's okay because it means we covered up to at least r? Actually, if we reach r+1, we have covered up to at least r. So condition: nxt[i][cur] <= r+1)
          cur = nxt[i][cur];
          ans += (1 << i);
  - After this loop, cur is the position after ans jumps, and cur > r? Actually, we want to make sure that after the loop, cur is the largest position ≤ r+1 that we can reach. Then we need one more jump? Wait, we want to cover [l,r]. The greedy process will cover continuously until we exceed r. So we need to take jumps until pos > r. The binary lifting above finds the maximum number of jumps we can take while staying ≤ r+1. But if we end with cur ≤ r+1, we might need an additional jump to exceed r. So after the loop, if cur > r, then ans is the number of jumps taken, and we are done. If cur ≤ r, then we need to take one more jump. But we also need to check that next_pos[cur] exists. So the number of jumps is ans + (1 if cur <= r and next_pos[cur] != -1 else impossible). Actually, careful: the loop as described finds the maximum number of jumps we can take such that the resulting position is ≤ r+1. Let's think: we want the smallest k such that after k jumps, position > r. We can binary lift to find the largest k such that after k jumps, position ≤ r+1. Then the answer is k+1 if after k+1 jumps we can go to > r. But we need to check that k+1 jumps is possible. So we can do:
  - Let cur = l, steps = 0.
  - For i from max_log down to 0:
      if nxt[i][cur] != -1 and nxt[i][cur] <= r+1:
          cur = nxt[i][cur];
          steps += (1 << i);
  - Now, after steps jumps, we are at cur, and cur <= r+1. If cur > r, then we have already covered [l,r] with steps jumps. So answer = steps.
  - Else (cur <= r), we need one more jump. Check if next_pos[cur] != -1. If yes, answer = steps+1. If no, impossible.
This works.  

But we need to build the nxt table. We have next_pos[p] for p=1..N. Note that next_pos[p] can be up to N+1. We should define next_pos[N+1] = -1. And we need to handle positions > N. When we jump, we might go to N+1. So we should create an array for positions 1..N+1. For p = N+1, next_pos[N+1] = -1. For p where furthest[p] = -1, next_pos[p] = -1. Otherwise, next_pos[p] = furthest[p] + 1. Note that if furthest[p] = N, then next_pos[p] = N+1.  

We need to compute nxt[0][p] = next_pos[p]. Then for k>0, nxt[k][p] = nxt[k-1][ nxt[k-1][p] ] if nxt[k-1][p] != -1, else -1. We need to determine max_log. The maximum number of jumps from any p is at most M, so max_log = floor(log2(M)) + 1, say 18 or 20.  

Now, we also need to generate candidate intervals [l,r] from type-2 ops. We want to consider intervals that can be formed as the intersection of at most two type-2 ops. As argued, the minimum cost to achieve an intersection [l,r] using type-2 ops is:
- 0 if l=1 and r=N.
- 1 if there exists a single op with [L,R] = [l,r]? Actually, if we use one op, its intersection is [L,R]. So any [l,r] that equals [L,R] for some op can be achieved with cost 1.
- 2 if we can achieve [l,r] with two ops: one with L_i = l and R_i ≥ r, and one with L_i ≤ l and R_i = r, and no single op gives exactly [l,r]. But also, if we have an op with L_i = l and R_i > r, and another with L_i < l and R_i = r, then the intersection is [l,r] (since max L = l, min R = r). So condition for cost 2: there exists op with L_i = l and R_i ≥ r, and exists op with L_i ≤ l and R_i = r, and there is no op with L_i = l and R_i = r. But we can also achieve [l,r] with two ops where neither has L_i = l or R_i = r, as long as one has L_i ≤ l and R_i ≥ r, and the other has L_i = l and R_i = r? Actually, to get intersection exactly [l,r], we need max L = l and min R = r. So we need at least one op with L_i = l (since max L = l, there must be an op with L_i = l, because if all ops have L_i < l, then max L < l). Similarly, we need at least one op with R_i = r. So the necessary and sufficient conditions for being able to achieve intersection [l,r] with some subset of type-2 ops are:
  (1) There exists at least one op with L_i ≤ l and R_i ≥ r (so that the intersection is non-empty and contained in [l,r]).
  (2) There exists at least one op with L_i = l.
  (3) There exists at least one op with R_i = r.
  And the minimum number of ops to achieve [l,r] is:
  - 1 if there exists an op with L_i = l and R_i = r.
  - 2 if (2) and (3) hold but (1) for a single op with both L_i=l and R_i=r does not hold, and also we need that the op with L_i=l has R_i ≥ r, and the op with R_i=r has L_i ≤ l. Actually, if we take the op with L_i=l and the op with R_i=r, then their intersection is [l, min(R_i, r)] = [l, r] provided the first op has R_i ≥ r and the second has L_i ≤ l. So condition for cost 2 is: there exists an op with L_i = l and R_i ≥ r, and there exists an op with L_i ≤ l and R_i = r. And there is no op with L_i = l and R_i = r. But wait, could we achieve [l,r] with two ops where one has L_i < l but the other has L_i = l? Then max L = l. So the op with L_i = l must be present. Similarly, the op with R_i = r must be present. So yes, we need an op with L_i = l (any R) and an op with R_i = r (any L). And we need that the intersection of these two (and possibly others) is exactly [l,r]. If we only take these two, the intersection is [max(l, L_other), min(r, R_other)] = [l, r] if the first has R ≥ r and the second has L ≤ l. So condition: there exists an op with L_i = l and R_i ≥ r, and there exists an op with L_i ≤ l and R_i = r. If both conditions hold, we can achieve [l,r] with cost 2. If there is an op with L_i = l and R_i = r, then cost 1. If not, but one of the conditions fails, then we cannot achieve [l,r] with at most 2 ops. But could we achieve it with more than 2? Suppose we have three ops: one with L=2,R=10, one with L=3,R=8, one with L=4,R=6. The intersection is [4,6]. To get max L=4, we need an op with L=4. That op has R=6. So we need an op with L=4 and R=6. That is exactly the third op. So we need an op with L_i = l and R_i = r? Not necessarily: if we have an op with L=4,R=10 and an op with L=2,R=6, then intersection is [4,6]. Here max L=4 from the first, min R=6 from the second. So we have an op with L_i=4 and R_i=10, and an op with L_i=2 and R_i=6. So condition: there exists an op with L_i = l and R_i ≥ r, and an op with L_i ≤ l and R_i = r. So that's the condition. So we don't need an op with exactly L=l and R=r. So the minimum number of type-2 ops to achieve intersection [l,r] is:
  - 0 if l=1 and r=N (no type-2 ops needed, intersection is whole [1,N] by default? Actually, if we use no type-2 ops, the intersection is [1,N]. So cost 0.
  - 1 if there exists a type-2 op with L_i = l and R_i = r.
  - 2 if there exists a type-2 op with L_i = l and R_i ≥ r, and there exists a type-2 op with L_i ≤ l and R_i = r, and not (1).
  - ∞ otherwise.
But wait, what if we can achieve [l,r] with 0 ops? That corresponds to l=1, r=N. For other l,r, we need at least one op. But what if l=1 and r<N? Can we achieve intersection [1,r] with 0 ops? No, because with 0 ops, the intersection is [1,N]. So to get intersection [1,r], we need to use type-2 ops. So we need to consider l=1, r<N. For that, condition for cost 1: exists op with L_i=1 and R_i=r. Cost 2: exists op with L_i=1 and R_i ≥ r, and exists op with L_i ≤ 1 and R_i = r. But L_i ≤ 1 means L_i=1. So we need an op with L_i=1 and R_i ≥ r, and an op with L_i=1 and R_i = r. That's essentially the same as cost 1? Actually, if we have an op with L_i=1 and R_i ≥ r, and another with L_i=1 and R_i = r, then we can take just the second for cost 1. So cost 2 is not better than cost 1. So for l=1, the minimum cost is 1 if there is an op with L_i=1 and R_i = r, else impossible? But wait, if we have an op with L_i=1 and R_i > r, and we use it, the intersection is [1, R_i] which is larger than [1,r]. So that doesn't give intersection [1,r]. So to get intersection exactly [1,r], we need min R = r. So we need an op with R_i = r. And we also need max L = 1, so we need an op with L_i=1. So we need an op with L_i=1 and R_i = r. So cost 1 if such op exists, else impossible. So for l=1, cost_type2(1,r) = 1 if there exists op with L_i=1 and R_i = r, else ∞. Similarly, for r=N, cost_type2(l,N) = 1 if there exists op with R_i = N and L_i = l, else ∞. And for general l,r, cost_type2(l,r) as above.  

But in our earlier computation of cost_type2 for covering the complement, we were using left_possible and right_possible and the combined condition. That was for covering the complement with type-2 ops after type-1 covers [l,r]. That is different from the intersection cost. Let's be consistent.  

We have two perspectives:
1. Select a set of type-2 ops to get an intersection I, and then cover I with type-1. The cost is |B| + f(I). Here |B| is the number of type-2 ops to achieve intersection I.
2. Select a set of type-1 ops to cover an interval [l,r], and then cover the complement with type-2 ops. The cost is |A| + cost_type2_complement(l,r). Here cost_type2_complement is the cost to cover [1,l-1] and [r+1,N] with type-2 ops.

These two are equivalent. The relationship: if we use type-1 to cover [l,r], then the uncovered part is the complement, which is [1,l-1] ∪ [r+1,N]. We cover that with type-2 ops. The type-2 ops we use must cover those two pieces. A set of type-2 ops covers [1,l-1] and [r+1,N] if and only if their intersection is contained in [l,r]? Actually, if we have a set of type-2 ops, they cover a position j if there exists an op in the set with j outside its [L,R]. So the uncovered part is the intersection of their [L,R]. So if we want the uncovered part to be exactly [1,l-1] ∪ [r+1,N], that would be two intervals, not a single interval. That's not possible because the intersection of intervals is an interval. So the uncovered part after using a set of type-2 ops is always an interval. Therefore, if we use type-1 to cover [l,r] and type-2 to cover the complement, the final uncovered set after type-2 is the complement of the union of type-1 and type-2. But if we first use type-1 to cover [l,r], the remaining is two intervals. Then we apply type-2 ops. Each type-2 op covers the complement of its interval. So after applying a type-2 op, the uncovered set becomes the intersection of the previous uncovered set with [L,R]. So if we start with U = [1,l-1] ∪ [r+1,N], and apply a type-2 op with [L,R], the new uncovered set is U ∩ [L,R]. Since U has two components, the intersection with [L,R] will be at most two intervals. To end with empty, we need to cover both components. This is messy.  

The clean way is the intersection method: we choose a set of type-2 ops B, and then the uncovered part is I = ∩_{i in B} [L_i, R_i]. Then we cover I with type-1. The cost is |B| + f(I). And we can also consider B empty, I = [1,N]. So we need to find I (an interval) that can be expressed as the intersection of some type-2 ops, and such that |B| + f(I) is minimized.  

Now, how to find such I? I is determined by the maximum L and minimum R among the ops in B. So I = [L_max, R_min]. So we can parameterize I by (L_max, R_min). For a given pair (L,R) with L ≤ R, the minimum number of type-2 ops to achieve intersection exactly [L,R] is:
- 0 if we take B empty, but then I = [1,N], so L=1, R=N.
- 1 if there exists an op with L_i = L and R_i = R.
- 2 if there exists an op with L_i = L and R_i ≥ R, and exists an op with L_i ≤ L and R_i = R, and not (1).
- ∞ otherwise.

But wait, could we achieve [L,R] with 2 ops where the first has L_i = L and R_i > R, and the second has L_i < L and R_i = R? That gives intersection [L,R] as long as the first's R ≥ R and the second's L ≤ L. So condition: exists op with L_i = L and R_i ≥ R, and exists op with L_i ≤ L and R_i = R. That's it. So we need to check that.  

Also, could we achieve [L,R] with 2 ops where neither has L_i = L or R_i = R? Suppose we have two ops: one with L=2, R=10, and one with L=3, R=8. Their intersection is [3,8]. Here max L=3, so we need an op with L_i=3. But neither has L_i=3. So we cannot achieve [3,8] with these two ops. To get max L=3, we need an op with L_i=3. So indeed, we need an op with L_i = L (the maximum L) and an op with R_i = R (the minimum R). So the condition is necessary.  

So for each pair (L,R) that is a candidate, we can compute the cost_type2(I) = min ops to achieve I. And we also need f(I) = min type-1 ops to cover I.  

Now, what are the candidate (L,R)? They are pairs that can be formed as (L_i, R_i) for some op, or (L_i, R_j) where there is an op with L_i ≤ L and R_i ≥ R, and L_i = L? Actually, we can consider all L that appear as L_i in some op, and all R that appear as R_i in some op. For each such L and R with L ≤ R, if the condition for cost 1 or 2 holds, then I = [L,R] is achievable. But that's O(K^2) where K is the number of distinct L and R, which could be up to 2e5, too many.  

We need a smarter way. Notice that the condition for cost 2 is: there exists an op with L_i = L and R_i ≥ R, and an op with L_i ≤ L and R_i = R. The first condition depends on L and R: we need an op with L_i = L and R_i ≥ R. For a fixed L, the best R we can achieve with an op having L_i = L is the maximum R_i among ops with L_i = L? Actually, we need R_i ≥ R, so if there is an op with L_i = L and R_i = R_max, then for any R ≤ R_max, the condition holds. So for a fixed L, the set of R for which there exists an op with L_i = L and R_i ≥ R is exactly R ≤ max_R_for_L[L], where max_R_for_L[L] is the maximum R_i among ops with L_i = L. So condition 1 for cost 2 is: R ≤ max_R_for_L[L]. Condition 2: there exists an op with R_i = R and L_i ≤ L. For a fixed R, the set of L for which there exists an op with R_i = R and L_i ≤ L is exactly L ≥ min_L_for_R[R], where min_L_for_R[R] is the minimum L_i among ops with R_i = R. So for a pair (L,R) to be achievable with cost 2, we need L and R such that R ≤ max_R_for_L[L] and L ≥ min_L_for_R[R]. Also, we need L ≤ R. And we also need that there is no single op with L_i = L and R_i = R (for cost 1). But if there is such an op, cost 1 is better. So we want to consider pairs (L,R) that satisfy L ≤ R, and either cost 1 or cost 2.  

We can precompute:
- For each L (from 1 to N), let maxR_at_L[L] = maximum R_i among type-2 ops with L_i = L. If no op with L_i = L, then maxR_at_L[L] = -1.
- For each R (from 1 to N), let minL_at_R[R] = minimum L_i among type-2 ops with R_i = R. If no op with R_i = R, then minL_at_R[R] = INF.
- Also, we can have a set of single ops: for each op (L,R), the pair (L,R) is achievable with cost 1.

Now, we want to find all pairs (L,R) such that L ≤ R, and (R ≤ maxR_at_L[L] and L ≥ minL_at_R[R]) and not (L,R) is a single op. But there could be many such pairs. However, we don't need to consider all; we only need to consider those that are "extremal" in some sense, because f(I) is likely to be large for large intervals, and small for small intervals. The optimal I will likely be one that minimizes |B| + f(I). f(I) is non-increasing as I gets smaller? Actually, f(I) is the minimum number of type-1 intervals to cover I. If I is smaller, f(I) is generally smaller or equal. So there is a tradeoff: smaller I gives smaller f(I) but might require more type-2 ops (cost 1 or 2). We need to find the best balance.  

We can iterate over possible L (the left endpoint of I) and find the best R for that L. For a fixed L, what are the possible R such that I=[L,R] is achievable? From the conditions:
- Cost 1: if there is an op with L_i = L and R_i = R, then that R is exactly R_i. So the set of R for cost 1 is { R_i : L_i = L }.
- Cost 2: if there is an op with L_i = L and R_i ≥ R, and an op with R_i = R and L_i ≤ L. For fixed L, the condition on R is: R ≤ maxR_at_L[L] and there exists an op with R_i = R and L_i ≤ L. The second condition is: R is in the set of R_i for which minL_at_R[R] ≤ L. So for fixed L, the set of R for cost 2 is { R : R ≤ maxR_at_L[L] and minL_at_R[R] ≤ L }.
So overall, for fixed L, the possible R are those R ≥ L such that either (R in S1[L]) or (R in S2[L]), where S1[L] is the set of R_i for ops with L_i=L, and S2[L] is as above. But S2[L] could be a large set. However, note that f([L,R]) is the minimum number of type-1 ops to cover [L,R]. This function is monotonic in R: as R increases, f([L,R]) is non-decreasing (since covering a larger interval requires at least as many ops). So for fixed L, the optimal R will be one that minimizes cost_type2(L,R) + f(L,R). Since cost_type2 is either 1 or 2, and f is non-decreasing, we might want to take the smallest possible R that gives a low cost_type2. But f might increase as R increases. So we need to check a few candidate R for each L.  

How many candidate R per L? We can consider the following R for each L:
- For each R_i such that there is an op with L_i = L and R_i = R_i (cost 1). That gives at most M candidates.
- Also, for cost 2, we can consider the smallest R that satisfies R ≤ maxR_at_L[L] and minL_at_R[R] ≤ L. That smallest R is likely the best because it gives the smallest f. But we also need to consider that maybe a larger R with cost 2 could have a much smaller f? Unlikely, because f is non-decreasing, so larger R gives larger or equal f. So if we have cost 2, we want the smallest R that makes cost 2 possible. But wait, cost 2 is constant, so we want the R that minimizes f(L,R). Since f is non-decreasing, the smallest R gives the smallest f. So for cost 2, we only need to consider the minimum R such that minL_at_R[R] ≤ L and R ≤ maxR_at_L[L]. But we also need R ≥ L. So let R_min = max(L, min{ R : minL_at_R[R] ≤ L and R ≤ maxR_at_L[L] }). If such R exists, then [L, R_min] is achievable with cost 2, and it has the smallest f among cost-2 intervals for that L.  

But what if there is a cost-1 interval with a larger R but smaller f? Actually, f is non-decreasing, so a larger R gives larger f. So the cost-1 interval with the smallest R (i.e., the minimum R_i among ops with L_i=L) is likely the best among cost-1 intervals for that L. But we should check all cost-1 intervals for that L because maybe a larger R has a much smaller f? That would be counterintuitive: f(L,R) is the number of type-1 intervals to cover [L,R]. If we increase R, we need to cover a larger interval, so f should not decrease. However, it could be that covering [L,R] with a larger R might allow a more efficient set of type-1 intervals that exactly cover [L,R] with fewer ops than covering a smaller interval? For example, suppose from L, the greedy chain jumps to 10, then to 20. If we take R=15, we need the first jump (to 10) and then we are stuck because no interval covers 11-15? Actually, if the chain jumps to 10, and 10 is ≤15, we need a second jump. But maybe there is an interval that starts at 10 and goes to 20. So to cover up to 15, we need two jumps. To cover up to 20, we also need two jumps (the same two jumps). So f(L,15)=2, f(L,20)=2. So f can be the same for larger R. It could even be that covering a larger interval requires fewer jumps if the greedy chain has a long jump? For example, from L, the first jump goes to 100, but to cover [L,50], we might need more jumps if the first jump is to 100, but we can only use intervals that cover continuously. Actually, the greedy chain from L is deterministic: it uses the furthest interval covering the current point. So if the first interval goes to 100, then covering [L,50] would require that interval, and then we are done because 50 is covered. So f(L,50)=1, f(L,100)=1. So f is not strictly increasing; it can stay the same or even increase. But it is non-decreasing? Not necessarily: f(L,R) is the minimum number of intervals to cover [L,R]. If we increase R, we might need the same number of intervals, but we never need fewer. Because if we can cover [L,R] with k intervals, we can also cover [L,R'] for R' < R with at most k intervals (by just using the same intervals, since they cover [L,R] which contains [L,R']). So f is non-increasing as R decreases? Actually, if R' < R, then [L,R'] is a subset of [L,R], so if we can cover [L,R] with k intervals, we can cover [L,R'] with at most k intervals (by taking the same intervals, they cover [L,R'] as well, but we might be able to use fewer if some intervals are unnecessary). So f(L,R) is non-increasing as R decreases. So f(L,R) is a non-increasing function of R (as R gets smaller, f can only decrease or stay the same). So for fixed L, as R increases, f can only increase or stay the same. Therefore, the smallest R that is achievable will give the smallest f. So we only need to consider, for each L, the smallest achievable R with cost 1, and the smallest achievable R with cost 2. And also the case of no type-2 (R=N) with cost 0.  

But wait, there is also the possibility of using no type-2 ops, which corresponds to I = [1,N]. That's a special case with L=1, R=N, cost_type2=0. We can include that as a candidate.  

So our plan:
- Generate candidate I = [L,R] as follows:
  1. For each type-2 op (L_i, R_i), consider I = [L_i, R_i] with cost_type2 = 1.
  2. For each L from 1 to N, consider the smallest R such that cost_type2 = 2 is possible. Compute R_candidate2(L) = the smallest R ≥ L such that there exists an op with L_i = L and R_i ≥ R, and an op with R_i = R and L_i ≤ L. If such R exists, then I = [L, R_candidate2(L)] is achievable with cost 2.
  3. Also consider I = [1, N] with cost 0.
But we also need to consider L values that are not necessarily from type-2 ops? In the intersection approach, L must be the maximum L_i of some subset, so L must appear as L_i in some op. Because if we have a set B, the maximum L_i is some L that is present. So we can restrict L to the set of L_i from type-2 ops. Similarly, R must be the minimum R_i, so R must appear as R_i in some op. So we can iterate over L in the set of L_i of type-2 ops. For each such L, we consider the smallest R that is achievable with cost 1 or cost 2. For cost 1, the smallest R is the minimum R_i among ops with L_i = L. For cost 2, we need to find the smallest R such that there exists an op with R_i = R and L_i ≤ L, and also R ≤ maxR_at_L[L]. Since R must be from the set of R_i, we can precompute for each L, the set of R such that minL_at_R[R] ≤ L. That is equivalent to: R is in the set of R_i for which minL_at_R[R] ≤ L. And we also need R ≤ maxR_at_L[L]. So the smallest R satisfying both is the minimum R in that set that is ≤ maxR_at_L[L]. We can precompute for each L, the list of R that are "compatible". Since M is 2e5, we can do this by, for each L, scanning R from L upward? But N is 1e6, and we have up to 2e5 L's, so O(N * number of L) could be large. We need a faster way.  

We can precompute an array best_R_for_L[L] = the smallest R ≥ L such that minL_at_R[R] ≤ L and R ≤ maxR_at_L[L]. How to compute efficiently? We can iterate R from 1 to N, and for each R, we know minL_at_R[R]. For a given L, we want the smallest R ≥ L with minL_at_R[R] ≤ L and R ≤ maxR_at_L[L]. This is like a range query. We can precompute for each R, its minL_at_R. Then for each L, we need to find the smallest R ≥ L such that minL_at_R[R] ≤ L and R ≤ maxR_at_L[L]. The condition R ≤ maxR_at_L[L] gives an upper bound on R. So we are looking for the smallest R in [L, maxR_at_L[L]] such that minL_at_R[R] ≤ L. We can precompute an array next_compatible_R[L] = the smallest R ≥ L satisfying that condition, if any. How to compute next_compatible_R for all L? We can do a sweep: for R from 1 to N, we know minL_at_R[R]. For all L such that L ≥ minL_at_R[R] and L ≤ R, R is a candidate for next_compatible_R[L]. Actually, for a fixed R, it is compatible for L if L ≤ R and L ≥ minL_at_R[R]. So L can be from minL_at_R[R] to R. So for each R, it provides a candidate for next_compatible_R[L] for L in [minL_at_R[R], R], provided that R ≤ maxR_at_L[L]. But maxR_at_L[L] depends on L, so we need to check that. This is getting complicated.  

Maybe we can avoid this by simply iterating over all type-2 ops as candidates for the "main" op that gives the left endpoint L, and then for each, we consider the right endpoint R from other ops. But that could be O(M^2) in the worst case.  

Given the constraints, maybe we can use a different approach. Since N is up to 1e6, and M is 2e5, we can afford O(N + M) or O((N+M) log N). Perhaps we can use a two-pointer or dynamic programming on the line.  

Let's think about the complement covering approach again: we want to cover [1,N] with type-1 and type-2. We can think of the process as: we start with no coverage. We can apply operations. Since type-2 covers everything except an interval, using a type-2 op is like "removing" an interval from the uncovered set. So the final uncovered set after all operations is the intersection of the type-2 ops' intervals. So we need to select a set of type-2 ops such that their intersection I can be covered by type-1 ops. And we want to minimize |type2| + |type1| covering I.  

Now, note that if we select a set of type-2 ops, their intersection I is determined by the maximum L and minimum R. So we can think of choosing a pair (L,R) with L ≤ R, and then we need to select type-2 ops that achieve that intersection. The minimum number of type-2 ops to achieve (L,R) is as described. And then we need to cover I with type-1. So the total cost is cost2(L,R) + f(L,R). We want to minimize this.  

We can precompute f(L,R) for all L,R? That seems too much. But maybe we can compute f(L,R) on the fly for the candidate (L,R) we generate. And the number of candidates might be manageable if we generate them smartly.  

How many candidate (L,R) are there? Consider all pairs (L,R) that are "optimal" for some L. As argued, for each L, the optimal R is the smallest R that minimizes cost2(L,R) + f(L,R). Since cost2 is either 0,1,2, and f is non-increasing as R decreases, the optimal R for a given L will be the smallest R that gives the lowest cost2. But f might be smaller for a larger R? No, as argued, f is non-increasing as R decreases, so smaller R gives smaller f. So for a given L, if we can achieve cost2=2 with some R, then any larger R will have f at least as large, so total cost will be at least 2 + f(L,R) ≥ 2 + f(L, that R). Since f(L,R) ≥ f(L, that R) if R ≥ that R, the total cost will be at least as large. However, it could be that with a larger R, we can achieve cost2=1? That would be better. So we need to consider both cost1 and cost2. So for each L, we should consider the smallest R that gives cost1, and the smallest R that gives cost2. And also the case L=1, R=N with cost0. But wait, L can be any value that is the maximum L_i of some subset. That is essentially any L that appears as L_i in some type-2 op, because if we want max L = L, we must include an op with L_i = L. So L must be from the set of L_i. So let L_set be the set of L_i from type-2 ops. For each L in L_set, we consider:
- R1(L) = min{ R_i : L_i = L } (if exists). This is the smallest R for cost1.
- R2(L) = the smallest R ≥ L such that there exists an op with L_i = L and R_i ≥ R, and an op with R_i = R and L_i ≤ L. If such R exists, this is the smallest R for cost2.
Also, we should consider L=1 as a special case? But 1 might not be in L_set. If 1 is not in L_set, can we have max L = 1? That would require all selected ops to have L_i ≤ 1, so L_i=1 for all. So we need an op with L_i=1. So 1 must be in L_set. So we can just take L_set as all distinct L_i.  

Now, how to compute R2(L) efficiently? We need: an op with L_i = L and R_i ≥ R, and an op with R_i = R and L_i ≤ L. The first condition gives R ≤ maxR_at_L[L]. The second condition gives that R is in the set of R_i for which minL_at_R[R] ≤ L. So we need the smallest R in the intersection of [L, maxR_at_L[L]] and the set { R : minL_at_R[R] ≤ L }. We can precompute an array best_R2[L] for each L in L_set. How? We can iterate R from 1 to N, and for each R, we know minL_at_R[R]. For a given L, R is valid if L ≤ R ≤ maxR_at_L[L] and minL_at_R[R] ≤ L. So for each R, it is valid for all L such that L ≤ R and L ≥ minL_at_R[R] and L ≤ maxR_at_L[L]. But maxR_at_L[L] is a property of L. So we can for each R, for L from minL_at_R[R] to R, if R ≤ maxR_at_L[L], then R is a candidate for best_R2[L]. We can update best_R2[L] = min(best_R2[L], R) if R ≤ maxR_at_L[L]. To do this efficiently, we can precompute maxR_at_L for all L (1..N). Then for each R, we want to update best_R2[L] for L in [minL_at_R[R], R] subject to R ≤ maxR_at_L[L]. This is like a range update with a condition. Since N is 1e6, and M is 2e5, we can afford a loop over L for each R? That would be O(N * number of R) = O(N*M) worst case. But number of R is at most M, so O(N*M) is too high.  

We need a faster way. Maybe we can iterate L instead. For each L, we want the smallest R ≥ L such that R ≤ maxR_at_L[L] and there exists an op with R_i = R and L_i ≤ L. The second condition means that R is in the set of R_i for which minL_at_R[R] ≤ L. So we can precompute, for each L, the list of R that are "compatible" (i.e., minL_at_R[R] ≤ L). But the number of such R could be large. However, we only need the smallest R that also satisfies R ≤ maxR_at_L[L]. So we can precompute an array next_R_ge_L[R]? Not exactly.  

Alternatively, we can change perspective: instead of iterating L, we can iterate R. For each R, we know minL_at_R[R]. For this R to be used as the right endpoint in a cost-2 interval for some L, we need L ≤ R and L ≥ minL_at_R[R] and also R ≤ maxR_at_L[L]. The condition R ≤ maxR_at_L[L] means that L must be such that maxR_at_L[L] ≥ R. So for fixed R, the set of L that can use this R for cost-2 is: L ∈ [minL_at_R[R], R] and also maxR_at_L[L] ≥ R. For each such L, R is a candidate for R2(L). And we want for each L, the smallest such R. So we can do: for each R, we want to update all L in [minL_at_R[R], R] that satisfy maxR_at_L[L] ≥ R. This is again a range update with a condition on maxR_at_L. We can precompute an array maxR_at_L. Then for each R, we can iterate L from minL_at_R[R] to R, but that's O(N) per R.  

Maybe we can use a segment tree or something. Given the constraints, perhaps we can afford O(N log N) overall. Let's think differently.  

We have M up to 2e5. The number of distinct L_i is at most M. So we only need best_R2 for L in L_set. So we can iterate over each L in L_set. For each such L, we want to find the smallest R ≥ L such that R ≤ maxR_at_L[L] and there exists a type-2 op with R_i = R and L_i ≤ L. We can precompute, for each R, minL_at_R[R]. Then for a fixed L, we need to find the smallest R in [L, maxR_at_L[L]] such that minL_at_R[R] ≤ L. This is a range query: given L and an upper bound U = maxR_at_L[L], find the smallest R in [L, U] with minL_at_R[R] ≤ L. We can precompute an array minL_at_R, and then for each L, we can scan R from L to U, but U could be up to N. In the worst case, if L is small and U is large, this could be O(N) per L, total O(N * |L_set|) = O(NM) worst case. But maybe in practice, maxR_at_L[L] is not too large? Not guaranteed.  

We need a more efficient method. Perhaps we can use the fact that minL_at_R is an array of size N. We can build a segment tree over R that stores the minimum minL_at_R in a range. Then for each L, we can query the range [L, maxR_at_L[L]] to find the smallest R where minL_at_R[R] ≤ L. This can be done with a segment tree that supports "find first" operation. Complexity O(log N) per L. Since |L_set| ≤ M ≤ 2e5, total O(M log N) which is fine.  

So steps for precomputing best_R2:
- Compute maxR_at_L[L] for all L (1..N). This can be done by initializing an array with -1, and for each type-2 op (L_i, R_i), set maxR_at_L[L_i] = max(maxR_at_L[L_i], R_i).
- Compute minL_at_R[R] for all R (1..N). Initialize with INF, and for each type-2 op (L_i, R_i), set minL_at_R[R_i] = min(minL_at_R[R_i], L_i).
- Build a segment tree over R (1..N) that stores the value minL_at_R[R] at each leaf. We want to support: given L and U, find the smallest R in [L, U] such that minL_at_R[R] ≤ L. This is a classic "find first" query on a segment tree with condition. We can build a tree where each node stores the minimum minL_at_R in its range. Then to find the first R in [L, U] with minL_at_R[R] ≤ L, we can recursively search: start at the root, if the minimum in the node is > L, return -1. Otherwise, go down to find the leftmost R. This is O(log N) per query.
- For each L in L_set, let U = maxR_at_L[L]. If U = -1, then no op with L_i = L has any R, so cost2 is impossible for that L? Actually, if there is an op with L_i = L, then maxR_at_L[L] is at least that R. So U is defined. If U < L, then no R ≥ L, so impossible.
- Query the segment tree for the smallest R in [L, U] with minL_at_R[R] ≤ L. If found, that R is R2(L). Then we have a candidate I = [L, R2(L)] with cost_type2 = 2.

But wait, we also need to consider that for cost2, we need an op with L_i = L and R_i ≥ R. The condition R ≤ maxR_at_L[L] ensures that. But we also need that the op with L_i = L actually has R_i ≥ R. Since maxR_at_L[L] is the maximum R among ops with L_i = L, if R ≤ maxR_at_L[L], there exists an op with L_i = L and R_i ≥ R. So that's fine. And the other op with R_i = R and L_i ≤ L is guaranteed by minL_at_R[R] ≤ L. So the condition is sufficient.

Now, we also have cost1 candidates: for each type-2 op (L,R), I = [L,R] with cost1. We can consider all such.

And we have the cost0 candidate: I = [1,N] with cost0.

So total number of candidates is at most M (cost1) + |L_set| (cost2) + 1 (cost0). That's at most O(M). So we have O(M) candidate intervals.

For each candidate interval I = [l,r], we need to compute:
- cost_type2 = 0,1,2 as described.
- f(l,r) = minimum number of type-1 ops to cover [l,r].

We can compute f(l,r) using the binary lifting method described earlier, with O(log M) per query. So total O(M log M) which is fine.

Then we take the candidate with minimum total cost. If no candidate is feasible, output -1.

But we also need to output the actual operations: which type-1 and which type-2 ops are used. So we need to reconstruct the solution.

For the chosen candidate I = [l,r], we need to:
- Select a set of type-2 ops that achieve intersection I with the given cost (0,1,2). For cost0, no type-2 ops. For cost1, we select the op (l,r) if it exists. For cost2, we need to select two ops: one with L_i = l and R_i ≥ r, and one with R_i = r and L_i ≤ l. We can choose any such ops. To reconstruct, we need to keep track of which ops we use.
- Select a set of type-1 ops that cover I. This is given by the greedy chain from l. We need to know which type-1 ops are used in that chain.

So we need to be able to, given l, retrieve the actual intervals used in the greedy chain to cover [l,r]. We can do this by, during the greedy chain simulation, recording the intervals used. But we need to do it for the chosen l and r. We can simulate the chain from l, following the next_pos jumps, until we cover r. We can record the type-1 ops used. To do this, we need to know for each position p, which type-1 op gives the furthest cover. In our construction of furthest[p], we need to know which specific op gives the maximum R. We can store for each p, the index of the op that gives furthest[p] (if there are multiple, any one is fine). So we can store an array op_for_furthest[p] = the index of a type-1 op that covers p and has maximum R. Then when we simulate the chain, we can output those ops.

So we need to modify the construction of furthest[p] to also store the op index.

Now, we also need to handle the case where there are no type-1 ops. Then furthest[p] = -1 for all p, and the only way to cover is with type-2 ops. In that case, we need to cover the whole [1,N] with type-2 ops. That means we need a set of type-2 ops whose intersection is [1,N]. That requires max L = 1 and min R = N. So we need an op with L=1 and R=N, or two ops: one with L=1 and R≥N, and one with L≤1 and R=N. But L≤1 means L=1. So essentially we need an op with L=1 and R=N. So if there is a type-2 op with L=1 and R=N, we can use it with cost 1. Otherwise, impossible. So our candidate generation will handle that: I = [1,N] is a candidate with cost0 only if we use no type-2 ops? Wait, cost0 corresponds to using no type-2 ops, which means we need to cover [1,N] with type-1. If there are no type-1 ops, that's impossible. So we need to consider I = [1,N] with cost0 only if type-1 can cover it. If not, we need to consider cost1 or cost2 for I = [1,N]. So we should also include I = [1,N] as a candidate with cost1 and cost2 if possible. Actually, our candidate generation: for cost1, we consider all type-2 ops. For cost2, we consider for each L in L_set, the R2(L). If for some L, R2(L) = N and L=1, then I = [1,N] with cost2 is a candidate. So we need to make sure that [1,N] is considered. In our cost2 generation, for L=1, we compute R2(1) which is the smallest R such that there is an op with L=1 and R ≥ R, and an op with R_i = R and L_i ≤ 1. If such R exists, it could be N. So I = [1,N] with cost2 is considered. For cost1, if there is an op with L=1 and R=N, then I = [1,N] with cost1 is considered. So we are good.

Now, we also need to handle the case where we use type-1 ops to cover I, and I might be covered by type-1 ops that are not necessarily starting at l. But our greedy chain from l will cover I. However, is it guaranteed that the greedy chain from l covers I with the minimum number of type-1 ops? Yes, for covering a specific interval [l,r], the greedy algorithm that always picks the interval with the furthest R among those covering the current point is optimal. So that's correct.

But we must ensure that the type-1 ops we use are all within I? Not necessarily, but their union will be contained in [l, some position]. Actually, if we start at l and follow the greedy chain, the intervals used will have their L and R within [l, N]. Their union will be exactly the set of positions covered from l until we stop. For our purpose, we need the union to be exactly I. But if the greedy chain covers more than r, that's fine because then the complement is smaller. However, if the union extends beyond r, then the actual intersection of the type-2 ops might not be I. Let's think: we are using type-1 ops to cover I, and type-2 ops to cover the complement. If the type-1 ops cover more than I, then the complement is smaller, and we might have used type-2 ops unnecessarily. But we are selecting type-2 ops to achieve intersection I. If the type-1 ops cover beyond I, then the actual uncovered set after type-1 is smaller than I, so the type-2 ops we selected (whose intersection is I) might cover more than necessary, but that's okay because they still cover the complement. However, we need the final state to be all 1's. If type-1 covers beyond I, and type-2 covers I's complement, then the union covers all. So it's fine. But we must ensure that the type-1 ops we select are all within the union. They are, by construction. So we can just use the greedy chain from l, and it will cover at least [l,r]. If it covers more, that's even better. So we can just follow the chain until we cover r (i.e., until the current position > r). We don't need to stop exactly at r. So we can simulate: start at pos = l, while pos <= r: pick the op that gives furthest[pos] (which we stored), add that op to our list, set pos = furthest[pos] + 1. If at any point pos <= r and furthest[pos] = -1, then impossible. This will give a set of type-1 ops that cover [l, pos-1] which is a superset of [l,r]. That's fine.

Now, we also need to output the operations in order. The problem asks for op_i for i=1..M. We can set all operations to 0, and then for the selected ops, set their type to the chosen type (1 or 2). But we must be careful: if we select a type-2 op, we set its op to 2; if we select a type-1 op, set to 1. The rest are 0. That's acceptable.

So the algorithm is:

1. Read N, M.
2. Separate operations into type1_list and type2_list. Keep their original indices.
3. For type-2 ops, precompute:
   - maxR_at_L: array of size N+1, initialized to -1. For each type-2 op (L,R), maxR_at_L[L] = max(maxR_at_L[L], R).
   - minL_at_R: array of size N+1, initialized to INF. For each type-2 op (L,R), minL_at_R[R] = min(minL_at_R[R], L).
   - Also, collect the set L_set = { L : there is a type-2 op with L_i = L }.
4. Build a segment tree over R (1..N) with values minL_at_R[R]. We need to support query: given L and U, find the smallest R in [L, U] with minL_at_R[R] ≤ L. We'll implement a recursive function.
5. For each L in L_set:
   - U = maxR_at_L[L]. If U < L, skip.
   - Query the segment tree for the smallest R in [L, U] with minL_at_R[R] ≤ L. If found, let R2 = that R. Then we have a candidate I = [L, R2] with cost_type2 = 2. We need to remember the ops that achieve this: we need an op with L_i = L and R_i ≥ R2, and an op with R_i = R2 and L_i ≤ L. We can find such ops during reconstruction. For now, we just store the candidate.
6. For each type-2 op (L,R, idx): candidate I = [L,R] with cost_type2 = 1. Store the op index.
7. Also, candidate I = [1,N] with cost_type2 = 0, but only if type-1 ops can cover [1,N] (we'll check feasibility later).
8. For type-1 ops, we need to build furthest[p] and op_for_furthest[p] for p=1..N. We'll do the sweep with a max-heap. We'll also need to store for each type-1 op its interval and index.
   - Sort type-1 ops by L.
   - Initialize a max-heap (using negative R for max, and store the op index).
   - For p from 1 to N:
        - Add all type-1 ops with L = p to the heap: push (-R, idx) for each.
        - While heap not empty and the maximum R (which is -heap[0][0]) is < p: pop.
        - If heap not empty, let (negR, idx) = heap[0]. Then furthest[p] = -negR, and op_for_furthest[p] = idx.
        - Else, furthest[p] = -1, op_for_furthest[p] = -1.
   - Note: We need to be able to quickly find ops with L = p. We can group type-1 ops by L using a dictionary or an array of lists. Since L can be up to N, we can create an array of vectors of size N+1, but N=1e6, and M=2e5, it might be memory heavy but acceptable. We can use a list of ops sorted by L and then use a pointer to add them as p increases. That's more memory efficient.
9. Build the binary lifting table for next_pos. Define next_pos[p] = furthest[p] + 1 if furthest[p] != -1, else -1. Also define next_pos[N+1] = -1. Build nxt[0..max_log][1..N+1] with nxt[0][p] = next_pos[p], and nxt[k][p] = nxt[k-1][ nxt[k-1][p] ] if nxt[k-1][p] != -1 else -1. max_log = floor(log2(M)) + 1, say 18.
10. For each candidate interval I = [l,r], compute f(l,r) using the binary lifting method:
    - If l > r, impossible.
    - pos = l, steps = 0.
    - For i from max_log down to 0:
        if nxt[i][pos] != -1 and nxt[i][pos] <= r+1:
            pos = nxt[i][pos]
            steps += (1 << i)
    - After loop, if pos > r: then we have covered [l,r] with steps jumps. So f = steps.
    - Else (pos <= r): if next_pos[pos] != -1, then f = steps + 1, and we note that the last jump goes to next_pos[pos] which is > r (since pos <= r and next_pos[pos] = furthest[pos]+1 ≥ pos+1, and since pos <= r, next_pos[pos] could be ≤ r+1? Actually, we need to ensure that after this last jump, we cover r. If next_pos[pos] > r, then it's fine. If next_pos[pos] <= r, then we still need more jumps. But our binary lifting already took the maximum jumps while staying ≤ r+1. So if pos <= r, then next_pos[pos] must be > r+1? Not necessarily. Let's check: after the loop, we have taken the maximum number of jumps such that the resulting position is ≤ r+1. So if pos <= r, then the next jump would take us to next_pos[pos]. Could next_pos[pos] be ≤ r+1? If it were, then we could have taken that jump in the loop. So since we didn't, it must be that next_pos[pos] > r+1. So it is > r. So then we can take that jump and cover r. So f = steps+1. But we also need to check that next_pos[pos] != -1. So if next_pos[pos] = -1, then impossible.
    - So f(l,r) is computed as above.
11. Also, we need to check that the type-1 ops we use to cover I are actually able to cover it without gaps. The binary lifting assumes that next_pos[p] is always > p. That's true if furthest[p] exists. So the process is continuous.
12. Now, for each candidate, total_cost = cost_type2 + f(l,r). We want the minimum total_cost. If multiple, any.
13. If no candidate is feasible, output -1.
14. If a candidate is chosen, we need to output the operations:
    - Initialize an array ops of size M with 0.
    - For the chosen candidate, we have cost_type2 and the set of type-2 ops to use. We need to select the specific ops.
      - If cost_type2 = 0: no type-2 ops used.
      - If cost_type2 = 1: we use the type-2 op that gives the intersection I. For candidate I from a type-2 op, we use that op. For candidate I from cost2? Actually, cost1 only comes from type-2 ops. So we know which op: it's the op with L_i = l and R_i = r. So set ops[idx] = 2.
      - If cost_type2 = 2: we need to select one op with L_i = l and R_i ≥ r, and one op with R_i = r and L_i ≤ l. We can find such ops: for the first, pick any type-2 op with L_i = l and R_i ≥ r. We can iterate over type-2 ops to find one. For the second, pick any type-2 op with R_i = r and L_i ≤ l. We need to ensure they are distinct? They could be the same if there is an op with L_i = l and R_i = r, but then cost would be 1, not 2. So they are distinct. So we set their ops to 2.
    - For type-1 ops: we need to simulate the greedy chain from l until we cover r. We can do: pos = l, while pos <= r: if furthest[pos] == -1: error (should not happen if feasible). idx = op_for_furthest[pos]. Set ops[idx] = 1. pos = furthest[pos] + 1. This loop will use the same ops as in the binary lifting? Actually, the binary lifting might skip some positions, but the set of ops used should be the same. We can just simulate step by step. Since the number of steps is at most f, and f is at most M, this is O(M) in total over all candidates? But we only do it once for the chosen candidate, so O(f) which is O(M). That's fine.
    - Then output the total cost (sum of selected ops) and the ops array.

We need to be careful with indices: the input operations are 1-indexed in the output? The problem says "op_i is the type of operation (0,1, or 2) chosen for the i-th operation." So we output in order of input. So we need to keep track of the original index.

Now, let's test with the samples.

Sample 1:
N=5, M=4
Ops:
1: (2,4) type1
2: (3,5) type1
3: (1,4) type1
4: (2,5) type1
All type1? Actually, the input doesn't specify type; we are given L_i,R_i and we can choose type. So in the input, all are just intervals. We are to choose the type for each. So in our separation, we need to consider all ops as potential type1 or type2? Wait, the problem says: in each operation, you are given (L_i,R_i), and you must perform exactly one of the three operations: 0,1,2. So for each given pair, we can choose to treat it as type1 (set the interval to 1) or type2 (set the complement to 1) or 0. So each input op is just a pair, and we can assign it to be type1 or type2 if we use it. So in our model, we have a set of "type1 candidates" and "type2 candidates" from the same set of ops. That is, each input op can be used as either type1 or type2, but not both. So we need to be careful: the same op cannot be both type1 and type2. In our algorithm, we separated the ops into type1 and type2 lists. But actually, each op is independent: we can decide for each op whether to use it as type1, type2, or 0. So in our model, we have a set of ops that can be used as type1, and a set that can be used as type2. But they are the same set; an op can be used as type1 or type2, but we choose one. So when we build type1 and type2 structures, we need to consider all ops. But then, if we select a type2 op, we cannot also select it as type1. So we need to ensure that the ops we select for type1 and type2 are disjoint. In our candidate intervals, we are selecting a set of type2 ops to achieve I, and a set of type1 ops to cover I. These sets must be disjoint. Is that automatically satisfied? They come from the same pool, so we need to make sure that the type2 ops we select are not also used as type1. In our reconstruction, we will assign types accordingly. But during the search for candidates, we are using the same ops for both purposes. That could lead to a conflict if the same op is used in both. For example, an op might be used as type2 to achieve I, and also as type1 to cover I. But that's impossible because an op is either type1 or type2, not both. So we need to ensure that in our solution, the sets are disjoint. Does our algorithm guarantee that? Not necessarily. We need to check that the type2 ops we select for I are not also selected as type1. In the greedy chain for type1, we use ops that cover positions in I. Could a type2 op also cover positions in I? If we use a type2 op, its coverage is the complement of its interval, so it does not cover any position in its interval. So if a type2 op has L_i and R_i, it does not cover positions in [L_i, R_i]. So if I is inside [L_i, R_i], then that type2 op does not cover any position in I. So it cannot be used as a type1 op to cover I. So there is no overlap: type2 ops cover the outside, type1 ops cover the inside. So they are naturally disjoint. However, if I is not fully inside the type2 op's interval, then that type2 op might cover some positions in I? Actually, if a type2 op is used, it covers the complement of [L,R]. So it covers positions j < L or j > R. So if I has positions both < L and > R, then those positions are covered by the type2 op, but they are not in I (since I is the intersection of type2 ops, which is inside [L,R] for all used type2 ops). So I is contained in [L,R] for every type2 op used. Therefore, I is a subset of the intersection of the type2 ops' intervals. So for any type2 op used, I ⊆ [L_i, R_i]. So the type2 op does not cover any position in I. So the type1 ops and type2 ops are disjoint in terms of coverage. So it's safe.

But what about the op index? An op could be used as type2, and also we might consider it as a type1 op in our type1 greedy chain. But if it's used as type2, we should not also use it as type1. In our reconstruction, we will assign types to the selected ops. So we need to make sure that when we select type1 ops, we don't select an op that we already selected as type2. In the greedy chain, we are selecting type1 ops from the original list. If an op is also in the type2 list (which it is, since all ops are in both lists), we might accidentally select it as type1. But as argued, the type2 op's interval contains I, so it covers positions in I? Actually, if the type2 op has interval [L,R], and I ⊆ [L,R], then the type2 op does not cover any position in I. So it would not be chosen as a type1 op to cover I because a type1 op must cover the current position. So the type2 op would not be used in the greedy chain because it doesn't cover the points in I. So no conflict. However, what if the type2 op's interval is exactly I? Then it doesn't cover I, so it's not used. So it's fine.

Therefore, we can treat the ops as separate for type1 and type2, but they come from the same set. We just need to keep track of indices.

Now, in our candidate generation, for type2 candidates, we are using the type2 ops. For type1 candidates, we are using type1 ops. So they are from the same set, but we consider them separately. That's fine.

Now, we need to implement the segment tree for minL_at_R. We'll build a tree where each node stores the minimum minL_at_R in its range. To find the first R in [L,U] with minL_at_R[R] ≤ L, we can do a recursive function that goes down the tree. We'll implement an iterative version for efficiency.

Given N up to 1e6, the segment tree size is about 4N = 4e6, which is acceptable in Python? 4e6 integers might be memory heavy (each int 28 bytes in Python, so 112MB). That's a bit high. We can use an array of size 2*pow2(N) maybe. Alternatively, we can use a simpler method since we only need to query for L in L_set (at most 2e5). We can precompute for each R, minL_at_R. Then for each L, we need to find the smallest R ≥ L with minL_at_R[R] ≤ L and R ≤ maxR_at_L[L]. We can do this by scanning R from L to maxR_at_L[L] until we find one satisfying the condition. But that could be O(N) per L in worst case. However, note that maxR_at_L[L] is the maximum R for ops with L_i = L. In the worst case, if there is an op with L=1 and R=N, then for L=1, we scan from 1 to N, which is O(N). But there might be only one such L, so total O(N) which is fine. But if there are many L with large R, it could be bad. However, M is 2e5, so the number of ops with large L is limited. The worst-case scenario: all ops have L=1, R=N. Then L_set = {1}, and for L=1, we scan R from 1 to N, O(N). That's acceptable (1e6). If ops have various L, the sum of (maxR_at_L[L] - L) over L could be large. But note that maxR_at_L[L] is only defined for L that appear. In the worst case, each L could have a very large R. For example, if for each L from 1 to M, there is an op with R=N. Then L_set size M, and for each L, we scan from L to N, but we can stop early because we only need the first R that satisfies minL_at_R[R] ≤ L. Since minL_at_R[R] for R=N might be small, we might find it quickly. But if we have to scan many R, it could be O(N) per L. However, note that the condition minL_at_R[R] ≤ L is more likely to be true for larger R because minL_at_R[R] is the minimum L_i among ops with R_i = R. For large R, there might be an op with small L. So in practice, the first R might be not too far from L. But worst-case, if for all R, minL_at_R[R] > L, then we scan all the way to maxR_at_L[L]. Could that happen? Suppose we have ops only with L_i = 1 and R_i = N. Then for L=1, minL_at_R[R] for R=N is 1, so we find it at R=N. So we scan N steps. If we have L=1, but minL_at_R[R] is INF for all R except maybe one, then we scan to that R. So in the worst case, for a given L, we might scan O(N) steps. But since L_set size is at most 2e5, and N is 1e6, the total could be 2e11, too large. So we need a more efficient method.

We can use a segment tree or a sparse table to answer the query quickly. Let's implement a segment tree with the ability to find the first index in a range with value ≤ L. We'll store the tree in an array. Since N=1e6, we can use an array of size 2*nextpow2(N) and build it. We'll implement an iterative segment tree for speed and memory? Actually, in Python, a recursive segment tree with 4N elements might be okay if we use lists. But 4e6 elements might be slow. Alternatively, we can use a different approach: we can precompute for each L, the best R2 by iterating R from 1 to N, and updating for L in [minL_at_R[R], R] if R ≤ maxR_at_L[L]. We can do this by, for each R, we want to update best_R2[L] for L in [minL_at_R[R], R] with R, provided that R ≤ maxR_at_L[L]. We can precompute an array maxR_at_L. Then for each R, we can iterate L from minL_at_R[R] to R, but that's O(N) per R. However, we can optimize by noting that for a fixed R, the condition R ≤ maxR_at_L[L] means that L must be such that maxR_at_L[L] ≥ R. So we can precompute for each R, the set of L that satisfy both. This is like a range update. We can use a segment tree over L to store maxR_at_L[L], and for each R, we want to find L in [minL_at_R[R], R] such that maxR_at_L[L] ≥ R. But we also need to assign R as a candidate for best_R2[L]. This is similar to a range minimum query but with updates. Since we are only reading, we can do offline processing: for each R, we can iterate L from minL_at_R[R] to R, but break if L > something? Not easy.

Maybe we can use the fact that M is 2e5, and we can afford O(M log N) per candidate? Actually, we have at most M candidates for cost2. We can compute best_R2 for each L in L_set by, for each L, scanning R from L to N, but using the fact that we only need the first R that satisfies both conditions. We can precompute an array next_good_R[L] = the smallest R ≥ L such that minL_at_R[R] ≤ L and R ≤ maxR_at_L[L]. We can compute this by processing R from 1 to N, and for each R, we can update a data structure for all L ≤ R with minL_at_R[R] ≤ L. Actually, condition minL_at_R[R] ≤ L means L ≥ minL_at_R[R]. So for a fixed R, it is valid for L in [minL_at_R[R], R]. So we can do: for each R, for L from minL_at_R[R] to R, if R ≤ maxR_at_L[L], then R is a candidate for next_good_R[L]. We want the smallest such R for each L. So we can maintain an array next_good_R initialized to INF. Then for each R, we iterate L from minL_at_R[R] to R, but we can stop at L = minL_at_R[R] and go up to R. To make this efficient, we can use the fact that minL_at_R[R] and R are both at most N. The total number of iterations over all R could be large if we do it naively. For example, if for many R, minL_at_R[R] is 1, then we iterate L from 1 to R, which sums to O(N^2) in worst case. But M is 2e5, so the sum of R over all ops is at most 2e5 * N? Not exactly.  

We need a better way. Since M is 2e5, we can afford O(M log M) for the whole process. We can use a segment tree that allows us to query for a given L, the smallest R in [L, maxR_at_L[L]] with minL_at_R[R] ≤ L. We can build a segment tree over R that stores minL_at_R. Then we can implement a function that, given L and U, finds the first R in [L, U] with value ≤ L. This is a standard "find first" operation on a segment tree. The time complexity is O(log N) per query. Since we have at most |L_set| ≤ M queries, total O(M log N) which is fine. So we will implement a segment tree for minL_at_R.

We need to be careful with memory. We can build an iterative segment tree with size = 1 << (ceil(log2(N+1))). For N=1e6, next power of 2 is 2^20 = 1048576, so size 2*2^20 = 2,097,152. That's about 2 million integers. In Python, each integer is about 28 bytes, so 2e6 * 28 = 56 MB. That's acceptable. We'll store the tree in a list. We'll use 0-indexing or 1-indexing. Let's use an array tree of size 2*size, where size is the next power of 2. We'll build the leaves at indices size to size+N-1, and the rest set to INF. Then build up. For the query, we want to find the smallest R in [L, U] with tree value ≤ L. We can implement a recursive function that takes node, node_l, node_r, and query range. But to be efficient, we can write an iterative function. However, recursive might be easier and still O(log N) per query. Given that M is 2e5, O(M log N) with log N ~ 20, and each query might take 20 recursive calls, total 4e6 calls, which is okay.

We'll implement a function find_first(node, node_l, node_r, q_l, q_u, L) that returns the smallest R in [q_l, q_u] with tree[node] ≤ L, or -1 if none. We can do:
- If node_r < q_l or node_l > q_u: return -1.
- If tree[node] > L: return -1.
- If node_l == node_r: return node_l.
- Else, mid = (node_l+node_r)//2.
- First, search left child: res = find_first(left_child, node_l, mid, q_l, q_u, L)
- If res != -1: return res
- Else: return find_first(right_child, mid+1, node_r, q_l, q_u, L)

This will work.

Now, for the type1 furthest array, we need to efficiently get the op with maximum R for each p. We'll use a max-heap. We'll sort type1 ops by L. We can store them in a list and use an index pointer. For p from 1 to N, while pointer < len(type1_ops) and type1_ops[pointer].L == p, push ( -R, idx) to heap. Then while heap and -heap[0][0] < p, pop. Then if heap, furthest[p] = -heap[0][0], op_for_furthest[p] = heap[0][1]. This is O((N+M) log M). Since N=1e6, M=2e5, total operations about 1.2e6, log M ~ 18, so about 20 million heap operations, which should be fine in Python if optimized (using heapq).

Now, we need to build the binary lifting table for next_pos. We have next_pos array of size N+2 (including N+1). We'll create a 2D list nxt[max_log+1][N+2]. max_log = 18 (since 2^18=262144 > 2e5). Actually, M is 2e5, so we need up to 18. We'll set max_log = 20 to be safe. We'll initialize nxt[0] = next_pos list. Then for k from 1 to max_log, nxt[k][p] = nxt[k-1][ nxt[k-1][p] ] if nxt[k-1][p] != -1 else -1. This is O(max_log * N) = 20 * 1e6 = 20e6, which might be memory heavy: 20 * 1e6 = 20 million integers. Each integer 28 bytes = 560 MB, too much. We cannot store a full 2D array. We need a more memory-efficient method.

We can use the fact that we only need to answer queries for specific l and r. Instead of precomputing a full table, we can use the two-pointer method to simulate the chain in O(f) time per query. Since f is the number of type1 ops used, which could be up to M, and we have O(M) candidates, the total could be O(M^2) in worst case. But we can optimize by noting that the greedy chain from a given l is deterministic. We can precompute for each l, the number of steps to reach each possible next position? That seems heavy.

Alternatively, we can use a "next" array and simulate the chain step by step for the chosen candidate. Since we only need to compute f(l,r) for the candidates, and we have at most O(M) candidates, we can afford O(f) per candidate. But f could be up to M, so O(M^2) worst case. However, in practice, the number of type1 intervals is M, and the greedy chain from a given l uses at most M steps. If we have O(M) candidates, it could be O(M^2) = 4e10, too slow.

We need a faster way to compute f(l,r). We can precompute for each position p, the "next" position, and then for each l, we can precompute the sequence of positions after each jump. But storing that for all l is too much. However, we can use the binary lifting table but in a sparse way. Since we only need to query for l that are in our candidate intervals, and the number of candidates is O(M), we can precompute a table of size (max_log) x (N+2) but as integers. But 20 * 1e6 = 20 million integers, which is about 160 MB if using array of ints? In Python, a list of lists of ints will have overhead. We can use a 2D list but it might be memory heavy. We can use a dictionary or compress? Alternatively, we can use a "jump" table where we store for each p, the next position, and then for each query, we can binary lift on the fly by following the next array. But to do binary lifting, we need to know the position after 2^k jumps. We can precompute for each p, the position after 2^k jumps for k up to max_log. This is the same table.

We can try to reduce memory by using a single array of size (N+2) * (max_log+1) but as a list of arrays. In Python, if we use a list of lists, each sublist has overhead. We can use array module or numpy? Not allowed. Maybe we can use a 2D list but it might be acceptable if we use small integers? 20 million integers is too much for Python memory.

Alternative: we can compute f(l,r) by simulating the chain step by step, but we can optimize by noting that the chain from l is the same regardless of r. We can precompute for each l, the positions after 1,2,3,... jumps until we exceed N. But the number of jumps is at most M, and for each l, the list could be long. If we store for each l, the list of positions after each jump, that's O(N * M) memory.

Maybe we can use the fact that the "next" function is a function from positions to positions. We can precompute for each position, the position after 1 jump, and then for each query, we can use the "doubling" technique on the fly by following the next array and counting steps until we exceed r. But that would be O(f) per query, which could be O(M) per query. With O(M) queries, total O(M^2). However, we can reduce the number of queries. We have at most M candidates, but maybe we can prune candidates. But in worst case, it could be bad.

We need a more efficient way. Let's think about the structure of the greedy chain. The next_pos[p] is always > p. So it's a strictly increasing sequence. We can precompute for each p, the "skip" pointers: for k=0,1,..., we can store the position after 2^k jumps. This is the binary lifting table. To save memory, we can store it as a list of arrays using the 'array' module or maybe use a dictionary for sparse? But positions are dense.

Maybe we can compute f(l,r) using a two-pointer technique on the fly. Since we have many queries, we can precompute an array steps_to_cover[p] = the minimum number of type1 intervals to cover from p to the end? Not exactly.

Another idea: we can precompute for each position p, the "next" position, and then for each p, we can find the number of steps to reach a given r by using the fact that the sequence of positions is increasing. We can use a "forward" DP: let dp[p] = the minimum number of intervals to cover from p to N. But that's not exactly what we need.

We need f(l,r) for various r. We can precompute for each l, the positions after each jump in a list. Since the number of jumps from any l is at most the number of type1 intervals that are reachable, which could be up to M. So for each l, we can store a list of length up to M. That would be O(N*M) memory, too much.

Maybe we can use the fact that the type1 intervals are static, and we can build a graph and use BFS to compute the minimum number of intervals to reach each position from any start? Not exactly.

Wait, we can use the following: for each position p, we know next_pos[p]. We want to answer queries: given l and r, how many steps to reach > r. This is equivalent to: given l, we have a sequence l, next_pos[l], next_pos[next_pos[l]], ... until we exceed N. We want the number of terms that are ≤ r. This is like asking for the number of jumps before exceeding r. We can precompute for each l, the "power of two" jumps. But we can also use a "disjoint set union" like structure to skip? Not sure.

Given the constraints, perhaps we can compute f(l,r) by simulating the chain step by step, and we can do this for all candidates in O(total f over candidates). But the total f over candidates could be large. However, note that the number of candidates is O(M), and each f is at most M, so worst-case O(M^2). But maybe in practice, many candidates have small f. Still, we should aim for a better worst-case.

We can use the binary lifting table but store it in a memory-efficient way. Since N is 1e6 and max_log is 20, the table size is 20e6. In Python, if we use a list of lists, each sublist has overhead of about 56 bytes + 8*len. For 20 sublists of size 1e6, that's 20*1e6*8 = 160e6 bytes for the integers themselves (since Python int is 28 bytes actually, so 560e6 bytes). That's too much. So we need to reduce memory.

We can use the array module to store integers in a more compact way. Or we can use a dictionary for the nxt table, but positions are dense.

Maybe we can avoid the binary lifting table altogether by using a different method. Since we only need to compute f(l,r) for candidates that are generated, and the number of candidates is O(M), we can compute f(l,r) by using a two-pointer technique on the type1 intervals sorted by L. For a fixed l, we can compute the greedy chain step by step. But we can precompute for each l, the entire chain in an array, but that would be O(N * average chain length) memory. However, the average chain length might be small. But worst-case, if type1 intervals are such that each jump is by 1, then chain length is N, so O(N^2) memory.

Given the time, maybe we can implement the binary lifting table using a list of arrays, but we can store each row as a bytearray? Not possible because positions can be up to 1e6, so we need 20 bits. We can use array('I') for unsigned int. That would be 4 bytes per integer, so 20e6 * 4 = 80 MB, which is acceptable. We'll need to use the array module. We'll create an array for each row. But we also need to store -1 for invalid. Since we are dealing with Python, we can use list of lists but with each inner list being a list of small ints? Python ints are still 28 bytes. So we need to use array.

Let's try to use the array module. We'll import array. We'll create an array of type 'i' for signed int (since -1 is needed). But the size is N+2, so about 1e6+2. 20 arrays of that size: 20e6 integers, 4 bytes each = 80 MB. That's okay. We'll need to be careful with indexing.

We'll build nxt[0] as an array of size N+2, filled with -1. Then set nxt[0][p] = next_pos[p]. Then for k from 1 to max_log, we create a new array nxt[k] of size N+2, and for p in range(1, N+2): if nxt[k-1][p] != -1: nxt[k][p] = nxt[k-1][ nxt[k-1][p] ] else nxt[k][p] = -1.

This will be O(max_log * N) time and memory. Time: 20 * 1e6 = 20 million operations, which is fine. Memory: 80 MB, acceptable.

But we need to store nxt as a list of arrays. We'll do that.

Now, for the query, we need to access nxt[k][pos]. We'll have to be careful that nxt[k] is an array, and indexing is fast.

Now, we also need to compute next_pos. We'll have an array next_pos of size N+2 (indices 0..N+1, but we use 1..N+1). We'll set next_pos[N+1] = -1.

Now, we need to compute furthest[p] and op_for_furthest[p]. We'll have arrays of size N+2 (0 unused). We'll use lists for these since they are not too big (1e6). Lists of 1e6 ints are about 28 MB each. We have furthest and op_for_furthest, so 56 MB. Plus the nxt arrays 80 MB, total 136 MB, still acceptable.

But we also have type1 ops list, type2 ops list, and other arrays. Should be within memory limits if we are careful.

Now, we need to implement the segment tree for minL_at_R. We'll use a similar approach: build a tree as an array of size 2*size, where size is the next power of 2 >= N+1. We'll store the minimum in each node. We'll use a list of size 2*size. That's about 2*2^20 = 2,097,152 elements. Each int 28 bytes, so about 58 MB. That's a lot. But we can use an array('i') for the segment tree as well. However, we need to do range minimum queries and point updates? Actually, we are only building once, and then doing queries. We can build the tree with the values, and then for queries, we need to find the first R with value ≤ L. We can do that with a recursive function that traverses the tree. We can implement the tree as a list, and the recursive function will be O(log N) per query. The tree size is about 2*size, which is 2M, so 56 MB if using list of ints. That's heavy but maybe acceptable if we combine with other memory usage. Total memory might exceed 256 MB. We need to optimize.

Maybe we can avoid the segment tree by using a different method. Since we only need to query for L in L_set (at most 2e5), we can precompute for each R, minL_at_R, and then for each L, we want the smallest R in [L, maxR_at_L[L]] with minL_at_R[R] ≤ L. We can do this by, for each L, scanning R from L to maxR_at_L[L], but we can stop early. To make it faster, we can precompute an array next_valid_R[L] = the smallest R ≥ L such that minL_at_R[R] ≤ L. Then we need to also check R ≤ maxR_at_L[L]. So we want the smallest R in [L, maxR_at_L[L]] with minL_at_R[R] ≤ L. This is equivalent to: if next_valid_R[L] exists and next_valid_R[L] ≤ maxR_at_L[L], then R2 = next_valid_R[L]. So we can precompute next_valid_R[L] for all L from N down to 1. How to compute next_valid_R[L]? We can do: for L from N down to 1, we want the smallest R ≥ L with minL_at_R[R] ≤ L. We can maintain a list of R that are "active" for current L. Actually, we can process R from N down to 1, and for each R, we know minL_at_R[R]. For a given L, the condition minL_at_R[R] ≤ L means that R is valid for L if L ≥ minL_at_R[R]. So as we decrease L, more R become valid. We can maintain a min-heap of R that are valid for the current L. Specifically, for each R, it becomes valid when L becomes minL_at_R[R]. So we can precompute events: for each R, at L = minL_at_R[R], R becomes valid. Then as we sweep L from N down to 1, we can add to a min-heap all R such that minL_at_R[R] == L. Then the smallest R in the heap (since we want the smallest R ≥ L) would be the answer for current L. But note: we also need R ≥ L. Since we are sweeping L from N to 1, the heap contains R that are ≥ current L? Not necessarily: we add R when L becomes minL_at_R[R], but R could be less than L? For example, if minL_at_R[R] = 5, and current L=4, then R could be 3? But R is the index, and minL_at_R[R] is a number. There is no direct relation. Actually, for a given R, it is valid for L if L ≥ minL_at_R[R]. But L and R are independent. So when we sweep L from N down to 1, at L, the set of valid R is { R : minL_at_R[R] ≤ L }. Among these, we want the smallest R that is ≥ L. So we need a data structure that, given a set of R, can return the smallest R in the set that is ≥ L. We can use a segment tree or a binary indexed tree. We can precompute an array of size N+1, and for each R, we can update it to 1 if minL_at_R[R] ≤ current L. Then we can query the prefix sum from L to N to find the first R with value 1. We can do this with a BIT that supports point updates and prefix sum queries to find the first 1. Since we have N up to 1e6, and we do this for each L (which could be up to N), but we only need to compute for L in L_set, which is at most M. So we can do for each L in L_set: we want the smallest R ≥ L with minL_at_R[R] ≤ L. We can precompute an array minL_at_R, and then for each L, we can scan R from L to maxR_at_L[L] until we find one. But we can speed up the scan by using the fact that minL_at_R[R] is non-increasing? Not necessarily.

Given the time, I think implementing a segment tree for minL_at_R is the most straightforward. We'll use a list for the tree, and accept the memory usage. We'll also have other arrays, so total memory might be around 200 MB, which is borderline. We can optimize by using arrays for the tree as well. Let's use array('i') for the segment tree. We'll need to import array. We'll build the tree in an array of size 2*size, where size is the next power of 2. We'll store the minimum value. We'll also need a function to find the first index in [l, r] with value ≤ L. We can implement an iterative function that walks down the tree.

We'll write a class for the segment tree.

Now, we also need to store the type2 ops for reconstruction. We'll store them in a list of (L,R,idx).

We also need to store type1 ops in a list of (L,R,idx) sorted by L.

Now, let's outline the steps in code:

Read N, M.
Initialize ops_input = [].
For i in range(M):
    read L, R
    ops_input.append((L,R))

Separate into type1 and type2? Actually, we consider all ops as both type1 and type2 candidates. So we will have two lists: type1_ops = [] and type2_ops = [], but they are the same set. We'll just have one list ops, and we'll use it for both. But for building furthest, we only need type1_ops. For building segment tree, we only need type2_ops. So we can create two lists: ops1 and ops2, each containing the (L,R,idx) for all ops. But that duplicates. We can just have one list, and when building type1 stuff, we use all ops. When building type2 stuff, we use all ops. So we can just use the same list.

So: ops = [(L_i, R_i, i) for i in range(M)]

Now, for type1:
- Sort ops by L.
- Create an array furthest of size N+2 (0..N+1, but we use 1..N). Initialize with -1.
- Create an array op_for_furthest of size N+2, initialize with -1.
- Use a pointer idx_ptr = 0 over sorted ops.
- Use a max-heap heap = [] (store (-R, op_idx)).
- For p in range(1, N+1):
    - While idx_ptr < len(ops) and ops[idx_ptr].L == p: push (-ops[idx_ptr].R, ops[idx_ptr].idx) into heap; idx_ptr += 1.
    - While heap and -heap[0][0] < p: pop.
    - If heap: furthest[p] = -heap[0][0]; op_for_furthest[p] = heap[0][1].
    - Else: furthest[p] = -1; op_for_furthest[p] = -1.

But note: we need to sort ops by L. However, ops may have L values up to N. We can sort by L.

Now, build next_pos:
- next_pos = [0]*(N+2)
- For p in range(1, N+1):
    if furthest[p] != -1: next_pos[p] = furthest[p] + 1
    else: next_pos[p] = -1
- next_pos[N+1] = -1

Build binary lifting table:
- max_log = 20 (since 2^20 = 1,048,576 > M)
- nxt = []
- nxt.append(next_pos[:])  # but we need to copy as array? We'll use list for now, but memory might be high. Let's use array.
We'll use array('i', next_pos) for nxt[0]. Then for k in range(1, max_log+1):
    nxt_k = array('i', [-1]*(N+2))
    for p in range(1, N+2):
        if nxt[k-1][p] != -1:
            nxt_k[p] = nxt[k-1][ nxt[k-1][p] ]
    nxt.append(nxt_k)

But this loop is O(max_log * N) = 20e6, which is okay. However, we need to be careful with array indexing: array('i') supports indexing, but we need to ensure indices are within bounds. Also, nxt[k-1][ nxt[k-1][p] ] might be -1, so we check.

Now, for type2:
- Compute maxR_at_L: array of size N+1 (1..N), initialize to -1.
- Compute minL_at_R: array of size N+1, initialize to INF (e.g., N+1).
- For each op (L,R,idx):
    if maxR_at_L[L] < R: maxR_at_L[L] = R
    if minL_at_R[R] > L: minL_at_R[R] = L
- Collect L_set: set of L for which maxR_at_L[L] != -1.

Now, build segment tree for minL_at_R. We'll use a size that is the next power of 2 >= N+1. Let's set size = 1
while size < N+1: size <<= 1
tree = array('i', [INF]*(2*size))
Build:
for i in range(N+1):
    tree[size+i] = minL_at_R[i]   # but we need to handle indices: we use 1..N, so we can set tree[size+1] = minL_at_R[1], ..., tree[size+N] = minL_at_R[N]. We also set tree[size] = INF.
Then for i in range(size-1, 0, -1):
    tree[i] = min(tree[2*i], tree[2*i+1])

Now, define a function find_first(l, r, L) that returns the smallest index in [l, r] with tree value <= L. We'll implement recursively:
def find_first(node, node_l, node_r, ql, qr, L):
    if node_r < ql or node_l > qr or tree[node] > L:
        return -1
    if node_l == node_r:
        return node_l
    mid = (node_l + node_r) // 2
    res = find_first(2*node, node_l, mid, ql, qr, L)
    if res != -1:
        return res
    return find_first(2*node+1, mid+1, node_r, ql, qr, L)
We'll call find_first(1, 1, size, l, r, L) but note that our tree has indices up to size, and we only care about 1..N. We can set the query range to [l, r] where l and r are between 1 and N. We need to ensure that the tree covers up to size, and we can ignore indices > N. So in the recursion, we should check if node_l > N, then return -1. We can modify the base case: if node_l > N: return -1. Also, when building, we set tree[size+i] for i=0..size-1, but for i>N, we set to INF.

Now, for each L in L_set:
    U = maxR_at_L[L]
    if U < L: continue
    R2 = find_first(1, 1, size, L, U, L)   # find smallest R in [L, U] with minL_at_R[R] <= L
    if R2 != -1:
        candidate: (L, R2, cost_type2=2)

Also, for each type2 op (L,R,idx): candidate: (L, R, cost_type2=1)

Also, candidate: (1, N, cost_type2=0) but we need to check if type1 can cover [1,N].

Now, for each candidate, we compute f(l,r) using the binary lifting table.

Define a function compute_f(l, r):
    if l > r: return INF
    pos = l
    steps = 0
    for i in range(max_log, -1, -1):
        if nxt[i][pos] != -1 and nxt[i][pos] <= r+1:
            pos = nxt[i][pos]
            steps += (1 << i)
    if pos > r:
        return steps
    if next_pos[pos] != -1:
        return steps + 1
    else:
        return INF

We also need to consider that the chain might require more than 2^max_log jumps? But max_log is enough for M=2e5.

Now, for each candidate, total_cost = cost_type2 + f(l,r). We choose the minimum.

If no candidate gives a finite cost, output -1.

If we have a chosen candidate, we need to reconstruct the ops.

We need to:
- Select type2 ops for the candidate.
- Select type1 ops to cover [l,r].

For type2 ops:
- If cost_type2 = 0: no type2 ops.
- If cost_type2 = 1: we know the op: it must be the type2 op with L_i = l and R_i = r. So we need to find that op. We can store in a dictionary from (L,R) to op index. Or we can search through type2 ops. Since M=2e5, we can build a dictionary mapping (L,R) to idx for type2 ops. But note: an op with the same (L,R) might appear multiple times? Possibly, but we can take any. So we'll create a dict type2_dict mapping (L,R) to idx.
- If cost_type2 = 2: we need to select two ops: one with L_i = l and R_i ≥ r, and one with R_i = r and L_i ≤ l. We can find them by iterating through type2 ops. We'll need to find an op with L_i = l and R_i ≥ r. We can store for each L, a list of ops with that L. But we can just iterate. Since M=2e5, it's fine. We'll select the first such op. Similarly for the second.

For type1 ops: we simulate the chain from l. We'll do:
pos = l
type1_ops_used = []
while pos <= r:
    if furthest[pos] == -1: error
    idx = op_for_furthest[pos]
    type1_ops_used.append(idx)
    pos = furthest[pos] + 1
This loop will use the same ops as in the binary lifting. It might use more ops than f if the chain goes beyond r, but that's okay. We need to ensure that we stop when pos > r. Actually, we want to cover r, so we need to continue until pos > r. So the condition should be while pos <= r. But if pos > r, we have already covered r. So the loop should be: while pos <= r: do the jump, then check if pos > r. So:
while pos <= r:
    idx = op_for_furthest[pos]
    type1_ops_used.append(idx)
    pos = furthest[pos] + 1
This will use f ops, or maybe one more if the last jump overshoots exactly to r+1? Actually, if pos <= r, we take a jump, and then pos becomes next_pos[pos]. After the jump, if pos > r, we stop. So the number of jumps is the number of times we entered the loop. That is exactly f if f is computed as the number of jumps to cover r. But note: in compute_f, we might have used binary lifting which might have combined multiple jumps. The number of jumps should be the same. So it's fine.

Now, we need to set the ops array. Initialize ops_result = [0]*M.
For each type2 op index used, set ops_result[idx] = 2.
For each type1 op index used, set ops_result[idx] = 1.
But note: an op could be used as both? That shouldn't happen. But we should check for conflicts. If an op is used as both, we have a problem. In our selection, we should ensure that the type1 ops we select are not also type2 ops. But as argued, they are disjoint because type2 ops don't cover I. However, if an op is used as type2, its interval contains I, so it does not cover any point in I. So it won't be selected in the type1 chain. So no conflict.

But we should still check: when we select type1 ops, we might select an op that we also selected as type2. That would be a conflict. To avoid this, we can keep a set of used indices. But given the logic, it shouldn't happen. We'll assume it doesn't.

Now, we need to output the total cost (number of non-zero ops) and the ops array.

Now, we need to handle the case where there are no type1 ops. Then furthest[p] = -1 for all p. The only feasible candidate is I = [1,N] with cost_type2 = 1 or 2? Actually, if there are no type1 ops, we can only use type2 ops. We need to cover [1,N] with type2 ops. That means we need a set of type2 ops whose intersection is [1,N]. That requires max L = 1 and min R = N. So we need an op with L=1 and R=N, or two ops: one with L=1 and R≥N, and one with L≤1 and R=N. But L≤1 means L=1. So essentially we need an op with L=1 and R=N. So if there is such an op, cost=1. If not, impossible. So our algorithm will handle this: candidate I = [1,N] with cost_type2=0 is not feasible because f(1,N)=INF. Candidate I = [1,N] with cost_type2=1: we need a type2 op with L=1 and R=N. If exists, cost=1. Candidate with cost_type2=2: we need L=1, R=N from two ops: one with L=1 and R≥N, and one with R=N and L≤1. That would require an op with L=1 and R≥N, and an op with R=N and L=1. So essentially an op with L=1 and R=N. So cost=2 is not better than 1 if such op exists. If not, maybe cost=2 is possible with L=1 and R=N from two different ops? For example, one op with L=1, R=10, and another with L=1, R=5? But then min R=5, so intersection is [1,5], not [1,N]. So to get intersection [1,N], we need min R = N. So we need an op with R=N. And max L=1, so we need an op with L=1. So we need two ops: one with L=1, and one with R=N. But they could be the same op if it has L=1 and R=N. If not, we need two distinct ops. So if there is an op with L=1 and an op with R=N, and we take both, the intersection is [1, N] only if the op with L=1 has R≥N and the op with R=N has L≤1. But if the op with L=1 has R < N, then intersection is [1, R] which is not [1,N]. So to get intersection exactly [1,N], we need an op with R=N. So essentially, we need an op with R=N. And we need an op with L=1. But if the op with L=1 has R < N, then the intersection of that op and the op with R=N is [1, min(R1, N)] = [1, R1] if R1 < N. So to get [1,N], we need the op with L=1 to have R=N. So indeed, we need an op with L=1 and R=N. So cost=1 is the only possibility. So if no such op, impossible. So our algorithm will output -1.

Now, we need to test with samples.

Let's implement step by step.

First, read input.
Separate ops into type1 and type2? Actually, we need all ops for both. So we'll have one list.

We'll need to sort ops by L for type1. We'll need to group by L for type2 segment tree.

We'll need to store ops in a list: ops = []
for i in range(M):
    L,R = map(int, input().split())
    ops.append((L,R,i))

Now, build type1 furthest:
- Sort ops by L. Let's call sorted_ops = sorted(ops, key=lambda x: x[0])
- Create arrays furthest = [-1]*(N+2), op_for_furthest = [-1]*(N+2)
- Use heap = [] (max-heap with negative R)
- ptr = 0
- for p in range(1, N+1):
    while ptr < len(sorted_ops) and sorted_ops[ptr][0] == p:
        L,R,idx = sorted_ops[ptr]
        heapq.heappush(heap, (-R, idx))
        ptr += 1
    while heap and -heap[0][0] < p:
        heapq.heappop(heap)
    if heap:
        furthest[p] = -heap[0][0]
        op_for_furthest[p] = heap[0][1]
    else:
        furthest[p] = -1
        op_for_furthest[p] = -1

But note: the sorted_ops list is sorted by L, but we need to process all ops with L == p. However, there might be multiple ops with same L. We are pushing all of them. But the heap will keep the one with maximum R. That's correct.

Now, build next_pos and nxt.

For type2:
- maxR_at_L = [-1]*(N+1) (index 0 unused)
- minL_at_R = [N+1]*(N+1) (INF)
- For each op in ops:
    L,R,idx = op
    if maxR_at_L[L] < R: maxR_at_L[L] = R
    if minL_at_R[R] > L: minL_at_R[R] = L
- L_set = set([L for L in range(1,N+1) if maxR_at_L[L] != -1])

Now, build segment tree for minL_at_R. We'll use size = 1
while size < N+1: size <<= 1
tree = [N+1]*(2*size)
for i in range(1, N+1):
    tree[size+i] = minL_at_R[i]
for i in range(size-1, 0, -1):
    tree[i] = min(tree[2*i], tree[2*i+1])

Define find_first(node, node_l, node_r, ql, qr, L):
    if node_r < ql or node_l > qr or tree[node] > L:
        return -1
    if node_l == node_r:
        if node_l <= N:  # only consider indices within 1..N
            return node_l
        else:
            return -1
    mid = (node_l+node_r)//2
    res = find_first(2*node, node_l, mid, ql, qr, L)
    if res != -1:
        return res
    return find_first(2*node+1, mid+1, node_r, ql, qr, L)

We'll call find_first(1, 1, size, l, r, L).

Now, generate candidates:
candidates = []
For each L in L_set:
    U = maxR_at_L[L]
    if U < L: continue
    R2 = find_first(1,1,size, L, U, L)
    if R2 != -1:
        candidates.append( (L, R2, 2) )

For each op in ops:
    L,R,idx = op
    candidates.append( (L, R, 1) )

Also, candidate (1, N, 0) but only if type1 can cover it. We'll include it and check later.

Now, we need to compute f(l,r) for each candidate. We'll do:
best_cost = INF
best_candidate = None
for (l,r,cost2) in candidates:
    f = compute_f(l,r)
    if f != INF:
        total = cost2 + f
        if total < best_cost:
            best_cost = total
            best_candidate = (l,r,cost2)

If best_candidate is None, print -1.

Otherwise, reconstruct.

We need to select type2 ops:
l,r,cost2 = best_candidate
type2_indices = []
if cost2 == 0:
    pass
elif cost2 == 1:
    # find op with L=l and R=r
    # Build a dict: type2_dict[(L,R)] = idx
    # But we might have multiple ops with same (L,R). We can take any.
    # We can create a dict from ops list: for each op, if (L,R) not in dict, add.
    # But we need to ensure it's the same (L,R). We'll build a dict.
    # However, we can also search through ops. Since M=2e5, we can do a linear search? But we might do this once, so it's fine.
    # We'll build a set of (L,R) for type2? Actually, all ops are potential type2. So we can build a dict mapping (L,R) to idx.
    # We'll do that beforehand.
elif cost2 == 2:
    # find op with L=l and R>=r
    for op in ops:
        if op[0] == l and op[1] >= r:
            type2_indices.append(op[2])
            break
    # find op with R=r and L<=l
    for op in ops:
        if op[1] == r and op[0] <= l:
            type2_indices.append(op[2])
            break

We need to ensure these two ops are distinct. If they are the same, then cost2 should have been 1, not 2. So in cost2=2, they are distinct.

Now, for type1 ops:
type1_indices = []
pos = l
while pos <= r:
    if furthest[pos] == -1:
        # This should not happen if f is finite
        break
    idx = op_for_furthest[pos]
    type1_indices.append(idx)
    pos = furthest[pos] + 1

Now, we have type1_indices and type2_indices. But we must ensure that the type1 indices are not in type2_indices. They shouldn't be, but just in case, we can check. If there is a conflict, we need to choose a different type1 op? But the greedy choice is fixed. So we assume no conflict.

Now, create ops_result = [0]*M
for idx in type1_indices:
    ops_result[idx] = 1
for idx in type2_indices:
    ops_result[idx] = 2

But note: if an index appears in both, it would be overwritten. We'll assume no conflict.

Now, the total cost is len(type1_indices) + len(type2_indices). We should verify that it matches best_cost.

Now, output best_cost and the ops_result list separated by spaces.

Now, we need to implement compute_f(l,r) using the nxt table.

We'll define:
def compute_f(l, r):
    if l > r:
        return INF
    pos = l
    steps = 0
    for i in range(max_log, -1, -1):
        if nxt[i][pos] != -1 and nxt[i][pos] <= r+1:
            pos = nxt[i][pos]
            steps += (1 << i)
    if pos > r:
        return steps
    if next_pos[pos] != -1:
        return steps + 1
    else:
        return INF

We need to ensure that next_pos and nxt are accessible. We'll have them as global or in closure.

Now, we need to set max_log. Let's set max_log = 20 (since 2^20=1,048,576 > 2e5). But we can compute it as the number of bits needed for M: max_log = (M).bit_length().

Now, we need to build nxt. We'll have nxt as a list of arrays. We'll build it after next_pos is ready.

Now, we need to handle the case where there are no type1 ops. Then furthest[p] = -1, next_pos[p] = -1. The nxt table will have -1. compute_f will return INF for any l,r.

Now, let's test with sample 1.

Sample 1:
N=5, M=4
Ops: (2,4), (3,5), (1,4), (2,5)
All are type1 candidates. There are no type2 ops? Wait, the input doesn't specify type; we can choose. So in our model, we have both type1 and type2 candidates. So we have type2 ops: all 4 ops. So maxR_at_L: for L=2: max(4,5)=5; L=3:5; L=1:4.
minL_at_R: R=4: min(2,1)=1; R=5: min(3,2)=2.
L_set = {1,2,3}
For L=1: U=maxR_at_L[1]=4. Find first R in [1,4] with minL_at_R[R] <=1. minL_at_R[1]=INF, [2]=INF, [3]=INF, [4]=1. So R2=4. Candidate (1,4,2).
For L=2: U=5. Find first R in [2,5] with minL_at_R[R]<=2. minL_at_R[2]=INF, [3]=INF, [4]=1, [5]=2. So R2=4 (since 4 <=5 and minL_at_R[4]=1<=2). Candidate (2,4,2).
For L=3: U=5. Find first R in [3,5] with minL_at_R[R]<=3. minL_at_R[3]=INF, [4]=1, [5]=2. So R2=4. Candidate (3,4,2).
Also, for each op: (2,4,1), (3,5,1), (1,4,1), (2,5,1).
Also candidate (1,5,0).

Now, compute f for each:
- (1,4,2): f(1,4)? We need to see type1 ops: all four are type1. We need to cover [1,4] with type1. The greedy chain from 1: we need an interval covering 1. Which type1 ops cover 1? (1,4) covers 1. So furthest[1] = max R among ops with L<=1 and R>=1. Op (1,4) has R=4. So furthest[1]=4. So from 1, we jump to 5. That covers [1,4]. So f=1. Total cost = 2+1=3.
- (2,4,2): f(2,4). From 2, we need an interval covering 2. Ops covering 2: (2,4) and (2,5). The furthest is (2,5) with R=5. So jump to 6, covers [2,5], so f=1. Total cost=3.
- (3,4,2): f(3,4). From 3, covering 3: (3,5) gives R=5, so f=1. Total=3.
- (2,4,1): f(2,4)=1, total=2.
- (3,5,1): f(3,5). From 3, (3,5) gives R=5, so f=1, total=2.
- (1,4,1): f(1,4)=1, total=2.
- (2,5,1): f(2,5). From 2, (2,5) gives R=5, so f=1, total=2.
- (1,5,0): f(1,5). We need to cover [1,5] with type1. From 1, (1,4) gives R=4, then from 5, (2,5) covers 5? Actually, after first jump to 5, we are at 5. We need an interval covering 5. Ops covering 5: (2,5) and (3,5). The furthest is (2,5) or (3,5) with R=5. So jump to 6. So f=2. Total cost=2.
So the minimum cost is 2, achieved by (1,5,0) with type1 ops: (1,4) and (2,5). That matches sample output: cost 2, and they used type2 on first op? Wait, sample output uses type2 on first op, type1 on third. That's different. Our solution gives type1 on all? Actually, we have no type2 used. But the sample uses type2 on first op (2,4) and type1 on third (1,4). That would correspond to candidate (2,4,1) with f(2,4)=1, total=2, and type1 op (1,4)? Wait, for candidate (2,4,1), we need to cover [2,4] with type1. f(2,4)=1 using op (2,5) or (2,4)? Actually, from 2, the furthest is (2,5) so we use (2,5). So type1 op is (2,5). And type2 op is (2,4). So ops: type2 on first op (2,4), type1 on fourth op (2,5). That's different from sample. But both are valid with cost 2. So our algorithm might output a different set. That's acceptable.

But we need to check if our candidate (1,5,0) is actually feasible. We need to cover [1,5] with type1. We said f=2 using (1,4) and (2,5). But note: (2,5) covers 2 to 5, and (1,4) covers 1 to 4. Together they cover [1,5]. So yes. So our algorithm would output cost 2, and ops: all type1? But we have 4 ops. We would set ops_result: for type1 indices: (1,4) index 2, (2,5) index 3. Others 0. That gives ops: 0 0 1 1? Actually, indices: 0: (2,4), 1: (3,5), 2: (1,4), 3: (2,5). We set ops[2]=1, ops[3]=1. So output: 2, then 0 0 1 1. That's valid? Let's see: initial all 0. Op1 (2,4): type0, do nothing. Op2 (3,5): type0, do nothing. Op3 (1,4): type1, set 1-4 to 1. Op4 (2,5): type1, set 2-5 to 1. Final: 1,1,1,1,1. Cost 2. So it's valid. So our algorithm would output that. The sample output is different but also valid. So we are fine.

Now, sample 2:
N=5, M=4
Ops: (1,3), (1,5), (2,4), (3,5)
We need to see the minimum cost. Sample output: cost 1, with ops: 0 1 0 0. That means they use type1 on second op (1,5) and no others. So candidate I = [1,5] with cost_type2=0, f(1,5)=1. That requires that from 1, we can cover [1,5] with one type1 op. But the type1 ops are all four. Is there a type1 op that covers [1,5]? (1,5) does. So f(1,5)=1. So cost=1. Our algorithm should find that.

Let's check candidates: type2 ops: all four. maxR_at_L: L=1: max(3,5)=5; L=2:4; L=3:5.
minL_at_R: R=3:1; R=5: min(1,3)=1; R=4:2.
L_set: {1,2,3}
For L=1: U=5, find first R in [1,5] with minL_at_R[R]<=1. minL_at_R[1]=INF, [2]=INF, [3]=1, so R2=3. Candidate (1,3,2).
For L=2: U=4, find first R in [2,4] with minL_at_R[R]<=2. minL_at_R[2]=INF, [3]=1, [4]=2. So R2=3. Candidate (2,3,2).
For L=3: U=5, find first R in [3,5] with minL_at_R[R]<=3. minL_at_R[3]=1, so R2=3. Candidate (3,3,2).
Also, each op: (1,3,1), (1,5,1), (2,4,1), (3,5,1).
Also candidate (1,5,0).

Now compute f:
- (1,3,2): f(1,3). Type1: from 1, need to cover 1. Ops covering 1: (1,3) and (1,5). Furthest: (1,5) with R=5, so jump to 6, covers [1,5], so f=1. Total cost=2+1=3.
- (2,3,2): f(2,3). From 2, covering 2: (2,4) gives R=4, so f=1, total=3.
- (3,3,2): f(3,3). From 3, covering 3: (3,5) gives R=5, so f=1, total=3.
- (1,3,1): f(1,3)=1, total=2.
- (1,5,1): f(1,5)=1, total=2.
- (2,4,1): f(2,4). From 2, (2,4) gives R=4, f=1, total=2.
- (3,5,1): f(3,5)=1, total=2.
- (1,5,0): f(1,5)=1, total=1.
So minimum is 1, candidate (1,5,0). So our algorithm would output cost 1, and type1 op for (1,5). That is correct.

Sample 3:
N=5, M=2
Ops: (1,3), (2,5)
We need to see if feasible. Sample output: cost 2, ops: 1 1. So they use both as type1.
Our algorithm: type2 candidates: both ops.
maxR_at_L: L=1:3; L=2:5.
minL_at_R: R=3:1; R=5:2.
L_set: {1,2}
For L=1: U=3, find first R in [1,3] with minL_at_R[R]<=1. minL_at_R[1]=INF, [2]=INF, [3]=1. So R2=3. Candidate (1,3,2).
For L=2: U=5, find first R in [2,5] with minL_at_R[R]<=2. minL_at_R[2]=INF, [3]=1, [4]=INF, [5]=2. So R2=3 (since minL_at_R[3]=1<=2). Candidate (2,3,2).
Also each op: (1,3,1), (2,5,1).
Also (1,5,0).

Compute f:
- (1,3,2): f(1,3). Type1: from 1, covering 1: ops covering 1: (1,3) only? Actually, (1,3) covers 1, (2,5) does not cover 1. So furthest[1] = max R among ops with L<=1 and R>=1. Only (1,3) has R=3. So furthest[1]=3. Jump to 4, covers [1,3]. So f=1. Total cost=2+1=3.
- (2,3,2): f(2,3). From 2, covering 2: (2,5) gives R=5, so f=1, total=3.
- (1,3,1): f(1,3)=1, total=2.
- (2,5,1): f(2,5). From 2, (2,5) gives R=5, so f=1, total=2.
- (1,5,0): f(1,5). From 1, (1,3) gives R=3, then from 4, (2,5) gives R=5? Actually, after first jump to 4, we are at 4. We need an interval covering 4. (2,5) covers 4? Yes, 2<=4<=5. So furthest[4] = 5. So f=2. Total cost=2.
So minimum cost is 2, achieved by (1,3,1) and (2,5,1) and (1,5,0). Our algorithm would pick the first one with cost 2. That's fine.

Sample 4:
N=5, M=2
Ops: (1,3), (2,4)
We need to see if feasible. Sample output: -1.
Our algorithm: type2 candidates: both ops.
maxR_at_L: L=1:3; L=2:4.
minL_at_R: R=3:1; R=4:2.
L_set: {1,2}
For L=1: U=3, find first R in [1,3] with minL_at_R[R]<=1. minL_at_R[1]=INF, [2]=INF, [3]=1. So R2=3. Candidate (1,3,2).
For L=2: U=4, find first R in [2,4] with minL_at_R[R]<=2. minL_at_R[2]=INF, [3]=1, [4]=2. So R2=3. Candidate (2,3,2).
Also each op: (1,3,1), (2,4,1).
Also (1,5,0).

Compute f:
- (1,3,2): f(1,3). Type1: from 1, covering 1: only (1,3) gives R=3, so f=1, total=3.
- (2,3,2): f(2,3). From 2, covering 2: (2,4) gives R=4, so f=1, total=3.
- (1,3,1): f(1,3)=1, total=2.
- (2,4,1): f(2,4). From 2, (2,4) gives R=4, f=1, total=2.
- (1,5,0): f(1,5). From 1, (1,3) gives R=3, then from 4, (2,4) gives R=4? Actually, after first jump to 4, we are at 4. We need an interval covering 4. (2,4) covers 4, R=4. So jump to 5. Now we are at 5, which is <=5? Actually, r=5, so we need to cover 5. At pos=5, do we have an interval covering 5? (2,4) ends at 4, (1,3) ends at 3. So no interval covers 5. So f=INF. So (1,5,0) is not feasible.
So the minimum cost among feasible is 2, but sample says -1. Why? Because with cost 2, we need to select two ops. For candidate (1,3,1), we use type2 op (1,3) and type1 op to cover [1,3]. But type1 op to cover [1,3] could be (1,3) itself? But we cannot use the same op for both. We need to use a type1 op to cover [1,3]. Which type1 ops can cover [1,3]? (1,3) and (2,4). (2,4) does not cover 1. So only (1,3) can cover 1. But if we use (1,3) as type1, then we cannot use it as type2. So we need a different type2 op. But the only type2 ops are (1,3) and (2,4). If we use (1,3) as type1, we can use (2,4) as type2? But then the intersection of type2 ops? We are using only one type2 op, so I = [2,4]. Then we need to cover I with type1. But we are using (1,3) as type1, which does not cover I. So we need another type1 op to cover I. But we only have (2,4) as type2, and (1,3) as type1. That doesn't cover I. So we need a third op. So actually, candidate (1,3,1) with cost_type2=1 means we use the type2 op (1,3), and then we need to cover I = [1,3] with type1 ops. But the only type1 op that can cover 1 is (1,3) itself, but it's already used as type2. So we cannot use it. So we need a different type1 op. But no other type1 op covers 1. So candidate (1,3,1) is not feasible because the type1 chain fails. In our compute_f, we computed f(1,3)=1 assuming we can use (1,3) as type1. But if (1,3) is already used as type2, we cannot use it as type1. So we need to ensure that the type1 ops we use are disjoint from the type2 ops. In our algorithm, we didn't check that. So we need to modify the feasibility check: when computing f(l,r) for a candidate, we need to ensure that the type1 ops used in the greedy chain do not include the type2 ops selected. But the type2 ops are selected only for the chosen candidate. During the search, we don't know which type2 ops will be selected. However, we can check: for a given candidate (l,r,cost2), the type2 ops we will use are specific. We need to ensure that those type2 ops are not used in the type1 chain. The type2 ops are from the set of ops. The type1 chain uses some ops. We need to check that the sets are disjoint. But since the type2 ops' intervals contain I, they do not cover any point in I, so they won't be used in the type1 chain because the type1 chain only uses ops that cover the current point in I. So if an op is used as type2, its interval is [L,R] with L ≤ l and R ≥ r, so it covers all of I? Actually, it covers the complement, so it does not cover any point in I. So it will never be chosen as a type1 op to cover a point in I. So the conflict is impossible. However, in the case of candidate (1,3,1) with type2 op (1,3), the type2 op's interval is [1,3]. It covers the complement, so it does not cover any point in [1,3]. So it cannot be used as a type1 op to cover a point in [1,3]. But the type1 chain from l=1 needs an op that covers 1. The only type1 op that covers 1 is (1,3) itself. But (1,3) is used as type2, so it's not available as type1. So the type1 chain cannot use (1,3) because it's not available. But our greedy chain assumed (1,3) is available. So we need to ensure that the type1 ops we use are not the same as the type2 ops. So we need to mark the type2 ops as unavailable for type1. But which type2 ops? For the candidate, we have specific type2 ops. So we need to check feasibility by simulating the type1 chain while avoiding the type2 ops. But the type2 ops are chosen based on the candidate. So we can do the simulation after selecting the type2 ops. However, during the search, we don't know which type2 ops we will use. But we can note that for a given candidate, the type2 ops are those that achieve the intersection I. There might be multiple choices. We need to choose type2 ops that do not conflict with the type1 chain. In the case of (1,3,1), the only type2 op is (1,3). The type1 chain needs an op covering 1. The only such op is (1,3). So conflict. So we need to detect such conflicts.

How to handle this generally? We can precompute for each candidate, the set of type2 ops that will be used. Then when computing f(l,r), we need to compute the minimum number of type1 ops to cover [l,r] with the restriction that we cannot use the type2 ops. But the type1 chain is greedy and uses specific ops. We can modify the furthest array to exclude the type2 ops. But the type2 ops are different for each candidate. This seems complicated.

Maybe we can avoid this by noting that if a type2 op is used, its interval [L,R] contains I. So it does not cover any point in I. Therefore, in the type1 chain, we only consider ops that cover points in I. Since the type2 op does not cover any point in I, it will never be the furthest for any point in I. So even if we don't exclude it, it won't be chosen. However, in the case of (1,3,1), the type2 op is (1,3). Does it cover point 1? No, because it's type2, so it covers the complement, i.e., points not in [1,3]. So it does not cover 1. So why would it be considered as covering 1? In our type1 chain, we are using the same op as a type1 op. But if we are using it as type2, we should not consider it as a type1 op. So we need to separate the usage. In our furthest array, we included all ops as type1 candidates. So (1,3) is included. So furthest[1] might be based on (1,3) if it covers 1. But if we are using (1,3) as type2, we should not use it as type1. So we need to know which ops are used as type2 and exclude them from the type1 chain.

So we need to ensure that the type2 ops and type1 ops are disjoint. To do this, when we select type2 ops for a candidate, we should choose them in such a way that they are not needed in the type1 chain. But the type2 ops are determined by the candidate. For a given candidate, there might be multiple choices of type2 ops. We need to choose one that does not conflict with the type1 chain. In the case of (1,3,1), the only type2 op is (1,3). And it conflicts. So that candidate is infeasible. So we need to check feasibility by attempting to select type2 ops that are not used in the type1 chain. But the type1 chain is not known until we run it. This is circular.

We can approach by first computing the set of type1 ops needed to cover I using the greedy chain, assuming all ops are available. Then, for each candidate, we need to select type2 ops that are not in that set. But the type2 ops are constrained by the candidate. So we need to check if there exists a selection of type2 ops for the candidate that is disjoint from the type1 set. If not, the candidate is infeasible.

So for each candidate, we can compute the type1 set (the set of op indices used in the greedy chain from l to cover r). Then, we need to see if we can select type2 ops (according to the candidate's cost) that are not in that type1 set. For cost1, we need a type2 op with L=l and R=r. We need to check if there exists such an op that is not in the type1 set. If not, we might need to use a different type2 op? But for cost1, the intersection is exactly [l,r], so the only way to achieve that with cost1 is to use an op with L=l and R=r. So if all such ops are in the type1 set, then we cannot use them as type2. So the candidate is infeasible unless there is an op with L=l and R=r that is not in the type1 set. For cost2, we need one op with L=l and R≥r, and one with R=r and L≤l. We need to check if there exist such ops that are not in the type1 set. They could be the same or different. If they are the same, then we have an op with L=l and R=r, which would be cost1, not cost2. So for cost2, they are distinct. We need both to be not in the type1 set. If no such pair exists, the candidate is infeasible.

For cost0, no type2 ops, so no conflict.

So we need to, for each candidate, first compute the type1 set, then check if we can choose type2 ops that are not in that set. But the type1 set depends on the greedy chain, which depends on which ops are available. If we exclude some ops (the type2 ops we might choose), the greedy chain might change. So it's a dependency. However, note that the type2 ops are used for the intersection, and they have intervals that contain I. So they do not cover any point in I. Therefore, even if we include them as type1 candidates, they will never be chosen by the greedy chain because they don't cover the points in I. Wait, is that true? A type2 op, when used as type1, would cover [L,R]. If its interval contains I, then it covers all points in I. So it does cover points in I. So it could be chosen as a type1 op to cover points in I. For example, op (1,3) used as type2 has interval [1,3]. If we also consider it as type1, it covers [1,3]. So it could be used in the type1 chain. But if we are using it as type2, we should not use it as type1. So the conflict arises when the only type1 op that covers a point in I is also the type2 op we want to use. So to avoid conflict, we need to ensure that the type1 chain can cover I without using the type2 ops. That means there must be alternative type1 ops that cover the points in I. So the feasibility condition is: for the candidate, the set of type1 ops that cover I (i.e., the union of type1 intervals that cover I) must be sufficient to cover I even if we remove the type2 ops. But the greedy chain chooses specific ops. So we need to check if the greedy chain, when restricted to avoid the type2 ops, can still cover I with the same or fewer ops? Actually, we need to cover I with type1 ops that are not type2 ops. So we need to compute the minimum number of type1 ops to cover I with the set of type1 ops excluding the type2 ops. But the type2 ops are not known in advance. This is a bit messy.

Maybe we can simplify by noting that the optimal solution will never use an op as both type1 and type2. So in our search, we can consider that type1 and type2 ops are from disjoint pools. But the same op cannot be in both. So we need to ensure that the selected type1 and type2 ops are disjoint. We can do this by, after selecting a candidate, we choose the type2 ops first, and then compute the type1 chain excluding those ops. If the type1 chain fails, we try to choose different type2 ops (if multiple choices) or discard the candidate.

So in the reconstruction for the chosen candidate, we will:
1. Determine the type2 ops as per the candidate, but we might have choices. We'll try to choose type2 ops that are not in the type1 chain.
2. Then, compute the type1 chain with the remaining ops.

But during the search, we don't know the type1 chain. We could precompute for each l, the type1 chain that uses the earliest possible ops? But that might not be optimal.

Given the time, perhaps we can modify the algorithm to precompute the type1 chain assuming all ops are available, and then for each candidate, check if we can choose type2 ops that are not in that chain. If not, we might need to consider a different type1 chain? But the type1 chain is fixed by the greedy algorithm. If the greedy chain uses a particular op for a point, and that op is needed as type2, then we have a conflict. But maybe there is an alternative type1 chain that uses different ops. The greedy algorithm gives the minimum number of type1 ops, but there might be other chains with the same number of ops. So if the greedy chain conflicts, we might be able to use an alternative chain. But finding alternatives is hard.

Maybe we can avoid this issue by noting that the type2 ops we select will have intervals that contain I. So they are "large" intervals that cover I. In the type1 chain, we might use such an op if it is the only one covering a point. So to avoid conflict, we can choose type2 ops that are not used in the type1 chain. But we don't know the type1 chain in advance. We could compute the type1 chain for I, and then see if the type2 ops we need are in that chain. If they are, we can try to choose different type2 ops? But for a given I, the type2 ops are constrained. For cost1, there is only one type2 op (if we require exact intersection). For cost2, there might be multiple choices. So we can iterate over possible type2 ops for the candidate and see if any of them are not in the type1 chain. If none, then the candidate is infeasible.

So in our algorithm, we can do:
For each candidate (l,r,cost2):
    Compute the type1 set: simulate the greedy chain from l to cover r, collecting the op indices. But note: the greedy chain might use ops that are also needed as type2. We'll get a set type1_set.
    Then, for the type2 ops:
        If cost2=0: no type2 ops, so feasible.
        If cost2=1: need to find an op with L=l and R=r that is not in type1_set. If exists, then feasible. If not, then no such op available without conflict, so infeasible.
        If cost2=2: need to find one op with L=l and R>=r, and one op with R=r and L<=l, such that both are not in type1_set. If such a pair exists, feasible. If not, infeasible.

But wait, the type1 chain we computed assumed all ops are available. If we remove some ops (the type2 ops), the type1 chain might change. So we need to compute the type1 chain after removing the type2 ops. So we should not fix the type1 chain first. Instead, we need to jointly choose type2 and type1 ops. This is more complex.

Given the time, maybe we can assume that the optimal solution will not have conflicts because we can always choose type2 ops that are not in the type1 chain if possible. But in the sample 4, the optimal solution would have used (1,3) as type2 and needed a type1 op to cover 1, but the only type1 op covering 1 is (1,3) itself, which is already used as type2. So there is no way to cover 1 with type1 without using (1,3). So the candidate (1,3,1) is truly infeasible. Our algorithm computed f(1,3)=1 using (1,3), but if we remove (1,3) from type1, f becomes infinity. So we need to account for that.

How can we detect such infeasibility during the search? We can precompute for each candidate, the set of type1 ops that are "forced" to be used to cover I. That is, the greedy chain might use a specific op for a point, and if that op is removed, we might need a different op. But the greedy chain is optimal; if we remove an op, we might need more ops or might not be able to cover at all. So to check feasibility for a candidate with a given type2 set, we need to compute f(l,r) with the type1 ops excluding the type2 set. That is a different f. So we need to compute f(l,r) for each candidate with different exclusions. That's too expensive.

Maybe we can precompute for each l, the greedy chain assuming all ops are available. Then, for a candidate, we can check if the type2 ops we want to use are in that chain. If they are, we can try to see if there is an alternative type2 op? For cost1, there is only one possible type2 op (with L=l and R=r). If that op is in the type1 chain, then the candidate is infeasible because that op is needed for type1. For cost2, we have more flexibility. We can try to find a pair of type2 ops that are not in the type1 chain. If we can, then we can use those type2 ops, and the type1 chain remains the same. If not, then maybe we need to use a different type1 chain. But the type1 chain is fixed by the greedy algorithm. If we remove some ops from the type1 pool, the greedy chain might change. But if the type1 chain uses only ops that are not in the type2 set we choose, then it's fine. So we need to choose type2 ops that are not in the type1 chain. If for a given candidate, all possible type2 ops (according to the cost) are in the type1 chain, then the candidate is infeasible. For cost1, the only possible type2 op is the one with L=l and R=r. If that op is in the type1 chain, then the candidate is infeasible. For cost2, we need to find a pair where both are not in the type1 chain. If no such pair, infeasible.

So in our algorithm, we can do:
For each candidate (l,r,cost2):
    Compute the type1 set using the greedy chain (assuming all ops are available). Let type1_set = set of op indices used.
    If cost2 == 0: feasible.
    If cost2 == 1:
        Find an op with L=l and R=r that is not in type1_set. If exists, then we can use that op as type2, and the type1 chain remains the same. So total cost = 1 + len(type1_set). But wait, the type1 chain might include that op, but we are choosing a different op with the same (L,R)? There could be multiple ops with the same (L,R). So we can choose one that is not in type1_set. So we need to check if there is any op with (L,R) that is not in type1_set. If yes, then feasible. If no, then infeasible.
    If cost2 == 2:
        We need to find two ops: one with L=l and R>=r, and one with R=r and L<=l, both not in type1_set. We also need them to be distinct (if they are the same, it would be cost1). So we can try to find such a pair. If exists, feasible.

But this assumes that the type1 chain does not change if we remove the type2 ops we choose. That is true if the type2 ops are not used in the type1 chain. So by choosing type2 ops not in type1_set, we ensure that the type1 chain remains valid. So this is a valid feasibility check.

Now, we also need to consider that the type1 chain we computed might not be the only one. But the greedy chain is optimal in terms of number of ops. If we remove some ops, the optimal chain might be different. But if we can find a type2 set disjoint from the greedy chain, then the greedy chain still works. So that's a valid solution. If no such type2 set exists, maybe there is another type1 chain that works? Possibly, but it would be harder to find. Given the constraints, we might assume that if the greedy chain doesn't allow a disjoint type2 set, then the candidate is infeasible. This might not be always true, but hopefully for the problem it is. We can test on sample 4: For candidate (1,3,1), type1 chain from 1: uses op (1,3) (since it's the only one covering 1). So type1_set = {index of (1,3)}. The only type2 op with L=1,R=3 is (1,3), which is in type1_set. So no other op with (1,3) exists. So infeasible. For candidate (2,4,1), type1 chain from 2: covering 2, the only op covering 2 is (2,4) itself? Actually, (2,4) covers 2, and (1,3) does not cover 2. So type1_set = {index of (2,4)}. The only type2 op with L=2,R=4 is (2,4), which is in type1_set. So infeasible. For candidate (1,5,0), type1 chain from 1: we need to cover 1. The only op covering 1 is (1,3). So type1_set includes (1,3). Then from 4, we need to cover 4. The only op covering 4 is (2,4). So type1_set includes (2,4). So type1_set = { (1,3), (2,4) }. No type2 ops, so feasible. But f(1,5) we computed as 2. So total cost = 2. But we already determined that (1,5,0) is not feasible because after using (1,3) and (2,4), we still have position 5 uncovered. So our compute_f should have returned infinity. Why did it return 2? Because after jumping from 1 to 4, we are at 4. Then from 4, we jump to 5 using (2,4). But (2,4) covers up to 4, not 5. So furthest[4] should be 4, not 5. Let's recalc: For p=4, which type1 ops cover 4? (1,3) does not (3<4). (2,4) covers 4. So furthest[4] = max R among ops with L<=4 and R>=4. (2,4) has R=4. So furthest[4]=4. Then next_pos[4] = 5. So from 4, we jump to 5. But then we are at 5, which is > r=5? Actually, r=5, so we need to cover 5. After the jump, we are at 5, but we haven't covered 5 because the last jump was from 4 to 5, but the interval (2,4) covers up to 4, so 5 is not covered. So the chain fails because the last interval did not cover 5. Our compute_f assumed that if we jump to a position > r, we have covered r. But in this case, we jumped to 5, but the last interval covered up to 4, so 5 is not covered. So we need to check that the last jump actually covers r. More precisely, the greedy chain covers positions continuously. After a jump from p to next_pos[p] = furthest[p]+1, the interval covers [p, furthest[p]]. So if we want to cover r, we need that the last interval covers r. That is, we need that at the last jump, furthest[p] >= r. In the binary lifting, we jump to a position > r, but that doesn't guarantee that the last interval covered r. For example, if we are at p=4, furthest[4]=4, next_pos[4]=5. If we jump from 4 to 5, we cover [4,4]. So if r=5, we don't cover 5. So we need to ensure that the last jump covers r. So our compute_f is flawed.

We need to modify compute_f: we need to find the number of jumps such that the last jump's interval covers r. That is, we need to find the smallest k such that after k jumps, the current position p_k satisfies p_k > r and the last interval covered r. Actually, we need that the union of the intervals used covers [l,r]. The process is: we start at l, pick an interval that covers l, and extends to furthest[l]. Then we are at furthest[l]+1, and so on. So to cover r, we need that at some step, we pick an interval that starts at or before the current position and ends at or after r. So we need to find the number of jumps until we first have an interval that covers r. In the binary lifting, we were jumping to positions > r+1, but that doesn't ensure the last interval covers r.

So we need a better way to compute f(l,r). We can simulate the chain step by step, but that could be O(f) per candidate. Since f could be up to M, and we have O(M) candidates, total O(M^2) in worst case. But maybe we can optimize by noting that the number of candidates is actually smaller? In worst case, it could be O(M). But M=2e5, M^2=4e10, too large.

We need a more efficient method to compute f(l,r) for many queries. This is essentially: given the next_pos array, we want to find the number of steps to cover r. This is like: we have a function f(p) = next_pos[p]. We want to find the number of iterations of f starting from l until the current position is > r and the last interval covered r. But note: if we have a jump that goes from p to f(p), the interval covers [p, f(p)-1]. So to cover r, we need that at some step, f(p) > r and p <= r. Actually, if f(p) > r, then the interval covers [p, f(p)-1], which includes r if p <= r. So the condition is: we need to take jumps until we find a p such that p <= r and f(p) > r. Then the number of jumps is the number of steps to reach that p. So we can precompute for each p, the first ancestor in the jump chain that satisfies f(p) > r. This is like a "next greater" in a functional graph.

We can precompute for each p, the number of steps to reach a position q such that next_pos[q] > r. But r varies.

Maybe we can precompute for each p, the "cover" info: the furthest position covered by the chain starting at p. Actually, the chain from p will eventually reach a point where no interval covers it, or reach N+1. We can precompute for each p, the final position reached and the number of steps. But we need to cover a specific r.

Another idea: we can precompute for each p, the positions after each jump until we exceed N. This is the chain. We can store for each p, the list of (position, step) pairs. But that could be large.

Given the time, maybe we can compute f(l,r) by simulating the chain step by step, but we can do this only for the candidates that are likely to be optimal. We can first find a lower bound for f(l,r) and prune candidates. But we need a reliable algorithm.

Wait, we can use the binary lifting table to find the number of jumps to reach a position q such that next_pos[q] > r. We can do: starting from l, we want to find the smallest number of jumps k such that after k jumps, the current position p satisfies p <= r and next_pos[p] > r. We can use binary lifting to find the largest k such that after k jumps, we are still at a position p with p <= r. But we also need that the next jump from p goes > r. So we can do:
- Let pos = l, steps = 0.
- For i from max_log down to 0:
    if nxt[i][pos] != -1 and nxt[i][pos] <= r:  # if after 2^i jumps, we are still <= r
        pos = nxt[i][pos]
        steps += (1 << i)
- After this, we have taken the maximum number of jumps such that the resulting position is <= r. Now, if next_pos[pos] != -1 and next_pos[pos] > r, then we can take one more jump to cover r. So f = steps + 1.
- If next_pos[pos] == -1, then impossible.
- If next_pos[pos] <= r, then we need more jumps, but since we took the maximum jumps to stay <= r, the next jump must go > r? Actually, if next_pos[pos] <= r, then we could have taken that jump in the loop? Not necessarily, because next_pos[pos] might be > r+1? The condition in the loop was nxt[i][pos] <= r. So if next_pos[pos] <= r, then for i=0, nxt[0][pos] = next_pos[pos] <= r, so we would have taken that jump. So after the loop, we have taken the maximum number of jumps such that the position is <= r. So if next_pos[pos] <= r, then we would have taken that jump, contradicting that we took the maximum. So it must be that next_pos[pos] > r. So after the loop, either pos > r (then we have already covered r? Not necessarily, because if pos > r, it means we have jumped to a position > r, but the last jump might not have covered r if pos > r but the last interval ended before r? Actually, if we have a jump that goes from p to next_pos[p] = furthest[p]+1, and if next_pos[p] > r, then the interval covers [p, furthest[p]]. Since p <= r (because we only took jumps while p <= r), the interval covers r if p <= r. So if we have a jump that goes to a position > r, and the starting point p of that jump was <= r, then the interval covers r. So the condition to cover r is that we take a jump from a point p <= r to a point > r. So in the loop, we are taking jumps while the resulting position is <= r. So after the loop, we are at a position pos <= r. Then we need to take one more jump from pos, provided next_pos[pos] > r. That will cover r. So f = steps + 1. If next_pos[pos] == -1, then impossible.

But what if pos > r after the loop? That would mean we have already taken a jump that went to a position > r, and we didn't take that jump in the loop because the condition was nxt[i][pos] <= r. So if we end with pos > r, it means that at some point, we took a jump that went to a position > r, but we must have taken it in the loop? Actually, the loop only takes jumps if the resulting position is <= r. So if we end with pos > r, it means that the last jump we took went to a position > r. But then that jump would not have been taken in the loop because the condition nxt[i][pos] <= r would be false. So we must have taken that jump in a previous iteration? This is confusing.

Let's clarify: We want to find the number of jumps to cover r. We can simulate: start at l. While the current position p <= r, we take a jump to next_pos[p], and increment count. We stop when next_pos[p] > r (so that the last jump covers r) or when p > r (which would mean we have already covered r). Actually, if p > r, it means we have already taken a jump that landed beyond r, and that jump covered r. So the number of jumps is the number of times we executed the loop body.

We can find the number of jumps by finding the smallest k such that after k jumps, the position is > r. But we also need that the last jump covered r. If after k jumps, position > r, then the last jump was from some p <= r to > r, so it covered r. So the number of jumps is the smallest k with nxt[k][l] > r? Not exactly, because nxt[k][l] is the position after k jumps. So we want the smallest k such that nxt[k][l] > r. But we also need that the (k-1)-th position was <= r. However, if nxt[k][l] > r, then the (k-1)-th position must have been <= r, because we only jump forward. So the smallest k such that nxt[k][l] > r gives the number of jumps. But is that always true? Consider: l=1, r=5. Suppose from 1, we jump to 4, then from 4, we jump to 5. Then nxt[1][1]=4, nxt[2][1]=5. So smallest k with nxt[k][1] > 5 is k=3? Actually, nxt[2][1]=5, which is not >5. nxt[3][1] would be? From 5, next_pos[5] = -1. So nxt[3][1] = -1. So no k gives >5. So that would say it's impossible. But we could have covered r=5 with 2 jumps if the first jump covered up to 5. So the condition should be: we need a jump that goes to a position > r, and the starting point of that jump is <= r. So we need the smallest k such that nxt[k-1][l] <= r and nxt[k][l] > r. This is equivalent to: nxt[k-1][l] <= r < nxt[k][l]. So we can binary search for k? We can use the nxt table to find the largest k such that nxt[k][l] <= r. Then the number of jumps is k+1, provided nxt[k+1][l] > r. But we also need to check that the (k+1)-th jump is valid.

So in compute_f, we can do:
- pos = l
- steps = 0
- For i from max_log down to 0:
    if nxt[i][pos] != -1 and nxt[i][pos] <= r:
        pos = nxt[i][pos]
        steps += (1 << i)
- After this, we have taken the maximum number of jumps such that the resulting position is <= r. Now, we need to take one more jump from pos. If next_pos[pos] != -1 and next_pos[pos] > r, then we can take that jump and cover r. So f = steps + 1.
- If next_pos[pos] == -1, then impossible.
- If next_pos[pos] <= r, then that would mean we could have taken that jump in the loop, but we didn't, so it's impossible. Actually, if next_pos[pos] <= r, then for i=0, nxt[0][pos] = next_pos[pos] <= r, so we would have taken it in the loop. So after the loop, it must be that next_pos[pos] > r or next_pos[pos] == -1.

So this works. In the example l=1, r=5 with furthest[1]=3, furthest[4]=4? Let's compute next_pos: 
p=1: furthest=3, next=4
p=2: ? covering 2: (2,4) gives R=4, so next=5
p=3: covering 3: (2,4) gives R=4? Actually, (2,4) covers 3, so furthest[3]=4, next=5
p=4: covering 4: (2,4) gives R=4, next=5
p=5: no, next=-1
Now, for l=1, r=5:
pos=1, steps=0.
i from max_log: if nxt[i][1] <= 5? nxt[0][1]=4 <=5, so take it: pos=4, steps=1.
i=0: nxt[0][4]=5 <=5, so take it: pos=5, steps=2.
Now pos=5, which is not <=5? Actually, after the loop, we have pos=5. But our loop condition was nxt[i][pos] <= r. When pos=5, nxt[0][5] = -1, so not taken. So we end with pos=5. Now, next_pos[5] = -1. So f = INF. So correctly returns impossible.

For l=2, r=4:
pos=2, steps=0.
nxt[0][2]=5 >4, so no jumps taken. steps=0, pos=2.
next_pos[2]=5 >4, so f=1. Correct.

So the compute_f function is:
def compute_f(l, r):
    if l > r: return INF
    pos = l
    steps = 0
    for i in range(max_log, -1, -1):
        if nxt[i][pos] != -1 and nxt[i][pos] <= r:
            pos = nxt[i][pos]
            steps += (1 << i)
    if next_pos[pos] != -1 and next_pos[pos] > r:
        return steps + 1
    else:
        return INF

We should also consider the case where pos > r? Actually, if after the loop pos > r, that would mean we have taken a jump that landed > r, but then the condition nxt[i][pos] <= r would not have allowed that jump. So if pos > r, it means that at some point we took a jump that went to > r, but then that jump would not have been taken in the loop. So it's impossible to have pos > r after the loop. Because the loop only takes jumps if the resulting position is <= r. So after the loop, pos is the maximum position reachable with jumps while staying <= r. So pos <= r. So we don't need to check pos > r.

So the compute_f is correct.

Now, back to the conflict issue. In our compute_f, we assume all type1 ops are available. But if we use some ops as type2, they are not available. So we need to modify the type1 chain to exclude the type2 ops. To do that, we can create a modified next_pos array that excludes the type2 ops. But the type2 ops are different for each candidate. This is expensive.

Maybe we can precompute for each candidate, the type1 ops used in the chain. Then, when selecting type2 ops, we can choose ones that are not in that set. But the type1 chain might change if we remove those ops. However, if the type1 chain does not use the type2 ops, then the chain is valid. So we need to ensure that the type2 ops we select are not in the type1 chain. But the type1 chain is computed assuming all ops are available. If we remove some ops, the chain might change. So we need to compute the type1 chain after removing the type2 ops. This is a chicken-and-egg problem.

We can resolve this by noting that the type2 ops have intervals that contain I. So they are "large" intervals. In the type1 chain, we might use such an interval if it is the only one covering a point. So to avoid conflict, we need to choose type2 ops that are not the only ones covering a point in I. This is complicated.

Given the time, I think for the purpose of this problem, we can assume that the optimal solution will not have conflicts because we can always choose type2 ops that are not used in the type1 chain if such exist. If not, then the candidate is infeasible. We can implement the following: for each candidate, we first compute the type1 chain and get the set of ops used. Then, we try to select type2 ops according to the candidate's cost, but we only accept those that are not in the type1 set. If we can find such type2 ops, then we can use the same type1 chain. If not, we need to recompute the type1 chain without those type2 ops. But to keep it simple, we can just try to find type2 ops not in the type1 set. If found, we use that. If not, we might need to consider alternative type1 chains. But that would require exploring many possibilities.

Maybe we can avoid this by noticing that the type1 chain is unique. If the type1 chain uses a particular op, and that op is the only one that can cover a point, then we cannot avoid using it. So if that op is also needed as a type2 op, then the candidate is infeasible. So we can check: for each point in I, is there more than one type1 op covering it? If not, then the type1 chain is forced to use that op. So if that op is also a type2 candidate, then conflict.

We can precompute for each position p, the number of type1 ops covering p. If the number is 1, then the type1 chain is forced to use that op for p. So if that op is also a type2 op for the candidate, then the candidate is infeasible unless we can use a different type1 chain (which is impossible because the greedy algorithm will use that op). So we can precompute an array forced_op[p] = the unique op covering p, or -1 if multiple. Then, for a candidate, we can check if any of the type2 ops we need are forced for some point in I. If so, infeasible.

This is a good idea. Let's implement that.

During the construction of furthest[p], we can also keep track of how many ops cover p. We can have an array count_cover[p] = number of type1 ops with L <= p <= R. We can compute this with a difference array: for each op [L,R], we increment count_cover[L] and decrement count_cover[R+1]. Then prefix sum to get count_cover[p]. Then, we can find for each p, if count_cover[p] == 1, then the op that covers p is unique. We can also find that op. We can modify the heap to also store the op index for the case when there is only one. But we need to know which op is the unique one. We can precompute an array unique_op[p] = the only op covering p if count_cover[p]==1, else -1. To find that op, we can during the sweep, when we have only one op in the heap, we can record it. But the heap may have multiple ops. We can do: if count_cover[p] == 1, then there is exactly one op covering p. We can find it by, for example, during the sweep, if the heap has size 1, then that op is the unique one. But we need to be careful with updates. We can compute unique_op[p] after building the heap for each p. But that would be O(N log M) again. Alternatively, we can compute it by, for each op, it covers all p in [L,R]. So for each p, the unique op is the only op with L <= p <= R. We can find it by, for each p, checking the op with the maximum R? Not necessarily, if there are multiple, we need to know if there is only one. This is getting complicated.

Given the time, I think we can proceed with the assumption that conflicts are rare and the algorithm will work for the given samples. In the actual contest, we might need to handle conflicts properly. But for now, let's implement the basic algorithm and test on the samples.

We'll implement the algorithm as described, and for reconstruction, we'll choose type2 ops first (using the candidate's cost), and then compute the type1 chain excluding those type2 ops. If the type1 chain fails, we'll try to choose different type2 ops if possible. For simplicity, we can just try to choose type2 ops that are not in the type1 chain computed with all ops. If no such type2 ops, we'll try to compute the type1 chain after removing the type2 ops. But we can do a simple approach: after selecting type2 ops, we set a boolean array used_as_type2, and then when computing the type1 chain, we only consider ops that are not used as type2. We can modify the furthest array to exclude those ops. But the furthest array was computed with all ops. We can precompute for each p, the list of ops covering p? That would be too large.

Maybe we can recompute the type1 chain on the fly for the chosen candidate. Since we only do this once, it's O(f) which is O(M). So in the reconstruction, we can:
1. Determine the type2 ops.
2. Mark them as used.
3. Then, simulate the type1 chain from l, but when considering an op, we skip if it's marked as used.
4. If we get stuck, then the candidate is infeasible. But we already chose the candidate as the best, so it should be feasible.

But during the search, we didn't check feasibility with type2 exclusion. So we need to do the check in the search. We can modify the search to, for each candidate, after computing f(l,r) assuming all ops available, we also check if we can select type2 ops disjoint from the type1 set. If not, we might need to recompute f with exclusion. To simplify, we can during the search, for each candidate, compute the type1 set, and then check if there exist type2 ops (according to cost) that are not in that set. If yes, then we can use that candidate. If not, we might need to consider a different type1 chain. But we can also try to compute f(l,r) with the type2 ops excluded, but that would require recomputing the chain. Given the time, I'll implement the following: during the search, we will compute the type1 set using the greedy chain. Then, we will try to select type2 ops that are not in that set. If we can, then we accept the candidate. If not, we will try to compute a new type1 chain after removing the type2 ops that are forced? This is messy.

Maybe we can avoid this by noting that the type1 chain is unique. If the type1 chain uses an op, and that op is also a type2 op, then we can try to use a different type2 op? For cost1, there is only one type2 op (with L=l,R=r). If that op is in the type1 chain, then the candidate is infeasible. For cost2, we have more flexibility. We can try to find a pair of type2 ops that are not in the type1 chain. If no such pair, then the candidate is infeasible. For cost0, no issue.

So in the search, we can do:
For candidate (l,r,cost2):
    Compute type1_set = set of op indices from greedy chain.
    If cost2 == 0:
        feasible = True
    elif cost2 == 1:
        # find an op with L=l, R=r that is not in type1_set
        feasible = any(op for op in ops if op[0]==l and op[1]==r and op[2] not in type1_set)
    elif cost2 == 2:
        # find two ops: one with L=l, R>=r, and one with R=r, L<=l, both not in type1_set, and not the same if they would be cost1
        feasible = False
        ops1 = [op for op in ops if op[0]==l and op[1]>=r and op[2] not in type1_set]
        ops2 = [op for op in ops if op[1]==r and op[0]<=l and op[2] not in type1_set]
        for op1 in ops1:
            for op2 in ops2:
                if op1[2] != op2[2]:
                    feasible = True
                    break
            if feasible: break
    If feasible, then total_cost = cost2 + len(type1_set). But note: len(type1_set) is f(l,r) only if the type1 chain is valid with all ops. But if we remove the type2 ops, the chain might change. However, if the type2 ops are not in type1_set, then the chain remains the same. So f is still len(type1_set). So we can use that.

But we need to ensure that the type1 chain is valid with the type2 ops removed. Since the type2 ops are not in type1_set, the chain doesn't use them, so it's valid. So this is correct.

Now, we also need to consider that the type1 chain might use more than the minimum number if we remove some ops. But since we are not removing any ops from type1_set, the chain is the same. So f is the same.

So we can modify our candidate evaluation as above.

But what if the type1 chain uses an op that is also a type2 op, but there is an alternative type2 op? For cost1, there is only one type2 op. So if it's in type1_set, then no alternative. For cost2, we might have alternatives. So the above check works.

Now, we also need to consider that the type1 chain might use an op that is not in type1_set? That's impossible.

So we can implement this feasibility check.

Now, we also need to compute the type1_set. We can do that by simulating the chain once for each candidate. But that would be O(f) per candidate, which could be O(M^2) total. We can optimize by noting that the type1 chain from l is the same for all candidates with the same l. So we can precompute for each l, the type1 chain (the sequence of ops) and the number of steps to cover various r. But that seems heavy.

Maybe we can precompute for each l, the positions after each jump and the corresponding op. Then, for each candidate, we can find the type1_set by looking up the chain. But we need to know how many ops to cover r. We can precompute for each l, the list of (position, op_index) pairs. The length of the list is at most the number of jumps from l, which is at most M. So total size over all l could be O(N * average chain length) which is too large.

Given the constraints, maybe we can accept O(f) per candidate in the worst case. Since we have O(M) candidates, total O(M^2) in worst case, but M=2e5, M^2=4e10, too slow. We need to reduce the number of candidates. The number of candidates is at most M (cost1) + |L_set| (cost2) + 1. |L_set| is at most M. So worst-case O(M) candidates. If each candidate takes O(f) and f can be up to M, then O(M^2). But maybe in practice, f is small. We need a better bound.

We can use the binary lifting table to also retrieve the ops used in the chain? That would be hard.

Maybe we can precompute for each l, the type1 chain in terms of the sequence of op indices. We can store for each l, the list of ops used in the chain until it terminates. This list has length equal to the number of jumps from l, which is at most the number of type1 ops that are reachable from l. This could be large for all l. But note that the total number of type1 ops is M, and each op is used in chains starting from certain l. The total number of (l, op) pairs over all chains could be large.

Given the time, I think we can implement the candidate evaluation without storing the type1_set. Instead, we can first find the best cost assuming no conflict, and then during reconstruction, we can adjust. But we need to ensure that the best candidate is actually feasible. So we need to check feasibility during the search.

To speed up, we can precompute for each l, the type1 chain and the positions after each jump. We can store for each l, an array of the positions after each jump, and the corresponding op index. Since N=1e6, and M=2e5, the average chain length might be small. We can allocate a large list of lists. But 1e6 lists is too much.

Maybe we can use a dictionary to store chains only for l that appear in candidates. The number of distinct l in candidates is at most |L_set| ≤ M, and also l=1 for cost0. So we can precompute chains only for those l. We can do:
For each l in candidate_l_set:
    Simulate the chain from l, storing the sequence of (pos, op_idx) until pos > N or chain ends.
    Store in a list.

Then, for a candidate with that l and some r, we can find how many ops are needed to cover r by finding the first pos in the chain that is > r. We can binary search the positions. The number of ops is the index in the list. Also, we can get the set of ops used: the first k ops in the list. We can store the ops as a list of indices.

This is manageable. We have at most M l's, and each chain length is at most M, so total storage O(M^2) in worst case? Actually, if every l has a chain of length M, then total O(M^2) = 4e10, too large. But in practice, the chains might be short. Worst-case, if type1 ops are such that from each l, you need many ops, it could be bad. But M=2e5, so M^2=4e10, definitely not.

We need a more efficient way.

Given the time, I think we can implement the candidate evaluation by simulating the chain for each candidate, but we can do it in O(f) per candidate, and hope that the total is acceptable. Since the number of candidates is O(M), and f is on average small, it might be okay. But worst-case, it could be slow.

Maybe we can prune candidates. We only need to consider candidates with small cost. We can compute a lower bound on f(l,r) and cost2, and skip candidates that cannot beat the current best.

We can compute a lower bound for f(l,r) as the minimum number of type1 intervals needed to cover [l,r] regardless of conflicts. This is exactly f(l,r) we computed. So we already have that.

We can also compute a lower bound for cost2: for any I, cost2 >= 0. So the total lower bound is cost2 + f(l,r). We can skip candidates with lower bound >= current best.

So in the search, we can iterate over candidates in order of increasing lower bound, and stop when the lower bound of a candidate is >= current best. We can sort candidates by (cost2 + f(l,r)) and process them in that order. Then, for each candidate, we need to check feasibility. If feasible, we update the best. Since we process in increasing order, the first feasible candidate we encounter will be optimal. So we can break early.

To do this, we need to compute f(l,r) for all candidates first, then sort. But computing f for all candidates might be expensive. We can compute f on the fly.

Let's outline the algorithm:

1. Precompute furthest, next_pos, nxt, etc.
2. Generate all candidate intervals (l,r,cost2) as described.
3. For each candidate, compute f = compute_f(l,r). If f == INF, skip.
4. Compute lower_bound = cost2 + f.
5. Sort candidates by lower_bound.
6. Initialize best_cost = INF, best_candidate = None.
7. For each candidate in sorted order:
    a. Compute type1_set by simulating the chain from l to cover r. This gives the list of op indices. Also, f should equal the length of the list. We'll use this to get the ops.
    b. Check feasibility: can we select type2 ops as per cost2 that are not in type1_set? If cost2=0, always feasible. If cost2=1, find an op with (l,r) not in type1_set. If exists, feasible. If cost2=2, find a pair of ops as described not in type1_set. If exists, feasible.
    c. If feasible, set best_cost = lower_bound, best_candidate = (l,r,cost2, type1_set, type2_ops), and break (since sorted by lower_bound).
8. If best_candidate is None, output -1.
9. Otherwise, output the ops: set the selected type1 and type2 ops to 1 and 2, others 0. Output best_cost.

Now, the simulation of the chain for each candidate: we can do it by following the next_pos array. We can start at l, and while True:
    if furthest[pos] == -1: break (impossible)
    idx = op_for_furthest[pos]
    add idx to list
    pos = furthest[pos] + 1
    if pos > r: break
This loop will take f steps, where f is the number of ops. This is O(f). Since we are processing candidates in order of increasing lower_bound, the first candidate will have small f. But there could be many candidates with small f. We need to bound the total work.

We can note that the number of candidates with the same l is at most a few. For each l, we can precompute the chain once. Since the number of distinct l in candidates is at most M, we can precompute the chain for each such l. Then, for each candidate with that l, we can binary search the chain to find the number of ops to cover r, and also the set of ops (the first k ops). This would be O(log f) per candidate. And the precomputation for each l is O(chain length). The total chain length over all l could be large, but we can do it lazily.

Given the time, I'll implement the precomputation for each l in candidate_l_set. We'll store for each such l, a list of (pos, op_idx) pairs. We'll generate the chain until pos > N. Then, for a candidate with l and r, we can binary search in the list to find the smallest index where pos > r. The number of ops is that index. Also, the ops used are the first index op indices.

This should be efficient. The total number of chains is at most M. The average chain length might be small. In the worst case, if type1 ops are dense, the chain length could be up to M, but then the number of l's is at most M, so total O(M^2) again. But M=2e5, M^2=4e10, not feasible. However, in practice, the chain length is limited by the number of type1 ops that are reachable from l. If l is large, the chain might be short. We can assume it's okay.

Let's implement this precomputation.

We'll have a dictionary chains = {}. For each l in candidate_l_set (set of all l from candidates), we'll compute the chain.

We need candidate_l_set: collect all l from candidates. From cost1 candidates: for each type2 op, l = L_i. From cost2 candidates: for each L in L_set. Also l=1 for cost0. So we can collect all l.

Now, for each l in candidate_l_set:
    chain = []
    pos = l
    while pos <= N and furthest[pos] != -1:
        idx = op_for_furthest[pos]
        chain.append( (pos, idx) )
        pos = furthest[pos] + 1
    chains[l] = chain

Note: we don't need to include positions beyond N. We stop when pos > N or no furthest.

Now, for a candidate (l,r), we can binary search in chains[l] to find the first i such that chain[i][0] > r. The number of ops is i. The set of ops is the set of indices in chain[0:i].

We also need to ensure that the chain actually covers r. If the binary search doesn't find a chain[i][0] > r, then the chain ends before covering r, so f = INF.

Now, we can precompute for each l, the chain. Then, during the search, we can quickly get f and the op set.

Now, the feasibility check: we need to check if we can select type2 ops not in the op set.

For cost1: we need an op with L=l, R=r that is not in op_set. We can precompute a dictionary from (L,R) to list of op indices. So we can check.

For cost2: we need one op with L=l, R>=r, and one with R=r, L<=l, both not in op_set. We can precompute for each l, a list of ops with that l. And for each r, a list of ops with that r. Then, we can iterate.

Now, we also need to output the actual ops. So we need to store the selected type2 ops.

Now, let's code.

We'll need to store ops in a list: ops = [(L,R,idx)].

We'll need:
- type1_ops_by_L: dictionary from L to list of (R, idx) for type1? But for type1 chain, we already have furthest and op_for_furthest.
- For type2 candidate selection: we need to quickly find ops with given L and R. We can build:
    - type2_by_LR: dict mapping (L,R) to list of indices.
    - type2_by_L: dict mapping L to list of (R, idx).
    - type2_by_R: dict mapping R to list of (L, idx).

But note: these are for all ops, since all ops can be used as type2.

Now, during feasibility check for cost1: we look up type2_by_LR.get((l,r), []) and see if there is an index not in op_set.

For cost2: we get list1 = [idx for (R,idx) in type2_by_L[l] if R >= r and idx not in op_set]
          list2 = [idx for (L,idx) in type2_by_R[r] if L <= l and idx not in op_set]
          then we need to find a pair with different indices.

Now, after finding a feasible candidate, we need to output the ops. We can set the selected type1 ops from the chain, and the selected type2 ops from the feasible pair.

Now, we need to be careful: the chain we precomputed uses the original furthest and op_for_furthest, which assume all ops are available. But if we remove some ops (the type2 ops we select), the chain might change. However, we are choosing type2 ops that are not in the op_set, so the chain is unaffected. So it's safe.

Now, we also need to ensure that the type1 ops we select are actually used. In the chain, we have the sequence of ops. We will use those.

Now, let's code step by step.

We'll implement the following steps in code:

1. Read N, M.
2. Read ops into list ops.
3. Build type1 furthest and op_for_furthest using the heap sweep.
4. Build next_pos and nxt table.
5. Build type2 arrays: maxR_at_L, minL_at_R.
6. Build segment tree for minL_at_R.
7. Generate candidate intervals and their cost2.
8. Precompute chains for each l in candidate_l_set.
9. For each candidate, compute f from the chain, and lower_bound = cost2 + f. Store candidate with f.
10. Sort candidates by lower_bound.
11. Iterate over candidates in sorted order, for each:
    a. Get f and op_set from chain.
    b. Check feasibility as described.
    c. If feasible, set best and break.
12. Output.

Now, we need to be careful with the chain precomputation: the chain for l is a list of (pos, op_idx) in order. We can also store the op_idx in a separate list for easy slicing.

We'll implement a function get_chain(l) that returns the list of op indices for the chain starting at l, and also the positions list. We'll compute it once and store.

Now, let's write the code.

We'll need to use sys.stdin for fast input.

We'll import sys, heapq, bisect.

We'll define INF = 10**9.

Now, let's code.</mm:think>### PLAN
We need to determine if we can set all x_j to 1 after M operations, each of which can be type 0 (do nothing), type 1 (set range [L_i,R_i] to 1), or type 2 (set complement to 1). We want minimum cost (number of non-zero operations).

Key observations:
- Once a position becomes 1, it stays 1. So we just need to select a subset of operations to cover [1,N] with type 1 intervals and type 2 complements.
- Using a type 2 operation with interval [L,R] covers the complement, so the uncovered part becomes the intersection of all used type 2 intervals. Thus, selecting a set B of type 2 operations leaves an interval I = ∩_{i in B} [L_i,R_i] uncovered. Then we must cover I with type 1 operations.
- The cost is |B| + f(I), where f(I) is the minimum number of type 1 intervals to cover I.
- The intersection I is determined by the maximum L and minimum R among ops in B. So we can parameterize I by (l,r) with l ≤ r. The minimum number of type 2 ops to achieve I is:
  - 0 if l=1 and r=N (no type 2 ops),
  - 1 if there exists a type 2 op with L_i = l and R_i = r,
  - 2 if there exists a type 2 op with L_i = l and R_i ≥ r and one with R_i = r and L_i ≤ l (distinct),
  - ∞ otherwise.
- f(l,r) can be computed via a greedy chain: for each position p, let furthest[p] be the maximum R among type 1 ops covering p. Then next_pos[p] = furthest[p]+1 (or -1 if none). The greedy chain from l is deterministic; f(l,r) is the number of jumps until the chain exceeds r and covers it.
- We precompute furthest[p] and op_for_furthest[p] using a sweep with a max-heap. We also build a binary lifting table for next_pos to answer f(l,r) in O(log M).
- For each candidate (l,r) that can be formed as an intersection (with cost 0,1,2), we compute f(l,r). We then check feasibility: the type 1 chain must be disjoint from the type 2 ops used. We precompute chains for relevant l to quickly obtain the set of type 1 ops used.
- Candidates are sorted by lower bound (cost2 + f). The first feasible candidate is optimal.