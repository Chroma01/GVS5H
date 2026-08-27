
## ideation
**Core Difficulty:**
The problem requires finding the $K$-th largest value among $N^3$ combinations of the form $A_iB_j + B_jC_k + C_kA_i$. With $N$ up to $2 \times 10^5$, an $O(N^3)$ or even $O(N^2)$ solution is impossible. The constraint $K \le 5 \times 10^5$ suggests that we only need to identify the top $K$ values, but since the values are not sorted, we likely need a method to count how many values are $\ge X$ efficiently.

**Candidate Approaches:**
1.  **Binary Search on Answer:**
    *   **Range:** The minimum possible value is $1$ (or min product) and the maximum is roughly $3 \times 10^{18}$ (since $A, B, C \le 10^9$).
    *   **Check Function (`count_ge(X)`):** For a fixed $X$, count pairs $(i, j, k)$ such that $A_iB_j + B_jC_k + C_kA_i \ge X$.
    *   **Optimization:** Rewrite the inequality: $B_j(A_i + C_k) + C_kA_i \ge X$.
        *   Iterate over $j$ (from $1$ to $N$). Let $B = B_j$.
        *   The condition becomes $B(A_i + C_k) + C_kA_i \ge X$.
        *   This looks like a 2D range query or a geometric problem. For a fixed $j$, we need to count pairs $(i, k)$ satisfying the condition.
        *   If we sort arrays $A$ and $C$, can we use two pointers?
            *   Rearranging: $B \cdot A_i + B \cdot C_k + A_i C_k \ge X$.
            *   This is symmetric in $A_i$ and $C_k$ if we consider the structure, but the coefficients depend on $B$.
            *   Actually, notice that $A_i B_j + B_j C_k + C_k A_i = B_j(A_i + C_k) + A_i C_k$.
            *   Let $x = A_i$ and $y = C_k$. We need $B_j(x+y) + xy \ge X$.
            *   For a fixed $j$ and fixed $x$, we need $y(B_j + x) \ge X - B_j x \implies y \ge \frac{X - B_j x}{B_j + x}$.
            *   Since $A$ and $C$ can be sorted, for each $x \in A$, we can find the smallest $y \in C$ satisfying the condition using binary search (specifically `bisect_left`).
            *   Complexity of check: $O(N \log N)$ (iterating $j$, then iterating $i$, then binary search on $C$). Total check: $O(N^2 \log N)$? No, wait.
            *   We iterate $j$ ($N$ times). Inside, we iterate $i$ ($N$ times). Inside that, binary search on $C$ ($\log N$). Total $O(N^2 \log N)$. This is too slow ($4 \times 10^{10}$ ops).
    *   **Refinement on Check:**
        *   Can we avoid iterating all $i$ for every $j$?
        *   Notice the expression is symmetric with respect to swapping roles of $A$ and $C$ if we fix $B$. But $A$ and $C$ are distinct arrays.
        *   However, observe that $A_i B_j + B_j C_k + C_k A_i = B_j(A_i + C_k) + A_i C_k$.
        *   Let's fix $j$. We have a set of values $A$ and a set of values $C$. We want to count pairs $(a, c)$ such that $B_j(a+c) + ac \ge X$.
        *   This function $f(a, c) = B_j(a+c) + ac$ is increasing in both $a$ and $c$ (since $A_i, B_i, C_i \ge 1$).
        *   If we sort $A$ and $C$ in ascending order.
        *   For a fixed $a$, as $c$ increases, the LHS increases. So for each $a$, there is a threshold $c_{min}$ such that all $c \ge c_{min}$ work.
        *   We can find $c_{min}$ for each $a$ using binary search.
        *   Summing up counts: $\sum_{a \in A} (\text{count of } c \in C \text{ s.t. } c \ge c_{min}(a))$.
        *   This is still $O(N \log N)$ per $j$, leading to $O(N^2 \log N)$ total for the check. Still too slow.
        *   **Wait, do we need to iterate $j$?**
        *   The expression is $A_i B_j + B_j C_k + C_k A_i$.
        *   Let's try to fix the pair $(i, k)$ and find valid $j$?
            *   $B_j(A_i + C_k) + A_i C_k \ge X$.
            *   Let $S = A_i + C_k$ and $P = A_i C_k$. Condition: $B_j \cdot S + P \ge X \implies B_j \ge \frac{X - P}{S}$.
            *   For fixed $(i, k)$, we need to count $j$ such that $B_j \ge \text{threshold}$.
            *   If we sort $B$, we can use binary search to find the count of valid $j$'s in $O(\log N)$.
            *   Total complexity: Iterate all pairs $(i, k)$ ($N^2$) $\times \log N$. Still $O(N^2 \log N)$. Too slow.

    *   **Re-evaluating the constraints and $K$:**
        *   $K$ is small ($5 \times 10^5$).
        *   Maybe we don't need the exact count for *all* $X$, but we can use the small $K$ property?
        *   Usually, small $K$ in such problems implies we only care about the largest values. The largest values come from the largest elements of $A, B, C$.
        *   However, the function is not monotonic in a simple way that allows truncating arrays easily without proof (e.g., a small $B$ with huge $A, C$ might beat a huge $B$ with small $A, C$? No, because $A,B,C \ge 1$, larger inputs generally yield larger outputs).
        *   Actually, since $A_i, B_j, C_k \ge 1$, the function $f(i,j,k)$ is monotonic with respect to each index if the arrays are sorted. $A_i$ increases $\implies f$ increases.
        *   Therefore, the largest values must come from indices $(i, j, k)$ where $i, j, k$ are large (if sorted descending).
        *   Specifically, if we sort $A, B, C$ in descending order, the top $K$ values are likely formed by indices within the top $M$ elements, where $M$ is small.
        *   How large is $M$? If we take the top $M$ elements from each, we get $M^3$ combinations. We need $M^3 \ge K$.
        *   Since $K \le 5 \times 10^5$, $M \approx \sqrt[3]{500000} \approx 80$.
        *   So, if we sort $A, B, C$ in descending order and only consider the first $M \approx 100$ elements, we might cover all the top $K$ values?
        *   **Hypothesis:** The $K$-th largest value is formed by indices $(i, j, k)$ where $i, j, k$ are among the indices of the largest $M$ elements in their respective arrays, with $M$ such that $M^3 \ge K$.
        *   Let's verify. Suppose the optimal triplet uses an index $i$ that is NOT in the top $M$ of $A$. Then $A_i$ is smaller than the $M$-th largest element. If we replace $i$ with a larger index $i'$ (from the top $M$), the value $A_{i'}B_j + B_jC_k + C_kA_{i'}$ will be strictly greater (since $B, C \ge 1$). Thus, the new value would be larger than the original.
        *   This implies that to maximize the sum, we should always pick the largest available $A_i$, $B_j$, and $C_k$.
        *   Therefore, the set of candidates for the top $K$ values is a subset of the combinations formed by the top $M$ elements of $A$, $B$, and $C$, where $M$ is the smallest integer such that $M^3 \ge K$.
        *   Given $K \le 5 \times 10^5$, $M = \lceil K^{1/3} \rceil \le 80$.
        *   Algorithm:
            1. Sort $A, B, C$ in descending order.
            2. Take the first $M = \lceil K^{1/3} \rceil$ elements from each. (Ensure $M \le N$).
            3. Generate all $M^3$ values.
            4. Sort these $M^3$ values and pick the $K$-th largest.
        *   Complexity: Sorting takes $O(N \log N)$. Generating takes $O(M^3)$. Sorting results takes $O(M^3 \log M^3)$.
        *   With $M \approx 80$, $M^3 \approx 512,000$. This fits perfectly within the time limit and memory.
        *   Edge case: If $N < M$, we just take all $N$. But since $K \le N^3$, $M$ will naturally be $\le N$.
        *   Wait, is it possible that a combination involving a smaller element yields a value equal to one with a larger element? Yes, if values are equal. But we are looking for the $K$-th *largest*. If there are ties, the logic still holds: if we have a candidate set that includes all combinations of the top $M$ elements, and $M^3 \ge K$, then the $K$-th largest value in the full set must be $\le$ the $K$-th largest value in this subset?
        *   Actually, the logic is: The set of values generated by the top $M$ elements of $A, B, C$ contains the $K$ largest values of the entire set.
        *   Proof sketch: Let $S$ be the set of all $N^3$ values. Let $S_M$ be the set of values using only top $M$ indices. $|S_M| = M^3 \ge K$.
        *   Suppose the $K$-th largest value in $S$ is $V$. Suppose there exists a value $v \in S \setminus S_M$ such that $v > V$.
        *   Any $v \in S \setminus S_M$ uses at least one index from outside the top $M$ in some array. Let's say index $i$ in $A$ is not in top $M$. Then $A_i < A_{i'}$ for some $i' \in \text{top } M$.
        *   Consider the triplet $(i', j, k)$ corresponding to $v$ (using same $j, k$). Then $val(i', j, k) > val(i, j, k) = v > V$.
        *   Since $val(i', j, k)$ is in $S_M$ (as $i' \in \text{top } M$), $S_M$ contains a value strictly greater than $V$.
        *   If $S_M$ contains a value $> V$, and $|S_M| \ge K$, does it imply the $K$-th largest of $S_M$ is $\ge V$?
        *   Yes. If $S_M$ has at least $K$ values, and at least one is $> V$, then the $K$-th largest could be $> V$ or $= V$?
        *   Wait, if $S_M$ has many values $> V$, then the $K$-th largest of $S_M$ is definitely $\ge V$.
        *   But we need the $K$-th largest of $S$. If $S_M$ "covers" the top values, then the $K$-th largest of $S$ is exactly the $K$-th largest of $S_M$.
        *   Why? Because any value in $S \setminus S_M$ is "dominated" by some value in $S_M$. Specifically, for any $x \in S \setminus S_M$, there exists $y \in S_M$ such that $y \ge x$.
        *   This means the multiset $S_M$ majorizes $S$ in terms of the top elements.
        *   Therefore, the $K$-th largest element of $S$ is the same as the $K$-th largest element of $S_M$.
        *   This approach is $O(N \log N + K \log K)$, which is extremely efficient.

