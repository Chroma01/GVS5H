We need to transform `caption` into a "good caption": every character must appear in contiguous runs of length ≥ 3. Allowed operations: for each position `i`, we may increment or decrement the character (cost = 1 per change) any number of times. We want minimum total operations, and among all minimal-cost solutions, return the lexicographically smallest result string; if impossible, return `""`.

Key insight (similar to classic "string to good string with min changes" problem):
- For a fixed target character `c` (in 'a'..'z'), we can compute the minimum cost to convert the whole string into only `c`'s, where `c` appears in groups of size ≥ 3 (so positions that stay not-`c` are deleted, but we can still fill them with other chars — yet in optimal solutions the result is usually single character repeated, or a few blocks).
- However, because the problem allows arbitrary alphabet change per step, an optimal solution is either:
  1. Convert to a single character repeated `n` times (all same letter) — feasible iff `n % 3 == 0` (since one run of length `n` must be ≥ 3; actually any `n ≥ 3` works for a single-char caption). Cost = sum of distances from each position to that char.
  2. Convert to two characters forming two blocks (each block length ≥ 3) — feasible iff `n ≥ 6` and we split into two valid lengths (3+3, 3+4, ...).
  3. Convert to three characters (3+3+3 minimal), etc. But in practice, for `n ≤ 5·10^4`, evaluating all splits is O(n^2 · alphabet) which is too heavy.

Better approach: dynamic programming with cost precomputation per character.

Precompute `cost[i][c] = |ord(caption[i]) - ord(c)` for each position `i` and char `c` (size `n × 26`). This is O(26·n) time/space.

DP state: `dp[i][k][c]` = minimum cost to make positions `[0..i-1]` into a good caption where the last block ends at `i-1`, has character `c`, and length `k` (where `1 ≤ k ≤ 3`, because once a block has length ≥ 3, we can finalize it; we only need to track up to length 3 since we can transition to a new character any time after length 3).

Transitions for position `i` (0-indexed) with char `c`:
- Start new block at `i`: cost = `cost[i][c] + dp[i-1][*][other_chars finalized]` → we need a way to query min cost of any previous finalized block. Maintain `best[i]` = min over all finalized states at position `i`.
- Extend existing block: if `k ≥ 1`, we extend the same char `c` from previous state: `new_dp[i][k+1][c] = min(new_dp[i][k+1][c], dp[i-1][k][c] + cost[i][c])`.
- Finalize a block of length 3 (i.e., when `k == 3`, this is now a valid run, contribute to `best[i]`): we finalize, so this run is "done" and next char can be anything new.

Algorithm:
1. Build `cost[i][c]` for all `i, c`.
2. Initialize `dp` for `i = 0` (first char): for each `c`, `dp[0][1][c] = cost[0][c]`. Also set `best[0] = min over c of dp[0][1][c]`.
3. For each `i` from 1 to `n-1`:
   - For each `c` in 'a'..'z':
     - Start new block: `start_cost = best[i-1] + cost[i][c]`
     - Extend from previous same char: for `k in [1,2]`, if `dp[i-1][k][c]` exists, `new_dp[i][k+1][c] = dp[i-1][k][c] + cost[i][c]`
     - Also carry over length-1 from previous same char to length-2, etc.
   - After processing, finalize: for any `c, k==3`, `best[i] = min(best[i], new_dp[i][3][c])`. Also `best[i] = min(best[i], start costs)`. Actually `best[i]` is the minimum over all "completed up to i" states.
4. Answer is `best[n-1]`. If infinite, return `""`.

But we also need to **reconstruct the lexicographically smallest result string** among those achieving `best[n-1]`. So we need to store predecessor info (parent pointer) and do a tie-breaking rule that prefers lexicographically smaller final string.

Tie-breaking during DP:
- When we have two ways to achieve the same `dp[i][k][c]` cost, we keep the one whose resulting string (up to position `i` with this state) is lexicographically smaller.
- However, this depends on the rest of the string; a greedy local choice may not yield global lex-smallest. We need a more careful approach.

Alternative: compute the minimum cost, then do a second pass to reconstruct the lexicographically smallest string given that minimum cost. This is the standard "lex smallest among min cost" reconstruction.

Reconstruction (greedy left-to-right):
- Maintain `dp` and `parent` info, plus `best[i]` as defined.
- For each position `i` from 0 to `n-1`, and for each `c`, we know the cost to reach state `(i, k, c)`. We also know `best_after[i][c]` = minimum cost to complete positions `[i+1..n-1]` given that the current block is character `c` with current length `k`. We can precompute this with backward DP too.

Actually, to get lex smallest, we can:
- Compute forward DP storing `dp_fwd[i][k][c]` and `best_fwd[i]` (min cost to end exactly at `i` with all blocks completed up to `i`).
- Compute backward DP `dp_bwd[i][k][c]` = min cost to convert positions `[i..n-1]` into a good caption where the block starting at `i` has character `c` and length `k` (k=1,2,3 meaning "we are k-th char of a new block of c").

Then total cost for a particular reconstruction is `best_fwd[i-1] + dp_fwd_transition_at_i + dp_bwd[i+block_len][...]`, etc. But for simplicity, since we only have small state (k up to 3, 26 chars), we can store `parent` and during reconstruction try characters from 'a' to 'z' and pick the smallest feasible.

