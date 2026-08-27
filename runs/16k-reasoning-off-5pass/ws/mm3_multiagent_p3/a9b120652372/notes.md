
## ideation
The operation is a "gravitational" pull toward a pivot square: all pieces simultaneously move one step toward the chosen index. Pieces are indistinguishable, multiple pieces can occupy the same square, and the relative order of pieces along the line is preserved (they never pass through each other, but since they're indistinguishable this doesn't restrict matching).

Key observations:
- The total number of pieces is invariant: $\sum A = \sum B$ is necessary.
- We can think of the "leftmost unmatched piece" and "rightmost unmatched piece" gradually being consumed as we sweep left-to-right matching $B$'s ones to $A$'s ones in order.
- For each matched pair (source position $p$, target position $i$):
  - If $p < i$: the piece must move right by $i - p$ steps.
  - If $p > i$: the piece must move left by $p - i$ steps.
  - If $p = i$: 0 steps.
- Since pieces are indistinguishable and can cross (they can occupy the same square temporarily), the greedy left-to-right matching always works.
- The minimum number of operations is the maximum of (max rightward displacement) and (max leftward displacement) — because in a single operation with pivot $i$, we can simultaneously move some pieces left and some right, so the number of ops needed is bounded by the max displacement in either direction.

Algorithm:
1. If $\sum A \ne \sum B$, output $-1$.
2. Build a queue of indices where $A_i = 1$.
3. Sweep $i = 1 \dots N$; whenever $B_i = 1$, pop the front of the queue to get $p$, update `right_max = max(right_max, i - p)` and `left_max = max(left_max, p - i)`.
4. If the queue is non-empty at the end, impossible (shouldn't happen if sums match).
5. Output $\max(\text{right\_max}, \text{left\_max})$.

Pitfalls:
- Forgetting the queue might have leftover pieces (saves an impossible check).
- Off-by-one in indexing (using 0-indexed vs 1-indexed carefully).
- Large input: need fast I/O since total N up to $10^6$ and T up to $2 \times 10^5$.

## worker: Implement the solution in Python with `sys.stdin`/
I implemented the greedy matching algorithm described in the plan. Key points:
- **Feasibility check**: `sum(A) != sum(B)` makes the answer `-1`. If after consuming all `B=1` entries the source queue still has pieces (or empties prematurely), it's also impossible — but this is already covered by the sum check, since equal sums and a proper matching guarantee the queue empties exactly when all `B=1` are matched. The `possible` flag also guards against the edge case where the queue runs out early.
- **Queue**: `collections.deque` with `append` (right) and `popleft` (left) gives O(1) push and pop, matching the sorted order of source positions.
- **Displacement tracking**: For each matched pair `(p, i)` (0-indexed), I compute the signed displacement and update `right_max` (piece moves right) or `left_max` (piece moves left). The final answer is the max of these two, since a single operation with pivot `i` moves left-side pieces right and right-side pieces left simultaneously, so the bottleneck is the larger of the two directions.
- **I/O**: Used `sys.stdin.buffer.read().split()` for fast tokenization and `sys.stdout.write` for batched output, crucial for the constraints (total N up to 10^6, T up to 2×10^5).
- The sample cases are verified mentally: case 1 gives 3, case 2 gives -1 (sum mismatch? no, "010" has sum 1, "111" has sum 3 → mismatch → -1), case 3 gives 5. All consistent.
