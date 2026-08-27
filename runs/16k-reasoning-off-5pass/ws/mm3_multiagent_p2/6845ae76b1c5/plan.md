We need to answer K queries each asking for sum_{i≤X} sum_{j≤Y} |A_i - B_j| where A, B are unsorted arrays of length N ≤ 1e5, K ≤ 1e4, values up to 2e8. Direct O(N^2) per query is impossible.

Key observation: the sum splits over the joint distribution of A and B up to indices X, Y. Sort A and B to obtain non-decreasing order, and precompute prefix sums of the sorted arrays: Asort, sumA. Likewise Bsort, sumB. For a query (X, Y), the top X elements of Asort (i.e., the X smallest A values) and top Y of Bsort are the smallest elements. We can find the count of A values ≤ t among first X and similarly for B, and use median-based formula:

For two multisets S (size X) and T (size Y), the sum of absolute differences equals
  sum_{a in S} sum_{b in T} |a - b|
= (number of pairs where a > b)*(a - b) summed = sum_{a∈S} a*count_T(≤ a) - sum_{a∈S} (sum of B values ≤ a) + similar symmetric term, but there's a classic linear time formula using median.

However, we need O(log N) per query. Since sorted arrays have prefix sums, we can use the identity:

Let countA = X, countB = Y.
For each a in S, let c = number of b in T with b ≤ a. Then contribution of a = a*c - sum_{b ≤ a} b.
Sum over all a: Σ a*c - Σ sum_{b ≤ a} b.

Similarly, for each b in T, let d = number of a in S with a ≤ b. Contribution of b = b*d - sum_{a ≤ b} a.
The total sum = Σ a*c - Σ sum_{b ≤ a} b + Σ b*d - Σ sum_{a ≤ b} a.

Notice that each unordered pair (a,b) is considered twice? Let's verify:
For pair (a,b) with a ≥ b: it's counted in first term a*c where c includes b (since b ≤ a). Also counted in second term b*d where d excludes a? Wait a ≥ b implies a > b, so a is not ≤ b, so d does not include a. So each pair with a > b counted once in first part, each pair with b > a counted once in second part. So the sum covers all pairs.

But we need to compute this efficiently. Let’s define the sorted arrays Asort[0..N-1], Bsort[0..N-1]. For query (X,Y), the considered subarrays are the first X elements of Asort, and first Y elements of Bsort. Since the full sorted array is globally sorted, the subarray of size X is the prefix of Asort: Asort[0:X-1] (0-index). Similarly B prefix.

Thus we can precompute prefix sums of the whole sorted arrays; then we need to be able to query:
- count of B values ≤ a among first Y: that's the index of the last element ≤ a within Bsort[0:Y-1]. Since B prefix is sorted, we can binary search within B[0:Y-1] (or just binary search in the whole Bsorted, but limit index < Y). Similarly count of A ≤ b among first X.

We also need the sum of B values ≤ a within first Y. That's sum of B prefix up to that index.

Thus for each query we can compute:

Let X, Y given.
Preprocess: For each query, we need to iterate over all a in S (size X) and all b in T (size Y) – not feasible.

We need a more clever approach. Since X,Y up to N=1e5 and K up to 1e4, O(N) per query is too slow (1e9). Need O(log N) per query.

We can think of representing sum as:

S = Σ_{a∈S} a * rank_B(a) - Σ_{a∈S} sum_B_up_to(rank_B(a))

where rank_B(a) = # {b in T | b ≤ a}. Also the symmetric part: Σ_{b∈T} b * rank_A(b) - Σ_{b∈T} sum_A_up_to(rank_A(b))

But this still appears O(X+Y). We need a closed-form using prefix sums of B, maybe via a piecewise linear function.

Another approach: sort A and B; then treat the sum of absolute differences as sum_{i=1}^{X} sum_{j=1}^{Y} |A_i - B_j|. Since both are sorted, we can think of each A_i compared to B_j. There is a known O(N) algorithm to compute all pairwise absolute differences for sorted arrays using two pointers and prefix sums, but we need for arbitrary prefixes X, Y per query. However, we can precompute a 2D prefix sum of something? Not feasible.

Alternative: Use order statistics. For sorted arrays, we can view the sum as a function of X and Y that is linear in X and Y plus something about the "median" of the combined set? Actually for any two multisets S and T, the sum of absolute differences equals (|S|+|T|) * (median weighted average?) Not simple.

We need a data structure to answer queries of the form: given a prefix of sorted A (size X) and a prefix of sorted B (size Y), compute sum_{i=1..X} sum_{j=1..Y} |A_i - B_j|.

We can think of building a BIT (Fenwick) or segment tree over A sorted values, where each node stores sorted B values of that segment? Too large.

Observe constraints: K ≤ 1e4, N ≤ 1e5. O((X+Y) log N) per query could be up to 1e5*1e4 = 1e9, too big.

But maybe we can answer each query in O(log N) time using the following technique: Because A and B are sorted, the sum can be expressed in terms of X, Y, sum of smallest X elements of A, sum of smallest Y elements of B, and some quantile (median) of the combined multiset? Wait, the sum of absolute differences between two sorted lists of equal size is something like Σ |A_i - B_i| if we align them by order? Not the case; we need all pairs.

Alternative viewpoint: sum_{i=1}^{X} sum_{j=1}^{Y} |A_i - B_j| = X * Σ_{j=1}^{Y} B_j + Y * Σ_{i=1}^{X} A_i - 2 * Σ_{i=1}^{X} Σ_{j=1}^{Y} min(A_i, B_j).

But still need min.

Consider sorting both arrays globally, and let’s denote the multiset union of the first X A's and first Y B's, but we need sum of min of each pair.

We can also think of double counting: For each value v (say integer but values large), we could consider contributions. Not efficient.

Maybe we can precompute prefix of sorted A and B and also prefix of counts of each value? Not helpful.

Another direction: Use offline processing: Since K ≤ 1e4, maybe we can answer each query in O((X+Y)) but X,Y are up to N=1e5 each, worst-case 1e9. But maybe typical constraints allow O(N sqrt K) or something? But we need guaranteed.

We can try to use a data structure that can answer sum_{i=1}^{X} sum_{j=1}^{Y} |A_i - B_j| by building a 2D BIT over the sorted A and B? Actually we can think of mapping pairs (i,j) to a point in 2D (A_i, B_j), and we need sum of |A_i - B_j| over rectangle [1..X] × [1..Y] after sorting. Sorting changes indices. This is not a static 2D grid.

However, after sorting, the condition "i ≤ X" and "j ≤ Y" corresponds to taking the first X elements of A and first Y of B in sorted order. So essentially the domain of pairs is a rectangle in the sorted index space: the set of pairs (i,j) with i ≤ X, j ≤ Y. We need to compute sum over this rectangle of f(A_i, B_j) where f(a,b) = |a-b|.

