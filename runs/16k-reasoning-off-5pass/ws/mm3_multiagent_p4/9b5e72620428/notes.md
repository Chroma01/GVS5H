
## ideation
The problem requires determining if we can fill -1 entries in A and B with non-negative integers and permute A so that A_i + B_i is constant for all i.

Key observations:
- We can freely assign non-negative values to -1 entries in A and B, and permute A arbitrarily.
- This means the multiset of A must equal the multiset {S - B_i} for some S ≥ 0, where B has all values filled.
- Fixed A values must be contained in {S - B_i}, and fixed B values must allow S - B_i ≥ 0.
- If nA + nB ≤ N (where nA, nB are counts of fixed entries), we can always succeed by matching fixed entries to free slots and choosing S large enough.
- If nA + nB > N, we need at least T = nA + nB - N pairs of fixed (A,B) with A_i + B_j = S, meaning S must equal A_i + B_j for some fixed pair.
- For each candidate S (from {A_i + B_j}), compute maximum matching size in the bipartite graph where edge (i,j) exists iff A_i + B_j = S. The graph is a union of complete bipartite graphs between value classes, so max matching is M(S) = Σ_v min(cntA[v], cntB[S-v]).
- Feasible if M(S) ≥ T and S ≥ max(max_fixed_A, max_fixed_B).
- Constraints: N ≤ 2000, so nA, nB ≤ 2000. Candidate S count ≤ 4×10^6, naive O(nA) per S is too slow (8×10^9 ops).
- Optimization needed: since values are up to 10^9 but counts are small, we can process by value frequencies. The sum M(S) can be computed by iterating over distinct values in A and B. We can batch process candidates S by noting that for each value v, cntA[v] is constant, and we need cntB[S-v]. We can iterate over all pairs of distinct values, but still O(distinct_A × distinct_B) candidates, each requiring O(1) if we have precomputed lookups. However, we can group by S: for each S, we need sum over v of min(cntA[v], cntB[S-v]). If we have cntB as a dictionary, and iterate over v in distinct_A, it's O(distinct_A) per S. With up to 4×10^6 S, this is still too slow.
- Better: Since the number of distinct values is small (≤ 2000), we can iterate over all possible S values efficiently by using the fact that S = a + b for a in distinct_A, b in distinct_B. There are at most 4×10^6 such S, but many duplicates. We can use a dictionary to accumulate contributions: for each a in distinct_A and b in distinct_B, S = a+b contributes min(cntA[a], cntB[b]) to M(S). This is O(distinct_A × distinct_B) which is at most 4×10^6, feasible! Then we iterate over the dictionary and check if any S ≥ M has value ≥ T.

Wait, careful: M(S) = Σ_v min(cntA[v], cntB[S-v]). If we iterate over all pairs (a,b) with a in values_A, b in values_B, then for S = a+b, the term for v=a is min(cntA[a], cntB[b]). But there might be multiple v contributing to the same S. Actually, for fixed S, the sum is over all v, and the term is min(cntA[v], cntB[S-v]). If we let b = S-v, then as v runs over values_A, b runs over values_B, but only when b = S-v. So the sum is over v in values_A, and we look up cntB[S-v]. If we instead iterate over all pairs (v, b) in values_A × values_B, then for each pair, S = v + b, and the contribution to M(S) from that v is min(cntA[v], cntB[b]). But wait, is that correct? In the sum M(S), for a fixed S, we have exactly one term per v: min(cntA[v], cntB[S-v]). If we set b = S-v, then the term is min(cntA[v], cntB[b]). So if we iterate over all pairs (v, b) and compute S = v + b, then for that S, the pair (v,b) contributes min(cntA[v], cntB[b]) to M(S). However, for a fixed S, there may be multiple pairs (v,b) with v+b=S, and each such pair gives a contribution. And indeed, M(S) = Σ_{v,b: v+b=S} min(cntA[v], cntB[b]). This is exactly a convolution! So we can compute M(S) for all S by computing the convolution-like sum over all pairs. Since the number of distinct values in A and B is at most 2000 each, the number of pairs is at most 4×10^6. We can use a dictionary to sum the contributions: for each v in distinct_A, for each b in distinct_B, S = v + b, add min(cntA[v], cntB[b]) to dict_M[S]. This is O(distinct_A * distinct_B) ≤ 4×10^6, which is fast in Python.

