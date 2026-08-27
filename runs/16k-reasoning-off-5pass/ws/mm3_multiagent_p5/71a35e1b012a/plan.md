We need to decide for each operation whether to apply type 0 (cost 0, no change), type 1 (set all indices in [L,R] to 1), or type 2 (set all indices outside [L,R] to 1). The goal is to make all positions 1 after all M operations, minimizing total cost.

Observation: Once a position becomes 1, it stays 1 forever (operations only set to 1). So we only need to ensure every position is covered by at least one operation that sets it to 1. For each operation i, we can choose to cover either the interval [L_i,R_i] (type 1) or its complement (type 2). This is a classic set cover problem where each operation can cover one of two sets, and we want minimum cost covering of all N elements.

We can solve it with a flow / bipartite matching approach: Build a bipartite graph where left side is operations, right side is positions. For each operation i, we can connect it to all positions in [L_i,R_i] (if we choose type 1) OR to all positions outside [L_i,R_i] (if we choose type 2). However, N can be up to 1e6, so we cannot build explicit edges for all positions.

Key insight: The problem can be reduced to checking whether the intervals and their complements can cover all positions. Since each operation can cover either an interval or its complement, we need to select a set of operations such that the union of their chosen sets covers [1,N].

We can think of it as: For each operation i, we have two possible "coverage sets": A_i = [L_i,R_i] and B_i = complement of [L_i,R_i]. We need to pick one of them (or none) for each i, paying cost 1 for picking A_i or B_i, cost 0 for picking none, such that union covers [1,N].

This is equivalent to: We have M operations, each can be assigned to cover either its interval or its complement. We need to cover all positions. This is like a 2-SAT or flow problem.

Alternative view: Consider the positions that are not covered by any chosen interval. They must be covered by complements. So we can think of selecting a set of operations to be type 1, and the rest type 2 (or 0). But type 0 does nothing, so if we select type 0, we don't cover anything. So we only care about operations we actually use (cost 1). We want to use a subset of operations, each assigned to either interval or complement, covering all positions, minimizing number of used operations.

This is a minimum set cover with two choices per set. Since N is large, we need a smarter approach.

Observation: The complement of an interval is two intervals: [1, L_i-1] and [R_i+1, N]. So type 2 covers two intervals. Type 1 covers one interval. So we have M intervals (type 1) and M pairs of intervals (type 2). We need to cover [1,N] with minimum number of these sets.

This is a covering problem on a line. We can solve it greedily? Not necessarily, because type 2 covers two disjoint intervals, which might be beneficial.

We can model it as a flow problem: Create a source, sink, and nodes for operations and positions? But positions are too many.

Better: Since the line is 1D, we can think of the problem as: We need to cover each point. For each operation, we can choose to cover either the interval or its complement. This is equivalent to: For each operation, we can "activate" either the interval or the complement. We want to minimize activations.

We can solve it using a greedy algorithm with a priority queue? Consider scanning from left to right. At each position, we need to cover it. We can choose an operation that covers it (either as interval or as complement). But complements cover two sides, so they might also cover future positions.

Actually, we can think of it as: We have M intervals (type 1) and M complements (type 2). We want to cover [1,N] with minimum number of these sets. Since complements are two intervals, we can treat them as two separate intervals but they come in pairs: if we pick a complement, we cover both sides simultaneously with cost 1.

This is similar to covering a line with intervals where some intervals are "paired" (if you pick one, you must pick its pair? No, picking a complement covers both sides, but picking an interval covers only one side). Actually, picking a complement is like picking two intervals at cost 1. Picking an interval is picking one interval at cost 1.

So we have M single intervals and M pairs of intervals (each pair is the complement of a single interval). We want to cover [1,N] with minimum cost, where cost of a single interval is 1, cost of a pair is 1 (but covers two intervals). This is like: we have a set of intervals, some are "bundled" in pairs. We can either take one interval from a bundle (cost 1) or both intervals from a bundle (cost 1). Wait, no: For operation i, we can either:
- Take interval [L_i,R_i] (cost 1)
- Take complement (cost 1), which is two intervals: [1,L_i-1] and [R_i+1,N]
- Take nothing (cost 0)

So it's like: For each i, we have a choice: either take one specific interval, or take two specific intervals (the complement), or take nothing. We want to cover [1,N] with minimum cost.

This is a classic problem that can be solved with a greedy algorithm using a priority queue, similar to covering a line with intervals, but with the twist that some choices cover two disjoint intervals.

We can solve it by considering the problem as a minimum cost to cover all points. Since N is up to 1e6, we can do a sweep line.

Idea: We want to cover the entire [1,N]. We can think of it as: we need to select a set of operations such that every point is covered by at least one selected operation's chosen set.

We can model it as a flow problem on a graph of intervals? But intervals are continuous.

Alternative: Since the operations are independent, we can think of the problem as: For each position j, we need at least one operation i such that either (L_i <= j <= R_i and we choose type 1) or (j < L_i or j > R_i and we choose type 2). So for each j, we need to satisfy: (exists i with L_i <= j <= R_i and op_i=1) OR (exists i with (j < L_i or j > R_i) and op_i=2).

This is a covering problem. We can solve it by reducing to a bipartite matching? Not directly.

Another approach: Since the operations only set to 1, we can think backwards: Start with all 1s, and operations can set to 0? No, they only set to 1.

Wait, maybe we can think of it as: We need to ensure that for every position j, there is some operation i that covers it. If we choose type 1 for i, it covers [L_i,R_i]. If we choose type 2 for i, it covers everything except [L_i,R_i].

So for each j, we need either:
- Some i with L_i <= j <= R_i and op_i=1, or
- Some i with (j < L_i or j > R_i) and op_i=2.

Equivalently, if we let S be the set of operations with op=1, and T be the set with op=2, then we need: [1,N] subset of (union of [L_i,R_i] for i in S) union (union of complements for i in T). But union of complements for i in T is the complement of intersection of [L_i,R_i] for i in T. So we need: [1,N] subset of A union (complement of B), where A = union of intervals for S, B = intersection of intervals for T. That is: complement of B subset of A. So we need: intersection of [L_i,R_i] for i in T is subset of union of [L_i,R_i] for i in S. And we want to minimize |S|+|T|.

