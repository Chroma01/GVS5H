
## ideation
The operation removes two adjacent numbers repeatedly until ≤1 element remains.  
Crucial observation: this is equivalent to choosing a set of disjoint pairs (and possibly one leftover if N is odd) to maximize the sum of |A_i − A_j|.  

Reason: any disjoint pairing can be realized by an appropriate removal order. After removing a pair (i, j), everything between them disappears, making other pairs adjacent. The only constraint is that pairs must be disjoint (no shared elements).  

Thus the problem becomes: pair up ⌊N/2⌋ elements to maximize total absolute difference.  

Classic result: sorting the array and pairing the smallest with the largest, second smallest with second largest, etc., gives the maximum possible sum. For odd N, the middle element is discarded.  

Proof sketch: Consider sorted values v1 ≤ v2 ≤ … ≤ vN. Any optimal matching can be transformed to this “extreme pairing” without decreasing total sum. (If two pairs are (a, b) and (c, d) with a < b and c < d, and a, b are not extremes relative to c, d, swapping to pair extremes increases or maintains the sum.)  

Therefore:
- If N even: answer = Σ_{i=0}^{N/2-1} |A_sorted[i] − A_sorted[N−1−i]|.
- If N odd: answer = Σ_{i=0}^{(N−1)/2} |A_sorted[i] − A_sorted[N−1−i]| (the middle element is automatically skipped).  

Complexities: O(N log N) time, O(N) memory for the sorted array. Fits N ≤ 3×10^5.

## worker: (none)
The problem asks to maximize the total score obtained by repeatedly removing adjacent pairs from the sequence. The crucial insight is that the set of achievable final pairings is exactly all possible disjoint pairings of the elements (with at most one leftover if N is odd), because any disjoint pairing can be realized by an appropriate order of removals: after removing a pair, the interval between them collapses, making the other pair adjacent.  

Thus the task reduces to selecting ⌊N/2⌋ disjoint pairs to maximize the sum of absolute differences. The classic solution is to sort the array and pair the smallest with the largest, the second smallest with the second largest, and so on. This yields the maximum possible sum, which can be shown by an exchange argument: if two pairs are not extreme, swapping to make them extreme does not decrease the total.  

The algorithm runs in O(N log N) time due to sorting and O(N) memory, well within the constraints (N ≤ 3·10⁵). Edge cases such as N odd and equal values are handled correctly.
