We need to maximize the sum of `K` pair prices where each pair's price is the maximum of the three component sums (X+X, Y+Y, Z+Z).  
Key observation: for a pair `(a,b)`, the price equals `max( X_a+X_b, Y_a+Y_b, Z_a+Z_b )`. For each pair we can equivalently write it as `max( S_x, S_y, S_z )` where `S_x = X_a+X_b`, etc.  

A standard trick: consider one "dominant" component per pair. For any pair, at least one of the three sums is the price. We can guess which one is the max (X, Y, or Z) and build candidate solutions, taking the best.

Approach: For each cake, define two derived vectors:  
- `P_i = (X_i, Y_i - X_i, Z_i - X_i)`  
- `Q_i = (Y_i, Z_i - Y_i, X_i - Y_i)`  
- `R_i = (Z_i, X_i - Z_i, Y_i - Z_i)`

For a pair `(a,b)`, if `X` dominates (i.e., `X_a+X_b` is the max), then  
`X_a+X_b = (P_a.x + P_b.x) = max( (P_a.x+P_b.x), (P_a.y+P_b.y + X_a+X_b), (P_a.z+P_b.z + X_a+X_b) )`.  
But we can rewrite the pair price in terms of `P`:  
`price = max( P_a.x + P_b.x,  P_a.y + P_b.y + X_a+X_b,  P_a.z + P_b.z + X_a+X_b )`.  
Since `P_a.y = Y_a - X_a`, `P_a.y + P_b.y + X_a+X_b = Y_a + Y_b`. So this is just the same expression. Not directly helpful.

Better: Use transformation to reduce to a simpler problem.  
Define for each cake three numbers:
- `a_i = X_i + Y_i + Z_i`
- `b_i = X_i`
- `c_i = Y_i`
- `d_i = Z_i`

For a pair (i,j), price = max(b_i+b_j, c_i+c_j, d_i+d_j).  
Consider 3 candidate values per cake: `X_i - Y_i`, `Y_i - Z_i`, `Z_i - X_i`.  
Idea: For each pair, the price is the maximum of three linear functions. We can try a "discrete convex hull" / Lagrangian relaxation approach: find optimal pairing with respect to a weighted sum, and binary search the weights to align the max with the chosen component.

This is known as the problem "Maximum weight K perfect matching with max of linear forms". Solution approach:
- For each cake, define a 3D point: `p_i = (X_i, Y_i, Z_i)`.
- Consider weighted sum: for a pair, the weighted sum is `(X_i+X_j)*α + (Y_i+Y_j)*β + (Z_i+Z_j)*γ` with `α+β+γ=1`, `α,β,γ≥0`.
- The pair's price is `max(...)`. If we choose weights such that one component dominates, the max equals the weighted sum of that component.

We can use ternary search / linear programming over the 2D simplex. But N up to 1e5, K up to N/2, T up to 1e3 but sum N ≤ 1e5, so we need O(N log N) or O(N) per test.

Observation: The price of a pair is the max of three sums. For any pair, we can think of "labeling" the pair with the component that achieves the max (X, Y, or Z). Among all K pairs, each pair is assigned to one of the three categories. But the categories are not independent — a pair's actual price depends on the sum of that component.

Alternative viewpoint: The max of three sums equals the minimum over all `λ,μ,ν≥0, λ+μ+ν=1` of `λ*(X_i+X_j) + μ*(Y_i+Y_j) + ν*(Z_i+Z_j) * 3? No, by convex dual, max of linear functions = infimum of convex combination that upper bounds? Actually max(f1,f2,f3) = max_{i} f_i = sup_{λ∈Δ} min_i f_i? Not helpful.

Better: For each pair, we can compute its price directly. The challenge is selecting K disjoint pairs to maximize sum of pair prices. This is exactly a **maximum weight K-matching** in a complete graph, but the weight function has special structure.

Key insight: The weight `w(i,j) = max(X_i+X_j, Y_i+Y_j, Z_i+Z_z)` is a **maximum of linear functions** of `i` and `j` separately. Such a weight is a **Monge** type? Actually `max(A_i + A_j, B_i + B_j, C_i + C_j)` is a sum of two functions each depending on one index, but the max of additive functions is still decomposable: `w(i,j) = max( (X_i + A_j), (Y_i + B_j), (Z_i + C_j) )`? Wait:  
`X_i + X_j` depends on i and j additively. The max of additive functions is also expressible as: for each i, define the "profile" relative to j.

Consider sorting by one component. Let's fix the X-component. Suppose we sort cakes by X. If we want a pair's price to be determined by X, we need `X_i+X_j ≥ Y_i+Y_j` and `X_i+X_j ≥ Z_i+Z_z`. That is `X_i - Y_i ≥ Y_j - X_j` and `X_i - Z_i ≥ Z_j - X_j`. So for the X to dominate, we need the differences to satisfy ordering.

This suggests a greedy / DP approach: we can pair cakes such that for each pair, the dominating component is consistent. Since we only have 3 components, we can try all 3! = 6 orderings of the "dominance". For each ordering, we pair the largest with the smallest in that order, etc.

Actually, a known solution: sort cakes by `X_i - Y_i` (or similar), then consider matching in a way that ensures the max is from a specific component. The trick is to transform the problem into finding a maximum weight matching where weight is just a sum (not max), by considering a 3D reduction.

Standard solution for AtCoder ABC 400 Ex (or similar) "Assorted Cake":
- For each cake, define `u_i = X_i - Y_i`, `v_i = Y_i - Z_i`. Then the pair price can be written as:  
  `max(X_i+X_j, Y_i+Y_j, Z_i+Z_j) = Z_i+Z_j + max(u_i+u_j, v_i+v_j, 0)`.  
  Wait: Let's check.  
  `X_i - Z_i = (X_i - Y_i) + (Y_i - Z_i) = u_i + v_i`.  
  `Y_i - Z_i = v_i`.  
  So `X_i+X_j = (Z_i+Z_j) + (u_i+u_j) + 2v_i+2v_j? No. Let's do carefully:

Let `S_z = Z_i+Z_j`. Then:
- `X_i+X_j = Z_i+Z_j + (X_i - Z_i) + (X_j - Z_j) = S_z + (u_i+v_i) + (u_j+v_j) = S_z + (u_i+u_j) + (v_i+v_j)`.
- `Y_i+Y_j = Z_i+Z_j + (Y_i - Z_i) + (Y_j - Z_j) = S_z + v_i + v_j`.
- `Z_i+Z_j = S_z`.

So the price is `S_z + max( (u_i+u_j)+(v_i+v_j), v_i+v_j, 0 ) = S_z + max( v_i+v_j, 0, u_i+u_j+v_i+v_j )`.

That's not simply additive. But we can choose which "base" to use. For example, if we set `base = Y_i+Y_j`, then:
- `X_i+X_j = (Y_i+Y_j) + (X_i - Y_i) + (X_j - Y_j) = S_y + u_i + u_j`.
- `Z_i+Z_j = (Y_i+Y_j) - (Y_i - Z_i) - (Y_j - Z_j) = S_y - v_i - v_j`.

