import sys

def solve():
    import sys
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    P = [0] * (N + 1)  # 1-indexed
    for i in range(1, N + 1):
        P[i] = int(next(it))
    
    # pos_of_value[v] = original index where value v currently sits (1-indexed)
    pos_of_value = [0] * (N + 1)
    for i in range(1, N + 1):
        pos_of_value[P[i]] = i
    
    # Fenwick tree over original positions, 1 = available, 0 = already placed
    size = N + 2
    bit = [0] * size
    
    def add(idx, delta):
        while idx < size:
            bit[idx] += delta
            idx += idx & -idx
    
    def sum_(idx):
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & -idx
        return s
    
    # initially all positions are free
    for i in range(1, N + 1):
        add(i, 1)
    
    total_cost = 0
    for v in range(N, 0, -1):
        orig_pos = pos_of_value[v]
        # current rank of this position among remaining elements
        current_pos = sum_(orig_pos)  # number of free positions <= orig_pos
        # target position is v (1-indexed) among remaining elements
        # The cost is sum of the original indices of all elements it jumps over
        # which is equivalent to sum_{j = v}^{current_pos} (sum of original indices of the j-th remaining element)
        # But we can compute it as: for each position k from v to current_pos, 
        # find the original index of the element currently at rank k, and sum them.
        # We need a way to get the original index of the j-th remaining element.
        # That's a "find kth" operation on the BIT.
        # Actually, a smarter formula: the cost of moving value v left to its target
        # is the sum of original indices of all elements that are currently to its left
        # and have target index > v? No, let's re-derive carefully.
        
        # Let's think: we process values from N down to 1.
        # When we process v, all values > v are already placed at their correct positions.
        # So they occupy positions v+1, v+2, ..., N in the final sorted array.
        # But physically, in the current array, they might be scattered.
        # The standard approach: use a BIT to track the "shift" caused by removed elements.
        # For value v, its target index is v (1-indexed). 
        # We need to find the current index of v in the "compressed" array of remaining elements.
        # That's `current_pos = sum_(orig_pos)` (1-indexed rank).
        # The elements with rank < current_pos are those to the left of v.
        # When we move v left to rank v, we pass over (current_pos - v) elements.
        # But we also need to account for the fact that those elements are shifted right.
        # Actually, the cost is the sum of the left indices of the swaps.
        # When we swap element at rank r with element at rank r+1 (1-indexed ranks),
        # the cost is the "physical" position of the left element, which is... 
        # Wait, the cost is the index i in the original array, not the current rank.
        # Hmm, this is tricky.
        
        # Alternative view: The total cost equals the sum over all elements of the sum of
        # original indices of all elements that it jumps over.
        # When we move v left, it jumps over all elements currently between its target
        # and its current position. Those elements have some original indices.
        # We can find the set of elements between rank v and rank current_pos.
        # We need to sum their original indices.
        
        # So for each v, we need:
        # 1. current_pos = rank of v in the remaining sequence
        # 2. sum_orig = sum of original indices of all remaining elements with rank in [v, current_pos - 1]
        # Then cost_v = sum_orig - (v - 1) * (number of such elements)? No.
        
        # Let's think differently. 
        # The cost of moving an element from rank R to rank V (V < R) is:
        # It swaps left (R - V) times. 
        # At step 1, it's at some physical position, but the cost is i where i is the index in the array at that time.
        # This is complicated because as we swap, the physical positions change.
        
        # However, there's a known greedy solution: 
        # Process from N down to 1. For value v, its target is index v.
        # Find its current position pos. 
        # The elements to the left of pos are some set. 
        # When we move v left, it will jump over all elements currently between target v and pos.
        # The cost is the sum of the "target indices" of those elements? No.
        
        # Actually, looking at the problem, the cost to swap at position i (1-indexed) 
        # is i. This is independent of which elements are being swapped.
        # So the total cost is simply the sum of the left indices of all swaps performed.
        # In the greedy algorithm of moving v from its current position to v:
        # It performs swaps at positions v, v+1, ..., pos-1? Or is it the other way?
        # If v is at position pos, and we want to move it to position v (pos >= v),
        # we swap it left repeatedly. The first swap is at position pos-1 (swap P_{pos-1} and P_pos).
        # The cost is (pos-1). Then it's at position pos-1. Next swap at pos-2, cost pos-2.
        # ... until it's at position v. The last swap is at position v, swapping P_v and P_{v+1}.
        # So the total cost for v is sum_{k=v}^{pos-1} k = (v + pos-1)*(pos-v)/2.
        # But wait: when we perform these swaps, the elements between v and pos are shifted right by one.
        # Their physical positions increase by 1. But the cost of swapping v left is based on the 
        # positions before the swap, which are exactly v, v+1, ..., pos-1 in the current array 
        # (assuming we do the swaps sequentially).
        # However, when we later move other elements, the positions might have changed.
        # But since we process from N down to 1, once we place v, we don't touch it again.
        # And the elements that were shifted right are those with value < v? No, they could be any values.
        # Actually, all values > v are already placed. So the elements between v and pos in the current 
        # array must have values < v (since values > v are at their final positions > v).
        # Wait, that's not necessarily true. Values > v are already placed at positions > v in the final 
        # array, but in the current array they might be anywhere.
        # Let's reconsider.
        
        # Let's use the standard solution for this problem (AtCoder ABC problem).
        # The solution is: process from N down to 1. For each v from N to 1:
        #   Find the current position of v (using BIT to account for removed elements).
        #   The cost added is: sum of indices from v to current_pos (inclusive? or exclusive?)
        # Actually, the formula is: cost += (v + current_pos) * (current_pos - v + 1) // 2
        # But that's the sum of indices v, v+1, ..., current_pos.
        # Wait, let's check with sample: 3 2 1
        # Process v=3: current_pos = 1. cost = (1+3)*(3-1+1)/2 = 4*3/2 = 6? That's wrong.
        # The sample answer is 4.
        # So that formula is wrong.
        
        # Let's look at the actual greedy:
        # For v=3, it's at position 1. Target is 3. We need to move it right? No, target is 3, so we move it right.
        # Wait, in the sample, the operations were:
        # Swap P1 and P2 (cost 1) -> 2 3 1
        # Swap P2 and P3 (cost 2) -> 2 1 3
        # Swap P1 and P2 (cost 1) -> 1 2 3
        # So 3 was moved from position 1 to position 3. The cost was 1 + 2 = 3? No, 1+2=3.
        # Then 1 was moved from position 3 to position 1. The cost was 1.
        # Total = 4.
        # If we process from N down to 1:
        # v=3: current pos = 1. Target = 3. We move it right. Cost = sum of left indices of swaps when moving right.
        # When moving right, we swap with the element to the right. The cost is the left index of the swap.
        # So moving from pos to target (pos < target), we perform swaps at positions pos, pos+1, ..., target-1.
        # Cost = sum_{k=pos}^{target-1} k.
        # For v=3: pos=1, target=3. Cost = 1+2 = 3. Correct.
        # Then v=2: after moving 3, array is 2 1 3. v=2 is at pos=1. Target=2. Cost = 1.
        # Then v=1: at pos=2. Target=1. We need to move left. Cost = 1? But it's already at 2, target 1, so swap at position 1, cost 1. Total = 3+1+1=5? That's not 4.
        # Wait, after moving 3 to position 3, the array is 2 1 3.
        # Then we process v=2. It's at position 1. Target is 2. We move it right by 1. Cost = 1. Array becomes 1 2 3.
        # Then v=1: it's at position 1, target 1. No move.
        # Total cost: 1+2 (for moving 3) + 1 (for moving 2) = 4. Correct.
        # So the rule: when processing v from N down to 1:
        #   Find current position of v (call it cur).
        #   The target position is v.
        #   If cur <= v: need to move right. Cost = sum_{k=cur}^{v-1} k.
        #   If cur >= v: need to move left. Cost = sum_{k=v}^{cur-1} k.
        #   If cur == v: cost = 0.
        # This is equivalent to: |cur - v| choose 2? No.
        # Sum from a to b (inclusive) is (a+b)*(b-a+1)/2.
        # So:
        #   if cur < v: cost = (cur + v-1) * (v-cur) / 2
        #   if cur > v: cost = (v + cur-1) * (cur-v) / 2
        #   if cur == v: cost = 0
        # We can unify: cost = sum of integers from min(cur,v) to max(cur,v)-1.
        # Which is (min + max - 1) * (max - min) / 2.
        
        # Now, how to find cur (current position) efficiently?
        # We process values from N down to 1. When we process v, all values > v are already placed at their final positions.
        # So the current array consists of: values < v (not yet placed) and value v, in some order.
        # The positions of values > v are "removed" from consideration.
        # We can use a BIT over the original positions, initially all 1.
        # When we place a value, we set its original position to 0 in the BIT.
        # Then, for value v at original position orig, its current rank (1-indexed) is sum_(orig).
        # This rank is its current position in the sequence of remaining elements.
        # But wait: the target position is v. However, v is the 1-indexed target in the final sorted array.
        # In the current array of remaining elements, the target rank for value v is also v? 
        # Let's see: the remaining elements are exactly the values 1, 2, ..., v.
        # Their target final positions are 1, 2, ..., v.
        # So yes, the target rank in the remaining sequence is v.
        # So cur = sum_(orig_pos[v]).
        # Then we compute cost based on cur and v.
        # After computing, we add cost to total, and remove orig_pos[v] from BIT.
        
        # Let's test with sample 1: P = [3,2,1], N=3
        # pos: 1->3, 2->2, 3->1
        # BIT: [_,1,1,1]
        # v=3: orig_pos=1, cur=sum(1)=1. target=3. cur < v. cost = sum(1..2) = 1+2=3. total=3. remove pos 1: BIT [_,0,1,1]
        # v=2: orig_pos=2, cur=sum(2)=1+1=2? Wait, sum(2) = bit[2] + bit[0] = 1+0=1? No.
        # BIT initially: add 1 to 1,2,3. So bit[1]=1, bit[2]=1, bit[3]=1.
        # After remove pos 1: add(1, -1). So bit[1]=0, bit[2]=1, bit[3]=1.
        # For v=2, orig=2. cur = sum(2) = bit[2] + bit[0]? Actually, sum(2) goes: idx=2, s+=1, idx=0. So s=1.
        # So cur=1. target=2. cur < v. cost = sum(1..1) = 1. total=4. remove pos 2: BIT [_,0,0,1]
        # v=1: orig=3. cur = sum(3) = bit[3] = 1. target=1. cur=1, target=1. cost=0. total=4.
        # Correct!
        
        # Test sample 2: N=5, P=2 4 1 3 5
        # pos: 1->2, 2->1, 3->4, 4->3, 5->5
        # v=5: orig=5, cur=5. target=5. cost=0. remove 5.
        # v=4: orig=3, cur=sum(3). BIT has 1,2,3,4. sum(3)=3. target=4. cur<target. cost=sum(3..3)=3. total=3. remove 3.
        # v=3: orig=4, cur=sum(4). BIT now has 1,2,4. sum(4)=3. target=3. cur>target. cost=sum(3..2)=2+3=5? Wait, min=2, max=3, sum 2+3? Actually sum from 2 to 2? No.
        # cur=3, target=3. Wait, cur=3, target=3. cost=0. Let's recalc.
        # After removing 5 and 3, BIT has: pos1, pos2, pos4. sum(4) = 3. target=3. So cur=3, target=3. cost=0. total=3.
        # v=2: orig=1, cur=sum(1). BIT has pos1, pos2, pos4. sum(1)=1. target=2. cur<target. cost=sum(1..1)=1. total=4. remove 1.
        # v=1: orig=2, cur=sum(2). BIT has pos2, pos4. sum(2)=1. target=1. cur=1, target=1. cost=0. total=4.
        # But sample output is 6. So my calculation is wrong.
        # Let's re-examine. 
        # v=4: orig=3, cur=3. target=4. Cost should be moving 4 from pos 3 to pos 4. 
        # Array: 2 4 1 3 5. Move 4 right: swap pos 3 and 4. Cost = 3. Array becomes 2 1 4 3 5? Wait, swapping pos 3 and 4: 
        # 2 4 1 3 5 -> swap index 3 (1) and 4 (3) -> 2 4 3 1 5. That's not right.
        # We want to move 4 from index 2 to index 4. Wait, 4 is at index 2 in the original? 
        # Original: 2 4 1 3 5. So 4 is at index 2.
        # My pos array: P[1]=2, P[2]=4, P[3]=1, P[4]=3, P[5]=5.
        # So pos[4] = 2.
        # Let's redo carefully:
        # v=5: pos[5]=5. cur=5. target=5. cost=0. remove 5.
        # v=4: pos[4]=2. BIT has 1,2,3,4. sum(2)=2. target=4. cur=2 < 4. cost = sum(2..3) = 2+3=5. total=5. remove 2.
        # v=3: pos[3]=4. BIT has 1,3,4. sum(4)=3. target=3. cur=3. cost=0. total=5. remove 4.
        # v=2: pos[2]=1. BIT has 1,3. sum(1)=1. target=2. cur=1. cost=sum(1..1)=1. total=6. remove 1.
        # v=1: pos[1]=3. BIT has 3. sum(3)=1. target=1. cost=0. total=6.
        # That matches sample output 6!
        # So the algorithm is correct.
        
        # So we just need:
        # cur = sum_(orig_pos)
        # if cur < v: cost = (cur + v - 1) * (v - cur) // 2
        # elif cur > v: cost = (v + cur - 1) * (cur - v) // 2
        # else: cost = 0
        
        # And we need to sum these costs.
        
        cur = sum_(orig_pos)
        if cur < v:
            # sum from cur to v-1
            a = cur
            b = v - 1
            cnt = b - a + 1
            cost = (a + b) * cnt // 2
        elif cur > v:
            # sum from v to cur-1
            a = v
            b = cur - 1
            cnt = b - a + 1
            cost = (a + b) * cnt // 2
        else:
            cost = 0
        total_cost += cost
        add(orig_pos, -1)
    
    print(total_cost)

if __name__ == "__main__":
    solve()