
## ideation
The problem asks for the minimum total cost to sort a permutation by adjacent swaps, where swapping at index i costs i. The cost of a swap depends only on the left index of the swap. This is equivalent to finding a sequence of adjacent transpositions that sorts the permutation and minimizes the sum of the indices where the swaps occur.

Key observations:
- The cost of moving an element from position a to b (|a-b| steps) is the sum of indices between min(a,b) and max(a,b)-1, regardless of direction.
- Moving an element left uses smaller indices (cheaper), while moving it right uses larger indices (more expensive). Thus, it's generally beneficial to move elements left rather than right.
- However, moving a small element all the way to the left first can push the remaining unsorted elements to the right, increasing the indices of subsequent swaps. The optimal strategy balances left and right movements to keep the unresolved part as far left as possible.
- The total cost can be expressed as the sum over all inversions of the cost of the swap that resolves them, but the order of resolving inversions affects the indices.
- A known greedy approach: process elements in increasing order, but for each element, instead of always moving it left, we should move it left only as far as necessary, and sometimes it's better to move larger elements right first to keep the active region left-aligned.
- Actually, the problem can be solved by considering the "inversion" cost or by using a Fenwick tree to simulate the optimal process. A common solution for this problem (from AtCoder ARC) processes the permutation from right to left, maintaining the current "cost" or using a greedy that always performs the cheapest possible swap that reduces the number of misplaced elements.

Another perspective: each element needs to be placed at its correct position. The relative order of elements is fixed. We can think of the process as repeatedly taking the element that is currently at some position and moving it to its correct place. Because moving right is expensive, we want to minimize rightward moves. The optimal strategy is to process the permutation from right to left, and for each value, determine how many times it must be swapped right vs left. But there is a simpler combinatorial formula.

Let's derive the minimal cost. Consider the final sorted array. For each element v, let pos[v] be its initial position. If pos[v] > v, the element must move left. If pos[v] < v, it must move right. The cost of moving v left from pos[v] to v is the sum of indices from v to pos[v]-1. The cost of moving v right from pos[v] to v is the sum of indices from pos[v] to v-1. However, we cannot simply sum these independently because swaps are shared. 

Actually, the minimum total cost equals the sum over all i of i times the number of elements that start in positions ≤ i and end in positions > i, PLUS the sum over all i of i times the number of elements that start in positions > i and end in positions ≤ i? No, that double counts.

Wait, there is a known solution: The minimum cost is equal to the sum of (i) * (number of elements that need to cross the boundary between i and i+1 from left to right) plus something? No.

Let's think differently. The operation is symmetric in cost but not in index. We can model the process as: we have a permutation, and we can swap any adjacent pair. We want to minimize sum of left indices. This is equivalent to: we have a graph of inversions, and we need to resolve them. Each inversion (u,v) with u>v and u left of v requires u and v to swap relative order. The cost of resolving this inversion depends on where the swap occurs. If we swap them when they are at positions (k, k+1), the cost is k. To minimize cost, we want to resolve inversions at as small k as possible. For a given inversion, the smallest possible k is the minimum of the current positions of u and v. As we process, elements move.

A known greedy algorithm: repeatedly find the smallest index i such that swapping P_i and P_{i+1} reduces the number of inversions (i.e., P_i > P_{i+1}), perform that swap, and add i to the cost. This is always optimal? Let's test on sample 1: P=3,2,1. i=1: P1=3, P2=2 >, swap cost 1. Array=2,3,1. i=1: 2<3 no. i=2: 3>1 swap cost 2. Array=2,1,3. i=1: 2>1 swap cost 1. Array=1,2,3. Total cost 4. Works. For reversed N=4: P=4,3,2,1. i=1: 4>3 swap cost 1. Array=3,4,2,1. i=1: 3<4 no. i=2: 4>2 swap cost 2. Array=3,2,4,1. i=1: 3>2 swap cost 1. Array=2,3,4,1. i=1: 2<3 no. i=2: 3<4 no. i=3: 4>1 swap cost 3. Array=2,3,1,4. i=1: 2<3 no. i=2: 3>1 swap cost 2. Array=2,1,3,4. i=1: 2>1 swap cost 1. Array=1,2,3,4. Total cost: 1+2+1+3+2+1 = 10. This matches the 10 we found! So the greedy "always swap the leftmost inversion" yields cost 10. Is it always optimal? Let's test another permutation. The problem is known as "Sorting a Permutation" with cost i, and the greedy of always performing the leftmost adjacent inversion is indeed optimal. Why? Because any swap at index i can only involve elements that are currently in positions i and i+1. If there is an inversion at i (P_i > P_{i+1}), performing that swap is the cheapest possible way to reduce the inversion count, and delaying it would require swapping at a larger index or doing extra swaps. This is a classic result: to minimize the sum of indices of swaps, you should always perform the cheapest available swap that reduces the inversion count. Since the cost is monotonic with index, the greedy strategy of scanning from left to right and swapping whenever P_i > P_{i+1} is optimal.

