
## ideation
We need the K‑th largest value among all N³ triples
f(i,j,k) = A_i·B_j + B_j·C_k + C_k·A_i.

Observations:
- The expression is symmetric in (i,j,k) after renaming variables, but the three arrays are distinct.
- N can be up to 2·10⁵, so enumerating all N³ triples is impossible.
- K ≤ 5·10⁵, relatively small compared to N³.
- Values can be as large as ~10⁹·10⁹·3 ≈ 3·10¹⁸, fits in 64‑bit.

Goal: find the K‑th largest value efficiently.

Standard approach for “K‑th largest among all combinations of three arrays” is:
1. Sort the three arrays in descending order (or one of them).
2. Use binary search on the answer X.
3. For a candidate X, count how many triples satisfy f(i,j,k) ≥ X.
4. Find the largest X with count ≥ K.

Counting triples is the hard part. We need an O(N² log N) or O(N²) method.

Key rewriting:
f(i,j,k) = B_j·(A_i + C_k) + A_i·C_k.

If we fix j, we need to count pairs (i,k) such that
B_j·(A_i + C_k) + A_i·C_k ≥ X.

Let S = A_i + C_k, P = A_i·C_k.
Then condition: B_j·S + P ≥ X.

For a fixed S, P is maximized when A_i and C_k are as close as possible (by AM‑GM). Conversely, for a fixed S, P is minimized when one of them is as small as possible.

Idea: Sort A in descending order, sort C in descending order. For each j, we can iterate over i (or over k) and use two‑pointer technique over the other array to count valid pairs.

Alternative: For each j, we can iterate over i (A_i) and for each i find the range of k such that the inequality holds. Since C_k is sorted, we can binary search on C_k.

Let's analyze the inequality for fixed i,j:
B_j·(A_i + C_k) + A_i·C_k ≥ X
=> B_j·A_i + B_j·C_k + A_i·C_k ≥ X
=> C_k·(B_j + A_i) ≥ X - B_j·A_i
=> C_k ≥ (X - B_j·A_i) / (A_i + B_j)   if A_i + B_j > 0.

Since all values are positive (≥1), A_i + B_j > 0 always. So we can binary search on C_k (sorted descending) to find how many C_k satisfy the condition.

Thus for each pair (i,j), we can count in O(log N) the number of valid k. Total O(N² log N) which is too slow for N=2·10⁵.

We need O(N²) or O(N² log N) with small constant? N² is 4·10¹⁰, impossible.

Better approach: Fix j, and iterate over i. For each i, we need to count k such that:
C_k ≥ (X - B_j·A_i) / (A_i + B_j).

Since C is sorted descending, we can precompute for each j an array of thresholds? No, thresholds depend on i.

Alternative: Sort A descending. For fixed j, as i increases, A_i decreases. The threshold for C_k changes. We can use two pointers: iterate i from 0 to N-1, and for each i find the smallest k such that the condition holds. Since A_i is decreasing, the threshold (X - B_j·A_i)/(A_i + B_j) might increase or decrease? Let's check monotonicity.

Let T(i) = (X - B_j·A_i) / (A_i + B_j).
As A_i decreases, numerator X - B_j·A_i increases (since -B_j·A_i becomes less negative), denominator A_i + B_j decreases. So T(i) increases as A_i decreases. That means the required C_k threshold gets larger as i increases. Since C_k is sorted descending, larger threshold means fewer valid k. So the number of valid k is non‑increasing as i increases. This suggests a two‑pointer approach: we can maintain a pointer k that only moves left (decreases) as i increases. However, we need to count total pairs, not just find one.

Actually, for each i we need to count how many k satisfy C_k ≥ T(i). Since C is sorted descending, the count is simply the index of the first element < T(i). Let’s call this count(i). Then total for fixed j is sum_i count(i).

If we process i in order of decreasing A_i (which is sorted descending), T(i) is increasing, so the cutoff index in C is non‑increasing. We can maintain a pointer `pos` starting at 0 (meaning all C_k are valid). As i increases, we move `pos` to the right (decrease count) until C[pos] < T(i). Then count(i) = pos. Sum over i.

This is O(N) per j, total O(N²) which is still too large (4·10¹⁰).

We need to reduce further. Since K ≤ 5·10⁵, we might not need to count all triples, but we need exact count to binary search. However, we can binary search on X and count. The counting must be efficient.

Alternative: Use the symmetry. The expression f(i,j,k) = A_i·B_j + B_j·C_k + C_k·A_i can be seen as sum of three pairwise products. There is a known technique: sort all three arrays, then for each i (largest A), we can consider pairs (j,k) and use two‑pointer. But still O(N²).

Wait, maybe we can fix the largest of the three? Since we want K‑th largest, and K is at most 5·10⁵, we can consider only the top K elements of each array? But the combination of top K from each gives K³ which is huge.

Another angle: The expression is linear in each variable when the other two are fixed. But we need to find K‑th largest.

Let's think about the structure: f(i,j,k) = (A_i + C_k)·B_j + A_i·C_k.
If we sort A and C descending, then for each j, we need to count pairs (i,k) with B_j·(A_i + C_k) + A_i·C_k ≥ X.

This is similar to counting pairs with a condition involving sum and product. There is a known trick: for fixed sum S = A_i + C_k, the product A_i·C_k is maximized when they are close. But we have inequality B_j·S + P ≥ X. For a given S, the maximum possible P is (S/2)² (if we could choose any split). However, A_i and C_k are discrete from the arrays.

Maybe we can iterate over possible sums S? There are at most N² possible sums A_i + C_k, which is too many.

But we can sort all pairs (A_i, C_k) by A_i + C_k? Still N².

Alternative: Since K is small (≤ 5·10⁵), we can use a priority queue to generate the top K values directly? For three arrays, generating top K combinations can be done with a heap in O(K log K) if we can efficiently generate next candidates. But the state space is 3D, not straightforward.

Wait, the expression is symmetric. We can think of it as: pick one element from each array. The value is sum of pairwise products. This is like the sum of products of three numbers.

There is a known problem: given three arrays, find K‑th largest sum of products A_i·B_j + B_j·C_k + C_k·A_i. This is a known AtCoder problem (ABC or ARC). The typical solution is:

