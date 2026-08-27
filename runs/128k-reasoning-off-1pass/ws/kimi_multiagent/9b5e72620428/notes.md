
## ideation
The core difficulty is handling the wildcards (-1) in both sequences and the ability to permute A. Since A can be rearranged arbitrarily, we only care about the multiset of values in A, not their original positions. The problem reduces to finding a target sum S such that:
1. All fixed elements in A and B are ≤ S.
2. We can match every element in A with a distinct element in B such that their sum is S, where wildcards can take any non-negative integer value to complete the sum.

Key observations:
- If there are no wildcards, we just check if the multiset of A values equals the multiset of S - B values for some S.
- With wildcards, we have flexibility. A wildcard in A can pair with any B_j ≤ S (becoming S - B_j). A wildcard in B can pair with any A_i ≤ S.
- The candidate sums S can be derived from fixed elements: if we pair fixed A_i with fixed B_j, then S = A_i + B_j. Also, if wildcards exist, S could be max(fixed elements) or similar values. In practice, checking all A_i + B_j pairs (O(N²) candidates) is sufficient because if a solution exists, there must be at least one fixed-fixed pair that determines S, or if one side is all wildcards, S is determined by the other side's max.
- For each candidate S, we need to check if a perfect matching exists between A and B where edge (i,j) exists if (A_i == -1 or A_i ≤ S) and (B_j == -1 or B_j ≤ S) and (A_i == -1 or B_j == -1 or A_i + B_j == S). Actually, if both are fixed, we need A_i + B_j == S. If one is wildcard, we need the fixed one ≤ S.
- This is a bipartite matching problem. N ≤ 2000, so O(N³) matching for each of O(N²) candidates is too slow (O(N⁵)). We need a smarter approach.

Better approach: For a fixed S, count how many elements in A are > S (call it a_bad) and how many in B are > S (b_bad). If a_bad > 0 or b_bad > 0, this S is impossible. Otherwise, all fixed elements are ≤ S. Let a_wild be the number of -1s in A, b_wild in B. Let a_fixed = N - a_wild, b_fixed = N - b_wild.
We need to match fixed A values with fixed B values where A_i + B_j == S. The remaining unmatched fixed elements must be matched with wildcards on the other side. Specifically:
- Let match_fixed be the maximum number of pairs (i,j) where A_i and B_j are both fixed and A_i + B_j == S. This is a bipartite matching on the fixed elements with equality constraint.
- After matching match_fixed pairs, we have (a_fixed - match_fixed) fixed A elements left and (b_fixed - match_fixed) fixed B elements left.
- These must be matched with wildcards: we need (a_fixed - match_fixed) ≤ b_wild and (b_fixed - match_fixed) ≤ a_wild.
- The total wildcards must cover the remaining slots: a_wild + b_wild ≥ (a_fixed - match_fixed) + (b_fixed - match_fixed), but this is automatically satisfied if the individual conditions hold because total slots are N.
Actually, the condition is: we can match all fixed A elements either to fixed B elements (with sum S) or to wildcard B elements. Similarly for fixed B elements. This is equivalent to: max matching in the bipartite graph where left side is fixed A, right side is fixed B, edge if A_i + B_j == S. Let M be the size of max matching. Then we need (a_fixed - M) ≤ b_wild and (b_fixed - M) ≤ a_wild.

To compute M efficiently for each S: we can use a greedy approach if we sort the fixed elements. For two sequences to be matched with sum S, we can use a two-pointer approach on sorted fixed A and sorted fixed B (where B is transformed to S - B). However, since we have duplicate values, we need to be careful. We can sort fixed A values and fixed B values. Then for each value in A, we need to find S - A_i in B. This is equivalent to checking if the multiset of fixed A can be matched with the multiset of fixed B such that pairs sum to S. We can use a greedy approach with two multisets or sort and use two pointers.

Wait, for each candidate S, we can compute the maximum matching in O(N log N) using sorting and two pointers if we process values in order. Specifically, sort fixed A ascending, sort fixed B ascending. Then try to match smallest A with largest B such that sum ≤ S? No, we need exact sum S. We can use a hash map or frequency array for B values, then for each A value, check if S - A_i exists in B. But this gives a greedy matching that might not be maximum if there are conflicts. However, for the equality constraint on a line, the greedy approach of matching smallest available works if we process in sorted order. Actually, this is a bipartite graph where edges connect A_i to B_j if A_i + B_j == S. This is a "convex" bipartite graph, and a greedy approach works: sort A ascending, sort B ascending. Use two pointers: for each A value from smallest to largest, try to find the smallest B value that equals S - A_i. If we process A in ascending order and B in ascending order, we can match greedily.

Actually, the standard approach: to check if we can match all fixed A with fixed B or wildcards, we can use Hall's theorem. The condition (a_fixed - M) ≤ b_wild and (b_fixed - M) ≤ a_wild must hold. M is the maximum matching. For this specific graph (interval bigraph), M can be computed greedily.

Simpler approach: For each candidate S, we can check feasibility in O(N log N) as follows:
1. Separate fixed and wildcards.
2. Check all fixed ≤ S.
3. Sort fixed A and fixed B.
4. Use a multiset (or frequency map) for B. Iterate through A in any order, try to match with S - A_i. If found, decrement count. If not, this A needs a wildcard B.
5. Count how many A needed wildcards (need_b_wild) and how many B left unmatched (need_a_wild). Check if need_b_wild ≤ b_wild and need_a_wild ≤ a_wild.

But does greedy matching give the correct maximum? If we process A in ascending order and always match with the smallest available B that equals S - A_i, it's optimal because the graph is a chain graph. Actually, since each A_i connects to exactly one value S - A_i in B (if it exists), the graph is a collection of edges between specific value pairs. The maximum matching is simply: for each value v, min(count of A with value v, count of B with value S - v). Summing over all v gives the maximum matching! This is because the graph is a disjoint union of complete bipartite graphs between A values v and B values S - v. So we can compute M exactly using frequency maps.

So for each S:
- freqA = Counter of fixed A values
- freqB = Counter of fixed B values
- M = sum over v of min(freqA[v], freqB[S - v])
- need_b_wild = a_fixed - M
- need_a_wild = b_fixed - M
- Feasible if need_b_wild ≤ b_wild and need_a_wild ≤ a_wild.

Candidate S values: We need to consider S values that could be the target. If there is at least one fixed A and one fixed B, then S must be at least max(max fixed A, max fixed B). Also, if we match fixed A_i with fixed B_j, S = A_i + B_j. So candidates are all A_i + B_j for fixed A_i, B_j. That's O(N²) candidates. For each, we do O(N) work with frequency maps (or O(N log N) if we rebuild). Total O(N³) which is 8×10⁹ for N=2000 - too slow.

Optimization: We don't need to check all pairs. Note that S must be at least max_A and max_B (max of fixed values). Also, if we fix S, the matching depends on the frequency maps. We can use a smarter approach: sort fixed A and fixed B. For each fixed A value a, the matching with B values S - a changes as S changes. 

Alternative: iterate S over candidate values but compute M incrementally? Or use the fact that M = sum min(freqA[v], freqB[S-v]). This is like a cross-correlation. We can compute this for all possible S efficiently using FFT? N=2000, values up to 1e9, but N is small. O(N²) candidates with O(N) each is O(N³) = 8e9, too slow.

