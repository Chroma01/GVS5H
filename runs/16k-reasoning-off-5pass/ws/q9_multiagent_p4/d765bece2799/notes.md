
## ideation
**Core Difficulty**: The problem asks for the sum of (min + max) for all subarrays with length $\le k$. A naive iteration over all subarrays is $O(N^2)$, which is too slow for $N=80,000$. The challenge is to efficiently calculate the contribution of each element as the minimum and maximum across all valid subarrays ending at each position, or to iterate through positions and query the current window's min/max in $O(1)$ amortized time.

**Candidate Approaches**:
1.  **Monotonic Deques (Sliding Window)**:
    *   Iterate through the array with index `i` as the right endpoint.
    *   Maintain two deques: `min_deque` (increasing) and `max_deque` (decreasing).
    *   For each `i`, update deques by removing elements from the back that violate monotonicity and adding `nums[i]`.
    *   Remove elements from the front if they are out of the window (index $< i - k + 1$).
    *   The front of `min_deque` gives the minimum, and the front of `max_deque` gives the maximum for the current window ending at `i`.
    *   **Crucial Detail**: The problem specifies subarrays with *at most* $k$ elements, not exactly $k$. This means for a fixed right endpoint `i`, we need to sum the min/max of windows of length $1, 2, \dots, \min(i+1, k)$.
    *   *Correction/Refinement*: The standard sliding window usually fixes the window size. Here, the window size varies. However, we can reframe the problem: Instead of summing over windows ending at `i` with varying lengths, we can iterate through the array and for each element, determine how many subarrays it serves as the min/max.
    *   *Alternative Refinement*: Actually, the standard monotonic stack/deque approach is often used to find the "previous smaller" and "next smaller" elements to determine the range where an element is the minimum.
    *   *Best Approach for "At Most K"*:
        *   For each element `nums[i]`, find the range $[L, R]$ where `nums[i]` is the minimum.
        *   Then, count how many subarrays within that range have length $\le k$ and where `nums[i]` is still the minimum.
        *   This requires careful calculation of boundaries considering the $k$ constraint.
        *   Alternatively, iterate `i` from $0$ to $n-1$. Maintain deques for the current window. But since the window length varies, simply taking the front of the deque at step `i` only gives the min/max for the window $[i-k+1, i]$. It does not give the sum for $[i-k+2, i]$, etc.
        *   *Wait, let's re-read the example*:
            `nums = [1,2,3], k=2`.
            Subarrays: `[1]`, `[2]`, `[3]`, `[1,2]`, `[2,3]`.
            Notice `[1,2,3]` is excluded.
            If we iterate `i` (right end):
            - `i=0`: `[1]`. Min=1, Max=1.
            - `i=1`: `[2]`, `[1,2]`. Min=2,1; Max=2,2.
            - `i=2`: `[3]`, `[2,3]`. Min=3,2; Max=3,3.
            The standard sliding window deque at step `i` gives the min/max for the window of size exactly $k$ (or $\min(i+1, k)$ if we clamp). It doesn't directly give the sum for all sizes $< k$.
        *   **Correct Strategy**: We need to sum contributions.
            For each `i`, let's find the range of indices $[l, r]$ such that `nums[i]` is the minimum for all subarrays starting in $[l, i]$ and ending in $[i, r]$.
            Actually, a simpler way with Deques for "at most K":
            Iterate `i` from $0$ to $n-1$.
            Maintain `min_deque` and `max_deque` representing the candidates for min/max in the window ending at `i`.
            But we need to sum over lengths $1$ to $k$.
            Maybe we can compute the sum for "at most K" by computing "exactly K" and "at most K-1"? No, that's recursive.
            
            Let's reconsider the contribution method.
            For a specific element `x = nums[i]` to be the minimum of a subarray `nums[j...p]` (where $j \le i \le p$):
            1. `nums[i]` must be $\le$ all elements in `nums[j...i]`.
            2. `nums[i]` must be $\le$ all elements in `nums[i...p]`.
            3. Length $p - j + 1 \le k$.
            
            We can find the nearest smaller element to the left (`prev_smaller[i]`) and right (`next_smaller[i]`).
            Let $L = prev\_smaller[i] + 1$ and $R = next\_smaller[i]$.
            The element `nums[i]` is the minimum for any subarray starting in $[L, i]$ and ending in $[i, R]$.
            Now we need to count pairs $(start, end)$ such that $L \le start \le i \le end \le R$ AND $end - start + 1 \le k$.
            This counting can be done in $O(1)$ with some math or a two-pointer approach if we iterate.
            Since we need to do this for both min and max, we can run the "nearest smaller/larger" logic twice (or once with a generic comparator).
            
            This approach is $O(N)$ because finding prev/next smaller can be done with a monotonic stack in one pass.

