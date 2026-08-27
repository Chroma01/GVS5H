
## ideation
The problem reduces to a clean combinatorial formula: answer = C(n-1, k) * m * (m-1)^(n-k-1) mod p, where p = 10^9+7.

Core reasoning:
- Exactly k equal adjacent pairs among n-1 positions: choose positions via C(n-1, k).
- This partitions the array into n-k runs. First run: m choices; each subsequent run must differ from previous: (m-1) choices each, giving m * (m-1)^(n-k-1).

Core difficulties / pitfalls:
1. Edge case m = 1: then (m-1)^(n-k-1) = 0^(n-k-1). If k = n-1 (all equal), exponent is 0, so 0^0 = 1 → answer = C(n-1, n-1) * 1 * 1 = 1 (correct: only one array [1,1,...,1]). If k < n-1, answer is 0. Python's pow(0, 0, p) returns 1, and pow(0, positive, p) returns 0, so pow handles this naturally — but must be careful not to special-case incorrectly.
2. k can be 0: C(n-1, 0) = 1, fine.
3. Factorials up to n-1 (max 10^5 - 1), precompute fact and inv_fact arrays of size n.
4. Modular inverse via Fermat's little theorem since p is prime: inv_fact[i] computed from inv_fact[n-1] downward, or pow(fact[i], p-2, p).
5. All multiplications must be mod p to avoid huge numbers (Python handles big ints but mod keeps it fast).
6. Complexity: O(n) precompute + O(log n) exponentiation — well within limits for n ≤ 10^5.

Verification against examples:
- n=3, m=2, k=1: C(2,1)*2*1^1 = 2*2 = 4 ✓
- n=4, m=2, k=2: C(3,2)*2*1^1 = 3*2 = 6 ✓
- n=5, m=2, k=0: C(4,0)*2*1^4 = 2 ✓

## worker: Implement countGoodArrays with formula C(n-1,k) * 
Implemented the closed-form formula: answer = C(n-1, k) * m * (m-1)^(n-k-1) mod p.

Reasoning: choosing which k of the n-1 adjacent positions are equal (C(n-1, k)) determines n-k runs of equal values. The first run has m choices; each subsequent run must differ from the previous, giving (m-1)^(n-k-1) choices.

Implementation details:
- Factorials/inverse factorials precomputed up to n-1 in O(n); inverse factorials derived from pow(fact[n-1], MOD-2, MOD) via Fermat's little theorem (MOD is prime), then filled downward.
- Array size is max(n, 1) so n=1 works (fact[0] used, comb = C(0,0) = 1, answer = m * (m-1)^0 = m).
- Python's pow(0, 0, MOD) == 1 handles m=1, k=n-1 → answer 1; pow(0, positive, MOD) == 0 handles m=1, k<n-1 → answer 0.

Verified against examples:
- n=3, m=2, k=1: C(2,1)*2*1^1 = 4 ✓
- n=4, m=2, k=2: C(3,2)*2*1^1 = 6 ✓
- n=5, m=2, k=0: C(4,0)*2*1^4 = 2 ✓
- Edge: n=1, k=0 → m ✓; m=1, n=5, k=4 → 1 ✓; m=1, n=5, k=2 → 0 ✓

Complexity: O(n) time, O(n) space.
