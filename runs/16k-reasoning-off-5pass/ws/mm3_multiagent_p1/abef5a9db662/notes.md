
## ideation
The problem involves processing a sequence of N contests, each with an interval [L_i, R_i]. For an initial rating X, the rating increases by 1 if it falls within the interval at the time of the contest. The rating only increases, and we need to compute the final rating for Q queries.

A key observation is that the final rating function F(X) (initial rating X to final rating) is non-decreasing. This is because if X1 < X2, the rating at each step for X1 is always ≤ that for X2 (proven by induction). Due to monotonicity, the set of X such that F(X) ∈ [L, R] is a contiguous interval [a, b]. Thus, each contest operation can be applied as a range add of 1 to the interval [a, b] in the X-domain.

We can maintain a segment tree over X ∈ [1, M] (where M = max possible initial rating, up to 5e5) that stores the current value F(X) = X + inc[X] (where inc[X] is the total increment added to X). The segment tree supports:
- Range add (update inc[X] for a range [l, r]).
- Query min and max of F(X) in a range to find the boundaries a and b.
- Point query to get the final F(X) for a query.

For each contest (L, R):
1. Find a: the smallest X such that F(X) ≥ L. This is done by traversing the segment tree: if a node's max < L, skip; else if leaf, return index; else search left if left child's max ≥ L, else search right.
2. Find b: the largest X such that F(X) ≤ R. Similarly, if a node's min > R, skip; else if leaf, return index; else search right if right child's min ≤ R, else search left.
3. If a and b exist and a ≤ b, perform a range add of 1 on [a, b] (update F(X) for all X in that range).

For each query X, perform a point query to get the final F(X).

Time complexity: O((N + Q) log M), where M ≤ 5e5. This is efficient for N ≤ 2e5 and Q ≤ 3e5.

## worker: Implement the segment tree with lazy propagation i
The solution uses a segment tree with lazy propagation to maintain the current rating `F(X) = X + inc[X]` for each initial rating `X` in the domain `[1, M]` where `M` is the maximum initial rating among all queries. Each contest `[L, R]` is processed by finding the contiguous interval `[a, b]` of `X` such that `F(X) ∈ [L, R]`, using `find_left` and `find_right` that exploit the monotonicity of `F`. Then a range add of 1 is applied to `[a, b]`. Finally, each query is answered by a point query.

The key insight is that `F` is non-decreasing, so the preimage of an interval is an interval. This allows batch updates on the `X`-domain instead of simulating each rating increment individually. The time complexity is `O((N + Q) log M)`, which fits the constraints.
