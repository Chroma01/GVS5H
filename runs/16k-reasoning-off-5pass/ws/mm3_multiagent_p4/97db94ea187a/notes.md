
## ideation
**Problem restatement**  
For each even `N ≤ 30` and each `M ∈ [N-1, N(N-1)/2]`, count labeled connected simple graphs on vertices `{1,…,N}` with `M` edges such that the BFS layers from vertex 1 have exactly `N/2` vertices in even distance and `N/2` in odd distance. Output counts modulo a prime `P`.

**Core difficulty**  
A direct enumeration is impossible (`N=30` gives up to ~4.35×10⁸ graphs). We need a combinatorial identity that extracts the exact layer sizes from generating functions.

**Key idea: signed EGFs and root of unity filter**  
Let `C(x) = Σ cₙ xⁿ/n!` be the EGF of connected labeled graphs where vertex 1 is the root. Let `D(x) = exp(C(x))` be the EGF of all labeled graphs (not necessarily connected). For `t ≥ 0`, let `Bₜ(x) = Σ bₜ,ₙ xⁿ/n!` be the EGF of graphs where the BFS distance from vertex 1 has parity congruent to `t (mod N+1)`. We can compute all `Bₜ(x)` for `t = 0..N` (a total of `N+1` series) using recurrences based on expanding the root's neighborhood layer by layer, and for each `t` keep a running EGF. The series have length up to `n = N`.

The signed count with weight `(-1)^k` for a root in a layer of size `k` is exactly the coefficient of `xⁿ/n!` in  
`F(x) = Σₜ Bₜ(x) · ζᵗ`, where `ζ = e^{2πi/(N+1)}` is a primitive `(N+1)`-th root of unity.  
Then by the inverse DFT:  
`Bₜ(x) = (1/(N+1)) Σⱼ F(x, ζʲ) · ζ^{-jt}`.

We only need `t = 0` (or any fixed `t`) to get the distribution of layer sizes. Actually, we need the exact count for even layer size `N/2`. This corresponds to a DFT of the sequence of counts over all possible parities in `ℤ_{N+1}`, then picking the correct frequency.

**Algorithm outline**  
1. Precompute factorials and inverse factorials up to `N` modulo `P`.  
2. Build the EGF for connected graphs rooted at 1:  
   - For `n = 1`: `c₁ = 1`.  
   - For `n ≥ 2`: `cₙ = 2^{\binom{n-1}{2}} - Σ_{k=1}^{n-1} \binom{n-1}{k-1} cₖ · 2^{\binom{n-k}{2}}`.  
   This counts connected graphs where 1 is in the component of size `n`.  
3. Compute the `Bₜ` series via a BFS layering DP:  
   - Maintain an array of EGFs `f[t]` for the current frontier, where `f[t]` records the contribution when the root's parity is `t mod (N+1)`.  
   - At each step, the frontier expands. When a new vertex is added, we choose a set of already-reached vertices to connect to (at least one), giving factors of `(2^{S} - 1)` where `S` is the number of already-reached vertices.  
   - This builds `Bₜ(x)` for all `t`.  
4. For each `j = 0..N`, evaluate the series `Fⱼ(x) = Σₜ Bₜ(x) ζ^{jt}` at the `N+1` roots of unity. Since we only need coefficients up to `x^N`, and `N ≤ 30`, we can precompute the values of `x^k` for `x = ζʲ` directly (no need for heavy polynomial multiplication).  
5. For each `M`, the answer is:  
   `Ans(M) = (1/(N+1)) Σ_{j=0}^{N} [coeff of x^N/N! in Fⱼ(x)] · ζ^{-j·0}`?  
   Actually we need to extract the count for layer size exactly `N/2`. The correct formula: the number of connected graphs where the even layer has exactly `N/2` vertices is the coefficient of `x^N/N!` in  
   `B₀(x)`? No, `Bₜ` is the sum over graphs with root parity `t` in the cyclic group `ℤ_{N+1}`. We need the exact number of vertices in the even layer, not a cyclic parity.  

   *Correction*: The standard trick: define a polynomial in a variable `u` where `u` tracks the number of vertices in even layers. The BFS partition is bipartite (ignoring the root's parity? Actually the graph is not necessarily bipartite in general, but the BFS layers from a root naturally alternate). The number of vertices at even distance is `|V₀|`, odd distance is `|V₁|`. We want `|V₀| = |V₁| = N/2`.  

   This can be solved by a two-variable generating function or by using a root of unity filter on the *size* of the even layer. Let `A(x, y) = Σ aₙ,ₖ xⁿ yᵏ/n!` where `k` is the number of vertices at even distance from root. Then we want `a_{N, N/2}`.  

   There is a known identity:  
   `aₙ,ₖ = (1/(N+1)) Σ_{j=0}^{N} ζ^{-jk} · [coeff]`, where `ζ` is a primitive `(N+1)`-th root of unity, and `[coeff]` is the coefficient in a modified EGF where each vertex in an even layer contributes a factor `ζʲ`.  

   Since `N ≤ 30`, we can just fix `j = 0..N`, and for each `j` compute a "weighted" EGF where each time we add a vertex to the even layer we multiply by `ζʲ`, and when we add to odd layer multiply by 1 (or the opposite, depending on convention). Then the inverse DFT gives the exact count for `k = N/2`.

6. Extract the coefficient of `x^N/N!` in this weighted EGF for each `j`, multiply by `ζ^{-j·N/2}`, sum over `j`, and divide by `N+1` (modulo `P`). This gives the answer for the connected count. Since we want connected graphs, we must use the connected EGF `C(x)`, not `D(x)`. The DFT and the connected nature are compatible because the root of unity filter is applied to the connected EGF directly (or we can do it on `D(x)` and subtract the disconnected part using the exponential formula, but it's easier to do it on `C(x)`).