If we could precompute a 2D structure for sorted arrays where we can query sum of f over any prefix rectangle, we could answer in O(log^2 N). Is that possible? Since the array is 1D, but we have two separate dimensions, we can think of building a segment tree over A (size N). In each node representing a segment of A (i.e., a range of A values), we can store a sorted list of B values that correspond to the same index range? Wait, we need to consider pairs across the two arrays independent of each other. For each query (X,Y), we need to consider all pairs (i in 1..X, j in 1..Y). The A values are taken from prefix of sorted A; the B values from prefix of sorted B. So the condition on i and j is independent: we need sum over i in [1,X] and j in [1,Y] of |A_i - B_j|. Since the A and B arrays are independent, we can treat the sum as:

Sum = Σ_{i=1}^{X} Σ_{j=1}^{Y} |A_i - B_j| = Σ_{i=1}^{X} g_i(Y) where g_i(Y) = Σ_{j=1}^{Y} |A_i - B_j|.

We can precompute for each i (1..N) the function g_i(y) = Σ_{j=1}^{y} |A_i - B_j|. Since B is sorted, g_i(y) is piecewise linear in y: as y increases, we add more B_j. We can express g_i(y) = y * A_i - 2 * Σ_{j: B_j ≤ A_i, j ≤ y} (A_i - B_j) + Σ_{j: B_j > A_i, j ≤ y} (B_j - A_i). Actually we can compute:

Let c = number of B_j ≤ A_i among first y.
Let sum_{B_j ≤ A_i, j ≤ y} B_j = s.
Then Σ_{j≤y} |A_i - B_j| = c * A_i - s + ( (y - c) * (some?) ) - (y - c)*A_i? Wait careful:

For j with B_j ≤ A_i, |A_i - B_j| = A_i - B_j. Sum = c * A_i - s.
For j with B_j > A_i, |A_i - B_j| = B_j - A_i. Sum = (y - c) * A_i? Actually B_j - A_i = B_j - A_i, sum = (sum_{B_j > A_i} B_j) - (y - c) * A_i.

Total = c*A_i - s + sum_{B_j > A_i} B_j - (y - c)*A_i = (c - (y - c)) * A_i - s + sum_{B_j > A_i} B_j = (2c - y) * A_i - s + sum_{B_j > A_i} B_j.

But sum_{B_j > A_i} B_j = total_sum_B(y) - s. Let total_sum_B(y) = prefix sum of B sorted up to y: SB[y] = Σ_{j=1}^{y} B_j.

Thus total = (2c - y) * A_i - s + (SB[y] - s) = (2c - y) * A_i + SB[y] - 2s.

So g_i(y) = (2c - y) * A_i + SB[y] - 2s, where c = count of B_j ≤ A_i in first y, s = sum of those B_j.

Now sum over i=1..X:

Total = Σ_{i=1}^{X} (2c_i - Y) * A_i + X * SB[Y] - 2 Σ_{i=1}^{X} s_i, where c_i = count_{j ≤ Y} [B_j ≤ A_i], s_i = sum_{j ≤ Y, B_j ≤ A_i} B_j.

Note: Y is fixed for the query. So total = Σ_{i=1}^{X} (2c_i * A_i) - Y * Σ_{i=1}^{X} A_i + X * SB[Y] - 2 Σ_{i=1}^{X} s_i.

Let SA[X] = Σ_{i=1}^{X} A_i (prefix sum of sorted A). So total = 2 Σ_{i=1}^{X} (c_i * A_i) - Y * SA[X] + X * SB[Y] - 2 Σ_{i=1}^{X} s_i.

Thus we need to compute for a given X, Y:
- SA[X] (precomputed)
- SB[Y] (precomputed)
- Sum1 = Σ_{i=1}^{X} (c_i * A_i) where c_i = count of B_j ≤ A_i in first Y.
- Sum2 = Σ_{i=1}^{X} s_i where s_i = sum of B_j ≤ A_i in first Y.

Observation: c_i and s_i are monotonic in A_i: for larger A_i, c_i is non-decreasing (since count of B_j ≤ A_i can only increase), and s_i is non-decreasing. Moreover, as we increase X (i.e., take more A_i), we need to sum over larger A_i. This is reminiscent of queries of the form: given a threshold Y (i.e., prefix of B), and we need to process A_i's in increasing order and accumulate contributions based on the B prefix.

This suggests we can preprocess the sorted A and B and build a data structure that can answer queries (X, Y) by performing some integration.

Idea: Since B prefix is defined by Y, we can treat B prefix as a set of Y values, sorted. For each A_i, we need to know among those Y values, how many are ≤ A_i, and their sum. This is exactly a 2D dominance query: given a point (A_i, Y) in the B-index dimension, we need to query the number and sum of B values with index ≤ Y and value ≤ A_i. Since B is sorted, the condition index ≤ Y is just taking the first Y elements of B. So we are effectively querying on the prefix of B (size Y) the number and sum of elements ≤ A_i.

Thus for each query (X, Y), we need to compute:
Sum1 = Σ_{i=1}^{X} A_i * count_{j=1}^{Y} [B_j ≤ A_i]
Sum2 = Σ_{i=1}^{X} sum_{j=1}^{Y, B_j ≤ A_i} B_j

Both can be expressed as:
Sum1 = Σ_{i=1}^{X} A_i * F(A_i, Y)
Sum2 = Σ_{i=1}^{X} G(A_i, Y)
where F(a, y) = count_{j ≤ y} [B_j ≤ a], G(a, y) = sum_{j ≤ y, B_j ≤ a} B_j.

If we think of the B array as points (B_j, j) in 2D (value, index), then for a given y (i.e., we restrict to j ≤ y), we need to query among those points with B_j ≤ a.

Since y is the upper bound on index, we can precompute for each possible y (up to N) the prefix of B values. But K is 1e4, Y up to N. Could we precompute for each y a BIT over B values? That would be O(N^2) memory.

