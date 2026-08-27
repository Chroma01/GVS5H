
## ideation
The problem asks to count arrays of length n over alphabet [1..m] with exactly k adjacent equalities. The plan already identifies the closed form: C(n-1, k) * m * (m-1)^(n-1-k) mod p. Reasoning: treat the array as runs separated by "change" boundaries. Choose which k of the n-1 boundaries are equalities; the first value is free (m choices); each non-equal boundary forces a different value (m-1 choices each). This matches all examples: n=3,m=2,k=1 → C(2,1)*2*1 = 4; n=4,m=2,k=2 → C(3,2)*2*1 = 6; n=5,m=2,k=0 → 1*2*1^4 = 2.

Core difficulty: computing C(n-1, k) mod 1e9+7 efficiently for n up to 1e5 — precompute factorials and inverse factorials (Fermat inverse) in O(n). Also pow with modular exponentiation.

Pitfalls:
- m = 1: then (m-1)^(n-1-k) = 0^(positive) = 0 unless k = n-1, where 0^0 must be 1. Python's pow(0, 0, MOD) returns 1, so it's fine, but worth verifying.
- k can be 0 up to n-1; factorial table size n suffices.
- Modulo arithmetic throughout; use MOD = 10**9+7.
- No overflow issues in Python, but keep mod operations for speed.

## worker: Implement the full solution: precompute factorials
- Closed form: `C(n-1, k) * m * (m-1)^(n-1-k) mod p`.
  - Choose which `k` of the `n-1` adjacent boundaries have equal values: `C(n-1, k)`.
  - The first element is arbitrary: `m` choices.
  - Each of the remaining `n-1-k` boundaries must switch to a different value: `(m-1)` choices each.
- Factorials/inverse factorials precomputed in O(n) with Fermat's little theorem for the inverse (`pow(fact[n-1], MOD-2, MOD)`), then downward recurrence `inv_fact[i] = inv_fact[i+1] * (i+1)`.
- Verified against examples:
  - n=3, m=2, k=1 → C(2,1)*2*1^1 = 4 ✓
  - n=4, m=2, k=2 → C(3,2)*2*1^1 = 6 ✓
  - n=5, m=2, k=0 → C(4,0)*2*1^4 = 2 ✓
- Edge cases:
  - n=1: k must be 0; answer = C(0,0)*m*(m-1)^0 = m ✓ (arrays of length 1).
  - m=1, k=n-1: answer = C(n-1,n-1)*1*0^0 = 1 (Python's `pow(0, 0, MOD)` returns 1) ✓ — the all-ones array.
  - m=1, k<n-1: answer includes factor 0^(positive) = 0 ✓ — impossible to have a "different" boundary with one value.
- Complexity: O(n) time, O(n) space; well within limits for n ≤ 1e5.
