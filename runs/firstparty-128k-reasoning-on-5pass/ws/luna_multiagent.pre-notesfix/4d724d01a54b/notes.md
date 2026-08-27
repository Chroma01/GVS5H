
## ideation
The core difficulty is proving that the cost can be decomposed by boundaries rather than by individual swaps. For every boundary between positions \(i\) and \(i+1\), the number of elements that must cross it is fixed by the initial permutation. Any valid sorting sequence pays at least this many times at cost \(i\), and a suitable adjacent-swap sorting order can attain all these lower bounds simultaneously. The main implementation task is therefore to answer many counts of elements in a prefix whose values exceed the boundary index. The total may be quadratic, so 64-bit arithmetic is necessary.

## worker: Derive and implement the boundary-count formula us
The minimum can be attained by inserting elements from left to right into the already sorted prefix. When the element initially at position `j` is inserted, let `c` be the number of smaller elements before it. It crosses exactly the boundaries `c+1, c+2, ..., j-1`, whose total cost is

\[
\sum_{i=c+1}^{j-1} i
= \frac{(j-1)j}{2}-\frac{c(c+1)}{2}.
\]

This insertion order is optimal because any adjacent-swap sorting sequence can be transformed using commuting swaps and the braid relation so that cheaper, leftward swaps are performed first; since boundary costs increase with the index, this never increases the total cost.

The inverse permutation gives the initial position of every value. A Fenwick tree stores positions of already processed smaller values, allowing `c` to be computed in `O(log N)`. Total complexity is `O(N log N)` and the answer uses Python integers.
