
## ideation
The core difficulty is efficiently pairing the smallest mochi as tops with valid larger mochi as bottoms to maximize the number of pairs. Since the array is sorted, we can use a greedy two-pointer approach. The key insight is that to maximize pairs, we should try to pair the smallest available mochi (as top) with the smallest possible valid mochi (as bottom) to save larger mochi for other potential tops. 

We can use two pointers:
- `i` for the top candidates, starting from index 0.
- `j` for the bottom candidates, starting from index `N // 2` (since we need at least as many bottoms as tops, and bottoms must be strictly larger than tops in terms of size constraint, but more importantly, we can't use the same mochi twice).

The algorithm:
1. Initialize `i = 0`, `j = N // 2`, and `count = 0`.
2. While `i < N // 2` and `j < N`:
   - If `A[i] <= A[j] // 2`, we can form a pair. Increment `count`, `i`, and `j`.
   - Otherwise, increment `j` to try a larger bottom.
3. The answer is `count`.

This works because:
- We only consider the first half as potential tops (since we need at least as many bottoms as tops).
- By starting `j` at `N // 2`, we ensure that we have enough candidates for bottoms.
- The greedy choice of pairing the smallest top with the smallest valid bottom is optimal because it leaves larger bottoms available for other tops.

Pitfalls:
- Make sure to use integer division for the condition `A[i] <= A[j] // 2`.
- Ensure that `i` does not exceed `N // 2 - 1` (since we can't have more tops than half the mochi).
- Ensure that `j` does not exceed `N - 1`.

## worker: <none>
The problem requires maximizing the number of pairs (top, bottom) from a sorted array such that `top <= bottom // 2`. The greedy two-pointer approach is optimal here:
1. We only need to consider the first `N//2` elements as potential tops, since each pair consumes two mochi.
2. We start the bottom pointer `j` at `N//2` because any valid bottom for a top in the first half must come from the second half (or later) to ensure we have enough distinct mochi.
3. For each top candidate `A[i]`, we find the smallest available bottom `A[j]` that satisfies `A[i] <= A[j] // 2`. If found, we form a pair and move both pointers. If not, we move `j` forward to try a larger bottom.
4. This greedy strategy works because pairing the smallest top with the smallest valid bottom leaves larger bottoms available for other tops, maximizing the total number of pairs.

Time complexity: O(N) since each pointer moves at most N times.
Space complexity: O(N) to store the input array.