So `price = S_y + max(u_i+u_j, 0, -(v_i+v_j))`. Still has three terms.

Let's try base = X:
- `Y_i+Y_j = (X_i+X_j) - (X_i - Y_i) - (X_j - Y_j) = S_x - u_i - u_j`.
- `Z_i+Z_j = (X_i+X_j) - (X_i - Z_i) - (X_j - Z_j) = S_x - (u_i+v_i) - (u_j+v_j)`.

So `price = S_x + max(0, -u_i-u_j, -(u_i+v_i)-(u_j+v_j))`.

In all cases, the price is `base_sum + max(0, f(i)+f(j), g(i)+g(j))` where f and g are derived.

This is reminiscent of the "maximum weight matching in a complete graph with weight = max of two additive functions" which can be solved by considering the convex hull of the points `(f(i), g(i))`.

Actually, there is a known solution for ABC 400 G (or F?) — let me recall. The problem is from ABC 400, I think it's F or G. The solution uses a transformation: for each cake i, define a 3D point `(X_i, Y_i, Z_i)`. Then the pair price is the max of three dot products with basis vectors e1, e2, e3 of the sum. By Lagrangian relaxation, the maximum total sum over K pairs is `max_{λ,μ,ν≥0, λ+μ+ν=1} [ min_{i} (λ X_i + μ Y_i + ν Z_i) * 2K? No.

Wait, there's a known approach: For each pair, `max(X_i+X_j, Y_i+Y_j, Z_i+Z_j) = max_{s∈{1,2,3}} (C_s(i) + C_s(j))` where `C_1(i)=X_i, C_2(i)=Y_i, C_3(i)=Z_i`. The total sum over K pairs is `max_{assignment of each pair to a component} sum_{pairs} (C_{s(p)}(i) + C_{s(p)}(j))`. This looks like we need to choose a set of 2K cakes and partition them into K pairs, assigning each pair a component label, such that the sum of the chosen component sums is maximized. But the actual pair price is the max, not a choice. However, the max is at least any one of the three, so the sum of maxes is at least the sum of any particular component's sums. Conversely, the sum of maxes equals the sum over pairs of the maximum of the three. If we assign each pair the component that achieves the maximum for that pair, then the total sum is exactly the sum of those assigned components. So we can think: we need to select a matching of 2K vertices, and for each edge in the matching, we can "pay" either `X_i+X_j`, `Y_i+Y_j`, or `Z_i+Z_j`, but we must pay the maximum of the three. So we are forced to pay the max. This is not a choice.

However, consider the following: For any matching, the total sum is `sum_{edges} max(A_e, B_e, C_e)`. This is equivalent to: we want to find a matching that maximizes this. Since each edge's weight is the max of three linear functions, and each function is a sum of vertex potentials, we can apply the "Greedy matching for Monge weights"? Not directly.

Another idea: Use the fact that `max(A,B,C) = (A+B+C) - min(A,B,C) - median(A,B,C)? No. There is identity: `max(a,b,c) = a+b+c - min(a,b) - min(b,c) - min(a,c) + min(a,b,c)`. Not helpful.

Let's search memory: This is AtCoder ABC 400 F? Actually, the constraints N up to 1e5, T up to 1e3, sum N 1e5. The problem is "Assorted Cake" (ABC 400 F?). I recall a solution involving sorting by one difference and using a priority queue or two-pointer to pair.

Let me think: Suppose we want to maximize the sum of `max(X_i+X_j, Y_i+Y_j, Z_i+Z_j)`. Consider that for a pair, the max is at least the average of the three sums: `(X_i+X_j + Y_i+Y_j + Z_i+Z_j)/3`. So a lower bound is sum of all chosen values divided by 3. But we need exact.

Key observation: The weight function `w(i,j) = max(s_i + s_j, t_i + t_j, u_i + u_j)` is a **convex function** of the vector `(s_i, t_i, u_i)`? Not exactly.

But note: If we fix a pair, the weight is the maximum of three linear functions. The sum of such functions over a matching is a piecewise linear function. The maximum over matchings can be found by considering extreme points.

Alternative approach: Since we have only 3 components, we can try to construct the optimal matching explicitly. Consider sorting cakes by `X_i` descending. Pair the top K with bottom K? But the weight depends on all three components.

Wait, there is a known transformation: For each cake, define a vector `v_i = (X_i - Y_i, Y_i - Z_i)`. Then the max of the three sums can be expressed as `Z_i+Z_j + max(0, (X_i-Z_i)+(X_j-Z_j), (Y_i-Z_i)+(Y_j-Z_j))`. But `X_i-Z_i = (X_i-Y_i)+(Y_i-Z_i) = a_i + b_i` where `a_i = X_i - Y_i`, `b_i = Y_i - Z_i`. And `Y_i-Z_i = b_i`. So the max is `Z_i+Z_j + max(0, a_i+a_j+b_i+b_j, b_i+b_j) = Z_i+Z_j + max(0, b_i+b_j, a_i+b_i + a_j+b_j)`.

Let `c_i = b_i`, `d_i = a_i + b_i = X_i - Z_i`. Then the price is `Z_i+Z_j + max(0, c_i+c_j, d_i+d_j)`. This is a sum of `Z_i+Z_j` plus the max of two additive functions (the zero function is additive with constant 0). The zero function corresponds to not adding anything. So we have three additive functions: 0, c_i+c_j, d_i+d_j. But 0 is just the constant 0, which is additive: 0 = 0_i + 0_j where 0_i=0. So we can think of each cake having three "potentials": `p1_i = Z_i`, `p2_i = Z_i + c_i = Y_i`, `p3_i = Z_i + d_i = X_i`. And the weight is `max(p1_i+p1_j, p2_i+p2_j, p3_i+p3_j)`. So we are back to the original with just renaming.

Now, for any pair, the weight is the max of three sums. If we assign to each cake a "type" based on which component is largest for that cake? Not necessarily.

Consider the following: We can binary search on the answer? Or rather, for a given value `M`, can we check if there exists a matching of K pairs with total weight ≥ M? The total weight condition is sum of max >= M. Not easy.

Let's look for the editorial in my mind. I think the solution is:
- Sort cakes by `X_i - Y_i` (or similar).
- Then use a greedy algorithm with a priority queue to match the best with the worst in terms of some derived value, similar to maximizing sum of absolute differences.

Actually, I recall a solution for a problem where the weight is `max(A_i + A_j, B_i + B_j)` (two components). The solution sorts by `A_i - B_i` and pairs the largest with smallest, etc. For three components, it's an extension.

Let's derive: For two components, `w(i,j) = max(A_i+A_j, B_i+B_j) = (A_i+A_j + B_i+B_j + |(A_i-B_i) - (A_j-B_j)|)/2? Let's check:
`max(a,b) = (a+b+|a-b|)/2`. So `max(A_i+A_j, B_i+B_j) = (A_i+A_j + B_i+B_j + |(A_i-B_i) - (A_j-B_j)|)/2`. This is because `(A_i+A_j) - (B_i+B_j) = (A_i-B_i) - (A_j-B_j)`. So the weight is half the sum of all four values plus half the absolute difference of the differences. This is an additive term plus a term that depends on the absolute difference of a scalar per cake. For a matching, the sum of `|d_i - d_j|` over pairs is maximized by pairing the largest `d` with the smallest, second largest with second smallest, etc. So the optimal matching for two components is to sort by `d_i = A_i - B_i` and pair `i` with `N+1-i` (after sorting). Then sum up. That's a known result.

