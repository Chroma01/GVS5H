
## ideation
**Core difficulty:**  
We have smoke that is advected by a known wind sequence S each integer time step, and new smoke is injected at the origin after the wind if it is empty. We need to know, for each half-integer time t+0.5 (i.e., just after the wind at step t), whether a particle exists at target cell (R,C).

**Key observations:**
- A particle that was generated at some integer time `k` (where `0 ≤ k < t`) will have been moved by all winds from time `k+1` up to `t`. The total displacement applied is the sum of the wind vectors from time `k+1` to `t`. If we define the prefix sum of wind vectors as `P[i] = sum_{j=1..i} v_j` (with `P[0] = (0,0)`), then a particle generated at time `k` ends up at position `P[t] - P[k]` after the wind at time `t` (and before the potential refill at time `t+1`? careful with indices).
- The times smoke exists: At time 0, smoke at (0,0). At each integer time t=1..N:
  1. wind blows (smoke moves according to S[t]),
  2. check if origin empty, if so add new smoke.
- We care about state immediately after the wind (time t+0.5). At that moment, the set of occupied cells is `{ P[t] - P[k] : k is a generation time ≤ t, and the smoke hasn't been "replaced"? }`. However, the generation rule: new smoke is added at origin only if there is no smoke at origin after the wind. This means that generation times are exactly the times `k` where the origin is empty after the wind at time k. But note: the check "if no smoke at (0,0) after wind" is performed after the wind. So generation time `k` is a time after wind at `k` where origin is empty.
- Alternatively, we can think of the process as: at each step, wind moves everything. Then we optionally add a new particle at origin. The set of particles is always finite? Actually, it could grow up to N+1. We need to track which "cohorts" (generation times) exist. Since each generation time corresponds to a particle that will be present forever after (it just moves), the set of positions at time t is the Minkowski sum of the set of generation times (as prefix sums) with the negative current wind displacement? Let's formalize.

