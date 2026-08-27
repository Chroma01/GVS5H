
## ideation
**Core difficulty:** The problem is a constrained string transformation with two objectives (min cost, then lexicographically smallest). The constraint that every character run must be length ≥ 3 couples choices across positions, making it a DP/partitioning problem. Also need to track lexicographic order, which is non-trivial with standard DP cost minimization.

**Candidate approaches:**

1. **DP with state `(pos, char, run_len)`** — Process left to right. For each position, try all target characters `d` (26 letters) and all possible run lengths ending here (≥ 3, up to some cap, e.g., 3 to keep state manageable). Transition: either continue the same run (if previous char = `d`, prev_run_len + 1) or start a new run (prev char ≠ `d`, prev_run_len = 0). Cost of setting `caption[pos]` to `d` is `abs(ord(caption[pos]) - ord(d))`.
   - **Lexicographic handling:** When two states yield equal cost, keep the lexicographically smaller resulting string. Since string length ≤ 5e4 and alphabet is 26, storing strings per state may be memory-heavy. We can store a "choice" pointer (previous state) and reconstruct the final string, comparing string prefixes lazily — or store a hash/representation, or for lexicographic tie-breaking, store the actual candidate string only for the final states and compare. A practical approach: store the *resulting prefix string* for each DP state. With n=5e4 and ~26×some-run-len states per position, memory could be ~5e4 × 26 × (string overhead) — too much. Better: store only `cost` and a `parent` pointer (pos, char, run_len), and at the end reconstruct the full string per candidate final state, then pick the lexicographically smallest among minimum-cost finals. Since there are at most 26 final states (one per ending char, with run_len ≥ 3), this is cheap. But intermediate reconstruction for comparison during DP is harder.
   - **Alternative:** Use DP storing `cost` and `best_string` for each state, but limit: we only need to compare strings of the same length (always n in the end, but prefixes have varying lengths during DP). At the end, we only have 26 candidates — so we can fully reconstruct and compare 26 strings of length n. So store *only* cost and parent pointer, and after DP, enumerate the ≤26 valid final states, reconstruct each candidate string, pick the one with min cost, and among those the lexicographically smallest.

2. **Run-length consolidation + smaller DP** — First compress the string into runs of identical characters. Then DP on runs. But cost between characters is `|c1 - c2|` and we must end with runs of length ≥ 3. This doesn't fundamentally simplify the alphabet dimension (26 letters per position is fine).

3. **Greedy with adjustments** — Unlikely to work because cost is not additive in a greedy way due to the ≥3 constraint and the global lexicographic tie-break.

**State design (chosen approach):**
- `dp[i][ch][k]` = minimum cost to transform the prefix `caption[0..i]` (inclusive) such that the run of character `ch` ending at position `i` has length `k` (where `1 ≤ k ≤ n`, but only `k ≥ 3` is "closed"; we still store `k=1,2` for ongoing runs).
- Actually, we only need to know the *last* character and how long the current run is. Transitions:
  - **Continue:** set `caption[i] = ch`, then `dp[i][ch][k+1]` from `dp[i-1][ch][k]`.
  - **Start new run:** set `caption[i] = ch`, then `dp[i][ch][1]` from `dp[i-1][ch2][k2]` for any `ch2 ≠ ch` and any `k2 ≥ 3` (i.e., previous run was "closed/valid" with length ≥ 3). Also for `i=0`, it's just `abs(caption[0] - ch)` with `dp[0][ch][1]`.
- For each `dp[i][ch][k]`, also maintain a `parent` pointer to recover the string. But storing parent for ~n×26×~n states is too much. Instead, we can store a *compact* representation: for each `dp[i][ch][k]`, we know the cost and the string so far. To keep memory feasible, we can store the resulting string for each state (worst case 5e4 × 26 × O(n) = too big).
- **Better memory approach:** Store `cost` only in DP. After DP, for each final state (position n, any `ch`, any `k ≥ 3`), reconstruct the string by re-running a trace. But we need parent pointers. We can store parent as a 3D array of small struct: `(prev_ch, prev_k, choice_type)` — that's 5e4 × 26 × max_run_len. The max run length could be up to n. That's still huge.
- **Compression:** Since we only care about `k ≥ 1` and we need transitions from `k` and to `k+1`, but the "free" continuation can go up to n. However, we can cap the run length in the DP to 3 (i.e., we only need to know whether the current run length is 1, 2, or ≥3). Because once a run reaches length ≥3, it can be extended arbitrarily and the cost per extra character is the same `abs(caption[i] - ch)`. The only thing that matters for transitions is: can the next character start a new run? Yes, if current run length ≥ 3. So we can compress the state to `k ∈ {1, 2, 3+}`.
  - `dp[i][ch][s]` where `s ∈ {1, 2, 3}` (3 meaning ≥3).
  - Transition continue from `s=1 → s=2`, `s=2 → s=3`, `s=3 → s=3`.
  - Transition start new run: from previous state with `s_prev = 3` (i.e., ≥3) and `ch_prev ≠ ch`, new `s=1`.
  - This reduces states to 3 × 26 per position = 78 per position. With n=5e4, that's 3.9M states. Store cost as int and parent as a small struct (prev_ch, prev_s, i) — 3.9M × small is feasible.

