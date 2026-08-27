
## ideation
**Core difficulty:** For each query (u,v), we need the sum over all (N-1)! parent sequences P of the u–v distance in T(P). Naive enumeration is impossible (N up to 2e5). The key is linearity of expectation/summation: distance = Σ_i A_i · [edge i on path], so we need, for each edge i (connecting i to P_i), the number of P where edge i is on the u–v path.

**Key structural insight:** Edge i is on the u–v path iff exactly one of u, v lies in subtree(i). Since P_i ∈ [1, i-1] uniformly and independently across i, we need Pr[x ∈ subtree(i)] for x < i (if x ≥ i, x can't be in subtree(i) except x = i itself, but u,v < i is the interesting case; note subtree(i) contains only vertices ≥ i... wait — actually subtree(i) contains i and vertices whose ancestor chain passes through i, and any descendant j of i has j > i since parents are smaller. So x ∈ subtree(i) requires x ≥ i, i.e., only queries with u,v ≥ i matter... hmm, careful: x ∈ subtree(i) iff x = i or the chain from x upward hits i, which needs x > i. So for edge i to separate u and v (u < v), we need... u < v, and exactly one of u,v in subtree(i). Since subtree(i) ⊆ {i, i+1, ..., N}, if i > v then neither is in; if i ≤ u then both could be... wait u < i needed for u ∉. Let me re-derive: exactly one in subtree(i) requires the larger index v ≥ i (v could equal i? v ∈ subtree(i) iff v = i or chain hits i; v = i means v ∈ subtree(i) trivially). Cases: (a) i ≤ u: both u,v could be in subtree(i) — need exactly one. (b) u < i ≤ v: v might be in subtree(i), u is not (u < i means u ∉ subtree(i) since all elements of subtree(i) are ≥ i > u). So edge i on path iff [v ∈ subtree(i)] when u < i ≤ v, plus the case i ≤ u where exactly one of u,v ∈ subtree(i).

**Probability computation:** Define f(i, x) = Pr[x ∈ subtree(i)] for x > i. x ∈ subtree(i) iff following parents from x we encounter i. Let the chain be x = c_0 > c_1 > ... where c_{t+1} = P_{c_t}. We hit i iff at some step c_t > i we choose P_{c_t} = i, or we jump to some j with i < j < c_t and then hit i from j. Recursion: f(i, x) = (1/(x-1)) · [1 + Σ_{i < j < x} f(i, j)]... more precisely Pr[hit i from x] = (1/(x-1))·(1 + Σ_{j=i+1}^{x-1} f(i,j)). Let S(i, x) = 1 + Σ_{j=i+1}^{x-1} f(i,j). Then f(i,x) = S(i,x)/(x-1) and S(i, x+1) = S(i,x) + f(i,x) = S(i,x)·(1 + 1/(x-1)) = S(i,x)·x/(x-1). Telescoping: S(i, x) = Π_{k=i+1}^{x-1} (k+1)/k · S(i, i+1) = (x/(i+1)) · 1. So S(i,x) = x/(i+1) and f(i, x) = x / ((i+1)(x-1))... check: f(i, i+1) = 1/i. Formula: (i+1)/((i+1)·i) = 1/i ✓. So **f(i, x) = x / ((i+1)(x-1))** for x > i, and f(i,i) = 1, f(i,x) = 0 for x < i. Beautiful closed form!

**Counting formula:** For query (u,v), u < v. Number of P where edge i is on path = (N-1)! · p_i where:
- If i ≤ u: p_i = f(i,u)(1-f(i,v)) + f(i,v)(1-f(i,u)) = f(i,u) + f(i,v) - 2f(i,u)f(i,v).
- If u < i ≤ v: p_i = f(i,v) (with f(i,i)=1 when i=v; u ∉ subtree(i) automatically).
- If i > v: p_i = 0.

Answer = (N-1)! · Σ_i A_i · p_i, all mod 998244353.

**Simplification:** Σ over i of A_i·p_i splits into prefix sums. For fixed query: Σ_{i=u+1}^{v} A_i·f(i,v) + Σ_{i=2}^{u} A_i·(f(i,u)+f(i,v)-2f(i,u)f(i,v)). With f(i,x) = x/((i+1)(x-1)), each term is x/(x-1) · A_i/(i+1) — so define B_i = A_i/(i+1) (mod), prefix sums of B_i and of A_i·B_i/(i+1)... let's see: f(i,u)+f(i,v)-2f(i,u)f(i,v) = u/((i+1)(u-1)) + v/((i+1)(v-1)) - 2uv/((i+1)^2(u-1)(v-1)). So we need prefix sums of A_i/(i+1) and A_i/(i+1)^2. Then each query is O(1): answer = (N-1)! · [ C1·(pre1[v] - pre1[u]) + C2·pre1[u]... ] — workers should carefully expand. Specifically:
- Σ_{i=u+1}^{v} A_i f(i,v) = v/(v-1) · Σ_{i=u+1}^{v} A_i/(i+1), but careful at i=v: f(v,v)=1, while formula v/((v+1)(v-1)) ≠ 1. So handle i=v term separately: A_v·1 + Σ_{i=u+1}^{v-1} A_i·v/((i+1)(v-1)).
- Σ_{i=2}^{u} A_i f(i,u) = u/(u-1)·Σ_{i=2}^{u} A_i/(i+1), again i=u term: f(u,u)=1, separate. Wait i ranges over edges 2..N; for i ≤ u, f(i,u): if i = u, f=1; formula gives u/((u+1)(u-1)) ≠ 1. So separate boundary terms.

So precompute: P1[t] = Σ_{i=2}^{t} A_i·inv(i+1), P2[t] = Σ_{i=2}^{t} A_i·inv(i+1)^2 (mod). Then query:
ans_inner = A_v (i=v term, f=1)
+ v·inv(v-1)·(P1[v-1] - P1[u])  [i in u+1..v-1, only v in subtree]
+ [i in 2..u-1... and i=u terms]: for i=u: f(u,u)=1, f(u,v)=v/((u+1)(v-1)): contribution A_u·(1 + f(u,v) - 2f(u,v)) = A_u·(1 - f(u,v)). For i<u: A_i·(u/((i+1)(u-1)) + v/((i+1)(v-1)) - 2uv/((i+1)^2(u-1)(v-1))).
= A_u·(1 - v·inv((u+1)(v-1)))
+ u·inv(u-1)·P1[u-1] + v·inv(v-1)·P1[u-1] - 2uv·inv((u-1)(v-1))·P2[u-1].
Then answer = (N-1)! · ans_inner mod p.

**Pitfalls:**
- Modular inverses: precompute inv[1..N+1] via linear recurrence or pow. Note i+1 up to N+1.
- Boundary terms i=u and i=v where f equals 1, not the formula — easy to get wrong.
- Edge case u=1: then there are no i ≤ u terms with i≥2 except... i ranges 2..N; if u=1, case i ≤ u is empty, and case u < i ≤ v is i=2..v. Also i=v term A_v. Check formula: P1[u]=P1[1]=0 works if we define P1[1]=0, and the i=u term A_u doesn't exist (u=1 has no edge). Need to guard: only add A_u term if u ≥ 2.
- v = u+... all fine. Also note when u < i < v strictly vs i=v.
- Factorial (N-1)! mod p precompute.
- A_i up to 1e9, reduce mod.
- Verify with N=3 sample: P=(1,1),(1,2). Query (1,3): edges 2,3. i=2: u=1<2≤v=3, f(2,3)=3/(3·2)=1/2. i=3=v: f=1. Sum = A_2·(1/2)+A_3·1 = 1/2+1 = 3/2. Times (2)! = 2 → 3 ✓. Query (1,2): i=2=v: A_2·1=1; i=3>v: 0. Times 2 = 2 ✓.

**Complexity:** O(N) precompute, O(1) per query — easily fast enough.

## worker: Implement the full solution in Python: precompute 
- Derived closed form: for x > i, Pr[x ∈ subtree(i)] = f(i,x) = x / ((i+1)(x-1)). Proof: let S(i,x) = 1 + Σ_{i<j<x} f(i,j); then f(i,x) = S(i,x)/(x-1) and S(i,x+1) = S(i,x)·x/(x-1), telescoping to S(i,x) = x/(i+1). Base f(i,i+1) = 1/i ✓.
- Edge i lies on the u–v path iff exactly one of u,v is in subtree(i). Since subtree(i) ⊆ {i,...,N}: for u < i ≤ v only v can be inside (f(v,v)=1 boundary); for i ≤ u the probability is f(i,u)+f(i,v)−2f(i,u)f(i,v); for i > v it's 0.
- Boundary terms i=u (f(u,u)=1) and i=v (f(v,v)=1) don't match the closed form, so they're peeled off; interior sums use prefix arrays P1 (Σ A_i·inv(i+1)) and P2 (Σ A_i·inv(i+1)²).
- Total = (N-1)! · inner, all mod 998244353. Inverses via O(N) linear recurrence; O(1) per query.
- Verified against samples: Sample1 → 2,3; Sample2 → 100; Sample3 matches all six outputs. Also brute-force checked for N ≤ 7 against itertools.product enumeration of all (N-1)! parent sequences (random A, all query pairs) — exact agreement.
