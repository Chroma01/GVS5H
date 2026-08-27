
## ideation
Core difficulty: N up to 200k, so we need O(N) or O(N log N). The smoke set can grow to O(N) cells, but we only need to answer whether (R,C) is occupied at each half-integer time, plus know whether (0,0) is empty at each half-integer time (to decide generation).

Key insight: every smoke particle is born at (0,0) at some integer time b (b=0 initial, or b≥1 generated at time b if (0,0) empty at time b-0.5... careful: generation happens at time t after wind, i.e., the new smoke exists at time t+0.5). A particle born at time b occupies, at time t+0.5 (t ≥ b), position = sum of wind vectors for steps b+1..t = P[t] - P[b], where P is prefix displacement (P[0]=(0,0)).

So smoke at (R,C) at time t+0.5 iff there exists a birth time b ∈ B (set of birth times, 0 ≤ b ≤ t) with P[t] - P[b] = (R,C), i.e., P[b] = P[t] - (R,C).

Birth rule: at time t (after wind), if no smoke at (0,0), generate. Smoke at (0,0) at time t+0.5 (before generation) iff ∃ b ∈ B, b ≤ t-... wait: at time t+0.5 after wind step t, particles present are those born at b ≤ t-1? No: wind step t moves all smoke present at time (t-1)+0.5. Particles born at time b exist from time b+0.5 onward... Actually generation at time t happens after wind at time t, so a particle generated at time t is first present at time t+0.5, and it does NOT move during wind step t. So a particle born at time b (b=0 initial, present at time 0.5? Let's check: at t=0 smoke at (0,0). Wind step 1 moves it. So initial particle is present at time 0+0.5? The problem says at time t=0 smoke exists only at (0,0). Queries are at t+0.5 for t≥1. Initial particle born at b=0: at time t+0.5 it's at P[t] - P[0] = P[t]. Good, consistent with formula P[t]-P[b] for b=0.

For b ≥ 1: generated at time b after wind step b, present at time b+0.5 at (0,0). At time t+0.5 (t ≥ b), it has been moved by wind steps b+1..t, so position = P[t] - P[b]. Consistent.

Generation condition at time t: "If there is no smoke in cell (0,0)" — checked after wind at time t, i.e., the state at time t+0.5 before generation. Smoke at (0,0) then iff ∃ b ∈ B with b < t (b ≤ t-1... actually b can equal t? No, births at time t happen after this check) such that P[t] - P[b] = (0,0), i.e., P[b] = P[t], with b < t. Also b=0 counts.

So algorithm: iterate t from 1..N. Maintain set of birth-time prefix positions: we need, for the target query, whether ∃ b ∈ B, b ≤ t (for query at t+0.5, births at time t are included since generation happens before t+0.5) with P[b] = P[t] - (R,C). And for generation at time t: whether ∃ b ∈ B, b ≤ t-1 (i.e., added before processing time t) with P[b] = P[t].

Order of operations at each t:
1. Compute P[t] from S[t-1].
2. Check generation: is there a birth b (already in set, b ≤ t-1) with P[b] = P[t]? If not, add t to B (birth at time t).
3. Answer query: is there b ∈ B (now including possibly t) with P[b] = P[t] - (R,C)?

Wait, careful with step 2: the check "no smoke at (0,0)" uses births b with b ≤ t-1, positions P[t]-P[b]. Since all births b < t are in our set before step 2, checking membership of P[t] in the set of P[b] values is correct. If empty, birth at time t: add P[t] to set (birth time b=t has P[b]=P[t]).

Step 3: query uses births b ≤ t, i.e., set after step 2. Check membership of P[t]-(R,C).

Edge: initial birth b=0, P[0]=(0,0), add to set before loop.

This is O(N) with a hash set. Positions are integer pairs bounded by N.

Pitfalls:
- Order: generation check must use set before adding time-t birth; query uses set after.
- The query target P[t]-(R,C): smoke at (R,C) iff P[b] = P[t] - (R,C). Yes.
- (R,C) ≠ (0,0) guaranteed, but algorithm works regardless.
- Use sys.stdin, fast I/O. Store set of tuples or encoded integers (r*(2N+1)+c offset) for speed. N=200k, tuples fine in Python but encoding to int is faster: encode (r,c) as (r+ N) * (2N+3) + (c + N) or use (r << 32) ^ c style. Simpler: (r, c) tuples in a set — 200k ops, fine.

Let me verify with sample 1 mentally: N=6, R=-2,C=1, S=NNEEWS.
Directions: N=(-1,0), E=(0,1), W=(0,-1), S=(1,0).
P[0]=(0,0). Set={(0,0)}.
t=1: N → P[1]=(-1,0). Gen check: (-1,0) in set? No → birth at 1, add (-1,0). Query: P[1]-(R,C)=(-1-(-2),0-1)=(1,-1). In set? No → 0. ✓ (expected 0)
t=2: N → P[2]=(-2,0). Gen: (-2,0) in set? No → add. Query: (-2+2,0-1)=(0,-1)? Wait P[2]-(R,C) = (-2-(-2), 0-1) = (0,-1). In set? No → 0 ✓.
t=3: E → P[3]=(-2,1). Gen: in set? No → add. Query: (-2+2,1-1)=(0,0). In set? Yes → 1 ✓.
t=4: E → P[4]=(-2,2). Gen: no → add. Query: (0,1). In set? No → 0 ✓.
t=5: W → P[5]=(-2,1). Gen: (-2,1) in set? Yes (added at t=3) → no birth. Query: (0,0) in set? Yes → 1 ✓.
t=6: S → P[6]=(-1,1). Gen: in set? No → add. Query: (1,0). In set? No → 0 ✓.
Output: 001010 ✓ matches.

Great, algorithm confirmed.

## worker: Implement the final Python solution: parse input, 
- Every smoke particle is born at (0,0) at some integer time b (b=0 initial, or generated at time b). At time t+0.5 it sits at P[t] − P[b], where P is the prefix wind displacement.
- Generation at time t happens iff no existing birth b (< t) satisfies P[b] = P[t]; if none, add birth at time t (its prefix position is P[t]).
- Query at t+0.5 (after generation) asks whether any birth b (≤ t) has P[b] = P[t] − (R,C).
- Order per step: update P[t], do generation membership check/add, then answer query. Verified against sample 1 by hand (produces 001010). O(N) time with a hash set of tuple positions.
