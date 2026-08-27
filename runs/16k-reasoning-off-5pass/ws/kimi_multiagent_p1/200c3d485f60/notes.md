
## ideation
The plan is already correct and complete. Let me verify the reasoning and identify edge cases:

**Core insight:** An array is fully determined by:
1. The first element: `m` choices
2. For each of the `n-1` adjacent pairs, whether it's "equal" (forced value, 1 way) or "different" (`m-1` choices)

We need exactly `k` equal transitions among `n-1` positions: `C(n-1, k)` ways to pick which positions.

**Formula:** `ans = m * C(n-1, k) * (m-1)^(n-1-k) mod (10^9+7)`

**Verification against examples:**
- Ex1: n=3,m=2,k=1 → 2 * C(2,1) * 1^1 = 2*2*1 = 4 ✓
- Ex2: n=4,m=2,k=2 → 2 * C(3,2) * 1^1 = 2*3*1 = 6 ✓
- Ex3: n=5,m=2,k=0 → 2 * C(4,0) * 1^4 = 2 ✓

**Edge cases / pitfalls:**
- `m = 1`: then `m-1 = 0`. If `k = n-1`, exponent is 0 → `pow(0, 0, MOD)` returns 1 in Python ✓ (only the all-same array exists, answer = 1). If `k < n-1`, `pow(0, positive, MOD) = 0` → answer 0 ✓.
- `k = 0`: `C(n-1, 0) = 1` ✓.
- `n = 1`: `n-1 = 0`, `k` must be 0 → answer = `m * 1 * (m-1)^0 = m` ✓.
- Factorials needed up to `n-1 ≤ 10^5 - 1`, well within precomputation limits.
- Modular inverse via Fermat's little theorem since MOD = 10^9+7 is prime.
- Constraints are small enough that even computing factorials per call is fine (LeetCode-style, single call per test typically, but multiple test cases may call repeatedly — precomputing up to 1e5 once at module/class level is safest and still fast).

**Implementation details:**
- Precompute `fact` and `inv_fact` arrays up to `n` (or a global max of 10^5) lazily or at class level.
- `C(a, b) = fact[a] * inv_fact[b] * inv_fact[a-b] % MOD`.
- Use built-in `pow(base, exp, MOD)`.

## worker: Implement the full solution: precompute factorials
- **Model:** An array is uniquely determined by its first element (`m` choices) and, for each of the `n-1` adjacent transitions, whether it is "equal" (1 way, value forced) or "different" (`m-1` choices). Choosing exactly `k` of the `n-1` transitions to be equal gives `C(n-1, k)` possibilities.
- **Formula:** `ans = m * C(n-1, k) * (m-1)^(n-1-k) mod (10^9+7)`.
- **Precomputation:** Factorials and inverse factorials up to `10^5` are computed once (class-level cache) using Fermat's little theorem (`inv_fact[MAX] = fact[MAX]^(MOD-2)`, then downward recurrence), giving O(1) binomial queries per call.
- **Verified examples:**
  - n=3, m=2, k=1 → 2·C(2,1)·1¹ = 4 ✓
  - n=4, m=2, k=2 → 2·C(3,2)·1¹ = 6 ✓
  - n=5, m=2, k=0 → 2·C(4,0)·1⁴ = 2 ✓
- **Edge cases:**
  - `n=1, k=0` → `m * 1 * (m-1)^0 = m` ✓
  - `m=1, k=n-1` → `1 * 1 * pow(0,0,MOD) = 1` (Python's `pow(0,0,MOD)` returns 1) ✓
  - `m=1, k<n-1` → `pow(0, positive, MOD) = 0` → answer 0 ✓
- **Complexity:** O(MAX) one-time precomputation, O(log n) per query (modular exponentiation).
