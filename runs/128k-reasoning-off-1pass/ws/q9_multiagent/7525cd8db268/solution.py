from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Sort pairs by start time. If start times are equal, sort by end time.
        intervals = []
        for a, b in conflictingPairs:
            u, v = min(a, b), max(a, b)
            intervals.append((u, v))
        
        intervals.sort()
        k = len(intervals)
        
        # Add dummy interval at the end to handle the case where no interval starts after some point
        # The dummy interval is (n+1, n+1) effectively meaning "no constraint" for i > n
        intervals.append((n + 1, n + 1))
        k += 1
        
        # Extract u and v arrays
        U = [x[0] for x in intervals]
        V = [x[1] for x in intervals]
        
        # Precompute suffix minimums M[j] = min(V[j], V[j+1], ..., V[k-1])
        M = [0] * k
        current_min = n + 1
        for j in range(k - 1, -1, -1):
            if V[j] < current_min:
                current_min = V[j]
            M[j] = current_min
            
        # Calculate initial total sum of f(i)
        # Sum = sum_{j=0}^{k-1} M[j] * (U[j] - U[j-1]) where U[-1] = 0
        total_sum = 0
        prev_u = 0
        for j in range(k):
            count = U[j] - prev_u
            if count > 0:
                total_sum += M[j] * count
            prev_u = U[j]
            
        # Precompute T[j] = M[j] * (U[j] - U[j-1]) and prefix sums
        T = [0] * k
        for j in range(k):
            count = U[j] - (U[j-1] if j > 0 else 0)
            T[j] = M[j] * count
            
        PrefT = [0] * (k + 1)
        for j in range(k):
            PrefT[j+1] = PrefT[j] + T[j]
            
        # Fenwick Tree (Binary Indexed Tree) to store max index p for a given value V[p]
        # We need to query max index p such that V[p] < X
        # BIT size needs to cover values up to n+1
        bit_size = n + 2
        bit = [0] * (bit_size + 1)
        
        def update_bit(idx, val):
            # idx is value v, val is index p
            # We want to store max p for a given v.
            while idx <= bit_size:
                if val > bit[idx]:
                    bit[idx] = val
                idx += idx & (-idx)
                
        def query_bit(idx):
            # max value in range [1, idx]
            res = 0
            while idx > 0:
                if bit[idx] > res:
                    res = bit[idx]
                idx -= idx & (-idx)
            return res
            
        max_total = total_sum
        
        # Iterate r from 0 to k-2 (since k-1 is dummy, we can't remove it)
        # We maintain the BIT with indices 0..r-1
        for r in range(k - 1):
            # Calculate l = max { p < r | V[p] < M[r+1] }
            limit_val = M[r+1] - 1
            if limit_val < 1:
                l = -1
            else:
                l = query_bit(limit_val)
            
            # Calculate gain from removing interval r
            # New sum = current_total - T[r] + sum_{j=l+1}^{r-1} (M[r+1] - M[j]) * (U[j] - U[j-1])
            # The sum part simplifies to: M[r+1] * (U[r-1] - U[l]) - (PrefT[r] - PrefT[l+1])
            
            gain = 0
            if l + 1 <= r - 1:
                # Range [l+1, r-1] is valid
                # U[r-1] - U[l] is the sum of (U[j] - U[j-1]) for j in [l+1, r-1]
                range_u_diff = U[r-1] - U[l]
                term1 = M[r+1] * range_u_diff
                subtract_term = PrefT[r] - PrefT[l+1]
                gain = term1 - subtract_term
            
            new_total = total_sum - T[r] + gain
            if new_total > max_total:
                max_total = new_total
            
            # Add current interval r to BIT for next steps
            update_bit(V[r], r)
            
        # The answer is max_total - n*(n+1)//2
        return max_total - n * (n + 1) // 2