Wait, we can reduce candidates. The maximum matching M for a given S is limited by the number of fixed elements. We need M ≥ a_fixed - b_wild and M ≥ b_fixed - a_wild. So M ≥ max(a_fixed - b_wild, b_fixed - a_wild). Let min_M = max(a_fixed - b_wild, b_fixed - a_wild, 0). We need to find if there exists S such that M(S) ≥ min_M and all fixed ≤ S.

Since values are up to 1e9 but N is 2000, the number of distinct values is at most 2000. The number of distinct sums is O(N²) = 4e6. For each distinct sum, we can compute M(S) in O(N) using frequency maps. That's 4e6 × 2000 = 8e9, still too slow.

Better: For each S, M(S) = sum_v min(freqA[v], freqB[S-v]). If we sort the distinct values, we can use a two-pointer approach. Let's sort distinct A values and distinct B values. For each A value a, as S increases, S - a increases. We can think of it as convolution. But with N=2000, O(N² log N) might be acceptable if we are clever.

Actually, O(N²) candidates with O(N) each is 4e6 × 2000 = 8e9 operations, which is too slow in Python. We need a better approach.

Wait, we can use the following: for each pair (a, b) where a is fixed A and b is fixed B, S = a + b. But we don't need to check all. We can use a sliding window / two pointers on sorted arrays.

Let's sort fixed A values: a_1 ≤ a_2 ≤ ... ≤ a_k. Sort fixed B values: b_1 ≤ b_2 ≤ ... ≤ b_m. For a given S, we want to match a_i with b_j where a_i + b_j = S. This is equivalent to matching in a grid. The maximum matching can be computed greedily: for each a_i from largest to smallest, match with the largest available b_j such that a_i + b_j ≤ S? No, we need exact equality.

Alternative: since the graph is a disjoint union of bicliques between value groups, M(S) = sum over distinct a of min(cntA[a], cntB[S-a]). We can compute this by iterating over distinct a values and looking up cntB[S-a]. If we use a hash map for cntB, each lookup is O(1). So for each S, computing M(S) is O(distinct_A) = O(N). 

To reduce the number of candidate S values: note that we only need to check S values where the matching changes. The matching changes when S passes a value a + b for some fixed a, b. So all O(N²) sums are candidates. But maybe we can prune: S must be at least max(maxA, maxB). Also, S must be such that there are enough matches.

For N=2000, O(N²) = 4e6 candidates. In Python, 4e6 × O(1) average with hash maps might be borderline but possible if optimized (using arrays instead of dicts). But 4e6 × 2000 is too much.

Wait, we can compute M(S) for all S more efficiently. Let's use the frequency arrays. Since values can be up to 1e9, we compress coordinates. Let distinct sorted values of A be A_vals, of B be B_vals. For each a in A_vals with count ca, and each b in B_vals with count cb, the sum s = a + b contributes min(ca, cb) to M(s). But we can't just add min(ca, cb) because for a fixed s, multiple pairs (a, b) with a + b = s contribute min(cntA[a], cntB[b]) each, and M(s) is the sum of these mins. Wait, M(s) = sum_a min(cntA[a], cntB[s-a]). So for each a, we look up b = s - a. This is exactly the sum over a of min(cntA[a], cntB[s-a]). 

If we iterate over all pairs (a, b) and add min(cntA[a], cntB[b]) to M[a+b], that's O(N²) total to build M for all s! Because there are O(N²) pairs, and each pair contributes to exactly one sum s = a + b. Then for each s, M(s) is the sum of min(cntA[a], cntB[b]) over all pairs with a + b = s. But wait, is that correct? M(s) = sum_a min(cntA[a], cntB[s-a]). If we let b = s - a, then for each pair (a, b) with a + b = s, we add min(cntA[a], cntB[b]). Summing over all such pairs gives exactly M(s). Yes!

So we can compute M(s) for all possible s in O(N²) time total. Then we iterate over all distinct sums s (O(N²) of them), check if s ≥ max(maxA, maxB) (so all fixed ≤ s), and check if M(s) ≥ min_M. If any s satisfies, answer is Yes.

Wait, we also need to handle the case where there are no fixed A or no fixed B. If a_fixed = 0 (all A are wild), then we can set A to any values. We need all B ≤ S and we can set A_i = S - B_i. So any S ≥ max(B) works. Similarly if b_fixed = 0. If both are all wild, any S works (e.g., S = 0).

Also, edge case: what if there are fixed elements but no fixed-fixed pairs? E.g., A has fixed, B all wild. Then S must be ≥ max(A), and we can set B_i = S - A_i. So any S ≥ max(A) works. Our formula: a_fixed = N, b_fixed = 0, b_wild = N. min_M = max(a_fixed - b_wild, b_fixed - a_wild) = max(N - N, 0 - a_wild) = 0. M(s) = 0 for all s (since no fixed B). So we need s ≥ max(A). We should check this separately or ensure candidate generation includes s = max(A) when b_fixed = 0.

Similarly if a_fixed = 0, b_fixed > 0: need s ≥ max(B).

If both a_fixed > 0 and b_fixed > 0, candidates are sums a + b. But we also need to ensure s ≥ max(maxA, maxB). Since a + b ≥ maxA + minB ≥ maxA (if minB ≥ 0), and ≥ maxB (if minA ≥ 0), the sum of maxA and maxB might be needed? Actually, s = a + b for some fixed a, b. The maximum fixed A is some a_max, maximum fixed B is b_max. s must be ≥ a_max and ≥ b_max. The candidate s = a_max + b_max satisfies this. But maybe a smaller s like a_max + b_min works if b_min ≥ 0. Since b_min ≥ 0, a_max + b_min ≥ a_max. And we need s ≥ b_max too. If a_max + b_min < b_max, then s < b_max, invalid. So we need to check the condition s ≥ max(maxA, maxB) explicitly.

But do we need to consider s values that are not sums of fixed pairs? Suppose a_fixed > 0 and b_fixed > 0. Could the optimal s be larger than all pairwise sums? If s is larger, then M(s) might be 0 because no fixed pair sums to s. But we need M(s) ≥ min_M. If min_M = 0, then any s ≥ max(maxA, maxB) works. When is min_M = 0? When a_fixed ≤ b_wild and b_fixed ≤ a_wild. In that case, we can match all fixed A with wild B and all fixed B with wild A. So any s ≥ max(maxA, maxB) works. The smallest such s is max(maxA, maxB). Is this a candidate? If a_fixed > 0 and b_fixed > 0, maxA + minB ≥ maxA, but we need s ≥ maxB too. max(maxA, maxB) might not be a pairwise sum. E.g., A = [10], B = [1]. maxA = 10, maxB = 1. s = 10 works (match A wild? no, A is fixed). Wait, A = [10] fixed, B = [1] fixed. Then s must be 11. max(maxA, maxB) = 10, but we need s = 11. So pairwise sum covers it.

But if min_M = 0, e.g., A = [10, -1], B = [1, -1]. a_fixed = 1, b_fixed = 1, a_wild = 1, b_wild = 1. min_M = max(1-1, 1-1) = 0. So any s ≥ max(10, 1) = 10 works. s = 10: match fixed A=10 with wild B (set to 0), match fixed B=1 with wild A (set to 9). Sums: 10+0=10, 9+1=10. Yes! s = 10 is not a pairwise sum of fixed elements (only fixed pair is 10+1=11). So we need to consider s = max(maxA, maxB) as a candidate when min_M = 0.

Actually, more generally, we should consider s = max(maxA, maxB) as a candidate always. And also all pairwise sums. But if min_M = 0, s = max(maxA, maxB) works. If min_M > 0, then we need some fixed-fixed matches, so s must be at least the sum of some matched pair. The matched pairs sum to s, so s must be a pairwise sum of fixed elements. Thus, candidates are: max(maxA, maxB) and all pairwise sums a + b.

