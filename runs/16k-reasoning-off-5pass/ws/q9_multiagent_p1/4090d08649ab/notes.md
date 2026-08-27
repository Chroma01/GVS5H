
## ideation
The problem asks for the sum of $f(L,R)$ over all $1 \le L \le R \le N$.
Based on the analysis of the operation rules:
1.  An operation removes all occurrences of a contiguous range of values $[l, r]$ present on the blackboard.
2.  This implies that in one step, we can remove a set of values $S$ if and only if $S$ forms a contiguous range of integers (i.e., if $u, v \in S$ and $u < v$, then all integers between $u$ and $v$ must also be in $S$).
3.  The process repeats until the blackboard is empty. To minimize operations, we should greedily remove the largest possible contiguous ranges of values.
4.  Consequently, $f(L,R)$ is equal to the number of connected components of the set of unique values present in the subarray $A[L..R]$, where connectivity is defined by $u \sim v \iff |u-v|=1$.
    -   Specifically, if the unique values in $A[L..R]$ are $u_1 < u_2 < \dots < u_k$, then $f(L,R) = 1 + \sum_{i=1}^{k-1} [u_{i+1} \neq u_i + 1]$.
    -   This is equivalent to counting the number of $x$ in the unique values such that $x-1$ is NOT in the unique values.

We need to compute:
$$ \text{Total} = \sum_{L=1}^N \sum_{R=L}^N \sum_{x \in \text{Unique}(L,R)} [x-1 \notin \text{Unique}(L,R)] $$
By swapping the summation order, we can iterate over each value $x$ from $1$ to $N$ and count how many pairs $(L,R)$ satisfy:
1.  $x$ is present in $A[L..R]$.
2.  $x-1$ is NOT present in $A[L..R]$.

Let $first(v)$ and $last(v)$ be the first and last indices where value $v$ appears in $A$.
-   Condition 1 ($x$ present): $L \le last(x)$ and $R \ge first(x)$.
-   Condition 2 ($x-1$ absent): The range $[L, R]$ contains no occurrence of $x-1$.

For a fixed $x$:
-   Calculate the number of pairs $(L,R)$ where $x$ is present. Let this be $C_x$.
-   If $x > 1$, calculate the number of pairs $(L,R)$ where BOTH $x$ and $x-1$ are present. Let this be $C_{x, x-1}$.
-   The contribution of $x$ to the answer is $C_x - C_{x, x-1}$.
-   If $x=1$, the contribution is $C_1$ (since $0$ is never in the array).

Calculating $C_{a, b}$ (pairs containing both $a$ and $b$):
-   Let $L_{lim} = \min(last(a), last(b))$ and $R_{lim} = \max(first(a), first(b))$.
-   We need $L \le L_{lim}$ and $R \ge R_{lim}$ with $L \le R$.
-   If $L_{lim} < R_{lim}$, count is 0.
-   Otherwise, the number of pairs is the number of valid $(L,R)$ in the rectangle $[1, L_{lim}] \times [R_{lim}, N]$ intersected with $L \le R$.
    -   Number of such pairs = $\sum_{L=1}^{L_{lim}} (\text{count of } R \in [R_{lim}, N] \text{ s.t. } R \ge L)$.
    -   If $L \le R_{lim}$, $R$ can be anything in $[R_{lim}, N]$. Count = $N - R_{lim} + 1$.
    -   If $L > R_{lim}$, $R$ can be anything in $[L, N]$. Count = $N - L + 1$.
    -   Sum = $R_{lim} \times (N - R_{lim} + 1) + \sum_{L=R_{lim}+1}^{L_{lim}} (N - L + 1)$.
    -   The second part is an arithmetic progression sum.

This approach is $O(N)$ time complexity, which fits the constraints ($N \le 3 \times 10^5$).

## worker: [todo] Implement the full solution in Python: read
The problem asks for the sum of the minimum operations $f(L,R)$ required to clear subarrays.
1.  **Analysis of $f(L,R)$**: The operation allows removing a contiguous range of values $[l, r]$ if all integers in that range are currently present. This implies that one operation can remove a set of values that forms a contiguous block of integers. To minimize operations, we should greedily remove the largest possible contiguous blocks. Thus, $f(L,R)$ is equal to the number of connected components of the set of unique values in $A[L..R]$ under the relation $u \sim v \iff |u-v|=1$.
2.  **Combinatorial Reformulation**: $f(L,R) = \sum_{x \in \text{Unique}(L,R)} [x-1 \notin \text{Unique}(L,R)]$.
    We need to compute $\sum_{L,R} \sum_{x} [x \in \text{Unique}(L,R) \land x-1 \notin \text{Unique}(L,R)]$.
    Swapping sums: $\sum_{x} (\text{Count}(x \in \text{Unique}) - \text{Count}(x \in \text{Unique} \land x-1 \in \text{Unique}))$.
