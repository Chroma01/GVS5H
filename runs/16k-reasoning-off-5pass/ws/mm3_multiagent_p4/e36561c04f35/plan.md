We can always make the sequence empty by deleting a single element at a time (using operation 2 with i=1) — that costs N operations. Swaps can reduce deletions by allowing longer blocks of equal elements at the front, enabling multi-element deletions. A swap only matters if it brings two equal elements together, effectively “undoing” a previous unnecessary split. The key insight: think of the array as a string and consider each pair of consecutive equal elements as a “free bond” that a swap can break/repair. The optimal strategy is: for every position i, we can pay 1 swap to change whether the pair (i,i+1) is equal, and then we can delete everything in big chunks from the front. The minimal number of operations equals the number of indices i (1 ≤ i < N) where A[i] ≠ A[i+1] **and** the cost of swapping them exceeds the benefit. A greedy DP from left to right: maintain state = current front element value. At each step, either delete the front (cost 1 if we delete one by one, or 0 if we can delete a whole equal block), or do a swap to fix the next element. The answer is exactly the number of “transitions” between different values that we cannot avoid.

Actually, a simpler characterization: sort the array conceptually by grouping equal elements. The minimal cost equals the number of indices i where A[i] > A[i+1] (a "descent") plus 1, capped at N. But we need to verify with the known AtCoder problem “Make Empty Sequence” (ABC300 F-like). The standard solution: answer = max(number of equal adjacent pairs, N - number_of_different_adjacent_pairs) — no, the known answer is simply the number of indices i (1 ≤ i ≤ N-1) such that A[i] ≠ A[i+1], plus 1, because each such boundary forces at least one extra operation (either a swap or a single-element delete).

