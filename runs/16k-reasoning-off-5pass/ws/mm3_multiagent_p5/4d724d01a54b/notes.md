
## ideation
The operation swaps adjacent elements with cost equal to the left index (1-indexed). We need the minimum total cost to sort the permutation.

- Core difficulty: Choose a sequence of adjacent swaps (each costing the left index) that sorts the array. The cost of swapping an element leftward by `k` steps is the sum of the indices it passes over.
- Equivalent view: Process elements from N down to 1. To place value `v` at its target index `v`, we need to move it left past all elements currently in positions `[v, pos-1]`, where `pos` is its current position. The cost contributed is sum of indices `v, v+1, ..., pos` (1-indexed) = `(v+pos)*(pos-v+1)/2`.
- Need to efficiently know the current position of each value after previous larger values have been moved. Use a Binary Indexed Tree (Fenwick) to mark which positions are still "free" (i.e., not yet occupied by a correctly placed larger element). Then the current position of value `v` is the number of free positions `≤ pos`, but it's easier: maintain a BIT over initial positions; as we place values, we remove that position from the BIT. For value `v`, its current position `pos` is the index where it resides in the original array, but we need its current rank among remaining elements. We can query: `pos = query(pos_in_original)` returns the current rank (number of unfilled positions ≤ original position). Then compute contribution.
- Summing all contributions yields the answer.
- Edge case: if already sorted, all contributions are 0.
- Complexity: O(N log N), works for N up to 2e5.

Pitfalls:
- Use 1-indexed BIT for simplicity.
- Compute sum of arithmetic series using integer arithmetic; watch for overflow in Python (not an issue, but be careful with formula).
- After placing `v`, mark its original position as filled in BIT.

## worker: Implement the solution using a Fenwick tree to tra
The solution processes values from N down to 1. For each value v, it finds the current position (rank) of v among the remaining (not yet placed) elements using a Fenwick tree. This is done by querying the prefix sum at the original position of v. Since all values greater than v are already placed at their final positions, the target rank for v is simply v. The cost to move v to its target is the sum of consecutive integers from min(cur, v) to max(cur, v)-1. After computing the cost, we remove v's original position from the Fenwick tree. The total time complexity is O(N log N).
