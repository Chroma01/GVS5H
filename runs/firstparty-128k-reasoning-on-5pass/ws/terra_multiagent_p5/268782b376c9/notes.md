- **Fixed target requirements:** For a target score `x > 0`, index `i` requires `r[i] = ceil(x / points[i])` visits.

- **Critical correction:** The previous checker omitted the mandatory initial move `-1 -> 0`. Feasibility must begin with `moves = 1` and `incoming = 1`. Without this, it incorrectly reports target `4` feasible for `points=[2,4], m=2`; the actual minimum is `3` moves.

- **Left-to-right greedy:** At current index `i < n-1`, suppose it has already received `incoming` visits. If it needs `extra = max(0, r[i]-incoming)` more, perform `extra` cycles `i -> i+1 -> i`, then one final move `i -> i+1`. This costs `2*extra+1` moves and gives index `i+1` exactly `extra+1` incoming visits.

- **Greedy optimality:** Any missing visit at `i` after arriving from the left requires returning to `i` across edge `(i,i+1)`. Each such return necessarily entails a crossing right and a crossing left, costing two moves. The construction uses exactly these forced crossings before advancing permanently, so it is optimal by induction over the prefix.

- **Last position:** Once index `n-1` has `incoming` visits, any additional required visits use bounces `n-1 -> n-2 -> n-1`, each costing two moves.

- **Exact endpoint adjustment:** The canonical construction ends at `n-1`. Its final forward crossing can be deleted exactly when `incoming > r[n-1]` and no last-position bounce is required. Then index `n-1` still has at least its required number of visits, and the walk ends at `n-2`. No larger suffix saving is possible: all earlier required returns are forced by the corresponding prefix requirements.

- **Validated examples:** `[2,4], m=3`, target `4` has requirements `[2,1]` and costs `3`; target `5` is infeasible. `[1,2,3], m=5`, target `2` has requirements `[2,1,1]` and costs `5`.

- **n=2 checks:** Requirements `[100,1]` cost `199`, via initial arrival plus `99` bounces, ending at index `0`; `[1,100]` costs `200`; `[1,1]` costs `2`. These confirm both the required initial move and the one-move endpoint adjustment.

- **Small move budgets:** If `m < n`, no positive target is feasible because each index must be visited at least once and reaching all indices requires at least `n` moves. Binary search correctly returns `0`.

- **Complexity:** Each feasibility test is `O(n)`, with `O(log(m * min(points)))` binary-search iterations and `O(1)` extra space.