Now for three components: `max(A, B, C)`. Is there a similar decomposition? We can use: `max(A,B,C) = max(A, max(B,C))`. And `max(B,C) = (B+C+|B-C|)/2`. Then `max(A, (B+C+|B-C|)/2)`. This is not linear.

But we can write: `max(A,B,C) = (A+B+C)/3 + something? No.

However, we can use the identity: `max(A,B,C) = A + B + C - min(A,B) - min(B,C) - min(C,A) + min(A,B,C)`. Not helpful.

Another identity: For any three numbers, the max is the maximum over all permutations. We can think of it as the maximum of three linear functions. The sum over pairs is a piecewise linear convex function? Actually, the pointwise max of linear functions is convex. The function `f(i,j) = max(...)` is convex in `(i,j)` if we consider indices as continuous? Not exactly.

But we can use the concept of "Kuhn-Munkres" or "Hungarian" for maximum weight matching? But N=1e5, too large for O(N^3).

Wait, the problem is from AtCoder, so there must be an O(N log N) or O(N) solution per test case. Given the structure, it's likely a greedy with sorting.

Let's think about the Lagrangian relaxation. We want to maximize `sum_{pairs} max( X_i+X_j, Y_i+Y_j, Z_i+Z_j )`. Consider weights `α, β, γ ≥ 0, α+β+γ=1`. For any pair, `max(...) ≥ α(X_i+X_j) + β(Y_i+Y_j) + γ(Z_i+Z_j)`. So the total sum is at least `α sum X_{matched} + β sum Y_{matched} + γ sum Z_{matched}`. The right side is a linear function of the matched sets. To maximize the lower bound, we can choose α,β,γ to make the matching easy. But the actual sum might be larger.

However, there is a known technique: The maximum sum of max of linear functions over matchings can be found by considering the convex hull of the vectors. Since the weight is the max of dot products with standard basis, it's the support function of the set `{ (X_i, Y_i, Z_i) }` evaluated at the sum of two vectors. The sum of support functions over pairs is the support function of the Minkowski sum? Not directly.

Wait, for a pair, `max(e1·(v_i+v_j), e2·(v_i+v_j), e3·(v_i+v_j))` where `v_i = (X_i, Y_i, Z_i)`. This is the support function of the set `{e1, e2, e3}` evaluated at the vector `v_i+v_j`. The sum over pairs is the sum of support functions. Since support function is convex, the sum is convex in the matched vertices. Maximizing a convex function over a matching is a combinatorial optimization that might be solved by extreme points, but not sure.

Another angle: The problem might be reducible to finding the maximum weight K matching in a graph where edge weight is `|X_i - X_j|` or similar. Let's test with the two-component case: `w(i,j) = max(A_i+A_j, B_i+B_j) = (A_i+A_j + B_i+B_j + |(A_i-B_i) - (A_j-B_j)|)/2`. The sum over pairs of `(A_i+A_j + B_i+B_j)` is constant once we select which 2K vertices are used, because each selected vertex contributes its A and B to the sum. Specifically, if we select a set S of size 2K, then sum_{i∈S} A_i + B_i is fixed. The variable part is `sum_{pairs in matching of S} |d_i - d_j|`. This is maximized by pairing the largest d with smallest, etc. So the optimal S is the set of 2K vertices with largest `A_i + B_i`? Not exactly, because the absolute difference term also depends on the values. Let's check: The total sum = `0.5 * sum_{i∈S} (A_i+B_i) + 0.5 * sum_{pairs} |d_i - d_j|`. The first term is maximized by picking the 2K vertices with largest `A_i+B_i`. The second term depends on the multiset of d_i for i∈S. To maximize the total, we need to choose S to maximize the sum. But since the first term is linear in the indicator of S, and the second term is a convex function of the d_i's (the sum of absolute differences of a pairing is maximized by pairing extremes), the overall function is not simply choosing top 2K by A+B. Actually, in the two-component case, the optimal matching is obtained by sorting all N by `d_i = A_i - B_i` and then pairing the first K with the last K, the next K with the next last K, etc., and taking all N? Wait, if we must use exactly 2K vertices, we can just sort by d_i and pair the i-th with the (2K+1-i)-th among the top 2K? But which 2K? The first term suggests we want large A_i+B_i. The second term wants large spread in d_i. There is a trade-off. However, the known result for two components is: sort by `A_i - B_i`, and then pair `i` with `N+1-i` for i=1..K. That uses the top K and bottom K by d_i. This maximizes the sum of |d_i - d_j| given we pair the extremes. But does it also maximize the constant part? The constant part sum_{i in S} (A_i+B_i) is sum of A+B for the top K and bottom K. Is that optimal? Not necessarily. Let's test: Suppose A_i+B_i is small for extreme d_i. Then maybe picking different vertices gives higher total. So the two-component problem is not trivial; the editorial solution might be more involved.

Wait, I recall a specific problem: "Maximize sum of max(A_i+A_j, B_i+B_j)" — the solution is to consider the convex hull or use a greedy that works because of the structure of the weight. Let me think.

Actually, for two components, the weight can be written as `max(A_i+A_j, B_i+B_j) = (A_i+B_i + A_j+B_j + |(A_i-B_i) - (A_j-B_j)|)/2`. Let `S_i = A_i+B_i`, `D_i = A_i-B_i`. Then weight = `(S_i+S_j + |D_i - D_j|)/2`. We want to choose 2K vertices and pair them to maximize sum of `(S_i+S_j + |D_i - D_j|)/2`. Since `S_i+S_j` sums to `sum_{i∈M} S_i` where M is the set of 2K vertices, we want to maximize `sum_{i∈M} S_i + sum_{pairs} |D_i - D_j|`. The second term is maximized for a given multiset of D_i by pairing the largest with smallest, etc. This is a submodular optimization? But since we can choose any 2K vertices, the problem is: select a set M of size 2K and a perfect matching on M to maximize `f(M) + g(matching)`, where f(M)=sum S_i, and g(matching)=sum |D_i-D_j|. Since g(matching) is convex in the D_i's (specifically, it's the sum of distances in a matching, which is maximized by pairing extremes), the total is a convex function of the chosen vertices? Not exactly.

But there is a known trick: Sort by D_i. For any set M, the maximum matching sum of |D_i-D_j| is achieved by pairing the k-th from left with k-th from right in the sorted order of M. So we can think of selecting 2K vertices and then pairing the i-th smallest D in M with the i-th largest D in M. The sum of |D_i - D_j| over these K pairs is simply `sum_{i=1}^K (D_{(2K+1-i)} - D_{(i)})` where the order is within M. This is exactly the sum of differences between the top K and bottom K D-values in M. So the second term depends only on the multiset of D_i, specifically on the sum of the K largest D_i in M minus the sum of the K smallest D_i in M. So `g = sum_{largest K D_i in M} D - sum_{smallest K D_i in M} D`. Then the total objective is `sum_{i∈M} S_i + sum_{largest K} D_i - sum_{smallest K} D_i`. Since `S_i = A_i+B_i` and `D_i = A_i-B_i`, we have `S_i + D_i = 2A_i` and `S_i - D_i = 2B_i`. So:
- If D_i is among the largest K in M, we get an extra `D_i` added.
- If D_i is among the smallest K in M, we subtract `D_i`.
- All selected vertices contribute `S_i`.

Thus the total objective can be written as a linear function of the selected vertices with some weights depending on their D_i rank. This suggests a greedy algorithm: sort all vertices by D_i. Then we can decide for each vertex whether to include it, and if included, whether it will be in the "large D" group, "small D" group, or "middle" (not contributing to the D-difference part but still contributing S). However, the middle group contributes S but not D, so it's like we have three types of slots: large D (contribute S+D = 2A), small D (contribute S-D = 2B), and unpaired in the difference (contribute S = A+B). But we must have exactly K large D and K small D, and the remaining 0? Wait, M has size 2K. Among them, K have the largest D, and K have the smallest D. That means the 2K vertices are exactly partitioned into two sets of size K: the K with largest D and the K with smallest D. There is no middle group! Because we need 2K vertices, and we take the top K and bottom K by D. So every selected vertex is either a "large D" or a "small D". So the total objective is `sum_{i in top K} (S_i + D_i) + sum_{i in bottom K} (S_i - D_i) = 2 sum_{top K} A_i + 2 sum_{bottom K} B_i`. Wait, check: `S_i + D_i = 2A_i`, `S_i - D_i = 2B_i`. So the total objective is `2 * ( sum of A_i for top K D_i + sum of B_i for bottom K D_i )`. And we need to choose the split point such that the top K are those with largest D, bottom K are those with smallest D. But the set M is exactly the union of these two groups, which are disjoint and together size 2K. So we are selecting a threshold T, taking all vertices with D_i > T as top K, and all with D_i < T as bottom K. Since we need exactly K in each, we can sort by D_i. For each possible split (i.e., after sorting, the first K are bottom, last K are top), the objective is `2 * ( sum_{last K} A_i + sum_{first K} B_i )`. So the optimal is to take the split that maximizes this sum. Since the sorted order is fixed, we can compute the suffix sum of A_i and prefix sum of B_i for each possible split. There are N-2K+1 possible splits (we need at least K on each side). So we can find the maximum in O(N). This solves the two-component problem.

Great! Now we have three components. Can we generalize? The weight is `max(X_i+X_j, Y_i+Y_j, Z_i+Z_j)`. Let's try to express it as a combination of additive terms and a "correction" term that depends on the differences.

For three components, we can write:
`max(A,B,C) = (A+B+C)/3 + (2/3) * something? No.

