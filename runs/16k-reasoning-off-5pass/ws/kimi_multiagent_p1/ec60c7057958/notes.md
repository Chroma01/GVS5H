
## ideation
**Core difficulty:** n ≤ 100 rules out enumeration; k ≤ 10^15 means we need combinatorial counting (factorial number system style), choosing each position's value by counting valid completions.

**Key structure of the constraint:** "No two adjacent same parity" means the parity pattern of the whole permutation must alternate. Two observations:
- For a valid full permutation to exist, counts of odds and evens must differ by at most 1.
- Once the parity of the first element is fixed, the entire parity pattern is forced: positions 1,3,5,... get that parity, positions 2,4,6,... get the other. So a valid permutation exists for a given starting parity iff the slot counts match the available counts.

**Counting completions:** Suppose we've placed a prefix ending with parity p, with `o` odds and `e` evens remaining. The next position must have parity 1-p, and thereafter the pattern is forced. Feasibility: the number of remaining slots of odd parity must equal `o`, and even-parity slots must equal `e`. If feasible, the number of completions is `o! * e!` (any assignment of remaining odds to odd slots, evens to even slots). Otherwise 0. This is O(1) per candidate given precomputed factorials.

**Algorithm (k-th permutation via counting):**
1. Precompute factorials fact[0..n] as Python big ints.
2. Compute total valid permutations: sum over feasible starting parities of (odds! * evens!). If total < k, return [].
3. Greedily build the answer: at each position, iterate candidate values in increasing order among remaining numbers; for each candidate, check parity compatibility with previous element, compute completions count c; if k > c, subtract c and move to next candidate; else pick this candidate and break.
4. First position has no previous parity constraint — but careful: the count for a candidate first value v is completions given last parity = parity(v), which automatically encodes feasibility of the whole pattern.

**Edge cases / pitfalls:**
- n=1: single permutation [1]; k=1 → [1], else [].
- Counts: odds = ceil(n/2) (numbers 1,3,5,...), evens = floor(n/2).
- When |odds - evens| > 1, zero valid permutations (can't happen for n≥1 actually: odds-evens ∈ {0,1} always, so always feasible — but starting parity may be forced when n is odd: must start with odd).
- k is 1-indexed per examples.
- Factorials up to 100! are huge but Python handles them; counts may exceed k but we only compare/subtract, fine.
- Complexity: O(n^2) candidate checks, each O(1) — trivially fast.
- Don't forget to import List from typing.

**Verification with examples:** n=4: odds=2, evens=2. Start odd: 2!*2!=4 perms; start even: 4. Total 8. k=6: first element candidates 1 (odd, 4 completions) → k=6>4, k=2; candidate 2 (even, 4) → k=2≤4, pick 2? But expected answer starts with 3... wait — expected [3,4,1,2]. Let me recheck: candidates in order 1,2,3,4. Candidate 1: 4 completions, k=6>4 → k=2. Candidate 2: 4 completions, k=2≤4 → pick 2, giving a permutation starting with 2. But the expected 6th is [3,4,1,2] and the listed order shows [2,1,4,3] and [2,3,4,1] as 3rd and 4th... Hmm, the example lists 8 permutations where those starting with 2 are positions 3,4 and those starting with 3 are positions 5,6. That means order is: start-1 (2 perms), start-2 (2 perms), start-3 (2 perms), start-4 (2 perms)?? But [1,2,3,4],[1,4,3,2] — only 2 starting with 1, not 4. Because after first element 1 (odd), remaining odds=1, evens=2, next must be even, then odd, then even: pattern O E O E needs 2 odds 2 evens but only 1 odd left → wait [1,2,3,4]: 1O,2E,3O,4E valid. [1,4,3,2] valid. [1,2,3,4] and [1,4,3,2] only — yes 2, because after fixing first=1, remaining odds=1, evens=2, pattern for rest is E,O,E → 1 odd slot, 2 even slots → 1!*2! = 2. I made an error: completions after placing first element use remaining counts, not original counts. So count for candidate first value v = f(o - is_odd(v), e - is_even(v), parity(v)). For v=1: o=1,e=2, last=odd → next even, pattern E O E: even slots 2 = e ✓, odd slots 1 = o ✓ → 1!*2!=2. ✓ matches example. Good — the formula handles it; just be careful to decrement counts before computing completions.

## worker: Implement the full solution: precompute factorials
- **Counting lemma:** Once the parity of the last placed element is fixed, the parity pattern of all remaining slots is forced (strict alternation). A completion exists iff the number of forced odd slots equals the remaining odd count `o` and even slots equals `e`; then completions = `o! · e!` since any remaining odd can go in any odd slot and likewise for evens. This makes each candidate check O(1) with precomputed factorials.
- **k-th construction:** Standard factorial-number-system style greedy: scan remaining values in ascending order, skip candidates whose parity matches the previous element, compute the block size `c` of valid completions, subtract while `k > c`, and pick the candidate whose block contains `k` (1-indexed).
- **Total check:** Sum completions over both starting parities (decrementing the appropriate count first); if `k` exceeds the total, return `[]`.
- **Verified against examples:**
  - n=4, k=6: blocks for first element are 1→2, 2→2, 3→2, 4→2. k=6 skips 1 (k=4), skips 2 (k=2), picks 3; then continues to produce [3,4,1,2]. ✓
  - n=3, k=2: odds=2, evens=1; only odd start feasible (2!·1!=2 total). First element: 1→1 completion, k=2>1 so k=1; 2 skipped (parity infeasible block 0); 3→1 completion, pick 3 → [3,2,1]. ✓
  - n=2, k=3: total = 2 < 3 → []. ✓
- **Complexity:** O(n²) candidate scans with O(1) work each; big-integer factorials up to 100! are handled natively by Python. Edge case n=1 works: total=1, k=1 → [1], k>1 → [].
