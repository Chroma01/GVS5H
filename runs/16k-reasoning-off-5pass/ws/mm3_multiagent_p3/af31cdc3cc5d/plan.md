We need to maximize the sum of absolute differences of pairs that we remove when repeatedly removing adjacent pairs until at most one element remains. This is equivalent to partitioning the sequence into ⌊N/2⌋ disjoint pairs (with possibly one leftover element if N is odd) such that each pair's elements are adjacent in the current sequence at removal time, and sum of |a−b| is maximized.

Key observation: The order in which pairs are removed does not change the final pairing structure; the final outcome is a perfect matching of elements (ignoring one leftover if N odd) where matched elements were adjacent at some step. It is known that the set of achievable matchings is exactly all ways to pair elements such that between any two matched pairs, the pairs' intervals are either nested or disjoint (i.e., the matching is a "non-crossing" matching when viewed with the original indices). However, the operation allows any pair of currently adjacent elements, which after removals can make previously non‑adjacent indices become adjacent. This actually allows us to realize ANY perfect matching (or near‑perfect) on the original indices, because we can always remove pairs in an order consistent with the matching: if pair (i,j) with i<j and another pair (k,l) with k<l, we can remove (i,j) first, then elements between them are gone, making (k,l) adjacent. The only restriction is that pairs must be disjoint in indices; they cannot share elements. And if N is odd, one element is left unpaired.

Thus the problem reduces to: given N numbers, pair up ⌊N/2⌋ disjoint pairs of indices to maximize sum of |A_i − A_j| (if N odd, one element is discarded). This is just a maximum-weight matching on a complete graph which is too large, but because weight depends only on absolute difference, we can sort values and observe that pairing the largest with smallest, second largest with second smallest, etc., maximizes total sum of absolute differences (a classic result). For odd N, the middle element is left out.

Proof sketch: Sort the array. Consider any optimal matching. If two pairs are not of the form (largest, smallest) style, we can swap to increase or keep sum. The sum of |A_{sorted} - B_{sorted}| is maximized when one list is reversed. Since we pair elements from the same multiset, the maximum sum is achieved by pairing smallest with largest, second smallest with second largest, etc.

So algorithm:
- If N is even: sort A, sum |A[i] - A[N-1-i]| for i = 0..N/2-1.
- If N is odd: sort A, sum |A[i] - A[N-1-i]| for i = 0..(N-1)/2-1 (i.e., N//2 pairs), leaving the middle element unpaired.

This is O(N log N), which fits N up to 3e5.

Let's verify with samples:
Sample1: [1,2,5,3] sorted [1,2,3,5]; pairs: |1-5|+|2-3|=4+1=5 ✔
Sample2: [3,1,4,1,5,9,2] sorted [1,1,2,3,4,5,9]; pairs: |1-9|+|1-5|+|2-4|=8+4+2=14 ✔
Sample3: all 1s -> 0 ✔

Now we produce the solution code.