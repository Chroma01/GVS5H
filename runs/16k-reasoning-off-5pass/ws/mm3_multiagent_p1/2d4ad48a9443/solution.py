import sys
from typing import List

class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Build a segment tree where each node stores a "profile": a list of 
        # (value, count) pairs representing the running max structure for that segment,
        # assuming we start with target = -infinity (or 0 since values >= 1).
        # The profile is increasing in value.
        # To combine two profiles left and right:
        #   The right profile's values are lifted by left's final value.
        #   Then the two profiles are merged (similar to merging two monotonic stacks).
        
        # Since n <= 1e5, we can use an O(n log^2 n) approach: 
        # For each L, binary search the maximum R. 
        # To compute cost(L, R) in O(log^2 n), we use a segment tree that can answer
        # "given initial target T, what is the total cost to make [l..r] non-decreasing 
        # and what is the final target?".
        
        # Build a sparse table-like structure: for each node, store the profile.
        # But storing O(n) per node is too much. 
        # Instead, we use a segment tree where each node stores the profile 
        # of its segment assuming initial target = 0 (or any reference).
        # The profile is small: it has at most O(log n) elements? No, worst case O(n).
        # Example: decreasing array 5,4,3,2,1 has profile [(5,1),(4,1),(3,1),(2,1),(1,1)].
        # So profile size is O(segment length) in worst case.
        
        # This means building the tree naively is O(n^2) in worst case.
        # We need a different approach.
        
        # Alternative: O(n log n) with two pointers and a Fenwick tree + monotonic stack,
        # but with careful handling of the "remove from left" operation.
        # 
        # Key insight: when we remove L, if the bottom block has count > 1, 
        # the cost is unchanged. If count == 1, we need to "rebuild" the prefix 
        # up to the next breakpoint, which can be done by popping the bottom 
        # and recalculating the cost for the new first block using the values 
        # that were "hidden" behind it.
        # 
        # Actually, we can maintain a second stack that stores the "full" profiles 
        # of each prefix. When L moves, we can pop from this stack.
        # This is similar to a persistent data structure.
        # 
        # Given the time, let's implement the O(n log n) two-pointer with a segment tree
        # that supports range add and range sum, maintaining the running max array M.
        
        # Segment tree with lazy propagation for range add and range sum
        size = 1
        while size < n:
            size *= 2
        
        # tree[i] = sum of M[i] over the range of node i
        # lazy[i] = pending range add for node i
        tree = [0] * (2 * size)
        lazy = [0] * (2 * size)
        
        def apply(node, val):
            tree[node] += val * (1 << (node.bit_length() - 1)) if node < size else 0
            # Actually, we need the length of the segment. Let's precompute lengths.
            pass
        
        # This is getting messy. Let's use a simpler O(n log n) approach with a 
        # Fenwick tree for range add and point query, and a separate Fenwick for 
        # the sum of M values.
        
        # Actually, we need range sum of M[i], so we need a segment tree or 
        # two Fenwicks for difference array.
        
        # Let me implement the segment tree properly.
        
        N = n
        size = 1
        while size < N:
            size <<= 1
        
        tree = [0] * (2 * size)
        lazy = [0] * (2 * size)
        
        def _apply(node, val, length):
            tree[node] += val * length
            lazy[node] += val
        
        def _push(node, length):
            if lazy[node] != 0:
                _apply(node*2, lazy[node], length // 2)
                _apply(node*2+1, lazy[node], length // 2)
                lazy[node] = 0
        
        def range_add(l, r, val):
            # add val to M[l..r] (0-indexed, inclusive)
            def _update(node, node_l, node_r):
                if r < node_l or node_r < l:
                    return
                if l <= node_l and node_r <= r:
                    _apply(node, val, node_r - node_l + 1)
                    return
                _push(node, node_r - node_l + 1)
                mid = (node_l + node_r) // 2
                _update(node*2, node_l, mid)
                _update(node*2+1, mid+1, node_r)
                tree[node] = tree[node*2] + tree[node*2+1]
            
            _update(1, 0, size-1)
        
        def range_sum(l, r):
            # sum of M[l..r]
            res = 0
            def _query(node, node_l, node_r):
                nonlocal res
                if r < node_l or node_r < l:
                    return
                if l <= node_l and node_r <= r:
                    res += tree[node]
                    return
                _push(node, node_r - node_l + 1)
                mid = (node_l + node_r) // 2
                _query(node*2, node_l, mid)
                _query(node*2+1, mid+1, node_r)
            _query(1, 0, size-1)
            return res
        
        # Now, we maintain the window [L..R] and the array M (running max).
        # Initially, empty.
        # When we add position R with value x:
        #   We need to find the first position p <= R such that M[p] >= x, 
        #   or p = -1 if none.
        #   Then for positions in [p+1, R], we set M[i] = x for i in [p+1, R-1], 
        #   and M[R] = x. Actually, for i in [p+1, R], M[i] becomes max(M[i], x).
        #   But since M is non-decreasing, and M[p] < x (or p=-1), 
        #   we set M[i] = x for i in [p+1, R].
        #   Wait, M[i] for i in [p+1, R-1] was >= M[p+1] > M[p]. 
        #   If x < M[p+1], then setting M[i] = x would decrease it, which is wrong.
        #   So we need: M[i] = max(M[i], x) for i in [p+1, R].
        #   This is a range add: add (x - M[p+1]) to [p+1, R]? No, M values differ.
        #   Actually, since M is non-decreasing, and we know M[p] < x <= M[p+1] 
        #   (if p+1 <= R), then for i in [p+1, R], max(M[i], x) = M[i] if M[i] >= x.
        #   But M[p+1] >= M[p] and could be > x or = x or < x.
        #   This is complicated.
        
        # The correct update when adding x at position R:
        #   Find the leftmost position p in [L..R] such that M[p] >= x.
        #   If p exists, then for i in [p..R], M[i] >= x, so M[i] unchanged.
        #     The new position R has M[R] = M[R-1] (which is >= x), so no change.
        #     Actually, M[R] = max(M[R-1], x) = M[R-1] since M[R-1] >= x.
        #   If p does not exist (all M[i] < x), then for i in [L..R], M[i] < x.
        #     We set M[i] = x for all i in [L..R], and M[R] = x.
        #     This is a range add: add (x - M[L]) to [L..R].
        #   But in the first case, M[R] is already >= x, so no change.
        #   In the second case, we need to add (x - M[L]) to [L..R] and M[R] = x.
        
        # So to add x, we need to find the first index in [L..R] with M[i] >= x.
        # We can do this with a segment tree that supports range max queries.
        # But we also need to support range add (when we update M).
        # So we need a segment tree with lazy propagation for range add and range max query.
        
        # Let's build that.
        # Re-initialize segment tree for M with range add and range max.
        # Actually, we can do this more simply with a stack as before, 
        # but handle removal correctly.
        
        # The key is: when we remove L, we just decrease the window size.
        # We don't need to update M for the removed position.
        # For the remaining positions, M is still correct because M[i] for i > L 
        # depends only on nums[L+1..i], not on nums[L].
        # Wait, is that true? M[i] = max(nums[L..i]). If we remove L, the new M[i) = max(nums[L+1..i]).
        # These are different! For positions where nums[L] was the unique maximum, 
        # the new M[i] is smaller.
        # So we DO need to update M when L moves.
        
        # This is the fundamental problem.
        # The two-pointer approach requires updating M for the suffix, 
        # which is not a simple range operation.
        
        # Given the complexity, the most reliable O(n log^2 n) approach is:
        # For each L, binary search R. To compute cost(L,R) in O(log^2 n):
        # Use a segment tree where each node stores a sorted list of values 
        # and prefix sums, enabling O(log n) cost computation.
        # 
        # Specifically, for a segment [l..r], we store:
        #   - sorted list of nums values
        #   - prefix sums
        # Then to compute the cost of making [L..R] non-decreasing, 
        # we process the segment tree from left to right, maintaining a current max.
        # For each node fully in [L..R], we need to add to the cost: 
        # sum_{i in node} max(0, current_max - nums[i]), 
        # and update current_max to max(current_max, max in node).
        # Since the node is sorted, we can binary search in the sorted list 
        # to find the first element >= current_max, and compute the sum.
        # This is O(log n) per node, O(log^2 n) per query.
        
        # Build the sorted lists and prefix sums for each node.
        # This is a "merge sort tree" (segment tree of sorted arrays).
        
        N = n
        size = 1
        while size < N:
            size <<= 1
        
        # merged[i] will store sorted values for node i
        merged = [[] for _ in range(2 * size)]
        # pref[i] will store prefix sums for node i
        pref = [[] for _ in range(2 * size)]
        
        # Initialize leaves
        for i in range(N):
            merged[size + i] = [nums[i]]
            pref[size + i] = [nums[i]]
        for i in range(size - 1, 0, -1):
            left = merged[2*i]
            right = merged[2*i+1]
            merged[i] = []
            pref[i] = []
            # Merge left and right
            p1 = p2 = 0
            s = 0
            while p1 < len(left) or p2 < len(right):
                if p2 == len(right) or (p1 < len(left) and left[p1] <= right[p2]):
                    val = left[p1]
                    p1 += 1
                else:
                    val = right[p2]
                    p2 += 1
                s += val
                merged[i].append(val)
                pref[i].append(s)
        
        def cost_range(l, r, initial_max):
            # Compute cost of making nums[l..r] non-decreasing, 
            # given that the running max before l is `initial_max`.
            # Returns (total_cost, final_max)
            # We process nodes in order from left to right.
            # We need to traverse the segment tree in order.
            
            # Collect the nodes that exactly cover [l..r]
            nodes = []
            def collect(node, node_l, node_r):
                if r < node_l or node_r < l:
                    return
                if l <= node_l and node_r <= r:
                    nodes.append((node_l, node_r, node))
                    return
                mid = (node_l + node_r) // 2
                collect(node*2, node_l, mid)
                collect(node*2+1, mid+1, node_r)
            collect(1, 0, size-1)
            
            # Sort by left endpoint (they are already in order due to recursion)
            # nodes are in left-to-right order.
            
            total_cost = 0
            cur_max = initial_max
            
            for nl, nr, node in nodes:
                arr = merged[node]
                ps = pref[node]
                # Find first index idx such that arr[idx] >= cur_max
                import bisect
                idx = bisect.bisect_left(arr, cur_max)
                if idx < len(arr):
                    # Elements at idx and above are >= cur_max
                    # Cost = (idx * cur_max - sum(arr[0:idx])) 
                    #        + (0 for the rest, since they are >= cur_max)
                    sum_below = ps[idx-1] if idx > 0 else 0
                    total_cost += idx * cur_max - sum_below
                    # Update cur_max to max of arr
                    cur_max = max(cur_max, arr[-1])
                else:
                    # All elements are < cur_max
                    # Cost = len(arr) * cur_max - sum(arr)
                    total_cost += len(arr) * cur_max - ps[-1]
                    # cur_max unchanged
            return total_cost, cur_max
        
        # Now for each L, binary search the maximum R.
        # We want to find the smallest R such that cost(L, R+1) > k, 
        # or R = n-1 if all valid.
        
        # For binary search, we need a function f(R) = cost(L, R) <= k.
        # f is non-decreasing in R.
        
        ans = 0
        for L in range(n):
            # Binary search for max R
            lo, hi = L, n  # hi is exclusive, cost(L, hi-1) <= k
            # Check if single element works: cost(L,L) = 0 <= k, so hi >= L+1
            while lo < hi:
                mid = (lo + hi) // 2
                # We need cost(L, mid) <= k
                # But we need to know initial_max. For subarray [L..mid], 
                # the initial max is 0 (or -inf) because there's no left context.
                c, _ = cost_range(L, mid, 0)
                if c <= k:
                    lo = mid + 1
                else:
                    hi = mid
            # lo is the first R where cost > k, so valid R are in [L, lo-1]
            ans += (lo - 1) - L + 1
        
        return ans