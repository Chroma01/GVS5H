
## ideation
**Core difficulty:** Simulating `N` insertions into an array where each insertion `i` is placed at position `P_i` (1-indexed). Naively using `list.insert` gives `O(N^2)` time, too slow for `N ≤ 5·10⁵`.

**Key insight:** Process insertions **in reverse** (from `N` down to `1`). When inserting `i` backwards, we are essentially deciding which final position (among `N` slots) the number `i` occupies. At step `i` (going backwards), there are exactly `i` empty slots left, and we must place `i` into the `P_i`-th empty slot from the left.

**Data structure:** A Fenwick tree (Binary Indexed Tree) storing for each position whether it is still empty (1) or already filled (0). Supports:
- `update(pos, -1)` to mark a slot as filled.
- `find_kth(k)` to locate the index of the `k`-th 1 (i.e., the `k`-th empty slot) in `O(log N)`.

**Algorithm outline:**
1. Read `N` and `P[1..N]`.
2. Build BIT of size `N` initialized to all 1’s (all slots free).
3. For `i = N, N-1, …, 1`:
   - Find `pos = find_kth(P[i])` → the `P_i`-th free slot.
   - `BIT.add(pos, -1)`.
   - `result[pos] = i`.
4. Print `result`.

**Complexities:** `O(N log N)` time, `O(N)` memory.

**Pitfalls to watch:**
- `P_i` is 1-indexed; BIT find_kth must be implemented correctly for 1-indexed `k`.
- Ensure `find_kth` handles the case `k = current_total` (largest valid `k`).
- Use fast I/O (`sys.stdin.buffer.read`) for `N = 5·10⁵`.
- Python recursion not needed; iterative BIT is fine.
- Beware of off-by-one: BIT indices are 1..N, same as slot positions.

## worker: Implement the Fenwick tree-based solution in Pytho
- The problem asks to simulate inserting `i` at position `P_i` (1-indexed) for `i = 1..N`.
- Processing in reverse allows us to map each `i` to a final slot: when we are at step `i` going backwards, there are exactly `i` empty slots, and we place `i` in the `P_i`-th empty slot from the left.
- A Fenwick tree (Binary Indexed Tree) stores `1` for empty slots and `0` for filled ones, supporting `O(log N)` range-sum queries and point updates.
- `find_kth(k)` uses the standard binary lifting on the BIT to locate the `k`-th `1` in `O(log N)`.
- The BIT is initialized in `O(N)` by setting `bit[i] = i & -i` (the classic way to build a BIT with all ones).
- Total complexity is `O(N log N)` with `O(N)` memory, well within constraints for `N ≤ 5·10⁵`.
- Fast I/O via `sys.stdin.buffer.read` is used to avoid slowdown.
