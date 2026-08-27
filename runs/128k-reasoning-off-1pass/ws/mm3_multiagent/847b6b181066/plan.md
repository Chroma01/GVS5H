We need to determine, for each time t (1..N), whether smoke exists at (R,C) at time t+0.5, i.e., after the wind at time t has moved the smoke, and after possibly regenerating smoke at (0,0) if empty.

Key observation: At any time t+0.5, the set of cells containing smoke consists of the cell (0,0) (always regenerated if empty after the move) plus all cells that originally started at (0,0) and have been shifted by a contiguous suffix of the wind directions up to time t. Specifically, after t steps, smoke occupies the origin plus all positions reachable by applying the last k moves (1 ≤ k ≤ t) starting from (0,0). The origin itself is always present at t+0.5 because after the move, if origin is empty, it is regenerated; even if the move would have left smoke at origin, the rule says "if there is no smoke" (after move) then generate, so origin is always filled at half-integer times.

So at time t+0.5, the occupied cells are: (0,0) and all cells obtained by following the wind directions S[t], S[t-1], ..., S[1] (i.e., the reversed suffix) from (0,0). Wait, careful: At time t+0.5, we have applied the t-th wind. The smoke that has been moving for j steps (1 ≤ j ≤ t) follows the last j moves: moves at times t, t-1, ..., t-j+1. So the set is the union of paths formed by prefixes of the reversed string S_rev[t..N]? Actually it's the union of all prefixes of the sequence of moves up to time t, but in reverse order of application. More concretely, define prefix of length k: apply moves S[1], S[2], ..., S[k] in order, ending at position P_k. At time t+0.5, for each k=1..t, the smoke that started at time 0 and has survived k steps is at position P_k. However, there is also the regeneration: after each wind, if origin empty, new smoke is added. So at time t+0.5, we have:
- Smoke from original that has been moving for exactly t steps: at P_t.
- Smoke generated at time 1 (after move 1) if origin was empty after move 1: that smoke then moves for t-1 steps, ending at position after applying S[2..t] (which is P_t - S[1] in vector terms, or equivalently starting from origin and applying S[2..t]).
- In general, at time t+0.5, the set of positions is the union of:
   { (0,0) }  (since origin is always regenerated after each move if empty)
 ∪ { P_k : 1 ≤ k ≤ t }   (positions after k steps from start)
but careful: after the move at time t, we check if origin empty; if so regenerate. The regenerated smoke at time t+ (just after move) will be at origin, and it hasn't moved yet. At time t+0.5 (which is after regeneration but before next move), the set includes:
- The regenerated smoke at origin (if origin was empty after move t, which it is unless some smoke is at origin after move t).
- Plus all the moving smokes that have been moving for various durations.

But importantly, at time t+0.5, the set of occupied cells is exactly the set of all positions reachable by applying some suffix of the moves S[1..t] starting from (0,0). That is, for each k from 0 to t (where k=0 means no moves, i.e., just (0,0)), the position after applying the last k moves in order (S[t-k+1] ... S[t])? Let's check.

Actually, the smoke that has been moving for exactly t steps (original) is at position P_t = S[1]+...+S[t] (vector sum). The smoke generated after the first move (at time 1.5) will be at origin, then it gets moved by moves 2..t, ending at position P_t - S[1] (i.e., applying moves S[2..t] from origin). In general, smoke generated after move j (1 ≤ j ≤ t) will be at origin just after move j, then gets moved by moves j+1..t, ending at position sum_{i=j+1..t} S[i] = P_t - P_j. So the set of positions at time t+0.5 is:
- (0,0) (the smoke generated at time t if origin was empty after move t, but actually it is always present at t+0.5 because if it was occupied, it's still there; if empty, it's regenerated. So origin is always in the set).
- { P_t - P_j : 0 ≤ j ≤ t-1 }? Wait, j from 1 to t gives positions P_t - P_j (for smoke generated after move j). But also P_t itself is included (original smoke). And origin corresponds to j=t? Actually if generated after move t (i.e., at time t.5), it is at origin, and hasn't moved yet, so it is origin. That corresponds to j=t, giving P_t - P_t = (0,0). So the set is { P_t - P_j : 0 ≤ j ≤ t } where we define P_0 = (0,0). So the set of positions is exactly the set of partial sums from the end: the set of vectors P_t - P_j for j=0..t. Equivalently, it's the set of all points that can be reached by starting at (0,0) and applying some suffix of the move sequence (the last k moves for k=0..t). Because P_t - P_{t-k} = sum_{i=t-k+1..t} S[i]. So the set is { sum_{i=t-k+1..t} S[i] : k=0..t } (with k=0 giving empty sum = (0,0)).

Thus at time t+0.5, the smoke positions are exactly the set of all suffix sums of the prefix S[1..t] (including the empty suffix giving (0,0)). So we need to check if (R,C) belongs to that set.

Therefore, for each t, we need to know if (R,C) equals the sum of some suffix of S[1..t]. That is, does there exist k (0 ≤ k ≤ t) such that sum_{i=t-k+1..t} S[i] = (R,C)?

We can precompute the prefix sums of the entire string: let P[i] be the sum of S[1..i] (as a 2D vector), with P[0]=(0,0). Then the suffix sum of length k ending at t is P[t] - P[t-k]. So we need to check if there exists k in [0,t] such that P[t] - P[t-k] = (R,C). Equivalently, P[t-k] = P[t] - (R,C). Let target = P[t] - (R,C). We need to check if target is equal to some P[j] where j = t-k, and j ranges from 0 to t. So for each t, we need to know if the value P[t] - (R,C) appears in the set {P[0], P[1], ..., P[t]}. Note that P[t] - (R,C) is a known point for each t.

