
## ideation
We need minimum total cost to sort a permutation using adjacent swaps where swapping at index i (between positions i and i+1) costs i. The operation can be applied any number of times, and we can move elements left or right at varying costs. The cost depends on the index i where the swap occurs, not the values swapped. We must find a sequence of swaps with minimum total cost to achieve sorted order [1,2,...,N].

Observations:
- Swapping at index i costs i. So moving an element from position a to position b (with a<b) requires swaps at indices a, a+1, ..., b-1. The total cost is sum of those indices = (a + (b-1)) * (b-a) / 2. If a>b, moving left requires swaps at indices b, b+1, ..., a-1 with total cost sum of those indices.
- This is equivalent to: each element's final position can be decided. But movements affect each other because the array changes. However, we can think of it as: we can process elements in some order (e.g., from largest to smallest) and place them at their correct positions, treating already placed elements as "fixed" and the rest as a compressed sequence.
- If we decide the final order of all elements, the total cost might be computed by considering each swap's index cost each time it's used. But the problem allows us to choose any sequence of swaps.

Alternative viewpoint: We can use the idea of "inversions" but with weighted costs. When we swap adjacent elements at index i, we pay i. This is similar to bubble sort but with non-uniform costs.

We can consider building the sorted array by placing elements from largest to smallest. Suppose we have processed elements N, N-1, ..., v+1 and fixed them at their correct positions (at the right end). Now we need to place element v. It currently resides somewhere among the remaining (unplaced) elements. Let the number of unplaced elements to its left (including itself?) be its rank in the current compressed array. Actually, we need to find its current position in the "compressed" array of remaining elements. Then we move it to the front of the remaining (which corresponds to position v in the original array). The cost to move it from compressed position pos to the beginning of the compressed array is sum of indices of swaps performed along the way, but careful: the indices are original indices, not compressed indices.

Wait, if we remove placed elements, the original indices shift. But the cost of a swap depends on the current index i in the current array (not original). So when we compress, the cost of moving an element left by one step in the compressed array corresponds to swapping at some index i in the current array, which is not simply the compressed index.

However, note that when we place elements from largest to smallest, we are effectively fixing them at the end. After placing N, N-1, ..., v+1, the last (N-v) positions are occupied by v+1..N in correct order. The remaining elements (including v) are a permutation of 1..v occupying the first v positions, but not necessarily in order. To place v at position v, we need to bring v to the end of the remaining block (i.e., position v). In the current array, the remaining block occupies indices 1 to v. v is at some position pos in this block (1-indexed). To move v to the end of the block (position v), we need to swap it rightwards pos-1 steps? Actually if it's at position pos in the block, it needs to move to position v, so it needs to move right by v-pos steps. Each swap at index i costs i. But as we move v right, the indices of swaps are: starting at index pos, then pos+1, ..., v-1. So total cost = sum_{i=pos}^{v-1} i = (pos + v-1)*(v-pos)/2.

But is this always optimal? If we process from largest to smallest, we are making greedy choices. Is the problem equivalent to sorting by a series of adjacent swaps with position-dependent costs, and the greedy of placing largest first works? Let's test on small examples.

Sample 1: [3,2,1], N=3.
Process N=3: pos in remaining [3,2,1]? Actually we consider whole array. v=3: current position is 1. Remaining block initially is whole array (size 3). We need to move 3 to position 3. pos=1, v=3, cost = sum_{1}^{2} = 1+2=3. Remove it. Array becomes [2,1] with indices 1,2. v=2: pos=1, v=2, cost = sum_{1}^{1}=1. Remove. v=1: cost=0. Total=4. Matches.

Sample 2: N=5, P=[2,4,1,3,5].
v=5: pos=5, v=5, cost=0. Remove.
v=4: pos=2, v=4? Wait, after removing 5, array is [2,4,1,3] (size 4). 4 is at pos=2. We need to move it to position 4. Cost = sum_{2}^{3} = 2+3=5. Remove. Array: [2,1,3].
v=3: pos=3? [2,1,3] -> 3 is at pos=3. Move to pos=3? Wait v=3, so we need to place it at position 3. But the current block size is 3, and we need to move 3 to the end of the block (position 3). pos=3, so cost=0. Remove. Array: [2,1].
v=2: pos=1, move to pos=2, cost = sum_{1}^{1}=1. Remove. Array: [1].
v=1: pos=1, cost=0. Total = 5+1=6. Matches.

So this greedy works on samples. But is it always optimal? Let's think: The operation is swapping adjacent elements with cost equal to the left index of the swap. This is similar to sorting with weighted adjacent swaps where the weight of swapping at position i is i. The total cost of a sequence of swaps is the sum over each swap of its index at the time it's performed.