Then for each S in dict_M, if S ≥ M and dict_M[S] ≥ T, we output Yes.

Edge cases: need to handle default values (0) when fixed list empty.

Verification with samples:
- Sample 1: nA=3, nB=3, N=4, nA+nB=6>4, T=2. M=4. Build dict: A values: 0:1,2:1,3:1. B values: 2:1,3:1,4:1. Pairs: (0,2)->S=2, min(1,1)=1; (0,3)->3,1; (0,4)->4,1; (2,2)->4,1; (2,3)->5,1; (2,4)->6,1; (3,2)->5,1; (3,3)->6,1; (3,4)->7,1. Dict: S=2:1,3:1,4:2,5:2,6:2,7:1. S=4≥4, value=2≥2, Yes.
- Sample 2: nA=3,nB=3,N=3,T=3. A:1,2,3. B:1,2,4. Pairs: S=2:1,3:2,4:1,5:2,6:1,7:1. Max value 2 < 3, No.
- Sample 3: nA=2,nB=3,N=3,T=2. M=max(2,4)=4. A:1,2. B:1,2,4. Pairs: (1,1)->2:1; (1,2)->3:1; (1,4)->5:1; (2,1)->3:1; (2,2)->4:1; (2,4)->6:1. Dict: 2:1,3:2,4:1,5:1,6:1. S≥4: S=4:1<2, S=5:1<2, S=6:1<2. No.

Looks good. Need to be careful with large values and memory. dict_M can have up to 4e6 entries in worst case, which is large but manageable (each entry is a key-value pair of integers). In Python, 4e6 dict entries might use a lot of memory (over 1GB), might be tight. We can optimize by only keeping S that are candidates and using default 0. But we can also note that in the worst case nA=nB=2000, distinct values could all be unique, so 2000*2000=4e6 pairs. 4e6 dictionary entries is heavy but possible. Alternatively, we can process differently: since we only need to check if any S works, and S must be ≥ M, we can iterate over the pairs and keep a running maximum or use a set. But we need the sum for each S. If we just want to know if there exists S with sum >= T, we could try to compute for each S the sum, but we can also bound: if many S, but we only care about those with large sum. However, the dict approach is straightforward and likely fast enough if memory permits. 4e6 entries with int keys and int values: each dict entry about 72 bytes, so ~288MB, might be too much. So we need a memory-efficient approach.

Alternative: Iterate over all pairs (a,b) and for each S=a+b, compute the contribution. But we can process by iterating over a in distinct_A, and for each a, iterate over b in distinct_B, and update a dictionary. But we can also avoid storing all S: we can iterate over all pairs and for each, check if S >= M and the sum for that S would be >= T, but we don't know the sum for S without all pairs. We need the full sum for each S.

We can use a dictionary but with default value 0, and only insert S when we have a contribution. The number of distinct S is at most the number of pairs, but could be less. In worst case all sums are distinct, so 4e6 entries. That's a lot. We can try to use a sorted list or something, but dictionary is easiest.

Given N=2000, 4e6 is the max. Maybe we can optimize: since nA + nB > N, at least one of nA or nB is > N/2. But still 4e6 is possible.

Another optimization: we can group by value. Since values are up to 1e9, but counts are small. We can use a dictionary for cntA and cntB. Then for each a in cntA, for each b in cntB, S=a+b. This is at most |cntA| * |cntB|. If many duplicates, less. |cntA| ≤ nA, |cntB| ≤ nB.

In Python, 4e6 dictionary entries might be too slow or memory heavy. We can try to use a different approach: for each S candidate, we need M(S). We can generate all S candidates and for each, compute M(S) on the fly using the counts, but we saw that's O(nA) per S. However, if we have only few S, it's fine. But worst case 4e6 S.

We can try to prune: S must be >= M. Also, the maximum possible M(S) is min(nA, nB). We need M(S) >= T. T = nA + nB - N. Since nA + nB > N, T >= 1. But also, M(S) is sum of mins. If T is large, only few S might work.

