
## ideation
The core difficulty is optimizing over two cuts while the middle segment’s distinct-count value changes nonlocally when the right endpoint moves. For a fixed right cut \(j\), every possible first cut \(i<j\) has a score consisting of the prefix contribution plus the number of values appearing between \(i+1\) and \(j\). When \(A_j\) is appended, its contribution increases precisely for cuts lying after the previous occurrence of \(A_j\). Thus each step produces a suffix/range increment over the set of candidate first cuts, followed by a maximum query. Care is needed when the previous occurrence does not exist and when introducing the newly available cut \(i=j-1\).

## worker: Implement and verify the lazy segment-tree sweep: 
For a fixed second cut `j`, each first cut `i < j` has value:

`distinct(A[1..i]) + distinct(A[i+1..j])`.

When `A[j]` is appended, its distinct count increases exactly for `i` from its previous occurrence position through `j-2`; if it has not appeared before, this starts at `1`. This is handled by a segment-tree range addition.

The newly available first cut `i = j-1` is activated with value `prefixDistinct[i] + 1`, since its middle segment contains only `A[j]`. The segment tree stores the maximum over all active first cuts, and adding `suffixDistinct[j+1]` evaluates the third segment.

The complexity is `O(N log N)` time and `O(N)` memory.

## worker: Fix the sweep by initializing `last` with the occu
The crucial correction is initializing `last[a[0]] = 1`. At the beginning of iteration `j`, `last[x]` must be the latest occurrence of `x` among positions `1..j-1`; otherwise an occurrence at position 1 is incorrectly treated as nonexistent.

When appending `A[j]`, the middle segment for a first cut `i` is `A[i+1..j]`. Its distinct count increases exactly when `i >= previous`, where `previous` is the previous occurrence position of `A[j]`. Therefore the segment tree receives a range addition on `[max(1, previous), j-2]`. The newly available cut `i=j-1` is then assigned `prefix[i] + 1`.

This handles repeated values whose previous occurrence lies before the active sweep, including arrays of all equal values and patterns such as `1 2 1 2`.
