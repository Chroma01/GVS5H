
## ideation
**Core structure.** In an alternating permutation the parities of *all* positions are forced as soon as the first element's parity is chosen (they must strictly alternate). With `o = ceil(n/2)` odd numbers and `e = n//2` even numbers available:

- Pattern starting with **odd** needs `ceil(n/2)` odds and `floor(n/2)` evens → always feasible.
- Pattern starting with **even** needs `ceil(n/2)` evens and `floor(n/2)` odds → feasible **only when n is even** (`o == e`).

Hence total count = `o! * e!` if `n` is odd, `2 * o! * e!` if `n` is even (n=1 → 1). If `k > total`, return `[]`.

**Counting completions.** Given a valid prefix, the remaining positions have a fixed alternating parity pattern and the remaining odd/even multiset sizes automatically match it, so the number of completions is exactly `(#remaining odds)! * (#remaining evens)!`. This makes the problem a clean mixed-radix / factorial-number-system digit extraction.

**Greedy construction (O(n²)).** Maintain sorted available odds/evens. At each position:
- Determine required parity (position 0: both parities allowed only if n even; otherwise forced odd; later positions: opposite of previous).
- Block size for choosing any single candidate of that parity = `fact(o' ) * fact(e')` with the chosen number removed.
- Since all candidates of the required parity at a given step yield the *same* block size B, do `idx = (k-1)//B`, pick the `idx`-th smallest available number of that parity, then `k -= idx*B`.
- Position 0 with n even: candidates are *all* numbers 1..n (both parities), and both parities give the same B = `(n/2-1)! * (n/2)!`, so the uniform-block trick still works — the candidate list is just `1..n` rather than one parity class.

**Careful point at position 0.** For even n, don't split into "odd-start half then even-start half": lexicographic order interleaves them (1,2,3,4,... as first element). Because block sizes coincide, treating first-position candidates as the full sorted list 1..n is correct. For odd n, the candidate list at position 0 is only the odds (1,3,5,...), and there the block size is `(o-1)! * e!`.

**Pitfalls / edge cases.**
- n = 1 → `[1]` if k == 1 else `[]`.
- n = 2 → 2 permutations; k=3 → `[]` (matches Example 3).
- k up to 1e15 but counts up to ~50!·50! are astronomically larger — Python big ints are fine; no overflow, but could cap counts at `>k` for speed (unnecessary at n≤100).
- Don't confuse "lexicographic on the interleaved sequence" with "lexicographic on (odd-subsequence, even-subsequence) pair" — they differ; the greedy avoids this trap.
- Ensure the "opposite parity of previous element" rule, not "position index parity of the value".
- Verify counts before greedy so we never run out of candidates mid-way.

**Sanity check (n=4,k=6).** total = 2·2!·2! = 8. B₀ = 1!·2! = 2, idx = (6-1)//2 = 2 → first = 3, k = 6-4 = 2. Next must be even, B = 1!·1! = 1, idx = 1 → 4, k = 1. Then 1, then 2 → `[3,4,1,2]` ✓. (n=3,k=2: only odd starts, B₀ = 1!·1! = 1, idx = 1 → 3, then 2, then 1 → `[3,2,1]` ✓.)

## worker: *Implement `Solution.permute`:** precompute `fact[
- Parities of all positions are forced by the first element's parity, so after a valid prefix the number of completions is `(#remaining odds)! * (#remaining evens)!` — identical for every candidate at a given step. That makes the selection a pure mixed-radix digit extraction: `idx = (k-1)//B`, `k -= idx*B`.
- Total count: `o!*e!` for odd `n` (must start odd, since an even start would need `ceil(n/2)` evens which don't exist), `2*o!*e!` for even `n`. Return `[]` when `k > total`.
- At position 0 with even `n`, candidates are all of `1..n` (lexicographic order interleaves odd- and even-starting permutations), and since `o == e` both parity choices give the same block `B = (o-1)!*e!`, so the uniform-block trick is still valid.
- Verified examples: n=4,k=6 → [3,4,1,2]; n=3,k=2 → [3,2,1]; n=2,k=3 → []; n=1,k=1 → [1], n=1,k=2 → [].
- Big integers (up to 50!·50!) are exact in Python; complexity O(n²) plus cheap bigint ops.
