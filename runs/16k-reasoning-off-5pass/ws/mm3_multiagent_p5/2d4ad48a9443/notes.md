
## ideation
The problem asks for the number of subarrays that can be made non-decreasing using at most `k` increment operations (each operation increments one element by 1). The minimal cost for a subarray is the sum of positive differences between each element and the running maximum from the left (prefix max). We need to count subarrays where this sum ≤ `k`.

**Core difficulty**: Efficiently maintaining the cost of a sliding window under both right-extension and left-contraction. The cost is not simply additive when removing the leftmost element because the prefix max for the remaining elements may drop.

**Candidate approaches**:
1. **Two-pointer sliding window with a data structure to maintain cost**: Use a monotonic queue for the maximum, but updating cost on left removal is tricky.
2. **Segment of "record highs"**: Partition the window into segments where the prefix max is constant. Maintain sums and lengths. On left removal, the first segment's prefix max may change, requiring careful updates.
3. **Two-stack queue**: Maintain the window as a concatenation of two stacks, each storing elements with accumulated cost relative to the stack's local maximum. This allows O(1) amortized push/pop and total cost query.
4. **Divide and conquer**: Count subarrays crossing the midpoint by combining left and right halves with a known initial max. O(n log n) possible.
5. **Binary search on left for each right**: If we can compute the cost of any subarray in O(log n), we can binary search the smallest left for each right. But cost computation per subarray is non-trivial.
