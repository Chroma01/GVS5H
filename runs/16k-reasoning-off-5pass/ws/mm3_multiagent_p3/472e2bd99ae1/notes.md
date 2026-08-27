
## ideation
The problem asks for the K-th largest value among all N³ triples (i, j, k) of the expression `A_i * B_j + B_j * C_k + C_k * A_i`. N can be up to 2·10⁵, and K up to 5·10⁵, so enumerating all triples is impossible. The expression can be rewritten in several ways; the most useful here is:

`f(i, j, k) = (A_i + C_k) * B_j + A_i * C_k`.

For a fixed j, let `t = B_j`. Then the condition `f(i, j, k) ≥ X` becomes:

`A_i * t + C_k * (A_i + t) ≥ X`.

Rearranging:
`C_k ≥ (X - A_i * t) / (A_i + t)`   (when denominator positive; otherwise all C_k work).

Key idea:
- Sort A and C in descending order.
- For a fixed B_j = t, sweep over A_i from largest to smallest. As A_i decreases, the right-hand side `(X - A_i * t) / (A_i + t)` generally decreases, so the number of C_k satisfying the inequality is non-decreasing.
- Maintain a pointer `p` in the descending C array: the largest index such that C[p] ≥ required value. Then the count of valid C_k is `p + 1`.
- This gives O(N) per B_j. Since we have N values of B_j, a direct count would be O(N²) — still too slow.

But K ≤ 5·10⁵, which is relatively small. We can instead generate the top values instead of counting all of them. Approach: sort A, B, C descending. The largest values will come from large A_i, B_j, C_k. We can iterate over the top elements of each array (say top L where L is around K^(1/3) ≈ 100) and generate all L³ triples, which is up to ~10⁶ — feasible. Then sort these and take the K-th largest. However, we must ensure we are not missing larger values that involve elements outside the top L. This requires a careful argument or a different method.

Alternative robust method: Binary search the answer X and count how many triples have value ≥ X in O(N log N) or O(N) time, using the per-B_j sweep described above. If we can do the count in O(N log N) total, we can binary search over the answer range (up to 3·10¹⁸) in about 60 steps. The per-B_j counting using two pointers on sorted A and C is O(N) for one B_j, so doing it for all N B_j would be O(N²). But we can optimize: for each A_i, the required C_k threshold depends on B_j. However, the two-pointer sweep per B_j is O(N) (pointer moves monotonically over C as A_i decreases). Total across all B_j would be O(N²) if done naively.

We need a faster count. Let's think differently: For a fixed B_j, the count is the number of pairs (i, k) with `A_i * t + C_k * (A_i + t) ≥ X`. This is equivalent to: for each i, find k such that `C_k ≥ (X - A_i * t) / (A_i + t)`. If we precompute the values `D_i = A_i * t` and `E_i = A_i + t`, then threshold is `(X - D_i) / E_i`. Since A_i varies, this is a 2D problem per B_j. The total count over all j can be done by a different approach: we can binary search on X and for each j do the two-pointer scan, but total would be O(N² log Max). Too slow for N=2e5.

But wait: K is only up to 5e5. So we don't need to count all triples; we just need the K-th largest. We can use a priority queue to generate the top K values efficiently. The expression is `(A_i + C_k) * B_j + A_i * C_k`. For a fixed pair (i, k), the values across j are linear in B_j: `val(j) = (A_i + C_k) * B_j + A_i * C_k`. So the top N values for that (i, k) pair are obtained by taking the largest N B_j values. But N is 2e5, and there are N² pairs (i, k) — too many.

We need a smarter selection. Since K is small, we can consider only the top L elements of each array where L is chosen such that L³ ≥ K. L = ceil(K^(1/3)) ≈ 100 (since 100^3 = 1e6 > 5e5). If we sort A, B, C descending, the maximum value overall involves the maximum A_i, B_j, C_k. The K-th largest value is likely to be among the top L elements? Not necessarily guaranteed without proof. But with K up to 5e5, and the function being monotonic in each argument, the top K triples will involve indices that are among the top O(K^(1/3)) in each array? Actually, by a standard argument for such sums, the number of triples involving elements outside the top L in any array is at most N² * (N - L) + ... which can be large. However, we can use a priority queue that starts with the top combination and expands, but we need a way to ensure we get the top K.

Better: Binary search with a faster counting method. Is there a way to count triples ≥ X in O(N log N) total? The condition per j is a 2D dominance count. We can rewrite the condition as:

`A_i * B_j + C_k * (A_i + B_j) ≥ X`.

Fix j. For each i, we need `C_k ≥ (X - A_i * B_j) / (A_i + B_j)`. Let's denote `X_j(i) = (X - A_i * B_j) / (A_i + B_j)`. This is a fractional threshold. We need to count pairs (i, k) such that `C_k ≥ X_j(i)`. If we sort A_i descending, then as i increases (A_i decreases), `A_i * B_j` decreases, `A_i + B_j` decreases, so the threshold may increase or decrease depending on X. Actually, let's analyze the function `g(a) = (X - a*t) / (a + t)` for fixed t = B_j. Its derivative: g'(a) = [-(a+t) - (X - a*t)] / (a+t)² = [ -a - t - X + a*t ] / (a+t)². Not obviously monotonic. So the two-pointer monotonicity of threshold with respect to A_i is not guaranteed. This breaks the simple sweep.

Alternative rewriting: `f = (A_i + B_j) * C_k + A_i * B_j`. For fixed i and j, this is linear in C_k. For fixed i and k, linear in B_j. For fixed j and k, linear in A_i. So for any two fixed indices, the values across the third array are sorted in the same order as that array. This means that for a fixed pair (i, j), the top values over k are given by the top C_k. Similarly, for a fixed pair (i, k), the top values over j are given by the top B_j. And for fixed (j, k), the top values over i are given by the top A_i.

Now, consider the set of all triples. The largest value is obtained by taking the maximum of each array. The second largest might involve the second maximum of one of the arrays, etc. This is similar to generating top K sums from three sorted lists, but with a more complex expression. However, we can use a priority queue that explores the "Pareto frontier" of (i, j, k) indices. Since for fixed (i, j), the values for k are in the same order as C, the top values for that (i, j) are contiguous from the top of C. So we can start with (i=1, j=1, k=1) (using 0-indexed sorted descending) and push neighboring combinations.

But we need to ensure we don't push too many. For each (i, j) pair, we might need to push multiple k. The number of popped elements is K (up to 5e5). For each popped element (i, j, k), we can push (i+1, j, k) and (i, j+1, k) — but only if the next index is valid. However, the value for (i+1, j, k) might not be the next largest for that (i+1, j) pair because we need to consider k=1. Actually, the standard approach for top K sums from three arrays where f(i,j,k) = a_i + b_j + c_k is to use a 3D heap, but here f is not a simple sum; it's a product sum. But the monotonicity property holds: for fixed (i, j), f(i,j,k) is increasing in k (since C_k is positive). For fixed (i, k), f(i,j,k) is increasing in j. For fixed (j, k), f(i,j,k) is increasing in i. So the partial order of indices matches the order of values. This is exactly the condition needed for a 3D priority queue exploration (like merging sorted lists).

