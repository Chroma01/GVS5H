
## ideation
**Core Difficulty**: The problem requires maximizing the number of pairs $(a, b)$ from a sorted array such that $a \leq b/2$. This is a classic greedy matching problem. The key challenge is determining the optimal strategy to pair elements to maximize the count. Since the array is sorted, we need to decide whether to pair the smallest available element as a "top" with the smallest valid "bottom," or if there's a different strategy that yields more pairs.

**Candidate Approaches**:
1.  **Greedy with Two Pointers**:
    *   Sort the array (already sorted per constraints).
    *   Use two pointers: `left` (for potential tops) and `right` (for potential bottoms).
    *   Iterate `left` from the start. For each `A[left]`, try to find the smallest `A[right]` (where `right > left`) such that `A[left] * 2 <= A[right]`.
    *   If found, increment the count, move both pointers.
    *   If not found (i.e., even the largest remaining element is too small), we cannot pair `A[left]`. However, since the array is sorted, if `A[left]` cannot be paired with any `A[right]`, it certainly can't be paired with any subsequent `A`. But wait, we might be able to skip `A[left]` to save it? No, `A[left]` is the smallest. If the smallest top can't find a bottom, no other top can find a bottom *with that specific bottom*. But we need to be careful: maybe `A[left]` is too small to be a *bottom* for anyone? Actually, the condition is $top \leq bottom/2$. Small numbers are better tops. Large numbers are better bottoms.
    *   Refined Greedy Strategy:
        *   We want to form as many pairs as possible.
        *   Consider the smallest available element. Can it be a top? Yes, if there exists a larger element $\geq 2 \times$ itself. To maximize future possibilities, we should pair it with the *smallest* valid bottom. Why? Because using a larger bottom than necessary "wastes" a large value that could potentially serve as a bottom for a larger top value later.
        *   Algorithm:
            1. Initialize `left = 0`, `right = 1`, `count = 0`.
            2. While `right < N`:
               - Check if `A[left] * 2 <= A[right]`.
               - If yes: We found a valid pair. Increment `count`, `left++`, `right++`.
               - If no: `A[right]` is too small to support `A[left]`. Since `A` is sorted, `A[right]` cannot support any `A[k]` where $k > left$. So `A[right]` is useless as a bottom for the current `left` or any subsequent top. We must advance `right` to find a larger bottom. `right++`.
            3. Wait, is this correct? What if `A[left]` is so large it can't be a top for *any* remaining element? The loop condition `right < N` handles the bottom search. If we run out of `right` before finding a match for `left`, that `left` is discarded.
            4. Let's trace Sample 1: `2 3 4 4 7 10`
               - `l=0 (2)`, `r=1 (3)`. $2*2=4 > 3$. No. `r=2 (4)`. $4 \le 4$. Match! `count=1`, `l=1 (3)`, `r=3 (4)`.
               - `l=1 (3)`, `r=3 (4)`. $6 > 4$. No. `r=4 (7)`. $6 \le 7$. Match! `count=2`, `l=2 (4)`, `r=5 (10)`.
               - `l=2 (4)`, `r=5 (10)`. $8 \le 10$. Match! `count=3`, `l=3 (4)`, `r=6`. End.
               - Result 3. Correct.
            5. Trace Sample 2: `387 388 389`
               - `l=0 (387)`, `r=1 (388)`. $774 > 388$. `r=2 (389)`. $774 > 389$. `r=3`. End. Count 0. Correct.

2.  **Binary Search Approach**:
    *   For each element considered as a top, binary search for the first element that satisfies the condition.
    *   Time complexity $O(N \log N)$. Given $N=5 \times 10^5$, this is acceptable but slower than $O(N)$.
    *   The greedy logic remains the same: match smallest top with smallest valid bottom.

3.  **Pitfalls**:
    *   **Off-by-one errors**: Indices for `left` and `right`.
    *   **Logic flaw**: Is it ever better to skip a valid pair?
        *   Suppose we have tops $t_1, t_2$ and bottoms $b_1, b_2$ with $t_1 < t_2$ and $b_1 < b_2$.
        *   If $t_1$ can pair with $b_1$, should we?
        *   If we pair $(t_1, b_1)$, remaining: $t_2, b_2$.
        *   If we skip $(t_1, b_1)$ and try $(t_1, b_2)$, remaining: $t_2, b_1$. Since $t_2 > t_1$, $t_2$ is harder to pair than $t_1$. $b_1$ is easier to use than $b_2$. So saving $b_1$ for $t_2$ is bad because $t_2$ needs a larger bottom. Thus, using the smallest valid bottom for the smallest top is optimal.
        *   What if $t_1$ pairs with $b_2$ but $t_2$ pairs with $b_1$? Impossible because $t_2 > t_1$ implies if $t_2 \le b_1/2$, then $t_1 \le b_1/2$ as well. So if $(t_2, b_1)$ works, $(t_1, b_1)$ also works. And since $b_1 < b_2$, using $b_1$ for $t_1$ leaves $b_2$ for $t_2$, which is strictly better or equal for $t_2$.
        *   Conclusion: Greedy works.

**Implementation Details**:
- Read N.
- Read list A.
- Implement the two-pointer loop.
- Print count.
- Constraints: $N$ up to $5 \times 10^5$, $A_i$ up to $10^9$. Python handles large integers automatically. Time limit usually 2s, $O(N)$ is perfect.

## worker: Write the Python code implementing the two-pointer
The problem asks for the maximum number of pairs $(A_i, A_j)$ such that $A_i \leq A_j / 2$ (where $A_i$ is on top of $A_j$). Since the input array is sorted in ascending order, a greedy strategy is optimal.

**Strategy:**
1.  Use two pointers: `left` for the candidate "top" mochi and `right` for the candidate "bottom" mochi.
2.  Initialize `left = 0` and `right = 1`.
3.  Iterate while `right < N`:
    *   Check if `A[right] >= 2 * A[left]`.
    *   If true, we form a pair. Increment the count `K`, move `left` forward (to try the next smallest top), and move `right` forward (since this bottom is used).
    *   If false, `A[right]` is too small to support `A[left]`. Since the array is sorted, `A[right]` cannot support any `A[k]` where $k > left$ (because those tops are even larger). Thus, `A[right]` is useless as a bottom for the current or future tops. We increment `right` to find a larger bottom.
4.  This approach ensures we use the smallest valid bottom for the smallest available top, preserving larger bottoms for potentially larger tops later, maximizing the total pairs.

**Complexity:**
*   Time Complexity: $O(N)$ because both pointers traverse the array at most once.
*   Space Complexity: $O(N)$ to store the input array (or $O(1)$ if reading stream-wise, but Python's `read().split()` loads all into memory which is fine for $N=5 \times 10^5$).
