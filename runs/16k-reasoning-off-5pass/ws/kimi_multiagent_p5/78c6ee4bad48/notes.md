
## ideation
The problem: N points on a line, operation picks 4 consecutive (in sorted order) pieces a<b<c<d, reflects b,c about midpoint M=(a+d)/2, so new middle values are a+d−c and a+d−b. Goal: minimize total sum.

Key structural analysis:
- The leftmost and rightmost pieces never move (only middle two of any quadruple move), so x_1 and x_N are fixed.
- In terms of gaps g_i = x_{i+1} − x_i (i=1..N−1), the operation on (x_i, x_{i+1}, x_{i+2}, x_{i+3}) transforms gaps (g_i, g_{i+1}, g_{i+2}) = (b−a, c−b, d−c) into (d−c, c−b, b−a) — i.e., it reverses the three consecutive gaps, which is exactly swapping g_i and g_{i+2} (middle unchanged).
- Swapping elements at distance 2 generates the full symmetric group within each parity class of gap indices. So reachable configurations = arbitrary permutations of gaps within odd-indexed gaps and even-indexed gaps separately. The two parity-class multisets of gaps are invariants.
- Total sum: x_k = x_1 + sum_{j<k} g_j, so Sum = N·x_1 + Σ_{k=1}^{N−1} (N−k)·g_k. Weights w_k = N−k are strictly decreasing in k.
- To minimize: within each parity class independently, assign larger gaps to smaller indices (larger weights) — rearrangement inequality. I.e., sort each parity class's gaps in descending order and place them at the class's indices in increasing index order.
- Answer = N·x_1 + Σ over parity classes of Σ sorted-descending gaps × increasing-position weights.

Check sample 1: gaps (4,2,3), x_1=1, N=4. Odd class indices {1,3}: gaps {4,3} desc → g1=4, g3=3; even class {2}: g2=2. Sum = 4·1 + 3·4 + 2·2 + 1·3 = 4+12+4+3 = 23? That's wrong — expected 21. Hmm. Wait: weights are (N−k): w1=3, w2=2, w3=1. Sum = N·x_1 + 3·g1 + 2·g2 + 1·g3 = 4 + 12 + 4 + 3 = 23. But answer is 21 with configuration 1,4,6,10 → gaps (3,2,5). Gap multiset: {3,2,5} vs original {4,2,3} — different! So gap multisets are NOT invariant?! Recheck the operation: a=1,b=5,c=7,d=10. New middles: a+d−c = 4, a+d−b = 6. New tuple (1,4,6,10). Gaps: (3,2,5). Original gaps (4,2,3). So (g1,g2,g3)=(4,2,3) → (3,2,5). Reversal would give (3,2,4) — wrong. Recompute: new gaps are (newb−a, newc−newb, d−newc) = (4−1, 6−4, 10−6) = (3,2,5). In terms of old: newb−a = d−c = g3 ✓ (3). newc−newb = (a+d−b)−(a+d−c) = c−b = g2 ✓ (2). d−newc = d−(a+d−b) = b−a = g1... but g1 = 4, yet actual is 5?! d−newc = 10−6 = 4. Wait newc = a+d−b = 1+10−5 = 6, so d−newc = 4 = g1 ✓. But I listed new tuple as (1,4,6,10): newb=4, newc=6. But ordering: is newb < newc? newb = a+d−c = 4, newc = a+d−b = 6. Since b<c, a+d−c < a+d−b, so the piece that was at b moves to a+d−b=6 and piece at c moves to a+d−c=4. After re-sorting, positions are (1,4,6,10). Gaps (3,2,4)?? 10−6=4, not 5. I mis-added. So gaps become (g3, g2, g1) = (3,2,4). Sum = 4 + 3·3 + 2·2 + 1·4 = 4+9+4+4 = 21 ✓. 

So the reversal claim holds: gaps (4,2,3) → (3,2,4), sum 21 matches. My earlier arithmetic error. The parity-class permutation model is validated: odd class {g1,g3} = {4,3}, we can arrange as g1=3,g3=4 (which is better since weight on g1 is larger, put smaller gap there — wait, to minimize with decreasing weights we want large gaps at small weights, i.e., large gaps at large indices). Rearrangement: minimize Σ w_k g_k with w decreasing → pair largest g with smallest w → sort gaps ascending as index increases? No: within a parity class, indices increase → weights decrease → to minimize, assign gaps in ascending order to indices in increasing order? Largest weight (smallest index) should get smallest gap. So sort gaps ascending, assign to indices in increasing order. Check: odd class gaps {4,3} at indices 1,3: ascending → g1=3, g3=4 ✓ gives 21.

Pitfalls:
- Half-integers: M can be non-integer, but reflected values a+d−b are integers — all values stay integral. Good, no floating point needed.
- Need to double-check reachability: adjacent transpositions within parity class via distance-2 swaps generate all permutations within each parity class (indices 1,3,5,... are connected; 2,4,6,... connected). Yes, swapping g_i and g_{i+2} for all valid i gives full S_n on each class.
- Also confirm any such permutation is achievable while keeping the "consecutive quadruple" condition — the operation only requires i ≤ N−3, operating on sorted order; since pieces remain distinct and order-preserving? The operation can change the sorted order of pieces identities, but gaps are defined by sorted positions; the operation on sorted consecutive four always reverses those three gaps regardless. Since we can apply it to any three consecutive gaps (any i from 1 to N−3 corresponds to gaps i..i+2), all distance-2 gap swaps are available. ✓
- Large N (2e5), values up to 1e12, sum up to ~2e17 — use 64-bit (Python int fine).

Algorithm: read N, X sorted. Compute gaps. Separate by index parity (1-indexed: odd indices 1,3,5,... and even). Sort each class ascending, assign to positions in increasing index order (equivalently pair ascending gaps with descending weights). Compute answer = N·X_1 + Σ (N−k)·g_k.

Verify sample 2 mentally later: X=0,1,6,10,14,16; gaps 1,5,4,4,2. Odd indices {1,3,5}: gaps {1,4,2} sorted asc → g1=1,g3=2,g5=4. Even {2,4}: {5,4} → g2=4,g4=5. Sum = 6·0 + 5·1 + 4·4 + 3·2 + 2·5 + 1·4 = 5+16+6+10+4 = 41 ✓ matches.

## worker: Write the final Python solution: read N and X from
- Operation on consecutive quadruple (a,b,c,d) replaces b,c with a+d−c and a+d−b. In gap terms, (g_i, g_{i+1}, g_{i+2}) = (b−a, c−b, d−c) becomes (d−c, c−b, b−a) — a reversal, i.e., swapping g_i and g_{i+2}. Distance-2 swaps generate all permutations within each parity class of gap indices, and the two parity-class multisets are invariants.
- Leftmost piece x_1 never moves (only middle two of any four move), so total sum = N·x_1 + Σ_{k=1}^{N−1} (N−k)·g_k with strictly decreasing weights N−k.
- By the rearrangement inequality, the minimum pairs the smallest gaps with the largest weights within each parity class: sort each class ascending and assign to indices in increasing order.
- Verified against samples: Sample 1 → gaps (4,2,3), odd class {4,3} → g1=3, g3=4, g2=2: 4·1 + 3·3 + 2·2 + 1·4 = 21 ✓. Sample 2 → gaps (1,5,4,4,2), odd {1,4,2}→(1,2,4) at indices 1,3,5, even {5,4}→(4,5) at 2,4: 0 + 5·1 + 4·4 + 3·2 + 2·5 + 1·4 = 41 ✓.
- All values remain integers (reflections are a+d−b), pure integer arithmetic, O(N log N).
