
## ideation
The core difficulty is that forward simulation requires O(N) shifting per insertion (O(N²) total), which is infeasible for N=5×10⁵. The key insight is to reverse the process: after all insertions, element i sits at position P_i among elements 1..i. So if we process i = N down to 1, in the current "occupied" set (elements 1..i), element i is exactly the P_i-th smallest position. We need an order-statistics structure supporting: (a) find the position of the k-th still-occupied slot, (b) mark that slot empty. A Fenwick tree with binary lifting gives O(log N) per step, O(N log N) total — fine in Python if implemented with tight loops (local variable binding, while-loops). Alternative: a treap/sorted list, but BIT is simplest and most reliable. Pitfalls: 1-indexed BIT; binary lifting must use the largest power of two ≤ N; answer array indexed by position; memory of size N+2 ints is fine; input parsing must be fast (sys.stdin.buffer.read). Edge cases: N=1; P_i = i (append at end) and P_i = 1 (push front) both handled naturally.

## worker: Implement the complete Python solution: fast input
- **Reverse simulation**: After all operations, element `i` occupies position `P_i` among elements `1..i`. Processing `i = N` down to `1`, the current set of occupied positions corresponds exactly to elements `1..i`, so element `i` is at the `P_i`-th occupied slot. We record `ans[pos] = i` and mark that slot empty.
- **Fenwick tree**: Initialized in O(N) with `bit[i] = i & -i` (all slots occupied, each with value 1). Supports:
  - *kth query* via binary lifting in O(log N): find smallest index with prefix sum ≥ k.
  - *removal* via point update `bit[j] -= 1` in O(log N).
- **Complexity**: O(N log N) time, O(N) memory — well within limits for N = 5×10⁵.
- **Sample trace verification** (N=4, P=[1,1,2,1]):
  - i=4, k=1 → 1st occupied = pos 1 → ans[1]=4, remove 1.
  - i=3, k=2 → occupied {2,3,4}, 2nd = pos 3 → ans[3]=3, remove 3.
  - i=2, k=1 → occupied {2,4}, 1st = pos 2 → ans[2]=2, remove 2.
  - i=1, k=1 → occupied {4}, 1st = pos 4 → ans[4]=1.
  - Output: `4 2 3 1` ✓ matches Sample 1. Sample 2 (P_i = i) trivially yields `1 2 3 4 5` since each element lands at the last occupied slot.