But in the worst case, say nA=2000, nB=2000, N=2000? But nA+nB=4000>2000, so T=2000. We need M(S) >= 2000. But M(S) ≤ min(nA,nB)=2000. So we need M(S)=2000. This requires that for all v, min(cntA[v], cntB[S-v]) = cntA[v], i.e., cntA[v] <= cntB[S-v] for all v, and sum cntA[v] = 2000, so cntB[S-v] >= cntA[v] for all v, and sum cntB[S-v] >= 2000, but there are only nB=2000 B's, so it must be that cntB[S-v] = cntA[v] for all v, and the multiset A equals S-B. This is a very restrictive condition. In this case, the number of S that work is at most 1 or a few. So we don't need to check all 4e6 S; we can stop when we find one. But in the algorithm, we still might compute M(S) for many S before finding one, or to conclude none.

But if we compute M(S) for all S, and most are 0, it's wasteful. We can iterate over all pairs (a,b) and build a frequency dict of S, but we need the sum of min(cntA[a], cntB[b]), not the count of pairs. For each S, we need the sum of min(cntA[a], cntB[b]) over all pairs with a+b=S. This is exactly what the dict does.

We can implement it with a dictionary. Let's estimate time: 4e6 iterations, each with a dict update. In Python, 4e6 operations is fast (a few seconds). 4e6 dict entries: each entry about 50-70 bytes, so 200-280MB, might be borderline but possibly okay for 256MB limit? Not sure. AtCoder memory limit is usually 1024MB or 512MB. We can try to use a more memory efficient structure, like a list of sums for only the S that are >= M, but we don't know them in advance.

Alternative: We can iterate over the smaller of cntA or cntB. Suppose nA <= nB. Then for each a in distinct_A, we can compute contributions to S for all b in distinct_B. But we can also note that for a fixed a, as b varies, S = a+b. The contribution to M(S) is min(cntA[a], cntB[b]). We can sort the distinct values or something.

Actually, we can compute M(S) by convolution if the values were small, but they are large.

Another idea: Since we only need to check if max M(S) >= T for S >= M, and M(S) is the size of the maximum matching, perhaps we can use a greedy matching or check if the condition holds without computing M(S) for all S. But the condition M(S) >= T is necessary and sufficient.

Given the constraints, the dict approach with O(nA * nB) time and space is acceptable. We can optimize memory by using collections.defaultdict(int) and only adding when needed. After populating, we iterate over items and check.

In Python, 4e6 items in a dict is large. Let's check: in Python 3.9, a dict with 4e6 int keys and int values: each entry is about 72 bytes (key+value+hash). 4e6 * 72 = 288MB. Plus overhead. Might be too much. We can try to reduce by using only S >= M, but we don't know M before processing? We can compute M = max(max_A, max_B) first. Then we can discard S < M. When building the dict, we can check S >= M before adding. But still, the number of S >= M could be large. In the worst case, if values are random, about half of the sums might be >= M. So still ~2e6 entries. 144MB, maybe okay.

But we can do better: we don't need to store all S. We can process per S. But we need the sum for each S. We can group by S on the fly. Actually, we can iterate over all pairs (a,b) and add to a dict. That's what we have.

Maybe we can use a different algorithm: Since nA and nB are at most 2000, and the threshold T is nA+nB-N, we can consider the number of "unmatched" A. As derived, we need Σ_v max(0, cntA[v] - cntB[S-v]) ≤ N - nB. This is equivalent to: the number of A values that are "excess" relative to B is small. This looks like we can iterate over possible S by considering the values.

Another approach: The problem is equivalent to: can we find a permutation π and fill -1's so that A_π(i) + B_i = S. This is like: the multiset A ∪ B can be partitioned into N pairs each summing to S? No.

I think the dict approach is the most straightforward. Let's optimize: use local variables, and maybe use array if values are bounded, but they are up to 1e9, so dict is necessary.

We can also note that the number of distinct values in A is at most nA, and in B at most nB. We can get the list of distinct values. Then iterate over the smaller list? If nA < nB, iterate over a in distinct_A, and for each a, iterate over b in distinct_B. This is nA * nB pairs. We can store the min(cntA[a], cntB[b]) in the dict.

To reduce memory, we can clear the dict after checking? No, we need all to find the max.