1. Sort A, B, C in descending order.
2. For each i (top X of A) and j (top Y of B), compute the value with the largest C (i.e., C_1) and push into a heap. Then pop the largest, and push the next candidate by incrementing the C index or something. But the heap would need to track (i,j,k) and avoid duplicates.

But the number of candidates is huge. However, since K ≤ 5·10⁵, we can limit the search to the top L elements of each array where L is small enough such that L³ ≥ K? If we take top L from each, we get L³ combinations. To get at least K=5·10⁵, we need L ≥ 100 (since 100³=1e6). So we could take top 1000 from each? 1000³ = 1e9, too many to generate.

But we can use a heap that only expands necessary nodes. However, the heap approach for 3D is tricky because the "next" candidates are not simply neighbors.

Let's reconsider the binary search + counting approach. We need to count number of triples with f ≥ X efficiently.

We have f(i,j,k) = A_i·B_j + B_j·C_k + C_k·A_i.

Fix j. Then we need to count pairs (i,k) such that:
A_i·B_j + B_j·C_k + C_k·A_i ≥ X
=> B_j·(A_i + C_k) + A_i·C_k ≥ X.

Let’s denote u = A_i, v = C_k. We need B_j·(u+v) + u·v ≥ X.

For fixed B_j, this is a condition on pairs (u,v). We can sort u descending, v descending.

We can iterate over u (i from 0 to N-1). For each u, we need to count v such that:
v·(B_j + u) ≥ X - B_j·u
=> v ≥ (X - B_j·u) / (B_j + u).

Since v is sorted descending, we can find the first index where v < threshold, and count is that index. This is O(N) per j using two pointers if we process u in order and maintain pointer for v. But as argued, the threshold increases as u decreases, so the pointer moves left (decreasing count). So we can do O(N) per j.

But O(N²) is too slow. However, note that K ≤ 5·10⁵. We don't need to count all triples; we only need to know if count ≥ K. So we can stop early once we have counted K. That could reduce the work.

But in the worst case, X is small (close to minimum), so count could be N³, and we need to count many. But we can binary search; the count function is monotonic. We need to evaluate count(X) for various X. If we can compute count(X) in O(N²) worst case, that's too slow.

We need a faster counting method.

Let's think about the structure of the inequality:
B_j·(u+v) + u·v ≥ X.

We can rewrite as:
(u + B_j)·(v + B_j) ≥ X + B_j².

Because:
(u + B_j)(v + B_j) = u·v + u·B_j + v·B_j + B_j² = u·v + B_j·(u+v) + B_j².

So the condition is:
(u + B_j)(v + B_j) ≥ X + B_j².

That's a huge simplification!

Let’s verify:
A_i·B_j + B_j·C_k + C_k·A_i = B_j·(A_i + C_k) + A_i·C_k.
Add B_j² to both sides? Actually:
(A_i + B_j)(C_k + B_j) = A_i·C_k + A_i·B_j + C_k·B_j + B_j².
So indeed:
f(i,j,k) + B_j² = (A_i + B_j)(C_k + B_j).

Thus f(i,j,k) ≥ X  <=>  (A_i + B_j)(C_k + B_j) ≥ X + B_j².

This is beautiful! Now the condition is a product of two terms.

Let’s define:
A'_i = A_i + B_j,
C'_k = C_k + B_j.

Then we need A'_i · C'_k ≥ X + B_j².

Since B_j is fixed for a given j, we can precompute A'_i = A_i + B_j and C'_k = C_k + B_j. Both are just shifted versions of A and C. Since A and C are positive, A'_i and C'_k are positive and sorted in the same order as A and C (if we sort A and C descending, then A' and C' are also descending).

Now we need to count pairs (i,k) such that A'_i · C'_k ≥ Y, where Y = X + B_j².

This is a classic problem: count pairs with product ≥ Y in two sorted arrays. Since both arrays are sorted descending, we can use two pointers in O(N) time per j.