We can model this as: We have a permutation. We can perform any adjacent swap, each with cost equal to the current index of the left element. We want to sort with min cost.

This is equivalent to: For each inversion (i,j) with i<j and P_i > P_j, we need to resolve it by moving the larger element rightwards or smaller element leftwards. But the cost of a swap is independent of which elements are swapped, only the index. So the total cost depends on how many times each index is used for swapping.

If we think of the process as moving elements, each time an element moves past another, we incur a cost equal to the index where the swap occurs. But if we move an element from left to right, the swaps occur at increasing indices. If we move an element from right to left, the swaps occur at decreasing indices? Actually if we move an element leftwards (swap with left neighbor), the swap index is the left neighbor's index. So moving leftwards uses indices starting from the current position-1 down to the target index.

The greedy algorithm of placing elements from N down to 1 by moving them to their correct position (the end of the current unplaced block) seems to compute the cost as the sum of indices of the swaps that would bring that element to its final spot, assuming we don't disturb already placed elements. Since we place from largest to smallest, the placed elements are at the end and are larger than any remaining element. Moving a remaining element to the right only passes through other remaining elements (which are smaller). So the swaps only involve elements not yet placed. This suggests the greedy is optimal because placing larger elements first never harms the ability to place smaller ones later (since larger elements are "heavier" and we want to move them rightwards to their final positions, which are to the right of smaller elements anyway). And the cost to move a larger element rightwards is independent of smaller elements except that we pay the index costs.

More formally, we can prove that the optimal solution is to sort by moving elements from N down to 1 to their final positions, each time moving the element to the right end of the current unplaced prefix. Because any solution must eventually move each element to its correct position. For element v, it must cross all elements smaller than it that are initially to its left. Actually, element v must end up at position v. It may be moved left or right. The cost to move v from its initial position to v depends on the path. If we move it leftwards (if initially to the right of v), we pay costs at indices before v. If we move it rightwards (if initially to the left of v), we pay costs at indices after v. The greedy chooses the direction based on current position: if initially to the left of v, move right; if to the right, move left? Wait, in the greedy, we only move rightwards to the end of the unplaced block. But is it always optimal to move rightwards? Could moving leftwards be cheaper? Let's test a case: N=2, P=[2,1]. v=2 is at pos=1, needs to go to pos=2. Move right: cost 1. v=1 is at pos=1 (after removing 2, array is [1]), cost 0. Total 1. Alternative: move 1 left? It's already at pos=1? Actually 1 is at pos=2. To sort, we need to swap at index 1, cost 1. So same.

N=3, P=[1,3,2]. v=3 at pos=2, needs to go to pos=3. Move right: cost at index 2 = 2. v=2 at pos=3? Wait after removing 3, array is [1,2]? Actually we remove 3, array becomes [1,2]. v=2 is at pos=2, needs to go to pos=2, cost 0. Total 2. Alternatively, move 2 right? 2 is at pos=3, needs to go to pos=2 (leftwards). To move 2 left, swap at index 1? Actually moving 2 from pos 3 to pos 2 requires swap at index 2? Wait, if 2 is at position 3, to move it left to position 2, we swap P_2 and P_3, paying cost 2. Then array becomes [1,2,3]. Total cost 2. Same.

N=3, P=[2,1,3]. v=3 at pos=3, cost 0. Remove, array [2,1]. v=2 at pos=1, needs to go to pos=2, move right cost 1. Total 1. Alternative: move 1 right? 1 is at pos=2, needs to go to pos=1 (left), swap at index 1 cost 1. Total 1. Same.

N=4, P=[4,1,2,3]. Greedy: v=4 at pos=1, move right to pos=4, cost 1+2+3=6. v=3: after removing 4, array [1,2,3]. 3 at pos=3, cost 0. v=2: pos=2, cost 0. v=1: pos=1, cost 0. Total 6. Alternative: maybe we can move 1,2,3 leftwards? 1 is at pos=2, need pos=1, swap at index 1 cost 1. 2 at pos=3, need pos=2, swap at index 2 cost 2. 3 at pos=4, need pos=3, swap at index 3 cost 3. Total 6. Same.

What about P=[2,3,1]? N=3. Greedy: v=3 at pos=2, move right to pos=3, cost 2. Remove, array [2,1]. v=2 at pos=1, move right to pos=2, cost 1. Total 3. Alternative: move 1 left? 1 at pos=3, need pos=1. Move left: swap at index 2 (cost 2) and index 1 (cost 1) = 3. Then 2 is at pos=1? Actually after moving 1 left, array becomes [1,2,3]? Let's simulate: start [2,3,1]. Move 1 left: swap at index 2 (cost 2) -> [2,1,3]. Then swap at index 1 (cost 1) -> [1,2,3]. Total cost 3. Same.