Alternative: Use offline processing with CDQ divide-and-conquer (also known as offline 2D BIT) to handle queries of the form: we have points (B_j, j) and queries (a, y) asking for sum of B_j where B_j ≤ a and j ≤ y, and also count of such points. Then we need to sum over many a_i values (the A_i's up to X). For each query (X, Y), we need to compute the sum of F(A_i, Y) * A_i and sum of G(A_i, Y) for i=1..X. That's like we need to compute two separate sums over the prefix of A (i.e., a range of A values) of a function defined by Y.

We can think of each query as two separate subqueries: one for counting and one for sum, but we need weighted by A_i.

Potentially, we can treat each A_i as a point (A_i, i) in a 2D space (value, index). For each query (X, Y), we consider the set of A_i for i ≤ X, and we need to compute for each A_i: the number and sum of B_j with B_j ≤ A_i and j ≤ Y.

We can precompute for each B_j its value, and we need to count B_j ≤ A_i and j ≤ Y. This is a 2D dominance problem with constraints: B_j value ≤ A_i value, and B_j index ≤ Y. For each A_i (point), we need to query the number of B points in a rectangle (B_j.value ≤ A_i.value, B_j.index ≤ Y). And we also need the sum of B_j values for those points (i.e., weighted sum). Then we need to sum over i=1..X the (A_i * count_i) and sum_i.

Thus we have a scenario: There are two static point sets (A and B) each with their own dimensions (value and index). The query asks for a sum over a prefix of A points of a function of a rectangle in B space. This is reminiscent of offline processing using BIT with divide-and-conquer on one dimension (index). But we need to handle up to 1e4 queries with up to 1e5 points each. Complexity must be about O((N+K) log^2 N) or similar.

Let's think more concretely: For each query (X, Y), define:

C_X(Y) = Σ_{i=1}^{X} count_{j=1}^{Y} [B_j ≤ A_i] * A_i
S_X(Y) = Σ_{i=1}^{X} sum_{j=1}^{Y, B_j ≤ A_i} B_j

We need to compute both quickly.

We can attempt to build a segment tree over A indices (i). Each node covers a range of A indices, say from l to r. In that node, we store the sorted values of A_i in that range (obviously they are the original A values in that index range, but they are already sorted globally, so within a range they are sorted). For each node, we also need to answer queries: given Y (prefix size of B), compute the contribution of the A_i in that node to C_X(Y) and S_X(Y). That is:

Given a sorted array of A values in a node (size m), and a prefix of B of size Y, we need to compute:
- Sum over a in node: a * count_{j ≤ Y, B_j ≤ a}
- Sum over a in node: sum_{j ≤ Y, B_j ≤ a} B_j

If we could compute this for a node in O(log N) time (or O(log^2 N)), then we can answer a query by traversing the segment tree for the range [1, X] and aggregating contributions. The number of nodes visited is O(log N). For each visited node, we need to compute its contribution in O(log N) time (or O(log^2 N)). So total O(log^2 N) per query.

Thus the problem reduces to: Given a sorted list of A values (size up to segment size) and a query Y (size of B prefix), compute two sums efficiently. For each A value a, we need count of B_j ≤ a in the first Y B's, and sum of those B's.

If we precompute for the B array a prefix of sorted B values and prefix sums (global), then for a given Y we have the sorted list B[0:Y-1] (prefix of B). We need to answer for many a's (the A values in the node) the count of B's ≤ a and sum of those B's. This is essentially a range counting/sum query on the prefix of B: for a given threshold a, we need to find the index pos = upper_bound(B, a, 0, Y-1). Then count = pos, sum = prefixSumB[pos-1] (or sum of B[0:pos-1]).

Thus for a node with m A values, we can iterate over them in O(m) time to compute contributions. But m could be up to N, leading to O(N) per node. Not good.

We need a faster way: For the node, we can treat its A values as a sorted list, and we need to compute for each a the count and sum of B prefix up to a. Since both A values and B prefix are sorted, we can compute these contributions in linear time per node (by two-pointer merging). However, each query may need to consider many nodes; the total work across nodes for a query could be O(N) in worst case (if we sum over all nodes visited, each node could have many A's). But we can precompute prefix contributions for each possible Y? Not possible.

Alternative: Use a 2D BIT where one dimension is A value and the other is B index, but the query wants sum over a range of A indices (prefix) and a range of B indices (prefix). Actually, we need to sum over a in prefix of A (i.e., first X sorted A's) and b in prefix of B (first Y sorted B's) of |a - b|. This is a 2D range query on a matrix M[i][j] = |A_i - B_j|? The matrix is size N x N, but we cannot store it. However, we can perhaps answer sum over a rectangle [1..X] × [1..Y] of |A_i - B_j| using some additive decomposition. Since |a - b| = (a - b) if a ≥ b else (b - a). We can think of splitting the rectangle into two parts: pairs where a ≥ b and pairs where a < b. For pairs where a ≥ b, the contribution is a - b = a + (-b). So sum_{a≥b} (a - b) = sum_{a≥b} a + sum_{a≥b} (-b). But a and b are not independent; the condition a≥b couples them.

However, we can write:

Sum_{i=1..X} Sum_{j=1..Y} |A_i - B_j| = Σ_i Σ_j (A_i - B_j) * sgn(A_i - B_j). This is not linear.

Maybe we can precompute partial sums of A_i and B_j and use combinatorial formulas.

Another angle: Because A_i and B_j are sorted, we can consider scanning i from 1 to X, and for each i, find the split point in B where B_j ≤ A_i. As we increase i, the split point moves monotonically. So we can compute the total sum in O(X+Y) time per query. Since K ≤ 1e4, X and Y up to N=1e5, total O(K * (X+Y)) could be up to 1e9, which is borderline but maybe with optimization in C++ it could pass? 1e9 operations is too much for Python; we need something like O((N+K) log N) or O((N+K) sqrt N) or similar.

But note that K is only 1e4, but X and Y can be up to 1e5 each. 1e4 * 1e5 = 1e9, too much.

We need a more clever approach.

Observation: The answer for query (X, Y) is monotonic in X and Y. We can perhaps use a 2D prefix sum approach: Let F(x, y) = Σ_{i=1}^{x} Σ_{j=1}^{y} |A_i - B_j|. Then answer is F(X, Y). If we can precompute F for all x up to N and y up to N, we could answer queries in O(1). But N is 1e5, so N^2 is impossible.

But we could precompute F for some dimensions and interpolate? Not straightforward.

We need to find a way to compute F(x,y) quickly.

Consider representing F(x,y) as:
F(x,y) = x * SB[y] + y * SA[x] - 2 * Σ_{i=1}^{x} Σ_{j=1}^{y} min(A_i, B_j).

Let M(x,y) = Σ_{i=1}^{x} Σ_{j=1}^{y} min(A_i, B_j). Then answer = x * SB[y] + y * SA[x] - 2 * M(x,y).

So we need to compute M(x,y). This is similar to sum of mins over two sorted arrays. The min of two sorted sequences can be computed via a known formula: For sorted sequences, the sum of mins over all pairs is related to the area under the curve of the sorted sequences? Actually, if we consider the sorted sequences, the min of each pair is the smaller of the two values. Summing over all pairs is like integrating the smaller of the two sequences.

Alternatively, M(x,y) = Σ_{i=1}^{x} Σ_{j=1}^{y} min(A_i, B_j) = Σ_{i=1}^{x} ( sum_{j: B_j ≤ A_i} B_j + sum_{j: B_j > A_i} A_i ) = Σ_{i=1}^{x} ( s_i + (y - c_i) * A_i ), where c_i = count_{j ≤ y} [B_j ≤ A_i], s_i = sum_{j ≤ y, B_j ≤ A_i} B_j.

Thus M(x,y) = Σ_{i=1}^{x} s_i + Σ_{i=1}^{x} (y - c_i) * A_i = Σ_{i=1}^{x} s_i + y * SA[x] - Σ_{i=1}^{x} c_i * A_i.

Plug back into answer:
Answer = x * SB[y] + y * SA[x] - 2 * ( Σ s_i + y * SA[x] - Σ c_i * A_i )
= x * SB[y] + y * SA[x] - 2 Σ s_i - 2 y SA[x] + 2 Σ c_i * A_i
= x * SB[y] - y * SA[x] - 2 Σ s_i + 2 Σ c_i * A_i

Wait, compute carefully:

Answer = x * SB[y] + y * SA[x] - 2 M
M = Σ s_i + y SA[x] - Σ c_i A_i

Thus Answer = x SB[y] + y SA[x] - 2 (Σ s_i + y SA[x] - Σ c_i A_i)
= x SB[y] + y SA[x] - 2 Σ s_i - 2 y SA[x] + 2 Σ c_i A_i
= x SB[y] - y SA[x] - 2 Σ s_i + 2 Σ c_i A_i

But earlier we derived:
Total = (2 Σ c_i * A_i) - Y * SA[X] + X * SB[Y] - 2 Σ s_i
This matches with X=x, Y=y: 2 Σ c_i A_i - y SA[x] + x SB[y] - 2 Σ s_i. Yes same.

Thus we need to compute Σ c_i A_i and Σ s_i for prefix of A up to x and prefix of B up to y.

Now, c_i and s_i are defined as count and sum of B values ≤ A_i in the first y B's. This is a 2D dominance problem.

We can treat each B_j as a point (value = B_j, index = j). For a given y, we consider the subset of points with index ≤ y (i.e., the first y B's). For each A_i, we need to query among those points with value ≤ A_i: the count and sum of B_j.

Thus we need to answer many such queries: for each query (x, y), we need to compute Σ_{i=1}^{x} (count_i * A_i) and Σ_{i=1}^{x} sum_i, where count_i and sum_i are computed from the prefix of B up to y.

We can think of building a BIT (Fenwick) or segment tree over A values, but the queries are over prefix of A (by index after sorting). However, we can map A_i to its value A_i, and also we need to consider prefix by index, not value. But after sorting A, the prefix of A is the set of smallest X A values. So we can treat the prefix of A as the first X elements in sorted order. Since the A array is sorted, the prefix of A is exactly the set of A values ≤ some threshold? Not exactly, because there could be duplicate values crossing the threshold. But we can treat it as: there exists a threshold t such that the prefix includes all A values < t, and some equal to t up to the required count. This is typical for prefix queries on sorted arrays: we can binary search for the value threshold and handle duplicates.

But the query we need is more complex: we need to sum over each A_i individually, not just the total count of B ≤ threshold. We need Σ c_i A_i and Σ s_i. Since c_i is count of B ≤ A_i, and s_i is sum of those B.

Observation: Since A_i are sorted, as we increase i, the threshold A_i increases. So the count c_i is monotonic non-decreasing with i. Similarly s_i is monotonic non-decreasing.

We can perhaps precompute for each i the function f_i(y) = (c_i(y), s_i(y)). Then for a query (x, y), we need Σ_{i=1}^{x} f_i(y) with appropriate weighting (multiply count by A_i). This suggests we could precompute prefix sums over i of these functions, but they depend on y.

If we could precompute for each i and each possible y the count and sum, that would be O(N^2). Not possible.

But note that c_i(y) and s_i(y) are defined as: c_i(y) = number of B_j ≤ A_i among first y B's. Since B is sorted, for a fixed y, the set of B values considered is the prefix of B. For a given A_i, the count is the position of the largest B ≤ A_i in the prefix B[0..y-1]. This is essentially the rank of A_i in the multiset of the first y B's. This can be computed via binary search in O(log y). So for each i we could compute c_i(y) and s_i(y) in O(log N) by binary searching in B[0:y-1]. Then we could sum over i=1..x. But that would be O(x log N) per query, too slow.

We need a faster way. Perhaps we can use a BIT to process queries offline sorted by y. Since K is up to 1e4, we could process each query in O((x + y) log N) if we can reuse computations across queries? Not straightforward.

Alternative: Use a 2D BIT where one dimension is A value and the other is B index, but we need to sum over a rectangle in the (A index, B index) space. Actually, we can reinterpret the problem in terms of original indices before sorting? But the queries are based on sorted order. However, we could precompute the sorted arrays and also the original indices are irrelevant after sorting.

We need a data structure that can answer sum over i=1..x of (c_i(y) * A_i) and sum of s_i(y). This is like we have a static set of points (A_i, i) in 2D. For each query (x, y), we consider the prefix of A points with i ≤ x, and for each point we need to compute something based on B points with index ≤ y and value ≤ A_i. This is reminiscent of a problem that can be solved by a BIT of BITs or a segment tree of BITs, but we need to handle sum of A_i * count and sum of s_i. Perhaps we can treat each A_i as adding a contribution to the B side.

Consider the following: For each B_j, it contributes to s_i for all A_i ≥ B_j (i.e., where B_j ≤ A_i). Specifically, for a given y (prefix of B), each B_j (j ≤ y) contributes its value to s_i for all i such that A_i ≥ B_j. Similarly, B_j contributes 1 to c_i for all A_i ≥ B_j. So we can think of building a BIT over A values that supports range add of +1 (for count) and +B_j (for sum) over the range of A indices where A_i ≥ B_j.

Specifically, for a fixed y, we can process B_j for j=1..y. For each B_j, we need to add to all A_i with A_i ≥ B_j: count +1, sum +B_j. Then after processing all j ≤ y, for each A_i, the accumulated count and sum are exactly c_i(y) and s_i(y). Then we need to compute Σ_{i=1}^{x} (A_i * count_i) and Σ_{i=1}^{x} sum_i.

If we can maintain a data structure that supports these operations and queries for prefix sums of weighted counts and sums, we could process queries offline sorted by y.

Idea: Sort queries by Y. Maintain a BIT (Fenwick) over the sorted A indices (size N). Initially empty (all zero). We'll iterate j from 1 to N over B sorted. At step j, we "activate" B_j: we need to add to all A_i with A_i ≥ B_j: count +1, sum +B_j. Then after activating first Y B's, we can answer queries with that Y. For each query (X, Y), we need to compute:
- totalCountWeight = Σ_{i=1}^{X} (A_i * count_i) where count_i is current count at A_i (which equals number of activated B's ≤ A_i)
- totalSum = Σ_{i=1}^{X} sum_i (which is sum of B values ≤ A_i among activated B's).

We can maintain two BITs:
- BITcnt: stores counts (c_i) for each A_i. When we add B_j, we need to add +1 to all A_i with A_i ≥ B_j. Since A is sorted, the set of indices i where A_i ≥ B_j is a suffix [pos, N-1] (where pos = lower_bound of B_j in A). So we can do a range add on BIT: add +1 to range [pos, N-1]. Similarly, BITsum: store sum of B values for each A_i. When we add B_j, we need to add +B_j to range [pos, N-1] (i.e., each A_i gets +B_j to its s_i). So we can maintain two BITs supporting range add and prefix sum query. Actually we need to query prefix sums: for a given X, we need Σ_{i=1}^{X} (A_i * count_i) and Σ_{i=1}^{X} sum_i. We can compute these if we have BIT for count_i and BIT for sum_i. For the weighted sum, we can compute as Σ_{i=1}^{X} A_i * count_i = Σ_{i=1}^{X} A_i * (c_i). Since c_i is stored in BITcnt (point value at i). So we can query prefix sum of (A_i * c_i). This can be computed if we have BIT that can give sum of values (A_i * c_i) over prefix. But we have only BIT for c_i. We could compute Σ_{i=1}^{X} A_i * c_i = Σ_{i=1}^{X} (c_i * A_i). Since A_i is known, we could compute weighted sum by iterating i=1..X if we had c_i array, but we need O(log N). However, we can maintain a BIT that stores A_i * c_i as values. Initially all zero. When we add a range add of +1 to count_i for i in [pos, N], we also need to add +A_i to the weighted BIT for each i in that range. Since the increment to weighted value for each i is A_i * (+1) = +A_i. So we need to add A_i to the weighted BIT for each i in [pos, N]. That's a range add of A_i (which varies per index) to the weighted BIT. Similarly, for sum_i, we need to add B_j to s_i for each i in [pos, N], i.e., range add of constant B_j.

Thus we need a data structure that supports:
- Range add of a constant to a BIT (like BITsum for s_i) -> easy with BIT using range add and point query, or BIT with point add and prefix sum. Actually standard BIT can support point update and prefix sum query. For range add and prefix sum query, we can use two BITs or a BIT that supports range add and range sum. But we can also handle by doing point updates: for each i in [pos, N], we add B_j to s_i. That's O(N) per B_j, too slow. So we need a data structure that supports range addition of a constant and prefix sum query of the values. That's classic: we can use a BIT (Fenwick) where we do point updates: for range add [l, r] of constant v, we do BIT.add(l, v), BIT.add(r+1, -v). Then to query prefix sum up to x, we compute BIT.prefix_sum(x). This works for range add + point query. For prefix sum of the values (i.e., sum of s_i over prefix), we can compute using another BIT that accumulates the range adds: maintain BIT1 for range add, and then prefix sum of values is sum of BIT1.prefix_sum(i) for i=1..x? Wait, standard trick: To support range add and range sum, we need two BITs. But we only need to query sum over prefix of the values (i.e., Σ_{i=1}^{X} s_i). If we maintain a BIT that supports range add and point query (i.e., we can get s_i at any i), we could then sum over i=1..X by iterating? Not good. We need prefix sum of the values directly.

Better: Use a segment tree with lazy propagation that supports range add and range sum queries. For each query, we need to get sum of s_i over i=1..X. Similarly, we need sum of (A_i * c_i) over i=1..X. Since c_i is just a counter (range add of +1), we can maintain a segment tree that stores two values: sumC = Σ c_i over segment, and sumWeighted = Σ A_i * c_i over segment. When we add +1 to a range [l, r] of c_i, we also need to add Σ_{i∈[l,r]} A_i to sumWeighted. Since A_i is static, we can precompute prefix sums of A_i to get sumA(l, r) quickly. But the segment tree needs to know sumA for a segment to update sumWeighted. That's doable: each node can store the sum of A_i in its segment (static). Then when we apply a range add of +1 to the segment (i.e., add 1 to each c_i), we can update sumC += length_of_segment, and sumWeighted += sumA_of_segment. Similarly, for s_i, we need to add B_j to each s_i in range [pos, N]. That's a range add of constant B_j. So we need to maintain sumS = Σ s_i over segment, and when we add B_j to each s_i in [l, r], we update sumS += B_j * length_of_segment.

Thus we can have a segment tree (or BIT with range add and range sum) that supports two types of range updates: add 1 to c_i and add B_j to s_i. But we can treat them as separate variables: we can maintain two separate segment trees, or one segment tree that holds both values. Since updates are range adds of constants (either +1 for c_i or +B_j for s_i), we can handle them in a unified way by storing a pair (cntAdd, sumAdd) for each node? Actually we can maintain two segment trees: one for c_i and weighted sum, and one for s_i.

But we also need to support query for prefix sum of weighted count and prefix sum of s_i for a given X. That's just a range sum query [1, X] on the segment tree.

Thus the plan: offline process queries sorted by Y. Initially, segment tree has all c_i = 0, s_i = 0, and sumWeighted = 0, sumS = 0. For each B_j (j from 1 to N) in order, we activate it: we find pos = lower_bound(A, B_j) (the first index in A where A[pos] >= B_j). Then we apply to the segment tree range [pos, N-1] (0-index) the updates:
- c_i += 1 for each i in range (i.e., add 1 to count)
- s_i += B_j for each i in range
Correspondingly, we update:
- sumC += length_of_range
- sumWeighted += sumA_range (since each c_i increments by 1, weighted sum increases by A_i)
- sumS += B_j * length_of_range

After processing B_j, the segment tree reflects the contributions of B_1..B_j.

Now, for each query with Y = j, after processing B_j (i.e., after activating j B's), we can answer the query: we need to compute for X (prefix size of A):
- SA[X] = sum of A[0:X-1] (precomputed)
- SB[Y] = sum of B[0:Y-1] (precomputed)
- sumWeighted = query segment tree for range [0, X-1] of weighted count (i.e., Σ A_i * c_i)
- sumS = query segment tree for range [0, X-1] of s_i

Then answer = 2 * sumWeighted - Y * SA[X] + X * SB[Y] - 2 * sumS.

Check formula: total = 2 Σ c_i A_i - Y SA[X] + X SB[Y] - 2 Σ s_i. Yes.

Thus we can answer each query in O(log N) time (segment tree query) after we have processed the necessary B's. Since we need to process queries in order of Y, we can sort queries by Y, iterate Y from 1 to N, and for each Y, after processing B_Y, we answer all queries with that Y.

Complexities: Sorting A and B each O(N log N). Sorting queries O(K log K). Segment tree with range updates and range queries: O(log N) per operation. For each B_j, we do one range update (two updates: add 1 to c_i and add B_j to s_i). That's O(N log N) total. For each query, we do a range query (two queries: sumWeighted and sumS) over prefix [0, X-1], O(log N). So total O((N+K) log N) which is fine.

We need to be careful with 1-index vs 0-index. We'll use 0-index for Python lists.

Segment tree details: We need to support range add of two types: for c_i (add 1) and for s_i (add B_j). Actually we can combine them: we can store in each node the sum of c_i (call it sumC) and sum of s_i (call it sumS). Also we need to know the sum of A_i in the segment (static) to update sumWeighted when we add to c_i. But we can also maintain sumWeighted directly: we can compute sumWeighted on the fly as sumC * something? Wait, sumWeighted = Σ A_i * c_i. When we add 1 to c_i for each i in a range, the increase in sumWeighted is Σ A_i over that range. So we need to know the sum of A_i in the range to update sumWeighted. We can precompute prefix sums of A to get sumA(l, r) quickly, but we need to apply this update many times (N times). If we query sumA(l, r) each time, that's O(1) using prefix sum array, fine. So we can handle sumWeighted update by using prefix sum of A to compute the sum of A_i in the range, then add that to a variable that tracks sumWeighted for the whole array? But we need to support range queries for sumWeighted over arbitrary prefix [0, X-1]. If we maintain a segment tree that stores sumWeighted as a value that can be updated with range adds of varying amounts (the amount is sumA(l, r) which depends on the range), we need to apply a range add of a value that is not constant across the segment tree nodes? Wait, when we add +1 to c_i for each i in a range [l, r], the increment to sumWeighted is Σ_{i=l}^{r} A_i. For a segment tree node covering a subrange, if we partially apply the update, the amount to add to sumWeighted for that node is sumA(node) (the sum of A_i in that node's segment). Since the node's segment is known, we can precompute for each node the sum of A_i in its segment (static). Then when we apply a range add of +1 to a node that is fully covered, we can update its sumWeighted by adding its static sumA. This is exactly a segment tree with lazy propagation for the c_i update: the lazy value indicates how many B's have been added to c_i (i.e., how many +1 increments are pending for this segment). When we apply lazy = +1 to a node, we update sumC += length_of_node, sumWeighted += sumA_node. Similarly, for s_i update, we need to add a constant B_j to s_i for each i in range. So we need another lazy for s_i: lazyS indicates how much to add to s_i for each element in the segment. When we apply lazyS = v to a node, we update sumS += v * length_of_node.

Thus we can maintain a segment tree with two lazy values: lazyC (for count) and lazyS (for sum). The node stores sumC, sumWeighted, sumS. The static sumA for each node is precomputed and stored (or we can compute on the fly from prefix sums). Since sumA is static, we can store it in the node.

When we process B_j, we find pos = lower_bound(A, B_j). The range to update is [pos, N-1] (0-index). We call a function update_range(l, r, addC=1, addS=B_j). This will apply the lazy updates to the segment tree.

Query: For a prefix [0, X-1], we query the segment tree to get sumWeighted and sumS over that range.

Edge Cases: B_j may be larger than all A_i, then pos = N, range is empty (no updates). If B_j is less than all A_i, pos = 0, update whole range.

We need to be careful with large numbers: sums can be up to N^2 * max_val (1e10 * 2e8 = 2e18?), let's compute: N=1e5, max value 2e8, sum of absolute differences up to N^2 * 2e8 = 1e10 * 2e8 = 2e18, which fits in 64-bit signed (9.22e18). So we need Python's int (unbounded) fine.

Implementation steps:

1. Read N, arrays A, B.
2. Sort A and B in non-decreasing order.
3. Compute prefix sums SA (size N+1), SB (size N+1). SA[i] = sum of first i elements of A (0-index: SA[0]=0, SA[i] = sum A[0:i]).
4. Read K, and queries (X, Y). Note that X and Y are 1-indexed counts. We'll store each query as (Y, X, index) to sort by Y. Actually we need to process queries after processing Y B's. So we sort queries by Y ascending.
5. Build a segment tree over indices 0..N-1. Each node stores:
   - sumC: total c_i (count of B <= A_i) in this segment
   - sumW: total weighted count Σ A_i * c_i
   - sumS: total s_i (sum of B <= A_i) in this segment
   - sumA_static: sum of A_i in this segment (static, precomputed)
   - lazyC: pending count addition to apply to children
   - lazyS: pending sum addition to apply to children

We need to support range update: addC (default 1) and addS (value). When applying to a node:
   node.sumC += addC * node.len
   node.sumW += addC * node.sumA_static
   node.sumS += addS * node.len
   node.lazyC += addC
   node.lazyS += addS

When pushing down to children, we propagate lazyC and lazyS.

The segment tree can be built with size N, and we can store sumA_static in each node. To compute sumA_static for a node, we can precompute prefix sum of A and use it during building. Or we can store an array of A and compute on the fly. Simpler: during building, we pass the segment range and compute sumA_static = sum of A[l:r+1] using prefix sum SA.

We also need to know the length of segment (r - l + 1). We can compute as node.len = r - l + 1.

Segment tree size: 4*N is fine.

Processing:
- Sort queries by Y.
- Initialize pointer cur = 0 (0-index for B). Actually we will iterate Y from 1 to N. For each Y, we need to have processed first Y B's (i.e., B[0..Y-1]). So we can have a variable processed = 0. For each query with given Y, we need to ensure that we have processed B up to Y-1 (since Y is 1-indexed). Actually if Y=1, we need to process B[0] (first element). So we can loop while processed < Y: process B[processed] (i.e., B[processed]), then processed += 1. Then answer query.

Alternatively, we can sort queries by Y, and iterate through B array once: for each query, while processed < query.Y: process B[processed] (0-index). Then answer.

Processing B_j:
   pos = lower_bound(A, B_j)  # first index i where A[i] >= B_j
   if pos < N:
       update_range(pos, N-1, addC=1, addS=B_j)

Query for (X, Y):
   X is 1-indexed count. So we need prefix of A of length X: indices 0..X-1.
   Query range [0, X-1] to get sumW and sumS.
   SA_X = SA[X]  # sum of first X A's
   SB_Y = SB[Y]  # sum of first Y B's
   ans = 2 * sumW - Y * SA_X + X * SB_Y - 2 * sumS
   store ans for original index.

Check formula: sumW = Σ_{i=1}^{X} A_i * c_i (c_i is count of B <= A_i in first Y). sumS = Σ_{i=1}^{X} s_i (s_i is sum of those B). So answer = 2*sumW - Y*SA_X + X*SB_Y - 2*sumS.

Let's test with sample.

Sample 1:
N=2
A = [2,4], B=[3,5] sorted: A=[2,4], B=[3,5].
SA: [0,2,6]
SB: [0,3,8]
Queries:
(1,1): X=1,Y=1
(1,2): X=1,Y=2
(2,1): X=2,Y=1
(2,2): X=2,Y=2

Process:
Initially segment tree all zero.

Query (1,1): Y=1.
Process B[0]=3. pos = lower_bound(A, 3) = index 1 (A[1]=4). Update range [1,1]: addC=1, addS=3.
Now c_i: A[0]=2: c=0, s=0; A[1]=4: c=1, s=3.
Query X=1: prefix [0,0]. sumW = A0*c0 = 2*0=0. sumS = 0.
SA_X = SA[1] = 2. SB_Y = SB[1] = 3.
ans = 2*0 - 1*2 + 1*3 - 2*0 = -2 + 3 = 1. Correct.

Query (1,2): Y=2.
Process B[1]=5. pos = lower_bound(A,5) = index 2 (N). So no update (range empty).
Now c_i: same as before. s_i: A[0]=0, A[1]=3.
Query X=1: sumW=0, sumS=0. SA_X=2, SB_Y=SB[2]=8.
ans = 0 - 1*2 + 1*8 - 0 = 6? Wait sample answer is 4. Something is off.

Our calculation gave 6, but correct answer is 4. Let's recompute manually: For X=1,Y=2, we consider A_1=2, B_1=3,B_2=5. Sum = |2-3|+|2-5| = 1+3=4. Our formula gave 6. Let's check the formula for answer.

Our derived answer: total = 2 Σ c_i A_i - Y SA[X] + X SB[Y] - 2 Σ s_i.

Compute c_i for X=1: i=1 (A=2). In B prefix of size 2 (B=[3,5]), B values ≤ 2? None, so c_1=0, s_1=0.
Thus Σ c_i A_i = 0, Σ s_i = 0.
SA[X] = 2, SB[Y] = 3+5=8, X=1, Y=2.
Plug: 2*0 - 2*2 + 1*8 - 2*0 = -4 + 8 = 4. Wait I mistakenly used Y=1? Actually Y=2. Let's recompute: 2*0 - Y*SA[X] = -2*2 = -4. + X*SB[Y] = 1*8 = +8. -2*sumS = 0. So total = 4. But earlier I used Y=1 incorrectly. In the code we will use Y correctly. So it's fine.

But in my manual step for (1,2), I used SB_Y = SB[2] = 8, correct. So ans = 0 - 2*2 + 1*8 - 0 = 4. Good.

Now query (2,1): X=2,Y=1. Process B[0]=3 already done. c_i: A[0]=2: c=0; A[1]=4: c=1. s_i: A[0]=0, A[1]=3.
sumW = A0*c0 + A1*c1 = 2*0 + 4*1 = 4.
sumS = 0+3=3.
SA_X = SA[2] = 2+4=6.
SB_Y = SB[1] = 3.
X=2,Y=1.
ans = 2*4 - 1*6 + 2*3 - 2*3 = 8 - 6 + 6 - 6 = 2. Correct.

Query (2,2): X=2,Y=2. c_i: A0:0, A1:1. s_i: A0:0, A1:3.
sumW=4, sumS=3.
SA_X=6, SB_Y=8, X=2,Y=2.
ans = 2*4 - 2*6 + 2*8 - 2*3 = 8 - 12 + 16 - 6 = 6. Correct.

Thus formula works.

Now we need to ensure that sumW and sumS are correctly computed for the prefix.

Implementation details:

Segment Tree:
- We'll use 0-indexed array for A.
- Build function build(node, l, r):
   if l == r:
       sumA_static = A[l]
       sumC = 0
       sumW = 0
       sumS = 0
       lazyC = 0
       lazyS = 0
   else:
       mid = (l+r)//2
       build left, right.
       sumA_static = left.sumA_static + right.sumA_static
       sumC = sumW = sumS = 0
       lazyC = lazyS = 0
- store in arrays: sumA[node], sumC[node], sumW[node], sumS[node], lazyC[node], lazyS[node].

Update function: update(node, l, r, ql, qr, addC, addS):
   if ql <= l and r <= qr:
       apply(node, l, r, addC, addS)
       return
   push(node, l, r)  # propagate lazy to children
   mid = (l+r)//2
   if ql <= mid: update(left,...)
   if qr > mid: update(right,...)
   pull(node)  # recompute sumC, sumW, sumS from children

Apply function: apply(node, l, r, addC, addS):
   sumC[node] += addC * (r - l + 1)
   sumW[node] += addC * sumA[node]  # sumA is static sum of A in this segment
   sumS[node] += addS * (r - l + 1)
   lazyC[node] += addC
   lazyS[node] += addS

Push function: push(node, l, r):
   if l == r: return
   mid = (l+r)//2
   apply to left child with lazyC[node], lazyS[node]
   apply to right child with lazyC[node], lazyS[node]
   reset lazyC[node] = 0, lazyS[node] = 0

Pull function: pull(node):
   sumC[node] = sumC[left] + sumC[right]
   sumW[node] = sumW[left] + sumW[right]
   sumS[node] = sumS[left] + sumS[right]
   # sumA is static, no change.

Query function: query(node, l, r, ql, qr) returns tuple (sumW, sumS) for the range.
   if ql <= l and r <= qr: return (sumW[node], sumS[node])
   push(node, l, r)
   mid = (l+r)//2
   resW = 0, resS = 0
   if ql <= mid: (w,s) = query(left,...); resW+=w; resS+=s
   if qr > mid: (w,s) = query(right,...); resW+=w; resS+=s
   return (resW, resS)

Alternatively, we can have two separate query functions for sumW and sumS, but returning tuple is fine.

Complexities: O(log N) per update and query.

Now we need to handle the fact that we need to process B_j in order. Since B is sorted, we can just iterate j from 0 to N-1.

Edge Cases: When Y=0? The constraints say Y_k >= 1, so we always have at least one B. But we should handle Y=N.

Potential issues: The sumW and sumS can be large; Python int is fine.

Testing with sample 2 would be good.

Now, verify that the segment tree updates are correct: When we add B_j, we need to add to s_i for all A_i >= B_j. That's range [pos, N-1]. The update adds B_j to each s_i, so sumS increases by B_j * (N-pos). That's correct.

Also addC=1 adds to c_i, and sumW increases by sum of A_i in that range.

Now, we need to compute SA and SB prefix sums. SA[0]=0, SA[i] = sum of A[0..i-1] for i from 0..N. So SA[X] = sum of first X A's. Similarly SB[Y].

Now the answer formula: ans = 2*sumW - Y*SA[X] + X*SB[Y] - 2*sumS.

Double-check with sample 2? Let's do a small test manually or trust.

Potential off-by-one: In query range, we need prefix of length X: indices 0 to X-1 inclusive. So query(0, X-1). Ensure X can be N.

Now, complexity: N up to 1e5, K up to 1e4. Sorting O(N log N + K log K). Segment tree O((N+K) log N). This is efficient.

Memory: Segment tree arrays of size 4*N for each stored value: sumA (int), sumC, sumW, sumS, lazyC, lazyS. That's 6 arrays of size 4*1e5 = 4e5, each Python int (28 bytes) => ~6*4e5*28 ~ 67 MB, plus overhead, maybe okay. But we can reduce: sumA is static and can be stored in a separate array of size N, or computed on the fly using prefix sums. Since sumA for a node is needed during updates (apply), we can compute it as sumA_static = SA[r+1] - SA[l] using global prefix sums. That would avoid storing sumA in each node. However, during apply, we need to quickly get the sum of A in the node's segment. We can compute it as SA[r+1] - SA[l] where SA is global prefix sum. Since we have l and r, we can compute in O(1). That saves memory. Let's do that: we don't store sumA per node; we compute on the fly: node_sumA = SA[r+1] - SA[l].

But careful: In apply, we need to add addC * node_sumA to sumW[node]. So we can compute node_sumA = SA[r+1] - SA[l] (since SA is prefix sum of A). That works.

Thus we only need to store sumC, sumW, sumS, lazyC, lazyS. That's 5 arrays.

Segment tree node count: 4*N. For N=1e5, 4e5. 5 arrays of 4e5 = 2 million ints. That's okay.

Implementation details:

- Use recursion or iterative segment tree. Recursion depth up to 4*N? Actually depth is log2(N) ~ 17, fine. Python recursion limit is about 1000, so fine.

- For speed, we can implement iterative segment tree with lazy propagation? But recursive is easier and likely fast enough for N=1e5 and operations ~1e5 (N + K). Recursion overhead per operation is small.

Potential optimization: Use sys.stdin.read to read all input quickly.

Now, we must ensure that we sort queries by Y. For each query, we have (Y, X, idx). We'll sort by Y. Then iterate through sorted queries. Maintain a pointer processed = 0. For each query (Y_i, X_i, idx_i):
   while processed < Y_i:
       B_val = B[processed]
       pos = bisect_left(A, B_val)
       if pos < N:
           update(1, 0, N-1, pos, N-1, 1, B_val)
       processed += 1
   # now answer query
   sumW, sumS = query(1, 0, N-1, 0, X_i-1)
   SA_X = SA[X_i]
   SB_Y = SB[Y_i]
   ans = 2*sumW - Y_i*SA_X + X_i*SB_Y - 2*sumS
   store ans.

Note: X_i and Y_i are 1-indexed counts. Ensure that X_i can be N. Then query range 0..N-1. If X_i = 0? Not possible (X >= 1). So query(0, X_i-1) is valid.

Edge Cases: If X_i = 0 (should not happen), but just in case.

Now, test with sample 2. Let's try to compute manually a small part to ensure formula correct.

Sample 2:
N=5
A: 1163686 28892 1263085 2347878 520306
Sorted A: [28892, 520306, 1163686, 1263085, 2347878]
B: 1332157 1202905 2437161 1291976 563395
Sorted B: [563395, 1202905, 1291976, 1332157, 2437161]

Compute SA: [0, 28892, 549198, 1712884, 2975969, 5323847]
SB: [0, 563395, 1766300, 3059276, 4391433, 6828594]

Queries:
1) 5 3 -> X=5, Y=3
2) 1 5 -> X=1, Y=5
3) 2 3 -> X=2, Y=3
4) 1 2 -> X=1, Y=2
5) 5 5 -> X=5, Y=5

