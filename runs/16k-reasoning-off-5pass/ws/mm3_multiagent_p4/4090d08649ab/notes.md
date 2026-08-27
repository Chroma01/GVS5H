
## ideation
The problem asks for the sum over all subarrays of the minimum number of operations to erase all elements, where each operation deletes all occurrences of a contiguous range of integer values `[l, r]`. This minimum number is exactly the number of maximal contiguous segments of distinct values in the subarray. Let this be `f(L,R)`. Equivalently, `f(L,R) = distinct(L,R) - adj(L,R)`, where `distinct` is the number of distinct values and `adj` is the number of adjacent value pairs (v, v+1) both present.

We can compute the sum of `distinct(L,R)` over all subarrays in O(N) using the standard "previous occurrence" trick: `sum_{i=1}^N (i - prev_occ[i])`. This is a well-known result.

The main challenge is computing `sum_{L,R} adj(L,R)`. Using divide and conquer (D&C) on the array index range, we can handle crossing subarrays `[L, R]` with `L <= mid < R`. The formula `f(L,R) = f(L,mid) + f(mid+1,R) - overlap(L,R)` holds, where `overlap` is the size of the intersection of value sets plus the number of edges crossing between the left and right parts. Because the left and right windows are independent given the split, the sum of `overlap(L,R)` over all crossing pairs factors into a product of counts for each value. Specifically, for each value `v`, we need:
- `left_cnt[v]`: number of `L` in `[l, mid]` where `v` appears in `A[L..mid]`.
- `right_cnt[v]`: number of `R` in `[mid+1, r]` where `v` appears in `A[mid+1..R]`.

Then the crossing overlap sum is `sum_v left_cnt[v] * (right_cnt[v] + right_cnt[v-1] + right_cnt[v+1])`. We can compute `left_cnt` by scanning leftwards from `mid` and maintaining a frequency array of values seen so far, recording for each newly added value `v` the current count of left windows that contain `v`. Doing this for all `L` yields `left_cnt` in O(length) time. Similarly for `right_cnt` scanning rightwards. The D&C processes O(N log N) total elements.

Total complexity: O(N log N) time and O(N) space, suitable for N up to 3e5.

## worker: Implement the divide-and-conquer solution in Pytho
- The D&C recurrence: `sum_adj(l, r) = sum_adj(l, mid) + sum_adj(mid+1, r) + crossing_adj(l, mid, r)`.
- `crossing_adj` counts the number of adjacencies `(v, v+1)` split across the two halves. Because left and right windows are independent given the split, the total crossing count factors as a product of per-value counts on each side.
- `left_cnt[v]` = number of `L` in `[l, mid]` such that `v` appears in `A[L..mid]`. This equals `p - l + 1` where `p` is the last occurrence of `v` in `[l, mid]`, or 0 if none.
- `right_cnt[v]` = number of `R` in `[mid+1, r]` such that `v` appears in `A[mid+1..R]`. This equals `r - q + 1` where `q` is the first occurrence of `v` in `[mid+1, r]`, or 0 if none.
- These counts are computed in `O(length)` per segment, giving `O(N log N)` total.
- The final answer is `sum_distinct - sum_adj` because `f(L,R) = distinct(L,R) - adj(L,R)`.

## worker: Test the current solution on the provided sample i
The solution uses a divide-and-conquer approach. The key insight is that `f(L,R) = distinct(L,R) - adj(L,R)`, where `adj` counts pairs of adjacent integers both present in the subarray. The sum of `distinct` is computed in O(N) using the previous-occurrence trick. The sum of `adj` is computed via D&C: for each segment, the crossing contribution factors into independent left and right counts per value, allowing O(length) computation per segment. Total complexity is O(N log N) time and O(N) space, which fits the constraints.

## worker: Run the provided solution on the three sample inpu
The solution is based on the formula `f(L,R) = distinct(L,R) - adj(L,R)`, where `adj(L,R)` counts pairs of adjacent integers both present. The sum of `distinct` is computed in O(N) using the previous-occurrence trick. The sum of `adj` is computed using divide and conquer: crossing subarrays are handled by factoring the contribution per value into independent left and right counts. The provided code correctly implements this approach and was tested on the sample inputs, producing the expected outputs: 16, 23, and 129. The algorithm runs in O(N log N) time and O(N) space, which is efficient for N up to 3e5.
