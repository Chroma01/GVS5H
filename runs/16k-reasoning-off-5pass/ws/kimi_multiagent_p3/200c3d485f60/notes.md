
## ideation
The plan is already correct: the answer is m * C(n-1, k) * (m-1)^(n-1-k) mod p. Reasoning: pick arr[0] in m ways; among the n-1 adjacent transitions, choose which k are "equal" (C(n-1,k)); each "different" transition has m-1 choices. Core implementation difficulty is doing this efficiently for n up to 1e5: precompute factorials and inverse factorials up to n-1 in O(n), then one pow for (m-1)^(n-1-k). Pitfalls: (a) m=1 edge case — (m-1)=0, so 0^(n-1-k): Python's pow(0, 0, p) returns 1, and pow(0, positive, p) returns 0, which correctly yields 1 only when k=n-1, so no special-casing needed, but worth verifying; (b) k can be 0 up to n-1, factorial array size n suffices; (c) use modular inverse via Fermat's little theorem (pow(fact[n-1], p-2, p)) then downward loop for inv_fact; (d) all multiplications must be taken mod p to avoid big-int slowdown (Python handles big ints but mod keeps it fast); (e) n=1 means zero transitions, k must be 0, formula gives m * C(0,0) * (m-1)^0 = m — correct.

## worker: Implement and verify the full solution: closed-for
- Formula: choose arr[0] in m ways; choose which k of the n-1 adjacent transitions are "equal" in C(n-1, k) ways; each of the remaining n-1-k "different" transitions has m-1 choices. Answer = m * C(n-1, k) * (m-1)^(n-1-k) mod p.
- Precompute factorials O(n), inverse factorials via Fermat inverse of fact[n-1] then a downward pass O(n); binomial is O(1). Total O(n) time, O(n) space — fine for n ≤ 1e5.
- Hand-verification:
  - Example 1: n=3, m=2, k=1 → 2 * C(2,1) * 1^1 = 2*2*1 = 4 ✓
  - Example 2: n=4, m=2, k=2 → 2 * C(3,2) * 1^1 = 2*3*1 = 6 ✓
  - Example 3: n=5, m=2, k=0 → 2 * C(4,0) * 1^4 = 2 ✓
  - Edge n=1, k=0: m * C(0,0) * (m-1)^0 = m ✓ (arrays of size 1)
  - Edge m=1, k=n-1: 1 * C(n-1,n-1) * 0^0 = 1 ✓ (all-ones array)
  - Edge m=1, k<n-1: factor 0^(positive) = 0 → 0 ✓
- Python's three-argument pow handles the 0^0 = 1 and 0^positive = 0 cases exactly as needed, so no special-casing is required.