It seems the total cost of moving an element from its initial position to its final position is fixed regardless of order, as long as we count the sum of indices where swaps occur involving that element. Actually, if we move an element v from position a to b (a<b), it must be swapped at indices a, a+1, ..., b-1. The total cost contributed by these swaps is sum_{i=a}^{b-1} i. This is independent of when we perform these swaps relative to other swaps, because the indices are determined by the positions where the swap occurs. However, if we perform other swaps in between, the indices might change because the array changes. But if we fix the path of element v, the set of indices where it participates in swaps is exactly the intervals between its current position and target position. The cost of each such swap is the index at the time. But if other elements move in between, the index where the swap occurs might be different. For example, moving an element rightwards through a block of smaller elements: the swaps occur at the current index of the element. If we move it step by step, each step's cost is the index of its current position. If we delay moving it, other elements might shift, but the total sum of indices where it swaps might change? Let's think carefully.

Suppose we have element v at position a. We want to move it to position b > a. If we do it immediately, we swap it rightwards: swap at a (cost a), then a+1 (cost a+1), ..., b-1 (cost b-1). Total sum = a + (a+1) + ... + (b-1) = (a + b-1)*(b-a)/2.

If we instead first move some other elements, the position of v might change. But eventually v must be at b. The number of times v is swapped with a neighbor to the right is at least b-a (if it only moves right). But could v move left then right? That would increase total swaps. Since we want minimum cost, we should move v monotonically in one direction? Not necessarily, but moving back and forth would only add extra swaps with positive cost, so never optimal. So v moves monotonically either left or right to its final position. If it moves right from a to b, the swaps occur at some indices. The sum of those indices might not be exactly the arithmetic sum if other elements intervene? Actually, each time v moves right by one, it swaps with the element immediately to its right. The cost of that swap is the current index of v. If v is at index i when it swaps, cost is i. As v moves right, its index increases by 1 each step. So the costs are exactly i, i+1, ..., up to b-1. But wait: if v is at index i, and it swaps with the element at i+1, v moves to i+1. The cost is i. So the sequence of costs is exactly the indices of v's positions before each swap. Since v starts at a, the first swap cost is a, then a+1, etc., until b-1. This is independent of any other swaps that might happen elsewhere, as long as v itself doesn't get swapped leftwards in between. But if v never moves left, its position is non-decreasing. If we do other swaps not involving v, v's index might change? No, v's index only changes when v itself is swapped. Other swaps between other elements don't change v's index. So if v only moves right, the costs are exactly a, a+1, ..., b-1. Similarly, if v moves left from a to b (a > b), the costs are a-1, a-2, ..., b (the indices of the left neighbor at each swap). Wait, moving left: v at a, swap with left neighbor at a-1, cost a-1. Then v at a-1, swap with left neighbor at a-2, cost a-2, ..., until v at b+1, swap with left neighbor at b, cost b. So total cost = (a-1) + (a-2) + ... + b = (b + a-1)*(a-b)/2.

Thus, for each element, if we know its starting position and final position, the minimum cost to move it is exactly the sum of indices along the path, assuming it moves monotonically. And we can achieve this by moving it directly to its final position without any other moves involving it. However, we must ensure that the path is not blocked by other elements that need to move in the opposite direction? Actually, if v moves right, it must cross all elements that are between a and b. Those elements are initially between a and b. If v moves right, it swaps with each of them. After v passes them, they are shifted left by one. If those elements also need to move right (they are smaller than v? Not necessarily), this might help or hinder. But in the greedy, we process from largest to smallest. When we move v rightwards, it crosses elements that are all smaller than v (since all larger are already placed at the end). Those smaller elements will eventually need to be placed in the left part. By moving v rightwards, we shift them left, which is good because they are supposed to be to the left of v. So this doesn't create conflicts.

The key insight: The total cost of the entire process is simply the sum over all elements of the cost to move them from their initial positions to their final positions, provided that the movement paths do not cross in a conflicting way (i.e., we can schedule the swaps so that the total cost is the sum of individual costs). But wait, when we perform swaps, each swap involves two elements. The cost of a swap is paid once. If element A moves right and element B moves left, and they cross each other, the swap between them is counted for both. But in our cost calculation for each element, we are summing the costs of swaps they participate in. If we just add the individual costs, we would be double-counting swaps that involve two moving elements. So we need to be careful: the total cost is the sum of costs of all swaps performed. Each swap is performed at a specific index and involves two elements. If both elements are moving, that swap's cost is shared. In our greedy, we are essentially computing the total cost of all swaps performed. When we move an element rightwards, we are performing swaps with the elements to its right. Those elements might also be moving later. The cost of those swaps is counted when we perform them. So the total cost is exactly the sum of the costs of the swaps we actually perform.