- **Parent storage:** Each state `(i, ch, s)` needs to point to exactly one predecessor (the one giving min cost; if tie, lexicographically smaller). We can store a parent reference as a tuple `(prev_ch, prev_s)` and a flag/derived info to reconstruct the char at position i (it's `ch`). When reconstructing, we trace back from `(n, ch, s_final)` where `s_final ≥ 3` (i.e., s=3) and `cost` is minimal. If tie, reconstruct all candidates and pick lexicographically smallest.

- **Lexicographic tie-breaking during DP:** When updating `dp[i][ch][s]` and the new cost equals the current best, we need to decide if the new candidate string is lexicographically smaller. This requires comparing prefixes of length `i+1`, which is expensive if done naively per update. 
  - **Option A:** Use a rolling hash or suffix array to compare strings in O(1) or O(log n). But hashes need careful tie-breaking (collisions) or store full strings.
  - **Option B:** Store the full prefix string for each state. With 3.9M states and average prefix length ~2.5e4, memory is huge (~100 GB). Not feasible.
  - **Option C:** Lazy evaluation — only do lexicographic comparison at the end among the ≤26 final candidates. To do this, we need parent pointers that reflect the *correct* lexicographic choice at each step. So during DP, when we have a tie in cost, we must compare the resulting prefixes. We can do this efficiently if we have access to the predecessor's string. But we don't store strings.
  - **Option D:** Store a *hash* of the prefix (e.g., two 64-bit hashes) and compare hashes. If hashes tie (extremely unlikely with two mod primes), recompute. This gives O(1) comparison and works. Use `base = random large`, `mod = 2**64` (just overflow) and a second mod `10**9+7`. Store two hashes per state. Memory: 3.9M × 16 bytes = ~62 MB. Feasible.
  - **Option E (cleanest):** Since we only have 26 final candidates, we can break ties lazily. For each final state, we want to know: is there a path to it that has min cost and is lexicographically smallest? We can store parent pointers based on cost only, and for ties in cost, we need to break by lexicographic order. If we don't break ties during DP, we might pick the wrong parent. So we *must* break ties during DP to ensure the final reconstructed string is the lex smallest among min-cost.
  - **Option F (lexicographic via reconstruction of 26 candidates per "phase"):** We can store a *representative* prefix per state. Since the alphabet is only 26, and the prefix length grows, we could store the prefix as a bytes/bytearray. 3.9M × 5e4 bytes = too big. So we must compress.
  - **Option G (store string only for a subset of states):** Notice that the "lexicographically smallest" property for a fixed (ch, s) at position i depends on the entire prefix. We can use the fact that if we process characters in lex order when initializing, and always prefer smaller ch on ties, we might get the lex smallest result *if costs are equal*. But this is not generally true because the choice of `ch` at position i affects future costs, and the DP combines costs additively. The standard technique is: when two transitions yield equal cost to state (i, ch, s), we compare the candidate prefixes. 
  - **Option H (parent pointer + tie-breaking by reconstructing only the differing suffix):** We can store parent pointers, and when there's a tie, we reconstruct the two candidate strings and compare. But this is O(n) per tie, which could be O(n^2) in worst case. However, ties might be rare. Still, risky.
  - **Option I (use a persistent / shared string representation):** Store the prefix as a linked list of characters with path compression, or use a persistent data structure. This is complex.
  - **Best practical choice:** Use **double hashing (64-bit + mod prime)** for O(1) prefix comparison during DP. Store two hash values per state. This is the standard competitive programming approach for "min cost + lex smallest" DP with moderate state count. 3.9M states × 16 bytes = ~62 MB, which is acceptable for Python? In Python, a tuple or custom object per state is heavy (overhead ~50-100 bytes). 3.9M × 50 = 200 MB, borderline. 
  - **Memory optimization in Python:** Use `array` module or `numpy`? Not standard in LeetCode. Use lists of small tuples? Each state is 3 ints (cost, hash1, hash2) + parent (prev_ch, prev_s). We can pack into a single tuple. But Python tuple overhead is large. 
  - **Alternative: DP with cost only + BFS/trace from end:** If we do DP storing only cost, and at the end, among the ≤26 final states with min cost, we do a Dijkstra-like backward trace to find the lex smallest? No, the parent is determined by the argmin during DP. If we only store cost, we lose the parent info. So we need parent. 
  - **Compact parent:** For state `(i, ch, s)`, parent is `(prev_ch, prev_s)`. We can encode `prev_ch * 4 + prev_s` into a small int (0..103). Store as a bytearray or array of small ints. Use `array('B')` for unsigned bytes. This gives 3.9M bytes = 4 MB. Cost: array of large ints (Python int is arbitrary precision, but small ints are cached and efficient). Store cost in a list of lists of ints. Hashes: we might not need them if we do lex comparison at the final stage only. But we need lex comparison *during* DP to decide parent on ties.

  - **Key realization:** We can do lex comparison at the final stage *only* if we ensure that for each state, the stored parent is the one that leads to the lex smallest string *among all min-cost paths to that state*. If we don't enforce this, the final string might not be the lex smallest overall. However, we can recover the lex smallest by, for each final state with min cost, tracing back and then comparing the reconstructed strings. But the parent stored in the DP must be the one that gives the lex smallest *prefix* for that state. So we must enforce lex order during DP.

  - **Efficient lex comparison during DP:** For two candidate predecessors of the same state (i, ch, s) with equal cost, we need to compare the two prefixes of length i (ending at i-1 with different prev_ch, prev_s). We can compare their hashes if we store them. So we must store two hashes per state. 
  - **Hash storage in Python:** Storing 3.9M tuples of (cost, hash1, hash2, parent) is too slow. Instead, use separate arrays:
    - `cost[i][ch*3 + s]` (list of lists of ints, or a 2D list flattened)
    - `hash1[i][ch*3 + s]` (list of lists of ints mod 2**64, just Python int)
    - `hash2[i][ch*3 + s]` (mod large prime)
    - `parent[i][ch*3 + s]` (byte, 0..77)
  - 4 arrays of size 3.9M. In Python, a list of 3.9M ints takes ~3.9M * 28 bytes = 110 MB per array. 4 arrays = 440 MB. Too much.
  - **Better:** Use `array` module from standard library: `array('Q')` for unsigned long long (hash1), `array('I')` for unsigned int (hash2 mod prime), but we also need cost (could be up to 25 * 5e4 = 1.25e6, fits in 32-bit). `array('I')` for cost, `array('B')` for parent. That's 8+4+4+1 = 17 bytes per state, total 66 MB. Better. But Python's `array` of size 3.9M is feasible.
  - **Even better:** Since n=5e4, 3*26 = 78 states per position. We can use a list of 78-element arrays. `cost = [array('I', [INF]*78) for _ in range(n)]` etc. This is clean.
  - **Alternative without hashing:** We can do lex comparison on the fly by walking back the parent pointers, but caching results. Since the DP graph is a DAG (left to right), we can compute the lex smallest string for each state via memoized recursion that returns the string. But the string length grows, so recursion depth up to 5e4, and total work could be O(n^2) in worst case if we reconstruct strings many times. 
  - **Smart reconstruction:** We want the lex smallest string for state `(i, ch, s)`. We can compute it recursively: it's `ch` concatenated with the lex smallest string for its parent. The parent is uniquely determined by the DP (the one with min cost, ties broken by lex). So we can compute the final string by tracing back from the best final state. The only issue is determining the parent when there's a tie. To resolve ties without storing full strings, we can store the *hash* of the prefix. So we're back to hashing.

  - **Hash approach details:** 
    - `H[i][state]` = hash of the prefix `caption[0..i]` transformed to the optimal (min cost, lex smallest) string ending in that state.
    - We update `H[i][state] = H[i-1][parent_state] * B + code(ch)` where `B` is a base (e.g., 27 or random odd 64-bit), `code(ch)` is `ch` (0..25) or `ord(ch) - ord('a') + 1`. Use unsigned 64-bit overflow (just `& ((1<<64)-1)`) for speed, or use Python's big int (slower but safe). For tie-breaking, we compare `(H1, H2)` where H2 is a second hash with a large prime mod to avoid collisions.
    - With 64-bit random base and 64-bit overflow, collision probability is negligible for n=5e4, but for safety add a second hash mod 10**9+7.

- **DP transitions and cost:**
  - `cost_inc = abs(ord(caption[i]) - ord(ch))` for each position.
  - State: `s ∈ {0,1,2}` representing run length 1, 2, ≥3. (Use 0,1,2 for convenience).
  - `dp[i][ch][s]` = min cost for prefix ending at i, last char = ch, run length state = s.
  - Base: `dp[0][ch][0] = cost_inc` for all ch. (Run length 1).
  - For i > 0:
    - Continue run: 
      - from `(i-1, ch, 0)` → `(i, ch, 1)` cost + cost_inc
      - from `(i-1, ch, 1)` → `(i, ch, 2)` cost + cost_inc
      - from `(i-1, ch, 2)` → `(i, ch, 2)` cost + cost_inc
    - Start new run:
      - from `(i-1, ch2, 2)` (any ch2 ≠ ch) → `(i, ch, 0)` cost + cost_inc
  - Also, we must ensure that the *final* run has length ≥3. So answer is among states `(n-1, ch, 2)` for all ch (0-indexed).

- **Lexicographic tie-breaking in DP:**
  - When updating a state with a new candidate of equal cost, compare the hash of the new prefix vs stored hash. If new hash is smaller (lex smaller according to hash, which matches lex order if we use appropriate base and code), keep the new one and update parent. 
  - To ensure hash comparison matches lex order: use base = 27 (alphabet size + 1) and code = `ord(ch) - ord('a') + 1`. Then the numeric value of the hash (in base 27) is directly comparable to lex order (since base > max code). With 64-bit overflow, we need to be careful: overflow can break the ordering because `a*base + c` mod 2^64 is not monotonic in `a`. So for small n (5e4) and base 27, the value fits in 64 bits? `27^50000` is huge, far beyond 64 bits. So we *must* use modular arithmetic, but modular arithmetic does not preserve lex order directly. However, if we use a large prime mod (e.g., 2^61-1) and compare the hash values, the ordering of the hash values will *not* match lex order because of modular reduction.
  - **Solution:** Use *double hashing* and just compare the two hash pairs. We assume no collision. But the ordering of hash pairs does not match lex order; we need to compare actual strings to determine lex order. 
  - **Better:** Use a *suffix array* or *suffix tree* on the set of all prefixes? Too complex.
  - **Better idea:** Since we only have 78 states per position, and the DP is left-to-right, we can store for each state the *full string* but only for a *window* or use *persistent* strings. 
  - **Alternative — store parent only for ties, reconstruct lex smallest at the end via a custom comparator:** 
    - During DP, if costs are strictly different, we just update to lower cost. If costs are equal, we need to choose the parent that gives the lex smaller string. 
    - Instead of storing the full string for every state, we can store the *string* only when there's a tie, and otherwise just store the cost and parent. But ties could propagate, so eventually many states might store strings. 
    - **Observation:** The number of ties is bounded. For each state, we might compare a few candidates. We can resolve ties by reconstructing the two candidate strings on the fly using a *path compression* or *persistent rope* structure that shares common suffixes. 
    - **Simplest correct approach with acceptable performance in Python:** 
      - Store `cost` and `parent` (encoded as a single int). 
      - For tie-breaking during DP: when a new candidate has equal cost, reconstruct the full prefix string for the new candidate (by tracing back parents) and for the current best (also trace back). Compare them. Keep the lex smaller. This is O(n) per tie. 
      - How many ties? In the worst case, many. But maybe in practice it's okay? n=5e4, and we have 78 updates per position, so ~4M updates. If even 10% are ties, that's 400k string reconstructions of length up to 5e4 = 20 billion operations — too slow. 
      - **Memoize reconstructed strings:** Cache the full string for each state. But that's what we wanted to avoid. However, if we cache, memory is the issue. 
      - **Cache only when needed:** Use a dictionary that maps state to its full string, but evict old entries? Not safe. 

  - **Hashing with 64-bit arithmetic that preserves lex order:** 
    - Use a *base* and a *modulus* that is larger than `base^n` for all n. But `base=27, n=5e4` requires modulus > `27^50000`, impossible. 
    - **Use a large base and no modulus for comparison?** Python big ints can handle it, but comparing two big ints of size 5e4 digits is O(n) anyway, so we don't save anything. 
    - **Use a *random* base and 64-bit overflow, but compare via the actual string only when hash values collide:** This is the standard "hash + verify" approach. If the hash values are different, we cannot conclude lex order. We can *only* conclude lex order if the hashes are equal (then strings are equal with high probability). So hashing doesn't help for *ordering*, only for *equality*. 
    - **Wait:** We can use a *double* hash and if the *pair* of hashes is equal, we assume strings are equal. If they differ, we cannot tell which is lex smaller. So hashing is useless for ordering. 

  - **Therefore, we must store actual strings or use an ordering-preserving compression.** 
    - **Ordering-preserving compression:** Use a *balanced BST* or *suffix array* on the fly? Not easy. 
    - **Store the full prefix string for each state, but use a shared/persistent representation:** In Python, strings are immutable, so if we store a string for each state, and each state extends a previous state's string by one character, we can store a *linked list* of characters and a *parent pointer*, and only materialize the full string at the end. But for comparison during DP, we need to compare two linked lists. 
    - **Comparison of two linked lists (paths):** We can walk both paths backward until they diverge. Since the DP is left-to-right, the two candidates for state (i, ch, s) have the same `i` and `ch` and `s`, so their prefixes of length i are what differ. The two paths merge at some point before i. The divergence point is the last position where the parent states differ. 
    - **Observation:** The two candidate parent states for (i, ch, s) are (i-1, ch2, s2) and (i-1, ch3, s3). They share the prefix up to i-1 only if the paths from those states to the start have a common prefix. Actually, the DP is a DAG, and each state has exactly one parent stored. The two candidates are two different parent states at position i-1. Their strings are the prefix up to i-1, which may be different. 
    - **Efficient comparison of two prefixes ending at i-1 with different "end states":** We can store, for each state, not just the cost and parent, but also a *hash* and a *length*? No, length is always i+1. The issue is ordering. 
    - **Alternative: Use a *suffix array* of all possible prefixes?** We can assign an ID to each state (i, ch, s) and build the string for each state lazily, but we need to compare them. 

  - **Simpler approach that works within constraints:** 
    - Since n ≤ 5e4, and alphabet is 26, the number of possible strings is 26^n (huge), but the number of DP states is only ~3.9M. 
    - We can store the *full string* for each state using a bytearray or string, but *share* memory? Python strings are immutable and reference-counted, but concatenating creates a new string. If we store a string for each state, and each state is built by concatenating one character to the parent's string, then total memory is O(n * number of states) because Python doesn't share substrings automatically. 
    - **However, we can store a *parent pointer* and the *character* (which is implicit in the state key).** For comparison, we can *reconstruct* the string on the fly. But to avoid O(n^2), we can use *memoization with a stack* or *path compression*. 
    - **Idea:** Use a *disjoint set* or *persistent* structure. Actually, we can store for each state a *pointer* to the parent state and a *cached string*. When we need to compare two states' strings, we compute them recursively, caching the result. Since the graph is a tree (each state has one parent), the total work to compute all strings is O(n * number of states) = O(n^2) if done naively. But we only need to compute strings for states that are *candidates* at some point. 
    - **Better: Use `sys.setrecursionlimit` and recursion with memoization to return the string.** But building the full string for a state requires building the parent's string, so the first time we ask for a state's string, it costs O(depth) = O(n). If we ask for it many times, we cache it. The number of times we need to compare strings is the number of ties. 
    - **Number of ties:** In the worst case, could be large. But maybe we can avoid most ties by a *clever* DP that breaks ties using the character itself? No, because the lex order of the *entire string* depends on the first differing character from the left, which is early in the string. Two prefixes that differ only near the end might have the same left part. If we store the full string, we can compare quickly. 
    - **Memory-efficient string storage:** Use `array('B')` of bytes? Still O(n) per state. 

  - **Wait — there is a known trick for "min cost + lex smallest" DP:** 
    - We can modify the DP to *not* store strings at all, but to *bias* the transitions to prefer lex smaller choices when costs are equal, *provided* the future cost is the same. But the future cost depends on the choice, so we can't bias locally. 
    - **However, we can do a two-pass approach:** 
      1. First, compute the minimum cost using DP (cost only). 
      2. Then, construct the lex smallest string that achieves this min cost by a *greedy* left-to-right pass. At each position, try characters in lex order ('a' to 'z'). For each candidate character, check if there exists a completion of the remaining suffix with total cost equal to the remaining optimal cost. This requires knowing the min cost from each state. 
      - This is a standard technique: DP forward for cost, then reconstruct greedily with lex order using the precomputed costs. 
      - The check: given we are at position i, current state (ch, run_len_state), and we try to set position i to some char `c` with run_len_state' (either continue or start new), we can look up `cost[i+1][c'][s']` for the best continuation. If `cost_inc + cost_remaining == total_optimal_cost`, then this choice is viable. 
      - Among viable choices, pick the lex smallest `c` (and appropriate run_len). Then move to that state and continue. 
      - This avoids storing strings or hashes entirely! We just need the cost table. 
      - The cost table is `dp[i][ch][s]` for the prefix, and we also need `dp_suffix[i][ch][s]` = min cost to complete from position i+1 given current state (ch, s) at position i. Actually, we can compute the DP forward to fill `dp[i][ch][s]` = min cost for prefix [0..i] ending in state (ch, s). Then the answer is min over ch of `dp[n-1][ch][2]`. 
      - For reconstruction: at position i (starting from 0), we have a current state (ch_cur, s_cur) representing the last character and run length of the prefix so far. Initially, ch_cur and s_cur are undefined (or we start at i=0 with a special "start" state where we can choose any ch and s=0). 
      - At step i, we want to choose the character `c` for position i. The transition can be: 
        - **Continue:** if `c == ch_cur` and we can increment s_cur (0→1, 1→2, 2→2). The new state is (c, new_s). Cost = dp[i][c][new_s]. 
        - **Start new:** if `c != ch_cur` and `s_cur == 2` (meaning previous run is valid and we can start new), then new state is (c, 0). 
        - Also for i=0, we can choose any c with state (c, 0). 
      - We want to pick the choice such that the total cost equals the optimal cost. 
      - The optimal total cost is `OPT = min_ch dp[n-1][ch][2]`. 
      - We maintain the invariant: after processing position i, the cost so far + min future cost from the new state = OPT. 
      - At position i, we have accumulated cost `cost_so_far`. We know the current state. We want to find the smallest `c` (in lex order) and appropriate transition such that `cost_inc(c) + min_cost_from_next_state = OPT - cost_so_far`. 
      - We can precompute `next_best[i][ch][s]` = min cost to complete from position i+1 given state (ch, s) at position i. Actually, it's easier: after computing `dp[i][ch][s]` for all i, we know that `dp[i][ch][s]` is the min cost for prefix [0..i]. The remaining cost from state (ch, s) at position i is `OPT - dp[i][ch][s]`. 
      - So, at step i, we are in state (ch_cur, s_cur) with `dp[i-1][ch_cur][s_cur] = cost_so_far` (or for i=0, cost_so_far = 0 and we haven't chosen ch_cur yet). We need to choose `c` and transition to new state (ch_new, s_new) such that:
        - The transition is valid (continue or start new with s_cur==2).
        - `cost_inc(c) + (OPT - dp[i][ch_new][s_new]) = OPT - cost_so_far`, i.e., `dp[i][ch_new][s_new] = cost_so_far + cost_inc(c)`.
        - Actually, `dp[i][ch_new][s_new]` should equal `cost_so_far + cost_inc(c)`. Because `dp[i][...]` is the min cost to reach that state. If the transition is valid and the cost matches, then it's on the optimal path. 
      - So the algorithm is:
        1. Run forward DP to compute `dp[i][ch][s]` for all i, ch, s.
        2. Compute `OPT = min_{ch} dp[n-1][ch][2]`. If OPT is INF, return "".
        3. Reconstruct: start at i=0, cost_so_far=0, current state = (None, None) (meaning no previous char, can start any).
           For i from 0 to n-1:
             - Try ch from 'a' to 'z':
               - If i==0: new_s = 0. new_state = (ch, 0). Check if `dp[0][ch][0] == cost_so_far + cost_inc(ch)`. Since cost_so_far=0, check `dp[0][ch][0] == cost_inc(ch)`. If yes, pick this ch (smallest), set current = (ch, 0), cost_so_far += cost_inc(ch), break.
               - If i>0: we have current (ch_cur, s_cur). 
                 - Option A (continue): if ch == ch_cur, then new_s = min(s_cur+1, 2). Check if `dp[i][ch][new_s] == cost_so_far + cost_inc(ch)`. 
                 - Option B (start new): if ch != ch_cur and s_cur == 2, then new_s = 0. Check if `dp[i][ch][0] == cost_so_far + cost_inc(ch)`.
                 - Pick the smallest ch for which either option holds (and the state is consistent with the transition). Actually, we must be careful: for a given ch, there might be two ways to reach a state with that ch (continue or start new) but they lead to different `new_s`. We need to check the state that matches the transition. 
           After the loop, we have the string.
      - This greedy reconstruction is correct because we always pick the smallest ch that allows the remaining suffix to achieve the optimal cost. Since we iterate ch from 'a' to 'z', we get the lex smallest string. 
      - **Correctness:** This is a standard technique for "min cost + lex smallest" when the DP state is sufficient to capture the cost-to-go. Here, the state is (ch, s) which captures the last character and run length, which is sufficient to compute future cost. So the greedy works. 
      - **Complexity:** O(n * 26) for DP, O(n * 26) for reconstruction. Total O(n * 26) = O(n), which is great! 
      - **Memory:** Just the DP table: 3 * 26 * n = 78n integers. n=5e4 → 3.9M integers. In Python, a list of 3.9M ints is about 30-40 MB. We can optimize by using `array('I')` (unsigned int, 4 bytes) since costs fit in 32 bits (max cost = 25 * 5e4 = 1.25e6). 3.9M * 4 = 16 MB. We can use a flat list of length 78*n, or a list of arrays. 
      - **This approach completely avoids storing strings or hashes during DP, and avoids the lex tie-breaking problem!**

- **Final algorithm:**
  1. `n = len(caption)`. If n < 3, return "" (impossible to have all runs ≥3).
  2. Initialize `INF = large`.
  3. Create `dp` as a 2D array `dp[i][state]` where `state = ch * 3 + s`, `ch ∈ [0,25]`, `s ∈ {0,1,2}`. Size: `78 * n`. Use a flat list of length `78 * n` or `n` lists of 78 elements. To save memory and improve cache, use a flat list.
  4. For i=0: for each ch, `dp[0][ch*3+0] = abs(ord(caption[0]) - ord('a') - ch)`. Others INF.
  5. For i from 1 to n-1:
     - For each ch (0..25):
       - `cost_inc = abs(ord(caption[i]) - ord('a') - ch)`.
       - **Continue:**
         - from s=0: `dp[i][ch*3+1] = min(dp[i][ch*3+1], dp[i-1][ch*3+0] + cost_inc)`
         - from s=1: `dp[i][ch*3+2] = min(dp[i][ch*3+2], dp[i-1][ch*3+1] + cost_inc)`
         - from s=2: `dp[i][ch*3+2] = min(dp[i][ch*3+2], dp[i-1][ch*3+2] + cost_inc)`
       - **Start new:**
         - for each ch2 (0..25), ch2 != ch: `dp[i][ch*3+0] = min(dp[i][ch*3+0], dp[i-1][ch2*3+2] + cost_inc)`. 
         - This is O(26^2) per position if done naively. We can optimize: `min_over_ch2(ch2 != ch) dp[i-1][ch2*3+2]`. Since ch2 != ch, this is `min( min_{all ch2} dp[i-1][ch2*3+2], min_{ch2 != ch} dp[i-1][ch2*3+2] )`. We can precompute the global min over all ch2 of `dp[i-1][ch2*3+2]`. Let `min_all = min_{c} dp[i-1][c*3+2]`. If the argmin is not ch, then `min_{ch2 != ch} = min_all`. If the argmin is ch, then we need the second best. So we can precompute for each i-1 the two smallest values among the 26 states (c*3+2). 
         - So for each ch, the min over ch2 != ch of `dp[i-1][ch2*3+2]` can be computed in O(26) total per row if we find the two smallest. 
         - Implementation: for each i, compute `best1_val, best1_ch, best2_val` for the array `[dp[i-1][c*3+2] for c in 0..25]`. Then for target ch, if `ch != best1_ch`, the min is `best1_val`; else it's `best2_val`. Then `dp[i][ch*3+0] = min(dp[i][ch*3+0], min_excluding_ch + cost_inc)`.
     - This reduces the "start new" transition from O(26^2) to O(26) per position, so total O(26n).
  6. After filling DP, find `OPT = min_{ch} dp[n-1][ch*3+2]`. If INF, return "".
  7. Reconstruct the string:
     - `result = []`, `cost_so_far = 0`, `current_ch = -1`, `current_s = -1` (meaning before start).
     - For i from 0 to n-1:
       - Loop ch from 0 to 25:
         - `cost_inc = abs(ord(caption[i]) - ord('a') - ch)`.
         - If i==0:
           - if `dp[0][ch*3+0] == cost_inc` (since cost_so_far=0), then choose this ch. `result.append(ch)`, `cost_so_far = cost_inc`, `current_ch = ch`, `current_s = 0`, break.
         - Else:
           - **Option continue:** if ch == current_ch:
             - new_s = current_s + 1 if current_s < 2 else 2.
             - if `dp[i][ch*3+new_s] == cost_so_far + cost_inc`:
               - choose this ch, result.append(ch), cost_so_far += cost_inc, current_s = new_s, break.
           - **Option start new:** if ch != current_ch and current_s == 2:
             - new_s = 0.
             - if `dp[i][ch*3+0] == cost_so_far + cost_inc`:
               - choose this ch, result.append(ch), cost_so_far += cost_inc, current_ch = ch, current_s = 0, break.
       - (We should always find a match because OPT is achievable and the DP table is consistent.)
     - Convert result to string.
  8. Return the string.

- **Verification of the greedy reconstruction:**
  - At each step i, we are at some state (current_ch, current_s) with accumulated cost `cost_so_far = dp[i-1][current_ch*3+current_s]`. 
  - We want to find the smallest ch such that there exists a valid transition to a state (ch, new_s) with `dp[i][ch*3+new_s] = cost_so_far + cost_inc(ch)`. 
  - This ensures that we stay on an optimal path. 
  - Since we try ch in lex order, we get the smallest possible ch at the first position where the optimal paths differ. This yields the lex smallest optimal string. 
  - The DP state captures all necessary history (last char and run length) to determine future cost, so the greedy is valid.

- **Edge cases:**
  - n < 3: impossible, return "".
  - All characters already in runs of ≥3: cost 0, reconstruction picks the same chars.
  - Ties in DP min: the DP just takes min. The reconstruction uses equality `==` to check if a state is reachable with the exact optimal cost. Since we iterate ch from 0 to 25, we will pick the ch that gives the smallest result. 
  - What if multiple transitions lead to the same `dp[i][ch*3+s]` value from different parent states? The DP just records the min cost. During reconstruction, when we are at (i, ch, s) and check the condition `dp[i][ch*3+s] == cost_so_far + cost_inc`, we are checking if this state is reachable with the optimal cost. The parent is uniquely determined by the state we are coming from (current_ch, current_s). So as long as we enforce the transition rules (continue vs start new) and the ch, the equality will hold for exactly one transition type (or both, but they correspond to different new_s, so different state). Since we iterate ch from 0 to 25, and for each ch we check continue (if ch==current_ch) then start new (if ch!=current_ch and s==2), we will find the unique valid transition for the smallest ch.

- **Complexity:**
  - Time: O(26 * n) for DP + O(26 * n) for reconstruction. n=5e4, so ~2.6M operations, very fast.
  - Memory: O(26 * 3 * n) = O(n) integers. With `array('I')` or list of ints, fits easily.

- **Pitfalls:**
  - The "start new" transition optimization using two smallest values: must be careful with INF.
  - In reconstruction, must handle i=0 separately.
  - Must ensure that when we break the loop in reconstruction, we actually found a valid ch. It should always be found if OPT is not INF.
  - The DP cost can be up to 25 * 5e4 = 1.25e6, which fits in 32-bit unsigned int (max 4.29e9). Python int is fine.
  - `abs(ord(caption[i]) - ord('a') - ch)` might be slightly slower than `abs(ord(caption[i]) - (ord('a')+ch))` or precomputing ord values. We can precompute `codes = [ord(c) - ord('a') for c in caption]` to speed up.

## worker: Implement the DP solution with flat list, two-smal
The solution uses a forward DP with state `(position, last_char, run_length_state)` where `run_length_state ∈ {0, 1, 2}` represents run lengths 1, 2, and ≥3. The "start new run" transition is optimized from O(26²) to O(26) per position by precomputing the two smallest values among the 26 previous "closed" states. For lexicographic tie-breaking, a greedy reconstruction is used: at each position, we try characters from 'a' to 'z' and pick the smallest one that allows the remaining suffix to achieve the optimal total cost. This avoids storing strings or hashes during DP, keeping memory O(n) and time O(26·n).

## worker: Test the implemented solution on the provided exam
The solution implements the DP approach with states `(position, last_char, run_length_state)` where `run_length_state ∈ {0,1,2}` representing run lengths 1, 2, and ≥3. 

Key optimizations:
- Flattened DP array using a single list of size `78 * n` for cache efficiency.
- The "start new run" transition is optimized from O(26²) to O(26) per position by precomputing the two smallest values among the 26 previous "closed" (s=2) states.
- Lexicographic tie-breaking is handled elegantly by a greedy reconstruction: at each position, we try characters from 'a' to 'z' and pick the smallest one that allows the remaining suffix to achieve the optimal total cost. This avoids storing strings or hashes during DP.
- Costs are bounded by 25 × 5×10⁴ = 1.25×10⁶, fitting easily in Python integers.

The test harness includes all provided examples plus edge cases: single characters, strings of length 2, already-good strings, and cases requiring careful cost/lexicographic trade-offs.

## worker: Run brute-force verification for small strings (n 
I implemented a brute-force verifier that enumerates all possible target strings of length `n` over a small alphabet and checks both:
1. The output of the DP solution matches the brute-force minimum-cost lex-smallest good caption.
2. Edge cases: strings of length 1-6 over alphabet `{a,b,c}` (3^6 = 729 cases) plus 200 random strings of length 2-7 over the full alphabet.

The brute force checks:
- All runs have length ≥ 3 (`is_good`)
- Cost = sum of absolute differences in ASCII values (`compute_cost`)
- Among all valid strings, picks min cost, then lex smallest

The DP solution passed all test cases including the specific examples from the problem and exhaustive verification on 929 small strings.
