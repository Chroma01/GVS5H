We need to sort a permutation using adjacent swaps where swapping positions i and i+1 costs i. This is equivalent to: for each element, it must move from its original position to its target position (value v goes to index v). The cost of moving an element left or right is the sum of indices of the swaps it participates in, which depends on the direction of movement.

For each value v, let original position be pos[v]. In the sorted array, v must end at index v. The element needs to move from pos[v] to v.

- If pos[v] > v (needs to move left): It will be swapped leftwards across positions pos[v]-1, pos[v]-2, ..., v. The cost contributed is sum_{i=v}^{pos[v]-1} i.
- If pos[v] < v (needs to move right): It will be swapped rightwards across positions pos[v], pos[v]+1, ..., v-1. The cost contributed is sum_{i=pos[v]}^{v-1} i.

However, we must be careful: the total cost is simply the sum over all swaps performed. Each swap between positions i and i+1 costs i. 

Key insight: The minimum total cost equals the sum over all pairs of elements that are "inverted" (out of order) of the index where their swap eventually occurs... actually, let me think differently.

Consider: each element v at position pos[v] must move to position v. The total cost is the sum of all swap indices used. Equivalently, think of it as: for each position i (1 to N-1), how many times do we swap at position i?

Alternative approach using BIT (Fenwick tree):
- Process elements in sorted order. For each v, the number of elements already placed that are to the right of v's current position... hmm, this is complex.

Let me think again. A cleaner formulation:

Sort the permutation. Process values v from 1 to N. When we place value v, it needs to shift from pos[v] to position v. The elements currently between positions v and pos[v] (if pos[v] > v) are values greater than v that haven't been placed yet—they need to shift right by 1. The cost of moving v left from pos[v] to v is sum_{i=v}^{pos[v]-1} i (cost of each swap at position i).

But we also need to account for the shifts of other elements. Actually, the total cost has a nice formula.

Total cost = sum over all swaps of their index. Consider that each element v makes a journey. The total cost = sum_{v=1}^{N} (cost of v's leftward moves) + (cost of v's rightward moves)... but we double count?

Actually, each swap at position i swaps two adjacent elements. After all operations, the result is sorted. The total cost is sum of indices of all swaps performed.

There's a known result: The answer equals the sum over v of f(v) where:
- If pos[v] >= v: contribution is sum of indices from v to pos[v]-1 (moving left)
- If pos[v] < v: contribution is sum of indices from pos[v] to v-1 (moving right)

Wait, I need to verify. Consider N=3, P=(3,2,1). pos[1]=3, pos[2]=2, pos[3]=1.
- v=1: pos[1]=3, needs to move left from 3 to 1. Cost = 1+2 = 3.
- v=2: pos[2]=2, already in place. Cost = 0.
- v=3: pos[3]=1, needs to move right from 1 to 3. Cost = 1+2 = 3.
Total = 6. But expected answer is 4. So this formula overcounts.

The issue: when we swap, both elements move. Let me reconsider.

When element at position i (cost i) swaps with position i+1, both elements' positions change. The element moving right pays for the swap, and the element moving left also pays? No—the cost is paid once per swap operation.

So my formula double-counts. Let me reconsider.

Think of it as: we perform a sequence of adjacent swaps. Each swap at boundary i costs i. Total cost = sum of costs of all swaps.

For each element v, count the number of swaps at each position it crosses. Element v at position pos[v] must reach position v. For each swap position i on its path, the swap costs i.

But each swap involves TWO elements crossing position i (or rather, swapping across boundary i). So if element v moves left across boundary i, some other element u moves right across boundary i. We pay i once, but both v and u "use" this swap.

So the total cost = sum over all swap boundaries i of (i × number of swaps at boundary i).

Alternative view: total cost = sum over all inversions (pairs (a,b) where a is left of b in P but a > b in sorted order) of... hmm, this gets complicated.

Let me think about the structure differently. 

