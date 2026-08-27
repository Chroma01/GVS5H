The problem asks for the minimum number of adjacent swaps to make all 1s contiguous. Let the positions of the 1s in the string be `p[0] < p[1] < ... < p[k-1]` where `k` is the total number of 1s. The optimal final configuration is to place the block of `k` ones starting at some position `start`. The cost to gather them starting at `start` is:
`cost(start) = sum_{i=0}^{k-1} |p[i] - (start + i)|`
This is a classic problem solvable by computing the median of the transformed values `q[i] = p[i] - i`. The optimal `start` is the median of `q`, and the minimal cost is `sum |q[i] - median(q)|`.

**Algorithm Steps:**
1. Read `N` and the string `S`.
2. Collect indices `i` (0-based) where `S[i] == '1'` into a list `p`.
3. Transform to `q[i] = p[i] - i` for each 1.
4. Find the median of `q`.
5. Compute the sum of absolute differences from the median.
6. Output the sum.

This is `O(N)` time and memory.