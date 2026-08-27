The expression is `A_i * B_j + B_j * C_k + C_k * A_i = (A_i + C_k) * B_j + A_i * C_k`. This is symmetric in choosing i and k (they appear as the pair (i,k) in the term `(A_i + C_k)*B_j + A_i*C_k`). 

Key insight: For a fixed j, the values across all i,k pairs are sorted by picking largest A_i and C_k, and for each pair (i,k) the expression is monotone in A_i and C_k. However the optimal approach uses a binary search on the answer X and counts how many triples produce a value >= X.

Counting method: For each j, we need to count pairs (i,k) such that `(A_i + C_k)*B_j + A_i*C_k >= X`. This is equivalent to `A_i*C_k + B_j*(A_i + C_k) >= X`. For a fixed j, sort A descending. For each i, we need C_k such that `C_k*(A_i + B_j) >= X - A_i*B_j`, so `C_k >= (X - A_i*B_j)/(A_i + B_j)`. Since A_i, B_j > 0, this is monotone — we binary search in sorted C. Sum counts for all j. Total work O(N^2 log N) might be too slow for N=2e5, but note K <= 5e5, so we can use a different approach.

Actually, the standard solution: sort A ascending, C ascending. The value `(A_i+C_k)*B_j + A_i*C_k` increases when both A_i and C_k increase. So the top K values can be found by iterating: for the largest A_i, pair it with largest C_k values, take top K, then next A_i, etc. But we need triples (i,j,k).

Better approach: binary search on value X. Count triples with value >= X efficiently. The count can be done in O(N log N) per check using the observation that for sorted A and C, we can use two pointers or binary search.

Let me reconsider: for fixed j, we want pairs (i,k) with `A_i*C_k + B_j*(A_i + C_k) >= X`. Sort A desc. For each i from largest, we binary search smallest k such that `A_i*C_k + B_j*(A_i + C_k) >= X`, i.e., `C_k*(A_i+B_j) >= X - A_i*B_j`. Since C is sorted ascending, we binary search from the right. For larger A_i, fewer C_k needed. We can use two pointers: maintain a pointer in C, but since as i decreases, A_i decreases, and the required threshold `C_k >= (X - A_i*B_j)/(A_i+B_j)` may increase or decrease. Actually as A_i decreases, denominator decreases but numerator also changes. This is complex.

Alternative efficient approach: Since K <= 5e5, and N up to 2e5, we can enumerate top K values using a priority queue. The maximum value is `max(A)*max(B) + max(B)*max(C) + max(C)*max(A)`. The expression is symmetric. We can fix i to max, then for each j, top values from k, etc. But generating top K triples where K=5e5 and N=2e5 — we need an efficient way.

Standard solution for this problem (from AtCoder ABC F or similar): binary search on X. Count how many (i,j,k) have value >= X. The counting is done in O(N^2) or O(N log N) per check? With N=2e5, O(N log N) per check is okay if number of checks is ~60. So total O(N log^2 N) or O(N^2) might be too slow.

Wait, let's think: we can fix j, and for each j, we want to count pairs (i,k) with `A_i*C_k >= X - B_j*(A_i+C_k)`. This is not easy to decouple.

Alternative: Sort A ascending. The function f(i,k) = A_i*C_k + B_j*(A_i+C_k) is increasing in both A_i and C_k. So for a fixed j, the count of pairs (i,k) with f(i,k) >= X can be computed by: for each i (sorted descending), find the smallest k such that f(i,k) >= X, then all k' >= k satisfy it. We can use binary search per i: O(N log N) per j, O(N^2 log N) total — too slow for N=2e5.

But we have K up to 5e5. This suggests a different approach: we don't need to count all, we can generate top K using a heap. 

Observation: The expression `(A_i+C_k)*B_j + A_i*C_k` is maximized when A_i, B_j, C_k are all large. Since K <= 5e5 << N^3, we can use a technique: sort A desc, B desc, C desc. The top values come from top elements. 

Specifically, we can fix i to the index of the largest A, and use a max-heap to generate top K values from triples (i,j,k). Initially, for i=1 (largest A), we push the value for (1,1,1) where j=1, k=1. Then we pop max, say (i,j,k), and push (i, j+1, k) and (i, j, k+1) if not visited. This generates top N^2 values for fixed i. We repeat for i=2,3,... until we have K values. This gives O(K log K) total. But we need to ensure we get the global top K across all i.

However, the values for different i are not easily comparable without considering all. But since for any i, the max is when j and k are max, and the values decrease as i increases (since A_i decreases, the product terms generally decrease), the global top K will mostly come from small i. But we need correctness.

