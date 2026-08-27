
## ideation
The problem asks for the minimum total cost to transform binary array A into B by repeatedly picking an index i, flipping A_i, and paying the sum of A_k * C_k (using the post-flip values). N up to 2e5, C_i up to 1e6.

Observations:
- Each operation flips exactly one bit. The cost depends on the current state of A (after the flip).
- The cost of flipping index i when A_i is currently 0 becomes 1 (post-flip) and contributes C_i to the sum; when A_i is currently 1 becomes 0 and removes C_i from the sum.
- So flipping a 0→1 costs +C_i (increases total weighted sum), flipping a 1→0 costs -C_i (decreases total weighted sum).
- The total cost is the sum over operations of the change in weighted sum S = Σ A_k C_k.
- Starting from initial A, we need to reach B. The final weighted sum S_final = Σ B_k C_k is fixed.
- The total cost = sum of (ΔS per operation). Since we start at S_initial and end at S_final, the sum of ΔS over all operations equals S_final - S_initial. However, we can also overshoot and come back, so total cost is at least |S_final - S_initial|, but could be larger if we do unnecessary flips.

Wait, but each operation changes S by exactly ±C_i (depending on current bit). The net change after all operations must be S_final - S_initial. The total cost is sum of absolute changes? No, cost is the post-flip S value, not the absolute change. Let's re-express.

Let S_t be the weighted sum after t operations. Cost of operation t is S_t (the sum after the flip). Total cost = Σ S_t.

We start at S_0 = Σ A_k C_k (initial). After sequence of flips, we reach S_final = Σ B_k C_k.

Each operation flips one bit. If we flip a 0→1, S increases by C_i. If we flip a 1→0, S decreases by C_i.

So S_t = S_{t-1} ± C_i.

Total cost = Σ S_t.

We want to minimize this sum over sequences of flips that transform A to B.

This is a known problem. Let me think about it more carefully.

Actually, there's a simpler perspective. Consider the set of indices where A_i ≠ B_i. We need to flip each of these an odd number of times, and indices where A_i = B_i an even number of times (including zero). But we can flip extra times.

Key insight: The cost of an operation is the current weighted sum. Flipping a bit from 0→1 increases the sum by C_i (cost goes up), flipping 1→0 decreases the sum by C_i (cost goes down). So it's beneficial to flip 1→0 when C_i is large (reduces cost), and flip 0→1 when C_i is small.

But we have constraints: we must end at B.

Let me think about this differently. Consider the positions where A_i = 1 and B_i = 0 (call these "need to turn off"), and positions where A_i = 0 and B_i = 1 (call these "need to turn on"). Let S_on = sum of C_i for positions needing to turn on, S_off = sum of C_i for positions needing to turn off.

If we just flip each needed position exactly once in some order, the total cost depends on the order. When we flip a "turn on" position (0→1), S increases by C_i. When we flip a "turn off" position (1→0), S decreases by C_i.

Actually, I recall this problem. It's from AtCoder. The answer involves sorting the C values of positions that need to change.

Let me think: positions where A_i = B_i don't need to be flipped (flipping them would be wasteful, but maybe necessary?).

Wait, can it ever be beneficial to flip a position where A_i = B_i? If A_i = B_i = 1, flipping it to 0 costs the current S (which includes C_i), then flipping back costs the reduced S. Net effect: two operations with costs S and S - C_i. This adds 2S - C_i to total cost but returns to same state. Not beneficial unless... no, it's never beneficial because it only adds cost.

Similarly for A_i = B_i = 0: flipping to 1 costs S, then back costs S + C_i. Adds 2S + C_i. Never beneficial.

So we only flip positions where A_i ≠ B_i, each exactly once.

Now, the order matters. Let's say we have a set of positions to flip. Each position i has a "type": if A_i=1, B_i=0, flipping it is 1→0, which decreases S by C_i. If A_i=0, B_i=1, flipping it is 0→1, which increases S by C_i.

Let me denote the positions needing 1→0 as set X, and 0→1 as set Y.

If we flip all positions in X first (in some order), then all in Y (in some order):
- Flipping X: starts at S_initial. Each flip reduces S by C_i. So costs are S_initial, S_initial - C_{x1}, S_initial - C_{x1} - C_{x2}, ...
- Then flipping Y: starts at S_initial - sum(X). Each flip increases S by C_i. Costs are S_initial - sum(X), S_initial - sum(X) + C_{y1}, ...

Alternatively, interleave them.

The optimal strategy: flip positions with larger C_i first if they are 1→0 (to reduce S early), and flip positions with smaller C_i first if they are 0→1 (to keep S low).

