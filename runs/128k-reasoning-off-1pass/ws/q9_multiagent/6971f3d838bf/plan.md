The problem requires maximizing the subarray sum after optionally removing all occurrences of a single number $x$. Since the array length is up to $10^5$, an $O(N^2)$ solution is too slow. We can iterate through each unique number in the array as a candidate for removal. For each candidate, we need to efficiently calculate the maximum subarray sum of the resulting array. Instead of physically removing elements (which is costly), we can simulate the removal by skipping those elements during a Kadane's algorithm pass. To optimize, we can precompute prefix sums and the maximum subarray sum ending at each index, then for a specific removal, the new maximum subarray sum is the maximum of: (1) a subarray entirely before the removed elements, (2) a subarray entirely after, or (3) a subarray crossing the gap formed by removal. However, a simpler and robust approach given the constraints is to iterate over unique elements, and for each, run a modified Kadane's algorithm in $O(N)$ time, resulting in $O(N \cdot U)$ where $U$ is the number of unique elements. In the worst case $U=N$, making it $O(N^2)$, which might TLE. 

Wait, let's re-evaluate the complexity. If we have many unique elements, $O(N^2)$ is bad. Is there an $O(N)$ or $O(N \log N)$ approach?
Actually, the operation is "remove all occurrences of $x$". This splits the array into contiguous segments of the original array. The new maximum subarray sum will be the maximum subarray sum within any of these segments.
Let the original array be split by removing $x$ into segments $S_1, S_2, \dots, S_k$. The answer for a specific $x$ is $\max(\text{max\_subarray}(S_1), \text{max\_subarray}(S_2), \dots)$.
Notice that if we don't remove anything, the answer is the global max subarray sum.
If we remove $x$, we are essentially taking the global max subarray sum and potentially breaking it if it contained $x$. If the global max subarray sum did not contain $x$, the answer remains the same. If it did contain $x$, the new max subarray sum will be the maximum of the parts of that specific subarray that remain, or some other subarray that didn't contain $x$.
Actually, the optimal strategy is:
1. Calculate the global maximum subarray sum (`global_max`).
2. Identify the maximum subarray sum that *does not* contain any specific element $x$.
This looks like we need to find, for each $x$, the max subarray sum excluding $x$.
We can compute the max subarray sum for the whole array. If the optimal subarray doesn't contain $x$, then removing $x$ doesn't hurt the max sum.
If the optimal subarray *does* contain $x$, then removing $x$ breaks it. The new max sum would be the max of the left part (before $x$'s occurrences) and the right part (after $x$'s occurrences).
But there might be another subarray that doesn't contain $x$ which is larger than the broken optimal one.
So, for each unique $x$, we want $\max(\text{max subarray in } nums \setminus \{x\})$.
This is equivalent to: $\max(\text{global max subarray sum}, \text{max subarray sum avoiding } x)$.
Actually, the "global max" is just one case (removing nothing). The problem says "at most once". So we compare `global_max` vs `max_subarray_sum_after_removing_x` for all $x$.
Since $N$ is $10^5$, we cannot afford $O(N^2)$.
Is it possible that the number of unique elements is small? No, constraints say values up to $10^6$.
Let's reconsider the structure.
The max subarray sum avoiding $x$ is the maximum of:
- Max subarray sum in the prefix before the first occurrence of $x$.
- Max subarray sum in the suffix after the last occurrence of $x$.
- Max subarray sum in any segment between two consecutive occurrences of $x$.
This still feels like it requires processing segments.
However, note that if we remove $x$, the array becomes a concatenation of segments of the original array. The max subarray sum of the new array is simply the maximum of the max subarray sums of these individual segments.
Let's precompute the max subarray sum for every possible contiguous segment? No, too many.
Alternative idea:
The answer is $\max($ `global_max`, $\max_{x} (\text{max subarray sum avoiding } x)$ $)$.
Actually, if `global_max` subarray does not contain $x$, then `max subarray sum avoiding x` is at least `global_max`.
If `global_max` subarray contains $x$, then `max subarray sum avoiding x` is the max of the subarrays formed by removing $x$ from that specific subarray, OR some other subarray that didn't contain $x$.
Wait, if there exists ANY subarray that doesn't contain $x$ with sum $S$, then the answer for removing $x$ is at least $S$.
So for a fixed $x$, we want the maximum subarray sum that does not include $x$.
This is a classic problem: "Maximum subarray sum excluding a specific element".
Can we solve this for all $x$ efficiently?
We can compute the max subarray sum for the entire array. Let this be $M$.
If the optimal subarray for $M$ does not contain $x$, then the answer for $x$ is $M$.
If the optimal subarray for $M$ contains $x$, then we need the next best subarray that avoids $x$.
Actually, the set of candidates for the "max subarray avoiding $x$" includes:
1. The max subarray sum of the array restricted to indices $[0, i-1]$ for all $i$ where $nums[i] == x$.
2. The max subarray sum of the array restricted to indices $[i+1, N-1]$ for all $i$ where $nums[i] == x$.
3. The max subarray sum of the array restricted to indices between two occurrences of $x$.
This seems complicated to aggregate.

