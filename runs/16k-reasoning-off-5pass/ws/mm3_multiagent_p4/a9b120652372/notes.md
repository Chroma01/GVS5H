
## ideation
**Core difficulty**: The operation moves all pieces one step toward a chosen square `i`. This is equivalent to saying the set of piece positions is a multiset, and in each step the "center of mass" shifts toward `i` while preserving the relative order of pieces (they never cross). So the sorted sequence of positions is preserved up to translation.

**Key insight**: Since pieces can never cross each other, the only possible way to transform the configuration is by a sequence of operations that effectively translates groups of adjacent pieces. The optimal strategy matches the k-th smallest initial position to the k-th smallest target position.

## worker: Extract sorted positions from binary strings A and
The operation moves every piece one step toward the chosen square `i`. Pieces never cross each other, so the sorted order of their positions is preserved. Therefore, a necessary and sufficient condition for reachability is that the number of `1`s in `A` equals the number in `B`. When reachable, the minimum number of operations equals the sum over matched pieces (by sorted order) of the absolute difference of their indices. Each operation moves a piece by at most one step, and grouping by direction per pivot achieves this bound exactly. The sample test cases confirm: 3, -1, 5.