3.  **Counting Logic**:
    -   $x \in \text{Unique}(L,R)$ iff the range $[L,R]$ contains at least one occurrence of $x$. This is equivalent to $L \le \text{last}(x)$ and $R \ge \text{first}(x)$.
    -   The number of such pairs $(L,R)$ with $0 \le L \le R < N$ can be calculated efficiently.
    -   Similarly for the intersection with $x-1$.
4.  **Complexity**: We iterate over unique values (at most $N$) and perform $O(1)$ arithmetic calculations for each. Total time complexity is $O(N)$. Space complexity is $O(N)$ to store first/last occurrences.

## worker: Run the code against the provided sample inputs to
The solution implements the derived logic:
1.  **Problem Interpretation**: $f(L,R)$ is the number of connected components of unique values in $A[L..R]$ where connectivity is defined by $|u-v|=1$. This equals the count of unique values $x$ in the subarray such that $x-1$ is NOT in the subarray.
2.  **Summation Swap**: The total sum is $\sum_{x} (\text{count}(x \in \text{Unique}) - \text{count}(x \in \text{Unique} \land x-1 \in \text{Unique}))$.
3.  **Counting Logic**:
    -   $x \in \text{Unique}(L,R)$ iff $L \le \text{last}(x)$ and $R \ge \text{first}(x)$.
    -   The number of valid pairs $(L,R)$ with $0 \le L \le R < N$ satisfying these bounds is calculated using a helper function `count_pairs`.
    -   The intersection case ($x$ and $x-1$ both present) requires $L \le \min(\text{last}(x), \text{last}(x-1))$ and $R \ge \max(\text{first}(x), \text{first}(x-1))$.
4.  **Complexity**: $O(N)$ time to scan the array, sort unique values (at most $N$), and iterate. Space $O(N)$.

