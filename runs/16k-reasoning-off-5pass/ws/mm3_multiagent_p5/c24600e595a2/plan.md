We can only flip bits individually. The order of flips is free, but each flip's cost depends on the current A. Since cost is linear in the sum of A_k*C_k after the flip, we can think of each operation as paying a price that depends on the state we are in.

Key observation: For a bit that is currently 0, flipping it to 1 costs `0 + c_i` plus the current total cost (since we add c_i to the sum). Actually: cost = sum(C_k where A_k=1 after flip). So if currently A has sum S of A_k*C_k, and we flip a 0 at i to 1, new cost = S + c_i. If we flip a 1 at i to 0, new cost = S - c_i.

So this is like we have a value S, and we can repeatedly add or subtract c_i for each i, with the constraint that we start from S0 = sum of c_i where A_i=1, and we want to reach Sf = sum of c_i where B_i=1. At each step we can add c_i (if current A_i=0) or subtract c_i (if A_i=1). The total cost paid is the sum of all intermediate S values.

We want to minimize the sum of S after each operation. This is equivalent to: we can reorder operations. Flipping 0→1 and 1→0 on the same i multiple times is wasteful (costs 0 net change but pays 2S which is positive), so optimal does at most one flip per index.

We need to choose for each i where A_i ≠ B_i: either flip 0→1 or flip 1→0. But wait, if A_i=0 and B_i=1, we must flip it 0→1 (add c_i). If A_i=1 and B_i=0, we must flip it 1→0 (subtract c_i). So the operations are determined! Each differing index must be flipped exactly once in the determined direction.

So the only choice is the **order** of these mandatory flips. We need to order a set of "+c_i" ops and "-c_i" ops to minimize sum of cumulative S.

Let P = multiset of c_i for indices where A_i=0, B_i=1 (positive flips, add c_i).
Let M = multiset of c_i for indices where A_i=1, B_i=0 (negative flips, subtract c_i).

Let S0 = initial sum = sum of c_i where A_i=1.

We need to interleave P and M. Let |P|=p, |M|=m. Total ops = p+m. We want to minimize sum of S after each op.

Greedy: When we have both types, we should pick the operation that makes S smaller (or equivalently, if S is large, subtract; if S is small, add). This is like: among remaining ops, choose the one that brings S closer to some target.

Let's think: S starts at S0. We apply +c for p ops and -c for m ops. Final S = S0 + sum(P) - sum(M) = Sf (sum of c_i where B_i=1). Good.

We want to minimize sum of intermediate S values. S starts at S0, ends at Sf, goes up and down. Since all c_i are positive, and we want to minimize the sum, we should keep S as small as possible throughout. That means:
- When we must do a "+c" op, we want S to be small at that time. So do all "+c" ops first? No wait, that would make S large.
- Actually we want to avoid S being large. Adding c increases S; subtracting c decreases S. So we should subtract (do "-c" ops, i.e., M ops) when S is large, and add when S is small... but we must do all ops.