Wait, but if min_M > 0, we need M(s) ≥ min_M > 0, so there is at least one fixed pair (a, b) with a + b = s. So s is a pairwise sum. Good.

So candidate set: {max(maxA, maxB)} ∪ {a + b : a in fixedA, b in fixedB}. Size O(N²). For each candidate, we can look up M(s) from our precomputed table in O(1). Building the table is O(N²). So total O(N²) time, which is fine for N=2000 (4e6 operations).

But we need to be careful with coordinate compression and hash maps. In Python, using a dictionary for M(s) with O(N²) entries might be memory heavy but 4e6 entries is too much memory (each entry ~50 bytes, 200MB). We need a better approach.

Alternative: instead of building M(s) for all s, we can iterate over candidates and compute M(s) on the fly. But that's O(N) per candidate, O(N³) total.

Better: we can sort the candidates and use a two-pointer / sliding window approach. Let's think differently.

For each distinct value a in A with count ca, and each distinct value b in B with count cb, they contribute min(ca, cb) to M(a+b). We can iterate over all pairs of distinct values (a, b), compute s = a+b, and add min(ca, cb) to a dictionary M[s]. The number of distinct values is at most N each, so O(N²) pairs. For N=2000, that's 4e6 dictionary operations. In Python, this might be borderline but could work if optimized (using dict.get). 4e6 operations is actually fine (well under 1 second). The memory for the dictionary: number of distinct sums is at most (2N-1) if values are consecutive, but here values are up to 1e9, so distinct sums could be up to N² = 4e6 in the worst case (if all sums are distinct). Storing 4e6 integers in a dict is memory intensive (~300MB). Too much.

We need to reduce memory. We can use the fact that we only need to check candidates s where s ≥ max(maxA, maxB). Still could be many.

Alternative: process candidates in sorted order and compute M(s) incrementally. If we sort distinct A values and distinct B values, and iterate s in increasing order, the pairs (a, b) with a + b = s form anti-diagonals. We can use a two-pointer approach: for each a in sorted A values, as s increases, b = s - a increases. Hmm, not straightforward.

Another approach: since N=2000, O(N²) time with O(N) memory is possible if we avoid storing all sums. We can generate candidates on the fly and compute M(s) using a smarter method.

Wait, we can compute M(s) for a given s in O(N) using frequency arrays. If we have O(N²) candidates, that's O(N³). But maybe we can reduce candidates: we only need to check s values that are "critical". The function M(s) changes only when s passes a pairwise sum. Between consecutive pairwise sums, M(s) is constant (actually 0 if no pair sums to s). So we only need to check pairwise sums and max(maxA, maxB).

To avoid storing all sums, we can iterate over distinct a values, and for each a, iterate over distinct b values, compute s = a+b, and check the condition. But we need M(s), which requires summing min(ca, cb) over all pairs with the same s. If we process pairs grouped by s, we need to know M(s). 

Alternative: for each s candidate, compute M(s) on the fly but cache results. Since we might revisit the same s multiple times (from different pairs), caching helps. But worst case distinct sums is O(N²).

Hmm, let's think about the actual complexity. In Python, 4e6 dictionary insertions/updates is feasible (maybe 2-3 seconds). Memory is the issue. But maybe the number of distinct sums is not that large in practice? With random values up to 1e9, sums are likely distinct, so ~4e6 distinct sums. That's too much memory.

We need a different approach. Let's use sorting and two pointers to compute M(s) for all s without storing all of them.

Sort distinct A values with counts: (a_1, ca_1), ..., (a_k, ca_k). Sort distinct B values: (b_1, cb_1), ..., (b_m, cb_m). For each pair (a_i, b_j), s = a_i + b_j. We want to group by s and sum min(ca_i, cb_j). This is like computing the sum of mins over anti-diagonals of a matrix.

We can iterate over s in increasing order. For a fixed s, the pairs (a_i, b_j) with a_i + b_j = s are those where b_j = s - a_i. If we iterate a_i in increasing order, b_j must be in B_vals. We can use a hash map from value to index for B_vals. Then for each s, we iterate over all a_i, check if s - a_i is in B_vals, and if so add min(ca_i, cb_j). This is O(k) per s, and there are O(k*m) distinct s, so O(k²m) total. Too slow.

Alternative: for each a_i, iterate over b_j, compute s, and add to a dictionary. This is O(k*m) time and O(distinct_s) memory. The issue is memory.

Can we check the condition without computing M(s) exactly? We need M(s) ≥ min_M. Since M(s) is a sum of non-negative terms, we can stop early if the sum reaches min_M. But we still need to group by s.

Maybe we can use a different algorithm altogether. Let's think about the structure.

We need to match fixed A and fixed B such that pairs sum to s, and the unmatched fixed elements are few enough to be covered by wildcards. This is equivalent to: there exists a matching of size at least min_M in the bipartite graph where edges are pairs summing to s.

Since the graph is a disjoint union of bicliques (by value), the max matching is sum of mins. We need this sum to be at least min_M.

Alternative formulation: we want to know if there exists s such that sum_a min(cntA[a], cntB[s-a]) ≥ min_M and s ≥ max(maxA, maxB).

Let's define f(s) = sum_a min(cntA[a], cntB[s-a]). This is the max matching. We want max over s of f(s) subject to s ≥ max(maxA, maxB), and check if that max is ≥ min_M. Actually, we just need existence.

Since cntA and cntB are frequency arrays (after compression), f(s) is like a "min-convolution". Computing this for all s is expensive.

But N=2000, so maybe O(N²) with a dictionary is acceptable if we use arrays instead of dicts. We can compress the sums: generate all pairwise sums, sort them, and for each distinct sum compute f(s). But generating all sums is O(N²) memory again.

Wait, we can use numpy? Probably not allowed. Let's think in pure Python.

Actually, 4e6 entries in a dictionary: each entry key (int) + value (int) in Python dict uses about 72 bytes + int objects. But small ints are cached, and sums up to 2e9 are not cached. Each int object ~28 bytes. So each entry ~100 bytes. 4e6 entries = 400MB. Too much.

We need to avoid storing all sums. Let's use a different strategy: iterate over a in A_vals, and for each a, iterate over b in B_vals, but process in a way that groups by s without storing all.

Alternative: use the fact that we only need to check if f(s) ≥ min_M. For a fixed s, f(s) = sum_a min(cntA[a], cntB[s-a]). We can compute this in O(k) where k = number of distinct A values. If we have O(N²) candidates, that's O(N³). But maybe we can prune candidates: we only need to check s values that are pairwise sums and s ≥ max(maxA, maxB). The number of such s could still be O(N²).

Hmm, let's reconsider. Maybe we can use a meet-in-the-middle or FFT approach. f(s) = sum_a min(cntA[a], cntB[s-a]). The min function makes it non-linear, hard for FFT.

Let's think about the problem constraints again. N ≤ 2000. O(N² log N) is fine. O(N²) with small constant is fine. O(N²) memory is not fine (4e6 ints = 32MB if using array('l') or list of ints? A list of 4e6 ints in Python is ~32MB for the pointers + int objects. Actually, a list of ints where ints are small (< 2^30) uses cached ints? No, Python caches small ints -5 to 256. Larger ints are separate objects. A list of 4e6 large ints: list has 4e6 pointers (32MB on 64-bit), each int object ~28 bytes (112MB). Total ~144MB. Might be borderline but possibly acceptable if memory limit is high (e.g., 512MB). But we also need the dictionary for counts.