Re-derive cleanly: deleting a prefix of length L where all elements are equal costs 1 operation. If adjacent elements differ, we must either swap them (cost 1) so they become equal and can be deleted together, or delete them separately (cost 2). The total cost over the array is: number of distinct adjacent "blocks" + (number of boundaries where we choose to swap instead of separate-delete). We want to minimize total cost. For each boundary between different values, swapping saves 0 or 1 operation. The optimal is: answer = (number of boundaries) + 1, but each swap costs 1 too. Actually the known result for this problem (AtCoder ABC335 F? no, it's ABC300 F or similar) is: **answer = number of indices i where A[i] ≠ A[i+1], plus 1**? Let me check with samples:
- Sample 1: 1 1 2 1 2. Adjacent differ at positions 2 (1≠2), 3 (2≠1), 4 (1≠2) → 3 boundaries. 3+? = 3 → so answer = 3. Yes, answer = number of adjacent-unequal + something. Here 3 boundaries → answer 3. So answer = number of unequal adjacent pairs? 3 unequal pairs, answer 3. But answer must be at least ceil(N/ something). 
- Sample 2: 4 2 1 3. Adjacent differ: 4≠2, 2≠1, 1≠3 → 3 unequal pairs. Answer = 4 = N. So answer = max(number of unequal adjacents, 1) + ... Hmm, 3 unequal but answer 4.
- Sample 3: 1 2 1 2 1 2 1 2 1 2 1. Adjacent all differ (10 boundaries). Answer = 8. So it's not simply the count.

Let me reconsider. The correct approach (known solution): we want to minimize (number of delete operations) + (number of swap operations). Delete operations: we can delete a prefix [1..i] if all equal. The best is to delete as many as possible at once. So we should group equal elements at the front via swaps. The total work = (number of swaps to group) + (number of groups deleted). 

For the full array, the minimum operations = (number of indices i where A[i] = A[i+1])? No.

Let me think of the known solution: This is AtCoder ABC335 F? Actually it's "Make Empty Sequence" — I recall the answer is: count = 0, iterate, for each i from 2 to N: if A[i] == A[i-1], then we can do something, answer = (number of distinct adjacent-equal pairs). Hmm.

I'll re-derive with DP. State: position i (0-indexed, considering first i elements processed), and value of the current front element v. Transitions: either we already have the front element equal to A[i] and we extend the equal block, or we swap A[i] with A[i-1] (cost 1) then delete the block. This is too vague.

Let me just recall: the answer is **the number of indices i (1 ≤ i ≤ N-1) such that A[i] ≠ A[i+1], plus 1, but also we can do swaps to fix mismatches**. Actually, let's think of it as: the minimum number of operations = number of "descents" where we cannot save. 

I'll use the known result: **Answer = max over all v of (number of occurrences of v) + (N - 2*occurrences_of_v) for v that appears?** No.

Let me just code the known greedy: We process from left to right. Maintain a multiset (or just a counter) of elements that are "candidates" — elements that have appeared and could be brought to the front. The answer is N minus the maximum number of swaps we can save... 

Actually, I'll just look up the logic: The answer equals the number of indices i (1 ≤ i ≤ N) such that A[i] is a "local extremum" in some sense. Let me think differently.

**Clean derivation:**
We need to delete the whole array. We can delete a prefix [1..i] for free (1 op) if all those elements are equal. To make a prefix equal, we can swap. The total cost = (# swaps) + (# delete operations).

Observe: each element except possibly the last in its "delete-batch" requires being merged. A delete-batch of size k costs 1 delete op and needs (k-1) merges? No, it needs 0 swaps if already a contiguous equal block, but to create a contiguous equal block from scattered equal elements, we need swaps.

The array has some sequence of values. We partition it into contiguous groups of equal values. Let the group sizes be g_1, g_2, ..., g_m (m = number of groups, which equals 1 + number of indices i with A[i]≠A[i+1]). To delete the whole array, we can delete each group separately (cost m). Or we can swap to merge groups of the same value, reducing m. Each swap of adjacent elements that merges two groups of the same value reduces m by 1 and costs 1. So min cost = m - (max number of group merges we can do). Max merges = total number of "extra" occurrences of each value beyond the first group of that value. If value v appears in groups with sizes g^{(v)}_1, g^{(v)}_2, ..., g^{(v)}_{k_v}, then we can merge (k_v - 1) pairs, saving (k_v - 1) operations. So total merges possible = sum over v of (k_v - 1) = total number of groups - (number of distinct values). Wait, sum of k_v = m, and number of distinct values = d, so total merges = m - d. Therefore min cost = m - (m - d) = d. 

But sample 1: values are {1,2}, d=2. m=4 (groups: 1,1 | 2 | 1 | 2). Answer predicted = 2, but actual = 3. So this is wrong because we can't always merge groups freely — merging might require intermediate swaps that conflict.

Indeed, to merge two non-adjacent groups of value 1, we might need to swap other elements in between, which could cost extra. The constraint is that we must delete the prefix, so we process left to right. 

**Left-to-right DP:**
At each step, we have a "front element" currently equal to some value v. We can:
- Delete the front block (1 op) and move on, or
- Swap to change the front value.

But actually, a better view: we're building the prefix to be all equal to some value, then delete. Repeat.

Let me think of it as: we choose a sequence of values v_1, v_2, ..., v_t such that deleting block of v_1, then v_2, etc., empties the array. To delete a block of v_j, we need all remaining elements to eventually be brought (via swaps) to the front and made equal. The swaps only swap adjacent elements, and each swap costs 1. This is equivalent to: given the array, we want to partition it into contiguous segments, each to be made into a single value via adjacent swaps, then deleted. The cost of making a segment with values [a_1,...,a_k] into all-equal value x is: we need all elements to become x, which requires |{i: a_i ≠ x}| swaps? Not exactly, because swaps are adjacent.

This is equivalent to the problem of sorting each segment to all-equal. The minimum adjacent swaps to make an array all equal to x is: sum over all positions of |original_pos - target_pos| for elements being x, minus... it's complicated.

Hmm, but actually, for a segment, making it all equal to the most frequent value is optimal. Cost = length - (max frequency). So total cost = sum over segments of (length of segment - max_freq_in_segment) + (number of segments) = sum of lengths - sum of max_freq + number_of_segments = N - sum of max_freq + number_of_segments.

We want to minimize N - sum_max_freq + num_segments, i.e., maximize (sum_max_freq - num_segments).

Now, the segments must be a partition of the array into contiguous parts, and each part is made all-equal. The value chosen for each part can be anything. This is a DP: dp[i] = min cost for first i elements, dp[0]=0. dp[i] = min over j<i of dp[j] + (i-j) - max_freq(j+1..i, x) + 1 for best x. This is O(N^2) per test case, too slow.

**Key insight (known solution):** The answer is simply: for each value v, compute the number of indices i where A[i] ≠ A[i+1] and... hmm.

Let me look at this from the answer's perspective. Let f = number of indices i (1 ≤ i < N) with A[i] = A[i+1]. The answer for the samples:
- Sample 1: 1 1 2 1 2. Equal adjacents: (1,1) at i=1. So f=1. N=5. Answer=3. 
- Sample 2: 4 2 1 3. f=0. Answer=4=N.
- Sample 3: 1 2 1 2 1 2 1 2 1 2 1. f=0. Answer=8.

Hmm. f=0 but answers differ. 

Let me think about sample 3 more: 1 2 1 2 1 2 1 2 1 2 1. We can swap to make it (1 1 2 2 1 ...)? With swaps, we can pair up 1's and 2's. Actually optimal: delete the 1 at position 1 (1 op). Now array is 2 1 2 1 2 1 2 1 2 1. Delete the 2 (1 op). Now 1 2 1 2 1 2 1 2 1. Continue alternating. That's 11 ops. But answer is 8, so better exists. Strategy: swap positions 2,3 → 1 1 2 2 1 2 1 2 1 2 1. Now delete first two 1's (1 op), array: 2 2 1 2 1 2 1 2 1. Delete first two 2's (1 op), array: 1 2 1 2 1 2 1. Hmm, this is getting complicated but seems to save ops. The point is, the answer is 8.

**I recall now:** The answer to this problem is computed as follows. For each test case, the answer is the number of indices i from 1 to N-1 such that **the set of values seen up to i contains A[i+1]** — no.

Let me think about it as a graph/stack. Actually, I'll derive it: we want to find the minimum number of operations. Consider processing and maintaining a set S of "active" values. 

**Approach: The answer is the number of "useful" elements plus 1.** Specifically:
- We process left to right. Maintain a counter of how many elements of each value are "available" (not yet deleted and not the front).
- Actually, the clean solution: **Answer = N - max_{value v} (number of times v appears such that we can "pair" them)**... 

I'm going in circles. Let me just recall the editorial: This is AtCoder ABC335 F? No. Let me search memory: "make the sequence empty" swap delete operations.

I believe this is **AtCoder Beginner Contest 300, Problem F**? No, ABC300 F is different. This might be **ARC** or **AGC**. 

OK, the solution I recall: **The answer is the number of indices i (1 ≤ i ≤ N) such that A[i] appears for the last time at or after position i in a specific sense.** Let me try: the answer is the size of the "front-distinct" set.

Alternative: **Greedy with a set.** Process i from 1 to N. Maintain a set S of values that have been "seen but not yet closed" (i.e., the last occurrence is still ahead). When we encounter A[i], add to S. When A[i] is the last occurrence of that value, we must do a "close" operation. The answer is the number of times we close + 1? Hmm.

**Let me just think of the dual problem.** The minimum ops = minimum swaps + minimum deletes. We can think of each element that is "wasted" (causes an extra delete) needs a swap to save. 

**The known answer formula:** For this problem, **the answer equals the number of indices i from 1 to N such that A[i] is a "record" in the following sense: the last occurrence of A[i] is at position ≥ i AND A[i] hasn't been "used"**. This is the size of the minimal set of values to delete, but counted with multiplicity in a specific way.

I'll just go with the correct known solution:

**Solution:** 
- We process the array from left to right. Maintain a set `s` of values that are currently "open" (their last occurrence is still ahead, or they are the front pending delete).
- More precisely: we want to count the minimum number of "delete operations". Each delete operation removes a prefix of equal elements. Between two delete operations, we may do swaps.
- **The answer is: 1 + (number of indices i from 1 to N-1 such that A[i] ≠ A[i+1] AND ... )**

Let me try to be concrete with a correct derivation via the "stack of groups" approach. 

**Definitive approach (I'll trust this):**
The minimum number of operations equals the number of elements in the array after we greedily match: **count = 0**. We use a set to track which values are "currently at the front" (i.e., the last value we decided to accumulate). Actually, the correct solution is:

Maintain a set `front` of values that are candidates. Process i=1..N. For each A[i], if A[i] is in the set, remove it (it can be merged into the existing front-value of that type, saving an operation). Else, add A[i] to the set (it starts a new "group" that needs to be accumulated). The answer is `|set| + (number of additions)`... no.

Hmm, let me re-examine. The problem allows: delete a prefix [1..i] if all equal. So after each delete, the front is reset. Between deletes, we swap to make the front equal.

**Clean model:** The sequence of operations is: (swap*, delete-prefix, swap*, delete-prefix, ...). The delete-prefix removes a block of equal elements from the front. So the array is partitioned into blocks B_1, B_2, ..., B_k (in order), each block is all-equal. The cost of processing block B_j is: (cost to make B_j's elements all equal and contiguous at front) + 1 (for the delete). "Making B_j all equal" means we take the original contiguous segment of the array assigned to B_j, and we rearrange it (via adjacent swaps, only swapping within the segment? or can we swap with elements of later blocks?). 

Wait — swaps happen on the current array, which includes later blocks not yet deleted. So swaps can move elements between the "to-be-deleted-soon" region and the "future" region. This makes it complex.

However, note that we can always process without looking ahead: when about to delete block B_j (which corresponds to some contiguous segment of the ORIGINAL array), we only care about making that segment all equal. Elements outside the segment are "future" and haven't been touched by swaps involving the front... actually they have, because swaps are global on the current array.

Let me reconsider. When we're about to make the first deletion, the array is the original (possibly with swaps). The prefix [1..i] to delete must be all equal. The rest [i+1..N] can be anything. So for the first block, we choose some i and value v, pay (cost to make A[1..i] all v via adjacent swaps) + 1. The cost to make a segment all equal to v via adjacent swaps is: number of inversions when aligning all v's to the left, which equals (number of non-v elements in the segment) = i - (count of v in [1..i]). Wait, more precisely, if we want to rearrange a segment to all-v using adjacent swaps, the minimum number of swaps equals the minimum number of element moves, which is: each non-v element must move past some v-elements. It's exactly the number of non-v elements that are to the left of some v-element, which equals (i - count_v) if we bring all v's to the left, minus... actually, the min adjacent swaps to sort a string to all-v (all v's) is: treat it as, all v's can be gathered to one end. The number of swaps equals the number of non-v elements in the way, which for bringing v's to the left = number of non-v elements = i - cnt_v. But this counts moving non-v elements right, which is i - cnt_v. And moving v's left, also i - cnt_v (same set of swaps). So min swaps for segment of length i to become all-v = i - cnt_v(i) where cnt_v(i) is count of v in the segment.

So for the first block: choose i and v, cost = (i - cnt_v_in_[1..i]) + 1.

For the second block: after deleting [1..i], the array is A[i+1..N] (with any internal swaps already done; note swaps within [1..i] don't affect [i+1..N]). Now choose j' and v', cost = (j' - cnt_{v'}_in_[i+1..i+j']) + 1.

But wait — swaps in the second block are on the array A[i+1..N], which is contiguous and unaffected by previous swaps (since previous swaps were within [1..i]). So each block is independent! Therefore:

**Total cost = sum over blocks of (len(block) - max_count_in_block) + number_of_blocks.**

Where max_count_in_block = maximum frequency of any value in that block. This matches my earlier derivation: N - sum(max_freq_per_block) + k, and we choose the partition into contiguous blocks to minimize this, i.e., maximize (sum_max_freq - k).

So the problem reduces to: partition the array into contiguous segments, each segment we compute max_freq, and minimize (N - sum_max_freq + k) = N + k - sum_max_freq.

Equivalently, maximize (sum_max_freq - k) over partitions. This is a DP.

**DP:** dp[i] = min cost for first i elements. dp[0] = 0. 
dp[i] = min_{j < i} { dp[j] + (i-j) - maxfreq(j+1..i) + 1 }.

We need to compute maxfreq of any subarray quickly. This is a standard DP for "partition array into subarrays minimizing cost" with a frequency-based cost. We can optimize with a "small-to-large" or observe constraints. N ≤ 2e5 total, so O(N sqrt N) or O(N * distinct) might work if distinct is small, but distinct can be up to N.

Hmm, N=2e5 and O(N²) won't work. Let me think of a better structure.

**Alternative characterization:** For each position i, let `best[i]` = max over j of (maxfreq in (j,i]) + dp[j-1] - (i - j + 1) + 1 ... this is getting complex.

Let me look for a pattern. Let me compute for the array, the "answer" using a different method and see if it matches.

**Greedy with a set (the correct solution):**

Here's the key insight: We can achieve the optimal by the following greedy. Process i from 1 to N. Maintain a set S of values. 
- When we see A[i], if A[i] is already in S, then we can "merge" this occurrence with the previous one of A[i] (they are in the same delete-block), so we don't need a new operation for it. Remove A[i] from S.
- If A[i] is not in S, add A[i] to S.

At the end, the answer is |S| + ... ? Let me test.

Sample 1: A = 1 1 2 1 2. 
i=1, A=1, S={1}, add.
i=2, A=1, in S, remove. S={}.
i=3, A=2, not in S, add. S={2}.
i=4, A=1, not in S, add. S={1,2}.
i=5, A=2, in S, remove. S={1}.
End. |S|=1. Answer = |S| + 1? = 2. But actual=3. Hmm.

Maybe answer = (number of adds) = ? Adds: i=1,3,4 → 3. Answer=3! Let me check others.
Sample 2: 4 2 1 3. 
i=1,4,add. S={4}.
i=2,2,add. S={4,2}.
i=3,1,add. S={4,2,1}.
i=4,3,add. S={4,2,1,3}. |S|=4. Adds=4. Answer should be 4. Yes! |S|=4, adds=4, answer=4. But the formula "answer = number of adds" gives 4, and "answer = |S|" gives 4. They coincide here. Hmm, but sample 1 they differ (adds=3, |S|=1). So "answer = number of adds" works for samples 1,2. Check sample 3:
1 2 1 2 1 2 1 2 1 2 1.
i=1,1,add. S={1}.
i=2,2,add. S={1,2}.
i=3,1,in S, remove. S={2}.
i=4,2,in S, remove. S={}.
i=5,1,add. S={1}.
i=6,2,add. S={1,2}.
i=7,1,remove. S={2}.
i=8,2,remove. S={}.
i=9,1,add. S={1}.
i=10,2,add. S={1,2}.
i=11,1,remove. S={2}.
End. Adds = i=1,2,5,6,9,10 = 6. But answer = 8. So "adds" = 6 ≠ 8. 

Hmm, so that greedy doesn't directly give the answer. But |S| at end = 1, which is also ≠ 8.

So neither |S| nor adds works. Let me reconsider.

**Let me re-examine the partition DP.** For sample 3: 1 2 1 2 1 2 1 2 1 2 1 (N=11). 
Cost = N + k - sum_max_freq. We want to maximize sum_max_freq - k.
If we take k=1 block (whole array), max_freq = 6 (value 1), cost = 11 - 6 + 1 = 6. But answer=8, so this is better than 8? Wait, cost=6 < 8, so this would be better. But can we achieve cost 6? That would mean: make the whole array all-1's with 11-6=5 swaps, then 1 delete. Is that possible? The array has 6 ones and 5 twos. To make it all-1's, we need to move the 5 twos to be grouped together (so ones surround them or they're at the end), requiring... adjacent swaps to gather 1's: the ones are at positions 1,3,5,7,9,11. To bring all 1's to the front, we swap (1,2)→1,1,2,1,2,... then (2,3)→1,1,1,2,2,... this takes multiple swaps. The minimum adjacent swaps to gather all 1's to the left = number of 2's to the left of the rightmost 1 in the sorted order, which equals 5 (each 2 must move right past some 1's). Actually, min swaps = 5. So cost = 5+1=6. 

But wait — the operations are: do 5 swaps to make array all-1's, then 1 delete. That's 6 operations. But the sample answer says 8 and the problem says 3 ops for sample 1. Let me recheck sample 3 answer = 8. And my calculation gives 6. There's a contradiction, so my model is wrong.

**Why is the model wrong?** Because when we delete a prefix [1..i] that is all-1's, we need those 1's to be at positions 1..i in the CURRENT array (after all swaps). But the swaps I described (gathering 1's to the front) are done before the delete, and that's fine. So why can't we do it in 6?

Let me trace: A = 1 2 1 2 1 2 1 2 1 2 1.
Swap pos 1,2: 1 1 2 1 2 1 2 1 2 1 2. (Wait, I need to be careful.)
Original: [1,2,1,2,1,2,1,2,1,2,1] (indices 1..11).
Swap (1,2): [1,1,2,1,2,1,2,1,2,1,2]? No, swapping positions 1 and 2: positions 1,2 were 1,2 → become 2,1? Let me re-read the problem. "swap the i-th and (i+1)-th elements". So swap positions 1 and 2: element at pos1 and pos2 exchange. So [1,2,...] becomes [2,1,...].

Let me redo. A = [1,2,1,2,1,2,1,2,1,2,1].
Swap (1,2): [2,1,1,2,1,2,1,2,1,2,1]. (now front is 2)
Swap (2,3): [2,1,1,2,1,2,1,2,1,2,1]? positions 2,3 are 1,1 → no change. Hmm.

This is getting messy. The point is, to make the front all-1, we want ones at the front. But the first element is 1 already. We need to move the 2 at position 2 away. Swap (2,3): elements at pos2,3 are 1,1 → swap gives 1,1 (no change). I meant swap to move the 2. The 2 is at position 2. To make position 1..k all 1, we need to eliminate 2's from the front.

Actually, to make the prefix all-1, we process: the first element is already 1 (good). The second element is 2 (bad). To make it 1, we can swap (2,3) only if position 3 is 1 — yes it is. After swap (2,3): positions 2,3 exchange 1,1 → 1,1. No change! Because both are 1. Wait, position 2 is 2, position 3 is 1. Swap: position 2 becomes 1, position 3 becomes 2. So array: [1,1,2,2,1,2,1,2,1,2,1]. Good.
Now positions 1,2 are 1,1. Position 3 is 2. Swap (3,4): [1,1,2,2,...] → [1,1,2,2,...] (both 2, no change). Hmm we need to get rid of the 2 at position 3. Swap (3,4) does nothing (both 2). We need to bring a 1 to position 3. The next 1 is at position 5. 
Swap (4,5): positions 4,5 are 2,1 → [1,1,2,1,2,2,1,2,1,2,1].
Swap (3,4): positions 3,4 are 2,1 → [1,1,1,2,2,2,1,2,1,2,1].
Now positions 1,2,3 are 1,1,1. Position 4 is 2. Continue...
Position 4 is 2, next 1 at position 7.
Swap (5,6): both 2, no. Swap (6,7): [1,1,1,2,2,1,2,2,1,2,1].
Swap (5,6): [1,1,1,2,1,2,2,2,1,2,1].
Swap (4,5): [1,1,1,1,2,2,2,2,1,2,1].
Now 1-4 are 1. Position 5 is 2. Next 1 at position 9.
... this is taking many swaps. The point: making the whole array all-1 requires exactly 5 adjacent swaps? Let me recount. Each 2 must move to the right past some 1's. There are 5 twos and 6 ones. Min adjacent swaps to sort to all-1 = 5 (move each 2 right by some amount; total displacement of 2's = sum of (final_pos - initial_pos) / ... actually for adjacent swaps, min swaps to gather 1's to the left = number of (2,1) inversions = 5*6 - ... = 5*6 - (number of 1's to left of 2's in sorted)... 

The number of inversions where a 2 comes before a 1: in the original, the 2's are at positions 2,4,6,8,10. Each is followed by ones. The 2 at pos 2 has 1's at pos 3,5,7,9,11 (5 ones after it). The 2 at pos 4 has ones at 5,7,9,11 (4). The 2 at pos 6 has 3, pos 8 has 2, pos 10 has 1. Total = 5+4+3+2+1 = 15. So 15 inversions of (2,1) where 2 precedes 1. To gather all 1's to the left, we need each 2 to move right past all 1's to its right. But some 2's are already to the right of 1's. Hmm.

Actually, to make the array all-1 (all 1's), we need all 2's to move to the right of all 1's. The 2 at position 2 needs to move right past the 1's at positions 3,5,7,9,11 (5 swaps minimum for this 2 alone, but shared). The total min swaps = number of 2's = 5? No, it's the number of 2's that need to cross 1's. Each 2 currently at an even position needs to end up after all 1's. The min swaps = sum over 2's of (number of 1's to its left that it needs to cross) + ... it's the inversion count between the multiset when we want all 1's then all 2's. Target: 1,1,1,1,1,1,2,2,2,2,2. Current: 1,2,1,2,1,2,1,2,1,2,1. Inversions (2 before 1 in current that must be 1 before 2 in target): a 2 at current pos p that is "before" a 1 at current pos q (p<q) — in target, all 1's come first, so if current has 2 at p and 1 at q with p<q, that's an inversion that must be resolved. Count: for each 2, count 1's to its right. 2@2: 1's at 3,5,7,9,11 → 5. 2@4: 1's at 5,7,9,11 → 4. 2@6: 3,7,9,11? pos7 is 1, pos9 is 1, pos11 is 1 → 3. 2@8: pos9,11 → 2. 2@10: pos11 → 1. Total = 15. But min adjacent swaps to sort the array to [1,1,1,1,1,1,2,2,2,2,2] equals the number of inversions of type (2,1) = 15. So 15 swaps, not 5.

I confused myself earlier. The cost to make a segment all-v is (length - count_v) only if the segment is arbitrary? No, the min adjacent swaps to make all elements equal to v in a segment is NOT just i - cnt_v. It's the number of non-v elements that are "blocking", but with the constraint that we can only swap adjacent.

For a segment, to make it all-v, we need to move all v's to one side. The min swaps = min_{k} (number of non-v in positions 1..k + number of non-v in positions k+1..i when k = count_v)... actually, the standard result: min adjacent swaps to gather all v's to the left = number of v's - (number of v's already in the left part)... Let's think: place all v's at positions 1..cnt_v. Each non-v at position ≤ cnt_v must move right (cost 1 per position moved? no, per swap). Actually, min adjacent swaps = number of non-v elements in the target region of v's, which is (cnt_v) - (number of v's in positions 1..cnt_v of current). Hmm.

Easier: the min adjacent swaps to transform string S into T (with same multiset) equals the number of inversions between S and T (i.e., pairs (i,j) with i<j, S[i] >_T S[j] where >_T means "comes after in T"). For T = v,v,...,v,others,...,others, the inversions are (v, non-v) pairs where v is to the left of non-v in S, plus (non-v, non-v) inversions which are 0 if T groups them. Wait, the formula is: for each pair of distinct values a,b, count pairs (a,b) with a before b in S and b before a in T, times... Actually, the min adjacent swaps to sort S to T (where T is a permutation of S) is the number of inversions in the permutation mapping S-positions to T-positions.

If T = [v,v,...,v, w,w,...,w, ...] (all v's first, then others), and S is arbitrary with same multiset. The mapping: each element in S maps to its position in T. An inversion is when an earlier element in S maps to a later position in T. So min swaps = sum over each v-element in S of (number of non-v elements to its right in S that are "before v in T"?... 

This is equivalent to: min swaps to make all v = number of non-v elements in S that are to the left of some v, which equals... hmm.

**Key formula:** Min adjacent swaps to make segment all-v = (number of non-v elements in the segment) = len - cnt_v. 

Wait, is that right? Consider S = [2,1]. Make all-1: target [1,1]? No, multiset is {1,2}, can't make all-1. I mean, to make the segment consist of only v's, we'd need to remove non-v's, but we can't remove, only swap. So "make all-v" is impossible if there are non-v's. I see my confusion.

The operation is: we want to delete the prefix. The prefix must be all-equal. So for a block B assigned value v, ALL elements in B must be v. The elements in B are a contiguous segment of the ORIGINAL array. If that segment has non-v elements, we CANNOT make it all-v (because we can only swap, not change values). 

Oh!!! I see the critical error. The values of elements don't change! We can only swap positions. So a block B_j is a contiguous segment of the array that must already consist entirely of the value v_j (in the original array, before any swaps)? No — swaps change positions, so a contiguous segment in the CURRENT array corresponds to a (possibly scattered) set in the original.

Let's be very precise. At the time we delete block B, the array is some permutation (via swaps) of the remaining elements. The prefix [1..|B|] of this current array must be all-v. The current array's first |B| elements come from the original array's remaining elements (those not yet deleted). So we are choosing a subset S of the remaining elements (of size |B|) and arranging them in positions 1..|B| all equal to v, which requires S to consist entirely of v. Therefore, **the block B must correspond to a set of elements that are all value v in the original array**, and they are placed at the front.

So the partition is: we partition the original array's elements into groups, each group is a set of elements all having the same value (not necessarily contiguous originally), and groups are processed in some order (the order they appear at the front). But the "order at the front" must correspond to a valid sequence of adjacent-swap arrangements.

Actually, since we can arbitrarily rearrange the remaining elements via swaps before each delete (as long as we only do adjacent swaps), the constraint is just that we process the elements in some order, and at each step, all remaining elements of the current value are brought to the front. But bringing them to the front requires moving past other elements.

**Revised model:** We process values in some order v_1, v_2, ..., v_k. At step j, we bring all remaining elements of value v_j to the front (cost = number of swaps to do so) and delete them (cost 1). The elements of value v_j are scattered in the current array. To bring them to the front, we need to move non-v_j elements to the right, past them. The min swaps = total number of non-v_j elements in the current array at that time, because each non-v_j element must move right past all the v_j elements (to get behind them). Wait, is that right?

If current array has a mix of v_j and non-v_j, and we want to bring all v_j to the front, the min adjacent swaps equals: for each non-v_j element, it must end up after all v_j elements. So it must swap with each v_j that is initially to its right... no, it must swap until it's after all v_j. A non-v_j at position p must move right past every v_j at position > p? No, past every v_j (since all v_j go to the front). So the min swaps for this non-v_j = (number of v_j to its left)? Hmm.

Let's think: we have a string of v's and n's. We want to sort to v...v n...n. The min adjacent swaps = number of (n,v) inversions where n is before v. Equivalently, for each n, count v's to its right. Sum = total inversions.

In our case, at step j, the current array consists of elements of values v_j, v_{j+1}, ..., v_k. We want to bring all v_j to front. The min swaps = number of (non-v_j, v_j) inversions = sum over each non-v_j element of (number of v_j to its right). Equivalently, = (number of v_j) * (number of non-v_j) - (number of v_j,v_j pairs with v_j left of v_j) ... = total non-v_j * v_j pairs where non-v_j is left of v_j.

If the elements are processed in order v_1,...,v_k, then at step j, the non-v_j elements are those of values v_{j+1},...,v_k. The inversions = sum over each (v_a, v_b) pair with a<j≤b of (number of v_a before v_b in original) - but with the remaining elements only.

Hmm, this is complex. But there's a clean total: **total swaps = number of (x,y) pairs with x≠y such that x appears to the left of y in the original, and y is processed before x.** Because each such pair needs to be swapped (x must move right past y, or y left past x, but y is processed first so y goes to front, meaning x must move right past y). Wait, if y is processed before x, then when we process y, we bring y to front, and x (still in the array, value v_a with a>j) is a non-v_j. So x must move right past y. That's 1 swap per (x,y) pair with x left of y in original and y processed before x. So:

**Total swaps = number of pairs (i,j) with i<j, A[i] ≠ A[j], and A[j] is processed before A[i].**

And total deletes = k (number of distinct values processed, but we can process a value multiple times? Actually, each value is processed at most once, because once all elements of a value are deleted, they're gone. So k ≤ number of distinct values in the array. But we could process only a subset, but to empty the array we must process all values that appear. So k = number of distinct values, and the processing order is a permutation of the distinct values.

Wait, but we might process a value, then later process another value, then the first value again? No, because all elements of the first value are deleted. So each value is processed exactly once. Therefore k = d (number of distinct values). And the processing order is a permutation of the d values.

Total ops = d + (swaps), where swaps = number of (x,y) pairs with x≠y, x left of y in original, and y processed before x.

We want to minimize total ops by choosing the processing order. So minimize d + swaps = d + (number of "inversions" w.r.t. the order, where inversion = x left of y but y before x in order).

For a fixed order, the inversions are pairs (x,y) distinct with x left of y and y before x in order. This equals (total pairs of distinct values) - (concordant pairs). Total pairs of distinct values where x left of y = sum_{distinct x≠y} count_{x left of y}. Let M[x][y] = number of times x appears before y (i.e., number of (i,j) with i<j, A[i]=x, A[j]=y). Then swaps for order π = sum_{π(y) < π(x)} M[x][y].

We want to minimize sum_{π(y) < π(x)} M[x][y] over permutations π. This is a minimum feedback arc set or minimum linear arrangement problem, which is NP-hard in general! So this can't be the right model, or I'm overcomplicating.

Wait, but the problem has a polynomial solution, so my model must allow more. We don't have to bring ALL of a value to the front at once. We can interleave: bring some v's, delete them (as a block of all-v), but wait, a block must be all equal and contiguous. So a "block" is a set of elements of the same value. But a value can be split into multiple blocks! E.g., for value 1 appearing at positions 1,3,5, we could delete positions 1 and 3 together (if we can make them adjacent and at the front), then later delete position 5.

Ah! I see. A value can be deleted in multiple chunks. So my model where each value is processed once is wrong. Let me reconsider.

**General model:** We have a sequence of delete operations. Each delete removes a prefix that is all-equal to some value v. So the array is partitioned into a sequence of blocks B_1, B_2, ..., B_k (in the order they are at the front when deleted), where each block B_j is a set of elements all having the same value v_j, and |B_j| ≥ 1. The blocks partition the multiset of elements. The sequence v_1, v_2, ..., v_k is a sequence (with repetition allowed) of values such that the elements of each value are distributed among the blocks of that value.

The cost is: swaps to arrange so that at each step, the current block is at the front, plus 1 per block.

When we delete block B_j, the elements of B_j must be at the front and contiguous. The elements at the front are exactly B_j (a subset of the remaining elements). So the remaining elements (those not in B_1 ∪ ... ∪ B_{j-1}) are partitioned into "to be deleted now" (B_j, all value v_j) and "to be deleted later" (the rest). To bring B_j to the front via adjacent swaps, the min swaps = number of (later, now) inversions where a "later" element is to the left of a "now" element in the current array.

Current array at step j: it's the original array with the first j-1 blocks' elements removed, and the rest in some order (from previous swaps). But swaps only rearrange; the multiset of remaining is fixed. The current order of remaining elements is determined by previous swaps. To minimize, we can assume previous swaps arranged things optimally. This is complex, but the total swaps over all steps = number of (x,y) pairs with x in some later block, y in some earlier block, and x was to the left of y in the original? 

Hmm, this is getting into minimum linear arrangement / APSP territory, which is hard. But the problem is solvable in poly time, so there must be a simpler structure.

**Let me reconsider the "contiguous segment" model.** Is each block B_j necessarily a contiguous segment in the ORIGINAL array? No, because of swaps. But here's a key observation: when we bring a set of elements to the front to form a block, we can choose ANY subset of the remaining elements that have the same value. However, the order in which we process blocks constrains things.

Actually, I realize: since the values don't change, and we only swap, the relative ORDER of elements with the same value doesn't matter (they're identical). So we only care about the relative order of elements of DIFFERENT values.

Let me define: consider only distinct values. The array is a sequence of values. A "block" is a set of positions with the same value. But positions are interchangeable for same value.

I think the correct simpler model is the following. Since we can arbitrarily reorder same-value elements, the state of the array (up to same-value reordering) is determined by the sequence of values. The minimum swaps to achieve a target arrangement of values is the number of inversions in the target sequence (w.r.t. the current sequence), which for rearranging values = number of pairs (a,b) with a before b currently and b before a in target, where a≠b.

In our problem, the target at each step is "all v's at the front". So from a current value-sequence S, to reach [v,v,...,v, S'], the swaps = number of non-v elements to the left of v elements... which equals (number of non-v) * ... as before, the inversions of type (non-v, v) with non-v before v.

And the total over all steps, summing the swaps, equals the total number of (x,y) pairs with x≠y, x before y in the original, and y is "processed" (i.e., reaches the front and is deleted) before x. Here "processed" means the value y is brought to the front at some step while x is still present.

But x being "still present" when y is processed means x is in a later block (deleted after y's block). So if x is in a later block than y, and originally x is before y, that's a swap. The total swaps = number of (i,j) with i<j, A[i]≠A[j], and the block containing A[j] is before the block containing A[i].

Now, blocks of the same value can be in any order, and each block is a subset of positions of that value. The block ordering is a total order on all blocks. We want to minimize (number of blocks) + (number of cross-block inversions where earlier-block value is to the right of later-block value in original).

Wait, swap condition: (i,j) with i<j, A[i]≠A[j], and block(A[j]) before block(A[i]). So block of j is earlier. This is like: for each pair of positions i<j with different values, if we put j's block before i's block, we pay 1 swap. We want to order all blocks (each block is a set of same-value positions, partitioning each value's positions) to minimize (#blocks) + (#such pairs).

Since each value's positions can be split into multiple blocks, and splitting a value into more blocks increases #blocks but might decrease the pair cost. This is a trade-off.

**Key insight (I recall now!):** The optimal is to NEVER split a value into multiple blocks. Because if a value v has two blocks, we could merge them (process all v together) and save 1 on #blocks, but the swap cost might increase. Let's check: if we merge two v-blocks, we combine them, saving 1 block, but any pair (v, x) where x is between the two v-blocks originally: the v before x and v after x — when merged, the v's are together. The swap condition: pairs (i,j) with i<j, A[i]≠A[j], block(j) before block(i). With merged v-block, for a v at position p1 and v at position p2 (p1<p2), and an x at position p1<q<p2: the pair (x at q, v at p1) with q>p1, so i=q, j=p1? No i<j means i=q>p1=j, so i>j, not i<j. The pair (v@p1, x@q): i=p1<j=q, A[i]=v≠x=A[j], block(j) before block(i)? If x's block is before v's block, then yes, swap. With two v-blocks: v@p1 in block 1, v@p2 in block 2, x@q in some block. If we merge, all v in one block. 

This is getting complicated. Let me just trust the following result which I now recall confidently:

**The answer is: N - (maximum number of "non-crossing" matching or equivalently the size of a maximum antichain / the answer is computed by: for each position i from 1 to N, if A[i] is the first occurrence, count it; the answer is this count.**

Wait, let me check. Sample 1: 1 1 2 1 2. First occurrences: 1 at i=1, 2 at i=3. Count=2. But answer=3. No.

How about: answer = (number of distinct values) + (number of indices i where A[i] is NOT the last occurrence and A[i+1] is a different value that appears later)... 

Let me try a different known formula. For the problem, the answer is:
- Count = 0
- For i = 1 to N:
  - If A[i] is the FIRST occurrence of its value, increment count.
- Answer = count.

Sample 1: first occurrences at 1(1), 3(2). Count=2. Answer should be 3. No.

**Let me try: answer = number of indices i (1 ≤ i ≤ N) such that A[i] appears for the last time at position ≥ i, and... **

Actually, I think the correct greedy is:

**Process from left to right. Maintain a set S. For i=1..N:**
- If A[i] is in S, remove A[i] from S (this A[i] can be merged with the previous A[i] in the same delete-block, saving an operation).
- Else, add A[i] to S.
- Also, if this is the LAST occurrence of A[i] in the array, we must "close" it... 

Hmm, the issue with my earlier test on sample 3 was that I only did add/remove but didn't account for something. Let me reconsider.

The correct greedy for the answer: 
- Initialize answer = 0, set S = {}.
- For i = 1 to N:
  - If A[i] in S: remove A[i] from S. (This A[i] joins its twin.)
  - Else: add A[i] to S.
- At the end, answer = |S| + 1? 

Sample 1: S sequence: {1}→{}(remove 1)→{2}→{1,2}→{1}(remove 2). |S|=1. |S|+1=2≠3.
Sample 2: S: {4}→{4,2}→{4,2,1}→{4,2,1,3}. |S|=4. |S|+1=5≠4.

Nope.

How about: answer = number of "add" operations.
Sample 1: adds at i=1,3,4 → 3. ✓
Sample 2: adds at i=1,2,3,4 → 4. ✓
Sample 3: adds at 1,2,5,6,9,10 → 6. ✗ (should be 8).

So sample 3 fails. The difference: in sample 3, the greedy with set gives 6 but answer is 8. The greedy assumes we can always merge same values perfectly, but we might be forced to interleave.

**The real issue:** In sample 3, the array alternates 1,2,1,2,... The greedy pairs 1-1 and 2-2, but these pairs are non-adjacent and require other operations. The constraint is that to pair a 1 at position 1 with a 1 at position 3, we need to deal with the 2 in between. The 2 at position 2 is "blocking" and must be handled, possibly creating a separate block.

**The correct algorithm (I'm now confident):**

We want to partition the array into the MINIMUM number of blocks such that... no.

**The answer is the size of a maximum matching in a certain bipartite sense, or equivalently:**

```
cnt = 0
S = set()
for i in 1..N:
    if A[i] in S:
        S.remove(A[i])
    else:
        S.add(A[i])
        cnt += 1
answer = cnt
```

Wait, I computed cnt=6 for sample 3 but answer=8. So this is wrong.

Let me look at this differently. The answer 8 for sample 3: 11 elements. We save 11-8=3 operations compared to deleting one-by-one. The savings come from grouping. 

**I think the correct solution is:**

The answer equals the number of indices i (1 ≤ i ≤ N) such that when processing, we "must" do something. Specifically:

Maintain a counter of active "unmatched" values. Process left to right. When we see A[i]:
- If A[i] is currently unmatched (we've seen it before but not closed it? no)...

Let me think about it as: each element is either "free" (can be grouped with a previous same-value element for free) or "costs" an operation. An element costs an operation if it starts a new block. We want to minimize the number of blocks.

The number of blocks ≥ the number of "inversions" in some sense. Specifically, consider the value 1 at positions 1,3,5,7,9,11. To put all 1's in one block, we need to group them, but there are 2's in between. The 2's between consecutive 1's force extra blocks.

**Clean formulation:** The minimum number of operations = maximum, over all values v, of... no.

**I'll go with the following, which I'll verify:**

The answer is computed by: process left to right, maintain a set S. For i=1..N:
- Remove A[i] from S if present, else add A[i] to S.
The answer is |S| + (number of removals) ... no.

Let me try: answer = (number of adds) + |S at end|. 
Sample 1: adds=3, |S|=1, total=4≠3.
Sample 2: adds=4, |S|=4, total=8≠4.

How about: the answer is the number of "distinct values in any suffix" summed... 

**Let me try to recall the exact problem.** This is "Make Empty Sequence" from AtCoder. I believe the answer is:

**Answer = 1 + |{ i : 1 ≤ i < N and the set of values in A[1..i] does not contain the last occurrence of some value... }|**

No. Let me think about the structure. The key observation is:

**The minimum number of operations = the minimum number of "delete prefixes" = N - maximum savings, where a saving occurs when two same-value elements are "mergeable" into one block.**

Two same-value elements at positions p<q can be in the same block iff all elements between them are in blocks that come AFTER this block (i.e., are deleted later). This is a constraint.

**The correct DP/greedy:** 

The answer is the number of "stack pushes" in the following: scan left to right, maintain a set S. When A[i] ∈ S, remove it (it pairs with a previous A[i]). When A[i] ∉ S, add it. The answer is the number of times we ADD to S. But we verified this fails for sample 3.

WAIT. Let me recompute sample 3 with the set:
1 2 1 2 1 2 1 2 1 2 1
i=1: A=1, S={1}, ADD. count=1.
i=2: A=2, S={1,2}, ADD. count=2.
i=3: A=1, in S, remove. S={2}.
i=4: A=2, in S, remove. S={}.
i=5: A=1, S={1}, ADD. count=3.
i=6: A=2, S={1,2}, ADD. count=4.
i=7: A=1, remove. S={2}.
i=8: A=2, remove. S={}.
i=9: A=1, ADD. count=5.
i=10: A=2, ADD. count=6.
i=11: A=1, remove. S={2}.
End. count=6. |S|=1. 

But answer is 8. So the "add count" is 6, but we need 8 operations. The discrepancy is 2. 

Hmm, what if the answer is count + |S at end| = 6+1=7? No, 8.
What if answer = count + (something)? 

Let me reconsider whether the answer for sample 3 is really 8. The array is 1 2 1 2 1 2 1 2 1 2 1 (11 elements). Let me try to achieve 7 operations.
To beat 8, we'd need 7. Can we? Each operation is either swap or delete-prefix. Delete-prefix removes ≥1 element. With k deletes, we remove the array in k chunks, and between chunks we do some swaps. The minimum deletes is the minimum number of blocks, which is... if we could group all 1's together, 1 block for 1's (6 elements) and 1 block for 2's (5 elements), k=2, plus swaps to group them. But grouping requires many swaps. 

If we delete 6 ones in one block: need to bring 6 ones to the front. The ones are at odd positions. To bring them to front, we need the 2's to move right. The swaps needed = number of (1,2) inversions where 1 is right of 2... actually to bring 1's to front, each 2 must move right past the 1's. The min swaps to gather 1's to the left = sum over each 2 of (number of 1's to its right) = 5+4+3+2+1=15. Then 1 delete. Total 16. Worse.

If we do multiple blocks: e.g., delete pairs. Delete 1,1 (positions 1,3): need to swap to make positions 1,2 both 1. Swap (2,3): positions 2,3 are 2,1→1,2. Array: 1 1 2 2 1 2 1 2 1 2 1. Now positions 1,2 are 1,1. Delete them. (2 ops for swap+delete? No: 1 swap + 1 delete = 2 ops, removing 2 elements). Remaining: 2 2 1 2 1 2 1 2 1 (9 elements).
Delete 2,2: already at front, 1 delete. Remaining: 1 2 1 2 1 2 1 2 1 (7 elements).
Now 1 2 1 2 1 2 1 2 1. This is the same pattern, 7 elements (4 ones, 3 twos). 
Delete 1,1: swap (2,3): 1 1 2 2 1 2 1 2 1. Delete first two. Remaining: 2 2 1 2 1 2 1 (5 elements).
Delete 2,2: remaining 1 2 1 2 1 (3 elements).
Swap (2,3): 1 1 2 2 1. Delete first two. Remaining: 2 1.
Delete 2, delete 1. 
Total ops: (swap+delete) for first pair = 2, (delete) for 2,2 = 1, (swap+delete) = 2, delete 2,2=1, swap+delete=2, delete 2=1, delete 1=1, delete 2=1. Let me recount carefully.

Original: 1 2 1 2 1 2 1 2 1 2 1 (11)
1. Swap (2,3): 1 1 2 2 1 2 1 2 1 2 1. (1 op)
2. Delete [1,2]: 2 2 1 2 1 2 1 2 1. (1 op, removed 2)
3. Delete [1,2]: 1 2 1 2 1 2 1 2 1. (1 op, removed 2)
4. Swap (2,3): 1 1 2 2 1 2 1 2 1. (1 op)
5. Delete [1,2]: 2 2 1 2 1 2 1. (1 op)
6. Delete [1,2]: 1 2 1 2 1 2 1. (1 op)
7. Swap (2,3): 1 1 2 2 1 2 1. (1 op)
8. Delete [1,2]: 2 2 1 2 1. (1 op)
9. Delete [1,2]: 1 2 1. (1 op)
10. Swap (2,3): 1 1 2. (1 op)
11. Delete [1,2]: 2. (1 op)
12. Delete [1]: empty. (1 op)
Total 12. Worse.

Let me try a smarter strategy. The known answer is 8. Let me find an 8-op sequence.

Strategy: process from left, whenever two same values become adjacent, delete them.

1 2 1 2 1 2 1 2 1 2 1
1. Swap (1,2): 2 1 1 2 1 2 1 2 1 2 1. (1 op, front is 2)
2. Delete [1]: 1 1 2 1 2 1 2 1 2 1. (1 op)
3. Delete [1,2]: 2 1 2 1 2 1 2 1 2 1. (1 op, removed two 1's)
4. Delete [1]: 1 2 1 2 1 2 1 2 1. (1 op)
5. Swap (1,2): 2 1 1 2 1 2 1 2 1. (1 op)
6. Delete [1]: 1 1 2 1 2 1 2 1. (1 op)
7. Delete [1,2]: 2 1 2 1 2 1 2 1. (1 op)
8. Delete [1]: 1 2 1 2 1 2 1. (1 op)
9. Swap (1,2): 2 1 1 2 1 2 1. (1 op)
... this is one-by-one with a swap each time. 

Let me try: 
A = 1 2 1 2 1 2 1 2 1 2 1.
1. Swap (2,3): A = 1 1 2 2 1 2 1 2 1 2 1. (1 op) [pos2,3: 2,1→1,2]
2. Delete [1,2] (both 1): A = 2 2 1 2 1 2 1 2 1. (1 op)
3. Delete [1,2] (both 2): A = 1 2 1 2 1 2 1. (1 op) [removed 2 twos]
4. Swap (2,3): A = 1 1 2 2 1 2 1. (1 op)
5. Delete [1,2]: A = 2 2 1 2 1. (1 op)
6. Delete [1,2]: A = 1 2 1. (1 op)
7. Swap (2,3): A = 1 1 2. (1 op)
8. Delete [1,2]: A = 2. (1 op)
9. Delete [1]: empty. (1 op)
Total: 9 ops. Close to 8.

Let me try to save one more:
1. Swap (2,3): 1 1 2 2 1 2 1 2 1 2 1. (1)
2. Delete [1,2]: 2 2 1 2 1 2 1 2 1. (1)
3. Delete [1,2]: 1 2 1 2 1 2 1. (1)
4. Swap (2,3): 1 1 2 2 1 2 1. (1)
5. Delete [1,2]: 2 2 1 2 1. (1)
6. Delete [1,2]: 1 2 1. (1)
7. Delete [1]: 2 1. (1)  [delete single 1]
8. Swap (1,2): 1 2. (1)
9. Delete [1,2]: empty. (1)  [delete 1,2 — but they aren't equal! Can't delete both unless equal.]
Oh, [1,2] must be all equal. So step 9 invalid.

Let me redo from 1 2 1:
7. Delete [1]: 2 1. (1)
8. Swap (1,2): 1 2. (1)
9. Delete [1]: 2. (1)
10. Delete [1]: empty. (1)
Total 10. Worse.

From 1 2 1 (after step 6):
7. Swap (2,3): 1 1 2. (1)
8. Delete [1,2]: 2. (1)
9. Delete [1]: empty. (1)
Total 9.

Hmm, can we do 8? The editorial answer is 8. Let me try:
1. Delete [1] (single 1): 2 1 2 1 2 1 2 1 2 1. (1 op)
2. Delete [1] (single 2): 1 2 1 2 1 2 1 2 1. (1 op)
3. Delete [1] (single 1): 2 1 2 1 2 1 2 1. (1 op)
... this is 11 ops.

Better:
1. Swap (2,3): 1 1 2 2 1 2 1 2 1 2 1. (1)
2. Swap (4,5): 1 1 2 1 2 2 1 2 1 2 1. (1) [pos4,5: 2,1→1,2]
3. Delete [1,2,3]? positions 1,2,3 are 1,1,2 — not all equal. 
3. Delete [1,2]: 2