Hmm, let me think differently. Consider the sequence of S values: S0, S1, ..., S_{p+m}=Sf. Each step changes S by +c or -c. We minimize sum of S_0 + S_1 + ... + S_{p+m-1} (since last operation's cost is the S after it, which equals Sf; wait actually there are p+m operations, and the cost of the last operation is the S after the last flip, which is Sf. The cost of the first operation is S1, ..., last is S_{p+m} = Sf. So we sum S_1 through S_{p+m}, or equivalently S_0 through S_{p+m-1} shifted... let me re-examine.

Operation 1: flip, then pay current sum S_1. Operation k: pay S_k. Last op pays S_{p+m} = Sf. So total cost = S_1 + S_2 + ... + S_{p+m}.

Equivalently, since S_0 is not paid (no op before), and S_{p+m} = Sf is paid, we pay S_1..S_{p+m}.

This equals: p+m terms. The sum of S values visited (after each op). Starting at S_0 (not counted as cost), ending at S_{p+m}=Sf (counted as cost of last op).

To minimize, we want S to stay small. When forced to do a +c op, it increases S. When forced to do a -c op, it decreases S. We should arrange so S doesn't get too large.

Claim: optimal strategy is greedy by current S. Among remaining ops, pick the one (if exists) that results in smaller S. If both are available, pick the smaller c (add small or subtract small appropriately)... actually:

If we have a +c op available and a -d op available, and current S is large, subtracting d brings S down by d, adding c brings S up by c. We should pick the one giving smaller S: min(S+c, S-d). So we subtract if S-d < S+c, i.e., always subtract when d>0 (which it is). Wait, S-d < S+c always since d,c>0. So we should always prefer subtracting?

But we must do all ops. So: we should do all "-c" (M) ops as early as possible, and "+c" (P) ops as late as possible? Let's check with sample.

Sample 1: S0 = c_2+c_3+c_4 = 6+2+9=17 (A=(0,1,1,1)). B=(1,0,1,0). P = {c_1=4}, M = {c_2=6, c_4=9}. p=1, m=2.

If we do M first: S=17→11 (sub 6)→2 (sub 9), then P: S=2→6 (add 4). Costs paid: 11+2+6=19. Hmm not 16.

Sample says optimal: flip A4 (sub 9): S 17→8. Then flip A2 (sub 6): S 8→2. Then flip A1 (add 4): S 2→6. Costs: 8+2+6=16. Same as my reorder? Both do M,M,P. S sequence: 8,2,6. Sum=16. My first: 11,2,6 sum=19. Oh! The difference is order within M: subtract larger c first (9 then 6) gives 8,2 vs subtract smaller first (6 then 9) gives 11,2. So within same-type ops, order matters too!

So greedy by "always subtract" is correct, but we need to order the subtracts by decreasing c (subtract largest first to bring S down fastest) and adds by increasing c (add smallest first to keep S low). But this depends on interleaving.

Actually the full greedy: at each step, among all available ops, pick the one that minimizes the *resulting* S. Resulting S after +c is S+c; after -c is S-c. We want min. So we compare S+c vs S-d, but we pick whichever is smaller. Since we must do all, we need to think globally.

Equivalently, this is a classic problem: we have a set of increments +a_i and decrements -b_j, minimize sum of partial sums. 

This can be solved by: sort the decrements (M) in decreasing order, sort the increments (P) in increasing order. Then the optimal is to interleave them greedily: at each step, do whichever keeps S minimal... but as shown, doing all M in decreasing order then all P in increasing order: S goes S0, S0-m_1, S0-m_1-m_2, ..., then S0-sum(M)+p_1, ..., Sf. 

But is that optimal? Let's check if interleaving could be better. Suppose we have one M (value d) and one P (value a). S0. Option 1 (M then P): S goes S0→S0-d→S0-d+a. Costs: (S0-d)+(S0-d+a) = 2S0-2d+a. Option 2 (P then M): S0→S0+a→S0+a-d. Costs: (S0+a)+(S0+a-d) = 2S0+2a-d. Difference: Option1 - Option2 = (2S0-2d+a)-(2S0+2a-d) = -2d+a-2a+d = -a-d <0. So Option 1 (M first) is always better. Good.

With multiple of each, generalizing: do all M before all P? Let's check 2M, 2P. M={d1,d2}, P={a1,a2}. 

All M then all P (with M in some order, P in some order): S0, S0-D1, S0-D1-D2, S0-D+a1, S0-D+a1+a2. Cost = (S0-D1)+(S0-D1-D2)+(S0-D+a1)+(S0-D+a1+a2) = 4S0 - 2D1 - 2D2 - D - wait let me recompute. D = d1+d2. Costs: C1=S0-d_{π(1)}, C2=S0-d_{π(1)}-d_{π(2)}, C3=S0-D+a_{σ(1)}, C4=S0-D+a_{σ(1)}+a_{σ(2)}.

Sum = 4S0 - 2(d_{π(1)}+d_{π(2)}) - (D) ... let me just expand: 
= S0 - d1' + S0 - d1' - d2' + S0 - D + a1' + S0 - D + a1' + a2'
where d1',d2' permuted, a1',a2' permuted.
= 4S0 - 2d1' - 2d2' - D + 2a1' + a2'... wait 
= 4S0 - 2(d1'+d2') - D + (a1') + (a1'+a2') 
= 4S0 - 2D - D + 2a1' + a2'
= 4S0 - 3D + 2a1' + a2'.

To minimize, we want d1'+d2' maximized (so d's large first → d1'=larger, but coefficient is -2 for both so order of d doesn't matter in this expression! -2D either way). For a's: 2a1'+a2' minimized → a1' small, a2' next. So M in any order, P in increasing order.

Alternative: P then M. S0, S0+a, S0+a1+a2, S0+A-d1, S0+A-D. Costs: (S0+a1')+(S0+A)+(S0+A-d1')+(S0-D). Sum = 4S0 + 3A - 2d1' - d2'. Minimize: maximize d1' (do large d first). But compare to "M then P": cost = 4S0 -3D + 2a1'+a2'. 

Which is smaller? Depends. We need to compare 4S0-3D+2a1+a2 (a sorted up) vs 4S0+3A-2d1-d2 (d sorted down).

So interleaving could matter! The question is: is the optimal always "group all M together and all P together" (M block then P block or P then M)? 

With the p+m ops, the S values form a path. The greedy "at each step pick min resulting S" is optimal. Let's think of it as: we have items +a_i and -b_j. Maintain a set. At each step, if there's a -b_j, S-b_j < S+a_i for all a_i (since b_j,a_i>0), so greedy picks the -b_j that minimizes S, i.e., the largest b_j (largest reduction). If no -b_j left, we must pick +a_i, and we want to minimize resulting S, so pick the smallest a_i.

Wait! If both types available, we always pick a -b (subtract) over +a (add), because S-b < S+a. Among subtracts, pick the largest b (gives smallest S). So: while there are M-ops left, do the largest remaining M-op. Then do P-ops in increasing order (smallest first to keep S small).

But wait, what if after some subtracts S becomes negative or very small, and a +a would make S less negative... no, we already showed M before P is optimal when one of each, and generally we should do M first.

But is "do largest M first, then smallest P first" globally optimal? Let's verify with the expression for "M block then P block, M in decreasing order, P in increasing order": we showed order within M doesn't matter for the "M then P" block cost (both subtractions appear with coefficient -2, so -2D regardless of order). Hmm earlier I got -2D. Let me recheck.

M block then P block. M = {d1,d2} in some order d_{(1)}, d_{(2)}. P = {a1,a2} in some order a_{(1)}, a_{(2)}.
S values after each op: 
1: S0 - d_{(1)}
2: S0 - d_{(1)} - d_{(2)}
3: S0 - D + a_{(1)}
4: S0 - D + a_{(1)} + a_{(2)} = S0 - D + A = Sf.

Sum = (S0-d_{(1)}) + (S0-D) + (S0-D+a_{(1)}) + (S0-D+A)
= 4S0 - d_{(1)} - D - D + a_{(1)} - D + A
= 4S0 + A - 3D + a_{(1)} - d_{(1)}.

Oh! I made an error. Let me redo carefully:
- Op1 cost: S0 - d_{(1)}
- Op2 cost: S0 - d_{(1)} - d_{(2)} = S0 - D
- Op3 cost: S0 - D + a_{(1)}
- Op4 cost: S0 - D + a_{(1)} + a_{(2)} = S0 - D + A

Sum = [S0-d_{(1)}] + [S0-D] + [S0-D+a_{(1)}] + [S0-D+A]
= 4S0 - d_{(1)} - D - D + a_{(1)} - D + A
= 4S0 + A - 3D + a_{(1)} - d_{(1)}.

To minimize: maximize d_{(1)} (do largest M first) and minimize a_{(1)} (do smallest P first). Good, that matches the greedy.

Now, could interleaving help? Consider we do P, M, P, M. 
S: S0, S0+a1, S0+a1-d1, S0+a1-d1+a2, S0+a1-d1+a2-d2.
Costs: (S0+a1)+(S0+a1-d1)+(S0+A-D+a2)+(S0+A-D). 
= 4S0 + 2a1 - d1 + A - D + a2 - D
= 4S0 + 2a1 + a2 - d1 - 2D + A.

Compare to M,P,M,P or M,M,P,P. M,M,P,P gave 4S0 + A - 3D + a1 - d1 (with a1 small, d1 large). 

Hmm, this is getting complex. Let me think of a cleaner approach.

This problem is known. Actually, the answer is: do all "-c" (M) operations in decreasing order of c, then all "+c" (P) operations in increasing order of c. But wait, I recall problems like this where the answer is that the optimal is a specific pattern. Let me reconsider.

Actually, I think the optimal strategy is: do all M-ops (1→0 flips) first, in decreasing order of c_i, then do all P-ops (0→1 flips), in increasing order of c_i. Let me verify this is indeed optimal by checking the "P then M" alternative and any interleaving.

General claim: It's optimal to do all M before all P. 

Proof sketch: Consider any optimal sequence. Take the first P-op (adding some a). Before it, only M-ops happened (else there's an earlier P). After this P-op, eventually we do all remaining ops. Consider swapping this P-op with all subsequent M-ops... this is like a bubble sort argument. Specifically, moving all P-ops to the end can only decrease (or maintain) the sum of S values, because each P-op increases S, and doing it later means it affects fewer future S values (smaller coefficient in the sum expression).

More precisely, the total cost can be written as: 
Total = (p+m)*S0 + sum over ops of (change to S) * (number of ops from this one to end).

For the k-th op in sequence, with change Δ_k ∈ {+c, -c}, the cost contribution beyond the S0 terms... actually let's express the sum of S after each op differently.

Let the sequence of changes be δ_1, δ_2, ..., δ_{p+m} where each δ is +a or -d. Then S_k = S0 + δ_1 + ... + δ_k for k≥1. 
Sum of S_k for k=1..p+m = (p+m)S0 + sum_{k=1}^{p+m} sum_{j=1}^{k} δ_j = (p+m)S0 + sum_{j=1}^{p+m} δ_j * (p+m - j + 1).

The term (p+m - j + 1) is the number of ops from position j to the end. So the last op has weight 1, the first has weight p+m.

We want to minimize sum δ_j * w_j where w_j = p+m-j+1 (decreasing weights from p+m to 1), subject to the multiset of δ values being fixed (p positive +a's and m negative -d's). Since all w_j > 0, to minimize we want the most negative δ (largest -d) to have the largest weight (earliest position), and the most positive δ (largest +a) to have the smallest weight (latest position). 

Wait: we have δ_j ∈ {+a_i, -d_j}. The negative values are -d (we want large magnitude negative to have large weight to minimize). The positive values are +a (we want large positive to have small weight). So:
- Among the -d's: assign largest d to earliest positions (largest weights). This means do largest M-ops first.
- Among the +a's: assign largest a to latest positions (smallest weights), equivalently smallest a to earliest among the P's. This means do smallest P-ops first (among the P block, which comes last).

But this assumes we interleave? No! The weights are fixed by position. We have m negative δ's and p positive δ's. We just need to assign which negative goes to which of the m earliest positions and which positive to which of the p latest positions. The optimal is:
- The m negative δ's occupy the first m positions; among them, the ones with larger magnitude (larger d) go to earlier positions (larger weights). So the sequence of M-ops is in decreasing d.
- The p positive δ's occupy the last p positions; among them, larger a's go to later positions (smaller weights), so earlier among P's are smaller a's. So P-ops are in increasing a.

This is the optimal! And it confirms: do all M first (in decreasing c), then all P (in increasing c). 

But wait, is it forced that the first m positions are all M and last p are all P? Could interleaving (some P early, some M late) be better?

If a P is at position j ≤ m (i.e., among the first m positions) and an M is at position j' > m, swapping them: P at j' and M at j. The weight difference: w_j - w_{j'} = (p+m-j+1) - (p+m-j'+1) = j' - j > 0. So M is at a higher-weight position in the original (w_j > w_{j'}). In the swap, P is at w_{j'} (lower) and M at w_j (higher). The change in total: original has P at w_j and M at w_{j'}; swap has M at w_j and P at w_{j'}. 
Change = [(-d)*w_j + (+a)*w_{j'}] - [(+a)*w_j + (-d)*w_{j'}]
= -d w_j + a w_{j'} - a w_j + d w_{j'}
= (a+d)(w_{j'} - w_j) = (a+d)(j - j') < 0.

So the swap (M early, P late) decreases the total cost. Hence any optimal solution has all M before all P. Combined with the within-block ordering, the optimal is:
1. Do M-ops in decreasing order of c.
2. Do P-ops in increasing order of c.

And the total cost is computed as the sum of S after each operation. Let m = |M|, p = |P|.

Let's compute the formula. Let M sorted decreasing: d_1 ≥ d_2 ≥ ... ≥ d_m. Let P sorted increasing: a_1 ≤ a_2 ≤ ... ≤ a_p.

S0 = initial sum = sum of c_i for A_i=1.
After k M-ops: S0 - (d_1+...+d_k), for k=1..m.
After all M then j P-ops: S0 - sum(M) + (a_1+...+a_j), for j=1..p.

Note sum(M) = S0 - Sf, where Sf = sum of c_i for B_i=1. Actually: S0 = sum_{A_i=1} c_i. sum(M) = sum_{A_i=1, B_i=0} c_i. sum(P) = sum_{A_i=0, B_i=1} c_i. Sf = S0 - sum(M) + sum(P). So S0 - sum(M) = Sf - sum(P). 

The S values we pay (m+p of them):
For k=1..m: S0 - partial_sum_M(k) = S0 - (d_1+...+d_k).
For j=1..p: Sf - sum(P) + (a_1+...+a_j) = S0 - sum(M) + partial_sum_P(j).

Total cost = sum_{k=1}^{m} [S0 - (d_1+...+d_k)] + sum_{j=1}^{p} [S0 - sum(M) + (a_1+...+a_j)]
= m*S0 - sum_{k=1}^{m} (d_1+...+d_k) + p*(S0 - sum(M)) + sum_{j=1}^{p} (a_1+...+a_j).

Let prefix sums: MD_k = d_1+...+d_k, MD_m = sum(M). PA_j = a_1+...+a_j, PA_p = sum(P).

= m*S0 - sum_{k=1}^m MD_k + p*(S0 - MD_m) + sum_{j=1}^p PA_j
= (m+p)*S0 - p*MD_m - sum_{k=1}^m MD_k + sum_{j=1}^p PA_j.

Note (m+p) = number of differing positions. Let's call it K.

We can also verify with sample 1: A=(0,1,1,1), B=(1,0,1,0). c=(4,6,2,9).
A_i=1: indices 2,3,4 → S0 = 6+2+9=17.
B_i=1: indices 1,3 → Sf = 4+2=6.
P (0→1): i=1, c=4. M (1→0): i=2 c=6, i=4 c=9. 
M sorted decreasing: 9, 6. MD: 9, 15. P sorted increasing: 4. PA: 4.
m=2, p=1, K=3.
Cost = 3*17 - 1*15 - (9+15) + 4 = 51 - 15 - 24 + 4 = 16. ✓

Sample 3: let's trust it. So the algorithm is:
1. Read N, arrays A, B, C.
2. Compute S0 = sum C[i] for A[i]=1.
3. Collect P = [C[i] for i where A[i]=0, B[i]=1], M = [C[i] for i where A[i]=1, B[i]=0].
4. Sort M descending, P ascending.
5. Compute total cost using the formula.

This is O(N log N). N up to 2e5, C up to 1e6, sums up to 2e11, fits in 64-bit (use Python int, fine).

Let's write the solution.