Alternative: use sorted list of sums and binary search. Generate all pairwise sums into a list (O(N²) memory), sort it (O(N² log N)), then for each distinct sum, compute f(s) by iterating over A_vals and looking up B_vals. That's O(N²) memory for the sums list, plus O(N) per distinct sum. If distinct sums = O(N²), total time O(N³). Too slow.

We need to compute f(s) for all distinct s in O(N²) total time and O(N) memory (or O(N²) memory but with small constant).

Idea: iterate over pairs (a, b) and accumulate f(s) in a dictionary, but use `collections.defaultdict(int)`. To reduce memory, we can use the fact that we only care about s ≥ max(maxA, maxB). Still could be many.

Alternative idea: since we only need the maximum of f(s), and f(s) is a sum of mins, maybe we can binary search on the answer? No, it's a decision problem.

Let's think about the structure of f(s). For each a, the function g_a(s) = min(cntA[a], cntB[s-a]) is a "tent" function: it's cntA[a] when cntB[s-a] ≥ cntA[a], else cntB[s-a]. As s varies, s-a varies over all values, so g_a(s) depends on cntB at s-a.

If we iterate s over all pairwise sums in sorted order, we can update f(s) incrementally? When s increases by 1, s-a increases by 1 for all a, so cntB[s-a] changes to the next value. But values are not consecutive, so this doesn't work directly.

Alternative: use a hash map for f(s) but limit the number of entries by only considering s that are pairwise sums and ≥ threshold. In the worst case, this is still O(N²). But maybe with N=2000, O(N²) = 4e6 dictionary entries is acceptable if we use a more memory-efficient structure.

Actually, in Python, we can use `dict` with int keys and values. Let's estimate more carefully. A Python dict entry uses a hash table slot. For a dict with 4e6 entries, the table size is ~8e6 (load factor 2/3). Each slot is 8 bytes (pointer) in the table, plus the entry object. Actually, Python dicts store entries in a compact array since 3.6. Each entry is 24 bytes (hash, key pointer, value pointer) plus the key and value objects. For int keys and values, small ints are cached only up to 256. Sums up to 2e9 are not cached, so each key is a distinct int object (~28 bytes), each value is an int object (~28 bytes, but values up to N=2000 might be cached if < 257? No, only -5 to 256 are cached. Values up to 2000 are not cached). So each entry: 24 (entry) + 28 (key) + 28 (value) = 80 bytes, plus table overhead ~8 bytes. Total ~88 bytes per entry. 4e6 entries = 352MB. Too much.

We need a better approach. Let's avoid storing f(s) for all s.

Key insight: we don't need to check all pairwise sums. We only need to find one s with f(s) ≥ min_M. We can iterate over candidates in a smart order and stop early. But worst case we might check many.

Alternative: use a two-pointer approach on sorted A_vals and B_vals. For each a in A_vals (sorted), the values b = s - a must be in B_vals. As s increases, b increases. Hmm.

Let's think about it as a matching problem directly. We want to match as many fixed A with fixed B as possible such that matched pairs have the same sum s. This is equivalent to: choose s, then match A values with B values where a + b = s. The matching is limited by the minimum count for each complementary pair.

We can think of it as: for each s, the matching size is sum over a of min(cntA[a], cntB[s-a]). We want this to be large.

Alternative approach: iterate over the matching directly. Suppose we match pairs (a_1, b_1), (a_2, b_2), ... with a_i + b_i = s. Then all matched pairs have the same sum. So we are looking for a large "matching" in the multiset union where all edges have the same sum.

This is equivalent to finding the largest subset of fixed elements that can be partitioned into pairs with equal sum, plus possibly using wildcards for the rest.

Hmm, let's think about the maximum matching over all s. We want max_s f(s). This is the maximum number of fixed-fixed pairs with equal sum. Let's call this M_max. Then the answer is Yes iff M_max ≥ min_M (and we can choose s ≥ max(maxA, maxB); but if M_max is achieved at s < max(maxA, maxB), we need to check other s).

Wait, we also need s ≥ max(maxA, maxB). But if s < maxA, then some fixed A > s, which is impossible because A_i + B_j = s and B_j ≥ 0 implies A_i ≤ s. So s must be ≥ all fixed values. Thus s ≥ max(maxA, maxB). So we need f(s) ≥ min_M for some s ≥ max(maxA, maxB).

Now, f(s) for s ≥ max(maxA, maxB): we want to know if any such s has f(s) ≥ min_M.

To compute max f(s) efficiently: note that f(s) = sum_a min(cntA[a], cntB[s-a]). Let's iterate over all pairs (a, b) and add min(cntA[a], cntB[b]) to f(a+b). To avoid memory issues, we can use a different data structure.

Since N=2000, the number of distinct values in A and B is at most 2000 each. The number of pairs is at most 4e6. We can afford O(N²) time. For memory, we can use a hash map but with a twist: process pairs and only keep track of the maximum f(s) seen so far, but we need to accumulate counts per s.

Alternative: use `collections.Counter` but clear it periodically? No.

Wait, maybe we can use the fact that values are integers and use a dictionary but with a limited key space. The sums range from minA+minB to maxA+maxB, which could be up to 2e9. Too large for an array.

Hmm, let's reconsider the memory. 4e6 distinct sums is the worst case, but is it achievable? If A has 2000 distinct values and B has 2000 distinct values, the number of distinct sums can be up to 4e6 (e.g., if values are chosen to avoid collisions, like Sidon sets). But constructing such sets with values up to 1e9 is possible. So worst case is real.

We need an algorithm with O(N²) time and O(N) memory, or O(N² log N) time and O(N) memory.

Idea: For each a in A_vals, iterate over b in B_vals, compute s = a+b, and store in a list of (s, min_count). Then sort this list and aggregate. But the list has O(N²) entries, memory issue again.

Alternative: process in blocks. Divide A_vals into blocks of size B_size. For each block, compute pairwise sums with all B_vals, aggregate in a dict, find max, then clear. But f(s) needs contributions from all a, so we can't clear until we've processed all a for a given s. If we process a in blocks, we need to keep f(s) across blocks. Memory still O(distinct_s).

Alternative: use external memory / sorting. Generate all (s, min_count) pairs, sort them externally, aggregate. In Python, we can use a list of tuples, but memory is O(N²). 4e6 tuples, each tuple ~56 bytes + ints, ~200MB. Too much.

Let's think differently. Maybe we don't need to compute f(s) for all s. We can use a greedy / constructive approach.

We want to match fixed A and B with equal sums. Let's sort fixed A and fixed B. For a given s, the matching is straightforward. To find a good s, we can consider that the matching pairs (a, b) with a + b = s. If we sort A ascending and B descending, then pairs (A_i, B_i) have sums that vary. We want many pairs with the same sum.

Alternative: this is equivalent to finding the largest k such that there exist indices i_1 < ... < i_k and j_1 < ... < j_k with A_{i_l} + B_{j_l} = s for all l. Since we can choose any pairs, it's about multisets.

Let's think about the complementary counts. For each value v, let ca[v] = count in A, cb[v] = count in B. For sum s, the contribution is min(ca[v], cb[s-v]). We want to maximize the total.

This is similar to the problem of finding the maximum overlap between two histograms under reflection and translation. Specifically, reflect B's histogram (cb[-v]) and convolve with ca using min instead of multiplication.

