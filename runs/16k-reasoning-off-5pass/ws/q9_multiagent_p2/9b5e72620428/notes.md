
## ideation
**Core Difficulty**:
The problem asks if we can fill missing values (-1) and rearrange array A such that $A_i + B_i = S$ (constant) for all $i$, with all resulting values non-negative.
The key challenge is determining the valid range for the constant sum $S$ and checking if a valid pairing exists.
1.  **Constraint on $S$**: Since $A_i, B_i \ge 0$, any $S$ must be at least the maximum of any single known value in A or B (i.e., $S \ge \max(\{a \mid a \in A, a \neq -1\} \cup \{b \mid b \in B, b \neq -1\})$).
2.  **Constraint on Total Sum**: The total sum of the final arrays will be $N \times S$. This must be greater than or equal to the sum of all currently known numbers.
3.  **Pairing Constraint**: If there are indices where both $A_i$ and $B_i$ are known, they *must* sum to $S$. However, we can rearrange A. This means we don't necessarily pair $A_i$ with $B_i$ at the same index if both are known initially. We just need to be able to partition the set of known values in A ($V_A$) and known values in B ($V_B$) into pairs $(a, b)$ such that $a+b=S$.
    *   Let $k_A$ be the count of knowns in A, $k_B$ be the count of knowns in B.
    *   We need to form $m = \min(k_A, k_B)$ pairs.
    *   The remaining $k_A - m$ values from A and $k_B - m$ values from B will be paired with the -1s we fill.
    *   Actually, a simpler view: We have a set of known numbers $V_A$ and $V_B$. We need to select a subset of pairs $(a, b)$ with $a \in V_A, b \in V_B$ such that $a+b=S$. Let the size of this subset be $p$.
    *   The remaining $|V_A| - p$ elements of A must be paired with the $-1$s in B (which we fill to be $S-a$). This requires $S-a \ge 0 \implies S \ge a$.
    *   The remaining $|V_B| - p$ elements of B must be paired with the $-1$s in A (which we fill to be $S-b$). This requires $S \ge b$.
    *   Crucially, the number of -1s in A is $N - |V_A|$ and in B is $N - |V_B|$.
    *   We need to match the remaining A's to the B's (-1s) and vice versa.
    *   Actually, the condition simplifies: We just need to find if there exists an $S$ such that we can form *some* number of pairs $(a,b)$ from $V_A \times V_B$ summing to $S$, and for all unpaired $a \in V_A$, $S \ge a$, and for all unpaired $b \in V_B$, $S \ge b$.
    *   Wait, is it "some number"? No. The problem allows rearranging A. So we can choose *which* $a$'s pair with *which* $b$'s.
    *   Let's re-evaluate the pairing logic.
        *   We have $k_A$ knowns in A, $k_B$ knowns in B.
        *   We can form at most $m = \min(k_A, k_B)$ pairs of (known A, known B).
        *   Suppose we form $p$ pairs where $a+b=S$.
        *   Then $k_A - p$ knowns in A must be paired with $-1$s in B. For these, we set $B_{new} = S - A_{old}$. Condition: $S \ge A_{old}$.
        *   Then $k_B - p$ knowns in B must be paired with $-1$s in A. For these, we set $A_{new} = S - B_{old}$. Condition: $S \ge B_{old}$.
        *   The number of -1s available in B is $N - k_B$. We need $k_A - p \le N - k_B \implies k_A + k_B - p \le N \implies p \ge k_A + k_B - N$.
        *   Similarly, $k_B - p \le N - k_A \implies p \ge k_A + k_B - N$.
        *   So we must form at least $L = \max(0, k_A + k_B - N)$ pairs.
        *   Also, we can form at most $R = \min(k_A, k_B)$ pairs.
        *   So we need to find an $S$ and an integer $p \in [L, R]$ such that we can pick $p$ pairs from $V_A \times V_B$ summing to $S$, AND for all remaining $a \in V_A$, $S \ge a$, AND for all remaining $b \in V_B$, $S \ge b$.
        *   Note: If we pick $p$ pairs, the remaining sets are $V_A' = V_A \setminus \{a_1, \dots, a_p\}$ and $V_B' = V_B \setminus \{b_1, \dots, b_p\}$.
        *   The condition "for all remaining $a$, $S \ge a$" is equivalent to $S \ge \max(V_A')$. To maximize our chances, we should try to remove the largest elements from $V_A$ into the pairs.
        *   Similarly, we should remove the largest elements from $V_B$ into the pairs.
        *   Therefore, for a fixed $S$ and fixed $p$, the best strategy is to greedily pair the largest available $a$'s and $b$'s. If we can't find $p$ pairs summing to $S$ using the largest elements, we certainly can't do it with smaller ones? Not necessarily. But we need to satisfy the global max condition.
        *   Actually, the condition $S \ge \max(V_A')$ is easiest satisfied if $V_A'$ contains the smallest elements. So we should pair the *largest* elements of $V_A$ and $V_B$ into the $p$ pairs.
        *   Algorithm refinement:
            1. Sort $V_A$ and $V_B$ in descending order.
            2. The candidate sums $S$ must be of the form $a_i + b_j$. Since $N$ is up to 2000, $|V_A|, |V_B| \le 2000$. The number of pairs is up to $4 \times 10^6$. We can iterate over all possible $S$ derived from $a \in V_A, b \in V_B$.
            3. For a specific $S$:
               - Check if $S \ge \max(V_A \cup V_B)$. If not, invalid.
               - Determine the minimum number of pairs required: $L = \max(0, |V_A| + |V_B| - N)$.
               - Determine the maximum number of pairs possible: $R = \min(|V_A|, |V_B|)$.
               - We need to check if there exists a $p \in [L, R]$ such that we can select $p$ pairs $(a, b)$ with $a+b=S$.
               - However, we also have the constraint that the *unpaired* elements must be $\le S$. Since we already checked $S \ge \max(V_A \cup V_B)$, *any* unpaired element will automatically satisfy the non-negativity condition ($S - x \ge 0$).
               - So the only constraint is: Can we form at least $L$ pairs summing to $S$?
               - Wait, is it "at least"?
                 - If we form $p > L$ pairs, the number of unpaired A's is $|V_A| - p$. We need $|V_A| - p \le N - |V_B| \implies p \ge |V_A| + |V_B| - N = L$.
                 - Yes, we just need to be able to form *at least* $L$ pairs.
                 - But wait, can we form *more*? Yes, if we can form $p$ pairs, we can just choose to only "use" $L$ of them? No, the pairing is structural.
                 - Let's trace:
                   - We have $k_A$ knowns in A, $k_B$ knowns in B.
                   - We need to assign each known $a \in V_A$ to a unique index $i$.
                   - We need to assign each known $b \in V_B$ to a unique index $j$.
                   - We need to pair them up such that $A_i + B_i = S$.
                   - This means we partition $V_A$ and $V_B$ into three sets:
                     - $P_A, P_B$: Pairs $(a, b)$ where $a \in P_A, b \in P_B, a+b=S$. Size $p$.
                     - $U_A$: Unpaired A's (paired with -1s in B). Size $k_A - p$.
                     - $U_B$: Unpaired B's (paired with -1s in A). Size $k_B - p$.
                   - Constraints:
                     1. $k_A - p \le N - k_B \implies p \ge k_A + k_B - N$.
                     2. $k_B - p \le N - k_A \implies p \ge k_A + k_B - N$.
                     3. $p \le k_A$ and $p \le k_B$.
                     4. $S \ge a$ for all $a \in U_A$.
                     5. $S \ge b$ for all $b \in U_B$.
                   - Since $S \ge \max(V_A \cup V_B)$, conditions 4 and 5 are always true.
                   - So we just need: Does there exist an integer $p \in [\max(0, k_A+k_B-N), \min(k_A, k_B)]$ such that we can find $p$ disjoint pairs $(a, b)$ with $a+b=S$?
                   - Actually, if we can find $p$ pairs, can we find $p+1$? Not necessarily.
                   - But notice: If we can find $p$ pairs, we satisfy the lower bound. Is it possible that we *must* form more pairs? No, we can always leave elements unpaired (fill with -1s) as long as the count of -1s allows.
                   - So the condition is simply: **Can we form at least $L = \max(0, k_A + k_B - N)$ pairs summing to $S$?**
                   - Wait, is it possible that forming $L$ pairs forces us to use specific elements, leaving others that violate $S \ge x$? No, because $S \ge \max(V_A \cup V_B)$ covers all elements.
                   - So the algorithm is:
                     1. Identify $V_A, V_B$.
                     2. If $V_A$ or $V_B$ is empty, check if $S$ (any non-negative) works?
                        - If $V_A$ empty, $k_A=0$. $L = \max(0, -k_B) = 0$. We need 0 pairs. Always possible?
                        - Yes, fill all A with $S$, fill B with $S$ (if B has -1s) or keep B (if B known). Wait, if B has knowns, we need $S \ge b$. We can choose $S = \max(B)$. Then fill A with $S-b$. Possible.
                        - So if $L=0$, answer is Yes (provided we can pick a valid $S$, which we can).
                     3. If $L > 0$:
                        - We need to find if there exists an $S$ such that the number of pairs $(a, b) \in V_A \times V_B$ with $a+b=S$ is $\ge L$.
                        - Candidate $S$ values: Only sums $a+b$ where $a \in V_A, b \in V_B$ matter.
                        - Iterate all $a \in V_A, b \in V_B$, let $S = a+b$.
                        - Check if $S \ge \max(V_A \cup V_B)$.
                        - Count pairs for this $S$. If count $\ge L$, return Yes.
                        - If loop finishes without success, return No.

## worker: Implement the solution in Python. Read N, A, B. Fi
1.  **Problem Analysis**: The problem asks if we can fill missing values (-1) in sequences A and B, and rearrange A, such that $A_i + B_i = S$ (constant) for all $i$, with all values non-negative.
2.  **Key Insight**:
    *   Let $V_A$ and $V_B$ be the sets of known values in A and B.
    *   Let $k_A = |V_A|$ and $k_B = |V_B|$.
    *   We can rearrange A arbitrarily. This means we can choose which known $a \in V_A$ pairs with which known $b \in V_B$.
    *   Let $p$ be the number of pairs $(a, b)$ where both are known and $a+b=S$.
    *   The remaining $k_A - p$ knowns in A must be paired with the $-1$s in B. The number of $-1$s in B is $N - k_B$. Thus, $k_A - p \le N - k_B \implies p \ge k_A + k_B - N$.
    *   Similarly, $k_B - p \le N - k_A \implies p \ge k_A + k_B - N$.
    *   So, we must form at least $L = \max(0, k_A + k_B - N)$ pairs summing to $S$.
    *   Additionally, for any unpaired known value $x$ (either in A or B), the corresponding filled value must be non-negative, i.e., $S - x \ge 0 \implies S \ge x$. This implies $S \ge \max(V_A \cup V_B)$.
3.  **Algorithm**:
    *   If $L = 0$, we don't need to form any specific pairs. We can simply choose $S = \max(V_A \cup V_B)$ (or 0 if empty) and fill the rest. Output "Yes".
    *   If $L > 0$, we need to find if there exists an $S \ge \max(V_A \cup V_B)$ such that the number of pairs $(a, b) \in V_A \times V_B$ with $a+b=S$ is at least $L$.
    *   Since $N \le 2000$, $|V_A| \cdot |V_B| \le 4 \times 10^6$. We can iterate through all pairs, compute their sum, and count frequencies.
    *   We only care about sums $S \ge \max(V_A \cup V_B)$.
    *   If any such sum has a count $\ge L$, output "Yes". Otherwise "No".
4.  **Complexity**: Time complexity is $O(|V_A| \cdot |V_B|)$, which fits within the time limit for $N=2000$. Space complexity is $O(|V_A| \cdot |V_B|)$ to store the counts.

## worker: [todo] If `forced_pairs > 0`:
The solution implements the logic derived in the thought process:
1.  **Input Parsing**: Reads N, A, and B from standard input.
2.  **Filtering**: Extracts known values ($V_A, V_B$) from the input sequences.
3.  **Constraint Calculation**: Calculates `forced_pairs` = $\max(0, |V_A| + |V_B| - N)$. This represents the minimum number of pairs $(a, b)$ where both $a \in V_A$ and $b \in V_B$ must sum to the target constant $S$.
4.  **Edge Case Handling**: If `forced_pairs` is 0, it's always possible to construct a valid sequence by choosing $S = \max(V_A \cup V_B)$ (or 0 if empty) and filling the rest. Output "Yes".
5.  **Main Logic**: If `forced_pairs > 0`, iterate through all pairs $(a, b) \in V_A \times V_B$. Calculate $S = a + b$. If $S \ge \max(V_A \cup V_B)$, increment the count for this $S$.
6.  **Validation**: Check if any $S$ has a count of pairs $\ge$ `forced_pairs`. If so, output "Yes", otherwise "No".
7.  **Complexity**: The nested loop runs $O(|V_A| \cdot |V_B|)$ times, which is at most $2000 \times 2000 = 4 \times 10^6$ operations, well within the time limits for Python.
