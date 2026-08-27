
## ideation
The problem requires counting subarrays that can be made non-decreasing with at most `k` increments. The minimum cost to make a subarray `nums[i..j]` non-decreasing is given by $\sum_{m=i}^{j} (\max_{p \in [i, m]} \text{nums}[p] - \text{nums}[m])$. This can be rewritten as $S_{\text{max}}(i, j) - S_{\text{nums}}(i, j)$, where $S_{\text{max}}$ is the sum of maximums of all prefixes of the subarray, and $S_{\text{nums}}$ is the sum of elements.

We can use a sliding window (two pointers) approach. As we expand the right pointer, we maintain $S_{\text{max}}$ and $S_{\text{nums}}$ efficiently. A monotonic deque is used to track the maximums in the current window. The deque stores pairs `[value, count]`, where `count` represents how many elements in the current window have this value as their maximum. 
- When adding `nums[right]`, we update the deque and $S_{\text{max}}$. If the new element is smaller than the deque's back, it shares the same maximum, so we increment the count and add that maximum to $S_{\text{max}}$. Otherwise, we pop smaller elements, accumulate their counts, and push the new element.
- When the cost $S_{\text{max}} - S_{\text{nums}}$ exceeds `k`, we shrink the window from the left. If the leftmost element equals the current maximum, we decrement its count in the deque and subtract its value from $S_{\text{max}}$. If the count drops to zero, we pop it. We also update $S_{\text{nums}}$.
- The number of valid subarrays ending at `right` is `right - left + 1`.

This approach runs in $O(n)$ time since each element is added and removed from the deque at most once, and uses $O(n)$ space for the deque.