With N=2000, maybe an O(N²) algorithm with a dictionary is intended, and the memory limit is generous (e.g., 1024MB). AtCoder problems (this looks like AtCoder) typically have 256MB or 512MB memory limit. 4e6 dict entries might be too much for 256MB but okay for 512MB? Let's estimate again: Python dict with 4e6 entries. Actually, the number of distinct sums might be less in practice. But worst case...

Wait, maybe we can use a smarter representation. Since we only need f(s) ≥ min_M, and min_M ≤ N, we can cap the values at min_M. But that doesn't reduce the number of keys.

Alternative: use `array` or `list` for sums if we compress. We can generate all pairwise sums, sort them, and use run-length encoding. But generating them requires O(N²) memory.

Hmm, let's think about the time limit. AtCoder typical time limit is 2 seconds. O(N²) = 4e6 operations in Python is fine. O(N² log N) = 4e6 × 22 = 88e6 might be too slow. So we want O(N²) with small constant.

Memory-efficient O(N²) algorithm: iterate over a in A_vals, and for each a, iterate over b in B_vals, compute s = a+b, and update a dictionary f[s] += min(ca, cb). To reduce memory, we can use the fact that we only need to check s ≥ max(maxA, maxB). But still O(N²) distinct s.

Wait, maybe we can use a different approach: instead of computing f(s) for all s, we can check the condition directly using a matching algorithm for each candidate s, but limit candidates.

Actually, let's reconsider: do we need to check all pairwise sums? The condition is f(s) ≥ min_M. f(s) is maximized when many complementary pairs align. The maximum of f(s) over all s is what we need. Let's denote M_max = max_s f(s). If M_max < min_M, answer is No. If M_max ≥ min_M, we need to ensure the s achieving it (or some s with f(s) ≥ min_M) is ≥ max(maxA, maxB). But if f(s) ≥ min_M > 0, then s is a sum of at least one fixed pair, and s ≥ maxA? Not necessarily: s = a + b where a ≤ maxA, b ≤ maxB. s could be less than maxA if a < maxA and b < 0? No, b ≥ 0, so s = a + b ≥ a. If a = maxA, then s ≥ maxA. But the pair achieving f(s) might not include maxA. E.g., A = [5, 1], B = [1, 1]. maxA = 5. f(2) = min(cntA[1], cntB[1]) = 1 (pair 1+1=2). s = 2 < maxA = 5. But s = 2 is invalid because fixed A = 5 > 2. So we need s ≥ maxA and s ≥ maxB.

So we need f(s) ≥ min_M for some s ≥ max(maxA, maxB). Let's call this threshold T = max(maxA, maxB).

Now, f(s) for s ≥ T. We want max over s ≥ T of f(s). Let's compute this max efficiently.

Observation: f(s) = sum_a min(ca[a], cb[s-a]). For s ≥ T ≥ maxA, s - a ≥ T - a ≥ 0. Not particularly helpful.

Let's think about the algorithm used in similar AtCoder problems. This looks like ABC/ARC problem. The intended solution is likely O(N²) with a hash map, and N=2000 means 4e6 entries, which might be acceptable in C++ but not Python. Since we're writing Python, we need to be careful.

Wait, maybe the number of distinct sums is manageable because we only consider sums ≥ T. Still worst case O(N²).

Alternative: use `collections.defaultdict(int)` and hope memory is enough. Let's estimate for N=2000: distinct values in A ≤ 2000, in B ≤ 2000. Pairs = 4e6. If we use a dict, worst case 4e6 entries. In Python, this might use ~400MB. If memory limit is 512MB, it might pass but risky.

We can reduce memory by using a two-pass approach: first pass, generate all sums and find the distinct ones (using a set, same memory issue). Not helpful.

Alternative: use sorting. Generate all pairwise sums into a list (4e6 ints). A list of 4e6 ints: the list itself is 32MB (8 bytes per pointer), and each int object... but if we generate sums, many might be small? No, sums up to 2e9. Each int object ~28 bytes. So 4e6 × (8 + 28) = 144MB. Then sort (Timsort, O(N² log N) time, O(N²) memory for temporary). Then aggregate: iterate sorted sums, for each distinct s, sum the min_counts. But we also need the min_counts, so we'd store tuples (s, min_count), more memory.

Alternatively, we can avoid storing min_counts by recomputing. Sort the sums, then for each distinct s, compute f(s) by iterating over A_vals and looking up cb[s-a]. That's O(N) per distinct s, O(N³) total. Too slow.

Hmm. Let's think about a different algorithm.

We want max_{s ≥ T} sum_a min(ca[a], cb[s-a]). Let's define for each a, the set of s where cb[s-a] > 0, i.e., s = a + b for b in B_vals. For each such s, the contribution is min(ca[a], cb[b]).

We can iterate over a in A_vals in decreasing order of ca[a] (or some order), and maintain a running max. But we still need to aggregate per s.

Idea: use a hash map but only store f(s) for s that have a chance to be large. Since we need f(s) ≥ min_M, and each pair contributes at most min(ca, cb), we can prune. But worst case still many.

Alternative: since min_M ≤ N = 2000, we can cap f(s) at min_M. Once f(s) reaches min_M, we can mark s as good. But we still need to store f(s) for all s until they reach min_M.

Wait, we can use a different strategy: iterate over pairs (a, b), and for each, check if s = a+b ≥ T. If so, we want to know if f(s) ≥ min_M. Instead of computing f(s) exactly, we can compute a lower bound and upper bound. Not straightforward.

Let's reconsider the problem. Maybe there's a simpler characterization.

We need to assign values to wildcards and permute A so that all A_i + B_i are equal. Since A can be permuted, we can think of it as: we have a multiset A (with wildcards) and a sequence B (with wildcards, but B is not permuted). Wait, B is not permuted! Only A is rearranged. But since we're matching A elements to B positions, and A can be permuted arbitrarily, we can match any A element to any B position. So B's order doesn't matter either; we just need to match multisets.

So the problem is: given multiset A with a_wild wildcards and multiset B with b_wild wildcards, can we replace wildcards and match elements such that all pairs sum to s?

Yes, our formulation is correct.

Now, the condition is: there exists s such that all fixed ≤ s, and f(s) ≥ min_M where min_M = max(a_fixed - b_wild, b_fixed - a_wild, 0).

Wait, let's re-derive. We have a_fixed fixed A, a_wild wild A, b_fixed fixed B, b_wild wild B. Total N each, so a_fixed + a_wild = N, b_fixed + b_wild = N.

We match fixed A to fixed B with sum s: M = f(s) pairs. Remaining fixed A: a_fixed - M, must match with wild B: need a_fixed - M ≤ b_wild. Remaining fixed B: b_fixed - M, must match with wild A: need b_fixed - M ≤ a_wild. Wild A and wild B can match with each other freely.

So conditions: M ≥ a_fixed - b_wild and M ≥ b_fixed - a_wild. So M ≥ max(a_fixed - b_wild, b_fixed - a_wild). Also M ≥ 0. So min_M = max(a_fixed - b_wild, b_fixed - a_wild, 0). Correct.

Now, a_fixed - b_wild = a_fixed - (N - b_fixed) = a_fixed + b_fixed - N. Similarly b_fixed - a_wild = a_fixed + b_fixed - N. So both are equal to a_fixed + b_fixed - N! Because a_wild = N - a_fixed, b_wild = N - b_fixed.

So min_M = max(a_fixed + b_fixed - N, 0). Let's call this K. We need f(s) ≥ K for some s ≥ T.

