
## ideation
Core difficulty: naive list insertion is O(N) per operation → O(N²), too slow for N=5×10^5. Need O(N log N).

Key insight (reverse processing): Process i from N down to 1. When inserting i, all elements j>i are already placed. In the final array, element i must have exactly P_i-1 elements before it — but wait, careful: elements inserted later (j>i) may be inserted before or after i, shifting it. The standard correct formulation: process in reverse, and insert i into the sequence of "remaining slots" such that exactly P_i-1 of the elements {i+1..N} that end up before it... Actually the clean way: think of N final slots. Process i=N down to 1; at each step, i occupies the P_i-th currently-free slot (counting from left). This is correct because when i was inserted (forward), exactly P_i-1 elements (all from {1..i-1}) were before it, and those smaller elements are precisely the ones not yet placed in reverse — they will fill the free slots. So i takes the P_i-th smallest free position.

Implementation: Fenwick tree (BIT) of size N, initially all 1s (all slots free). For i from N down to 1: find the smallest index pos such that prefix_sum(pos) = P_i (i.e., the P_i-th free slot) via BIT binary lifting in O(log N); set answer[pos]=i; then update BIT at pos by -1 (mark occupied).

Pitfalls:
- BIT find-by-order must use binary lifting (largest idx with prefix sum < P_i, then answer is idx+1).
- 1-indexed BIT; careful with off-by-one.
- Fast I/O needed (sys.stdin.buffer).
- Alternative approaches: implicit treap / splay with split-merge (forward simulation), or sortedcontainers — but BIT reverse method is simplest and safest.
- Memory: arrays of size N+1, fine.

## worker: Write the complete Python program: parse input wit
- Reverse-processing correctness: when element `i` was inserted (forward pass), exactly `P_i - 1` elements were before it, and all of them belong to `{1..i-1}` (since only elements `1..i-1` existed). Processing `i` from `N` down to `1`, the already-placed elements are exactly `{i+1..N}`; the free slots will be filled by `{1..i-1}`. So `i` must occupy the `P_i`-th free slot from the left, guaranteeing exactly `P_i - 1` smaller elements before it in the final array. Induction over the reverse loop gives the final array.
- Fenwick tree initialized with all slots free (`bit[i] = i & -i` builds it in O(N)). `find_kth` uses binary lifting to locate the `k`-th free slot in O(log N); `add(pos, -1)` marks it occupied.
- Complexity: O(N log N) time, O(N) memory — fine for N = 5×10^5. Fast I/O via `sys.stdin.buffer`.
- Edge cases: N=1 works (LOG=1, find_kth(1) returns 1). P_i = i (append at end) and P_i = 1 (prepend) both handled naturally.