## worker: Run the code against Sample 1, 2, and 3 to verify 
The code implements the derived $O(N)$ solution.
1.  **Logic**: It calculates the sum of $f(L,R)$ by iterating over each value $x$ and counting how many subarrays $A[L..R]$ contain $x$ but do not contain $x-1$.
2.  **Counting**: `count_pairs(L_lim, R_lim)` calculates the number of valid $(L, R)$ pairs where $0 \le L \le R < N$, $L \le L_{lim}$, and $R \ge R_{lim}$. This is done by splitting the range of $L$ into two parts: $L \le R_{lim}$ and $L > R_{lim}$, summing the valid $R$ counts for each.
3.  **Verification**:
    -   **Sample 1**: Input `4 \n 1 3 1 4`. Unique values: 1, 3, 4.
        -   $x=1$: Present in $[0, 2]$ (indices). Pairs: $L \le 2, R \ge 0$. Count = $3 \times 4 + \dots = 10$. $x-1=0$ not present. Add 10.
        -   $x=3$: Present in $[1, 1]$. Pairs: $L \le 1, R \ge 1$. Count = $2 \times 3 + 1 = 7$. $x-1=2$ not present. Add 7.
        -   $x=4$: Present in $[3, 3]$. Pairs: $L \le 3, R \ge 3$. Count = $4 \times 1 + 3 = 7$. $x-1=3$ present.
            -   Intersection ($3, 4$): $L \le \min(1, 3)=1, R \ge \max(1, 3)=3$. Pairs: $L \le 1, R \ge 3$. Count = $2 \times 1 = 2$.
            -   Net for 4: $7 - 2 = 5$.
        -   Total: $10 + 7 + 5 = 22$. Wait, Sample 1 output is 16.
        -   Let's re-verify the logic.
        -   $f(L,R)$ is number of connected components of unique values.
        -   Unique values in $A[1..4]$ (indices 0..3): $\{1, 3, 4\}$. Components: $\{1\}, \{3, 4\}$. Count = 2.
        -   My formula: $\sum_{x \in Unique} [x-1 \notin Unique]$.
            -   $x=1$: $0 \notin \{1, 3, 4\}$. Yes.
            -   $x=3$: $2 \notin \{1, 3, 4\}$. Yes.
            -   $x=4$: $3 \in \{1, 3, 4\}$. No.
            -   Sum = 2. Correct.
        -   Why did my manual trace of counts yield 22?
            -   $x=1$: Indices $\{0, 2\}$. $first=0, last=2$.
                -   $L \in [0, 2], R \in [0, 3], L \le R$.
                -   $L=0: R \in [0,3] \to 4$
                -   $L=1: R \in [0,3] \to 4$ (since $1 \le R$) -> Wait, $R \ge first=0$. So $R \in [0,3]$. But $L \le R$.
                -   $L=0: R \in [0,3] \to 4$
                -   $L=1: R \in [1,3] \to 3$
                -   $L=2: R \in [2,3] \to 2$
                -   Total = 9.
            -   $x=3$: Indices $\{1\}$. $first=1, last=1$.
                -   $L \in [0, 1], R \in [1, 3], L \le R$.
                -   $L=0: R \in [1,3] \to 3$
                -   $L=1: R \in [1,3] \to 3$
                -   Total = 6.
            -   $x=4$: Indices $\{3\}$. $first=3, last=3$.
                -   $L \in [0, 3], R \in [3, 3], L \le R$.
                -   $L=0: R=3 \to 1$
                -   $L=1: R=3 \to 1$
                -   $L=2: R=3 \to 1$
                -   $L=3: R=3 \to 1$
                -   Total = 4.
            -   Intersection ($3, 4$): $first(3)=1, last(3)=1, first(4)=3, last(4)=3$.
                -   $L \le \min(1, 3)=1, R \ge \max(1, 3)=3$.
                -   $L \in [0, 1], R \in [3, 3], L \le R$.
                -   $L=0: R=3 \to 1$
                -   $L=1: R=3 \to 1$
                -   Total = 2.
            -   Sum: $9 + 6 + (4 - 2) = 17$. Still not 16.
            -   Let's re-check $x=1$ count.
                -   $L \le 2, R \ge 0, L \le R$.
                -   $L=0: R \in [0,3] \to 4$
                -   $L=1: R \in [1,3] \to 3$
                -   $L=2: R \in [2,3] \to 2$
                -   Total = 9. Correct.
            -   Let's re-check $x=3$ count.
                -   $L \le 1, R \ge 1, L \le R$.
                -   $L=0: R \in [1,3] \to 3$
                -   $L=1: R \in [1,3] \to 3$
                -   Total = 6. Correct.
            -   Let's re-check $x=4$ count.
                -   $L \le 3, R \ge 3, L \le R$.
                -   $L=0: R=3 \to 1$
                -   $L=1: R=3 \to 1$
                -   $L=2: R=3 \to 1$
                -   $L=3: R=3 \to 1$
                -   Total = 4. Correct.
            -   Intersection: 2.
            -   Sum = 17.
            -   Wait, Sample 1 output is 16.
            -   Let's manually calculate $f(L,R)$ for all pairs.
                -   (1,1): {1} -> 1
                -   (1,2): {1,3} -> 2 (1, 3)
                -   (1,3): {1,3} -> 2 (1, 3)
                -   (1,4): {1,3,4} -> 2 ({1}, {3,4})
                -   (2,2): {3} -> 1
                -   (2,3): {3,1} -> 2 ({1}, {3})
                -   (2,4): {3,1,4} -> 2 ({1}, {3,4})
                -   (3,3): {1} -> 1
                -   (3,4): {1,4} -> 2 ({1}, {4})
                -   (4,4): {4} -> 1
                -   Sum: 1+2+2+2 + 1+2+2 + 1+2 + 1 = 16.
            -   My calculation gave 17. Where is the error?
            -   Ah, $x=1$ count: $L \le 2, R \ge 0$.
                -   Pairs: (0,0), (0,1), (0,2), (0,3), (1,1), (1,2), (1,3), (2,2), (2,3). Total 9.
                -   Are all these valid? Yes, 1 is at 0 and 2.
            -   $x=3$ count: $L \le 1, R \ge 1$.
                -   Pairs: (0,1), (0,2), (0,3), (1,1), (1,2), (1,3). Total 6.
            -   $x=4$ count: $L \le 3, R \ge 3$.
                -   Pairs: (0,3), (1,3), (2,3), (3,3). Total 4.
            -   Intersection ($3,4$): $L \le 1, R \ge 3$.
                -   Pairs: (0,3), (1,3). Total 2.
            -   Sum: $9 + 6 + (4-2) = 17$.
            -   Why is the manual sum 16?
                -   (1,1): {1}. $x=1$ present. $x-1=0$ no. Count 1.
                -   (1,2): {1,3}. $x=1$ yes, $x=3$ yes.
                    -   Contribution of 1: $1-1=0$ (since 0 not present). Wait.
                    -   Formula: $\sum_{x \in Unique} [x-1 \notin Unique]$.
                    -   For {1,3}: $x=1 \to 0 \notin \{1,3\}$ (Yes). $x=3 \to 2 \notin \{1,3\}$ (Yes). Sum = 2. Correct.
                -   (1,3): {1,3}. Sum = 2.
                -   (1,4): {1,3,4}. $x=1 \to$ Yes. $x=3 \to$ Yes. $x=4 \to 3 \in \{1,3,4\}$ (No). Sum = 2. Correct.
                -   (2,2): {3}. $x=3 \to 2 \notin \{3\}$ (Yes). Sum = 1.
                -   (2,3): {3,1}. $x=1 \to$ Yes. $x=3 \to$ Yes. Sum = 2.
                -   (2,4): {3,1,4}. $x=1 \to$ Yes. $x=3 \to$ Yes. $x=4 \to$ No. Sum = 2.
                -   (3,3): {1}. $x=1 \to$ Yes. Sum = 1.
                -   (3,4): {1,4}. $x=1 \to$ Yes. $x=4 \to$ No. Sum = 1. **Wait**.
                    -   Unique {1, 4}. $x=1 \to 0 \notin$ (Yes). $x=4 \to 3 \notin$ (Yes). Sum = 2.
                    -   My manual trace above said 2.
                -   (4,4): {4}. $x=4 \to 3 \notin$ (Yes). Sum = 1.
                -   Total: 1+2+2+2 + 1+2+2 + 1+2 + 1 = 16.
            -   So the formula works. Why did my count give 17?
            -   Let's re-evaluate $x=1$ count.
                -   $first(1)=0, last(1)=2$.
                -   Pairs $(L,R)$ with $L \le 2, R \ge 0, L \le R$.
                -   $L=0: R \in [0,3] \to 4$.
                -   $L=1: R \in [1,3] \to 3$.
                -   $L=2: R \in [2,3] \to 2$.
                -   Total 9.
            -   $x=3$ count.
                -   $first(3)=1, last(3)=1$.
                -   $L \le 1, R \ge 1, L \le R$.
                -   $L=0: R \in [1,3] \to 3$.
                -   $L=1: R \in [1,3] \to 3$.
                -   Total 6.
            -   $x=4$ count.
                -   $first(4)=3, last(4)=3$.
                -   $L \le 3, R \ge 3, L \le R$.
                -   $L=0: R=3 \to 1$.
                -   $L=1: R=3 \to 1$.
                -   $L=2: R=3 \to 1$.
                -   $L=3: R=3 \to 1$.
                -   Total 4.
            -   Intersection ($3,4$).
                -   $L \le 1, R \ge 3, L \le R$.
                -   $L=0: R=3 \to 1$.
                -   $L=1: R=3 \to 1$.
                -   Total 2.
            -   Sum: $9 + 6 + (4-2) = 17$.
            -   There must be a double counting or logic error in the formula application.
            -   Formula: $\sum_{L,R} \sum_{x \in Unique(L,R)} [x-1 \notin Unique(L,R)]$.
            -   Let's check specific pair (3,4) -> indices 2,3 -> values 1, 4. Unique {1, 4}.
                -   $x=1$: Present? Yes. $0 \notin \{1,4\}$? Yes. Count 1.
                -   $x=4$: Present? Yes. $3 \notin \{1,4\}$? Yes. Count 1.
                -   Total contribution 2.
                -   My counts:
                    -   $x=1$ includes (2,3)? $L=2 \le 2, R=3 \ge 0$. Yes.
                    -   $x=4$ includes (2,3)? $L=2 \le 3, R=3 \ge 3$. Yes.
                    -   Intersection ($3,4$) includes (2,3)? $L=2 \le 1$? No.
                    -   So for (2,3), we count $x=1$ and $x=4$. Total 2. Correct.
            -   Let's check pair (1,4) -> indices 0..3 -> values 1,3,1,4. Unique {1,3,4}.
                -   $x=1$: Yes. $0 \notin$? Yes.
                -   $x=3$: Yes. $2 \notin$? Yes.
                -   $x=4$: Yes. $3 \in$? No.
                -   Total 2.
                -   My counts:
                    -   $x=1$ includes (0,3)? Yes.
                    -   $x=3$ includes (0,3)? Yes.
                    -   $x=4$ includes (0,3)? Yes.
                    -   Intersection ($3,4$) includes (0,3)? $L=0 \le 1, R=3 \ge 3$. Yes.
                    -   Net for 4: $1 - 1 = 0$.
                    -   Total: $1+1+0 = 2$. Correct.
            -   Where is the extra 1 coming from?
            -   Maybe $x=1$ count is wrong?
                -   $L \le 2, R \ge 0$.
                -   Pairs: (0,0), (0,1), (0,2), (0,3), (1,1), (1,2), (1,3), (2,2), (2,3).
                -   Values:
                    -   (0,0): {1}. $x=1$ yes.
                    -   (0,1): {1,3}. $x=1$ yes.
                    -   (0,2): {1,3,1}. $x=1$ yes.
                    -   (0,3): {1,3,1,4}. $x=1$ yes.
                    -   (1,1): {3}. $x=1$ NO. (Wait! $L=1, R=1$. Subarray is A[1..1] = 3. 1 is NOT present).
                    -   Ah! My condition $L \le last(x)$ and $R \ge first(x)$ is correct for existence.
                    -   For $x=1$, $first=0, last=2$.
                    -   Pair (1,1): $L=1, R=1$. $L \le 2$ (True), $R \ge 0$ (True).
                    -   But $A[1..1]$ is 3. 1 is NOT present.
                    -   Why? Because $first(x)$ is the index of the *first* occurrence. If $L > first(x)$, we might miss the first occurrence, but we might catch a later one.
                    -   Condition for existence: $L \le last(x)$ AND $R \ge first(x)$ is WRONG.
                    -   Correct condition: There exists an index $k$ such that $L \le k \le R$ and $A_k = x$.
                    -   This is equivalent to: $L \le last(x)$ AND $R \ge first(x)$?
                    -   No. Example: $A = [3, 1, 3]$. $x=1$. $first=1, last=1$.
                        -   $L=0, R=0$. $L \le 1, R \ge 1$? $0 \le 1$ (T), $0 \ge 1$ (F). Correct (1 not present).
                        -   $L=2, R=2$. $L \le 1$ (F). Correct.
                        -   $L=1, R=1$. $1 \le 1, 1 \ge 1$. Present.
                    -   Example: $A = [1, 3, 1]$. $x=1$. $first=0, last=2$.
                        -   $L=1, R=1$. $1 \le 2, 1 \ge 0$. Condition says Present.
                        -   Actual $A[1..1] = 3$. Not present.
                        -   So the condition $L \le last(x) \land R \ge first(x)$ is **INCORRECT**.
                    -   Correct condition: $L \le last(x)$ AND $R \ge first(x)$ is only valid if we consider the range of indices where $x$ appears.
                    -   Actually, $x$ is present in $A[L..R]$ iff $L \le \text{last\_occurrence\_in\_range}(x)$? No.
                    -   $x$ is present iff $\max(\{k \mid A_k=x, k < L\}) < \min(\{k \mid A_k=x, k > R\})$? No.
                    -   Simple logic: $x$ is present iff there is at least one $k \in [L, R]$ with $A_k=x$.
                    -   This is equivalent to: $L \le \text{last\_pos}(x)$ AND $R \ge \text{first\_pos}(x)$ is FALSE.
                    -   It is equivalent to: $L \le \text{last\_pos}(x)$ AND $R \ge \text{first\_pos}(x)$ is NOT sufficient.
                    -   Wait, if $L \le last(x)$ and $R \ge first(x)$, does it guarantee existence?
                        -   In $[1, 3, 1]$, $first=0, last=2$.
                        -   $L=1, R=1$. $1 \le 2$ and $1 \ge 0$.
                        -   But $A[1]=3$.
                        -   The condition $L \le last(x)$ means we start before or at the last occurrence.
                        -   The condition $R \ge first(x)$ means we end after or at the first occurrence.
                        -   This implies the interval $[L, R]$ covers the interval $[first(x), last(x)]$? No.
                        -   It implies $[first(x), last(x)] \subseteq [L, R]$? No.
                        -   It implies $L \le last(x)$ and $R \ge first(x)$.
                        -   If $first(x) \le last(x)$, then $[first(x), last(x)]$ is a valid range.
                        -   If $L \le last(x)$ and $R \ge first(x)$, does $[L, R]$ intersect $[first(x), last(x)]$?
                            -   Intersection is $[\max(L, first), \min(R, last)]$.
                            -   We need $\max(L, first) \le \min(R, last)$.
                            -   We know $L \le last$ and $R \ge first$.
                            -   Is $\max(L, first) \le \min(R, last)$?
                            -   $L \le last$ (given). $first \le R$ (given).
                            -   We need $L \le R$ (given) and $first \le last$ (true).
                            -   Also need $L \le last$ (true) and $first \le R$ (true).
                            -   Wait, we need $L \le \min(R, last)$ and $first \le \min(R, last)$.
                            -   $L \le R$ and $L \le last$.
                            -   $first \le R$ and $first \le last$.
                            -   So yes, if $L \le R$, $L \le last$, $first \le R$, then intersection is non-empty.
                            -   Why did $[1, 3, 1]$ fail?
                                -   $first=0, last=2$.
                                -   $L=1, R=1$.
                                -   $L \le 2$ (True). $R \ge 0$ (True). $L \le R$ (True).
                                -   Intersection of $[1, 1]$ and $[0, 2]$ is $[1, 1]$. Non-empty.
                                -   But $A[1] = 3 \neq 1$.
                                -   Ah! $first(x)$ and $last(x)$ are indices of value $x$.
                                -   In $[1, 3, 1]$, $A_0=1, A_1=3, A_2=1$.
                                -   $first(1)=0, last(1)=2$.
                                -   Indices where $A_k=1$ are $\{0, 2\}$.
                                -   The interval $[first, last]$ is $[0, 2]$.
                                -   If $[L, R]$ intersects $[0, 2]$, does it contain a 1?
                                -   Intersection $[1, 1]$. $A_1=3$. No 1.
                                -   So the condition "intersects $[first, last]$" is NOT sufficient.
                                -   We need $[L, R]$ to contain at least one index from the set of positions of $x$.
                                -   This is equivalent to: $L \le \text{last\_pos\_before\_or\_at\_R}(x)$?
                                -   Actually, simpler: $x$ is present in $A[L..R]$ iff $L \le \text{last\_occurrence\_in\_prefix}(R)$.
                                -   Let $last\_pos[x][i]$ be the largest index $\le i$ where $A_k=x$.
                                -   Then $x \in A[L..R] \iff L \le last\_pos[x][R]$.
                                -   This requires precomputing for each $x$ and each $R$.
                                -   Alternatively, for a fixed $x$, the valid $(L, R)$ pairs are those where $L \le k$ for some $k \in \text{Pos}(x)$ and $R \ge k$.
                                -   This is equivalent to: $L \le \max(\{k \in \text{Pos}(x) \mid k \le R\})$.
                                -   Let $P_x$ be the sorted list of positions of $x$.
                                -   For a fixed $R$, let $k$ be the largest element in $P_x$ such that $k \le R$. If no such $k$, then $x$ not present.
                                -   Then $L$ can be any value in $[0, k]$.
                                -   So for a fixed $R$, count is $k+1$ (if $k$ exists).
                                -   Total count = $\sum_{R=0}^{N-1} (\text{largest pos } \le R + 1)$.
                                -   This can be computed in $O(N)$ by iterating $R$ and maintaining the current last seen position for each $x$.
            -   Okay, I need to rewrite the counting logic.
            -   Algorithm:
                1.  Compute `first_occ` and `last_occ` (global).
                2.  For each $x$, we need to count pairs $(L, R)$ where $x$ is present.
                    -   Iterate $R$ from $0$ to $N-1$.
                    -   Maintain `last_seen[x]` for each $x$.
                    -   If $A[R] == x$, update `last_seen[x] = R`.
                    -   If `last_seen[x]` is set, add `last_seen[x] + 1` to `cnt_x`.
                    -   Wait, this counts pairs where $x$ is present.
                    -   But we need to subtract pairs where $x-1$ is also present.
                    -   We can do this in one pass?
                    -   For each $R$, we can determine the contribution of each $x$ to the answer for subarrays ending at $R$.
                    -   For a fixed $R$, and for each $x$ present in $A[0..R]$, let $k = \text{last\_seen}[x]$.
                    -   The valid $L$'s are $0 \dots k$.
                    -   For each such $L$, we add 1 if $x-1$ is NOT present in $A[L..R]$.
                    -   $x-1$ is NOT present in $A[L..R]$ iff $L > \text{last\_seen}[x-1]$ (where last\_seen is relative to $R$).
                    -   Let $k_{x-1} = \text{last\_seen}[x-1]$ at step $R$. If $x-1$ not seen yet, $k_{x-1} = -1$.
                    -   We need $L \in [0, k_x]$ such that $L > k_{x-1}$.
                    -   So $L \in [\max(0, k_{x-1} + 1), k_x]$.
                    -   Number of such $L$'s is $\max(0, k_x - \max(0, k_{x-1} + 1) + 1)$.
                    -   We sum this over all $x$ present at $R$.
                    -   This is $O(N \cdot \text{distinct values})$ which is $O(N^2)$ worst case.
                    -   We need a faster way.
                    -   Notice that for a fixed $R$, we sum over $x$.
                    -   Total = $\sum_{R} \sum_{x \in \text{Unique}(0..R)} \max(0, \text{last\_pos}(x, R) - \max(0, \text{last\_pos}(x-1, R) + 1) + 1)$.
                    -   This still looks like iterating all $x$.
                    -   However, we only care about $x$ that are present.
                    -   Can we optimize?
                    -   Actually, the previous $O(N)$ approach was based on the formula:
                        $\sum_{x} (\text{Count}(x \in \text{Unique}) - \text{Count}(x \in \text{Unique} \land x-1 \in \text{Unique}))$.
                    -   The error was in `Count(x in Unique)`.
                    -   Correct `Count(x in Unique)`:
                        -   Iterate $R$ from $0$ to $N-1$.
                        -   Update `last_pos[x]` if $A[R] == x$.
                        -   Add `last_pos[x] + 1` to total.
                    -   Correct `Count(x and x-1 in Unique)`:
                        -   Iterate $R$.
                        -   Update `last_pos[x]` and `last_pos[x-1]`.
                        -   We need pairs $(L, R)$ where $L \le \text{last\_pos}(x)$ and $L > \text{last\_pos}(x-1)$.
                        -   Wait, condition for $x-1$ present in $A[L..R]$ is $L \le \text{last\_pos}(x-1)$.
                        -   So we need $L \le \text{last\_pos}(x)$ AND $L \le \text{last\_pos}(x-1)$.
                        -   So $L \le \min(\text{last\_pos}(x), \text{last\_pos}(x-1))$.
                        -   Count is $\min(\text{last\_pos}(x), \text{last\_pos}(x-1)) + 1$.
                        -   So for each $R$, contribution of $x$ is:
                            $(\text{last\_pos}(x) + 1) - (\min(\text{last\_pos}(x), \text{last\_pos}(x-1)) + 1)$.
                            $= \text{last\_pos}(x) - \min(\text{last\_pos}(x), \text{last\_pos}(x-1))$.
                            $= \max(0, \text{last\_pos}(x) - \text{last\_pos}(x-1))$.
                        -   Sum this over all $R$ and all $x$.
                        -   This is $O(N \cdot \text{distinct})$. Still potentially $O(N^2)$.
                        -   But we can maintain the sum.
                        -   We need $\sum_{x} \max(0, \text{last\_pos}(x) - \text{last\_pos}(x-1))$.
                        -   This is hard to maintain incrementally for all $x$.
                        -   Wait, the constraints are $N \le 3 \times 10^5$. $O(N^2)$ is TLE.
                        -   Is there a property?
                        -   Maybe the number of distinct values is small? No.
                        -   Let's re-read the problem. Maybe my interpretation of $f(L,R)$ is wrong?
                        -   "Choose integers $l, r$ such that every integer from $l$ through $r$ appears at least once... erase all integers from $l$ through $r$".
                        -   This is exactly covering the set of unique values with minimum number of contiguous intervals.
                        -   My formula $f(L,R) = \sum_{x \in Unique} [x-1 \notin Unique]$ is correct.
                        -   The counting logic must be optimized.
                        -   Let's go back to the $O(N)$ approach with the corrected counting.
                        -   We need $\sum_{L,R} \sum_{x} [x \in U(L,R) \land x-1 \notin U(L,R)]$.
                        -   $= \sum_{x} \sum_{L,R} [x \in U(L,R) \land x-1 \notin U(L,R)]$.
                        -   For a fixed $x$, we need to count pairs $(L,R)$ such that:
                            1. $x$ is present in $A[L..R]$.
                            2. $x-1$ is NOT present in $A[L..R]$.
                        -   Condition 1: $\exists k \in [L, R], A_k = x$.
                        -   Condition 2: $\forall k \in [L, R], A_k \neq x-1$.
                        -   Let $P_x$ be the set of indices where $A_k = x$.
                        -   Let $P_{x-1}$ be the set of indices where $A_k = x-1$.
                        -   We need $[L, R] \cap P_x \neq \emptyset$ and $[L, R] \cap P_{x-1} = \emptyset$.
                        -   $[L, R] \cap P_{x-1} = \emptyset \iff L > \max(P_{x-1} \cap [0, R-1])$? No.
                        -   It means no index in $P_{x-1}$ is in $[L, R]$.
                        -   This implies $R < \min(P_{x-1} \cap [L, \infty))$ OR $L > \max(P_{x-1} \cap (-\infty, R])$.
                        -   Actually, simpler: The interval $[L, R]$ must be contained in a gap between occurrences of $x-1$.
                        -   Let $g_0, g_1, \dots, g_m$ be the gaps between occurrences of $x-1$.
                            -   $g_0 = [0, \text{first}(x-1)-1]$.
                            -   $g_i = (\text{occ}_i, \text{occ}_{i+1}-1]$.
                            -   $g_m = (\text{last}(x-1), N-1]$.
                        -   For $[L, R]$ to avoid $x-1$, it must be fully inside one of these gaps.
                        -   Also, it must contain at least one $x$.
                        -   So for each gap $[a, b]$ (where $a \le b$), we count pairs $(L, R)$ with $a \le L \le R \le b$ such that $[L, R] \cap P_x \neq \emptyset$.
                        -   Total count for $x$ = $\sum_{\text{gaps } [a,b]} (\text{pairs in } [a,b] \text{ containing } x)$.
                        -   Pairs in $[a,b]$ containing $x$:
                            -   Total pairs in $[a,b]$ is $(b-a+1)(b-a+2)/2$.
                            -   Pairs NOT containing $x$: Sum of lengths of gaps between occurrences of $x$ within $[a,b]$.
                            -   Alternatively: $\sum_{R=a}^b (\text{last\_pos}(x, R) - a + 1)$ where last\_pos is relative to $a$.
                            -   Let's use the global positions.
                            -   For a gap $[a, b]$, we need $L \in [a, b], R \in [L, b]$ and $\exists k \in [L, R] \cap P_x$.
                            -   This is equivalent to: $L \le \max(P_x \cap [a, b])$? No.
                            -   It is: $L \le \text{last\_pos}(x, R)$ where last\_pos is restricted to $[a, b]$.
                            -   Let's iterate over the gaps of $x-1$.
                            -   For each gap $[a, b]$, we need to count pairs $(L, R) \subseteq [a, b]$ that contain $x$.
                            -   This is a standard problem: count subsegments of $[a, b]$ containing at least one $x$.
                            -   Let the occurrences of $x$ in $[a, b]$ be $p_1, p_2, \dots, p_k$.
                            -   Also consider virtual $p_0 = a-1$ and $p_{k+1} = b+1$.
                            -   Pairs NOT containing $x$ are those strictly between $p_i$ and $p_{i+1}$.
                            -   Count = Total pairs in $[a, b]$ - $\sum_{i=0}^k \text{pairs in } (p_i, p_{i+1})$.
                            -   Pairs in $(u, v)$ (exclusive) is $(v-u-1)(v-u)/2$.
                            -   This approach is $O(N)$ because the sum of gaps is $O(N)$ and occurrences are $O(N)$.
                            -   We can iterate over all $x$, find gaps of $x-1$, and sum up.
                            -   Total complexity: $\sum_x (\text{occurrences of } x-1 + \text{occurrences of } x) = O(N)$.
                            -   This is the correct $O(N)$ solution.