This simplifies things! K = max(a_fixed + b_fixed - N, 0). If K = 0, we just need any s ≥ T (i.e., s = T works, since we can match all fixed with wildcards). If K > 0, we need at least K fixed-fixed pairs with sum s.

So the problem reduces to: is there s ≥ T such that at least K fixed-fixed pairs (a, b) have a + b = s? Where pairs are counted with multiplicity: f(s) = sum_a min(ca[a], cb[s-a]) ≥ K.

Now, K ≤ N. We need to find if any s has f(s) ≥ K.

This is still the same computational problem, but now we have a clearer target.

Algorithm: compute f(s) for all s ≥ T, check if any ≥ K. To compute f(s) efficiently, we can use the pairwise aggregation.

Given the constraints, let's just use a dictionary and hope it fits. But to be safe, let's optimize memory.

Optimization: instead of storing f(s) for all s, we can early-terminate. We iterate over pairs (a, b) with a + b ≥ T, and add min(ca[a], cb[b]) to f[a+b]. If at any point f[s] ≥ K for some s, we can return Yes immediately (after checking s ≥ T). But we need to make sure we don't return Yes prematurely based on partial f(s). Since contributions are non-negative, if f(s) ≥ K at any point, the final f(s) ≥ K. So we can return Yes as soon as any f(s) reaches K (and s ≥ T). This can save time but not memory (in the worst case, we process all pairs and no s reaches K).

For memory, in the worst case (answer No), we store all distinct sums. If K > N/2 or so, maybe fewer pairs needed? Not necessarily.

Let's estimate memory more carefully for the worst case. Suppose A and B each have 2000 distinct values, all sums distinct. Then dict has 4e6 entries. Each entry: key int (28 bytes), value int (28 bytes, but values < 257 are cached? Python caches -5 to 256. If K ≤ 2000, values can exceed 256, so not cached). Dict entry overhead: in CPython 3.8+, dict uses a combined table. For a dict with n entries, the table has ~n/0.66 slots, each slot is 8 bytes (index) in the hash table plus the entries array. The entries array has n entries, each 24 bytes (hash, key, value as pointers). Plus key and value objects. So per entry: 24 (entry) + 8 (hash table slot, amortized) + 28 (key) + 28 (value) = 88 bytes. For 4e6 entries: 352MB. Plus the int objects for keys: actually, the key ints are created when we compute a+b. If we create 4e6 distinct ints, they are stored in the dict. The value ints: many are small (min counts), but counts can be up to 2000. Values 0-256 are cached, 257-2000 are not. So value ints are also allocated.

352MB is likely too much for a 256MB limit but might pass 512MB or 1024MB. AtCoder typical is 256MB for Python? Actually, AtCoder gives 256MB for most problems, but Python might get more. This is risky.

Let's think of a memory-efficient approach.

Approach: use sorting with O(N²) time but O(N) memory by processing in a streaming fashion.

We can iterate over a in A_vals. For each a, we compute the list of (a+b, min(ca[a], cb[b])) for b in B_vals. If we process a values one by one, we need to aggregate across a values. 

Alternative: use a hash map from s to f(s), but limit the size by using the fact that we only need s ≥ T and f(s) ≥ K. We can use a "counter" that only tracks s values that have appeared. Still O(distinct s).

Hmm, what if we use numpy? With numpy, we can use arrays and vectorized operations. But sums up to 2e9, can't use direct indexing. We could use `np.unique` on pairwise sums, but that's O(N²) memory (4e6 int64 = 32MB, fine!). Then for each unique sum, compute f(s) using vectorized operations? f(s) = sum_a min(ca[a], cb[s-a]). With numpy, we can broadcast: for each s, compute s - A_vals, look up in B_vals (using searchsorted), get cb values, compute min with ca, sum. That's O(N) per s, O(N³) total. Too slow.

But with numpy, we can compute the full convolution-like thing? The min operation prevents FFT.

Alternative numpy approach: create a matrix M[i, j] = min(ca[i], cb[j]) if A_vals[i] + B_vals[j] >= T else 0. Then we want to sum M over anti-diagonals and find the max anti-diagonal sum. This is O(N²) memory (4e6 int64 = 32MB) and O(N²) time to fill. Then summing over anti-diagonals: for each anti-diagonal, sum the entries. We can do this by iterating over i and j and accumulating into a dict, or by using numpy's diagonal summation after rotating. Actually, anti-diagonal sums can be computed by flipping one axis and using np.add.reduceat or by iterating.

With numpy, we can compute anti-diagonal sums efficiently: create the matrix M (N_A × N_B), then for each anti-diagonal index d = i + j (after appropriate offset), sum M[i, j] where i + j = d. But the sum s = A_vals[i] + B_vals[j] is not simply i + j unless values are consecutive. So anti-diagonals in the (i, j) index space don't correspond to constant s. We need to group by s = A_vals[i] + B_vals[j].

We can compute all pairwise sums S[i, j] = A_vals[i] + B_vals[j] (O(N²) memory, 32MB), and values V[i, j] = min(ca[i], cb[j]) (O(N²) memory, 32MB). Then use np.unique(S, return_inverse=True) to group, and np.bincount(inverse, weights=V) to get f(s) for each unique s. This is O(N²) time and O(N²) memory (S and V arrays, 64MB total, plus unique output). This is feasible memory-wise (64MB for the arrays, plus unique sums up to 32MB, plus inverse 32MB, total ~128MB). Time: O(N²) for broadcasting, O(N² log N) for unique (sorting). For N=2000, N² = 4e6, sorting 4e6 int64 with numpy is fast (~0.5s). bincount is fast. This could work!

But do we have numpy? AtCoder allows numpy in Python. The problem says "python program", doesn't specify. AtCoder's Python includes numpy. Let's assume numpy is available. But to be safe, maybe we should write pure Python.

Actually, let's reconsider pure Python with dict. The memory estimate of 352MB is worst case. In practice, for N=2000, the number of distinct sums might be less. But adversarial input could make it 4e6. However, AtCoder test cases are usually not adversarial against hash maps (they're designed for the intended solution). The intended solution in C++ uses unordered_map or map with O(N²) entries, which in C++ uses ~4e6 × 16 bytes = 64MB (for unordered_map with int64 key and int value, plus overhead, maybe 100-200MB). Hmm, even C++ might struggle with 4e6 unordered_map entries. So maybe the intended solution is different.

Wait, maybe the intended solution uses a map from sum to count, but with N=2000, O(N²) = 4e6 is fine in C++ with unordered_map (reserve). In Python, it's riskier.

Let me reconsider: maybe we don't need to consider all pairwise sums. Let's think about which s can achieve f(s) ≥ K.

f(s) = sum_a min(ca[a], cb[s-a]). For f(s) ≥ K, we need enough complementary pairs. The maximum f(s) is achieved when the histograms align well after reflection.

Alternative: think of it as a transportation problem. Not helpful.

Let's just go with the dict approach in pure Python, but optimize:
- Use local variables for speed.
- Use dict.get with default.
- Early termination when f(s) ≥ K.
- Only consider s ≥ T.

For memory, we can try to reduce by using a single dict and capping values at K (since we only care if f(s) ≥ K). Once f(s) reaches K, we return Yes. So values in the dict are at most K-1 (≤ 1999), which are cached ints? Python caches -5 to 256 only. So values 257-1999 are not cached. But we can store them as small ints; each is a distinct object only if > 256. Hmm.

Actually, we can avoid storing value int objects by using the fact that dict values are pointers to int objects. When we do f[s] = f.get(s, 0) + v, the new value is a new int object. Over time, many int objects are created but old ones are freed. The dict holds one value int per key. So memory is dominated by keys (distinct sums) and the dict structure.

