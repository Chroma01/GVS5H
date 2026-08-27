from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        n = len(nums)
        # Maximum possible absolute alternating sum
        max_abs_sum = n * 12  # 150 * 12 = 1800
        OFFSET = max_abs_sum
        SUM_RANGE = 2 * max_abs_sum + 1  # indices 0..2*max_abs_sum
        
        # Initialize two layers: prev and curr
        # Each is a list of two lists (parity 0 and 1), each of length SUM_RANGE
        # Use -1 to indicate unreachable state
        prev = [[-1] * SUM_RANGE for _ in range(2)]
        # Empty subsequence: parity 0 (next element will be at even index), sum 0, product 1
        prev[0][OFFSET] = 1
        
        for idx, val in enumerate(nums):
            curr = [[-1] * SUM_RANGE for _ in range(2)]
            for parity in range(2):
                row = prev[parity]
                for s in range(SUM_RANGE):
                    prod = row[s]
                    if prod == -1:
                        continue
                    # Option 1: skip nums[idx]
                    if curr[parity][s] < prod:
                        curr[parity][s] = prod
                    # Option 2: take nums[idx]
                    # New parity flips
                    new_parity = 1 - parity
                    # New sum: add if current parity is 0 (even), subtract if 1 (odd)
                    if parity == 0:
                        new_s = s + val
                    else:
                        new_s = s - val
                    # Check bounds
                    if new_s < 0 or new_s >= SUM_RANGE:
                        continue
                    # Compute new product
                    if val == 0:
                        new_prod = 0
                    else:
                        # prod could be 0 (from previous zeros) or positive
                        if prod == 0:
                            new_prod = 0
                        else:
                            new_prod = prod * val
                    # Only keep if product <= limit
                    if new_prod <= limit:
                        if curr[new_parity][new_s] < new_prod:
                            curr[new_parity][new_s] = new_prod
            prev = curr
        
        # After processing all elements, check both parities for sum = k
        target = k + OFFSET
        if target < 0 or target >= SUM_RANGE:
            return -1
        best = -1
        for parity in range(2):
            p = prev[parity][target]
            if p != -1 and p > best:
                best = p
        return best if best != -1 else -1


# ----------------- Testing the implementation -----------------
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    nums1 = [1, 2, 3]
    k1 = 2
    limit1 = 10
    print("Example 1:", sol.maxProduct(nums1, k1, limit1))  # Expected: 6
    
    # Example 2
    nums2 = [0, 2, 3]
    k2 = -5
    limit2 = 12
    print("Example 2:", sol.maxProduct(nums2, k2, limit2))  # Expected: -1
    
    # Example 3
    nums3 = [2, 2, 3, 3]
    k3 = 0
    limit3 = 9
    print("Example 3:", sol.maxProduct(nums3, k3, limit3))  # Expected: 9
    
    # Additional edge cases
    # Single element equal to k
    print("Single [5], k=5, limit=10:", sol.maxProduct([5], 5, 10))  # 5
    
    # Single element, not matching k
    print("Single [5], k=3, limit=10:", sol.maxProduct([5], 3, 10))  # -1
    
    # All zeros, k=0
    print("[0,0,0], k=0, limit=1:", sol.maxProduct([0, 0, 0], 0, 1))  # 0
    
    # Mixed zeros
    print("[0,1,2], k=1, limit=5:", sol.maxProduct([0, 1, 2], 1, 5))
    # Subsequences with sum 1: [1] (product 1), [0,1] (product 0), [0,2,?]... 
    # Actually we need to think: [0,1] sum = 0-1 = -1, no. [0,1,2] = 0-1+2 = 1, product 0.
    # [1] product 1, [0,1,2] product 0, [0,2] = 0-2 = -2. [1,2] = 1-2 = -1.
    # So max product is 1.
    
    # Larger case
    nums4 = [1,1,1,1,1,1,1,1]
    k4 = 0
    limit4 = 100
    # 8 elements: subsequence of length 2 has sum 0 and product 1; length 4 product 1; etc.
    # All products are 1. So answer 1.
    print("Eight 1's, k=0, limit=100:", sol.maxProduct(nums4, k4, limit4))  # 1
    
    # Product limit reached
    nums5 = [2,3,4]
    k5 = 1
    limit5 = 10
    # [2,3] sum = 2-3 = -1, no. [3,4] sum = 3-4 = -1. [2,3,4] sum = 2-3+4 = 3, no.
    # [2,4] sum = 2-4 = -2. [2] sum=2, [3] sum=3, [4] sum=4.
    # Actually with k=1: [2,3,4] = 2-3+4=3, [2,3]= -1, [3,4] = -1, [2,4] = -2.
    # [4] =4. [2] =2. None gives 1? Actually [2,3,4] gives 3.
    # So no subsequence with sum 1? Let's see: [2,3] = -1, [2,4] = -2, [3,4] = -1, [2,3,4] = 3.
    # No single gives 1. So answer -1.
    print("[2,3,4], k=1, limit=10:", sol.maxProduct(nums5, k5, limit5))  # -1
    
    # Negative k reachable
    nums6 = [5, 3, 2]
    k6 = -1
    limit6 = 100
    # [5,3] = 5-3 = 2, [5,2] = 5-2=3, [3,2] = 3-2=1, [5,3,2] = 5-3+2=4.
    # No -1. So -1.
    print("[5,3,2], k=-1, limit=100:", sol.maxProduct(nums6, k6, limit6))  # -1
    
    # Product exceeds limit, find next best
    nums7 = [4, 4, 4]
    k7 = 4
    limit7 = 30
    # [4] sum=4, prod=4; [4,4] sum=4-4=0; [4,4,4] sum=4-4+4=4, prod=64>30.
    # [4,4] sum=0 no. [4,4,4] prod too big. So only [4] works, product 4.
    print("[4,4,4], k=4, limit=30:", sol.maxProduct(nums7, k7, limit7))  # 4
    
    # Larger product within limit
    nums8 = [3, 2, 3, 2]
    k8 = 0
    limit8 = 100
    # [3,3] sum=0 prod=9; [2,2] sum=0 prod=4; [3,2,3,2] sum=3-2+3-2=2 no.
    # [3,2,3] sum=3-2+3=4; [2,3,2] sum=2-3+2=1.
    # [3,2] sum=1; [2,3] sum=-1.
    # Actually [3,3] product 9, [2,2] product 4. So max is 9.
    print("[3,2,3,2], k=0, limit=100:", sol.maxProduct(nums8, k8, limit8))  # 9
    
    # Edge: limit = 1
    print("[1,1,1], k=1, limit=1:", sol.maxProduct([1,1,1], 1, 1))  # 1 (any single 1)
    
    # Edge: large n
    nums9 = [1] * 150
    k9 = 1
    limit9 = 5000
    # Pick single 1: sum 1, product 1. Pick two: sum 0. So 1.
    print("150 ones, k=1, limit=5000:", sol.maxProduct(nums9, k9, limit9))  # 1
    
    # Mix to get product exactly limit
    nums10 = [5, 4, 2]
    k10 = 1
    limit10 = 40
    # [5,4] sum=1 prod=20; [5,2] sum=3; [4,2] sum=2; [5,4,2] sum=5-4+2=3.
    # [5] sum=5. [4] sum=4. [2] sum=2. No 1? Actually [5,4] gives 1, product 20.
    # That's the only one with sum 1? Let's see [5,2,?] no. So 20.
    print("[5,4,2], k=1, limit=40:", sol.maxProduct(nums10, k10, limit10))  # 20