Thus, the minimum cost can be computed by simulating this greedy process. But N is up to 2e5, and the number of swaps could be O(N^2) in the worst case (e.g., reversed permutation has N(N-1)/2 inversions). We cannot simulate swap by swap.

We need a way to compute the total cost of this greedy process efficiently. The process is essentially bubble sort but with a specific order: we scan from left to right, and whenever we see an inversion, we swap and continue. This is exactly the bubble sort algorithm. In bubble sort, for each i from 1 to N-1, we bubble the i-th element to the left? Actually, standard bubble sort scans left to right, swapping if out of order, and repeats until sorted. The greedy described is: for i from 1 to N-1, if P_i > P_{i+1}, swap them and restart? No, the greedy as I did: after swapping at i, we continue scanning? In my simulation for N=4, after swap at 1, I continued to i=2. That is: for i=1..N-1, if P_i > P_{i+1}, swap and maybe continue? Actually, the process I did was: for i=1..N-1, check, swap, then move to next i. But after swapping at i, the new element at i might be smaller, so we might need to swap again at i-1. In my simulation, I didn't restart; I just moved forward. That is not standard bubble sort. Let's re-check my simulation steps carefully:

P = [4,3,2,1]
i=1: 4>3, swap -> [3,4,2,1], cost 1. Move to i=2.
i=2: now at i=2, we look at P_2=4, P_3=2. 4>2, swap -> [3,2,4,1], cost 2. Move to i=3.
i=3: P_3=4, P_4=1. 4>1, swap -> [3,2,1,4], cost 3. End of first pass.
Now array is [3,2,1,4]. The process then repeats from i=1:
i=1: 3>2, swap -> [2,3,1,4], cost 1.
i=2: 3>1, swap -> [2,1,3,4], cost 2.
i=3: 3<4, no swap.
Next pass:
i=1: 2>1, swap -> [1,2,3,4], cost 1.
i=2: 2<3, etc.
Total cost = 1+2+3+1+2+1 = 10.

This is exactly the standard bubble sort algorithm! Standard bubble sort repeatedly passes through the array, swapping adjacent inversions, moving from left to right. The total cost is the sum of indices of all swaps performed. So the problem reduces to computing the total sum of indices of all swaps performed by bubble sort on the given permutation.

Is bubble sort optimal for minimizing the sum of indices of swaps? Yes, because each swap at index i resolves an inversion and costs i. Any swap at a larger index would cost more. The greedy of always performing the leftmost possible swap is optimal. This is equivalent to: the total cost is the sum over all inversions of the position at which they are resolved. In bubble sort, an inversion (a,b) with a>b and a left of b is resolved when the smaller element b moves left past a. The swaps that resolve this inversion occur at indices that are the positions of b as it moves left. In bubble sort, b moves left one step at a time, and each step costs the current index. The sum of these costs is exactly the sum of the positions where b passes a. Since bubble sort moves b left as soon as possible (it never moves an element right if it can move left), the costs are minimized.

But we still need to compute the total cost efficiently without simulating all O(N^2) swaps. We need an O(N log N) or O(N) algorithm.

