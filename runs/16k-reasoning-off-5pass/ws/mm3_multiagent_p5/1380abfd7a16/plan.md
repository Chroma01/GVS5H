We need to simulate N insertions where element i is inserted at position P_i (1-indexed) into a growing array. A direct list insert at an arbitrary position is O(N) each, leading to O(N²) worst-case, which is too slow for N up to 5·10⁵. The classic trick is to process the operations **backwards**: start with an empty result list, then for i = N down to 1, insert i at position P_i in the current list. Since the list size at step i is N - i + 1, the total work is Σ (N - i + 1) = O(N²) in the worst case, which is still too slow.

A better approach uses a Fenwick tree (Binary Indexed Tree) or a balanced binary indexed structure to locate the actual position in O(log N) per operation, total O(N log N). However, we can also exploit a simpler O(N) method: maintain a doubly linked list of free slots and resolve positions by counting empty slots using a Fenwick tree.

I'll implement the Fenwick-tree method:
- Initially, all N positions are "free". FT stores 1 for each free slot.
- Process i from N down to 1. We need to find the position where after inserting i, the number of free slots before it equals P_i - 1. Using the FT, we binary-search the smallest index `pos` such that prefix sum ≥ P_i. That is the insertion index.
- Set FT[pos] = 0 (occupy it), store result[pos] = i.
- After processing all i, output result in order.

This runs in O(N log N) time and O(N) memory, well within limits.