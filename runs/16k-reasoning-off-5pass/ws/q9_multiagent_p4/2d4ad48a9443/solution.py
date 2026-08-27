from typing import List

class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Stack stores tuples: (value, count, cost, original_val)
        # value: the value of the segment after operations
        # count: number of elements in this segment
        # cost: total operations to make this segment 'value' (relative to the start of the segment)
        # original_val: the original value of the leftmost element in this segment
        stack = []
        total_cost = 0
        left = 0
        count = 0
        
        for right in range(n):
            # Add nums[right] to the stack
            current_val = nums[right]
            current_count = 1
            current_cost = 0
            current_orig = current_val
            
            # Merge segments that are larger than current_val
            while stack and stack[-1][0] > current_val:
                v, c, c_cost, orig = stack.pop()
                # The cost to raise 'c' elements from 'orig' (or whatever they were) to 'v'
                # was already accounted for in c_cost. Now we raise them to 'current_val'.
                # The additional cost is c * (v - current_val).
                # Note: The 'orig' stored is the original value of the leftmost element of this segment.
                # The cost contribution of this segment to the total was c_cost.
                # After merging, the new cost for this merged segment (relative to the new base current_val)
                # is c_cost + c * (v - current_val).
                # However, we need to be careful. The 'c_cost' in the stack represents the cost to make
                # the segment 'v' given the previous context.
                # When we merge with a smaller value 'current_val', we are effectively saying:
                # "All these 'c' elements, which were previously raised to 'v', must now be raised to 'current_val'".
                # Wait, if v > current_val, we must raise current_val to v? No.
                # The stack maintains non-decreasing values. If we encounter a smaller value,
                # it means the previous larger values must be raised to match the current value?
                # No, that's for making the array non-decreasing by raising smaller elements.
                # If we have [10, 5], we raise 5 to 10. Cost 5.
                # Stack: [(10, 1, 0), (5, 1, 5)].
                # If we then see 8: [10, 5, 8]. 8 < 10. We raise 8 to 10. Cost 2.
                # Stack: [(10, 1, 0), (5, 1, 5), (8, 1, 7)].
                # But wait, the standard monotonic stack for this problem merges segments.
                # If we have [10, 5] -> Stack [(10, 2, 5)] (merged).
                # Then 8 comes. 8 < 10. We raise 8 to 10. Cost 2.
                # Stack [(10, 3, 7)].
                # The logic: If stack top > current, we pop and merge.
                # The cost added is c * (stack_top_val - current_val).
                # The new value of the merged segment is current_val? No, it's stack_top_val?
                # No, if we have [10, 5] and we see 8.
                # 10 > 8. We must raise 8 to 10? No, we must raise 5 to 10 (already done) and 8 to 10.
                # So the segment becomes [10, 10, 10]. Value 10.
                # So if stack top > current, we pop, add cost, and the new value is stack_top_val?
                # Yes, because the current element must be raised to match the larger previous element.
                # So the merged segment has value = stack_top_val.
                # But wait, if we have [5, 10] and see 8.
                # 10 > 8. Pop 10. Cost += 1*(10-8)=2.
                # Now stack has [5]. 5 < 8. Push 8.
                # Stack: [(5, 1, 0), (8, 1, 2)].
                # This represents [5, 10, 8] -> [5, 10, 10]. Cost 2.
                # Correct.
                
                # So the logic is:
                # While stack top > current_val:
                #   Pop (v, c, c_cost, orig)
                #   total_cost += c * (v - current_val)
                #   current_val = v  <-- The segment value becomes v (the larger one)
                #   current_count += c
                #   current_orig = orig (The leftmost original value remains the same)
                #   current_cost += c_cost (The cost to make the popped segment 'v' is added)
                
                # Wait, if we merge, the new segment has value 'v' (the popped one).
                # And the cost is c_cost + c * (v - current_val_new)?
                # Let's trace [10, 5, 8] again with this logic.
                # 1. Add 10: Stack [(10, 1, 0, 10)]. Total 0.
                # 2. Add 5: 10 > 5. Pop (10, 1, 0, 10).
                #    Cost += 1 * (10 - 5) = 5.
                #    Current val = 10. Count = 1 + 1 = 2. Orig = 10. Cost = 0 + 0 = 0?
                #    No, the cost of the merged segment is the sum of costs to make it 'v'.
                #    The popped segment cost was 0. The new element (5) needs to be raised to 10 (cost 5).
                #    So new cost = 0 + 5 = 5.
                #    Stack [(10, 2, 5, 10)]. Total 5.
                # 3. Add 8: 10 > 8. Pop (10, 2, 5, 10).
                #    Cost += 2 * (10 - 8) = 4.
                #    Current val = 10. Count = 2 + 1 = 3. Orig = 10. Cost = 5 + 4 = 9?
                #    Wait, manual calc for [10, 5, 8] is 7.
                #    My logic gave 9. Why?
                #    Because the cost to raise 5 to 10 is 5. The cost to raise 8 to 10 is 2. Total 7.
                #    In the stack, the segment (10, 2, 5) means: 2 elements, value 10, cost 5.
                #    When we add 8, we raise 8 to 10 (cost 2).
                #    So total cost should be 5 + 2 = 7.
                #    My formula `c * (v - current_val)` gave 2 * (10 - 8) = 4.
                #    Ah, `current_val` in the loop is the value we are trying to match.
                #    But if we merge, the new value is `v` (the popped value).
                #    So `current_val` becomes `v`.
                #    Then `c * (v - current_val)` is `c * (v - v) = 0`.
                #    This is wrong.
                #    The cost added is `c * (v - new_val)` where `new_val` is the value of the current element being processed?
                #    No. The current element is 8. The stack top is 10.
                #    We must raise 8 to 10. Cost 2.
                #    So the cost added is `1 * (10 - 8)`.
                #    But we also have 2 elements in the stack.
                #    The stack represents the prefix. The current element is the new one.
                #    If stack top > current, it means the current element is smaller than the max of the prefix.
                #    So we must raise the current element to the max.
                #    But wait, if we have [10, 5] -> [10, 10]. Max is 10.
                #    Now add 8. [10, 10, 8]. Max is 10. Raise 8 to 10.
                #    So the cost added is `1 * (10 - 8)`.
                #    But what if we have [10, 5, 12]?
                #    [10, 5] -> [10, 10]. Stack [(10, 2, 5)].
                #    Add 12. 12 > 10. No merge. Push (12, 1, 0).
                #    Stack [(10, 2, 5), (12, 1, 0)]. Total 5.
                #    Correct.
                #    What if we have [10, 5, 8, 9]?
                #    [10, 5] -> [(10, 2, 5)].
                #    Add 8. 10 > 8. Pop (10, 2, 5).
                #    Cost += 1 * (10 - 8) = 2. (Only the current element 8 is raised? No.)
                #    Wait, if we have [10, 5, 8], the cost is 7.
                #    My logic: Pop (10, 2, 5). Current val = 8.
                #    Cost += 1 * (10 - 8) = 2.
                #    New segment: value 10? No, if we raise 8 to 10, the segment becomes [10, 10, 10].
                #    So the new segment has value 10.
                #    Count = 2 + 1 = 3.
                #    Cost = 5 (from before) + 2 (for 8) = 7.
                #    So the logic is:
                #    While stack and stack[-1][0] > current_val:
                #        v, c, c_cost, orig = stack.pop()
                #        # We are raising the current element to v?
                #        # No, we are merging the current element into the segment of value v.
                #        # The current element is smaller, so it must be raised to v.
                #        # But wait, if we have multiple segments, say [(10, 2, 5), (12, 1, 0)].
                #        # And we add 8.
                #        # 12 > 8. Pop (12, 1, 0).
                #        # Cost += 1 * (12 - 8) = 4.
                #        # Current val = 12. Count = 1 + 1 = 2. Cost = 0 + 4 = 4.
                #        # Now stack top is 10. 10 < 12. Stop.
                #        # Push (12, 2, 4).
                #        # Stack: [(10, 2, 5), (12, 2, 4)]. Total 9.
                #        # Check [10, 5, 12, 8] -> [10, 10, 12, 12]. Cost 5 + 4 = 9. Correct.
                #        # So the logic is:
                #        # If stack top > current_val, we pop, and the current_val becomes the popped value?
                #        # No, the current_val becomes the popped value ONLY if we are merging the current element into the popped segment.
                #        # But if we have multiple segments, we might pop multiple.
                #        # Example: [10, 5, 12, 8, 7].
                #        # ... Stack [(10, 2, 5), (12, 2, 4)].
                #        # Add 7.
                #        # 12 > 7. Pop (12, 2, 4).
                #        # Cost += 2 * (12 - 7) = 10.
                #        # Current val = 12. Count = 2 + 1 = 3. Cost = 4 + 10 = 14.
                #        # Stack top 10 < 12. Stop.
                #        # Push (12, 3, 14).
                #        # Stack [(10, 2, 5), (12, 3, 14)]. Total 19.
                #        # Check [10, 5, 12, 8, 7] -> [10, 10, 12, 12, 12].
                #        # Cost: 5 (for 5->10) + 4 (for 8->12) + 5 (for 7->12) = 14?
                #        # Wait, 8->12 is 4. 7->12 is 5. Total 9. Plus 5 = 14.
                #        # My calc: 4 + 10 = 14. Correct.
                #        # So the logic is:
                #        # While stack and stack[-1][0] > current_val:
                #        #   v, c, c_cost, orig = stack.pop()
                #        #   total_cost += c * (v - current_val)
                #        #   current_val = v
                #        #   current_count += c
                #        #   current_cost += c_cost
                #        #   current_orig = orig
                #        # Push (current_val, current_count, current_cost, current_orig)
                
                # But wait, in the example [10, 5, 12, 8, 7], when we process 7:
                # Stack: [(10, 2, 5), (12, 2, 4)].
                # Pop (12, 2, 4). v=12, c=2, c_cost=4.
                # total_cost += 2 * (12 - 7) = 10.
                # current_val = 12.
                # current_count = 2 + 1 = 3.
                # current_cost = 4 + 10 = 14.
                # This implies the segment of 12s (size 2) and the new 7 (size 1) are merged into a segment of 12s (size 3).
                # And the cost to make them 12s is 14.
                # This is correct.
                
                # However, there is a catch.
                # If we have [10, 5] -> [(10, 2, 5)].
                # Add 12. 12 > 10. No pop.
                # Push (12, 1, 0).
                # Stack [(10, 2, 5), (12, 1, 0)].
                # Add 8.
                # 12 > 8. Pop (12, 1, 0).
                # total_cost += 1 * (12 - 8) = 4.
                # current_val = 12.
                # current_count = 1 + 1 = 2.
                # current_cost = 0 + 4 = 4.
                # Now stack top 10 < 12. Stop.
                # Push (12, 2, 4).
                # Stack [(10, 2, 5), (12, 2, 4)].
                # This is correct.
                
                # So the logic holds.
                v, c, c_cost, orig = stack.pop()
                total_cost += c * (v - current_val)
                current_val = v
                current_count += c
                current_cost += c_cost
                current_orig = orig # The leftmost original value of the merged segment is the same as the popped segment.
            
            # After merging, push the new segment
            stack.append((current_val, current_count, current_cost, current_orig))
            total_cost += current_cost # Wait, total_cost should be the sum of costs of all segments?
            # No, total_cost is the sum of costs of all segments in the stack.
            # But when we merge, we update `current_cost` which is the cost of the new segment.
            # And we add `c * (v - current_val)` to `total_cost`.
            # But `current_cost` already includes `c_cost` (from popped) and `c * (v - current_val)`.
            # So we should not add `current_cost` to `total_cost` again if we are maintaining `total_cost` incrementally.
            # Let's redefine `total_cost` as the sum of `c_cost` for all segments in the stack.
            # When we pop, we remove `c_cost` from `total_cost`.
            # When we push, we add `current_cost` to `total_cost`.
            # So:
            #   total_cost -= c_cost (remove popped)
            #   total_cost += current_cost (add new)
            #   But we also add `c * (v - current_val)` to the new segment's cost.
            #   So `current_cost = c_cost + c * (v - current_val)`.
            #   So `total_cost` update is correct.
            
            # Let's re-verify the `total_cost` update.
            # Initially `total_cost` = 0.
            # Add 10: Stack [(10, 1, 0, 10)]. total_cost = 0.
            # Add 5: Pop (10, 1, 0, 10). total_cost -= 0.
            #   current_val = 10, count = 2, cost = 0 + 1*(10-5)=5, orig=10.
            #   total_cost += 5.
            #   Stack [(10, 2, 5, 10)].
            # Add 8: Pop (10, 2, 5, 10). total_cost -= 5.
            #   current_val = 10, count = 3, cost = 5 + 2*(10-8)=9, orig=10.
            #   total_cost += 9.
            #   Stack [(10, 3, 9, 10)].
            # Total cost 9. Correct.
            
            # So the update logic is:
            #   total_cost -= c_cost
            #   ... merge ...
            #   total_cost += current_cost
            
            # But wait, in the loop, I did `total_cost += c * (v - current_val)`.
            # And `current_cost = c_cost + c * (v - current_val)`.
            # So `total_cost` should be updated as:
            #   total_cost -= c_cost
            #   total_cost += current_cost
            # Which is equivalent to `total_cost += c * (v - current_val)`.
            # So my previous code block was correct in terms of `total_cost` update.
            
            # Now, handle the removal from the left.
            # We need to remove `nums[left]`.
            # The leftmost element is at the bottom of the stack.
            # Let bottom = stack[0].
            # If bottom[1] > 1:
            #   We decrement count.
            #   The cost of this segment changes.
            #   The cost to make `c` elements `v` is `c_cost`.
            #   The cost to make `c-1` elements `v` is `c_cost - (v - bottom[3])`.
            #   Because `bottom[3]` is the original value of the leftmost element.
            #   And we raised it to `v`.
            #   So we subtract `(v - bottom[3])` from `total_cost`.
            #   And update `bottom[1] -= 1`.
            #   And `bottom[2] -= (v - bottom[3])`.
            # Else (count == 1):
            #   We pop the segment.
            #   Subtract `bottom[2]` from `total_cost`.
            #   If stack not empty, the new bottom segment's `original_val` is its own `original_val`.
            #   (No change to the new bottom segment's cost, because its cost is relative to the element before it, which is now the new bottom).
            #   Wait, if we pop the bottom segment, the new bottom segment's cost is unchanged?
            #   Yes, because the new bottom segment's cost is the cost to make it `v` given the element before it.
            #   The element before it is now the new bottom segment (which was previously the second segment).
            #   So its cost is unchanged.
            
            # So the removal logic:
            #   while total_cost > k:
            #       if not stack: break # Should not happen if total_cost > k and k >= 0
            #       v, c, c_cost, orig = stack[0]
            #       if c > 1:
            #           # Remove one element from this segment
            #           total_cost -= (v - orig)
            #           stack[0] = (v, c - 1, c_cost - (v - orig), orig)
            #           left += 1
            #       else:
            #           # Remove the entire segment
            #           total_cost -= c_cost
            #           stack.pop(0)
            #           left += 1
            #           # If stack is not empty, the new bottom segment's original_val is its own.
            #           # No need to update anything else.
            
            # Wait, there is a subtle issue.
            # If we have [(10, 2, 5, 10)] and we remove one element.
            # The segment becomes [(10, 1, 4, 10)].
            # The cost is 4.
            # The original value of the remaining element is... well, the segment represents [10, 5].
            # We remove 10. Remaining is 5.
            # The cost to make 5 into 10 is 5.
            # But my logic says cost becomes 4.
            # Why? Because `orig` is 10. `v - orig` = 0.
            # So `total_cost -= 0`.
            # But the cost should be 5?
            # No, if we remove 10, the remaining element is 5.
            # The cost to make it 10 is 5.
            # But wait, if we remove 10, the segment is just [5].
            # The cost to make it 10 is 5.
            # But the stack segment value is 10.
            # So the cost is 5.
            # My logic: `c_cost` was 5. `orig` was 10. `v - orig` = 0.
            # So `new_cost = 5 - 0 = 5`.
            # So it works.
            # What if the segment was [5, 10] -> [(10, 2, 5, 5)].
            # Remove 5. Remaining [10].
            # Cost to make 10 into 10 is 0.
            # My logic: `orig` = 5. `v - orig` = 5.
            # `new_cost = 5 - 5 = 0`.
            # Correct.
            
            # So the removal logic is correct.
            
            while total_cost > k:
                if not stack:
                    break
                v, c, c_cost, orig = stack[0]
                if c > 1:
                    total_cost -= (v - orig)
                    stack[0] = (v, c - 1, c_cost - (v - orig), orig)
                    left += 1
                else:
                    total_cost -= c_cost
                    stack.pop(0)
                    left += 1
            
            count += (right - left + 1)
        
        return count