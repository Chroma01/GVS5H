
## ideation
The problem asks to maximize the number of pairs $(a, b)$ from a sorted array $A$ such that $a \le b/2$.
**Core Difficulty**: This is a maximum matching problem on a specific constraint graph, but due to the sorted nature of the input and the specific inequality ($a \le b/2$), a greedy strategy is optimal. The challenge is to correctly implement the greedy choice to ensure we don't "waste" small bases on large tops or small tops on unnecessarily large bases.

**Candidate Approaches**:
1.  **Greedy with Two Pointers**:
    -   Maintain two pointers, `left` (for the potential top mochi) and `right` (for the potential bottom mochi).
    -   Since the array is sorted ($A_1 \le A_2 \le \dots \le A_N$), the smallest available mochi is the best candidate for a "top". The smallest available mochi that is large enough to be a "bottom" is the best candidate to save larger bases for even larger tops later.
    -   Algorithm:
        -   Initialize `left = 0`, `right = 0`, `count = 0`.
        -   While `right < N`:
            -   If `left == right`: `right++` (cannot pair an element with itself).
            -   Check condition: `A[left] * 2 <= A[right]`.
            -   If true: We form a pair. Increment `count`, `left++`, `right++`.
            -   If false: The current `A[right]` is too small to support `A[left]`. Since the array is sorted, `A[right]` cannot support any future `A[k]` where $k > left$ (because those are larger). Thus, `A[right]` is useless as a base. Increment `right` to find a larger base.
    -   *Correction/Refinement*: Wait, if `A[left] * 2 > A[right]`, does it mean `A[right]` is useless? Yes, because any subsequent top `A[k]` ($k > left$) will be $\ge A[left]$, so `A[k] * 2 \ge A[left] * 2 > A[right]`. So `A[right]` can never be a base for any remaining top. We must discard `A[right]`.
    -   What if `A[left]` is too large for `A[right]`, but `A[left+1]` is even larger? Yes, so if the condition fails, `A[right]` is discarded.
    -   Is it ever beneficial to skip `left` (i.e., not use `A[left]` as a top even if it fits)? No. Using the smallest possible top allows us to save larger tops for larger bases, maximizing the pool of potential pairs. Using the smallest valid base saves larger bases for larger tops. This is a standard greedy exchange argument.

2.  **Binary Search on Answer**:
    -   Check if it's possible to make $K$ pairs.
    -   To check feasibility for $K$: We need to select $K$ tops and $K$ bottoms.
    -   Greedy check: Pick the $K$ smallest elements as tops? Not necessarily. Actually, to maximize the chance of satisfying $a \le b/2$, we should pick the smallest $K$ elements as tops and the largest $K$ elements as bottoms? No, that's not quite right because they must be disjoint.
    -   Better check: Sort array (already sorted). Try to match the $i$-th smallest available top with the $i$-th smallest available bottom.
    -   This approach is $O(N \log N)$ or $O(N)$ with two pointers inside the check, leading to $O(N \log N)$ total. Given $N=5 \times 10^5$, this is acceptable but more complex to implement than the direct greedy.

## worker: Write the Python solution using the two-pointer gr
The problem requires finding the maximum number of pairs $(a, b)$ from a sorted array such that $a \le b/2$.
The greedy strategy employed is:
1.  Maintain two pointers, `left` (for the top mochi) and `right` (for the bottom mochi).
2.  Start both at 0.
3.  If `left == right`, increment `right` to ensure distinct elements.
4.  Check if `a[left] * 2 <= a[right]`.
    -   If true, we form a pair. This is optimal because `a[left]` is the smallest available top, and `a[right]` is the smallest available base that can support it. Using the smallest valid base saves larger bases for potentially larger tops later. Increment both pointers.
    -   If false, `a[right]` is too small to support `a[left]`. Since the array is sorted, any subsequent top `a[k]` (where $k > left$) will be $\ge a[left]$, so `a[right]` cannot support any remaining top. Thus, `a[right]` is discarded, and we increment `right`.
5.  Repeat until `right` reaches the end of the array.

This approach runs in $O(N)$ time complexity, which fits well within the constraints ($N \le 5 \times 10^5$).