In the greedy algorithm (placing from N down to 1), the total cost computed as sum over v of cost to move v to position v (which is the sum of indices of swaps performed for v) is exactly the total cost of the sequence of swaps. Because when we move v, we only perform swaps involving v and the elements currently to its right (which are all unplaced). Since we process from largest to smallest, these unplaced elements are smaller than v, and we will later move them. The swaps we perform for v are distinct from the swaps we will perform for those smaller elements? Not necessarily: a smaller element might later be moved and perform swaps that cross other elements. But the swaps we did for v were at indices where v crossed those smaller elements. Later, when we move a smaller element, it might cross other smaller elements, but it will not need to cross v again because v is already placed at the end. So the swaps for v are not repeated. Thus, the total cost is indeed the sum of the costs of the moves for each v.

Therefore, the greedy algorithm is valid and optimal. The problem reduces to: we have an array. We repeatedly find the position of the largest remaining element, and add the cost of moving it to the end of the current array. Then we remove it. The cost of moving an element from its current position `pos` to the end of the array (which has current length `len`) is the sum of integers from `pos` to `len-1`. Wait, careful: When we say "end of the current array", we mean the position equal to the number of remaining elements? Actually, if we have processed elements > v, the remaining block is of size v. The target position for v is position v in the original array, which is the last position of the remaining block. So the current length of the remaining block is v. The element v is at some position `pos` within this block (1-indexed). We need to move it to position v. The number of swaps is v - pos. The swaps occur at indices: the current global index of the element, which is exactly its position in the current array? Wait, if we have removed some elements from the end, the array is shorter. The indices of the remaining elements are 1 to v. So the cost to move v from pos to v is sum_{i=pos}^{v-1} i. This is correct.

So the algorithm is:
Initialize a Fenwick tree or BIT to represent the current array. We can support:
- Find the position of a value (we need to find where the element v currently is in the compressed array).
- Remove an element at a given position (so future queries for positions to the left of removed elements adjust).

We can process v from N down to 1:
- Find the current position of v in the BIT. Let this be `pos` (1-indexed in the current compressed array). The current length of the compressed array is v.
- The cost to move v to position v is sum_{i=pos}^{v-1} i = (pos + (v-1)) * (v - pos) / 2.
- Add this to total cost.
- Remove v from its position.

But we need to find the position of v quickly. We can maintain an array `pos` of size N+1, storing the current position (in the compressed array) of each value. Initially, `pos[v] = index of v in original P`. When we remove an element at position p, all elements to the right of p shift left by 1. So their positions decrease by 1. We can maintain a BIT where we can query the number of alive elements before a given original index, but here we need the compressed position. Alternatively, we can use a BIT to find the current position by value: we know the original index of v, and we can query how many alive elements are to its left. That gives its 0-indexed position in the compressed array. Then pos = that + 1.

So we need a BIT that supports:
- Remove an element at original index idx (set to 0).
- Query: given an original index idx, return the number of alive elements strictly before it. (0-indexed rank - 1).

We also need to find the original index of v. We can precompute an array `where[v] = original index of v`.

Algorithm:
1. Read N and P.
2. Build array `where[1..N]` such that where[P[i]] = i.
3. Initialize BIT of size N with all 1s.
4. For v from N down to 1:
   a. orig_idx = where[v].
   b. pos = BIT.query(orig_idx)  // number of alive elements before orig_idx, so if we want 1-indexed position, pos = BIT.query(orig_idx) + 1? Actually BIT.query(i) returns sum[1..i]. If we want the number of alive elements before orig_idx, it's BIT.query(orig_idx - 1). Then the 1-indexed rank is BIT.query(orig_idx - 1) + 1. But we can also just get BIT.query(orig_idx) and since the element at orig_idx is alive, BIT.query(orig_idx) is the 1-indexed position. So pos = BIT.query(orig_idx).
   c. The current size of the alive set is v. (Because we have removed N, N-1, ..., v+1, so v elements remain.)
   d. Cost addition: sum_{i=pos}^{v-1} i.
   e. Remove v: BIT.update(orig_idx, -1).
5. Print total cost.

We must be careful: The BIT query returns the prefix sum. Initially, BIT[i] = 1 for all i. So BIT.query(orig_idx) gives the number of alive elements up to orig_idx, which is exactly its 1-indexed position in the current alive array. When we remove an element, we update -1, and future queries will be adjusted.

