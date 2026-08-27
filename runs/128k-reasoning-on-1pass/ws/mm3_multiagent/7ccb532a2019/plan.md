We model the problem as transforming the original multiset of characters into a “good” string where every present letter appears exactly `k` times (for some `k ≥ 1`).  
Allowed operations: delete (cost 1), insert (cost 1), change a character to its next letter (cost 1 per step).  
Only forward changes of distance 1 give a net benefit (‑1 operation compared to delete+insert); distance ≥ 2 is never better than delete+insert.  
Thus each original character of type `c` can either stay as `c` (benefit 2), be changed to `c+1` (benefit 1), or be deleted/inserted (benefit 0).  

For a fixed target frequency `k`, the minimal cost to make a **contiguous** block of letters `L…R` good is:
```
cost(L,R,k) = sum_{i=L..R} freq[i] + (R-L+1)*k – benefit(L,R,k)
```
where `benefit(L,R,k)` is computed greedily from left to right:
* keep as many `freq[i]` as possible as themselves,
* any leftover supply from `i` is forwarded to `i+1` (cost 1 per unit, benefit 1),
* any unmet demand is filled by insertion (no benefit).

The whole string is a disjoint union of such blocks (intervals of selected letters).  
For a given `k` we run a DP over the 26 letters:
```
dp[i] = minimal cost for letters 0..i
dp[i] = min( dp[i-1] + freq[i] ,  min_{0≤j≤i} ( dp[j-1] + cost(j,i,k) ) )
```
The answer is `min_{k≥1} dp[25]` (also compare with deleting everything, cost = n).

The cost functions are evaluated for all `k` from 1 to `max(freq)`.  
The total work is about 9·10⁷ simple operations, well within limits.