
## ideation
Core difficulty: simulating insertions directly is O(N^2) for N up to 5e5. The key observation is the reverse-process invariant: in the final array, after removing all values greater than i, value i is exactly the P_i-th remaining element. Therefore processing i = N down to 1, we can place i into the P_i-th currently unoccupied final position.

Candidate approaches:
- Fenwick/BIT over positions 1..N initialized as empty; support mark occupied and find kth empty via binary lifting / prefix-sum lower_bound. O(N log N), simple and robust.
- Order-statistics tree / balanced BST of empty positions; same asymptotics but more implementation overhead in Python.
- sqrt decomposition over position blocks; possible O(N sqrt N), likely unnecessary and riskier.
- Direct list insertion is conceptually simple but too slow.

Pitfalls: 1-indexed positions and P_i; “kth empty” must mean among still-unassigned final slots, not current dynamic array; ensure Fenwick find_kth returns the smallest index with prefix sum >= k; handle P_i = i append case and P_i = 1 front-insert case; use fast input/output; avoid recursion limits and avoid storing huge intermediate strings.

## worker: Implement the complete Python solution using a Fen
Processes insertions in reverse. In the final array, after deleting all values greater than `i`, value `i` is exactly the `P_i`-th remaining element, because later insertions never reorder already-inserted smaller values. So for `i = N ... 1`, place `i` into the `P_i`-th currently empty final position.

A Fenwick tree stores which final positions are still empty (`1`) or occupied (`0`). `find_kth` uses binary lifting to locate the `k`-th empty slot, and `occupy` marks it used. Each operation is `O(log N)`, giving `O(N log N)` total time and `O(N)` memory, suitable for `N <= 5e5`.
