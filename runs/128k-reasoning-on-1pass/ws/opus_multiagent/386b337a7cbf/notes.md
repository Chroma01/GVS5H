
## ideation
**Restating the task.** Choose a non‑empty subsequence; its "alternating sum" (1st chosen element `+`, 2nd `-`, 3rd `+`, …, based on position *within the subsequence*, not the original array) must equal `k`; among all such subsequences maximize the product, subject to product ≤ `limit`. Return that product, or `-1`.

**Core difficulty.** Three coupled quantities must be tracked simultaneously: (a) parity of how many elements have been chosen so far (decides `+`/`-` for the next pick), (b) running alternating sum, (c) running product. A naive `dp[i][parity][sum][product]` boolean is ~150 × 2 × 1801 × 5001 states — far too big in Python if done element‑wise with sets/dicts of tuples. The trick is to notice the state space is actually tiny in two of the three dimensions and to vectorize the third with Python big‑int bitmasks.

**Key structural observations.**
- Sum range: at most 150 elements, values ≤ 12; the `+` picks are at most 75 and the `-` picks at most 75, so the alternating sum lies in `[-900, 900]`. Using OFFSET = 900 (or 1800 for safety) gives a bitmask of ≤ ~1801–3601 bits. If `|k| > 900` (certainly if `|k| > 1800`) → immediate `-1`. `k` can be up to 1e5, so this guard matters.
- Product range: any nonzero product is a product of factors in `{1,…,12}`, i.e. an **11‑smooth number ≤ limit** (primes 2,3,5,7,11 all ≤ 12). For limit = 5000 that's only a few hundred distinct values. So "product" is a cheap dictionary key, while "sum" becomes the bitmask dimension because the transitions on sum are pure **shifts**: parity 0 → `mask << num` (add), parity 1 → `mask >> num` (subtract).
- Special products: `0` (subsequence contains a zero — absorbing) and an `OVER` sentinel for "exceeded limit". `OVER` is *not* absorbing: `OVER * 0 = 0`, so an over‑limit prefix followed by a `0` yields a legitimate product‑0 subsequence. Must keep `OVER` states alive for this reason (or, equivalently, run a separate unconstrained "contains a zero" DP).

**Transitions (per element `num`, from state `(parity, prod)` with sum‑mask `m`).**
- new sum mask: `m << num` if `parity == 0`, else `m >> num`; new parity = `1 - parity`.
- new product: `0` if `num == 0` or `prod == 0`; else `prod*num` if `prod != OVER and prod*num <= limit`; else `OVER`.
- Additionally seed the singleton `[num]`: parity 1, sum `num`, product = `0 / num / OVER`.

**Pitfalls to watch.**
1. **Empty subsequence must be excluded.** Do not initialize with `{(0, prod=1): bit at sum 0}` and forget it — that would return `1` for `k = 0` even when no nonempty subsequence works. Either seed singletons at each step, or carry a "started" flag.
2. **Same element used twice in one step.** Compute all transitions from the *old* dict, then merge into a copy of the old dict (`new = dict(old)`, then OR in transitions), never iterate a dict you're mutating.
3. **Right shift must not drop valid bits.** With OFFSET ≥ 900 every reachable state has index ≥ num before subtracting, but choose OFFSET = 1800 (mask length 3601) to be bulletproof; also mask off overflow on left shift only if you rely on a fixed width (not needed with Python ints, but sizes grow — optionally `& FULLMASK`).
4. **Product 0 is a legal answer.** `nums=[0], k=0` → answer `0`, not `-1`. Since `limit ≥ 1`, `0 ≤ limit` always. So the final max must consider `0` as a candidate and distinguish "found with product 0" from "not found".
5. **Elements equal to 1**: change parity/sum but not product — handled automatically, but they mean many distinct sums map to the same product.
6. **Single element already > limit** → goes straight to `OVER`.
7. Don't forget `nums[i]` can be `0` *and* that a zero contributes `+0`/`-0` to the sum, i.e. only flips parity.
8. Final answer = max over all keys `(parity, p)` with `p != OVER` such that bit `k + OFFSET` is set in the mask; `-1` if none.

**Complexity.** 150 elements × (#products ≈ 300–700) × 2 parities big‑int shifts of ~3600 bits ≈ 10⁵–2·10⁵ cheap bigint ops — comfortably fast.

**Alternative framings (for cross‑checking).**
- Bitmask over *products* keyed by `(parity, sum)`: 2×1801 keys of 5001‑bit ints — but multiplying by `num` is not a shift, so transitions cost O(#products) anyway; worse.
- Avoid the `OVER` sentinel by running two DPs: (i) products only over 11‑smooth values ≤ limit for zero‑free subsequences, (ii) an unconstrained `(parity, sum)` reachability DP marking "contains at least one 0" to cover product‑0 subsequences.
- Brute-force/memo `dfs(i, parity, sum, prod)` with `functools.lru_cache` for a slow reference implementation to validate against on random small inputs.

## worker: *Task A+B+C (write the full solution):** Implement
Implemented exactly the planned big-integer bitmask DP.

- **State**: `(parity, prod)` → bitmask of achievable alternating sums, bit index `s + OFFSET` with `OFFSET = 1800`, `SIZE = 3601`. `parity` = number of already-chosen elements mod 2, so the next chosen element is added (`parity == 0`) or subtracted (`parity == 1`); this makes the sum transition a pure shift (`<< num` / `>> num`), letting one bigint op handle all ~1801 sums at once.
- **Product**: kept as a dict key. Nonzero products are 11-smooth numbers ≤ `limit` (only a few hundred for `limit ≤ 5000`), plus `0` and the sentinel `OVER = limit + 1`. `OVER` states are retained (not pruned) because `OVER * 0 = 0`, so an over-limit prefix followed by a `0` still yields a legal product-0 subsequence — handled by `cap`.
- **Non-emptiness**: dp starts empty; at each element we seed the singleton `[num]` into `(1, cap(1, num))`. So the empty subsequence is never represented and `k = 0` cannot be satisfied vacuously.
- **No self-reuse in one step**: all transitions are computed from the old `dp` into a fresh `add`, then OR-ed in, so an element can't be used twice.
- **Early exit**: `|k| > 900` is unreachable (≤ 75 positive picks × 12), return `-1`; this also prevents out-of-range bit indices for `k` up to 1e5.
- **Right shift safety**: every dp state corresponds to a real (prefix) subsequence, so its sum is in `[-900, 900]`; with `OFFSET = 1800` no meaningful bit is ever shifted out below zero. Left shifts are masked with `FULL`.
- **Answer**: max `prod != OVER` whose mask has bit `k + OFFSET` set. `best` starts at `-1`, so product `0` (e.g. `nums=[0], k=0` → `0`) is correctly returned rather than `-1`.
- **Complexity**: 150 elements × O(#products·2) states × one ~3.6 kbit shift ≈ 10⁵ cheap bigint ops.

Hand-checked examples: `[1,2,3],k=2,limit=10` → 6; `[0,2,3],k=-5` → -1 (unreachable sum); `[2,2,3,3],k=0,limit=9` → 9 (36 maps to `OVER`, 9 is kept via `[3,3]`).