Simpler: since `n` is 5e4 and alphabet 26, we can store full DP tables. Use two arrays:
- `dp_prev[c][k]` (for position `i-1`) and `dp_curr[c][k]` (for position `i`).
- Also `best_prev = min over all "finalized" states at position `i-1`. A state is "finalized" if its last block has length ≥ 3, OR we are at the end of string (only the last block must be ≥ 3 at the very end). We can track `best_prev` = minimum cost to have a fully good prefix `[0..i-1]`.

Reconstruction strategy:
- After computing `best[n-1]` (min cost for full string), we walk from `i=0` to `n-1`.
- At position `i`, we try each character `c` from 'a' to 'z':
  - We need to determine the minimum cost path that goes through `c` at position `i` (with some block length `k`), such that total cost = `best[n-1]`.
  - Since the alphabet is only 26, we can do this efficiently: precompute `dp[i][k][c]` and also `suffix_best[i][c][k]` (min cost to finalize the rest given we are at state `(i,k,c)`).
  - Then at each step, iterate `c` from 'a' to 'z', and for valid `k` (compatible with previous block choice), check if `best_prev + cost_to_reach(i,k,c) + suffix_best[i+1][...] == best[n-1]`. Pick the smallest `c` that works, fix it, update state (which `c`, which `k`), update `best_prev` accordingly, and move on.

State during reconstruction: we need to know the current block's character and length (k=1,2). When `k=3`, the block completes and we reset `k=0` (no current block, ready to start new). We also need to know the cost so far.

To make this efficient:
- `dp[i][k][c]` = min cost to make prefix `[0..i-1]` valid and currently being in a block of char `c` with length `k` (where `k=1,2,3`, and `k=3` means the block just completed at `i-1` — but then it's "finalized" state). Actually let's define:
  - `dp[i][c][k]`: minimum cost for prefix `[0..i]` such that positions `[0..i-1]` form a good caption (all completed blocks ≥ 3) and position `i` is the start of a new block of char `c` with current length `k` (`k=1` since it's a new start). Wait, this is getting confusing.

Let me redefine cleanly:

Let `dp[i][c][t]` = minimum cost to convert `caption[0..i]` such that:
- The whole string up to position `i` consists of some completed blocks (each length ≥ 3), and
- The last block (which is ongoing) has character `c` and current length `t` (where `t = 1, 2, or 3+`).
- For "completed" prefix states (i.e., the last block is done), we can think of them as finalized. But since we always need blocks of length ≥ 3, we can only "finalize" when `t ≥ 3`.

Simplify: track `dp[i][c][t]` for `t = 1, 2, 3`. When `t = 3`, the block is "complete" and next character must start a new block. So `best[i]` = `min over c of dp[i][c][3]`. (At the very end `i = n-1`, the answer is `best[n-1]`.)

Transitions at position `i` (for char `c`):
- Start new block at `i` (length 1): `dp[i][c][1] = min over c' (if c' ≠ c or after a completed block)`. Specifically, we can start new block of `c` if the previous state's block was either:
  - Completed (length 3) of any char `c'`, or
  - This is the very first position (`i = 0`).
  So `dp[i][c][1] = best[i-1] + cost[i][c]`.
- Extend: if `t = 1` or `t = 2` and same char, `dp[i][c][t+1] = min(dp[i][c][t+1], dp[i-1][c][t] + cost[i][c])`.

Finalize: when `t = 3` at position `i`, that block is done. `best[i] = min(best[i], dp[i][c][3])` over all `c`.

This DP is O(n × 26 × 3) = O(78n), which is fine for `n = 5e4`.

We also need `parent` pointers to reconstruct:
- For each `dp[i][c][t]`, store the previous state's `(c_prev, t_prev)` that gave the minimum. If ties, choose the one leading to lex smaller final string. But we don't know the future yet.

So we do **two passes**:
1. Forward pass: compute `dp[i][c][t]` and `best[i]`. Also store `parent[i][c][t]` = `(c_prev, t_prev)` (or a sentinel for "start"). This gives us the minimum cost.
2. Backward pass (reconstruction): knowing the target total cost `target = best[n-1]`, we walk from `i = 0` to `n-1`. At each step, we have a current state `(c_cur, t_cur)` and accumulated cost `acc`. We try to extend or finalize, picking the smallest possible next character that can still achieve `target`.

Actually for reconstruction, since alphabet is only 26, we can do a greedy left-to-right pass trying each character. At position `i`, we are in some state (either at start of a new block, or continuing). We need to decide what character `caption[i]` becomes. We iterate `c` from 'a' to 'z':
- Determine the cost if we set position `i` to `c` and transition to state `(c, t_new)`.
- Check if there's a path from this new state to the end with total cost = `target`.
- The "remaining cost from new state" can be precomputed with a backward DP: `rem[i][c][t]` = minimum cost to convert positions `[i..n-1]` into a good caption given that position `i` starts/continues a block of char `c` with length `t` (where `t` is the length of this block including position `i`).

Let me define `rem[i][c][t]` = min cost for suffix `[i..n-1]` where position `i` is the `t`-th character of a block of `c` (so `t ≥ 1`), and the rest forms a good caption. When `t = 3`, the block is "just completed" and we still need to handle `[i+1..n-1]` as a new good caption (starting fresh).

Transitions for `rem` (backward, from `i = n-1` down to `0`):
- Base case `i = n-1`: for each `c`, `rem[n-1][c][1] = cost[n-1][c]`. (The single char forms a block of length 1, but it must reach length 3, so this is only valid if `n == 1`? Actually no, at the last position we need the block to be completed. Hmm.)

Wait, the DP is tricky because the last block must also have length ≥ 3. So we need to ensure the final block completes before/at the end of the string.

Let's redefine to handle this cleanly. A "state" is always "in the middle of a block" or "between blocks". Let's say:
- State A: "between blocks" (previous block completed). This is the start state.
- State B(c, t): "inside a block of char c, currently at length t" where t ∈ {1, 2}. When t reaches 3, we transition back to State A.

So at any position, we are either in State A (ready to start a new block) or State B(c, t) (continuing a block). The DP tracks cost so far.

Forward DP:
- `dp[i][state]` = min cost for prefix `[0..i]` ending in `state`.
- States: 1 (A) + 26×2 (B(c,1), B(c,2)) = 53 states.