Let's test on sample 1:
N=3, P=[3,2,1]. where[3]=1, where[2]=2, where[1]=3.
BIT initially: [1,1,1].
v=3: orig_idx=1, pos=BIT.query(1)=1. v=3. Cost = sum_{1}^{2} i = 1+2=3. Remove 3 at idx 1: BIT.update(1,-1). BIT becomes [0,1,1].
v=2: orig_idx=2, pos=BIT.query(2)= (0+1)=1? Wait BIT.query(2) = sum[1..2] = 0+1=1. So pos=1. v=2. Cost = sum_{1}^{1} i = 1. Remove 2 at idx 2: BIT.update(2,-1). BIT becomes [0,0,1].
v=1: orig_idx=3, pos=BIT.query(3)=1. v=1. Cost = sum_{1}^{0} = 0. Total = 4. OK.

Sample 2: N=5, P=[2,4,1,3,5]. where[2]=1, where[4]=2, where[1]=3, where[3]=4, where[5]=5.
BIT: [1,1,1,1,1].
v=5: orig=5, pos=5. Cost=0. Remove 5.
BIT: [1,1,1,1,0].
v=4: orig=2, pos=BIT.query(2)=2? BIT.query(2) = 1+1=2. v=4? Wait v=4, but current size is 4? Actually we removed 5, so remaining size is 4. v=4, so cost = sum_{2}^{3} i = 2+3=5. Remove 4 at idx 2. BIT.update(2,-1). BIT: [1,0,1,1,0].
v=3: orig=4, pos=BIT.query(4) = 1+0+1+1 = 3. v=3. Cost = sum_{3}^{2} = 0. Remove 3 at idx 4. BIT.update(4,-1). BIT: [1,0,1,0,0].
v=2: orig=1, pos=BIT.query(1)=1. v=2. Cost = sum_{1}^{1}=1. Remove 2 at idx 1. BIT: [0,0,1,0,0].
v=1: orig=3, pos=BIT.query(3)=1. v=1. Cost 0. Total 6. OK.

The algorithm is O(N log N) and works.

Now, we need to handle large N (2e5). The cost can be large. Maximum cost: if P is reverse sorted [N, N-1, ..., 1], then for v=N, pos=1, cost = sum_{1}^{N-1} i = N(N-1)/2. For v=N-1, pos=1 (after removing N), cost = sum_{1}^{N-2} i = (N-1)(N-2)/2. Total sum = sum_{k=1}^{N-1} k(k+1)/2? Let's compute: sum_{v=1}^{N} (v-1)v/2 = 1/2 sum (v^2 - v) = 1/2 (N(N+1)(2N+1)/6 - N(N+1)/2) = N(N+1)(2N+1)/12 - N(N+1)/4 = N(N+1)(2N+1 - 3)/12 = N(N+1)(2N-2)/12 = N(N+1)(N-1)/6. For N=2e5, this is about (2e5)^3 / 6 = 8e15/6 = 1.33e15, which fits in 64-bit integer (max ~9e18). So we need to use Python's int (which is arbitrary precision) or 64-bit. In Python, int is fine.

Edge case: N=2, sorted, cost 0. Our loop: v=2: pos=2, cost 0. v=1: pos=1, cost 0. OK.

Now, we must code the BIT. Simple class with update and query.

But wait: Is the greedy always optimal? Let's think of a potential counterexample. Consider N=4, P=[2,1,4,3]. Greedy:
v=4: pos=3? Actually P: idx1=2, idx2=1, idx3=4, idx4=3. where[4]=3, where[3]=4.
v=4: pos=BIT.query(3)=3. v=4, cost = sum_{3}^{3}=3. Remove 4.
BIT: [1,1,0,1].
v=3: orig=4, pos=BIT.query(4)= 1+1+0+1=3. v=3, cost = sum_{3}^{2}=0. Remove 3.
BIT: [1,1,0,0].
v=2: orig=1, pos=1. v=2, cost = sum_{1}^{1}=1. Remove 2.
BIT: [0,1,0,0].
v=1: pos=1, cost 0. Total = 4.
Alternative: swap 1 and 2 at index 1 (cost 1) -> [1,2,4,3]. Then swap 3 and 4 at index 3 (cost 3) -> [1,2,3,4]. Total 4. Same.
What about P=[3,1,2]? N=3.
v=3: pos=1, cost=1+2=3. Remove 3 -> [1,2].
v=2: pos=2? where[2]=3. BIT after remove 3: [1,1,1] -> remove idx1? Actually P=[3,1,2], where[3]=1, where[1]=2, where[2]=3. Remove 3 at idx1: BIT: [0,1,1]. v=2: orig=3, pos=BIT.query(3)=1+1=2. v=2, cost=0. Total 3.
Alternative: move 1 left? 1 is at idx2, need idx1, swap cost 1. Then 2 is at idx3, need idx2, swap cost 2. Total 3. Same.
What about P=[1,3,2]? Greedy: v=3: pos=2, cost=2. Remove -> [1,2]. v=2: pos=2, cost=0. Total 2. Alternative: move 2 left: cost 2. Same.