Standard approach for this problem (it's a known AtCoder problem):

The answer can be computed as follows. For each v from 1 to N:
- If pos[v] >= v: add (pos[v] - v) * v + (pos[v] - v) * (pos[v] - v + 1) / 2... no wait.

Let me look at this more carefully. Actually I recall the solution:

Process v = 1 to N. Maintain pos[v] (original position). The element v needs to go to position v. 
- If pos[v] > v: v moves left. The number of swaps v participates in (moving left) is pos[v] - v, at boundaries v, v+1, ..., pos[v]-1. But we also need to account for shifts of other elements.

Actually, here's the correct decomposition:

The total cost = sum_{v=1}^{N} C(v) where C(v) is computed as:
- If pos[v] >= v (v moves left or stays): v crosses boundaries v, v+1, ..., pos[v]-1. Cost contribution from v's leftward journey for these swaps: but we share the cost with the element moving the other way.

Hmm, let me think about it as: the cost of swap at boundary i is paid, and this swap is "used" by exactly two elements (the two being swapped). So total cost = sum_{i=1}^{N-1} i * (number of times boundary i is swapped).

When is boundary i swapped? Whenever an element crosses from position ≤ i to position > i (moving right) or from > i to ≤ i (moving left), across that specific boundary in the sequence of operations.

This is getting complex. Let me just think of a direct approach.

Direct approach: Greedy/simulation is too expensive for N up to 2*10^5. We need O(N log N).

Key insight: Consider processing elements in order of value (v = 1, 2, ..., N). When we "place" element v, we shift it from pos[v] to position v. The elements between positions v and pos[v] (exclusive on the v side) all have values > v (since v is the smallest unplaced). These elements each shift by 1 position in the direction away from v.

Cost of placing v:
- If pos[v] >= v: v moves left. Swaps happen at boundaries v, v+1, ..., pos[v]-1. The cost of these swaps (from v's perspective) involves boundaries v through pos[v]-1. Specifically, the swaps to move v from pos[v] to v cost sum_{i=v}^{pos[v]-1} i. Additionally, the elements between v and pos[v] shift right by 1, and this shifting requires additional swaps. Each such element (there are pos[v]-v of them) shifts right by 1 across some boundary, contributing to the cost.

Wait, I think I'm overcomplicating. Let me re-examine.

When v moves from pos[v] to v (assuming pos[v] > v):
- v performs pos[v]-v leftward swaps at boundaries v, v+1, ..., pos[v]-1.
- Each leftward swap at boundary i also moves some element (with value > v) rightward by 1.
- The cost paid for each such swap is i (one cost per swap).

But do we pay additional cost for those rightward movements? The rightward movement of element u is "part of" the same swap operation. So the cost of swap at boundary i is just i, paid once.

So when v moves from pos[v] to v (pos[v] > v), the total cost added = sum_{i=v}^{pos[v]-1} i. This is because v makes pos[v]-v swaps, at boundaries v, v+1, ..., pos[v]-1, each costing i.

Now what about the other elements that need to move right (from position < v to position > v, i.e., elements with original position < v and value > v)? These elements' rightward movements: when do they happen?

Consider element u with value > v and original position pos[u] < v. Element u needs to end at position u > v. So u moves from pos[u] to u, moving right. u's rightward swaps happen at boundaries pos[u], pos[u]+1, ..., u-1.

These swaps are independent of v's swaps (in terms of which operations we perform, but the cost accumulates).

Hmm, but here's the thing: when v moves left from pos[v] to v, the elements between original positions v and pos[v] shift. But in the final sorted array, those elements (with values > v) need to be to the right of v. Their final positions are determined by their values. The question is: what's the total cost?

Let me reconsider. The total cost is the sum of all swap costs. Let me categorize swaps by the element moving LEFT through a boundary.

Element v at original position pos[v], final position v.
- Number of leftward moves of v = max(0, pos[v] - v). These happen at boundaries v, v+1, ..., pos[v]-1 (if pos[v] > v).
- Number of rightward moves of v = max(0, v - pos[v]). These happen at boundaries pos[v], pos[v]+1, ..., v-1 (if v > pos[v]).

Each swap at boundary i involves one leftward mover and one rightward mover crossing that boundary. The cost of the swap is i.

Total cost = sum_{i=1}^{N-1} i * (# of times boundary i is swapped) = sum_{i=1}^{N-1} i * (# of elements crossing boundary i leftward) = sum_{i=1}^{N-1} i * (# of elements crossing boundary i rightward) [these are equal].

So total cost = sum_{i=1}^{N-1} i * (number of elements v with pos[v] > v >= i+1, i.e., v <= i and pos[v] > i, OR v > i and pos[v] <= i).

Wait, let me reconsider. An element v crosses boundary i leftward if its original position is > i and final position is <= i, i.e., pos[v] > i and v <= i. 

An element v crosses boundary i rightward if pos[v] <= i and v > i.

These two counts are equal (each swap moves one element each way).

Total cost = sum_{i=1}^{N-1} i * |{v : v <= i and pos[v] > i}|.

This is computable! For each i, count how many values v in {1, ..., i} have pos[v] > i.

So the algorithm:
1. Compute pos[v] for all v.
2. For i from 1 to N-1, compute count_i = number of v in [1, i] with pos[v] > i.
3. Answer = sum_{i=1}^{N-1} i * count_i.

We can compute this efficiently using a BIT:
- Sort values v by pos[v].
- For i from 1 to N-1, count_i = (number of v in [1,i] with pos[v] > i) = i - (number of v in [1,i] with pos[v] <= i).

Maintain a BIT over positions. Initially, all positions have 1 (meaning "v at this position exists"). Or better: process i from 1 to N-1, and track how many v <= i have pos <= i.

Let me reformulate. We have pos[1], pos[2], ..., pos[N]. For each i from 1 to N-1:
- count_i = #{v : 1 <= v <= i, pos[v] > i}
- = i - #{v : 1 <= v <= i, pos[v] <= i}

Compute #{v : 1 <= v <= i, pos[v] <= i} using a BIT. Sort the pairs (pos[v], v) by pos[v]. For each i, we need count of v in [1,i] among those with pos[v] <= i.

Approach: Sort values v=1..N by pos[v]. Process i from 1 to N-1. Maintain a pointer: among sorted values, how many have pos[v] <= i. Use a BIT or just a running count.

Actually simpler: just use a BIT on positions. For each i, we want to know: among v=1..i, how many have pos[v] <= i?

We can process i from 1 to N, and after handling i, "add" v=i to the structure. Or pre-process.

Easiest: Sort v by pos[v]. Let sorted_v = values sorted by pos[v] ascending. Process i from 1 to N-1. Maintain a multiset (or sorted list) of values v with pos[v] <= i. We want count of v in [1, i] within this multiset.

Use a BIT over values v (size N). For each i from 1 to N-1:
- Add to BIT all v with pos[v] == i (i.e., v whose original position is i). Wait, but we add them when we process boundary i.

Let me re-approach. Process boundaries i = 1, 2, ..., N-1. We want count_i = #{v <= i : pos[v] > i}.

Equivalently, count_i = (number of v <= i) - (number of v <= i with pos[v] <= i) = i - (number of v in [1,i] with pos[v] <= i).

To compute this for all i efficiently:
- For each i, after processing, the values v with pos[v] <= i form a set S_i.
- |S_i ∩ [1, i]| = number of v in [1,i] with pos[v] <= i.

Use a BIT of size N. Initially empty. For i = 1, 2, ..., N-1:
- Add value v = pos^{-1}(i) (the value at position i in P) to the BIT. Mark: v is at position i, so once we pass i, v is "available" with pos[v] <= i.
- Wait, I should be careful. We want values v with pos[v] <= i. For i = 1, this means values at position 1. For i = 2, values at positions 1 or 2. Etc.

So for i = 1: add the value at position 1 (call it v_1 = P[1]). Then |S_1 ∩ [1, 1]| = 1 if v_1 == 1, else 0.
For i = 2: add v_2 = P[2]. |S_2 ∩ [1, 2]| = count of v_1, v_2 in [1,2] = 2 if {v_1, v_2} = {1, 2}, else fewer.

Hmm, but we want count_i for i from 1 to N-1. And count_i = i - |S_i ∩ [1, i]|.

Wait, this only works if we're considering i where v in [1, i] are exactly i values. Let me redo.

count_i = #{v : 1 <= v <= i, pos[v] > i}
        = |{1,...,i}| - |{v in [1,i] : pos[v] <= i}|
        = i - |S_i ∩ [1, i]|

where S_i = {v : pos[v] <= i}.

So for each i from 1 to N-1, compute |S_i ∩ [1,i]|.

Algorithm:
- pos[v] = original position of value v.
- For i = 1 to N-1:
  - S_i = {v : pos[v] <= i}. This grows as i increases.
  - We need |S_i ∩ [1, i]|.
- Use a BIT (Fenwick tree) over the value axis (1 to N).
- Process i from 1 to N-1:
  - "Insert" value v_i = P[i] (the value at position i) into the BIT at index v_i. (Because pos[v_i] = i <= i, so v_i is now in S_i.)
  - Query BIT for prefix sum up to i: this gives |S_i ∩ [1, i]|.
  - count_i = i - prefix_sum.
  - Add i * count_i to answer.

Let me verify with sample 1: N=3, P=(3,2,1). pos[1]=3, pos[2]=2, pos[3]=1.
- i=1: S_1 = {v : pos[v] <= 1} = {3} (since pos[3]=1). Insert v=3 into BIT. Query prefix up to 1: |S_1 ∩ [1,1]| = 0 (since 3 is not in [1,1]). count_1 = 1 - 0 = 1. Answer += 1*1 = 1.
- i=2: S_2 = {v : pos[v] <= 2} = {2, 3}. Insert v=2 (since P[2]=2, pos[2]=2). Query prefix up to 2: |S_2 ∩ [1,2]| = |{2}| = 1. count_2 = 2 - 1 = 1. Answer += 2*1 = 2.
- Total = 1 + 2 = 3. But expected answer is 4!

Hmm, discrepancy. Let me recheck.

Oh wait, count_i should include v <= i with pos[v] > i. Let me recheck i=1:
- v in [1,1], i.e., v=1. pos[1] = 3 > 1. So count_1 = 1. ✓
- i=2: v in [1,2], i.e., v=1,2. pos[1]=3>2 ✓, pos[2]=2, not > 2. So count_2 = 1. ✓

Total = 1*1 + 2*1 = 3. But answer should be 4.

So my formula is wrong. Let me reconsider.

Hmm. Let me re-examine. The issue might be that I'm not accounting for something.

Let me reconsider what "crossing boundary i" means and the cost.

Total cost = sum over swaps of (index of swap).

A swap at boundary i swaps elements at positions i and i+1. Cost is i.

Total cost = sum_{i=1}^{N-1} i * (number of swaps at boundary i).

Number of swaps at boundary i = number of times an element crosses from left side (pos <= i) to right side (pos > i) of boundary i, OR equivalently from right to left. Both counts are equal.

An element v crosses boundary i leftward if pos[v] > i and v <= i (original on right, final on left).
An element v crosses boundary i rightward if pos[v] <= i and v > i (original on left, final on right).

So # swaps at i = #{v : v <= i, pos[v] > i} = #{v : v > i, pos[v] <= i}.

For sample 1, N=3, P=(3,2,1):
- i=1: #{v<=1, pos[v]>1} = #{v=1: pos[1]=3>1} = 1. #{v>1, pos[v]<=1} = #{v=2: pos[2]=2>1 no; v=3: pos[3]=1<=1 yes} = 1. ✓
- i=2: #{v<=2, pos[v]>2} = #{v=1: 3>2 yes, v=2: 2>2 no} = 1. #{v>2, pos[v]<=2} = #{v=3: 1<=2 yes} = 1. ✓

Total cost = 1*1 + 2*1 = 3. But expected is 4!

So either my formula is wrong or my counting of swaps is wrong. Let me recount swaps in the sample solution:

Sample 1: P = (3,2,1) → (2,3,1) [swap at i=1, cost 1] → (2,1,3) [swap at i=2, cost 2] → (1,2,3) [swap at i=1, cost 1]. Total = 1+2+1 = 4. Swaps at boundary 1: 2 times. Swaps at boundary 2: 1 time. Cost = 1*2 + 2*1 = 4. ✓

So in this sorting, boundary 1 is swapped 2 times, not 1. My formula gives 1, which is wrong.

Let me re-examine. Boundary 1 swaps: first swap (3,2) → (2,3), then later (2,1) → (1,2). So 2 swaps at boundary 1.

According to my formula, # swaps at boundary 1 = #{v : v <= 1, pos[v] > 1} = #{v=1: pos[1]=3>1} = 1. But actual is 2.

So my formula undercounts. Why?

Oh! I see. The issue is that after some operations, the "positions" of elements change. The original pos[v] is fixed, but elements can cross boundary i multiple times in different ways... no wait, an element crosses a boundary at most once in one direction (net).

Wait, can an element cross boundary i more than once? In a sequence of adjacent swaps to sort, can element v cross boundary i, then cross back, then cross again? That would be inefficient. The minimum-cost sorting would not have such "back and forth".

But even so, my formula counts net crossings. Hmm.

Wait, let me re-examine. In the sample, P=(3,2,1):
- Element 1: pos[1]=3, final pos=1. Crosses boundaries 1, 2 leftward (net: 2 leftward crossings). So element 1 contributes 1 leftward crossing at boundary 1 and 1 at boundary 2.
- Element 2: pos[2]=2, final pos=2. No crossings.
- Element 3: pos[3]=1, final pos=3. Crosses boundaries 1, 2 rightward (net: 2 rightward crossings). Contributes 1 rightward crossing at boundary 1 and 1 at boundary 2.

So net crossings: boundary 1 has 1 left + 1 right = 2 total crossings. So # swaps at boundary 1 = 2. ✓
Boundary 2: 1 left + 1 right = 2 total. # swaps = 2? But actual is 1!

Hmm, contradiction. Let me recount.

Element 1 moves from pos 3 to pos 1. It needs to cross boundaries 1 and 2 leftward. That's 2 leftward moves.
Element 3 moves from pos 1 to pos 3. It needs to cross boundaries 1 and 2 rightward. That's 2 rightward moves.

But in the actual swaps:
- Swap at i=1 (3,2): element 3 moves left (from pos 1 to... wait, swapping positions 1 and 2 means element at pos 1 (which is 3) moves to pos 2, and element at pos 2 (which is 2) moves to pos 1). So 3 moves right, 2 moves left.
- Swap at i=2 (3,1): element 3 (at pos 2) moves to pos 3 (right), element 1 (at pos 3) moves to pos 2 (left).
- Swap at i=1 (2,1): element 2 (at pos 1) moves to pos 2 (right), element 1 (at pos 2) moves to pos 1 (left).

So:
- Element 1: moves left twice (at boundary 1 then at boundary 2? No, at boundary 2 first (in second swap), then at boundary 1 (in third swap)). Wait, in the second swap (boundary 2), element 1 goes from pos 3 to pos 2 (leftward across boundary 2). In the third swap (boundary 1), element 1 goes from pos 2 to pos 1 (leftward across boundary 1). So element 1 crosses boundary 2 leftward once and boundary 1 leftward once.
- Element 3: in first swap, pos 1 → pos 2 (rightward across boundary 1). In second swap, pos 2 → pos 3 (rightward across boundary 2).
- Element 2: in first swap, pos 2 → pos 1 (leftward across boundary 1). In third swap, pos 1 → pos 2 (rightward across boundary 1).

So element 2 crosses boundary 1 leftward once AND rightward once (net zero). So boundary 1 has crossings: element 1 (left), element 2 (left), element 2 (right), element 3 (right). That's 4 crossings but only 2 swaps!

I see, so the relationship "crossings = 2 * swaps" doesn't hold in general because elements can cross back and forth. But in a minimum-cost solution, we want to minimize total cost, which is sum of i * (# swaps at boundary i). 

Hmm, but my formula based on net crossings isn't right then. Let me reconsider.

Actually, the key insight: # swaps at boundary i = # of pairs (left_element, right_element) that get swapped across boundary i. Each swap at boundary i involves one element on the left moving right and one on the right moving left.

In the minimum cost solution, we want to minimize sum of i * (swaps at i). This is equivalent to... 

Hmm, let me think again. The net crossing counts give the minimum number of swaps, but the actual number of swaps at each boundary can be higher due to elements "passing through" multiple times.

Wait, actually, I think for sorting a permutation, the minimum total swaps is N - (number of cycles), but here we're not minimizing # of swaps, we're minimizing weighted sum.

Let me reconsider. For the minimum cost problem, I believe the correct approach is:

The total cost = sum_{v=1}^{N} (cost of v's journey).

When v moves from pos[v] to v:
- If pos[v] > v (moves left): v makes swaps at boundaries v, v+1, ..., pos[v]-1. The cost of each swap is the boundary index. But v only participates in one swap per boundary on its path. Wait, can v be involved in a swap at boundary i more than once?

In a minimum solution, v traverses each boundary at most once. Because going back and forth would only add cost. So v's contribution is: sum of boundary indices on its path.

- If pos[v] >= v: v moves left across boundaries v, v+1, ..., pos[v]-1. Cost = sum_{i=v}^{pos[v]-1} i.
- If pos[v] < v: v moves right across boundaries pos[v], pos[v]+1, ..., v-1. Cost = sum_{i=pos[v]}^{v-1} i.

Total cost = sum_v (cost of v's journey).

Wait, but this seems to overcount because each swap involves two elements. Let me re-examine.

When v moves left from pos[v] to v, it swaps with the element to its left at each step. Each such swap is a distinct operation with cost = boundary index. So v participates in (pos[v] - v) swap operations, with total cost = sum_{i=v}^{pos[v]-1} i.

But the element it swaps with also participates. That element's journey is also counted separately.

So total cost = sum over all v of (cost of v's leftward journey) + (cost of v's rightward journey).

Let me re-examine with sample 1:
- v=1: pos[1]=3, moves left from 3 to 1. Cost = 1+2 = 3.
- v=2: pos[2]=2, stays. Cost = 0.
- v=3: pos[3]=1, moves right from 1 to 3. Cost = 1+2 = 3.
Total = 6. But expected is 4.

So this overcounts by 2. The overcounting is because when v moves left and u moves right, the swap between them is counted in both v's and u's journey. Specifically, when v (moving left) and u (moving right) swap at boundary i, the cost i is counted in both v's sum and u's sum, but should only be counted once.

So the correct total = (sum of v's leftward costs) + (sum of v's rightward costs) - (overcounting correction).

Hmm, this is getting complex. Let me think differently.

Alternative: Think of it as, for each swap operation (at boundary i, cost i), it's performed once. The total cost is sum of these.

Let me try yet another approach. Process elements v = 1, 2, ..., N in order. Place each element v into its correct position.

When placing v (which is currently at pos[v], with all values 1..v-1 already placed at positions 1..v-1):
- The elements at positions 1..v-1 are {1, 2, ..., v-1} in order.
- Element v is somewhere at position pos[v]. If pos[v] < v, then v is among the already-placed region, but that's impossible since all of 1..v-1 are placed and v > all of them. So pos[v] > v or pos[v]... wait, pos[v] could be anything.

Hmm, if we process in order and place v, then v must currently be at some position. The elements 1..v-1 are at positions 1..v-1. So v is at some position >= v. Wait, but v could be at position v already (if it was in the right place), or at position > v.

But wait, what if pos[v] < v? Then v is currently in the region [1, v-1], but that region is occupied by {1, ..., v-1}. Contradiction unless v hasn't been placed yet but is in that region... but {1,...,v-1} are exactly the elements there. So v can't be at position < v if 1..v-1 are at 1..v-1.

Hmm, so after placing 1..v-1 at positions 1..v-1, element v is at position >= v. (Since positions 1..v-1 are taken by 1..v-1.)

Wait, but v was originally somewhere, and as we place 1, 2, ..., v-1, they shift around. Let me reconsider.

Let's think of it as: we process v = 1, 2, ..., N. To place v, we first need to bring v to position v. The elements between current position of v and v are values > v (since 1..v-1 are at 1..v-1).

Actually, this is the standard approach. Let me formalize.

State: positions 1..(v-1) contain {1, ..., v-1} in sorted order. Position v onwards contains {v, v+1, ..., N} in some order.

To place v at position v: v is currently at some position p_v >= v (since positions 1..v-1 are occupied by 1..v-1). We swap v leftward from p_v to v. Each swap at boundary i (i from v to p_v - 1) costs i. The elements that v swaps with (all > v) shift right by 1.

Cost of placing v = sum_{i=v}^{p_v - 1} i = (v + (v+1) + ... + (p_v - 1)) = (p_v - 1) * p_v / 2 - (v-1) * v / 2.

But wait, we also need to account for the cost of those other elements moving right. When v swaps with element u (at boundary i), u moves right by 1. Does this cost extra? No, the cost of the swap is just i, paid once. But u's rightward movement is "free" in terms of this swap.

However, u still needs to reach its final position. U's final position is u (since u > v, u is among {v+1, ..., N}). U's rightward shift by 1 means u's effective position increases by 1, so u needs to move right by 1 less in the future.

Hmm wait, the elements {v+1, ..., N} are at positions v, v+1, ..., N. After placing v at position v, the elements {v+1, ..., N} are at positions v+1, v+2, ..., N+1... no, the array is still size N. Positions v+1, ..., N contain {v+1, ..., N} in some order, which is N - v elements in N - v positions. OK.

So placing v costs sum_{i=v}^{p_v-1} i. The total cost is sum over v=1 to N of (cost to place v).

Let me verify with sample 1: P=(3,2,1).
- pos[1]=3, pos[2]=2, pos[3]=1.
- Place v=1: p_1 = 3 (element 1 is at position 3). Cost = sum_{i=1}^{2} i = 1+2 = 3. Now P = (1, 2, 3) effectively? Wait, let me re-examine.

Original P = (3, 2, 1). 
- Place v=1: element 1 is at position 3. Swap left: swap boundary 2 (cost 2): P = (3, 1, 2). Swap boundary 1 (cost 1): P = (1, 3, 2). Cost so far: 3.
- Place v=2: element 2 is at position 3. Swap boundary 2 (cost 2): P = (1, 2, 3). Cost: 3+2 = 5.
- Place v=3: already in place. Cost: 0.
- Total: 5. But expected is 4!

So this greedy "place in order" gives 5, not the optimal 4. So this isn't the minimum cost approach.

The issue: the greedy approach doesn't necessarily give minimum cost. We need to choose the order of swaps carefully.

Let me reconsider. In sample 1, the optimal is:
- Swap boundary 1 (3,2): cost 1. P=(2,3,1).
- Swap boundary 2 (3,1): cost 2. P=(2,1,3).
- Swap boundary 1 (2,1): cost 1. P=(1,2,3).
- Total: 4.

In my greedy: 
- Swap boundary 2 (1, ... wait, element 1 is at position 3, so swap boundary 2 first: (3,1) at positions 2,3 → swap: P=(3,1,2). Cost 2.
- Swap boundary 1: (3,1) → (1,3). Cost 1. P=(1,3,2).
- Then for v=2: at position 3, swap boundary 2: (3,2) → (1,2,3). Cost 2.
- Total: 2+1+2 = 5.

So the greedy is suboptimal. We need a better approach.

OK so let me think about the structure more carefully.

Reformulation: We have a permutation, and we want to sort it with adjacent swaps. Cost of swap at boundary i is i. Find min cost.

This is equivalent to: we have a graph (path) with N-1 edges (boundaries), and we want to route each element from its origin to its destination, where each routing is a sequence of edge traversals. The cost of traversing edge i is i (per traversal). But each traversal of an edge is a swap of the two elements on either side.

Wait, but in an optimal solution, each edge is traversed... hmm. Let me think of it as a flow / min-cost problem.

Alternative model: Think of the sorted permutation as the target. We need to transform P into (1,2,...,N) using adjacent swaps.

For each element v, it travels from pos[v] to v. The path is along the line 1-2-...-N. If pos[v] > v, v travels left; else right.

The cost of v's travel: each edge (i, i+1) that v crosses costs i. So if v travels left from pos[v] to v, it crosses edges (v, v+1), (v+1, v+2), ..., (pos[v]-1, pos[v]). Costs: v, v+1, ..., pos[v]-1. Sum = sum_{i=v}^{pos[v]-1} i.

Similarly for rightward.

But as noted, when two elements cross each other (swap), the cost is shared. Actually, in terms of the cost model, each swap is one operation costing the boundary index. So if v and u swap at boundary i, cost i is paid once.

The total cost is the sum of costs of all swap operations. Each swap at boundary i costs i.

Now, here's a key insight: think of each element v as a "particle" traveling from pos[v] to v. The total cost is the sum over boundaries of (boundary index) * (# of times the boundary is swapped).

But # of times a boundary is swapped = # of pairs of particles that cross that boundary (in opposite directions) = ... hmm, this is where it gets tricky because of the order.

Let me think of it as a min-cost flow on a line. Actually, there's a classical result for this type of problem.

Reformulation: Let's think of each element v as needing to go from pos[v] to v. Consider the "demand" at each position: position j has demand (final value) - (initial value) = j - P[j]... no wait, the initial array has P[j] at position j, and we want value j at position j. So element at position j (value P[j]) needs to go to position P[j]. This is a permutation routing problem.

For permutation routing on a line (path graph) with costs on edges, the minimum cost is... well, this is related to the earth mover's distance or optimal transport.

Actually, let me think of it as: we have N "tokens" at positions pos[1], pos[2], ..., pos[N] (but they're at the same positions, just with different identities), and we want to move them to positions 1, 2, ..., N. Each token v goes from pos[v] to v.

But this is just sorting. Hmm.

Let me think of a different model. Consider the line 1-2-...-N. Each element v moves from pos[v] to v. The cost of v's movement = sum of edge costs on its path.

But the constraint is that moves are simultaneous (swaps), and each swap costs the edge cost once.

Alternative: think of it as, for each boundary i, the number of swaps at i equals the number of elements that need to cross boundary i. Specifically, an element v crosses boundary i (in some direction) if pos[v] and v are on opposite sides of i.

If pos[v] > i and v <= i: v crosses leftward.
If pos[v] <= i and v > i: v crosses rightward.

In a valid sorting, each element crosses each boundary the correct number of times. The # of leftward crossings at i = # of rightward crossings at i = # of swaps at i.

But wait, the # of leftward crossings = #{v : pos[v] > i, v <= i}, and # of rightward crossings = #{v : pos[v] <= i, v > i}. These two are equal (this is a property of permutations).

So # swaps at boundary i = #{v : pos[v] > i, v <= i}.

And total cost = sum_{i=1}^{N-1} i * #{v : pos[v] > i, v <= i}.

Let me recompute sample 1:
- i=1: #{v : pos[v] > 1, v <= 1} = #{v=1 : pos[1]=3>1} = 1. Cost contribution: 1*1 = 1.
- i=2: #{v : pos[v] > 2, v <= 2} = #{v=1: pos[1]=3>2 yes, v=2: pos[2]=2>2 no} = 1. Cost contribution: 2*1 = 2.
- Total: 3.

But expected is 4! So my formula is still wrong.

Hmm. Let me recount swaps in the optimal solution.

Optimal: P=(3,2,1) → (2,3,1) → (2,1,3) → (1,2,3). Swaps: (1,2) at i=1, (2,3) at i=2, (1,2) at i=1. So 2 swaps at i=1, 1 swap at i=2. Cost = 1*2 + 2*1 = 4.

But my formula gives 1 swap at i=1 and 1 at i=2, cost 3. So I'm undercounting by 1 swap at i=1.

The issue: my formula computes the # of elements crossing boundary i, which is the # of swaps at i in a "minimal swap" sorting. But in the optimal (for cost) sorting, some boundaries are swapped more than the minimum.

Wait, the minimum # of swaps to sort is N - (number of cycles), and # swaps at boundary i is fixed = #{v: pos[v]>i, v<=i} regardless of the order of swaps. This is a theorem.

Hmm, is that true? Let me think. # of swaps at boundary i = # of inversions (a,b) with a < b <= i < pos^{-1}(a) or something... 

Actually, I recall: in any sorting of a permutation by adjacent swaps, the # of times boundary i is swapped is fixed = #{v: v <= i, pos[v] > i}. This is because it's the # of inversions (v, w) with v < w and pos[v] > pos[w]... no wait, it's the # of (v) with v <= i and pos[v] > i, which is the # of pairs... hmm, let me think.

The # of swaps at boundary i in any sorting is fixed. This is a known result. So if my formula gives 1 swap at i=1 but the actual optimal has 2, then either my formula is wrong or the "optimal" sample solution isn't actually using minimum swaps at each boundary.

Wait, let me recount. In the sample:
- Swap 1: boundary 1, (3,2). Now P=(2,3,1).
- Swap 2: boundary 2, (3,1). Now P=(2,1,3).
- Swap 3: boundary 1, (2,1). Now P=(1,2,3).

Boundary 1 swaps: swap 1 and swap 3. That's 2.
Boundary 2 swaps: swap 2. That's 1.

Total: 1*2 + 2*1 = 4. ✓

But by the formula, # swaps at boundary 1 = #{v <= 1, pos[v] > 1} = #{v=1: pos[1]=3>1} = 1.

So the formula says 1, but actual is 2. Contradiction with the "fixed # of swaps" theorem.

Let me re-examine the theorem. The # of swaps at boundary i = # of inversions across boundary i = #{pairs (a,b) with a < b, a <= i, b > i, and pos[a] > pos[b]}... hmm wait, that's # of inversions of pairs (a,b) with a<=i<b. Which equals # of (a <= i) with pos[a] > i (if we consider that each such a must be swapped with some b > i that's currently to its left, but that b has pos[b] < pos[a], i.e., b is to the left of a, so b <= i... contradiction).

Hmm, let me reconsider. The # of swaps at boundary i (in any adjacent-swap sorting) = # of inversions (x, y) where x < y, pos[x] > pos[y], and the boundary i separates them at some point... 

Actually, the standard result: # of times boundary i is crossed (in either direction) in any sorting = # of (v) with min(pos[v], v) <= i < max(pos[v], v), i.e., v's origin and destination are on opposite sides of i. This equals #{v : (v <= i and pos[v] > i) or (v > i and pos[v] <= i)} = 2 * #{v : v <= i, pos[v] > i} (by symmetry of permutations).

Wait, #{v : v <= i, pos[v] > i} = #{v : v > i, pos[v] <= i} (property of permutations). So total = 2 * this.

And # of swaps at boundary i = this count (since each swap is one crossing in each direction, so # swaps = # leftward = # rightward = the count).

So # swaps at i = #{v : v <= i, pos[v] > i}.

For sample 1, i=1: #{v<=1, pos[v]>1} = #{v=1: 3>1} = 1. So 1 swap at boundary 1.

But the actual solution has 2 swaps at boundary 1. So the theorem is wrong, or I'm miscounting.

Let me recount the actual swaps and trace each element.

P=(3,2,1), sorted=(1,2,3).
- Element 1: pos 3 → 1. Crosses boundaries 1, 2 leftward.
- Element 2: pos 2 → 2. No crossing.
- Element 3: pos 1 → 3. Crosses boundaries 1, 2 rightward.

In the swaps:
- Swap 1 (boundary 1, cost 1): 3↔2. 3 moves from pos 1 to pos 2 (right, crosses boundary 1). 2 moves from pos 2 to pos 1 (left, crosses boundary 1).
- Swap 2 (boundary 2, cost 2): 3↔1. 3 moves from pos 2 to pos 3 (right, crosses boundary 2). 1 moves from pos 3 to pos 2 (left, crosses boundary 2).
- Swap 3 (boundary 1, cost 1): 2↔1. 2 moves from pos 1 to pos 2 (right, crosses boundary 1). 1 moves from pos 2 to pos 1 (left, crosses boundary 1).

Boundary 1 crossings: swap 1 (3 right, 2 left), swap 3 (2 right, 1 left). So 4 crossings, 2 swaps.
Boundary 2 crossings: swap 2 (3 right, 1 left). 2 crossings, 1 swap.

# swaps at boundary 1 = 2. By formula: #{v<=1, pos[v]>1} = 1. Discrepancy.

So the formula is wrong. The correct # of swaps at boundary i is not just #{v<=i, pos[v]>i}.

Let me reconsider. The issue is that element 2 crosses boundary 1 twice (left in swap 1, right in swap 3), but it shouldn't need to (it starts and ends at position 2). So the "wasted" crossing of element 2 contributes to the # of swaps at boundary 1.

So the minimum # of swaps at boundary i is #{v: v<=i, pos[v]>i}, but in general (and in the cost-minimizing solution), it can be more.

Hmm wait, but is the cost-minimizing solution the one with minimum swaps? Not necessarily.

OK so the problem is more subtle. Let me think about what the cost-minimizing solution looks like.

Key realization: The cost of a swap depends on the boundary. To minimize cost, we want to use cheaper boundaries (smaller i) as much as possible, and avoid expensive ones (larger i).

But the constraint is that we must sort the permutation, so each element must reach its destination.

Hmm, let me think of it as an optimization problem.

Alternative model: Consider the permutation as a set of "demands". At each step, we can swap adjacent elements, paying the cost of the left position.

I think the key insight is related to the following: process the elements in order of value. When processing v, we want to move v from pos[v] to v. But we have a choice: we can delay moving v (do other swaps first) to reduce cost.

Actually, let me think about it from the perspective of the optimal solution structure.

In the optimal solution for sample 1: 
- First, we swap (3,2) at boundary 1, cost 1.
- Then (3,1) at boundary 2, cost 2.
- Then (2,1) at boundary 1, cost 1.

Notice that the first and third swaps are at boundary 1 (cheap), and the second is at boundary 2 (expensive). The order matters.

Alternative: what if we did (3,1) at boundary 2 first, then (3,2) at boundary 1, then (2,1) at boundary 1? Let's see:
- P=(3,2,1). 
- Swap boundary 2 (3,1): positions 2,3 → swap: P=(3,1,2). Cost 2.
- Swap boundary 1 (3,1): positions 1,2 → swap: P=(1,3,2). Cost 1.
- Swap boundary 2 (3,2): positions 2,3 → swap: P=(1,2,3). Cost 2.
- Total: 2+1+2 = 5. More expensive.

So the order matters. The optimal order uses cheap boundaries more.

Insight: To sort, we can think of it as repeatedly "bubbling" elements to their positions, but we should prioritize cheap boundaries.

Let me think of it as: the minimum cost is achieved by a specific strategy. 

Hmm, here's another thought. Consider processing from left to right. At each step i, we want to ensure position i has the correct element (value i+1... wait, 0-indexed vs 1-indexed).

Let me use 1-indexed. We want position j to have value j. 

Greedy: for j = 1, 2, ..., N-1, bring value j to position j. 

To bring value j to position j, value j is at some position pos[j] >= j (assuming values 1..j-1 are already at positions 1..j-1). We move value j left from pos[j] to j by swapping at boundaries j, j+1, ..., pos[j]-1.

But this greedy might not be optimal, as we saw.

Let me reconsider. When we bring value j to position j, the cost is sum_{i=j}^{pos[j]-1} i. This is the cost if we do these swaps right now. But if we delay (do other swaps first), the cost changes.

Alternative strategy: Think of it as, for each boundary i, we use it to "process" inversions. The # of times we use boundary i = # of inversions (v, w) with v < w and the inversion is "resolved" at boundary i.

Hmm, this is getting complicated. Let me look up / recall the standard solution.

Standard solution for this problem (AtCoder ABC 224 F? or similar):

I recall now. The answer is:
- Process v from 1 to N.
- For each v, compute the cost to move v from pos[v] to v, considering the current state.

The state evolves as we place v. The key is: when we place v, the cost is sum_{i=v}^{pos[v]-1} i where pos[v] is the current position of v (which might differ from the original if other elements have been moved).

But the original pos[v] is fixed. After placing 1, 2, ..., v-1, the positions of remaining elements (v, v+1, ..., N) shift. Specifically, elements originally at positions 1..v-1 are now at 1..v-1 (sorted), so elements at original positions v..N are now at positions v..N (but their relative order is preserved, and they're shifted left by 0... wait, no).

Hmm, let me think. When we place value 1 at position 1, we swap it left from pos[1] to 1. The elements between original positions 1 and pos[1] (i.e., at positions 1, 2, ..., pos[1]-1, excluding 1 itself) shift right by 1. Wait, value 1 moves left, so the elements it swaps with move right.

So after placing 1 at position 1, the elements originally at positions 1, ..., pos[1]-1 (excluding value 1, which is at pos[1]) shift right by 1. Wait, value 1 is at pos[1]. It swaps left with pos[1]-1, pos[1]-2, ..., 1. So the elements at pos[1]-1, pos[1]-2, ..., 1 (in that order) shift right by 1.

This is getting complex. Let me think of the positions of remaining elements after placing 1..v-1.

Actually, here's a cleaner way. After placing 1..v-1 at positions 1..v-1, the remaining elements {v, v+1, ..., N} are at positions v..N in some order. The element v is at some position >= v (since positions 1..v-1 are taken).

But what is v's current position? It depends on the swaps done.

Hmm, this is where the choice of strategy matters. The greedy "place v immediately" has v at position pos'[v] where pos'[v] is determined by the swaps.

Wait, actually, if we just do the swaps to move v from its current position to v, the current position of v (after placing 1..v-1) is... let me think.

After placing 1 at position 1: the array is (1, ?, ?, ...). The ? are values {2, ..., N} in some order. The element that was at position 1 (value P[1]) is now at position 2 (if pos[1] > 1, i.e., P[1] != 1). The element at position 2 (after) is the one that was at position 2 originally, unless pos[1] = 2, in which case the original position-2 element is at position 3, etc.

This is essentially: after placing 1, the array is (1) + (original P with 1 removed, shifted). Hmm, more precisely, the elements at original positions 1, ..., pos[1]-1 (which are values P[1], ..., P[pos[1]-1], none equal to 1) are now at positions 2, 3, ..., pos[1]. And elements at original positions pos[1]+1, ..., N are at positions pos[1]+1, ..., N.

So after placing 1: array is (1, P[1], P[2], ..., P[pos[1]-1], P[pos[1]+1], ..., P[N]).

Wait, let me re-examine. Original: (P[1], P[2], ..., P[pos[1]-1], P[pos[1]], P[pos[1]+1], ..., P[N]) where P[pos[1]] = 1.

After moving 1 left from pos[1] to 1: 1 swaps with P[pos[1]-1], then P[pos[1]-2], ..., then P[1]. So the array becomes (1, P[1], P[2], ..., P[pos[1]-1], P[pos[1]+1], ..., P[N]).

Yes! So after placing 1, the subarray from position 2 onwards is (P[1], P[2], ..., P[pos[1]-1], P[pos[1]+1], ..., P[N]).

Then we place 2. Value 2 is somewhere in this subarray. We find its current position and move it to position 2.

This is equivalent to: we maintain a "current array" that is a permutation of the remaining elements. When we place v, we find v in the current array and move it to the front (position v in the original indexing, which is the front of the remaining subarray).

The cost of moving v from its current position to the front of the remaining subarray: the current position of v in the remaining subarray is some index k (1-indexed within the subarray, which corresponds to original position v - 1 + k). The swaps are at boundaries (v-1+1), (v-1+2), ..., (v-1+k-1) = v, v+1, ..., v+k-2. Cost = sum_{i=v}^{v+k-2} i.

So we need to know k, the position of v in the current remaining subarray.

The current remaining subarray (after placing 1..v-1) is a permutation of {v, v+1, ..., N}. The element v is at some position k within this subarray.

To find k efficiently, we can use a BIT or segment tree over original positions.

Specifically, let's track which original positions are "still active" (not yet removed/used). Initially, all positions 1..N are active. When we place value v (which is at original position pos[v]), we remove pos[v] from the active set.

After placing 1..v-1, the active positions are {pos[v], pos[v+1], ..., pos[N]} (the original positions of remaining values), and they correspond to current positions v, v+1, ..., N (in some order based on their original position values).

Wait, let me re-examine. After placing 1, the active original positions are {2, 3, ..., N} (since position 1 is now occupied by value 1). The remaining elements at these positions are {2, ..., N}. The current array from position 2 onwards corresponds to original positions 1, 2, ..., pos[1]-1, pos[1]+1, ..., N, in order.

Hmm wait, after placing 1, the array is (1, P[1], P[2], ..., P[pos[1]-1], P[pos[1]+1], ..., P[N]). The elements at current positions 2, 3, ..., N are P[1], P[2], ..., P[pos[1]-1], P[pos[1]+1], ..., P[N]. These correspond to original positions 1, 2, ..., pos[1]-1, pos[1]+1, ..., N. So the active original positions are {1, 2, ..., pos[1]-1, pos[1]+1, ..., N}, mapped to current positions 2, ..., N.

In general, after placing 1..v-1, the active original positions are {1, ..., N} \ {pos[1], ..., pos[v-1]}. These are mapped to current positions v, v+1, ..., N in order of their original position.

So to find the current position of v (within the remaining subarray), we count the number of active original positions <= pos[v], minus (v-1) (since the first v-1 current positions are taken).

Wait, the remaining subarray starts at current position v. The active original positions are mapped to current positions v, v+1, ..., N in order. So the active original position at index j (in sorted order) maps to current position v - 1 + j.

Value v is at original position pos[v]. Its rank among active original positions (1-indexed) = #{active original positions <= pos[v]}. Let's call this rank r. Then v is at current position v - 1 + r.

To move v to current position v, we need to shift it left by r - 1 positions. The swaps are at boundaries v, v+1, ..., v - 1 + r - 1 = v + r - 2. Cost = sum_{i=v}^{v+r-2} i.

So the cost of placing v is sum_{i=v}^{v+r-2} i where r = rank of pos[v] among active original positions.

We compute this for v = 1, 2, ..., N. Total cost = sum.

This is a known greedy strategy. Let me verify with sample 1.

P=(3,2,1), pos[1]=3, pos[2]=2, pos[3]=1.
- v=1: active original positions = {1,2,3}. rank of pos[1]=3 is 3. r=3. Cost = sum_{i=1}^{1+3-2=2} i = 1+2 = 3.
- After placing 1, active = {1, 2} (original positions of remaining values 2, 3). Wait, remaining values are {2, 3}, at original positions pos[2]=2, pos[3]=1. So active = {1, 2}.
- v=2: rank of pos[2]=2 among {1,2} is 2. r=2. Cost = sum_{i=2}^{2+2-2=2} i = 2.
- After placing 2, active = {1} (only pos[3]=1 remaining, value 3).
- v=3: rank of pos[3]=1 among {1} is 1. r=1. Cost = sum_{i=3}^{3+1-2=2} i = sum from 3 to 2 = 0 (empty).
- Total: 3+2+0 = 5.

But expected is 4! So this greedy is not optimal (as I found before).

Hmm. So the "place in order" greedy gives 5, but the optimal is 4. The difference is in the order of swaps.

In the optimal solution:
- Swap boundary 1 (3,2): cost 1.
- Swap boundary 2 (3,1): cost 2.
- Swap boundary 1 (2,1): cost 1.
- Total: 4.

In my greedy (place 1 first):
- Swap boundary 2 (3,1): cost 2. [moving 1 from pos 3 to pos 2]
- Swap boundary 1 (3,1): cost 1. [moving 1 from pos 2 to pos 1]
- Swap boundary 2 (3,2): cost 2. [moving 2 from pos 3 to pos 2]
- Total: 5.

The difference: in the optimal, boundary 2 is used once (cost 2), but in greedy, boundary 2 is used twice (cost 4). So saving 2.

How does the optimal achieve this? By first doing a cheap swap (boundary 1, cost 1) to "set up" the expensive swap to be avoidable.

Let me think about this more carefully. The issue is that placing 1 first requires moving it across boundary 2 (cost 2) and boundary 1 (cost 1). But if we first swap 3 and 2 at boundary 1 (cost 1), then 1 is still at pos 3, but 2 is at pos 1 and 3 is at pos 2. Then swapping 3 and 1 at boundary 2 (cost 2) moves 1 to pos 2 and 3 to pos 3. Then swapping 2 and 1 at boundary 1 (cost 1) moves 1 to pos 1 and 2 to pos 2.

So the optimal uses boundary 2 only once (for the swap of 3 and 1), while the greedy uses boundary 2 twice (once to move 1 past 3, and once to move 2 past 3).

Key insight: By doing a "preprocessing" swap (3↔2 at boundary 1), we reduce the work at boundary 2.

Hmm, this is like: the cost depends on the order, and we need to find the optimal order.

Let me think of the problem differently. 

Observation: The total cost = sum over all swaps of (boundary index). We want to find a sequence of swaps that sorts P with minimum total cost.

Equivalent formulation: We're building the sorted permutation by inserting elements. Think of it as: we have a target permutation (1,2,...,N), and we start with P. We apply adjacent swaps.

Another way: think of the sorted permutation as built from right to left. We can "insert" elements into the sorted prefix.

Hmm, let me think of a different greedy. 

Alternative greedy: process from right to left. For j = N, N-1, ..., 1, bring value j to position j.

Wait, let me think. The key insight might be:

When we move value v from pos[v] to v, the cost is sum of boundaries. But we can choose to "delay" the move. Specifically, we can first do other swaps that change the effective pos[v].

But pos[v] (original position) is fixed. After other swaps, v's current position changes. If we move other elements first, v's current position can change.

For example, in sample 1, value 1 is originally at pos 3. If we first swap 3 and 2 (moving 3 right and 2 left), then 1 is still at pos 3, but 3 is at pos 2 and 2 is at pos 1. Then swapping 3 and 1 moves 1 to pos 2. Then swapping 2 and 1 moves 1 to pos 1.

In this sequence, 1 moved from pos 3 to pos 2 (cost 2, swap at boundary 2) and pos 2 to pos 1 (cost 1, swap at boundary 1). So cost for 1 = 3, same as before. But the total cost is 4, not 3+2+0=5.

Wait, let me recount the optimal:
- Swap 1: boundary 1, cost 1. (3↔2)
- Swap 2: boundary 2, cost 2. (3↔1)
- Swap 3: boundary 1, cost 1. (2↔1)

Element 1: starts at pos 3. After swap 2, 1 is at pos 2 (swapped with 3). After swap 3, 1 is at pos 1 (swapped with 2). So 1's journey: pos 3 → pos 2 (swap at boundary 2) → pos 1 (swap at boundary 1). Cost for 1's swaps: 2 + 1 = 3.

Element 2: starts at pos 2. After swap 1, 2 is at pos 1 (swapped with 3). After swap 3, 2 is at pos 2 (swapped with 1). So 2's journey: pos 2 → pos 1 → pos 2. Cost for 2's swaps: 1 + 1 = 2. (2 is shuffled.)

Element 3: starts at pos 1. After swap 1, 3 is at pos 2. After swap 2, 3 is at pos 3. Cost for 3's swaps: 1 + 2 = 3.

Total cost = 3 + 2 + 3 = 8. But actual cost is 4. So summing per-element costs double-counts (each swap is counted for both elements involved).

Each swap at boundary i costs i. So total cost = sum of swap costs. In the optimal, swaps are at boundaries 1, 2, 1 with costs 1, 2, 1. Total = 4.

Each swap involves 2 elements. Sum of per-element swap costs = 2 * total cost = 8. ✓ (matches 3+2+3=8).

OK so the per-element cost sum is 2 * total. Not directly useful.

Let me reconsider the problem. 

I think the correct approach is:

Think of it as a min-cost to sort. Consider the "inversion" structure. Each pair (i, j) with i < j and P[i] > P[j] is an inversion. To resolve it, we must swap i and j at some point, which requires a sequence of adjacent swaps. The inversions that cross boundary k contribute to the cost of boundary k.

Hmm, let me think about the cost differently. 

Consider that the sorted permutation (1, 2, ..., N) is built by inserting values 1, 2, ..., N in order. When we insert value v, it goes to position v, and elements originally at positions v, v+1, ... shift right.

But the cost of insertion depends on how we do it. If we insert v at the current position v (which might not be its original position), the cost is the sum of boundaries v to v+k-1 where k is v's current rank in the remaining array.

Hmm, I think I need to reconsider the greedy.

Let me reconsider the greedy. In the greedy "place v from 1 to N", the cost of placing v is sum_{i=v}^{v+r-2} i where r is the rank of v in the remaining array. This gave 5 for sample 1, but optimal is 4.

The issue: this greedy doesn't account for the fact that we can "pre-sort" elements to reduce future costs.

Hmm wait, but in the greedy, when we place v, we're doing the minimum-cost sequence to move v to position v. Any other order would either cost more for placing v or not change the remaining array in a useful way.

Let me reconsider. After placing 1, the remaining array is (P[1], P[2], ..., P[pos[1]-1], P[pos[1]+1], ..., P[N]) starting at current position 2.

In the optimal, after the first swap (3↔2 at boundary 1), the array is (2, 3, 1). This is not the same as the greedy's state after placing 1, which would be (1, 3, 2).

So the optimal doesn't "place 1 first". It does other swaps first.

I think the correct greedy is: place values in a different order, or use a different strategy.

Let me think... Actually, I recall now that for this problem, the answer is computed by processing values in order, but the cost formula is different. Let me re-derive.

OK here is a key insight I was missing. The problem is equivalent to:

We process values v = 1, 2, ..., N. We maintain the current array. The cost of the entire process is the sum of costs of all swaps.

Claim: The minimum cost is achieved by the following greedy: process v = 1, 2, ..., N. When processing v, find v in the current array and move it to the front (position v). The cost of this move is sum of boundary indices.

Wait, I did this and got 5, not 4. So this greedy is wrong.

Let me re-examine. In the optimal, value 1 ends up at position 1 via swaps at boundaries 2 and 1 (cost 2+1=3). In the greedy, value 1 also ends up at position 1 via swaps at boundaries 2 and 1 (cost 2+1=3). So the cost for value 1 is the same.

But in the optimal, the total cost is 4, meaning the other swaps cost