**Pitfalls:**
1.  **Integer Overflow:** The values can be up to $10^9 \times 10^9 + \dots \approx 3 \times 10^{18}$. This fits in a 64-bit signed integer (max $\approx 9 \times 10^{18}$). Python handles large integers automatically, so no overflow issues.
2.  **Sorting Order:** Must sort descending to pick the "top" elements.
3.  **Value of M:** Calculate $M = \lceil K^{1/3} \rceil$. Be careful with floating point precision. Since $K \le 5 \times 10^5$, $K^{1/3} \approx 79.37$. So $M=80$ is safe. Even $M=100$ is safe and fast enough.
4.  **Constraints:** $N$ can be small ($N < M$). In that case, just take $N$. The loop should go up to $\min(N, M)$. But since $K \le N^3$, if $N < M$, then $N^3 < M^3$, but we are constrained by $K \le N^3$, so we will just generate $N^3$ values which is $\ge K$. The logic holds: take all $N$ elements.

**Conclusion:**
The "top $M$" strategy is correct and optimal given the constraints.

## worker: Read input $N, K$ and arrays $A, B, C$. Sort them 
The problem asks for the $K$-th largest value among $N^3$ combinations of the form $A_iB_j + B_jC_k + C_kA_i$. Given $N \le 2 \times 10^5$, an $O(N^3)$ or even $O(N^2)$ solution is infeasible. However, $K$ is relatively small ($K \le 5 \times 10^5$).

