
## ideation
**Core Difficulty**:
The problem asks for the minimum operations to make all character frequencies equal. The operations (delete, insert, change) allow us to adjust frequencies.
- **Delete**: Reduces frequency of a specific char. Cost = 1 per char.
- **Insert**: Increases frequency of a specific char. Cost = 1 per char.
- **Change**: Transforms one char to another (next letter). Effectively, this reduces the count of the source char by 1 and increases the count of the target char by 1. Cost = 1 per char.

Crucially, "Change" allows us to move characters from a bucket with too many occurrences to a bucket with too few, without changing the *total* length of the string. "Delete" reduces total length, "Insert" increases total length.
The goal is to reach a state where every character present has frequency $k$.
Possible strategies for a target frequency $k$:
1.  **Target $k = 0$**: Delete all characters. Cost = length of $s$. (Usually not optimal unless $s$ is very long and frequencies are weird, but valid).
2.  **Target $k > 0$**: We need to select a set of characters that will remain in the string, each having frequency $k$.
    - For a character $c$ with current frequency $freq[c]$:
        - If $freq[c] > k$: We must delete $freq[c] - k$ characters. (Cost: $freq[c] - k$)
        - If $freq[c] < k$: We must add $k - freq[c]$ characters. These can come from changing other characters or inserting new ones.
    - Total operations = (Sum of deletions) + (Sum of insertions needed for deficits).
    - However, "Change" operations are more efficient than "Delete" + "Insert". If we have a surplus in char A and a deficit in char B, we can change the surplus A's to B's. This costs 1 operation and fixes both a surplus and a deficit simultaneously.
    - Only if we have a global surplus (total chars > sum of $k$ for chosen chars) do we need deletes. Only if we have a global deficit (total chars < sum of $k$) do we need inserts.
    - Actually, the constraint is simpler: We pick a target frequency $k$. We iterate through all unique characters present in $s$.
        - Let $S_{surplus}$ be the count of characters with $freq > k$.
        - Let $S_{deficit}$ be the count of characters with $freq < k$ (and $>0$).
        - Let $S_{zero}$ be characters not in $s$.
        - Total characters to keep = $count\_unique \times k$.
        - Current total characters = $N$.
        - If $N > count\_unique \times k$: We must delete $N - count\_unique \times k$ characters. (All deficits must be filled by changes from surpluses, and remaining surpluses deleted).
        - If $N < count\_unique \times k$: We must insert $count\_unique \times k - N$ characters. (All surpluses must be reduced to $k$ via deletion or change? No, if we need to insert, it means we are expanding the set. But wait, if we change a char, we don't change total count. If we delete, count goes down. If we insert, count goes up.
        - Let's refine the cost calculation for a fixed $k$ and a fixed set of characters to keep (say $m$ characters):
          - We want $m$ characters each with freq $k$.
          - Total target length = $m \times k$.
          - Current length = $N$.
          - Operations needed:
            1. Identify which characters to keep. To minimize cost, we should keep characters that are "close" to $k$? Actually, the cost function is linear.
            2. For any character $c$ with $freq[c] > k$: Cost contribution is $freq[c] - k$ (must delete excess).
            3. For any character $c$ with $0 < freq[c] < k$: Cost contribution is $k - freq[c]$ (must add).
            4. For characters not in $s$: Cost contribution is $k$ (must insert).
          - Total "gap" = $\sum_{c \in kept} |freq[c] - k| + \sum_{c \notin kept} k$.
          - But we can use "Change" operations. A change operation takes 1 char from a surplus bucket and gives it to a deficit bucket.
          - Let $TotalSurplus = \sum_{freq[c] > k} (freq[c] - k)$.
          - Let $TotalDeficit = \sum_{0 < freq[c] < k} (k - freq[c]) + \sum_{c \notin kept} k$.
          - We can satisfy $\min(TotalSurplus, TotalDeficit)$ using changes.
          - The remaining difference must be handled by deletes or inserts.
          - Actually, simpler view:
            - We MUST delete all characters that exceed $k$. Cost = $\sum_{freq[c] > k} (freq[c] - k)$.
            - After deleting these, we have some characters with count $> k$ (now exactly $k$) and some with $< k$.
            - Wait, if we delete, we remove characters. We can't "change" a deleted character.
            - Correct Logic:
              - For a fixed $k$ and a fixed subset of characters $U$ (size $m$) that will have frequency $k$:
                - Cost = (Operations to fix counts in $U$) + (Operations to fix counts outside $U$).
                - Characters in $U$ with $freq > k$: Delete $freq - k$.
                - Characters in $U$ with $freq < k$: Need $k - freq$. These can be filled by changing characters from outside $U$ (if available) or inserting.
                - Characters not in $U$:
                  - If $freq > 0$: Delete all $freq$ (since they shouldn't be there).
                  - If $freq = 0$: Insert $k$ (if we decide to include them, but we assumed they are not in $U$).
              - This seems complicated because choosing $U$ matters.
              - **Alternative Insight**:
                - We can iterate over all possible target frequencies $k$. What are the bounds for $k$?
                  - Min $k$: 0 (delete everything).
                  - Max $k$: Max frequency in $s$ (or maybe slightly more? No, if $k > max\_freq$, then for all chars we have $freq < k$, so we just insert. Cost = $m \times k - N$. This is likely high).
                  - Actually, the optimal $k$ is likely one of the existing frequencies or $0$. Why? Because the cost function is convex-ish.
                  - Let's reconsider the "Change" operation. It moves mass.
                  - Strategy:
                    1. Count frequencies of all chars in $s$.
                    2. Collect all non-zero frequencies into a list `freqs`.
                    3. Sort `freqs`.
                    4. Consider candidate target frequencies $k$.
                       - Candidate 1: $k = 0$. Cost = $N$.
                       - Candidate 2: $k \in \{f \mid f \in freqs\}$.
                       - Candidate 3: Maybe $k$ is not in `freqs`? If we pick a $k$ not present, we are moving everyone to a new level. Is it ever better?
                         - Suppose frequencies are [2, 5]. Target $k=3$.
                         - Char A: 2 -> 3 (need +1). Char B: 5 -> 3 (need -2).
                         - Change 1 from B to A. Cost 1. Remaining B: 4 -> 3 (delete 1). Total 2.
                         - If target $k=2$: A: 2 (ok), B: 5 -> 2 (delete 3). Total 3.
                         - If target $k=5$: A: 2 -> 5 (insert/change 3), B: 5 (ok). Total 3.
                         - It seems checking existing frequencies is usually sufficient, but we must be careful.
                         - Actually, the standard solution for this type of problem (making all frequencies equal) involves checking $k$ from 1 to max_freq, and also $k=0$.
                         - Optimization: Since $N$ is up to $20,000$, iterating $k$ from 1 to $N$ is $O(N)$. Inside, we sum over 26 chars. Total $O(26 \cdot N)$, which is fine.
                    5. Algorithm for a fixed $k$:
                       - Calculate `cost` = 0.
                       - `surplus` = 0, `deficit` = 0.
                       - Iterate over all 26 chars:
                         - If $freq[c] == 0$:
                           - If we decide to keep this char, we need to insert $k$. But we don't know which chars to keep yet.
                           - Wait, the problem says "all characters of t occur the same number of times". It doesn't say "all 26 characters". It says "all characters of t". So we can choose a subset of characters to be present.
                           - To minimize cost, for a fixed $k$, we should keep the characters that require the least operations to reach $k$.
                           - For a char $c$ with $freq[c] > 0$:
                             - Cost to make it $k$:
                               - If $freq[c] > k$: delete $freq[c] - k$. (Cannot change to something else if we want to keep $c$, because then $c$'s count drops further. We could change $c$ to $d$, but then $c$ is no longer in the set of "characters of t".)
                               - If $freq[c] < k$: we need $k - freq[c]$. We can get this by changing other chars to $c$, or inserting.
                           - For a char $c$ with $freq[c] == 0$:
                             - Cost to make it $k$: insert $k$ (or change others).
                           - Let's reframe:
                             - We select a subset of characters $S$ to be present in the final string.
                             - For each $c \in S$, final count = $k$.
                             - For each $c \notin S$, final count = 0.
                             - Cost = (Total chars in $s$) - (Chars kept from $s$ that are $\le k$) + (Insertions needed)?
                             - Let's use the "Change" logic properly.
                             - Total operations = (Number of deletions) + (Number of insertions).
                             - Note: 1 Change = 1 Delete + 1 Insert effectively (in terms of count balance), but costs 1 op.
                             - Let $TotalOps = \sum_{c \in S} |freq[c] - k| + \sum_{c \notin S} (k \text{ if we insert? no})$.
                             - Better approach:
                               - For a fixed $k$:
                                 - Calculate cost if we keep ALL characters present in $s$ (ignoring those with 0 freq).
                                   - For $freq[c] > k$: cost += $freq[c] - k$.
                                   - For $freq[c] < k$: cost += $k - freq[c]$.
                                   - This assumes we can fill deficits using changes from surpluses or inserts.
                                   - Let $Surplus = \sum_{freq[c] > k} (freq[c] - k)$.
                                   - Let $Deficit = \sum_{freq[c] < k} (k - freq[c])$.
                                   - We can cover $\min(Surplus, Deficit)$ with changes.
                                   - Remaining $Surplus$ must be deleted.
                                   - Remaining $Deficit$ must be inserted.
                                   - Cost = $\min(Surplus, Deficit) + (Surplus - \min) + (Deficit - \min) = Surplus + Deficit - \min(Surplus, Deficit) = \max(Surplus, Deficit)$.
                                   - Wait, is this correct?
                                     - Example: freqs [2, 5], $k=3$.
                                     - Surplus (5-3)=2. Deficit (3-2)=1.
                                     - Min(2,1)=1. Cost = 1 (change) + (2-1) delete + (1-1) insert = 2. Correct.
                                     - Example: freqs [2, 2], $k=3$.
                                     - Surplus=0. Deficit=(3-2)+(3-2)=2.
                                     - Cost = 0 + 2 = 2. (Insert 2). Correct.
                                     - Example: freqs [5, 5], $k=3$.
                                     - Surplus=2+2=4. Deficit=0.
                                     - Cost = 4. (Delete 4). Correct.
                                 - BUT, this assumes we keep ALL characters present in $s$. What if removing a character entirely (making its final count 0) is cheaper?
                                   - If we remove char $c$ (freq $f$):
                                     - Instead of paying $|f-k|$ (or part of it), we pay $f$ (delete all).
                                     - Is $f < |f-k|$?
                                       - If $f > k$: $|f-k| = f-k$. Since $k \ge 1$, $f > f-k$. So deleting all is MORE expensive than reducing to $k$.
                                       - If $f < k$: $|f-k| = k-f$. If $k-f < f \implies k < 2f$.
                                         - Example: $f=1, k=3$. Reduce to 3 costs 2. Delete costs 1. Deleting is better!
                                         - Example: $f=2, k=3$. Reduce to 3 costs 1. Delete costs 2. Reducing is better.
                                   - So, for a fixed $k$, we should decide for each char $c$ whether to keep it or delete it all.
                                   - Cost to keep $c$:
                                     - If $f > k$: $f-k$ (delete excess).
                                     - If $f < k$: $k-f$ (fill deficit).
                                   - Cost to delete $c$: $f$.
                                   - We choose $\min(f, \text{cost to keep})$.
                                   - However, there's a catch: The "Change" operation allows moving characters between kept characters. If we delete a character $c$ entirely, those $f$ characters are gone. They cannot be used to fill deficits of other kept characters.
                                   - So the calculation becomes:
                                     1. Identify a subset of characters to keep.
                                     2. For kept chars, calculate Surplus and Deficit.
                                     3. Cost = $\max(Surplus, Deficit)$ + (Sum of deletions for kept chars that have $f>k$) + (Sum of deletions for removed chars).
                                     - Actually, simpler:
                                       - Total Cost = (Sum of all chars in $s$) - (Sum of chars we successfully "save" via changes/keeps) + (Insertions).
                                       - Let's stick to the explicit formula:
                                         - For a fixed $k$:
                                           - For each char $c$ with freq $f$:
                                             - Option A: Keep $c$. Cost contribution to "local" adjustment is $|f-k|$.
                                             - Option B: Delete $c$. Cost contribution is $f$.
                                             - But "local" adjustment assumes we can use changes from surpluses to deficits.
                                             - Let $S_{keep}$ be the set of kept chars.
                                             - $Surplus = \sum_{c \in S_{keep}, f > k} (f-k)$.
                                             - $Deficit = \sum_{c \in S_{keep}, f < k} (k-f)$.
                                             - Cost = (Sum of $f$ for $c \notin S_{keep}$) + $\max(Surplus, Deficit)$.
                                             - Why? Because $\min(Surplus, Deficit)$ operations are changes (cost 1 each, fix 1 surplus and 1 deficit). The rest of the surplus must be deleted (cost 1 each). The rest of the deficit must be inserted (cost 1 each).
                                             - Note: $\max(Surplus, Deficit) = Surplus + Deficit - \min(Surplus, Deficit)$.
                                             - Total Cost = $\sum_{c \notin S_{keep}} f + \sum_{c \in S_{keep}, f > k} (f-k) + \sum_{c \in S_{keep}, f < k} (k-f) - \min(Surplus, Deficit)$.
                                             - This looks like we need to optimize $S_{keep}$.
                                             - Observation: For a char $c$, if we keep it, we pay $|f-k|$ (conceptually) but we also enable it to participate in the $\min(Surplus, Deficit)$ reduction.
                                             - Actually, the term $\max(Surplus, Deficit)$ is the cost of balancing the kept set. The term $\sum_{c \notin S_{keep}} f$ is the cost of removing others.
                                             - Is it ever optimal to remove a char $c$ with $f > k$?
                                               - Cost to keep: $f-k$. Cost to remove: $f$. Since $k \ge 1$, $f-k < f$. So always keep if $f > k$.
                                             - Is it ever optimal to remove a char $c$ with $f < k$?
                                               - Cost to keep: $k-f$. Cost to remove: $f$.
                                               - Remove if $f < k-f \iff 2f < k$.
                                               - If we remove, we save $k-f$ but pay $f$. Net change in cost: $f - (k-f) = 2f - k$. If $2f < k$, removing is cheaper.
                                               - BUT, if we remove $c$, we lose its potential to be a "deficit" filler.
                                               - Wait, if $c$ is a deficit ($f < k$), it needs $k-f$ items. If we remove it, we pay $f$ (delete all).
                                               - If we keep it, we pay $k-f$ (insert/change).
                                               - Clearly if $f < k-f$, removing is cheaper.
                                               - So for each char, we can independently decide to keep or remove?
                                               - Almost. The $\min(Surplus, Deficit)$ term couples them.
                                               - However, note that $Surplus$ only comes from chars with $f > k$. We established we should always keep those.
                                               - $Deficit$ comes from chars with $f < k$.
                                               - If we remove a char with $f < k$, it reduces $Deficit$ by $(k-f)$ and adds $f$ to the deletion cost.
                                               - Change in cost = $f - (k-f) = 2f - k$.
                                               - If $2f < k$, we should remove it.
                                               - Does removing it affect $Surplus$? No.
                                               - Does it affect the $\min(Surplus, Deficit)$ term?
                                                 - Yes. If we remove a deficit char, $Deficit$ decreases.
                                                 - If $Surplus > Deficit_{new}$, then $\max$ decreases.
                                                 - If $Surplus \le Deficit_{new}$, then $\max$ might decrease or stay same.
                                                 - Since removing a deficit char reduces $Deficit$, it can only reduce or keep $\max(Surplus, Deficit)$ same (since $Surplus$ is constant).
                                                 - So the decision to remove a deficit char is always locally optimal if $2f < k$, and the global coupling doesn't make it worse (it reduces the max term).
                                               - Conclusion: For a fixed $k$:
                                                 - Keep all chars with $f > k$.
                                                 - For chars with $f < k$: Keep if $2f \ge k$, else Remove.
                                                 - For chars with $f = 0$: Always Remove (cost 0).
                                                 - Calculate $Surplus$ (from kept $f>k$) and $Deficit$ (from kept $f<k$).
                                                 - Cost = (Sum of $f$ for removed chars) + $\max(Surplus, Deficit)$.
                                                 - Wait, what about chars with $f=0$? They are not in the input, so freq is 0. We never keep them (cost $k$ vs 0).
                                                 - So the algorithm for a fixed $k$:
                                                   1. Initialize `surplus = 0`, `deficit = 0`, `removed_cost = 0`.
                                                   2. For each char $c$ with freq $f$:
                                                      - If $f > k$:
                                                        - `surplus += f - k`
                                                      - Else if $f < k$:
                                                        - If $2 * f >= k$:
                                                          - `deficit += k - f`
                                                        - Else:
                                                          - `removed_cost += f`
                                                      - Else ($f == k$):
                                                        - Do nothing.
                                                   3. `ans = min(ans, removed_cost + max(surplus, deficit))`
                                                   4. Also consider $k=0$: `ans = min(ans, len(s))`.

## worker: Implement the frequency counting and the main loop
The solution iterates through all possible target frequencies $k$ from 1 to the maximum frequency present in the string. For each $k$, it calculates the minimum operations required:
1.  **Characters with frequency $f > k$**: We must delete the excess $f - k$. These contribute to `surplus`.
2.  **Characters with frequency $f < k$**: We have a choice.
    *   **Keep**: We need to add $k - f$ characters (via change or insert). Cost = $k - f$.
    *   **Remove**: We delete all $f$ characters. Cost = $f$.
    *   We choose the minimum of these two. If $2f \ge k$, keeping is cheaper or equal; otherwise, removing is cheaper.
    *   If kept, they contribute to `deficit`. If removed, they add to `removed_cost`.
3.  **Balancing**: After deciding which characters to keep, we have a total `surplus` (excess characters) and `deficit` (missing characters). We can use "Change" operations to move characters from surplus buckets to deficit buckets. Each change fixes 1 unit of surplus and 1 unit of deficit. The remaining imbalance (either remaining surplus or remaining deficit) must be handled by deletions or insertions. The cost for this step is $\max(\text{surplus}, \text{deficit})$.
4.  **Total Cost**: `removed_cost` + $\max(\text{surplus}, \text{deficit})$.
5.  We also consider the case where we delete all characters (target $k=0$), which costs `len(s)`.

The complexity is $O(N \cdot \Sigma)$ where $N$ is string length and $\Sigma$ is the alphabet size (26), which fits well within the constraints.

## worker: Run the solution against provided examples to veri
The solution implements the logic derived in the thought process:
1.  **Frequency Counting**: Uses `Counter` to get frequencies of all characters.
2.  **Base Case**: Initializes `ans` with `len(s)` (cost to delete everything, i.e., target frequency 0).
3.  **Iterate Target Frequencies**: Loops `k` from 1 to `max_freq`.
4.  **Cost Calculation for `k`**:
    *   **Surplus**: For characters with `freq > k`, we must delete `freq - k` characters. These contribute to `surplus`.
    *   **Deficit vs. Removal**: For characters with `freq < k`:
        *   Cost to keep (fill to `k`) is `k - freq`.
        *   Cost to remove (delete all) is `freq`.
        *   We choose the minimum. If `2 * freq >= k`, keeping is cheaper/equal; otherwise, removing is cheaper.
        *   If kept, add `k - freq` to `deficit`. If removed, add `freq` to `removed_cost`.
    *   **Balancing**: The `min(surplus, deficit)` amount can be resolved using "Change" operations (cost 1 per op). The remaining `max(surplus, deficit)` must be resolved by either more deletions (if surplus > deficit) or insertions (if deficit > surplus).
    *   **Total Cost**: `removed_cost + max(surplus, deficit)`.
5.  **Optimization**: Updates `ans` with the minimum cost found.

This approach covers all optimal strategies because:
-   Target frequency 0 is explicitly checked.
-   For any target frequency $k > 0$, the optimal set of characters to keep is determined by the local cost comparison ($2f \ge k$), and the balancing cost is correctly calculated.
-   The range of $k$ up to `max_freq` is sufficient because increasing $k$ beyond `max_freq` only increases the deficit for all characters without reducing any surplus (since no character has $f > k$), leading to a strictly increasing cost function for $k > \max(freqs)$.
