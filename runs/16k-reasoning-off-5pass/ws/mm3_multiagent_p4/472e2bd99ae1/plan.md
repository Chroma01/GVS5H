We need the K-th largest value of `f(i,j,k) = A_i*B_j + B_j*C_k + C_k*A_i`.  
Key idea: fix `j` (the B index). Then for each j, we need to efficiently count how many pairs (i,k) give `f(i,j,k) >= X` for a given threshold X, to support binary search on the answer.  

Observe that for fixed j, `f = B_j*(A_i + C_k) + A_i*C_k`. If we define `S_i = A_i` and `T_k = C_k`, then  
`f = B_j*(S_i + T_k) + S_i*T_k`.  
For a fixed j, the pairs (S_i, T_k) are independent of B_j. So we can precompute, for each possible value of B_j, the list of values `B_j*(S+T) + S*T` sorted descending — but N is up to 2e5, so that's too big.

Alternative: binary search on the answer `X`. For a given X, we need to count how many triples (i,j,k) satisfy `A_i*B_j + B_j*C_k + C_k*A_i >= X`.  
For fixed j, count pairs (i,k) with `A_i*B_j + B_j*C_k + C_k*A_i >= X`.  
This can be rewritten as `(A_i + C_k)*B_j + A_i*C_k >= X`.  
For fixed j, we can sort A and C, and for each A_i, find the number of C_k such that `(A_i + C_k)*B_j + A_i*C_k >= X`.  
Since both A_i and C_k are up to 1e9, and B_j up to 1e9, the values are large. We can sort C in descending order. For each A_i (iterating in descending order), we need to find the largest index in C such that the condition holds. Because the condition is monotonic in C_k (if C_k is larger, the left side is larger), we can use two pointers. But N=2e5, and we do binary search (log 1e18 ~ 60 steps), and for each step we iterate over all j, and for each j do O(N) pointer scan, total O(N^2 log M) which is too big.

We need a better way. Notice that the expression is symmetric in a way. Let's denote `a = A_i`, `b = B_j`, `c = C_k`. The value is `ab + bc + ca`. We need the K-th largest among all such products.  
We can binary search on the answer X, and for each X, we need to count the number of triples (i,j,k) with `A_i*B_j + B_j*C_k + C_k*A_i >= X`.  
The count can be done by iterating over j, and for each j, we need to count pairs (i,k) with `A_i*B_j + B_j*C_k + C_k*A_i >= X`.  
For a fixed j, let `b = B_j`. The condition is `b*(A_i + C_k) + A_i*C_k >= X`.  
For fixed A_i, as C_k increases, the left side increases (since b, A_i, C_k are positive). So we can sort C in descending order, and for each A_i (also sorted descending), we find the minimal index such that the condition holds? Actually, we need to count pairs where the condition is true. For a given A_i, we need the number of C_k such that the inequality holds. Since the left side is increasing in C_k, we can binary search on C (or two pointers) to find the first C_k where the condition fails, and take the rest. But we need to do this for all i, and the two pointers must move monotonically.

However, we also need to do this for each j. If we sort A and C in descending order once, then for each b, we can do a two-pointer scan over A and C. But the two pointers depend on b because the inequality involves b. For larger b, the left side is larger, so the threshold C_k might be smaller. Actually, if b is larger, then for a fixed A_i, the left side is larger for any C_k, so the number of valid C_k is larger. So as b increases, the count increases. If we process j in increasing order of B_j, the two pointers for each j will only move forward (or stay). But we have N up to 2e5, and for each j we do O(N) work, total O(N^2) which is too big.

We need to reduce the per-j cost. Notice that the condition is `b*(A_i + C_k) + A_i*C_k >= X`. For fixed b, we can consider the pairs (A_i, C_k). The total number of such pairs is N^2, and we need to count how many are >= X. We can do this by sorting all pairs? But N^2 is too large.

Wait, the problem constraints say K <= 5e5. That's a crucial hint! We don't need to count all triples up to some threshold, we just need the K-th largest. The typical approach for K-th largest with K relatively small is to use a priority queue (max-heap) to generate the top K values. Since K <= 5e5, we can afford O(K log K * something). But N^3 is huge, so we need an efficient way to generate the top K values.

The expression `A_i*B_j + B_j*C_k + C_k*A_i` can be rewritten. Let's see: it's equal to `(A_i + B_j)*(B_j + C_k) - B_j^2`? Not exactly. Let's expand: `(A_i + B_j)*(B_j + C_k) = A_i*B_j + A_i*C_k + B_j^2 + B_j*C_k`. That's not matching. Another identity: `A_i*B_j + B_j*C_k + C_k*A_i = (A_i + B_j + C_k)^2 - (A_i^2 + B_j^2 + C_k^2)` over 2? No.

