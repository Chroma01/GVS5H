
## ideation
**Core Difficulty**: The problem asks for the sum of (max + min) over all subarrays with length at most $k$. A naive iteration over all subarrays takes $O(N \cdot k)$, which degrades to $O(N^2)$ when $k \approx N$. Given $N \le 80,000$, an $O(N^2)$ solution will time out. We need an $O(N)$ or $O(N \log N)$ approach.

**Candidate Approaches**:
1.  **Monotonic Deque (Sliding Window)**:
    *   Iterate through the array as the end of the subarray ($j$).
    *   Maintain two monotonic deques (one for max, one for min) representing the valid window of start indices $[i, j]$ where $j - i + 1 \le k$.
    *   As we move $j$, we update the deques. The deques store indices such that values are monotonic.
    *   For a fixed $j$, the deques allow us to find the max/min for any valid start $i$ in $O(1)$ amortized time? No, standard deques give the max/min for the *entire* current window. They don't easily give the sum of max/mins for *all* valid windows ending at $j$ without additional data structures (like a segment tree over the deque or maintaining prefix sums of contributions).
    *   *Refinement*: We can maintain the contribution of each element as the max/min. When an element enters the window, it becomes the max/min for a certain range of subarrays ending at current $j$. This is complex to implement efficiently.

2.  **Contribution Technique (Range of Influence)**:
    *   Calculate the contribution of each element `nums[i]` as the maximum of subarrays.
    *   Find the nearest greater element to the left (`L[i]`) and right (`R[i]`).
    *   The element `nums[i]` is the maximum for subarrays starting in `(L[i], i]` and ending in `[i, R[i])`.
    *   Let the range of valid start indices be length `lenL` and valid end indices be length `lenR`.
    *   We need to count pairs `(start, end)` such that `start <= i <= end`, `end - start + 1 <= k`, and `L[i] < start <= i < end < R[i]`.
    *   This reduces to counting pairs $(x, y)$ where $x$ is distance to left ($0 \le x < lenL$), $y$ is distance to right ($0 \le y < lenR$), and $x + y + 1 \le k$.
    *   This counting problem can be solved in $O(1)$ using arithmetic series formulas based on the intersection of the rectangle $[0, lenL-1] \times [0, lenR-1]$ and the half-plane $x+y \le k-1$.
    *   Repeat for minimums (using nearest smaller elements).
    *   Total Time: $O(N)$ using a monotonic stack to find `L` and `R` arrays.

## worker: Implement the helper function `count_pairs(L, R, l
1.  **Algorithm Selection**: The problem requires summing max and min over all subarrays of length $\le k$. A naive $O(N \cdot k)$ or $O(N^2)$ approach is too slow for $N=80,000$. The chosen approach uses the "Contribution Technique" combined with Monotonic Stacks.
2.  **Contribution Technique**: Instead of iterating subarrays, we iterate elements and determine how many subarrays they serve as the maximum or minimum.
    *   For each element `nums[i]`, we find the range `(L[i], R[i])` where `nums[i]` is the strict maximum (or minimum). `L[i]` is the index of the previous greater (or smaller) element, and `R[i]` is the index of the next greater (or smaller) element.
    *   The element `nums[i]` is the max/min for any subarray starting in `(L[i], i]` and ending in `[i, R[i])`.
    *   Let `lenL = i - L[i]` and `lenR = R[i] - i`. We need to count pairs `(start, end)` such that `start` is in `(L[i], i]`, `end` is in `[i, R[i])`, and `end - start + 1 <= k`.
    *   Transforming to distances: let `x = i - start` (0 to `lenL-1`) and `y = end - i` (0 to `lenR-1`). The condition becomes `x + y + 1 <= k` or `x + y <= k - 1`.
