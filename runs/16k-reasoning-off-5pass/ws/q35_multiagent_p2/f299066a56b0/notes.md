
## ideation
The problem asks for the maximum number of pairs (top, bottom) such that `top_size <= bottom_size / 2`. The array is sorted. The key insight is that we should try to pair the smallest available mochi as "tops" with the smallest valid "bottoms" to save larger bottoms for potentially larger tops. 

A greedy two-pointer approach works:
1. Use one pointer `i` for potential tops, starting from the beginning (index 0).
2. Use another pointer `j` for potential bottoms, starting from the middle (index N//2). Why middle? Because in the best case, we can pair at most N//2 pairs. The smallest N//2 elements are candidates for tops, and the largest N//2 elements are candidates for bottoms. If we start `j` at 0, we might pair small bottoms with small tops, but we need to ensure bottoms are large enough. Starting `j` at N//2 is a safe heuristic because any valid pair must have the bottom index greater than the top index (since A is sorted and A[i] <= A[j]/2 implies A[i] < A[j] for positive integers), and we can't have more than N//2 pairs.

Algorithm:
- Initialize `i = 0`, `j = N // 2`, `count = 0`.
- While `i < N // 2` and `j < N`:
  - If `A[i] * 2 <= A[j]`, then we can form a pair. Increment `count`, `i`, and `j`.
  - Else, the current bottom `A[j]` is too small for the current top `A[i]`. Since the array is sorted, we need a larger bottom, so increment `j`.
- The answer is `count`.

This works because:
- We try to pair the smallest available top with the smallest available valid bottom.
- If a bottom is too small for a top, it's too small for any subsequent (larger) top, so we discard it by moving `j`.
- If a bottom is valid, we use it because using a larger bottom for the same top would be wasteful.

Pitfalls:
- Starting `j` at 0 instead of N//2 might lead to incorrect results or inefficiency, but starting at N//2 is safe because we can't have more than N//2 pairs, and the bottoms must come from the upper half if we want to maximize pairs with the lower half as tops. Actually, even if we start `j` at 0, the logic still holds, but starting at N//2 is an optimization. Let's verify: if we start `j` at 0, we might pair A[0] with A[0] if A[0]*2 <= A[0], which is impossible for positive A[0]. So `j` must be > `i`. Starting `j` at N//2 ensures `j > i` for the first many iterations.

Let's trace with Sample 1: [2, 3, 4, 4, 7, 10], N=6.
i=0, j=3. A[0]=2, A[3]=4. 2*2=4 <= 4? Yes. count=1, i=1, j=4.
i=1, j=4. A[1]=3, A[4]=7. 3*2=6 <= 7? Yes. count=2, i=2, j=5.
i=2, j=5. A[2]=4, A[5]=10. 4*2=8 <= 10? Yes. count=3, i=3, j=6.
Loop ends. Output 3. Correct.

Sample 2: [387, 388, 389], N=3.
i=0, j=1. A[0]=387, A[1]=388. 387*2=774 <= 388? No. j=2.
i=0, j=2. A[0]=387, A[2]=389. 774 <= 389? No. j=3. Loop ends. Output 0. Correct.

## worker: Implement the two-pointer greedy approach as descr
The solution uses a greedy two-pointer approach. Since the array is sorted, we want to pair the smallest available mochi as "tops" with the smallest valid "bottoms" to save larger bottoms for other pairs. 

- Pointer `i` starts at 0 (smallest elements as top candidates).
- Pointer `j` starts at N//2 (larger elements as bottom candidates). This is because we can form at most N//2 pairs, and the bottoms must be from the upper half to potentially satisfy the condition A[i] * 2 <= A[j].
- If A[i] * 2 <= A[j], we form a pair and move both pointers forward.
- If not, the current bottom A[j] is too small for A[i]. Since the array is sorted, A[j] will also be too small for any subsequent (larger) A[i'], so we discard A[j] by moving j forward.

This greedy strategy is optimal because:
1. We always try to pair the smallest available top with the smallest valid bottom, which is the most "conservative" use of resources.
2. If a bottom is too small for a top, it's useless for any larger top, so discarding it is correct.
3. If a bottom is valid, using it is optimal because saving it for a larger top would be wasteful (the larger top might not find a valid bottom, or we'd need an even larger bottom).

Time complexity: O(N) since both pointers move at most N times.
Space complexity: O(N) to store the input array.