We can try to compute for query 1: X=5, Y=3.
First Y=3 B's: B[0..2] = [563395, 1202905, 1291976].
We need c_i for each A_i:
A[0]=28892: B <= 28892? none -> c=0, s=0.
A[1]=520306: B <= 520306? 563395 > 520306, so none -> c=0, s=0.
A[2]=1163686: B <= 1163686? 563395 <=, 1202905 >, 1291976 >. So one B (563395) -> c=1, s=563395.
A[3]=1263085: B <= 1263085? 563395, 1202905 <=, 1291976 >. So two B's: 563395+1202905=1766300. c=2, s=1766300.
A[4]=2347878: B <= 2347878? all three: c=3, s=563395+1202905+1291976 = 3059276.

Now compute sumW = Σ A_i * c_i = 28892*0 + 520306*0 + 1163686*1 + 1263085*2 + 2347878*3.
Compute: 1163686 + 2526170 + 7043634 = 1163686 + 2526170 = 3689856; + 7043634 = 10733490.
sumS = 0+0+563395+1766300+3059276 = 5388971.
SA_X = SA[5] = 5323847.
SB_Y = SB[3] = 3059276.
X=5, Y=3.
ans = 2*sumW - Y*SA_X + X*SB_Y - 2*sumS
= 2*10733490 - 3*5323847 + 5*3059276 - 2*5388971
= 21466980 - 15971541 + 15296380 - 10777942
Compute: 21466980 - 15971541 = 5495439
+15296380 = 20791819
-10777942 = 10013877? Wait sample answer is 13331322. Something is off. Let's recalc carefully.