Alternatively, use the identity: `max(A,B,C) = max(A, max(B,C))`. We already know `max(B,C) = (B+C+|B-C|)/2`. So `max(A,B,C) = max(A, (B+C+|B-C|)/2)`. This is not a single max of additive forms; it's a max of A and a function that is a max of two additive forms. But we can apply the same trick again: `max(A, (B+C+|B-C|)/2) = (A + (B+C+|B-C|)/2 + |A - (B+C+|B-C|)/2|)/2`. That introduces nested absolute values, which is not simple.

However, there is a known decomposition for three components using two differences. Consider the following: For each pair, the price is the max of three sums. We can think of the three sums as the three possible "pair types". The maximum is the largest among them. In the optimal solution, each pair will be "covered" by one of the three components that is the max. But we don't know which one ahead of time. However, we can consider the three cases separately and take the best.

Idea: For a fixed assignment of each pair to a component, the total price is simply the sum of the sums of that component over the pairs. But the assignment must be consistent: if a pair is assigned to X, then for that pair, `X_i+X_j ≥ Y_i+Y_j` and `X_i+X_j ≥ Z_i+Z_j`. This is a constraint on which pairs can be assigned to X. So we can formulate: we need to select a matching of K edges, and for each edge, choose a label from {X,Y,Z} such that the label's sum is indeed the max. Then maximize the sum of the labeled sums.

This is a maximum weight K-matching with a constraint that the weight of an edge is the max of three numbers, which is equal to the chosen label's sum. So we can think of each edge having three possible "weights" depending on which label is valid. The actual weight is the max, so it's at least any valid label's sum. But if we pick a label, the actual weight might be higher. However, if we ensure the chosen label is the max, then the weight equals that sum. So we can think of it as: we want to find a matching and a labeling of its edges such that for each edge, the label's sum is the max, and we maximize the sum of the label's sums. But since the label's sum is the max, the total sum is exactly the sum of the maxes. So we can instead try to find a matching and a labeling that satisfies the max conditions and maximizes the sum of the label's sums. The max conditions are inequalities: for an edge labeled X, we need `X_i+X_j ≥ Y_i+Y_j` and `X_i+X_j ≥ Z_i+Z_j`. This is equivalent to `(X_i - Y_i) + (X_j - Y_j) ≥ 0` and `(X_i - Z_i) + (X_j - Z_j) ≥ 0`. Let `a_i = X_i - Y_i`, `b_i = X_i - Z_i`. Then conditions are `a_i + a_j ≥ 0` and `b_i + b_j ≥ 0`. Similarly for other labels.

This is a matching problem with edge feasibility conditions. Since the conditions are of the form `f(i) + f(j) ≥ 0`, which is a "threshold" condition. This is similar to the two-component case where the condition for X to dominate is `a_i + a_j ≥ 0` (only one condition). For three components, we have two conditions per label.

But wait, we don't need to enforce the max condition if we are going to take the max anyway. The total sum is always the max, regardless of which component we think of it as. So we can ignore the feasibility and just compute the max for each edge. The challenge is to select K edges to maximize the sum of maxes. This is a combinatorial optimization on a complete graph with a special weight function. The weight function is a max of three additive functions. The sum of such weights over a matching is a submodular or supermodular function? Let's check: For a fixed set of vertices, the sum of maxes is a function of the pairing. The max function is convex, so the sum of convex functions is convex. Maximizing a convex function over a set of matchings is a combinatorial optimization that often has a greedy solution (like the maximum weight matching for convex weight functions on a line). But here the vertices are not ordered naturally.

Wait, there is a known result: For a weight function `w(i,j) = max_{k=1..m} (c_{k,i} + c_{k,j})`, the maximum weight matching can be found by considering the convex hull of the vectors `(c_{1,i}, c_{2,i}, ..., c_{m,i})`. Specifically, the weight is the support function of the set of standard basis vectors. The sum over pairs is the support function of the Minkowski sum. I recall a paper or a competitive programming trick: for three components, the solution is to sort by one of the differences and then use a priority queue or something.