Let's estimate keys: distinct sums ≥ T. Worst case 4e6. Dict with 4e6 keys: the keys are int objects (28 bytes each), dict entries (24 bytes each) + hash table (8 bytes per slot, ~6e6 slots = 48MB). Total: 4e6 × (28 + 24) + 48e6 = 208e6 + 48e6 = 256MB. Plus value ints: if values are small (< 257), they're cached (no extra memory). If we cap at K and K ≤ 2000, values up to 256 are cached, values 257-1999 are new ints (28 bytes each). But once f(s) ≥ K we return, so values are at most K-1 ≤ 1999. If K ≤ 256, all values cached. If K > 256, some values not cached. Worst case K = 2000, values up to 1999, each distinct value int is shared? No, each dict value is a separate int object unless interned. Python doesn't intern large ints. So each dict value is a distinct int object (28 bytes). So add 4e6 × 28 = 112MB. Total ~368MB. Too much.

To avoid value int objects, we can cap values at min(K, 256)? No, we need to know when f(s) reaches K. If K > 256, we need to count up to K. But we can store values as bytes? Not in a dict.

Alternative: since we return as soon as f(s) ≥ K, and K ≤ N = 2000, maybe the number of distinct s with f(s) < K is limited? No, adversarial input can have many s with f(s) = K-1.

Hmm. Let's think about whether the worst case is realistic. For f(s) to be computed, we iterate over distinct value pairs. The number of distinct sums is at most N_A × N_B where N_A, N_B are distinct counts. If N_A = N_B = 2000, distinct sums up to 4e6. But for the answer to be No, we need f(s) < K for all s. K = a_fixed + b_fixed - N. If all elements are fixed (no wildcards), K = N + N - N = N = 2000. Then we need f(s) ≥ 2000, i.e., all elements matched with the same sum. f(s) ≤ N always. So we need f(s) = N for some s. This means the multiset A equals the multiset {s - b : b in B}. Equivalently, sorted A and sorted (s - B) match. For random distinct values, f(s) is small for most s, and the number of distinct sums is large. So worst case memory is a real concern for the No case with all fixed.

But wait, if all elements are fixed and distinct, f(s) for a given s is the number of a such that s - a is in B. For random values, this is 0 or 1 for most s. The number of s with f(s) ≥ 1 is the number of pairs (a, b) with a + b = s, which is at most 4e6 but with distinct sums, each s has f(s) = 1 (if one pair) or more. So the dict would have ~4e6 entries with value 1. Memory ~256MB (keys + entries, values are cached int 1). Actually, value 1 is cached! So no extra memory for values. So ~256MB. Still too much for 256MB limit.

We need a better approach. Let's use the numpy approach or find an O(N²) time / O(N) memory algorithm.

O(N²) time / O(N) memory algorithm:

We want to compute max over s ≥ T of f(s), where f(s) = sum_a min(ca[a], cb[s-a]).

Let's sort A_vals and B_vals. For each pair (a, b), s = a + b. We want to group by s. 

Idea: for each a, the values s = a + b for b in B_vals are just B_vals shifted by a. So the multiset of sums is the union over a of (a + B_vals). We want to find the sum s that maximizes the total min-count.

We can use a sweep line: sort all pairs (s, ...) but that's O(N²) memory.

Alternative: use a hash map but with a limited key space by processing in blocks and using the fact that we only need the max. Hmm.

Wait, here's an idea: iterate over a in A_vals. Maintain a global dict f. For each a, iterate over b in B_vals, s = a + b, f[s] += min(ca[a], cb[b]). To save memory, after processing all a, we have the full f. No savings.

Alternative: use `collections.Counter` and update with a dict comprehension? Same memory.

Let's think about the numpy approach more concretely, and also consider that maybe pure Python dict is acceptable if we're careful.

Actually, let's reconsider the memory. In CPython, a dict with n entries uses:
- A hash table of size m (power of 2, m > n / (2/3)), each slot is 1 byte for small dicts? No. Since Python 3.6, dicts use a compact representation: an array of indices (hash table) and an array of entries. The indices array uses 1, 2, 4, or 8 bytes per slot depending on size. For n = 4e6, the entries array has ~4e6 entries × 24 bytes = 96MB. The indices array has ~8e6 slots × 4 bytes = 32MB (since 4e6 < 2^24, uses 4-byte indices? Actually, for n up to 2^7 use 1 byte, 2^15 use 2 bytes, 2^31 use 4 bytes). So indices ~8e6 × 4 = 32MB. Entries: each entry is 24 bytes (me_hash, me_key, me_value). 4e6 × 24 = 96MB. Keys: 4e6 int objects × 28 bytes = 112MB. Values: if all values are the same small int (e.g., 1), they're cached, no extra. But values vary; however, Python caches ints -5 to 256. If values are ≤ 256, cached. In the all-fixed distinct case, f(s) values are small (0, 1, 2, ...), mostly ≤ a few. So cached. Total: 96 + 32 + 112 = 240MB. Plus the input arrays and other overhead. This is right at the 256MB limit, likely to MLE.

So pure Python dict is too risky. Let's use numpy.

Numpy approach:
1. Read input.
2. Separate fixed and wildcards in A and B.
3. Compute a_fixed, b_fixed, a_wild, b_wild, K = max(a_fixed + b_fixed - N, 0), T = max(max fixed A, max fixed B) (handle empty cases).
4. If K == 0: check if we can choose s ≥ T. If a_fixed == 0 and b_fixed == 0, Yes. Else, s = T works (all fixed ≤ T, match with wildcards). So Yes. Wait, need to confirm: if K == 0, then a_fixed ≤ b_wild and b_fixed ≤ a_wild. So all fixed A can be matched to wild B (set B_wild = s - A_fixed ≥ 0 since s ≥ T ≥ A_fixed), and all fixed B matched to wild A. So Yes for any s ≥ T. So if K == 0, answer is Yes (as long as we can pick s ≥ T, which we can, e.g., s = T). Actually, we also need s such that wildcards assigned are non-negative. s ≥ T ≥ all fixed, so s - fixed ≥ 0. Good. So K == 0 → Yes.

Wait, but what if a_fixed = 0 and b_fixed = 0? Then all wild, Yes. If a_fixed = 0, b_fixed > 0: K = max(0 + b_fixed - N, 0) = max(b_fixed - N, 0) = 0 (since b_fixed ≤ N). So K = 0, Yes. Indeed, set A wild to s - B_fixed, need s ≥ max B. Yes.

So K == 0 always → Yes? Let's double check with sample 3: N=3, A = [1, 2, -1], B = [1, 2, 4]. a_fixed = 2 (1, 2), a_wild = 1. b_fixed = 3 (1, 2, 4), b_wild = 0. K = max(2 + 3 - 3, 0) = 2. So K = 2. We need f(s) ≥ 2 for some s ≥ T = max(2, 4) = 4. f(s) = sum_a min(ca[a], cb[s-a]). Fixed A values: {1:1, 2:1}. Fixed B: {1:1, 2:1, 4:1}. For s = 4: min(ca[1], cb[3]) + min(ca[2], cb[2]) = 0 + min(1, 1) = 1. f(4) = 1 < 2. s = 5: min(ca[1], cb[4]) + min(ca[2], cb[3]) = 1 + 0 = 1. s = 6: min(ca[2], cb[4]) = 1. s = 3: min(ca[1], cb[2]) + min(ca[2], cb[1]) = 1 + 1 = 2, but s = 3 < T = 4 (fixed B = 4 > 3). So invalid. Max f(s) for s ≥ 4 is 1 < 2. Answer No. Matches sample.

