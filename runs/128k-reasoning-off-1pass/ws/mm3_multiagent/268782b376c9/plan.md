We need to maximize the minimum final score across all positions after at most `m` moves starting from index -1. Each move visits a position and adds `points[i]` to its score, so the score of index `i` equals `points[i] * (number of visits to i)`. We want to maximize `min_i points[i] * visits_i` subject to the walk constraints.

**Key insight:** The walk must start at -1 and stay within [0, n-1]. The structure of an optimal walk is to partition the array into contiguous segments, each segment fully traversed (go right to its end, then back left to its start) — except possibly the first segment (which starts the walk). Specifically, an optimal walk visits a set of positions; between consecutive visits to a position, we must traverse a contiguous block and return. A known result: the optimal walk visits all positions, and the number of visits to each position differs by at most 1.

The cost (moves) to give a position `i` exactly `k` visits: if it's the first (leftmost) visited, it needs `k` visits with cost `2k-1` (start, go right, return k-1 times). If it's not the leftmost, it needs `2k` moves. We want to assign visits so that `points[i] * visits[i] >= target` for all `i`, minimizing total moves, then binary search on target.

**Algorithm:**
1. Binary search on answer `T` (the minimum score).
2. For a given `T`, compute required visits: `need[i] = ceil(T / points[i])` for each `i`.
3. Compute total moves needed:
   - Find the leftmost index `L` that gets the maximum number of visits (or any index with odd visit count), costing `2*need[L] - 1`.
   - All other positions cost `2*need[i]`.
   - If `L` is not the leftmost index 0, the positions before `L` must also be visited to reach `L`, so they get at least 1 visit: `need[i] = max(need[i], 1)` for `i < L`. The leftmost of those has odd cost.
4. Check if total moves ≤ m.