Let's search my memory for AtCoder ABC 400 F. The problem is "Cake 400" or something. Actually, ABC 400 F is "Happy Birthday! 2"? Not sure. Let me think. The problem title might be "Assorted Cake" as given. I can try to recall the solution from the editorial.

I remember a problem: "Given N items with three attributes A, B, C. Choose K pairs to maximize sum of max(A_i+A_j, B_i+B_j, C_i+C_j)." The solution involves:
- Compute for each item a "value" and a "type".
- Sort by one attribute difference.
- Use a data structure to maintain the best candidates for the other two attributes.

Alternatively, there is a solution using the "Lagrangian relaxation" and "parametric search". Since the weight is the max of three linear functions, we can guess the "tightest" component for each pair. But that's circular.

Another approach: Since the weight is the max of three sums, we can write it as:
`max(X_i+X_j, Y_i+Y_j, Z_i+Z_j) = X_i+X_j + Y_i+Y_j + Z_i+Z_j - min( (Y_i+Y_j) - (X_i+X_j), ... )` Not simple.

Let's try to reduce to two-component problems. For any pair, the max is at least the max of any two. In particular, `max(A,B,C) ≥ max(A,B)`. So the sum of maxes is at least the sum of max of A and B. The optimal solution for max(A,B) is as derived above. But the actual sum of max(A,B,C) could be larger because the Z component might be the max for some pairs. So the true optimum is at least the optimum for the two-component case (taking the best pair of components). But is the optimum always achieved by some two-component reduction? Not necessarily, because the three components might interplay.

Wait, consider three components. We can choose which component is the "base" for each pair. For each pair, we pay the maximum. So we can think of assigning each pair to the component that is the maximum. Then the total sum is the sum over pairs of that component's sum. So if we could decide the assignment, the problem would be: select K pairs and assign each to a component such that the assigned component's sum is actually the max. This is a matching problem with three types of edges, and each edge of type X has weight X_i+X_j, but is only feasible if X_i+X_j ≥ Y_i+Y_j and X_i+X_j ≥ Z_i+Z_j. The feasibility condition is a linear inequality. The maximum weight K-matching in a graph with three types of edges and type-dependent feasibility might be solved by considering the convex hull of the feasible region.

Actually, I think the solution is to sort the cakes by `X_i - Y_i` (or similar), and then for each cake, we can determine which component would be the max if paired with some other cake. The structure is such that we can pair the cakes in a "greedy" way from both ends.

Let's try to find a pattern. For each cake, consider the differences: d1 = X - Y, d2 = Y - Z, d3 = Z - X (which is -d1-d2). The max of the three sums for a pair (i,j) is determined by the largest of the three sums. The sum of X is X_i+X_j. The difference between X sum and Y sum is (X_i - Y_i) + (X_j - Y_j) = d1_i + d1_j. So X is the max if d1_i + d1_j ≥ 0 and (X_i - Z_i) + (X_j - Z_j) ≥ 0, i.e., d1_i + d1_j + d2_i + d2_j ≥ 0. So X is the max iff d1_i + d1_j ≥ 0 and d1_i+d2_i + d1_j+d2_j ≥ 0. Similarly, Y is the max iff d1_i + d1_j ≤ 0 and d2_i + d2_j ≥ 0. Z is the max iff d1_i+d2_i + d1_j+d2_j ≤ 0 and d2_i + d2_j ≤ 0.

Let u_i = d1_i = X_i - Y_i, v_i = d2_i = Y_i - Z_i. Then:
- X max: u_i + u_j ≥ 0 and (u_i+v_i) + (u_j+v_j) ≥ 0.
- Y max: u_i + u_j ≤ 0 and v_i + v_j ≥ 0.
- Z max: (u_i+v_i) + (u_j+v_j) ≤ 0 and v_i + v_j ≤ 0.

Note that these three regions partition the (u_i, v_i) plane. Each cake is a point in the plane. The condition for a pair to have X as max is that the sum of their u's is ≥ 0 and sum of their (u+v)'s is ≥ 0. This is equivalent to: the midpoint of the two points lies in the region where u ≥ 0 and u+v ≥ 0. So if we sort the points by some angle, maybe we can pair them.

Alternatively, consider the transformation: For each cake, define a value `w_i = X_i - Y_i` and a value `t_i = Y_i - Z_i`. The pair price is `Z_i+Z_j + max(0, u_i+u_j, v_i+v_j)`? Let's recalc:
`X_i+X_j = Z_i+Z_j + (X_i-Z_i)+(X_j-Z_j) = Z_i+Z_j + (u_i+v_i)+(u_j+v_j)`.
`Y_i+Y_j = Z_i+Z_j + v_i+v_j`.
`Z_i+Z_j = Z_i+Z_j`.
So price = `Z_i+Z_j + max( (u_i+v_i)+(u_j+v_j), v_i+v_j, 0 ) = Z_i+Z_j + max( v_i+v_j, 0, u_i+u_j+v_i+v_j )`.

Let `a_i = v_i = Y_i - Z_i`, `b_i = u_i+v_i = X_i - Z_i`. Then price = `Z_i+Z_j + max( 0, a_i+a_j, b_i+b_j )`. This is a sum of `Z_i+Z_j` plus the max of three additive functions: 0, a_i+a_j, b_i+b_j. Note that 0 is additive (0_i + 0_j with 0_i=0). So we have three components: Z, a, b. And we want to maximize sum of (Z_i+Z_j) + sum of max(0, a_i+a_j, b_i+b_j). The first part is just the sum of Z_i over the matched vertices. The second part is similar to the original problem but with two "potential" components a and b, and a constant 0 component. The constant 0 component means that if a_i+a_j and b_i+b_j are both negative, the max is 0, so the price is just Z_i+Z_j. So it's like we have three components: Z, a, b, but the "0" is like a component that is always 0 for every cake? Actually, 0 is not a cake attribute; it's a constant. So the max of (0, a_i+a_j, b_i+b_j) is the same as the max of (0_i+0_j, a_i+a_j, b_i+b_j) where 0_i = 0. So we can think of each cake having a third attribute that is always 0? No, that would mean every cake has Z_i = 0, which is not true. Wait, the expression is `Z_i+Z_j + max(0, a_i+a_j, b_i+b_j)`. The `Z_i+Z_j` is separate. So we can write the total price as sum over pairs of `max( Z_i+Z_j, Z_i+Z_j + a_i+a_j, Z_i+Z_j + b_i+b_j )`. That is exactly `max( Z_i+Z_j, (Z_i+a_i)+(Z_j+a_j), (Z_i+b_i)+(Z_j+b_j) )`. But `Z_i+a_i = Y_i`, and `Z_i+b_i = X_i`. So it's back to the original. So this transformation didn't help.

What if we choose a different base? For example, use Y as base:
`price = Y_i+Y_j + max( 0, (X_i-Y_i)+(X_j-Y_j), -(Y_i-Z_i)-(Y_j-Z_j) )` = `Y_i+Y_j + max( 0, u_i+u_j, -v_i-v_j )`. Let `p_i = u_i`, `q_i = -v_i = Z_i - Y_i`. Then price = `Y_i+Y_j + max(0, p_i+p_j, q_i+q_j)`. Here the "extra" terms are p and q. Note that p_i = X_i - Y_i, q_i = Z_i - Y_i. So p_i + q_i = X_i + Z_i - 2Y_i. Not necessarily related.