We can process in batches: for each a, compute its contribution to all S = a + b, and for each such S, we can keep a running max? But we need the sum for each S, not just max. Because different a contribute to the same S. However, note that for a fixed S, the contributions are from different a. We can accumulate.

Since the number of pairs is at most 4e6, and we only need to know if any S has sum >= T, we can try to compute the sum for each S but stop early if we find one >= T. But we still need to accumulate to know the sum for S. We can use a dict and during accumulation, after adding, check if the current value >= T. But we need to ensure that we don't check before all contributions are added. So we need to finish accumulation for that S. We can do: after processing all pairs, iterate over dict. Or we can process S one by one: generate all S and their contributions. But S are many.

We can sort the pairs by S? No, that would require storing all pairs.

Given that 4e6 is the maximum, and Python can handle 4e6 simple operations, but memory is a concern. Let's check if we can avoid storing all S.

We can use a dictionary with default 0. Let's assume the memory is okay (AtCoder problems with N=2000 often allow O(N^2) memory). The time is also O(N^2). I think it's fine.

We should also handle the case when fixed_A or fixed_B is empty. If nA=0, then nA+nB <= N? Not necessarily: nB could be N. If nA=0, nB=N, then nA+nB=N, so nA+nB <= N, so Yes. If nA=0, nB > N? Impossible since nB ≤ N. So if nA=0, always Yes? Wait: nA=0, nB=N, then nA+nB=N, so nA+nB <= N, so Yes. If nA=0 and nB=0, Yes. So the only interesting case is nA>0 and nB>0 and nA+nB > N.

In the dict approach, if nA=0 or nB=0, the product is 0, so dict empty. We need to handle the early return.

Implementation steps:
1. Read N, A, B.
2. fixed_A = [x for x in A if x != -1]
3. fixed_B = [x for x in B if x != -1]
4. nA = len(fixed_A), nB = len(fixed_B)
5. If nA + nB <= N: print("Yes") and return.
6. Compute max_A = max(fixed_A) if nA>0 else 0
7. Compute max_B = max(fixed_B) if nB>0 else 0
8. M = max(max_A, max_B)
9. T = nA + nB - N
10. Build cntA: dict, cntB: dict.
11. For a in fixed_A: cntA[a] = cntA.get(a,0)+1
12. For b in fixed_B: cntB[b] = cntB.get(b,0)+1
13. dict_M = defaultdict(int)
14. For a, ca in cntA.items():
      for b, cb in cntB.items():
          S = a + b
          if S >= M:
              dict_M[S] += min(ca, cb)
15. For S, m in dict_M.items():
      if m >= T:
          print("Yes") and return
16. Print("No")

This is O(nA_distinct * nB_distinct) time and space. nA_distinct ≤ 2000, nB_distinct ≤ 2000, so 4e6 max.

Potential issue: if values are large, S is large, but that's fine.

We should also consider: what if nA + nB > N but nA=0 or nB=0? If nA=0, nB > N? Impossible. So nA>0 and nB>0.

Edge case: nA + nB > N but one of them is 0? Impossible since nA,nB ≥ 0 and sum > N ≥ 2, so both >0.

So the algorithm is correct.

We can optimize the inner loop: iterate over the smaller dict to reduce iterations? But product is the same.

We can also avoid the dict by using a list if we compress coordinates, but not necessary.

Let's test with a custom case: N=2, A=[-1,5], B=[-1,3]. fixed_A=[5], fixed_B=[3], nA=1,nB=1,N=2, nA+nB=2<=2, Yes. Indeed, set A=[2,5], B=[2,3], S=4? Wait, we need S such that A_i = S - B_i. For fixed A=5, need S - B = 5, so B = S-5. Fixed B=3, so S-5=3 => S=8. Then A for other is S - B_other. We can set B_other=0, A_other=8. So A=[5,8], B=[3,0]? But B_other is free, we set to 0, then A_other=8-0=8. But fixed B is 3, fixed A is 5. A=[5,8], B=[3,0], S=8. Works. So Yes.

Another case: N=2, A=[5,5], B=[3,3]. nA=2,nB=2,N=2, nA+nB=4>2, T=2. M=max(5,3)=5. Candidates: S=5+3=8. cntA[5]=2, cntB[3]=2. S=8: min(2,2)=2 >= T=2. S=8>=5, Yes. Indeed, A=[5,5], B=[3,3], S=8.

