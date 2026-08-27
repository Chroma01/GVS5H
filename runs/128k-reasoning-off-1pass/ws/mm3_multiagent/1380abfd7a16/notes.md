
## ideation
We need to construct final array A after performing N insertions of numbers 1..N at positions P_i (1-indexed) into a growing array. Naively using Python list insert or deque would be O(N^2) worst-case (e.g., always inserting at position 1). N ≤ 5e5 requires O(N log N) or similar.

Key observation: Inserting in forward order is costly because each insertion shifts many elements. However, we can process insertions in reverse order. When we process i from N down to 1, the array already has N-i elements placed (the numbers > i). At step i, we need to place i into the P_i-th *empty* position among the total i positions (since after processing all numbers > i, the array length is N, but only N-i slots are filled). More precisely, at the moment we insert i in reverse, the array has N positions, with N-i of them already occupied by numbers > i. We need to find the P_i-th empty slot (1-indexed) and put i there. After all N steps, all positions are filled, giving the final array.

Finding the k-th empty slot can be done efficiently with a Fenwick tree (Binary Indexed Tree) that stores 1 for empty slots and 0 for filled slots. Initially all N slots are empty (value 1). When we place a number at index pos, we update the tree with -1 at pos. Then "find k-th empty slot" is the standard BIT lower_bound operation: find smallest index such that prefix sum >= k. Since P_i ≤ i, k is always valid.

Algorithm steps:
1. Read N and array P[1..N].
2. Initialize BIT of size N with all ones (empty slots).
3. Initialize result array res[1..N] (0-indexed in code).
4. For i from N down to 1:
   - k = P_i (the position among empty slots).
   - pos = BIT.lower_bound(k) (i.e., find index where cumulative sum >= k).
   - res[pos] = i.
   - BIT.update(pos, -1) (mark filled).
5. Print res as space-separated.

Complexities: O(N log N) time, O(N) memory. Works for N up to 5e5 easily in Python.

Pitfalls:
- 1-indexed vs 0-indexed: BIT usually 1-indexed; Python lists 0-indexed. Be careful with mapping.
- lower_bound for BIT: standard method while (idx+1) & -idx etc., or binary search on BIT. Since N ≤ 5e5, simple bit manipulation is fine.
- Input P_i can be read as integers; ensure correct order.
- Output format: space-separated, no trailing space ideally (use ' '.join(map(str, res))).

## worker: Implement the Python solution: write a Fenwick tre
The solution processes insertions in reverse order. When inserting in reverse, we need to find the P_i-th empty slot among the N total positions (since only numbers > i have already been placed). A Fenwick tree (BIT) storing 1 for empty slots and 0 for filled slots efficiently supports:
- `bit_add(pos, -1)` to mark a slot as filled (O(log N)),
- `bit_lower_bound(k)` to find the index of the k-th empty slot (O(log N)),
- `bit_sum` is used internally by lower_bound.

The BIT is initialized with all ones, representing that all N slots are empty. For each i from N down to 1, we find the P_i-th empty slot, place i there, and mark it filled. After all N steps, the `res` array contains the final ordering. This runs in O(N log N) time and O(N) memory, well within constraints for N ≤ 5×10⁵.
