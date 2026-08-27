
## ideation
**Core difficulty:**  
We must transform the multiset of characters into a “good” string where every present character appears the same number of times \(k\). The allowed operations are delete, insert (cost 1) and “change to the next letter” (cost 1, only forward). Changing a character more than one step is never better than deleting it and inserting a new one, because a two‑step change costs 2 while delete+insert also costs 2. Hence each original character can be treated as:  
* stay at its current position (cost 0),  
* move one step right (cost 1), or  
* be deleted/inserted (cost 1).

The problem becomes: choose a target frequency \(k\ge 1\) and a set of letters to keep (they must form disjoint contiguous intervals because moving right only affects the next letter). For a fixed interval \([L,R]\) and target \(k\) the minimal cost is obtained by scanning left to right, maintaining a carry of units that have been moved from the left. At each position we have supply = original frequency + carry. We keep \(k\) of them (cost 0) and decide how many of the excess to move right. Moving is beneficial only when it fills a deficit later; the amount we must move is exactly the future deficit  
\[
\text{needed}_i = \max\bigl(0,\;(R-i)\cdot k - \sum_{j=i+1}^{R}\text{freq}[j]\bigr).
\]
We move \(\min(\text{excess},\text{needed}_i)\) units (cost 1 each) and delete the rest (cost 1 each). If supply < \(k\) we insert the deficit (cost 1 each) and set carry = 0. This greedy yields the optimal cost for the interval.

**Candidate approaches**  
1. **DP over letters for each \(k\)** – compute the cost of every interval once per \(k\), then use DP to partition the 26 letters into intervals.  
2. **Min‑cost flow on a line** – the interval problem is a small linear program; the greedy above is essentially its optimal solution.  
3. **Brute‑force over all possible intervals and \(k\)** – too slow (26·2⁶ possible intervals).  

The DP approach is sufficient: for each \(k\) we pre‑compute an upper‑triangular matrix \(\text{cost}[L][R]\) in \(O(26^2)\) time, then run a linear DP in \(O(26^2)\). The total work is about \( \max\_freq \times 26^3 \le 2\cdot10^4 \times 17576 \approx 3.5\cdot10^8\) simple integer operations, which fits in time for \(n\le 2\cdot10^4\).

## worker: Count frequencies of the 26 letters in `s` and com
We model the problem as transforming the multiset of characters into a “good” string where every present letter appears exactly `k` times. Each original character can stay (cost 0), be changed to the next letter (cost 1), or be deleted/inserted (cost 1). Changing more than one step is never better than delete + insert, so we only need to consider one‑step moves.

For a fixed target frequency `k` and a contiguous interval `[L,R]` of letters, the minimal number of operations is
\[
\text{cost}(L,R,k)=\sum_{i=L}^{R}\lvert f_i-k\rvert-\text{flow}(L,R,k),
\]
where `f_i` is the original frequency of letter `i`, and `flow` is the maximum amount of excess that can be shifted right to cover deficits. The flow can be computed greedily by scanning the interval left‑to‑right, maintaining a carry of unused excess; whenever a deficit appears we consume as much carry as possible (each unit of flow saves one operation).

The whole string is a disjoint union of such intervals. For a given `k` we fill a DP over the 26 letters:
\[
dp[i]=\min\Bigl(dp[i-1]+f_i,\;\min_{0\le j\le i}\bigl(dp[j-1]+\text{cost}(j,i,k)\bigr)\Bigr),
\]
where the first term corresponds to deleting the letter `i` (i.e. not including it in any interval) and the second term makes the interval `[j,i]` good with target `k`.

We evaluate every `k` from 1 to `max(freq)`, compute the cost matrix for all intervals in `O(26²)` per `k` using an incremental scan, run the DP also in `O(26²)`, and keep the best answer. The total work is about `max_freq · 26² ≈ 1.3·10⁷` operations, well within limits.

The algorithm correctly reproduces the examples:
- `"acab"` → 1
- `"wddw"` → 0
- `"aaabc"` → 2
