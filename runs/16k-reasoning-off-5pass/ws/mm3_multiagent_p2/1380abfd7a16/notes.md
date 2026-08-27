
## ideation
We need to build an array by inserting each integer `i` (1..N) at position `P_i` of the growing array. Direct `list.insert` is O(N) each, total O(N^2) → too slow for N up to 5e5.

Key observation: If we process insertions in **reverse order** (from i=N down to 1), each step we are placing `i` into a currently empty slot of a final array of size N. The number of empty slots decreases by 1 each step. We must pick the `P_i`-th empty slot (1-indexed) because all later elements (i+1..N) have already been placed and occupy the first part of the array according to the reversed process. This is a classic problem: dynamic order-statistics on a set of free positions.

Data structure options:
- Balanced BST (e.g., `bisect` on sorted list) → O(N^2) in worst case.
- Fenwick Tree / BIT (Binary Indexed Tree) or Segment Tree: store 1 for each free position, 0 for occupied. Find the P_i-th free slot via binary search on prefix sums in O(log N). Update: set the chosen slot to 0 (O(log N)). Total O(N log N) which is fine for 5e5.

Algorithm steps:
1. Read N and the array P[1..N] (1-indexed in description; convert to 0-indexed list in code).
2. Initialize a BIT of size N with all ones (all N positions initially free).
3. Allocate result array `ans` of length N.
4. For i from N down to 1:
   - Use BIT to find the index `pos` of the P_i-th free slot (smallest index such that prefix sum >= P_i).
   - Assign `ans[pos] = i`.
   - Update BIT at `pos` to 0 (subtract 1).
5. Print `ans` separated by spaces.

Implementation details for Fenwick:
- `add(idx, delta)`: standard.
- `sum(idx)`: prefix sum.
- `find_kth(k)`: binary search using bit length. Implementation:
  ```
  pos = 0
  bit_mask = highest power of 2 <= N
  while bit_mask:
      nxt = pos + bit_mask
      if nxt <= N and tree[nxt] < k:
          k -= tree[nxt]
          pos = nxt
      bit_mask >>= 1
  return pos + 1
  ```
  Here `tree[nxt]` is the BIT cumulative array; note that in BIT, `tree[i]` stores sum of a specific range, so the condition `tree[nxt] < k` works for the standard fenwick implementation (cumulative addition). Actually the standard fenwick find uses `if nxt <= N and bit[nxt] < k`. Verify: Yes, because `bit[nxt]` is the sum of the last `lowbit(nxt)` elements. The standard approach works.

Edge cases:
- N=1.
- P_i always equals i → final array is 1,2,...,N.
- P_i always 1 → final array is N, N-1, ..., 1.

Complexities: O(N log N) time, O(N) memory.

Pitfalls:
- Must use 1-indexed BIT internally; the resulting `pos` is 0-indexed for ans array.
- Use `sys.stdin.buffer.read` for fast input due to N up to 5e5.
- Print using `' '.join(map(str, ans))` for speed.

## worker: Implement the Fenwick tree based solution in Pytho
- Implemented the reverse-insertion method using a Fenwick tree (Binary Indexed Tree) for order-statistic queries in `O(log N)`.
- All N positions start free (value 1 in BIT). For each `i` from N down to 1, we find the `P_i`-th free slot via `find_kth`, place `i` there, and update the BIT to mark the slot occupied.
- Input parsing uses `sys.stdin.buffer.read` for speed; output uses `join` on the result list.
- The BIT is built with the standard `add` logic in the initialization loop, giving `O(N)` build time.
- Verified mentally with the samples:
  - Sample 1 (`N=4`, `P=[1,1,2,1]`) yields `[4,2,3,1]`.
  - Sample 2 (`N=5`, `P=[1,2,3,4,5]`) yields `[1,2,3,4,5]`.
- Complexity: `O(N log N)` time, `O(N)` memory, suitable for `N ≤ 5×10^5`.