So the price is `Y_i+Y_j + max(0, p_i+p_j, q_i+q_j)`. This is the sum of Y_i+Y_j plus the max of three additive functions: 0, p, q. Again, we can think of each cake having an attribute `Y_i` and two "bonus" attributes `p_i` and `q_i`. The total price is `sum Y_i` over matched vertices plus the sum of the maxes of the bonuses. But the max of bonuses is exactly the same as the original problem with three components where one component is always 0? No, because the 0 is not attached to a specific cake; it's a constant. But if we imagine a "dummy" component that is 0 for every cake, then the max of (0, p_i+p_j, q_i+q_j) is the max of the sums of three components: 0, p, q. However, the actual price includes `Y_i+Y_j`. So if we define a new cake with attributes: `Y_i` (base), and three "components" for the max: `0`, `p_i`, `q_i`. But the `0` is the same for all cakes. So the max is over three components, but one component is constant 0. This means that for any pair, the bonus is at least 0, and at least p_i+p_j, and at least q_i+q_j. So the bonus is `max(0, p_i+p_j, q_i+q_j)`. This is like having three components where one component is identically 0. But the problem is symmetric in the three components originally. Now we have broken the symmetry.

If we have three components where one is constant 0, we can perhaps reduce to the two-component case? Because for any pair, the max of (0, p, q) is the same as the max of (p, q) if p or q is positive, and 0 if both are negative. But we still have the max of three.