Let's think differently. The expression is symmetric in A, B, C. The maximum value occurs when A_i, B_j, C_k are all large. Since we want the K-th largest, and K is only up to 5e5, we can use a max-heap that stores triples (i, j, k) with their value, and we pop the maximum, then push neighbors? But there are N^3 possible triples, we cannot even represent all.

We need a way to enumerate the top K values efficiently. The expression is sum of pairwise products. If we sort A, B, C in descending order, the top values will likely come from the largest elements. But we need to be careful because the expression is not fully symmetric in the sense that it's not just a sum of independent choices. However, we can use the fact that for fixed i, the function `f(i,j,k) = A_i*(B_j + C_k) + B_j*C_k` is increasing in B_j and C_k. So if we have a candidate (i,j,k) that is large, then increasing j or k (to a larger index in sorted descending order) will give an even larger value. So the set of top values is "monotone" in the indices if we sort the sequences in descending order. That suggests we can use a best-first search on the lattice of indices (i, j, k) sorted descending. We start with (1,1,1) (all largest), and then we can push (1,1,2), (1,2,1), (2,1,1). But we need to avoid duplicates and ensure we only push promising ones. However, the number of candidates might be large because each popped node could generate up to 3 new ones, so up to O(K) nodes. Since K <= 5e5, O(K log K) is fine. But we need to ensure we don't push too many nodes. Actually, each pop generates 3, so total pushes are O(K). The heap size is O(K). This is feasible if we can generate the neighbors efficiently and avoid duplicates.

But we need to be careful: the value might not be strictly increasing in each index individually? Let's check: For fixed i and j, as k increases (i.e., C_k smaller if sorted descending), the value decreases? Actually, if we sort C in descending order, then as k increases, C_k decreases. So the value `A_i*B_j + B_j*C_k + C_k*A_i` = `B_j*(A_i + C_k) + A_i*C_k`. As C_k decreases, both terms decrease (since all positive). So yes, if we sort A, B, C in descending order, the value is strictly decreasing in each index individually (if we fix the other two). So the set of values is anti-monotone in each coordinate. That means the top K values are among the K largest indices in the sorted order? Not exactly, but we can use a heap that starts with (1,1,1) and we only push (i+1, j, k), (i, j+1, k), (i, j, k+1) when we pop a state. This is similar to generating the top K sums of three sorted lists. The total number of generated states is O(K) because each state is pushed at most once (if we use a visited set). And since K <= 5e5, this is efficient.

But wait: is the value strictly decreasing in each index? If we have duplicates, it might be equal, but that's fine. The important part is that for any (i,j,k), the value is at least the value of (i+1, j, k) (if sorted descending). So if we pop a state, any state that is "worse" in one coordinate is not necessarily worse overall? Actually, if we pop (i,j,k), its value is >= the value of (i+1, j, k) because A_{i+1} <= A_i. But we don't know the relative order of (i+1, j, k) and (i, j+1, k) etc. So the heap approach is valid: we start with the maximum (1,1,1). When we pop (i,j,k), we push (i+1, j, k) if i < N, (i, j+1, k) if j < N, (i, j, k+1) if k < N. We need to ensure we don't push duplicates. Since each state is uniquely defined by the triple, we can use a 3D boolean array or a set to track visited states. With N up to 2e5, we cannot use a 2D array of size N^2. But K is only 5e5, so the number of visited states is at most 3K (since each pop generates at most 3, and we only push those). So we can use a hash set of tuples (i,j,k) to keep track of visited states. The total number of heap operations is O(K), and each operation is O(log K) (since heap size is O(K)). The only concern is the time to compute the value for each state, which is O(1). So the total time is O(K log K), which is fine for K=5e5.

