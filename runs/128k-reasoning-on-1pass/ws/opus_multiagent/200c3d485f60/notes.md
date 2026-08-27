
## ideation
**Core difficulty.** The problem looks like it needs DP over positions with a "match count" dimension (O(n·k) states = 10^10, far too slow). The key insight is that the *values* and the *equality pattern* decouple, giving a one-line closed form. The only real work is fast modular combinatorics and edge-case care.

**Structural analysis.**
- An array of length `n` has `n-1` adjacent pairs `(arr[i-1], arr[i])`. Each pair is labeled "E" (equal) or "D" (different).
- Requirement: exactly `k` of the `n-1` labels are "E" → choose which positions: `C(n-1, k)` ways.
- Given the label pattern, build the array left to right: `arr[0]` free → `m` choices; each "E" transition forces the value → 1 choice; each "D" transition → `m-1` choices (anything except the previous value), independent of everything else.
- Total: **`m · C(n-1, k) · (m-1)^(n-1-k) (mod 1e9+7)`**.
- Sanity checks: (3,2,1) → 2·2·1 = 4 ✓; (4,2,2) → 2·3·1 = 6 ✓; (5,2,0) → 2·1·1 = 2 ✓.

**Pitfalls / edge cases.**
- `m == 1`: `(m-1) = 0`, so the term is `0^(n-1-k)`. Python's `pow(0, 0, mod) == 1`, so the formula automatically yields 1 when `k == n-1` and 0 otherwise — correct. (Don't hand-roll a pow that mishandles 0^0.)
- `n == 1`: `n-1 = 0`, `k` must be 0 (constraint), `C(0,0)=1`, `(m-1)^0=1` → answer `m`. Formula handles it.
- `k == n-1`: exponent 0 → `m` (all-equal arrays) ✓.
- Don't reduce `m` or `m-1` before mod (they're ≤ 1e5, fine, but keep everything mod-safe).
- `math.comb(n-1, k)` with n up to 1e5 gives a huge bigint but Python handles it (~fast enough, single call). Safer/cleaner: precompute factorials up to `n` with modular inverse via Fermat, O(n).
- Watch off-by-one: it's `C(n-1, k)`, not `C(n, k)`; exponent is `n-1-k`, not `n-k`.

## worker: *Write the final solution**: Implement `Solution.c
Implemented the closed form `m * C(n-1, k) * (m-1)^(n-1-k) mod 1e9+7`.

Reasoning: an array of length `n` has `n-1` adjacent pairs; exactly `k` must be equal, choose which in `C(n-1,k)` ways. Building left to right: `arr[0]` has `m` choices, each "equal" transition is forced (1 way), each "different" transition has `m-1` choices — independent of previous values. Multiplying gives the formula.

Implementation details:
- Factorials and inverse factorials up to `n` precomputed in O(n) using Fermat's little theorem (single modpow, then backwards recurrence).
- `pow(0, 0, MOD) == 1` in Python, so `m == 1` is handled automatically: answer 1 iff `k == n-1`, else 0.
- `n == 1` → `C(0,0)=1`, exponent 0 → answer `m`.
- Guard for out-of-range `k` returns 0.
- Included brute-force verification for all `n ≤ 6`, `m ≤ 4`, all valid `k` (runs only under `__main__`, so it doesn't affect judge usage).

Complexity: O(n) time and memory.