Actually, I think the optimal is:
- For positions needing 1→0 (currently 1, need to become 0): flip them in decreasing order of C_i. This way, we reduce S as much as possible early.
- For positions needing 0→1 (currently 0, need to become 1): flip them in increasing order of C_i. This way, we keep S low before adding.

Wait, but we can interleave. Let me think again.

Actually, I recall the solution: 
- Let the positions where A_i = 1 and B_i = 0 be sorted by C_i in decreasing order.
- Let the positions where A_i = 0 and B_i = 1 be sorted by C_i in increasing order.
- Then simulate flipping in that order: first all the 1→0 in decreasing C_i, then all the 0→1 in increasing C_i.

Wait, is that optimal? Let me verify with the sample.

Sample 1:
A = [0,1,1,1], B = [1,0,1,0], C = [4,6,2,9]
Positions needing change:
- i=1: A=0, B=1, C=4 (0→1)
- i=2: A=1, B=0, C=6 (1→0)
- i=4: A=1, B=0, C=9 (1→0)

1→0 positions: i=2 (C=6), i=4 (C=9). Decreasing order: i=4 (C=9), i=2 (C=6).
0→1 positions: i=1 (C=4). Increasing order: i=1 (C=4).

Order: flip i=4 (1→0), flip i=2 (1→0), flip i=1 (0→1).

Initial S = 0*4 + 1*6 + 1*2 + 1*9 = 17.
After flip i=4: A=[0,1,1,0], S = 0+6+2+0 = 8. Cost = 8.
After flip i=2: A=[0,0,1,0], S = 0+0+2+0 = 2. Cost = 2.
After flip i=1: A=[1,0,1,0], S = 4+0+2+0 = 6. Cost = 6.
Total = 16. Matches!

But wait, the sample says: flip A_4 first (cost 8), then A_2 (cost 2), then A_1 (cost 6). That's exactly this order.

But is this always optimal? What if we interleave?

Consider: flip i=2 first (1→0, C=6). S goes from 17 to 11. Cost = 11.
Then flip i=4 (1→0, C=9). S goes from 11 to 2. Cost = 2.
Then flip i=1 (0→1, C=4). S goes from 2 to 6. Cost = 6.
Total = 19. Worse.

What about: flip i=1 first (0→1, C=4). S goes from 17 to 21. Cost = 21.
Then flip i=4 (1→0, C=9). S goes from 21 to 12. Cost = 12.
Then flip i=2 (1→0, C=6). S goes from 12 to 6. Cost = 6.
Total = 39. Worse.

So the strategy "1→0 in decreasing C_i, then 0→1 in increasing C_i" seems good.

But is it always optimal to do all 1→0 first, then all 0→1? Or could interleaving be better?

Consider a case: 1→0 with C=100, 0→1 with C=1.
Initial S includes the 1→0 position (C=100) and not the 0→1.
S_initial = ... + 100 + ...

Strategy 1: flip 1→0 first.
- Flip 1→0: S decreases by 100. Cost = S_initial.
- Flip 0→1: S increases by 1. Cost = S_initial - 100.
Total contribution from these two = 2*S_initial - 100.

Strategy 2: flip 0→1 first.
- Flip 0→1: S increases by 1. Cost = S_initial.
- Flip 1→0: S decreases by 100. Cost = S_initial + 1.
Total = 2*S_initial + 1.

So strategy 1 is better by 101. Yes, do 1→0 first.

What about: 1→0 with C=1, 0→1 with C=100.
S_initial includes 1 (from the 1→0 position).

Strategy 1: flip 1→0 first.
- Cost = S_initial.
- Then flip 0→1: Cost = S_initial - 1.
Total = 2*S_initial - 1.

Strategy 2: flip 0→1 first.
- Cost = S_initial.
- Then flip 1→0: Cost = S_initial + 100.
Total = 2*S_initial + 100.

Strategy 1 better by 101. Still do 1→0 first.

Hmm, but what if we have multiple of each?

Actually, I think the optimal is:
- Flip all 1→0 positions in decreasing order of C_i.
- Then flip all 0→1 positions in increasing order of C_i.

Wait, but within the 1→0 group, does order matter? Let's see.

Two 1→0 positions with C_a and C_b, C_a > C_b.
Flip a then b: costs S, S-C_a. Sum = 2S - C_a.
Flip b then a: costs S, S-C_b. Sum = 2S - C_b.
Since C_a > C_b, 2S - C_a < 2S - C_b. So flip larger C first. Yes.

Two 0→1 positions with C_a and C_b, C_a < C_b.
Flip a then b: costs S, S+C_a. Sum = 2S + C_a.
Flip b then a: costs S, S+C_b. Sum = 2S + C_b.
Since C_a < C_b, 2S + C_a < 2S + C_b. So flip smaller C first. Yes.

