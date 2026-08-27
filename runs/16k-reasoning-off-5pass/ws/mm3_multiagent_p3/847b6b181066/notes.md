
## ideation
The problem asks for, at each half-integer time t+0.5 (t=1..N), whether the target cell (R,C) contains smoke.

**Key observations:**
- At time 0, smoke exists only at (0,0) (the campfire).
- At each integer time t=1..N, two things happen in order:
  1. Wind moves *all* existing smoke by one cell according to the t-th character of S.
  2. If (0,0) is empty after the wind (but before generation? The statement says "If there is no smoke in cell (0,0), new smoke is generated at cell (0,0)."—since wind just moved all smoke, the new puff is created after the wind at time t+0.5), a new puff is generated at (0,0).
- The question asks about time t+0.5, which is *after* the wind at time t and after any potential new puff at (0,0) for time t. So we need to know the state of smoke at half-integer times.

**Modeling with offsets:**
Instead of tracking absolute positions of all smoke puffs (which can be huge), we can track the campfire's position relative to the target.
- Let `offset = (R, C) - campfire_pos` (i.e., vector from campfire to target).
- Initially, campfire is at (0,0), so offset = (R, C).
- When wind blows, all smoke moves by wind_dir. So the campfire's smoke moves too, but a *new* campfire is effectively "at" the same physical cell (0,0) after wind? Wait—careful: the campfire itself is fixed at (0,0). The smoke that was at the campfire moves away with the wind. Then if (0,0) is empty, a new puff is placed at (0,0).
- So the physical campfire position never moves; it's always at (0,0). The smoke puffs (including the original one) move with the wind.
- If we want to know if target (R,C) has smoke at time t+0.5, we can ask: is there a puff that started at some time s (0 ≤ s ≤ t) and has been moved by the total wind displacement from time s+1 to time t? The puff generated at time s (at the campfire (0,0)) will be at position equal to the net displacement of winds from s+1 to t.

**Alternative formulation (relative tracking):**
Let `campfire_offset` = the position of the campfire relative to itself? No.
Better: Think of the target cell (R,C) as fixed. After each wind, the *entire smoke field* shifts by the wind direction. So relative to the target, the campfire (which is fixed at (0,0) in absolute coordinates) stays at (0,0) in absolute coordinates, but the smoke that was at (0,0) moves away.