Actually, a cleaner approach: binary search on the answer. Let me figure out the count efficiently.

For a threshold X, we want to count triples (i,j,k) with `A_i*B_j + B_j*C_k + C_k*A_i >= X`.
Rewrite: `B_j*(A_i + C_k) + A_i*C_k >= X`.
For fixed j, define `D = A_i + C_k` and `P = A_i*C_k`. Then `B_j*D + P >= X`, i.e., `P >= X - B_j*D`.
But P and D are related: for fixed D, max P is when A_i and C_k are as far apart as possible? No, for fixed D = A+C, max P is when one is as large as possible.

Alternatively, note that `A_i*B_j + B_j*C_k + C_k*A_i = (A_i + C_k)(B_j + C_k) - C_k^2`? No.
`= A_i*B_j + B_j*C_k + C_k*A_i = B_j(A_i+C_k) + A_i*C_k`.

Let's sort A ascending: A_1 <= ... <= A_N, and C ascending: C_1 <= ... <= C_N.
For fixed j (B_j), we want count of (i,k) with `A_i*C_k + B_j*(A_i+C_k) >= X`.
Let `u = A_i, v = C_k`. Condition: `u*v + B_j*(u+v) >= X`, i.e., `v*(u+B_j) >= X - u*B_j`, i.e., `v >= (X - u*B_j)/(u+B_j)`.
If X <= u*B_j, then any v works (all N). If X > u*B_j + u*B_j = ... wait, if X <= u*B_j, then numerator <= 0, so condition holds for all v >= 0, so all k.

So for a given j, we iterate i from N down to 1 (largest u first). For each u, compute `need = ceil((X - u*B_j)/(u+B_j))` if positive, else 1. Find number of v in C >= need using binary search. Sum over i.

This is O(N log N) per j, O(N^2 log N) total — too slow.

But we can speed up: as u decreases, need increases. So the binary search index in C (for the threshold) moves rightward. We can use a two-pointer approach: for j fixed, start with pointer at N (largest v), and as u decreases, the required v increases, so pointer moves right. Wait, as u decreases, need = (X - u*B_j)/(u+B_j). Let's analyze: let f(u) = (X - u*B_j)/(u+B_j). Derivative: f'(u) = [(-B_j)(u+B_j) - (X-u*B_j)(1)]/(u+B_j)^2 = [-B_j*u - B_j^2 - X + u*B_j]/(...) = -(B_j^2 + X)/(u+B_j)^2 < 0. So f is decreasing in u. That means as u decreases, need increases. Since C is sorted ascending, the smallest v >= need has index moving right. So we can use a pointer that only moves right as i decreases. 

But wait, we iterate i from 1 to N or N to 1? If we iterate i from 1 (smallest u) to N (largest u), need decreases as i increases, so pointer moves left. Either way, O(N) per j. Total O(N^2) — still too slow for N=2e5.

We need a better counting method. Let's think differently.

The expression is symmetric. We can binary search X, and for each X, we want to count triples. The count can be computed in O(N log N) total? Maybe using a different arrangement.

Another idea: For each i, sort C_k and B_j. The condition is `A_i*B_j + B_j*C_k + C_k*A_i >= X`. For fixed i, this is `C_k*(A_i + B_j) + A_i*B_j >= X`, i.e., `C_k >= (X - A_i*B_j)/(A_i+B_j)`. For fixed i and j, we need C_k above some threshold. We can sort j's or do 2D queries.

But maybe we can do the counting in O(N sqrt K) or something. Given K <= 5e5, the binary search needs about 60 iterations. O(N log N) per iteration is 2e5 * 60 * 17 ~ 2e8, might be borderline but possibly okay in PyPy with optimization? Let's estimate: 2e5 * 60 = 1.2e7, times log(2e5) ~ 17, is 2e8 operations — likely too slow in Python.

We need a faster counting method. Let's think about the structure again.

`val = A_i*B_j + B_j*C_k + C_k*A_i = (A_i+C_k)*B_j + A_i*C_k`.
Sort A desc, C desc. For fixed i, as k increases, val increases. For fixed k, as i increases, val increases. So for a fixed i, the best k's are the largest. For fixed j, the best (i,k) pairs are with large i and k.

Now, to count how many (i,j,k) have val >= X:
We can iterate over j, and for each j, count pairs (i,k) with val >= X in O(N) using two pointers as analyzed. But O(N) per j is O(N^2).