So the problem reduces to: for each t=1..N, let Q_t = P[t] - (R,C). Check if Q_t is in the set of prefix sums up to index t (including P[0]).

We can process t from 1 to N, maintaining a set (hash set) of prefix sums encountered so far (P[0] through P[t-1]?), and for each t, we check if Q_t is in that set. Wait, careful: The condition is existence of j in [0,t] such that P[j] = P[t] - (R,C). At time t, we have already computed P[t]. The set of available P[j] for j=0..t includes P[t] itself. So we should include P[t] in the set before checking? Actually, for k=0, we have j=t, so P[t] - P[t] = (0,0). That would require (R,C) = (0,0), but given (R,C) != (0,0), k=0 is not a solution. So we don't need to consider j=t unless (R,C)=(0,0). Since it's given that (R,C) != (0,0), we only need to check j from 0 to t-1. But it's easier to include all j from 0 to t, and the answer for k=0 would only be true if (R,C)=(0,0) which is not the case. So we can just include all prefix sums up to t, and for each t, check if P[t] - (R,C) is in the set of prefix sums from 0 to t. If yes, output 1, else 0.

But we need to be careful: The set of prefix sums up to t includes P[t] itself. But if P[t] - (R,C) = P[t], that would imply (R,C)=(0,0), which is false. So it doesn't matter. So we can just maintain a set of all prefix sums encountered so far, initially containing P[0]=(0,0). For each t from 1 to N, we compute P[t] = P[t-1] + move(S[t]). Then we check if P[t] - (R,C) is in the set. After that, we add P[t] to the set.

But wait: At time t+0.5, the set of positions is the set of suffix sums of S[1..t]. That includes the empty suffix (0,0) and all non-empty suffixes. So we need to check if (R,C) is in that set. The condition is: there exists k in [0,t] such that sum_{i=t-k+1..t} S[i] = (R,C). This is equivalent to: there exists j in [0,t] such that P[t] - P[j] = (R,C), i.e., P[j] = P[t] - (R,C). So indeed, we need to check if P[t] - (R,C) is in the set {P[0], P[1], ..., P[t]}. Since P[t] itself is in the set only if (R,C)=(0,0), we can just check if P[t] - (R,C) is in the set of all prefix sums up to t. We can maintain a set of all prefix sums as we iterate.

However, we must be careful: The set at time t should be the set of prefix sums up to t, not just up to t-1. So we need to add P[t] to the set after checking, or before checking? If we add P[t] before checking, then we are checking against the set {P[0],...,P[t]}. That's correct. But if we add after, we are checking against {P[0],...,P[t-1]}. That would miss the possibility of j=t, but as argued, j=t only works if (R,C)=(0,0). So either way is fine for the given condition (R,C) != (0,0). But to be precise, we should include P[t] in the set for the check, because the condition includes j=t. So we can either:
- First add P[t] to the set, then check if P[t] - (R,C) is in the set.
- Or check first, then add.
Since (R,C) != (0,0), P[t] - (R,C) = P[t] would imply (R,C)=(0,0) so it's not an issue. But to avoid any off-by-one, we can do: for each t, compute P[t], then check if P[t] - (R,C) is in the set (which currently contains P[0]..P[t-1]), then add P[t] to the set. This is safe because if P[t] - (R,C) equals P[t], it would be false anyway, so it doesn't matter that we haven't added P[t] yet. So we can do check before adding.

Thus algorithm:
- Read N, R, C, and string S.
- Map characters to vectors: N: (-1,0), W: (0,-1), S: (1,0), E: (0,1).
- Initialize set with (0,0) (as a tuple or complex number).
- Initialize current position (r,c) = (0,0).
- For t from 1 to N:
   - Update current position according to S[t-1] (0-indexed).
   - Compute target = (current_r - R, current_c - C).
   - If target is in the set, output '1', else '0'.
   - Add current position to the set.
- Print the resulting string.

This is O(N) time and O(N) space (set size up to N+1). N up to 200,000, so that's fine.

Let's test on sample 1:
N=6, R=-2, C=1, S=NNEEWS.
t=1: move N: r=-1, c=0. target = (-1 - (-2), 0 - 1) = (1, -1). Set contains (0,0). Not in set -> 0. Add (-1,0).
t=2: move N: r=-2, c=0. target = (-2+2, 0-1) = (0, -1). Set: (0,0), (-1,0). Not in set -> 0. Add (-2,0).
t=3: move E: r=-2, c=1. target = (-2+2, 1-1) = (0,0). Set contains (0,0) -> 1. Add (-2,1).
t=4: move E: r=-2, c=2. target = (-2+2, 2-1) = (0,1). Set: (0,0), (-1,0), (-2,0), (-2,1). Not in set -> 0. Add (-2,2).
t=5: move W: r=-2, c=1. target = (-2+2, 1-1) = (0,0). Set contains (0,0) -> 1. Add (-2,1) (already there).
t=6: move S: r=-1, c=1. target = (-1+2, 1-1) = (1,0). Set does not contain (1,0) -> 0. Add (-1,1).
Output: 001010. Matches sample.

Sample 2: Should match.

We need to be careful with the set representation. Since coordinates are within -N..N, we can use tuples or complex numbers. Using complex numbers might be faster and simpler: a + bj. But tuples are fine.

Edge cases: (R,C) might be unreachable? That's fine.

Thus the plan is solid.