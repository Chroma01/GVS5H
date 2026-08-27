1. The problem asks for the sum of (max + min) for all subarrays of length 1 to k.
2. A naive O(N^2) solution will be too slow given N up to 80,000. We need an O(N) or O(N log N) approach.
3. We can use a monotonic deque (double-ended queue) to efficiently track the minimum and maximum elements in a sliding window.
4. However, since we need to consider all subarrays of length 1 to k ending at each index i, we can iterate through the array and maintain two deques: one for minimums and one for maximums.
5. For each index i, we add nums[i] to the deques, removing elements from the back that are worse than the current element (larger for min-deque, smaller for max-deque).
6. We then remove elements from the front of the deques if they are outside the window of size k (i.e., index < i - k + 1).
7. The current minimum is nums[deque_min[0]] and the current maximum is nums[deque_max[0]]. We add their sum to the total.
8. This approach runs in O(N) time because each element is added and removed from the deques at most once.