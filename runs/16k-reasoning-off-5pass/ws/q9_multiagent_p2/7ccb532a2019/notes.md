
## ideation
**Core Difficulty:**
The problem asks for the minimum operations to make all character frequencies equal. The allowed operations (delete, insert, change) have specific costs relative to frequency adjustments:
1.  **Delete/Insert:** Changing the count of a character by $k$ costs $k$. This effectively allows us to change any frequency $f$ to any other frequency $f'$ with cost $|f - f'|$.
2.  **Change Character:** Changing a character 'a' to 'b' costs 1. This allows us to convert one instance of a character with frequency $f$ to a character with frequency $f'$. If we do this for $k$ characters, the source frequency decreases by $k$ and the target frequency increases by $k$. The net cost is $k$.
    *   Crucially, this operation allows us to *redistribute* counts between existing characters without changing the total length of the string, but the cost is simply the number of characters changed.
    *   However, the problem statement says "Delete" and "Insert" are separate operations. "Change" is also an operation.
    *   Let's re-evaluate the cost model based on the examples.
        *   Ex 3: "aaabc" (a:3, b:1, c:1). Target: all 2? Or all 1?
            *   If target is 2: Change one 'a' to 'b' (a:2, b:2), then Insert 'c' (a:2, b:2, c:2). Total ops: 1 (change) + 1 (insert) = 2.
            *   If target is 1: Delete two 'a's (a:1, b:1, c:1). Total ops: 2.
        *   The key insight is that we can treat the problem as moving frequencies to a target value $T$.
        *   For a character with frequency $f$:
            *   If we keep it, we must adjust its frequency to $T$.
                *   If $f > T$, we must delete $f-T$ characters. Cost: $f-T$.
                *   If $f < T$, we must insert $T-f$ characters. Cost: $T-f$.
                *   Wait, can we use "Change" to fix frequency? Yes. If we have 'a' (freq $f$) and want it to be 'b' (which we want to have freq $T$), we can change 'a' to 'b'. This reduces 'a' count by 1 and increases 'b' count by 1.
                *   Actually, the "Change" operation is most useful when we want to *convert* a character type that has a "bad" frequency into a character type that has a "good" frequency, effectively merging the counts.
                *   But simpler view: We can change the frequency of any character $c$ to any value $v$ with cost $|f_c - v|$ using Delete/Insert.
                *   Can we do better with "Change"? Suppose we have 'a': 3, 'b': 1. Target 2.
                    *   Option A: Delete 1 'a' (cost 1), Insert 1 'b' (cost 1). Total 2.
                    *   Option B: Change 1 'a' to 'b'. Now 'a': 2, 'b': 2. Cost 1. This is better!
                *   So, if we have multiple characters with frequencies that need adjustment, "Change" allows us to transfer count from one to another at cost 1 per unit, whereas Delete+Insert costs 2 per unit (1 delete + 1 insert).
                *   Therefore, the strategy is:
                    1.  Identify the set of unique frequencies present in the string.
                    2.  Sort these frequencies.
                    3.  Consider each unique frequency as a potential target $T$.
                    4.  Also consider $T=0$ (delete everything).
                    5.  For a chosen target $T$:
                        *   Calculate the total "surplus" (freq > T) and "deficit" (freq < T).
                        *   We can satisfy the deficit by converting surplus characters to the target character type.
                        *   Specifically, if we have surplus $S$ and deficit $D$:
                            *   We can convert $\min(S, D)$ units from surplus to deficit using "Change" operations. Cost = $\min(S, D)$.
                            *   The remaining surplus must be deleted. Cost = $S - \min(S, D)$.
                            *   The remaining deficit must be filled by insertion. Cost = $D - \min(S, D)$.
                            *   Total Cost = $\min(S, D) + (S - \min(S, D)) + (D - \min(S, D)) = S + D - \min(S, D) = \max(S, D)$.
                        *   Wait, is it always $\max(S, D)$?
                            *   Example: 'a':3, 'b':1. Target 2. $S=1, D=1$. $\max(1,1)=1$. Correct.
                            *   Example: 'a':4, 'b':1, 'c':1. Target 2. $S=2, D=2$. $\max(2,2)=2$.
                                *   Change 2 'a's to 'b' and 'c'. 'a':2, 'b':3, 'c':2. Wait, 'b' becomes 3. Then delete 1 'b'.
                                *   Let's trace carefully.
                                *   Start: a:4, b:1, c:1. Target 2.
                                *   Surplus from 'a': 2. Deficit for 'b': 1, 'c': 1.
                                *   Change 1 'a' -> 'b'. State: a:3, b:2, c:1. Cost 1.
                                *   Change 1 'a' -> 'c'. State: a:2, b:2, c:2. Cost 1.
                                *   Total cost 2. Matches $\max(2,2)$.
                            *   Example: 'a':5, 'b':1. Target 2. $S=3, D=1$. $\max(3,1)=3$.
                                *   Change 1 'a' -> 'b'. State: a:4, b:2. Cost 1.
                                *   Delete 2 'a's. State: a:2, b:2. Cost 2.
                                *   Total 3. Matches.
                        *   So the cost for a specific target $T$ is $\sum_{f > T} (f - T) + \sum_{f < T} (T - f) - \min(\sum_{f > T} (f - T), \sum_{f < T} (T - f))$.
                        *   Wait, the formula simplifies to: Total Cost = $\sum |f - T| - \min(\text{surplus}, \text{deficit})$.
                        *   Why? Because the overlapping part (where we have both surplus and deficit) can be handled by "Change" (cost 1 per unit) instead of "Delete + Insert" (cost 2 per unit). The difference is 1 per unit.
                        *   Total cost if we only used Delete/Insert = $\sum |f - T|$.
                        *   We save 1 unit of cost for every unit we can convert. Max conversion is $\min(\text{surplus}, \text{deficit})$.
                        *   So Cost = $\sum |f - T| - \min(\text{surplus}, \text{deficit})$.

