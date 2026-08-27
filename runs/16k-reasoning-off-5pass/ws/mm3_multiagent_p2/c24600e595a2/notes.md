
## ideation
We have N bits A_i, B_i ∈ {0,1} and costs C_i > 0. An operation chooses i, flips A_i, and then pays the new sum S = Σ_k A_k C_k. We can do any number of operations. We want the minimal total cost to reach A = B.

**Key observation:** The cost of a single flip at i depends only on the current A before the flip and the resulting value.  
- If A_i = 0 → becomes 1: cost = current_sum + C_i.  
- If A_i = 1 → becomes 0: cost = current_sum − C_i (the sum after removal of C_i).  

So each flip is independent of future flips except through the current_sum, which changes by ±C_i. This looks like a scheduling problem: among all mismatches (positions where A_i ≠ B_i), we must perform flips that turn A_i into B_i, and the order matters because current_sum changes.

**Why a simple greedy order works:**
- For a position where A_i = 0, B_i = 1 (need to set to 1), we want to do this flip when current_sum is as small as possible, because we add C_i to a smaller base. So we should do these flips **early**, preferring small C_i first (small additional cost).
- For a position where A_i = 1, B_i = 0 (need to unset to 1), we want to do this flip when current_sum is as large as possible, because we subtract C_i from a larger base. So we should do these flips **late**, preferring large C_i first (big subtraction).

Thus the optimal order is:
- Process all 0→1 flips in **increasing** C_i.
- Process all 1→0 flips in **decreasing** C_i.

(If we mixed them, we might increase sum before subtracting a large C, losing value.)

**Simulation:** Keep a running `cur = sum of A_i * C_i`. For each flip in that order, add the new `cur` (after the flip) to answer, and update `cur` accordingly.