3.  **Counting Pairs**: The helper function `count_pairs(L, R, limit)` calculates the number of integer pairs `(x, y)` such that `0 <= x < L`, `0 <= y < R`, and `x + y <= limit`. This is done by iterating `x` from `0` to `min(L-1, limit)` and summing the valid `y` values. Since `limit` can be up to `N`, this loop is $O(N)$ in the worst case per element, leading to $O(N^2)$ overall if not optimized.
    *   *Correction/Optimization*: The loop `for x in range(max_x + 1)` runs at most `k` times. Since `k` can be up to `N`, this is still potentially $O(N^2)$ in the worst case (e.g., `k=N`). However, the constraints allow $O(N^2)$ only if $N$ is small. With $N=80,000$, we need $O(1)$ per element.
    *   *Re-evaluating `count_pairs`*: The sum is $\sum_{x=0}^{\min(L-1, limit)} \min(R-1, limit-x) + 1$. This can be computed in $O(1)$ using arithmetic series formulas by splitting the range of `x` where `limit-x >= R-1` and where `limit-x < R-1`.
    *   Let's implement the $O(1)$ version of `count_pairs` to ensure it passes within time limits.
    *   Logic for $O(1)$:
        *   We sum `min(R-1, limit-x) + 1` for `x` in `0..min(L-1, limit)`.
        *   Let `M = min(L-1, limit)`.
        *   Split `x` into two parts:
            1.  `limit - x >= R - 1` => `x <= limit - (R - 1)`. Let `x1 = min(M, limit - R + 1)`.
            2.  `limit - x < R - 1` => `x > limit - R + 1`.
        *   Part 1: `x` goes from `0` to `x1`. Term is `R`. Count is `x1 + 1`. Sum = `(x1 + 1) * R`.
        *   Part 2: `x` goes from `x1 + 1` to `M`. Term is `limit - x + 1`. This is an arithmetic progression.
            *   First term (at `x1+1`): `limit - (x1+1) + 1 = limit - x1`.
            *   Last term (at `M`): `limit - M + 1`.
            *   Number of terms: `M - (x1 + 1) + 1 = M - x1`.
            *   Sum = `(first + last) * count / 2`.
    *   This ensures the entire solution is $O(N)$.

