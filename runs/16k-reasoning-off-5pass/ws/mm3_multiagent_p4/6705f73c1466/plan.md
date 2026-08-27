We have a string of 0s and 1s and we want to make all 1s contiguous using adjacent swaps. The total number of swaps needed to reorder the 1s to occupy some contiguous block of length K (the total number of 1s) is the minimum, over all possible target positions, of the sum of distances each 1 must move.

Let the positions (0‑indexed) of the 1s be `p[0] < p[1] < ... < p[K-1]`. If we decide that after reordering the 1s occupy indices `L, L+1, ..., L+K-1`, then the i‑th 1 (sorted by current order) must move to index `L + i`. The total swaps needed are

`sum_{i=0}^{K-1} |p[i] - (L + i)|`.

Because `p[i] >= i` and `L >= 0`, both sequences are increasing, so absolute values can be dropped:

`cost(L) = (sum p[i]) - K*L - K*(K-1)/2`.

`sum p[i]` is constant, and the term `-K*(K-1)/2` is constant, so we only need to minimise `-K*L`, i.e. maximise `L`. The largest feasible `L` is `N - K` (place the block of 1s at the right end of the string). Therefore the minimal number of swaps is

`answer = (sum of positions of 1s) - K*(N - K) - K*(K-1)/2`.

We can compute this in O(N) time and O(1) extra space, which is fast enough for N up to 5·10⁵.