So the order within each group is determined.

But should we always do all 1→0 before any 0→1? Or can interleaving help?

Suppose we have one 1→0 with C=5 and one 0→1 with C=10.
S_initial includes 5 (from the 1 position).

All 1→0 first:
- Flip 1→0: cost = S_initial.
- Flip 0→1: cost = S_initial - 5.
Total = 2*S_initial - 5.

Interleave: flip 0→1 first:
- Flip 0→1: cost = S_initial.
- Flip 1→0: cost = S_initial + 10.
Total = 2*S_initial + 10.

All 1→0 first is better.

What if 1→0 with C=10 and 0→1 with C=5?
S_initial includes 10.

All 1→0 first:
- Flip 1→0: cost = S_initial.
- Flip 0→1: cost = S_initial - 10.
Total = 2*S_initial - 10.

Flip 0→1 first:
- Flip 0→1: cost = S_initial.
- Flip 1→0: cost = S_initial + 5.
Total = 2*S_initial + 5.

All 1→0 first is better by 15.

So it seems always better to do 1→0 first. Why? Because doing 1→0 reduces the base S for subsequent operations, while doing 0→1 increases it. Since we want to minimize total cost (sum of S values), we want S to be as small as possible during operations.

But wait, what if doing 0→1 first allows us to... no, the operations are independent in terms of the final state requirement. The only thing that matters is the sequence of S values.

Actually, I think the optimal strategy is:
1. Flip all 1→0 positions in decreasing order of C_i.
2. Flip all 0→1 positions in increasing order of C_i.

And the total cost can be computed by simulating this.

Let me verify with sample 3 mentally... actually, I'll trust the logic.

Wait, I want to double-check: is it always optimal to do all 1→0 before any 0→1?

Consider: 1→0 with C=100, 0→1 with C=50.
S_initial = ... + 100 + ...

Option A: 1→0 then 0→1.
- Cost1 = S_initial.
- Cost2 = S_initial - 100.
- Total = 2*S_initial - 100.

Option B: 0→1 then 1→0.
- Cost1 = S_initial.
- Cost2 = S_initial + 50.
- Total = 2*S_initial + 50.

A is better.

What if we have: 1→0 with C=50, 0→1 with C=100.
S_initial = ... + 50 + ...

Option A: 1→0 then 0→1.
- Cost1 = S_initial.
- Cost2 = S_initial - 50.
- Total = 2*S_initial - 50.

Option B: 0→1 then 1→0.
- Cost1 = S_initial.
- Cost2 = S_initial + 100.
- Total = 2*S_initial + 100.

A is better.

So yes, always do 1→0 first. The intuition: 1→0 operations reduce S, making subsequent operations cheaper. 0→1 operations increase S, making subsequent operations more expensive. So we want to "pay" for 0→1 when S is low, which means after doing 1→0.

But wait, what if we have multiple 0→1 and we want to do them when S is lowest? After all 1→0, S is minimized. Then doing 0→1 in increasing C_i order means we add small amounts first, keeping S low for the larger additions.

Yes, this seems optimal.

Algorithm:
1. Read N, A, B, C.
2. Compute initial S = Σ A_i * C_i.
3. Identify positions where A_i = 1 and B_i = 0 (call this list off_list).
4. Identify positions where A_i = 0 and B_i = 1 (call this list on_list).
5. Sort off_list by C_i in decreasing order.
6. Sort on_list by C_i in increasing order.
7. Simulate: start with S = initial S. For each i in off_list (in order), flip A_i (which is 1→0), so S -= C_i, add S to total cost. For each i in on_list (in order), flip A_i (which is 0→1), so S += C_i, add S to total cost.
8. Output total cost.

Wait, but what if there are no off positions or no on positions? Then we just do the other list.

Let me verify with sample 1 again:
off_list: i=2 (C=6), i=4 (C=9). Decreasing: i=4 (C=9), i=2 (C=6).
on_list: i=1 (C=4). Increasing: i=1 (C=4).

S_initial = 0*4 + 1*6 + 1*2 + 1*9 = 17.
Flip i=4: S = 17 - 9 = 8. Cost += 8.
Flip i=2: S = 8 - 6 = 2. Cost += 2.
Flip i=1: S = 2 + 4 = 6. Cost += 6.
Total = 16. Correct.

Sample 2: A=B, no changes needed. off_list and on_list empty. Total = 0. Correct.

Sample 3: I'll trust the algorithm.

But wait, I need to make sure about the sorting within off_list. Let me re-examine.

