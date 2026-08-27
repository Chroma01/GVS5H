class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        # dp_even[s] = max product for a non-empty subsequence with even length and alternating sum s
        # dp_odd[s] = max product for a non-empty subsequence with odd length and alternating sum s
        dp_even = {}
        dp_odd = {}
        
        for num in nums:
            # Create copies to avoid using the same number multiple times in one step
            new_dp_even = dp_even.copy()
            new_dp_odd = dp_odd.copy()
            
            # Option 1: Start a new subsequence with just num
            # This subsequence has length 1 (odd), so it goes to dp_odd
            ns = num
            np = num
            if np <= limit:
                if ns not in new_dp_odd or np > new_dp_odd[ns]:
                    new_dp_odd[ns] = np
            
            # Option 2: Extend an even-length subsequence by adding num
            # Adding num (at even index in subsequence) means: new_sum = s + num
            # The new subsequence has odd length, so goes to dp_odd
            for s, prod in dp_even.items():
                ns = s + num
                np = prod * num
                if np <= limit:
                    if ns not in new_dp_odd or np > new_dp_odd[ns]:
                        new_dp_odd[ns] = np
            
            # Option 3: Extend an odd-length subsequence by adding num
            # Adding num (at odd index in subsequence) means: new_sum = s - num
            # The new subsequence has even length, so goes to dp_even
            for s, prod in dp_odd.items():
                ns = s - num
                np = prod * num
                if np <= limit:
                    if ns not in new_dp_even or np > new_dp_even[ns]:
                        new_dp_even[ns] = np
            
            dp_even = new_dp_even
            dp_odd = new_dp_odd
        
        result = -1
        if k in dp_even:
            result = max(result, dp_even[k])
        if k in dp_odd:
            result = max(result, dp_odd[k])
        
        return result