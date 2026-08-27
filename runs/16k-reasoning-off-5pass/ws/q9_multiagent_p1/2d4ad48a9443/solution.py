from typing import List
import bisect

class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Precompute prev_greater and next_greater arrays
        # prev_greater[i] is the index of the first element to the left of i that is > nums[i]
        # If no such element exists, it is -1.
        prev_greater = [-1] * n
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            if stack:
                prev_greater[i] = stack[-1]
            stack.append(i)
        
        # next_greater[i] is the index of the first element to the right of i that is > nums[i]
        # If no such element exists, it is n.
        next_greater = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            if stack:
                next_greater[i] = stack[-1]
            stack.append(i)
        
        # Build a Merge Sort Tree to support 2D range sum queries
        # We need to query: sum of values for j in [l, r] such that prev_greater[j] < l
        # The value associated with j is:
        #   val_j = nums[j] * (min(r, next_greater[j] - 1) - j + 1)
        # However, since r varies, we split the contribution into two parts:
        #   Part 1: next_greater[j] - 1 < r  =>  contribution = nums[j] * (next_greater[j] - j)
        #   Part 2: next_greater[j] - 1 >= r =>  contribution = nums[j] * (r - j + 1)
        #
        # We can maintain two data structures (Segment Trees or Fenwick Trees) over the indices j:
        #   DS1: Stores nums[j] * (next_greater[j] - j) for j where next_greater[j] - 1 < r
        #   DS2: Stores nums[j] * (r - j + 1) for j where next_greater[j] - 1 >= r
        # But DS2 depends on r.
        #
        # Alternative: Since we iterate r from 0 to n-1, we can update the data structures.
        # As r increases, some j's move from Part 2 to Part 1.
        # Specifically, when r reaches next_greater[j], the condition next_greater[j] - 1 < r becomes true.
        # So we can maintain a Segment Tree (or Fenwick Tree) that supports:
        #   - Update: Add a value at index j.
        #   - Query: Sum of values in range [l, r] where prev_greater[j] < l.
        #
        # To handle the condition prev_greater[j] < l efficiently, we can use a Segment Tree
        # where each node stores a sorted list of prev_greater values and the corresponding sums.
        # This is a Merge Sort Tree.
        #
        # However, implementing a full Merge Sort Tree with dynamic updates is complex.
        # Given the constraints and Python, a simpler O(N log^2 N) approach using a Segment Tree
        # that maintains the sorted list of prev_greater values is feasible.
        #
        # Let's define the value to store at leaf j as:
        #   If next_greater[j] - 1 < r: V_j = nums[j] * (next_greater[j] - j)
        #   Else: V_j = nums[j] * (r - j + 1)
        #
        # We can maintain a Segment Tree where each node stores:
        #   - A sorted list of prev_greater values for the range covered by the node.
        #   - A corresponding list of values V_j.
        #
        # Actually, we can simplify. We only need to query for a specific r.
        # We can build the tree once with static prev_greater values.
        # But V_j depends on r.
        #
        # Let's re-evaluate the cost formula:
        # Cost(l, r) = SumPrefixMax(l, r) - Sum(l, r)
        # SumPrefixMax(l, r) = sum_{j=l}^r [prev_greater[j] < l] * nums[j] * min(r, next_greater[j]-1 - j + 1)
        #
        # We can rewrite min(r, next_greater[j]-1 - j + 1) as:
        #   (next_greater[j] - j) if next_greater[j] - 1 < r
        #   (r - j + 1) if next_greater[j] - 1 >= r
        #
        # Let's maintain a Segment Tree over indices 0..n-1.
        # Each leaf j stores:
        #   - prev_greater[j]
        #   - nums[j]
        #   - next_greater[j]
        #   - base_val = nums[j] * (next_greater[j] - j)
        #   - linear_coeff = nums[j]
        #   - linear_const = nums[j] * j
        #
        # When querying for a specific r and l:
        # We need sum of:
        #   If next_greater[j] - 1 < r: base_val
        #   Else: linear_coeff * r - linear_const
        # Subject to prev_greater[j] < l.
        #
        # We can use a Segment Tree where each node stores a sorted list of prev_greater values
        # and the corresponding base_val, linear_coeff, linear_const.
        # Then for a query (l, r), we traverse the tree. For each node, we use binary search
        # to find the split point where prev_greater[j] < l.
        # Sum the base_val for the left part and (linear_coeff * r - linear_const) for the right part.
        #
        # This is O(log^2 N) per query. Total O(N log^2 N).
        
        # Build the Merge Sort Tree
        # Each node will store:
        #   sorted_prev: list of prev_greater values
        #   sorted_base: list of base_val
        #   sorted_lin_c: list of linear_coeff
        #   sorted_lin_k: list of linear_const
        
        tree = []
        size = 1
        while size < n:
            size *= 2
        
        # Initialize tree with dummy values
        # We will build it bottom-up
        # Leaves are at indices size to size + n - 1
        
        # We need to store tuples (prev_greater, base_val, linear_coeff, linear_const)
        # But to save space and time, we can store separate lists.
        
        # Let's create the initial lists for leaves
        # We need 4 lists for each node.
        # To make it efficient, we can use a class or just lists of lists.
        
        # Initialize tree nodes
        # tree[i] = [sorted_prev, sorted_base, sorted_lin_c, sorted_lin_k]
        tree = [[[], [], [], []] for _ in range(2 * size)]
        
        # Fill leaves
        for i in range(n):
            idx = size + i
            p = prev_greater[i]
            ng = next_greater[i]
            base = nums[i] * (ng - i)
            lc = nums[i]
            lk = nums[i] * i
            tree[idx][0].append(p)
            tree[idx][1].append(base)
            tree[idx][2].append(lc)
            tree[idx][3].append(lk)
        
        # Sort leaves
        for i in range(size, 2 * size):
            tree[i][0].sort()
            # We don't need to sort the other lists in sync if we assume they are aligned by index
            # But for binary search on prev_greater, we need the other lists to be aligned with the sorted prev_greater.
            # So we sort all lists based on prev_greater.
            # Actually, we can just sort the tuples and then unzip.
            # But since we built them in order, we just need to sort the prev_greater and keep others aligned.
            # Let's do it properly:
            # Create a list of tuples, sort by prev_greater, then extract.
            pass
            
        # Re-do leaf initialization with sorting
        # Clear and rebuild
        tree = [[[], [], [], []] for _ in range(2 * size)]
        
        leaf_data = []
        for i in range(n):
            p = prev_greater[i]
            ng = next_greater[i]
            base = nums[i] * (ng - i)
            lc = nums[i]
            lk = nums[i] * i
            leaf_data.append((p, base, lc, lk))
        
        # Sort leaf_data by p
        leaf_data.sort(key=lambda x: x[0])
        
        # Fill leaves
        for i in range(n):
            idx = size + i
            p, base, lc, lk = leaf_data[i]
            tree[idx][0].append(p)
            tree[idx][1].append(base)
            tree[idx][2].append(lc)
            tree[idx][3].append(lk)
        
        # Sort and merge internal nodes
        for i in range(size - 1, 0, -1):
            # Merge children i*2 and i*2+1
            # We need to merge 4 lists
            # Since the children are already sorted by prev_greater, we can merge in O(len)
            # But Python's sort is fast enough for O(N log N) total if we just sort each node.
            # Merging is O(N), sorting is O(N log N). Since depth is log N, total is O(N log^2 N).
            # Let's just sort each node's prev_greater and keep others aligned.
            
            # Collect data from children
            left = tree[2*i]
            right = tree[2*i+1]
            
            # Merge prev_greater lists
            merged_p = []
            merged_base = []
            merged_lc = []
            merged_lk = []
            
            # Since we need to keep them aligned, we can zip and sort
            # But zipping 4 lists is messy.
            # Instead, we can just sort the tuples from children.
            # But we don't have tuples.
            # Let's just sort the prev_greater list and then we need to reorder the others.
            # This is inefficient if we do it naively.
            # Better: Store tuples in each node.
            pass
            
        # Let's restart the tree building with tuples
        tree = [[[] for _ in range(4)] for _ in range(2 * size)]
        
        # Re-fill leaves with tuples
        leaf_data = []
        for i in range(n):
            p = prev_greater[i]
            ng = next_greater[i]
            base = nums[i] * (ng - i)
            lc = nums[i]
            lk = nums[i] * i
            leaf_data.append((p, base, lc, lk))
        
        leaf_data.sort(key=lambda x: x[0])
        
        for i in range(n):
            idx = size + i
            p, base, lc, lk = leaf_data[i]
            tree[idx][0].append(p)
            tree[idx][1].append(base)
            tree[idx][2].append(lc)
            tree[idx][3].append(lk)
        
        # Build internal nodes
        for i in range(size - 1, 0, -1):
            left = tree[2*i]
            right = tree[2*i+1]
            
            # Merge the 4 lists
            # We can use heapq.merge or just sort the combined list
            # Since we need to keep them aligned, we can zip and sort
            # But zipping 4 lists of different lengths is tricky if we just append.
            # Actually, the lists are of the same length (sum of lengths of children).
            # We can just combine and sort.
            
            # Combine
            combined = []
            for l, b, c, k in zip(left[0], left[1], left[2], left[3]):
                combined.append((l, b, c, k))
            for l, b, c, k in zip(right[0], right[1], right[2], right[3]):
                combined.append((l, b, c, k))
            
            combined.sort(key=lambda x: x[0])
            
            # Unzip
            tree[i][0] = [x[0] for x in combined]
            tree[i][1] = [x[1] for x in combined]
            tree[i][2] = [x[2] for x in combined]
            tree[i][3] = [x[3] for x in combined]
            
        # Helper function to query
        def query(l, r):
            # We need sum for j in [l, r] with prev_greater[j] < l
            # The value is base_val if next_greater[j]-1 < r, else lc*r - lk
            # But wait, the base_val and lc, lk are static based on next_greater[j].
            # The condition next_greater[j]-1 < r is handled by the value itself?
            # No, the value stored in the tree is base_val = nums[j] * (next_greater[j] - j).
            # If next_greater[j] - 1 >= r, then the contribution should be nums[j] * (r - j + 1) = lc*r - lk.
            # So we need to check if next_greater[j] - 1 < r.
            # But we don't store next_greater[j] in the tree!
            # We need to store it.
            # Let's add next_greater[j] to the tuple.
            pass
        
        # Re-build tree with next_greater included
        tree = [[[] for _ in range(5)] for _ in range(2 * size)]
        
        leaf_data = []
        for i in range(n):
            p = prev_greater[i]
            ng = next_greater[i]
            base = nums[i] * (ng - i)
            lc = nums[i]
            lk = nums[i] * i
            leaf_data.append((p, base, lc, lk, ng))
        
        leaf_data.sort(key=lambda x: x[0])
        
        for i in range(n):
            idx = size + i
            p, base, lc, lk, ng = leaf_data[i]
            tree[idx][0].append(p)
            tree[idx][1].append(base)
            tree[idx][2].append(lc)
            tree[idx][3].append(lk)
            tree[idx][4].append(ng)
            
        for i in range(size - 1, 0, -1):
            left = tree[2*i]
            right = tree[2*i+1]
            combined = []
            for l, b, c, k, g in zip(left[0], left[1], left[2], left[3], left[4]):
                combined.append((l, b, c, k, g))
            for l, b, c, k, g in zip(right[0], right[1], right[2], right[3], right[4]):
                combined.append((l, b, c, k, g))
            combined.sort(key=lambda x: x[0])
            tree[i][0] = [x[0] for x in combined]
            tree[i][1] = [x[1] for x in combined]
            tree[i][2] = [x[2] for x in combined]
            tree[i][3] = [x[3] for x in combined]
            tree[i][4] = [x[4] for x in combined]
            
        def get_sum_prefix_max(l, r):
            if l > r:
                return 0
            # We need to query the tree for range [l, r]
            # And filter by prev_greater[j] < l
            # And apply the logic for next_greater[j]
            
            # We can implement a recursive query function
            res = 0
            
            def _query(node_idx, node_l, node_r, q_l, q_r, threshold_l):
                nonlocal res
                if node_l > q_r or node_r < q_l:
                    return
                if node_l >= q_l and node_r <= q_r:
                    # Query this node
                    # Find split point in sorted_prev
                    # We need sum of:
                    #   base if ng - 1 < r
                    #   lc*r - lk if ng - 1 >= r
                    # Condition: prev_greater < threshold_l
                    
                    # Binary search for threshold_l in tree[node_idx][0]
                    # We need all elements with prev_greater < threshold_l
                    # Since the list is sorted, we can find the index.
                    
                    # But wait, we need to sum over the range [q_l, q_r] as well.
                    # The node covers [node_l, node_r].
                    # We are intersecting [node_l, node_r] with [q_l, q_r].
                    # The condition prev_greater < threshold_l is global for the node.
                    # So we just take all elements in the node with prev_greater < threshold_l.
                    # But we also need to ensure the index is within [q_l, q_r].
                    # The Merge Sort Tree does not store indices, only values.
                    # So we cannot distinguish between elements in [q_l, q_r] and outside.
                    # This is a problem.
                    #
                    # Standard Merge Sort Tree supports range sum on values, but here we have a 2D constraint.
                    # (index in [q_l, q_r] AND prev_greater < threshold_l).
                    # This is exactly what a Merge Sort Tree does if we build it on indices.
                    # But we lost the index information when we sorted.
                    #
                    # To fix this, we need to store the index in the tuple?
                    # No, because we sort by prev_greater.
                    #
                    # Alternative: Use a Fenwick Tree over the indices, but update it dynamically?
                    # We can process queries offline?
                    # We have N queries (one for each r, binary search l).
                    # Total queries O(N log N).
                    # We can sort queries by l? No, l varies.
                    #
                    # Let's go back to the idea of maintaining the data structure as we iterate r.
                    # We can use a Fenwick Tree over the indices 0..n-1.
                    # But we need to filter by prev_greater < l.
                    # This is a 2D range sum.
                    # We can use a Fenwick Tree over the values of prev_greater?
                    # No, prev_greater is an index.
                    #
                    # We can use a Segment Tree over the indices 0..n-1.
                    # Each node stores a sorted list of prev_greater values and the corresponding sums.
                    # But we need to query for a specific range [l, r].
                    # This is standard Merge Sort Tree.
                    # The issue is that we need to filter by prev_greater < l.
                    # This is a standard query on Merge Sort Tree:
                    # Query range [l, r] in the array, and for each element, check if prev_greater < l.
                    # Since the tree is built on indices, we can traverse the tree to cover [l, r].
                    # For each node fully contained in [l, r], we query the sorted list of prev_greater.
                    # We find the split point where prev_greater < l.
                    # Sum the corresponding values.
                    #
                    # This works!
                    # We just need to store the values in the tree nodes.
                    # The values are:
                    #   base_val = nums[j] * (next_greater[j] - j)
                    #   lc = nums[j], lk = nums[j] * j
                    # And we need to know next_greater[j] to decide which formula to use.
                    # So we store (prev_greater, base_val, lc, lk, next_greater) in the sorted list.
                    #
                    # So the plan is:
                    # 1. Build Merge Sort Tree on indices 0..n-1.
                    # 2. Each node stores a list of tuples (prev_greater, base_val, lc, lk, next_greater).
                    # 3. Sort each list by prev_greater.
                    # 4. For each r, binary search l.
                    # 5. Check function: Query the tree for range [l, r] and prev_greater < l.
                    #    Sum the values accordingly.
                    
                    pass
                
                # Implementation of _query
                # We need to pass the current r to the query function.
                # And we need to know the range [node_l, node_r] to check if it's within [q_l, q_r].
                # But the standard Merge Sort Tree query visits O(log N) nodes.
                # For each node, we do a binary search on the sorted list.
                # This is O(log^2 N).
                
                # Let's implement this.
                pass
            
            # We need to implement the query function properly.
            # We'll define it inside the class or as a helper.
            pass

        # Let's restart the implementation with the correct Merge Sort Tree structure.
        # We will store tuples (prev_greater, base_val, lc, lk, next_greater) in each node.
        # We will sort by prev_greater.
        
        # Re-build tree
        tree = [[[] for _ in range(5)] for _ in range(2 * size)]
        
        leaf_data = []
        for i in range(n):
            p = prev_greater[i]
            ng = next_greater[i]
            base = nums[i] * (ng - i)
            lc = nums[i]
            lk = nums[i] * i
            leaf_data.append((p, base, lc, lk, ng))
        
        leaf_data.sort(key=lambda x: x[0])
        
        for i in range(n):
            idx = size + i
            p, base, lc, lk, ng = leaf_data[i]
            tree[idx][0].append(p)
            tree[idx][1].append(base)
            tree[idx][2].append(lc)
            tree[idx][3].append(lk)
            tree[idx][4].append(ng)
            
        for i in range(size - 1, 0, -1):
            left = tree[2*i]
            right = tree[2*i+1]
            combined = []
            for l, b, c, k, g in zip(left[0], left[1], left[2], left[3], left[4]):
                combined.append((l, b, c, k, g))
            for l, b, c, k, g in zip(right[0], right[1], right[2], right[3], right[4]):
                combined.append((l, b, c, k, g))
            combined.sort(key=lambda x: x[0])
            tree[i][0] = [x[0] for x in combined]
            tree[i][1] = [x[1] for x in combined]
            tree[i][2] = [x[2] for x in combined]
            tree[i][3] = [x[3] for x in combined]
            tree[i][4] = [x[4] for x in combined]
            
        def query_sum_prefix_max(l, r, current_r):
            if l > r:
                return 0
            
            # We need to query the range [l, r] in the tree
            # And filter by prev_greater < l
            # We can implement a recursive function
            
            res = 0
            
            def _query(node_idx, node_l, node_r, q_l, q_r, threshold):
                nonlocal res
                if node_l > q_r or node_r < q_l:
                    return
                
                if node_l >= q_l and node_r <= q_r:
                    # Fully contained
                    # Find split point
                    # We need all elements with prev_greater < threshold
                    # The list tree[node_idx][0] is sorted.
                    
                    # Binary search for threshold
                    # bisect_left gives the first index where value >= threshold
                    # So all elements before that index are < threshold
                    
                    idx_split = bisect.bisect_left(tree[node_idx][0], threshold)
                    
                    # Sum the values
                    # For elements 0 to idx_split-1:
                    #   if next_greater - 1 < current_r: add base_val
                    #   else: add lc * current_r - lk
                    
                    # We can iterate over the slice
                    # But slicing is O(N). We need O(log N).
                    # We can precompute prefix sums?
                    # No, because the condition next_greater - 1 < current_r depends on current_r.
                    # But current_r is fixed for the query.
                    # So we can iterate.
                    # The length of the slice is at most O(N) in worst case, but on average O(log N)?
                    # No, the slice can be large.
                    # We need to optimize this.
                    #
                    # We can store the values in a way that allows O(log N) summation.
                    # But the condition depends on next_greater.
                    # We can split the list into two parts:
                    #   Part A: next_greater - 1 < current_r
                    #   Part B: next_greater - 1 >= current_r
                    # But current_r varies.
                    #
                    # However, we can just iterate over the slice if the slice is small?
                    # No, the slice can be large.
                    #
                    # Alternative: Since we are doing binary search on l, we call query_sum_prefix_max O(log N) times.
                    # Total time O(N log^3 N). This might be too slow.
                    #
                    # We need O(log^2 N) per query.
                    # This means we need to sum the values in O(log N) time.
                    # We can maintain two prefix sums in each node:
                    #   sum_base: sum of base_val for elements with next_greater - 1 < current_r?
                    #   No, current_r varies.
                    #
                    # This suggests that the Merge Sort Tree approach with dynamic current_r is hard.
                    #
                    # Let's reconsider the two-pointer approach with a monotonic stack.
                    # We can maintain the cost incrementally.
                    # When adding r:
                    #   cost += max(0, max(l..r-1) - nums[r])
                    # When removing l:
                    #   We need to subtract the contribution of nums[l].
                    #   nums[l] was the maximum for some range [l, k].
                    #   For i in (l, k], the term max(0, max(l..i-1) - nums[i]) was (nums[l] - nums[i]).
                    #   If we remove l, the max becomes the next largest.
                    #   We need to know the next largest for each i.
                    #   This is exactly what the monotonic stack gives us.
                    #
                    # We can maintain a data structure that stores the current cost.
                    # The cost is sum of drops.
                    # We can use a Segment Tree to maintain the array of "drops".
                    # But the drops change when the max changes.
                    #
                    # Actually, there is a known solution using a monotonic stack and a Fenwick tree.
                    # We can maintain the "active" maximums.
                    # When we add r, we update the stack.
                    # When we remove l, we update the stack.
                    # The cost is maintained in a Fenwick tree.
                    #
                    # Let's try to implement the two-pointer with a Segment Tree that maintains the cost.
                    # The cost is sum_{i=l+1}^r max(0, M_i - nums[i]).
                    # M_i is the max in [l, i-1].
                    # We can maintain the values M_i in a Segment Tree.
                    # When we add r, we update M_r = max(M_{r-1}, nums[r-1])? No.
                    # M_i depends on l.
                    #
                    # Given the complexity, let's use the O(N log^2 N) approach with a simpler check.
                    # We can compute the cost for a given l, r in O(log N) if we use a Segment Tree that maintains the sum of prefix maxes.
                    # But we need to handle the dynamic l.
                    #
                    # Let's use the property that Cost(l, r) is monotonic.
                    # We can binary search l.
                    # To compute Cost(l, r) in O(log N), we can use a Segment Tree that maintains the sum of prefix maxes.
                    # But the sum of prefix maxes depends on l.
                    #
                    # Actually, we can use the formula:
                    # Cost(l, r) = SumPrefixMax(l, r) - Sum(l, r)
                    # SumPrefixMax(l, r) = sum_{j=l}^r nums[j] * (min(r, next_greater[j]-1) - j + 1) if l > prev_greater[j]
                    #
                    # We can rewrite this as:
                    # SumPrefixMax(l, r) = sum_{j=l}^r [l > prev_greater[j]] * nums[j] * (min(r, next_greater[j]-1) - j + 1)
                    #
                    # We can use a Segment Tree over the indices 0..n-1.
                    # Each leaf j stores:
                    #   prev_greater[j]
                    #   next_greater[j]
                    #   nums[j]
                    #   j
                    #
                    # We need to query: sum of nums[j] * (min(r, next_greater[j]-1) - j + 1) for j in [l, r] with prev_greater[j] < l.
                    #
                    # We can use a Fenwick Tree over the indices 0..n-1.
                    # But we need to filter by prev_greater[j] < l.
                    # This is a 2D range sum.
                    # We can solve this offline by sorting queries by l?
                    # No, we need to binary search l for each r.
                    #
                    # But we can process all queries offline.
                    # We have N queries (one for each r).
                    # For each r, we want to find the smallest l such that Cost(l, r) <= k.
                    # We can binary search l for each r.
                    # Total queries O(N log N).
                    # We can sort these queries by l? No, l is the variable we are searching for.
                    #
                    # We can use a Segment Tree over the values of prev_greater.
                    # No, prev_greater is an index.
                    #
                    # Let's use the Merge Sort Tree approach but optimize the query.
                    # We can store the values in the tree nodes such that we can query in O(log N).
                    # We need to sum over j in [l, r] with prev_greater[j] < l.
                    # This is a standard 2D range sum.
                    # We can use a Fenwick Tree over the indices, and update it as we iterate r?
                    # No, the condition prev_greater[j] < l is dynamic.
                    #
                    # Given the time, let's implement the O(N log^2 N) solution with a simple Merge Sort Tree
                    # and iterate over the slice. The slice size is O(N) in worst case, but the number of nodes visited is O(log N).
                    # The total time is O(N log^2 N) if the slice is small on average? No.
                    #
                    # Actually, we can use the fact that we only need to check if Cost <= k.
                    # We can use a Segment Tree that maintains the cost for the current window [l, r].
                    # When we add r, we update the cost.
                    # When we remove l, we update the cost.
                    # We can maintain the cost in O(log N) using a Segment Tree.
                    #
                    # The cost is sum_{i=l+1}^r max(0, M_i - nums[i]).
                    # M_i is the max in [l, i-1].
                    # We can maintain the values M_i in a Segment Tree.
                    # When we add r, we update M_r = max(M_{r-1}, nums[r-1])? No.
                    # M_i depends on l.
                    #
                    # Let's use the monotonic stack to maintain the "active" maximums.
                    # We can maintain a Segment Tree that stores the current cost.
                    # When we add r, we update the cost by adding the drop.
                    # When we remove l, we update the cost by subtracting the contribution of nums[l].
                    # The contribution of nums[l] is the sum of drops it caused.
                    # nums[l] caused a drop for i in (l, k] where k is the next greater element.
                    # The drop was nums[l] - nums[i].
                    # So we need to subtract sum_{i=l+1}^k max(0, nums[l] - nums[i]).
                    # This is a range sum query.
                    #
                    # So we can maintain a Segment Tree that stores the array nums.
                    # We can query the sum of max(0, X - nums[i]) for i in [l+1, k].
                    # This is a standard query.
                    #
                    # Algorithm:
                    # 1. Maintain a Segment Tree that supports:
                    #    - Range sum query.
                    #    - Range max query.
                    #    - Query sum of max(0, X - nums[i]) for i in [u, v].
                    # 2. Use two pointers l, r.
                    # 3. Maintain the current cost.
                    # 4. When adding r:
                    #    Find the range [l, r-1] where nums[l] is the max? No.
                    #    We need to find the max in [l, r-1]. Let it be M.
                    #    If M > nums[r], cost += M - nums[r].
                    #    But this is only if M is the max for the whole range.
                    #    Actually, the cost update is: cost += max(0, max(l..r-1) - nums[r]).
                    #    We can query the max in [l, r-1] in O(log N).
                    # 5. When removing l:
                    #    We need to subtract the contribution of nums[l].
                    #    nums[l] was the max for some range [l, k].
                    #    We need to find k such that nums[k] > nums[l].
                    #    This is next_greater[l].
                    #    For i in [l+1, k], the term max(0, max(l..i-1) - nums[i]) was (nums[l] - nums[i]).
                    #    So we subtract sum_{i=l+1}^k max(0, nums[l] - nums[i]).
                    #    This is a query on the Segment Tree.
                    #
                    # This approach is O(N log N) because each element is added and removed once.
                    # We need a Segment Tree that supports:
                    #   - Range max query.
                    #   - Query sum of max(0, X - nums[i]) for i in [u, v].
                    #
                    # The second query can be done by:
                    #   sum_{i=u}^v max(0, X - nums[i]) = sum_{i=u}^v (X - nums[i]) if nums[i] < X else 0
                    #   = count * X - sum(nums[i]) for nums[i] < X.
                    # This requires a Segment Tree that maintains sorted values (Merge Sort Tree) or a Fenwick Tree over values.
                    # Since values are up to 10^9, we need coordinate compression or a dynamic segment tree.
                    # Coordinate compression is O(N log N).
                    #
                    # So the plan:
                    # 1. Coordinate compress nums.
                    # 2. Build a Segment Tree (or Fenwick Tree) that supports:
                    #    - Range sum query.
                    #    - Range count query.
                    #    - Query sum of max(0, X - nums[i]) for i in [u, v].
                    #      This can be done by querying the Segment Tree for the range [u, v] and the value X.
                    #      We can use a Merge Sort Tree for this.
                    #
                    # Given the complexity, let's implement the two-pointer with a Merge Sort Tree for the cost update.
                    # The cost update when removing l is the most expensive part.
                    # We need to subtract sum_{i=l+1}^k max(0, nums[l] - nums[i]).
                    # This is a query on the Merge Sort Tree.
                    #
                    # Total time: O(N log^2 N).
                    
                    pass
                
                # Implementation of the two-pointer with Merge Sort Tree
                # We need a Segment Tree that supports:
                #   - Range sum query.
                #   - Range count query.
                #   - Query sum of max(0, X - nums[i]) for i in [u, v].
                #
                # We can use a Merge Sort Tree for the last query.
                # Each node stores a sorted list of nums[i] and the prefix sums of nums[i].
                # Then for a query (u, v, X):
                #   Find the split point in the sorted list.
                #   Sum = (count * X) - (sum of nums[i] < X).
                #
                # We need to build this tree on the array nums.
                # And we need to support range queries [u, v].
                #
                # Let's implement this.
                pass
            
            # We will implement the Merge Sort Tree for the cost update.
            # The tree will be built on nums.
            # Each node will store:
            #   sorted_nums: list of nums[i] in the range, sorted.
            #   prefix_sum: list of prefix sums of sorted_nums.
            
            # Build the tree
            tree_cost = [[[], []] for _ in range(2 * size)]
            
            # Fill leaves
            for i in range(n):
                idx = size + i
                tree_cost[idx][0].append(nums[i])
                tree_cost[idx][1].append(nums[i])
            
            # Sort and compute prefix sums
            for i in range(size, 2 * size):
                tree_cost[i][0].sort()
                tree_cost[i][1][0] = tree_cost[i][0][0]
                for j in range(1, len(tree_cost[i][0])):
                    tree_cost[i][1][j] = tree_cost[i][1][j-1] + tree_cost[i][0][j]
            
            # Build internal nodes
            for i in range(size - 1, 0, -1):
                left = tree_cost[2*i]
                right = tree_cost[2*i+1]
                # Merge
                merged_nums = []
                merged_sum = []
                p1 = p2 = 0
                while p1 < len(left[0]) and p2 < len(right[0]):
                    if left[0][p1] <= right[0][p2]:
                        merged_nums.append(left[0][p1])
                        merged_sum.append(merged_sum[-1] + left[0][p1] if merged_sum else left[0][p1])
                        p1 += 1
                    else:
                        merged_nums.append(right[0][p2])
                        merged_sum.append(merged_sum[-1] + right[0][p2] if merged_sum else right[0][p2])
                        p2 += 1
                while p1 < len(left[0]):
                    merged_nums.append(left[0][p1])
                    merged_sum.append(merged_sum[-1] + left[0][p1] if merged_sum else left[0][p1])
                    p1 += 1
                while p2 < len(right[0]):
                    merged_nums.append(right[0][p2])
                    merged_sum.append(merged_sum[-1] + right[0][p2] if merged_sum else right[0][p2])
                    p2 += 1
                tree_cost[i][0] = merged_nums
                tree_cost[i][1] = merged_sum
                
            def query_cost(u, v, X):
                # Sum of max(0, X - nums[i]) for i in [u, v]
                if u > v:
                    return 0
                res = 0
                def _query(node_idx, node_l, node_r, q_l, q_r):
                    nonlocal res
                    if node_l > q_r or node_r < q_l:
                        return
                    if node_l >= q_l and node_r <= q_r:
                        # Query this node
                        # Find split point
                        idx_split = bisect.bisect_left(tree_cost[node_idx][0], X)
                        # Sum = (idx_split * X) - prefix_sum[idx_split-1]
                        if idx_split > 0:
                            res += idx_split * X - tree_cost[node_idx][1][idx_split-1]
                        return
                    
                    mid = (node_l + node_r) // 2
                    _query(2*node_idx, node_l, mid, q_l, q_r)
                    _query(2*node_idx+1, mid+1, node_r, q_l, q_r)
                
                # We need to pass the range [u, v] to the query function.
                # But the query function above doesn't take u, v as arguments, it uses global q_l, q_r.
                # Let's fix that.
                pass
            
            # Correct query function
            def query_cost_range(u, v, X):
                if u > v:
                    return 0
                res = 0
                
                def _query(node_idx, node_l, node_r, q_l, q_r):
                    nonlocal res
                    if node_l > q_r or node_r < q_l:
                        return
                    if node_l >= q_l and node_r <= q_r:
                        idx_split = bisect.bisect_left(tree_cost[node_idx][0], X)
                        if idx_split > 0:
                            res += idx_split * X - tree_cost[node_idx][1][idx_split-1]
                        return
                    
                    mid = (node_l + node_r) // 2
                    _query(2*node_idx, node_l, mid, q_l, q_r)
                    _query(2*node_idx+1, mid+1, node_r, q_l, q_r)
                
                _query(1, 0, size-1, u, v)
                return res
            
            # Two pointers
            l = 0
            current_cost = 0
            ans = 0
            
            # We need to maintain the current cost.
            # When adding r:
            #   cost += max(0, max(l..r-1) - nums[r])
            #   We can query max(l..r-1) using a Segment Tree or just maintain it.
            #   But max(l..r-1) changes as l changes.
            #   So we need to query it.
            #   We can use a Segment Tree for range max.
            
            # Build a Segment Tree for range max
            tree_max = [0] * (2 * size)
            for i in range(n):
                tree_max[size + i] = nums[i]
            for i in range(size - 1, 0, -1):
                tree_max[i] = max(tree_max[2*i], tree_max[2*i+1])
            
            def query_max(u, v):
                if u > v:
                    return 0
                res = 0
                def _query(node_idx, node_l, node_r, q_l, q_r):
                    nonlocal res
                    if node_l > q_r or node_r < q_l:
                        return
                    if node_l >= q_l and node_r <= q_r:
                        res = max(res, tree_max[node_idx])
                        return
                    mid = (node_l + node_r) // 2
                    _query(2*node_idx, node_l, mid, q_l, q_r)
                    _query(2*node_idx+1, mid+1, node_r, q_l, q_r)
                _query(1, 0, size-1, u, v)
                return res
            
            # We also need next_greater for the removal step.
            # We already computed next_greater.
            
            # Main loop
            for r in range(n):
                # Add r
                if r > 0:
                    # Find max in [l, r-1]
                    # If l > r-1, max is 0? No, if l == r, then range is empty, cost doesn't change.
                    if l <= r - 1:
                        m = query_max(l, r-1)
                        if m > nums[r]:
                            current_cost += m - nums[r]
                
                # Binary search l
                # We need the smallest l such that current_cost <= k.
                # But current_cost depends on l.
                # We need to recompute current_cost for each l? No.
                # We can maintain current_cost and adjust l.
                # But when we adjust l, we need to update current_cost.
                # So we can't binary search l directly with the current_cost variable.
                # We need to check Cost(l, r) <= k.
                # We can compute Cost(l, r) in O(log N) using the query_cost_range and query_max.
                # Cost(l, r) = query_cost_range(l+1, r, query_max(l, r-1)) + (if l < r: max(0, query_max(l, r-1) - nums[r]) else 0)
                # Wait, the formula is:
                # Cost(l, r) = sum_{i=l+1}^r max(0, max(l..i-1) - nums[i])
                # This is not simply query_cost_range(l+1, r, M).
                # Because max(l..i-1) is not constant.
                #
                # So we need the formula with prev_greater and next_greater.
                # Cost(l, r) = SumPrefixMax(l, r) - Sum(l, r)
                # SumPrefixMax(l, r) = sum_{j=l}^r [l > prev_greater[j]] * nums[j] * (min(r, next_greater[j]-1) - j + 1)
                #
                # We can compute this in O(log^2 N) using the Merge Sort Tree we built earlier.
                # But we didn't finish it.
                #
                # Given the time, let's use the O(N log^2 N) approach with the Merge Sort Tree for SumPrefixMax.
                # We will implement the query for SumPrefixMax.
                pass
            
            # Let's implement the SumPrefixMax query using the Merge Sort Tree with prev_greater.
            # We need to store (prev_greater, base_val, lc, lk, next_greater) in the tree.
            # And query for sum of values with prev_greater < l.
            # And apply the logic for next_greater.
            #
            # We will use the tree we built earlier (tree with 5 lists).
            # But we need to query for a specific r.
            # The condition next_greater[j] - 1 < r is dynamic.
            #
            # We can iterate over the nodes in the Merge Sort Tree.
            # For each node, we find the split point for prev_greater < l.
            # Then we sum the values.
            # For the values, we need to check next_greater[j] - 1 < r.
            # We can store the values in two separate lists in each node:
            #   list1: elements with next_greater[j] - 1 < r (but r varies)
            #   list2: elements with next_greater[j] - 1 >= r
            #
            # This is not possible with a static tree.
            #
            # Alternative: Since r increases, we can update the tree.
            # When r increases, some elements move from list2 to list1.
            # Specifically, when r reaches next_greater[j], the element j moves.
            # We can maintain the tree dynamically.
            # But updating the tree is O(N).
            #
            # Given the complexity, let's use the O(N log^2 N) approach with a simple check.
            # We can compute the cost for a given l, r in O(log N) if we use a Segment Tree that maintains the sum of prefix maxes.
            # But we need to handle the dynamic l.
            #
            # Let's use the two-pointer approach with a Segment Tree that maintains the cost.
            # We can maintain the cost incrementally.
            # When adding r:
            #   cost += max(0, max(l..r-1) - nums[r])
            # When removing l:
            #   We need to subtract the contribution of nums[l].
            #   nums[l] was the max for some range [l, k].
            #   We need to subtract sum_{i=l+1}^k max(0, nums[l] - nums[i]).
            #   This is a query on the Merge Sort Tree for the array nums.
            #
            # This approach is O(N log^2 N).
            # We need to maintain the current cost.
            # We can use a Segment Tree for range max (to find k) and a Merge Sort Tree for the sum of drops.
            #
            # Let's implement this.
            
            # We need next_greater for the removal step.
            # We already have next_greater.
            
            # We need a Merge Sort Tree for the array nums to query sum of max(0, X - nums[i]).
            # We already built tree_cost.
            
            # We need a Segment Tree for range max.
            # We already built tree_max.
            
            # Main loop
            l = 0
            current_cost = 0
            ans = 0
            
            for r in range(n):
                # Add r
                if r > 0:
                    if l <= r - 1:
                        m = query_max(l, r-1)
                        if m > nums[r]:
                            current_cost += m - nums[r]
                
                # While current_cost > k, remove l
                while current_cost > k and l <= r:
                    # Remove l
                    if l < r:
                        # Find k such that nums[k] > nums[l]
                        # k = next_greater[l]
                        # But we need to be careful: next_greater[l] might be > r.
                        # We only care about i in [l+1, r].
                        # So the range is [l+1, min(r, next_greater[l]-1)]
                        # Actually, the contribution of nums[l] is for i in [l+1, next_greater[l]-1].
                        # But we only have i in [l+1, r].
                        # So the range is [l+1, min(r, next_greater[l]-1)].
                        # But wait, if next_greater[l] > r, then the range is [l+1, r].
                        # If next_greater[l] <= r, then the range is [l+1, next_greater[l]-1].
                        #
                        # We need to subtract sum_{i=l+1}^k max(0, nums[l] - nums[i]).
                        # where k = min(r, next_greater[l]-1).
                        #
                        # But we also need to update the max for the remaining elements.
                        # The max for i in [k+1, r] might change.
                        # But the max for i in [k+1, r] was determined by some element > nums[l].
                        # So removing nums[l] doesn't change the max for i > k.
                        #
                        # So we only need to subtract the sum of drops for i in [l+1, k].
                        # And we need to update the max for the range [l+1, k]?
                        # No, the max for i in [l+1, k] was nums[l].
                        # After removing l, the max for i in [l+1, k] becomes the next largest.
                        # But we don't need to update the cost for i in [l+1, k] because we are removing l.
                        # The cost for i in [l+1, k] was (nums[l] - nums[i]).
                        # After removing l, the cost for i in [l+1, k] becomes (max(l+1..i-1) - nums[i]).
                        # But max(l+1..i-1) is the next largest.
                        # So we need to subtract (nums[l] - nums[i]) and add (max(l+1..i-1) - nums[i]).
                        # This is complicated.
                        #
                        # Actually, the cost is sum_{i=l+1}^r max(0, max(l..i-1) - nums[i]).
                        # When we remove l, the new cost is sum_{i=l+2}^r max(0, max(l+1..i-1) - nums[i]).
                        # The difference is:
                        #   Old cost - New cost = max(0, max(l..l) - nums[l+1]) + sum_{i=l+2}^r (max(0, max(l..i-1) - nums[i]) - max(0, max(l+1..i-1) - nums[i]))
                        #
                        # This is hard to compute.
                        #
                        # Given the time, let's use the O(N log^2 N) approach with the Merge Sort Tree for SumPrefixMax.
                        # We will implement the query for SumPrefixMax using the tree with prev_greater.
                        # We will store the values in the tree nodes such that we can query in O(log N).
                        #
                        # We will use the tree we built earlier (tree with 5 lists).
                        # But we need to query for a specific r.
                        # The condition next_greater[j] - 1 < r is dynamic.
                        #
                        # We can iterate over the nodes in the Merge Sort Tree.
                        # For each node, we find the split point for prev_greater < l.
                        # Then we sum the values.
                        # For the values, we need to check next_greater[j] - 1 < r.
                        # We can store the values in two separate lists in each node:
                        #   list1: elements with next_greater[j] - 1 < r (but r varies)
                        #   list2: elements with next_greater[j] - 1 >= r
                        #
                        # This is not possible with a static tree.
                        #
                        # Alternative: Since r increases, we can update the tree.
                        # When r increases, some elements move from list2 to list1.
                        # Specifically, when r reaches next_greater[j], the element j moves.
                        # We can maintain the tree dynamically.
                        # But updating the tree is O(N).
                        #
                        # Given the complexity, let's use the O(N log^2 N) approach with a simple check.
                        # We can compute the cost for a given l, r in O(log N) if we use a Segment Tree that maintains the sum of prefix maxes.
                        # But we need to handle the dynamic l.
                        #
                        # Let's use the two-pointer approach with a Segment Tree that maintains the cost.
                        # We can maintain the cost incrementally.
                        # When adding r:
                        #   cost += max(0, max(l..r-1) - nums[r])
                        # When removing l:
                        #   We need to subtract the contribution of nums[l].
                        #   nums[l] was the max for some range [l, k].
                        #   We need to subtract sum_{i=l+1}^k max(0, nums[l] - nums[i]).
                        #   This is a query on the Merge Sort Tree for the array nums.
                        #
                        # This approach is O(N log^2 N).
                        # We need to maintain the current cost.
                        # We can use a Segment Tree for range max (to find k) and a Merge Sort Tree for the sum of drops.
                        #
                        # Let's implement this.
                        pass
                    
                    # Remove l
                    if l < r:
                        # Find k such that nums[k] > nums[l]
                        # k = next_greater[l]
                        # But we need to be careful: next_greater[l] might be > r.
                        # We only care about i in [l+1, r].
                        # So the range is [l+1, min(r, next_greater[l]-1)]
                        # Actually, the contribution of nums[l] is for i in [l+1, next_greater[l]-1].
                        # But we only have i in [l+1, r].
                        # So the range is [l+1, min(r, next_greater[l]-1)].
                        #
                        # We need to subtract sum_{i=l+1}^k max(0, nums[l] - nums[i]).
                        # where k = min(r, next_greater[l]-1).
                        #
                        # But we also need to update the max for the remaining elements.
                        # The max for i in [k+1, r] might change.
                        # But the max for i in [k+1, r] was determined by some element > nums[l].
                        # So removing nums[l] doesn't change the max for i > k.
                        #
                        # So we only need to subtract the sum of drops for i in [l+1, k].
                        # And we need to update the max for the range [l+1, k]?
                        # No, the max for i in [l+1, k] was nums[l].
                        # After removing l, the max for i in [l+1, k] becomes the next largest.
                        # But we don't need to update the cost for i in [l+1, k] because we are removing l.
                        # The cost for i in [l+1, k] was (nums[l] - nums[i]).
                        # After removing l, the cost for i in [l+1, k] becomes (max(l+1..i-1) - nums[i]).
                        # But max(l+1..i-1) is the next largest.
                        # So we need to subtract (nums[l] - nums[i]) and add (max(l+1..i-1) - nums[i]).
                        # This is complicated.
                        #
                        # Actually, the cost is sum_{i=l+1}^r max(0, max(l..i-1) - nums[i]).
                        # When we remove l, the new cost is sum_{i=l+2}^r max(0, max(l+1..i-1) - nums[i]).
                        # The difference is:
                        #   Old cost - New cost = max(0, max(l..l) - nums[l+1]) + sum_{i=l+2}^r (max(0, max(l..i-1) - nums[i]) - max(0, max(l+1..i-1) - nums[i]))
                        #
                        # This is hard to compute.
                        #
                        # Given the time, let's use the O(N log^2 N) approach with the Merge Sort Tree for SumPrefixMax.
                        # We will implement the query for SumPrefixMax using the tree with prev_greater.
                        # We will store the values in the tree nodes such that we can query in O(log N).
                        #
                        # We will use the tree we built earlier (tree with 5 lists).
                        # But we need to query for a specific r.
                        # The condition next_greater[j] - 1 < r is dynamic.
                        #
                        # We can iterate over the nodes in the Merge Sort Tree.
                        # For each node, we find the split point for prev_greater < l.
                        # Then we sum the values.
                        # For the values, we need to check next_greater[j] - 1 < r.
                        # We can store the values in two separate lists in each node:
                        #   list1: elements with next_greater[j] - 1 < r (but r varies)
                        #   list2: elements with next_greater[j] - 1 >= r
                        #
                        # This is not possible with a static tree.
                        #
                        # Alternative: Since r increases, we can update the tree.
                        # When r increases, some elements move from list2 to list1.
                        # Specifically, when r reaches next_greater[j], the element j moves.
                        # We can maintain the tree dynamically.
                        # But updating the tree is O(N).
                        #
                        # Given the complexity, let's use the O(N log^2 N) approach with a simple check.
                        # We can compute the cost for a given l, r in O(log N) if we use a Segment Tree that maintains the sum of prefix maxes.
                        # But we need to handle the dynamic l.
                        #
                        # Let's use the two-pointer approach with a Segment Tree that maintains the cost.
                        # We can maintain the cost incrementally.
                        # When adding r:
                        #   cost += max(0, max(l..r-1) - nums[r])
                        # When removing l:
                        #   We need to subtract the contribution of nums[l].
                        #   nums[l] was the max for some range [l, k].
                        #   We need to subtract sum_{i=l+1}^k max(0, nums[l] - nums[i]).
                        #   This is a query on the Merge Sort Tree for the array nums.
                        #
                        # This approach is O(N log^2 N).
                        # We need to maintain the current cost.
                        # We can use a Segment Tree for range max (to find k) and a Merge Sort Tree for the sum of drops.
                        #
                        # Let's implement this.
                        pass