
## ideation
We need for each i, the maximum possible GCD of a K‑element subset that includes A_i. Since A_i is in the subset, the GCD of the K elements must divide A_i, so the answer is the largest divisor d of A_i for which there are at least K‑1 other elements (i.e., at least K total elements in the whole array) divisible by d.

Thus if we know, for every integer v (1 ≤ v ≤ 10^6), the count cnt[v] = number of A_j divisible by v, then the answer for index i is simply the largest divisor d of A_i with cnt[d] ≥ K.

Constraints: N up to 1.2·10^6, A_i up to 10^6. Computing cnt[v] for all v can be done with a frequency array freq[1..1e6] and then iterating v from 1 to 1e6, adding freq[v] to multiples of v. This is a classic sieve‑style divisor counting: for d = 1..M, cnt[d] = sum_{multiple m of d} freq[m]. Complexity O(M log M) (harmonic sum) ≈ M·(1 + 1/2 + 1/3 + ... ) ≈ M·log M ≈ 2·10^7 for M=1e6, fine.

Then for each A_i we need to enumerate its divisors. A_i ≤ 10^6, enumerating divisors by iterating up to sqrt(A_i) gives O(√A_i) ≈ up to 1000 per element, total ~1.2e9? That’s too much. But N=1.2e6 and average sqrt is 500, gives 6e8 operations, borderline. We need faster divisor enumeration. However, we only need the *largest* divisor with cnt[d] ≥ K. We can iterate divisors in decreasing order to break early. We can also precompute for each number its divisors (a list) but that would be too memory heavy (total number of divisor pairs is about M log M). Better: iterate i from 1..sqrt(A) and collect pairs (i, A//i). Then test the larger ones first.

Even O(√A) per element might be okay in C++ but in Python we need optimization. 1.2e6 * 1000 = 1.2e9 operations → too slow in Python. We need a smarter way.

Observation: We only need the largest divisor d of A_i satisfying cnt[d] ≥ K. Since cnt is non‑increasing as d increases? Actually cnt[d] is decreasing as d grows (fewer multiples). So we can find the answer by scanning from A_i downwards, checking each divisor of A_i? That would be up to 1e6 per element, also too much.

Alternative: For each possible d, we can compute the set of indices i for which d is a divisor of A_i. Then for each such i, we could try to update answer[i] = max(answer[i], d) if cnt[d] ≥ K. This is similar to: for each d from 1..M, if cnt[d] ≥ K, then for all indices i with A_i divisible by d, set ans[i] = max(ans[i], d). Then after processing all d, ans[i] will be the largest divisor d of A_i with cnt[d] ≥ K, which is exactly the required answer. Complexity: For each d, we need to iterate over its multiples (i.e., all values v = multiple of d) and then over indices where A_i = v. So total work is sum_{d=1..M} (M/d) * (average number of indices with value v) but actually we can process via multiples of d in the array: for each position, we iterate over its divisors? Wait.

We can process as: for d = 1..M:
  if cnt[d] >= K:
    for each value v that is a multiple of d:
        for each index i where A_i == v:
            ans[i] = max(ans[i], d)

But we can avoid iterating over indices directly by noting that we can update a temporary answer per value. Actually we need answer per index. We could, for each value v, maintain a list of indices where A_i = v. Then for each d, we iterate over multiples m of d, and for each m, for each idx in positions_of_value[m], we update ans[idx] = max(ans[idx], d). This is essentially the same as enumerating divisors for each index but in reverse.

The total work of this double loop is: sum_{d=1..M} sum_{m multiple of d} (number of occurrences of value m). Let freq[m] be the count of occurrences of value m. Then total updates = sum_{d=1..M} sum_{m: d|m} freq[m] = sum_{m=1..M} freq[m] * (number of divisors of m). Since each index contributes its number of divisors. Sum of number of divisors over all m up to M is about M log M (average divisor count ~ log m). With M=1e6, that's about 1e6 * (log 1e6 ≈ 14) ≈ 1.4e7 updates, which is fine! Actually we have N up to 1.2e6, but total sum of divisors of each A_i (which are bounded by 1e6) is roughly N * average divisor count (which for random numbers up to 1e6 is about O(log N) or maybe ~100? Wait average number of divisors up to 1e6 is around 100? Let's check: d(n) average is about log n + (2γ-1) ≈ log n + 0.154. For n=1e6, log 1e6 ≈ 13.8, so average ~14. So total divisor count across N=1.2e6 is about 1.2e6 * 14 = 1.68e7, which is okay. So enumerating divisors per element is okay! But earlier I thought 1.2e6 * 1000 = 1.2e9. That's because sqrt(1e6)=1000, worst-case divisor enumeration is O(sqrt) not O(divisor count). However worst-case numbers like 720720 have many divisors (~240). But still the total number of divisors is at most about N * 240 ≈ 2.9e8, which might be high. But typical distribution is much lower. However we need a guaranteed solution.

The double loop approach (processing d and multiples) ensures total work = sum_{i} d(A_i) where d(A_i) is number of divisors of A_i. Since each divisor d of A_i is processed exactly once for that index (when we process d and consider A_i). Actually each pair (i, d) where d|A_i corresponds to a step where we update ans[i] = max(ans[i], d) if cnt[d] >= K. So total updates = sum_i τ(A_i) where τ(n) is number of divisors. For n up to 1e6, the maximum τ(n) is 240 (for 720720). So worst-case total updates ≤ 1.2e6 * 240 = 288 million, which is borderline but maybe okay in Py with optimized loops? Might be too slow. But we can optimize: we only need to consider d where cnt[d] >= K. If K is large, many small d will be skipped. However K can be as small as 1. Then we would need to consider all d. In that case, answer for each i is just A_i itself (since we can pick K elements that include A_i and all other elements, but GCD may be less than A_i? Wait K=1: we choose 1 element including A_i, so GCD is just A_i. So answer = A_i. Indeed if K=1, we just output A_i. That matches condition: we need largest divisor d of A_i with cnt[d] >= 1. Since cnt[A_i] >= 1 (the element itself), answer = A_i. So we can handle K=1 separately as trivial O(N). For K>1, cnt[d] >= K is a constraint. But K can be as low as 2. For K=2, we need at least two elements divisible by d. Many d will have count >=2, but still could be many. For K=2, worst-case we still might need to consider many divisors.

Alternative: For each A_i, we can enumerate its divisors via sqrt and check count. Since A_i ≤ 1e6, sqrt is 1000, so per element we do up to 1000 iterations. For N=1.2e6, that's 1.2e9 operations, which is too slow. However we can prune: we only need the largest divisor d with cnt[d] >= K. We can iterate divisors in decreasing order, but we still need to generate them. The number of divisors of A_i is at most 240, so enumerating all divisors by sqrt method yields at most ~1000 checks, but the inner loop (checking if divisor) is cheap. But the overhead of the sqrt loop (i from 1 to sqrt) for each element is 1000 iterations, which is huge. However we can generate divisors more efficiently: we can precompute for each integer its prime factorization using a sieve of smallest prime factor (SPF) up to 1e6. Then enumerate divisors from prime factors using recursion or iterative product generation. The number of divisors τ(n) is at most 240, so generating all divisors for each A_i would be sum τ(A_i) ≤ 288 million, which is okay. 288 million operations might be borderline in Python but maybe acceptable with some optimization (like using loops and list comprehensions). 288 million is too high for Python (likely >5 seconds). However we can reduce by noting we only need the largest divisor with cnt[d] >= K, and we can generate divisors in decreasing order without enumerating all. But generating all divisors is required to find the max. We can generate them in decreasing order: we can generate all divisors then sort descending, but sorting each list would be heavy. We can generate divisors via recursion and keep a max. But still need to generate all to ensure we find max. However we can stop early if we find a divisor d that equals A_i? Actually the maximum possible is A_i itself. If cnt[A_i] >= K, answer is A_i. So we can check that first. If not, we need to find the next largest divisor of A_i that has count >= K. We can try to iterate divisors from large to small: we can generate divisors via prime factorization and produce them in descending order by exploring exponents from max to 0. That still may need to generate many divisors before finding a suitable one. In worst-case (K large, count only for d=1), we may have to generate all divisors to realize only 1 works. That could be up to 240 checks per element, which is fine (240*1.2e6 = 288 million). But 288 million simple operations (just integer division and array lookups) might be borderline but maybe okay in Py if optimized? Let's estimate: 288 million operations at ~0.1 ns? No, Python ~50 ns per simple operation? Actually Python can do about 50-100 million simple operations per second? That seems optimistic. Typically Python can do ~30-50 million simple integer operations per second? Not sure. 288 million may be too high (maybe 6-10 seconds). But we can perhaps do better: we can precompute for each value v, the list of its divisors? That would be memory heavy: total number of divisor entries is sum τ(n) for n up to 1e6, which is about 1e6 * log 1e6 ≈ 14 million. Actually sum_{n=1}^{M} τ(n) ≈ M log M + (2γ-1)M + O(sqrt(M)). For M=1e6, that's about 1e6 * (log 1e6 + 0.154) ≈ 1e6 * (13.8155 + 0.154) ≈ 13.97 million. So storing a list of divisors for each value up to 1e6 would be about 14 million integers, which is okay memory wise (~112 MB if 8 bytes each). But building that might be time-consuming but still okay.

But we also need to map values to indices. We need to know for each value v, the list of indices where A_i = v. We can store a list of indices for each v. The total number of indices is N=1.2e6, so storing them is okay.

Then the algorithm: 
1. Read N, K, array A.
2. Build freq array of size M=1e6: freq[v] = number of occurrences of v in A.
3. Build cnt array of size M: for d in 1..M: for multiple m in range(d, M+1, d): cnt[d] += freq[m].
   Complexity O(M log M) ~ 14 million steps.
4. If K == 1: answer is just A_i (since any single element subset's GCD is the element). Output A_i.
   Actually we must be careful: For K=1, we choose exactly one element (must include A_i), so GCD = A_i. So answer = A_i. So we can output directly.
5. For K > 1: For each d where cnt[d] >= K, we need to update ans for all indices i such that d | A_i. We can do:
   ans = [0]*N (or maybe default to 1?).
   For d from 1 to M:
       if cnt[d] >= K:
           # iterate over multiples m of d
           for m in range(d, M+1, d):
               # for each index idx in positions[m]:
               for idx in pos[m]:
                   if ans[idx] < d: ans[idx] = d
   This will assign the largest d for each index (since we iterate d from 1 upward, we assign and later larger d will overwrite). This double loop will iterate over each pair (d, m) where d|m and there is at least one occurrence of m. That's sum_{d} sum_{m: d|m} freq[m] = sum_i τ(A_i). As discussed, about 14 million? Wait earlier we said sum_i τ(A_i) where A_i are up to 1e6. For N=1.2e6, average τ is about 14, so total pairs is ~16.8 million. Actually sum_{i=1}^{N} τ(A_i) is at most N * max τ(1e6) = 1.2e6 * 240 = 288 million, but typical average is 14, so ~16.8 million. However worst-case input could be all numbers with many divisors (e.g., many 720720). But N=1.2e6, each 720720 has 240 divisors, so total pairs = 1.2e6 * 240 = 288 million. That's the worst-case bound. Is 288 million updates feasible in Python? Possibly borderline but maybe okay with optimized loops and using local variables. But we also have the outer loop over d (1..1e6) and inner loop over multiples. The sum of lengths of inner loops (over multiples) is M/1 + M/2 + ... + M/M = M * H_M ≈ M log M ≈ 14 million. Wait we need to be careful: The double loop for d from 1..M and for m multiple of d is M * (1 + 1/2 + ... + 1/M) = M * H_M ≈ M * (ln M + gamma) ≈ 1e6 * 14.4 ≈ 14.4 million. That's the number of (d,m) pairs. For each such pair, we then iterate over indices where A_i == m. So total updates = sum_{d} sum_{m: d|m} freq[m] = sum_{m} freq[m] * (number of divisors of m). That is sum_i τ(A_i). So the pair iteration cost is 14 million (the pairs) plus the cost of iterating over indices. So the main cost is the inner loop over indices. So total index updates = sum_i τ(A_i). For worst-case 288 million, that's the cost.

We can possibly reduce the number of d we consider: only d where cnt[d] >= K. For K large, many d will be skipped, reducing total work. For K small (like 2), many d will satisfy. But maybe we can also stop early for each index: we want the largest d. We can process d from M down to 1, and for each d, update all indices divisible by d. Then we can break early when all indices have been assigned (i.e., ans[i] > 0). However we need to assign the largest d for each index, so processing descending ensures first assignment is the maximum. If we process descending, we can maintain a counter of how many indices still have ans[i] == 0 (i.e., not assigned). When we process a d that satisfies cnt[d] >= K, we assign ans for those indices. Once all indices are assigned, we can break. This can drastically reduce work if K is large, because many d will not be needed. However for K=2, many d will be needed; but still maybe we can break after processing d=some value? Actually we need to assign each index its answer. The answer is the largest divisor d of A_i with cnt[d] >= K. If we process d descending, we will assign each index at the first d (largest) that divides A_i and has cnt[d] >= K. So we can break when all indices are assigned. This is similar to a "sieve" assignment.

The number of d we process depends on K. For K large, early d may be small. For K=2, the answer for many indices may be relatively large (maybe the element itself if it appears at least twice, else a large divisor). But we can estimate worst-case: Suppose all A_i are distinct and prime numbers > N/2? Then cnt[d] >= 2 only for d=1 (since each prime appears once). Then answer for all i is 1. So we would process d from M down to 1, but only d=1 satisfies cnt[d] >= 2. So we only need to process d=1, assign ans[i]=1 for all i (since 1 divides everything). So we can break after d=1. That's great. Actually we need to check: For each index, we need the largest divisor d of A_i with cnt[d] >= K. If cnt[1] >= K (always true because N >= K), then for all i, answer is at least 1. But we need the maximum. If no larger divisor works, answer is 1. So processing d descending: we check d=M, M-1, ... 1. At d=1, we assign all remaining indices. So we can break. So the algorithm will process only d where cnt[d] >= K and for which there is at least one index not yet assigned that has d as a divisor and for which no larger divisor with count >=K divides it. In the worst-case scenario (K small, many d satisfy), we may have to process many d. But we can analyze worst-case number of d processed. For each d, we assign ans for indices that have d as a divisor and for which no larger divisor with count >=K divides them. In the worst case, each index may be assigned at a different d. So the total number of assignments is at most N (once per index). However the inner loops still iterate over multiples of d and indices. But we can skip iterating over indices that are already assigned (ans[idx] != 0). So we can reduce work.

Implementation details:
- Build pos: list of lists for each value v (1..M). Since M=1e6, creating a list of 1e6 empty lists is okay (about 8 MB for the list of lists overhead? Actually each empty list is an object ~56 bytes, so 1e6 * 56 = 56 MB, plus the list container itself ~8 MB, total ~64 MB, which may be borderline but okay. But we can avoid storing pos for all values; we can store a dictionary mapping value to list of indices only for values that appear. Since N up to 1.2e6, we can store a dict of value->list of indices. The number of distinct values is at most min(N, M) = 1.2e6. Each list will be allocated as needed. However we also need to iterate over multiples of d quickly. For each d, we need to iterate over values m that are multiples of d and appear in the array. We can iterate over m in steps of d, and check if m is present (i.e., freq[m] > 0). If present, we iterate over its indices. This is O(M log M) iterations for the outer loops, plus per index assignments.

But we need to be careful about time: iterating m from d to M step d for each d yields total steps M * H_M ≈ 14 million. That's fine. For each m with freq[m] > 0, we need to iterate over its indices. The total number of index visits is sum_i τ(A_i) as before. So we need to implement this efficiently.

We can store pos as a list of lists of indices, but we can also store a list of lists of indices for each value, but we can compress using array of vectors? In Python, a list of lists of size M+1 (1e6+1) is memory heavy but maybe okay if we store only for values that appear: we can create an array of size M+1 where each element is either a list of indices or None. But we can also store a dictionary mapping value to list of indices. However iterating over m from d to M step d requires checking if m is a key in the dict, which is O(1) average but overhead of dict lookups may be high for 14 million steps. So better to use a list of lists of size M+1 where we pre-fill empty list for each v. That's memory heavy but may be okay (1e6 lists). Let's compute memory: each empty list object is about 56 bytes (on 64-bit CPython). 1e6 * 56 = 56 MB. Plus the outer list of 1e6 references (8 bytes each) = 8 MB. Total ~64 MB. Plus the freq array (M+1 ints, 4 or 8 bytes) ~8 MB. Plus cnt array ~8 MB. Plus ans array (N ints) ~10 MB. Total < 100 MB, which is within typical limits (256 MB). However Python's memory overhead for list of lists can be larger due to pointer alignment. But 1e6 empty lists is too many objects; each list object is separate Python object, memory overhead is high. Actually each empty list is a PyObject with ob_base, ob_size, allocated size, etc. Might be around 56 bytes as said. 1e6 * 56 = 56 MB. The outer list holds references to these objects (8 bytes each) = 8 MB. So total 64 MB. That's okay. However creating 1e6 empty lists might be slow (time). But we can allocate a list of N empty lists for values that appear only, using a dict. But dict overhead per key is also high. Let's examine alternatives.

Alternative: Instead of storing indices per value, we can store a list of (value, index) pairs sorted by value, then for each d we iterate over multiples and binary search for occurrences? That would be more complex.

We can also avoid storing per value indices altogether: Instead of iterating over multiples m and then indices, we can for each index i, enumerate divisors of A_i and find the largest with cnt[d] >= K. Since τ(A_i) average ~14, total divisor enumerations ~ 16 million, which is less than 14 million pairs? Wait sum_i τ(A_i) is about 16 million average. Actually earlier we said sum_i τ(A_i) ≈ N * average τ ≈ 1.2e6 * 14 = 16.8 million. That's much less than 14 million pairs? Wait we need to compare: The pair iteration approach also yields sum_i τ(A_i) updates. The difference is the overhead of iterating over d and multiples. The pair iteration has overhead of iterating over d and multiples (14 million steps) plus index updates (sum_i τ(A_i)). The divisor enumeration per index approach has to compute divisors for each index, which also is sum_i τ(A_i) operations, but also requires factorization (maybe using SPF). So both have similar total work, but the pair iteration may have lower constant factor because it avoids factorization for each index (just simple loops). However we need to handle the condition cnt[d] >= K. The pair iteration naturally checks that per d.

Thus the pair iteration approach is viable.

Now memory: we need pos per value. We can store a list of indices per value as a list of lists. Let's estimate memory more accurately: In CPython, each list object is about 56 bytes (for 64-bit). For 1e6 values, that's 56 MB. The outer list (list of length M+1) holds references (8 bytes each) = 8 MB. So total ~64 MB. That's okay. However we also have freq and cnt arrays of size M+1 of ints (maybe use array('I') or list of ints). A list of 1e6 ints uses about 28 MB (since each int is 28 bytes). That's too big: 1e6 ints * 28 = 28 MB. Actually Python int is 28 bytes (for 64-bit). So freq and cnt each would be 28 MB, total 56 MB. That's large but still maybe okay. However we can use array('I') or 'i' from module array to store ints in C array (4 bytes each). That would reduce memory. But we need to index quickly. We can use list of ints for freq and cnt for simplicity, but memory may be high: freq (M+1) ~ 1e6 * 28 = 28 MB, cnt same, plus pos lists overhead, plus ans list (N ints) ~ 1.2e6 * 28 = 33.6 MB, total > 100 MB, maybe borderline but okay if limit is 1024 MB. Usually memory limit is 1024 MB or 512 MB. But we should be safe.

We can reduce memory: we can use a list of ints for freq and cnt, but we can reuse memory? Actually we need both. We can compute cnt from freq in place: after building cnt, we can discard freq or reuse its array. But we need freq only for building cnt; after cnt is built, we can free freq (set to None) to allow GC. But we also need pos per value. pos is list of lists. We can avoid storing pos by using an array of start indices and a flat list of indices, like an adjacency list. But that is more complex.

Alternatively, we can avoid pos altogether: For each d, we iterate over multiples m, and for each m, we need to know which indices have value m. If we have an array of lists of indices, we can iterate. That's fine.

Memory estimation: freq (list of ints) 28 MB, cnt 28 MB, pos (list of 1e6 lists) 64 MB, ans (list of ints) 34 MB, plus A (list of ints) maybe we can reuse A for reading and not store separate? Actually we need A for building freq and pos. We can read A, store in a list, and also fill freq and pos. So A list is needed (N ints) ~34 MB. That's huge. So total memory: A (34) + freq (28) + cnt (28) + pos (64) + ans (34) = 188 MB. That's okay if limit is 1024 MB. If limit is 256 MB, we may be near limit but still okay. However we can reduce memory: we don't need to keep A after building freq and pos. Actually we need A to answer? Not after building pos. We can discard A after building freq and pos. But we need to output ans per index. We can just compute ans and output. So we can free A. But we need to store A_i values for later? No. So we can just read values, fill freq, pos, and discard the list. But we also need to iterate over indices to output ans. Actually we will output ans after computing. We can compute ans in place and then output. So we can free A after building freq and pos. That reduces memory by 34 MB.

But we also need to know A_i for each index to compute answer? No, we compute ans per index using the method that doesn't need A_i after building pos. So we can discard A.

Thus we can read values, fill freq and pos (list of lists). Then we can delete the input list to free memory. Then compute cnt from freq. Then compute ans.

But we also need to store ans list of size N (int). That's 34 MB. So total memory maybe around 28+28+64+34 = 154 MB + overhead for list of lists (the references to lists) maybe 8 MB, plus the lists themselves (the inner lists) each have overhead but many will be empty. Actually many values may not appear, but we still have empty list objects for them. That's the 64 MB. So total maybe ~150 MB. That's okay.

But we need to be careful: 1e6 empty list objects may cause memory fragmentation and time to allocate. We can avoid creating empty lists for values that never appear. Instead we can store a dict mapping value to list of indices. Since N=1.2e6, the number of distinct values is at most N. The dict overhead per key is high (like 72 bytes). For 1.2e6 distinct values, that's huge memory (86 MB). But we can store pos as a list of lists but allocate only when needed: we can create an array of size M+1 of None, and when we see a value v, we create a list and store at pos[v] = [idx]. That's still a list of length M+1 with references (8 bytes each) to None (or list). So memory for the outer list: 1e6+1 references (8 MB) plus each reference points to a list object (the ones we create) or None. So memory for empty slots is just 8 MB (the list of references). Actually the list of references holds 1e6+1 pointers (8 bytes each) = ~8 MB. That's fine. The list objects themselves are only created for values that appear. So memory for pos is about 8 MB for the outer list plus overhead for each list object (56 bytes) + overhead for the list's internal array (maybe 8 bytes per element?). For each value, we store indices in a Python list. The total number of stored indices is N (1.2e6). Each integer is 28 bytes, plus list overhead per list (maybe 56 bytes). So total memory for indices: N * 28 = 33.6 MB, plus overhead for each list object: distinct values * 56. Distinct values <= N, so worst-case 1.2e6 * 56 = 67 MB. So total maybe 8 + 33.6 + 67 = 108 MB. That's okay.

Thus we can implement pos as a list of length M+1 initialized with None. For each index i, v = A_i, if pos[v] is None: pos[v] = [i] else pos[v].append(i). This is O(N) time.

Now we need to compute cnt[d] for all d. We'll have freq array of size M+1. We'll fill freq[v] = count of occurrences (or just use len(pos[v])?). Actually we can compute freq from pos: we can have freq = [0]*(M+1), and for each v in pos where pos[v] is not None, freq[v] = len(pos[v]). That is O(number of distinct values). Simpler: we can just use len(pos[v]) when needed, but for speed we can fill freq.

Now compute cnt: for d in range(1, M+1): for m in range(d, M+1, d): cnt[d] += freq[m]. This is O(M log M) ~ 14 million iterations. Each iteration is a simple addition. That's fine.

Now we need to compute ans. We'll have ans = [0]*N.

If K == 1: ans[i] = A_i (but we have discarded A). Actually we need to output for each i, which is just A_i. Since we have pos per value, we can output A_i by reconstructing? But we need to output in order. We could store A_i in a list of size N (maybe we can keep it for output). Actually we can compute ans for K>1 using the method. For K=1, we can just output the original A_i. So we can keep A list. But we wanted to free A to save memory. But we can also compute ans for K=1 using the same method: For K=1, condition cnt[d] >= 1 holds for all d (since freq[d] >= 1 for d that appear). But we need the largest divisor of A_i with count >=1, which is A_i. So we can just output A_i. So we can handle K=1 separately. So we need to store A_i anyway to output for K=1. But we can also compute ans for K=1 using the same method: for d from M down to 1: if cnt[d] >= 1 (which is always true for d that appear), then for each index with value divisible by d, assign ans. That would be heavy. So it's better to treat K=1 as special case and store A. Since N up to 1.2e6, storing A is okay (33 MB). So we can keep A.

Thus overall memory: A (33 MB), freq (28 MB), cnt (28 MB), pos (8 + 33 + maybe 67) ~108 MB, ans (33 MB). Total ~230 MB. Might be high but perhaps okay if limit is 1024 MB. If limit is 256 MB, we might be close. We can reduce memory by not storing freq and cnt as Python lists of ints; we can use array('I') for them. That reduces each to 4 MB (since M=1e6, 4 bytes each). Actually 1e6 * 4 = 4 MB. That's huge savings. We can use the module 'array' or 'ctypes' or 'numpy'? Not allowed. We can use built-in list of int but memory is large. However we can use memoryview of bytearray? Not convenient. We can use list of int for freq and cnt but we can also compute cnt in place from freq: we can reuse freq array to store cnt? Actually we need both for building cnt and for later use. We can compute cnt in a separate array. But we can also compute cnt directly from pos without freq: for d in range(1, M+1): for m in range(d, M+1, d): cnt[d] += len(pos[m]) if pos[m] else 0. That avoids freq array. However len(pos[m]) each time is O(1) but we need to call len each time, which is a function call overhead. But we can store freq in a list of ints, but we can use array('I') to store them. Let's consider using array('I') for freq and cnt. However array('I') elements are Python ints when accessed? Actually array('I') returns Python int on indexing, but the storage is C array. So memory is 4 bytes per element. That's good. We can also use list of int for freq and cnt but we can free one after use. For instance, we can compute cnt directly into a list of ints, then we can reuse freq array for something else? Not needed. But we can compute cnt using pos: we can allocate cnt = [0]*(M+1). Then for d in range(1, M+1): total = 0; for m in range(d, M+1, d): if pos[m]: total += len(pos[m]); cnt[d] = total. This is O(M log M) but with an extra if check. That's okay.

But we need to be careful about speed: iterating d from 1 to M (1e6) and inner loop multiples (M/d) steps yields about 14 million steps. Each step we do if pos[m]: (checking if not None) and then len(pos[m]) (which is O(1) but a function call). That's okay. However we also need to store cnt[d] for later use. So we can allocate cnt as a list of ints.

Now for assignment: ans = [0]*N. We'll also need a counter remaining = N (or maybe we can use ans[i] = 0 to indicate not assigned). For d from M down to 1:
   if cnt[d] >= K:
       # iterate multiples m of d
       for m in range(d, M+1, d):
           if pos[m]:
               for idx in pos[m]:
                   if ans[idx] == 0:
                       ans[idx] = d
                       remaining -= 1
       if remaining == 0:
           break

This ensures we only assign each index once (the first d that divides it and satisfies condition). Since we iterate d descending, we assign the maximum d.

We need to ensure we break early when all assigned.

Complexities: The outer loop d from M down to 1 is up to 1e6 iterations. In each iteration, we iterate over multiples m = d, 2d, ... <= M. The total number of (d,m) pairs is M * H_M ~ 14 million. For each pair, we check if pos[m] exists. If yes, we iterate over its indices and assign those with ans[idx]==0. The total number of index assignments is N (since each index assigned once). But the inner loop over indices may still iterate over indices that are already assigned? Actually we check ans[idx]==0 before assigning, so we skip already assigned indices. So the total number of times we check ans[idx] == 0 is sum over all (d,m) pairs of the number of indices in pos[m]. But we will assign each index at most once, but we may still check it many times for larger d that don't divide its value? Wait we only iterate over m that are multiples of d. For a given index i with value v = A_i, we will consider d in descending order. For each d that divides v, we will have a pair (d,m=v) where m = v. So for each divisor d of v, we will examine that index. Since we iterate d descending, the first divisor d that satisfies cnt[d] >= K will assign the index. After assignment, for smaller d, we will still encounter the same index (since v is a multiple of smaller d as well) and we will skip because ans[idx] != 0. So each index may be examined for each divisor of its value, which is exactly τ(v). So total number of index checks (i.e., the inner loop iterations over indices) is sum_i τ(A_i) ≈ up to 288 million worst-case. That's the same as before. So the algorithm is essentially the same as enumerating divisors per index, but with the overhead of iterating d and multiples. However we can reduce the number of index checks by early break when remaining==0, but that only stops after all indices assigned. In worst-case (K=2, many indices need to be assigned at small d), we may still process many d and multiples.

But we can further optimize: For each d, we can skip multiples m for which pos[m] is None. That's already done. But we still need to iterate over m in steps of d. That's about 14 million steps. That's fine. The heavy part is the index checks.

Now, can we reduce the number of index checks? The sum of τ(A_i) is inevitable because each divisor must be considered for each index to find the maximum. However we can attempt to compute the answer per index using a different method: For each d, we can assign all indices that have d as a divisor and for which no larger divisor with count >= K divides them. This is exactly what we are doing. The number of assignments is N. The number of checks is sum_i τ(A_i). So we cannot avoid that in worst-case.

But we can attempt to reduce the constant factor. 288 million simple operations in Python may be too slow (maybe 10 seconds). However typical time limit is 2 seconds. We need a faster approach.

We need to find a more efficient method.

Let's think deeper: The problem is to compute for each i, max_{d | A_i, cnt[d] >= K} d. This is similar to "for each element, find the largest divisor that appears at least K times in the whole array." This is reminiscent of problems where we compute the answer for each position by processing values in decreasing order and using a union-find or something? But here we have divisibility, not adjacency.

We can think of it as: For each possible d, we can find the set of indices i where d | A_i. Then the answer for i is the maximum d in that set such that cnt[d] >= K. This is essentially a "max over divisors with a condition". The condition depends only on d, not on i. So we can precompute for each d whether cnt[d] >= K. Then for each i, we need the max divisor of A_i among those d.

This is a classic problem that can be solved by precomputing for each value v the largest divisor d of v such that cnt[d] >= K. Since v <= 1e6, we can compute an array best[v] for all v. Then answer for i is best[A_i].

We can compute best[v] using a sieve-like approach: For each d where cnt[d] >= K, we want to set best[m] = max(best[m], d) for all multiples m of d. Since we process d in increasing order, we can set best[m] = d if best[m] is not set yet? Actually we need the largest d, so we should process d in decreasing order and set best[m] = d if not already set. But we can also process d in increasing order and update best[m] = max(best[m], d). Since we only need the maximum, processing in increasing order and taking max works: for each d with cnt[d] >= K, for each multiple m: best[m] = max(best[m], d). At the end, best[m] will be the maximum d that divides m and satisfies cnt[d] >= K (since we processed all d). This is O(M log M) time and O(M) memory.

But we need to be careful: We need to iterate over multiples of d, but we can skip those m where best[m] already equals the maximum possible (which is m itself). However we can just do the full loops.

Complexities: For each d, we iterate over multiples m = d, 2d, ..., M. The total number of pair iterations is M * H_M ≈ 14 million. For each such pair, we do a max operation and assignment to best[m] (which is a Python int). That's about 14 million operations, which is fine. Then for each index i, answer = best[A_i] (O(1)). So total time is O(M log M + N). M=1e6, N=1.2e6, total ~15 million loops, which is definitely fast in Python.

Wait, is it correct? Let's test: For each d with cnt[d] >= K, we iterate over multiples m of d, and set best[m] = max(best[m], d). At the end, best[m] is the largest divisor d of m such that cnt[d] >= K. Since we processed all d, and we take max, yes. This is essentially the same as the earlier method but we compute best per value rather than per index. Since values are bounded by 1e6, this is efficient.

But we need to ensure we don't process d where cnt[d] < K to avoid unnecessary loops. However we can just check condition and skip if false. The number of d with cnt[d] >= K may be large for small K (like 2). For K=2, many d may have at least 2 multiples. But we still need to process them. The total number of pairs (d,m) where cnt[d] >= K and d|m is at most M * H_M, but we will skip many if cnt[d] < K. However for K=2, the number of d with cnt[d] >= 2 is also large. Let's approximate: For each d, cnt[d] = sum_{multiple m} freq[m]. For random frequencies, expected cnt[d] ~ N * (1/d) (if uniform). For N=1.2e6, cnt[d] >= 2 holds for d up to about N/2 = 6e5? Actually if frequencies are uniform 1 per value, cnt[d] = floor(M/d). For M=1e6, cnt[d] >= 2 when M/d >= 2 => d <= M/2 = 5e5. So about 500k values of d have cnt >= 2. That's many. So we would process d from 1 to 5e5, and for each d iterate over multiples. The total number of pairs for d <= M/2 is about M * (1/1 + 1/2 + ... + 1/(M/2)) = M * (ln(M/2) + gamma) ≈ 1e6 * (ln 5e5 ≈ 13.12) ≈ 13 million. So still around 14 million. So it's okay.

Thus the best per value approach is efficient.

Implementation details:

- Input N, K.
- Read A list of N ints.
- Determine M = max(A) maybe 10^6 (given). We can set M = 10**6 (or 1_000_000). But we can also set M = max(A) to reduce loops. However we need to compute cnt for all d up to M. But for d > max(A), cnt[d] = 0 (since no element equals multiple > max(A) except maybe 0). Actually if d > max(A), the only multiple <= max(A) is none, so cnt[d] = 0. So we can restrict loops to M = max(A). But we also need to consider that best array size M+1. That's fine.

- Build freq array of size M+1: freq = [0]*(M+1). For each a in A: freq[a] += 1.

- Build cnt array of size M+1: cnt = [0]*(M+1). For d in range(1, M+1): sum = 0; for m in range(d, M+1, d): sum += freq[m]; cnt[d] = sum.

But we can compute cnt using a sieve: for d in range(1, M+1): for m in range(d, M+1, d): cnt[d] += freq[m]. This is O(M log M). We can also do: for m in range(1, M+1): if freq[m] > 0: for d in divisors of m? That would be similar to enumerating divisors per element, which is sum τ(A_i) ~ 14 million, also okay. But we need to compute cnt for all d, not just those with freq>0. The typical approach is to iterate d from 1 to M and for each multiple m add freq[m] to cnt[d]. That is straightforward.

Potential optimization: Use range with step d. In Python, range(d, M+1, d) is efficient.

Now we have cnt.

Now we need best array: best = [0]*(M+1). We'll process d from 1 to M (or descending?). Since we need max, we can process d from 1 to M and do best[m] = max(best[m], d) if cnt[d] >= K. This ensures that after processing all d, best[m] is the maximum d that divides m and satisfies condition. Since we process in increasing order, we can assign max. However we need to ensure that we don't process d that doesn't satisfy condition. So:

for d in range(1, M+1):
    if cnt[d] >= K:
        for m in range(d, M+1, d):
            if best[m] < d:
                best[m] = d

But we can also skip the if check if we just assign best[m] = d (since d increases, we can just assign best[m] = d, as later d will be larger and overwrite). However we need to ensure we only assign when cnt[d] >= K. So we can just do best[m] = d (no condition). Since we only enter the loop when cnt[d] >= K. That works: best[m] will be set to d (the current d) and later larger d (if also satisfies) will overwrite. So we can do:

for d in range(1, M+1):
    if cnt[d] >= K:
        for m in range(d, M+1, d):
            best[m] = d

But careful: best[m] should be the maximum d that divides m and satisfies condition. If we process d in increasing order, we will assign best[m] = d for each d that divides m and satisfies condition, and finally best[m] will be the largest d (since we overwrite). So it's correct.

Now we need to consider K=1: For K=1, condition cnt[d] >= 1 holds for any d that appears (freq[d] > 0). But also for d that doesn't appear, cnt[d] = 0. The best[m] will be set to the largest divisor d of m such that freq[d] > 0. But we need the largest divisor d of m with freq[d] > 0. Since m itself appears (freq[m] > 0), best[m] = m. So answer is m. So we can just use the same algorithm for K=1, but we need to ensure that for d > max(A) we don't have cnt[d] >= 1 (since freq[d] = 0). So best[m] will be max divisor of m that appears in the array. Since m appears, best[m] = m. So it's fine. So we can treat K=1 uniformly.

But we need to handle K > N? Actually K <= N, given. So fine.

Now we need to output ans_i = best[A_i] for each i.

Complexities: O(M log M + N). M up to 1e6, N up to 1.2e6. O(1e6 * log 1e6) ~ 14 million loops for cnt computation, plus another 14 million for best computation. That's ~28 million loops. Each loop is simple integer addition/comparison. Should be fast in Python (< 1 sec maybe 2). However we need to be careful with constant factors. The inner loops for best may be a bit heavy because we are writing best[m] for each pair (d,m). That's also about 14 million assignments. That's okay.

But we also need to compute cnt: For each d, we iterate m multiples. That's also about 14 million. So total loops ~28 million. Should be okay.

But we also need to handle memory: best array of size M+1 (1e6+1) of ints. That's 28 MB if list of ints. We can use array('I') to reduce memory, but maybe not needed. Let's compute memory: freq (list of ints) 28 MB, cnt (list of ints) 28 MB, best (list of ints) 28 MB, A (list of ints) 28 MB. That's 112 MB. That's okay.

But we can also avoid storing freq and cnt separately: we can compute cnt directly into cnt array, and then reuse freq array for something else? Actually we need freq only for building cnt. After building cnt, we can delete freq to free memory. So we can have freq = [0]*(M+1). Build freq. Then compute cnt using freq, then optionally del freq. Then compute best using cnt. Then output.

Thus memory at peak: freq (28 MB) + cnt (28 MB) + best (28 MB) + A (28 MB) = 112 MB. Plus overhead for list objects (the list itself). That's fine.

Now we need to consider the time to compute cnt. The double loop is:

for d in range(1, M+1):
    s = 0
    for m in range(d, M+1, d):
        s += freq[m]
    cnt[d] = s

We can micro-opt: use local variables for speed: M1 = M+1, freq_local = freq, cnt_local = cnt. Use range(d, M1, d). The inner loop is about 14 million iterations. That's fine.

But we also need to consider that M can be as large as 1e6, and we have N up to 1.2e6. So total time should be okay.

Potential pitfalls: The answer for each i is the largest divisor d of A_i with cnt[d] >= K. However we must consider that we need to select K elements that include A_i, not necessarily distinct? The problem says "choose K elements from A that include A_i". It doesn't say they have to be distinct indices, but usually "choose K elements" means choose K distinct elements (since it's a set). In sample 1, they choose two distinct indices. So we assume distinct positions. Our condition requires at least K elements divisible by d in the whole array (including the chosen A_i). That matches.

Edge Cases: K = N. Then we need to select all elements. The GCD of all N elements must include A_i. The answer is gcd of all elements that include A_i. That is the GCD of the whole array (since we must include all). Our condition: we need the largest divisor d of A_i such that at least N elements are divisible by d. Since there are N elements total, cnt[d] >= N means d divides all elements. So the answer is the GCD of all elements (which divides A_i). That is correct. So algorithm works.

Now we need to ensure we handle large N and K correctly.

Let's test with sample.

We'll implement in Python.

But we need to be careful about reading input fast. Use sys.stdin.buffer.read() to read all and split.

Implementation steps:

1. import sys.
2. data = sys.stdin.buffer.read().split()
3. N = int(data[0]); K = int(data[1]); A = list(map(int, data[2:]))
4. M = max(A)  # or 10**6
5. freq = [0]*(M+1)
   for a in A: freq[a] += 1
6. cnt = [0]*(M+1)
   for d in range(1, M+1):
       s = 0
       for m in range(d, M+1, d):
           s += freq[m]
       cnt[d] = s
   # optional: del freq
7. best = [0]*(M+1)
   if K == 1:
       # best[a] = a for all a in A? Actually we can just compute best same as general.
       pass
   for d in range(1, M+1):
       if cnt[d] >= K:
           # iterate multiples
           step = d
           # Use local variables
           best_local = best
           for m in range(d, M+1, step):
               best_local[m] = d
   # However, note that for d where cnt[d] < K, we skip.
   # At the end, best[m] will be the largest d that divides m and satisfies condition.
   # For values m that have no divisor d with cnt[d] >= K, best[m] will remain 0. But there is always d=1 (since cnt[1] = N >= K). So best[m] will be at least 1.

8. Output each A_i: for a in A: print(best[a]).

But we need to be careful: In the best computation loop, we are iterating d from 1 to M. For each d satisfying condition, we set best[m] = d for all multiples m. Since d is increasing, later d will overwrite earlier smaller d. This works.

But we need to ensure we don't exceed time due to large loops. Let's approximate:

M = max(A). In worst-case, M = 10^6.

Number of pairs (d,m) where d|m and d <= M is M * H_M ~ 1e6 * 14.39 ≈ 14.39 million. That's for each of the two loops (cnt and best). So total ~28.8 million inner loop iterations. Each iteration does a simple operation (addition or assignment). That's fine.

But we also have to consider the overhead of Python loops. 28 million loops may be okay (maybe 0.5 sec per million? Actually Python can do about 30-50 million simple loop iterations per second? Let's estimate: a for loop with range and a simple addition may take about 0.1 microsecond per iteration? Actually typical Python speed: about 50 million simple operations per second is unrealistic; more like 20-30 million simple operations per second? Not sure. Let's approximate: 1e7 operations ~ 0.2 sec? Actually Python can do about 1e7 simple integer additions per second? Let's test mental: a loop of 10 million with a simple addition may take ~0.5 sec. So 28 million may take ~1.5 sec. That's okay.

But we also have reading input and building arrays, which also take time.

Thus this approach should be fast enough.

But we need to be careful about memory and time for building cnt. The double loop for cnt may be slower because we have a sum variable and we add freq[m] each iteration. That's similar to best loop. So total loops ~28 million.

Now we need to ensure that we handle the case K > N? Not allowed.

Edge Cases: If K > N, not possible.

Now let's test with sample.

We'll implement the solution in Python.

But we need to ensure that we don't overflow recursion or memory.

Let's implement.

Potential improvements: We can combine the two loops: we can compute cnt and best in one pass? Actually we need cnt before best. So two passes.

But we can also compute best directly from freq without cnt? We need cnt[d] >= K condition. We could compute best by scanning d from M down to 1 and using a data structure to assign answers to multiples. But the current approach is simple.

We need to be careful about the case K > N? Not needed.

Now we need to handle large N and M efficiently.

Potential issue: In the best loop, we are assigning best[m] = d for all multiples m. However we also need to consider that for values m that are not in the array (i.e., not in A), we still compute best[m] but we don't need them. However we need best for values that appear in A. We can restrict best to only values in A to reduce loops? Not necessary.

But we can restrict best computation to only values that appear. However we don't know which values appear ahead of time without scanning. We can after building freq, we can iterate over d and for each multiple m, if freq[m] > 0, then assign. That would reduce number of inner iterations. Let's see: For each d, we iterate over multiples m. If we check if freq[m] > 0 before assigning, we still need to iterate over all multiples, but we skip assignment. That still does the loop over multiples, which is the heavy part. The heavy part is the iteration over multiples, not the assignment. So we cannot avoid iterating over multiples.

But we can avoid the inner loop for d that have cnt[d] < K. So we only do inner loops for d that satisfy condition. That's already done.

Now, we can also break early if we have assigned all values? But we are assigning best for all values up to M, not just those in A. But we only need best for values in A. However we don't know which values are in A for each d. We could maintain a set of values that are not yet assigned? Not needed.

Thus the algorithm stands.

Now we need to verify correctness for K=1: For each d, cnt[d] >= 1 if freq[d] > 0. For d that do not appear, cnt[d] = 0, so we skip. For d that appear, we assign best[m] = d for all multiples m. Since we process d in increasing order, for each m, the largest d that appears and divides m will be assigned last, which is the answer. Since m appears, d=m will be processed (since freq[m] > 0 => cnt[m] >= 1). So best[m] = m. So answer is m. Good.

Now for K > 1, same.

Thus algorithm is correct.

Now we need to code efficiently.

Potential memory/performance improvements: Use array module for freq, cnt, best. But we can just use lists.

Potential speed-ups: Use local variables in loops: M1 = M+1; freq_local = freq; cnt_local = cnt; best_local = best.

Now we need to handle reading input. Use sys.stdin.buffer.read() and map to ints.

Potential pitfalls: The max value M may be less than 10^6, but we can allocate arrays of size M+1. That's fine.

Now we need to think about the case where M is small (like 1). Then loops are trivial.

Now we should test with the sample.

Let's code in Python.

Implementation details:

def solve():
    import sys
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    M = max(A) if A else 0
    freq = [0]*(M+1)
    for a in A:
        freq[a] += 1
    cnt = [0]*(M+1)
    # compute cnt
    # Use local variables for speed
    M1 = M+1
    freq_local = freq
    cnt_local = cnt
    for d in range(1, M1):
        s = 0
        # using range with step d
        for m in range(d, M1, d):
            s += freq_local[m]
        cnt_local[d] = s
    # Now compute best
    best = [0]*(M1)
    best_local = best
    if K == 1:
        # We could just set best[a] = a for each a in A and skip loops.
        # But we can also reuse the general method, but it's fine.
        # Let's just fill best with values from A? Actually we need best for each value up to M. We can set best[a] = a.
        # But we also need best for values that may not appear? Not needed.
        # However we can just compute best using general method, which will be correct.
        pass
    for d in range(1, M1):
        if cnt_local[d] >= K:
            # assign to multiples
            # We can use step = d
            for m in range(d, M1, d):
                best_local[m] = d

## worker: Implement the O(M log M) solution: compute `cnt[d]
The solution uses the observation that the GCD of a K‑element subset containing A_i must be a divisor d of A_i, and such a subset exists iff at least K elements of the whole array are multiples of d.  
We precompute for every possible d (1 ≤ d ≤ max A_i) the count of array elements divisible by d using a classic sieve over the frequency array. Then we determine, for each value v, the largest divisor d of v with cnt[d] ≥ K by scanning d in increasing order and overwriting `best[m] = d` for all multiples m when the condition holds. Since d increases, the final value stored in `best[v]` is the maximum required divisor. Finally we answer each query with `best[A_i]`.  
Complexities:  
- Building `cnt` costs O(M log M) ≈ 1.4·10⁷ operations for M = 10⁶.  
- Building `best` also costs O(M log M).  
- Answering each of the N queries is O(1).  
Memory usage is O(M + N) (a few integer arrays and the input), well within typical limits.  
The algorithm handles K = 1 correctly because every element itself satisfies the condition, so `best[a]` becomes a.

## worker: Implement the O(M log M) solution in Python: read 
The solution works as follows:

1. For each index `i` the required GCD must be a divisor `d` of `A[i]`, and such a subset exists iff at least `K` elements of the whole array are multiples of `d`.  
2. We pre‑compute `cnt[d]` for all `d` up to `max(A)` using a sieve over the frequency array: `cnt[d] = Σ_{m multiple of d} freq[m]`. This takes `O(M log M)` operations (≈ 1.4·10⁷ for `M=10⁶`).  
3. We then compute `best[v]` – the largest divisor `d` of `v` with `cnt[d] ≥ K`. This is done by scanning `d` in increasing order and, whenever the condition holds, writing `d` into `best[m]` for every multiple `m` of `d`. Since `d` grows, the final value stored in `best[v]` is the maximum possible divisor.  
4. Finally, for each element `A[i]` we output `best[A[i]]`.  

The algorithm runs in `O(M log M + N)` time and uses `O(M + N)` memory, well within the limits for the given constraints.

## worker: Compute divisor counts `cnt[d]` for d=1..maxA by s
The solution uses the divisor‑count observation: the GCD of any K‑element subset containing A_i must be a divisor d of A_i, and such a subset exists iff at least K elements of the whole array are multiples of d.  
We pre‑compute `cnt[d]` (the number of array elements divisible by d) with a classic sieve over the frequency array, then for each value v we store the largest divisor d with `cnt[d] ≥ K` by scanning d in increasing order and overwriting `best[m] = d` for all multiples m. Finally we answer each query with `best[A_i]`.  
Complexities: O(M log M) time for the two sieves (≈ 1.4·10⁷ operations for M = 10⁶) and O(N) for output, with O(M + N) memory. This handles all K values, including K = 1, correctly.

## worker: finalize
The solution uses the key observation: for any K‑element subset that includes `A_i`, its GCD must be a divisor `d` of `A_i`. Such a subset exists iff at least `K` elements of the whole array are multiples of `d`.  

We first compute `cnt[d]` for all `d` up to the maximum element using a classic sieve over the frequency array. This is `O(M log M)` (≈ 1.4·10⁷ operations for `M = 10⁶`).  

Then we determine, for each value `v`, the largest divisor `d` of `v` with `cnt[d] ≥ K`. We scan `d` in increasing order and, whenever the condition holds, write `d` into `best[m]` for every multiple `m` of `d`. Since `d` grows, the final value stored in `best[v]` is the maximum possible divisor. This also costs `O(M log M)`.  

Finally, each query is answered in `O(1)` time by `best[A_i]`.  

The algorithm runs in `O(M log M + N)` time and uses `O(M + N)` memory, well within the limits for `N ≤ 1.2·10⁶` and `M ≤ 10⁶`. It handles all values of `K` (including `K = 1`) correctly.
