
## ideation
We need to find the minimum total cost to sort a permutation using adjacent swaps where swapping at position i (swapping elements at i and i+1) costs i. The cost depends on the index where the swap is performed, not the values.

Key observations:
- The greedy approach of processing values 1..N and moving each to its correct position works optimally. Since all costs are positive and we never need to move a smaller value rightwards (it only increases cost).
- For value v, suppose its current position is cur (≥ v). It needs to move left by (cur - v) steps, paying costs (v) + (v+1) + … + (cur-1). The total cost for this move is the arithmetic sum of those indices.
- We need an efficient way to track the current positions of values as earlier moves shift them. A Fenwick tree (BIT) over the array stores 1 at each "free" position. When we move v from cur to v, we remove the free slot at cur and add one at v (or equivalently update the BIT).
- To find the current position of v, we can use a "find_kth" operation on the BIT: find the position with a given prefix sum (specifically, the position of the v-th free slot). This works because we process in order and fill positions 1..N as we go.

Algorithm:
1. Initialize BIT with N ones (all positions free).
2. For v = 1 to N:
   - Find the position cur = find_kth(v) — the v-th free slot.
   - Compute steps = cur - v.
   - Add cost = steps * (v + cur - 1) // 2 to total answer.
   - Update BIT: add -1 at cur (remove the free slot) and +1 at v (add free slot) — though v's position is already filled by the current move, the standard approach is just to remove cur and keep the invariant that positions ≤ v become unavailable gradually. Actually, we can just mark position cur as used: BIT.add(cur, -1). Since we are filling from left to right, the v-th free slot is always ≥ v, and we fill the current position.
3. Output the total cost.

Alternative simpler view: after processing values 1..v-1, the first v-1 positions are occupied. So the current position of v is exactly the v-th empty slot. Using BIT to maintain empty slots gives O(N log N) total.

Edge cases:
- When cur == v, steps = 0, cost = 0.
- N up to 2*10^5, cost fits in 64-bit (max cost roughly N^2/2 ≈ 2*10^10, fits in 64-bit).

The greedy proof: any sequence of adjacent swaps that sorts the array can be transformed so that value 1 is moved to position 1 using only swaps at positions 1,2,...,(pos(1)-1), paying minimal sum. Then inductively the same holds for the rest, because moving a smaller value left never requires a larger value to move right (which would cost more). The arithmetic sum of consecutive integers gives the exact cost.

## worker: Implement the BIT-based algorithm in Python: read 
The algorithm uses a Fenwick tree (Binary Indexed Tree) to maintain the set of "free" positions. Initially all N positions are free. When we process value `v` from 1 to N:

1. We find the current position of `v` by locating the `v`-th free slot in the BIT. This works because after processing values `1..v-1`, the first `v-1` positions are occupied, so the `v`-th free slot is exactly where `v` currently resides.

2. The element must move from `cur` to its target position `v`, requiring `steps = cur - v` leftward adjacent swaps. The cost of these swaps is the sum of indices `v + (v+1) + ... + (cur-1)`, computed in O(1) via the arithmetic series formula.

3. We update the BIT: remove the free slot at `cur` (since that position is now empty after `v` leaves) and add a free slot at `v` (the destination). This correctly maintains the invariant for subsequent values.

The total complexity is O(N log N), and the maximum cost (roughly N²/2 ≈ 2×10¹⁰) fits comfortably in 64-bit integers. The greedy approach is provably optimal because moving a smaller value leftward via the cheapest available swaps never forces a larger value to move rightward (which would be more expensive).

## worker: Write a complete, correct Python solution: impleme
The solution uses a Fenwick tree to maintain the count of free slots. For each value `v` (processed in order 1..N), its current position is computed as `cur = v - 1 + bit.sum(pos[v])`, which correctly accounts for the fact that the first `v-1` positions are already occupied by smaller values. The cost to move `v` leftwards from `cur` to `v` is the sum of indices `v + (v+1) + ... + (cur-1)`, computed in O(1) via the arithmetic series formula. The original position is then marked as filled in the BIT. This greedy approach is optimal because any optimal sorting sequence can be rearranged so that each value `v` is moved leftwards using the cheapest possible swaps without ever requiring a smaller value to move rightwards. The total complexity is O(N log N), and Python's arbitrary-precision integers safely handle the maximum cost (~2×10¹⁰).

## worker: Write a complete, correct Python solution with Fen
- Uses a Fenwick tree to track free (unfilled) positions. Initially all N positions are free.
- For each value `v` from 1 to N, its current position is computed as `(v-1) + bit.sum(pos[v])`, which equals the number of already-fixed positions to its left plus the number of free slots up to its original index. This works because when we process values in increasing order, the first `v-1` positions become occupied.
- The cost to move `v` leftward from `cur` to `v` is the arithmetic sum `v + (v+1) + ... + (cur-1)`, computed in O(1) via `steps * (v + cur - 1) // 2`.
- After moving `v`, we mark its original position as no longer free (`bit.add(pos[v], -1)`). The destination position `v` is already accounted for in the `(v-1)` filled slots for the next iteration.
- The greedy approach is provably optimal: any optimal sorting sequence can be rearranged so that each value `v` is moved leftward using the cheapest possible adjacent swaps, never requiring a smaller value to move rightward (which would be more expensive).
- Complexity: O(N log N) time and O(N) memory. The maximum cost (~N²/2 ≈ 2×10¹⁰) fits in Python's arbitrary-precision integers.
- Verified against the three samples: produces 4, 6, and 0 respectively.