The key insight is that the function $f(i, j, k) = A_iB_j + B_jC_k + C_kA_i$ is monotonically increasing with respect to each component $A_i, B_j, C_k$ (since all values are positive integers). Therefore, the largest values in the set of all combinations must be formed by the largest elements of arrays $A$, $B$, and $C$.

Specifically, if we sort $A$, $B$, and $C$ in descending order, the top $K$ values of the entire set must be contained within the set of combinations formed by the top $M$ elements of each array, where $M$ is the smallest integer such that $M^3 \ge K$. This is because any combination involving an element outside the top $M$ of any array can be "dominated" (replaced by a larger value) by swapping that index with one of the top $M$ indices, resulting in a strictly larger sum. Thus, the $K$-th largest value of the full set is identical to the $K$-th largest value of the subset formed by the top $M$ elements.

Algorithm steps:
1. Read inputs.
2. Sort $A$, $B$, $C$ in descending order.
3. Calculate $M = \lceil K^{1/3} \rceil$.
4. Take the first $M$ elements from each sorted array (capped at $N$).
5. Generate all $M^3$ combinations of the form $A_iB_j + B_jC_k + C_kA_i$.
6. Sort these generated values in descending order.
7. Output the value at index $K-1$.

Complexity:
- Sorting: $O(N \log N)$.
- Generating values: $O(M^3)$. Since $M \approx K^{1/3}$, $M^3 \approx K$. With $K \le 5 \times 10^5$, this is roughly $5 \times 10^5$ operations.
- Sorting values: $O(K \log K)$.
- Total time complexity: $O(N \log N + K \log K)$, which easily fits within the time limit.
- Space complexity: $O(K)$ to store the generated values.