It seems the total cost is always the sum of the "displacement" costs, and the greedy just sums them in a convenient order. Actually, the cost to move an element from its initial position to its final position is determined solely by its initial and final positions, as argued, if it moves monotonically. But in any sorting, each element must end at its sorted position. The sum over all elements of the cost to move them from their initial positions to their final positions (if each moves monotonically) might be greater than the actual minimum cost because moving one element might cause another to move in the same direction, and we can share some swaps? Wait, if we move element A rightwards and element B rightwards, and B is initially to the right of A, then moving A rightwards might push B further right, so B's total displacement might be less? Actually, if we process from largest to smallest, we are moving larger elements rightwards past smaller elements. This is exactly the same as if each smaller element moves leftwards relative to the larger ones. The total number of swaps performed is the number of inversions? Not exactly, because each swap has a cost that depends on the index. But if we think of the final sorted array, each pair of elements that are inverted in the original permutation must be swapped an odd number of times. The minimum number of swaps to sort a permutation is the number of inversions (each adjacent swap fixes exactly one inversion). But here, each swap has a cost. The total cost of a sequence of adjacent swaps is the sum of the indices where the swaps occur. If we simply do bubble sort, we would perform a swap for each inversion. The cost of each swap depends on when it occurs. If we process from right to left (moving elements to their correct positions), we can minimize the indices? Actually, moving larger elements rightwards uses larger indices, which are more expensive. Moving smaller elements leftwards uses smaller indices, which are cheaper. So to minimize cost, we should move smaller elements leftwards rather than larger elements rightwards? But the problem is symmetric? Wait, the cost of swapping at index i is i, regardless of which elements are swapped. So if we have an inversion between a large element on the left and a small element on the right, we can either move the large element rightwards (incurring costs at larger indices) or move the small element leftwards (incurring costs at smaller indices). Clearly, moving the small element leftwards is cheaper because the indices are smaller. But in the greedy from N down to 1, we are moving the large elements rightwards! That would be suboptimal if we have a choice. But wait, the greedy moves the large element to the end of the current array, which might require it to cross many small elements. The cost is high. Could we instead move the small elements leftwards past the large element, achieving the same final state but with lower total cost? Let's test.

Consider an inversion: large element L at position i, small element S at position j (i < j). To fix the inversion, we can either move L rightwards past S, paying cost at index i, i+1, ..., j-1. Or move S leftwards past L, paying cost at index i, i+1, ..., j-1? Wait, moving S leftwards: S is at j, to move to i, it must swap with elements at j-1, j-2, ..., i. The costs are at indices i, i+1, ..., j-1. So the cost is exactly the same! The sum of indices from i to j-1 is the same regardless of which element moves. So the cost of resolving an inversion is symmetric. However, the order of resolving multiple inversions matters because resolving one inversion might change the indices of others. But the sum of costs for a single inversion is fixed: if two elements are at positions a and b (a < b) and need to be in opposite order, the cost to fix that inversion (by moving one past the other) is the sum of indices from a to b-1. But note that the indices are the original positions if we do it without any other moves. If we move other elements in between, the indices might change. So the total cost is not simply the sum over inversions of the sum of their original position intervals. The greedy algorithm computes a specific total cost. Is it the minimum possible? The problem is known: AtCoder ABC 224 F? No, this looks like AtCoder ABC 224 D? Actually, I recall a similar problem: "Swapping" with cost equal to index. The solution is exactly this greedy with Fenwick tree. So it is correct.

Let's confirm with a more complex example. N=4, P=[4,3,2,1].
Greedy:
v=4: pos=1, cost=1+2+3=6. Remove 4.
v=3: pos=1 (in remaining [3,2,1]), cost=1+2=3. Remove.
v=2: pos=1, cost=1.
v=1: cost 0. Total 10.
Formula: N(N+1)(N-1)/6 = 4*5*3/6 = 10. OK.