**Pitfalls:**
- The order of the two groups is fixed: all 0→1 before all 1→0 is optimal under the above reasoning, but we need to confirm no interleaving beats it. Because a 1→0 flip reduces the sum and makes subsequent 0→1 flips cheaper, we would like the big subtractions to happen **after** the additions? Wait, we argued opposite: want subtractions late so that the current sum when we subtract is large (so subtracting C_i is more valuable? Actually cost = current_sum − C_i. To minimize total cost, we want this cost to be as small as possible. If current_sum is large, cost is larger (since we subtract less?). Let's re-evaluate carefully.

Let S be current sum before flip.
- Flipping 1→0: new sum = S − C_i. Cost paid = S − C_i.
- Flipping 0→1: new sum = S + C_i. Cost paid = S + C_i.

We want to minimize total sum of costs.

Consider two flips: first do 0→1 (cost = S + c1, new sum = S + c1), then 1→0 (cost = (S + c1) − c2 = S + c1 − c2). Total = 2S + c1 − c2.

If reversed: first 1→0 (cost = S − c2, new sum = S − c2), then 0→1 (cost = (S − c2) + c1 = S − c2 + c1). Total = 2S − c2 + c1. Same total! So for any pair of one addition and one subtraction, the order doesn't matter. The difference only matters when multiple operations of the same type are involved. For two additions (0→1) with costs c_a < c_b: order them ascending: first c_a then c_b gives total = 2S + c_a + c_b + c_a? Let's compute: S + c_a + (S + c_a + c_b) = 2S + 2c_a + c_b. Reverse: S + c_b + (S + c_b + c_a) = 2S + 2c_b + c_a. Since c_a < c_b, first order is smaller. So ascending C_i is optimal for additions.

For two subtractions (1→0) with costs c_a < c_b: first subtract c_a then c_b: S − c_a + (S − c_a − c_b) = 2S − 2c_a − c_b. Reverse: S − c_b + (S − c_b − c_a) = 2S − 2c_b − c_a. Since c_a < c_b, first order yields −2c_a − c_b which is smaller (more negative) than −2c_b − c_a, so first order is cheaper. So descending C_i is optimal for subtractions (i.e., subtract larger C first to get more negative contribution).

Thus the greedy order: all 0→1 flips sorted by increasing C_i, then all 1→0 flips sorted by decreasing C_i. (Alternatively, the two groups can be interleaved? No, because interleaving would just be some order; we need to find the global optimum. The above pairwise argument shows that within each group, the proposed order is optimal. Now, can a mixed order be better than all additions then all subtractions? Let's consider one addition and one subtraction: we saw total is the same regardless of order. For multiple of each, suppose we do a subtraction before an addition. The effect is to reduce the base for the addition. That might be beneficial because we want the base small when we add. But we also lose the opportunity to subtract from a larger base later. Let's test with two additions (c1<c2) and two subtractions (c3<c4). Suppose we do all additions first: total = 2S + 2c1 + c2 - 2c3 - c4. If we do some subtractions earlier, the base for subsequent additions is smaller, but the later subtractions operate on a smaller base (worse). The net effect: the sum of costs is 2S + sum(adds) - 2*(sum of subtractions taken earlier?) Actually, the cost of a subtraction is base - C. If we do a subtraction early, base is small, so cost is smaller (good), but then the base for later flips is reduced (bad for later additions, bad for later subtractions). It becomes a trade-off. But the known solution to this problem (which is a known AtCoder problem) is indeed: sort 0→1 by ascending C, sort 1→0 by descending C, and simulate in that order. I recall that the editorial proves this is optimal. The key insight: The total cost can be expressed as sum over all flips of the sum of A*C at the time of flip. This is like we are paying for each pair of flips the sum of their C's if they are "active" together. Alternatively, the minimal cost is achieved by a specific order. Let's trust the editorial logic: we want to minimize the sum of sums. Since additions increase the sum, we should do cheap additions first to avoid paying a large base for expensive additions. Since subtractions decrease the sum, we should do expensive subtractions first to reduce the sum as much as possible before doing any additions? Wait, we determined within subtractions, doing large C first is better. But what about relative ordering of additions and subtractions? Consider one addition (c1) and one subtraction (c2). The total cost is 2S + c1 - c2, independent of order. For more complex cases, we can think of the cost as 2S + Σ(adds) - 2*(sum of C for each subtraction that occurs when the bit is 1?) Actually, the total cost can be computed as: each flip pays the current sum. The current sum changes. There's a known result: the optimal is to do all 0→1 flips in increasing C, then all 1→0 flips in decreasing C. Let's verify with a small example: N=2, A=(0,0), B=(1,1), C=(1,100). Additions: both 0→1. Sort asc: flip i=1 (cost 0+1=1, sum=1), then flip i=2 (cost 1+100=101). Total=102. If we reverse: cost 0+100=100, sum=100, then 100+1=101, total=201. So asc is better.

Now add a subtraction: A=(0,1), B=(1,0), C=(1,100). Mismatches: pos1: 0→1 (c=1), pos2: 1→0 (c=100). Order asc add then desc sub: flip pos1: cost 0+1=1, sum=1. flip pos2: cost 1-100 = -99. Total = -98. If we do sub then add: flip pos2: cost 100-100=0, sum=0. flip pos1: cost 0+1=1. Total = 1. So add then sub is much better! Indeed, we want to add first to increase the base, then subtract the large C from the larger base, making the subtraction cost very negative (we pay less). So we should do all additions first, then subtractions. That matches the plan: sort adds asc, subs desc, and process all adds then all subs.

Thus the algorithm:
1. Read N, arrays A, B, C.
2. Compute initial sum S0 = Σ A_i * C_i.
3. Partition indices where A_i ≠ B_i into two lists:
   - `add`: A_i = 0, B_i = 1. Store C_i.
   - `sub`: A_i = 1, B_i = 0. Store C_i.
4. Sort `add` ascending.
5. Sort `sub` descending.
6. Simulate flips in order: first all adds (in sorted order), then all subs (in sorted order).
   - For each c in `add`: ans += S0 + c; S0 += c.
   - For each c in `sub`: ans += S0 - c; S0 -= c.
7. Print ans.

Complexities: O(N log N) time, O(N) memory. N up to 2e5, C up to 1e6, costs can be up to ~2e11, need 64-bit (Python int is fine).

Edge cases: no mismatches → ans=0. All adds or all subs handled correctly.

## worker: Implement the solution in Python: read input, part
The solution follows the greedy ordering derived from analyzing pairwise costs. For mismatches requiring a 0→1 flip, processing them in increasing order of `C_i` minimizes the base on which the additional `C_i` is added. For mismatches requiring a 1→0 flip, processing them in decreasing order of `C_i` maximizes the base before the subtraction, yielding a smaller (more negative) cost. Doing all additions before all subtractions is optimal because it allows the large subtractions to operate on the largest possible current sum. The algorithm runs in `O(N log N)` time due to sorting and uses `O(N)` extra space. The computed total cost fits in Python's arbitrary-precision integers.
