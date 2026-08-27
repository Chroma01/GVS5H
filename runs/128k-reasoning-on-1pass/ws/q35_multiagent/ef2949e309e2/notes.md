
## ideation
The problem requires counting subsequences of length 5 where the middle element is the unique mode. This translates to selecting 2 elements from the left of the middle index and 2 from the right, such that the middle value `v` appears more frequently than any other value in the selected 4 elements.
The condition simplifies to:
1. Count of `v` in the 4 elements ($k$) must be $\ge 1$.
2. If $k=1$, the other 3 elements must be distinct.
3. If $k \ge 2$, the non-`v` elements must not have frequency $\ge 2$ (i.e., they must be distinct).

We can classify pairs from the left and right into 4 types based on their composition relative to `v`:
- Type 0: Two distinct non-`v` elements.
- Type 1: One `v`, one non-`v`.
- Type 2: Two `v`'s.
- Type 3: Two identical non-`v` elements.

By iterating through each possible middle index $i$, we can compute the number of valid pairs of each type from the left and right partitions. The valid combinations of left and right pairs are those that satisfy the unique mode condition. Given the constraint $N \le 1000$, an $O(N^2)$ approach is feasible and avoids complex dynamic updates. We will rebuild frequency maps for each $i$ and compute the answer in $O(N)$ per iteration, resulting in $O(N^2)$ total time complexity.

## worker: finalize
The solution iterates through each possible middle index `i` (from 2 to `n-3`). For each `i`, it considers `nums[i]` as the middle element `v` of the subsequence. It partitions the remaining elements into left (`L`) and right (`R`) sets.
Pairs from `L` and `R` are classified into 4 types based on their composition relative to `v`:
- Type 0: Two distinct non-`v` elements.
- Type 1: One `v`, one non-`v`.
- Type 2: Two `v`'s.
- Type 3: Two identical non-`v` elements.

Counts for each type are computed in $O(N)$ time using frequency maps. The valid combinations are:
1. $k \ge 2$ (where $k$ is the count of `v` in the 4 chosen elements): All combinations of types that yield $k \ge 2$ are valid. This is computed in $O(1)$ using precomputed counts.
2. $k = 1$: The 3 non-`v` elements must be distinct. This requires checking value overlaps, handled by iterating over distinct values in `L` and `R` and subtracting invalid pairs. This takes $O(N)$ per middle index.

Total time complexity is $O(N^2)$, which fits well within the constraint $N \le 1000$. Space complexity is $O(N)$ for frequency maps.