However, note that B_j can be grouped? Or we can iterate over i and k? That gives O(N^2) pairs, and for each pair, count j with `B_j >= (X - A_i*C_k)/(A_i+C_k)`. Again O(N^2) per check.

Given constraints, perhaps the intended solution is O(N^2) with small constant? N=2e5, so N^2 is impossible.

Wait, maybe the counting can be done in O(N) total for a fixed X using the fact that we only need to know if count >= K. That is, we can early stop. But the binary search requires knowing the exact count or at least comparison to K, but we can do a "find K-th largest" using a priority queue without binary search.

Let's reconsider the priority queue approach. Since K <= 5e5, we can generate the top K values directly.

Sort A desc (indices a[0..N-1]), B desc (b[0..N-1]), C desc (c[0..N-1]).
The maximum value is at (0,0,0). We can use a 3D max-heap. But 3D visited set is tricky.

However, note that the expression is monotone in each variable. The set of top K triples is such that if we sort all triples by value desc, they can be enumerated. But 3D enumeration of top K is O(K log K) if we use a heap with visited set. But we need to generate up to 5e5 elements, each with O(log K) operations, and checking visited in O(1) with a hash set. The total work is O(K log K) ~ 5e5 * 19 ~ 1e7, which is fine. But we need to ensure we don't miss any or generate too many.

The standard way: start with (i=0, j=0, k=0) in heap. When we pop (i,j,k), we push (i+1, j, k), (i, j+1, k), (i, j, k+1) if not already generated. This generates all triples in decreasing order, provided that the value function is such that neighbors of a popped element are not larger than the popped element. This is true if the function is monotone (increasing in each coordinate). Here val increases when any of i,j,k increases (since A, B, C are sorted descending, larger index means smaller value, wait!).

I sorted A desc, so a[0] is largest A. Then as index i increases, A_i decreases. The value `A_i*B_j + B_j*C_k + C_k*A_i` — if A_i decreases, the value might decrease. So val is decreasing in i (if we use sorted desc indices). So the max is at (0,0,0). If we pop (i,j,k), then (i+1, j, k) has smaller A, so smaller val? Not necessarily because of interactions. But the expression is linear in A_i: `A_i*(B_j + C_k) + B_j*C_k`. Since B_j+C_k > 0, val is increasing in A_i. Since A_i is sorted descending, larger index i means smaller A_i, so val is smaller. Similarly for j and k. So val is strictly decreasing in i, j, k (as indices increase). So the max is at (0,0,0), and neighbors (i+1,j,k), (i,j+1,k), (i,j,k+1) are smaller than (i,j,k). Therefore, the heap enumeration with the rule "push three neighbors" generates all triples in non-increasing order! And we never need a visited set because the set of generated triples forms a "staircase" and we can push neighbors without duplication? Actually, we might push duplicates: if we pop (i,j,k) and push (i+1,j,k), then later pop (i,j+1,k) and push (i+1,j+1,k) and (i,j+1,k+1), etc. The standard approach for 2D top-K is to use a visited set to avoid duplicates. For 3D, the number of generated elements before getting K is O(K). We can use a hash set to avoid duplicates. Memory for visited set of size O(K) is fine.

So algorithm:
1. Sort A desc, B desc, C desc.
2. Max-heap with (-val, i, j, k) for (0,0,0).
3. Visited set {(0,0,0)}.
4. For _ in range(K-1): pop, push (i+1,j,k), (i,j+1,k), (i,j,k+1) if within bounds and not visited.
5. The K-th popped is the answer.

But wait: is it true that the K-th largest is among the first K popped? Yes, because we pop in decreasing order. But we need to ensure we generate enough candidates. The number of pushes is at most 3*(K-1) + 1, so O(K). Each operation O(log K). Total O(K log K) ~ 5e5 * 19 = 9.5e6, which is fast.

But we must be careful: does this enumeration visit all "necessary" triples? In 2D monotone matrices, the top K can be found this way. In 3D, it also works: the set of popped elements is the set of all triples that are not strictly dominated by another unpopped element? Actually, the standard method for 3D is to push the three neighbors. However, we might miss some triples if they are not reachable by a path of decreasing steps? But since we start from max and allow increments in any coordinate, we can reach any triple from (0,0,0) by incrementing coordinates. So we will eventually generate all triples, but in what order? The heap ensures we always pop the largest among the frontier. This is the standard "best-first search" on the lattice graph. It will generate all triples in non-increasing order of value. So the first K popped are the K largest.

But is there a risk of generating too many? No, because we only push when popping, so total pushes <= 3*(K-1) + 1.

However, we need to store the values in the heap. The values can be up to 3e9^2 ~ 1e19, need Python int (which is arbitrary precision, fine).

