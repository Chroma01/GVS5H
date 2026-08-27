from typing import List, Tuple, Optional

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Merge function for two intervals: (total, pref, suff, best)
        def merge(a: Optional[Tuple[int, int, int, int]], b: Optional[Tuple[int, int, int, int]]) -> Optional[Tuple[int, int, int, int]]:
            if a is None:
                return b
            if b is None:
                return a
            total = a[0] + b[0]
            pref = max(a[1], a[0] + b[1])
            suff = max(b[2], a[2] + b[0])
            best = max(a[3], b[3], a[2] + b[1])
            return (total, pref, suff, best)
        
        # Build segment tree
        size = 4 * n
        tree: List[Optional[Tuple[int, int, int, int]]] = [None] * size
        
        def build(node: int, l: int, r: int):
            if l == r:
                val = nums[l]
                tree[node] = (val, val, val, val)
            else:
                mid = (l + r) // 2
                build(node * 2, l, mid)
                build(node * 2 + 1, mid + 1, r)
                tree[node] = merge(tree[node * 2], tree[node * 2 + 1])
        
        build(1, 0, n - 1)
        
        def query(node: int, l: int, r: int, ql: int, qr: int) -> Optional[Tuple[int, int, int, int]]:
            if ql <= l and r <= qr:
                return tree[node]
            if qr < l or r < ql:
                return None
            mid = (l + r) // 2
            left = query(node * 2, l, mid, ql, qr)
            right = query(node * 2 + 1, mid + 1, r, ql, qr)
            return merge(left, right)
        
        # Original max subarray sum (no deletion)
        full_tuple = query(1, 0, n - 1, 0, n - 1)
        global_max = full_tuple[3]
        
        # Group indices by value
        val_to_indices: dict[int, List[int]] = {}
        for i, v in enumerate(nums):
            if v not in val_to_indices:
                val_to_indices[v] = []
            val_to_indices[v].append(i)
        
        # For each value, simulate deletion
        for v, indices in val_to_indices.items():
            if len(indices) == n:
                # Deleting this value would empty the array, not allowed
                continue
            
            # Collect segments (v-free blocks)
            segments: List[Tuple[int, int, int, int]] = []
            prev = -1
            for idx in indices:
                l = prev + 1
                r = idx - 1
                if l <= r:
                    seg_tuple = query(1, 0, n - 1, l, r)
                    if seg_tuple is not None:
                        segments.append(seg_tuple)
                prev = idx
            # Last segment after the last occurrence
            l = prev + 1
            r = n - 1
            if l <= r:
                seg_tuple = query(1, 0, n - 1, l, r)
                if seg_tuple is not None:
                    segments.append(seg_tuple)
            
            m = len(segments)
            if m == 0:
                continue
            
            # Compute max for this v
            max_k = max(seg[3] for seg in segments)
            if m == 1:
                current_max = max_k
            else:
                T = [seg[0] for seg in segments]
                P = [seg[1] for seg in segments]
                S = [seg[2] for seg in segments]
                # Prefix sums of T
                A = [0] * m
                A[0] = T[0]
                for i in range(1, m):
                    A[i] = A[i-1] + T[i]
                
                # Compute max spanning subarray: max_{i<j} (S_i - A_i) + A_{j-1} + P_j
                max_si_ai = S[0] - A[0]
                max_candidate = float('-inf')
                for j in range(1, m):
                    candidate = max_si_ai + A[j-1] + P[j]
                    if candidate > max_candidate:
                        max_candidate = candidate
                    val = S[j] - A[j]
                    if val > max_si_ai:
                        max_si_ai = val
                current_max = max(max_k, max_candidate)
            
            if current_max > global_max:
                global_max = current_max
        
        return global_max