Let's analyze bubble sort cost. In bubble sort, we can think of each element moving left. The number of leftward moves of an element equals the number of elements larger than it that are to its left. Let L[v] be the number of elements > v that are to the left of v initially. Then v must move left L[v] steps. Each leftward move of v from position p to p-1 costs p-1. So the total cost contributed by v is the sum of (current position - 1) for each step. The current position of v when it makes its k-th leftward move (k=1..L[v]) is: initial position pos[v] minus (k-1) minus the number of larger elements that were originally to its left but have already moved? Actually, in bubble sort, the larger elements to the left of v also move left? No, larger elements to the left of v are already to the left; they don't move left past v. v moves left past them. So when v moves left, the elements it passes are those to its left that are larger. As it moves left, its position decreases. The cost of its k-th leftward move is (pos[v] - k). Because after k-1 moves, it's at pos[v] - (k-1), and the next swap is at index pos[v] - k. So the total cost for v is sum_{k=1}^{L[v]} (pos[v] - k) = L[v] * pos[v] - L[v]*(L[v]+1)/2. But wait, is that correct? Let's test on sample 1: P=3,2,1. pos[1]=3, L[1]=2 (elements >1 to left: 3,2). Cost for 1: 2*3 - 3 = 3. pos[2]=2, L[2]=1 (3>2 to left). Cost for 2: 1*2 - 1 = 1. pos[3]=1, L[3]=0. Total cost = 3+1=4. Matches!
Test on reversed N=4: pos[1]=4, L[1]=3. Cost = 3*4 - 6 = 12-6=6. pos[2]=3, L[2]=2. Cost = 2*3 - 3 = 6-3=3. pos[3]=2, L[3]=1. Cost = 1*2 - 1 = 2-1=1. pos[4]=1, L[4]=0. Total = 6+3+1=10. Matches!

So the formula seems to be: for each element v, let pos[v] be its initial position (1-indexed). Let L[v] be the number of elements to the left of pos[v] that are greater than v. Then the total cost is sum_{v=1}^N (L[v] * pos[v] - L[v]*(L[v]+1)/2). We need to compute L[v] for all v efficiently. L[v] is exactly the number of inversions where v is the smaller element. That is, for each v, we need the number of u > v with pos[u] < pos[v]. We can compute this using a Fenwick tree or BIT in O(N log N). But wait: N is up to 2e5, so O(N log N) is fine. However, the values P_i are a permutation of 1..N. We can iterate through the permutation from left to right, and for each element, we can query the BIT to see how many elements seen so far are greater than it. Let BIT store counts of values. For i from 1 to N, v = P_i. Then L[v] = number of elements > v among P_1..P_{i-1}. This is exactly i-1 - query(v) where query(v) is the number of elements ≤ v seen so far. Or we can query from v+1 to N. So L[v] = (i-1) - sum_{k=1}^{v} count. Then we add v to BIT.

Then total cost = sum (L[v] * i - L[v]*(L[v]+1)/2) where i is the position pos[v]. But careful: in the formula, pos[v] is the initial position, which is i in the loop. So we can compute directly during the scan.

Let's verify with a few more cases. Sample 2: N=5, P=2,4,1,3,5.
Positions: 1:pos=3, L[1]=? elements >1 to left: 2,4. So L[1]=2. Cost1 = 2*3 - 3 = 3.
2:pos=1, L[2]=0. Cost2=0.
3:pos=4, L[3]=? elements >3 to left: 4. So L[3]=1. Cost3 = 1*4 - 1 = 3.
4:pos=2, L[4]=? elements >4 to left: none. L[4]=0. Cost4=0.
5:pos=5, L[5]=0. Cost5=0.
Total = 3+3=6. Matches sample output 6.

Sample 3: N=2, P=1,2. L[1]=0, L[2]=0, cost=0. Matches.

What about a case where an element needs to move right? In bubble sort, elements only move left. The sorted array is achieved by moving each element left past all larger elements to its left. There is no rightward movement. So L[v] is exactly the number of leftward moves v makes. The cost formula seems to hold.