Actually, let's reframe:
- At time t+0.5, smoke exists at absolute position p if there was a generation event at some time s ≤ t (where s=0 means initial smoke at (0,0) at time 0.5? Wait—initial smoke is at (0,0) at time 0. At time 0.5, no wind has happened yet, so the initial smoke is still at (0,0). Then at time 1, wind blows, moving it. So the initial smoke is treated as generated at time 0, and winds from t=1 to t move it.

So a puff generated at time s (0 ≤ s ≤ N) is at absolute position:
- (0,0) if s = t (just generated, hasn't moved yet)
- sum of wind directions from time max(s+1, 1) to t, if s < t

But this is complex. Let's use the offset idea properly.

**Offset approach (from the plan):**
- We maintain the position of the campfire *as seen from the target*? Or rather: we maintain the current displacement of the smoke field.
- Actually, since all smoke moves identically with each wind, we can think of the smoke field as being "shifted" by the wind each step. A puff generated at time s will have been shifted by the sum of winds from s+1 to current time t.
- But the campfire is fixed at (0,0). So after a sequence of winds, the physical position of a puff generated at time s is (sum of winds from s+1 to t).

We want to know if (R,C) is occupied at time t+0.5. That means: is there some s ≤ t such that (R,C) = (sum of winds from s+1 to t) (with the convention that for s=t, the sum is 0, meaning the puff is still at (0,0))?

Equivalently, is (R,C) equal to the negative of the sum of winds from 1 to t, plus the sum of winds from 1 to s? That is, is (R,C) = (sum of winds from 1 to s) - (sum of winds from 1 to t)? Hmm, let's check:
- Position at time t+0.5 of puff generated at s: 
  - If s = 0: sum of winds from 1 to t.
  - If s ≥ 1: sum of winds from s+1 to t.
  - If s = t: 0 (just generated at (0,0)).
- We can unify: Let prefix_wind[0] = (0,0). prefix_wind[k] = sum of winds from 1 to k.
  - For s=0: position = prefix_wind[t] - prefix_wind[0] = prefix_wind[t].
  - For s ≥ 1: position = prefix_wind[t] - prefix_wind[s].
  - For s = t: position = prefix_wind[t] - prefix_wind[t] = 0. ✓
- So position = prefix_wind[t] - prefix_wind[s] for s = 0,1,...,t.
- We want to know if (R,C) equals this for some s.
- That is, is (R,C) = prefix_wind[t] - prefix_wind[s] for some s ∈ {0,1,...,t}?
- Equivalently, is prefix_wind[s] = prefix_wind[t] - (R,C) for some s?
- Let target_prefix = prefix_wind[t] - (R,C). We need to check if target_prefix has appeared in the set {prefix_wind[0], prefix_wind[1], ..., prefix_wind[t]}.

But wait! There's the condition about generating new smoke: a new puff is generated at time t only if the campfire (0,0) was empty at time t-0.5. 
- At time t-0.5, the campfire (0,0) is occupied iff there exists some s ≤ t-1 such that (0,0) = prefix_wind[t-1] - prefix_wind[s].
- Equivalently, is prefix_wind[s] = prefix_wind[t-1] for some s ∈ {0,1,...,t-1}?
- So the new puff at time t is generated iff prefix_wind[t-1] is NOT in the set {prefix_wind[0], ..., prefix_wind[t-2]}. (Note: s can be t-1, so we need to exclude that? Wait, s can be t-1: then the puff generated at t-1 is at position prefix_wind[t-1] - prefix_wind[t-1] = 0. So yes, s=t-1 is valid. The set of prefix_wind for s=0..t-1 includes prefix_wind[t-1] from s=t-1. So the condition is: prefix_wind[t-1] is unique among prefix_wind[0..t-1] for the campfire to be empty? No, wait.)

Let me re-derive carefully:
- A puff at position (0,0) at time t-0.5 exists iff there is some s ∈ {0,1,...,t-1} such that the puff generated at s is at (0,0) at time t-0.5.
- Puff generated at s is at position prefix_wind[t-1] - prefix_wind[s] at time t-0.5.
- Set this to (0,0): prefix_wind[s] = prefix_wind[t-1].
- So the campfire is occupied at time t-0.5 iff prefix_wind[t-1] appears in the multiset {prefix_wind[0], prefix_wind[1], ..., prefix_wind[t-1]}.
- Since prefix_wind[t-1] is one of them (when s=t-1), it's always there! Wait, that means the campfire is always occupied at time t-0.5 for t ≥ 1? That can't be right because the problem says new smoke is generated only if empty.

Let's check: s ranges from 0 to t-1 inclusive. s=t-1 gives prefix_wind[t-1] - prefix_wind[t-1] = 0. So yes, the puff generated at time t-1 is at (0,0) at time t-0.5? No! Wait, the puff generated at time t-1 was generated at time t-1, which is after the wind at time t-1. So at time t-0.5, which is after generation at t-1 and before wind at t, the puff is at (0,0). So yes, there is always a puff at (0,0) at time t-0.5 (the one just generated at t-1, or the initial one if t-1=0). So the condition "if there is no smoke at (0,0)" would never be true, and no new smoke would ever be generated after t=0? That contradicts the problem statement and examples.

Let me re-read the problem carefully:
"At times t=1,2,...,N, the following happen in order:
- Wind blows, and all the smoke present at that time moves...
- If there is no smoke in cell (0,0), new smoke is generated at cell (0,0)."

At time t, the wind blows first. Then we check if (0,0) is empty and generate if so.
At time t+0.5 (which is the state after the above two steps at time t), we want to know if (R,C) has smoke.

So the sequence is:
- Time 0: smoke at (0,0).
- For t=1 to N:
  - Wind: all smoke moves.
  - Check (0,0): if empty, generate smoke at (0,0).
- Then we ask about time t+0.5, which is after these two steps.

So at time t+0.5, the set of smoke positions is:
- The initial smoke (generated effectively at "time 0") has been moved by winds 1 through t.
- Plus any new puffs generated at times 1,2,...,t, which have been moved by winds (generation_time+1) through t.

Now, when is (0,0) empty at the check time (after wind, before generation at time t)?
- After wind at time t, the smoke positions are those from time t-0.5 moved by wind t.
- The smoke at (0,0) at time t-0.5 was either:
  - The initial smoke (if it has been moved to (0,0) by winds 1..t-1).
  - A puff generated at some time s (1 ≤ s ≤ t-1) and moved by winds s+1..t-1.
- Specifically, a puff is at (0,0) at time t-0.5 iff prefix_wind[t-1] - prefix_wind[s] = (0,0), i.e., prefix_wind[s] = prefix_wind[t-1], for some s ∈ {0,1,...,t-1}.
- As noted, s=t-1 gives prefix_wind[t-1] = prefix_wind[t-1], so the puff generated at time t-1 is at (0,0) at time t-0.5? Wait, when was the puff at time t-1 generated? It was generated after the wind at time t-1. So at time t-0.5, the puff generated at time t-1 has not yet been moved by wind t. So it sits at (0,0). So yes, (0,0) is always occupied at time t-0.5 for t ≥ 1. Then no new smoke is ever generated? That seems wrong.

Let's check with the sample.
Sample 1: N=6, R=-2, C=1, S=NNEEWS.
Let's manually simulate:
- t=0: smoke at (0,0). [Time 0.5]
- t=1: wind N. Smoke moves to (-1,0). (0,0) is now empty. Generate new smoke at (0,0). So at time 1.5: smoke at (-1,0) and (0,0).
- t=2: wind N. Smoke at (-2,0) and (-1,0). (0,0) empty. Generate at (0,0). Time 2.5: (-2,0), (-1,0), (0,0).
- t=3: wind E. Smoke moves: (-2,1), (-1,1), (0,1). (0,0) empty. Generate at (0,0). Time 3.5: (-2,1), (-1,1), (0,1), (0,0).
- t=4: wind E. Smoke: (-2,2), (-1,2), (0,2), (0,1). (0,0) empty. Generate at (0,0). Time 4.5: (-2,2), (-1,2), (0,2), (0,1), (0,0).
- t=5: wind W. Smoke: (-2,1), (-1,1), (0,1), (0,0), (0,-1). (0,0) has smoke! (the one generated at t=4). So NO generation at t=5. Time 5.5: (-2,1), (-1,1), (0,1), (0,0), (0,-1).
- t=6: wind S. Smoke: (-1,1), (0,1), (1,1), (1,0), (1,-1). (0,0) empty? Let's see: the puff at (0,0) at time 5.5 was generated at t=4, moved by wind 5 (W) to (0,-1), then by wind 6 (S) to (1,-1). So no puff at (0,0). Generate new at (0,0). Time 6.5: (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,0).

Target (R,C) = (-2,1).
- t=1.5: positions: (-1,0), (0,0). No. Output 0.
- t=2.5: (-2,0), (-1,0), (0,0). No. Output 0.
- t=3.5: (-2,1), (-1,1), (0,1), (0,0). Yes. Output 1.
- t=4.5: (-2,2), (-1,2), (0,2), (0,1), (0,0). No. Output 0.
- t=5.5: (-2,1), (-1,1), (0,1), (0,0), (0,-1). Yes. Output 1.
- t=6.5: (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,0). No. Output 0.
Result: 001010. Matches sample!

So my earlier reasoning was wrong. The puff generated at time t-1 is NOT at (0,0) at time t-0.5. Why? Because at time t-1, the wind blows, then the puff is generated. So at time (t-1)+0.5, there is a puff at (0,0). Then at time t, the wind blows, moving that puff away. So at time t-0.5 (which is after wind t), the puff generated at t-1 is no longer at (0,0); it has been moved by wind t.

Ah! I confused the time indices. Let's clarify:
- Let state at time k+0.5 be after all processing at integer time k (for k ≥ 1) or initial state for k=0.
- At time 0.5: smoke at (0,0) [initial].
- For t = 1 to N:
  - Start with state at time (t-1)+0.5.
  - Wind blows: all smoke moves according to S[t]. Now we are at time t (integer).
  - Check (0,0): if empty, generate smoke. Now we are at time t+0.5.
- The question asks for state at time t+0.5 for t=1..N.

So for t=1..N, we want state after wind t and possibly generation at t.

Now, at time (t-1)+0.5, the puffs are those generated at times 0, 1, ..., t-1.
At time t+0.5, after wind t and generation at t, the puffs are:
- Those from time (t-1)+0.5 moved by wind t.
- Plus a new puff at (0,0) if (0,0) was empty after wind t.

So a puff generated at time s (where 0 ≤ s ≤ t) at time t+0.5 is at position:
- If s = t: (0,0) (just generated).
- If s < t: it was at some position at (t-1)+0.5, then moved by wind t.
- Position at (t-1)+0.5 of puff generated at s:
  - If s = 0: sum of winds 1..t-1.
  - If 1 ≤ s ≤ t-1: sum of winds s+1..t-1.
- So position at t+0.5:
  - If s = t: (0,0).
  - If s = 0: sum of winds 1..t.
  - If 1 ≤ s ≤ t-1: sum of winds s+1..t.

Using prefix_wind[k] = sum of winds 1..k (with prefix_wind[0] = (0,0)):
- s = t: position = 0 = prefix_wind[t] - prefix_wind[t].
- s = 0: position = prefix_wind[t].
- s (1 ≤ s ≤ t-1): position = prefix_wind[t] - prefix_wind[s].

So position = prefix_wind[t] - prefix_wind[s] for s = 0, 1, ..., t.
We want to know if (R,C) equals this for some s.

**Condition for generation at time t:**
A new puff is generated at time t if (0,0) is empty after wind t.
After wind t, the smoke from time (t-1)+0.5 is at positions prefix_wind[t] - prefix_wind[s] for s = 0, 1, ..., t-1.
(0,0) is empty after wind t iff (0,0) is not among these, i.e., prefix_wind[t] - prefix_wind[s] ≠ (0,0) for all s = 0..t-1.
That is, prefix_wind[s] ≠ prefix_wind[t] for all s = 0..t-1.
Equivalently, prefix_wind[t] is a new value not seen in prefix_wind[0..t-1].

**Algorithm:**
1. Compute prefix_wind[t] for t=0..N. (O(N))
2. We need to know, for each t=1..N, whether (R,C) is in the set of positions of puffs at time t+0.5.
   The set of positions is {prefix_wind[t] - prefix_wind[s] : s = 0..t} if generation happened at t, or s = 0..t-1 if not.
   But we can think of it as: the set of available s values is {0, 1, ..., t-1} plus possibly t if generation happens.
   However, we can just maintain a set of "available offsets" relative to the current prefix.
   Actually, the set of positions at time t+0.5 is prefix_wind[t] - S_t, where S_t is the set of prefix_wind values s for which a puff exists.
   Initially (time 0.5), S_0 = {prefix_wind[0]} = {(0,0)}. The smoke is at prefix_wind[0] - prefix_wind[0] = (0,0). ✓
   At time t+0.5, after processing, S_t = {prefix_wind[s] : s = 0..t} ∩ "generation conditions". Actually, the puff at s exists if it was generated and hasn't been "removed". But puffs never disappear; they just move. So a puff generated at s always exists. The only question is whether a puff is generated at t.
   So S_t = {prefix_wind[0], prefix_wind[1], ..., prefix_wind[t]} if generation happens at t, else {prefix_wind[0], ..., prefix_wind[t-1]}.
   But wait: if generation does NOT happen at t, then prefix_wind[t] is not in S_t, so the set of positions is prefix_wind[t] - S_t.
   We want to know if (R,C) ∈ prefix_wind[t] - S_t, i.e., if prefix_wind[t] - (R,C) ∈ S_t.
   Let target_prefix = prefix_wind[t] - (R,C). We need to check if target_prefix ∈ S_t.

   S_t consists of:
   - All prefix_wind[i] for i = 0..t-1 (always).
   - Plus prefix_wind[t] if generation happened at t (i.e., if prefix_wind[t] was not already in the set {prefix_wind[0..t-1]}).

   So we can maintain a set `seen` of prefix_wind values that have been "generated" (i.e., correspond to existing puffs).
   At time 0.5, seen = {prefix_wind[0]}.
   For t = 1..N:
     - After wind t, the positions are prefix_wind[t] - seen.
     - Check if (0,0) is in these positions: (0,0) = prefix_wind[t] - p for some p ∈ seen. This is equivalent to prefix_wind[t] ∈ seen.
     - If prefix_wind[t] ∉ seen, then generate: add prefix_wind[t] to seen.
     - Now, the target (R,C) is occupied at time t+0.5 iff (R,C) = prefix_wind[t] - p for some p ∈ seen.
     - That is, p = prefix_wind[t] - (R,C).
     - So we just need to check if prefix_wind[t] - (R,C) ∈ seen.

   This matches the plan exactly!

**Implementation details:**
- prefix_wind[t] can be large, but we only care about it relative to target.
- We can store seen as a set of tuples or complex numbers or strings. Since coordinates range from -N to N, we can use strings like "r,c" or just tuples.
- At each step t, we update the current position (r, c) by adding the wind direction.
- We check if (r - R, c - C) is in seen. (Because prefix_wind[t] - (R,C) = (r, c) - (R, C) = (r-R, c-C).)
- Then check if (r, c) is in seen. If not, add (r, c) to seen and record '1' for generation? Actually, we just need to add to seen if not present.
- Output '1' if (r-R, c-C) ∈ seen, else '0'.

Let's verify with sample 1:
S = NNEEWS
Winds: N=(−1,0), N=(−1,0), E=(0,1), E=(0,1), W=(0,−1), S=(1,0).
R=-2, C=1. Target offset from current pos: we need (r - (-2), c - 1) = (r+2, c-1) in seen? Wait, target_prefix = prefix_wind[t] - (R,C) = (r, c) - (R, C) = (r - (-2), c - 1) = (r+2, c-1).
Let's compute:
t=0: pos=(0,0). seen={(0,0)}.
t=1: pos=(-1,0). Check target: (-1+2, 0-1) = (1, -1) ∈ seen? No. Check generation: (-1,0) ∈ seen? No -> add (-1,0). seen={(0,0),(-1,0)}. Output 0.
t=2: pos=(-2,0). Check target: (0, -1) ∈ seen? No. Generation: (-2,0) ∉ seen -> add. seen={(0,0),(-1,0),(-2,0)}. Output 0.
t=3: pos=(-2,1). Check target: (0, 0) ∈ seen? Yes! Output 1. Generation: (-2,1) ∉ seen -> add. seen={(0,0),(-1,0),(-2,0),(-2,1)}.
t=4: pos=(-2,2). Check target: (0, 1) ∈ seen? No. Generation: (-2,2) ∉ seen -> add. seen={...,(-2,2)}. Output 0.
t=5: pos=(-2,1). Check target: (0, 0) ∈ seen? Yes! Output 1. Generation: (-2,1) ∈ seen -> do not add.
t=6: pos=(-1,1). Check target: (1, 0) ∈ seen? No. Generation: (-1,1) ∉ seen -> add. seen={...,(-1,1)}. Output 0.
Result: 001010. Matches!

**Complexity:**
- O(N) time, O(N) space for the set.
- N up to 200,000, so easily fits.

**Pitfalls:**
- The condition for generation: if current pos is already in seen, do not add. This happens when the wind brings the smoke back to a previously visited prefix.
- The target check uses the current pos minus (R, C), not plus.
- The set seen should be updated only when generation happens.
- Use appropriate data structures for set of pairs in Python. Tuples are fine. Or we can use a single integer by encoding as (r+N)*2N + (c+N) or something, but tuples are fine for 200k elements.

**Final check on interpretation:**
The problem says "determine if smoke exists at cell (R,C) at time t+0.5". This is after the wind at time t and after any generation at time t. Our algorithm checks the set after generation (or not). The set seen contains prefix positions of all puffs that exist. At time t+0.5, the puffs are at positions current_pos - p for all p in seen. So target is occupied iff current_pos - target is in seen. Correct.

**One more check:**
At t=1, we check if (0,0) was empty after wind 1. After wind 1, the initial smoke is at (-1,0). So (0,0) is empty, so we generate. Our algorithm: current_pos = (-1,0). Is (-1,0) in seen? Initially seen={(0,0)}. No, so we add. Then for target, check if (-1,0) - (-2,1) = (1,-1) in seen? No. So output 0. At t=1.5, smoke is at (-1,0) and (0,0). Target (-2,1) is not there. Correct.

At t=3, after wind E, pos=(-2,1). seen contains (0,0), (-1,0), (-2,0). Is (-2,1) in seen? No, so we add it. Then for target, check if (-2,1) - (-2,1) = (0,0) in seen? Yes. Output 1. At t=3.5, smoke is at positions: current_pos - p = (-2,1) - p for p in seen.
- p=(0,0): (-2,1) ← target!
- p=(-1,0): (-1,1)
- p=(-2,0): (0,1)
- p=(-2,1): (0,0)
So yes, target has smoke. Correct.

At t=5, pos=(-2,1) again. seen now includes (0,0), (-1,0), (-2,0), (-2,1), (-2,2). Check target: (-2,1) - (-2,1) = (0,0) ∈ seen? Yes. Output 1. Check generation: (-2,1) ∈ seen? Yes! So do not add. This matches the manual simulation where no new smoke was generated at t=5 because the puff generated at t=4 was still at (0,0) after wind 5? Wait, at t=5 wind W: the puff at (0,0) at t=4.5 was generated at t=4, moved by wind 5 (W) to (0,-1). So (0,0) is empty after wind 5? No, in the manual simulation I said (0,0) has smoke at t=5.5 (the one generated at t=4). Let me re-check manual sim:
t=4.5: smoke at (-2,2), (-1,2), (0,2), (0,1), (0,0). The one at (0,0) was generated at t=4.
t=5: wind W. The smoke moves west: (-2,1), (-1,1), (0,1), (0,0), (0,-1). So the puff generated at t=4 moves to (0,-1)? No, the puff at (0,0) moves to (0,-1). But there was also a puff at (0,1) which moves to (0,0). So after wind, there is a puff at (0,0) (the one that was at (0,1) at t=4.5). That one was generated at t=2? Let's trace: t=2 generated at (0,0), moved by t=3 (E) to (0,1), t=4 (E) to (0,2)? No, wait.
At t=2.5: puffs at (-2,0), (-1,0), (0,0). The (0,0) is from t=2 generation.
t=3: wind E. (-2,0)→(-2,1), (-1,0)→(-1,1), (0,0)→(0,1). Generate at (0,0). So t=3.5: (-2,1), (-1,1), (0,1), (0,0).
t=4: wind E. (-2,1)→(-2,2), (-1,1)→(-1,2), (0,1)→(0,2), (0,0)→(0,1). Generate at (0,0). So t=4.5: (-2,2), (-1,2), (0,2), (0,1), (0,0).
t=5: wind W. (-2,2)→(-2,1), (-1,2)→(-1,1), (0,2)→(0,1), (0,1)→(0,0), (0,0)→(0,-1). So after wind, we have (-2,1), (-1,1), (0,1), (0,0), (0,-1). So (0,0) is occupied! The puff there is the one that was at (0,1) at t=4.5, which was generated at t=2 (moved by E, E, W). So indeed, (0,0) is occupied, so no new generation at t=5.
In our algorithm: at t=5, pos=(-2,1). seen contains prefix positions of all puffs generated so far. At t=4, we added (-2,2) to seen. But what about the puff generated at t=2? Its prefix is (-2,0). The puff generated at t=2 is at (-2,0) in the prefix space. At t=4.5, its position is current_pos - p = (-2,2) - (-2,0) = (0,2). At t=5.5, after wind, its position is (-2,1) - (-2,0) = (0,1)? Wait, current_pos at t=5 is (-2,1). The position is current_pos - prefix. For p=(-2,0), position = (-2,1) - (-2,0) = (0,1). That's not (0,0). The puff at (0,0) at t=5.5 is the one that was at (0,1) at t=4.5. Which puff was that? At t=4.5, position (0,1) = current_pos - p = (-2,2) - p => p = (-2,1). That is the puff generated at t=3! At t=3, prefix was (-2,1). Yes, we added (-2,1) to seen at t=3. So at t=5, seen contains (-2,1). So current_pos = (-2,1) is in seen. Therefore, we do NOT generate. This matches! And the target check: current_pos - target = (-2,1) - (-2,1) = (0,0). Is (0,0) in seen? Yes, from t=0. So output 1. Perfect.

The algorithm is solid.

**Implementation in Python:**
```python
import sys
input = sys.stdin.readline

def solve():
    N, R, C = map(int, input().split())
    S = input().strip()

## worker: Implement the solution in Python using the prefix-
The solution uses a prefix-wind tracking approach:
- `cr, cc` represents the cumulative wind displacement (prefix_wind) from time 0 to current time.
- `seen` stores all prefix positions that correspond to generated smoke puffs.
- A new puff is generated at time t if the campfire (0,0) is empty after wind t, which happens exactly when the current prefix position is not already in `seen`.
- The target cell (R,C) is occupied at time t+0.5 iff there exists a puff with prefix position `p` such that `current_pos - p = (R,C)`, i.e., `p = (cr-R, cc-C)`. So we check if `(cr-R, cc-C)` is in `seen`.
- The algorithm runs in O(N) time with O(N) space for the set, easily handling N up to 200,000.
