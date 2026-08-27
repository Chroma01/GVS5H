
## ideation
The operation "replace every occurrence of x with y" is a global letter renaming. Key observations:

1. **Per-position constraint**: For each position i, the final image of S[i] must equal T[i]. Since operations apply globally, define a required mapping: for each letter c, all positions where S[i]=c must have the same T[i]; otherwise impossible (Sample 3: S has 'a' mapping to both 'a' and 'r'... actually 'a'→'a' and 'a'→'r' conflict → -1).

2. **Mapping graph**: Build f[c] = required target (or c itself if unconstrained... careful: unconstrained letters we can leave alone). Each letter has out-degree ≤ 1. So the graph is a functional graph: chains ending in self-loops (fixed points) or cycles.

3. **Feasibility check**: For every position i, following the chain from S[i] must terminate at T[i]. If S[i]'s chain ends in a cycle, then T[i] must be reachable... actually letters in a cycle can only ever become letters within that cycle (renaming x→y merges x into y's chain). Wait — renaming x→y means x now follows y's future renames. So the final image of c is found by following edges. If c is in a cycle, its final image can be any letter in the cycle (by rotating), but cannot leave the cycle. So: if f-chain from S[i] ends at fixed point r, need r == T[i]. If it ends in cycle C, need T[i] ∈ C.

