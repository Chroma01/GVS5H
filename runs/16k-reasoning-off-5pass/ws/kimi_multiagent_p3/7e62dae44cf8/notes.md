
## ideation
The problem models an expanding connected region (Takahashi) on a grid. At any time, he can absorb any 4-directionally adjacent slime whose strength s satisfies s < cur/X (strictly), i.e., s * X < cur using integers to avoid precision issues (s up to 1e12, X up to 1e9, product up to 1e21 — Python handles big ints natively; in other languages need 128-bit or careful comparison).

Key insight: absorbing any valid slime never hurts — it strictly increases strength and only adds new boundary cells (never removes options). So a greedy that absorbs any currently-absorbable slime is optimal. The process terminates when no boundary slime satisfies the condition.

Efficient frontier management: maintain a min-heap of boundary slime strengths. Repeatedly peek the minimum:
- If min * X < cur: absorb it (cur += s), mark cell visited, push unvisited neighbors onto the heap.
- Else: since the minimum fails, all others fail too → stop.

Each cell is pushed/popped at most a constant number of times (each cell enters the heap once when it becomes boundary), so complexity is O(HW log(HW)), fine for H,W ≤ 500 (250k cells).

Pitfalls:
- Strict inequality: s * X < cur (not ≤). Sample 2: X=1, adjacent slime 10 vs cur 5: 10*1 < 5 false → stop, answer 5. ✓
- Avoid floating point division (cur/X) — precision errors with large values.
- Mark cells visited when pushed to heap to avoid duplicate pushes (a cell could become adjacent via multiple absorbed cells).
- Takahashi's starting cell must be marked visited initially.
- Heap entries should carry position (or we can store (strength, i, j)); stale entries avoided by visited-on-push.
- Strength can grow large: sum up to 250k * 1e12 = 2.5e17, fits in Python int easily.
- Verify with sample 1 logic: start cur=9 at (2,2). Boundary: 6,4,20,15. Min=4: 4*2=8<9 → cur=13. New boundary: 14,17. Min=6: 12<13 → cur=19. New: 9. Min=9: 18<19 → cur=28. New: nothing new ((1,3) neighbors (1,2) visited). Min=14: 28<28 false → stop. Answer 28 ✓.

## worker: Implement solve() in Python: read H, W, X, P, Q an
- Greedy frontier expansion with a min-heap of boundary slimes.
- Absorbing any valid slime strictly increases strength and only adds new boundary cells, so absorbing whenever possible is optimal.
- Min-heap: if the smallest boundary slime fails `s * X < cur`, all others fail too → stop. Otherwise absorb it and push its unvisited neighbors.
- Integer comparison `s * X < cur` avoids floating-point precision issues (values up to 1e12 * 1e9 = 1e21, fine for Python ints).
- Cells are marked visited when pushed, preventing duplicates; each cell enters the heap at most once → O(HW log(HW)) ≈ 250k log 250k, well within limits.
- Verified logic against samples: Sample 1 → 28 (9→13→19→28, then 14*2=28 not < 28, stop). Sample 2 → 5 (10*1 < 5 false immediately). Sample 3 → 1343.
