
## ideation
The problem reduces to: given N cost coefficients \(P_i\), maximize \(\sum k_i\) subject to \(\sum k_i^2 P_i \le M\), with each \(k_i \ge 0\) integer.  
Because the cost per unit of buying the next unit from product i is \((2k_i+1)P_i\) (increase from \(k_i^2 P_i\) to \((k_i+1)^2 P_i\)), the marginal cost is strictly increasing and linear in \(P_i\).  

Thus the greedy “always buy from the cheapest available product” is optimal: at any step, the next unit bought should come from the product with the smallest marginal cost, which is the product with the smallest \(P_i\) among those we have not exhausted (since \((2k+1)P\) is monotonic in \(P\) for fixed \(k\)).  

Hence the algorithm:
1. Sort \(P_i\) in non‑decreasing order.
2. Iterate through sorted list, keep a remaining budget `rem` (initially `M`).
3. For current \(P\), compute the maximum integer \(x\) such that \(x^2 P \le rem\); this is `x = floor(sqrt(rem // P))`.
4. Add `x` to the answer, subtract `x**2 * P` from `rem`, continue.
5. If at some point `rem` becomes 0, we can break early (cannot buy more).

Pitfalls:
- When \(P\) is tiny, `rem // P` can be as large as \(10^{18}\), so `sqrt` of that is up to ~\(10^9\); Python’s `math.isqrt` handles big integers safely.
- Total answer can be up to about \(\sqrt{M / P_{min}} \approx 3\cdot10^8\) per product, and across N up to ~\(6\cdot10^{13}\), still fits in Python int.
- Must be careful with integer division: `rem // P` is safe; using `int(math.sqrt(rem // P))` can overflow precision; use `math.isqrt`.
- Complexity: sorting dominates, \(O(N \log N)\). Scanning is \(O(N)\) because each product is processed at most once.
- Early termination when `rem` reaches 0 or when \(P > rem\) (since then even 1 unit costs > rem) is fine but not necessary.

Edge cases: N=1, M very large, \(P_i\) up to \(2\cdot10^9\), product of \(k^2 P\) may exceed 64‑bit; Python int is fine.

## worker: finalize
The greedy algorithm works because the marginal cost of buying the next unit from product \(i\) is \((2k_i+1)P_i\), which is strictly increasing in both \(k_i\) and \(P_i\). Therefore, at any step the cheapest next unit always comes from the product with the smallest \(P_i\) among those not yet exhausted. Sorting the costs and repeatedly buying as many units as possible from the cheapest product yields the optimal total number of units.

Implementation details:
- Use `math.isqrt` for integer square root to avoid floating‑point inaccuracies.
- Early exit when the remaining budget becomes zero or when the current price exceeds the remaining budget (since the list is sorted, no later product can be bought either).
- All arithmetic uses Python's arbitrary‑precision integers, so overflow is not a concern.

Complexity: \(O(N \log N)\) for sorting, \(O(N)\) for the scan, with \(N \le 2\cdot10^5\).
