
## ideation
The problem reduces to a clean combinatorial count:
- First element: m choices.
- Each of the n-1 adjacent gaps is either "equal" (value forced, 1 way) or "different" (m-1 ways).
- We need exactly k equal gaps: choose positions C(n-1, k), and the remaining n-1-k gaps each contribute (m-1).

Answer = m * (m-1)^(n-1-k) * C(n-1, k) mod (1e9+7).

Verification against examples:
- n=3,m=2,k=1: 2 * 1^1 * C(2,1) = 2*1*2 = 4 ✓
- n=4,m=2,k=2: 2 * 1^1 * C(3,2) = 2*1*3 = 6 ✓
- n=5,m=2,k=0: 2 * 1^4 * C(4,0) = 2 ✓

Core difficulties / pitfalls:
- Edge case m=1: (m-1) = 0. If n-1-k > 0, answer is 0 (can't have any "different" gap). If n-1-k = 0 (i.e., k = n-1), answer is 1 (all equal). Python's pow(0, 0, mod) = 1 handles this naturally, so no special-casing strictly needed, but worth double-checking.
- Need factorials and inverse factorials up to n-1 (n ≤ 1e5) for the binomial coefficient mod 1e9+7 (prime).
- Use fast modular exponentiation pow(base, exp, MOD).
- Precomputing factorials per call is O(n), fine for a single call. Could cache across calls but not required.
- k can be 0 up to n-1; C(n-1, k) valid for all these.

## worker: Implement countGoodArrays with the closed-form for
- Derived closed form: an array is fully determined by its first element (m choices) and, for each of the n-1 adjacent gaps, whether it is "equal" (forced value, 1 way) or "different" (m-1 ways). Exactly k equal gaps gives C(n-1, k) position choices, and the remaining n-1-k gaps each contribute (m-1).
- Answer = m * (m-1)^(n-1-k) * C(n-1, k) mod (1e9+7).
- Binomial computed via factorials and inverse factorials using Fermat's little theorem (MOD is prime), O(n) precompute, O(1) query.
- Verified examples:
  - n=3, m=2, k=1 → 2 * 1^1 * C(2,1) = 4 ✓
  - n=4, m=2, k=2 → 2 * 1^1 * C(3,2) = 6 ✓
  - n=5, m=2, k=0 → 2 * 1^4 * C(4,0) = 2 ✓
- Edge cases:
  - m=1, k=n-1: pow(0, 0, MOD) = 1, comb = 1 → answer 1 (the all-equal array) ✓
  - m=1, k<n-1: pow(0, positive, MOD) = 0 → answer 0 ✓
  - n=1: N=0, factorial arrays size 1, k must be 0 → answer = m * (m-1)^0 * 1 = m ✓
- Complexity: O(n) time, O(n) space per call; well within limits for n ≤ 1e5.