Wait, note that `max(0, p, q) = max( max(p, q), 0 )`. And `max(p, q) = (p+q+|p-q|)/2`. So `max(0, p, q) = max( 0, (p+q+|p-q|)/2 ) = (p+q+|p-q|)/2 + max(0, -(p+q+|p-q|)/2 )? Not simple.

But we can write: `max(0, p, q) = (p+q+|p-q|)/2 if p+q+|p-q| ≥ 0, else 0`. This is piecewise.

Alternatively, we can use the identity: `max(0, p, q) = (p+q+|p-q|)/2 - min(0, (p+q+|p-q|)/2)`. Not helpful.

Maybe we can find a direct greedy by sorting. Let's test with small N. Suppose we have N=2K cakes. We need to pair them. The total price is sum of maxes. Is there a way to determine the optimal pairing by sorting? For two components, the optimal pairing for a fixed set is to pair the i-th from left with i-th from right in the sorted order of d_i = A_i - B_i. For three components, we have two differences: u and v. The max of the three sums is determined by which of the three regions the pair falls into. The pairing that maximizes the sum of maxes might be to pair cakes that are "complementary" in some sense.

Consider the plane with axes u and v. Each cake is a point (u_i, v_i). The price of pairing i and j is `Z_i+Z_j + max(0, u_i+u_j, v_i+v_j)`. (Using the Z-base). The term `max(0, u_i+u_j, v_i+v_j)` is the "bonus". We want to maximize the sum of bonuses plus the sum of Z's. The sum of Z's is constant once we choose the 2K vertices. So we can first choose the 2K vertices to maximize the sum of Z_i plus the maximum possible sum of bonuses for that set. Then we pair them optimally. The maximum possible sum of bonuses for a given set M is the maximum weight matching in the complete graph on M with edge weight `max(0, u_i+u_j, v_i+v_j)`. This is again the same problem but with a 0 component and no Z component (the Z is already accounted for in the vertex selection). So we can separate: choose a set of 2K vertices to maximize `sum_{i∈M} Z_i + best_matching_bonus(M)`. The best_matching_bonus(M) is the maximum sum of `max(0, u_i+u_j, v_i+v_j)` over perfect matchings of M. This is a two-dimensional version.

Now, the bonus is the max of three additive functions. This is similar to the two-component case but with an extra 0. Can we solve the problem: given a set of points (u_i, v_i), find a perfect matching to maximize sum of `max(0, u_i+u_j, v_i+v_j)`? Note that `max(0, a, b) = max( max(a, b), 0 )`. And `max(a, b) = (a+b+|a-b|)/2`. So `max(0, a, b) = max( 0, (a+b+|a-b|)/2 )`. This is not additive.

But there is a known result: For any two points, the max of three additive functions is a convex function of the points. The maximum weight matching with a convex weight function on a line can be found by pairing extremes. But here the points are in 2D. However, we can map each point to a scalar that determines the matching. What scalar? In the two-component case, the weight is `(S_i+S_j + |D_i-D_j|)/2`, and the optimal matching pairs the extremes of D. For three components, maybe the optimal matching pairs the extremes of some derived scalar.

Let's try to express `max(0, a, b)` in a form similar to the two-component case. We have three numbers: 0, a, b. The max of three numbers can be written as:
`max(0, a, b) = (0 + a + b + |0-a| + |0-b| + |a-b|)/2? No, that's for min? Let's recall: For three numbers x, y, z, the max is `(x+y+z + |x-y| + |y-z| + |z-x|)/2? Let's test: x=3, y=2, z=1. Sum=6, |3-2|=1, |2-1|=1, |1-3|=2, total=10, half=5, which is max=3. Not 3. So that's wrong.
The correct identity: `max(x,y) = (x+y+|x-y|)/2`. For three: `max(x,y,z) = x + max(0, y-x, z-x)`. Not a simple sum of absolute differences.
Actually, `max(x,y,z) = (x+y+z) - min(x,y) - min(y,z) - min(z,x) + min(x,y,z)`. Not simple.

But there is a known approach: the maximum of three linear functions can be handled by considering the convex hull in 3D. For each cake, define a point P_i = (X_i, Y_i, Z_i). The pair price is the support function of the convex hull of the standard basis vectors evaluated at P_i + P_j. The sum over pairs is the support function of the Minkowski sum. I think the solution uses the fact that the optimal matching is obtained by sorting the points by a certain linear combination and then pairing.

Wait, I recall a problem: "Maximize sum of max(A_i+A_j, B_i+B_j, C_i+C_j) over K disjoint pairs." The solution is to compute the "convex hull" or "upper envelope" and then do a greedy. Specifically, for each cake, we can define a "value" as a linear function of the coordinates, and the optimal matching is to pair the largest with smallest, etc. But which linear function? It might be the one that maximizes the minimum of the three components? No.

Let's search my memory for the editorial. The problem is from AtCoder ABC 400, which was in early 2024. The problem F is "Happy Birthday! 2"? No, ABC 400 F is "Frog Jump"? Not sure. Let's think: ABC 400 is the 400th contest. The problems are A, B, C, D, E, F, G. The constraints N up to 1e5, T up to 1e3, sum N 1e5. This is likely problem F or G. The problem statement says "Find the maximum possible total price of the K pairs." It might be problem F "Assorted Cake"? Actually, I think it's problem F. I can try to reconstruct the solution from typical AtCoder F-level problems.

AtCoder F-level problems often have solutions involving sorting and data structures, or greedy. For this problem, I suspect the solution is:
- Sort the cakes by `X_i` (or some derived value).
- Use a priority queue or two pointers to match them.
- The key observation: The pair price is `max(X_i+X_j, Y_i+Y_j, Z_i+Z_j)`. For the optimal matching, we can assume that the pairs are formed between cakes that are "complementary" in the sense that one has a high X and the other has a high Y or Z, etc.

Another idea: Since we want to maximize the sum of maxes, we can think of it as: for each pair, the price is the maximum of three possible "values". We can consider the three possible values as the "gain" from that pair. The total gain is the sum of these maximums. We can try to construct a pairing that makes the max as large as possible. The max is large if the two cakes have a large sum in at least one component. So we want to pair cakes such that for each pair, at least one component sum is large.

Consider the following greedy: Sort cakes by X descending. Take the top K and bottom K? But the bottom K might have small X, so their X sum is small, but maybe their Y or Z is large. So we want to pair high X with high Y, etc. This is like a 3-dimensional matching.

Wait, there is a known solution using the "K-th best" or "parametric search" on the answer. For a given value M, we want to know if there is a matching of K pairs with total weight ≥ M. The total weight is sum of maxes. For each pair, the max is at least the max of any two. But that's not a linear condition.

Let's consider the Lagrangian relaxation more formally. We want to maximize `sum_{pairs} max( X_i+X_j, Y_i+Y_j, Z_i+Z_j )`. For any weights `α, β, γ ≥ 0` with `α+β+γ=1`, we have `max( X_i+X_j, Y_i+Y_j, Z_i+Z_j ) ≥ α(X_i+X_j) + β(Y_i+Y_j) + γ(Z_i+Z_j)`. So the maximum total weight is at least the maximum over all matchings of the linear combination. But the linear combination is just a weighted sum of the three attributes. For fixed α,β,γ, the weight of a pair is `(α X_i + β Y_i + γ Z_i) + (α X_j + β Y_j + γ Z_j)`. So the total weight of a matching is the sum of the values `w_i = α X_i + β Y_i + γ Z_i` over the 2K matched vertices. This is maximized by simply taking the 2K vertices with the largest `w_i`. The value of the linear combination for that matching is `sum_{top 2K} w_i`. So the maximum total weight of the original problem is at least `max_{α,β,γ≥0, α+β+γ=1} sum_{top 2K} (α X_i + β Y_i + γ Z_i)`. But this is only a lower bound, not necessarily achievable. However, there is a known property: for the maximum of linear functions, the bound is actually tight if the optimal matching for the original problem can be "priced" by some α,β,γ. In fact, the maximum over matchings of the sum of maxes is equal to the maximum over α,β,γ of the sum of the top 2K weighted values? Not exactly, because the max of the linear combination is not tight for all pairs. But there is a theorem: For a weight function that is the maximum of m linear functions, the maximum weight matching is equal to the maximum over the convex hull of the weight vectors of the linear assignment. This is related to the "assignment problem" with a cost that is the max of linear functions. I recall that for such problems, the optimal value is indeed the maximum over the convex hull of the weight vectors of the linear assignment problem. Specifically, the weight matrix `W_{ij} = max_k (A_{ki} + A_{kj})` is the support function of the set of columns of A. The maximum weight matching over this matrix is equal to the maximum over `λ` in the simplex of the maximum weight matching for the matrix `∑ λ_k A_{ki} + A_{kj}`. But since the matrix is a sum of two vectors, the optimal matching for a fixed λ is just to take the top 2K vertices by the score `s_i(λ) = ∑ λ_k A_{ki}`. Then the value is `sum_{top 2K} s_i(λ)`. So the maximum total weight is `max_{λ∈Δ} sum_{top 2K} s_i(λ)`. This is a concave function of λ? Actually, `s_i(λ)` is linear in λ, and the top 2K selection makes the sum a piecewise linear concave function of λ. The maximum over a convex set can be found at an extreme point. The extreme points of the simplex are the unit vectors. So the maximum over λ is achieved at a vertex! That means the maximum total weight is simply the maximum over the three components of the sum of the top 2K values of that component! Wait, is that true? Let's test.

If λ = (1,0,0), then s_i = X_i. The top 2K sum is sum of top 2K X_i. The value is that sum. But the actual pair weight for a matching using only X is just the sum of X_i+X_j = sum of X_i over 2K vertices. So the lower bound for λ=(1,0,0) is sum of top 2K X_i. Similarly for Y and Z. So the maximum over λ of the lower bound is max( sum top 2K X_i, sum top 2K Y_i, sum top 2K Z_i ). But the true optimum is at least this, but could be larger. For example, in the sample 1, N=3, K=1. Top 2 X: X=(6,3,2), top 2 sum = 9. Top 2 Y: Y=(3,5,7), top 2 sum = 12. Top 2 Z: Z=(8,0,3), top 2 sum = 11. Max of these is 12, which is the answer. So in that case, the answer equals the max of the top 2K sums of a single component. But in sample 2, first test case: N=5, K=2. Top 4 X: X = (1,1,1,1,100), top 4 sum = 103. Top 4 Y: Y = (2,2,2,2,100), top 4 sum = 106. Top 4 Z: Z = (3,3,3,3,200), top 4 sum = 209. Max of these is 209, which is the answer. So again, the answer is the max of the top 2K sums of a single component. In the second test case of sample 2: N=6, K=2. Top 4 X: (81,55,46,44) sum = 226? Wait, X values: 21,44,46,1,81,55. Top 4: 81,55,46,44 = 226. Top 4 Y: 74,71,74,83? Y: 74,71,28,74,83,31. Top 4: 83,74,74,71 = 302. Top 4 Z: 25,80,96,24,16,1. Top 4: 96,80,25,24 = 225. Max is 302? But the sample answer is 333. So the answer is greater than the max of the top 2K single component sums! Because 333 > 302. So the optimum is not just a single component. In the sample, the optimal pairing used pairs where one pair had price 176 (X+Y+Z? Actually, the pair (2,3): cake 2 (44,71,80) and cake 3 (46,28,96). X sum=90, Y sum=99, Z sum=176, max=176. The other pair (4,5): cake 4 (1,74,24) and cake 5 (81,83,16). X sum=82, Y sum=157, Z sum=40, max=157. Total = 176+157=333. The top 2K X sum is 226, top 2K Y sum is 302, top 2K Z sum is 225. The sum of top 2K Y is 302, but the actual total 333 is larger because the Y sums in the pairs are not just the top 2K Y values; they are paired with X or Z to boost the max. For the first pair, the max is Z (176), which is larger than the Y sum (99). For the second pair, the max is Y (157), which is larger than the Z sum (40). So the total is 176+157 = 333. Notice that the sum of the maxes is 333, while the sum of the Z components for the first pair is 176, and for the second is 40, total Z sum = 216. The sum of the Y components is 99+157=256. The sum of the X components is 90+82=172. The total maxes 333 is not simply a single component sum.

So the answer is not just the top 2K of one component. We need to find the optimal matching.

Now, how to solve it? Let's look at the structure. The weight is `max(X_i+X_j, Y_i+Y_j, Z_i+Z_j)`. We can think of each cake as a point in 3D. The pair weight is the L_infinity norm? No.

Consider the following transformation: For each cake, define a "value" `v_i = X_i + Y_i + Z_i`. Not directly.

Another idea: The problem can be solved by considering the "maximum weight K-matching" in a graph where the weight is the max of three sums. There is a known algorithm for this when the number of components is small: we can do a ternary search on the "angles" of the weight vector. But here the weight is the max of three fixed vectors. Actually, the weight is the support function of the set `{e1, e2, e3}`. The sum of support functions over a matching is the support function of the Minkowski sum of the matched points? No, the sum of support functions is not a support function of a sum; it's the support function of the union? Actually, `max_{k} (a_k + b_k) = max_{k} (a_k + b_k)`. The sum over pairs of `max_k (a_{ik} + a_{jk})` is the sum of support functions. The support function of a set is convex. The sum of convex functions is convex. The maximum weight matching with a convex weight function on a set of points can be found by a greedy algorithm if the points are sorted in a certain way. But here the points are in 3D.

Wait, there is a known result: For a weight function `w(i,j) = max_{k=1..m} (A_{ki} + A_{kj})`, the maximum weight perfect matching can be found by sorting the items by the "slope" of the upper envelope. Specifically, we can define a total order on the items such that the optimal matching pairs the i-th with the (N+1-i)-th in that order. But is that true? For m=2, we sorted by `A_{1i} - A_{2i}`. For m=3, maybe we sort by some linear combination? But the optimal matching might not be a simple "pair extremes" in a single total order. In the two-component case, the weight is `(S_i+S_j + |D_i-D_j|)/2`, which is the sum of a constant and a term that depends only on |D_i-D_j|. This allowed us to separate the constant part and the absolute difference part, and the absolute difference part is maximized by pairing extremes of D. For three components, the weight is not a simple function of differences. However, we can try to express `max(X_i+X_j, Y_i+Y_j, Z_i+Z_j)` in a form that separates into a sum of constants and a term that depends only on some differences.

Let's attempt to find such a decomposition. We want to write `max(A,B,C) = C + something`. We had `max(A,B,C) = C + max(A-C, B-C, 0)`. Let `a = A-C`, `b = B-C`. Then the extra is `max(a, b, 0)`. Now, `max(a, b, 0)` is the max of three numbers. We can write `max(a, b, 0) = max( max(a,b), 0 )`. And `max(a,b) = (a+b+|a-b|)/2`. So `max(a,b,0) = max( (a+b+|a-b|)/2, 0 )`. This is the max of two numbers: `M1 = (a+b+|a-b|)/2` and `M2 = 0`. The max of two numbers is `(M1 + M2 + |M1 - M2|)/2 = (M1 + |M1|)/2 = max(M1, 0)`. So `max(a,b,0) = max(0, (a+b+|a-b|)/2)`. This is not a simple additive form.

But we can write `max(0, M1) = (M1 + |M1|)/2 = (a+b+|a-b| + |a+b+|a-b||)/4`. This is getting messy.

Alternatively, use the fact that for any two pairs, the weight can be compared based on the components. Maybe we can solve the problem by reducing to a maximum weight matching in a bipartite graph? But N is up to 1e5, and we can choose any disjoint pairs, not necessarily bipartite. It's a general matching (non-bipartite) in a complete graph. The weight is a special function. There is a known polynomial-time algorithm for maximum weight matching in general graphs, but it's O(N^3). We need O(N log N).

Wait, the problem is not a general graph; it's a complete graph with a specific weight function. There is a known greedy for this: sort the items by one coordinate, and then pair them in a certain way. Let's look at the sample 2 second test case to see the optimal matching. The items:
1: (21,74,25)
2: (44,71,80)
3: (46,28,96)
4: (1,74,24)
5: (81,83,16)
6: (55,31,1)

We need K=2 pairs. The optimal pairs: (2,3) and (4,5). Let's compute the differences:
u = X-Y: 1: -53, 2: -27, 3: 18, 4: -73, 5: -2, 6: 24.
v = Y-Z: 1: 49, 2: -9, 3: -68, 4: 50, 5: 67, 6: 30.
b = X-Z: 1: -4, 2: -36, 3: -50, 4: -23, 5: 65, 6: 54.

For pair (2,3): u sum = -27+18 = -9 (negative), v sum = -9-68 = -77 (negative), b sum = -36-50 = -86 (negative). The max is Z (since b sum is most negative, meaning Z is largest). Indeed, price = Z sum = 80+96=176.
For pair (4,5): u sum = -73-2 = -75 (negative), v sum = 50+67 = 117 (positive), b sum = -23+65 = 42 (positive). The max is Y? Actually, v sum is positive, so Y is larger than Z. u sum is negative, so Y is larger than X. So Y is the max. Price = Y sum = 74+83=157.

So the optimal matching uses one pair where Z dominates, and one where Y dominates. The X component is never the max. The total sum is 176+157=333.

Notice that in the Z-dominant pair, both items have negative v and negative u? Actually, item 2: v=-9, u=-27; item 3: v=-68, u=18. Their u sum is -9, v sum is -77. So both sums are negative, meaning Z is the max. In the Y-dominant pair, item 4: v=50, u=-73; item 5: v=67, u=-2. Their v sum is 117, u sum is -75. So v sum positive, u sum negative, meaning Y is max.

So the optimal matching pairs items that are "complementary" in the sense that their u and v sums have certain signs. In general, the max component is determined by the signs of the sums of the differences. There are 3 possible sign patterns for the pair of (u, v) sums, corresponding to the three components dominating. For each pattern, the price is a specific linear function of the components.

Specifically, using the Z-base: price = Z_i+Z_j + max(0, u_i+u_j, v_i+v_j). The max is 0 if both u and v sums are ≤ 0. It's u sum if u sum ≥ 0 and u sum ≥ v sum. It's v sum if v sum ≥ 0 and v sum ≥ u sum. So the price is a piecewise linear function.

Now, suppose we decide that for a given pair, the max is Z. Then we must have u_i+u_j ≤ 0 and v_i+v_j ≤ 0. In that case, the price is just Z_i+Z_j. So if we can find a matching where every pair satisfies u_i+u_j ≤ 0 and v_i+v_j ≤ 0, then the total price is just the sum of Z_i over the matched vertices. To maximize this, we would want to pick the 2K vertices with the largest Z_i such that they can be paired with these conditions. The condition u_i+u_j ≤ 0 and v_i+v_j ≤ 0 is a "threshold" condition. Similarly, if the max is Y for a pair, then using the Y-base: price = Y_i+Y_j + max(0, p_i+p_j, q_i+q_j) where p = X-Y, q = Z-Y. The max is Y if p sum ≤ 0 and q sum ≥ 0? Let's derive: For Y to be the max, we need Y_i+Y_j ≥ X_i+X_j and Y_i+Y_j ≥ Z_i+Z_j. This is equivalent to (X_i - Y_i) + (X_j - Y_j) ≤ 0 and (Z_i - Y_i) + (Z_j