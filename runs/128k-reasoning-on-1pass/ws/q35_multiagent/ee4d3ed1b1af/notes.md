
## ideation
The problem requires finding the shortest substring in `s` that matches a pattern `p` with exactly two `*` wildcards. The pattern can be split into three literal parts `p1`, `p2`, `p3` separated by the wildcards. A match corresponds to indices `i` (start of `p1`), `j` (start of `p2`), and `k` (start of `p3`) in `s` such that `i + len(p1) <= j` and `j + len(p2) <= k`. The length of the matching substring is `k + len(p3) - i`.

To solve this efficiently:
1. Find all starting indices of `p1`, `p2`, and `p3` in `s`. Since `s` is up to 10^5, using Python's efficient `str.find` in a loop is acceptable and typically runs in near-linear time.
2. Store these indices in sorted lists `A`, `B`, and `C`.
3. Iterate through the middle part's occurrences (`B`). For each `j` in `B`, use binary search to find:
   - The largest `i` in `A` such that `i <= j - len(p1)`.
   - The smallest `k` in `C` such that `k >= j + len(p2)`.
   Update the minimum length `k + len(p3) - i`.
4. Handle edge cases where `p1`, `p2`, or `p3` are empty. If a part is empty, it effectively matches at any valid position, so we can directly assign the boundary indices instead of searching.
5. If `p2` is empty, the pattern reduces to `p1 * p3`, and we iterate through `C` instead, finding the best `i` for each `k`.
6. Time complexity is dominated by finding occurrences and binary searches, resulting in O(N log N) worst-case, which fits well within the constraints.

## worker: finalize
The pattern `p` is split into three literal parts `p1`, `p2`, `p3` separated by the two `*` wildcards. A valid match corresponds to indices `i`, `j`, `k` in `s` such that `p1` starts at `i`, `p2` starts at `j`, and `p3` starts at `k`, with `i + L1 <= j` and `j + L2 <= k`. The length of the matching substring is `k + L3 - i`.

We find all starting indices of each literal part in `s` using an efficient `find` loop. To minimize the substring length:
1. If `L2 > 0`, we iterate through each occurrence `j` of `p2`. For each `j`, we use binary search to find the largest valid `i` in `A` (or `i=j` if `L1=0`) and the smallest valid `k` in `C` (or `k=j+L2` if `L3=0`). We update the minimum length.
2. If `L2 == 0`, the middle wildcard matches empty string, effectively merging `p1` and `p3`. We iterate through `C` (if `L3>0`) and find the best `i`, or handle the trivial `L3=0` case directly.
3. Empty literal parts are handled logically by adjusting bounds instead of storing all indices, keeping space complexity optimal.
Time complexity is dominated by finding occurrences and binary searches: `O(N log N)` worst-case, which fits well within `10^5` constraints. Space complexity is `O(N)` to store occurrence lists.