Sample 2: N=3, A = [1,2,3], B=[1,2,4]. a_fixed=3, b_fixed=3, K = max(3+3-3,0)=3. T = max(3,4)=4. Need f(s) ≥ 3 for s ≥ 4. f(s) ≤ 3. f(4): A {1,2,3}, B {1,2,4}. s=4: pairs (1,3)? 3 not in B. (2,2): yes. (3,1): yes. So f(4) = min(ca[2],cb[2]) + min(ca[3],cb[1]) = 1 + 1 = 2. Also min(ca[1], cb[3]) = 0. f(4)=2 <3. s=5: (1,4),(2,3 no),(3,2): min(ca[1],cb[4]) + min(ca[3],cb[2]) = 1+1=2. s=6: (2,4),(3,3 no): 1. s=7: (3,4):1. Max 2 < 3. No. Matches.

Sample 1: N=4, A=[2,0,-1,3], B=[3,-1,4,2]. a_fixed=3 (2,0,3), a_wild=1. b_fixed=3 (3,4,2), b_wild=1. K = max(3+3-4,0)=2. T = max(3,4)=4. Need f(s)≥2 for s≥4. Fixed A {2,0,3}, B {3,4,2}. s=4: (0,4),(2,2): min(ca[0],cb[4]) + min(ca[2],cb[2]) = 1+1=2. Also (3,1 no). f(4)=2 ≥2. s=4≥T=4. Yes. Matches.

Great, the formula works.

Now, K == 0 → Yes. Let's verify: K = max(a_fixed + b_fixed - N, 0). K = 0 iff a_fixed + b_fixed ≤ N. Since a_wild = N - a_fixed, b_wild = N - b_fixed, a_fixed ≤ b_wild iff a_fixed ≤ N - b_fixed iff a_fixed + b_fixed ≤ N. Yes. So K = 0 means enough wildcards to cover all fixed. Then any s ≥ T works. So Yes.

Wait, but we need to ensure that the wildcards matched to fixed elements get non-negative values. Fixed A matched to wild B: wild B = s - fixed A ≥ 0 since s ≥ T ≥ fixed A. Fixed B matched to wild A: wild A = s - fixed B ≥ 0 since s ≥ T ≥ fixed B. Good. And wild-wild pairs: set both to 0, sum 0? No, all pairs must sum to s. If there are remaining wild A and wild B (after matching fixed), they pair up: wild A + wild B = s. We can set wild A = 0, wild B = s (≥ 0). Or any split. Since s ≥ 0, fine. Actually, the number of remaining wild A equals remaining wild B (both equal N - (number of fixed matched) - ... let's see). Total pairs = N. Fixed-fixed pairs: M (we set M=0 for K=0). Fixed A - wild B: a_fixed. Fixed B - wild A: b_fixed. Wild-wild: N - a_fixed - b_fixed (could be negative if a_fixed + b_fixed > N, but K=0 means ≤ N, so ≥ 0). So wild-wild pairs = N - a_fixed - b_fixed ≥ 0. Set them to sum s (e.g., 0 + s). Good. So K=0 → Yes confirmed.

So we only need to handle K > 0. In that case, a_fixed + b_fixed > N, so there are many fixed elements. We need f(s) ≥ K for some s ≥ T.

Now, for K > 0, we compute f(s) for candidate s. Since K > 0, we need at least one fixed-fixed pair, so s must be a pairwise sum (and ≥ T). Candidates: pairwise sums a + b ≥ T.

Now, the computational task: find max f(s) over s ≥ T, check ≥ K.

Numpy approach:
- Get unique sorted A_vals (fixed) and counts ca. Similarly B_vals, cb.
- If a_fixed == 0 or b_fixed == 0: then K = max(0 + b_fixed - N, 0) or max(a_fixed + 0 - N, 0). If a_fixed = 0, K = max(b_fixed - N, 0) = 0 (since b_fixed ≤ N). So K = 0, handled. So if K > 0, both a_fixed > 0 and b_fixed > 0. Good.
- Compute pairwise sums and min-counts, aggregate, find max f(s) for s ≥ T.

With numpy:
```python
import numpy as np
A_vals = np.array(sorted(ca.keys()), dtype=np.int64)
A_cnt = np.array([ca[v] for v in A_vals], dtype=np.int64)
B_vals = np.array(sorted(cb.keys()), dtype=np.int64)
B_cnt = np.array([cb[v] for v in B_vals], dtype=np.int64)
# pairwise sums
S = A_vals[:, None] + B_vals[None, :]  # shape (na, nb)
V = np.minimum(A_cnt[:, None], B_cnt[None, :])
mask = S >= T
S_flat = S[mask]
V_flat = V[mask]

## worker: Implement the complete Python solution: parse inpu
- Reduced the problem to: choose target sum `S`; all fixed values must be `≤ S`; with `M(S)` = max fixed-fixed pairs summing to `S`, feasibility needs `M(S) ≥ a_fixed - b_wild` and `M(S) ≥ b_fixed - a_wild`. Both thresholds equal `a_fixed + b_fixed - N = K`, so condition is `M(S) ≥ K` for some `S ≥ T = max(max fixed A, max fixed B)`.
- If `K ≤ 0`, wildcards alone cover all fixed elements → always `Yes`.
- For `K > 0`, `S` must be a pairwise fixed sum `a+b` (≥ T). `M(S) = Σ_v min(cntA[v], cntB[S−v])` because the equality graph splits into independent bicliques per value pair `(v, S−v)`.
- Verified against all three samples (Yes / No / No).

Complexity: candidate sums are O(D_A·D_B) and each evaluation is O(D_A), worst case O(N^3) with N=2000 (too slow in the worst case). Needs optimization (e.g., accumulate `min(ca,cb)` per sum in one O(D_A·D_B) pass with early exit, or numpy bincount over pairwise sums).

## worker: Optimize the M(S) computation: replace the O(N³) p
- Replaced the O(N³) per-candidate evaluation with a single aggregation pass: for each distinct value pair `(a, b)` with counts `(ca, cb)`, add `min(ca, cb)` to `f[a+b]`, skipping sums `< T`. This is exact because `f(S) = Σ_v min(cntA[v], cntB[S−v])` is precisely the sum of `min(ca, cb)` over all pairs with `a + b = S` (the equality graph is a disjoint union of bicliques per complementary value pair).
- Early exit: since all contributions are non-negative, the moment any accumulated `f[s]` reaches `K` (with `s ≥ T`), the final value also satisfies `f(s) ≥ K`, so we can print `Yes` immediately. This helps a lot on Yes instances.
- Memory: the dict holds at most one entry per distinct achievable sum `≥ T`. In the worst case (all `D_A·D_B` sums distinct, answer No) this can be up to ~4·10⁶ entries for N=2000, which is heavy but the early-exit and the `s ≥ T` filter keep it manageable in practice; the algorithm is O(D_A·D_B) time.
- Verified logic against samples:
  - Sample 1: K = 3+3−4 = 2, T = 4; f(4) = min(cntA[0],cntB[4]) + min(cntA[2],cntB[2]) = 2 ≥ 2 → Yes.
  - Sample 2: K = 3, T = 4; max f(S) for S ≥ 4 is 2 → No.
  - Sample 3: K = 2, T = 4; f(3)=2 but 3 < T; for S ≥ 4 max is 1 → No.