## worker: Implement the gap-based counting logic to correctl
The problem asks for the sum of $f(L,R)$ over all subarrays. $f(L,R)$ is the number of connected components of unique values in $A[L..R]$ under the relation $u \sim v \iff |u-v|=1$. This is equivalent to counting the number of unique values $x$ in $A[L..R]$ such that $x-1$ is NOT in $A[L..R]$.
We need to compute $\sum_{L,R} \sum_{x \in \text{Unique}(L,R)} [x-1 \notin \text{Unique}(L,R)]$.
By swapping sums, this is $\sum_{x} \sum_{L,R} [x \in \text{Unique}(L,R) \land x-1 \notin \text{Unique}(L,R)]$.
For a fixed $x$, the condition $x-1 \notin \text{Unique}(L,R)$ means the subarray $A[L..R]$ must not contain any occurrence of $x-1$. This implies $[L, R]$ must be fully contained within a "gap" of $x-1$ (a contiguous range of indices with no $x-1$).
For each such gap $[a, b]$, we count the number of subsegments $[L, R] \subseteq [a, b]$ that contain at least one occurrence of $x$.
The algorithm iterates over each value $x$ present in the array. For each $x$, it identifies the gaps of $x-1$. For each gap, it calculates the number of valid subsegments containing $x$ by subtracting the "bad" subsegments (those containing no $x$) from the total subsegments in the gap.
The complexity is $O(N)$ because the sum of the lengths of all gaps for all values is $O(N)$, and we process each occurrence of each value a constant number of times.

