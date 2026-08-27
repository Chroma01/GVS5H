
## ideation
Core difficulty: N is up to 1.2e6, so any per-index search over subsets/pairs is impossible. The key structural observation is that a candidate GCD `g` is feasible for index `i` iff `g | A_i` and at least `K` array elements are divisible by `g`. Necessity: if the chosen set has GCD `g`, all chosen elements are divisible by `g`. Sufficiency: if `g | A_i` and `cnt[g] >= K`, choose `A_i` plus any `K-1` other multiples of `g`; their GCD is at least `g`, so the true maximum is the largest feasible divisor of `A_i`.

This reduces the problem to a divisor/multiple sieve over values `1..M`, where `M = max(A) <= 1e6`. Duplicates only matter through frequencies. Candidate GCDs need not appear in `A`, e.g. elements `4` and `8` can yield GCD `2` even if `2` is absent. Edge case `K=1` works naturally: every `A_i` is feasible for itself, so the answer is `A_i`.

Main pitfalls: confusing “value appears in array” with “value can be a GCD”; forgetting that including `A_i` still leaves `cnt[g]-1 >= K-1`, equivalent to `cnt[g] >= K`; using too much memory in Python with several lists of Python ints; slow I/O for 1.2e6 integers; and accidentally doing divisor enumeration per index instead of per distinct value or via a global `best[x]` table.

Complexity target: `O(M log M + N)` time and `O(M)` memory. The harmonic sum over multiples is about `M * H_M ≈ 1e6 * ~14`, which is fine if implemented with tight loops and fast I/O.

## worker: Implement the complete Python solution in one pass
- **Key fact:** candidate gcd `g` is usable for index `i` iff `g | A_i` and at least `K` elements of `A` are divisible by `g`. Necessity is obvious; sufficiency follows by taking `A_i` plus any `K-1` other multiples of `g` (possible since `cnt[g] >= K`), giving gcd at least `g`. So the answer for `i` is the largest divisor `g` of `A_i` with `cnt[g] >= K`.
- **Implementation:**
  - Fast parse via `read().split()`; values stored in a compact `array('i')` (4 bytes each), token list freed immediately.
  - `cnt` starts as frequencies, then an ascending in-place sieve `cnt[d] = sum(cnt[d::d])` turns it into "number of elements divisible by d". Correct because all multiples of `d` are `>= d`, and only indices `< d` have been overwritten. Slice + `sum` run at C speed; total work is `M * H_M ≈ 1.4e7`.
  - `best[x]` table built by ascending slice assignment `best[d::d] = [d] * (M//d)` only for feasible `d`, so the largest feasible divisor wins. `d = 1` is always feasible (`cnt[1] = N >= K`), so every value gets an answer.
  - Output buffered in 65536-line chunks to bound memory.
- **Correctness checks:** Sample 1 gives `3,4,6,1,6`; Sample 2 (`K=N`) gives all `1`s since only `g=1` divides `K` elements. `K=1` yields `best[A_i] = A_i` as required.
- **Complexity:** `O(M log M + N)` time, `O(M)` memory (two lists of size `M+1` plus a 4-byte-per-element array for `A`).