This is a nice characterization: We need to choose two sets S and T (disjoint? Not necessarily, an operation can be both? No, each operation is exactly one of 0,1,2. So S and T are disjoint, and we can have operations not in S or T (type 0). So we need: intersection_{i in T} [L_i,R_i] subset of union_{i in S} [L_i,R_i]. And we want to minimize |S|+|T|.

This is a set cover problem with intersection condition. Still hard.

Maybe we can solve it with a greedy algorithm that scans from left to right, maintaining the current uncovered position, and using a priority queue of available operations that can cover it.

Consider scanning from left to right. At position x, we need to cover it. We can use an operation i that covers x either as interval (if L_i <= x <= R_i) or as complement (if x < L_i or x > R_i). But if we use it as complement, it also covers the other side. So we might want to use complements to cover the ends.

Actually, we can think of it as: We need to cover the whole line. The complement of an interval is two intervals at the ends. So type 2 is useful for covering the ends (1 and N) or gaps in the middle? But if we use type 2, it covers everything except the interval, so it covers two separate pieces. That might be inefficient if the interval is large, because then the complement is small. But if the interval is small, the complement is large.

We can solve this with a minimum cost flow on a graph of intervals? Since N is up to 1e6, we can compress coordinates.

Idea: We have M intervals. We want to cover [1,N] with either intervals or their complements. This is equivalent to: We want to select a set of intervals (some from the M, some from the complements) to cover [1,N]. The complements are also intervals (actually two intervals). So we have a set of intervals: for each i, we have [L_i,R_i] and also [1,L_i-1] and [R_i+1,N]. We can pick at most one from each i (either the interval or the two complements, but picking the two complements costs 1, picking the interval costs 1, picking nothing costs 0). So we have a set of "options": for each i, we have option A: pick interval [L_i,R_i] (cost 1), option B: pick two intervals [1,L_i-1] and [R_i+1,N] (cost 1), option C: pick nothing (cost 0). We want to cover [1,N] with minimum cost.

This is a covering problem with options that cover multiple intervals. Since the line is 1D, we can solve it with a greedy algorithm that always covers the leftmost uncovered point with the option that extends furthest to the right? But options can cover two disjoint intervals, so they might also cover points on the right end.

We can think of it as: We need to cover the entire [1,N]. We can process from left to right. At each step, we have a current position cur that is not yet covered. We need to cover it. We can choose an operation i such that either:
- L_i <= cur <= R_i (then we can use type 1 to cover from L_i to R_i, which covers cur and extends to R_i)
- cur < L_i or cur > R_i (then we can use type 2, which covers [1,L_i-1] and [R_i+1,N]. If cur < L_i, then type 2 covers cur (since cur is in [1,L_i-1]) and also covers [R_i+1,N]. If cur > R_i, then type 2 covers cur and also covers [1,L_i-1].)

So if we are at cur, and we pick an operation with L_i <= cur <= R_i and use type 1, we cover up to R_i. If we pick an operation with cur < L_i and use type 2, we cover [1,L_i-1] (which includes cur) and also [R_i+1,N]. But that might cover the right end as well. Similarly, if cur > R_i and we use type 2, we cover [R_i+1,N] (including cur) and [1,L_i-1].

So using type 2 can cover two separate regions. This makes the greedy approach tricky because a single choice can cover both left and right ends.

Maybe we can solve it by considering the problem as a minimum cut or flow on a graph of intervals. Since the intervals are on a line, we can create a graph where nodes are the interval endpoints, and edges represent possible coverings.

Another idea: Since we only need to cover all points, and the operations are independent, we can think of it as a 2-SAT problem? For each position j, we need at least one operation covering it. But that's a covering problem, not 2-SAT.

Wait, maybe we can solve it by dynamic programming on the line? Since N is up to 1e6, we can do DP if we compress coordinates. But the state would be the current coverage? That's too large.

Let's think differently. The problem is equivalent to: We have M operations. We want to assign each operation to 0,1,2 such that the union of the chosen sets covers [1,N]. We want to minimize the number of operations assigned to 1 or 2.

This is a minimum cost set cover problem with two choices per set. Since the universe is a line, we might be able to solve it with a greedy algorithm that is optimal for intervals? For covering a line with intervals, the greedy algorithm (always pick the interval that starts at or before the current point and extends furthest) is optimal. Here we have two types of intervals: single intervals and pairs of intervals (the complement). But the pairs are not arbitrary: they are the complement of a single interval. So if we pick the complement, we cover two intervals that are separated by the original interval.

We can think of it as: We have a set of intervals I_i = [L_i,R_i]. We can either pick I_i or its complement. The complement is two intervals: left = [1,L_i-1] and right = [R_i+1,N]. So picking the complement is like picking two intervals that are at the ends.

Observation: If we pick the complement of I_i, we cover everything except I_i. So if we pick the complement, we don't need to cover I_i with other operations. But we might still need to cover parts of I_i if we don't pick the complement? Actually, if we pick the complement, I_i is not covered by that operation, so we need to cover I_i with other operations (either type 1 or type 2 of other operations). So picking the complement forces us to cover I_i using other operations.

This suggests a duality: If we pick type 1 for i, we cover I_i. If we pick type 2 for i, we cover the complement, so we need to cover I_i by other means.

We can think of it as: We need to cover [1,N]. For each i, we can either "block" I_i (by picking type 2, which covers everything else, so I_i becomes the only uncovered part, but we still need to cover it) or "unblock" I_i (by picking type 1, which covers I_i). Actually, picking type 2 covers the complement, so I_i is left uncovered by that operation. So to cover I_i, we need other operations that cover it. So if we pick type 2 for i, we must ensure I_i is covered by other operations (either type 1 or type 2 of other operations). But if another operation j has type 2, it covers the complement of I_j, so it covers I_i only if I_i is not subset of I_j? Actually, type 2 of j covers everything except I_j. So it covers I_i if I_i is not entirely contained in I_j. If I_i is contained in I_j, then type 2 of j does not cover I_i. So type 2 of j covers I_i unless I_i subset I_j.

This is getting complicated.

Maybe we can solve it with a flow network: Create a bipartite graph between operations and positions? But positions are too many.

Alternative: Since N is up to 1e6, we can use a segment tree or interval tree to represent the uncovered positions. We can greedily cover the leftmost uncovered position. At each step, we have a set of operations that can cover the current position. We want to choose the one that minimizes the total cost. But we need to look ahead because type 2 covers two sides.

We can model it as: We want to cover the entire [1,N]. We can think of it as a game where we have operations that can cover either an interval or its complement. We want to minimize the number of operations used.

This is similar to the problem of covering a line with intervals where you can also cover the complement. I recall a similar problem: "Set Cover on a Line" can be solved with a greedy algorithm if the sets are intervals. But here we have complements.

Let's try to solve it with a greedy algorithm that scans from left to right and uses a priority queue of operations that can cover the current point. At point cur, we consider all operations i such that either L_i <= cur <= R_i (can use type 1) or cur < L_i (can use type 2 to cover left side) or cur > R_i (can use type 2 to cover right side). But if we use type 2 for cur < L_i, it also covers the right side [R_i+1,N]. So it might be beneficial to use type 2 even if it doesn't extend the left coverage much, because it also covers the right end.

We can maintain two priority queues: one for operations that can cover cur as type 1 (i.e., L_i <= cur <= R_i), and one for operations that can cover cur as type 2 from the left (i.e., cur < L_i). Actually, if cur < L_i, then type 2 covers [1,L_i-1], so it covers cur and everything to the left up to L_i-1. So it extends left coverage to L_i-1. But it also covers the right side [R_i+1,N]. So if we use it, we cover left up to L_i-1 and right from R_i+1 to N. That might cover the entire right side if R_i+1 is small.

Similarly, if cur > R_i, type 2 covers [R_i+1,N] and [1,L_i-1].

So we can think of it as: We need to cover the whole line. We can process from left to right. At each step, we have a current leftmost uncovered position cur. We want to cover it. We can choose an operation that covers cur. If we choose type 1, we cover up to R_i. If we choose type 2, we cover left up to L_i-1 (if cur < L_i) or right from R_i+1 (if cur > R_i). But type 2 also covers the other side. So if we choose type 2 with cur < L_i, we cover left up to L_i-1 and right from R_i+1 to N. That means we might cover the entire right side in one go if R_i+1 is the start of the right uncovered part.

This suggests that we can solve it by considering the problem as covering the line with intervals, but with the option to cover two disjoint intervals at once. We can use a greedy algorithm that always covers the leftmost uncovered point with the operation that gives the best "coverage" in terms of extending the left boundary and also covering the right boundary.

We can maintain the current covered interval on the left: [1, cur-1] is covered, and we need to cover from cur to N. We also have a set of operations that can cover cur. We want to choose one that minimizes the total cost. Since we want to minimize the number of operations, we want to cover as much as possible with each operation.

But type 2 can cover two separate parts. So if we use type 2, we might cover the right end completely, leaving only the middle uncovered. Then we need to cover the middle with other operations.

We can think of it as: We need to cover [1,N]. We can choose a set of operations. Each operation either covers an interval or its complement. This is equivalent to: We have a set of intervals (the original ones) and we can also choose to cover the complement. But covering the complement is like covering two intervals at the ends.

We can solve this by reducing to a minimum path cover or something? Not sure.

Let's think about the sample inputs to get intuition.

Sample 1:
N=5, M=4
Intervals: [2,4], [3,5], [1,4], [2,5]
Solution: 2 0 1 0 (cost 2)
So we use operation 3 (type 1) and operation 1 (type 2)? Actually output: op1=2, op2=0, op3=1, op4=0.
So we use type 2 on [2,4] (covers 1 and 5), and type 1 on [1,4] (covers 1,2,3,4). Together they cover all.

Sample 2:
N=5, M=4
Intervals: [1,3], [1,5], [2,4], [3,5]
Solution: 0 1 0 0 (cost 1)
Use type 1 on [1,5] covers all.

Sample 3:
N=5, M=2
Intervals: [1,3], [2,5]
Solution: 1 1 (cost 2)
Use type 1 on both: [1,3] and [2,5] together cover all.

Sample 4:
N=5, M=2
Intervals: [1,3], [2,4]
Solution: -1
Because [1,3] and [2,4] overlap but leave 5 uncovered. Can we use type 2? Type 2 on [1,3] covers 4,5. Type 2 on [2,4] covers 1,5. But we need to cover all. If we use type 2 on [1,3], we cover 4,5. Then we need to cover 1,2,3. But [2,4] type 1 covers 2,3,4. So 1 is uncovered. If we use type 2 on [2,4], we cover 1,5. Then we need to cover 2,3,4. [1,3] type 1 covers 1,2,3. So 4 is uncovered. If we use both type 2: [1,3] type 2 covers 4,5; [2,4] type 2 covers 1,5. Union: 1,4,5. Missing 2,3. So impossible.

So the problem is to determine if we can cover all positions with a set of intervals where each operation gives us either the interval or its complement.

We can think of it as a covering problem on a line. Since the line is 1D, we can solve it with a greedy algorithm that is optimal for covering with intervals, but we need to handle the complement option.

I recall that covering a line with intervals (where you can choose any intervals) is solved by greedy: sort intervals by start, then for each point, pick the interval that starts at or before the point and extends furthest. Here we have two choices per operation: either the interval or its complement. The complement is two intervals: left and right. So we have a set of intervals: for each i, we have I_i = [L_i,R_i], and also left_i = [1,L_i-1] and right_i = [R_i+1,N]. But we can only pick at most one "bundle" per i: either I_i, or left_i and right_i together, or nothing.

This is like a set cover with bundles. Since the universe is a line, we might be able to solve it with a greedy algorithm that considers the bundles.

We can think of it as: We want to cover [1,N]. We can choose a set of bundles. Each bundle is either a single interval or a pair of intervals (left and right). We want to minimize the number of bundles.

We can solve this by considering the problem as a minimum cost to cover all points, where the cost of a bundle is 1. This is a classic problem that can be solved with a greedy algorithm if the bundles are "interval graphs" or something. But here the bundles are not arbitrary: the pair is always the complement of the single interval.

Observation: If we pick the complement of I_i, we cover everything except I_i. So if we pick the complement, we don't cover I_i. So we need to cover I_i with other bundles. This means that if we pick the complement, we must ensure that I_i is covered by other bundles. So picking the complement is only useful if we can cover I_i efficiently with other bundles.

We can think of it as: We need to cover [1,N]. For each i, we have two options: cover I_i (cost 1) or cover the complement (cost 1) but then we need to cover I_i by other means. So it's like: we can either "pay 1 to cover I_i" or "pay 1 to cover the complement, but then we still need to cover I_i". So the complement option is only better if covering I_i is expensive.

This suggests a dynamic programming approach: We can decide for each operation whether to use it as type 1 or type 2. But we need to cover all positions.

Maybe we can solve it by reducing to a minimum cut in a graph. Consider the following: Create a graph with nodes for each position? Too many.

Another idea: Since the operations are independent, we can think of the problem as: We need to select a set of operations such that the union of their chosen sets covers [1,N]. This is equivalent to: The complement of the union is empty. The complement of the union is the intersection of the complements of the chosen sets. For operation i, if we choose type 1, its complement is the set of positions not in [L_i,R_i]. If we choose type 2, its complement is [L_i,R_i]. If we choose type 0, its complement is everything. So the intersection of the complements of the chosen sets (type 1 and type 2) must be empty. That is: For every position j, there is no operation i such that j is in the complement of the chosen set for i. In other words, for every j, there exists i such that j is not in the complement of the chosen set for i. That is: For every j, there exists i such that either (i is type 1 and j in [L_i,R_i]) or (i is type 2 and j not in [L_i,R_i]). This is just restating the condition.

We can think of it as a hitting set problem: We need to hit every position j with at least one operation's chosen set. This is set cover.

Given the constraints, we need an O((N+M) log N) or O(M log M) solution.

I think we can solve it with a greedy algorithm that scans from left to right and uses a priority queue of available operations that can cover the current point. But we need to handle the fact that type 2 covers two sides.

Let's try to design a greedy algorithm:

We want to cover [1,N]. We can process from left to right. Let cur be the leftmost uncovered position. We want to cover cur. We have a set of operations that can cover cur. For each such operation i, we have two choices:
- Use type 1: covers [L_i,R_i]. Since cur is in [L_i,R_i], this covers from L_i to R_i. So it covers cur and extends to R_i.
- Use type 2: covers complement. Since cur is in [L_i,R_i]? Wait, if cur is in [L_i,R_i], then type 2 does NOT cover cur. So if cur is in [L_i,R_i], we cannot use type 2 to cover cur. So for an operation i with L_i <= cur <= R_i, we can only use type 1 to cover cur.
If cur < L_i, then type 2 covers cur (since cur is in [1,L_i-1]). So we can use type 2. This covers [1,L_i-1] and [R_i+1,N]. So it covers cur and extends left to 1, and also covers right from R_i+1 to N.
If cur > R_i, then type 2 covers cur (since cur is in [R_i+1,N]). So we can use type 2. This covers [R_i+1,N] and [1,L_i-1]. So it covers cur and extends right to N, and also covers left from 1 to L_i-1.

So at position cur, the operations that can cover cur are:
- Those with L_i <= cur <= R_i: can use type 1, covers up to R_i.
- Those with cur < L_i: can use type 2, covers left up to L_i-1 and right from R_i+1 to N.
- Those with cur > R_i: can use type 2, covers right up to N and left from 1 to L_i-1.

Note that if cur < L_i, then using type 2 covers left up to L_i-1, which is at least cur. So it covers cur and possibly more left. But since we are scanning from left to right, we have already covered up to cur-1. So covering left further is not useful. However, it also covers right from R_i+1 to N. So it might cover the entire right side. So using type 2 for cur < L_i is beneficial if R_i+1 is small (i.e., the right uncovered part is small). Similarly, if cur > R_i, using type 2 covers right up to N (which is good) and left from 1 to L_i-1 (which is already covered, so not useful).

So the interesting case is when we have operations with cur < L_i. Using type 2 on them covers the right side. So we might want to use them to cover the right side.

We can maintain the current uncovered interval: [cur, N] (since left is covered). We want to cover [cur, N]. We can choose an operation that covers cur. If we choose type 1 on i with L_i <= cur <= R_i, we cover [cur, R_i] (and possibly left, but left is already covered). So we cover up to R_i. Then we set cur = R_i+1.
If we choose type 2 on i with cur < L_i, we cover [cur, L_i-1] (but left is already covered, so we cover [cur, L_i-1] which is new) and [R_i+1, N]. So we cover the right side from R_i+1 to N. So if we do this, we cover the entire right side if R_i+1 <= cur? Actually, if cur < L_i, then R_i+1 could be anything. But we cover [R_i+1, N]. So if R_i+1 <= cur, then we cover [cur, N] completely? Not necessarily: we cover [R_i+1, N]. If R_i+1 <= cur, then we cover [cur, N] as part of [R_i+1, N]. So we cover the entire right side. But we also cover [1, L_i-1], which is already covered. So effectively, using type 2 on i with cur < L_i covers [R_i+1, N]. So it covers the right side from R_i+1 to N. So if we choose such an operation, we can set cur = max(cur, R_i+1)? Actually, we cover [R_i+1, N], so the new uncovered part is [cur, R_i] if R_i >= cur. But we already have cur < L_i, so R_i could be anything. We need to see what is covered.

Let's formalize: At step, we have covered [1, cur-1]. We need to cover [cur, N]. We choose an operation i that covers cur.
Case 1: L_i <= cur <= R_i. Use type 1. Covers [L_i, R_i]. Since cur is in there, we cover [cur, R_i]. So new covered: [1, R_i]. New cur = R_i+1.
Case 2: cur < L_i. Use type 2. Covers [1, L_i-1] and [R_i+1, N]. Since cur < L_i, cur is in [1, L_i-1], so we cover [cur, L_i-1] (but left is already covered, so we cover [1, L_i-1] which is already covered). We also cover [R_i+1, N]. So new covered: [1, L_i-1] union [R_i+1, N]. But we already have [1, cur-1] covered. So the new covered is [1, cur-1] union [R_i+1, N]. So the uncovered part is [cur, R_i] if R_i >= cur, or empty if R_i < cur. But note that cur < L_i, so R_i could be less than cur or greater. If R_i < cur, then [R_i+1, N] includes [cur, N], so we cover everything. If R_i >= cur, then we cover [R_i+1, N], so uncovered is [cur, R_i]. So new cur = cur (if R_i >= cur) or we are done (if R_i < cur). But wait, if R_i < cur, then [R_i+1, N] covers from R_i+1 to N. Since R_i+1 <= cur, it covers [cur, N]. So we are done. So using type 2 on i with cur < L_i covers the right side from R_i+1 to N. So it is beneficial if R_i+1 is small.
Case 3: cur > R_i. Use type 2. Covers [R_i+1, N] and [1, L_i-1]. Since cur > R_i, cur is in [R_i+1, N], so we cover [cur, N]. Also covers [1, L_i-1] (already covered). So new covered: [1, cur-1] union [cur, N] = [1, N]. So we are done. So if we have an operation with cur > R_i, using type 2 covers everything to the right of cur, so we finish.

So the greedy algorithm: At each step, we have cur. We want to cover cur. We have three types of operations:
- Type A: L_i <= cur <= R_i. Using type 1 covers up to R_i.
- Type B: cur < L_i. Using type 2 covers right from R_i+1 to N.
- Type C: cur > R_i. Using type 2 covers right from cur to N (so finishes).

We want to minimize the number of operations. So we want to choose the operation that gives the best coverage. For Type A, we cover up to R_i. For Type B, we cover right from R_i+1 to N. For Type C, we finish.

We can maintain a priority queue of available operations. As we increase cur, the set of available operations changes. We can add operations to the queue when they become available.

Specifically:
- For Type A: operations with L_i <= cur <= R_i. As cur increases, we add operations when cur reaches L_i, and they are available until cur > R_i.
- For Type B: operations with cur < L_i. These are operations where L_i > cur. They are available as long as cur < L_i. But if we use them, we cover right from R_i+1. So we want to use the one with smallest R_i+1? Actually, we want to cover as much right as possible, so we want R_i+1 to be as small as possible, i.e., R_i as small as possible. But we also need cur < L_i. So we want an operation with L_i > cur and small R_i.
- For Type C: operations with cur > R_i. These are operations where R_i < cur. They are available when cur > R_i. Using them finishes the job.

So the greedy strategy: At each cur, we want to choose the operation that maximizes the new cur. For Type A, new cur = R_i+1. For Type B, new cur = max(cur, R_i+1) but if R_i+1 <= cur, we finish. Actually, if we use Type B, we cover [R_i+1, N]. So if R_i+1 <= cur, we cover everything. So we can finish if there exists an operation with cur < L_i and R_i < cur. That is, L_i > cur and R_i < cur. So if there is an operation that is entirely to the left of cur (i.e., R_i < cur), then using type 2 on it covers everything to the right of cur, so we finish. But wait, if R_i < cur, then cur > R_i, so it's Type C. So Type C is exactly that: operations with R_i < cur. So if we have any operation with R_i < cur, we can use type 2 to finish. So we should always check if there is an operation with R_i < cur. If yes, we can finish in one operation.

Otherwise, we need to cover cur. We can use Type A or Type B. For Type A, we cover up to R_i. For Type B, we cover right from R_i+1. But if we use Type B, we might not cover cur if R_i >= cur? Actually, if we use Type B, we cover [R_i+1, N]. So if R_i >= cur, then we cover [R_i+1, N], but we don't cover [cur, R_i]. So we still need to cover [cur, R_i]. So using Type B when R_i >= cur leaves a gap. So we would need to cover that gap later. So it's better to use Type A if possible, because it covers continuously from cur to R_i. Type B covers a separate interval on the right. So if we use Type B, we might create two separate uncovered intervals: [cur, R_i] and maybe something else? Actually, after using Type B, we have covered [1, L_i-1] and [R_i+1, N]. So the uncovered part is [L_i, R_i]. But we started with cur < L_i, so the uncovered part is [cur, R_i] (since [1, cur-1] is covered). So we have a single uncovered interval [cur, R_i]. So we still need to cover that. So using Type B essentially reduces the problem to covering [cur, R_i] with the remaining operations. But note that we used one operation to cover the right side, so we saved covering [R_i+1, N]. So it's beneficial if R_i is small.

So the greedy algorithm: At each cur, we want to cover [cur, N]. We have operations. We can choose an operation that covers cur. We want to minimize the number of operations. This is similar to covering a line with intervals, but with the option to cover the right side separately.

We can think of it as: We need to cover [cur, N]. We can either:
- Pick an interval [L_i,R_i] that contains cur, which covers up to R_i.
- Pick an operation with L_i > cur, which covers [R_i+1, N] (and also [1, L_i-1], but that's already covered). So it covers the right part from R_i+1 to N, leaving [cur, R_i] uncovered.

So if we pick the second option, we split the problem into two parts: [cur, R_i] and [R_i+1, N] (but the latter is covered). So we only need to cover [cur, R_i]. So we can think of it as: we choose an operation i with L_i > cur, and we pay 1 to cover [R_i+1, N], and then we need to cover [cur, R_i]. So it's like we are reducing the right endpoint from N to R_i.

So we can define a recursive process: We want to cover [cur, N]. We can choose an operation i such that either:
- L_i <= cur <= R_i: then we cover [cur, R_i] and need to cover [R_i+1, N].
- L_i > cur: then we cover [R_i+1, N] and need to cover [cur, R_i].

In both cases, we need to cover [cur, max(R_i)]? Actually, in the first case, we cover [cur, R_i] and need to cover [R_i+1, N]. In the second case, we cover [R_i+1, N] and need to cover [cur, R_i]. So in both cases, we need to cover [cur, R_i] and [R_i+1, N]? Wait, in the first case, we cover [cur, R_i] (since cur is in [L_i,R_i], we cover from L_i to R_i, but left is already covered, so we cover [cur, R_i]). So we cover [cur, R_i] and need to cover [R_i+1, N]. In the second case, we cover [R_i+1, N] and need to cover [cur, R_i]. So in both cases, we need to cover [cur, R_i] and [R_i+1, N]? But in the first case, we already covered [cur, R_i], so we only need to cover [R_i+1, N]. In the second case, we covered [R_i+1, N], so we only need to cover [cur, R_i]. So it's symmetric: we choose an operation i, and we cover either the left part or the right part, and we need to cover the other part.

So we can think of it as: We have an interval [cur, N]. We choose an operation i. We can either cover [cur, R_i] (if cur in [L_i,R_i]) or cover [R_i+1, N] (if cur < L_i). In both cases, we need to cover the remaining part. So we are essentially splitting the interval at R_i. We pay 1 for the operation, and we need to cover the other part.

This is exactly the problem of covering an interval with operations that can cover either a subinterval containing the left end or a subinterval starting after the left end. This is similar to the problem of covering a line with intervals where you can choose intervals that start at or before the current point and extend as far as possible, or you can choose intervals that start after the current point and cover the right part.

We can solve this with a greedy algorithm that always chooses the operation that minimizes the remaining uncovered part. But we need to be careful because the remaining part might be on the left or right.

We can use a priority queue to keep track of available operations. As we move cur from left to right, we add operations to the queue when they become available. For each cur, we want to choose an operation that maximizes the coverage. But we have two types of coverage: covering to the right (Type A) and covering the right end (Type B). We want to minimize the number of operations, so we want to cover as much as possible with each operation.

We can maintain two sets:
- Set A: operations with L_i <= cur <= R_i. For these, using type 1 covers up to R_i. We want the one with maximum R_i.
- Set B: operations with L_i > cur. For these, using type 2 covers from R_i+1 to N. We want the one with minimum R_i (so that R_i+1 is as small as possible, covering more of the right side). But note that if we use Type B, we cover [R_i+1, N], so we need to cover [cur, R_i]. So we want R_i to be as small as possible to minimize the remaining left part. But we also need L_i > cur. So we want an operation with L_i > cur and small R_i.

Also, we have Set C: operations with R_i < cur. For these, using type 2 covers [cur, N] (since it covers [R_i+1, N] and cur > R_i, so cur is in [R_i+1, N]). So we can finish immediately.

So the algorithm:
Initialize cur = 1.
While cur <= N:
  Add to Set A all operations with L_i == cur.
  Add to Set B all operations with L_i == cur? Actually, Set B is operations with L_i > cur. So we can add operations to Set B when we pass L_i? Better: we can maintain a pointer to operations sorted by L_i. As cur increases, we move operations from "future" to "available for B" when cur < L_i. But we need to know when L_i > cur. So we can sort operations by L_i. For each cur, we can add operations with L_i == cur to Set A (if R_i >= cur) and also they are not in Set B anymore. Actually, when cur reaches L_i, the operation becomes available for Type A (if R_i >= cur) and leaves Set B (since now cur is not < L_i). So we can maintain a data structure.

We also need to add operations to Set C when cur > R_i. So we can sort operations by R_i. As cur increases, when cur becomes R_i+1, the operation becomes available for Set C.

So we can do:
Sort operations by L_i. Have an index into this sorted list. For each cur from 1 to N:
  While there are operations with L_i == cur, add them to Set A (if R_i >= cur) and remove from Set B? Actually, we can maintain Set B as operations with L_i > cur. So initially, all operations are in Set B. As cur increases, when cur reaches L_i, we move the operation from Set B to Set A (if R_i >= cur) or to Set C (if R_i < cur). But we can handle this by checking R_i.

Alternatively, we can maintain three sets:
- Set A: operations with L_i <= cur <= R_i. These are available for Type A.
- Set B: operations with L_i > cur. These are available for Type B.
- Set C: operations with R_i < cur. These are available for Type C (finish).

We can update these sets as cur increases. When cur increases by 1, some operations may move from Set B to Set A (if L_i == cur) or from Set A to Set C (if R_i == cur-1). Actually, when cur becomes L_i, the operation moves from Set B to Set A (if R_i >= L_i) or to Set C (if R_i < L_i). When cur becomes R_i+1, the operation moves from Set A to Set C.

So we can process cur from 1 to N. At each cur, we update the sets. Then we check:
- If Set C is non-empty, we can finish: choose any operation from Set C, use type 2, and we are done. So we can output the operations and finish.
- Else, we need to cover cur. We can choose from Set A or Set B.
  - From Set A, we can use type 1 to cover up to R_i. We want the operation with maximum R_i.
  - From Set B, we can use type 2 to cover [R_i+1, N]. We want the operation with minimum R_i (so that the remaining left part [cur, R_i] is as small as possible).
  We want to choose the option that minimizes the total number of operations. This is like a shortest path problem. We can use a greedy choice: always choose the option that gives the largest "jump" in cur? But we need to consider that using Set B might leave a gap that needs to be covered later.

We can think of it as: We want to minimize the number of steps to reach N+1 (meaning covered). At each step, we can either:
- Use an operation from Set A: new cur = R_i+1 (where R_i is max in Set A).
- Use an operation from Set B: new cur = R_i+1 (where R_i is min in Set B), but note that after using Set B, we cover [R_i+1, N], so we are done if R_i+1 <= cur? Actually, if we use Set B, we cover [R_i+1, N]. So if R_i+1 <= cur, we are done. But since we are in the case where Set C is empty, we have R_i >= cur for all operations? Not necessarily: Set B has L_i > cur, so R_i could be anything. But if there is an operation with R_i < cur, it would be in Set C. So in Set B, we have L_i > cur and R_i >= cur (since if R_i < cur, it would be in Set C). So for Set B, R_i >= cur. So using Set B covers [R_i+1, N], leaving [cur, R_i] uncovered. So new cur is still cur, but the right endpoint is reduced to R_i. So we need to cover [cur, R_i]. So it's like we are moving the right endpoint from N to R_i. So we can think of it as: we have an interval [cur, right] where right = N initially. We can either:
- Use Set A: move cur to R_i+1 (where R_i is max in Set A).
- Use Set B: move right to R_i (where R_i is min in Set B), and cur stays the same.
We want to reach cur > right.

This is a two-dimensional state: (cur, right). We want to minimize the number of steps to reach cur > right. We can do a BFS or Dijkstra on this state. But the state space is large (cur up to N, right up to N). However, we can optimize because the transitions are monotonic.

We can use a greedy algorithm that always chooses the option that minimizes the number of steps. But we need to prove optimality.

Alternatively, we can model it as a shortest path problem on a graph where nodes are positions and edges are operations. But that might be too large.

Given the constraints, we need an O((N+M) log N) solution.

I think we can solve it with a greedy algorithm that always chooses the operation that maximizes the coverage, but we need to handle the two types.

Let's try to design a greedy algorithm that is optimal.

We want to cover [1,N]. We can think of it as: we need to select a set of operations. Each operation i can be assigned to cover either [L_i,R_i] or its complement. We want to minimize the number of operations used.

This is equivalent to: we have a set of intervals. We want to cover [1,N] with a set of intervals, where each operation gives us either the interval or its complement. The complement is two intervals: [1,L_i-1] and [R_i+1,N]. So we have a set of intervals: for each i, we have I_i = [L_i,R_i], and also left_i = [1,L_i-1] and right_i = [R_i+1,N]. We can pick at most one "bundle" per i: either I_i, or left_i and right_i together, or nothing.

We want to cover [1,N] with minimum number of bundles.

This is a set cover problem on a line with bundles. Since the line is 1D, we can solve it with a greedy algorithm that scans from left to right and uses a priority queue of available bundles. But we need to handle the fact that some bundles cover two disjoint intervals.

We can think of it as: we need to cover the line. We can process from left to right. At each step, we have a current leftmost uncovered point cur. We want to cover it. We have a set of bundles that can cover cur. A bundle can cover cur if:
- It is I_i and L_i <= cur <= R_i.
- It is left_i and cur <= L_i-1 (i.e., cur < L_i).
- It is right_i and cur >= R_i+1 (i.e., cur > R_i).

We want to choose a bundle that minimizes the total cost. Since we want to minimize the number of bundles, we want to cover as much as possible with each bundle.

We can maintain a priority queue of available bundles. As we move cur, we add bundles that become available. For each bundle, we know what it covers. We want to choose the one that gives the best coverage.

But we need to be careful because choosing a bundle that covers two disjoint intervals might be better than choosing one that covers a single interval.

We can use a greedy algorithm that always chooses the bundle that extends the covered region the furthest to the right, but also considers the left coverage? Actually, since we are scanning from left to right, we only care about covering the leftmost uncovered point. So we want to choose a bundle that covers cur and extends as far to the right as possible. But if we choose a bundle that covers two disjoint intervals, it might cover a point far to the right, but it might not cover the region immediately to the right of cur. So we need to consider both the immediate coverage and the far coverage.

We can think of it as: we have a current covered interval [1, cur-1]. We want to cover [cur, N]. We can choose a bundle that covers some part of [cur, N]. We want to minimize the number of bundles. This is similar to the problem of covering a line with intervals, but with the option to cover two disjoint intervals.

I recall that this problem can be solved by reducing to a minimum cost flow on a graph of intervals. Specifically, we can create a graph where nodes are the endpoints of the intervals, and edges represent possible coverings. But we need to incorporate the cost.

Another idea: Since the operations are independent, we can think of the problem as: we need to assign each operation to 0,1,2 such that the union covers [1,N]. This is a Boolean satisfiability problem. We can solve it with a SAT solver? But we need an efficient algorithm.

Given the time, I think we can solve it with a greedy algorithm that is optimal for this problem. Let's try to prove optimality.

We want to cover [1,N]. Consider the leftmost uncovered point x. We need to cover x. Any solution must use an operation that covers x. There are three types of operations that can cover x:
1. Operations with L_i <= x <= R_i. If we use such an operation, we must use it as type 1 (since type 2 would not cover x). So we use type 1, which covers [L_i,R_i]. This covers x and possibly points to the left (but left is already covered) and to the right up to R_i. So we cover up to R_i.
2. Operations with x < L_i. If we use such an operation, we can use it as type 2, which covers [1,L_i-1] and [R_i+1,N]. Since x < L_i, x is covered. This covers left up to L_i-1 (already covered) and right from R_i+1 to N. So it covers the right part from R_i+1 to N.
3. Operations with x > R_i. If we use such an operation, we can use it as type 2, which covers [R_i+1,N] and [1,L_i-1]. Since x > R_i, x is covered. This covers right from R_i+1 to N (so from x to N) and left from 1 to L_i-1 (already covered). So it covers the entire right part from x to N.

So if there is an operation of type 3, we can cover the entire right side in one operation. So we should always use a type 3 operation if available. So we can check: if there is an operation with R_i < x, we can use it as type 2 and finish. So we can finish in one operation.

Otherwise, we have no operation with R_i < x. So all operations have R_i >= x. Then we have two choices: use a type 1 operation (which covers up to R_i) or use a type 2 operation with L_i > x (which covers right from R_i+1 to N). Note that for type 2, since R_i >= x, the right part covered is [R_i+1, N], which leaves [x, R_i] uncovered. So using type 2 essentially reduces the right endpoint from N to R_i.

So we can think of it as: we have an interval [x, right] where right = N. We can either:
- Use a type 1 operation: move x to R_i+1 (where R_i is the maximum R_i among operations with L_i <= x <= R_i).
- Use a type 2 operation: move right to R_i (where R_i is the minimum R_i among operations with L_i > x).

We want to minimize the number of steps to reach x > right.

This is a problem of moving two pointers: x and right. We can move x to the right by using type 1 operations, or we can move right to the left by using type 2 operations. We want to minimize the number of moves.

We can solve this with a greedy algorithm that always chooses the move that gives the largest reduction in the distance (right - x). But we need to consider that moving x to the right might enable new type 2 operations (since L_i > x might become L_i <= x). Actually, as x increases, operations with L_i == x become available for type 1, and operations with L_i > x are available for type 2. Also, as x increases, operations with R_i < x become available for type 3 (finish). So we need to update the available sets.

We can maintain:
- maxR: the maximum R_i among operations with L_i <= x <= R_i.
- minR: the minimum R_i among operations with L_i > x.

We want to choose the move that minimizes the number of steps. This is like a shortest path problem. We can use a BFS on the state (x, right). But the state space is O(N^2). However, we can optimize because the transitions are monotonic.

We can use a greedy algorithm that always chooses the move that maximizes the progress. But we need to prove that it is optimal.

Consider the distance d = right - x. We want to reduce d to negative. At each step, we can either increase x by up to maxR - x + 1 (if we use type 1 with maxR), or decrease right by up to right - minR (if we use type 2 with minR). We want to minimize the number of steps.

This is similar to the problem of covering a line with intervals where you can also cover the complement. I think the optimal strategy is to always use the type 1 operation with the maximum R_i, because it covers the most to the right. But sometimes using a type 2 operation might be better because it reduces the right endpoint significantly, making the remaining interval smaller.

We can try to simulate the greedy algorithm: always use type 1 if possible, otherwise use type 2. But we need to handle the case where type 1 is not available (i.e., no operation with L_i <= x <= R_i). Then we must use type 2.

But is this optimal? Let's test on samples.

Sample 1: N=5, intervals: [2,4], [3,5], [1,4], [2,5].
Start x=1, right=5.
Available: 
Type 1: operations with L_i <=1 <= R_i: none (since min L_i=1, but [1,4] has L_i=1, R_i=4, so yes: [1,4] is type 1). So maxR=4.
Type 2: operations with L_i >1: [2,4], [3,5], [2,5]. minR among these: [2,4] has R_i=4, [3,5] has R_i=5, [2,5] has R_i=5. So minR=4.
Type 3: operations with R_i <1: none.
So we have type 1 available. Greedy: use type 1 with maxR=4. So use [1,4] as type 1. Then x becomes 5. Now x=5, right=5.
Update: 
Type 1: operations with L_i <=5 <= R_i: [3,5] (L=3,R=5), [2,5] (L=2,R=5). maxR=5.
Type 2: operations with L_i >5: none.
Type 3: operations with R_i <5: [2,4] (R=4), [1,4] (R=4). So type 3 available. So we can finish with type 3. Use [2,4] as type 2. Then we are done. Total operations: 2. This matches the sample output (but they used [2,4] as type 2 and [1,4] as type 1, same).

Sample 2: N=5, intervals: [1,3], [1,5], [2,4], [3,5].
Start x=1, right=5.
Type 1: [1,3], [1,5]. maxR=5.
Type 2: [2,4], [3,5]. minR=4 (from [2,4]).
Type 3: none.
Greedy: use type 1 with maxR=5. Use [1,5] as type 1. Then x=6 > right=5, done. Cost 1. Matches sample.

Sample 3: N=5, intervals: [1,3], [2,5].
Start x=1, right=5.
Type 1: [1,3]. maxR=3.
Type 2: [2,5]. minR=5.
Type 3: none.
Greedy: use type 1 with maxR=3. Use [1,3] as type 1. Then x=4, right=5.
Update: 
Type 1: operations with L_i <=4 <= R_i: [2,5] (L=2,R=5). maxR=5.
Type 2: none.
Type 3: none.
Now use type 1 with maxR=5. Use [2,5] as type 1. Then x=6 > right=5, done. Cost 2. Matches sample.

Sample 4: N=5, intervals: [1,3], [2,4].
Start x=1, right=5.
Type 1: [1,3]. maxR=3.
Type 2: [2,4]. minR=4.
Type 3: none.
Greedy: use type 1 with maxR=3. Use [1,3] as type 1. Then x=4, right=5.
Update:
Type 1: operations with L_i <=4 <= R_i: [2,4] (L=2,R=4). maxR=4.
Type 2: none.
Type 3: none.
Now use type 1 with maxR=4. Use [2,4] as type 1. Then x=5, right=5.
Update:
Type 1: operations with L_i <=5 <= R_i: none.
Type 2: none.
Type 3: operations with R_i <5: [1,3] (R=3), [2,4] (R=4). So type 3 available. Use one as type 2. Then we cover [R_i+1, N] = [4,5] or [5,5]. But we already covered up to x=5? Wait, after using [2,4] as type 1, x=5. So we have covered [1,4]. Now we need to cover 5. Type 3: use [1,3] as type 2, covers [4,5]? Actually, [1,3] type 2 covers [4,5]. So we cover 5. So we are done. But the sample says -1. Why? Because we used three operations: [1,3] type 1, [2,4] type 1, [1,3] type 2. But we can only use each operation once. We used [1,3] twice. So we cannot reuse operations. So the greedy algorithm must keep track of which operations are used. In the above, we used [1,3] as type 1, then later we tried to use it again as type 2. That's not allowed. So we need to ensure we don't reuse operations.

So the greedy algorithm needs to mark operations as used. In sample 4, after using [1,3] as type 1, it is used. Then we cannot use it again. So when we are at x=5, we have type 3 available from [2,4] (R=4). But [2,4] is already used as type 1. So no available type 3. So we are stuck. So the greedy algorithm should check if there is an unused operation in the set.

So we need to maintain sets of unused operations.

We can modify the greedy algorithm to always choose an unused operation. But we need to ensure that we don't get stuck.

We can use a priority queue for each set, and when we use an operation, we remove it from all sets.

Let's try to implement the greedy algorithm with unused operations.

We maintain:
- Set A: unused operations with L_i <= cur <= R_i. We want the one with max R_i.
- Set B: unused operations with L_i > cur. We want the one with min R_i.
- Set C: unused operations with R_i < cur. We can use any to finish.

We update these sets as cur increases. We need to efficiently move operations between sets.

We can sort operations by L_i and by R_i. We can use pointers to add operations to the appropriate sets as cur changes.

We can do:
Sort operations by L_i. Have an index idxL. For cur from 1 to N:
  While idxL < M and L[idxL] == cur:
    op = operations[idxL]
    if R_i >= cur: add to Set A
    else: add to Set C? Actually, if R_i < cur, then it's type 3. But we are at cur, so if R_i < cur, it should be in Set C. But we are adding when L_i == cur. If R_i < cur, then since L_i <= R_i, we have L_i <= R_i < cur, so L_i < cur. So this case doesn't happen when L_i == cur. So when L_i == cur, we have R_i >= cur. So we add to Set A.
  Also, we need to move operations from Set A to Set C when cur > R_i. So we can sort operations by R_i. Have an index idxR. While idxR < M and R[idxR] < cur:
    op = operations[idxR]
    if L_i <= cur: remove from Set A and add to Set C.
    else: add to Set B? Actually, if R_i < cur and L_i > cur, then it's in Set B? But if L_i > cur, then since L_i <= R_i, we have cur < L_i <= R_i, so R_i >= cur. So R_i < cur implies L_i <= cur. So if R_i < cur, then L_i <= cur. So it should be in Set A. So we move from Set A to Set C.
  Also, we need to move operations from Set B to Set A when cur reaches L_i. But we already handled that when L_i == cur. So Set B is operations with L_i > cur. We can maintain Set B as operations with L_i > cur. Initially, all operations are in Set B. When cur reaches L_i, we move from Set B to Set A (if R_i >= cur) or to Set C (if R_i < cur). But since L_i <= R_i, if L_i == cur, then R_i >= cur. So we move to Set A.

So we can do:
Initialize Set B with all operations.
For cur from 1 to N:
  Move operations with L_i == cur from Set B to Set A.
  Move operations with R_i == cur-1 from Set A to Set C.
  Then check:
    If Set C is non-empty, we can finish: pick any operation from Set C, use type 2, and we are done.
    Else, if Set A is non-empty, we can use type 1: pick the operation with max R_i from Set A, use type 1, and set cur = R_i+1.
    Else, if Set B is non-empty, we can use type 2: pick the operation with min R_i from Set B, use type 2, and set right = R_i (but we need to track right). Actually, using type 2 on Set B covers [R_i+1, N], so we reduce right to R_i. But we also need to cover [cur, R_i]. So we set right = R_i, and cur remains the same. But then we need to continue covering [cur, right]. So we need to loop with the same cur but reduced right.
    Else, no available operations: impossible.

But we need to track right. Initially right = N. When we use type 2 from Set B, we set right = R_i. Then we continue with the same cur but right = R_i. So we need to loop until cur > right.

We can implement this as a while loop: while cur <= right:
  update sets for cur
  if Set C non-empty: finish
  elif Set A non-empty: use type 1 with max R_i, cur = R_i+1
  elif Set B non-empty: use type 2 with min R_i, right = R_i
  else: impossible

But we need to be careful: when we use type 2 from Set B, we cover [R_i+1, N], so we set right = R_i. But we also need to cover [cur, R_i]. So we continue with the same cur. But note that after setting right = R_i, we might have cur > right? If R_i < cur, then we are done. But since we are in the case where Set C is empty, we have no operation with R_i < cur. So for Set B, we have L_i > cur, so R_i >= L_i > cur, so R_i > cur. So right = R_i > cur. So we continue.

We need to update the sets when right changes? Actually, the sets depend on cur and also on right? No, the sets are defined based on cur and the intervals. The condition for Set A is L_i <= cur <= R_i. This does not depend on right. Set B is L_i > cur. Set C is R_i < cur. So they only depend on cur. So when we change right, we don't need to update the sets. But we need to ensure that the operations we use are still available. When we use an operation, we remove it from the sets. So we need to remove it from Set A or Set B when we use it.

So the algorithm:
Initialize cur = 1, right = N.
Initialize Set B with all operations.
We need to efficiently get max R_i from Set A and min R_i from Set B. We can use priority queues: Set A as max-heap on R_i, Set B as min-heap on R_i. But we also need to remove operations when they are moved between sets. We can do this by storing the operations in the heaps and ignoring stale entries.

We also need to move operations from Set B to Set A when cur reaches L_i. We can do this by sorting operations by L_i. For each cur, we move all operations with L_i == cur from Set B to Set A. But we need to remove them from Set B. We can do this by popping from Set B until we find one with L_i == cur? But Set B is a heap on R_i, not on L_i. So we cannot efficiently find operations with L_i == cur. So we need a different data structure.

We can sort operations by L_i. Then we can iterate through them in order of L_i. For each cur, we add operations with L_i == cur to Set A. But we also need to remove them from Set B. Since Set B is a heap on R_i, we cannot remove specific elements. So we need to use