
## ideation
The problem involves moving balls from boxes using two permutation graphs (one for red, one for blue). The goal is to collect all balls into box X. An operation consists of picking a box, moving its red balls to the box indicated by P and its blue balls to the box indicated by Q.

**Core difficulty**: Determining if it's possible to gather all balls into X, and if so, finding the minimum number of operations.

**Key observations**:
- Since P and Q are permutations, each forms disjoint cycles. A ball can reach X only if it starts in the same cycle as X (in its respective color's graph).
- For balls in the correct cycle, moving a ball from box u to X requires picking all boxes along the unique path from u to X (following the permutation). These picks are unavoidable.
- The minimum number of operations equals the number of distinct boxes (excluding X) that lie on at least one such path for either red or blue balls.
- In a cycle, if we list boxes in reverse order from X (following the inverse permutation), the set of boxes needed for a color is exactly the prefix of this list up to the farthest source (ball) in that color.

## worker: Implement the algorithm in Python: compute the cyc
The solution works as follows:
1. For each color (red and blue), the permutation graph consists of disjoint cycles. A ball can reach X only if it starts in the same cycle as X.
2. For balls in the correct cycle, we find the "farthest" ball from X by traversing the cycle backwards (using the inverse permutation). The boxes that must be picked are exactly those on the path from this farthest ball to X.
3. We mark these boxes for each color and count the union (excluding X) to get the minimum number of operations. This works because picking a box moves balls along the unique path, and we can process boxes from farthest to nearest to X, ensuring no unnecessary picks.