## worker: finalize
The problem asks for the sum of $f(L,R)$ over all $1 \le L \le R \le N$.
1.  **Analysis of $f(L,R)$**: The operation allows removing a contiguous range of values $[l, r]$ if all integers in that range are currently present. This implies that one operation can remove a set of values that forms a contiguous block of integers. To minimize operations, we should greedily remove the largest possible contiguous blocks. Thus, $f(L,R)$ is equal to the number of connected components of the set of unique values in $A[L..R]$ under the relation $u \sim v \iff |u-v|=1$.
2.  **Combinatorial Reformulation**: $f(L,R) = \sum_{x \in \text{Unique}(L,R)} [x-1 \notin \text{Unique}(L,R)]$.
    We need to compute $\sum_{L,R} \sum_{x} [x \in \text{Unique}(L,R) \land x-1 \notin \text{Unique}(L,R)]$.
    By swapping sums, this is $\sum_{x} \sum_{L,R} [x \in \text{Unique}(L,R) \land x-1 \notin \text{Unique}(L,R)]$.
3.  **Counting Logic**:
    -   For a fixed $x$, we need to count pairs $(L,R)$ such that $x$ is present in $A[L..R]$ and $x-1$ is NOT present in $A[L..R]$.
    -   The condition "$x-1$ is NOT present in $A[L..R]$" means the subarray $A[L..R]$ must not contain any occurrence of $x-1$. This implies $[L, R]$ must be fully contained within a "gap" of $x-1$ (a contiguous range of indices with no $x-1$).
    -   For each such gap $[a, b]$, we count the number of subsegments $[L, R] \subseteq [a, b]$ that contain at least one occurrence of $x$.
    -   The number of such subsegments is calculated as: (Total subsegments in $[a, b]$) - (Subsegments in $[a, b]$ that contain NO $x$).
    -   Subsegments containing no $x$ are those strictly between consecutive occurrences of $x$ within $[a, b]$.
4.  **Complexity**:
    -   We iterate over each value $x$ present in the array.
    -   For each $x$, we iterate over the gaps of $x-1$.
    -   The sum of the lengths of all gaps for all values is $O(N)$ because each index belongs to exactly one gap for a specific value.
    -   The occurrences of $x$ are processed linearly.
    -   Total time complexity is $O(N)$. Space complexity is $O(N)$.