**Formalization:**
Let `wind[1..N]` be the vector for each step. Let `pref[i] = sum_{j=1..i} wind[j]`. Let `pref[0] = (0,0)`.
At time 0 (before any wind), we have a particle at `pref[0] = (0,0)`.
At time t (after wind t, before refill t+1? careful with indexing):
Actually, the problem states: at time t (integer), wind blows, then if origin empty, new smoke generated. The time "t+0.5" is after the wind, before the refill (since refill happens at integer times, the half-integer is between integer and integer+1? Let's read carefully:
"At times t=1,2,...,N, the following happen in order:
- Wind blows, ...
- If there is no smoke in cell (0,0), new smoke is generated at cell (0,0).
We need to determine if smoke exists at cell (R,C) at time t+0.5"
So t+0.5 is after the wind at time t, but before the refill at time t? Wait, the events at time t happen in order: first wind, then possible refill. So at time t+0.5, we are after the wind but before the refill? Actually, the refill is instantaneous at time t (or after the wind). The phrase "at time t+0.5" likely means immediately after the wind and after the refill? Let's check sample.
In sample 1: N=6, R=-2, C=1, S=NNEEWS.
Let's simulate manually to see the pattern.
Time 0: smoke at (0,0).
Time 1: wind N: smoke moves to (-1,0). Then check origin: empty? Yes, so generate new smoke at (0,0). So after time 1, smoke at (-1,0) and (0,0).
Time 1.5: after time 1 events, so positions: (-1,0) and (0,0). Target (-2,1) not present.
Time 2: wind N: all smoke moves north. (-1,0)->(-2,0); (0,0)->(-1,0). Then check origin: empty? Yes (no smoke at (0,0)). So generate new at (0,0). So after time 2: smoke at (-2,0), (-1,0), (0,0).
Time 2.5: target (-2,1)? No, we have (-2,0), (-1,0), (0,0).
Time 3: wind E: all moves east. (-2,0)->(-2,1); (-1,0)->(-1,1); (0,0)->(0,1). Then check origin: empty? Yes. Generate new at (0,0). So after time 3: smoke at (-2,1), (-1,1), (0,1), (0,0).
Time 3.5: target (-2,1) is present! So output 1 for t=3. Sample output t=3 is 1? Output "001010": t=1:0, t=2:0, t=3:1, t=4:0, t=5:1, t=6:0. Yes.
So at time t+0.5, we consider the state after the wind AND after the refill (if any) of that time step? Wait, at time 3, after wind and refill, we have the new smoke at origin. So time 3.5 includes the refill at time 3. But the problem says "at time t+0.5". So t+0.5 is after all events of time t. So we want the set of particles that exist after the refill at time t.

**Alternative formulation using prefix sums of generation times:**
Let the set of generation times be G ⊆ {0, 1, ..., N}. At time 0, we have generation time 0 (initial smoke). At each integer time t from 1 to N, after the wind, we check if the origin is occupied. If not, we add t to G. But note: the check "is there smoke at (0,0) after wind" is equivalent to: does there exist a generation time k ∈ G such that after wind t, that particle is at (0,0)? The particle generated at time k will be at position P[t] - P[k] after wind t. So we need 0 = P[t] - P[k] => P[k] = P[t]. So the origin is occupied at time t (after wind) if and only if there exists a previous generation time k < t such that P[k] = P[t] (or k = t? but k is already in G, we are checking before adding t). So generation time t is added to G if P[t] is not in the set {P[k] : k ∈ G} (with k < t). This is exactly the condition that P[t] is a new prefix sum that hasn't appeared before among generation times.

Now, at time t (after refill), the set of particles is: for each k ∈ G with k ≤ t, position is P[t] - P[k]. (Because generation time k means it was added at time k, and has been moved by all winds from k+1 to t. If k = t, then P[t] - P[t] = 0, so it's at origin.)
So at time t+0.5, the positions are { P[t] - P[k] : k ∈ G, k ≤ t }.
We want to know if (R,C) is in this set. That is, does there exist k ∈ G with k ≤ t such that P[t] - P[k] = (R,C) => P[k] = P[t] - (R,C).
So the condition for output 1 at time t is: P[t] - (R,C) ∈ { P[k] : k ∈ G, k ≤ t }.
But note: k must be ≤ t. Since we are adding P[t] to G at the end of time t (if not already present), the set of P[k] for k ∈ G with k ≤ t is exactly the set of all P[k] for k ∈ G after processing time t. So we can maintain a set `prefix_set` of all P[k] for k that are generation times. Initially, prefix_set = {P[0]} = {(0,0)}. For each t from 1 to N:
1. Check if P[t] - (R,C) is in prefix_set. If yes, output '1', else '0'.
2. After that, we need to add P[t] to prefix_set if it is not already there (i.e., if P[t] is not in prefix_set). But wait, the condition for adding P[t] is exactly that origin was empty after wind t, which is equivalent to P[t] not in prefix_set (since origin occupied means some previous k with P[k] = P[t]). So we check: if P[t] not in prefix_set, then add it (this corresponds to generating new smoke at origin). And we output the query before that addition? Actually, the query for time t+0.5 uses the set of generation times up to and including t. So we must include P[t] in the set for the query if it was added. But we only add P[t] if it wasn't there. So the set of P[k] for k ∈ G, k ≤ t is: prefix_set after potentially adding P[t]. So the query should be: after updating the set? Let's check order.
At time t, the events are: wind, then maybe refill. The query at t+0.5 is after the refill. So the set G includes t if refill happened. So the condition is: P[t] - (R,C) ∈ { P[k] : k ∈ G, k ≤ t }.
So we should first compute P[t], then check if P[t] - (R,C) is in the current set of generation prefix sums (which does not include P[t] yet, because t is not yet in G). Wait, but if t is added to G, then the set for k ≤ t includes P[t]. So the set of P[k] for k ≤ t is the old set plus possibly P[t]. So we need to check if P[t] - (R,C) is in the old set OR equals P[t] (if we add P[t]). But P[t] - (R,C) = P[t] only if (R,C) = (0,0), which is given as false. So we only need to check if P[t] - (R,C) is in the old set (before adding P[t]). Because P[t] is not equal to P[t] - (R,C) for non-zero (R,C). So the order can be: compute P[t]; check if P[t] - (R,C) is in prefix_set; output result; then if P[t] not in prefix_set, add it.
Let's verify with sample 1.
S=NNEEWS, N=6, target (-2,1).
t=0: P[0]=(0,0), prefix_set={(0,0)}.
t=1: wind N => P[1]=( -1,0). Query: P[1] - (-2,1) = (1,-1). Is (1,-1) in prefix_set? No. Output 0. Check if P[1] in prefix_set? No, so add (-1,0). prefix_set={(0,0), (-1,0)}.
t=2: wind N => P[2]=(-2,0). Query: P[2] - (-2,1) = (0,-1). In set? No. Output 0. Add P[2] to set. prefix_set={(0,0), (-1,0), (-2,0)}.
t=3: wind E => P[3]=(-2,1). Query: P[3] - (-2,1) = (0,0). In set? Yes (0,0). Output 1. Check if P[3] in set? No, so add (-2,1). prefix_set={(0,0), (-1,0), (-2,0), (-2,1)}.
t=4: wind E => P[4]=(-2,2). Query: P[4] - (-2,1) = (0,1). In set? No. Output 0. Add P[4]? No, (-2,2) not in set. prefix_set adds (-2,2).
t=5: wind W => P[5]=(-2,1). Query: P[5] - (-2,1) = (0,0). In set? Yes. Output 1. Check if P[5] in set? Yes! P[5]=(-2,1) is already in set (from t=3). So we do NOT add it. prefix_set unchanged.
t=6: wind S => P[6]=(-1,1). Query: P[6] - (-2,1) = (1,0). In set? No. Output 0. Add P[6]? Yes. prefix_set adds (-1,1).
Outputs: 0,0,1,0,1,0. Matches sample.

So the algorithm is:
- Compute prefix sums P[0..N]. P[0]=(0,0). For i=1..N, P[i] = P[i-1] + vector(S[i]).
- Initialize a set `prefix_set` with P[0] = (0,0).
- For t=1..N:
  - target_offset = (P[t].r - R, P[t].c - C).
  - if target_offset in prefix_set: output '1', else '0'.
  - if P[t] not in prefix_set: add P[t] to prefix_set.

We need to store pairs (r,c) in a hash set. N up to 200k, coordinates are within [-N, N], so we can use a tuple or a single integer by shifting (e.g., r * (2N+1) + (c+N)). Since N up to 2e5, (2N+1) up to 4e5, product up to ~8e10, fits in 64-bit integer. Using Python's built-in set of tuples is fine for 200k.

**Pitfalls:**
- Off-by-one on times: The problem asks for time t+0.5 for t=1..N. Our simulation uses integer t as the step index. The query at step t corresponds to the state after the wind and refill at time t, which is exactly time t+0.5? Wait, in our manual simulation, t=1 gave the state after wind 1 and refill 1, and we output for t=1.5. So yes, t in the loop is the step index, and we output for that step.
- (R,C) != (0,0) guaranteed, so we don't need to handle the case where target is origin (though the algorithm would naturally work even if it were, but it's not needed).
- The set might grow up to N+1 elements. Python set operations are O(1) average.
- We need to read N, R, C, and string S. S is length N.
- The wind directions: N: (-1,0), S: (1,0), W: (0,-1), E: (0,1). Note that row increases downward? The problem says: "cell (r,c) is drawn: -r cells up if r<0, r cells down if r>=0". This is just a description; our coordinate system can be standard. So N: r-1, S: r+1, W: c-1, E: c+1. The sample: target (-2,1) with S=NNEEWS. We got correct results with N: r-1, E: c+1, W: c-1, S: r+1. Let's verify: P[0]=(0,0). N: (-1,0). So P[1]=(-1,0). Correct.
- The query condition: P[t] - (R,C) = (P[t].r - R, P[t].c - C). In sample, R=-2, C=1. So P[3]=(-2,1). P[3] - (-2,1) = (0,0). Yes.

**Complexity:** O(N) time, O(N) space.

## worker: Implement the solution in Python: read inputs, ite
The solution uses the observation that a smoke particle generated at time `k` (where generation times are exactly the times when the prefix sum of wind vectors is new) will be at position `P[t] - P[k]` at time `t+0.5`. We maintain a set of all `P[k]` for generation times `k`. For each step, we check whether `P[t] - (R,C)` is in this set, which directly tells us if smoke exists at the target. We then add `P[t]` to the set if it wasn't already there (simulating the refill). This runs in O(N) time and uses O(N) space.