Alternative: maybe we can do better? Let's try to sort manually. To sort [4,3,2,1], we can:
Swap 1 and 2 at index 2? Actually, we can move 1 leftwards: swap at index 3 (cost 3) -> [4,3,1,2]; swap at index 2 (cost 2) -> [4,1,3,2]; swap at index 1 (cost 1) -> [1,4,3,2]. Then move 2 left: swap at index 3 (cost 3) -> [1,4,2,3]; swap at index 2 (cost 2) -> [1,2,4,3]. Then move 3 left: swap at index 3 (cost 3) -> [1,2,3,4]. Total cost: 3+2+1 + 3+2 + 3 = 14. That's higher.
Another: move 4 left? 4 is at pos1, can't move left. Move 4 right: swap at 1 (1) -> [3,4,2,1]; swap at 2 (2) -> [3,2,4,1]; swap at 3 (3) -> [3,2,1,4]. Then move 3 right: swap at 2 (2) -> [2,3,1,4]; swap at 3 (3) -> [2,1,3,4]; then move 2 right: swap at 1 (1) -> [1,2,3,4]. Total: 1+2+3 + 2+3 + 1 = 12. Still higher than 10.
The greedy gave 10. Can we do 10? Let's see: greedy does: move 4 right: cost 1+2+3=6. Then move 3 right: cost 1+2=3. Then move 2 right: cost 1. So sequence: start [4,3,2,1]. Move 4 right: swap 1-2 (1) -> [3,4,2,1]; swap 2-3 (2) -> [3,2,4,1]; swap 3-4 (3) -> [3,2,1,4]. Now remove 4 (conceptually), we have [3,2,1]. Move 3 right: swap 1-2 (1) -> [2,3,1]; swap 2-3 (2) -> [2,1,3]. Now [2,1,3]. Move 2 right: swap 1-2 (1) -> [1,2,3]. Total cost: 1+2+3 + 1+2 + 1 = 10. So the greedy achieves 10, which is better than the other attempts. So greedy is optimal here.

Thus, the algorithm is correct.

Implementation details:
- N up to 2e5, O(N log N) is fine.
- BIT: we can use a list of size N+2 (1-indexed).
- Precompute where array.
- For each v from N to 1:
   pos = bit.query(where[v])  # 1-indexed position in current alive array
   # current size is v
   # cost = sum_{i=pos}^{v-1} i
   # Compute using arithmetic series: if pos <= v-1, (pos + v-1) * (v - pos) // 2 else 0.
   total += (pos + v - 1) * (v - pos) // 2
   bit.update(where[v], -1)

We need to be careful with the sum formula. The number of terms is (v - pos). The first term is pos, last term is v-1. Sum = (pos + v-1) * (v-pos) / 2. Since v-pos is integer, and pos + v-1 is integer, the product is even? Not necessarily, but in Python, integer division // 2 is fine.

Let's test with the samples and some random small cases against brute force to be absolutely sure. We can write a brute force for N <= 6 to check all permutations and verify the greedy gives the same cost as the true minimum. Since the operation is expensive to brute force (all sequences of adjacent swaps), we can compute the minimum cost by BFS or by the known property. But for now, we trust the greedy.

One more check: N=3, P=[2,1,3]. Greedy: v=3: pos=3, cost 0. v=2: pos=1, cost 1. Total 1. Correct.
N=3, P=[2,3,1]. Greedy: v=3: pos=2, cost 2. v=2: pos=1? Wait, after removing 3, array is [2,1]. v=2: pos=1, cost 1. Total 3. Let's see if we can do better. To sort [2,3,1], we can move 1 left: swap at 2 (cost 2) -> [2,1,3]; swap at 1 (cost 1) -> [1,2,3]. Total 3. Or move 3 right: swap at 2 (cost 2) -> [2,1,3]; then 2 right: swap at 1 (1) -> [1,2,3]. Total 3. So 3 is min.
N=3, P=[1,3,2]. Greedy: v=3: pos=2, cost 2. v=2: pos=2? After remove 3, array [1,2]. v=2 at pos=2, cost 0. Total 2. Can we do 2? Move 2 left: swap at 2 (cost 2) -> [1,2,3]. Yes.
N=4, P=[1,4,2,3]. Greedy:
where[4]=2, where[2]=3, where[3]=4, where[1]=1.
v=4: pos=2, cost = sum_{2}^{3} = 5. Remove 4 at idx2. BIT: [1,0,1,1].
v=3: orig=4, pos=BIT.query(4)=1+0+1+1=3. v=3, cost = sum_{3}^{2}=0. Remove 3 at idx4. BIT: [1,0,1,0].
v=2: orig=3, pos=BIT.query(3)=1+0+1=2. v=2, cost = sum_{2}^{1}=0. Remove 2 at idx3. BIT: [1,0,0,0].
v=1: pos=1, cost 0. Total 5.
Alternative: move 2 left? 2 at idx3, need idx2, swap at 2 (cost 2) -> [1,2,4,3]. Then 3 left: 3 at idx4, need idx3, swap at 3 (cost 3) -> [1,2,3,4]. Total 5. Same.
What about moving 4 right? 4 at idx2, need idx4: swap at 2 (2) -> [1,2,4,3]; swap at 3 (3) -> [1,2,3,4]. Total 5. Same.

Seems consistent.

Now, we must implement the solution. We'll write a Python script with a Fenwick tree class.

We need to handle input reading. The problem statement says "Read the inputs from stdin solve the problem and write the answer to stdout". We'll write a complete program.

