
## ideation
The problem involves inserting elements into an array at specific positions. A naive simulation would be O(N^2) due to array shifts, which is too slow for N up to 5×10^5.

The key insight is to process the operations in **reverse order**.
1.  Consider the final array of size N.
2.  The last operation inserted number `N` at position `P_N`. This means that in the final array, the number `N` is at the `P_N`-th position among the currently "available" slots if we were to reconstruct the array backwards? No, that's not quite right.
3.  Let's rethink: When we insert `i` at `P_i`, it shifts existing elements. If we go backwards from `N` down to `1`, we know that `N` was the last one inserted. So, in the final array, `N` is located at the position that corresponds to the `P_N`-th empty slot if we consider that all slots are initially empty?
    *   Actually, a standard technique for this "insert at position" problem is to determine the final index of each element.
    *   Let's use a Binary Indexed Tree (BIT) or Segment Tree to represent the availability of positions. Initially, all positions `1` to `N` are empty (value 1).
    *   We process `i` from `N` down to `1`.
    *   For each `i`, we want to find the `P_i`-th empty position in the current state of the array. This position is where `i` will end up in the final array.
    *   Once we find this position, we place `i` there and mark that position as occupied (update BIT to 0).
    *   Since we are going backwards, the "empty positions" correspond to the slots that haven't been filled by larger numbers yet. The `P_i`-th empty position is exactly where `i` should be placed in the final array because all numbers `> i` have already been placed, and `i` is inserted before them in the reverse logic?
    *   Let's verify with Sample 1: `P = [1, 1, 2, 1]`. N=4.
        *   Start with BIT representing `[1, 1, 1, 1]` (all empty).
        *   i=4, P_4=1. Find 1st empty pos. It's index 1. Place A[1] = 4. Mark index 1 as occupied. BIT: `[0, 1, 1, 1]`.
        *   i=3, P_3=2. Find 2nd empty pos. Empty indices are 2,3,4. 2nd is 3. Place A[3] = 3. Mark index 3 as occupied. BIT: `[0, 1, 0, 1]`.
        *   i=2, P_2=1. Find 1st empty pos. Empty indices are 2,4. 1st is 2. Place A[2] = 2. Mark index 2 as occupied. BIT: `[0, 0, 0, 1]`.
        *   i=1, P_1=1. Find 1st empty pos. Empty index is 4. 1st is 4. Place A[4] = 1. Mark index 4 as occupied. BIT: `[0, 0, 0, 0]`.
        *   Final Array A: `[4, 2, 3, 1]`. Matches Sample Output 1.

    *   Algorithm:
        1.  Initialize a BIT of size N with all 1s.
        2.  Create an array `ans` of size N+1.
        3.  For `i` from `N` down to `1`:
            a.  Find the `P_i`-th smallest index `j` such that `BIT.query(j) - BIT.query(j-1) == 1` (i.e., the `P_i`-th 1 in the BIT). This can be done with binary lifting on the BIT in O(log N).
            b.  Set `ans[j] = i`.
            c.  Update BIT at `j` by adding -1 (marking as occupied).
        4.  Print `ans[1..N]`.

    *   Complexity: O(N log N) due to N steps, each involving a BIT query/update which is O(log N). This fits within the time limit.

## worker: <none>
The problem requires inserting elements into an array at specific positions, which naively takes O(N^2) time due to array shifts. Given N up to 5×10^5, we need an O(N log N) solution.

The key insight is to process the operations in **reverse order** (from N down to 1). When we consider the final array of size N, the last inserted element `N` was placed at position `P_N`. In the context of the final array, this means `N` occupies the `P_N`-th "empty" slot if we imagine all slots are initially empty and we fill them from the end.

More precisely:
1.  We maintain a data structure (Binary Indexed Tree / Fenwick Tree) that tracks which positions in the final array are still "available" (not yet assigned a number). Initially, all positions 1 to N are available.
2.  For each number `i` from `N` down to `1`, we need to find the `P_i`-th available position. This is because when `i` was inserted, it became the `P_i`-th element among the elements that existed at that time (which are exactly the elements `1` to `i`). In the final array, the positions occupied by numbers `> i` are already determined, and the positions occupied by numbers `≤ i` are the "available" ones. The `P_i`-th available position is where `i` must end up.
3.  We use binary lifting on the BIT to efficiently find the `k`-th available position in O(log N) time.
4.  After placing `i` at the found position, we mark that position as occupied by updating the BIT.

This approach runs in O(N log N) time, which is efficient enough for the given constraints.
