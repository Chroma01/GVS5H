class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        OFFSET = 2000
        # dp[p][0] stores bitmask of reachable alternating sums for subsequences with product p and even length
        # dp[p][1] stores bitmask of reachable alternating sums for subsequences with product p and odd length
        dp = [[0, 0] for _ in range(limit + 1)]
        
        for x in nums:
            updates = []
            for p in range(limit + 1):
                m0, m1 = dp[p]
                if m0 == 0 and m1 == 0:
                    continue
                
                # Extend even-length subsequence (parity 0) -> adds x -> becomes odd-length (parity 1)
                if p * x <= limit:
                    updates.append((p * x, 1, m0 << x))
                # Extend odd-length subsequence (parity 1) -> subtracts x -> becomes even-length (parity 0)
                if p * x <= limit:
                    updates.append((p * x, 0, m1 >> x))
                # Start a new subsequence with x (length 1, odd parity)
                if x <= limit:
                    updates.append((x, 1, 1 << (x + OFFSET)))
                    
            for p_new, parity, mask in updates:
                dp[p_new][parity] |= mask
                
        target_bit = k + OFFSET
        # Check from largest product down to 0
        for p in range(limit, -1, -1):
            m0, m1 = dp[p]
            if 0 <= target_bit < 4000:
                if (m0 >> target_bit) & 1 or (m1 >> target_bit) & 1:
                    return p
        return -1