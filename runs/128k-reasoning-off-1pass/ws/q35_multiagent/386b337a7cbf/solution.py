class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        # dp_even[s] = max product of a subsequence with alternating sum s and even length
        # dp_odd[s] = max product of a subsequence with alternating sum s and odd length
        dp_even = {}
        dp_odd = {}
        
        for x in nums:
            # We need to create new states based on current dp_even and dp_odd
            # to avoid using updated values in the same iteration
            
            # New states for dp_odd:
            # 1. Start a new subsequence [x]: length 1 (odd), sum = x, product = x
            # 2. Append x to an even-length subsequence: 
            #    new_sum = s + x, new_product = dp_even[s] * x
            
            new_odd_updates = {}
            
            # Start new subsequence
            if x <= limit:  # product must not exceed limit
                new_odd_updates[x] = x
            
            # Append to even-length subsequences
            for s, prod in dp_even.items():
                new_sum = s + x
                new_prod = prod * x
                if new_prod <= limit:
                    if new_sum not in new_odd_updates or new_odd_updates[new_sum] < new_prod:
                        new_odd_updates[new_sum] = new_prod
            
            # Update dp_odd with new_odd_updates
            for s, prod in new_odd_updates.items():
                if s not in dp_odd or dp_odd[s] < prod:
                    dp_odd[s] = prod
            
            # New states for dp_even:
            # 1. Append x to an odd-length subsequence:
            #    new_sum = s - x, new_product = dp_odd[s] * x
            # Note: We cannot start a new subsequence for dp_even because a single element
            # has odd length.
            
            new_even_updates = {}
            
            # Append to odd-length subsequences
            for s, prod in dp_odd.items():
                new_sum = s - x
                new_prod = prod * x
                if new_prod <= limit:
                    if new_sum not in new_even_updates or new_even_updates[new_sum] < new_prod:
                        new_even_updates[new_sum] = new_prod
            
            # Update dp_even with new_even_updates
            for s, prod in new_even_updates.items():
                if s not in dp_even or dp_even[s] < prod:
                    dp_even[s] = prod
                    
        # The answer is the max product in dp_even[k] or dp_odd[k]
        ans = -1
        if k in dp_even:
            ans = max(ans, dp_even[k])
        if k in dp_odd:
            ans = max(ans, dp_odd[k])
            
        return ans