
## ideation
The operation selects 4 consecutive pieces (in sorted order). The two outer pieces are fixed, and the two inner pieces are reflected across the midpoint M of the outer pieces.  
Key observation: for any four points `a < b < c < d`, reflecting `b` and `c` across `(a+d)/2` yields new coordinates `b' = a + d - b` and `c' = a + d - c`.  
The sum `a + b' + c' + d = a + (a+d-b) + (a+d-c) + d = 3a + 3d - b - c`, which is **not** equal to the original sum `a+b+c+d`. So the sum is not obviously invariant.  
However, note that `b' + c' = (a+d-b) + (a+d-c) = 2(a+d) - (b+c)`. The sum of the four becomes `a + d + 2(a+d) - (b+c) = 3(a+d) - (b+c)`. The change is `2(a+d) - 2(b+c) = 2((a+d) - (b+c))`.  
Wait — we need to be careful. The problem says all pieces always remain distinct, so the configuration is valid. The goal is to minimize the total sum. This is not a trivial "sum is invariant" problem; we need a smarter insight.

Let’s think about what configurations are reachable. The operation on indices `i, i+1, i+2, i+3` replaces `x_{i+1}, x_{i+2}` with `x_i + x_{i+3} - x_{i+1}, x_i + x_{i+3} - x_{i+2}` (after re-sorting, the order may swap, but the pieces are distinguishable by their original labels? Actually, the operation references the pieces by their current order on the number line, not by original labels. So after reflection, the relative order of the two inner pieces swaps if `b' > c'`? Let's check: originally `a < b < c < d`. New values are `b' = a+d-b`, `c' = a+d-c`. Since `b < c`, we have `b' > c'`. So the new order is `a, c', b', d` (i.e., `a < a+d-c < a+d-b < d`). So the two inner pieces swap their order.

The sum changes by `2(d - c) + 2(b - a)`? Let's recompute: new sum minus old sum = `(a + (a+d-c) + (a+d-b) + d) - (a + b + c + d) = (3a + 3d - b - c) - (a + b + c + d) = 2a + 2d - 2b - 2c = 2(a - b) + 2(d - c) = -2(b-a) + 2(d-c)`. Since `b-a > 0` and `d-c > 0`, the sign depends on which is larger. So the sum can increase or decrease.

But the problem asks for the minimum possible sum after any number of operations. We need to find the reachable set of configurations and the minimal total sum.

Let’s search for patterns. With 4 points, we can apply the operation once. The sum becomes `3a+3d-b-c`. Can we apply it again? After the operation, the order is `a, c', b', d`. If we apply the operation again on the same 4 points, we reflect `c'` and `b'` across `(a+d)/2`, which restores them to `b` and `c` (order may swap back). So it's reversible.

What about larger N? The operation on a block of 4 only affects those 4 points. The rest remain unchanged. So the total sum is not invariant, but we can change the sum of the 4-point block.

Let’s denote the block as `a, b, c, d` (sorted). The operation replaces the block with `a, a+d-c, a+d-b, d`. The sum of the block becomes `S' = 2a + 2d + (a+d) - (b+c)`? Wait: `a + (a+d-c) + (a+d-b) + d = 3a + 3d - b - c`. The original sum is `a+b+c+d`. So the change is `2(a+d) - 2(b+c) = 2((a+d) - (b+c))`. Since `a < b < c < d`, we have `a+d` compared to `b+c`. It's possible that `a+d > b+c` or `a+d < b+c` or equal. The sum decreases if `a+d < b+c`, increases if `a+d > b+c`, unchanged if equal.

Thus, to minimize the total sum, we would like to apply the operation whenever `a+d < b+c` (making the inner pieces more "spread out" away from the midpoint? Actually reflecting across the midpoint pulls them toward the midpoint if they are on the same side? Let's see: if `b` and `c` are close to each other and near the midpoint, then `a+d` is larger? No, the condition for decrease is `a+d < b+c`. That means the outer two are relatively close compared to the inner two? Wait, `a` is smallest, `d` is largest. `a+d` is the sum of extremes. `b+c` is the sum of the middle two. Since `a < b < c < d`, typically `a+d` could be larger or smaller. For example, `a=1, b=2, c=10, d=11`: `a+d=12`, `b+c=12`, equal. If `a=1, b=5, c=6, d=10`: `a+d=11`, `b+c=11`, equal. If `a=1, b=2, c=3, d=100`: `a+d=101`, `b+c=5`, so `a+d > b+c`, sum increases. If `a=1, b=90, c=95, d=100`: `a+d=101`, `b+c=185`, so `a+d < b+c`, sum decreases.

So the operation reduces the sum when the inner two are far from the outer two (i.e., the middle is "heavy"). But after the operation, the new values are `a, a+d-c, a+d-b, d`. The new middle two are symmetric around `(a+d)/2`. Their sum is `2(a+d) - (b+c)`. So the new sum of the block is `a + d + 2(a+d) - (b+c) = 3(a+d) - (b+c)`. The new `a+d` is still the same, but the new `b'+c' = 2(a+d) - (b+c)`. If originally `b+c > a+d`, then `b'+c' < a+d`. After the operation, the new condition for the block: the new `a` and `d` are the same, the new `b'` and `c'` (in sorted order) are `a+d-c` and `a+d-b`. Since `b' + c' = 2(a+d) - (b+c)`, if originally `b+c > a+d`, then `b'+c' < a+d`. So after one operation, the inequality flips or becomes equal. Indeed, `b'+c' - (a+d) = (a+d) - (b+c)`. So the new deviation is the negative of the old deviation. Thus, if we apply the operation again, the sum will change by the opposite amount, returning to the original sum. So for a block of 4, the operation toggles the sum between two values: `S0 = a+b+c+d` and `S1 = 3(a+d) - (b+c)`. The minimum of the two is `min(S0, S1)`. But wait, is it possible to apply the operation to overlapping blocks to get a different configuration? Yes, because the operation affects the order of the pieces. After the operation on block `[i, i+3]`, the two middle pieces swap order. This could affect future operations on overlapping blocks.

This is reminiscent of the "folding" operation in problems about sorting or minimizing sum. It might be that the minimum sum is achieved when the sequence is "balanced" in some way, perhaps when the pieces are in arithmetic progression or something? But the sample 1: `1,5,7,10`. Initial sum = 23. After operation: `1,4,6,10`, sum = 21. Can we do better? If we apply the operation again: `1,4,6,10` -> `a=1, b=4, c=6, d=10`. `a+d=11`, `b+c=10`. `a+d > b+c`, so sum increases. So min is 21. The result is not symmetric: `1,4,6,10` is not an arithmetic progression. But note that `1+10 = 11`, `4+6=10`, so the outer sum is larger than the inner sum.

Sample 2: `0,1,6,10,14,16`. Sum = 47. Output: 41. Let's see if we can achieve 41. The operation on any 4 consecutive. Let's try to find a sequence of operations.

We need to think about the problem more abstractly. The operation is a reflection of the middle two across the midpoint of the outer two. This is equivalent to: given a sorted quadruple `(a,b,c,d)`, replace `(b,c)` with `(a+d-c, a+d-b)` (and then re-sort, which swaps their order). This is exactly the operation in the "folding" of a sequence to minimize the sum of absolute deviations or something. Actually, there is a known problem: "Minimum possible sum of coordinates after folding operations" or something similar. It might be related to the fact that the operation preserves the sum of the first and last, second and second last, etc.? Let's check invariants.

Consider the entire sequence. The operation on indices `i, i+1, i+2, i+3` (0-indexed) changes the sequence. Let's see if there is an invariant like the sum of elements at even positions minus odd positions, or something. Define `Y_k = X_{k+1} - X_k` (differences). The operation might have a nice effect on differences. For a quadruple `a,b,c,d`, the differences are `b-a, c-b, d-c`. After the operation, the new sequence is `a, a+d-c, a+d-b, d` (sorted). The new differences: `(a+d-c) - a = d-c`, `(a+d-b) - (a+d-c) = c-b`, `d - (a+d-b) = b-a`. So the multiset of differences is permuted! Specifically, the three differences are swapped: the leftmost becomes the rightmost, the rightmost becomes the leftmost, and the middle stays. Actually: old differences: `d1 = b-a`, `d2 = c-b`, `d3 = d-c`. New differences: `d1' = (a+d-c)-a = d-c = d3`, `d2' = (a+d-b) - (a+d-c) = c-b = d2`, `d3' = d - (a+d-b) = b-a = d1`. So the operation swaps the first and third differences of the block, while keeping the middle difference the same. This is a crucial observation!

Since the operation only affects the four pieces, and within them, the multiset of the three consecutive differences is invariant (just swapped). But note: the pieces outside the block have their differences to the block changed. For the left neighbor (if exists) of the block, the difference with the new leftmost piece of the block changes from `b - left` to `(a+d-c) - left`. For the right neighbor, the difference with the new rightmost piece changes from `right - d` to `right - (a+d-b)`. So the operation swaps the two end-differences of the block, and also changes the differences connecting the block to its neighbors.

Wait, the differences between pieces are not fully invariant because the block's boundaries change the differences with neighbors. However, if we consider the whole sequence as a set of points, the operation is a specific transformation. But the difference observation is powerful: the operation on a block of 4 swaps the two outer gaps within the block, while preserving the middle gap. The inner gaps (between the two middle pieces) remains the same! Actually, `c-b` is preserved. So the distance between the two middle pieces is invariant under this operation. And the two outer gaps (between outer and inner) are swapped.

Now, think about the whole sequence of N pieces. The gaps are `g_1, g_2, ..., g_{N-1}`. The operation on `i, i+1, i+2, i+3` (1-indexed) corresponds to swapping `g_i` and `g_{i+2}` (the gaps adjacent to the two outer pieces of the block), and leaving `g_{i+1}` unchanged. But also, the positions of the pieces change, so the gaps to the left and right of the block (i.e., `g_{i-1}` and `g_{i+3}`) are affected because the boundaries move. Specifically, the leftmost piece `X_i` stays fixed, so the left gap `g_{i-1}` (if i>1) is unchanged. The rightmost piece `X_{i+3}` stays fixed, so the right gap `g_{i+3}` (if i+3<N) is unchanged. Wait, the operation says: choose i (1-indexed) such that 1 <= i <= N-3. So the block is pieces i, i+1, i+2, i+3. The outer pieces are i and i+3. They do not move. The inner pieces i+1 and i+2 move to symmetric positions around the midpoint of i and i+3. So indeed, the outer pieces are fixed. Therefore, the gaps to the left of the block (between i-1 and i) and to the right of the block (between i+3 and i+4) are unchanged because the positions of the boundary pieces i and i+3 don't change. The gaps inside the block: originally `g_i` (between i and i+1), `g_{i+1}` (between i+1 and i+2), `g_{i+2}` (between i+2 and i+3). After the operation, the new positions of i+1 and i+2 are `M - (X_{i+1} - M) = 2M - X_{i+1}` and `2M - X_{i+2}`. Since `M = (X_i + X_{i+3})/2`, the new positions are `X_i + X_{i+3} - X_{i+1}` and `X_i + X_{i+3} - X_{i+2}`. The new gaps: between i and new i+1: `(X_i + X_{i+3} - X_{i+1}) - X_i = X_{i+3} - X_{i+1}`. Originally, the distance between i+1 and i+3 was `X_{i+3} - X_{i+1} = g_i + g_{i+1} + g_{i+2}`. That doesn't seem right. Let's compute carefully.

Let the positions be `a, b, c, d` for pieces i, i+1, i+2, i+3. The gaps are `b-a`, `c-b`, `d-c`. After operation, positions are `a, a+d-c, a+d-b, d`. The new gaps: 
- between a and new b: `(a+d-c) - a = d-c`. This is the old gap `g_{i+2}`.
- between new b and new c: `(a+d-b) - (a+d-c) = c-b`. This is the old gap `g_{i+1}`.
- between new c and d: `d - (a+d-b) = b-a`. This is the old gap `g_i`.

So indeed, the three internal gaps are permuted: `g_i` (old) goes to the right, `g_{i+1}` stays in the middle, `g_{i+2}` goes to the left. The outer gaps (if any) remain unchanged because the boundary pieces don't move. So the operation is exactly: swap `g_i` and `g_{i+2}`. It does not change any other gaps! This is a massive simplification.

Thus, the state of the system is fully described by the sequence of gaps `g_1, ..., g_{N-1}`. The operation on index `i` (1 <= i <= N-3) swaps `g_i` and `g_{i+2}`. The positions of the pieces can be reconstructed by prefix sums: `X_1 = 0` (or some reference, but sum depends on reference? Actually, the sum of coordinates depends on the absolute positions. The gaps determine relative positions, but the absolute positions are determined by fixing the first piece or the whole sum. Let's see: the sum of all pieces is `X_1 + (X_1+g_1) + (X_1+g_1+g_2) + ... = N*X_1 + (N-1)g_1 + (N-2)g_2 + ... + 1*g_{N-1}`. But `X_1` itself is not fixed; the pieces can move? Wait, the operation does not move the outer pieces of the block, but if we apply operations to different blocks, the pieces can move overall. However, the first piece `X_1` never moves? Let's check: the first piece can only be moved if it is inside a block. But the block is defined on consecutive pieces in ascending order. The first piece is piece 1. It can be the leftmost piece of a block if we choose i=1. In that case, piece 1 is the left outer piece and does not move. If we choose i=0? No, i starts at 1. So piece 1 can never be an inner piece of a block. It can only be the leftmost piece of a block (i=1) or not involved. In either case, it never moves. Similarly, piece N never moves. So `X_1` and `X_N` are fixed! The operation only moves pieces that are not at the ends of the entire sequence? Actually, any piece except the very first and very last can move. But piece 1 is always the leftmost, and it is never moved because it is always the leftmost of any block it's in (since blocks are contiguous from the leftmost). Wait, could piece 1 become not the leftmost? The pieces are always sorted by coordinate. Piece 1 is the smallest coordinate initially. Could it become larger than another piece? The operation moves pieces i+1 and i+2 to positions symmetric to the midpoint. Since the new positions are within the interval [X_i, X_{i+3}], and piece i is the smallest in that block, piece i remains the smallest among the four. So piece 1, being the overall minimum, can never be overtaken because it is always the leftmost of any block it belongs to, and it doesn't move. So indeed, `X_1` is invariant. Similarly, `X_N` is invariant. Therefore, the gaps sequence is not completely free: the first piece is anchored.

But the operation on the gaps: swapping `g_i` and `g_{i+2}` for any `i` from 1 to N-3. This is exactly the operation of swapping adjacent elements with a gap of one? Actually, it swaps the i-th and (i+2)-th gaps. This is a restricted set of permutations. What permutations of the gaps can we achieve? We can swap any two gaps that are separated by exactly one other gap. By composing such swaps, can we achieve any permutation? This is like a sorting network. For example, to swap `g_1` and `g_3`, we can directly swap them with i=1. To swap `g_1` and `g_4`, we can swap `g_1` and `g_3`, then `g_2` and `g_4`, then `g_1` and `g_3` again? Let's see. We want to permute the gaps. The allowed operation is: pick i, swap g_i and g_{i+2}. This is equivalent to a 3-cycle? Actually, swapping two non-adjacent elements is possible. This operation is known to generate the symmetric group for N-1 >= 4? Let's check: the allowed transpositions are between i and i+2. These generate the alternating group? Actually, the set of transpositions (i, i+2) for i=1..N-3. For N-1=4, we have gaps g1,g2,g3,g4. Allowed swaps: (1,3) and (2,4). These generate the Klein four-group? They can swap 1 and 3, and 2 and 4 independently. The full symmetric group is not generated; only even permutations? Actually, swapping 1 and 3 is an odd permutation on 4 elements. Wait, a single swap is odd. But we can only do swaps of pairs at distance 2. For 4 gaps, the allowed swaps are (1,3) and (2,4). These are two disjoint transpositions. They generate a group of order 4. The total permutations reachable are the identity, (1,3), (2,4), and (1,3)(2,4). We cannot swap 1 and 2, for example. So the reachable permutations are restricted.

For N-1 gaps, the allowed swaps are between positions i and i+2. This is exactly the operation of a "bubble sort" but only swapping elements at distance 2. This is equivalent to: we can reorder the gaps as long as the permutation is even? Or maybe we can achieve any permutation? Let's think: The set of allowed swaps generates the alternating group? Actually, the transpositions (1,2), (2,3), ... generate the full symmetric group. Here we have (1,3), (2,4), (3,5), ... So we don't have adjacent swaps. Can we simulate an adjacent swap? To swap g1 and g2, we would need to bring one of them to position 3, swap, then back. For example, to swap g1 and g2: swap g1 and g3 (now order: g3, g2, g1, g4,...), then swap g2 and g4? That doesn't swap 1 and 2. Let's try to swap g1 and g2. Current: g1, g2, g3, g4. We want g2, g1, g3, g4. Can we? Allowed: swap 1 and 3 -> g3, g2, g1, g4. Then swap 2 and 4 -> g3, g4, g1, g2. Then swap 1 and 3 -> g1, g4, g3, g2. Then swap 2 and 4 -> g1, g2, g3, g4. We got back. So maybe we cannot swap adjacent gaps. The reachable permutations are those that preserve the parity of the permutation of the gaps? Actually, each allowed swap is a transposition of two elements, which changes the parity. But maybe there is an invariant modulo 2? Let's check the sum of the indices weighted by the values? Or consider the parity of the permutation of the gaps. Since we only have transpositions of elements at odd distance? i and i+2 have the same parity. So swapping two elements of the same parity might preserve the parity of the number of inversions between even and odd positions? There is a known result: the group generated by transpositions (i, i+2) is the alternating group if N-1 >= 5? Actually, it's the group of permutations that preserve the parity of the sum of positions? Not sure.

But we don't need the full group; we want to minimize the sum of coordinates. The sum is a linear function of the gaps. Since we can permute the gaps in a restricted way, we want to arrange the gaps to minimize the sum. The sum of coordinates is `S = sum_{j=1}^N X_j`. As derived: `S = N*X_1 + sum_{k=1}^{N-1} (N - k) g_k`. Wait, check: `X_1` is fixed. `X_2 = X_1 + g_1`, so contributes `N-1` times g_1. `X_3 = X_1 + g_1 + g_2`, contributes `N-2` times g_2, etc. `X_N = X_1 + sum g_k`, contributes `1` times g_{N-1}. So the coefficient of `g_k` is `N - k`. So to minimize the sum, we want to assign the largest gaps to the smallest coefficients (i.e., largest k), and the smallest gaps to the largest coefficients (smallest k). That is, we want the gaps to be sorted in non-decreasing order? Actually, since coefficients decrease with k, we want the gaps to be sorted in non-increasing order to minimize the sum: largest gaps at the end (small coefficients), smallest gaps at the beginning (large coefficients). Wait: coefficient for g_1 is N-1, for g_{N-1} is 1. So we want g_1 to be as small as possible, and g_{N-1} as large as possible. So the optimal arrangement is `g_1 <= g_2 <= ... <= g_{N-1}` (sorted ascending). But can we achieve that arrangement via the allowed swaps? The allowed swaps are only swapping g_i and g_{i+2}. This is a very restricted set. We cannot arbitrarily sort the gaps. So the problem reduces to: given the initial multiset of gaps, and allowed swaps of elements at distance 2, what is the minimum possible value of `sum_{k=1}^{N-1} c_k g_{\pi(k)}` where `c_k = N-k` are decreasing, and the permutation `\pi` is reachable by the allowed swaps? And we need to find the minimum over all reachable permutations.

This is a combinatorial optimization on a restricted permutation group. The allowed swaps are transpositions of elements separated by one position. This is exactly the operation of "bubble sort" but only on even-odd positions? Actually, the indices of gaps: we can swap g_i and g_{i+2}. This means we can only swap elements that are in the same parity class (both odd or both even). So the permutation must map odd indices to odd indices, and even indices to even indices. Is that the only restriction? Let's verify: if we only swap elements of the same parity, then the parity of the index of each gap is invariant. Because a swap between i and i+2 preserves the parity of the positions of all elements? Actually, swapping two elements of the same parity: the set of elements at odd positions remains exactly the same, just permuted among themselves. Similarly for even positions. So any reachable permutation must preserve the set of gaps at odd indices and the set at even indices separately. In other words, we can only permute the odd-indexed gaps among themselves, and the even-indexed gaps among themselves. Is that true? Let's check: can an odd-indexed gap move to an even index? Suppose we have gaps at positions 1,2,3,4,5. Allowed swaps: (1,3), (2,4), (3,5), etc. If we swap 1 and 3, both odd, the gap originally at 1 goes to 3, and 3 goes to 1. The set of odd positions still contains the same two gaps, just swapped. So indeed, the set of gaps that occupy odd positions is invariant. Similarly for even positions. Therefore, the reachable configurations are exactly those where the odd-indexed gaps are a permutation of the original odd-indexed gaps, and the even-indexed gaps are a permutation of the original even-indexed gaps. Is that all? We also need to check if any permutation within the odd positions is reachable. The allowed swaps within odd positions are between odd i and i+2. For odd positions, the indices are 1,3,5,... So the allowed swaps are (1,3), (3,5), (5,7), etc. These are adjacent swaps in the subsequence of odd-indexed gaps. Since adjacent swaps generate the full symmetric group on the odd positions, we can achieve any permutation of the odd-indexed gaps among themselves. Similarly, for even positions: 2,4,6,... allowed swaps (2,4), (4,6), etc., which generate the full symmetric group on even positions. So the reachable permutations are exactly those that independently permute the odd-indexed gaps and the even-indexed gaps. That is, the set of odd positions and even positions are each fully sortable.

Wait, is there any additional restriction? The swaps are performed sequentially, but since the gaps are just numbers, and we can do any sequence of swaps, as long as we can generate the symmetric group on each parity class, we can achieve any permutation within each class. So the reachable states are characterized by: the odd-indexed gaps can be in any order, and the even-indexed gaps can be in any order, independently. There is no cross-parity mixing.

Let's double-check with a small example. N=4, so 3 gaps: g1, g2, g3. Allowed swaps: i=1 only (since N-3=1). So we can swap g1 and g3. Odd positions: 1 and 3. Even: 2. We can swap g1 and g3 arbitrarily, but g2 stays. That matches: odd positions can be permuted (only two elements), even position has one element. So reachable permutations: (g1,g2,g3) -> (g3,g2,g1). Sum = (N-1)g1 + (N-2)g2 + (N-3)g3 = 3g1+2g2+1g3. With swap: 3g3+2g2+1g1. The difference is 2(g1-g3). So if g1 > g3, swapping reduces sum. So we should put the larger of g1 and g3 at position 3 to minimize. So the minimum is achieved by sorting the odd positions in ascending order? Wait: coefficient for g1 is 3, for g3 is 1. So we want the smallest gap at position 1, largest at position 3. So among odd positions, we want them sorted ascending (small to large as index increases). For even positions, we want the smallest gap at the smallest even index? Actually, coefficient decreases with index, so we want the gaps to be sorted in non-decreasing order overall. But since we can only permute within parity, the optimal strategy is: sort the odd-indexed gaps in non-decreasing order, and sort the even-indexed gaps in non-decreasing order, and then place them back. But wait, is that always optimal? Because the coefficients are decreasing with index, to minimize the sum, we want the sequence of gaps to be as "small-to-large" as possible. But we have two independent sequences. The coefficients for odd positions: for position 1 (odd), coefficient is N-1; position 3: N-3; position 5: N-5; etc. So the odd positions have coefficients that are strictly decreasing. Similarly for even positions: position 2: N-2; position 4: N-4; etc. So for each parity class, the coefficients are decreasing with the position index. Therefore, within each parity class, we should sort the gaps in non-decreasing order (i.e., assign the smallest gap to the largest coefficient, which is the smallest index in that class). But note: the smallest index in the odd class is 1, then 3, then 5. The largest coefficient is for index 1. So we want the smallest odd gap to go to index 1, the next smallest to index 3, etc. Similarly for even: smallest even gap to index 2, next to index 4, etc. So the optimal configuration is: the gaps are sorted in non-decreasing order when restricted to odd indices, and similarly for even indices. But is that independent? Yes, because we can permute them independently. So the minimal sum is obtained by: take the original odd-indexed gaps, sort them ascending, and place them back in odd positions in order. Take the original even-indexed gaps, sort them ascending, and place them back in even positions in order. Then compute the sum.

But wait: is it always possible to achieve this configuration? Since the odd positions can be fully permuted among themselves, we can indeed sort them. However, we must ensure that the operation of swapping g_i and g_{i+2} can achieve any permutation of the odd positions. The allowed swaps within odd positions are between 1 and 3, 3 and 5, etc. These are adjacent transpositions in the sequence of odd positions. By composing them, we can generate any permutation of the odd positions (bubble sort). So yes, we can sort them arbitrarily. Similarly for even.

But there is a catch: the positions of the pieces must remain distinct. The problem states that under the constraints, all pieces always occupy distinct coordinates, no matter how one repeatedly performs the operation. So we don't need to worry about distinctness; it's guaranteed.

Thus, the problem reduces to: 
1. Compute the gaps `g_i = X_{i+1} - X_i` for i=1..N-1.
2. Separate into odd-indexed gaps (i=1,3,5,...) and even-indexed gaps (i=2,4,6,...).
3. Sort each list in non-decreasing order.
4. Reconstruct the new gaps: for i odd, take the i-th smallest from the odd list; for i even, take the i-th smallest from the even list.
5. Compute the new sum of coordinates.

But wait: the sum of coordinates depends on `X_1` and the gaps. However, the first piece `X_1` is fixed. The last piece `X_N` is also fixed. The sum of all pieces is `N*X_1 + sum_{k=1}^{N-1} (N-k) g_k`. Since `X_1` is constant, we just need to minimize the weighted sum of the gaps. So we can compute the minimal weighted sum by assigning the sorted gaps to the positions with appropriate weights.

Let's test this on Sample 1: N=4, X = [1,5,7,10]. Gaps: g1=4, g2=2, g3=3. Odd positions: 1,3 -> gaps [4,3]. Sorted odd: [3,4]. Even: position 2 -> gap [2]. New gaps: g1=3, g2=2, g3=4. New positions: X1=1, X2=1+3=4, X3=4+2=6, X4=6+4=10. Sum = 1+4+6+10=21. Matches.

Sample 2: N=6, X = [0,1,6,10,14,16]. Gaps: g1=1, g2=5, g3=4, g4=4, g5=2. Odd positions: 1,3,5 -> gaps [1,4,2]. Sorted odd: [1,2,4]. Even: 2,4 -> gaps [5,4]. Sorted even: [4,5]. New gaps: g1=1, g2=4, g3=2, g4=5, g5=4. New positions: X1=0, X2=1, X3=1+4=5, X4=5+2=7, X5=7+5=12, X6=12+4=16. Sum = 0+1+5+7+12+16 = 41. Matches.

So the algorithm is correct.

Now, we need to implement this efficiently for N up to 2e5. We can just collect the odd and even gaps, sort them, then iterate to compute the new sum.

Let's formalize:
- Read N and array X.
- Compute gaps: for i in 0..N-2: g[i] = X[i+1] - X[i].
- Separate: odd_gaps = [g[i] for i in range(0, N-1, 2)]; even_gaps = [g[i] for i in range(1, N-1, 2)].
- Sort odd_gaps ascending; sort even_gaps ascending.
- Reconstruct new gaps:
  - Initialize pointer o=0, e=0.
  - For k from 1 to N-1 (1-indexed):
    - if k is odd: new_g = odd_gaps[o]; o++
    - else: new_g = even_gaps[e]; e++
- Compute new sum: 
  - Let S = X[0] (since X_1 is fixed).
  - current = X[0]
  - For i from 0 to N-2:
    - current += new_gaps[i]
    - S += current
- Alternatively, compute weighted sum directly: S = N*X[0] + sum_{i=0}^{N-2} (N-1 - i) * new_gaps[i]. But careful: coefficients are N-1, N-2, ..., 1. For 0-indexed gaps g[0]..g[N-2], the coefficient for g[k] is N-1-k. So we can compute S = N*X[0] + sum_{k=0}^{N-2} (N-1-k) * new_gap[k]. This is O(N). We must use 64-bit integers (X up to 1e12, N up to 2e5, sum up to 2e5*1e12 = 2e17, fits in 64-bit signed).

Let's verify with a small case where N=4, X=[1,5,7,10]. N=4, X0=1. Gaps: [4,2,3]. Odd: indices 0,2 -> [4,3] -> sorted [3,4]. Even: index 1 -> [2] -> sorted [2]. New gaps: [3,2,4]. Weighted sum: N*X0 = 4*1=4. Coefficients: for g0: 3, g1: 2, g2: 1. Sum = 3*3 + 2*2 + 1*4 = 9+4+4=17. Total S = 4+17=21. Correct.

Sample 2: N=6, X0=0. Gaps: [1,5,4,4,2]. Odd: [1,4,2] -> sorted [1,2,4]. Even: [5,4] -> sorted [4,5]. New gaps: [1,4,2,5,4]. Coefficients: 5,4,3,2,1. Weighted sum = 5*1 + 4*4 + 3*2 + 2*5 + 1*4 = 5+16+6+10+4=41. Total S = 6*0 + 41 = 41. Correct.

So the solution is straightforward.

But wait: is it always true that the odd and even gaps can be sorted independently? We argued that the allowed swaps are only between i and i+2, which means we can only swap gaps of the same parity. And since the allowed swaps within each parity are adjacent in that subsequence, we can generate any permutation. However, is there any interaction between the odd and even gaps through the fact that the operation on a block of 4 pieces swaps g_i and g_{i+2} (which are both odd or both even depending on i). For i=1 (odd), we swap g1 and g3 (both odd). For i=2 (even), we swap g2 and g4 (both even). So indeed, no cross-parity swapping. So the reachable set of gap sequences is exactly the product of the symmetric groups on the odd and even positions. Therefore, the minimum is achieved by sorting each list independently.

Thus, the algorithm is:
1. Read N and list X.
2. Compute gaps: g[i] = X[i+1] - X[i] for i in 0..N-2.
3. Extract odd_gaps = g[0::2] and even_gaps = g[1::2].
4. Sort odd_gaps and even_gaps.
5. Reconstruct new_gaps by merging: for i in 0..N-2: if i%2==0: new_gaps[i] = odd_gaps[i//2]; else: new_gaps[i] = even_gaps[i//2].
6. Compute answer = N * X[0] + sum_{i=0}^{N-2} (N-1-i) * new_gaps[i].
7. Print answer.

Complexity: O(N log N) for sorting, O(N) for the rest. N up to 2e5, so it's fine.

Let's consider if there is any edge case: N=4, works. N=5: gaps g0..g3. Odd: g0,g2; even: g1,g3. Allowed swaps: i=1 (swap g1,g3) and i=2 (swap g0,g2). So we can swap g0 and g2, and g1 and g3. So indeed independent. The reasoning holds.

Thus, the solution is correct.

We should write the Python code accordingly.

One more check: the problem says "all pieces always occupy distinct coordinates, no matter how one repeatedly performs the operation." So we don't need to check for distinctness.

Also, the operation definition: "move each of the (i+1)-th and (i+2)-th pieces in ascending order of coordinate to positions symmetric to M." This is exactly the reflection we used.

So the code is simple.

Let's write it.

```python
import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = [int(next(it)) for _ in range(N)]
    if N == 1:
        print(X[0])
        return
    # Compute gaps
    gaps = [X[i+1] - X[i] for i in range(N-1)]
    odd_gaps = []
    even_gaps = []
    for i, g in enumerate(gaps):
        if i % 2 == 0:
            odd_gaps.append(g)
        else:
            even_gaps.append(g)
    odd_gaps.sort()
    even_gaps.sort()
    # Reconstruct new gaps
    new_gaps = [0] * (N-1)
    oi = 0
    ei = 0
    for i in range(N-1):
        if i % 2 == 0:
            new_gaps[i] = odd_gaps[oi]
            oi += 1
        else:
            new_gaps[i] = even_gaps[ei]
            ei += 1
    # Compute sum
    # S = N * X[0] + sum_{k=0}^{N-2} (N-1-k) * new_gaps[k]
    total = N * X[0]
    for k, g in enumerate(new_gaps):
        total += (N - 1 - k) * g
    print(total)

if __name__ == "__main__":
    solve()
```

This should work.

Let's double-check with a random small N by brute force to be absolutely sure. But since we can't run code here, we trust the reasoning. The problem is known; it's from AtCoder ABC 311 F? Actually, it might be from a recent contest. The insight about gaps is standard for such "folding" operations.

Wait, is there any possibility that the operation can be applied to indices that are not just the gaps? The operation is defined on the pieces in ascending order. The pieces are always sorted because the operation preserves order within the block (the new positions are within the interval, and the two inner pieces swap order, but the whole sequence remains sorted). So the indices always refer to the sorted order. Our gap analysis used the sorted order and the fact that the outer pieces don't move. This is correct.

One more subtle point: the operation says "choose an integer i such that 1 <= i <= N-3, and let M be the midpoint between the positions of the i-th and (i+3)-rd pieces in ascending order of coordinate." So the pieces are always taken in sorted order. Our analysis assumed that the pieces are indexed by their current sorted order. This is correct.

Thus, the solution is solid.

## worker: omitted
The operation reflects the two middle pieces across the midpoint of the outer pieces. In terms of the gaps \(g_i = X_{i+1} - X_i\) between consecutive pieces, this operation simply swaps \(g_i\) and \(g_{i+2}\) for some \(i\), leaving all other gaps unchanged. Thus, only gaps of the same parity (both odd-indexed or both even-indexed) can ever be swapped. Within each parity class, the allowed swaps are adjacent in the subsequence, so any permutation of the odd-indexed gaps among themselves and any permutation of the even-indexed gaps among themselves is reachable.

The total sum of coordinates is \(N \cdot X_1 + \sum_{k=1}^{N-1} (N-k) g_k\). Since the coefficients \((N-k)\) are strictly decreasing, the sum is minimized by assigning the smallest gaps to the largest coefficients, i.e., sorting the odd-indexed gaps in non-decreasing order and placing them back in odd positions, and doing the same for the even-indexed gaps. The first piece \(X_1\) is invariant and never moves.

The algorithm: compute gaps, split into odd/even lists, sort each, reconstruct the new gap sequence, and compute the weighted sum.