## worker: Run the code against the provided sample inputs to
The solution implements the "top M" strategy. Since the function $f(i, j, k) = A_iB_j + B_jC_k + C_kA_i$ is monotonically increasing with respect to each component (given positive integers), the largest values in the set of all $N^3$ combinations must be formed by the largest elements of arrays $A$, $B$, and $C$. Specifically, the top $K$ values are guaranteed to be within the combinations formed by the top $M$ elements of each array, where $M = \lceil K^{1/3} \rceil$. 

With $K \le 5 \times 10^5$, $M$ is at most 80. This reduces the problem complexity from $O(N^3)$ to $O(N \log N + M^3 \log M^3)$, which is well within the time limits. The code sorts the arrays, selects the top $M$ elements, generates all $M^3$ combinations, sorts them, and prints the $K$-th largest.

## worker: Run the provided sample inputs to verify correctne
The solution implements the "top M" strategy. Since the function $f(i, j, k) = A_iB_j + B_jC_k + C_kA_i$ is monotonically increasing with respect to each component (given positive integers), the largest values in the set of all $N^3$ combinations must be formed by the largest elements of arrays $A$, $B$, and $C$. Specifically, the top $K$ values are guaranteed to be within the combinations formed by the top $M$ elements of each array, where $M = \lceil K^{1/3} \rceil$. 

With $K \le 5 \times 10^5$, $M$ is at most 80. This reduces the problem complexity from $O(N^3)$ to $O(N \log N + M^3 \log M^3)$, which is well within the time limits. The code sorts the arrays, selects the top $M$ elements, generates all $M^3$ combinations, sorts them, and prints the $K$-th largest.

## worker: finalize
The problem asks for the $K$-th largest value among $N^3$ combinations of the form $A_iB_j + B_jC_k + C_kA_i$. Since $N$ is up to $2 \times 10^5$, an $O(N^3)$ solution is impossible. However, $K$ is relatively small ($K \le 5 \times 10^5$).

The key insight is that the function $f(i, j, k) = A_iB_j + B_jC_k + C_kA_i$ is monotonically increasing with respect to each component $A_i, B_j, C_k$ because all input values are positive integers ($\ge 1$). This implies that larger indices in the sorted arrays (descending order) yield larger values.

Consequently, the set of the $K$ largest values in the entire $N^3$ space must be a subset of the combinations formed by the top $M$ elements of each array, where $M$ is the smallest integer such that $M^3 \ge K$. If we were to use an element outside the top $M$ of any array, we could replace it with a larger element from the top $M$ to get a strictly larger sum, meaning the original combination couldn't be among the top $K$ unless there are ties, in which case the top $M$ set still covers the necessary values.

Algorithm:
1. Read inputs.
2. Sort $A, B, C$ in descending order.
3. Calculate $M = \lceil K^{1/3} \rceil$.
4. Take the first $M$ elements from each sorted array.
5. Generate all $M^3$ combinations. Since $M^3 \approx K \le 5 \times 10^5$, this is computationally feasible.
6. Sort the generated values and pick the $K$-th largest.

Complexity:
- Sorting arrays: $O(N \log N)$.
- Generating values: $O(M^3) \approx O(K)$.
- Sorting values: $O(K \log K)$.
- Total time: $O(N \log N + K \log K)$, which fits well within the time limit.
