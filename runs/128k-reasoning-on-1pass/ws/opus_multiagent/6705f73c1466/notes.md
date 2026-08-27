
## ideation
**Core task.** Minimum adjacent swaps to make all 1s contiguous. Standard reduction:

- Let `p_0 < p_1 < ... < p_{k-1}` be the 0-indexed positions of the 1s.
- Relative order of the 1s never needs to change (swapping two 1s is a no-op / never helps), so the final configuration is `p_j -> t + j` for some block start `t`.
- Number of adjacent swaps = total displacement of the 1s = `Σ_j |p_j - (t + j)| = Σ_j |b_j - t|` where `b_j = p_j - j`. (Justification: each swap moves exactly one 1 by one position when it exchanges a 1 with a 0; swaps of equal characters are wasted. The 1s never cross, so displacements add.)
- `b` is non-decreasing (since `p` strictly increasing ⇒ `p_{j+1}-p_j ≥ 1` ⇒ `b_{j+1} ≥ b_j`), so **no sorting is needed**; the median is `b[k//2]` (or `b[(k-1)//2]` — both give the same optimum).
- Answer = `Σ_j |b_j - b[k//2]|`.

**Sanity checks (hand):**
- `0101001`: p = 1,3,6 → b = 1,2,4 → med 2 → 1+0+2 = 3 ✔
- `100`: p = 0 → b = 0 → 0 ✔
- `0101001001`: p = 1,3,6,9 → b = 1,2,4,6 → med (index 2) = 4 → 3+2+0+2 = 7 ✔ (lower median 2 also gives 7)

The proposed PLAN is correct. Remaining concerns are purely implementation/performance.

**Pitfalls to watch:**
1. **Speed in pure Python.** N = 5·10⁵ is small enough that a pure-Python loop over the string (or a list comprehension building positions) is fine (~0.1–0.3 s), but avoid per-character `S[i]` indexing in a naive double loop. Better: numpy `np.frombuffer(S.encode(), dtype=np.uint8)` + `np.flatnonzero(arr == 49)`.
2. **Overflow in numpy.** `Σ|b_j - med|` can be ~ (2.5e5)·(5e5) ≈ 1.25e11 — exceeds int32. Use `dtype=np.int64` explicitly (on Windows numpy defaults to int32 for some ops) or convert with `.astype(np.int64)` before summing; then `int(...)` for printing. Pure Python ints avoid this entirely.
3. **Input parsing.** Read with `sys.stdin.buffer.read().split()`; strip newline/CR from S. Don't rely on `input()` twice for large lines (fine here, but buffer read is safer). N is given but should trust `S` length after stripping.
4. **Edge cases.** k = 1 → answer 0; already contiguous → answer 0 automatically; all-1 string → b all equal → 0. Guaranteed at least one 1, so no division by zero / empty median.
5. **Don't** try to minimize over "block of 1s placed anywhere including pushing against boundaries" separately — the median formula already handles it, and the resulting `t` is automatically feasible (`t ≥ 0` and `t + k - 1 ≤ N-1` since `t = b_m = p_m - m` with `0 ≤ p_m ≤ N-1`).
6. Alternative equivalent formulation (prefix-sum / choosing the window of length k that maximizes contained 1s, i.e. cost = Σ distances) is more error-prone; the median-of-`b` form is cleanest.

**Complexity.** O(N) time, O(k) memory.

## worker: Write the complete final program: read `N` and `S`
- Implemented the median-of `b_j = p_j - j` formula: minimum adjacent swaps = `Σ_j |b_j - b[k//2]|`, where `p` are 0-indexed positions of 1s. `b` is non-decreasing so no sorting is needed.
- Numpy fast path: `np.frombuffer` on the raw bytes (comparison against `49 == ord('1')`), positions via `np.flatnonzero`, cast to `int64` before subtraction/sum to avoid 32-bit overflow (max sum ≈ 1.25e11).
- Fallback loops over the bytes object (iterating a `bytes` yields ints in Py3, hence the `ch == 49` check; the `'1'` check keeps it safe if a str somehow appears) and uses Python big ints.
- Input read via `sys.stdin.buffer.read().split()`, which strips whitespace/CR automatically; tolerant of a missing N token.
- Hand-verified against the three samples: `0101001` → 3, `100` → 0, `0101001001` → 7.
- Complexity: O(N) time, O(k) memory.