**Candidate Approaches:**
1.  **Frequency Counting:** Count char frequencies.
2.  **Unique Frequencies:** Extract unique non-zero frequencies. Sort them.
3.  **Iterate Targets:** For each unique frequency $f_i$ and also $0$:
    *   Calculate surplus and deficit relative to $f_i$.
    *   Compute cost using the formula derived.
4.  **Optimization:** Since the number of unique frequencies is small (at most 26), iterating through all is $O(26 \cdot N)$ or $O(26^2)$, which is negligible.

**Pitfalls:**
*   **Target 0:** Must consider the case where we delete all characters. Cost = length of string.
*   **Multiple characters with same frequency:** The logic holds; we sum up all surpluses/deficits.
*   **Empty string?** Constraints say length >= 3.
*   **Complexity:** Counting is $O(N)$. Sorting unique freqs is $O(26 \log 26)$. Iterating is $O(26 \cdot 26)$. Overall $O(N)$. Very efficient.
*   **Logic Error:** Forgetting that "Change" reduces the cost compared to "Delete+Insert". The formula $\sum |f-T| - \min(S, D)$ handles this correctly.

## worker: Implement the solution in Python by counting chara
The solution involves the following steps:
1.  **Count Frequencies**: Use `Counter` to get the frequency of each character in the string.
2.  **Identify Unique Frequencies**: Extract the set of unique frequencies present. Since there are at most 26 lowercase English letters, this list is very small (size <= 26).
3.  **Evaluate Targets**: Iterate through each unique frequency as a candidate target frequency $T$. Additionally, consider $T=0$ (which implies deleting all characters).
4.  **Calculate Cost**: For a given target $T$:
    *   Calculate the total **surplus** (sum of differences where frequency > $T$).
    *   Calculate the total **deficit** (sum of differences where frequency < $T$).
    *   The cost to align frequencies using only Delete and Insert operations would be `surplus + deficit`.
    *   However, the "Change" operation allows us to convert a character from a surplus frequency to a deficit frequency at a cost of 1 per unit, which is cheaper than Delete (1) + Insert (1) = 2.
    *   We can transfer at most `min(surplus, deficit)` units using the "Change" operation.
    *   Therefore, the minimum cost for target $T$ is `(surplus + deficit) - min(surplus, deficit)`.
5.  **Result**: The answer is the minimum cost found across all candidate targets.

Time Complexity: $O(N + K \log K)$, where $N$ is the length of the string and $K$ is the number of unique frequencies (at most 26). This is effectively $O(N)$.
Space Complexity: $O(1)$ (since the alphabet size is constant).

## worker: Return the minimum cost found across all candidate
The solution implements the logic derived in the ideation phase:
1.  **Frequency Counting**: We count the occurrences of each character in the string `s`.
2.  **Unique Frequencies**: We extract the set of unique frequencies present. Since the alphabet size is small (26), this list is short.
3.  **Target Evaluation**: We iterate through each unique frequency as a candidate target frequency `T`. We also explicitly consider `T=0` (deleting all characters).
4.  **Cost Calculation**: For a target `T`, we calculate the total surplus (characters with frequency > T) and deficit (characters with frequency < T).
    *   The cost to adjust frequencies using only Delete and Insert operations is `surplus + deficit`.
    *   The "Change" operation allows us to convert a character from a surplus frequency to a deficit frequency at a cost of 1, which is cheaper than Delete (1) + Insert (1) = 2.
    *   We can transfer at most `min(surplus, deficit)` units using the "Change" operation.
    *   Therefore, the minimum cost for target `T` is `(surplus + deficit) - min(surplus, deficit)`.
5.  **Result**: The answer is the minimum cost found across all candidate targets.

The time complexity is $O(N + K \log K)$, where $N$ is the length of the string and $K$ is the number of unique frequencies (at most 26). This is effectively $O(N)$. The space complexity is $O(1)$ (since the alphabet size is constant).