Let's test on sample 1:
A=[1,2] desc -> [2,1]
B=[3,4] desc -> [4,3]
C=[5,6] desc -> [6,5]
Triples (i,j,k) with 0-indexed:
(0,0,0): A=2,B=4,C=6 -> 2*4+4*6+6*2 = 8+24+12=44
(0,0,1): 2*4+4*5+5*2 = 8+20+10=38
(0,1,0): 2*3+3*6+6*2 = 6+18+12=36
(1,0,0): 1*4+4*6+6*1 = 4+24+6=34
(0,1,1): 2*3+3*5+5*2 = 6+15+10=31
(1,0,1): 1*4+4*5+5*1 = 4+20+5=29
(1,1,0): 1*3+3*6+6*1 = 3+18+6=27
(1,1,1): 1*3+3*5+5*1 = 3+15+5=23
Sorted desc: 44,38,36,34,31,29,27,23. K=5 -> 31. Correct.

Heap order:
Start: (0,0,0):44
Pop 44, push (1,0,0):34, (0,1,0):36, (0,0,1):38
Heap: 38,36,34
Pop 38, push (1,0,1):29, (0,1,1):31, (0,0,2?) out of bounds.
Heap: 36,34,31,29
Pop 36, push (1,1,0):27, (0,2,0) out, (0,1,1) already? Wait (0,1,1) was pushed from (0,0,1) -> (0,1,1) and from (0,1,0) -> (0,1,1). So we need visited set.
Let's track visited:
Initially: (0,0,0) visited.
Pop (0,0,0): push (1,0,0), (0,1,0), (0,0,1) -> add to visited.
Pop (0,0,1): push (1,0,1), (0,1,1), (0,0,2 OOB). Add visited.
Pop (0,1,0): push (1,1,0), (0,2,0 OOB), (0,1,1) already visited. Add visited.
Pop (1,0,0): push (2,0,0 OOB), (1,1,0) already? (1,1,0) was pushed from (0,1,0). So skip. (1,0,1) already pushed.
So we get the correct order.

So the algorithm works.

But wait: what if N=2e5, and we only need K=1? Then it's fine. If K=5e5, the heap size is at most 5e5, operations are fast.

One potential issue: the value computation might overflow in some languages, but Python handles big ints. Also, the time to compute value for each push: 3 multiplications and 2 additions. 3 * 5e5 = 1.5e6, negligible.

But is the sort descending necessary? Yes, to ensure that increasing index means decreasing value. But we must be careful: the value is `A_i*B_j + B_j*C_k + C_k*A_i`. If A is sorted descending, then as i increases, A_i decreases, and the term `A_i*(B_j+C_k)` decreases. So val decreases. Good.

Now, we need to handle the case where K > N^3? The constraints say K <= min(N^3, 5e5). So we don't need to handle K > N^3. But if N^3 < 5e5, then we might need to generate all N^3 values. For N=2e5, N^3 is huge, so K will be <=5e5. The smallest N^3 for N=2e5 is 8e15, so K=5e5 is always <= N^3 for N>=2. Actually if N=1, N^3=1, K=1. If N=2, N^3=8, K<=8. So K is always <= N^3. So the heap method always works.

But wait: if N is small, say N=2, K=8, we will pop 8 times. The heap will try to push neighbors, but indices go out of bounds quickly. That's fine.

Edge case: N=1, K=1. Only one value.

So the algorithm is:
1. Read N, K, A, B, C.
2. Sort A, B, C in descending order.
3. Initialize a max-heap with (-(A[0]*B[0] + B[0]*C[0] + C[0]*A[0]), 0, 0, 0).
4. Initialize a set visited = {(0,0,0)}.
5. For _ in range(K-1):
   - Pop the heap: get neg_val, i, j, k.
   - For each neighbor (i+1,j,k), (i,j+1,k), (i,j,k+1):
     - If not out of bounds and not in visited, compute val, push (-val, ni, nj, nk), add to visited.
6. After loop, pop the heap one more time to get the K-th value? Wait, the loop runs K-1 times, popping K-1 values. The next pop is the K-th largest. So we can just pop one more time and print the value (positive).

But careful: the first pop is the largest (1st). We need the K-th. So we pop K-1 times, then the next pop is K-th. Alternatively, we can pop K times and the last popped is the K-th. Let's do: for _ in range(K): pop, then the last popped is answer. But we need to push neighbors during the process. The standard way: for step in range(K): pop, then push neighbors. After K pops, the last popped is the K-th. We don't need an extra pop.

