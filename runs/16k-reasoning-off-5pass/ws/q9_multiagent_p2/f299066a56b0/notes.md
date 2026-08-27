
## ideation
The problem asks to maximize the number of pairs $(a, b)$ from a sorted array $A$ such that $a \le b/2$ (or $2a \le b$). Each element can be used at most once.
Since the array is sorted ($A_1 \le A_2 \le \dots \le A_N$), a greedy strategy is optimal.
**Core Difficulty**: Determining the exact pairing strategy that maximizes the count.
**Candidate Approaches**:
1.  **Two Pointers (Greedy)**:
    -   Maintain two pointers, `left` (for the top mochi) and `right` (for the bottom mochi).
    -   Start with `left = 0`, `right = 1`.
    -   While `right < N`:
        -   If $A_{left} \le A_{right} / 2$: We can form a pair. Increment count, move both `left` and `right` forward (consume both).
        -   Else ($A_{left} > A_{right} / 2$): The current `right` is too small to support `left`. Since the array is sorted, no future `right` (which will be larger) might necessarily help `left` if we are trying to save larger numbers for even larger `left`s? Wait, actually, if $A_{right}$ is too small for $A_{left}$, it is definitely too small for any $A_{k}$ where $k > left$. So $A_{right}$ cannot be a bottom piece for $A_{left}$ or any subsequent top piece. Thus, we must discard $A_{right}$ (increment `right`) and keep `left` hoping to find a larger bottom piece.
    -   This logic seems sound: always try to satisfy the smallest available top with the smallest available valid bottom. If the smallest available bottom is invalid, it's useless for the current top (and any larger top), so discard it. If it is valid, use it because using a larger bottom than necessary is suboptimal (it might be needed for a larger top later).

2.  **Binary Search on Answer**:
    -   Check if it's possible to make $K$ pairs.
    -   To check feasibility for $K$: We need to select $K$ tops and $K$ bottoms. To maximize chances, we should pick the $K$ smallest elements as tops and the $K$ largest elements as bottoms? Not exactly, because the pairing must be valid.
    -   Actually, for a fixed $K$, the optimal strategy to check feasibility is: Pick the $K$ smallest elements as candidates for tops ($T_1, \dots, T_K$) and the $K$ largest as candidates for bottoms ($B_1, \dots, B_K$). Then try to match them. However, simply picking the smallest $K$ and largest $K$ doesn't guarantee a valid matching exists even if a larger set could be formed?
    -   Actually, the standard greedy check for "can we form $K$ pairs" usually involves trying to match the $i$-th smallest top with the $i$-th smallest valid bottom. But determining the set of tops and bottoms is tricky.
    -   Given $N \le 5 \times 10^5$, an $O(N)$ or $O(N \log N)$ solution is needed. The two-pointer approach is $O(N)$, which is better. Binary search would be $O(N \log N)$ or $O(N \log (\text{max\_ans}))$, which is acceptable but likely more complex to implement correctly for the specific constraint.

## worker: Write the Python code implementing the two-pointer
The problem requires finding the maximum number of pairs $(a, b)$ such that $a \le b/2$ from a sorted array of sizes.
The greedy strategy employed is:
1.  Maintain two pointers: `left` (index of the smallest available mochi to be the top) and `right` (index of the smallest available mochi to be the bottom).
2.  Initialize `left = 0` and `right = 1`.
3.  Iterate while `right < N`:
    *   If $2 \times A[\text{left}] \le A[\text{right}]$, we form a pair. We increment the count, and move both `left` and `right` forward to consider the next smallest available mochi for the top and bottom respectively. This is optimal because using the smallest valid bottom for the current top saves larger bottoms for potentially larger tops later.
    *   If the condition is not met ($2 \times A[\text{left}] > A[\text{right}]$), the current `right` mochi is too small to support `left`. Since the array is sorted, $A[\text{right}]$ is also too small to support any $A[k]$ where $k > \text{left}$. Thus, $A[\text{right}]$ is useless as a bottom piece for any remaining top piece. We discard it by incrementing `right` only.
4.  The loop terminates when `right` reaches the end of the array. The count `k` is the answer.
Time Complexity: $O(N)$ because each element is visited at most once by the pointers.
Space Complexity: $O(N)$ to store the input array.

## worker: [done] Write the Python code implementing the two-
The solution implements a greedy two-pointer strategy. Since the input array `A` is sorted in ascending order, we can efficiently determine the maximum number of pairs $(a, b)$ such that $a \le b/2$.
1.  **Initialization**: We set `left` to 0 (the smallest available mochi to be the top) and `right` to 1 (the smallest available mochi to be the bottom).
2.  **Iteration**:
    *   If $2 \times A[\text{left}] \le A[\text{right}]$, we form a pair. This is optimal because we use the smallest valid bottom element for the current top, saving larger elements for potentially larger tops later. We increment both pointers and the count `k`.
    *   If the condition is not met, $A[\text{right}]$ is too small to support $A[\text{left}]$. Since the array is sorted, $A[\text{right}]$ is also too small to support any $A[k]$ where $k > \text{left}$. Thus, $A[\text{right}]$ is useless as a bottom piece and is discarded (increment `right` only).
3.  **Termination**: The loop ends when `right` reaches the end of the array. The value of `k` is the maximum number of kagamimochi.
4.  **Complexity**: The algorithm runs in $O(N)$ time as each element is visited at most once by the pointers, and $O(N)$ space to store the input. This fits well within the constraints ($N \le 5 \times 10^5$).
