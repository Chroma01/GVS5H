class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Precompute total frequency of each number
        from collections import Counter
        total_freq = Counter(nums)
        
        # Left frequency map, initially empty
        left_freq = Counter()
        
        ans = 0
        
        # We'll iterate i from 0 to n-1, considering nums[i] as the middle element
        # Before processing i, left_freq has counts for nums[0:i]
        # right_freq should have counts for nums[i+1:n]
        # We can maintain right_freq by starting with total_freq and decrementing as we go
        
        right_freq = Counter(total_freq)
        
        for i in range(n):
            m = nums[i]
            
            # Update right_freq: remove current element m
            right_freq[m] -= 1
            if right_freq[m] == 0:
                del right_freq[m]
            
            # Number of elements to the left and right
            total_left = i
            total_right = n - 1 - i
            
            # If not enough elements on either side, skip
            if total_left < 2 or total_right < 2:
                # Update left_freq for next iteration
                left_freq[m] += 1
                continue
            
            cL = left_freq[m]
            cR = right_freq[m]
            
            # Calculate ways for left part: a = number of m's in the 2 chosen from left
            # a=0: choose 2 from non-m elements
            non_m_left = total_left - cL
            ways_left = [0, 0, 0]
            if non_m_left >= 2:
                ways_left[0] = non_m_left * (non_m_left - 1) // 2
            if cL >= 1 and non_m_left >= 1:
                ways_left[1] = cL * non_m_left
            if cL >= 2:
                ways_left[2] = cL * (cL - 1) // 2
            
            # Calculate ways for right part: b = number of m's in the 2 chosen from right
            non_m_right = total_right - cR
            ways_right = [0, 0, 0]
            if non_m_right >= 2:
                ways_right[0] = non_m_right * (non_m_right - 1) // 2
            if cR >= 1 and non_m_right >= 1:
                ways_right[1] = cR * non_m_right
            if cR >= 2:
                ways_right[2] = cR * (cR - 1) // 2
            
            # Valid cases: a + b >= 2
            # (0,2), (1,1), (1,2), (2,0), (2,1), (2,2)
            valid_ways = 0
            valid_ways += ways_left[0] * ways_right[2]
            valid_ways += ways_left[1] * ways_right[1]
            valid_ways += ways_left[1] * ways_right[2]
            valid_ways += ways_left[2] * ways_right[0]
            valid_ways += ways_left[2] * ways_right[1]
            valid_ways += ways_left[2] * ways_right[2]
            
            ans = (ans + valid_ways) % MOD
            
            # Update left_freq for next iteration
            left_freq[m] += 1
            
        return ans