So:
ans = None
for _ in range(K):
    neg_val, i, j, k = heapq.heappop(heap)
    ans = -neg_val
    for di,dj,dk in [(1,0,0),(0,1,0),(0,0,1)]:
        ni, nj, nk = i+di, j+dj, k+dk
        if ni < N and nj < N and nk < N and (ni,nj,nk) not in visited:
            val = A[ni]*B[nj] + B[nj]*C[nk] + C[nk]*A[ni]
            heapq.heappush(heap, (-val, ni, nj, nk))
            visited.add((ni,nj,nk))
print(ans)

This should work.

But is there a risk of visited set becoming too large? At most O(K) entries, 5e5, fine.

Time complexity: O(K log K) heap operations, plus O(K) value computations. The value computation uses Python integers up to ~3e9, products up to ~9e18, sum up to ~2.7e19, fine.

Let's verify with sample 1:
N=2, K=5.
A=[2,1], B=[4,3], C=[6,5]
Heap: (-44, 0,0,0)
ans=None
1: pop (-44,0,0,0), ans=44. Push (1,0,0): -34, (0,1,0): -36, (0,0,1): -38. visited: (0,0,0), (1,0,0), (0,1,0), (0,0,1).
Heap: [-38, -36, -34] (or similar order)
2: pop (-38,0,0,1), ans=38. Push (1,0,1): -29, (0,1,1): -31, (0,0,2 OOB). visited add (1,0,1), (0,1,1).
Heap: [-36, -34, -31, -29]
3: pop (-36,0,1,0), ans=36. Push (1,1,0): -27, (0,2,0 OOB), (0,1,1) already visited.
Heap: [-34, -29, -31, -27]
4: pop (-34,1,0,0), ans=34. Push (2,0,0 OOB), (1,1,0) already? (1,1,0) is in heap? Wait, (1,1,0) was pushed from (0,1,0) step 3. Yes, so already visited? Actually visited set has (1,1,0) because we added when pushing. So skip. (1,0,1) already visited.
Heap: [-31, -29, -27]
5: pop (-31,0,1,1), ans=31. Push neighbors: (1,1,1): -23, (0,2,1 OOB), (0,1,2 OOB).
Now K=5, we have ans=31. Correct.

Sample 2: all 100. N=3, K=10.
A=[100,100,100], B=[100,100,100], C=[100,100,100].
All values are 100*100+100*100+100*100 = 30000.
The 10th largest is 30000. Algorithm will pop 10 times, all values 30000. Correct.

Sample 3: large numbers. Should work.

One concern: the value computation for neighbors might be slow if we compute it many times. But we only compute when pushing. Number of pushes is at most 3*(K-1) + 1. For K=5e5, that's ~1.5e6 computations. Each is a few multiplications, very fast in Python.

Memory: visited set of up to ~1.5e6 tuples of 3 ints. 1.5e6 * 3 * 28 bytes ~ 126 MB? Actually Python tuple overhead is large. A tuple of 3 ints is about 72 bytes or more. 1.5e6 * 72 = 108 MB. Plus heap. This might be a bit high but probably okay for 1GB memory limit. But we can optimize: use a dictionary with a single integer key (i*N*N + j*N + k) or use a set of integers. Since N up to 2e5, N^3 is huge, but we only store O(K) entries. Encoding as i*N*N + j*N + k uses up to N^3 which is 8e15, fits in Python int. So visited_set = set() of int keys. That reduces memory significantly. Let's do that.

Key: i * N * N + j * N + k. But N*N might be large, but Python int handles it. Actually, to avoid huge N*N, we can use i * (N*N) but N=2e5, N*N=4e10, i up to 2e5, product up to 8e15, fine. Or we can do i * 1000000 + j * 1000 + k? No, N=2e5, so we need unique encoding. i * N * N + j * N + k is safe.

Alternatively, we can use a 2D visited for pairs? But we have 3D. So integer encoding is best.

Let's implement.

One more check: the problem asks for K-th largest among all N^3 values. Our algorithm finds the K-th largest from the sorted A, B, C (descending). Since we sort each array in descending order, the set of triples is the same, just permuted. So the multiset of values is identical. The order is just the sorted order of the new indices. So the K-th largest value is the same. Correct.

Potential issue: the heap may contain many elements with the same value. The order among them doesn't matter as long as we pop K elements. But if there are ties, we might not get the correct K-th if we stop early? No, we just need the value, not the specific triple. The K-th largest value is well-defined. If there are ties, any of the tied values is the K-th. So we are fine.

Thus, the plan is solid.