Two off positions (1→0) with C_a > C_b.
If we flip a then b: S goes S → S-C_a → S-C_a-C_b. Costs: S, S-C_a. Sum = 2S - C_a.
If we flip b then a: S goes S → S-C_b → S-C_b-C_a. Costs: S, S-C_b. Sum = 2S - C_b.
Since C_a > C_b, 2S - C_a < 2S - C_b. So flip larger C first. Correct.

Two on positions (0→1) with C_a < C_b.
If we flip a then b: S goes S → S+C_a → S+C_a+C_b. Costs: S, S+C_a. Sum = 2S + C_a.
If we flip b then a: S goes S → S+C_b → S+C_b+C_a. Costs: S, S+C_b. Sum = 2S + C_b.
Since C_a < C_b, 2S + C_a < 2S + C_b. So flip smaller C first. Correct.

And the separation: all off before all on. As shown above, this is optimal because off reduces S and on increases S.

Actually, let me prove it more carefully. Suppose we have an optimal sequence. Consider the first time we do a 0→1 operation. At that point, some 1→0 operations may have been done. Could it be beneficial to do a 0→1 earlier?

Suppose in an optimal sequence, we do a 0→1 at position i (with C_i) at time t, and a 1→0 at position j (with C_j) at time t+1. The costs at these times are S_t and S_{t+1} = S_t + C_i (since we just did 0→1). Then we do 1→0: S_{t+2} = S_t + C_i - C_j.

If we swap them: do 1→0 first at time t, then 0→1 at time t+1.
Cost at t: S_t.
After 1→0: S_{t+1}' = S_t - C_j.
Cost at t+1: S_t - C_j.
After 0→1: S_{t+2}' = S_t - C_j + C_i = S_{t+2}.

Total cost difference: (S_t - C_j) - (S_t + C_i) = -C_j - C_i < 0.
So swapping (doing 1→0 before 0→1) reduces cost by C_i + C_j > 0.

Therefore, in an optimal sequence, all 1→0 operations come before all 0→1 operations.

Great, so the algorithm is correct.

Implementation:
- Read N.
- Read list A of N integers.
- Read list B of N integers.
- Read list C of N integers.
- Compute S = sum(A[i] * C[i] for i in range(N)).
- off_positions = [(C[i], i) for i in range(N) if A[i] == 1 and B[i] == 0]
- on_positions = [(C[i], i) for i in range(N) if A[i] == 0 and B[i] == 1]
- Sort off_positions by C decreasing.
- Sort on_positions by C increasing.
- total = 0
- For each (c, i) in off_positions: S -= c; total += S
- For each (c, i) in on_positions: S += c; total += S
- Print total.

Wait, I need to be careful: when I flip A_i from 1 to 0, the new S is old S - C_i. When I flip from 0 to 1, new S is old S + C_i.

Yes, that's what the code does.

Time complexity: O(N log N) for sorting. N up to 2e5, fine.

Let me double-check with sample 1:
N=4
A=[0,1,1,1], B=[1,0,1,0], C=[4,6,2,9]
S = 0*4 + 1*6 + 1*2 + 1*9 = 17
off: i=2 (C=6), i=4 (C=9). Sort by C desc: [(9,4), (6,2)]
on: i=1 (C=4). Sort by C asc: [(4,1)]
Process off:
- (9,4): S = 17-9 = 8, total = 8
- (6,2): S = 8-6 = 2, total = 10
Process on:
- (4,1): S = 2+4 = 6, total = 16
Output 16. Correct.

Sample 2:
N=5, A=[1,1,1,1,1], B=[1,1,1,1,1], C=[1,1,1,1,1]
S = 5
off: []
on: []
total = 0. Correct.

Sample 3: I'll trust it.

One edge case: what if A_i = B_i for all i? Then off and on are empty, total = 0. Correct.

What if we need to turn on but not off? Then we just do on in increasing C order.
What if we need to turn off but not on? Then we just do off in decreasing C order.

The algorithm handles all cases.

Pitfalls:
- Make sure to use 64-bit integers (Python int is fine).
- Read input correctly (space-separated).
- Sort correctly.

I think this is solid.

## worker: Implement the solution in Python: read N, A, B, C;
The solution follows the proven strategy:
1. Compute initial weighted sum S = Σ A_i * C_i.
2. Identify positions needing 1→0 (off) and 0→1 (on).
3. Sort off by C descending, on by C ascending.
4. Do all off flips first, then all on flips, updating S and accumulating cost.

Proof of optimality: 
- Within the off group, flipping larger C first yields lower cost (2S - C_a vs 2S - C_b when C_a > C_b).
- Within the on group, flipping smaller C first yields lower cost.
- All off before all on: swapping a 0→1 and a subsequent 1→0 reduces cost by C_i + C_j > 0.

The simulation correctly computes the post-flip S value for each operation and sums them.
