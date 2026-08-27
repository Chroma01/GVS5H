
## ideation
**Core Difficulty**: The problem involves checking consistency across two sequences where one can be permuted. The key constraint is that after filling $-1$s and rearranging $A$, every pair $(A_i, B_i)$ must sum to the same constant $S$. Since $A$ can be rearranged, the initial positions of known values in $A$ are irrelevant; only the multiset of known values in $A$ matters. However, the positions of known values in $B$ are fixed relative to the final array indices.

**Candidate Approaches**:
1.  **Consistency Check**:
    -   Identify all indices $i$ where both $A_i \neq -1$ and $B_i \neq -1$. Let this set be $K$.
    -   If $K$ is not empty, calculate $S = A_i + B_i$ for any $i \in K$. Verify that for all $j \in K$, $A_j + B_j = S$. If not, output "No".
    -   If $K$ is empty, $S$ is not yet determined by known pairs. We need to determine if there exists *some* non-negative integer $S$ that allows a valid filling.
2.  **Feasibility of $S$**:
    -   For any index $i$, if $A_i \neq -1$ and $B_i = -1$, we must have $B_i = S - A_i \geq 0 \implies S \geq A_i$.
    -   If $A_i = -1$ and $B_i \neq -1$, we must have $A_i = S - B_i \geq 0 \implies S \geq B_i$.
    -   If both are $-1$, we can choose any non-negative $A_i, B_i$ such that $A_i + B_i = S$. This is always possible for any $S \geq 0$ (e.g., $A_i=S, B_i=0$).
    -   Therefore, if $K$ is empty, the condition reduces to finding an $S \geq 0$ such that $S \geq \max(\{A_i \mid B_i=-1\} \cup \{B_i \mid A_i=-1\} \cup \{0\})$. Since we can pick arbitrarily large integers, such an $S$ always exists.
    -   **Wait, is there a catch?** The problem allows rearranging $A$. Does this change the constraints?
        -   If we rearrange $A$, we are effectively matching the multiset of known values in $A$ to the slots in $B$.
        -   Let $A_{known}$ be the multiset of non-negative values currently in $A$.
        -   Let $B_{known}$ be the sequence of non-negative values currently in $B$ (at specific indices).
        -   We need to pair elements from $A_{known}$ with elements from $B$ (some known, some $-1$) such that sums are equal to $S$.
        -   Actually, the operation "Rearrange A" means we can assign any $A_{known}$ value to any index $i$.
        -   So, for each index $i$, we have a target sum $S$.
        -   If $B_i \neq -1$, we need an $A$ value $x \in A_{known}$ such that $x + B_i = S \implies x = S - B_i$.
        -   If $B_i = -1$, we can use any remaining $x \in A_{known}$ (since we can set $A_i = x, B_i = S-x$, provided $S-x \geq 0$).
        -   **Crucial Logic**:
            -   Case 1: Both $A_i, B_i$ known initially. They must sum to $S$. If multiple such pairs exist, they must all sum to the same $S$. If inconsistent -> No.
            -   Case 2: Some pairs are fully known. Let this define $S$. Then check if we can fill the rest.
                -   For indices where $B_i \neq -1$ but $A_i = -1$: We need to fill $A_i = S - B_i$. This requires $S \geq B_i$. Also, we don't need to consume a specific value from $A_{known}$ here because $A_i$ was $-1$. Wait, the operation is "Replace $A_i=-1$ with any non-negative". So if $A_i$ is $-1$, we can just pick the value $S-B_i$ directly. We don't need to use a value from the original $A_{known}$ multiset for this slot. The original $A_{known}$ values are only needed for slots where $A_i$ is *already* non-negative.
                -   Let's re-read carefully: "Choose an index i such that $A_i = -1$, and replace...". "Rearrange A".
                -   So, we have a multiset $M_A$ of known values in $A$. We have a sequence $B$.
                -   We permute $M_A$ to form a sequence $A'$.
                -   Then we fill $-1$s in $A'$ and $B$ with non-negative integers.
                -   Condition: $A'_i + B_i = S$ for all $i$.
                -   For indices where $B_i \neq -1$:
                    -   If $A'_i$ comes from $M_A$ (i.e., original $A_k$ was non-negative), then $A_k + B_i = S$. This implies that for every $k$ where $A_k \neq -1$, if we place it at index $i$ where $B_i \neq -1$, then $A_k + B_i$ must be $S$.
                    -   If $A'_i$ is filled (was $-1$), then $A'_i = S - B_i$. This requires $S \geq B_i$.
                -   For indices where $B_i = -1$:
                    -   $A'_i$ can be from $M_A$ or filled.
                    -   If from $M_A$: $A_k + (-1 \text{ slot}) = S \implies A_k = S - A'_i$. Wait, if $B_i=-1$, we set $B'_i = S - A'_i$. Since we can choose $B'_i \geq 0$, we just need $S \geq A'_i$.
                    -   If filled: $A'_i$ is new, $B'_i$ is new. $A'_i + B'_i = S$. Always possible for any $S \geq 0$.
    
    **Refined Logic**:
    1.  Calculate $S$ from any pair $(i, j)$ where $A_i \neq -1$ and $B_i \neq -1$. If multiple such pairs exist, all must yield the same sum. If not, return "No". If none exist, $S$ is free (but must be $\geq 0$).
    2.  Let $M_A$ be the multiset of known values in $A$.
    3.  Let $B_{fixed}$ be the list of values in $B$ where $B_i \neq -1$.
    4.  Let $B_{free}$ be the count of indices where $B_i = -1$.
    5.  We need to match elements of $M_A$ to indices $i$ such that $B_i \neq -1$.
        -   Why? Because if we place an element $x \in M_A$ at an index $i$ where $B_i \neq -1$, then $x + B_i = S \implies x = S - B_i$.
        -   If $x \neq S - B_i$, we cannot place $x$ there.
        -   If $x = S - B_i$, we can place it there.
        -   If we place $x$ at an index where $B_i = -1$, then $x + B'_i = S \implies B'_i = S - x$. This is valid as long as $S \geq x$.
    6.  So, the strategy is:
        -   Determine $S$.
        -   Identify which elements of $M_A$ *must* be placed at indices with $B_i \neq -1$.
            -   Actually, we have a choice. We can put any $x \in M_A$ anywhere.
            -   However, if we put $x$ at an index $i$ where $B_i \neq -1$, we *require* $x = S - B_i$.
            -   If we put $x$ at an index $i$ where $B_i = -1$, we *require* $x \leq S$.
        -   Let $U$ be the set of indices where $B_i \neq -1$. Let $V$ be the set of indices where $B_i = -1$.
        -   We need to partition $M_A$ into two sets $P$ (placed in $U$) and $Q$ (placed in $V$).
        -   For $p \in P$ and $i \in U$, we must have $p = S - B_i$.
        -   For $q \in Q$ and $j \in V$, we must have $q \leq S$.
        -   Also, the sizes must match: $|P| = |U|$? No, $|P|$ is the number of elements from $M_A$ we choose to put in $U$. The remaining $|M_A| - |P|$ go to $V$.
        -   Wait, the indices in $U$ must be filled. Some are filled by $M_A$, some by new values (from filling $-1$s in $A$).
        -   Let $k = |M_A|$.
        -   Let $n_U = |U|$ (count of $B_i \neq -1$).
        -   Let $n_V = |V|$ (count of $B_i = -1$).
        -   We choose $x$ elements from $M_A$ to fill $x$ slots in $U$. The remaining $n_U - x$ slots in $U$ are filled by new values.
        -   The remaining $k - x$ elements of $M_A$ go to $V$. The remaining $n_V - (k-x)$ slots in $V$ are filled by new values.
        -   Constraints:
            1.  The $x$ elements chosen for $U$ must be exactly the set $\{S - B_i \mid i \in U_{chosen}\}$. But we can choose which $i \in U$ to fill with $M_A$.
            2.  Actually, simpler: For every $i \in U$, if we decide to use a value from $M_A$, say $v$, then $v = S - B_i$. If we don't use a value from $M_A$, we fill $A_i$ with $S - B_i$ (which is valid since $S \geq B_i$ is required for the fill to be non-negative).
            3.  So, for each $i \in U$, we have a requirement: either we provide a specific value $S - B_i$ from $M_A$, OR we provide a new value (which requires $S \geq B_i$).
            4.  For each $j \in V$, if we use a value $v \in M_A$, we need $v \leq S$. If we use a new value, no constraint on $S$ other than $S \geq 0$.
    
    **Simplified Algorithm**:
    1.  Collect all pairs $(A_i, B_i)$ where both are non-negative. Check if they all sum to the same $S$. If not, return "No". If none, $S$ is undefined (free).
    2.  If $S$ is defined:
        -   Check if for all $i$ where $B_i \neq -1$, $S \geq B_i$. If any $B_i > S$, we cannot fill $A_i$ (since $A_i = S - B_i < 0$). Return "No".
        -   Now, we have a multiset $M_A$ of known values in $A$.
        -   We need to match a subset of $M_A$ to a subset of indices $U = \{i \mid B_i \neq -1\}$.
        -   Specifically, for each $i \in U$, if $B_i \neq S$, then we *cannot* fill $A_i$ with a value from $M_A$ unless $M_A$ contains exactly $S - B_i$. But wait, if $B_i \neq S$, then $S - B_i \neq 0$. If $B_i = S$, then $S - B_i = 0$.
        -   Actually, the condition is: For each $i \in U$, we need $A_i + B_i = S$.
            -   Option A: Use a value $v \in M_A$. Then $v = S - B_i$.
            -   Option B: Fill $A_i$ with $S - B_i$. Valid if $S \geq B_i$.
        -   So, for each $i \in U$, we can satisfy it either by consuming a specific $v = S - B_i$ from $M_A$, or by creating a new value (costing nothing from $M_A$).
        -   However, we must use *all* elements of $M_A$ somewhere.
        -   Where can elements of $M_A$ go?
            -   To $U$: Must satisfy $v = S - B_i$.
            -   To $V$: Must satisfy $v \leq S$.
        -   Let $req\_U$ be the multiset of values $\{S - B_i \mid i \in U\}$. Note: If $S < B_i$, this is invalid immediately (handled above).
        -   We need to partition $M_A$ into $M_{U}$ and $M_{V}$ such that:
            -   $M_{U} \subseteq req\_U$ (actually, since we can choose which $i \in U$ to fill, $M_{U}$ must be a sub-multiset of $req\_U$? No. $req\_U$ is the set of *required* values if we fill with $M_A$. If we don't fill with $M_A$, we don't need that value. So $M_{U}$ must be a sub-multiset of $req\_U$? Yes, because if we put $v \in M_{U}$ at index $i$, then $v$ must equal $S - B_i$. So $v$ must be in $req\_U$).
            -   $M_{V} \subseteq \{v \mid v \leq S\}$.
        -   Wait, is it "subset"? We can choose to put *fewer* elements of $M_A$ into $U$ than $|U|$. The rest of $U$ is filled by new values.
        -   So, we need to find a sub-multiset $M_{U} \subseteq M_A$ such that $M_{U} \subseteq req\_U$ (element-wise count) and the remaining elements $M_A \setminus M_{U}$ satisfy $\forall v \in M_A \setminus M_{U}, v \leq S$.
        -   This is equivalent to: Can we remove some elements from $M_A$ such that the remaining ones are all $\leq S$, and the removed ones can cover the "gaps" in $req\_U$?
        -   Actually, simpler:
            -   Let $cnt[v]$ be the count of value $v$ in $M_A$.
            -   Let $need[v]$ be the count of value $v$ in $req\_U$ (i.e., count of $i \in U$ such that $S - B_i = v$).
            -   We need to select a count $k_v \leq cnt[v]$ to assign to $U$ such that $k_v \leq need[v]$.
            -   The remaining count $cnt[v] - k_v$ must satisfy $v \leq S$.
            -   To maximize our chances, we should greedily assign as many elements as possible to $U$ that satisfy the condition, or rather, check if there exists *any* valid assignment.
            -   Actually, the constraint is: For every $v > S$, we *must* assign it to $U$ (because it cannot go to $V$).
            -   So, for all $v > S$, we must have $cnt[v] \leq need[v]$. If $cnt[v] > need[v]$, return "No".
            -   For $v \leq S$, we can assign them to $U$ or $V$.
            -   The total number of slots in $U$ is $|U| = \sum_{v} need[v]$.
            -   The number of elements we *must* put in $U$ is $\sum_{v > S} cnt[v]$.
            -   The remaining elements $\sum_{v \leq S} cnt[v]$ can go to $U$ or $V$.
            -   We need to fill $U$ completely? No, we fill $U$ with either $M_A$ or new values.
            -   We need to fill $V$ with either $M_A$ or new values.
            -   The only hard constraint is that elements $> S$ cannot go to $V$. They must go to $U$.
            -   So, if $\sum_{v > S} cnt[v] > |U|$, impossible (not enough slots in $U$).
            -   Also, for each specific value $v > S$, we need $cnt[v] \leq need[v]$ (since each slot in $U$ requiring $v$ can only take one $v$).
            -   Is that it?
            -   What about $v \leq S$? They can go to $U$ or $V$. Is there any restriction?
                -   If we put $v \leq S$ in $U$, it must match a slot $i$ where $S - B_i = v$.
                -   If we put $v \leq S$ in $V$, it's fine ($S - v \geq 0$).
                -   So we can always put $v \leq S$ in $V$.
                -   The only risk is if we are forced to put them in $U$ but there aren't enough matching slots? No, we can always choose to put them in $V$ instead.
                -   The only constraint is that we cannot put $v > S$ in $V$.
                -   So the condition is simply:
                    1.  For all $v \in M_A$, if $v > S$, then $cnt[v] \leq need[v]$.
                    2.  Sum of counts of $v > S$ must be $\leq |U|$. (This is implied by 1 since $\sum need[v] = |U|$).
            -   Wait, is it possible that $need[v]$ is 0 for some $v > S$? Yes. Then if $cnt[v] > 0$, we fail.
            -   So the condition is: For every value $v$ present in $M_A$, if $v > S$, then the number of times $v$ appears in $M_A$ must be $\leq$ the number of indices $i \in U$ such that $S - B_i = v$.
    
    3.  If $S$ is NOT defined (no fully known pairs):
        -   We need to find *some* $S \geq 0$.
        -   Constraints on $S$:
            -   For all $i \in U$, if we fill with new value, need $S \geq B_i$. If we fill with $M_A$ value $v$, need $S = v + B_i$.
            -   For all $j \in V$, if we fill with $M_A$ value $v$, need $S \geq v$.
        -   Since we can choose $S$ arbitrarily large, can we always satisfy this?
        -   If we pick $S$ very large (e.g., $S = \max(M_A) + \max(B_{fixed}) + 100$):
            -   Then for all $v \in M_A$, $v \leq S$. So condition 1 ($v > S$) is never met.
            -   For all $i \in U$, $S \geq B_i$ holds.
            -   Can we always arrange?
                -   We need to match $M_A$ to slots.
                -   If we pick $S$ large enough, $v \leq S$ for all $v$. So all $v$ can go to $V$.
                -   Can we fill $U$? Yes, with new values (since $S \geq B_i$).
                -   So if $S$ is free, the answer is always "Yes"?
                -   Wait, is there a constraint I missed? "non-negative integer". Yes.
                -   Is it possible that we *must* use a value from $M_A$ in $U$ such that $v + B_i = S$?
                -   No, we can always choose to fill $A_i$ with a new value for any $i \in U$. The only reason to use $M_A$ in $U$ is if we have "extra" elements in $M_A$ that must go somewhere, and $V$ is full?
                -   No, $V$ is not full; we can fill $V$ with new values too.
                -   The only constraint is that we must use *all* elements of $M_A$.
                -   If $S$ is large, all $v \in M_A$ satisfy $v \leq S$, so they can all go to $V$.
                -   Then $U$ is filled entirely with new values.
                -   This seems to imply if $S$ is free, answer is always Yes.
                -   Let's check Sample 2: $A=(1,2,3), B=(1,2,4)$. No $-1$. $S$ is fixed. $1+1=2, 2+2=4, 3+4=7$. Inconsistent. Output No. Correct.
                -   Sample 3: $A=(1,2,-1), B=(1,2,4)$.
                    -   Pairs: $(1,1) \to 2$, $(2,2) \to 4$. Inconsistent. Output No. Correct.
                -   What if $A=(1, -1), B=(-1, 2)$?
                    -   No fully known pairs. $S$ free.
                    -   $M_A = \{1\}$. $U=\{2\}$ (index 1, $B_1=2$), $V=\{1\}$ (index 0, $B_0=-1$).
                    -   Pick $S=10$. $1 \leq 10$. Put $1$ in $V$. Fill $U$ with new value $10-2=8$. Valid.
                -   Is there any case where $S$ free fails?
                    -   Maybe if $M_A$ has elements that force $S$ to be small? No, we can always increase $S$.
                    -   Maybe if $B_i$ are very large? $S$ must be $\geq B_i$. We can pick $S$ large.
                    -   So if no fully known pairs, answer is "Yes"?
                    -   Wait, what if $A$ has $-1$ and $B$ has $-1$?
                    -   Example: $A=(-1, -1), B=(-1, -1)$. $S$ free. Yes.
                    -   Example: $A=(100), B=(-1)$. $S$ free. $M_A=\{100\}$. $U=\emptyset, V=\{1\}$. Put 100 in $V$. Need $S \geq 100$. Pick $S=100$. $A_1=100, B_1=0$. Valid.
                    -   It seems if no fixed pairs, always Yes.
    
    **Wait, re-verify Sample 3**:
    $A = [1, 2, -1]$, $B = [1, 2, 4]$.
    Indices:
    0: $A=1, B=1 \implies S=2$.
    1: $A=2, B=2 \implies S=4$.
    Contradiction. So No.

