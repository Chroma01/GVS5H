
## ideation
The core difficulty is deciding the order of absorptions, since absorbing changes both strength and the frontier (adjacent cells). The key insight is that absorbing any absorbable cell is always beneficial: strength strictly increases and the frontier only expands (the absorbed cell's neighbors become adjacent). So the set of eventually-absorbable cells is uniquely determined — we just need to simulate the closure.

A clean way to simulate: maintain a max-heap of frontier cell strengths. Pop the strongest frontier cell. If even the strongest frontier cell is NOT absorbable (S * X >= current strength), then no frontier cell is absorbable, and since strength can no longer increase, the process terminates. If it is absorbable, absorb it, add its strength, and push its unvisited neighbors. This greedy is correct because absorbability is monotone in current strength, and the strongest frontier cell is the "hardest" one — if it fails, all fail.

Pitfalls:
- Condition is strict: absorb iff S < strength/X, i.e., S * X < strength (integer arithmetic, no floats). S up to 1e12, X up to 1e9 → product up to 1e21; Python handles big ints natively, but in other languages need 128-bit or careful comparison.
- Grid up to 500x500 = 250,000 cells; heap operations O(N log N) fine.
- Must mark cells visited when pushed to avoid duplicates in heap.
- Strength sum can reach 250,000 * 1e12 = 2.5e17 — fits in Python int easily.
- Edge case X=1: condition S < strength, strict — sample 2 confirms nothing absorbable when equal.
- Starting cell (P,Q) is Takahashi; mark visited, initial strength = S[P][Q], push its neighbors.

## worker: finalize
- **Model**: The absorbed region grows from (P,Q). At any moment, Takahashi can absorb any cell adjacent to the region (4-neighborhood) whose strength `s` satisfies `s * X < current_strength` (strict inequality, equivalent to `s < strength/X` using exact integer arithmetic — avoids floats; `s*X` can be up to 1e21, fine for Python ints).
- **Greedy correctness**: Absorbing any absorbable cell strictly increases strength and only expands the frontier (the absorbed cell's other neighbors become adjacent). Hence absorbing is never harmful, and the final reachable set is unique. To find *some* absorbable frontier cell efficiently, keep a max-heap of frontier strengths and check the strongest one: if even the strongest fails (`s * X >= strength`), all frontier cells fail, and since strength can no longer increase, no cell will ever become absorbable — terminate. If it passes, absorb it and push its unvisited neighbors.
- **Visited marking on push** prevents duplicate heap entries; each cell is pushed at most once → O(HW log(HW)) time, O(HW) memory. With H,W ≤ 500 (250k cells), this is fast.
- **Edge cases**: X=1 requires strictly smaller strength (sample 2: equal-strength neighbors can't be absorbed). Single-cell grids yield no frontier. Total strength ≤ 2.5e17 fits easily in Python int.
- Verified logic against samples: sample 1 → 28 (9→13→19→28; next frontier strongest is 14 with 14*2=28 ≥ 28, stop), sample 2 → 5, sample 3 → 1343.
