
## ideation
The problem: given nums (n up to 1e5), we may delete all occurrences of at most one value x (array must stay non-empty), then take the maximum subarray sum of the resulting array. Return the max over all choices (including not deleting).

Core observations:
- Deleting a positive value never helps (removing positive elements can only shrink or keep subarray sums; any subarray in the filtered array also exists... actually careful: deleting positives could merge two segments across a negative? No—deleting a positive value removes positive contributions, never beneficial; formally, the filtered array's elements are a subset, and any subarray of the filtered array corresponds to a subsequence but NOT necessarily a contiguous subarray of the original. Hmm, wait: deleting elements merges neighbors, so a subarray of the filtered array may correspond to a non-contiguous pattern in the original. So deleting a positive value x could in theory join two segments separated only by x's. But joining across removed positives means the joined sum = left + right without the positive x's in between — that's strictly less than including the x's if x > 0... but including them requires contiguity in the original, which is allowed since the region between contains only x's (positive). So any filtered subarray sum ≤ the corresponding original subarray sum when x > 0. Hence only negative x (or zero? deleting zeros: joining across zeros gives same sum as including them, so no gain) need consideration. So candidates: no deletion, and delete each distinct negative value.
- For a fixed negative value x, the filtered array = concatenation of maximal segments between consecutive occurrences of x. Max subarray sum of the concatenation can be computed by a Kadane scan over the segments: treat each segment's total and best prefix/suffix, or simply run Kadane where x positions act as skippable zero-cost boundaries... Actually simplest: for value x, iterate over the array once; maintain running sum; when hitting x, we may "reset-free" skip — the filtered concatenation means the element after x directly follows the element before x. So Kadane on filtered array = Kadane on original where x elements are simply skipped (contribute nothing, don't break contiguity). That's an O(n) scan per distinct negative value → O(n · distinct) worst case (e.g., all elements distinct negatives → O(n^2)). Too slow.
- Better: for value x, the filtered array is segments S0 x S1 x S2 ... Sk. Kadane over concatenation needs: total sum of each segment, max prefix sum of each segment, max suffix sum, max subarray within segment. Then combine: answer for x = max over "windows of consecutive segments" of (suffix of Si + sum of middle segments + prefix of Sj). This is itself a Kadane over segment-level values where each segment contributes value = its total, but endpoints can use partial (prefix/suffix). Standard technique: answer = max over i≤j of suff[i] + sum(tot[i+1..j-1]) + pref[j]. Can be computed in O(#segments) with a running best. Sum over all distinct x of (#segments for x) = sum of (occurrences(x)+1) = n + #distinct = O(n). So total O(n).
- Alternative simpler O(n) approach: process positions grouped by value. For each position i with value v = nums[i], we want to know the best subarray sum when v is deleted. Equivalent to: best subarray that either avoids v entirely, or spans across v's. Hmm, the segment approach is cleaner.
- Another angle: compute prefix sums. For value x with occurrence indices p1..pk, filtered array concatenation subarray sums correspond to (prefix sums differences skipping x's). Define adjusted prefix sum P[i] = sum of nums[0..i-1] excluding x's. Then filtered subarray sums = P[j] - P[i] for i≤j where the range contains at least one non-x element. Max subarray sum = max over j of P[j] - min P[i] over valid i<j. Still O(n) per x naively, but we can compute contributions incrementally: each index i participates in the scan for value x = nums[i] only as a "skip", and for all other values as a regular element. That doesn't directly give O(n).
- The segment-decomposition approach is genuinely O(n) total: build for each distinct negative value the list of segments (each segment = maximal run of elements ≠ x). But building segments per x naively is O(n) per x. Instead: note segments for x are determined by positions of x. For each x, we need for each gap between consecutive x's: the segment's total, max prefix, max suffix, max subarray. A gap is a contiguous range of the original array with no x inside. Computing these four values per gap naively costs O(gap length), and summing over all gaps of all x gives sum_x (n) = O(n·distinct). Too slow if done per gap by scanning.

Hmm — so the naive per-gap computation is O(n) per distinct x. Need something smarter. Let me reconsider.

Alternative: For each value x, answer = max subarray sum of array with x removed. Think of it as: max over pairs (i, j) of sum of elements in [i..j] excluding x's, where the range contains ≥1 non-x element. = max over i≤j of (prefixSum[j+1] - prefixSum[i]) - (count/sum of x in [i..j]) = max over i≤j of (PS[j+1] - PS[i]) - x·(cntX[j+1] - cntX[i]). For fixed x, define for each index t a transformed value A[t] = PS[t] - x·cntX[t]. Then answer for x = max over i<j (with at least one non-x in [i..j-1]) of A[j+1] - A[i]. That's "max difference where j is to the right of i" — computable in O(n) per x with running minimum. Still O(n·distinct).

So we need a global O(n log n) or O(n) method. Think differently:

Key structural insight: the optimal deleted value x — consider the optimal filtered subarray; it corresponds to a range [l..r] in the original array, and x is some value appearing inside (or outside) the range... Actually the filtered subarray is a contiguous range [l..r] of the original with all x's inside removed, and the answer sum = rangeSum(l,r) - x·(occurrences of x in [l..r]). We want max over l,r,x. For fixed range, best x is the most negative... no, x·count minimized → x the minimum value in the range? We subtract x·cnt(x in range); to maximize, pick x negative with large |x|·count. But x must appear... actually x can be any value; if x doesn't appear in [l..r], subtracting 0 — but deleting x outside the range doesn't affect this subarray; however deleting x must leave array non-empty (fine). So effectively: answer = max over ranges [l..r] of (rangeSum - min over x of x·cnt_x(range)) where we can choose x = any negative value (only those in the range matter; choosing x not in range = no deletion = subtract 0). So answer = max over ranges of rangeSum - min(0, min over negative x present in range of x·cnt_x). Hmm, x·cnt for negative x is negative, so we subtract a negative → add |x|·cnt. So answer = max over ranges [l..r] of rangeSum(l,r) + max(0, max over negative values v of |v|·cnt_v(l,r)).

That's an interesting formulation: for each range, gain = sum + best "bonus" = |v|·frequency of v within the range for the best negative v. Maximizing this over ranges — n ranges is O(n^2). Need cleverness.

Alternative known approach for this exact problem (it's a LeetCode problem, "Maximum Subarray Sum After Deleting All Occurrences of a Value" or similar — actually LC 3418? "Maximum Amount of Money Robot Can Earn"? No. It's LC weekly: "Maximize Subarray Sum After Removing All Occurrences of One Element" — I recall solution uses grouping by value and prefix minima): 

Trick: For each distinct value x, we want max over j of (A_x[j] - min over i≤j of A_x[i]) where A_x[t] = PS[t] - x·cntX[t]. Rewrite: A_x[t] = PS[t] - x·cntX[t]. For the scan for value x, only positions where cntX changes matter for the "correction". Consider iterating t from 0..n, maintaining for each active value x the running minimum of A_x. That's O(n·distinct) again.

Different idea: process by grouping positions of each value. For value x with positions p1<...<pk: the filtered array's elements are everything except those positions. Max subarray sum of filtered array: consider Kadane on filtered array. Between consecutive x positions, segments. As computed, combining segments needs per-segment (total, pref, suff, best). Total across all (x, gap) pairs of gap length is O(n·distinct) worst case (e.g., array with two interleaved distinct negatives a,b,a,b,...: for value a, gaps are single b's — gap length 1 each, k = n/2 gaps, total O(n). For value b similarly O(n). Actually sum over x of (n) is the worry only if gaps are long for many x. Sum over x of total gap length = sum over x of (n - occ(x)) = n·distinct - n. With many distinct values each appearing few times, e.g., all distinct: each value has 1 occurrence, gaps total n-1 per value → O(n^2). BUT if each value appears once, deleting it just removes one element; answer for x = max subarray sum of array without that single element. Hmm.

Wait — but for values appearing once, deleting x splits array into left and right; filtered max subarray = max(best subarray not crossing position p, and best suffix ending at p-1 + best prefix starting at p+1). That can be computed for all single-occurrence positions in O(n) total using precomputed prefix Kadane (max subarray sum within [0..i], best suffix ending at i) and suffix arrays. Generalizing: for value x with occurrences p1..pk, filtered array = concatenation of segments. Max subarray of concatenation = max over: within one segment, or suffix of segment i + totals of segments i+1..j-1 + prefix of segment j. If we precompute for every position: prefix-sum, best prefix sum starting at position, best suffix ending at position, and segment totals via prefix sums — then per gap of value x we need: total (O(1) via prefix sums), max prefix of gap (max subarray sum starting at gap start — precomputable as "best prefix starting at each index" via reverse Kadane in O(n) once), max suffix of gap (best subarray ending at gap end — forward Kadane once), and within-gap best (max subarray fully inside gap — this is the tricky one: range max subarray query). But within-gap best for gap g of value x is just a candidate "subarray avoiding x" — the global max over all gaps of all x of within-gap best... hmm, we need per-x max though, since answer per x = max(cross-segment combos, within-segment bests). Actually answer for x = max over its segments' within-best AND cross combos. The within-best for x = max subarray sum over ranges containing no x = max over gaps of (range max subarray in gap). 

Range max subarray queries: for value x, gaps are intervals [prev+1, next-1]. We need max subarray sum within each gap. This is a standard "range maximum subarray sum" query — can be answered with a segment tree in O(log n) per query. Total queries = sum over x of (occ(x)+1) = O(n). So total O(n log n). That works!

Simpler alternative: handle within-gap via precomputed "max subarray sum in range [l..r]" queries with a segment tree (each node stores sum, pref, suff, best). Build once O(n), query O(log n). Number of gap queries across all x = n + distinct ≤ 2n. Then per x, combine gaps: answer_x = max over gaps g of within(g), and cross: iterate gaps of x in order, maintaining best = max(best + total(g), suff(g))... standard: cross answer = max over i≤j of suff(g_i) + sum(tot between) + pref(g_j). Compute running: cur = -inf; for each gap in order: candidate = cur + pref(g) (if cur set), update answer; cur = max(cur + total(g), suff(g)). Also answer includes within(g) and single-gap cases (suff+pref within same gap is just within(g) essentially — careful: i=j case gives suff(g)+pref(g) which double counts; restrict cross to i<j, within handled separately).

Per x cost O(#gaps) = O(occ(x)+1). Total O(n + distinct) = O(n), plus segment tree queries O(log n) each → O(n log n) overall. n=1e5, fine.

But wait — do we even need within-gap range queries? The within-gap best for gap g of value x is a subarray avoiding x entirely. The global answer = max over x of answer_x. Note answer_x ≥ any subarray sum avoiding x. The overall no-deletion answer covers subarrays... no, a subarray avoiding x might contain other deletable values — but for answer_x we specifically need max subarray with no x. Hmm, but here's a thought: the overall answer = max over ranges [l..r] of rangeSum + max(0, max over negative v in range |v|·cnt_v). The optimal range for value x might have within-gap portions... I think the segment tree approach is correct and clean. Alternatively, compute within-gap best differently: for each gap (maximal range without x), the max subarray inside it. 

Alternative cleaner overall approach avoiding segment tree: For each x, answer_x = max subarray sum of filtered array. Consider scanning the array once with a "virtual" Kadane per x... no.

Hmm, actually there's an even simpler observation for within-gap: we don't need per-gap within-best separately if we handle it via the cross-segment DP including "within segment" as the segment's own best — but that requires range max subarray per gap regardless.

Let me reconsider: is there an O(n) total way to get within-gap bests for all gaps of all values? Each gap is an interval; total number of gaps O(n); but gaps for different x overlap arbitrarily. Range max subarray queries → segment tree is the standard answer. O(n log n) total is acceptable for n=1e5.

Alternative simpler implementation: for each distinct negative value x, do a modified Kadane scan over the whole array treating x as "skip" (zero-cost, non-breaking). That's O(n) per x — worst case O(n·distinctNeg). Worst case: array of 1e5 distinct negative values → 1e10. Too slow. So segment-tree approach it is. Or:

Another approach: meet in the middle on occurrence counts. For values with high frequency (> B), do the O(n) skip-Kadane scan per value: at most n/B such values → O(n^2/B). For low-frequency values (≤ B occurrences), use the gap method: per x, gaps = occ+1 ≤ B+1, each gap needs total/pref/suff/within. total via prefix sums O(1); pref = max subarray starting at gap start — precompute globally array L[i] = max subarray sum starting exactly at i (reverse Kadane) O(n); suff = R[i] = max subarray ending exactly at i (forward Kadane); within-gap = range max subarray query... still need it. Hmm, but for low-frequency x, maybe within-gap can be bounded differently? No, within-gap can be large (gap could be whole array minus one element).

OK here's another thought — do we actually need exact within-gap max subarray? answer_x = max subarray of filtered array. Any subarray of filtered array either lies within one gap or spans ≥2 gaps. Within-gap ones: max subarray sum of a range with no x. Claim: we can get this from precomputed "max subarray sum over range [l..r]" queries. Segment tree with (sum, pref, suff, best) answers these in O(log n). Total queries O(n). Fine — just implement it. Complexity O(n log n), well within limits.

Actually, wait. Let me reconsider the problem source: this is LeetCode 3418? Let me recall... "Maximum Subarray Sum With One Deletion"? No. This is LC 3483? The constraints 1e5 and the operation "remove all occurrences of x" — I believe the intended solution is O(n) or O(n log n) using prefix sums + per-value grouping with the transformed array trick, plus handling. Hmm, actually I recall a similar problem where the intended solution: for each distinct value x, compute using prefix sums and a sliding minimum over the transformed array A[t] = PS[t] - x·cntX[t], but done efficiently by only updating at positions where x occurs... Let me think: answer_x = max over pairs i<j, range contains non-x of A[j] - A[i] where A[t] = PS[t] - x·cntX[t]. For fixed x, as t increases, A[t] changes by nums[t] - x·[t is x]... The running minimum of A[i] for i ≤ j: between consecutive occurrences of x, cntX is constant, so A[t] = PS[t] - x·c. The min of A over a stretch with constant c = (min PS over stretch) - x·c. So answer_x = max over j of PS[j] - x·cntX[j] - min over i of (PS[i] - x·cntX[i]). Process occurrences of x to maintain the running min in pieces: for each block between x's, min PS in block minus x·c. So per x: O(#blocks) = O(occ(x)+1) using a sparse table / segment tree for range-min of PS, or precompute prefix minima of PS between marks... Range min queries on PS: O(1) with sparse table O(n log n) build, or O(log n) segment tree. Total O((n + distinct)·log n). Also need the "range contains at least one non-x" condition — handle by ensuring j is a non-x position or i... Actually subarray must be non-empty in filtered array, i.e., range [i..j-1] contains a non-x element. If we take j at positions where nums[j-1] ≠ x... simpler: compute candidate for each j (1..n) where nums[j-1] ≠ x: A[j] - minA(i≤j, and ensure range non-empty: i can equal j only if... range [i..j-1] non-empty of non-x means i ≤ j-1 and there's non-x in between; if nums[j-1] ≠ x then i=j-1 works (single element). So for each j with nums[j-1]≠x, candidate = A[j] - min over i ≤ j-1 of A[i]. Running min over blocks works.

This avoids the (pref/suff/best) segment tree and instead needs range-min of prefix sums. But honestly the segment-combination approach with a max-subarray segment tree is also fine. The transformed-prefix-sum approach is more elegant: per value x, answer = max over non-x positions j of (PS[j] - x·c[j]) - (running min of PS[i] - x·c[i] over i in earlier-or-same blocks). Implementation: for each x, get sorted occurrence list; blocks of t in [0..n] split at occurrences+1... For each block [a..b] (indices t where cntX = const = c): we need (1) min of PS[t] - x·c over t in block → (min PS in [a..b]) - x·c; (2) max of PS[t] - x·c over t in block where t≥1 and nums[t-1]≠x → (max PS in [a..b] restricted t≥1... block boundaries: t in block means cntX[t]=c; positions t where nums[t-1]=x are exactly t = p+1 for occurrences p; those t start a new block? cntX[t] = #{occurrences < t}. At t = p+1 where p is occurrence: cntX = c+... let me define cntX[t] = number of occurrences of x in nums[0..t-1]. Then cntX[p] = c (x at p not yet counted), cntX[p+1] = c+1. So blocks are [prev_p+1 .. next_p] in t-space. Within a block, all t have nums[t-1] ≠ x for t ≥ 1? t in (p+1 .. q] where q is next occurrence: nums[t-1] for t-1 in (p .. q-1], i.e., indices p+1..q-1 are non-x, and t-1 = q is x but t = q+1 not in block... block = t ∈ [p+1, q]: t-1 ∈ [p, q-1]; t-1 = p is x! So the leftmost t of each block (except first block) has nums[t-1] = x. So "valid j" in block = block minus its leftmost point (unless block starts at 0). Fine — so we need range min of PS and range max of PS over [a..b] and [a+1..b]. Range min/max queries on static array PS: sparse table O(1) per query after O(n log n) build, or segment tree O(log n). Total queries O(n + distinct). 

Then answer_x = max over blocks of (maxPS_block_valid - x·c - runningMin), updating runningMin = min(runningMin, minPS_block - x·c) as we sweep blocks in order. Also candidate within same block: maxPS in [a+1..b] minus minPS in [a..b-1]... careful: within a block, i<j both in block: candidate = (max PS[j] over valid j in block) - (min PS[i] over i in block, i<j). Since x·c cancels within a block. This is just max subarray sum within the block's element range — the within-gap case again! Ugh, right: within-block pairs (i,j) correspond to subarrays with no x. So we need within-block max subarray too — OR fold it into the sweep: within block, max_{i<j} PS[j]-PS[i] = range max subarray sum of that element range. So we still need range max subarray queries. Unless... we handle it globally: the within-block candidates for value x are subarrays avoiding x. Note the overall final answer = max over x of answer_x, and answer_x includes within-block parts. Could within-block optimum for x ever be the global answer while not being captured by the no-delete case? No-delete case = max subarray sum overall = within-block for... no: max subarray overall might contain x's. A subarray avoiding x with sum S: it's a candidate for answer_x (deleting x keeps it, sum unchanged... wait deleting x doesn't change this subarray's sum, and it's present in filtered array). And it's also present in the no-delete array! So S ≤ no-delete answer. Therefore within-block candidates are ALWAYS dominated by the no-deletion answer! 

So we only need cross-block candidates: subarrays that actually include at least one x (which gets deleted, adding |x|·count bonus). In the sweep, cross-block candidates: j in block c' ≥ c+1, i in block c: A[j] - A[i] = PS[j] - PS[i] - x(c' - c), c' > c. Since x < 0, -x(c'-c) > 0 bonus. The sweep with running min across blocks captures exactly these (i in earlier block, j in later block). Also need i ≤ j-1 and range contains non-x: j valid (nums[j-1]≠x) ensures element nums[j-1] in range, and i ≤ j-1: since i in earlier block, i ≤ p+1 ≤ ... < j automatically i < j. Good. Also i can be in same position range... fine.

Also the "array remains non-empty after deletion" constraint: deleting x requires at least one non-x element exists. If the entire array consists of value x (all same negative), we cannot delete x. Handle: skip x if occ(x) == n. Also we could delete a positive value — never beneficial as argued (any filtered subarray sum ≤ corresponding original range sum... let me double check: deleting positive x, filtered subarray = range [l..r] minus x's, sum = rangeSum - x·cnt < rangeSum ≤ no-delete answer. Yes dominated). Deleting zero: sum unchanged, dominated by no-delete. So only negatives considered. 

Also answer must consider that filtered subarray could be empty? No—subarray non-empty; our candidates always include ≥1 non-x element. Also the no-delete answer: standard Kadane max subarray (non-empty). Edge: all numbers negative, e.g., [-5]: no-delete = -5; deleting -5 not allowed (array would be empty). Answer -5. Another: [-5, -3]: delete -5 → [-3] sum -3; delete -3 → [-5]; no-delete -5? max subarray = -3. Answer -3. Our method: no-delete = -3; for x=-5: blocks t∈[0..0] (c=0), [1..2] (c=1). Valid j in block2: t∈[2..2] (t=1 excluded as nums[0]=x... wait block2 = [p+1..q] = [1..2], leftmost t=1 has nums[0]=x excluded, valid j: t=2, PS[2]=-8, A= -8 -(-5)(1) = -3. Running min from block1: min PS[0..0] - (-5)(0) = 0. Candidate = -3 - 0 = -3. Good. For x=-3: blocks [0..1] c=0, [2..2] c=1. Block1 valid j: t=1 (nums[0]=-5≠-3): but cross-block needs j in later block; block2 valid j: t=2? nums[1]=-3=x → excluded! Block2 = [2..2], leftmost excluded → no valid j. So no cross candidate → answer_x=-3 contributes nothing. Fine, final = max(-3, -3) = -3. Correct.

Range min/max queries on PS: build sparse table or segment tree. n=1e5 → segment tree O(log n) per query, total queries ≈ 2 per block, blocks total = n + distinctNeg ≤ 2n → ~4e5 queries · log n ≈ 7e6 ops. Fine. Or sparse table for O(1): build two sparse tables (min, max) over PS (length n+1): memory n log n = 1e5·17 ≈ 1.7e6 ints each — fine in Python? Might be heavy but okay (~2 lists of 17·1e5 ints ≈ 3.4e6 ints ≈ 100MB in Python lists of ints... Python ints are 28 bytes → too heavy!). Better: use segment tree (iterative, arrays of size 2·2^17) or just use math: actually we can avoid range queries entirely!

Avoiding range queries: For value x, blocks are intervals in t-space. We need min PS and max PS over each block. Precompute prefix min/max of PS? Blocks are arbitrary intervals [a..b], so prefix min alone insufficient — need range min. BUT: process per x by scanning positions of x and using precomputed... hmm. Alternative: for each x, we can compute block min/max by scanning the block — total cost sum over x of block lengths = O(n·distinct). No.

Use segment tree (iterative) with size 2·N where N = next pow2 ≥ n+1: arrays of ~4e5... wait 2·2^17 = 262144·... N=131072, tree size 2N = 262144 for min and one for max — small. Queries O(log n). Total fine. Or even simpler: since we need both min and max range queries on a static array of length n+1, and total queries O(n), a segment tree is simplest to implement correctly. Alternatively sqrt decomposition. Segment tree it is.

Wait, actually there's an even simpler O(n)-total trick: process values x in order and for each block compute min/max PS via... no, stick with segment tree. Or: note we can compute for each x the needed quantities using a different decomposition — for each index t, it belongs to exactly one block of value x=nums[t-1]... not helpful for arbitrary blocks.

Hmm wait, actually let me reconsider: per x, blocks = gaps between occurrences. For each block we need min PS and max PS over the block range. Instead of a general RMQ, precompute nothing fancy — use sparse table only if memory allows. In Python, segment tree with lists of ints size 2·131072 ≈ 262144 entries each — trivial memory. Build O(N). Queries: ~2·(total blocks) = O(n). 

Let me now double-check the formula derivation once more.

Define PS[t] = sum(nums[0..t-1]), t=0..n. For value x, cntX[t] = # occurrences of x in nums[0..t-1]. Filtered array (x removed) subarray sums: choose range [i..j-1] of original (0-indexed, i<j), sum of non-x elements = (PS[j]-PS[i]) - x·(cntX[j]-cntX[i]), requiring range contains ≥1 non-x element. answer_x = max over such pairs. For negative x: sweep t=0..n in order of blocks (constant cntX). Maintain minA = min over processed i of (PS[i] - x·cntX[i]). For each valid j (nums[j-1] ≠ x, j≥1): candidate = (PS[j] - x·cntX[j]) - minA, but only counting pairs where i is in a strictly earlier block OR same block with i<j — same-block pairs are dominated by no-delete answer as shown, EXCEPT we must be careful: same-block pair candidate = PS[j]-PS[i] (x cancels) = subarray sum of range with no x → ≤ no-delete max subarray. Yes dominated. But in the sweep, if minA includes i from the same block as j, the candidate computed might be a same-block pair — harmless (it's ≤ no-delete answer, doesn't inflate). But could minA from same block produce a candidate that's NOT achievable and LARGER than any real pair? Same-block pair (i,j) with i<j is achievable (range has no x, contains non-x since nums[j-1]≠x). If minA comes from i in same block with i ≥ j? In a left-to-right sweep we only add i < current block position... if we process block by block: query max over valid j in block using minA from previous blocks only, then update minA with this block's i's. That gives exactly cross-block pairs. Within-block we skip (dominated). 

But wait: is it truly dominated in all cases? The no-delete max subarray is the max over ALL ranges of rangeSum, including ranges with no x. A within-block pair (i,j) gives range with no x, sum = rangeSum(i,j) ≤ noDeleteMax. Yes. So answer = max(noDeleteMax, max over negative x with occ(x)<n of crossBlockBest_x). 

Edge: what if the optimal for x uses a subarray consisting of elements from multiple blocks where some middle block contributes fully — captured automatically since any i in earlier block, j in later block, range includes everything between (including all x's between, which get deleted). Yes, formula handles it: sum = rangeSum - x·(cnt diff).

Now per-block processing for value x with occurrences p1<...<pk (0-indexed positions in nums). Blocks in t-space: B0 = [0..p1], B1 = [p1+1..p2], ..., Bk = [pk+1..n]. (t ranges 0..n.) For block Bm = [a..b], cntX = m. Valid j's in Bm: t ∈ [a..b] with t ≥ 1 and nums[t-1] ≠ x. For B0 (a=0): valid j = [max(a,1)..b] = [1..p1] (nums[t-1] for t-1 in 0..p1-1: none are x since p1 is first occurrence — correct, all valid). For Bm (m≥1, a = pm+1): t=a has nums[a-1] = nums[pm] = x → invalid; valid j = [a+1..b]. Note b could be < a+1 (empty) — e.g., consecutive occurrences: pk+1 = p{k+1} → block [pk+1 .. p{k+1}] has single t = pk+1 which is invalid → no valid j. Fine.

For each block we need: maxPS over valid-j range, minPS over full block range [a..b] (i's can be any t in block, including t with nums[t-1]=x? i is start of range; range [i..j-1]; i can be any index 0..n-1... i ≤ n-1 since i<j≤n. i = t where range starts at element i. Can i be a position with nums[i]=x? Yes! Range can start with x (deleted). i ∈ [a..b] as long as i ≤ n-1... also i can equal b only if b ≤ n-1 and there's valid j > i in later block — fine, include it. Hmm but also i must satisfy: range [i..j-1] contains non-x — guaranteed by valid j. So minPS over [a..b] but cap b at n-1? i ranges 0..n-1; t=n can't be i. Blocks: last block Bk = [pk+1..n]; i can be up to n-1. If pk = n-1 (x is last element), last block = [n..n], i=n invalid as start (no elements after) — but also no valid j after, so minA from it never used. To be safe, when updating minA use range [a..min(b, n-1)]... actually if we update minA with i=n (PS[n]) it could only affect later blocks — there are none. So harmless. Simpler: just use full block.

Sweep: minA = +inf; ans_x = -inf. For m = 0..k: block [a..b], c=m. (1) If m ≥ 1 and minA finite: query maxPS over valid-j range [jv..b] (jv = a+1 for m≥1; for m=0 we skip candidate since no earlier block); candidate = (maxPS - x·c) - minA; ans_x = max(ans_x, candidate). Wait for m=0 there are no earlier blocks, skip. (2) Update minA = min(minA, minPS over [a..b] - x·c). 

Hold on — order: candidates for block m use minA from blocks 0..m-1. Then update with block m. Correct.

Also need maxPS query over [a+1..b] where a+1 ≤ b else skip; and for m=0 no candidate. Also j must be ≤ n: b ≤ n always. Good.

Number of RMQ queries: 2 per block → total 2·(n + distinctNeg) ≤ 4n... wait total blocks over all x = sum (occ(x)+1) = (sum occ) + distinctNeg = nNeg + distinctNeg where nNeg = # negative elements ≤ n. So ≤ 2n blocks total, ~4n queries, each O(log n) → ~4·1e5·17 = 6.8e6 — okay in Python (borderline but fine with iterative segment tree; could also do sparse table with array module... let's just do segment tree, or even better: since queries are static and offline, we could... keep it simple).

Actually, simpler & faster: precompute prefix-min and suffix-min of PS? Range min over [a..b] isn't derivable from prefix min alone. Use segment tree. Or use Sparse Table with lists of ints — memory: 17 levels × 1e5 × 8 bytes (if using array('i') or just accept Python int list ~ 17·1e5·28B ≈ 48MB per table, two tables 96MB — risky). Segment tree: 2·131072·28B ≈ 7MB per tree, two trees 15MB — fine. Or one tree storing pairs (min,max) as tuples — tuple overhead; use two separate trees or encode. I'll use two iterative segment trees (min-tree, max-tree) or a single tree with combined... Let me just write min and max segment trees with lists.

Alternatively — completely different, simpler-to-code approach: for each negative value x, run the "skip-Kadane" O(n) scan, but bound total cost by noting sum over x of n is too big... no. Another simple approach: for each x, iterate only over occurrences and use precomputed prefix sums + precomputed "range min/max of PS" via segment tree as above. I'll go with that.

Let me also double check the "only negative x" claim once more with a tricky example: nums = [5, -1, 5]. No-delete max = 5-1+5 = 9. Delete x=5 (positive): filtered = [-1], max = -1. Worse. Delete -1: [5,5] sum 10 > 9. Negative only. Good. Zero: nums=[3,0,3]: no-delete=6, delete 0 → [3,3] sum 6 same. Fine.

Another check: x appears, all cross candidates — example from problem: nums=[-3,2,-2,-1,3,-2,3], x=-2, occurrences at 1... 0-indexed: p=[2,5]. PS: t=0:0; t=1:-3; t=2:-1; t=3:-3; t=4:-4; t=5:-1; t=6:-3; t=7:0. Blocks: B0=[0..2] c=0; B1=[3..5] c=1; B2=[6..7] c=2. x=-2.
- B0: update minA: min PS[0..2] = min(0,-3,-1) = -3 → minA = -3 - (-2·0) = -3.
- B1=[3..5]: valid j = [4..5]: max PS[4..5] = max(-4,-1) = -1. candidate = (-1 - (-2)(1)) - (-3) = (-1+2)+3 = 4. Hmm that gives 4? Expected answer 7 via range [1..6] (2,-1,3,3 after deleting -2's): i=1 (t=1, in B0), j=7 (t=7 in B2). Let me continue. Update minA: min PS[3..5] = min(-3,-4,-1) = -4; A = -4 - (-2)(1) = -2; minA = min(-3, -2) = -3.
- B2=[6..7]: valid j=[7..7]: PS[7]=0. candidate = (0 - (-2)(2)) - (-3) = (0+4)+3 = 7. ✓. Update minA: min PS[6..7]=min(-3,0)=-3; A=-3+4=1; minA stays -3.
ans_x = 7. ✓ 

Now complexity: distinct negatives up to 1e5, each with 1 occurrence → blocks per x = 2, total blocks 2e5, queries 4e5, each O(log n) ≈ 17 steps → ~7e6 Python operations — acceptable (maybe ~2-3s; could optimize with sparse table using min over precomputed logs... let's consider a faster RMQ: since PS is static, build a sparse table only for min and max? Memory concern. Alternative: sqrt decomposition with block size ~320: query O(320) worst → 4e5·320 too slow. Segment tree fine. Actually, we can halve queries: note for consecutive occurrences blocks with no valid j, skip max query. Minor.)

Alternative neat optimization: instead of RMQ per block, process each x by scanning its occurrences and using precomputed arrays: prefixMin/Max of PS and suffixMin/Max of PS. Block [a..b] min = ? Not derivable. OK segment tree.

Hmm, wait — actually there's an even simpler global O(n) approach I should consider: For each index t (0..n), and for the value x = nums[t] (the element at position t, if we think of deletions)... Let me think about the structure differently: answer_x cross candidate = max over occurrence-boundary pairs. Consider each occurrence p of x: it separates "before" and "after". The best subarray that deletes x and includes elements from both sides of p... Not exactly; subarray may span multiple occurrences. But: optimal (i,j) for x: let p be the first occurrence of x in [i..j-1] and q the last. Then i is in block ending at p (i ∈ (prevOcc..p]), j in block starting after q. Sum = (PS[j] - x·cntX[j]) - (PS[i] - x·cntX[i]). For fixed x, we want min A[i] over i ≤ p (i in blocks before... i can be anywhere ≤ p with cntX[i] = cntX at that block) and max A[j] over j ≥ q+1. Since cntX[i] ≤ cntX[p] = c and A[i] = PS[i] - x·c_i with x<0: -x·c_i ≥ ... hmm this doesn't decouple per-occurrence nicely because i's block matters. The block sweep is clean. Keep it.

Implementation plan:
1. n = len(nums). PS = [0]*(n+1); accumulate.
2. noDelete = Kadane max subarray of nums. (Standard, non-empty.)
3. Build segment trees for range-min and range-max over PS (length n+1). Iterative segment tree with size N = 1 << (n).bit_length()... n+1 leaves; size = 1 << ceil(log2(n+1)). minTree = [inf]*(2*size), fill leaves; build. Same for max with -inf.
4. Group positions by value for negative values: dict value → list of indices (increasing, naturally by scan order).
5. ans = noDelete. For each negative x with occ list pos (len < n, i.e., skip if len(pos)==n — only possible when n==len(pos), meaning all elements equal x):
   blocks: prev = -1; minA = inf; best = -inf.
   For m, p in enumerate(pos): block = [prev+1 .. p], c = m. Then after loop, last block [pos[-1]+1 .. n], c = len(pos).
   Process blocks in order: for block [a..b] with c=m:
     if m ≥ 1 (i.e., not first block) and minA finite: jv = a+1; if jv ≤ b: qmax = rangeMax(jv, b); cand = qmax - x*c - minA; best = max(best, cand).
     qmin = rangeMin(a, b); minA = min(minA, qmin - x*c).
   Note for first block (m=0, a=0): valid j range would be [1..b] but no earlier blocks → no candidate; just update minA with [0..b].
   Wait — careful: for m≥1 blocks, a = prev_occ+1, and t=a corresponds to nums[a-1]=nums[prev_occ]=x → invalid j. jv=a+1. ✓. For the last block (m=k): same rule (a = pos[-1]+1, a-1 is occurrence) → jv=a+1. ✓.
   ans = max(ans, best) if best finite.
6. Also consider: what about deleting a negative x where cross candidate uses i in block m and j in same... no, handled.
7. Return ans.

Wait, one more subtlety: the "i" range within block — i can be any t in [a..b], but i must be ≤ n-1 (range non-empty needs i < j ≤ n; since j in later block ≥ a'+1 > b ≥ i... j ≥ (next block's a')+1 = p+2 > p ≥ b ≥ i, and j ≤ n, so i ≤ n-2 automatically? If b = n (last block) no later block. For non-last blocks b = p ≤ n-1, i ≤ p ≤ n-1 ✓ (i=p means range starts at element p which is x — allowed, it gets deleted; range [p..j-1] contains non-x since j valid). ✓.

Also minA initialized from block 0 which always exists (possibly empty? block0 = [0..p1], p1 ≥ 0 so non-empty, contains t=0). ✓.

Edge: x occurs but all blocks after first have no valid j (x is last element or consecutive at end): best stays -inf → contributes nothing. Fine.

Edge: n=1: nums=[5]: noDelete=5; negatives none (or if [-5]: occ=1=n → skip). Answer 5 / -5. ✓.

Now, is skipping x when occ(x)==n correct? If all elements equal x (negative), we cannot perform the operation (array would become empty). But we also don't need to: noDelete = x (single element max... all same negative, max subarray = x). But wait — could we delete a different value y not present? "Choose any integer x such that nums remains non-empty on removing all occurrences of x." If y not present, removing all occurrences of y leaves nums unchanged (non-empty) — allowed but useless. So answer = noDelete. ✓. Our loop skips x (the only distinct value) → ans = noDelete. ✓.

Double-check the dominance argument for within-block pairs once more, because the sweep's minA only includes earlier blocks — we never compute within-block candidates, and we argued they're ≤ noDelete. Within-block pair (i,j) both in block m, i<j, j valid: sum = PS[j]-PS[i] (x terms cancel) = sum of elements nums[i..j-1], a range with no x. This is a subarray of the original array → its sum ≤ noDelete (Kadane max). ✓. So ignoring them is safe.

Also pairs where j invalid (nums[j-1]=x)? Then range [i..j-1] ends with x; the same filtered subarray is represented by (i, j-1)... range [i..j-2] has same non-x elements (since nums[j-1]=x removed anyway). If j-1 valid or range still non-empty... The filtered subarray corresponding to (i,j) = filtered subarray of (i, j') where j' = j-1 if nums[j-1]=x. Eventually reduces to valid j or empty. So restricting to valid j loses nothing. ✓.

Similarly i with... i can be anything; if nums[i]=x, range [i..j-1] filtered = range [i+1..j-1] filtered, same sum. Our minA might pick i with nums[i]=x giving same A value as i+1? A[i] vs A[i+1]: PS[i+1]-PS[i] = x, cntX differs by 1 → A[i+1] = PS[i+1] - x(c+1) = PS[i]+x - xc - x = A[i]. Equal! Nice — consistent, no issue.

Great, the approach is solid. Now the segment tree: I'll implement range min and range max over PS array of length m=n+1.

Iterative segment tree:
size = 1
while size < m: size <<= 1
INF = float('inf')
mn = [INF]*(2*size); mx = [-INF]*(2*size)
mn[size:size+m] = PS; mx[size:size+m] = PS
for i in range(size-1, 0, -1): mn[i] = min(mn[2i], mn[2i+1]); mx[i] = max(...)
Query(l, r) inclusive: standard l+=size, r+=size+1 loop.

Total queries ~4e5, each O(log size) ≈ 17 iterations with a few ops — ~1e7 basic ops in Python. Might be ~2-4 seconds. Acceptable for most judges; could micro-optimize. Alternative: Sparse table with O(1) query using precomputed log table and min of two — build O(n log n) memory heavy in Python. Or: since we need both min and max, and queries are many, maybe use a different trick: process each value's blocks and use precomputed prefix min/max AND suffix min/max: rangeMin(a,b) — no.

Actually, here's a cleaner O(1)-amortized idea: for each value x, its blocks partition [0..n] — but different x give different partitions. No sharing. Segment tree is fine. Let me estimate better: total blocks = sum over neg distinct x of (occ+1) ≤ n_neg + d ≤ 2e5 (n=1e5). Per block: 1 min query always, 1 max query if has valid j and m≥1. So ≤ ~2e5 min queries + ~2e5 max queries = 4e5 queries. Each query ~2·17 = 34 loop iterations → 1.4e7 iterations. In Python ~5-10s. Hmm, risky. Optimize:

Option A: Sparse table for min and max with O(1) queries. Build: log table via DP; st[k][i] for k up to 17, each a list of length m. Memory: 17 lists × 1e5 Python ints ≈ 17·1e5·28 bytes ≈ 48MB per table → 96MB for two. Might MLE depending on judge (typical 256-512MB → okay actually). Build time O(n log n) = 1.7e6 min ops per table — fast. Queries O(1): 4e5 queries → trivial. This is better time-wise. But Python int memory... using array('i')? PS values up to 1e11 (1e5·1e6) — need 64-bit: array('q'). array module operations convert to Python ints on access anyway; memory 8 bytes × 17 × 1e5 = 13.6MB per table. 

Option B: Reduce query count. Note min query per block and max query per block. Combine: single segment tree query returning (min,max) pair — halves the traversal count (one traversal gets both). ~2e5 combined queries × 34 iters = 7e6 — better. Implement query returning tuple; node stores... two trees but query both simultaneously in one loop over l,r — just write a function that queries both trees in the same loop. Easy.

Option C: Cartesian tree / RMQ via ±1 ... overkill.

Option D: Notice we can precompute for each position t the "previous occurrence of nums[t-1]" and process... no.

Option E: Different algorithm altogether avoiding RMQ: Hmm, think about processing values in increasing order of... Let me think if there's a known simpler solution. Actually, I recall this problem: LeetCode 3418 "Maximum Amount of Money..."? No. Let me recall: "Remove All Occurrences of a Value to Maximize Subarray Sum" — I think it's from a recent LC contest (maybe Biweekly 140-ish?), and intended solutions include O(n log n) with prefix sums + monotonic/stack or segment tree. Our approach matches.

Let me also reconsider Option F: for each value x, instead of RMQ per block, compute block min/max by direct scan but amortize: total over x of sum of block lengths = sum_x (n+1) = (n+1)·d — too big when d large. But when d large, occ per x small → blocks small? No: sum of block lengths for x = n+1 regardless of occ. So no.

Go with Option B (single-pass dual min/max segment tree query) or sparse table. I'll implement an iterative segment tree storing min and max in two arrays, with a combined query loop. Or simpler to code: sparse table? Build code is short:

log = [0]*(m+1); for i in 2..m: log[i]=log[i//2]+1
K = log[m]+1
stMin = [PS[:]] ; stMax = [PS[:]]
for k in 1..K-1: prev = stMin[-1]; stMin.append([min(prev[i], prev[i+2^(k-1)]) for i in range(m - 2^k + 1)]) — list comprehensions, total 1.7e6 ops per table, fine. Memory as discussed ~50MB per table with Python ints... PS entries are Python ints (big, up to 1e11, still small objects ~32 bytes). 17 levels × avg 1e5 × 32B ≈ 54MB per table, 108MB both. Risky. Segment tree (Option B) memory: 2 arrays × 2·131072 entries × 32B ≈ 17MB. Safer. Go with segment tree + combined query.

Actually, even simpler: one segment tree where each node packs (min << 40) + (max + offset)? Values up to 1e11 < 2^37; pack min and max into single int: node = (min+OFF) * BASE + (max+OFF)? Then query needs min of mins and max of maxes — packing doesn't allow independent combine. Skip; two arrays, one combined query function.

Let me now also handle the noDelete via Kadane: cur = max ending here = max(num, cur+num); best = max(best, cur). Initialize cur = -inf or nums[0].

Now, grouping: positions = dict; for i,v in enumerate(nums): if v < 0: positions.setdefault(v, []).append(i).

Main loop per x:
pos = positions[x]; k = len(pos)
if k == n: continue
minA = INF; best = -INF
prev = -1
blocks = []
for m in range(k+1):
    a = prev+1
    b = pos[m] if m < k else n
    # block [a..b], c = m
    if m >= 1 and minA != INF:
        jv = a+1
        if jv <= b:
            qmax = rangeMax(jv, b)
            cand = qmax - x*m - minA
            if cand > best: best = cand
    qmin = rangeMin(a, b)
    val = qmin - x*m
    if val < minA: minA = val
    prev = pos[m] if m < k else None  # update prev
if best != -INF: ans = max(ans, best)

Wait, x·m: x negative, m = c. A[t] = PS[t] - x·cntX[t] = PS[t] - x·m. ✓.

Combined query function query(a,b) returns (mn, mx). Use it once per block: qmin, qmax = query(a, b) — but max needed only over [a+1..b] for m≥1. Two different ranges. Hmm: query(a,b) for min; query(a+1,b) for max when needed. So up to 2 queries per block. Could derive: max over [a+1..b] from query(a,b) unless the max is attained only at a — can't know. Just do second query when needed. Total queries ≤ 2 per block ≈ 4e5... combined dual-tree query does both trees in one loop but here ranges differ, so two separate query calls; each call traverses both trees? No — min query only needs min tree, max only max tree. So write rangeMin(a,b) and rangeMax(a,b) separately, each ~34 iters. Total ≈ (2e5 min + up to 2e5 max) × 34 ≈ 1.4e7. Hmm. Optimization: skip max query when jv > b (empty) — happens for consecutive occurrences; in worst case (all distinct negatives) every block has valid j... blocks for single occurrence: [0..p] and [p+1..n]; second block valid j = [p+2..n] non-empty unless p=n-1. So ~2 queries per value × 1e5 values × 34 = 7e6 for max + 7e6 for min = 1.4e7 iterations. Python ~0.1µs per simple iteration... more like 50-100ns → 1.4e7 × ~80ns ≈ 1.1s. Plus overhead. Probably OK (~2s total). Fine.

Alternatively reduce: for the min update, note we process blocks left to right and minA accumulates — we need rangeMin(a,b) each block. Unavoidable with this method. OK.

Let me reconsider whether there's an O(n) method without RMQ, for elegance: 

Claim: answer_x (cross) = max over occurrences pairs... Let me define for each index t, and consider value x. Hmm, alternative: for each pair (i, j) contributing to answer_x, x is some negative value in (i..j-1). Consider scanning j from 1..n, maintaining a data structure over i of A_x[i] for "the x that..." — x varies per pair. No.

Different: answer = max over negative x of max over j valid (PS[j] - x·c_j) - min over i in earlier block (PS[i] - x·c_i). Rewrite candidate for pair (i,j): PS[j] - PS[i] - x(c_j - c_i) where c_j > c_i. = rangeSum(i,j) + |x|(c_j - c_i). For fixed pair (i,j), best x = the negative value maximizing |x|·(occurrences in range) — as noted before. No simple O(n).

I'm confident in the segment tree approach. Let me also sanity check a few more examples mentally.

Example: nums = [1,2,3,4] → no negatives → ans = noDelete = 10. ✓ (matches Example 2).

Example: nums = [-1, 5, -1, 5]: noDelete: Kadane: -1, 4, 3? compute: cur=-1 best=-1; cur=max(5,4)=5 best=5; cur=max(-1,4)=4 best=5; cur=max(5,9)=9 best=9. noDelete=9. x=-1, pos=[0,2], k=2. PS=[0,-1,4,3,8]. Blocks: m=0: [0..0]: minA = PS[0]-(-1·0)=0. m=1: a=1,b=2: valid j=[2..2]: PS[2]=4; cand = 4 - (-1)(1) - 0 = 5. update minA: min PS[1..2]=min(-1,4)=-1; A=-1+1=0; minA=0. m=2: a=3,b=4: valid j=[4..4]: PS[4]=8; cand=8-(-1)(2)-0=10. best=10. ans=max(9,10)=10. Check: delete -1 → [5,5] sum 10. ✓.

Example: nums=[-2, -3]: noDelete=-2. x=-2: pos=[0]; blocks m=0:[0..0] minA=0; m=1: a=1,b=2: valid j=[2..2]: PS=[0,-2,-5]; PS[2]=-5; cand=-5-(-2)(1)-0=-3. best=-3 → delete -2 → [-3] sum -3 ✓. x=-3: pos=[1]; m=0:[0..1]: minA=min(PS[0],PS[1])=min(0,-2)=-2. m=1: a=2,b=2: valid j=[3..2] empty → no cand. best=-inf. ans=max(-2,-3)=-2. Correct: options: no delete -2; delete -2 → -3; delete -3 → [-2] sum -2. Answer -2. ✓.

Example: all same: [-7,-7]: noDelete=-7; x=-7 occ=2=n → skip. ans=-7. ✓.

Example with zero: [0, -1, 0]: noDelete=0. x=-1: pos=[1]; PS=[0,0,-1,-1]. m=0:[0..1]: minA=min(0,0)=0. m=1: a=2,b=3: valid j=[3..3]: PS[3]=-1; cand=-1-(-1)(1)-0=0. best=0. ans=0. Delete -1 → [0,0] sum 0. ✓.

Large positive separated by single negative: [5, -1, 5] done → 10. ✓.

Now, potential pitfall: float('inf') arithmetic — qmin - x*m with qmin=inf? Block always non-empty (a≤b guaranteed? block [a..b]: a=prev+1, b=pos[m] or n; a≤b since prev < pos[m]. Yes non-empty). So queries always valid range. Good. Use int inf = 10**30 to keep int arithmetic.

One more correctness consideration: we restrict to negative x. What about deleting a positive x to merge across negatives? Deleting positive x removes x's from array; a filtered subarray corresponds to range [i..j] with sum' = rangeSum - x·cnt ≤ rangeSum ≤ noDelete. So dominated. ✓. Zero similar (sum'=rangeSum). ✓.

Also "at most once" includes not deleting → noDelete covers it. ✓.

Now complexity summary: O(n) Kadane + O(n) PS + O(n) segtree build + O((n + d) log n) queries ≈ O(n log n). n=1e5 fine.

Implementation details for segment tree (iterative):
m = n+1
size = 1
while size < m: size <<= 1
INF = 10**30
tmin = [INF]*(2*size)
tmax = [-INF]*(2*size)
tmin[size:size+m] = PS
tmax[size:size+m] = PS
for i in range(size-1, 0, -1):
    a = tmin[2*i]; b = tmin[2*i+1]; tmin[i] = a if a<b else b
    a = tmax[2*i]; b = tmax[2*i+1]; tmax[i] = a if a>b else b

def rmin(l, r):  # inclusive
    res = INF; l += size; r += size+1... wait r inclusive: r += size; then while l <= r style or use l, r+1 half-open. I'll write half-open [l, rr):
def rmin(l, rr):  # [l, rr)
    l += size; rr += size; res = INF
    while l < rr:
        if l & 1: res = min(res, tmin[l]); l += 1
        if rr & 1: rr -= 1; res = min(res, tmin[rr])
        l >>= 1; rr >>= 1
    return res
Similarly rmax.

To speed up, inline these as local variables in the loop (function call overhead ×4e5 is okay-ish ~0.2s). Could also bind tmin_local = tmin etc.

Alternatively, to cut constant: note we need rmin over [a..b] and rmax over [a+1..b]. Write one function rminmax(l, r) inclusive returning both, and for max over [a+1..b] call rmax separately only when needed... I'll just implement rmin and rmax and call as needed; micro-opt by assigning to locals.

Actually, better idea to halve queries: for block m≥1, we need rmax(a+1, b) and rmin(a, b). For block 0 only rmin. Fine, ~1.5 queries avg.

Let me also double check the candidate formula sign: cand = qmax - x*m - minA where qmax = max PS[t] over valid j in block m, and A[j] = PS[j] - x·m. x negative → -x·m positive bonus. minA = min over earlier blocks of (PS[i] - x·c_i). cand = A[j] - minA. ✓.

Now write final code:

from typing import List

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        PS = [0]*(n+1)
        for i, v in enumerate(nums):
            PS[i+1] = PS[i] + v

## worker: Implement the full solution: prefix sums + dual mi
- **Reduction**: A filtered subarray (after deleting all `x`) corresponds to an original range `[i..j-1]`; its sum is `(PS[j]-PS[i]) - x*(cntX[j]-cntX[i])`. Deleting a non-negative `x` never beats the no-delete answer (sum only decreases or stays equal), so only distinct negative values are candidates.
- **Dominance**: Pairs `(i,j)` lying in the same block (constant `cntX`, i.e., range contains no `x`) give sums that are ordinary subarray sums of the original array, hence ≤ the Kadane no-delete answer. Only cross-block pairs need evaluation.
- **Sweep per value**: For value `x` with occurrences `p1..pk`, blocks in prefix-sum index space are `[prev+1 .. p]` (plus final `[pk+1 .. n]`). Sweeping blocks in order, maintain `minA = min(PS[i] - x*cntX[i])` over earlier blocks; for each block, the best `j` is `max PS[j] - x*cntX` over valid `j` (excluding the block's first index, whose preceding element is `x`). Candidate = `A[j] - minA`.
- **RMQ**: Range min/max over the static `PS` array via two iterative segment trees. Total blocks across all values = `n_neg + distinct_neg ≤ 2n`, so total queries are O(n), each O(log n) → overall O(n log n), well within limits for n = 1e5.
- **Edge cases handled**: all-equal negative array (skip deletion when `occ(x) == n`), single element, all positives (no candidates, return Kadane), zeros (never beneficial), consecutive occurrences (empty valid-`j` ranges skipped).
- Verified against both provided examples mentally: Example 1 yields 7 via `x = -2` (blocks `[0..2]`, `[3..5]`, `[6..7]`, candidate `0 + 4 + 3 = 7`); Example 2 yields 10 with no negatives.

## worker: Verify the implementation against both provided ex
I verified the implementation thoroughly against the provided examples and all requested edge cases, tracing the block logic by hand. Everything checks out.

**Provided examples:**
- Example 1 `[-3,2,-2,-1,3,-2,3]`: For `x=-2` (positions 2,5), PS = `[0,-3,-1,-3,-4,-1,-3,0]`. Blocks: `[0..2]` (c=0), `[3..5]` (c=1), `[6..7]` (c=2). Sweep: minA=-3 after block 0; block 1 candidate = `max(PS[4..5]) - (-2)(1) - (-3) = -1+2+3 = 4`; block 2 candidate = `PS[7] - (-2)(2) - (-3) = 0+4+3 = 7`. ✓ Returns 7.
- Example 2 `[1,2,3,4]`: no negatives → returns Kadane result 10. ✓

**Edge cases verified:**
- `n=1` (`[5]` → 5; `[-5]` → -5): Kadane handles it; for `[-5]`, `occ(-5)==1==n` → skipped (deletion would empty the array). ✓
- All-same-negative `[-7,-7]`: `occ(-7)==2==n` → skipped; answer = -7. ✓ (Deleting a value not present is allowed but useless, so no-delete answer stands.)
- Zeros `[0,-1,0]`: deleting 0 never helps (sum unchanged); `x=-1` gives candidate 0; answer 0. ✓
- Consecutive occurrences `[-1,-1,5]`: block between the two `-1`s is `[1..1]`; valid-j range `[2..1]` is empty → max query correctly skipped; min update still runs. Result: delete -1 → [5], answer 5. ✓
- All positives: `positions` empty → early return of Kadane sum. ✓
- Mixed trace `[-1,5,-1,5]`: candidates 5 and 10 → answer 10 (delete -1 → [5,5]). ✓
- `[-2,-3]`: delete -2 → -3; delete -3 → -2 (block after occurrence has empty valid-j, no candidate); no-delete -2. Answer -2. ✓

**Block-boundary logic double-checked:**
- *Valid-j exclusion*: For block `m≥1`, `a = prev_occurrence+1`, so `t=a` has `nums[t-1] == x` — invalid as a subarray end (the filtered subarray would be identical to ending at `t-1`... rather, ending with a deleted element, which is redundant). Excluding it loses nothing because any range ending exactly on an `x` has the same filtered sum as the range ending one earlier. For block 0, `t=0` is excluded naturally since `j≥1` and block 0 never generates candidates anyway (no earlier block).
- *minA ordering*: Candidates for block `m` are computed BEFORE merging block `m`'s values into minA, so only strictly earlier blocks contribute — exactly the cross-block pairs. Within-block pairs are provably dominated by the no-delete Kadane answer (their `x` terms cancel, yielding an ordinary subarray sum of the original array), so excluding them is safe.
- *i-position validity*: `i` may coincide with an `x` position (range starting with a deleted element) — allowed and correctly included in minA; note `A[i]` equals `A[i+1]` in that case, so no inconsistency arises.
- *occ(x)==n skip*: correct per the non-emptiness constraint.
- *Only negatives considered*: deleting `x>0` gives filtered sums `rangeSum - x*cnt < rangeSum ≤ noDelete`; deleting `x=0` changes nothing. Both dominated. ✓

**Complexity**: O(n) Kadane + O(n) prefix sums + O(n) segment-tree build + O((n + distinct_neg)) blocks with O(log n) RMQ each → O(n log n) total, ~4·10⁵ queries worst case. Well within limits for n = 10⁵.
