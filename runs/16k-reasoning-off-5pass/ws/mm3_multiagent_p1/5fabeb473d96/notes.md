
## ideation
The problem asks for the sum of distances between two vertices \(u\) and \(v\) over all possible rooted trees \(T(P)\) where each vertex \(i\) (for \(2 \le i \le N\)) chooses a parent uniformly from \(\{1, \dots, i-1\}\). The sum is taken over all \((N-1)!\) possible parent sequences \(P\), modulo \(998244353\).

Key observations:
1. The random tree generation process (each vertex \(i\) picks a parent uniformly from earlier vertices) produces a uniform random rooted tree on \(N\) vertices. This is known as a random recursive tree.
2. The distance between \(u\) and \(v\) is the sum of edge weights \(A_i\) for edges on the path. By linearity of expectation (extended to total sum over all trees), the total sum over all \((N-1)!\) trees equals \((N-1)! \times \mathbb{E}[\text{distance}]\), but we can also compute it directly as \(\sum_{i=2}^N A_i \times (\text{number of trees where edge } (i, P_i) \text{ is on the path})\).
3. For a fixed vertex \(i > 1\), the edge \((i, P_i)\) is on the path between \(u\) and \(v\) if and only if \(i\) lies on the path. The probability that \(i\) lies on the path in a uniform random recursive tree depends on the relative order of \(i, u, v\).
4. Known result for random recursive trees: For vertices \(u < v\), the probability that vertex \(i\) is on the path between \(u\) and \(v\) is:
   - \(1\) if \(i = u\) or \(i = v\)
   - \(\frac{1}{i}\) if \(u < i < v\)
   - \(\frac{1}{u}\) if \(i < u\)
   - \(0\) if \(i > v\)
5. Therefore, the contribution of \(A_i\) to the expected distance is \(A_i \times p_i\), where \(p_i\) is the above probability. The total sum over all \((N-1)!\) trees is \((N-1)! \times \sum_{i=2}^N A_i p_i\). Since we need the sum modulo \(998244353\), we can compute \(\sum A_i p_i\) and multiply by \((N-1)! \bmod 998244353\).
6. For each query \((u, v)\) with \(u < v\), we can compute the answer as:
   \[
   \text{ans} = (N-1)! \times \left( A_u + A_v + \sum_{i=u+1}^{v-1} \frac{A_i}{i} + \sum_{i=2}^{u-1} \frac{A_i}{u} \right) \bmod 998244353
   \]
   (with the convention that empty sums are 0).
7. We need to answer up to \(2 \times 10^5\) queries efficiently. Precompute prefix sums of \(A_i / i\) and \(A_i\) to answer range sums in \(O(1)\) per query. Also precompute \((N-1)! \bmod 998244353\).

Pitfalls:
- Ensure modular inverse is used for division by \(i\) and \(u\).
- Handle the case where \(u=1\) (then the sum over \(i < u\) is empty).
- The constraints \(N, Q \le 2 \times 10^5\) require \(O(N + Q)\) or \(O((N+Q) \log N)\) time.
- The weights \(A_i\) can be up to \(10^9\), so use 64-bit integers before modulo.

## worker: Implement the solution in Python: precompute facto
- The solution uses the known probability distribution for a vertex to lie on the path between two vertices in a uniform random recursive tree.
- For a query (u, v) with u < v, the probability that vertex i is on the path is:
  - 1 if i = u or i = v
  - 1/i if u < i < v
  - 1/u if i < u
  - 0 if i > v
- The total sum over all (N-1)! trees is (N-1)! times the expected distance. We compute this modulo 998244353.
- Prefix sums allow O(1) query answering after O(N) preprocessing.
- Modular inverses are precomputed using the linear method O(N).
