class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        m = n - x + 1
        
        # Coordinate compression for BIT
        vals = sorted(list(set(nums)))
        rank_map = {v: i+1 for i, v in enumerate(vals)}
        M = len(vals)
        
        bit_freq = [0] * (M + 1)
        bit_sum = [0] * (M + 1)
        
        def update(i, df, ds):
            while i <= M:
                bit_freq[i] += df
                bit_sum[i] += ds
                i += i & (-i)
                
        def query(i):
            f, s = 0, 0
            while i > 0:
                f += bit_freq[i]
                s += bit_sum[i]
                i -= i & (-i)
            return f, s
            
        def find_kth(k):
            idx = 0
            for i in range(M.bit_length(), -1, -1):
                next_idx = idx + (1 << i)
                if next_idx <= M and bit_freq[next_idx] < k:
                    idx = next_idx
                    k -= bit_freq[idx]
            return idx + 1
            
        costs = [0] * m
        current_total_sum = 0
        
        # Initialize first window
        for i in range(x):
            r = rank_map[nums[i]]
            update(r, 1, nums[i])
            current_total_sum += nums[i]
            
        def get_cost():
            med_rank = find_kth((x + 1) // 2)
            med_val = vals[med_rank - 1]
            cnt_lo, sum_lo = query(med_rank)
            cnt_hi = x - cnt_lo
            sum_hi = current_total_sum - sum_lo
            return (med_val * cnt_lo - sum_lo) + (sum_hi - med_val * cnt_hi)
            
        costs[0] = get_cost()
        
        # Slide window
        for i in range(1, m):
            r_out = rank_map[nums[i-1]]
            update(r_out, -1, -nums[i-1])
            current_total_sum -= nums[i-1]
            
            r_in = rank_map[nums[i+x-1]]
            update(r_in, 1, nums[i+x-1])
            current_total_sum += nums[i+x-1]
            
            costs[i] = get_cost()
            
        # DP to select k non-overlapping windows
        INF = float('inf')
        dp = [[INF] * (m + 1) for _ in range(k + 1)]
        for i in range(m + 1):
            dp[0][i] = 0
            
        for j in range(1, k + 1):
            for i in range(1, m + 1):
                dp[j][i] = dp[j][i-1]
                if i >= x:
                    if dp[j-1][i-x] != INF:
                        dp[j][i] = min(dp[j][i], dp[j-1][i-x] + costs[i-1])
                        
        return dp[k][m]