
## ideation
**Problem restatement**  
We need a non‑empty subsequence of `nums` (order preserved) whose alternating sum  
\(a_0 - a_1 + a_2 - a_3 + \dots\) equals `k`.  
Among all such subsequences we want the maximum product that does not exceed `limit`.  
If none exists return `-1`.

**Constraints & observations**  
* `n ≤ 150`, each `nums[i] ≤ 12` (non‑negative).  
* `limit ≤ 5000` – product space is small (0 … limit).  
* Alternating sum magnitude ≤ `n·12 ≤ 1800` – manageable integer range.  
* All numbers are ≥ 0, so product 0 is possible (once a zero is taken, product stays 0).  
* Adding 1’s does not change the product but can adjust the alternating sum – useful for reaching `k` while keeping a large product.

**State design**  
We keep DP over processed prefix of the array.  
For each possible product `p` (0 ≤ p ≤ limit) we store two bitsets:

* `dp0[p]` – bitset of reachable alternating sums when the current subsequence length is **even**.  
* `dp1[p]` – bitset of reachable alternating sums when the length is **odd**.

A bit at position `i` (`0 ≤ i < BITS`) corresponds to sum `i - SHIFT`.  
`SHIFT = n·12` (1800), `BITS = 2·SHIFT+1` (3601).  

We also keep two parallel bitsets `ndp0_non` and `ndp1_non` to mark states that are reachable by a **non‑empty** subsequence.  
Initially only the empty subsequence exists: product `1`, sum `0`, even length. It is present in `dp0[1]` but not in the “non‑empty” structures.

**Transition for an element `x`**  
Let `newp = p * x`. If `newp > limit` the transition is impossible.

*If `x == 0`*  
  * `newp = 0` (product stays 0).  
  * Even → odd: `ndp1[0] |= dp0[p]` (sum unchanged).  
  * Odd → even: `ndp0[0] |= dp1[p]`.  
  * The same bits are added to the “non‑empty” sets because we have taken an element.

*If `x > 0`*  
  * Even length (contribute `+x`): `shifted = (dp0[p] << x) & MASK`.  
    `ndp1[newp] |= shifted` and also mark the same bits in the “non‑empty” set.  
  * Odd length (contribute `‑x`): `shifted = dp1[p] >> x`.  
    `ndp0[newp] |= shifted` and mark in the “non‑empty” set.

The “skip” case (not taking `x`) is handled by copying the old arrays to the new ones.

All operations are bitwise on Python big integers; each product bucket holds at most `BITS` bits (≈ 3600).  
With `limit ≤ 5000` the total memory is modest (four arrays of size `limit+1`).

**Answer extraction**  
After processing all numbers, the target bit is `target = 1 << (k + SHIFT)` (if `k` is inside `[‑SHIFT, SHIFT]`).  
Scan `p` from `limit` down to `0`. If `(ndp0_non[p] | ndp1_non[p]) & target != 0` we have a non‑empty subsequence achieving product `p` and sum `k`. Return the largest such `p`. If none found, return `-1`.

**Why this works**  
*Every reachable state is represented.*  
- The DP iterates over the array exactly once, considering both possibilities (take/skip) for each element.  
- Alternating sum updates are correct because we track parity (even/odd length) and apply `+x` or `‑x` accordingly.  
- Product stays within `limit` by construction.  
- The bitset representation compresses the sum dimension, allowing all reachable sums for a given product to be handled in O(1) per transition.

## worker: Implement the DP solution in the `Solution.maxProd
The implementation follows the planned DP with bitsets.  
Key points:

* **State representation** – For each product `p` (0 … `limit`) we keep two Python‑int bitsets:
  * `dp0[p]` – reachable alternating sums with current subsequence length even.
  * `dp1[p]` – reachable alternating sums with length odd.
  * `ndp0[p]`, `ndp1[p]` – the same but only for **non‑empty** subsequences.
* **Bit index** – Position `i` encodes sum `i‑SHIFT`. `SHIFT = n·12` (max possible magnitude), so `BITS = 2·SHIFT+1` is sufficient.
* **Transitions** – For each element `x` we either skip it (copy the old arrays) or take it:
  * If `x == 0`, product becomes 0 and the alternating sum does not change; parity flips.
  * If `x > 0`, product becomes `p·x` (if ≤ `limit`). Even length adds `+x` (left shift), odd length adds `‑x` (right shift). The left shift is masked to keep bits inside `[0, BITS‑1]`.
* **Non‑empty tracking** – Every transition that *takes* the current element updates the corresponding “non‑empty” bitsets, guaranteeing we never return the empty subsequence.
* **Answer retrieval** – The target bit `k+SHIFT` is checked against the union of the two non‑empty bitsets for each product. Scanning from `limit` downwards gives the maximum feasible product.

Complexity is roughly `O(n·limit·(BITS/wordsize))` ≈ 4·10⁷ elementary operations, well within limits for Python. Memory usage stays around a few megabytes.
