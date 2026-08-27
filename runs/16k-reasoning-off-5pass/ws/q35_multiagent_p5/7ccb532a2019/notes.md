
## ideation
The core difficulty lies in efficiently calculating the minimum operations for a fixed target frequency $k$.
1.  **Understanding Operations**:
    *   Delete: Reduces count of a character by 1. Cost 1.
    *   Insert: Increases count of a character by 1. Cost 1.
    *   Change: Decreases count of char $A$ by 1, increases count of char $B$ by 1. Cost 1.
    *   Key Insight: A change operation is equivalent to a deletion and an insertion combined, but costs only 1 instead of 2. Therefore, if we have a surplus of characters (to be deleted) and a deficit of characters (to be inserted), we can pair them up using change operations. The remaining unpaired deletions or insertions must be done individually.
    *   Thus, for a fixed set of characters that remain in the final string (each with frequency $k$), the cost is $\max(\text{total insertions needed}, \text{total deletions needed})$.

2.  **Strategy for Fixed $k$**:
    *   The final string will have length $k \times m$, where $m$ is the number of distinct characters kept.
    *   Since the total length cannot exceed $n$ (original string length), $m \le n // k$. Also, $m \le 26$ (number of lowercase letters). So, $m = \min(26, n // k)$.
    *   To minimize cost, we should keep the $m$ characters with the highest frequencies. Why? Because keeping a character with a higher frequency reduces the number of insertions needed (if $f < k$) and reduces the number of deletions needed from that character (if $f > k$). More importantly, characters *not* kept must be fully deleted, so keeping high-frequency characters minimizes the "deletions from non-kept characters" part.
    *   Let the sorted frequencies (descending) be $f_1, f_2, ..., f_{26}$.
    *   We keep the top $m$ characters.
    *   Calculate `insertions`: Sum of $(k - f_i)$ for each kept character where $f_i < k$.
    *   Calculate `deletions`: 
        *   Sum of $(f_i - k)$ for each kept character where $f_i > k$.
        *   Sum of $f_j$ for all characters *not* kept (i.e., from index $m$ to 25).
    *   The cost for this $k$ is $\max(\text{insertions}, \text{deletions})$.

3.  **Complexity**:
    *   Counting frequencies: $O(N)$.
    *   Sorting frequencies: $O(1)$ since there are only 26 characters.
    *   Iterating $k$ from 1 to $N$: $O(N)$.
    *   Inside loop: Constant time operations (summing over 26 items).
    *   Total Time: $O(N)$. This fits within constraints ($N \le 2 \cdot 10^4$).

4.  **Pitfalls**:
    *   Forgetting that $m$ is limited by both 26 and $n // k$.
    *   Incorrectly calculating deletions: must include deletions of characters not in the kept set.
    *   Incorrectly calculating the cost formula: it's $\max(\text{insertions}, \text{deletions})$, not the sum.

## worker: None
The solution iterates through all possible target frequencies $k$ from 1 to $n$. For each $k$, it determines the optimal set of characters to keep in the final string. The final string will consist of $m$ distinct characters, each appearing exactly $k$ times, where $m = \min(26, n // k)$. To minimize operations, we greedily choose the $m$ characters with the highest original frequencies.

For a fixed $k$ and chosen set of $m$ characters:
1.  **Insertions**: For each kept character with original frequency $f < k$, we need $k - f$ insertions.
2.  **Deletions**: 
    - For each kept character with original frequency $f > k$, we need $f - k$ deletions.
    - For all characters *not* in the kept set, we must delete all their occurrences, contributing their full frequency to the deletion count.

The key insight is that a "change" operation (cost 1) can simultaneously satisfy one deletion and one insertion. Therefore, the total cost is the maximum of the total insertions and total deletions required, i.e., $\max(\text{insertions}, \text{deletions})$. This is because we can pair up $\min(\text{insertions}, \text{deletions})$ operations into changes, and the remaining unpaired operations must be done individually.

The time complexity is $O(N)$ because counting frequencies takes $O(N)$, sorting 26 frequencies is $O(1)$, and the loop runs $N$ times with constant work inside. This fits the constraints.
