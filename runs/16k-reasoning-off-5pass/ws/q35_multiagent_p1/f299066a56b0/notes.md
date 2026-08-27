
## ideation
The problem asks for the maximum number of pairs $(a, b)$ such that $a \le b/2$ (or $2a \le b$), where each mochi is used at most once. The input array $A$ is sorted in non-decreasing order.

Key observations:
1. To maximize the number of pairs, we should try to pair the smallest available mochi (potential top) with the smallest available mochi that is large enough to be its base. This "greedy" strategy saves larger mochi for potentially larger top candidates.
2. Since each pair consumes two distinct mochi, the maximum possible answer is $\lfloor N/2 \rfloor$.
3. We can use a two-pointer approach:
   - Let `left` point to the start of the array (candidates for the top/smaller mochi).
   - Let `right` point to the middle of the array (candidates for the bottom/larger mochi). Why start `right` at `N // 2`? Because if we are to form $K$ pairs, we need $K$ small mochi and $K$ large mochi. The best chance to pair the $K$ smallest mochi is with the $K$ largest mochi. Specifically, the $i$-th smallest mochi (0-indexed) should ideally be paired with a mochi from the upper half. Starting `right` at `N // 2` ensures we are looking at candidates that are likely to be large enough. If we started `right` at 0, we'd be checking small mochi as bases, which is inefficient and incorrect because small mochi can't be bases for other small mochi.
   - Actually, a more robust way to think about it: We want to match elements from the first half (as tops) with elements from the second half (as bottoms). Let `i` range from `0` to `N//2 - 1` (potential tops) and `j` range from `N//2` to `N-1` (potential bottoms).
   - For each `i` (top candidate), we find the smallest `j` (bottom candidate) such that `A[i] * 2 <= A[j]`. If found, we form a pair and move to the next `i` and next `j`. If not found (i.e., we exhaust `j`), we stop.
   - This greedy works because if `A[i]` can be paired with `A[j]`, it's optimal to do so because `A[i]` is the smallest available top, and `A[j]` is the smallest available bottom that satisfies the condition. Using a larger bottom for `A[i]` would only hurt our chances for larger tops. Using a smaller bottom (which doesn't satisfy the condition) is impossible.

Algorithm:
1. Initialize `i = 0` (pointer for top mochi, starting from beginning).
2. Initialize `j = N // 2` (pointer for bottom mochi, starting from middle).
3. Initialize `count = 0`.
4. While `i < N // 2` and `j < N`:
   - If `A[i] * 2 <= A[j]`:
     - We can form a pair. Increment `count`, `i`, and `j`.
   - Else:
     - `A[j]` is too small for `A[i]`. Since `A` is sorted, `A[j]` is also too small for any `A[k]` with `k > i`. So `A[j]` cannot be used as a bottom for any remaining top candidate. Increment `j` to try a larger bottom.
5. The answer is `count`.

Pitfalls:
- Starting `j` at 0 instead of `N//2` might work but is less efficient and conceptually messier. Starting at `N//2` is safe because we can't have more than `N//2` pairs, so the bottoms must come from at least the second half of the array in the optimal matching of smallest-to-largest.
- Edge case: $N=2$. `i` goes from 0 to 0, `j` starts at 1. Correct.
- The condition is `A[i] * 2 <= A[j]`, not `A[i] <= A[j] / 2` (to avoid floating point issues).

## worker: none
The solution uses a greedy two-pointer approach. We sort of implicitly rely on the input being sorted (which it is). We set up two pointers: `i` starting at 0 (for potential top mochi) and `j` starting at `N // 2` (for potential bottom mochi). The idea is that we can form at most `N // 2` pairs, so the bottoms must come from the second half of the array in an optimal strategy when trying to pair the smallest tops. For each top candidate `A[i]`, we find the smallest bottom candidate `A[j]` such that `2 * A[i] <= A[j]`. If such a `A[j]` is found, we form a pair and move both pointers. If not, `A[j]` is too small for `A[i]` and thus too small for any larger top candidate, so we move `j` forward to try a larger bottom. The number of successful pairs is the answer. This runs in O(N) time after the initial read, which is efficient for N up to 5 * 10^5.