## worker: Implement the `calculate_sum` helper that takes `n
The solution uses a monotonic stack approach to determine the range $[L, R]$ for each element where it acts as the minimum (or maximum) of a subarray.
1.  **Boundaries Calculation**:
    *   For minimums: `prev[i]` is the index of the first element to the left strictly smaller than `nums[i]`. `next[i]` is the index of the first element to the right smaller or equal to `nums[i]`. This ensures that for any subarray within $(prev[i], next[i])$ containing $i$, `nums[i]` is the minimum, and we count each subarray's minimum exactly once (handling duplicates by associating them with the leftmost occurrence).
    *   For maximums: Similar logic but with strict inequality on the left and non-strict on the right (or vice versa depending on implementation, here: left strictly larger, right larger or equal).
2.  **Counting Valid Subarrays**:
    *   For each $i$, the valid start indices are $[L, i]$ and valid end indices are $[i, R]$.
    *   Let $a = i - \text{start}$ and $b = \text{end} - i$. We need $0 \le a \le \text{max\_a}$, $0 \le b \le \text{max\_b}$, and $a + b \le k - 1$.
    *   The number of such pairs $(a, b)$ is calculated using combinatorial logic (summing an arithmetic progression) to handle the constraint $a+b \le k-1$ efficiently in $O(1)$.
3.  **Complexity**:
    *   Time: $O(N)$ because each element is pushed and popped from the stack at most once, and the counting logic is $O(1)$.
    *   Space: $O(N)$ for the stacks and boundary arrays.
This meets the constraints ($N \le 80,000$) efficiently.

## worker: Run the solution against the provided examples to 
The solution implements the "contribution technique" combined with monotonic stacks to determine the range $[L, R]$ for each element where it acts as the minimum (or maximum) of a subarray.
1.  **Boundaries**:
    *   For minimums: `prev[i]` is the index of the first element to the left strictly smaller than `nums[i]`. `next[i]` is the index of the first element to the right smaller or equal to `nums[i]`. This handles duplicates correctly by associating the minimum with the leftmost occurrence.
    *   For maximums: `prev[i]` is the index of the first element to the left strictly larger than `nums[i]`. `next[i]` is the index of the first element to the right larger or equal to `nums[i]`.
2.  **Counting**:
    *   For each element `nums[i]`, valid subarrays start in $[L, i]$ and end in $[i, R]$.
    *   Let $a = i - \text{start}$ and $b = \text{end} - i$. The condition is $a + b \le k - 1$.
    *   We count pairs $(a, b)$ satisfying $0 \le a \le i-L$, $0 \le b \le R-i$, and $a+b \le k-1$ using arithmetic series summation in $O(1)$.
3.  **Complexity**:
    *   Time: $O(N)$ due to single passes for stack operations and the final loop.
    *   Space: $O(N)$ for storing boundaries and stacks.
This approach efficiently handles the constraints ($N \le 80,000$) and edge cases like duplicates and varying window sizes.

## worker: finalize
The solution implements the "contribution technique" combined with monotonic stacks to determine the range $[L, R]$ for each element where it acts as the minimum (or maximum) of a subarray.
1.  **Boundaries**:
    *   For minimums: `prev[i]` is the index of the first element to the left strictly smaller than `nums[i]`. `next[i]` is the index of the first element to the right smaller or equal to `nums[i]`. This handles duplicates correctly by associating the minimum with the leftmost occurrence.
    *   For maximums: `prev[i]` is the index of the first element to the left strictly larger than `nums[i]`. `next[i]` is the index of the first element to the right larger or equal to `nums[i]`.
2.  **Counting**:
    *   For each element `nums[i]`, valid subarrays start in $[L, i]$ and end in $[i, R]$.
    *   Let $a = i - \text{start}$ and $b = \text{end} - i$. The condition is $a + b \le k - 1$.
    *   We count pairs $(a, b)$ satisfying $0 \le a \le i-L$, $0 \le b \le R-i$, and $a+b \le k-1$ using arithmetic series summation in $O(1)$.
3.  **Complexity**:
    *   Time: $O(N)$ due to single passes for stack operations and the final loop.
    *   Space: $O(N)$ for storing boundaries and stacks.
This approach efficiently handles the constraints ($N \le 80,000$) and edge cases like duplicates and varying window sizes.