Transitions from position `i-1` to `i` (adding position `i` with target char choice `c`):
- From A: go to B(c, 1) with cost `dp[i-1][A] + cost[i][c]`.
- From B(c', 1) where `c' == c`: go to B(c, 2) with cost `dp[i-1][B(c,1)] + cost[i][c]`.
- From B(c', 2) where `c' == c`: go to A with cost `dp[i-1][B(c,2)] + cost[i][c]`. (Block of c completes at position i, with total length 3.)
- From B(c', 1) where `c' != c`: this is invalid (can't switch char mid-block).
- From B(c', 2) where `c' != c`: invalid.

State A at position i means: prefix `[0..i]` is fully good (all completed blocks of length 3), and we're ready to start a new block at position `i+1`.

At the end, `i = n-1`, the valid final state is A (all blocks completed). So `answer_cost = dp[n-1][A]`.

Reconstruction:
- At each position `i` (from 0 to n-1), we have a current state (A or B(c, t)). We choose target char `c` for position `i`:
  - If state is A: we can start B(c, 1) for any c. Cost increment = `cost[i][c]`. New state = B(c, 1).
  - If state is B(c', t) with `t ∈ {1, 2}`: we must keep `c'`. Cost increment = `cost[i][c']`. New state = B(c', t+1) (if t+1 == 3, new state is A).

Wait, so during reconstruction the character is forced by the state if we're mid-block! That means the character at position `i` is determined by the state. So we don't have freedom to choose character during reconstruction if we're mid-block.

Hmm, but we want lex smallest. So we need to choose the **sequence of block characters** (c1, c2, c3, ...) such that total cost is minimized, and among those, the resulting string is lex smallest.

The block characters determine the string entirely. The string is: block1_char × 3 + block2_char × 3 + ... (with possible longer blocks). But in our DP, blocks are exactly length 3 (we only track up to t=2, and at t=3 we finalize). However, what if a block has length > 3? The DP allows extending: if t=3 (state A), we can start a new block of same char? No, the transition from A to B(c,1) allows any c, including the same as the just-finished block. So effectively, two adjacent blocks of the same char would just merge into one block of length 6. The DP naturally handles this: we could go A → B(c,1) → B(c,2) → A → B(c,1) → B(c,2) → A, giving ccccc c (length 6), or A → B(c,1) → B(c,2) → A → B(c,1) → ... 

But there's no direct "extend a completed block" transition. The string "cccccc" (6 c's) would be represented as two blocks of c of length 3 each, which is fine. So the resulting string is always a sequence of length-3 blocks (possibly more if we have A → B(c,1) → B(c,2) → A repeated). So the string is uniquely determined by the sequence of block characters (each block of length 3). Wait, but what if n is not a multiple of 3? Then the last block must have length 3, 4, 5, or 6? 

The constraint is every character appears in groups of ≥ 3. So the last block can be longer than 3. But our DP forces all blocks to be exactly 3? Let's see: in the DP, we finalize at t=3, and then start a new block. But we could also "not finalize" and keep extending. However, the state A is the only "between blocks" state, and the only way to reach A is via B(c, 2) → A. So blocks are always exactly length 3 in this DP.

But the problem allows blocks of length > 3! E.g., "aaaaaa" (6 a's) is a good caption. Our DP would represent it as two blocks of "aaa" and "aaa", which is also valid (every char in groups of ≥ 3). The string is the same. So the resulting string is always a concatenation of length-3 blocks. But the number of blocks is `n / 3` if `n % 3 == 0`, else we can't have all blocks of length 3 if n is not a multiple of 3.

Wait! If `n = 4`, can we have a good caption? "aaaa" — yes, it's a single block of length 4 ≥ 3. But our DP would require blocks of length 3 each. So "aaa" + "a" (incomplete block) is invalid, and "aaaa" (one block of 4) can't be represented. So the DP as described forces `n` to be a multiple of 3.

This is a problem! We need to allow the last block (and any block) to be of length > 3. The transition should allow: from B(c, 2) (length 2), we can either finalize (go to A) or extend to B(c, 3+)? But "3+" is unbounded.

Alternative: since we only need to track whether a block has length ≥ 3, once it reaches length 3, it's "complete" but we can choose to continue the same character (which would make a longer block, but that's equivalent to two adjacent blocks of the same char). Wait, no! If we have a block of length 3 of char c, and we extend to length 4, the characters are cccc. But in the final string, it's just cccc. If we instead "finalize" the block of 3 c's and start a new block of c of length 1 (and then extend to 4), the resulting string is cccc. Same thing.

So any string where each character run has length ≥ 3 can be decomposed into blocks of length 3 (with possibly the last block longer). But wait, the decomposition into length-3 blocks is not unique if blocks can be longer. E.g., "cccccc" (6 c's) can be "ccc" + "ccc" or "ccc" + "ccc" (same). What about "aaabbbccc"? "aaa"+"bbb"+"ccc" (three blocks of 3). 

But for "aaaa" (4 a's), we can't decompose into length-3 blocks. "aaa" + "a" is invalid (last block too short). "a" + "aaa" same. So the DP as stated (forcing block length exactly 3) only handles `n` divisible by 3.

To fix: allow the last block (and any block) to be of any length ≥ 3. The simplest way: we only finalize when necessary. Let's redefine:
- State B(c, t) for t = 1, 2, 3+ where "3+" means length ≥ 3 but we don't care exactly.
- From B(c, 2), we can go to B(c, 3+) with cost `cost[i][c]`.
- From B(c, 3+), we can stay in B(c, 3+) with cost `cost[i][c]` (i.e., extend further).
- From B(c, 3+), we can "finalize" to A at any time, but we only finalize when the next char is different or at end. Actually, in the final string, a "block" of length L ≥ 3 of char c is represented as: B(c,1) → B(c,2) → B(c,3+) → ... → B(c,L). The final state is B(c, L) which is "3+".

So the final state should allow B(c, 3+) (length ≥ 3, exact length not tracked). Transitions:
- A → B(c, 1): cost `cost[i][c]`.
- B(c, 1) → B(c, 2): cost `cost[i][c]`.
- B(c, 2) → B(c, 3+): cost `cost[i][c]`. (Block becomes "long enough", i.e., ≥ 3)
- B(c, 3+) → B(c, 3+): cost `cost[i][c]`. (Continue same char)
- B(c, 3+) → A: no cost (block is done, we're between blocks). But we need to be careful: we only go to A when we want to start a new block of a different char. But actually, we can always "finalize" the current block. However, if the next char in the reconstruction is the same, we wouldn't finalize. So in the DP, we need to consider both possibilities: either continue in B(c, 3+) or finalize to A. But once in B(c, 3+), we can stay there forever (for the same char). And we can also jump to A (meaning the block ends here).

But the state A means "previous block is done and we can start any new char". The transition B(c, 3+) → A means the block of c ends at position i-1, and position i starts something new (or i is past the end).

Actually, the cleanest formulation: we have a "run-length" encoding. The string is a sequence of runs (c1^L1, c2^L2, ..., ck^Lk) with each Li ≥ 3. The DP needs to find the optimal sequence of (c_j, L_j).

This is the "minimum cost to partition string into good runs" problem. The number of runs can be up to n/3.

For each possible run length L (from 3 to n), the cost of making `caption[i..i+L-1]` all equal to char c is `sum_{j=i}^{i+L-1} |ord(caption[j]) - ord(c)|`. If we precompute prefix sums for each character, we can compute this in O(1) per (i, L, c). Then the problem becomes: partition [0..n-1] into intervals of length ≥ 3, minimizing total cost (where cost of interval [i, j] with char c is the sum). This is a standard DP: `dp[j] = min over i ≤ j-3 and c of (dp[i] + cost(i, j, c))`, where `dp[-1] = 0`. Answer is `dp[n-1]`, or `inf` if impossible.

For reconstruction, we need to find the lex smallest string among optimal partitions. This DP is O(n^2 × 26) which is too slow for n=5e4.

So we need the original O(n × 26) DP with blocks of length exactly 3, and somehow handle the remainder.

Wait, I recall a similar problem (LeetCode "Minimum Cost to Make String Good" or similar). The solution indeed uses DP with states tracking run length up to 3, and the answer is the min cost over all possible "last run" configurations. Let me think again.

If `n % 3 != 0`, we can't have all runs of length 3. But we can have runs of length 3, 4, 5, etc. The key insight: for any run of length L > 3, we can split it into a run of 3 and a run of L-3. So the cost is the same. But wait, if L-3 < 3, we can't. So L can be 3, 4, 5, 6, 7, ... and splitting L into 3 + (L-3) only works if L-3 ≥ 3, i.e., L ≥ 6. For L=4 or L=5, we can't split into valid runs.

So the DP must handle runs of length 3, 4, 5, 6, ... up to n.

But the problem reduces to: for each position i (start of a run), we choose char c and length L (3 ≤ L ≤ n-i), pay cost(i, L, c), and add dp[i]. Then dp[j] = min.

For efficiency, we note that the cost function `cost(i, L, c)` is additive in L: `cost(i, L+1, c) = cost(i, L, c) + |ord(caption[i+L]) - ord(c)|`. This allows us to do DP with "sliding window" or just process runs incrementally.

The standard solution for this type of problem (LeetCode 3250 or similar?) uses DP with state (position, last_char, run_length_mod?). 

Let me reconsider the state machine approach. We want to allow runs of any length ≥ 3. We can model it as:
- States based on the current run's char and length modulo something? No, because we need length ≥ 3 to "finalize", but once length ≥ 3, we can continue indefinitely (the run can be arbitrarily long). 

So the states are: (in a run of char c, length t) for t = 1, 2, 3+. We have 26 × 3 states = 78 states. The "3+" state means length ≥ 3, and we can either continue (stay in 3+ with same char) or end the run (go to state A, meaning ready to start a new run).

Transitions at position i (0-indexed) with target char `c_i` (the character we set position i to):
- From A: → B(c_i, 1). Cost = `cost[i][c_i]`.
- From B(c, 1): → B(c, 2). Cost = `cost[i][c]`.
- From B(c, 2): → B(c, 3+). Cost = `cost[i][c]`.
- From B(c, 3+): → B(c, 3+). Cost = `cost[i][c]`. (Extend)
- From B(c, 3+): → A. Cost = 0? No, the cost of position i was already paid when we entered B(c, 3+). The transition B(c, 3+) → A means "end the run here" (position i is the last char of the run). So no additional cost for position i. But then position i+1 will start a new run.

Wait, this is getting confusing. Let me re-index: when we are at position i, we decide what char to put there. So the cost is incurred at position i. The state after processing position i reflects the status.

Let's define:
- After processing position i (i.e., we've decided chars for 0..i), the state is either:
  - A: all runs so far are complete (last run ended at some position ≤ i, and we're between runs, but actually since we just processed i, "between runs" means the last run ended at i). Hmm, A means "the run containing position i is complete". If the run has length ≥ 3 and ends at i, then after i we're "ready for next run". But position i+1 hasn't been processed yet.
  
Let me re-define: state after processing position i represents the status of the run containing i (or that i is the end of a run).

State: (c, t) where c is the char of the current run and t is the length of the run so far (t = 1, 2, or 3+). Additionally, we need to know if the run is "active" (i.e., position i is part of it). And we need to handle the "between runs" case, but that's just t = 3+ and we choose to end it.

Actually, the state space is: we are building a run. The run's character is c, and its current length is t. For t = 1, 2, the run is not yet "good" (length < 3). For t = 3+, the run is "good" (length ≥ 3). At any point when t = 3+, we can either continue the run (t becomes 4+, still 3+) or end the run (move to a new run of a different char, or if it's the end of string, we just need t ≥ 3).

So states: (c, t) with t ∈ {1, 2, 3+}, c ∈ 26 letters. Total 78 states.

Transitions from state (c_prev, t_prev) at position i-1 to state (c_curr, t_curr) at position i:
- The character at position i is c_curr.
- If t_prev == 3+ (i.e., previous run has length ≥ 3): we can either:
  - End previous run at i-1, start new run of c_curr at i: t_curr = 1. (We can start any char.)
  - Continue previous run: need c_curr == c_prev. t_curr = 3+ (and we extend by 1).
- If t_prev == 1 or 2: we must continue the same run. So c_curr == c_prev. t_curr = t_prev + 1 (if t_prev=1, t_curr=2; if t_prev=2, t_curr=3+).
- If i == 0: special start. t_prev is "none" (cost 0, no char). We can start any c_curr with t_curr = 1.

Cost of transition = `cost[i][c_curr]` (the cost to change position i to c_curr).

The "start" state (before position 0) is special: no cost, no char. We can think of it as a virtual state.

At the end (i = n-1), valid final states are those where the run is complete and length ≥ 3. So we need t == 3+ at i = n-1. The answer is `min over c of dp[n-1][c, 3+]`.

Wait, but what about runs that end before n-1? That would mean the last run ended at some j < n-1, and positions j+1..n-1 are part of a new run that must also have length ≥ 3 and end at n-1. So actually, the state at i=n-1 must be a run of length ≥ 3 (t=3+). The character of that run is the last block's char.

So the DP is:
- `dp[i][c][s]` where s ∈ {1, 2, 3} (3 meaning "3+").
- Initialize `dp[0][c][1] = cost[0][c]` for all c.
- For i = 1 to n-1:
  - For all c, s:
    - `dp[i][c][1] = min over c' (dp[i-1][c'][3] + cost[i][c])`. (End previous run of c' at i-1, start new run of c at i.)
    - `dp[i][c][2] = dp[i-1][c][1] + cost[i][c]`. (Continue run of c, length 1→2.)
    - `dp[i][c][3] = min(dp[i-1][c][2] + cost[i][c], dp[i-1][c][3] + cost[i][c])`. (Continue run of c, length 2→3+, or 3+→3+.)
- Answer = `min over c of dp[n-1][c][3]`.

This is O(n × 26 × 26) = O(676n) which is fine (≈ 3.4e7 for n=5e4). We can optimize the first transition: `min over c' of dp[i-1][c'][3]` is just `min_s3 = min over c of dp[i-1][c][3]`. So `dp[i][c][1] = min_s3 + cost[i][c]`. That's O(26).

Total: O(n × 26) time and space. Space: `dp_prev` and `dp_curr` of size 26×3 each.

Now, for reconstruction of the lex smallest string:
- We need to find the sequence of run characters c_1, c_2, ..., c_k (where k is the number of runs) such that the total cost is minimized, and the resulting string is lex smallest.
- The resulting string is: c_1 repeated L_1 times, c_2 repeated L_2 times, ..., c_k repeated L_k times, where each L_j ≥ 3 and sum L_j = n.
- Among all (c_1, ..., c_k, L_1, ..., L_k) with min cost, we want lex smallest string.

Since the string is compared lex, and all runs have length ≥ 3, the first run determines the first 3+ characters. So c_1 should be as small as possible. If there are ties, we look at c_2, etc.

This is a multi-criteria optimization. We can do reconstruction by walking left to right, at each step choosing the smallest possible character for the current run, subject to being able to complete the rest with total cost = target.

To do this efficiently, we can precompute the "suffix cost" for each state (i, c, s) representing: starting from position i in state (c, s) (meaning position i is the s-th char of a run of c), what's the min cost to finish the string? Then during reconstruction, at each position i with current state (c_cur, s_cur) and accumulated cost acc, we try to extend the run (if s_cur < 3) — this is forced, we must keep c_cur. Or, if s_cur == 3 (run is complete), we can choose any next char c_next and start a new run (s=1), paying cost[i][c_next], and the remaining cost from (i+1, c_next, 1) is known.

Wait, during reconstruction, the run length is determined as we go. At position i, if we are in the middle of a run (s=1 or 2), the char is forced (c_cur). If s=3 (run just completed at previous position or we are continuing), we have a choice.

Actually, the state at position i is (c, s) where s is the length of the run so far including position i. So at position i, we know s and c. If s < 3, we must continue with c at position i+1 (if i+1 < n). If s ≥ 3, at position i+1 we can either continue with c (extending the run) or end the run and start a new char.

But during reconstruction, we are constructing the string. We process positions 0, 1, 2, ... At each step, we decide the character. The state after position i tells us the run's char and length. The constraint is: if run length < 3, the next char must be the same; if run length ≥ 3, the next char can be anything (but if same, the run continues; if different, a new run starts).

So at position i, given state (c, s) with s = length so far:
- If s < 3: position i is c. Next position i+1 will be in state (c, s+1) or (c, 3+) depending.
- If s ≥ 3: position i is c. For position i+1, we can go to (c, s+1) [still 3+] or (c', 1) for any c' ≠ c? Actually, we can also go to (c, 1) which is equivalent to ending the run at i and starting a new run of c at i+1. This is valid because a run of length s ≥ 3 ending at i, followed by a run of length 1 starting at i+1 (and continuing), gives total run length s+1+... but wait, that would merge the runs! If we have a run of c of length s ≥ 3 ending at i, and then at i+1 we put c again, it's just one run of c of length s+1. So "ending and restarting with same char" is the same as "continuing the run". So we don't need to distinguish.

Therefore, from state (c, 3+), at position i+1 we can:
- Continue: (c, 3+) [i.e., s stays 3+].
- End and start new: (c', 1) for any c'.

Both are valid. The cost is the same `cost[i+1][target_char]`.

So during reconstruction, at position i we have a state. We need to output char c, update state, and move to i+1. To get lex smallest, when we have a choice (i.e., when current state is 3+), we should try to put the smallest possible char at position i+1 such that the total cost can still reach the target.

To check feasibility of choosing a particular char at position i+1 and following a particular path, we need to know the min cost of the suffix from i+1 given the new state. This is the backward DP.

So let's precompute:
- `fwd[i][c][s]` = min cost for prefix [0..i] ending in state (c, s) at position i. (This is `dp[i][c][s]`.)
- `bwd[i][c][s]` = min cost for suffix [i..n-1] starting in state (c, s) at position i. Here "starting in state (c, s)" means position i is the s-th character of a run of c.

Transitions for bwd (backward, from i = n-1 down to 0):
- At i = n-1: 
  - `bwd[n-1][c][1]` = cost[n-1][c] (run of length 1, not enough, invalid? No, it's just a state. But for the suffix to be valid, we need the run to reach length ≥ 3 by the end. If the string is just one position, impossible unless... well, n=1 is impossible because we need groups of ≥ 3. But let's compute anyway.)
  - Actually, bwd[i][c][s] should represent the min cost to make suffix [i..n-1] a good caption, given that at position i we are in state (c, s) (i.e., we commit to making position i the s-th char of a run of c). The run must reach length ≥ 3 at or before n-1.
  
This is getting complex. Let's think differently.

Alternative reconstruction: since the state space is small (78 states), we can store the full DP table `fwd[i][c][s]` for all i. Then we know the total min cost `T = min over c of fwd[n-1][c][3]`. 

To reconstruct, we start at i=0. We are in state (c, 1) for some c. We want to choose c (the first character) to be as small as possible, such that there exists a path from (0, c, 1) to a final state (n-1, c', 3) with total cost T.

We can compute `reach[i][c][s]` = min cost to reach (i, c, s) from start. This is `fwd[i][c][s]`.
And `complete[i][c][s]` = min cost to complete from (i, c, s) to the end. We need to compute this backward.

`complete[i][c][s]` = min cost for suffix [i..n-1] given that at position i we are in state (c, s) (meaning position i is the s-th char of a run of c, and we must continue to fill positions i..n-1 to form a good caption, where the run containing i may extend beyond i and subsequent runs follow the normal rules).

But the "given state" constrains position i to be c. The cost of position i is already paid in the "reach" part. The "complete" part should be the additional cost for positions i+1..n-1 (and possibly the rest of the current run).

Actually, let's define `complete[i][c][s]` = min cost to fill positions [i..n-1] such that:
- Position i is part of a run of char c, and the run has length s at position i (i.e., this is the s-th char of the run).
- The entire string [i..n-1] is a good caption (all runs ≥ 3).
- The cost includes the cost for all positions in [i..n-1], including position i.

But then `reach[i][c][s] + complete[i][c][s]` is not the total cost, because position i is counted twice. We need to be careful.

Let's define:
- `fwd[i][c][s]` = min cost to fill [0..i] such that the string is a good caption up to i, and position i is the s-th char of a run of c. (Cost includes positions 0..i.)
- `total_target = min over c of fwd[n-1][c][3]`.

For reconstruction, we need `bwd[i][c][s]` = min cost to fill [i..n-1] given that position i is the s-th char of a run of c, and the result is a good caption. (Cost includes positions i..n-1.)

If we have both, then at position i with state (c, s), the remaining cost from i to end is `bwd[i][c][s]`. The total cost would be (cost for [0..i-1]) + bwd[i][c][s]. But the cost for [0..i-1] depends on the path.

Specifically, if we are at position i and we choose to be in state (c, s) (meaning position i = c and run length is s), then the total cost is (min cost to reach i-1 and be in a state compatible with starting/continuing a run of c at i) + bwd[i][c][s] - cost[i][c]? No, bwd includes cost[i][c].

Total cost for a path = sum of cost[j][char_at_j] for j=0..n-1.

If we split at i: total = (cost[0..i-1]) + (cost[i..n-1]).
If we know the state at i is (c, s), then cost[i..n-1] ≥ bwd[i][c][s], and the minimum is achieved by the optimal completion.

For reconstruction at position i, given that we are currently at state (c_prev, s_prev) at position i-1 and we need to transition to position i, we want to choose the action (which determines c_i, the char at i, and s_i, the new state) such that the total cost can be T.

The condition is: `fwd[i-1][c_prev][s_prev] + transition_cost + (min cost from new state to end) = T`. Here `transition_cost = cost[i][c_i]`, and `min cost from new state to end` = `bwd[i][c_i][s_i] - cost[i][c_i]`? No, `bwd[i][c_i][s_i]` includes the cost of position i, which is the same `cost[i][c_i]`. So:

Total = `fwd[i-1][c_prev][s_prev] + bwd[i][c_i][s_i]`. (Since fwd includes cost[0..i-1] and bwd includes cost[i..n-1].)

Wait, is that right? fwd[i-1][...] includes costs for positions 0..i-1. bwd[i][...] includes costs for positions i..n-1. Yes, together they cover all positions, no overlap. And they share the state transition at i: from state at i-1 to state at i. The compatibility is:
- If s_prev = 1 or 2 (not yet 3+), then c_i must equal c_prev, and s_i = s_prev + 1 (so s_i=2 or 3+).
- If s_prev = 3+, then c_i can be anything, and s_i = 1 if c_i ≠ c_prev (new run), or s_i = 3+ if c_i = c_prev (continue run).

So the total cost for a path that at position i-1 is in state (c_prev, s_prev) and at position i is in state (c_i, s_i) is `fwd[i-1][c_prev][s_prev] + bwd[i][c_i][s_i]`, provided the transition is valid.

For reconstruction, we know the current state (c_prev, s_prev) at position i-1 (or i=0 start). We want to find the lex smallest choice for position i (i.e., smallest c_i, and if tie, then we look ahead). To find if a choice leads to total cost T, we check if there exists a valid transition (c_prev, s_prev) → (c_i, s_i) such that `fwd[i-1][c_prev][s_prev] + bwd[i][c_i][s_i] = T` and the transition is valid (c_i == c_prev if s_prev < 3, else any).

Since we want lex smallest string, we try c_i from 'a' to 'z'. For each candidate c_i, we determine the possible s_i values based on s_prev:
- If s_prev = 1 or 2: only s_i = s_prev + 1, and c_i must equal c_prev. So there's at most one option.
- If s_prev = 3+ (which we denote s=3 in our state): we can have s_i = 1 (new run) with any c_i (including c_prev, but if c_i == c_prev, it's equivalent to continuing, so we can treat it as either; but in terms of state, c_i = c_prev, s_i = 3 is also valid and represents the same string? Actually, if c_i = c_prev and s_prev = 3, the run continues. The state is still (c_prev, 3). The string is the same whether we say "continue" or "end and start new run of same char". For DP, we might have both transitions, but they give the same cost and same string. We can just treat it as: if s_prev = 3, c_i can be anything, s_i = 1 if c_i ≠ c_prev, or s_i = 3 if c_i = c_prev.

So for each candidate c_i, we check if there exists valid s_i such that `fwd[i-1][c_prev][s_prev] + bwd[i][c_i][s_i] = T`. If yes, we fix c_i, update s_prev to s_i, and move to i+1.

We also need to handle the start: at i=0, we are in a "start" state (no previous char). We choose c_0 from 'a' to 'z', s_0 = 1, and check if `bwd[0][c_0][1] = T` (since fwd[-1] = 0).

Wait, `fwd[i][c][s]` is defined for i ≥ 0. At i=0, `fwd[0][c][1] = cost[0][c]`. The condition is: total cost = `bwd[0][c_0][1]`. But `bwd[0][c][1]` should equal `fwd[n-1][final state] = T` if we follow the optimal path. So we check if `bwd[0][c_0][1] == T` and pick smallest c_0.

But `bwd[0][c][1]` is the min cost to complete from (0, c, 1). If the path from (0, c, 1) can reach total T, then `bwd[0][c][1] = T`. However, `bwd[0][c][1]` might be larger than T if no optimal path goes through (0, c, 1). So we just check equality with T.

But computing `bwd` requires a backward DP. Let's define `bwd[i][c][s]` properly.

`bwd[i][c][s]` = min cost to fill positions [i..n-1] into a good caption, given that:
- Position i is the s-th character of a run of char c (so position i is set to c, and the run has already s characters up to i... wait, the run is being built from the left. If we are at position i and we say "s-th character of a run", we mean the run started at some position ≤ i and i is the s-th position of it. But for the suffix [i..n-1], the run containing i may have started before i. So the state (c, s) at position i means: the run of c that contains position i has length s at position i, and will continue (possibly) to the right. The run may end at some position ≥ i.

This is symmetric to the forward DP. In forward DP, we built from left to right. In backward, we build from right to left. But the run length grows as we add characters. So at position i, if the run has length s at i, then at position i+1, the run length is s+1 (if we continue) or s ends and a new run of length 1 starts (if we change char).

So `bwd[i][c][s]` is the min cost for suffix [i..n-1] with the constraint that position i is c and the current run (containing i) has length s at position i. This means positions before i are not constrained by this state (they are handled by the forward part or a previous state). The run may extend to the right.

But wait, in the forward DP, the state at position i represents the run that ends at i (or includes i). In the backward DP, it should be similar. The transition at position i (from i to i+1) in the forward direction: given state at i, we choose char at i+1 and get new state. In backward direction: given state at i, we are at the "left" end of the remaining suffix. We need to fill position i (with char c, since state is (c, s)), then position i+1, etc.

Actually, the backward DP is exactly symmetric. We can compute it by reversing the string and doing the same forward DP, but the state meanings need to be adjusted because runs have direction.

Simpler: since the forward DP gives us the cost to reach any state, and the total cost T, we can reconstruct without explicitly computing bwd. We can do a greedy left-to-right reconstruction by trying options and checking feasibility using the forward DP table and the target T.

At position i (starting from 0), we are in state (c_prev, s_prev) at position i-1 (or start). We want to choose position i. The future cost is determined by the rest of the DP. We can precompute, for each position i and each state (c, s), the min cost to complete the string from there. Call this `suffix[i][c][s]`. We can compute this with a backward DP.

Backward DP for `suffix[i][c][s]`:
- At position i, we must place char c (cost cost[i][c]). The run length is s at this position.
- We need to fill [i..n-1] to get a good caption.
- For i = n-1:
  - suffix[n-1][c][1] = cost[n-1][c] (run of length 1, invalid, but we compute anyway; the min over c of suffix[n-1][c][3] would be the answer, but we need length ≥ 3 at the end).
  - Actually, at the last position, the run must be complete. So we need s ≥ 3 at the end, or more precisely, the run containing n-1 must have length ≥ 3. So suffix[i][c][s] is only valid if we can reach a state at n-1 with s ≥ 3.
  
Let's compute suffix[i][c][s] as the min cost to fill [i..n-1] with the constraint that position i is in state (c, s). The cost includes cost[i][c]. For i < n-1, we transition to i+1:
- If s < 3 (i.e., s=1 or 2): we must continue the same run. So position i+1 must be c, and the new state is (c, s+1). Cost addition = cost[i+1][c]. So suffix[i][c][s] = cost[i][c] + suffix[i+1][c][s+1] (for s=1,2).
- If s = 3 (meaning ≥ 3): at position i+1, we can either:
  - Continue: position i+1 = c, state (c, 3). Cost = cost[i+1][c] + suffix[i+1][c][3].
  - End run and start new: position i+1 = c' (any), state (c', 1). Cost = cost[i+1][c'] + suffix[i+1][c'][1].
  So suffix[i][c][3] = cost[i][c] + min( suffix[i+1][c][3], min over c' of suffix[i+1][c'][1] ).

This is O(n × 26 × 26) = O(676n), same as forward.

Then for reconstruction:
- target = min over c of suffix[0][c][1]? No, target = min over c of fwd[n-1][c][3].
- At position 0: we are in "start" (no previous state). We try c from 'a' to 'z'. The state at position 0 is (c, 1). The total cost if we start with c is suffix[0][c][1]. We need suffix[0][c][1] == target. Pick smallest such c.
- At position i > 0: we are in state (c_prev, s_prev) from position i-1. We need to choose char c_i for position i. The new state is (c_i, s_i) where:
  - If s_prev = 1 or 2: c_i must equal c_prev, s_i = s_prev + 1. (Forced.)
  - If s_prev = 3: c_i can be anything. If c_i = c_prev, s_i = 3. If c_i ≠ c_prev, s_i = 1.
  The total cost would be (cost for [0..i-1]) + suffix[i][c_i][s_i]. The cost for [0..i-1] is already determined by the path. We know the accumulated cost for the prefix. Let `acc` be the cost for positions [0..i-1] along our chosen path. Then the total cost if we choose c_i with new state s_i is `acc + suffix[i][c_i][s_i]`. We need this to equal `target`. We try c_i from 'a' to 'z' (and appropriate s_i) and pick the smallest that satisfies `acc + suffix[i][c_i][s_i] == target`.

But we need to track `acc`. We can compute `acc` as we go: `acc` starts at 0 (before position 0). When we choose c_0, `acc` becomes cost[0][c_0]. When we choose c_i, `acc += cost[i][c_i]`.

To avoid floating point and ensure exact equality, we use the fact that `suffix[i][c][s]` is the total cost from i to end. So `acc + suffix[i][c_i][s_i] == target`. Since `acc` is sum of cost[0..i-1], and `suffix[i][c_i][s_i]` includes cost[i..n-1], the sum is the total.

We can also precompute `fwd[i][c][s]` and check `fwd[i][c][s] + suffix[i][c][s] == target`? No, fwd includes cost[0..i], suffix includes cost[i..n-1], so fwd + suffix overcounts position i.

Better: just track acc and check `acc + suffix[i][c_i][s_i] == target`.

Implementation details:
- States: 26 chars × 3 lengths (1, 2, 3). Index: `idx(c, s) = (ord(c)-ord('a'))*3 + (s-1)`.
- `fwd[i][idx]` = min cost for prefix [0..i] ending in state idx.
- Transitions: as described.
- `suffix[i][idx]` = min cost for suffix [i..n-1] starting in state idx (meaning position i is in state idx).
- Compute suffix backward.
- target = min over c of fwd[n-1][idx(c, 3)].
- Reconstruct:
  - acc = 0
  - prev_state = None (start)
  - For i in 0..n-1:
    - candidates = []
    - If prev_state is None (i=0):
      - For c in 'a'..'z': s=1. If acc + suffix[0][idx(c,1)] == target: add (c, 1).
    - Else:
      - c_prev, s_prev = prev_state
      - If s_prev in (1,2):
        - c = c_prev, s = s_prev+1. If acc + suffix[i][idx(c,s)] == target: add (c,s).
      - Else (s_prev=3):
        - For c in 'a'..'z':
          - If c == c_prev: s = 3.
          - Else: s = 1.
          - If acc + suffix[i][idx(c,s)] == target: add (c,s).
    - Pick the candidate with smallest c (lex order of the string). If multiple with same c, but s is determined by c (if c==c_prev then s=3 else s=1), so no tie.
    - Wait, for s_prev=3 and c=c_prev, s=3. For c≠c_prev, s=1. These give different s. We pick based on c. The string gets c at position i. We want smallest c that works. So just iterate c from 'a' to 'z' and check the corresponding s.
    - Fix the choice: c_i = c, s_i = s.
    - acc += cost[i][c_i]
    - prev_state = (c_i, s_i)
    - Append c_i to result.

But wait, is it possible that for s_prev=3, c=c_prev works with s=3, and also c'=c_prev+1 works with s=1, and both give the same total cost? We pick the smaller c. That's correct for lex smallest.

However, there's a subtlety: when s_prev=3 and we pick c=c_prev with s=3, the run continues. The character is c_prev. If we pick c' > c_prev, the character is c' which is larger, so the string is lex larger. So picking smallest c is correct.

But what about the case where s_prev=1 or 2 (forced char)? Then there's no choice, we just check if it works. If it doesn't work, our previous choice was wrong. But we always pick a valid choice, so it should work.

One more thing: the target cost might be `inf` (unreachable). We need to check if the string can be made good. The DP will naturally give `inf` if impossible (e.g., n=2, can't have groups of 3). We should return "" if target is inf or n < 3? Actually, if n < 3, it's impossible because the maximum run length is n < 3. So return "". If n >= 3, DP might still give inf if... well, it's always possible to make all chars 'a', which gives one run of length n ≥ 3. So it's always possible! Wait, is it? The operation allows changing to any adjacent letter any number of times. So yes, we can change every character to 'a'. The result is "aaa...a" (n times), which is one run of length n. This is always a good caption (since n ≥ 3 in the constraints? Constraints say n ≥ 1. But if n=1 or n=2, it's impossible. For n ≥ 3, it's always possible. So we only return "" if n < 3 or DP says impossible (shouldn't happen for n≥3).

But wait, is the cost to change a character to 'a' just the number of steps? Yes, each operation changes by 1 in alphabet. So distance = |ord(c) - ord('a')|.

So the problem is always solvable for n ≥ 3. For n = 1 or 2, impossible.

So algorithm:
1. If n < 3: return "".
2. Compute cost[i][c] for all i, c. (n × 26 array.)
3. Forward DP to compute fwd[i][c][s] (we can use rolling array to save memory, but n=5e4, 26×3=78, 5e4×78 ≈ 4M, which is fine. Or we can store only prev and curr for fwd, but for suffix we need the full table or compute backward similarly. Actually, for reconstruction we need suffix for all i. So we need O(n × 78) space for suffix, and we can compute fwd on the fly or also store it. Let's store both, or compute suffix using the fact that it's similar to fwd on reversed string.

Wait, the suffix DP is exactly the same as forward DP but on the reversed string! Because "good caption" is symmetric (the condition is on consecutive characters, which is symmetric left-right). So we can reverse the string, run the same forward DP, and then map back. But careful: the state (c, s) in the forward direction means run length s at position i. In the reversed string, the same DP would give "run length from the right", which corresponds to the suffix DP. Yes! So we can compute suffix by reversing the string, running the forward DP, and then reversing the indices. The cost is the same.

So:
- Compute fwd on original string. Store fwd[i][state] for all i (or just keep rolling and store the final min cost T). Actually, for reconstruction we need to check `acc + suffix[i][c][s] == T`. We don't need fwd for reconstruction if we have suffix and track acc. So we only need:
  - T = min cost (from fwd on original).
  - suffix[i][state] for all i (from fwd on reversed string, then reversed back).
  
But we also need to know the state transitions during reconstruction. The suffix array gives us the cost from any state at any position. We don't need fwd for reconstruction.

Wait, we also need to ensure that the path we take is consistent. The suffix[i][c][s] is the min cost to complete from state (c,s) at position i. During reconstruction, we are building the string and tracking acc. At position i, we choose c_i, s_i. We check if `acc + suffix[i][c_i][s_i] == T`. If yes, we proceed. This ensures the total cost is T. But we also need to ensure that the transition from previous state is valid. The candidates are generated based on valid transitions. So if we find a valid candidate that satisfies the cost equation, we are good.

But is it possible that `suffix[i][c][s]` counts a path that is not compatible with reaching this state from the left? The suffix DP starts at position i in state (c,s) and goes to the end. It doesn't know about the left. But that's fine, because we are only using the cost value, and the left part is accounted for by `acc`. The transition validity is checked separately.

However, there is a potential issue: the suffix[i][c][s] might be computed assuming we can "teleport" into state (c,s) at position i, but the cost to reach (c,s) from the left might be such that no path achieves the min suffix cost with the correct total. But since we are checking `acc + suffix[i][c_i][s_i] == T`, and T is the global min, and suffix[i][c_i][s_i] is the min cost from there, this should work.

One more catch: when s_prev = 3 and we choose c = c_prev with s = 3, the suffix[i][c][3] includes the cost of position i with c. But in the forward DP, the transition from (c_prev, 3) at i-1 to (c, 3) at i is valid and costs cost[i][c]. The suffix accounts for cost[i][c] and beyond. So it's fine.

But there's a subtle issue: in the suffix DP on the reversed string, what does state (c, s) mean? If we reverse the string, the forward DP on the reversed string builds runs from left to right of the reversed string, which corresponds to right to left of the original. The state (c, s) in the reversed DP means "run of c of length s in the reversed string". When we map back to original, this corresponds to a run of c ending at position i (in original) with length s? Or starting at position i? Let's be careful.

Let's define: in the original string, suffix[i][c][s] = min cost to convert caption[i..n-1] into a good caption, given that position i is the s-th character of a run of c (counting from the left of the suffix, i.e., the run may have started at or before i, and position i is the s-th char of it).

If we reverse the string, let rev[j] = caption[n-1-j]. Then position j in rev corresponds to position n-1-j in original. We run the forward DP on rev: `fwd_rev[j][c][s]` = min cost to convert rev[0..j] into a good caption where position j ends a run of c of length s (i.e., j is the s-th char of the run in rev). 

Now, in original, suffix starting at i corresponds to rev starting at 0. Position i in original is j=0 in rev. Position n-1 in original is j=n-1 in rev. The state at position i in original (which is j=0 in rev) in the suffix DP should correspond to the state at j=0 in rev. But in fwd_rev, the state at j=0 is the start of a run, i.e., length 1. However, in the original suffix, the run containing i might have started before i. So they don't match directly.

This is a problem. The forward DP on reversed string gives the cost assuming the run starts at the beginning of the reversed suffix. But in the original suffix DP, the run may have started earlier.

To fix this, we need to define the suffix DP properly. The suffix DP state (c, s) at position i means: in the conversion of caption[i..n-1], position i is set to c, and it is the s-th character of a run of c. This run may continue to the left (i.e., the run started at some position ≤ i and i is the s-th position of it). But in the suffix [i..n-1], we only see positions i and to the right. The "s-th character" means that there are s-1 characters to the left of i (within the run) that are also c, but they are at positions i-1, i-2, ... which are not in the suffix [i..n-1]. So for the suffix [i..n-1], the state (c, s) means: the first s-1 characters of the run are "already accounted for" (they are at positions < i, not in the suffix), and position i is the s-th. But in the suffix, we only care about positions ≥ i. The cost of positions < i is not included in suffix[i].

However, the transition from position i-1 to i in the suffix DP: if at i-1 we were in state (c', s'), and at i we are in state (c, s), the relationship is:
- If s' < 3 and c' = c and s = s'+1: continuing the same run.
- If s' ≥ 3: we can end the run and start new (c, 1) with any c, or continue (c, 3) with c = c'.

This is exactly the same as the forward DP transitions! So the suffix DP is isomorphic to the forward DP if we think of it as: "given that we are at position i in state (c, s), what is the min cost to fill i..n-1 to a good