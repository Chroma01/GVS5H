- **Strong connectivity reduction:** The fixed edges form a forward path. A directed graph is strongly connected iff every proper prefix cut has at least one added edge from a white vertex on the right to a black vertex on the left. For a prefix with `w` whites and `b` blacks, the cut is uncovered exactly when all first `b` black vertices are matched to first `w` white vertices. If `b=0` or `w=N`, the cut is always uncovered; this is equivalent to `S[0]=='W'` or `S[-1]=='B'`, giving answer `0`. If `b>w`, the cut is automatically crossed.
- **Permutation model:** Order white vertices and black vertices by index. A pairing is a permutation `pi` where white rank `k` is paired with black rank `pi(k)`. A prefix event is `E(w,b)`: `{1,...,b}` is contained in `{pi(1),...,pi(w)}`. The number of permutations satisfying `E(w,b)` is `P(w,b) * (N-b)!`, where `P(a,b)=a!/(a-b)!` is a falling factorial.
- **Active cuts:** `E(w,b)` is contained in `E(w',b')` if `w' >= w` and `b' <= b`. Therefore cuts dominated by another cut are redundant. Keep the Pareto frontier: for each `w`, keep minimum `b`; scan `w` descending and keep a pair only if its `b` is strictly smaller than all larger-`w` kept `b`'s. Reverse the result. Active cuts are sorted with both `w_i` and `b_i` strictly increasing. If there are no active cuts, every pairing works and the answer is `N!`.
- **First bad active constraint:** Let `C_i` be the number of injective placements of the first `b_i` black ranks into the first `w_i` white positions such that `E_i` holds but no earlier active `E_j` holds. Then:
  `C_i = P(w_i,b_i) - sum_{j<i} C_j * P(w_i-b_j, b_i-b_j)`.
  The subtraction partitions placements by the earliest earlier active constraint `j`.
- **Final answer formula:** If the earliest active bad constraint is `i`, the remaining `N-b_i` black ranks can be placed arbitrarily, giving `(N-b_i)!` extensions. Thus bad pairings are `sum_i C_i * (N-b_i)!`, and the answer is `N! - bad` modulo `998244353`.
- **Efficient recurrence:** Let `slack_i = w_i - b_i` and `S_i = sum_{j<i} C_j * fact[w_i-b_j]`. Since `P(w_i-b_j,b_i-b_j) = fact[w_i-b_j] / fact[slack_i]`, we have:
  `C_i = (fact[w_i] - S_i) * invfact[slack_i]`.
  The hard part is computing all `S_i` online.
- **CDQ convolution:** Active cuts have increasing `b_j` and `w_i`. For a CDQ node `[l,r]` with mid, after computing left `C_j`, add to right `S_i`:
  `sum_{j in left} C_j * fact[w_i-b_j]`.
  Let `b0=b_l`. Build `A[x]=C_j` at `x=b_j-b0`, and `B[t]=fact[t]`. Then `conv=A*B`, and the contribution to `S_i` is `conv[w_i-b0]`. Use NTT for large blocks and naive loops for small blocks.
- **Pseudocode:**
  1. If `S[0]=='W'` or `S[-1]=='B'`, print `0`.
  2. Precompute factorials and inverse factorials.
  3. Scan proper prefixes, store minimal `b` for each `w` with `1<=b<=w<N`.
  4. Build active frontier by descending `w`, keeping strictly decreasing `b`, then reverse.
  5. If active is empty, print `N!`.
  6. Compute `C` by CDQ:
     - small block: sequential recurrence and local propagation;
     - large node: solve left, convolution-add left to right, solve right.
  7. Print `N! - sum_i C_i*(N-b_i)!`.