But wait: is it guaranteed that the top K values are all among the first few indices? For example, if the sequences are such that the value function has a weird shape? Since the value is strictly decreasing in each coordinate, the maximum over the entire domain is at (1,1,1). The next largest could be (1,1,2), (1,2,1), or (2,1,1). In general, the set of top K values is contained in the set of states that can be reached from (1,1,1) by increasing indices. And since the number of such states is exactly the number of paths in the lattice, but we only need the top K, the heap approach will generate them in the correct order. This is a standard technique for "K-th largest sum" problems with monotone decreasing functions. The only requirement is that the function is non-increasing in each coordinate. Here it is strictly increasing as we move to smaller indices (i.e., as index increases, the element value decreases). So if we sort all sequences in descending order, then for any (i,j,k), the value is >= the value of (i',j',k') if i' >= i, j' >= j, k' >= k. So the set of values is a partially ordered set. The top K elements can be found by exploring the lattice in best-first order. The number of elements we need to pop is K, and each pop pushes at most 3 new elements. So total pushes is at most 3K. We just need to store visited states in a set. Since K <= 5e5, the set size is at most 3K, which is manageable in memory (each tuple of three integers up to 2e5, we can pack into a single 64-bit integer: e.g., (i * (N+1) + j) * (N+1) + k, or use tuple hashing). Python's set of tuples might be a bit slow but should be okay for 1.5 million entries? Actually 3K = 1.5e6, which is fine.

But we must be careful: the number of distinct states we visit might be larger than 3K because of the way duplicates are handled? In the standard algorithm for K-th largest sum of three arrays, we start with (0,0,0) (if sorted ascending) and push (i+1,j,k), (i,j+1,k), (i,j,k+1). We use a visited set to avoid duplicates. The number of visited states is O(K) because each pop generates at most 3, and we only push if not visited. So total pushes is O(K). This is a known technique.

Let's verify the monotonicity: Let A, B, C be sorted in descending order. For any i <= i', j <= j', k <= k', we have A_i >= A_i', B_j >= B_j', C_k >= C_k'. Then the value f(i,j,k) = A_i B_j + B_j C_k + C_k A_i. Compare f(i,j,k) and f(i',j',k'): Since each term is product of two non-increasing sequences, the product is non-increasing in each index. So f(i,j,k) >= f(i',j',k'). So indeed, the value is non-increasing in each index. Therefore, the partial order holds.

Thus, the top K values are among the "maximal" elements in the lattice. The best-first search with a max-heap on the lattice is valid. We pop the largest value, and then push the "children": (i+1, j, k), (i, j+1, k), (i, j, k+1) if they are within bounds and not visited. We do this K times, and the K-th popped value is the answer. We need to be careful with 1-based vs 0-based indices. Let's use 0-based for Python: indices 0 to N-1. Sorted descending. Start with (0,0,0). The heap stores (-value, i, j, k) to use max-heap. We need to compute value = A[i]*B[j] + B[j]*C[k] + C[k]*A[i]. Since values can be up to 1e9*1e9*3 = 3e18, we need to use Python's integers (which are arbitrary precision), so no overflow issue.

We need to pop K times. The first pop is the maximum, which is the answer if K=1. The K-th pop is the K-th largest. We must ensure we pop exactly K times. The heap will contain the candidates. We use a visited set. Since N can be up to 2e5, we cannot use a 2D boolean array. But the number of visited states is at most 3K (actually, each state is pushed at most once, and we push at most 3K total, so visited set size is at most 3K). For K=5e5, 1.5e6 entries in a Python set. Each entry is a tuple of three integers. That might use a lot of memory. Let's estimate: a tuple of 3 integers in Python takes about 72 bytes (3*28 for ints + overhead). 1.5e6 * 72 = 108 MB. Plus the set overhead, maybe around 200-300 MB. That might be too much for typical memory limits (usually 1024 MB is okay, but some are 256 MB). We need to be more memory efficient.

We can encode the triple (i, j, k) into a single 64-bit integer to use less memory. Since N <= 2e5, we can use N as the base. The number of possible indices is N. We can encode as (i * N + j) * N + k, which gives a unique integer in [0, N^3). For N=2e5, N^3 = 8e15, which fits in 64 bits (since 2^63-1 is about 9.2e18). So we can use a single integer as the key in the set. This will drastically reduce memory usage. Python's set of integers is much more memory efficient. So we should encode each state as a single integer: `i * N * N + j * N + k`. But wait, N*N*N might overflow Python's integer? No, Python int is arbitrary precision. But we can just compute it. However, the multiplication N*N might be 4e10, which is fine. But for efficiency, we can precompute N_sq = N*N. Then key = i * N_sq + j * N + k. This is a unique mapping. So we can use a set of integers for visited. That will be much more memory efficient.

But we need to be careful: the number of visited states is at most 3K, so up to 1.5e6 integers. Each integer in a Python set takes about 28 bytes (for small ints, actually Python caches small ints, but these will be large ints, so maybe 28+ bytes). 1.5e6 * 28 = 42 MB. Plus the heap, which stores tuples of (neg_value, i, j, k). The heap size is at most 3K, so 1.5e6 tuples. Each tuple has 4 elements, so maybe 48+ bytes per tuple. That's another 70 MB. So total around 112 MB, which is acceptable.

But we need to consider the time. Pushing into a set of 1.5e6 elements is O(1) average. The heap operations are O(log(1.5e6)) ~ 20. For 1.5e6 operations, total time is around 30 million operations, which is fine in Python if optimized (using local variables, etc.). However, we need to be careful with the heap implementation. We can use `heapq` but we need to store tuples. The comparison will be on the first element, which is the negative value. But if two values are equal, the next elements (i,j,k) will be compared. Since i,j,k are up to 2e5, that's fine.

One potential issue: the number of distinct states might be more than 3K? Let's analyze the standard algorithm. We start with (0,0,0). We pop it, then we push (1,0,0), (0,1,0), (0,0,1). Now the heap has these three. We pop the largest, say (1,0,0). Then we push (2,0,0), (1,1,0), (1,0,1). But (1,1,0) and (1,0,1) are new. So the number of states in the heap can grow. In the worst case, if the values decrease very slowly, we might generate many states before we pop the top K. But is it bounded by 3K? Actually, each pop generates at most 3 new states, so the number of pushes is at most 3 * (number of pops). The number of pops is K. So the number of pushes is at most 3K. However, the number of states in the heap at any time is the number of pushes minus the number of pops. So the maximum heap size is at most 3K - (K-1) = 2K+1. So the heap size is O(K). The total number of states ever pushed is at most 3K. So the visited set size is at most 3K. This is a standard result for this kind of lattice exploration. So it's safe.

But wait: is it always true that the top K values are all among the states reachable by this process? The process explores the lattice in a best-first manner. The key property is that for any state (i,j,k), its value is >= the value of any state (i',j',k') with i' >= i, j' >= j, k' >= k. So the value is non-increasing as we increase any index. This means that the set of values is a "monotone" set. The best-first search on the lattice with the property that we only push neighbors that are "worse" by one index will eventually cover all states in decreasing order of value. This is analogous to the algorithm for K-th largest sum of two arrays. For three arrays, it's the same. The only requirement is that the function is non-increasing in each variable. Here it is, so it's valid.

But we must be careful: the function is not necessarily strictly decreasing, but that's fine. There could be ties, but the heap will handle them by index.

So the algorithm:
1. Read N, K, and arrays A, B, C.
2. Sort A, B, C in descending order.
3. Initialize a max-heap (using negative values) with the state (0,0,0) and its value.
4. Initialize an empty set for visited states. Encode state as i*N*N + j*N + k.
5. Loop for _ in range(K):
   - Pop the heap: (neg_val, i, j, k).
   - The value is -neg_val. If this is the K-th pop, store it as answer.
   - For each of the three neighbors (i+1, j, k), (i, j+1, k), (i, j, k+1):
     - If within bounds and not visited:
       - Mark visited.
       - Compute value.
       - Push (-value, i+1, j, k) etc.
6. Print the answer.

But we need to be careful with the encoding: N can be up to 2e5, so N*N = 4e10, which is fine for Python int. But we can precompute N_sq = N * N. Then key = i * N_sq + j * N + k. This is unique and fast.

We also need to consider the time to compute the value. Each value computation involves two multiplications and two additions? Actually: A[i]*B[j] + B[j]*C[k] + C[k]*A[i]. We can compute it as (A[i] + C[k]) * B[j] + A[i]*C[k]. But since Python integer multiplication is fast, it's fine.

Now, is there any issue with the constraints? N up to 2e5, K up to 5e5. The number of iterations is 5e5. Each iteration does up to 3 neighbor checks and 3 pushes. So total pushes up to 1.5e6. Heap operations: 1.5e6 pushes and 5e5 pops, total 2e6 operations. Each operation is O(log heap size) ~ O(log 1.5e6) ~ 20. So total time around 40 million comparisons, which is okay in Python. The visited set will have up to 1.5e6 elements, so checking membership is O(1) average.

But we need to ensure that the heap doesn't grow too large due to the way we push neighbors. Actually, the maximum number of elements in the heap is bounded by the number of pushes minus the number of pops. Since we do K pops, the maximum heap size is when we have pushed many but not popped many. In the worst case, we might push all 3K elements before popping K? No, because we pop one at a time. At any point, the heap size is the number of elements that have been pushed but not yet popped. The number of pushes is at most 3 * (number of pops executed so far) + 1 (the initial). So after t pops, pushes <= 3t+1. So heap size <= 2t+1. So it's O(K).

We also need to be careful about the memory of the heap. The heap stores tuples. To reduce memory, we can store the negative value, the encoded state, and then decode i, j, k. But then we need to decode to compute neighbors. Decoding is just division and modulo. But if we store (neg_val, i, j, k) as separate integers, it's 4 integers per tuple. If we encode the state, we can store (neg_val, key), and then decode the key to get i, j, k. That would reduce the tuple size to 2 integers, but we need to decode each time we pop. Decoding involves division and modulo by N and N_sq. Since N is up to 2e5, division is relatively expensive but not too bad. But maybe storing i, j, k directly is fine. Let's see: 1.5e6 tuples * 4 ints = 6e6 ints. Each int in Python is at least 28 bytes, so 168 MB. That's a lot. If we store (neg_val, key), that's 2 ints, so 84 MB. Plus the visited set: 1.5e6 ints = 42 MB. Total around 126 MB. That might be okay if memory limit is 1024 MB, but if it's 256 MB, it could be tight. However, Python's overhead for small tuples might be less. Actually, a tuple of 3 integers in Python takes about 64 bytes (3*28 for ints + 16 for tuple header?). For a tuple of 2, it's 56 bytes. So saving 2 ints per entry saves about 56 bytes per entry, which for 1.5e6 entries is 84 MB. So it's worth it. We can store (neg_val, key) in the heap. When we pop, we decode key to i, j, k. Then for neighbors, we compute new_key and push (-new_val, new_key). We need to be careful with the order: we want to compare by neg_val first, then key (or i,j,k) to break ties. If we only store key, ties in value will be broken by key, which is determined by i, j, k. Since we want to ensure that if two values are equal, we pop the one with smaller indices? Actually, the order among equal values doesn't matter for the K-th largest, as long as we count them correctly. But we need to be careful: if there are duplicates, we might pop the same value multiple times from different states? No, because the value is a function of the state, and different states can have the same value. But that's fine; the heap will treat them as separate entries. The K-th largest is the K-th value we pop. If there are ties, we need to ensure we pop exactly K times. The algorithm will pop the K-th largest (with ties) correctly because it explores in non-increasing order of value. The only issue is if the heap contains multiple states with the same value, the order in which they are popped depends on the secondary key. But since we are counting each pop as a separate value, it's correct. So we can use the encoded state as the secondary key. That is fine.

But we need to ensure that the encoded state is unique and we can decode it correctly. We can precompute N_sq = N * N. Then key = i * N_sq + j * N + k. To decode: k = key % N; temp = key // N; j = temp % N; i = temp // N. This is straightforward.

Now, we need to compute the value for a given state. We can store A, B, C as Python lists after sorting. Since we will access them many times, it's better to store them as lists.

One more thing: the initial state (0,0,0) is the maximum. We push it first. Then we pop and push neighbors. We need to mark visited before pushing to avoid duplicates. We should mark visited when we push, not when we pop. Because if we mark when we pop, we might push the same state multiple times from different parents. So we should check visited before pushing, and if not visited, mark it and push. This is standard.

Let's test with the sample. N=2, K=5. A=[1,2] sorted descending: [2,1]. B=[3,4] sorted: [4,3]. C=[5,6] sorted: [6,5]. Then values:
(0,0,0): A0=2, B0=4, C0=6 -> 2*4 + 4*6 + 6*2 = 8+24+12=44.
(0,0,1): 2*4 + 4*5 + 5*2 = 8+20+10=38.
(0,1,0): 2*3 + 3*6 + 6*2 = 6+18+12=36.
(1,0,0): 1*4 + 4*6 + 6*1 = 4+24+6=34.
(0,1,1): 2*3 + 3*5 + 5*2 = 6+15+10=31.
(1,0,1): 1*4 + 4*5 + 5*1 = 4+20+5=29.
(1,1,0): 1*3 + 3*6 + 6*1 = 3+18+6=27.
(1,1,1): 1*3 + 3*5 + 5*1 = 3+15+5=23.
Sorted: 44,38,36,34,31,29,27,23. The 5th is 31. Our algorithm should pop 44, then 38, 36, 34, 31. So it should work.

Now, we need to consider the case when N=1. Then only one state. K=1. The algorithm should handle it: push (0,0,0), pop, done.

What about the memory for the visited set? We can use a set. But 1.5e6 integers in a set is okay. However, we need to be careful with the time to hash integers. It should be fast.

We should also consider using `sys.stdin.buffer` for fast input, and `sys.stdout.write` for output.

Potential issue: The number of iterations is K, but we need to pop K times. The first pop is the maximum, which we don't necessarily need to output unless K=1. We just need to keep track of the K-th popped value.

One more thing: The problem asks for the K-th largest. Our heap pops in descending order. So the K-th pop is exactly the K-th largest. But we must ensure that we don't pop the same state twice. The visited set ensures that.

But wait: Is it possible that the value function is not strictly decreasing in each index? Actually, it's non-increasing. So if we have a state (i,j,k), its value is >= the value of (i+1,j,k) because A[i+1] <= A[i]. But could it be that the value of (i+1,j,k) is equal to (i,j,k)? Only if A[i] = A[i+1] and the other products are the same? But if A[i] = A[i+1], then the value might be the same if B and C are the same. So the function is non-increasing, which is sufficient for the algorithm to work. The algorithm assumes that the set of values is totally ordered by the partial order, but the heap explores in the order of the values. The key property is that if we have a state in the heap, all its "descendants" (states with larger indices) have values <= the state's value. So when we pop a state, we know that no other state in the heap can have a value greater than the popped value? Not necessarily, because there might be other states not yet discovered that have the same value. But the algorithm is correct for finding the top K values when the function is non-increasing in each variable. This is a known fact: the "K-th largest sum" problem for sorted arrays uses the same technique. The reason it works is that the lattice is explored in a best-first manner, and any state not yet pushed has all indices >= the current state, so its value is <= the current state's value. But wait, that's not true: a state not yet pushed might have a smaller index in one coordinate and larger in another, so it could have a larger value. But the algorithm pushes all immediate neighbors, so it will eventually push that state if it is among the top K. The standard proof is by induction: the heap always contains the "frontier" states. The maximum value among all unvisited states is always in the heap. This holds because the function is non-increasing, so the maximum over the entire lattice is at (0,0,0). When we pop the maximum, we then push its neighbors, which are the next candidates with one index increased. Any other state not yet pushed has at least one index >= the corresponding neighbor? Actually, the standard proof for the "K-th largest sum of three arrays" relies on the fact that the arrays are sorted in descending order, and the sum is non-increasing. The algorithm is exactly as we described. So it should be correct.

But let's double-check with a potential counterexample. Suppose we have A=[10,1], B=[10,1], C=[10,1]. Sorted descending: same. Values:
(0,0,0): 10*10 + 10*10 + 10*10 = 300.
(0,0,1): 10*10 + 10*1 + 1*10 = 100+10+10=120.
(0,1,0): 10*1 + 1*10 + 10*10 = 10+10+100=120.
(1,0,0): 1*10 + 10*10 + 10*1 = 10+100+10=120.
(0,1,1): 10*1 + 1*1 + 1*10 = 10+1+10=21.
(1,0,1): 1*10 + 10*1 + 1*1 = 10+10+1=21.
(1,1,0): 1*1 + 1*10 + 10*1 = 1+10+10=21.
(1,1,1): 1+1+1=3.
Top 3: 300, 120, 120, 120. So the 2nd, 3rd, 4th largest are all 120. Our algorithm will pop 300, then it will push (1,0,0), (0,1,0), (0,0,1). The heap will have these three with value 120. The secondary key will determine the order. We pop one of them, say (1,0,0). Then we push (2,0,0) (but N=2, so i+1=1? Wait, N=2, indices 0,1. So (1,0,0) has i=1, so i+1=2 is out of bounds. So we only push (1,1,0) and (1,0,1). Their values are 21. So the heap now has the other two 120s and the two 21s. Then we pop the next 120, and so on. So we will correctly pop 300, 120, 120. The 3rd pop is 120. So it works.

Now, what about the case where the function is not strictly decreasing, but the top K values might come from states that are not directly connected to (0,0,0)? The lattice is connected, so starting from (0,0,0) and moving one step at a time, we can reach any state. The algorithm explores the lattice in a way that always expands the current maximum. So it will eventually reach the states that are among the top K. The key is that the number of steps to reach the K-th largest is bounded. Since we pop K times, and each pop expands by at most 3, the maximum distance in indices from (0,0,0) to the popped states is at most K? Not necessarily, but the total number of states explored is O(K). So it's efficient.

Now, we need to consider the constraint that K can be up to N^3, but min(N^3, 5e5). So K <= 5e5. That's good.

But wait: Is it always true that the number of states explored is O(K)? Let's think. The worst-case scenario for the number of states explored in the standard "K-th largest sum" problem is indeed O(K). But there is a known issue: if the arrays are such that the function is not strictly decreasing, the heap might contain many states with the same value. But the number of such states is still bounded by the number of states we can reach with a given sum. However, in our case, the function is not a simple sum, but a product. But the monotonicity still holds. The number of states with the same value could be large. For example, if all A, B, C are equal, then many states might have the same value? Let's check: if all elements are 1, then f(i,j,k) = 1*1 + 1*1 + 1*1 = 3 for all states. So all N^3 states have the same value. Then the top K values are all 3. Our algorithm will start with (0,0,0) value 3, pop it, push neighbors (1,0,0), (0,1,0), (0,0,1) all with value 3. Then we pop one of them, push its neighbors, etc. The heap will quickly fill up with many states with value 3. But how many states will we push before we pop K times? Each pop generates up to 3 new states, but many might be duplicates? Actually, with all 1s, every state has value 3. The algorithm will just explore the lattice. The number of distinct states we can reach after t pops is at most the number of paths of length up to t? Actually, the number of distinct states visited after t pops is the number of states in the lattice that are within a certain Manhattan distance from (0,0,0). The maximum number of distinct states within Manhattan distance d from (0,0,0) in a 3D grid of size N is O(d^3). But we are not exploring all states within distance d; we are exploring in a specific order. In the worst case, if we pop the states in an order that corresponds to increasing distance, the number of states visited after t pops could be as large as O(t^3)? Let's analyze: The standard algorithm for K-th largest sum of three sorted arrays (with ascending order) is known to have worst-case time complexity O(K log K) if K is much smaller than N^3, but there is a catch: if the arrays have many duplicates, the algorithm might generate a large number of states. Actually, the standard algorithm using a heap and visited set for the "K-th smallest sum" problem (with sorted ascending) is correct and runs in O(K log K) time, but it requires that the sum function is non-decreasing in each coordinate (if sorted ascending). The number of generated states is at most 3K. This is a known result. Let's verify: In the worst case, each popped state generates 3 new states, but some of them might already be visited. The total number of states ever pushed is at most 3K + 1. Why? Because each state is pushed at most once (due to visited set). And each state is pushed only when it is generated by popping some state. The only way a state is generated is by incrementing one coordinate of a popped state. So each pushed state corresponds to a pop event that generated it. Since there are at most 3K pops, there are at most 3K pushes. So the number of distinct states ever pushed is at most 3K. So the visited set size is at most 3K. This is independent of the number of duplicates. So even if all values are the same, we will only push at most 3K states before we have popped K times. Because we stop after K pops. So we will never explore the entire lattice; we only explore up to 3K states. So the time complexity is O(K log K). The only issue is if the top K values are not among the first 3K states? But the algorithm is proven to find the K-th largest correctly because the heap always contains the smallest element among the unvisited states? Actually, it's the largest. The invariant is that the heap contains all unvisited states that are "minimal" in some sense. But is it always true that the K-th largest is among the first 3K popped states? Yes, because we pop K times, and we push at most 3 new states each time. So the maximum number of states we ever consider is K + 3K = 4K. So the algorithm will correctly find the K-th largest. This is a standard property of this algorithm. So it's correct.

But wait: In the case where all values are equal, the algorithm will pop (0,0,0), then push (1,0,0), (0,1,0), (0,0,1). Then it pops one of them, say (1,0,0), and pushes (2,0,0) (if N>1), (1,1,0), (1,0,1). So after 2 pops, we have 4 states in the heap: (0,1,0), (0,0,1), (1,1,0), (1,0,1), and maybe (2,0,0) if N>2. After t pops, the heap contains states that are on the "frontier". The number of states in the heap is the number of states with exactly one coordinate increased from the popped states? Actually, it's the number of unvisited states that have at least one neighbor popped. This is similar to the number of edges in a graph. The maximum number of states in the heap at any time is O(t). So it's fine.

So the algorithm is correct and efficient.

Now, we need to implement it in Python. Let's write the code.

Steps:
1. Import sys, heapq.
2. Read all input. Use sys.stdin.buffer.read() to read all at once, then split. This is faster.
3. Parse N, K.
4. Read the next N integers as A, next N as B, next N as C.
5. Sort A, B, C in descending order: A.sort(reverse=True), etc.
6. Precompute N_sq = N * N.
7. Initialize visited as a set.
8. Initialize heap as a list. The initial state is (0,0,0). Compute value = A[0]*B[0] + B[0]*C[0] + C[0]*A[0]. Push (-value, 0) because we encode the state as key = 0.
9. Add key 0 to visited.
10. Loop for _ in range(K):
    - Pop: neg_val, key = heapq.heappop(heap).
    - val = -neg_val.
    - This is the next largest. If _ == K-1, answer = val.
    - Decode key: k = key % N; temp = key // N; j = temp % N; i = temp // N.
    - For each neighbor: (i+1, j, k), (i, j+1, k), (i, j, k+1). But careful: we need to compute the new key for each.
    - For each neighbor, check bounds: if the index < N.
    - Compute new_key: if neighbor is (i+1, j, k), then new_key = (i+1)*N_sq + j*N + k. Similarly for others.
    - If new_key not in visited, add to visited, compute new_val, push (-new_val, new_key).
11. Print answer.

But we need to be careful: The initial state is (0,0,0). We mark it visited before pushing. Then we pop it. That's correct.

Now, we need to compute the value for a state. We can write a function that takes i, j, k and returns the value. But since we will compute it many times, we can inline it. However, we need to access A[i], B[j], C[k]. Since the arrays are sorted descending, the indices are 0-based.

One optimization: We can precompute A[i] + C[k]? Not necessary.

Let's test with the sample.

Potential issues:
- The heap can store up to 2K elements. The visited set can store up to 3K elements. For K=5e5, 3K=1.5e6. That's fine.
- The encoding: N_sq = N*N. For N=2e5, N_sq=4e10. Multiplying i by N_sq: i up to N-1, so i*N_sq up to 2e5*4e10=8e15. This fits in Python int.
- Decoding: key // N_sq gives i, then key % N_sq gives remainder, then // N gives j, % N gives k. This is straightforward.

We need to ensure that the heap comparison works correctly. Since we push (-val, key), the smallest first element corresponds to the largest val. If two vals are equal, the smaller key will be popped first. That's fine.

Now, we need to consider the case when N is large but K is small. The algorithm is still O(K log K), so it's fine.

But wait: There is a known issue with this algorithm for the "K-th largest sum" problem: if the arrays are sorted in ascending order, the algorithm works for K-th smallest. For descending, it's the same. But there is a subtlety: the function must be non-decreasing in each coordinate if sorted ascending, or non-increasing if sorted descending. Here it is non-increasing. So it's correct.

Let's double-check the monotonicity with an example. Suppose A=[5,4], B=[5,4], C=[5,4]. Sorted descending. Value for (0,0,0)=5*5+5*5+5*5=75. (1,0,0)=4*5+5*5+5*4=20+25+20=65. So 75 >= 65. (0,1,0)=5*4+4*5+5*5=20+20+25=65. (0,0,1)=65. So all neighbors are 65. So it's non-increasing.

Now, what if A=[5,1], B=[5,1], C=[5,1]? (0,0,0)=75. (1,0,0)=1*5+5*5+5*1=5+25+5=35. (0,1,0)=5*1+1*5+5*5=5+5+25=35. (0,0,1)=35. So non-increasing.

So it's correct.

Now, we should also consider if the input values are up to 1e9, and we multiply two of them, the product is up to 1e18, and sum of three such products is up to 3e18, which fits in Python int.

Now, let's think about the time. The main loop runs K times. Inside, we do:
- heappop
- decode key (3 operations)
- for up to 3 neighbors: check bounds, compute new_key, check visited, compute value, heappush.
Each heappop and heappush is O(log heap_size). The heap size is at most 2K. So log(2*5e5) ~ 20. So total operations: 5e5 * (1 + 3*2) = 5e5 * 7 = 3.5e6 heap operations? Actually, heappop is one, heappush is up to 3, so total heap operations: 1 pop + up to 3 pushes per iteration. So 4 * 5e5 = 2e6 heap operations. Each heap operation is O(20), so 40 million comparisons. That should be okay in Python if optimized.

But we also have the visited set lookups. 3 lookups per iteration, 1.5e6 lookups. Set lookup is O(1) average, so that's fine.

The main bottleneck might be the Python overhead. We can try to optimize by using local variables and avoiding function calls. We can also use array module or something, but not necessary.

One potential optimization: Instead of storing the key in the heap, we could store the negative value and the three indices directly. But that increases memory. However, it might be faster because we avoid decoding. Let's see: decoding involves two divisions and two modulo operations. That's 4 operations per pop. If we store i, j, k directly, we avoid that. But then the heap tuple has 4 elements, which might be slower to compare. Actually, comparing tuples in Python is element-wise. So comparing (neg_val, i, j, k) and (neg_val2, i2, j2, k2) will compare neg_val first, then if equal, compare i, then j, then k. That's 4 comparisons. But if we use (neg_val, key), then the comparison will compare neg_val first, then key. The key is a single integer, so one comparison. So (neg_val, key) might be faster for comparison because comparing integers is faster than comparing tuples. And decoding is just a few integer operations. So I think (neg_val, key) is better.

But we need to be careful with the order of key: we want the secondary key to be such that the order is consistent. Since we are using the key as a unique identifier, any order works. But we might want to ensure that the heap doesn't have to compare large keys unnecessarily. Since the keys are up to 8e15, comparing them is fast.

Let's write the code.

We need to be careful with the visited set: we should add the initial state to visited before pushing, to avoid pushing it again.

One more thing: The number of iterations is K. But we need to pop K times. However, the heap might become empty before we pop K times? That can only happen if the total number of states is less than K. But N^3 >= K because K <= N^3. So there are at least K states. So the heap will not be empty.

But wait: Is it possible that the heap becomes empty if we don't push enough states? No, because we start with 1 state, and each pop pushes at most 3, so the number of states in the heap is non-negative as long as we don't pop more than the total number of states. Since K <= N^3, we will not pop all states.

Now, let's consider the memory of the visited set. We are storing up to 1.5e6 integers. In Python, a set of integers is efficient. But we can also use a boolean array if N is small? But N can be 2e5, so N^3 is 8e15, we cannot use an array. So set is necessary.

We can also use a dictionary, but set is faster for membership testing.

Now, we need to ensure that the code is efficient. We can use `sys.setrecursionlimit` if needed, but not here.

Let's write the code step by step.

First, read input:
```python
import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    C = [int(next(it)) for _ in range(N)]
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)
    N_sq = N * N
    visited = set()
    # initial state
    i0, j0, k0 = 0, 0, 0
    key0 = 0
    visited.add(key0)
    val0 = A[0]*B[0] + B[0]*C[0] + C[0]*A[0]
    heap = [(-val0, key0)]
    heapq.heapify(heap)
    ans = None
    for _ in range(K):
        neg_val, key = heapq.heappop(heap)
        val = -neg_val
        ans = val