But is bubble sort always the optimal sequence? We already verified with examples that bubble sort gives the same cost as the leftmost-inversion greedy. And the leftmost-inversion greedy is optimal because any swap at index i is cheaper than at i+1, and you should resolve inversions at the smallest possible indices. The bubble sort algorithm exactly does that: it repeatedly scans from left to right, performing all possible swaps at the current index, which are the smallest possible indices at that moment. 

Wait, does bubble sort always perform the leftmost possible swap? In bubble sort, during a pass, you might skip an index because P_i < P_{i+1}, but later after some swaps, P_i might become larger than P_{i+1}, and you would swap them in the next pass. Could you have swapped them earlier? In the leftmost-inversion greedy, you would swap them as soon as they become an inversion. In bubble sort, they might only become an inversion after some other swaps, and then you swap them in the same pass? Actually, bubble sort's pass from left to right: you compare P_i and P_{i+1}. If P_i > P_{i+1}, you swap them. Then you move to i+1. You never go back. So if P_i < P_{i+1} initially, you don't swap. But later, a larger element from the right might move left and become P_{i+1}, making P_i < new P_{i+1}? No, that would make P_i even smaller relative to P_{i+1}, so still no inversion. An inversion occurs when a larger element moves left past a smaller one. In bubble sort, a larger element can only move left by swapping with smaller elements to its left. When it swaps with a smaller element, it moves left by one, and the smaller element moves right by one. So the larger element moves left one step per swap. The smaller element that gets swapped to the right might then be larger than its right neighbor, causing another swap. So the larger element "bubbles" left step by step. The smaller elements it passes move right. The process is exactly that each larger element moves left as far as possible, passing all smaller elements to its left. The cost of each step is the index where the swap occurs. The total cost is the sum of the indices of the positions where each larger element passes a smaller element.

But wait, in the formula we derived, we summed over each element v the cost of its leftward moves. That is exactly the cost of the swaps where v is the right element (moving left). In each such swap, v moves left, and the other element u moves right. The cost is the index i of the swap. The sum of costs over all leftward moves of all elements equals the total cost. And the leftward moves of v are exactly L[v] moves, and the positions at which they occur are pos[v], pos[v]-1, ..., pos[v]-L[v]+1. So the sum of indices is exactly sum_{k=1}^{L[v]} (pos[v] - k + 1)? Wait, careful: if v is at position p and moves left one step, the swap is at index p-1 (the left index). The cost is p-1. So the k-th leftward move from position p - (k-1) costs (p - (k-1) - 1) = p - k. So the cost sum is sum_{k=1}^{L[v]} (pos[v] - k). That's what we had.

Now, is it always true that the optimal set of swaps is exactly the set of all leftward moves of each element? Could there be a situation where an element moves left and then right, or where two elements cross multiple times? The number of inversions is the minimum number of swaps. To minimize cost, we want to use the smallest possible indices. The leftward move of a smaller element v past a larger element u is necessary to resolve the inversion (u,v). The cost of this crossing is the index at which they cross. If we do it when they are at positions (i, i+1), cost is i. To minimize cost, we want to cross them as early as possible, i.e., at the smallest possible index. In bubble sort, they cross as soon as the larger element moves left to be adjacent to v? Actually, the crossing happens when the larger element (moving left) meets v (which is stationary until the larger element passes it). The larger element moves left step by step, and the cost of each step is the index. The sum of costs for the larger element to move left past v is exactly the sum of indices it traverses. The total cost for all crossings is the sum over all inversions of the index where they cross. This is exactly the sum over all elements of the sum of indices they traverse while moving left. And bubble sort achieves this by having each element move left exactly as many times as the number of larger elements to its left, and the indices are exactly the positions it passes through. Since no element ever moves right in bubble sort, the indices are exactly the current positions before each leftward move. This seems to be the minimal possible cost because any leftward move of an element from position p costs p-1, and we must have at least that many leftward moves (the number of larger elements to its left). So the cost is at least the sum we computed. And bubble sort achieves it. So the formula is correct and optimal.

