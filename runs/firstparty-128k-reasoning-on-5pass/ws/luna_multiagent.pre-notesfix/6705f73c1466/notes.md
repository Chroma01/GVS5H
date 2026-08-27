
## ideation
The core difficulty is recognizing that adjacent swaps measure the total distance that each `1` must move, while preserving the relative order of all `1`s. If the `1`s initially occur at positions \(p_i\), any final contiguous block must place them at consecutive positions \(x, x+1, \ldots\), so the cost for a chosen block start is the sum of their movement distances. The optimization must be done in linear time because \(N\) can be as large as \(5\times10^5\). Care is also needed with indexing and with 64-bit-sized costs.

## worker: Implement the adjusted-position median algorithm i
For the positions `p_i` of the `1`s, their relative order is preserved by adjacent swaps. If the final contiguous block starts at `x`, the `i`-th `1` must move to `x + i`, so the number of swaps is:

`sum(abs(p_i - (x + i)))`

Let `a_i = p_i - i`. Then this becomes `sum(abs(a_i - x))`, minimized by choosing `x` as a median of the adjusted positions. The algorithm computes these values and evaluates the cost at the median in `O(N)` time and `O(N)` memory.
