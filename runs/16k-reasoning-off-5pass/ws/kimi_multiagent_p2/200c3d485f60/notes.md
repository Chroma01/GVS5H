
## ideation
The core difficulty is counting arrays with exactly k adjacent equalities efficiently for n, m up to 1e5. Key insight: the equality pattern is determined by choosing which k of the n-1 adjacent positions have equal neighbors — this is C(n-1, k) ways. Given any such pattern, the array is determined by: the first element (m choices), and each "different" boundary contributes a factor of (m-1) (any value except the previous). Equal boundaries contribute a factor of 1. So the answer is C(n-1, k) * m * (m-1)^(n-1-k) mod (1e9+7).

Candidate approaches:
1. Closed form with precomputed factorials/inverse factorials (O(n) precompute, O(log n) pow) — best.
2. DP over (position, count of equalities) — O(n*k), too slow for n=1e5.

Pitfalls:
- Modular inverse for binomial: need Fermat's little theorem with prime mod 1e9+7.
- Edge cases: n=1 (k must be 0, answer = m); m=1 (only possible if k = n-1, formula gives (m-1)^0 = 1 correctly, and 0 otherwise since 0^positive = 0).
- 0^0 case: when m=1 and k=n-1, pow(0, 0) = 1 in Python, which is correct.
- Factorials needed only up to n-1.

## worker: Implement and verify the closed-form solution: pre
- **Formula derivation**: Choose which k of the n-1 adjacent boundaries are "equal" (C(n-1, k) ways). The first element has m choices; each of the remaining n-1-k "different" boundaries has (m-1) choices (any value except the previous one). Equal boundaries are forced. Total: C(n-1, k) * m * (m-1)^(n-1-k) mod (1e9+7).
- **Verification against examples**:
  - n=3, m=2, k=1: C(2,1)*2*1^1 = 2*2*1 = 4 ✓
  - n=4, m=2, k=2: C(3,2)*2*1^1 = 3*2*1 = 6 ✓
  - n=5, m=2, k=0: C(4,0)*2*1^4 = 1*2*1 = 2 ✓
- **Edge cases**:
  - n=1: N=0, factorial arrays of size 1, k=0, ans = C(0,0)*m*(m-1)^0 = m ✓
  - m=1, k=n-1: (m-1)^0 = pow(0,0,MOD) = 1, ans = 1 ✓ (the all-same array)
  - m=1, k<n-1: (m-1)^(positive) = 0, ans = 0 ✓
- **Complexity**: O(n) time and space for factorial precomputation; pow is O(log n). Fits n, m ≤ 1e5 easily.