Potential pitfalls:
- The cost sum formula: for v, pos can be equal to v, then v-pos=0, cost=0.
- The BIT query: we need to pass the original index. Since we use 1-indexed BIT, we store where[v] as 0-indexed or 1-indexed? Let's use 0-indexed for where array to match Python indexing, but BIT is 1-indexed. So we can store where[v] as the 0-based index, and when updating/querying BIT, we add 1. Or we can store 1-based. Let's store 0-based for array, and BIT uses indices 1..N. So in code:
  where = [0] * (N+1)
  for i in range(N): where[P[i]] = i  # 0-based
  Then BIT.update(i+1, -1) and BIT.query(i+1).
  pos = BIT.query(where[v] + 1)  # 1-indexed position in alive array.

- The cost sum: we need v as the current size. Since we loop v from N down to 1, the current size is exactly v. So that's fine.

- Total cost can be large, but Python handles big integers.

We should test with the provided samples.

Let's code.

We'll also add a main guard if needed, but the problem likely expects a script that reads from stdin and prints.

One more check: Is there any case where the greedy fails? Let's think about the proof. The problem is known as "Minimum Cost to Sort a Permutation with Swaps of Cost Equal to Index". Actually, there's a known result: the minimum cost is exactly the sum over all elements of the sum of indices they cross, but the greedy from largest to smallest gives the minimum. I'm confident.

We'll write the code now.

We'll include a BIT class:

class BIT:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n+1)
    def update(self, i, delta):
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i
    def query(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

Then the main logic.

Complexity: O(N log N) time, O(N) space.

We can also do this without a BIT by using a list and maintaining positions, but updating positions after removal would be O(N) per removal, so O(N^2) worst case. BIT is better.

Alternatively, we can use a segment tree or order statistics tree, but BIT is sufficient.

Let's double-check the formula: sum_{i=pos}^{v-1} i. If pos=1, v=4, sum=1+2+3=6. Formula: (1+3)*3//2 = 4*3//2=6. If pos=2, v=4, sum=2+3=5. Formula: (2+3)*2//2=5. If pos=3, v=4, sum=3. Formula: (3+3)*1//2=3. If pos=4, v=4, sum=0. Formula: (4+3)*0//2=0. Correct.

Now, we must ensure that the BIT query gives the correct 1-indexed position. Initially, BIT has 1 at every index. For a given original index i (0-based), we query i+1. The query returns the number of alive elements up to i, which is exactly its rank among alive elements. Since we haven't removed any yet, the rank is i+1. After some removals, the rank is the number of alive elements before it plus one. This matches the position in the compressed array.

One edge case: when we remove an element, we update its position. We must be careful to not query for a value that is already removed. Since we process from N down to 1, each value is removed exactly once, and we query it before removal. So it's fine.

We should also consider that the array P is a permutation, so all values 1..N appear exactly once.

Let's test with N=2e5 random permutation to ensure performance. BIT operations are fast.

Now, the plan is complete. We'll write the code accordingly.

We need to output the answer as an integer.

We can also write the code without a BIT by using a list of positions and updating them, but with a BIT it's straightforward.

Let's write the final solution.</mm:think>### NOTES
The problem asks for the minimum total cost to sort a permutation using adjacent swaps where swapping at index `i` costs `i`. The cost of moving an element from position `a` to `b` (with `a < b`) is the sum of indices `a + (a+1) + ... + (b-1)`, which equals `(a + b - 1) * (b - a) / 2`. Moving leftwards gives a symmetric sum.

A greedy strategy works optimally: process the values from `N` down to `1`. For each value `v`, find its current position in the "compressed" array of unplaced elements (initially the whole array, then the prefix of size `v`). Move `v` to the end of this compressed array (its final position `v`). The cost of this move is the sum of indices of the swaps performed. After placing `v`, remove it from the structure.

To find the current position of `v` efficiently, we can use a Fenwick tree (Binary Indexed Tree). We precompute the original index of each value. The BIT tracks which elements are still present (1 for present, 0 for removed). For a value `v`, its 1-indexed position in the compressed array is the prefix sum up to its original index. We then compute the cost using the arithmetic series formula and remove `v` by updating the BIT with -1.

This greedy is optimal because each element's movement cost is independent of the order in which we fix the other elements, and processing from largest to smallest ensures we never need to move a larger element past an already placed (larger) element. The total time complexity is O(N log N), which is suitable for N up to 2×10⁵.

## worker: Implement the solution in Python: define a Fenwick
The solution uses a Fenwick tree to maintain the positions of unplaced elements. For each value `v` from `N` down to `1`, we find its current rank among unplaced elements (which corresponds to its 1-indexed position in the compressed array). We then add the cost of moving it to the end of the current block (position `v`) using the arithmetic series sum formula. Finally, we remove the element by updating the tree. This greedy approach is optimal because processing larger elements first never increases the cost of placing smaller elements later. The time complexity is O(N log N).
