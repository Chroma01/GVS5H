
## ideation
The problem asks for the maximum final strength of a slime starting at (P,Q) that can repeatedly absorb adjacent slimes whose strength is strictly less than his current strength divided by X. As strength only increases, the condition `s < cur / X` is monotonic: once a slime is absorbable, it stays absorbable, and absorbing it may unlock more. This suggests a greedy approach using a min-heap of currently adjacent slimes: always try to absorb the weakest adjacent slime; if it satisfies the condition, absorb it and push its newly adjacent neighbors. If the weakest adjacent slime does not satisfy the condition, no other can, so stop.

The core difficulty is handling dynamic adjacency (the "gap" is filled) and the condition involving large numbers. The solution is essentially a BFS-like expansion with a priority queue.

Pitfalls:
- Using floating point for the condition `s < cur / X` can cause precision errors. Use integer arithmetic: `s * X < cur` (since all are integers).
- Duplicate heap entries: a cell may be pushed multiple times before being visited. When popping, skip if already visited.
- 1-indexed input must be converted to 0-indexed.
- Strength sum can be up to ~2.5e17, but Python handles big integers natively; in other languages, ensure 64-bit.

## worker: Implement the greedy algorithm with a min-heap to 
The solution uses a greedy approach with a min-heap (priority queue). At each step, we check the weakest adjacent slime. If it satisfies `s * X < cur` (equivalent to `s < cur / X` with strict inequality), we absorb it, increasing `cur` and adding its neighbors to the heap. Because `cur` only grows, once a slime fails the condition, all stronger adjacent slimes will also fail, so we can stop. Duplicate heap entries are handled by checking the `visited` flag when popping. This runs in O(N log N) where N is the number of reachable cells, well within the limits for H, W ≤ 500.
