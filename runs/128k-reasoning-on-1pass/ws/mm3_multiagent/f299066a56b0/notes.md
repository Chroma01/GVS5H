
## ideation


## worker: **Read input** – parse `N` and the sorted list `A`
- The problem reduces to finding the maximum number of disjoint pairs \((a,b)\) with \(a \le b/2\).
- Because the mochi sizes are sorted, a greedy two‑pointer strategy is optimal:
  - Use the smallest still‑unused mochi as the top.
  - Pair it with the smallest unused mochi that satisfies the size condition.
  - This never wastes a larger bottom that could be needed for a smaller top later.
- The algorithm runs in \(O(N)\) time and \(O(1)\) extra memory, easily handling \(N \le 5\cdot10^5\).
- The condition `A[j] < 2 * A[i]` uses Python's arbitrary‑precision integers, avoiding overflow.