Another: N=2, A=[5,6], B=[3,3]. T=2. S candidates: 5+3=8, 6+3=9. For S=8: cntA[5]=1, cntB[3]=2? Wait, cntA:5:1,6:1. cntB:3:2. S=8: need cntB[8-5]=cntB[3]=2 >=1? min(1,2)=1. For v=6, cntB[2]=0, min(1,0)=0. Total M(8)=1 <2. S=9: v=5: cntB[4]=0; v=6: cntB[3]=2, min(1,2)=1. M=1. So No. Indeed, we need two pairs summing to S, but only one B value 3, so S must be 5+3=8 or 6+3=9. At S=8, A=5 matches B=3, but A=6 has no B=2. At S=9, A=6 matches B=3, but A=5 has no B=4. So No.

Looks good.

One more: N=3, A=[1,2,-1], B=[1,2,4] (sample 3). We already did.

What about large N? It should work.

Potential optimization: we can break early if dict_M[S] >= T, but we need to finish all contributions to that S. However, since we are building the dict, we can check after the full accumulation. We can also use a max-heap or something, but not needed.

Memory: 4e6 entries might be heavy. Let's check if we can reduce. In the dict, we only store S >= M. The number of such S could be up to 4e6, but typically less. In the worst case, if all values are random, about half of the sums are >= M. Still 2e6. 2e6 * 72 = 144MB. Might be okay. If memory is an issue, we can use a more compact representation, but I think it's acceptable.

We can also note that we only need to know if any S works. We can iterate over the pairs and keep a running count in a dict, but we can also process by S. Since the pairs are independent, we can group by S using a dict. I think it's fine.

Let's code it.

We must be careful with large integers: a+b could be up to 2e9, but Python handles big ints.

Implementation details:
- Use sys.stdin.read() to read fast.
- Parse ints.
- Use collections.defaultdict(int) for counts and for M_dict.
- After building, iterate over M_dict items.

We can also sort the keys and check from largest to smallest? Not needed.

Time complexity: O(N^2) with N=2000 is 4e6 iterations, each doing a few operations. Should run in < 1 second in PyPy.

Let's write the code.

One more check: what if nA + nB > N but we have S < M? The condition S >= M is necessary because for any fixed A_i, if it's matched to a fixed B, S = A_i + B_j >= A_i and >= B_j, so S >= max(max_A, max_B). If it's matched to free B, S >= A_i. So S >= max_A. Similarly for fixed B. So S >= M is necessary. So we can safely ignore S < M.

In the dict building, we only add if S >= M.

Edge case: if M is 0 (all fixed A and B are 0), then S >= 0 is fine. S could be 0. Our condition S >= M is satisfied.

What about the case where fixed_A or fixed_B is empty but nA+nB > N? Impossible as argued.

So the solution is complete.

We should also consider if there are duplicate values: using dict for counts handles that.

Now, write the final code.

## worker: Implement the solution in Python using the describ
The algorithm works as follows:
1. Separate fixed (non -1) entries in A and B.
2. If the total number of fixed entries `nA + nB` is at most `N`, we can always succeed by matching fixed entries to free slots and choosing a sufficiently large common sum `S`. This is because we have enough free positions to absorb all fixed values.
3. Otherwise, we need at least `T = nA + nB - N` pairs of fixed A and fixed B that sum to the same `S`. The sum `S` must be at least `M = max(max_fixed_A, max_fixed_B)` to ensure all derived values are non-negative.
4. For each candidate sum `S = a + b` (where `a` is a fixed A value and `b` is a fixed B value), the maximum number of cross-pairs we can form is `M(S) = Σ_v min(cntA[v], cntB[S-v])`, because the bipartite graph decomposes into complete bipartite graphs between value classes.
5. We compute this efficiently by iterating over all pairs of distinct values in A and B (at most 4×10^6 pairs for N=2000) and accumulating the minimum counts into a dictionary keyed by `S`.
6. If any `S >= M` achieves `M(S) >= T`, we output "Yes"; otherwise "No".

This runs in O(nA_distinct × nB_distinct) time and space, which is at most O(N²) = 4×10^6, well within limits for N=2000.