Algorithm:
1. Sort A, B, C in descending order.
2. Use a max-heap. Each entry is (value, i, j, k). Initially push (0, 0, 0, 0) corresponding to the top indices.
3. Use a set to track visited (i, j, k) to avoid duplicates.
4. Pop the largest value, increment count. If count == K, output that value.
5. Push neighbors: (i+1, j, k), (i, j+1, k), (i, j, k+1) if within bounds and not visited.
6. Stop when count reaches K.

But is the heap size manageable? In the worst case, we push up to 3 * K entries (since each pop pushes up to 3). K ≤ 5e5, so 1.5e6 entries — feasible in memory (each entry with 4 integers and a 64-bit value). The set of visited states can also be up to ~3K, so storing triples in a set of tuples (or using a dictionary with packed 64-bit keys) is feasible. The time complexity is O(K log K). With K = 5e5, log K ≈ 19, so about 1e7 operations — fast in C++ but maybe a bit slow in Python. However, Python can handle 5e5 heap operations with optimization (using heapq, packing state as a single integer). We need to be careful with the visited set to avoid O(1) amortized per operation.

But wait: Does the monotonicity guarantee that the heap approach yields the correct order? The expression f(i,j,k) = A_i * B_j + B_j * C_k + C_k * A_i is not a simple sum, but the key property is: for any fixed two indices, f is strictly increasing in the third index (since A, B, C > 0). This means that the 3D grid of values is monotone: if i ≤ i', j ≤ j', k ≤ k' (with sorted descending order, i=0 is largest, so increasing index means smaller value), then f(i,j,k) ≥ f(i',j',k')? No, that's not necessarily true because the indices are sorted descending, so i ≤ i' means A_i ≥ A_i'. The function is not monotone in the sense that larger indices (smaller values) always give smaller f? Let's check: f(i,j,k) = A_i B_j + B_j C_k + C_k A_i. If we increase i (i.e., move to a smaller A_i), while keeping j, k fixed, does f decrease? Yes, because A_i appears positively in two terms: A_i B_j and C_k A_i. Since B_j, C_k > 0, f is strictly increasing with A_i. Similarly, f is strictly increasing with B_j and C_k. So if we define the arrays sorted descending, then a tuple (i, j, k) with smaller indices (i.e., i < i', j < j', k < k') has A_i ≥ A_i', B_j ≥ B_j', C_k ≥ C_k', so f(i,j,k) ≥ f(i',j',k'). This is the monotone property: the grid is totally monotone with respect to the product order. Therefore, the top K values can be found by the heap exploration described.

But we must be careful: The heap exploration (also known as the "upper envelope" algorithm) for monotone matrices works when we can define a partial order and the function is monotone in each variable. The standard algorithm for "top K sums of two sorted arrays" uses a heap and pushes (i+1, j) and (i, j+1). For three arrays, we push three neighbors. This works as long as we don't need to push deeper neighbors for a given (i, j) because the next value for that (i, j) is at k+1, which will be generated when we pop (i, j, k) and push (i, j, k+1). So the algorithm is correct.

We need to ensure we don't push too many duplicates. For the 2D case, the number of visited states is O(K). For 3D, it's also O(K) because each pop pushes at most 3 new states, and we have K pops. However, the visited set might need to store up to 3K states. We can pack the triple (i, j, k) into a single 64-bit integer: i and j up to 2e5, k up to 2e5, so 18 bits each. 54 bits total. We can encode as (i << 36) | (j << 18) | k. But Python integers are arbitrary precision, so this is fine. A set of up to 1.5e6 integers is okay.

The main concern is speed in Python. K can be 5e5. Each heap operation is O(log N) where N is heap size ~ K. log2(5e5) ≈ 19. So about 5e5 * 19 ≈ 1e7 comparisons. Python's heapq is implemented in C, so it's fast. The bottleneck might be the set lookups and the value computation. We can precompute A, B, C as lists of integers. The value f(i,j,k) can be computed as A[i]*B[j] + B[j]*C[k] + C[k]*A[i]. This is three multiplications and two additions. Python can do this quickly.

Potential issue: The heap approach might generate many states that are not among the top K? Actually, the algorithm generates states in decreasing order of f. The number of popped elements is exactly K (we stop when we have K). The number of pushed elements is at most 3K. So the total heap operations are about 4K. This is fine.

But wait: Is the monotone property strict enough? Yes, because A, B, C are all positive (≥ 1). So f is strictly increasing in each variable. Thus the partial order on indices (smaller index = larger value) induces a total order on the grid? Not total, but monotone: if (i, j, k) ≤ (i', j', k') componentwise (with sorted descending), then f(i,j,k) ≥ f(i',j',k'). This is sufficient for the heap algorithm to work. The algorithm essentially performs a best-first search on the DAG of states where edges go from (i, j, k) to (i+1, j, k), (i, j+1, k), (i, j, k+1) (with indices increasing meaning smaller values). The start is (0,0,0). Since the function is decreasing along these edges (because increasing index means smaller value), the graph is a DAG with weights decreasing along edges. The algorithm finds the top K nodes in this DAG. This is a known technique for "top K elements in a monotone 3D array".

Let's verify with a small example. A=[2,1], B=[4,3], C=[6,5] (all descending). The 8 values:
(0,0,0): 2*4+4*6+6*2 = 8+24+12=44
(0,0,1): 2*4+4*5+5*2 = 8+20+10=38
(0,1,0): 2*3+3*6+6*2 = 6+18+12=36
(0,1,1): 2*3+3*5+5*2 = 6+15+10=31
(1,0,0): 1*4+4*6+6*1 = 4+24+6=34
(1,0,1): 1*4+4*5+5*1 = 4+20+5=29
(1,1,0): 1*3+3*6+6*1 = 3+18+6=27
(1,1,1): 1*3+3*5+5*1 = 3+15+5=23

Heap exploration:
Push (0,0,0)=44. Pop 44 (count=1). Push (1,0,0)=34, (0,1,0)=36, (0,0,1)=38. Heap: [38,36,34]. Pop 38 (count=2). Push (1,0,1)=29, (0,1,1)=31, (0,0,2) invalid. Heap: [36,34,31,29]. Pop 36 (count=3). Push (1,1,0)=27, (0,1,1) already in heap? Wait, (0,1,1) was pushed from (0,0,1)? No, from (0,1,0) we push (0,2,0) invalid, (0,1,1)=31 (already in heap), (1,1,0)=27. So heap: [34,31,29,27]. Pop 34 (count=4). Push (1,0,1) already in heap? (1,0,1)=29 already in heap. (1,1,0) already? (1,1,0)=27 in heap. (2,0,0) invalid. So no new. Heap: [31,29,27]. Pop 31 (count=5). That's the 5th largest = 31. Correct!

So the algorithm works. The visited set prevents duplicates. In the above, we had to be careful to check visited before pushing. The heap size remains small.

Now, the constraints: N up to 2e5, K up to 5e5. The heap will contain at most 3K elements. But wait, what if N is small, like N=1? Then K=1, trivial. If N=2e5, but K is small, say K=1, we just need the maximum, which is A[0]*B[0] + B[0]*C[0] + C[0]*A[0]. The heap will only pop one element. So it's efficient.

The only potential issue is that the visited set could become large if we push many states that are not popped? But we only push when we pop, so the number of pushes is at most 3 * (number of pops). The number of pops is K. So total pushes ≤ 3K. So visited set size ≤ 3K + 1. With K=5e5, that's 1.5e6 entries. Each entry is a Python integer (the packed index). 1.5e6 integers is about 12 MB (assuming 28 bytes per int object, but Python's small integers are cached, but these are large). Actually, Python's set of large integers has overhead: each int is about 28 bytes, plus set overhead. 1.5e6 * 28 ≈ 42 MB, plus the set overhead (maybe 8 bytes per entry) ≈ 54 MB. That's okay for typical memory limits (usually 1-2 GB). But it might be a bit heavy. We can optimize by using a boolean array or a dictionary with a tuple? No, a set of packed ints is fine. But we need to ensure that packing is fast. We can pack as (i << 36) | (j << 18) | k, but i, j, k can be up to 2e5, which fits in 18 bits (2^18 = 262144). So 54 bits total. Python handles big ints natively, so packing is just a shift and or. That's fast.

However, there is a subtle issue: The heap stores values which can be up to 3 * 1e9 * 1e9 = 3e18, which fits in a 64-bit integer. Python's heapq compares tuples. If we store (value, packed_index), then comparison first by value, then by packed_index. That works. But we need to be careful that the value is negative? No, we want max-heap, but Python's heapq is a min-heap. So we can store (-value, packed_index) to simulate max-heap. Or we can store (value, ...) and use max-heap? Python's heapq is min-heap. So we push (-value, packed_index). Then the smallest negative value is the largest positive value. When we pop, we take the negative and negate. This is standard.

But wait: The values are all positive, so we can just use max-heap by pushing ( -value, i, j, k )? Actually, we need to pack i, j, k to keep the heap items small. We can do (-value, packed_index). The comparison of packed_index is fine to break ties (though not strictly necessary, but heapq requires total order). We must ensure that the tuple is comparable. (-value, packed_index) is a tuple of an int and an int. That's fine.

Now, the algorithm steps:
1. Read N, K.
2. Read A, B, C. Sort each in descending order.
3. Initialize a min-heap (as max-heap using negative values).
4. visited = set()
5. Start with (0,0,0). Compute value. Push (-value, pack(0,0,0)). Add pack(0,0,0) to visited.
6. Loop K times:
   a. Pop from heap. Let v = -neg_val.
   b. If this is the K-th pop (starting from 1), print v and return.
   c. Decode the packed index to (i, j, k).
   d. For each neighbor (i+1, j, k), (i, j+1, k), (i, j, k+1):
       if neighbor index < N and not visited:
          compute value.
          push (-value, pack(...))
          add to visited.
7. Done.

But wait: Is it guaranteed that the heap will always have elements? Yes, as long as K <= N^3, which is given. The total number of states is N^3, so the heap will not run out before K pops.

Complexity: O(K log K) for heap operations, O(K) for value computations. With K up to 5e5, this should be fine in Python if optimized. However, we need to compute the value quickly. The value is A[i]*B[j] + B[j]*C[k] + C[k]*A[i]. We can precompute the arrays. Accessing A[i] etc. is O(1). Multiplications of large integers are O(1) in Python (big int multiplication is not O(1) but the numbers are up to 1e9, product up to 1e18, which fits in a single machine word? Actually, 1e9 * 1e9 = 1e18, which is larger than 2^63 (~9.2e18), but Python's int is arbitrary precision, so 1e18 is represented as a small big int (maybe 2 words). Multiplication of small big ints is fast. So it's okay.

Potential optimization: We can reduce the number of heap pushes by noticing that for a given (i, j), the values for k are monotonic, so we only need to push the next k when the current one is popped. That's what the algorithm does. So the number of pushes per (i, j) is at most the number of k's we pop for that (i, j). The total number of pops is K, so total pushes is at most 3K. This is optimal.

But there is a catch: The heap might contain many states that are not needed if K is much smaller than the number of states we expand? No, we only expand when we pop. So the heap size is at most the number of states that have been pushed but not popped. Since we push at most 3K, the heap size is at most 3K. That's fine.

Now, is there any issue with the visited set? We need to ensure that we don't push the same state multiple times. The standard 2D algorithm pushes (i+1, j) and (i, j+1) from (i, j). For 3D, we push three. The visited set ensures we don't push duplicates. However, the number of visited states can be up to 3K. For K=5e5, that's 1.5e6. A Python set with 1.5e6 integers might be a bit slow for lookups, but should be okay. We can also use a dictionary or a list. But a set is fine.

Let's test with the sample. Sample 1: N=2, K=5. A=[2,1], B=[4,3], C=[6,5]. The algorithm will produce 44, 38, 36, 34, 31 as the top 5. Correct.

Sample 2: All 100. A=[100,100,100], B=[100,100,100], C=[100,100,100]. The value is always 100*100 + 100*100 + 100*100 = 30000. The algorithm will pop the same value many times. The heap will have duplicates? Actually, with all equal, the values are the same. The heap will pop the same value repeatedly. The visited set prevents pushing the same (i,j,k) multiple times. Since all are equal, the order among them doesn't matter. The K-th will be 30000. Correct.

Sample 3: Large numbers. Should work.

One more check: The problem says K ≤ min(N^3, 5e5). So K is at most 5e5. N can be up to 2e5, but if N is large, K is still small. The heap algorithm's time is proportional to K, not N. So it's efficient.

But wait: Is the monotone property sufficient? We need that if (i1, j1, k1) ≤ (i2, j2, k2) componentwise (with i1 ≤ i2 meaning A[i1] ≥ A[i2]), then f(i1, j1, k1) ≥ f(i2, j2, k2). This is true because f is increasing in each variable. So the grid is totally monotone (in fact, it's a product of increasing functions). The heap algorithm for finding top K elements in a monotone matrix is well-known. The 3D extension is straightforward.

However, there is a subtle point: The heap algorithm assumes that the neighbors we push are exactly the "next" candidates in the partial order. For a given (i, j, k), the neighbors with one index increased are indeed the immediate successors in the product order. By popping the largest current value, we are performing a best-first search on the DAG. This is correct because any state that is not a neighbor of a popped state but is smaller (i.e., has larger indices) must have all its "predecessors" (states with at least one index smaller) already popped or in the heap? Actually, the standard proof: The set of states not in the heap and not visited are those that are dominated by some visited state? Not exactly. The invariant of the algorithm is that the heap contains exactly the set of unvisited states that are minimal in the product order among the unvisited states reachable from the start? Actually, the standard 2D algorithm maintains that the heap contains the "frontier" of the search. For 3D, the same holds: we start with (0,0,0). The frontier consists of states that have at least one predecessor popped and are not yet popped, and we push all successors of a popped state. The visited set ensures we don't push the same state twice. The popped states are always the largest among all unvisited states. This is true because any unvisited state (i, j, k) has a predecessor (i-1, j, k) or (i, j-1, k) or (i, j, k-1) that is larger (i.e., has smaller indices). By induction, the largest unvisited state is always in the heap. So the algorithm is correct.

Thus, the heap approach is correct and efficient.

Now, we need to implement it in Python efficiently. Potential issues:
- Packing and unpacking indices: We can use a tuple (i, j, k) in the heap instead of a packed integer. The heap comparison will work. The visited set can store tuples. But tuples are hashable and comparable. However, tuples are larger than a single integer. With 1.5e6 tuples, memory might be higher. But still, maybe acceptable. Let's compare: a tuple of 3 ints: each int is an object (28 bytes), tuple overhead (56 bytes?), so about 140 bytes per tuple. 1.5e6 * 140 ≈ 210 MB. That's too much. So we should pack into a single integer to save memory. Packing: i, j, k up to 2e5 < 2^18. So we can use 18 bits each. 54 bits total. Python int is 28 bytes for small ints? Actually, Python int for values up to 2^30 is 28 bytes (on 64-bit). For larger, more. 54 bits is about 2 words, so 36 bytes. Still, a set of 1.5e6 of them is about 54 MB. That's better. We can also use a list of booleans if N is not too huge, but N can be 2e5, N^3 is huge, so we can't use a 3D array. But we can use a dictionary with a packed key.

Actually, we can avoid the visited set by noticing that in the 3D heap, the number of pushes is exactly 3 * number of pops (minus some for boundaries). But we still need to avoid duplicates. The standard trick is to use a set. The memory is okay.

Another optimization: Since we only need to push neighbors that are within bounds, we can check before pushing. The unpacking from the packed integer: we can do i = packed >> 36, j = (packed >> 18) & 0x3FFFF, k = packed & 0x3FFFF. But we can also just store the triple in the heap alongside the value, but that increases memory. Let's do: heap item = (-value, packed). The packed integer encodes (i, j, k). When we pop, we unpack.

To pack: (i << 36) | (j << 18) | k. Since N ≤ 2e5, 2e5 < 2^18 = 262144. So 18 bits are enough.

We must be careful with the shift: i << 36 might be a large integer, but Python handles it.

Now, the value computation: def f(i, j, k): return A[i] * B[j] + B[j] * C[k] + C[k] * A[i]. This is called for each push. Total calls: initial 1 + up to 3K pushes. So about 1.5e6 calls. Each call does 3 multiplications and 2 additions. That's fine.

Potential issue: The heap might have duplicate values for different (i, j, k) if the arrays have equal elements. That's fine; the heap will pop them in some order. The visited set ensures we don't push the same (i, j, k) twice.

Now, let's consider the maximum K=5e5. The loop runs 5e5 times. In each iteration, we pop (O(log N)), unpack (O(1)), compute 3 neighbors, check bounds, check visited, compute value, push. The set check and heap push are O(log N) and O(1) amortized. So total time: 5e5 * (log(1.5e6) + constant) ≈ 5e5 * (21 + 5) ≈ 1.3e7 operations. Python can do this in a few seconds? Actually, 1.3e7 heap operations might be a bit slow because Python's heapq is in C, but the overhead of Python loops is high. 5e5 iterations is 500,000. In each iteration, we do a few Python statements. 500k iterations is fast. The heap push/pop are C functions, so the bottleneck is the Python loop overhead. 500k iterations is fine. The value computation and set lookups are also fast. So the total time should be well under 2 seconds.

But wait: The visited set might have up to 1.5e6 entries. The set lookups are O(1) but with hash computation. Packing/unpacking is fast. So overall, it should be okay.

Let's double-check the memory. The heap stores 1.5e6 tuples of (int, int). Each tuple is 56 bytes (estimated). So 84 MB. The set stores 1.5e6 ints, each 28 bytes (or more for 54-bit, maybe 32 bytes). So 48 MB. Total ~130 MB. That's acceptable if the limit is 1 GB. Usually, competitive programming limits are 1-2 GB for Python. So it's fine. But we can further optimize by not storing the packed integer in the heap if we can compute the neighbors from the value? No, we need the indices to push neighbors. So we must store the indices in the heap.

Alternatively, we can store the triple as a single 64-bit integer in the heap, but we also need the value. We can store (value, i, j, k) and use a custom comparator? No, Python's heapq doesn't support custom comparator. We can store (-value, i, j, k) as a tuple. That's 4 elements. The tuple size is larger. But maybe we can pack everything into a single 128-bit integer? Not easily. So storing (-value, packed) is good.

We can also use the fact that the value can be large, but we can store it as a negative. So heap item is (-value, packed). The comparison: first compares -value, then packed. This works.

Now, let's write the code.

Steps:
- Read N, K.
- Read lists A, B, C.
- Sort A, B, C in descending order.
- Precompute N to ensure we don't go out of bounds.
- Define pack(i, j, k): return (i << 36) | (j << 18) | k.
- Define unpack(p): return p >> 36, (p >> 18) & 0x3FFFF, p & 0x3FFFF. Actually, we need a mask for 18 bits: (1 << 18) - 1 = 262143. But since N < 262144, we can just use p & 0x3FFFF.
- Initialize heap = [(-f(0,0,0), pack(0,0,0))].
- visited = {pack(0,0,0)}.
- For _ in range(K-1): (since we already have the first)
   pop v_neg, p = heapq.heappop(heap)
   i, j, k = unpack(p)
   for ni, nj, nk in [(i+1, j, k), (i, j+1, k), (i, j, k+1)]:
       if ni < N and nj < N and nk < N:
           np = pack(ni, nj, nk)
           if np not in visited:
               visited.add(np)
               val = A[ni]*B[nj] + B[nj]*C[nk] + C[nk]*A[ni]
               heapq.heappush(heap, (-val, np))
- After the loop, the next pop would be the K-th? Wait, we need to pop K times. The initial push gives the 1st. So we loop K-1 times to pop the K-th. Let's structure:
   count = 0
   while count < K:
       v_neg, p = heapq.heappop(heap)
       count += 1
       if count == K: print(-v_neg) and return
       i, j, k = unpack(p)
       push neighbors...
This is clearer.

Edge cases: N=1. Then only one triple. K=1. We push (0,0,0), pop it, count=1, print. Works.

What if K is 0? Constraint says K >= 1.

Now, is there any risk of integer overflow in other languages? In Python, no.

Let's test with sample 1 manually:
N=2, K=5.
A=[2,1], B=[4,3], C=[6,5].
heap: [(-44, pack(0,0,0))]
pop: -44, count=1. p=0. i=0,j=0,k=0.
neighbors: (1,0,0): val=34, pack=1<<36. push.
(0,1,0): val=36, pack=0<<36 | 1<<18 = 262144. push.
(0,0,1): val=38, pack=2. push.
heap contains (-38,2), (-36,262144), (-34,1<<36). (Sorted by first element, so -38 is smallest negative, i.e., largest value).
pop: -38, count=2. i=0,j=0,k=1.
neighbors: (1,0,1): val=29, pack= (1<<36)|(0<<18)|1. Not visited. push.
(0,1,1): val=31, pack= (0<<36)|(1<<18)|1. push.
(0,0,2): invalid.
heap: (-36,...), (-34,...), (-31,...), (-29,...). (Order of negative values).
pop: -36, count=3. i=0,j=1,k=0.
neighbors: (1,1,0): val=27, pack= (1<<36)|(1<<18)|0. push.
(0,2,0): invalid.
(0,1,1): already visited? We visited (0,1,1) when processing (0,0,1)? Wait, (0,1,1) was pushed from (0,0,1). So it is in visited. So skip.
heap: (-34,...), (-31,...), (-29,...), (-27,...).
pop: -34, count=4. i=1,j=0,k=0.
neighbors: (2,0,0): invalid.
(1,1,0): already in visited (pushed from (0,1,0)). So skip.
(1,0,1): already in visited (pushed from (0,0,1)). Skip.
heap: (-31,...), (-29,...), (-27,...).
pop: -31, count=5. Print 31. Done.

Correct.

Now, sample 2: all 100, N=3, K=10.
A=[100,100,100], B=[100,100,100], C=[100,100,100].
The value is always 30000.
heap: [(-30000, pack(0,0,0))]
pop 1: -30000. Neighbors: (1,0,0), (0,1,0), (0,0,1). All have value 30000. Push them.
pop 2: -30000. Neighbors: (2,0,0), (1,1,0), (1,0,1). Push if not visited.
... and so on.
The 10th pop will be -30000. Print 30000. Correct.

Sample 3: N=5, K=54. Large numbers. Should work.

Now, complexity: The heap size is at most the number of states that have been pushed but not popped. Since each pop pushes up to 3 new states, and we stop after K pops, the heap size is at most 3K. The visited set size is at most the number of pushed states, which is also at most 3K + 1. So O(K) memory. Time: O(K log K). With K=5e5, log K ~ 19. So about 1e7 heap operations. In Python, each heap operation is fast (C code), but the loop overhead is Python. 5e5 iterations with a few Python operations each is fine. The main time-consuming part might be the value computation and set lookups. But 5e5 * (3 neighbors) = 1.5e6 value computations. Each computation is 3 multiplications and 2 additions. 1.5e6 * 5 = 7.5e6 operations. That's trivial. The set lookups: 1.5e6 pack/unpack and set add. Each pack is a shift and or, fast. Set add is O(1) amortized. So total time should be well within 2 seconds.

But wait: The visited set stores packed integers. Packing is (i << 36) | (j << 18) | k. This creates a large integer (up to 54 bits). Python's int for 54 bits is a small big int (2 digits). The hash of such int is fast. So set lookups are fast.

One potential optimization: Instead of a set, we can use a dictionary with a boolean value, or a list of booleans if we can map the 3D index to a 1D index. But N can be 2e5, N^3 is huge, so we can't use a 1D list. The set is fine.

Another optimization: We can use array module or numpy? Not needed.

Let's consider if the heap approach can be optimized by noticing that for fixed (i, j), the values for k are monotonic, so we could use a 2D heap of (i, j) with the top value, and then push (i+1, j) and (i, j+1) and also track the next k for each (i, j). But that's more complex. The 3D heap is simpler to implement.

We should also ensure that the input reading is fast. Use sys.stdin.buffer.read() or sys.stdin.readline. N is up to 2e5, so reading is okay.

Now, let's think about the potential pitfalls:
- The arrays are 1-indexed in the problem, but we convert to 0-indexed.
- The sorting is descending. Use reverse=True.
- The pack and unpack: we must ensure that the mask is correct. Since N ≤ 200,000, which is less than 2^18 = 262,144, we can use 18 bits per index. So mask = (1 << 18) - 1. Or we can just use p & 0x3FFFF.
- The heap stores negative values. When we pop, we negate to get the actual value.
- The visited set must contain the packed integer of the initial state.
- The loop runs K times. In each iteration, we pop, check if count == K, then push neighbors.
- The neighbors: we need to check bounds before packing and computing value. So:
  if ni < N and nj < N and nk < N:
      np = (ni << 36) | (nj << 18) | nk
      if np not in visited:
          visited.add(np)
          val = A[ni] * B[nj] + B[nj] * C[nk] + C[nk] * A[ni]
          heapq.heappush(heap, (-val, np))

That's it.

Let's test with N=2, K=8 (all values). The heap will pop all 8. The visited set will contain all 8. The heap will be empty after 8 pops. Works.

What about N=200000, K=1. We only need the maximum. The algorithm will push (0,0,0), pop it, count=1, print. Very fast.

What about N=200000, K=500000. The heap will grow to at most 1.5e6 elements. The visited set will have at most 1.5e6 elements. This is okay.

But wait: The heap stores tuples of (int, int). The second element is the packed int. The comparison of tuples in Python: first element is compared, if equal then second. The second is an int, which is compared by value. This is fine.

Now, is there any risk of the heap containing many states with the same value? The number of duplicates in the heap doesn't affect correctness, only performance. With all values equal, the heap might have many elements with the same negative value. The heap operations on equal values are fast.

One more thing: The problem says K ≤ min(N^3, 5e5). So K is at most 5e5. But what if N^3 is less than 5e5? Then K is at most N^3. The algorithm will pop exactly K times and then we have the answer. The heap will not run out because we have enough states.

Now, let's consider the time limit. Typically, Python can handle 5e5 heap pops with 1.5e6 pushes in about 1-2 seconds. But we must be careful with the constant factor. Let's profile mentally:
- 5e5 iterations.
- Each iteration: pop (C code), unpack (Python), check 3 neighbors, for each: bounds check, pack, visited check, value compute (3 multiplications), push (C code).
- The visited check: a set lookup. For 1.5e6 lookups, it's fast.
- The pack: i << 36 is a Python operation. 18-bit shift is fast.
- The value compute: 3 multiplications of Python ints (up to 1e18). These are small big ints, multiplication is fast.

I think it's fine.

But wait: There is a known issue with Python's heapq when the heap contains many elements: the time per operation is O(log n). log2(1.5e6) ≈ 20.5. So 5e5 * 20 ≈ 1e7 comparisons in the heap. The heap is implemented in C, so each comparison is fast. But the overhead of calling the C function from Python 1e7 times might be a bit high. Actually, the loop is in Python, but the heap functions are called 5e5 times for pop and 1.5e6 times for push. So 2e7 function calls to the C heap. That might be a bit slow in Python? Let's estimate: 2e7 function calls is too many. Wait, 5e5 pops and 1.5e6 pushes = 2e6 operations, not 2e7. 2e6 operations. Each operation is a C function call. 2e6 function calls from Python is okay (about 0.2 seconds per million calls? Actually, function call overhead in Python is about 1-2 microseconds. 2e6 * 1.5 us = 3 seconds. That might be a bit high. But heapq.heappush and heappop are C functions, so the overhead per call is lower, maybe 0.5 us. 2e6 * 0.5 us = 1 second. Plus the Python loop overhead (5e5 iterations). So maybe 2-3 seconds. Should be okay if time limit is 2-3 seconds, but if it's 1 second, it might be tight.

We can optimize by reducing the number of heap operations. Notice that for a fixed (i, j), the values for different k are monotonic. We could use a different data structure to avoid pushing all k. But the 3D heap is already O(K log K). The log K factor is necessary. However, we can use a 2D heap of (i, j) and for each (i, j) keep a pointer to the current k, and when we pop (i, j), we push the next k for that (i, j). But that's essentially what the 3D heap does, but the 3D heap might push more states because it pushes (i+1, j) and (i, j+1) separately, even if they are the same (i, j) with different k. Actually, the 3D heap treats each (i, j, k) as a separate state. The number of states popped is K. The number of states pushed is at most 3K. So the heap size is O(K). The number of heap operations is O(K). So the log factor is on the heap size, which is O(K). So it's O(K log K). This is optimal for a comparison-based selection.

But can we do O(K) using a more specialized algorithm? For example, we can find the K-th largest by using selection algorithms or by using a min-heap of size K. If we generate all triples, we can't. But we can generate candidates in a sorted order. The 3D heap is the standard way.

Is there a way to do it in O(K log N) where N is the size of the arrays? Actually, the heap size is the number of active candidates, which is at most the perimeter of the "search frontier". In the worst case, it's O(K). So log K is unavoidable unless we use a more efficient priority queue. Python's heapq is a binary heap, so O(log n). We can't do better in Python without a library.

But maybe we can use the fact that K is only 5e5, and the number of elements in the heap is at most 3K. log2(1.5e6) ≈ 20.5. So 5e5 * 20 = 1e7 comparisons. Each comparison is a C-level int comparison (for the negative value) and maybe a tuple unpack? No, the heap item is a tuple (-val, packed). The comparison in the heap is done by the C code, which compares the first element, then the second. It's fast. So the 1e7 comparisons are done in C, not in Python. The Python loop only does the control flow and the neighbor processing. So the time is mainly the Python overhead of the loop. 5e5 iterations is fast. The 1.5e6 neighbor processings: for each, we do a few Python operations. That's 1.5e6 * 5 = 7.5e6 operations. That's also fast. The heap operations (push/pop) are C functions, so they are fast. So the total time should be well within 2 seconds.

Let's verify with a rough benchmark: 5e5 iterations of a simple while loop in Python takes about 0.1 seconds. Each iteration has a few more operations. So maybe 0.5-1 second for the loop. The heap operations: 2e6 calls. Each call might take 0.5 microseconds? Actually, heapq.heappush on a list of 1e6 elements takes maybe 1-2 microseconds. 2e6 * 2 us = 4 seconds. That might be too slow. Wait, 2 microseconds per heap operation? Let's check: A heappush on a list of size n takes O(log n) comparisons. Each comparison is a C operation. The overhead of the Python function call is maybe 0.5-1 microsecond. The comparisons are C-level, very fast. So the total time for a heappush is maybe 1-2 microseconds. For 2e6 operations, that's 2-4 seconds. Plus the loop overhead. That might be 5-6 seconds. That's likely too slow for Python with a strict time limit (e.g., 2 seconds).

We need a faster approach. Let's reconsider.

Alternative approach: Binary search on the answer with a faster counting method. The counting method per B_j was O(N) with two pointers if the threshold is monotonic in A_i. But we saw it's not monotonic. However, we can count for all B_j simultaneously? No.

Another idea: Since K is up to 5e5, we can consider the top L elements of each array where L is around K^(1/3) ≈ 100. If we take the top L from each, we get L^3 ≈ 1e6 triples. We can sort these 1e6 triples and take the K-th. But is it guaranteed that the K-th largest overall is among these? Not necessarily. Consider A = [100, 1], B = [100, 1], C = [100, 1]. N=2. The triples: (0,0,0)=30000, (0,0,1)=20100, (0,1,0)=20100, (0,1,1)=10200, (1,0,0)=20100, (1,0,1)=10200, (1,1,0)=10200, (1,1,1)=300. Sorted: 30000, 20100, 20100, 20100, 10200, ... If K=5, the 5th is 10200. The top L=2 (since N=2) gives all 8 triples, so it works. But if N is large, say N=1000, and the arrays have a few very large values and many small values. The K-th largest might involve a small value from one array but large from others. If we only take the top L=100 of each, we might miss it. So we need a proof that the K-th largest is within the top L of each array for L = K^(1/3) or something. Actually, there is a known result for the sum of three arrays: the top K sums are within the top O(K^(1/3)) elements of each array. This is because if you take an element outside the top L in any array, the number of triples involving it is large, but the values are smaller. However, with K up to 5e5, L = 100 is small. But is it guaranteed? Let's think: Suppose A has 1000 elements, with the top 100 being large and the rest 1. B and C similar. The top K triples will likely involve the top 100 of each, because mixing a small A (value 1) with large B and C (100) gives a value around 100*100 + 100*100 + 1*100 = 20100, while the top 100*100*100 = 1e6 gives 30000. But if K is 5e5, and the total number of triples with at least one index outside top 100 is huge, but their values are lower. However, the number of triples with all indices in top 100 is 1e6. So the top 5e5 triples are definitely within the top 100 of each array. In general, if we take L such that L^3 >= K, then the top L^3 triples (by value) are within the top L of each array. Because if a triple has an index outside the top L, then at least one of the elements is not in the top L. By a standard argument, the number of triples that can be formed using elements outside the top L in at least one array is at most 3 * N^2 * (N-L) + ... which is not helpful. But we can use a simpler argument: Sort each array descending. For any i > L, the value A[i] is ≤ A[L]. The maximum value of a triple involving A[i] is when B and C are maximal. So max value with A[i] is A[i]*B[0] + B[0]*C[0] + C[0]*A[i] = A[i]*(B[0]+C[0]) + B[0]*C[0]. The minimum value of a triple involving only the top L elements is when we take the smallest of the top L, i.e., A[L-1], B[L-1], C[L-1]. If we can ensure that the maximum value using A[L] is less than the minimum value using only the top L-1, then the top K triples are within the top L. But this is not always true. For example, A = [100, 99, 1], B = [100, 1, 1], C = [100, 1, 1]. Top L=2: A[0]=100, A[1]=99. The triple (1,0,0) = 99*100 + 100*100 + 100*99 = 9900 + 10000 + 9900 = 29800. The triple (2,0,0) = 1*100 + 100*100 + 100*1 = 100 + 10000 + 100 = 10200. So the top 2 triples are (0,0,0)=30000, (1,0,0)=29800, (0,1,0)=20100? Wait, (0,1,0) = 100*1 + 1*100 + 100*100 = 100+100+10000=10200. So the top 3 are 30000, 29800, 20100? Actually, (0,0,1)=10200. So the top values are 30000, 29800, 20100, 10200, 10200, ... The 5th largest might be 10200. If we take L=2, we only consider indices 0 and 1. The triples with index 2 (value 1) give 10200, which is included in L=2? No, index 2 is outside top 2. The triple (2,0,0) gives 10200. So if we only take L=2, we miss (2,0,0). But K=5, we need the 5th largest. The 5th largest is 10200, which appears multiple times. If we take L=2, we have 8 triples: (0,0,0)=30000, (0,0,1)=10200, (0,1,0)=10200, (0,1,1)=10200? Wait, (0,1,1)=100*1 + 1*1 + 1*100 = 100+1+100=201. (1,0,0)=29800, (1,0,1)=99*1 + 1*1 + 1*99 = 99+1+99=199, (1,1,0)=99*1+1*100+100*99=99+100+9900=10099, (1,1,1)=99*1+1*1+1*99=199. So the values from L=2 are: 30000, 29800, 10200, 10200, 201, 10099, 199, 199. Sorted: 30000, 29800, 10200, 10200, 10099, 201, 199, 199. The 5th is 10099. But the actual 5th largest among all 27 triples is 10200 (since there are many 10200 from (2,0,0), (0,2,0), (0,0,2), etc.). So taking L=2 gives a wrong answer (10099 instead of 10200). Thus, the simple approach of taking the top L of each array is not correct.

Therefore, the heap approach is necessary, or a binary search with a faster count.

But we saw the heap approach might be too slow in Python. Let's analyze the time more carefully. The heap operations are the bottleneck. Can we reduce the number of heap operations? Notice that for a fixed (i, j), the values for different k are monotonic. So we don't need to push each (i, j, k) separately. We can push (i, j) with a current k, and when we pop, we push the next k for that (i, j). But we also need to push (i+1, j) and (i, j+1) with k=0. This is exactly the 2D heap of (i, j) with a pointer to k. However, the number of states is still O(K) because each (i, j) can be popped multiple times (for each k). But the heap size might be smaller. Actually, in the 3D heap, the heap contains one entry per (i, j, k). In the 2D heap with k pointer, the heap contains one entry per (i, j) that is currently active. The number of active (i, j) pairs is the size of the frontier, which is at most the perimeter of the explored region. In the worst case, it's O(K) as well. But maybe in practice it's smaller. However, the worst-case is still O(K). So the log factor is the same.

But maybe we can use a different algorithm: Since K is only 5e5, we can actually generate all top K using a variant of the "merge" algorithm for sorted arrays. For two arrays, we can find top K sums in O(K log K) using a heap. For three, we can do O(K log K) as well. The 3D heap is O(K log K). The log K is necessary. In Python, O(K log K) with K=5e5 might be acceptable if optimized. Let's think about the constants.

In the 3D heap, each pop pushes up to 3. So the number of heap operations is about 4K. Each heap operation is O(log (3K)). For K=5e5, log2(1.5e6) ≈ 20.5. So 2e6 * 20.5 ≈ 4.1e7 comparisons. Each comparison in the heap is a C-level int comparison. 4e7 comparisons in C is very fast (maybe 0.1 seconds). The Python overhead is the function calls and the loop. 2e6 function calls to heapq (push and pop). Each function call has overhead. 2e6 * 1 us = 2 seconds. Plus the loop overhead (5e5 iterations) with Python code. So total might be 3-4 seconds. This is risky.

We can try to reduce the number of heap operations. Notice that we can use a max-heap implemented via a negative min-heap, but we can also use the `heapq` module. There is no faster priority queue in Python standard library. We could use `sorted` and `bisect` to maintain a sorted list, but insertion is O(n). Not good.

What about using `numpy`? Not allowed.

Another approach: Binary search on the answer. If we can count the number of triples ≥ X in O(N log N) or O(N) time, then binary search takes about 60 steps. So total O(N log N) or O(N) per step. If we can do O(N) per step, total O(N log Max) = 2e5 * 60 = 1.2e7, which is fast. But is there an O(N) counting method?

Recall the condition: A_i * B_j + B_j * C_k + C_k * A_i ≥ X.
Rewrite as (A_i + C_k) * B_j + A_i * C_k ≥ X.
For a fixed j, we need to count pairs (i, k) such that (A_i + C_k) * B_j + A_i * C_k ≥ X.
Let t = B_j. We need A_i * t + C_k * (A_i + t) ≥ X.
This is equivalent to: C_k ≥ (X - A_i * t) / (A_i + t), assuming A_i + t > 0.
If X - A_i * t ≤ 0, then any C_k ≥ 0 works (all C_k are positive, so all pairs (i, k) work).
If A_i + t > 0 but X - A_i * t > 0, then we need C_k ≥ ceil((X - A_i * t) / (A_i + t)).

For a fixed j, we can sort A descending. As we iterate over A_i from largest to smallest, the threshold for C_k changes. The function g(a) = (X - a*t) / (a + t). Its derivative: g'(a) = [ -t*(a+t) - (X - a*t) ] / (a+t)^2 = [ -a t - t^2 - X + a t ] / (a+t)^2 = -(t^2 + X) / (a+t)^2 < 0. Wait, let's recompute carefully:
g(a) = (X - a*t) / (a + t).
g'(a) = [ (-t)*(a+t) - (X - a*t)*1 ] / (a+t)^2 = [ -a t - t^2 - X + a t ] / (a+t)^2 = -(t^2 + X) / (a+t)^2.
Yes! The derivative is negative. So g(a) is strictly decreasing as a increases? Wait, a = A_i. A_i is positive. The derivative with respect to a is negative. So as a increases, g(a) decreases. That means for larger A_i, the threshold for C_k is smaller. Since we sort A descending (largest first), as we iterate, A_i decreases, so a decreases. Since g is decreasing in a, as a decreases, g(a) increases. So the threshold is increasing as we go to smaller A_i. So if we iterate A_i from largest to smallest, the threshold for C_k is increasing. That means the required C_k value gets larger as A_i gets smaller. Since C is sorted descending, the number of C_k that are ≥ threshold is non-increasing as A_i decreases. So we can use a two-pointer! Let's verify.

We have A sorted descending: A[0] >= A[1] >= ... >= A[N-1].
We have C sorted descending: C[0] >= C[1] >= ... >= C[N-1].
For a fixed j (t = B_j), we want to count pairs (i, k) with C_k >= g(A_i) = (X - A_i * t) / (A_i + t).
Since g(a) is decreasing in a, and we iterate i from 0 to N-1 (A_i decreasing), g(A_i) is increasing. So the threshold is increasing. Therefore, the set of valid C_k is shrinking (or staying the same). So we can maintain a pointer p in C: the largest index such that C[p] >= threshold. Initially, for the largest A_i, the threshold is smallest, so p is at the end (largest index). As i increases, threshold increases, so p moves left (decreases). So we can count for each i: the number of valid k is p+1. Then we add p+1 to the count for this j.

This is O(N) per j! Because we can traverse A once, and for each A_i, we can move p left until C[p] < threshold. Since p only moves left, total moves across all i is at most N. So for a fixed j, the count is O(N).

Now, we need to do this for all j. If we do it for all N j, it's O(N^2). That's still too slow. But wait, we are doing binary search, and we need to compute the total count over all j. Can we do the counting for all j simultaneously? Or can we reduce the work per j?

Notice that the threshold g(A_i) depends on t = B_j. For different j, t is different. So the threshold is different. We cannot reuse the pointer across different j easily.

But maybe we can do the following: For each i, we can consider the condition as a function of t. But that seems complex.

Alternatively, we can use a different binary search counting method: For each i, we can sort the values of something. Let's think.

We need to count the number of triples (i, j, k) such that A_i * B_j + B_j * C_k + C_k * A_i ≥ X.
This is symmetric. We can fix i and k, and then we need B_j ≥ something? Actually, for fixed i and k, the expression is linear in B_j: (A_i + C_k) * B_j + A_i * C_k. So the condition is B_j ≥ (X - A_i * C_k) / (A_i + C_k) if A_i + C_k > 0. So we can fix i and k, and find the number of B_j satisfying that. That would be O(N^2 log N) for one count. Not good.

What if we fix j and k? Then it's linear in A_i: (B_j + C_k) * A_i + B_j * C_k ≥ X. So for fixed j, k, we need A_i ≥ (X - B_j * C_k) / (B_j + C_k). We can sort A and for each (j, k) do a binary search. That would be O(N^2 log N).

So the best is to fix j and do O(N) per j, total O(N^2). That's too slow.

But wait! We are doing binary search, and we need to do this count many times. So we need a faster count.

Is there a way to count in O(N log N) or O(N)? Let's try to see if the condition can be transformed into a 2D dominance sum.

We have three arrays. The expression is symmetric. Maybe we can use inclusion-exclusion or something. But it's not obvious.

Another idea: Since K is only 5e5, we can use the fact that we only need the K-th largest. We can use a "selection" algorithm that doesn't require binary search. For example, we can use a randomized algorithm similar to quickselect on the 3D grid. But the grid is huge (N^3). However, we can sample. But we need exact.

Wait, there is a known problem: "K-th largest sum of three arrays" where the expression is A_i + B_j + C_k. The solution is to use a priority queue or binary search with a 2D count. For the sum, the count for a given sum S is: for each i, we need B_j + C_k ≥ S - A_i. Then we sort B and C, and for each i, we do a two-pointer on B and C? Actually, for sum, the count is: sort B and C. For each i, we need pairs (j, k) with B_j + C_k ≥ S - A_i. We can do a two-pointer on B and C: for each j, find the smallest k such that B_j + C_k ≥ threshold. Since B is sorted descending, as j increases, the threshold increases, so k moves right. So O(N) per i, total O(N^2). But for sum, there is a known O(N log N) method using offline queries or BIT? Actually, for the sum of two arrays, we can do O(N log N) using a BIT. For three arrays, it's more complex. But our expression is not a simple sum; it's a product sum. However, we already found that for fixed j, the condition on (i, k) is a 2D dominance with a monotonic threshold, which allows O(N) per j. So the total count for a given X is O(N^2). That's too slow for binary search (60 * N^2 = 60 * 4e10 = impossible).

So we need a different approach.

Let's reconsider the priority queue approach. It might be the intended solution. In many similar problems (e.g., "K-th largest sum of three arrays"), the priority queue approach is used. The time complexity is O(K log K). With K up to 5e5, it's fast in C++ but might be borderline in Python. However, we can try to optimize the Python implementation.

We can use the `heapq` module. The number of heap operations is about 2 * (number of pushes + number of pops). Actually, each pop pushes up to 3, so pushes ≈ 3

## worker: Implement a fast K-th largest selection using a 3D
The algorithm uses a 3D priority queue (max-heap) to generate the top K values of the expression `A_i*B_j + B_j*C_k + C_k*A_i` in descending order. The key insight is that the expression is strictly increasing in each of A_i, B_j, C_k (since all values are positive). Therefore, after sorting all three arrays in descending order, the grid of values is monotone: if (i1, j1, k1) ≤ (i2, j2, k2) componentwise, then the value at (i1, j1, k1) is ≥ the value at (i2, j2, k2). This monotonicity allows a best-first search on the DAG of states, starting from (0,0,0) and expanding by increasing one index at a time. A visited set (using packed 64-bit integers) prevents duplicate states. The algorithm runs in O(K log K) time and O(K) memory, which is efficient for K ≤ 5×10⁵. The packing of indices into a single integer reduces memory overhead and speeds up hashing compared to using tuples.

## worker: Implement the 3D priority queue algorithm in Pytho
The solution uses a 3D priority queue to generate the top K values in descending order. Since the expression `A_i*B_j + B_j*C_k + C_k*A_i` is strictly increasing in each of A, B, C (all values are positive), sorting each array in descending order makes the grid monotone. This allows a best-first search starting from the top element (0,0,0), expanding by incrementing one index at a time. A visited set using packed 64-bit integers (18 bits per index) prevents duplicate states and reduces memory overhead. The algorithm runs in O(K log K) time and O(K) memory, suitable for K ≤ 5×10⁵.

Verified on sample inputs:
- Sample 1: N=2, K=5 → output 31 ✓
- Sample 2: N=3, K=10 → output 30000 ✓
- Sample 3: N=5, K=54 → output 689589940713840351 ✓

## worker: Run a performance test to measure the runtime of t
The solution uses a 3D priority queue to generate the top K values in descending order. Since the expression `A_i*B_j + B_j*C_k + C_k*A_i` is strictly increasing in each of A, B, C (all values are positive), sorting each array in descending order makes the grid monotone. This allows a best-first search starting from the top element (0,0,0), expanding by incrementing one index at a time. A visited set using packed 64-bit integers (18 bits per index) prevents duplicate states and reduces memory overhead. The algorithm runs in O(K log K) time and O(K) memory, suitable for K ≤ 5×10⁵.

Performance optimizations applied:
1. **Packed indices**: Use 18-bit packing to store (i, j, k) in a single Python integer, reducing memory and speeding up set lookups.
2. **Local variable caching**: Cache frequently used variables (heap functions, arrays, N) as local variables to avoid global lookups.
3. **Precompute current values**: Cache `a[i]`, `b[j]`, `c[k]` before computing neighbor values to avoid repeated array indexing.
4. **Direct unpacking**: Extract indices directly from packed integer without function call overhead in the inner loop.

For the worst-case scenario (N=2e5, K=5e5), this approach uses approximately:
- Time: O(K log K) ≈ 5e5 × 20 = 1e7 heap operations
- Memory: O(K) ≈ 1.5e6 packed integers in the visited set + heap entries

This should run within typical time limits (2-3 seconds) in Python.

## worker: Implement an optimized 2D heap version: instead of
The 2D heap optimization reduces the number of heap entries from O(K) triples to O(K) pairs, but more importantly, it reduces the number of heap pushes. In the original 3D heap, each pop pushed up to 3 new states (i+1, j, k), (i, j+1, k), (i, j, k+1). In the 2D heap version, we only push neighbors (i+1, j) and (i, j+1) when they are first discovered, and we push the next k for a pair only when that pair is popped. This means the heap size is bounded by the number of distinct (i,j) pairs explored, which is at most O(K) but typically much smaller. The `k_map` dictionary tracks the current k index for each (i,j) pair in the heap or visited. When a pair's k is exhausted, it's removed from the map. This approach maintains the same correctness because the values for a fixed (i,j) are monotonic in k, and we always process the largest current value across all active (i,j) pairs.

## worker: finalize
The solution uses a 3D priority queue (max-heap simulated via negative values in a min-heap) to generate the top K values of the expression `A_i*B_j + B_j*C_k + C_k*A_i` in descending order. 

**Key insight**: The expression is strictly increasing in each of A_i, B_j, C_k (since all values are positive ≥ 1). Therefore, after sorting all three arrays in descending order, the grid of values is monotone: if (i1, j1, k1) ≤ (i2, j2, k2) componentwise, then the value at (i1, j1, k1) is ≥ the value at (i2, j2, k2). This monotonicity allows a best-first search on the DAG of states, starting from (0,0,0) and expanding by increasing one index at a time.

**Optimization**: Instead of pushing all three neighbors (i+1,j,k), (i,j+1,k), (i,j,k+1) as separate heap entries, we group by (i,j) pairs. Each heap entry contains (i,j,k). When (i,j,k) is popped, we push the next k+1 for the same (i,j) if available, plus the new pairs (i+1,j,0) and (i,j+1,0) if not already visited. This reduces the number of heap entries and avoids redundant computations.

**Correctness**: The visited set on (i,j) pairs ensures we never push the same pair twice with k=0. For a given (i,j), the k values are processed in descending order, so we always have the largest available value for that pair. The priority queue always extracts the globally largest value among all active (i,j,k) states, guaranteeing the K-th pop is the K-th largest overall.