4. **Counting operations**: Each letter c with f[c] ≠ c that actually "needs to move" costs 1 operation. Chains are straightforward (process from the end). Cycles: renaming a→b when b also needs to move would merge them incorrectly — like swapping in a cycle you need a temporary. A k-cycle needs k+1 operations normally (rotate using a buffer letter), but k operations suffice if there's a buffer: a letter not in the cycle that either (a) maps into the cycle but... hmm, actually the standard result: a cycle needs +1 extra operation unless there exists a "free" letter — one that doesn't appear in S at all (or doesn't need to change and isn't a target conflict) to use as temporary. Actually more precisely: if some letter in the cycle doesn't appear in S, we can use... no wait.

   Let me think again: to resolve a cycle c1→c2→...→ck→c1: pick any letter z not constrained to be in the cycle finally, rename c1→z (1 op), then rotate ck→... wait. Standard: rename c1→temp, then c2→... hmm, we need each ci to end at f(ci). Do: c1→z (z a buffer whose final required image is z itself or unused), then ck→c1? No...

   Simplest: with buffer z (a letter with no requirement, i.e., doesn't appear in S, so renaming things into z and out of z is safe as long as finally nothing is z... but if z appears in T? If z doesn't appear in S, positions with z don't exist, so z's final image doesn't matter). Operations: c1→z, c2→c1? No — we need c2's occurrences to become f(c2)=c3. So sequence: c1→z (now c1's chars are z), then we need c_k → c1? f(ck)=c1. Rename ck→c1 (good, c1 currently empty), then c_{k-1}→c_k, ..., c2→c3, then z→c2. Total k+1 ops. If a buffer z exists (letter not appearing in S, or more generally a letter whose current occurrences are empty at that moment), cycle costs k+1... wait that's k+1 renames? Count: c1→z, ck→c1, c_{k-1}→ck, ..., c2→c3, z→c2 = k+1 operations. Without any buffer, impossible? No — Sample 1 has cycle? S=afbfda, T=bkckbb: a→b, f→k, b→c, d→b. No cycle; answer 4 = number of changing letters. Sample 4: abac→bcba: a→b, b→c, c→a. Cycle of 3, all 26 letters: buffer letters exist (d..z unused). Answer 4 = 3+1. So with buffer, k-cycle costs k+1.

   When can a cycle be done in k? If one of the cycle letters currently has zero occurrences in S — then it's already "empty" and serves as the buffer: cost k (skip the final cleanup? Let's see: if c1 doesn't appear in S, then we don't need c1→z; do ck→c1 (c1 empty, fine), c_{k-1}→ck, ..., c2→c3: that's k-1... wait we need every ci's chars to become f(ci). If c1 has no occurrences, ops: ck→c1? But ck's target is c1 — yes rename ck→c1, then c_{k-1}→ck, ..., c2→c3. That's k-1 ops? Hmm but c1→c2 requirement: no occurrences, so nothing needed. So cost k-1? Hmm, but also letters not in the cycle and not in S can serve as z giving k+1. Actually wait, can we do better: use z as buffer costs k+1 total as computed. Hmm, but known AtCoder answer for this problem (ABC 247? No — it's AGC/ABC "Ex - Directed Substring"? Actually this is ABC 283? It's "HHKB2020?" Let me recall: This is AtCoder ABC 301? No... It's typical problem "Swap and Flip"? The known solution: answer = (number of letters c with f(c)≠c) + (number of cycles where every letter in cycle has f(c)≠c and the cycle is "tight" — i.e., all 26 letters are used in the mapping... ) Hmm.

   The known condition for +1 per cycle: a cycle needs +1 operation, EXCEPT when there exists a letter not in the cycle that can be used as a buffer, meaning a letter that doesn't appear in S (so it's free). If all 26 letters appear in S... wait, buffer z must not appear in S at the time of use, and also z must not be a letter that itself needs to end somewhere. If z appears in S, renaming c1→z would merge c1's chars with z's chars, corrupting z's positions. So buffer must be a letter with zero occurrences in S. If every letter appears in S (only possible when N≥26 and all used), and there's a cycle, then... you can still do it? Hmm, with no free letter, a "pure" cycle where every letter appears: is it solvable at all? Yes: rename c1→c2 directly? That merges c1 and c2 chars — then both would follow c2's chain and end at c3 — wrong for c2's original chars. So without buffer, a cycle is impossible? But wait, known answer: it's possible only if there's an unused letter; otherwise -1? Hmm, but actually there's subtlety: a letter in the cycle that doesn't appear in S acts as buffer and cycle costs k (not k+1): sequence ck→c1? Wait c1 empty: we need ci's chars → f(ci). Do c2→c3? No wait, order: we want to avoid merging. Rename in order: c1 is empty. Rename ck→c1? f(ck)=c1 ✓ (c1 empty so no merge issue... merging into empty letter is fine). Then c_{k-1}→ck, ..., c2→c3. Total k-1 operations for the cycle letters... but number of letters with f(c)≠c in cycle is k, and c1 doesn't appear so its "change" is vacuous. Hmm, so formula: base = count of c with f(c)≠c AND c appears in S? Not exactly — letters not in S never need operations.

   Let me restructure: Only letters appearing in S matter. For letter c in S with final required image g(c): if g(c)=c, no op needed for c. The operations needed: think of it as we must realize the mapping. Known editorial (this is ABC 296 F? No. It's "AtCoder AGC 040?" — Actually this is typical problem from ABC 249? Let me just derive).

   Derivation: Consider directed graph of required edges c→f(c) for c appearing in S with f(c)≠c. Each such edge requires exactly one rename operation c→f(c) at some point (c must be renamed at least once; renaming c more than once is wasteful but needed in cycle resolution: in the k+1 cycle scheme, c1 is renamed twice: c1→z and z→c2 — actually c1 renamed once, z renamed once; total ops = k+1 = k edges + 1 extra).

   For a chain (ending at fixed point), process in reverse topological order: each letter renamed once, cost = number of edges.

   For a cycle of length k: need a buffer. If there exists any letter z with zero occurrences in S (z may be in cycle or not):
   - If some cycle letter ci has zero occurrences in S: cost k-1? Wait but ci has f(ci)≠c as requirement — but no occurrences, so no op needed for ci's edge. Then the cycle breaks into a chain: cost = k-1 (each other letter renamed once). Hmm wait, is that right? Cycle c1→c2→...→ck→c1, c1 absent from S. Rename c2→c3? But c3's chars not yet moved — merging c2 into c3 corrupts. Correct order: start from the "sink" side: ck→c1 (c1 empty ✓), then c_{k-1}→ck, ..., c2→c3. Each merges into a now-empty letter. Cost k-1. ✓.
   - Else if some z outside cycle has zero occurrences in S: cost k+1 (as shown).
   - Else (all 26 letters appear in S — requires the cycle plus all other letters present): impossible? Hmm, but known result for this AtCoder problem: if the cycle uses... I recall the condition: if there is a cycle and the number of distinct letters available... Actually I recall this exact problem: it's from AIZU? It's AtCoder "typical90"? Let me just reason: all 26 letters appear in S, cycle exists. Any first operation x→y merges x into y. If x is in cycle, x's chars get stuck following y... could still work if y's final image equals x's required image? No, f(x)≠f(y) in a cycle (distinct). If x outside cycle: x's chars merge into y and then follow y's chain to g(y) — but x needed g(x)≠g(y) (chains differ... unless x's chain and y's chain converge — if g(x)=g(y) then merging is fine!). Hmm! So a letter x outside the cycle whose chain converges with y's... renaming x→y where g(x)=g(y) is harmless. But that doesn't help the cycle.

   Actually wait — can a letter whose chain leads INTO the cycle serve as buffer? Letter w with f(w) in cycle: w appears in S, w's chars must end at g(w) ∈ cycle. Hmm, using w as buffer: c1→w would merge c1's chars with w's chars — w's chars need to end at g(w), c1's at c2 — different cycle letters, conflict. So no.

   So with all 26 letters in S and a cycle: impossible → -1? Hmm, but I recall the known condition is exactly: cycle is "bad" if all 26 letters appear... Let me double check with small reasoning: 2 letters a,b; S contains both; f(a)=b, f(b)=a. Any op: a→b merges a into b, both end... then b→a makes everything a. Final: all a or all b — can't get a→b and b→a simultaneously. Impossible ✓. With buffer c (c not in S): a→c, b→a, c→b: 3 ops = k+1 ✓.

   So algorithm:
   - Build f[c] from positions; conflict → -1.
   - Compute g(c) = final image by following f (with cycle detection). For each position: if g(S[i]) ≠ T[i] → -1. (For cycle letters, g undefined — handle: if S[i] in cycle C, require T[i] ∈ C.)
   - Answer = sum over letters c appearing in S with f(c)≠c of 1, plus for each cycle (in the subgraph restricted to letters with f(c)≠c... cycles automatically have f(c)≠c): if all letters of cycle appear in S: need buffer: if some letter outside cycle doesn't appear in S → +1; else → -1. If some cycle letter absent from S → +0 (and subtract... base count already excludes absent letters since we only count letters in S).

   Wait, base count: letters c in S with f(c)≠c. For cycle with all present: k letters counted, +1 extra → k+1 ✓. Cycle with one absent: k-1 counted, +0 ✓. Chains: counted once each ✓.

   Edge: cycle letter absent from S but the cycle still constrains positions? If c1 absent, other letters' T values must be in cycle — checked via reachability.

   Also self-loops f(c)=c: no op.

   Hmm, one more check on "buffer outside cycle": z absent from S. After using z (c1→z, ..., z→c2), z ends empty, fine even if z has f(z) defined? If z absent from S, f(z) unconstrained — but wait f(z) might be constrained? No: constraints come only from positions of S. z absent → no constraint. ✓.

   Also possibility: multiple cycles — each needs its own buffer check, but one absent letter can serve as buffer for all cycles sequentially (it ends empty after each cycle resolution). ✓.

   Complexity O(N + 26·something). Fine.

Pitfalls:
- Conflict detection: same S-letter mapping to two T-letters → -1.
- Chain following must terminate; use memoization/DFS on 26 nodes.
- Letters in cycle: T[i] must be a cycle member.
- The "all 26 letters appear in S" buffer condition: buffer = letter (any of 26) not appearing in S and not in the cycle... actually if a cycle letter is absent, no buffer needed at all. Buffer needed only when all cycle letters present; then need any non-cycle letter absent from S.
- Note: non-cycle letter absent from S — includes letters with chains? Chain letters present in S by definition of needing... a letter could be absent from S entirely. That's the buffer.

## worker: Implement the full Python solution: parse input, b
- Built the required mapping `f[c]` from all positions; any letter of S forced to two different targets yields `-1` immediately.
- Unconstrained letters (absent from S) are treated as fixed points `f[c] = c`.
- Classified each of the 26 nodes via iterative DFS on the functional graph: chains ending at a fixed point get `final[c]`; nodes in (or leading into) a cycle are marked, with `cycle_id` assigned per cycle.
- Position validation: if `S[i]` lies in a cycle, `T[i]` must belong to the same cycle (letters can rotate within a cycle but never leave it); otherwise the chain's terminal fixed point must equal `T[i]`.
- Operation count: base = number of letters appearing in S with `f[c] != c` (each renamed exactly once, chains processed from the sink side). For each non-trivial cycle:
  - if some cycle letter is absent from S, the cycle is effectively a chain (that empty letter is the buffer) → no extra cost;
  - else if some letter outside the cycle is absent from S, it serves as a temporary buffer → +1 operation (rotate via buffer);
  - else (all 26 letters appear in S and the cycle is fully present) → impossible, print `-1`.
- A single absent letter can buffer multiple cycles sequentially since it ends empty after each rotation, so the check is per-cycle independent.
- Complexity: O(N + 26²) worst case, well within limits for N ≤ 2×10⁵.
- Verified mentally against samples: (1) afbfda→bkckbb: 4 changing letters, no cycle → 4. (2) identical → 0. (3) 'a'→'a' and 'a'→'r' conflict → -1. (4) abac→bcba: 3-cycle a→b→c→a, letters d..z unused → 3+1 = 4.

## worker: Verify the solution against additional edge cases 
- Found and fixed two bugs in the existing code during verification:
  1. **Over-strict chain validation**: the old code required `final[s] == T[i]` (chain terminal), but chains are always feasible by processing renames from the sink backwards (e.g., S="ab", T="bc" is solvable in 2 ops: b→c then a→b; old code wrongly returned -1). Since `T[i] = f(S[i])` by construction, no per-position validation is needed beyond conflict detection.
  2. **Self-loops treated as cycles** (`final = -2`), which corrupted chain-into-fixed-point propagation (e.g., S="wa", T="aa" wrongly rejected).
- Simplified correct model: requirements form a functional graph (out-degree ≤ 1). Given no conflicts:
  - Acyclic parts are always feasible: rename letters in reverse topological order, each exactly once → ends exactly at `f(c)`.
  - Each non-trivial cycle needs one extra buffer operation (rotate via a temporary letter). Buffer must be a letter absent from S; since every cycle letter necessarily appears in S (edges only arise from S positions), the buffer is automatically outside the cycle, and one absent letter serves all cycles sequentially.
  - If a non-trivial cycle exists and all 26 letters appear in S → impossible (-1).
- Answer = `#{c in S : f(c) ≠ c}` + `(number of non-trivial cycles)`.
- Verified: samples 1–4 (4, 0, -1, 4); chain case S="ab"/T="bc" → 2; chain-into-self-loop S="wa"/T="aa" → 1; 3-cycle with buffer → 4; 2-cycle with all 26 letters present → -1; identical strings → 0.
- Complexity O(N + 26²), memory O(26) besides input.

## worker: Rewrite the solution to match the verified simplif
- Rewrote the solution per the verified simplified model, removing the flawed `final`-image propagation and per-position validation entirely.
- Model justification:
  - Requirements form a functional graph on 26 letters (out-degree ≤ 1). A conflict (one source letter forced to two targets) is the only per-position impossibility, caught while building `f`.
  - Acyclic parts are always feasible: process renames from the sink backward, each letter renamed exactly once, ending exactly at `f(c)`. Hence no extra validation needed — `T[i] = f(S[i])` holds by construction.
  - Each non-trivial cycle (length ≥ 2) requires one extra "rotation" operation via a temporary buffer letter absent from S (like a temp variable in a cyclic swap). Since edges only arise from S positions, every cycle letter appears in S, so the buffer is automatically outside the cycle; a single absent letter serves all cycles sequentially because it ends empty after each rotation.
  - If a non-trivial cycle exists and all 26 letters appear in S, no buffer exists → `-1`.
- Answer = `#{c ∈ S : f(c) ≠ c}` + `(number of non-trivial cycles)`.
- Cycle detection: standard iterative three-color DFS on the 26-node functional graph; a back-edge to an on-stack node yields a cycle, counted only when its length > 1 (self-loops are fixed points, cost 0).
- Sanity checks: samples give 4, 0, -1, 4; S="ab"/T="bc" → 2 (chain, feasible); S="wa"/T="aa" → 1 (chain into self-loop); 3-cycle with unused letters → 4; 2-cycle with all 26 letters present → -1.
- Complexity: O(N + 26²) time, O(26) extra space.