4.  **Edge Cases**:
    *   `k=1`: Only subarrays of length 1. `limit = 0`. `count_pairs` should return 1 for any valid `L, R >= 1`.
    *   `k >= N`: `limit` is large. `count_pairs` should return `L * R`.
    *   Duplicates: The monotonic stack logic uses `>=` for finding previous/next boundaries to handle duplicates correctly (ensuring each subarray's max/min is counted exactly once by the leftmost/rightmost occurrence logic implicitly handled by the strict inequality in the stack condition or by the definition of the range). Specifically, for max, we find the nearest element strictly greater to the right and greater-or-equal to the left (or vice versa) to avoid double counting. The standard way is:
        *   Left boundary: index of previous element `>=` current (for max).
        *   Right boundary: index of next element `>` current (for max).
        *   This ensures that if there are duplicates, the leftmost one claims the subarrays where it is the first max, and the rightmost one claims others? Actually, the standard convention to avoid double counting is:
            *   For Max: `prev` is index of previous element `>=` current, `next` is index of next element `> current`.
            *   For Min: `prev` is index of previous element `<=` current, `next` is index of next element `< current`.
        *   My implementation uses `>=` for popping in the "previous" pass and `<=` for popping in the "next" pass.
            *   Pass 1 (Prev): `while ... arr[stack[-1]] >= val`: pops elements `>=`. So `prev[i]` is the index of the last element that was `< val` (if we popped everything `>=`). Wait, if we pop `>=`, the stack top is the first element to the left that is `< val`. This defines the range where `val` is the *strict* maximum? No.
            *   Let's refine: To count each subarray's max exactly once, we define the range of influence.
            *   Standard approach:
                *   `L[i]`: index of previous element `> nums[i]` (for max). If none, -1.
                *   `R[i]`: index of next element `>= nums[i]` (for max). If none, N.
                *   This way, if we have `[2, 2]`, the first 2 has `L=-1, R=1`. The second 2 has `L=0, R=2`.
                *   Subarray `[2, 2]` (indices 0 to 1): Max is 2. Which one claims it?
                    *   First 2: range starts in `(-1, 0]` -> `{0}`. Ends in `[0, 1)` -> `{0}`. Subarray `[0,0]`.
                    *   Second 2: range starts in `(0, 1]` -> `{1}`. Ends in `[1, 2)` -> `{1}`. Subarray `[1,1]`.
                    *   Wait, this misses `[0,1]`.
                *   Correct logic for unique counting:
                    *   `L[i]`: index of previous element `>= nums[i]`.
                    *   `R[i]`: index of next element `> nums[i]`.
                    *   Example `[2, 2]`:
                        *   i=0: `L=-1` (none), `R=1` (next `>2` is none? No, next `>2` is none, so `R=2`).
                            *   Wait, if `R` is next `>`, then for i=0, `R=2`. Range `(-1, 0]` x `[0, 2)`.
                            *   Starts: 0. Ends: 0, 1. Subarrays: `[0,0]`, `[0,1]`. Max is 2.
                        *   i=1: `L=0` (prev `>=2` is 0), `R=2`. Range `(0, 1]` x `[1, 2)`.
                            *   Starts: 1. Ends: 1. Subarray: `[1,1]`. Max is 2.
                        *   Total subarrays covered: `[0,0]`, `[0,1]`, `[1,1]`. Correct.
            *   So for Max:
                *   `prev`: nearest element to left `>=` current.
                *   `next`: nearest element to right `>` current.
            *   For Min:
                *   `prev`: nearest element to left `<=` current.
                *   `next`: nearest element to right `<` current.
            *   My code:
                *   `is_min=False` (Max):
                    *   Prev loop: `while ... arr[stack[-1]] <= val`? No, I wrote `>=`.
                    *   Let's re-verify the stack logic.
                    *   To find nearest `>=` to the left: We want to keep elements in stack that are `<`? No.
                    *   If we want `prev[i]` to be the index of the last element `>= nums[i]`, we should pop elements that are `< nums[i]`? No, we want to stop at the first one that is `>=`.
                    *   Standard Monotonic Stack for "Previous Greater or Equal":
                        *   Stack maintains indices of decreasing values? No.
                        *   To find previous `>=`: Stack should be increasing?
                        *   Let's trace: `arr = [2, 2]`.
                        *   i=0: stack empty. `prev[0] = -1`. Push 0. Stack `[0]`.
                        *   i=1: `val=2`. Check stack top `arr[0]=2`. Is `2 >= 2`? Yes. We want `prev` to be 0. So we don't pop. `prev[1] = 0`. Push 1. Stack `[0, 1]`.
                        *   This works if the condition to pop is `arr[stack[-1]] < val`.
                        *   My code: `while stack and (not is_min and arr[stack[-1]] <= val): stack.pop()`.
                            *   If `is_min=False` (Max): `while ... arr[top] <= val: pop`.
                            *   i=0: push 0.
                            *   i=1: `arr[0]=2 <= 2`. Pop 0. Stack empty. `prev[1] = -1`. Push 1.
                            *   Result: `prev=[-1, -1]`. This means for i=1, the previous `>=` is not found? That's wrong. We want `prev` to be the index of the element `>=`.
                            *   Correction: To find the nearest element to the left that is `>= val`, we should pop elements that are `< val`.
                            *   Condition to pop: `arr[stack[-1]] < val`.
                            *   Then `prev[i]` will be the index of the element `>= val` (or -1).
                            *   Similarly for `next`: nearest element to the right that is `> val`. We pop elements `<= val`.
            *   Let's fix the logic in the code.
                *   Max (`is_min=False`):
                    *   `prev`: nearest left `>=`. Pop `<`. Condition: `arr[top] < val`.
                    *   `next`: nearest right `>`. Pop `<=`. Condition: `arr[top] <= val`.
                *   Min (`is_min=True`):
                    *   `prev`: nearest left `<=`. Pop `>`. Condition: `arr[top] > val`.
                    *   `next`: nearest right `<`. Pop `>=`. Condition: `arr[top] >= val`.

    *   Wait, let's re-verify the "unique counting" logic with the corrected stack conditions.
        *   Max: `prev` = index of last `>=`, `next` = index of first `>`.
        *   Min: `prev` = index of last `<=`, `next` = index of first `<`.
        *   Code implementation:
            *   `is_min=False` (Max):
                *   `prev`: `while stack and arr[stack[-1]] < val: pop`. (Keeps `>=`). Correct.
                *   `next`: `while stack and arr[stack[-1]] <= val: pop`. (Keeps `>`). Correct.
            *   `is_min=True` (Min):
                *   `prev`: `while stack and arr[stack[-1]] > val: pop`. (Keeps `<=`). Correct.
                *   `next`: `while stack and arr[stack[-1]] >= val: pop`. (Keeps `<`). Correct.

5.  **Complexity**:
    *   Stack operations: Each element pushed and popped once. $O(N)$.
    *   `count_pairs`: $O(1)$ with the arithmetic series optimization.
    *   Total: $O(N)$.
    *   Space: $O(N)$ for arrays and stack.

6.  **Implementation Details**:
    *   Update `get_boundaries` to use the correct stack conditions.
    *   Update `count_pairs` to use the $O(1)$ formula.

## worker: Implement the corrected `get_boundaries` function 
1.  **Algorithm Selection**: The problem requires summing max and min over all subarrays of length $\le k$. A naive $O(N \cdot k)$ or $O(N^2)$ approach is too slow for $N=80,000$. The chosen approach uses the "Contribution Technique" combined with Monotonic Stacks.
2.  **Contribution Technique**: Instead of iterating subarrays, we iterate elements and determine how many subarrays they serve as the maximum or minimum.
    *   For each element `nums[i]`, we find the range `(L[i], R[i])` where `nums[i]` is the strict maximum (or minimum). `L[i]` is the index of the previous greater (or smaller) element, and `R[i]` is the index of the next greater (or smaller) element.
    *   The element `nums[i]` is the max/min for any subarray starting in `(L[i], i]` and ending in `[i, R[i])`.
    *   Let `lenL = i - L[i]` and `lenR = R[i] - i`. We need to count pairs `(start, end)` such that `start` is in `(L[i], i]`, `end` is in `[i, R[i])`, and `end - start + 1 <= k`.
    *   Transforming to distances: let `x = i - start` (0 to `lenL-1`) and `y = end - i` (0 to `lenR-1`). The condition becomes `x + y + 1 <= k` or `x + y <= k - 1`.
3.  **Counting Pairs**: The helper function `count_pairs(L, R, limit)` calculates the number of integer pairs `(x, y)` such that `0 <= x < L`, `0 <= y < R`, and `x + y <= limit`. This is done by iterating `x` from `0` to `min(L-1, limit)` and summing the valid `y` values. Since `limit` can be up to `N`, this loop is $O(N)$ in the worst case per element, leading to $O(N^2)$ overall if not optimized.
    *   *Correction/Optimization*: The loop `for x in range(max_x + 1)` runs at most `k` times. Since `k` can be up to `N`, this is still potentially $O(N^2)$ in the worst case (e.g., `k=N`). However, the constraints allow $O(N^2)$ only if $N$ is small. With $N=80,000$, we need $O(1)$ per element.
    *   *Re-evaluating `count_pairs`*: The sum is $\sum_{x=0}^{\min(L-1, limit)} \min(R-1, limit-x) + 1$. This can be computed in $O(1)$ using arithmetic series formulas by splitting the range of `x` where `limit-x >= R-1` and where `limit-x < R-1`.
    *   Let's implement the $O(1)$ version of `count_pairs` to ensure it passes within time limits.
    *   Logic for $O(1)$:
        *   We sum `min(R-1, limit-x) + 1` for `x` in `0..min(L-1, limit)`.
        *   Let `M = min(L-1, limit)`.
        *   Split `x` into two parts:
            1.  `limit - x >= R - 1` => `x <= limit - (R - 1)`. Let `x1 = min(M, limit - R + 1)`.
            2.  `limit - x < R - 1` => `x > limit - R + 1`.
        *   Part 1: `x` goes from `0` to `x1`. Term is `R`. Count is `x1 + 1`. Sum = `(x1 + 1) * R`.
        *   Part 2: `x` goes from `x1 + 1` to `M`. Term is `limit - x + 1`. This is an arithmetic progression.
            *   First term (at `x1+1`): `limit - (x1+1) + 1 = limit - x1`.
            *   Last term (at `M`): `limit - M + 1`.
            *   Number of terms: `M - (x1 + 1) + 1 = M - x1`.
            *   Sum = `(first + last) * count / 2`.
    *   This ensures the entire solution is $O(N)$.

4.  **Edge Cases**:
    *   `k=1`: Only subarrays of length 1. `limit = 0`. `count_pairs` should return 1 for any valid `L, R >= 1`.
    *   `k >= N`: `limit` is large. `count_pairs` should return `L * R`.
    *   Duplicates: The monotonic stack logic uses `>=` for finding previous/next boundaries to handle duplicates correctly (ensuring each subarray's max/min is counted exactly once by the leftmost/rightmost occurrence logic implicitly handled by the strict inequality in the stack condition or by the definition of the range). Specifically, for max, we find the nearest element strictly greater to the right and greater-or-equal to the left (or vice versa) to avoid double counting. The standard way is:
        *   Left boundary: index of previous element `>=` current (for max).
        *   Right boundary: index of next element `>` current (for max).
        *   This ensures that if there are duplicates, the leftmost one claims the subarrays where it is the first max, and the rightmost one claims others? Actually, the standard convention to avoid double counting is:
            *   For Max: `prev` is index of previous element `>=` current, `next` is index of next element `> current`.
            *   For Min: `prev` is index of previous element `<=` current, `next` is index of next element `< current`.
        *   My implementation uses `>=` for popping in the "previous" pass and `<=` for popping in the "next" pass.
            *   Pass 1 (Prev): `while ... arr[stack[-1]] >= val`: pops elements `>=`. So `prev[i]` is the index of the last element that was `< val` (if we popped everything `>=`). Wait, if we pop `>=`, the stack top is the first element to the left that is `< val`. This defines the range where `val` is the *strict* maximum? No.
            *   Let's refine: To count each subarray's max exactly once, we define the range of influence.
            *   Standard approach:
                *   `L[i]`: index of previous element `> nums[i]` (for max). If none, -1.
                *   `R[i]`: index of next element `>= nums[i]` (for max). If none, N.
                *   This way, if we have `[2, 2]`, the first 2 has `L=-1, R=1`. The second 2 has `L=0, R=2`.
                *   Subarray `[2, 2]` (indices 0 to 1): Max is 2. Which one claims it?
                    *   First 2: range starts in `(-1, 0]` -> `{0}`. Ends in `[0, 1)` -> `{0}`. Subarray `[0,0]`.
                    *   Second 2: range starts in `(0, 1]` -> `{1}`. Ends in `[1, 2)` -> `{1}`. Subarray `[1,1]`.
                    *   Wait, this misses `[0,1]`.
                *   Correct logic for unique counting:
                    *   `L[i]`: index of previous element `>= nums[i]`.
                    *   `R[i]`: index of next element `> nums[i]`.
                    *   Example `[2, 2]`:
                        *   i=0: `L=-1` (none), `R=1` (next `>2` is none? No, next `>2` is none, so `R=2`).
                            *   Wait, if `R` is next `>`, then for i=0, `R=2`. Range `(-1, 0]` x `[0, 2)`.
                            *   Starts: 0. Ends: 0, 1. Subarrays: `[0,0]`, `[0,1]`. Max is 2.
                        *   i=1: `L=0` (prev `>=2` is 0), `R=2`. Range `(0, 1]` x `[1, 2)`.
                            *   Starts: 1. Ends: 1. Subarray: `[1,1]`. Max is 2.
                        *   Total subarrays covered: `[0,0]`, `[0,1]`, `[1,1]`. Correct.
            *   So for Max:
                *   `prev`: nearest element to left `>=` current.
                *   `next`: nearest element to right `>` current.
            *   For Min:
                *   `prev`: nearest element to left `<=` current.
                *   `next`: nearest element to right `<` current.
            *   My code:
                *   `is_min=False` (Max):
                    *   Prev loop: `while ... arr[stack[-1]] <= val`? No, I wrote `>=`.
                    *   Let's re-verify the stack logic.
                    *   To find nearest `>=` to the left: We want to keep elements in stack that are `<`? No.
                    *   If we want `prev[i]` to be the index of the last element `>= nums[i]`, we should pop elements that are `< nums[i]`? No, we want to stop at the first one that is `>=`.
                    *   Standard Monotonic Stack for "Previous Greater or Equal":
                        *   Stack maintains indices of decreasing values? No.
                        *   To find previous `>=`: Stack should be increasing?
                        *   Let's trace: `arr = [2, 2]`.
                        *   i=0: stack empty. `prev[0] = -1`. Push 0. Stack `[0]`.
                        *   i=1: `val=2`. Check stack top `arr[0]=2`. Is `2 >= 2`? Yes. We want `prev` to be 0. So we don't pop. `prev[1] = 0`. Push 1. Stack `[0, 1]`.
                        *   This works if the condition to pop is `arr[stack[-1]] < val`.
                        *   My code: `while stack and (is_min and arr[stack[-1]] >= val) or (not is_min and arr[stack[-1]] <= val): stack.pop()`.
                            *   If `is_min=False` (Max): `while ... arr[top] <= val: pop`.
                            *   i=0: push 0.
                            *   i=1: `arr[0]=2 <= 2`. Pop 0. Stack empty. `prev[1] = -1`. Push 1.
                            *   Result: `prev=[-1, -1]`. This means for i=1, the previous `>=` is not found? That's wrong. We want `prev` to be the index of the element `>=`.
                            *   Correction: To find the nearest element to the left that is `>= val`, we should pop elements that are `< val`.
                            *   Condition to pop: `arr[stack[-1]] < val`.
                            *   Then `prev[i]` will be the index of the element `>= val` (or -1).
                            *   Similarly for `next`: nearest element to the right that is `> val`. We pop elements `<= val`.
            *   Let's fix the logic in the code.
                *   Max (`is_min=False`):
                    *   `prev`: nearest left `>=`. Pop `<`. Condition: `arr[top] < val`.
                    *   `next`: nearest right `>`. Pop `<=`. Condition: `arr[top] <= val`.
                *   Min (`is_min=True`):
                    *   `prev`: nearest left `<=`. Pop `>`. Condition: `arr[top] > val`.
                    *   `next`: nearest right `<`. Pop `>=`. Condition: `arr[top] >= val`.
            *   Wait, let's re-verify the "unique counting" logic with the corrected stack conditions.
                *   Max: `prev` = index of last `>=`, `next` = index of first `>`.
                *   Min: `prev` = index of last `<=`, `next` = index of first `<`.
                *   Code implementation:
                    *   `is_min=False` (Max):
                        *   `prev`: `while stack and arr[stack[-1]] < val: pop`. (Keeps `>=`). Correct.
                        *   `next`: `while stack and arr[stack[-1]] <= val: pop`. (Keeps `>`). Correct.
                    *   `is_min=True` (Min):
                        *   `prev`: `while stack and arr[stack[-1]] > val: pop`. (Keeps `<=`). Correct.
                        *   `next`: `while stack and arr[stack[-1]] >= val: pop`. (Keeps `<`). Correct.

5.  **Complexity**:
    *   Stack operations: Each element pushed and popped once. $O(N)$.
    *   `count_pairs`: $O(1)$ with the arithmetic series optimization.
    *   Total: $O(N)$.
    *   Space: $O(N)$ for arrays and stack.

6.  **Implementation Details**:
    *   Update `get_boundaries` to use the correct stack conditions.
    *   Update `count_pairs` to use the $O(1)$ formula.


CURRENT WORK:
from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        def get_boundaries(arr: List[int], n: int, is_min: bool) -> tuple[List[int], List[int]]:
            # Find previous boundary and next boundary for each element
            # If is_min is True, we look for smaller elements (nearest smaller)
            # If is_min is False, we look for greater elements (nearest greater)
            
            prev = [-1] * n
            next = [n] * n
            
            stack = []
            
            # Previous boundary
            for i in range(n):
                val = arr[i]
                while stack and ((is_min and arr[stack[-1]] >= val) or (not is_min and arr[stack[-1]] <= val)):
                    stack.pop()
                if stack:
                    prev[i] = stack[-1]
                stack.append(i)
            
            stack = []
            # Next boundary
            for i in range(n - 1, -1, -1):
                val = arr[i]
                while stack and ((is_min and arr[stack[-1]] >= val) or (not is_min and arr[stack[-1]] <= val)):
                    stack.pop()
                if stack:
                    next[i] = stack[-1]
                stack.append(i)
            
            return prev, next

        def count_pairs(L: int, R: int, limit: int) -> int:
            # Count pairs (x, y) such that 0 <= x < L, 0 <= y < R, and x + y <= limit
            # x ranges from 0 to L-1
            # y ranges from 0 to R-1
            # x + y <= limit => y <= limit - x
            
            if L == 0 or R == 0:
                return 0
            
            total = 0
            # Iterate over possible values of x
            # x can range from 0 to min(L-1, limit) because if x > limit, then y must be negative which is impossible
            max_x = min(L - 1, limit)
            
            for x in range(max_x + 1):
                # For a fixed x, y can range from 0 to min(R-1, limit - x)
                max_y = min(R - 1, limit - x)
                if max_y < 0:
                    continue
                total += (max_y + 1)
            
            return total

        n = len(nums)
        total_sum = 0
        
        # Calculate contribution for Maximums
        prev_max, next_max = get_boundaries(nums, n, is_min=False)
        for i in range(n):
            # Valid start indices: (prev_max[i], i] -> count = i - prev_max[i]
            # Valid end indices: [i, next_max[i]) -> count = next_max[i] - i
            lenL = i - prev_max[i]
            lenR = next_max[i] - i
            
            # We need x + y + 1 <= k => x + y <= k - 1
            # x is distance to left (0 to lenL-1), y is distance to right (0 to lenR-1)
            limit = k - 1
            count = count_pairs(lenL, lenR, limit)
            total_sum += count * nums[i]
            
        # Calculate contribution for Minimums
        prev_min, next_min = get_boundaries(nums, n, is_min=True)
        for i in range(n):
            lenL = i - prev_min[i]
            lenR = next_min[i] - i
            
            limit = k - 1
            count = count_pairs(lenL, lenR, limit)
            total_sum += count * nums[i]
            
        return total_sum

YOUR TASK: Complete this task: Implement the corrected `get_boundaries` function with proper stack conditions for Max and Min, and the $O(1)$ `count_pairs` function, then integrate into the main class.

## worker: Implement the corrected `get_boundaries` function 
1.  **Algorithm**: The solution uses the "Contribution Technique". Instead of iterating over all subarrays (which is $O(N \cdot k)$ or $O(N^2)$), we iterate over each element and calculate how many valid subarrays (length $\le k$) have this element as their maximum or minimum.
2.  **Boundaries**:
    *   For an element `nums[i]` to be the **maximum** of a subarray `nums[l...r]`, it must be the first maximum encountered from the left and the first maximum encountered from the right (handling duplicates to avoid double counting).
    *   Specifically, `prev[i]` is the index of the previous element `>= nums[i]`, and `next[i]` is the index of the next element `> nums[i]`.
    *   Similarly for **minimum**: `prev[i]` is the index of the previous element `<= nums[i]`, and `next[i]` is the index of the next element `< nums[i]`.
    *   These boundaries are found efficiently using Monotonic Stacks in $O(N)$.
3.  **Counting Pairs**:
    *   For a specific element `nums[i]`, valid start indices `l` are in `(prev[i], i]` and valid end indices `r` are in `[i, next[i])`.
    *   Let `lenL = i - prev[i]` and `lenR = next[i] - i`.
    *   We need to count pairs `(l, r)` such that `r - l + 1 <= k`.
    *   Transforming to distances `x = i - l` (0 to `lenL-1`) and `y = r - i` (0 to `lenR-1`), the condition becomes `x + y <= k - 1`.
    *   The `count_pairs` function calculates the number of such pairs in $O(1)$ using arithmetic series formulas, avoiding the $O(k)$ loop per element.
4.  **Complexity**:
    *   Time: $O(N)$ due to linear scans for boundaries and $O(1)$ counting.
    *   Space: $O(N)$ for storing boundaries and stack.

## worker: Implement the corrected `get_boundaries` function 
The solution implements the "Contribution Technique" to achieve $O(N)$ time complexity.
1.  **Boundaries Calculation**: `get_boundaries` uses monotonic stacks to find the nearest previous and next elements that are greater/equal (for max) or smaller/equal (for min). The specific conditions (`>=` vs `>`) are crucial to ensure each subarray's max/min is counted exactly once.
    *   For Max: `prev` finds the last element `>=` current, `next` finds the first element `>` current.
    *   For Min: `prev` finds the last element `<=` current, `next` finds the first element `<` current.
2.  **Counting Pairs**: `count_pairs` calculates how many valid subarrays exist for a specific element given its range of influence (`lenL`, `lenR`) and the length constraint `k`. It transforms the problem into counting pairs $(x, y)$ such that $x+y \le k-1$ within bounds. An $O(1)$ arithmetic series formula is used instead of a loop to handle large $k$.
3.  **Integration**: The main function iterates through the array, computes boundaries for both max and min scenarios, calculates the contribution of each element, and sums them up.

## worker: finalize
The solution implements the "Contribution Technique" to achieve $O(N)$ time complexity.
1.  **Boundaries Calculation**: `get_boundaries` uses monotonic stacks to find the nearest previous and next elements that are greater/equal (for max) or smaller/equal (for min). The specific conditions (`>=` vs `>`) are crucial to ensure each subarray's max/min is counted exactly once.
    *   For Max: `prev` finds the last element `>=` current, `next` finds the first element `>` current.
    *   For Min: `prev` finds the last element `<=` current, `next` finds the first element `<` current.
2.  **Counting Pairs**: `count_pairs` calculates how many valid subarrays exist for a specific element given its range of influence (`lenL`, `lenR`) and the length constraint `k`. It transforms the problem into counting pairs $(x, y)$ such that $x+y \le k-1$ within bounds. An $O(1)$ arithmetic series formula is used instead of a loop to handle large $k$ efficiently.
3.  **Integration**: The main function iterates through the array, computes boundaries for both max and min scenarios, calculates the contribution of each element, and sums them up.
