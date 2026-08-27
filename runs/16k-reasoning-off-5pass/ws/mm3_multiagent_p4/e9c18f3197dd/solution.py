from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        n = len(nums)
        t_len = len(target)
        full_mask = (1 << t_len) - 1
        
        INF = 10**18
        
        # prev[mask] = minimum cost to achieve mask using processed elements
        prev = [INF] * (1 << t_len)
        prev[0] = 0  # no targets satisfied, zero cost
        
        for i in range(n):
            # start cur as a copy of prev (skip case is handled by copying)
            cur = prev[:]  # copying ensures we read from previous i-1 state
            
            # Now consider using nums[i] to satisfy some target t
            # Read from prev (state BEFORE element i) to avoid using updated cur values
            for mask in range(1 << t_len):
                if prev[mask] == INF:
                    continue
                # Try to assign an unassigned target t to this nums[i]
                for t in range(t_len):
                    if mask & (1 << t):
                        continue  # already satisfied
                    new_mask = mask | (1 << t)
                    # Cost to make nums[i] a multiple of target[t]
                    r = nums[i] % target[t]
                    cost = 0 if r == 0 else target[t] - r
                    new_cost = prev[mask] + cost
                    if new_cost < cur[new_mask]:
                        cur[new_mask] = new_cost
            prev = cur
        
        return prev[full_mask]


# Test harness
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    print("Example 1:", sol.minimumIncrements([1, 2, 3], [4]))  # Expected: 1
    
    # Example 2
    print("Example 2:", sol.minimumIncrements([8, 4], [10, 5]))  # Expected: 2
    
    # Example 3
    print("Example 3:", sol.minimumIncrements([7, 9, 10], [7]))  # Expected: 0
    
    # Edge case: target already a multiple
    print("Already multiple:", sol.minimumIncrements([5, 10, 15], [5]))  # Expected: 0
    
    # Edge case: duplicate target values
    print("Duplicate targets:", sol.minimumIncrements([3, 6], [5, 5]))  # Expected: 4 (both targets can share one nums[1]=6 if we raise 3 to 5, cost=2; but need both, so 3->5(2), 6 already multiple of 5? 6%5=1, need 5, cost=4; better: 6->10 cost=4, 3->5 cost=2 total=6; or 3->5 cost=2 and 6->10 cost=4 => 6. Actually 3->5(2) and 6 stays: 6%5=1 not multiple. 6->5? no decrease. So min is 6.)
    # Let me recalculate duplicate: targets [5,5], nums [3,6].
    # Options:
    #   Assign both to 3: 3->5 (cost 2) and 3->10 (cost 7) = 9
    #   Assign both to 6: 6->5 (impossible), 6->5 (impossible) actually need to go to multiples of 5: 6->10 (cost 4) for both = 8? No, same element can't be incremented twice.
    #   Assign first to 3 (3->5 cost 2), second to 6 (6->10 cost 4) = 6
    #   Assign first to 6 (6->10 cost 4), second to 3 (3->5 cost 2) = 6
    # So answer is 6.
    
    # Edge case: single target, single element
    print("Single single:", sol.minimumIncrements([7], [5]))  # 7->10 cost 3
    
    # Edge case: need to increase one element to cover multiple targets
    print("One element covers multiple:", sol.minimumIncrements([4], [6, 9]))  # 4->12 (cost 8) covers 6 and 9? 12%6=0, 12%9=3 no. 4->18 (cost 14) covers both. 4->6 (cost 2) covers 6, 4->9 (cost 5) covers 9, total 7. So 7.
    
    # Edge case: large nums
    print("Large nums:", sol.minimumIncrements([100, 200], [150]))  # 100->150 cost 50, 200 already? 200%150=50, need 100, cost 100. Min 50.
    
    # Verify duplicate test gives 6
    print("Duplicate targets retest:", sol.minimumIncrements([3, 6], [5, 5]))