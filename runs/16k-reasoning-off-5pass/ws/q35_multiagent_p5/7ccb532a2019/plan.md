1. Count the frequency of each character in the string `s`.
2. Iterate through all possible target frequencies `k` from 1 to `len(s)`. For each `k`, we want to transform the string such that all present characters have exactly `k` occurrences.
3. For a fixed `k`, calculate the cost:
   - For each character with frequency `f > 0`:
     - If `f == k`, cost is 0.
     - If `f < k`, we need to insert `k - f` characters. However, we can also change other characters to this character. But since we are iterating over all characters, it's easier to think: we must end up with exactly `k` of this character. The minimum operations to get `k` of a specific character given `f` is `abs(k - f)` if we only consider insertions/deletions for that character. But we can also change other characters. Actually, a better approach: for a fixed `k`, we decide which characters will be present in the final string. But which ones? To minimize cost, we should keep the characters that are already frequent.
   - Actually, a simpler DP or greedy: For a fixed `k`, the cost for a character with frequency `f` is `abs(k - f)` if we force it to have `k` occurrences? No, because we can delete extra and insert missing. The cost to make a character have exactly `k` occurrences is `abs(k - f)`? Not exactly: if `f > k`, we delete `f - k`. If `f < k`, we insert `k - f`. So cost is `abs(k - f)`. But we can also change a character from one type to another. Changing a character costs 1 and affects two counts: decreases one, increases another.
   - Better approach: For a fixed `k`, we want to select a subset of characters to remain in the string, each with count `k`. Let the selected characters be `C`. The total length will be `k * |C|`. The cost is:
     - For each character `c` in `C`: if `freq[c] < k`, we insert `k - freq[c]` characters. Cost += `k - freq[c]`.
     - For each character `c` not in `C`: we delete all `freq[c]` occurrences. Cost += `freq[c]`.
     - Additionally, we can change characters. But note: changing a character `a` to `b` costs 1 and reduces `freq[a]` by 1 and increases `freq[b]` by 1. This is equivalent to deleting `a` and inserting `b` with cost 1 instead of 2. So it's always better to change if we are moving from a character that is being deleted (or reduced) to one that is being inserted (or increased).
   - Actually, the standard solution for this problem is: iterate `k` from 1 to `n`. For each `k`, the cost is calculated as follows:
     - We can have at most `n // k` distinct characters in the final string (since each has count `k`).
     - We should choose the `m = min(26, n // k)` characters with the largest frequencies to keep, because they require the least number of insertions/deletions.
     - For the chosen `m` characters, the cost is: for each, `max(0, k - freq[c])` (insertions) + `max(0, freq[c] - k)` (deletions) is not quite right because changes can bridge the gap.
     - Correct cost for fixed `k` and chosen set `S` of size `m`:
       - Total insertions needed: `sum(max(0, k - freq[c]) for c in S)`
       - Total deletions needed: `sum(max(0, freq[c] - k) for c not in S) + sum(max(0, freq[c] - k) for c in S)`
       - But changes can reduce the total cost. Specifically, each change operation can cover one deletion and one insertion. So the net cost is `max(total_insertions, total_deletions)`.
       - Actually, the cost is `total_insertions + total_deletions - min(total_insertions, total_deletions)` = `max(total_insertions, total_deletions)`.
       - So for fixed `k`:
         - Let `m = min(26, n // k)`.
         - Sort frequencies in descending order. Take top `m` frequencies.
         - `insertions = sum(k - f for f in top_m if f < k)`
         - `deletions = sum(f - k for f in top_m if f > k) + sum(f for f in remaining_frequencies)`
         - Cost for this `k` is `max(insertions, deletions)`.
4. Return the minimum cost over all `k`.