Let's flip the perspective.
For each unique $x$, we want to find the max subarray sum in $nums$ without $x$.
Let's compute the max subarray sum for the whole array. If we remove $x$, we break the array into pieces.
The max subarray sum of the new array is $\max(\text{max subarray of piece}_1, \text{max subarray of piece}_2, \dots)$.
We can precompute:
- `left_max[i]`: max subarray sum in `nums[0...i]`
- `right_max[i]`: max subarray sum in `nums[i...N-1]`
But this doesn't handle the "between occurrences" case easily because the pieces are not just prefixes/suffixes.
However, notice that if we remove $x$, the resulting array is just the original array with $x$'s removed.
The max subarray sum of the new array is the maximum of the max subarray sums of the contiguous blocks of non-$x$ elements.
Let's denote the blocks of non-$x$ elements as $B_1, B_2, \dots, B_k$.
We need $\max_j (\text{max\_subarray}(B_j))$.
Since $B_j$ are contiguous subarrays of the original `nums`, we can precompute the max subarray sum for *all* contiguous subarrays? No, $O(N^2)$.
But we only care about the max subarray sum of the *entire* array, and how it changes when $x$ is removed.
Actually, the maximum subarray sum avoiding $x$ is simply the maximum of:
- The max subarray sum of the prefix ending before the first $x$.
- The max subarray sum of the suffix starting after the last $x$.
- The max subarray sum of any segment between two $x$'s.
Wait, if a segment between two $x$'s has a large positive sum, it will be captured.
Is it possible to compute this in $O(N)$ total?
Consider the global max subarray sum. Let the indices of the global max subarray be $[L, R]$.
If $x$ is not in $[L, R]$, then removing $x$ doesn't affect this subarray, so the answer is the global max.
If $x$ is in $[L, R]$, then this specific subarray is broken. The new max sum could be:
1. A subarray entirely within $[L, \text{first } x]$.
2. A subarray entirely within $[\text{last } x, R]$.
3. A subarray entirely outside $[L, R]$.
4. A subarray inside a gap between two $x$'s that is not covered by $[L, R]$.
This suggests we need to know the max subarray sum for every possible "gap" created by removing $x$.
But notice that the "gaps" are just contiguous subarrays of the original array that do not contain $x$.
So for a fixed $x$, we want $\max \{ \text{max\_subarray}(S) \mid S \subseteq nums, x \notin S \}$.
This is equivalent to finding the max subarray sum in the array where we treat $x$ as $-\infty$ (so it can never be part of a subarray).
We can solve this for all $x$ using a segment tree or similar structure?
Or simpler:
The answer is $\max($ `global_max`, $\max_{x} (\text{max subarray sum avoiding } x)$ $)$.
Actually, we can compute `max_subarray_avoiding_x` for all $x$ by iterating.
But we need to do it faster than $O(N^2)$.
Let's observe: The max subarray sum avoiding $x$ is the maximum of:
- `max_subarray(nums[0...i-1])` for all $i$ such that $nums[i] == x$.
- `max_subarray(nums[i+1...N-1])` for all $i$ such that $nums[i] == x$.
- `max_subarray(nums[j...k])` where $nums[j] \neq x, \dots, nums[k] \neq x$ and there is an $x$ before $j$ and an $x$ after $k$.
This third case is tricky.
However, note that if we remove $x$, the array is split into segments. The max subarray sum of the new array is the max of the max subarray sums of these segments.
The segments are:
1. `nums[0...first_x-1]`
2. `nums[first_x+1...second_x-1]`
3. ...
4. `nums[last_x+1...N-1]`
We can precompute the max subarray sum for every prefix and every suffix.
Let `pref_max[i]` be the max subarray sum in `nums[0...i]`.
Let `suff_max[i]` be the max subarray sum in `nums[i...N-1]`.
For a specific $x$, let its occurrences be at indices $idx_1, idx_2, \dots, idx_k$.
The segments are:
- `nums[0...idx_1-1]`: max subarray sum is `pref_max[idx_1-1]`.
- `nums[idx_j+1...idx_{j+1}-1]`: This is a subarray. We need the max subarray sum of this specific range.
- `nums[idx_k+1...N-1]`: max subarray sum is `suff_max[idx_k+1]`.
The problem is the middle segments.
But wait, if the global max subarray sum is $M$, and it does not contain $x$, then the answer is $M$.
If it contains $x$, then the answer is $\max($ max subarray in `nums[0...first_x-1]`, max subarray in `nums[last_x+1...N-1]`, max subarray in any gap between $x$'s $)$.
The max subarray in a gap `nums[a...b]` is a subarray of `nums`.
Is it possible that the max subarray in a gap is larger than the global max? No, because the global max is the max over ALL subarrays. So the max subarray in any gap is $\le$ global max.
Therefore, if the global max subarray does NOT contain $x$, the answer is `global_max`.
If the global max subarray DOES contain $x$, then the answer is $\max($ `pref_max[first_x-1]`, `suff_max[last_x+1]`, $\max_{j} (\text{max subarray in } nums[idx_j+1...idx_{j+1}-1])$ $)$.
Wait, if the global max subarray contains $x$, it means the global max subarray is "broken" by $x$. The new max sum will be the maximum of the pieces of the global max subarray (left of $x$, right of $x$) OR some other subarray that doesn't contain $x$.
But any subarray that doesn't contain $x$ is a subarray of one of the segments defined by removing $x$.
So the answer for removing $x$ is $\max($ `pref_max[first_x-1]`, `suff_max[last_x+1]`, $\max_{j} (\text{max subarray sum of } nums[idx_j+1...idx_{j+1}-1])$ $)$.
We need to efficiently query the max subarray sum of any subarray `nums[a...b]`.
This is a range query problem. We can use a Segment Tree to store the max subarray sum for any range. Each node in the segment tree stores: `sum`, `max_prefix`, `max_suffix`, `max_subarray`.
Building the tree takes $O(N)$. Querying takes $O(\log N)$.
Then for each unique $x$, we find its occurrences, query the relevant ranges, and take the max.
Total complexity: $O(N \log N)$ to build tree + $O(U \cdot \log N)$ to query, where $U$ is number of unique elements. Since $U \le N$, this is $O(N \log N)$.
This fits within the time limit.

Steps:
1. Build a Segment Tree over `nums` where each node stores `max_subarray`, `max_prefix`, `max_suffix`, and `total_sum`.
2. Find all unique elements and their indices.
3. Initialize `ans` with the global max subarray sum (root of segment tree).
4. For each unique element $x$:
   - Get all indices where $x$ occurs.
   - If no occurrences, skip (or handle as "remove nothing" which is already covered by initial `ans`).
   - Identify the segments formed by removing $x$:
     - Segment 1: `0` to `first_index - 1`. Query max subarray.
     - Segment 2: `last_index + 1` to `N - 1`. Query max subarray.
     - Segments between consecutive occurrences: `idx_j + 1` to `idx_{j+1} - 1`. Query max subarray.
   - Update `ans` with the maximum of these queries.
5. Return `ans`.

Edge cases:
- Array with all same elements: removing one leaves empty? Problem says "nums remains non-empty". If removing $x$ makes it empty, we cannot choose that $x$. But we can choose NOT to remove anything. So we just ignore $x$ if it's the only element.
- If after removal, the array is empty, that option is invalid. But we always have the option of doing nothing, so the answer is at least the global max.

Implementation details:
- Segment Tree class.
- Merge function.
- Coordinate compression or direct mapping for indices? Just store lists of indices for each unique number.
- Handle ranges carefully (if start > end, ignore).

```python
class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0: return 0
        
        # Segment Tree Node
        class Node:
            def __init__(self, l, r):
                self.l, self.r = l, r
                self.max_sub = -float('inf')
                self.max_pref = -float('inf')
                self.max_suff = -float('inf')
                self.total = 0
        
        # Build tree
        # We can use an array based tree for efficiency
        size = 1
        while size < n:
            size *= 2
        tree = [None] * (2 * size)
        
        def build(node, start, end):
            if start == end:
                val = nums[start]
                tree[node] = Node(start, end)
                tree[node].max_sub = val
                tree[node].max_pref = val
                tree[node].max_suff = val
                tree[node].total = val
                return
            mid = (start + end) // 2
            left_node = 2 * node
            right_node = 2 * node + 1
            build(left_node, start, mid)
            build(right_node, mid + 1, end)
            
            left = tree[left_node]
            right = tree[right_node]
            tree[node] = Node(start, end)
            tree[node].total = left.total + right.total
            tree[node].max_pref = max(left.max_pref, left.total + right.max_pref)
            tree[node].max_suff = max(right.max_suff, right.total + left.max_suff)
            tree[node].max_sub = max(left.max_sub, right.max_sub, left.max_suff + right.max_pref)
        
        build(1, 0, size - 1)
        
        def query(node, l, r):
            if r < node.l or l > node.r:
                return None
            if l <= node.l and node.r <= r:
                return tree[node]
            mid = (node.l + node.r) // 2
            left_res = query(2 * node, l, r)
            right_res = query(2 * node + 1, l, r)
            if left_res is None: return right_res
            if right_res is None: return left_res
            res = Node(0, 0)
            res.total = left_res.total + right_res.total
            res.max_pref = max(left_res.max_pref, left_res.total + right_res.max_pref)
            res.max_suff = max(right_res.max_suff, right_res.total + left_res.max_suff)
            res.max_sub = max(left_res.max_sub, right_res.max_sub, left_res.max_suff + right_res.max_pref)
            return res

        # Group indices by value
        from collections import defaultdict
        indices_map = defaultdict(list)
        for i, x in enumerate(nums):
            indices_map[x].append(i)
        
        unique_elements = list(indices_map.keys())
        
        # Initial answer: global max subarray sum
        global_max = tree[1].max_sub
        ans = global_max
        
        for x in unique_elements:
            idxs = indices_map[x]
            # If removing x makes array empty, skip (but we have 'do nothing' option)
            # Actually, if len(nums) == 1 and we remove it, array is empty -> invalid.
            # But we can always choose not to remove.
            
            current_max = -float('inf')
            
            # Segments:
            # 1. Before first occurrence
            if idxs[0] > 0:
                res = query(1, 0, idxs[0] - 1)
                if res:
                    current_max = max(current_max, res.max_sub)
            
            # 2. After last occurrence
            if idxs[-1] < n - 1:
                res = query(1, idxs[-1] + 1, n - 1)
                if res:
                    current_max = max(current_max, res.max_sub)
            
            # 3. Between occurrences
            for k in range(len(idxs) - 1):
                start = idxs[k] + 1
                end = idxs[k+1] - 1
                if start <= end:
                    res = query(1, start, end)
                    if res:
                        current_max = max(current_max, res.max_sub)
            
            if current_max > ans:
                ans = current_max
        
        return ans
```

Wait, the constraints say $1 \le nums.length$. If $nums = [-3]$, removing -3 leaves empty. We must not choose that. But we can choose not to remove. So `ans` initialized to global max is correct.
One detail: `query` returns `None` if range is invalid. Handled.
The segment tree size logic: `size` is power of 2 >= n. Indices $0$ to $size-1$. If $n < size$, the extra leaves are $-\infty$?
In `build`, if `start == end`, we use `nums[start]`. If `start >= n`, `nums[start]` would be out of bounds.
We should handle the padding.
Initialize the tree with $-\infty$ for indices $\ge n$.
Modified `build`:
If `start >= n`:
  `tree[node].max_sub = -inf`
  `tree[node].max_pref = -inf`
  `tree[node].max_suff = -inf`
  `tree[node].total = 0` (or -inf? Sum of empty is 0, but max subarray of empty is -inf. Let's use -inf for max subarray, 0 for total sum of empty range? No, total sum of empty range is 0. But max_pref/suff should be -inf because you can't pick a non-empty subarray from empty.
Actually, standard Kadane's on empty array is undefined or -inf.
Let's set `total = 0`, `max_sub = -inf`, `max_pref = -inf`, `max_suff = -inf`.
Then merging:
`total = left.total + right.total` (0 + 0 = 0)
`max_pref = max(left.max_pref, left.total + right.max_pref)` -> `max(-inf, 0 + -inf) = -inf`. Correct.
`max_sub = max(left.max_sub, right.max_sub, left.max_suff + right.max_pref)` -> `-inf`. Correct.
So padding with empty nodes works.

Refined plan for code:
1. Determine `size` = power of 2 >= n.
2. Initialize `tree` array of size `2*size`.
3. Fill leaves $0$ to $n-1$ with actual values. Leaves $n$ to $size-1$ with empty node properties.
4. Build tree bottom-up.
5. Proceed with logic.

Double check constraints: $N=10^5$, values $\pm 10^6$. Sums can exceed $2^{31}-1$, so use 64-bit integers (Python handles this automatically).
Time complexity: $O(N \log N)$ due to segment tree build and queries.
Space complexity: $O(N)$.

```python
class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0: return 0
        
        # Determine size for segment tree
        size = 1
        while size < n:
            size *= 2
        
        # Initialize tree with -inf for max_sub/pref/suff and 0 for total
        # Using a large negative number for -inf
        NEG_INF = -10**18 
        tree = [None] * (2 * size)
        
        # Helper to create a node
        def create_node(l, r, val):
            return {'l': l, 'r': r, 'max_sub': val, 'max_pref': val, 'max_suff': val, 'total': val}
        
        # Initialize leaves
        for i in range(n):
            tree[size + i] = create_node(i, i, nums[i])
        for i in range(n, size):
            tree[size + i] = create_node(i, i, NEG_INF)
            
        # Build tree
        for i in range(size - 1, 0, -1):
            left = tree[2 * i]
            right = tree[2 * i + 1]
            node = create_node(left['l'], right['r'], NEG_INF)
            node['total'] = left['total'] + right['total']
            node['max_pref'] = max(left['max_pref'], left['total'] + right['max_pref'])
            node['max_suff'] = max(right['max_suff'], right['total'] + left['max_suff'])
            node['max_sub'] = max(left['max_sub'], right['max_sub'], left['max_suff'] + right['max_pref'])
            tree[i] = node
            
        def query(node_idx, l, r):
            if l > r:
                return None
            if l <= tree[node_idx]['l'] and tree[node_idx]['r'] <= r:
                return tree[node_idx]
            mid = (tree[node_idx]['l'] + tree[node_idx]['r']) // 2
            left_res = query(2 * node_idx, l, r) if l <= mid else None
            right_res = query(2 * node_idx + 1, l, r) if r > mid else None
            
            if left_res is None: return right_res
            if right_res is None: return left_res
            
            # Merge results
            res = create_node(0, 0, NEG_INF)
            res['total'] = left_res['total'] + right_res['total']
            res['max_pref'] = max(left_res['max_pref'], left_res['total'] + right_res['max_pref'])
            res['max_suff'] = max(right_res['max_suff'], right_res['total'] + left_res['max_suff'])
            res['max_sub'] = max(left_res['max_sub'], right_res['max_sub'], left_res['max_suff'] + right_res['max_pref'])
            return res

        from collections import defaultdict
        indices_map = defaultdict(list)
        for i, x in enumerate(nums):
            indices_map[x].append(i)
            
        unique_elements = list(indices_map.keys())
        
        # Initial answer: global max subarray sum
        global_max = tree[1]['max_sub']
        ans = global_max
        
        for x in unique_elements:
            idxs = indices_map[x]
            current_max = NEG_INF
            
            # 1. Before first occurrence
            if idxs[0] > 0:
                res = query(1, 0, idxs[0] - 1)
                if res and res['max_sub'] > current_max:
                    current_max = res['max_sub']
            
            # 2. After last occurrence
            if idxs[-1] < n - 1:
                res = query(1, idxs[-1] + 1, n - 1)
                if res and res['max_sub'] > current_max:
                    current_max = res['max_sub']
            
            # 3. Between occurrences
            for k in range(len(idxs) - 1):
                start = idxs[k] + 1
                end = idxs[k+1] - 1
                if start <= end:
                    res = query(1, start, end)
                    if res and res['max_sub'] > current_max:
                        current_max = res['max_sub']
            
            if current_max > ans:
                ans = current_max
                
        return ans
```
One small fix: `query` logic for `mid` calculation. `tree[node_idx]['l']` and `['r']` are needed.
Also, the `query` function logic `if l <= mid` assumes `mid` is calculated correctly relative to the node's range.
Correct logic:
`mid = (tree[node_idx]['l'] + tree[node_idx]['r']) // 2`
Then check overlap.
The simplified `query` above tries to avoid recursion if no overlap, but the condition `if l <= mid` is heuristic. Better to stick to standard recursive overlap check.
Revised `query`:
```python
        def query(node_idx, l, r):
            if l > r:
                return None
            # Check overlap
            if r < tree[node_idx]['l'] or l > tree[node_idx]['r']:
                return None
            if l <= tree[node_idx]['l'] and tree[node_idx]['r'] <= r:
                return tree[node_idx]
            
            mid = (tree[node_idx]['l'] + tree[node_idx]['r']) // 2
            left_res = query(2 * node_idx, l, r)
            right_res = query(2 * node_idx + 1, l, r)
            
            if left_res is None: return right_res
            if right_res is None: return left_res