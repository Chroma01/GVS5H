
## ideation
The core difficulty is finding an ordered chain of occurrences of the three literal fragments around the two wildcards while minimizing the distance from the start of the first fragment to the end of the third. Empty fragments and wildcards at either end create zero-length matches, and a direct scan over every occurrence can become quadratic.

The main implementation concerns are:
- Correctly splitting the pattern into fragments, including empty fragments.
- Treating each wildcard as matching any number of characters, so the next fragment may begin immediately after—or overlap in position with—an empty preceding fragment.
- Choosing the earliest feasible later occurrence greedily for a fixed starting occurrence; this is valid because later choices cannot improve the ending position.
- Handling the all-wildcard case, where the answer is zero.
- Avoiding substring-search implementations that repeatedly rescan large portions of `s`, which can exceed the constraints.

## worker: Implement the KMP-based solution for `A*B*C`: spli
- Splits the pattern into `A*B*C`.
- Uses KMP to find every occurrence of each nonempty fragment in `s`.
- Uses `bisect_left` to select the earliest valid successor occurrence, which minimizes the ending position for each fixed starting occurrence.
- Handles empty fragments and all-wildcard patterns separately.
- Time complexity is `O(|s| + |p| + k log |s|)`, where `k` is the number of relevant occurrences; memory usage is `O(|s| + |p|)`.