Thus, the solution is:
1. Read N and permutation P.
2. Initialize a Fenwick tree (BIT) of size N to store counts of elements seen so far.
3. Iterate i from 1 to N:
   - v = P[i]
   - Query BIT: number of elements > v among P[1..i-1]. This is (i-1) - query(v) where query(v) is sum of counts up to v. Or we can do query(v+1, N) = sum up to N minus sum up to v.
   - Let L = that number.
   - Add to total cost: L * i - L*(L+1)/2. (Be careful with 1-indexing: the cost sum is sum_{k=1}^{L} (i - k). The sum of i from k=1 to L is L*i. The sum of k is L*(L+1)/2. So cost = L*i - L*(L+1)/2.
   - Update BIT: add 1 at position v.
4. Print total cost.

The total cost can be large: N up to 2e5, L up to N, i up to N, so maximum term is about N^2, sum up to O(N^3)? Actually, sum of L*i is at most sum of (N * N) = N^2? Wait, L can be up to N-1, i up to N, so L*i up to N^2. There are N terms, so total sum could be O(N^3) in worst case? Let's check worst-case: reversed permutation, P = [N, N-1, ..., 1]. For v=1, pos= N, L = N-1. Cost = (N-1)*N - (N-1)*N/2 = N(N-1)/2. For v=2, pos=N-1, L=N-2, cost = (N-2)(N-1) - (N-2)(N-1)/2 = (N-2)(N-1)/2. Summing over v gives roughly N^3/6. For N=2e5, N^3/6 is about 1.3e15, which fits in 64-bit integer (max ~9e18). So we need 64-bit (Python int handles it automatically).

Let's test with another example to be sure. N=3, P=2,3,1. Expected cost? Let's compute manually. Bubble sort passes:
[2,3,1] -> swap at 2 (3>1): [2,1,3] cost 2. Then swap at 1 (2>1): [1,2,3] cost 1. Total 3.
Formula: i=1: v=2, L=0, cost=0. i=2: v=3, L=0 (elements >3: none), cost=0. i=3: v=1, L=2 (2 and 3 >1). pos=3. cost = 2*3 - 3 = 3. Total 3. Matches.

Another: N=4, P=1,3,2,4. Bubble sort: [1,3,2,4] -> swap at 2 (3>2): [1,2,3,4] cost 2. Total 2. Formula: i=1: v=1, L=0. i=2: v=3, L=0. i=3: v=2, L=1 (3>2). pos=3, cost = 1*3 - 1 = 2. i=4: v=4, L=0. Total 2. Matches.

What about a case where an element moves right? In bubble sort, elements only move left. The sorted array is achieved entirely by leftward movements. So the formula covers all.

Thus, the algorithm is O(N log N) using a Fenwick tree. We can implement BIT with size N.

Let's double-check the formula derivation. The cost for element v at initial position i with L leftward moves:
The moves happen at indices i-1, i-2, ..., i-L.
Sum of these indices = L*i - (1+2+...+L) = L*i - L*(L+1)/2.
This is correct.

We need to compute L for each v. L is the number of elements to the left of v that are greater than v. As we scan from left to right, for each v, the number of greater elements already seen is (i-1) - (number of elements ≤ v seen). So L = i-1 - query(v). Where query(v) is the prefix sum up to v. Then we add 1 at v.

We must be careful with 1-indexing. In the formula, i is the 1-based position. The cost sum uses i-1 as the first index? Wait: if v is at position i, and it moves left one step, the swap is at index i-1. So the first cost is i-1. The second is i-2, etc. So the sum is (i-1) + (i-2) + ... + (i-L) = L*(i-1) - (0+1+...+(L-1))? Let's recalc carefully:
Sum_{k=1}^{L} (i - k) = L*i - sum_{k=1}^{L} k = L*i - L*(L+1)/2.
But wait, if L=1, the first cost is i-1. Our formula gives 1*i - 1*2/2 = i - 1. Correct.
If L=2, costs: i-1, i-2. Sum = 2i - 3. Formula: 2i - 2*3/2 = 2i - 3. Correct.
So the formula is correct.

Let's test on the sample 1 again: P=3,2,1.
i=1: v=3, L = 0 - query(3) = 0. cost=0. Update BIT(3)=1.
i=2: v=2, L = 1 - query(2) = 1 - 1 (since 3>2, query(2)=1? Actually query(2) counts ≤2. Seen: 3. So query(2)=0. Wait, BIT has 3. So query(2) = 0. So L = 1 - 0 = 1. But earlier we said L[2]=1 (3>2). Correct. pos=2, L=1. cost = 1*2 - 1 = 1. Update BIT(2)=1.
i=3: v=1, L = 2 - query(1) = 2 - 0 = 2. pos=3. cost = 2*3 - 3 = 3. Update BIT(1)=1.
Total = 0+1+3=4. Correct.

So the algorithm is correct.

We need to implement the Fenwick tree for sum queries and point updates. The range is 1..N. We can use 1-based indexing for BIT. The query function returns the sum of counts up to index v. We need the number of elements > v: total seen so far (i-1) minus query(v). So we can maintain a running count of seen elements.

Complexities: O(N log N) time, O(N) space. N up to 2e5 is fine.

Let's write the code.

Plan:
- Read N.
- Read list P of length N.
- Initialize BIT with size N.
- total_cost = 0
- For i from 1 to N:
    v = P[i-1] (since P is 0-indexed)
    L = (i-1) - bit.query(v)  # query(v) gives number of elements ≤ v seen so far
    cost = L * i - L * (L + 1) // 2
    total_cost += cost
    bit.update(v, 1)
- Print total_cost.

We should use Python's arbitrary precision integers, so no overflow.

Let's verify with a larger random case by writing a small brute force to compare for small N. (But I can't run code here, so I'll trust the logic and known results.)

Wait, is bubble sort always the optimal? The leftmost-inversion greedy is optimal. The leftmost-inversion greedy: at each step, find the smallest i such that P_i > P_{i+1}, swap, and repeat. This is exactly the same as the "cocktail sort" or a variant? Actually, the leftmost-inversion greedy: you scan from left to right, and whenever you see an inversion, you swap and then restart from the left? Or you continue? In my earlier simulation, I continued scanning after the swap. That is not the leftmost-inversion greedy; that is bubble sort. The leftmost-inversion greedy would, after a swap at i, check if the new element at i is greater than the one at i-1, and if so, swap leftwards, effectively moving the larger element left as far as possible immediately. Let's test the leftmost-inversion greedy on reversed N=4:
Start: [4,3,2,1]. i=1: 4>3 swap -> [3,4,2,1], cost 1. Now check i=1: 3<4 no. i=2: 4>2 swap -> [3,2,4,1], cost 2. i=2: 2<4 no. i=3: 4>1 swap -> [3,2,1,4], cost 3. i=3: 1<4 no. End of pass? But we didn't restart from left. The leftmost-inversion greedy would, after a swap, immediately check the new element at the same index i to see if it can move left further. In this case, after swapping at i=1, the new element at 1 is 3, which is not > the element to its left (none). So it wouldn't move left. But what if we had [3,4,2,1]? At i=1, 3<4 no. i=2: 4>2 swap -> [3,2,4,1]. Now at i=2, the new element is 2. Check i=2: 2<4 no. But leftmost-inversion greedy would also check i=1: now array is [3,2,4,1]. At i=1, 3>2, so it would swap at i=1, cost 1, giving [2,3,4,1]. Then check i=1: 2<3 no. Then i=2: 3<4 no. i=3: 4>1 swap, cost 3, etc. This is different from bubble sort! Let's simulate the full leftmost-inversion greedy on reversed N=4:
Start: [4,3,2,1]
i=1: 4>3 -> swap, cost 1 -> [3,4,2,1]
Now we might restart from i=1? The greedy says: always perform the smallest possible swap. After the swap, the array changed, so we need to find the new smallest i with an inversion. The smallest i with an inversion is now i=1? Check i=1: 3<4 no. i=2: 4>2 yes, so the smallest is i=2. Swap at i=2, cost 2 -> [3,2,4,1].
Now smallest i with inversion: i=1? Check: 3>2 yes! So smallest is i=1. Swap at i=1, cost 1 -> [2,3,4,1].
Now smallest i: i=1? 2<3 no. i=2: 3<4 no. i=3: 4>1 yes, swap at i=3, cost 3 -> [2,3,1,4].
Smallest i: i=1: 2<3 no. i=2: 3>1 yes, swap at i=2, cost 2 -> [2,1,3,4].
Smallest i: i=1: 2>1 yes, swap at i=1, cost 1 -> [1,2,3,4].
Total cost: 1+2+1+3+2+1 = 10. Exactly the same as bubble sort! So the leftmost-inversion greedy yields the same sequence of swaps as bubble sort in this case. In fact, the leftmost-inversion greedy is known to be equivalent to bubble sort in terms of the set of swaps? Not exactly, but they can have the same total cost. Actually, the leftmost-inversion greedy is the same as always performing the swap with the smallest index that is an inversion. This is exactly the same as the process of repeatedly finding the leftmost inversion and swapping. This is known to be optimal for minimizing the sum of swap indices. And it turns out the total cost is given by the formula we derived.

But is the formula always equal to the total cost of the leftmost-inversion greedy? Our formula was derived from bubble sort, which is one specific sequence of swaps. But since the total cost is minimized and the leftmost-inversion greedy is optimal, the minimum cost must be at most the bubble sort cost. And since the formula gives a lower bound (each element must move left past larger elements, and the cost of each such move is at least the index where it happens, and the indices are at least the positions it passes through), the bubble sort cost is actually the minimum. So the formula is correct.

Thus, the algorithm is solid.

Let's code it.

We'll implement a Fenwick tree class:
- __init__(self, n): self.n = n; self.bit = [0]*(n+1)
- update(self, idx, delta): while idx <= self.n: self.bit[idx] += delta; idx += idx & -idx
- query(self, idx): s=0; while idx>0: s+=self.bit[idx]; idx-=idx&-idx; return s

In the loop:
i from 1 to N:
v = P[i-1]
le = bit.query(v)  # number of elements ≤ v
L = (i-1) - le
cost = L * i - L * (L+1) // 2
total += cost
bit.update(v, 1)

Print total.

Test on samples:
Sample 1: N=3, P=[3,2,1] -> 4
Sample 2: N=5, P=[2,4,1,3,5] -> 6
Sample 3: N=2, P=[1,2] -> 0

All good.

Edge cases: N=2e5, reversed permutation. The sum can be large, Python handles it.

We should also consider that the problem might have a different interpretation, but the formula matches the samples and the greedy reasoning.

Thus, the final answer is the code implementing the above.</mm:think>### NOTES
The problem requires finding the minimum total cost to sort a permutation by adjacent swaps, where swapping at index i costs i. The cost of a swap depends only on the left index. 

The optimal strategy is to always perform the cheapest possible swap that reduces inversions, i.e., always swap the leftmost adjacent inversion. This is equivalent to bubble sort, and it yields the minimal total cost. In this process, each element only moves leftward. For an element v initially at position i (1-indexed), it must move left past all larger elements to its left. Let L be the number of such larger elements. The leftward moves occur at indices i-1, i-2, ..., i-L. The sum of these indices is L*i - L*(L+1)/2. The total cost is the sum of this value over all elements.

We can compute L for each element efficiently using a Fenwick tree (BIT). Scan the permutation from left to right. For each element v at position i, the number of larger elements to its left is (i-1) minus the number of elements ≤ v seen so far. This gives L. The BIT stores counts of values seen so far.

## worker: Implement the Fenwick tree based solution in Pytho
The solution uses the fact that the optimal sorting sequence (always swapping the leftmost adjacent inversion) is equivalent to bubble sort. In bubble sort, each element only moves left, and its cost is the sum of the indices of the swaps it participates in. For an element initially at position i that needs to move left past L larger elements, the swaps occur at indices i-1, i-2, ..., i-L, summing to L*i - L*(L+1)/2. The BIT efficiently computes L for each element as (i-1) minus the number of already-seen elements ≤ v. The total cost is accumulated and printed. The algorithm runs in O(N log N) time and O(N) space, suitable for N up to 2·10⁵.
