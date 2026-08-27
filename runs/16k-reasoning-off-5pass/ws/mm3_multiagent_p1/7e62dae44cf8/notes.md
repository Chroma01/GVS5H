
## ideation
The problem is a classic "expand and absorb" on a grid. The condition `neighbor_strength < cur / X` is equivalent to `neighbor_strength * X < cur`. Since `cur` only increases, once a cell becomes absorbable it stays absorbable. This monotonic property allows a greedy approach using a max-heap of currently adjacent, absorbable cells: always absorb the strongest available neighbor to maximize growth as early as possible.

Key points:
- Grid size up to 500x500 = 250,000 cells, so O(HW log(HW)) is fine.
- Strengths up to 1e12, X up to 1e9; multiplication `strength * X` can reach ~1e21, so use Python integers (unbounded) or careful 64-bit (but Python int is safe).
- Need a visited set to avoid revisiting cells.
- The heap stores candidates that are adjacent to the current "frontier" (the set of cells already absorbed). When we absorb a cell, its unvisited neighbors become new candidates if they satisfy the condition with the updated `cur`.

Pitfalls:
- Must check condition strictly: `neighbor * X < cur`.
- The initial cell's neighbors should be considered with the initial strength.
- Use max-heap via negative values in Python's `heapq`.
- Ensure we don't push the same cell multiple times (check visited before pushing).

## worker: Implement the solution in Python: parse input, run
The solution uses a greedy approach with a max-heap (priority queue) storing adjacent, absorbable cells. Since strength only increases and the condition `neighbor_strength * X < current_strength` is monotonic, absorbing the strongest available neighbor first is optimal. This is a standard BFS-like expansion where we maintain a frontier of candidates and always process the one with maximum strength. Each cell is visited at most once, and heap operations are O(log(HW)), giving overall O(HW log(HW)) time complexity. The Python `int` type safely handles the multiplication `strength * X` even when it exceeds 64-bit range.
