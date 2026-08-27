
## ideation
The core difficulty lies in efficiently calculating the minimum operations for each possible target frequency `k` (from 1 to `n`). 

Key insights:
1. **Target Frequency**: The final string must have all present characters occurring exactly `k` times. `k` can range from 1 to `n` (the length of the string).
2. **Character Selection**: For a fixed `k`, we don't need to keep all 26 characters. We should choose a subset of characters to "keep" (i.e., have frequency `k` in the final string). Characters not chosen must be entirely deleted.
3. **Cost Calculation for Fixed `k` and Subset**:
   - Let `counts` be the frequency array of the 26 lowercase letters.
   - Sort `counts` in descending order.
   - For a fixed `k`, if we choose to keep the top `m` characters (those with highest frequencies), then:
     - For each kept character `i` (from 0 to m-1):
       - Surplus: `max(0, counts[i] - k)`
       - Deficit: `max(0, k - counts[i])`
     - For excluded characters (from m to 25): Cost is `counts[i]` (all deleted).
     - Total surplus `S = sum(surplus for kept chars)`
     - Total deficit `D = sum(deficit for kept chars)`
     - The number of change operations that can be used is `min(S, D)` because each change reduces one surplus and one deficit.
     - Remaining surplus must be deleted: `S - min(S, D)`
     - Remaining deficit must be inserted: `D - min(S, D)`
     - Total cost for this configuration = `(S - min(S, D)) + (D - min(S, D)) + min(S, D) + sum(excluded counts)`
       = `max(S, D) + sum(excluded counts)`
4. **Optimization**: Since there are only 26 characters, for each `k` (1 to n), we can iterate `m` from 1 to 26 (number of characters to keep). We compute the cost and take the minimum over all `k` and `m`.
5. **Pitfall**: Ensure that we only consider `m` such that `m * k <= n` is not strictly required because we can insert characters, but the total length of the final string will be `m * k`. The operations account for deletions and insertions. The formula `max(S, D) + sum(excluded)` correctly accounts for all operations.

## worker: Implement the solution by counting character frequ
The solution works by iterating over all possible target frequencies `k` (from 1 to the length of the string `n`). For each `k`, it considers keeping `m` characters (from 1 to 26, the number of distinct lowercase letters). The characters kept are the ones with the highest frequencies (after sorting the frequency array in descending order). 

For a fixed `k` and `m`:
1. **Surplus**: For each of the top `m` characters, if its frequency is greater than `k`, the excess (`freq[i] - k`) is surplus. These excess characters must be deleted or changed.
2. **Deficit**: For each of the top `m` characters, if its frequency is less than `k`, the missing amount (`k - freq[i]`) is deficit. These must be inserted or filled by changing other characters.
3. **Excluded Characters**: Characters not in the top `m` must be entirely deleted, costing `freq[i]` for each.
4. **Change Operations**: A change operation can simultaneously reduce one unit of surplus and one unit of deficit. Thus, `min(surplus, deficit)` change operations are optimal. The remaining surplus must be deleted and the remaining deficit must be inserted. The total cost for the kept characters is `max(surplus, deficit)`.
5. **Total Cost**: `max(surplus, deficit) + sum(freq[m:])`.

The minimum cost over all `k` and `m` is the answer. The complexity is O(n + 26^2 * n) which simplifies to O(n) since 26 is constant and the inner loop runs 26 times for each k (up to n). Actually, the inner loop over m runs 26 times, and for each m, we do a loop of size m (up to 26). So it's O(n * 26 * 26) = O(n), which is efficient for n up to 2*10^4.
