
## ideation
**Reformulation.** A sequence of operations on the array corresponds exactly to a *non‑crossing perfect matching* of positions (with one unmatched position if N is odd): a pair (i,j) can be removed together only after everything strictly between them is gone, so matched pairs are properly nested/disjoint, and j−i must be odd. Total score = Σ |A_i − A_j| over matched pairs.

**Upper bound per block.** For a contiguous block B of even length 2m, every pair contributes one "+" element and one "−" element, so the score ≤ (sum of the m largest of B) − (sum of the m smallest) = 2·top_m(B) − sum(B). Call this g(B).

**Tightness.** Label the m largest elements "+" (break ties arbitrarily) and the rest "−". While the block is nonempty there is always an adjacent +/− pair (equal counts of each sign ⇒ not all equal); delete it — this is a legal operation, its score is exactly (+ value) − (− value) because every "+" element is ≥ every "−" element, and the remaining block still has balanced signs. Induction ⇒ g(B) is achievable. So for even N the answer is just g(A).

**Odd N.** Exactly one element survives, say at 1‑indexed position i. No matched pair may straddle i (the elements between a pair must all be deleted), so [1..i−1] and [i+1..N] are each matched internally ⇒ both even ⇒ i is odd. The two blocks are independent, so
answer = max over odd i of pre[i−1] + suf[N−i], where pre[k] = g(A[1..k]) and suf[m] = g(A[N−m+1..N]) (even k, m).
Note pre[i−1]+suf[N−i] ≠ g(whole array minus A_i) in general — the top‑half selection is *per block*, so both arrays must be computed separately.

**Computation.** Need, incrementally for growing prefixes (and separately growing suffixes), the sum of the top ⌊k/2⌋ elements. Classic two‑heap (median maintenance): max‑heap `low` for the small half, min‑heap `high` for the large half with |high| = ⌊k/2⌋, maintaining `sum_high` explicitly on every push/pop. Then g = 2·sum_high − running_total for even k. O(N log N), heapq is C‑level so ~3·10^5 elements × 2 passes is fine.

**Verification.**
- Sample 1 (even): top2 = 5+3 = 8, total 11 ⇒ 2·8−11 = 5 ✓.
- Sample 2 (odd, N=7, total 25): remove i=1 (value 3) ⇒ suffix {1,4,1,5,9,2}: 18−4 = 14 ✓.
- Sample 3: all equal ⇒ 0 ✓.

**Pitfalls to watch.**
- Off‑by‑one: only odd 1‑indexed i allowed for the survivor; pre[0] = suf[0] = 0; arrays indexed by *length*, not position.
- Don't reuse the same heap state across prefix and suffix passes (reset).
- Even N must not go through the odd‑case loop (and vice versa); N=2 edge case.
- Values up to 1e9 × 3e5 ⇒ use Python ints (fine), but read input with sys.stdin.buffer.
- Ensure sum_high is updated on *every* heap movement (rebalancing pop from `high` back to `low`).
- Careful with the "+ ≥ −" tie argument (duplicates) — splitting by sorted order with arbitrary tie‑break keeps the inequality, so |a−b| = a⁺−a⁻ still holds.

## worker: *Task 2+3 (implement the solution):** Write the co
- Implemented exactly the plan. `topsum_prefix` uses the classic two‑heap median structure: `low` is a max‑heap (negated) for the smaller half, `high` a min‑heap for the larger half, kept at size `k//2` after inserting the k‑th element. `sum_high` is updated on every push/pop, so `res[k] = 2*sum_high - total` equals `g` of that prefix when `k` is even (sum of top half minus sum of bottom half).
- Insertion routine: push into `low`, move its max into `high` (so the new element competes correctly), then if `|high| > k//2` move `high`'s min back into `low`. Check: k=1 → high becomes size 1 > 0 → moved back, size 0 ✓; k=2 → size 1 ✓.
- Even N: answer is `pre[N]` (single block, all elements matched, achievable by the +/− adjacent‑pair deletion argument).
- Odd N: survivor must be at an odd 1‑indexed position i (both sides even length, matchings non‑crossing), and the two sides are independent blocks, so answer = max over odd i of `pre[i-1] + suf[N-i]`, with `suf` computed on the reversed array (prefix of reverse = suffix of original).
- Complexity O(N log N), memory O(N); Python ints handle sums up to 3e14 fine. Input read via `sys.stdin.buffer`.
- Hand-checks: sample1 → 2*(5+3)-11 = 5; sample3 → all equal → 0; sample2 → i=1 gives suf[6] = 2*(9+5+4)-22 = 36-22 = 14 (max) ✓.