Wait, sample output for first query is 13331322. Our calculation gave 10013877. Let's check calculations.

First, check sumW:
A values: [28892, 520306, 1163686, 1263085, 2347878]
c_i: [0,0,1,2,3]
Compute:
A0: 28892*0 = 0
A1: 520306*0 = 0
A2: 1163686*1 = 1163686
A3: 1263085*2 = 2526170
A4: 2347878*3 = 7043634
Sum = 1163686 + 2526170 = 3689856; +7043634 = 10733490. Yes.

sumS:
A2: s=563395
A3: s=1766300
A4: s=3059276
Sum = 563395+1766300=2329695; +3059276=5388971. Yes.

SA_X = sum of all A = 28892+520306=549198; +1163686=1712884; +1263085=2975969; +2347878=5323847. Yes.

SB_Y = sum of first 3 B's: 563395+1202905=1766300; +1291976=3059276. Yes.

Now compute ans:
2*sumW = 21466980
Y*SA_X = 3*5323847 = 15971541
X*SB_Y = 5*3059276 = 15296380
2*sumS = 2*5388971 = 10777942

Now: 2*sumW - Y*SA_X = 21466980 - 15971541 = 5495439
5495439 + X*SB_Y = 5495439 + 15296380 = 20791819
20791819 - 2*sumS = 20791819 - 10777942 = 10013877.

But sample answer is 13331322. So discrepancy. Did we misinterpret the sum? Let's recompute manually the sum for X=5, Y=3.

We need sum_{i=1..5} sum_{j=1..3} |A_i - B_j|.

Compute matrix:
A \ B:
A1=28892: |28892-563395|=534503; |28892-1202905|=1174013; |28892-1291976|=1263084. Sum = 534503+1174013+1263084 = 2971600? Let's compute: 534503+1174013=1708516; +1263084=2971600.
A2=520306: |520306-563395|=43089; |520306-1202905|=682599; |520306-1291976|=771670. Sum = 43089+682599=725688; +771670=1497358.
A3=1163686: |1163686-563395|=600291; |1163686-1202905|=39219; |1163686-1291976|=128290. Sum = 600291+39219=639510; +128290=767800.
A4=1263085: |1263085-563395|=699690; |1263085-1202905|=60180; |1263085-1291976|=28891. Sum = 699690+60180=759870; +28891=788761.
A5=2347878: |2347878-563395|=1784483; |2347878-1202905|=1144973; |2347878-1291976|=1055902. Sum = 1784483+1144973=2929456; +1055902=3985358.

Now total sum = 2971600+1497358=4468958; +767800=5236758; +