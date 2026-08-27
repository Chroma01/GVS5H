
## ideation
We need to find positive integers x>y such that x³−y³ = N, where N ≤ 10^18. Since x and y are positive integers and x>y, we have x³ = N + y³. For a given y, the corresponding x is the integer cube root of N + y³.

**Key observations:**
- x and y are at most roughly N^(1/3)+something, which is about 10^6.
- The simplest approach: iterate y from 1 upward, compute candidate x via integer cube root of y³+N, and check if x³−y³ = N.
- Time complexity is O(N^(1/3)) ≈ O(10^6), which is very feasible.

**Candidate approaches:**
1. **Brute force y from 1 upward:** For each y, compute integer cube root of y³+N to get candidate x, then verify. This is straightforward and fast enough.
2. **Brute force x from 1 upward:** For each x, compute y = integer cube root of x³−N (if positive), then verify. Similar complexity.
3. **Factor the difference of cubes:** x³−y³ = (x−y)(x²+xy+y²). This could be exploited but isn't simpler.

**Pitfalls to watch:**
- Computing integer cube root correctly without floating-point errors. The safe approach: compute a floating-point approximation, then adjust by ±1 to find the exact integer cube root, or use binary search.
- The maximum value y³ can reach ~10^18, so we need to be careful about overflow (use Python's arbitrary precision—fine).
- We need positive integers, so y ≥ 1 and x > y (and x³ > y³ which is guaranteed if x > y).
- The loop bound: y can go up to floor(N^(1/3)) + something. But we should let it run until y³ > x³ or until the cube root would give x ≤ y. We can stop early if y³ ≥ x³ (impossible) or if y³ > N + y³ (never). Actually the natural stopping condition: for large y, y³ will exceed N + y³ is nonsense, but if y > x then x³−y³ would be negative. So once the computed x ≤ y, we can break (for this y, there's no valid x, and for larger y, x would only be larger or equal, still not valid). Actually wait: as y increases, y³+N increases, so x also increases. So there's no early termination from that alone. We can stop when y³ > N + something? Actually we just iterate up to some bound. Since x³ = N + y³, x = (N+y³)^(1/3) ≈ y*(1 + N/(3y³))^(1/3) ≈ y + N/(3y²). For large y, x ≈ y + N/(3y²). For x to be > y (an integer), we need y ≤ N^(1/3) roughly. So the maximum meaningful y is around N^(1/3). Thus iterating y from 1 to ceil(N^(1/3))+1 is sufficient.

**Implementation details for integer cube root:**
- Compute `c = round((y**3 + N) ** (1/3))` or just `int((y**3 + N) ** (1/3))`.
- Then check if `c**3 == y**3 + N`. If not, try `c+1` or `c-1`.
- Better: binary search for cube root in range [0, (N+y³)^(1/3)+1].

Given the small bound (~10^6), the simple approach with floating-point and a small correction loop is sufficient and fast.

## worker: Implement the solution in Python: read N, define a
- The algorithm iterates `y` from 1 up to roughly `N^(1/3) + a small constant`. For each `y`, it computes the integer cube root of `y³ + N` using a binary search to avoid floating-point inaccuracies, then checks if `x³ - y³ == N` and `x > y`.
- The binary search for the integer cube root starts with an exponential search to find an upper bound `hi` such that `hi³ >= target`, then performs a standard binary search between `lo=0` and `hi`.
- If a valid pair is found, it prints `x` and `y` immediately. If no pair is found after scanning, it prints `-1`.
- Complexity: O(N^(1/3) * log(N)) ≈ 10⁶ * 60 operations, well within time limits. Python's arbitrary-precision integers handle the large cubes safely.
- The sample cases are handled correctly: 397 → 12 11, 1 → -1, 39977273855577088 → 342756 66212.