## worker: Identify indices where both $A_i$ and $B_i$ are kn
The problem asks if we can make $A_i + B_i = S$ for all $i$ by filling $-1$s and rearranging $A$.
1.  **Consistency Check**: First, identify all indices where both $A_i$ and $B_i$ are known. If there are any such indices, they must all sum to the same value $S$. If not, output "No".
2.  **Feasibility Check**: If $S$ is determined:
    *   For any index $i$ where $B_i \neq -1$, we must be able to form the sum $S$. If $A_i$ is known, it's already consistent. If $A_i = -1$, we must fill it with $S - B_i$. This is valid only if $S - B_i \geq 0 \implies S \geq B_i$.
    *   We also need to ensure that the known values in $A$ (let's call the multiset $M_A$) can be distributed.
        *   Values in $M_A$ can be placed at indices where $B_i \neq -1$ (set $U$) or where $B_i = -1$ (set $V$).
        *   If placed in $U$ at index $i$, the value $v$ must satisfy $v + B_i = S \implies v = S - B_i$.
        *   If placed in $V$, the value $v$ must satisfy $v + B'_i = S$ where $B'_i \geq 0 \implies v \leq S$.
        *   Therefore, any value $v \in M_A$ such that $v > S$ **cannot** be placed in $V$. It **must** be placed in $U$.
        *   For such values to be valid, there must be enough slots in $U$ that require exactly $v$. Specifically, the count of $v$ in $M_A$ must not exceed the count of indices $i \in U$ where $S - B_i = v$.
3.  **Free $S$**: If there are no indices where both $A_i$ and $B_i$ are known, we can choose $S$ arbitrarily large. This ensures $S \geq B_i$ for all $i$ and $v \leq S$ for all $v \in M_A$. Thus, we can always satisfy the conditions. Output "Yes".

The logic covers all constraints and edge cases derived from the problem statement.

## worker: Refine the logic for determining $S$ and the valid
The solution implements the refined logic:
1.  **Consistency Check**: It first identifies all indices where both $A_i$ and $B_i$ are known. If such indices exist, they must all yield the same sum $S$. If not, output "No".
2.  **Feasibility with Fixed $S$**:
    *   If $S$ is determined, verify that for every index $i$ where $B_i \neq -1$, $S \geq B_i$. If $B_i > S$, we cannot fill $A_i$ with a non-negative integer to reach sum $S$.
    *   Analyze the multiset of known values in $A$ ($M_A$). Values in $M_A$ greater than $S$ cannot be placed in positions where $B_i = -1$ (because $A_i + B'_i = S \implies B'_i = S - A_i < 0$). Therefore, any value $v \in M_A$ with $v > S$ must be placed at an index $i$ where $B_i \neq -1$ and specifically $S - B_i = v$. The code checks if the count of such values in $M_A$ does not exceed the count of available slots in $U$ (indices with $B_i \neq -1$) that require exactly $v$.
3.  **Free $S$**: If no fully known pairs exist, the code outputs "Yes". This is because we can always choose a sufficiently large $S$ such that $S \geq \max(B_{known})$ and $S \geq \max(A_{known})$. This allows all known $A$ values to be placed in $V$ (where $B_i = -1$) and all $U$ slots to be filled with new values.

## worker: Write the complete Python code to stdin/stdout.
The solution implements the logic derived in the thought process:
1.  **Consistency Check**: First, it identifies all indices where both $A_i$ and $B_i$ are known. If such indices exist, they must all sum to the same value $S$. If not, the answer is "No".
2.  **Feasibility with Fixed $S$**:
    *   If $S$ is determined, it verifies that for every index $i$ where $B_i \neq -1$, $S \geq B_i$. If $B_i > S$, we cannot fill $A_i$ with a non-negative integer to reach sum $S$.
    *   It then analyzes the multiset of known values in $A$ ($M_A$). Values in $M_A$ greater than $S$ cannot be placed in positions where $B_i = -1$ (because $A_i + B'_i = S \implies B'_i = S - A_i < 0$). Therefore, any value $v \in M_A$ with $v > S$ must be placed at an index $i$ where $B_i \neq -1$ and specifically $S - B_i = v$. The code checks if the count of such values in $M_A$ does not exceed the count of available slots in $U$ (indices with $B_i \neq -1$) that require exactly $v$.
3.  **Free $S$**: If no fully known pairs exist, the code outputs "Yes". This is because we can always choose a sufficiently large $S$ such that $S \geq \max(B_{known})$ and $S \geq \max(A_{known})$. This allows all known $A$ values to be placed in $V$ (where $B_i = -1$) and all $U$ slots to be filled with new values.