Specifically:
- i = 0, k = 0.
- While i < N and k < N:
  - If A'[i] * C'[k] ≥ Y, then all pairs (i, k') for k' ≥ k are valid? Wait, careful with sorting order.

We have A' sorted descending, C' sorted descending.
We want to count pairs (i,k) with A'[i] * C'[k] ≥ Y.

We can use two pointers:
- Initialize count = 0.
- For each i from 0 to N-1:
  - While k < N and A'[i] * C'[k] < Y:
    - k += 1
  - If k == N, break (no more valid k for any larger i? Actually as i increases, A'[i] decreases, so product decreases. So if for current i, we need k to be larger (i.e., smaller C'), then for next i (smaller A'), we will need even larger k. So we can break the outer loop when k == N.)
  - count += (N - k).

This is O(N) per j. Total O(N²) for counting all j. Still too slow for N=2e5.

But wait, we can do better? We have N up to 2e5, N² is 4e10, impossible.

However, note that K ≤ 5e5. We only need to count up to K. So we can stop early. But in the binary search, we need to know if count ≥ K. If we stop early when count reaches K, we can return K (or a value ≥ K). But we need the exact count for the binary search to work correctly? Actually, to binary search for the largest X with count ≥ K, we need to know whether count ≥ K or not. We don't need the exact count, just whether it's ≥ K. So we can cap the counting at K. That means we can stop as soon as count ≥ K.

But can we compute count ≥ K efficiently without iterating over all j? We need to sum over j. For each j, we count pairs (i,k). If we stop early for each j when count_j ≥ K, we might still do O(N) per j in the worst case if many j have large counts. But if we only need to know if total ≥ K, we can process j in some order and stop when total ≥ K.

But the binary search requires evaluating count(X) for many X (up to ~60 iterations). Each evaluation must be fast enough. If we can do O(N) per evaluation, that's 2e5 * 60 = 1.2e7, which is fine! Wait, O(N) per evaluation is great. But we have O(N) per j? No, we need to sum over all j. If we do O(N) per j, that's O(N²). But we can do O(N) total per evaluation if we are clever?

Let's think: For a fixed X, we need to count triples (i,j,k) such that (A_i + B_j)(C_k + B_j) ≥ X + B_j².

We can think of this as: for each j, we need to count pairs (i,k) with product ≥ Y_j = X + B_j².

If we could process all j together, maybe we can sort B and use some data structure.

Alternatively, note that the condition is symmetric. We can fix i and k, and sum over j? That would be similar.

But the O(N) per j is too slow. However, we can reduce the work by noting that for large B_j, Y_j is large, so the count of pairs might be small. For small B_j, Y_j is small, count is large. But we still need to iterate over all j.

Wait, maybe we can sort B and process j in order of decreasing B_j. As B_j decreases, Y_j decreases, so the count for each j increases. But we still need to sum over all j.

Is there a way to compute the total count in O(N log N) or O(N)?

Let's analyze the condition: (A_i + B_j)(C_k + B_j) ≥ X + B_j².

Let’s denote a = A_i, b = B_j, c = C_k.
Condition: (a+b)(c+b) ≥ X + b².

We can rewrite as: a·c + b·(a+c) + b² ≥ X.
Which is original.

Maybe we can fix the sum S = a + c? Not helpful.

Another idea: Since K is small, we can use a selection algorithm? But we need exact K-th largest.

Let's reconsider the binary search + counting with early termination. For a given X, we need to count triples with f ≥ X. We can iterate over j (or i or k). For each j, we count pairs (i,k) using two pointers in O(N). That's O(N²) per X. Too slow.

But we can iterate over i instead? Same.

We need a sub-quadratic counting method.

Observation: The condition (A_i + B_j)(C_k + B_j) ≥ X + B_j² is equivalent to:
A_i + B_j ≥ (X + B_j²) / (C_k + B_j).

For fixed k and j, we can count i. Still O(N²).

Maybe we can use the fact that the arrays are sorted and we can use a merge-like process across all three arrays simultaneously.

Consider sorting A, B, C all descending. We want to count triples with f ≥ X.

We can think of a 3D grid. The condition defines a region. We need to count points in that region.

Alternatively, we can use the following approach: Since K ≤ 5e5, we can find the K-th largest by generating the top K values using a priority queue, but we need to ensure we don't miss any. The heap approach for 3D sum of products is known but tricky.

Let's search memory: This problem is likely from AtCoder. "K-th largest value among A_i B_j + B_j C_k + C_k A_i". I recall a problem: ABC 134 F? No. Maybe ARC 080? Or a typical problem.

Actually, there is a known solution: Sort A, B, C in descending order. Then for each i (0 to N-1) and j (0 to N-1), compute the value with k=0 (largest C), and push into a heap. Then repeatedly extract the maximum, and push the next candidate by incrementing k. But we need to avoid duplicates and ensure we cover all top K. The heap size would be O(K) and each operation O(log K). But the number of pushes could be large? Actually, we start with N² candidates (i,j) with k=0. That's too many (4e10). So we cannot push all N².

But we can limit i and j to small ranges? Since K is small, the top K values likely come from the top elements of each array. If we take top L from each, we get L³ combinations. To get K=5e5, we need L ≈ 100 (100³=1e6). So we could take top 1000 from each? 1000³=1e9, too many to generate.

But we can use a heap that only stores necessary (i,j,k) triples. However, the "next" triples from a popped (i,j,k) would be (i+1,j,k), (i,j+1,k), (i,j,k+1). But we need to ensure we don't push too many.

Actually, there is a known algorithm for K-th largest sum of three arrays: use binary search on the answer and count using O(N²) with early termination? But O(N²) is too slow.

Wait, maybe we can count in O(N log N) per X using the following: For each j, we need to count pairs (i,k) with (A_i + B_j)(C_k + B_j) ≥ Y. This is equivalent to counting pairs with product ≥ Y in two arrays of size N. There is an O(N log N) algorithm for counting pairs with product ≥ Y in two sorted arrays? Actually, for two sorted arrays, counting pairs with product ≥ Y can be done in O(N) using two pointers if both are sorted in the same order. But if they are sorted in opposite orders, it's O(N log N). Here both are sorted descending, so O(N) per j.

But O(N) per j is O(N²). However, we can note that for many j, the count might be 0 or N², and we can skip? Not really.

Maybe we can use the fact that the condition is symmetric and we can fix the maximum of the three? Since we want large values, the largest values come from large A, B, C. So we can restrict to the top M elements of each array, where M is chosen such that the number of triples among them is at least K, and the K-th largest overall is guaranteed to be among them. Then we can brute force or use a heap on that smaller set.

What M to choose? If we take top M from each, we get M³ triples. We need M³ ≥ K to ensure the K-th largest is among them? Not necessarily; the K-th largest overall might involve a smaller element if the top M³ are not the actual top K? Actually, if we take the top M elements from each array, the maximum possible value is achieved by the top elements. But the K-th largest overall might involve an element outside the top M if the distribution is skewed? No, if we take the top M from each, any triple using an element outside top M would have at least one smaller element, so its value would be less than or equal to some triple using only top M? Not necessarily, because the expression is not monotonic in each variable independently? Wait, f(i,j,k) = A_i B_j + B_j C_k + C_k A_i. If we increase A_i, does f always increase? Let's check partial derivative w.r.t A_i: B_j + C_k > 0. So yes, f is strictly increasing in each variable (since all values positive). Therefore, if we replace any element with a smaller one, the value decreases. So the maximum values are achieved by the largest elements. More precisely, if we sort A descending, B descending, C descending, then the set of triples (i,j,k) with i,j,k in [0, M-1] contains the top M³ values. So if we choose M such that M³ ≥ K, then the K-th largest overall is guaranteed to be within the top M elements of each array. Because any triple with an index ≥ M has at least one element smaller than the M-th largest, so its value is less than some triple with all indices < M? Actually, we need to be careful: Suppose we have A sorted descending. If we take i ≥ M, then A_i ≤ A_{M-1}. But we could have j < M and k < M. The value f(i,j,k) might still be larger than some triple with i < M, j ≥ M, k ≥ M? But we want to guarantee that the top K values are all within the first M elements of each array. Since f is increasing in each argument, the maximum value for a given set of indices is achieved by the smallest indices. So the set of triples with i,j,k < M is exactly the set of M³ largest values? Not exactly: The values are not totally ordered by index because the expression is not separable. However, if we consider the partial order: (i,j,k) ≤ (i',j',k') if i ≤ i', j ≤ j', k ≤ k' (with sorted descending arrays, smaller index means larger value). Then f is monotonic with respect to this partial order: if (i,j,k) ≤ (i',j',k') in the index order (i.e., i ≤ i', j ≤ j', k ≤ k'), then A_i ≥ A_{i'}, etc., so f(i,j,k) ≥ f(i',j',k'). So the values are monotonic in the product order. Therefore, the top M³ values are exactly the triples with i,j,k < M? Not exactly, because there could be triples with some indices small and some large that are larger than some triples with all indices small. But the set of triples with all indices < M is an "upward closed" set in the index partial order (if we consider smaller index as "larger" element). Actually, if we define the order as i ≤ i' means A_i ≥ A_{i'}, then the set of triples with i < M, j < M, k < M is the set of "maximal" elements in the product order? No, it's the set of elements that are minimal in the index order (i.e., largest values). Any triple with an index ≥ M has at least one coordinate larger (i.e., smaller value). So it is "less than or equal to" some triple with all coordinates < M? Not necessarily: consider (M, 0, 0) vs (0, M, M). Which is larger? f(M,0,0) = A_M B_0 + B_0 C_0 + C_0 A_M. f(0,M,M) = A_0 B_M + B_M C_M + C_M A_0. It's not clear which is larger. So the top M³ values are not necessarily exactly the triples with all indices < M. However, the K-th largest value will involve only elements that are among the top something.

But we can bound: For any triple (i,j,k), if we replace A_i with A_0 (the largest), B_j with B_0, C_k with C_0, we get a larger or equal value. So the maximum value overall is f(0,0,0). The K-th largest value is at most the K-th largest value among triples where we pick the largest available element for each coordinate? That doesn't help.

Actually, we can use the following: Since f is increasing in each variable, if we take the top L elements from each array, the number of triples is L³. If we choose L such that L³ ≥ K, then the K-th largest value overall is at least the minimum value among those L³ triples? No, the K-th largest overall could be smaller than the minimum of those L³ triples if the L³ triples are not the actual top K. But we can choose L large enough so that the L³ triples include the top K. How large? We need to ensure that any triple not in the top L³ has value ≤ the K-th largest among the top L³. This is not guaranteed for a fixed L.

However, we can use the binary search approach with counting, but we need to count efficiently.

Let's revisit the counting with the product form:
f(i,j,k) + B_j² = (A_i + B_j)(C_k + B_j).

We want to count triples with f ≥ X, i.e., (A_i + B_j)(C_k + B_j) ≥ X + B_j².

Let Y_j = X + B_j².

For each j, we need to count pairs (i,k) with (A_i + B_j)(C_k + B_j) ≥ Y_j.

This is equivalent to: for each i, count k such that C_k + B_j ≥ Y_j / (A_i + B_j).

Since C_k is sorted descending, C_k + B_j is also sorted descending. So for fixed j, we can iterate i from 0 to N-1, and for each i, find the smallest k such that C_k + B_j < Y_j / (A_i + B_j). The count is that k. Since A_i + B_j is decreasing as i increases, the threshold Y_j / (A_i + B_j) is increasing. So the required k is non-decreasing. Thus we can use a pointer that moves forward. This is O(N) per j.

But O(N) per j is O(N²). However, we can note that for many j, the count might be 0 or N. But we still need to process them.

Wait, can we process all j simultaneously? We have three arrays. The condition involves B_j in a specific way. Maybe we can sort B and use a data structure to query for each i,k the number of j satisfying the condition? That would be O(N² log N) or something.

Alternatively, we can fix i and k, and sum over j. The condition is:
(A_i + B_j)(C_k + B_j) ≥ X + B_j².

Let’s denote b = B_j. Then:
(A_i + b)(C_k + b) ≥ X + b²
=> A_i C_k + b(A_i + C_k) + b² ≥ X
=> b² + (A_i + C_k)b + (A_i C_k - X) ≥ 0.

This is a quadratic inequality in b. For fixed A_i and C_k, we can solve for b. Since b > 0, we can find the range of b that satisfies it. Then we can count how many B_j are in that range. Since B is sorted, we can binary search. This would be O(N² log N) for counting all pairs (i,k). Still too slow.

But we can limit the pairs (i,k) we consider? Since K is small, we only need to consider pairs that could produce large values. The largest values come from large A_i and C_k. So we can restrict i and k to the top L elements. If we choose L such that L² ≥ K, then we only need to consider L² pairs. For each pair, we can count j in O(log N) using binary search on B. Total O(L² log N). If L=1000, L²=1e6, log N≈18, total ~1.8e7, which is feasible. But we need to ensure that the K-th largest is among these L² pairs.

Is it true that the K-th largest value involves only the top L elements of A and C? Not necessarily, because a large B_j could compensate for small A_i and C_k. However, since B_j is also an array, we can similarly restrict B to top L. If we take top L from each, we have L³ triples. If L³ ≥ K, then the K-th largest is among them. So we can set L = ceil(K^(1/3)) + some margin. For K=5e5, K^(1/3) ≈ 79. So L=100 gives 1e6 triples. That's small enough to brute force? 1e6 triples is fine to compute and sort. But wait, we need to find the K-th largest among all N³ triples. If we only consider the top L from each, we might miss some triples that are in the top K but involve an element outside the top L. For example, suppose A has one huge value and many small ones. The top K might involve the huge A with many combinations of B and C, some of which might have B or C outside the top L. But if we take top L of B and C, we might miss some.

However, we can use the following: The K-th largest value is at least the K-th largest value among the top L³ triples. If we choose L large enough such that the number of triples with any element outside top L is less than K, then we are safe. But that's not easy to guarantee.

Alternatively, we can use the binary search + counting approach but with a faster counting method that is O(N log N) or O(N) per X.

Let's think about the counting again. We need to count triples with (A_i + B_j)(C_k + B_j) ≥ Y_j.

We can rewrite as: for each j, count pairs (i,k) with product ≥ Y_j.

If we could compute for each possible product threshold the number of pairs, we could sum over j. But Y_j varies with j.

Maybe we can sort the pairs (i,k) by the product (A_i + B_j)(C_k + B_j)? Not helpful.

Another idea: Since K ≤ 5e5, we can use a selection algorithm that finds the K-th largest without sorting all. But we need to count.

Wait, there is a known solution for this exact problem. Let me recall: This is from AtCoder ABC 134 F? No, ABC 134 F is about permutations. Maybe it's from a contest like "K-th Largest A_i B_j + B_j C_k + C_k A_i". I think it's from AtCoder Regular Contest 080 F? Or maybe a typical problem.

Actually, I remember a problem: "K-th Largest Sum of Products" where the expression is A_i * B_j + B_j * C_k + C_k * A_i. The solution involves sorting the arrays and using a priority queue with a trick to avoid duplicates. But the heap approach for 3D is tricky.

Let's think about the heap approach more carefully. We want the top K values of f(i,j,k). Since f is increasing in each variable, the maximum is at (0,0,0). The next maximum could be (0,0,1), (0,1,0), or (1,0,0). We can push these into a heap. Then we pop the largest, and push its "neighbors": (i+1,j,k), (i,j+1,k), (i,j,k+1). But we need to avoid duplicates. This is similar to generating top K sums from three sorted arrays. However, the number of pushes could be up to 3K, which is fine. But we need to ensure that we don't miss any candidates. The issue is that the "neighbors" might not cover all possibilities? Actually, if we start with (0,0,0) and always push the three neighbors of the popped node, we will generate all triples in the product order? This is a known method for K-th largest sum of three arrays: use a visited set or a tuple of indices. Since K ≤ 5e5, the heap size is manageable. The time complexity is O(K log K). This is very efficient!

Let's verify: We have three arrays sorted descending. We want the K-th largest value of f(i,j,k). We can use a max-heap. Initially, push (f(0,0,0), 0,0,0). Then we pop the largest, and push the three neighbors: (i+1,j,k), (i,j+1,k), (i,j,k+1), provided the indices are within bounds and not already visited. We use a set or a 3D boolean array to mark visited. Since N can be up to 2e5, we cannot use a 2D array of size N². But we can use a hash set of tuples (i,j,k). The number of visited nodes is at most 3K (since each pop pushes at most 3 new nodes, and we pop K times). So the hash set size is O(K). This is feasible.

But is it correct? The heap generates triples in decreasing order of f? Not necessarily, because f is not monotonic in the index order in a simple way? Wait, f is increasing in each variable, so if we increase any index, f decreases. So the function f is strictly decreasing in each coordinate (since arrays are sorted descending). Therefore, the set of triples is a 3D grid where moving in the positive direction (increasing index) decreases the value. The heap starting from (0,0,0) and expanding to neighbors (i+1,j,k), (i,j+1,k), (i,j,k+1) will generate all triples in some order. But does it generate them in sorted order? Not necessarily, because there could be a triple like (1,0,0) that is larger than (0,1,0). The heap will correctly order them because we push the actual values. The key is that we don't miss any triple. Since we start from the maximum and expand to all neighbors, we will eventually reach every triple? Actually, from (0,0,0), we can reach (i,j,k) by a path of steps in the positive directions. So yes, we can reach any triple. The heap will generate them in order of value. This is a standard algorithm for K-th largest sum from multiple sorted arrays.

However, there is a catch: The number of pushes could be large if we don't limit the search space. But we only need the top K. So we stop after popping K times. The heap will contain at most 3K elements. The visited set will have at most 3K entries. This is O(K log K) time and O(K) space. Since K ≤ 5e5, this is very fast.

But wait: Is it guaranteed that the top K values are all within the region explored? Yes, because we explore in decreasing order of value. The heap always contains the smallest index among the "frontier". The maximum value in the heap is the next largest value overall. So after K pops, we have the K largest values. The K-th pop gives the K-th largest value.

This seems perfect! Let's double-check with the sample. N=2, K=5. Arrays sorted descending: A=[2,1], B=[4,3], C=[6,5]. Heap:
- Push (44, 0,0,0) -> f(0,0,0)=2*4+4*6+6*2=8+24+12=44.
- Pop 44. Push neighbors: (1,0,0)=f(1,0,0)=1*4+4*6+6*1=4+24+6=34; (0,1,0)=f(0,1,0)=2*3+3*6+6*2=6+18+12=36; (0,0,1)=f(0,0,1)=2*4+4*5+5*2=8+20+10=38.
- Heap: 38, 36, 34. Pop 38 (0,0,1). Push neighbors: (1,0,1)=1*4+4*5+5*1=4+20+5=29; (0,1,1)=2*3+3*5+5*2=6+15+10=31; (0,0,2) out of bounds.
- Heap: 36, 34, 31, 29. Pop 36 (0,1,0). Push neighbors: (1,1,0)=1*3+3*6+6*1=3+18+6=27; (0,2,0) out; (0,1,1) already visited? We need to check visited. (0,1,1) was pushed from (0,0,1)? Actually, (0,1,1) is neighbor of (0,1,0) in k direction? Wait, neighbors are (i+1,j,k), (i,j+1,k), (i,j,k+1). For (0,1,0), neighbors are (1,1,0), (0,2,0), (0,1,1). (0,1,1) was already pushed from (0,0,1) as (0,1,1)? No, from (0,0,1), neighbors are (1,0,1), (0,1,1), (0,0,2). So (0,1,1) is already in heap or visited. We must avoid duplicates. So we use a visited set.
- Heap after popping 36: 34, 31, 29, 27. Pop 34 (1,0,0). Push neighbors: (2,0,0) out; (1,1,0) already visited? (1,1,0) was pushed from (0,1,0) as (1,1,0)? Actually, (1,1,0) is neighbor of (0,1,0) in i direction? Wait, (0,1,0) neighbors: (1,1,0), (0,2,0), (0,1,1). So (1,1,0) is already pushed. (1,0,1) already pushed. So no new.
- Heap: 31, 29, 27. Pop 31 (0,1,1). This is the 5th pop. Value 31. Correct!

So the heap approach works! The time complexity is O(K log K). For K=5e5, log K ≈ 19, so about 1e7 operations, which is fine in Python if optimized (using heapq). The visited set can be a set of tuples (i,j,k). However, storing tuples of three integers in a set might be slow due to hashing. We can encode the triple into a single integer: i * N * N + j * N + k, but N can be 2e5, so N² is 4e10, which fits in 64-bit. So we can use a 64-bit integer as key. Or we can use a dictionary with tuple keys. But we need to be careful with memory: 3K = 1.5e6 entries. Each entry in a set is maybe 72 bytes, so ~100 MB. Might be tight but possible. Alternatively, we can use a more efficient visited structure: since we only push neighbors, we can use a 2D array of sets? Not needed.

But wait: Is the heap approach always correct? The function f is strictly decreasing in each coordinate (since arrays are sorted descending and all values positive). So the partial order is a product order. The heap starting from (0,0,0) and expanding to all immediate successors (i+1,j,k), (i,j+1,k), (i,j,k+1) will generate all elements in the product order. This is a known algorithm for "K-th smallest/largest in a partially ordered set" when the set is a grid and the function is monotonic. However, there is a subtlety: The heap might generate elements that are not the immediate successors in the value order, but that's fine because the heap orders by value. The key is that we don't miss any element. Since every element can be reached by a path from (0,0,0) by incrementing one coordinate at a time, and we push all neighbors of popped elements, we will eventually push every element. But we only push neighbors that are within bounds and not visited. So we will generate all elements in the frontier. The heap will contain the "current frontier" of unvisited elements that are adjacent to visited ones. The maximum of the frontier is the next maximum overall. This is exactly the algorithm for K-th largest sum of k sorted arrays. It works for any monotonic function on a product set.

But is f strictly decreasing in each coordinate? Let's check: f(i,j,k) = A_i B_j + B_j C_k + C_k A_i.
∂f/∂i = B_j + C_k > 0. Since B_j, C_k ≥ 1, it's positive. So as i increases (A_i decreases), f decreases. Similarly for j and k. So yes, f is strictly decreasing in each index when arrays are sorted descending.

Thus the heap approach is valid and efficient.

However, there is a potential issue: The number of pushes is at most 3K, but we also need to check bounds and visited. The visited set size is O(K). This is fine.

But wait: The sample input 3 has N=5, K=54. The heap would work. But what about the time limit? The problem likely expects an O(N log N) or O(K log K) solution. Since K ≤ 5e5, O(K log K) is definitely acceptable.

Let's verify the constraints: N up to 2e5, but K is at most 5e5. So the heap approach is independent of N (except for the array sizes). We only need to access A[i], B[j], C[k] for indices up to maybe O(K) in each dimension? Actually, the heap might push indices up to N-1. But we only push K times, so the maximum index we might access is at most K (since each pop pushes at most one new index in each dimension? Actually, we could push (i+1,j,k) many times, but i can grow up to N-1. However, we only pop K times, so the maximum i we might encounter is at most K (because to reach index i, we need to have popped at least i times in that dimension? Not exactly: we could have (0,0,0) -> (1,0,0) -> (2,0,0) ... So after K pops, we could have i up to K. So we only need the first K elements of each array? But wait, what if the K-th largest value involves an index larger than K? For example, if A has many equal values, we might need to go deeper. But since K ≤ 5e5, and N can be 2e5, K could be larger than N. If K > N, we might need indices beyond N? No, N is the length. If K > N, we still only have N elements. But the heap will generate indices up to N-1. However, if K is large (e.g., K = N³, but K ≤ 5e5, and N can be 2e5, so N³ is huge, but K is capped at 5e5). So K is at most 5e5. N can be 2e5. So K could be larger than N. In that case, we might need to access all N elements of each array. That's fine.

But there is a catch: The heap approach generates the top K values. However, the number of distinct values might be less than K if there are many duplicates. The problem asks for the K-th largest value, so if there are ties, we need to handle them correctly. The heap will generate values in non-increasing order. If we pop K times, the K-th popped value is the K-th largest. If there are duplicates, the order among them doesn't matter as long as we count them correctly. The heap will naturally handle duplicates because we push each triple separately. But if there are many duplicates, the heap might have many entries with the same value. That's fine.

One potential issue: The visited set prevents pushing the same triple multiple times. But if there are duplicate values from different triples, we still need to count them separately for the K-th largest. The visited set ensures we don't push the same (i,j,k) twice. That's correct.

So the heap approach seems correct and efficient.

But wait: Is it always true that the top K values are generated by this neighbor expansion? Yes, because the set of triples is a 3D grid, and we are performing a best-first search on a monotonic function. This is exactly the algorithm for "K-th largest sum of products" or similar. I've seen this in problems like "K-th smallest sum of three arrays".

However, there is a known issue with this approach: The number of visited nodes can be up to 3K, but the heap operations are O(log (3K)). This is fine.

But let's consider the time complexity more carefully. For each pop, we push up to 3 neighbors. So total pushes ≤ 3K. Each push/pop is O(log K). So total O(K log K). For K=5e5, log K ≈ 19, so about 1e7 heap operations. In Python, this might be a bit slow but should pass with optimization (using heapq and a set). However, we need to compute f(i,j,k) quickly. f(i,j,k) = A[i]*B[j] + B[j]*C[k] + C[k]*A[i]. This involves three multiplications and two additions. That's fine.

But wait: The arrays are given in the original order. We need to sort them descending. But the indices i,j,k in the heap correspond to the sorted order. So we need to sort A, B, C and keep the sorted arrays. The original indices don't matter.

So the algorithm:
1. Read N, K.
2. Read arrays A, B, C.
3. Sort A, B, C in descending order.
4. Initialize a max-heap (using negative values for heapq).
5. Push (-f(0,0,0), 0, 0, 0).
6. Initialize visited set: add (0,0,0) encoded as 0*N*N + 0*N + 0 = 0.
7. For _ in range(K):
   - Pop the heap: val, i, j, k = heapq.heappop(heap). val is negative, so actual value = -val.
   - If this is the K-th pop, output -val and return.
   - For each neighbor (i+1,j,k), (i,j+1,k), (i,j,k+1):
     - If within bounds and not visited:
       - Compute f.
       - Push (-f, i', j', k').
       - Add to visited.

This should work.

But is there any risk of memory or time issues? The visited set can be a Python set of integers. Each integer is up to N^3, which is up to 8e15, fits in Python int. The set will have up to 3K = 1.5e6 entries. That's fine.

However, we need to be careful: The heapq in Python is a min-heap. We push negative values to simulate max-heap. The tuple (-val, i, j, k) will be ordered by -val, then i, j, k. That's fine.

But there is a subtle bug: When we push neighbors, we might push the same neighbor from different parents. The visited set prevents duplicates. But we need to ensure we check visited before pushing. That's standard.

Let's test with sample 1:
N=2, K=5.
A=[2,1], B=[4,3], C=[6,5].
Heap: [(-44,0,0,0)]
Pop 1: val=44, i=j=k=0. Output? Not yet.
Push neighbors:
(1,0,0): f=1*4+4*6+6*1=34 -> push (-34,1,0,0)
(0,1,0): f=2*3+3*6+6*2=36 -> push (-36,0,1,0)
(0,0,1): f=2*4+4*5+5*2=38 -> push (-38,0,0,1)
Visited: (0,0,0), (1,0,0), (0,1,0), (0,0,1)
Heap: [(-38,0,0,1), (-36,0,1,0), (-34,1,0,0)]
Pop 2: val=38, (0,0,1)
Push neighbors:
(1,0,1): f=1*4+4*5+5*1=29 -> push (-29,1,0,1)
(0,1,1): f=2*3+3*5+5*2=31 -> push (-31,0,1,1)
(0,0,2): out
Visited add (1,0,1), (0,1,1)
Heap: [(-36,0,1,0), (-34,1,0,0), (-31,0,1,1), (-29,1,0,1)]
Pop 3: val=36, (0,1,0)
Push neighbors:
(1,1,0): f=1*3+3*6+6*1=27 -> push (-27,1,1,0)
(0,2,0): out
(0,1,1): already visited
Heap: [(-34,1,0,0), (-31,0,1,1), (-29,1,0,1), (-27,1,1,0)]
Pop 4: val=34, (1,0,0)
Push neighbors:
(2,0,0): out
(1,1,0): already visited
(1,0,1): already visited
Heap: [(-31,0,1,1), (-29,1,0,1), (-27,1,1,0)]
Pop 5: val=31, (0,1,1). This is the 5th pop. Output 31. Correct.

So the algorithm works for sample 1.

Now, is there any case where this algorithm fails? Consider if the function is not strictly monotonic? But it is strictly monotonic because all values are positive. So it's fine.

But wait: The problem says "Among all these values, find the K-th largest value." If there are duplicate values, the K-th largest is well-defined (e.g., if values are [10, 10, 9], the 2nd largest is 10). Our algorithm pops values in non-increasing order. If there are duplicates, we will pop them in some order. The K-th pop will give the K-th largest value. That's correct.

One potential issue: The heap might contain many elements with the same value. The visited set ensures we don't push the same triple twice. But if there are multiple triples with the same value, they are distinct entries in the heap. That's fine.

Now, what about the time limit? K up to 5e5. Each iteration does up to 3 pushes and 1 pop. So about 2 million heap operations. Each heap operation is O(log (heap size)) ~ O(log K). So about 2e6 * 20 = 4e7 comparisons. In Python, this might be slow but should pass if optimized. However, we need to compute f(i,j,k) for each push. That's a few multiplications. The visited set operations are O(1) average.

But there is a known optimization: Instead of storing (i,j,k) in the heap, we can store the value and the indices. But we need the indices to generate neighbors. So we must store them.

Another optimization: We can precompute A[i], B[j], C[k] as lists. Since we only access indices up to maybe N, but we might not need all N if K is small. But we can just use the sorted arrays.

Wait, there is a potential problem: The number of visited nodes is O(K), but the indices i,j,k can be up to N-1. If N is large (2e5) and K is small (e.g., 1), we only visit a few nodes. That's fine.

But what if K is large, say 5e5, and N is 2e5? Then we might visit up to 5e5 nodes. The indices could go up to 5e5, but N is only 2e5, so we might run out of bounds. The heap will stop pushing when indices reach N. So we only push valid indices.

So the algorithm is safe.

However, I recall that for some problems, the heap approach can be too slow in Python due to the overhead of tuples and hashing. But with K=5e5, it should be okay if we use integer encoding for visited and avoid tuple hashing in the heap? Actually, the heap elements are tuples of 4 integers. That's fine. The visited set can be a set of integers encoded as i * N * N + j * N + k. But N can be 2e5, so N*N = 4e10, which fits in Python int. So we can encode as i * (N*N) + j * N + k. But N*N might overflow 32-bit, but Python int is arbitrary precision. So it's fine.

Alternatively, we can use a dictionary with tuple keys. But integer encoding is faster.

Let's think about the maximum value of i*N*N + j*N + k. i,j,k < N ≤ 2e5. So max is (2e5-1)*4e10 + (2e5-1)*2e5 + (2e5-1) ≈ 8e15. Python int can handle that.

So the visited set can be a set of integers.

Now, is there any edge case where the heap approach misses some values? For example, if the function is not monotonic? But we established it is. However, there is a subtle point: The heap approach works for finding the K-th smallest/largest in a set where the function is monotonic and the domain is a product of chains. This is a standard result. The algorithm is essentially a best-first search on the DAG of the product order. Since every element has a path from the minimum element (0,0,0) by incrementing one coordinate at a time, and we push all immediate successors of visited nodes, we will eventually visit all nodes. The heap always contains the frontier. The maximum of the frontier is the next maximum overall. So after K pops, we have the K largest values. This is correct.

But wait: The function f is decreasing in each coordinate. So the "minimum" element in the index order (0,0,0) gives the maximum value. The "maximum" element in the index order (N-1,N-1,N-1) gives the minimum value. So we start from the maximum value and go downwards. That's fine.

One more thing: The problem asks for the K-th largest value. If K=1, we just output f(0,0,0). Our algorithm will pop once and output. That's correct.

Now, let's consider the time complexity in Python. For K=5e5, we have about 5e5 pops and up to 1.5e6 pushes. Each push/pop involves heap operations on tuples of 4 integers. The heapq implementation in Python is efficient. The visited set operations are O(1). The f computation is O(1). So total time should be around a few seconds. Should be okay.

But is there any faster method? The binary search + counting method with O(N log N) per count might be O(N log N log Max) which is about 2e5 * 20 * 60 = 2.4e8, too slow. The heap method is O(K log K) which is independent of N (except for array access). Since K is at most 5e5, it's much faster.

However, I recall that for this specific problem (K-th largest A_i B_j + B_j C_k + C_k A_i), the intended solution might be different. Let me think: The problem is from AtCoder. I think it's ABC 134 F? No. Maybe it's from a contest where N is up to 2e5 and K up to 5e5. The heap solution is a common technique for such problems. I've seen similar problems: "K-th largest sum of products" where the solution uses a heap.

But wait: There is a known issue with the heap approach for 3D: The number of visited nodes can be up to 3K, but the heap size can be up to 3K. That's fine. However, some problems require a more efficient method because the heap approach might be too slow in Python due to the constant factor. But with K=5e5, it should be okay.

Let's check the sample 3: N=5, K=54. That's small. The heap will work.

But what about the worst case? N=2e5, K=5e5. The arrays are large. We need to sort them: O(N log N). That's fine. Then we run the heap. The heap will access A[i], B[j], C[k] for indices up to maybe 5e5. But N is 2e5, so we might access indices beyond N? No, we check bounds. So we only access valid indices. The maximum index we might access is min(K, N-1) in each dimension? Actually, we could have i up to N-1, but if K > N, we might need to access all N elements. That's fine.

One potential optimization: We can precompute the arrays and sort them. Since we only need the first K elements? Not necessarily, because the K-th largest might involve an element with index > K if there are many duplicates? But if there are duplicates, the top K values might involve many elements with the same value. For example, if all values are equal, then the top K values are all the same. The heap will generate many triples. But the indices will go up to N-1. So we need the full arrays.

But sorting O(N log N) with N=2e5 is fast.

Now, let's think about the memory. The visited set will have up to 3K = 1.5e6 integers. Each integer in Python is about 28 bytes (for small ints) plus set overhead. So maybe 50 MB. That's okay.

But there is a catch: The heap might contain many elements with the same value. The heapq in Python compares tuples element by element. If the values are large (up to 3e18), the comparison is fast. The indices are small. So it's fine.

I think the heap approach is the intended solution for this problem. It's elegant and efficient.

However, let's double-check if there is any case where the heap approach fails to find the K-th largest because of duplicates or because the function is not strictly monotonic? The function is strictly monotonic because all A_i, B_j, C_k are positive integers. So B_j + C_k ≥ 2, etc. So it's strictly decreasing in each index. So the partial order is strict. The heap will generate distinct triples. The K-th pop will be the K-th largest value. If there are duplicates, the K-th pop might be the same as the (K-1)-th pop. That's fine.

One more thing: The problem says "Among all these values, find the K-th largest value." If there are ties, the K-th largest is the K-th element in the sorted list with ties. Our algorithm produces the values in non-increasing order. So the K-th popped value is exactly the K-th largest. That's correct.

Now, let's consider if we can optimize the heap further. We can use a custom heap or use numpy? No, we need to be careful with large integers.

Another approach: Binary search on the answer and counting using the product form. We can count in O(N log N) per X? Let's see: For each j, we need to count pairs (i,k) with (A_i + B_j)(C_k + B_j) ≥ Y_j. This is equivalent to counting pairs with product ≥ Y_j in two arrays. If we sort A and C descending, we can for each j do a two-pointer sweep in O(N). That's O(N²). But we can do it in O(N log N) by using a merge sort tree? Not needed.

But wait: We can count for all j simultaneously by iterating over i and k? For each pair (i,k), we can find the range of j that satisfies the condition. The condition is quadratic in B_j. We can solve for B_j. Since B is sorted, we can binary search. That's O(N² log N). Still too slow.

But we can limit i and k to the top L elements. If we choose L such that L² ≥ K, then we only need to consider L² pairs. For each pair, we can count j in O(log N). Total O(L² log N). If L=1000, L²=1e6, log N=18, total 1.8e7. That's feasible. And we can choose L adaptively? But we need to ensure that the K-th largest is among these L² pairs. Is it guaranteed? Not necessarily. But we can use binary search on X and for each X, count using this limited set? That might not be accurate.

Alternatively, we can use the heap approach which is simpler and guaranteed correct.

Given the constraints, the heap approach is the most straightforward and likely intended.

But let's verify the time limit. The problem doesn't specify the time limit, but typical AtCoder problems have 2 sec or 3 sec. Python with heap might be okay for K=5e5. However, we need to be careful with the constant factor. We can optimize by using local variables and avoiding attribute lookups.

Let's write a draft of the heap solution in Python:

```python
import sys
import heapq

def solve():
    input = sys.stdin.readline
    N, K = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    C = list(map(int, input().split()))
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)
    
    # Heap elements: (-value, i, j, k)
    # Visited set: encode (i,j,k) as i*N*N + j*N + k
    # But N*N might be large, but Python int is fine.
    # However, we can use a tuple in the set for simplicity, but integer is faster.
    
    # Actually, we can use a set of tuples. Let's see which is faster.
    # For N=2e5, N*N = 4e10, which is fine.
    
    NN = N * N
    visited = set()
    heap = []
    
    def f(i, j, k):
        return A[i] * B[j] + B[j] * C[k] + C[k] * A[i]
    
    start_val = f(0, 0, 0)
    heapq.heappush(heap, (-start_val, 0, 0, 0))
    visited.add(0)  # 0*NN + 0*N + 0
    
    for _ in range(K):
        neg_val, i, j, k = heapq.heappop(heap)
        val = -neg_val
        if _ == K-1:
            print(val)
            return

## worker: Continue the heap-based solution in Python: implem
The solution uses a max-heap (simulated with negative values in Python's `heapq`) to perform a best-first search on the 3D grid of triples `(i, j, k)`. Since `f(i,j,k) = A_i*B_j + B_j*C_k + C_k*A_i` is strictly decreasing in each index when arrays are sorted descending, starting from `(0,0,0)` and expanding to immediate neighbors `(i+1,j,k)`, `(i,j+1,k)`, `(i,j,k+1)` generates all triples in non-increasing order of value. A visited set (using integer encoding `i*N*N + j*N + k`) prevents duplicate entries. The K-th popped value is the K-th largest. Complexity is O(K log K) with O(K) extra space, well within limits for K ≤ 5×10⁵.

## worker: Complete the neighbor generation logic in the heap
The heap-based best-first search correctly generates the top K values in non-increasing order. The integer encoding `i*N*N + j*N + k` for visited triples is efficient and avoids tuple hashing overhead. The algorithm runs in O(K log K) time with O(K) extra space, which is well within the constraints (K ≤ 5×10⁵). All neighbor generation logic is now complete.
