
## ideation
The core difficulty is that appending a value changes the alternating-sum contribution according to the current subsequence length parity, while the objective depends on the entire product and products can collapse information when a zero is selected. A correct method must distinguish empty from non-empty subsequences, preserve parity, enforce the product limit, and avoid treating product zero as an unreachable state. The alternating-sum range is manageable because each value is at most 12, but the requested `k` may lie far outside the attainable range.

## worker: Implement and validate a product-indexed DP: map e
The DP maps each attainable product to bitsets of alternating sums for even- and odd-length non-empty subsequences. Appending a value shifts the even-length bitset left by the value and the odd-length bitset right by the value, while multiplying the product. Snapshotting states before each number prevents reusing an element. Singleton states explicitly handle subsequences beginning with each value, including zero-product states.
