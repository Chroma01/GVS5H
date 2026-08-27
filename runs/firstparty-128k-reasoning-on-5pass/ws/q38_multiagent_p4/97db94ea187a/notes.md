- **Layer decomposition:** Every connected graph has unique BFS distance layers from vertex 1. Root layer size is 1. Edges can only appear inside a layer or between consecutive layers, and every vertex in a non-root layer must have at least one edge to the previous layer.
- **Layer weight:** If previous layer size is p and new layer size is s, the edge generating function is  
  `W(p,s) = (1+x)^{C(s,2)} * (((1+x)^p - 1)^s) / s!`.  
  In `z = 1+x`, this is `z^{C(s,2)} * (z^p - 1)^s * invfact[s]`.
- **Label factor:** For a fixed ordered layer-size sequence, labels can be assigned in `(N-1)! / prod(s_i!)` ways. The DP keeps the `1/s!` factors and multiplies by `fact[N-1]` at the end.
- **State:** `(o, e, p, par)`, where `o` is total odd-distance non-root vertices, `e` is total even-distance non-root vertices, `p` is last layer size, and `par=0` means last layer even (initial root), `par=1` means last layer odd. Target is `o=H=N/2`, `e=H-1`.
- **Feasibility to finish:** From `par=0`, next layer must be odd, so unless final we need `H-o > 0`. From `par=1`, next layer must be even, so unless final we need `H-1-e > 0`. This is exact because all remaining vertices of one parity can be placed in a single layer.
- **Reachability with last size p:**  
  - `par=1`, `e=0`: only one odd layer, so `p=o`.  
  - `par=1`, `e>0`: need a previous odd layer, so `p <= o-1`.  
  - `par=0` non-root: need `o>=1, e>=1`; if `o=1`, the single odd layer forces one even layer, so `p=e`; if `o>=2`, any `1 <= p <= e` is reachable.  
  These prunes remove states that cannot occur, e.g. final odd layer with `p=H` when `e>0`.
- **Transitions:** `par=0 -> par=1` by adding odd size `a=1..H-o`. `par=1 -> par=0` by adding even size `b=1..H-1-e`; if `o=H`, only `b=H-1-e` can lead to a feasible final state. Precompute target indices and flat weight offsets `p*stride+s`.
- **Evaluation degree bound:** A balanced graph has `H-1` non-root even vertices, none adjacent to vertex 1, so at least `H-1` edges are missing. Thus maximum edges is `D = C(N,2) - H + 1`. Evaluate `F(x)` at `x=0..D`; `F(0)=0`.
- **DP per evaluation:** For each `x`, set `z=x+1 mod P`, compute `w[p,s]` for `1<=p,s<=H`, then run in-place DP over states sorted by `o+e`. Reduce a source value modulo P when read; target accumulations can be left unmodded because indegree is small and values stay around at most `15*P^2`.
- **Interpolation:** Use Newton forward differences: `c[k] = Δ^k vals[0]`, then expand `C(x,k)` iteratively: `C(x,k) = C(x,k-1)*(x-(k-1))/k`. Accumulate power-basis coefficients modulo P.
- **Output:** Coefficient of `x^M` is the answer for `M` edges. Output `M=N-1..C(N,2)`, with zeros for `M>D`.
- **Complexity:** For `N=30`, states are about 2.8k and transitions about 17k. With `D=421`, total inner DP updates are around 7 million, easily feasible in Python.
- **Pitfalls:** Do not prune using layer-count inequalities like `o <= e+1`; a single layer may contain many vertices. Do not forget that final odd layer with `p=H` is unreachable when there is any even layer. All inverses are valid because `P >= 1e8` and `D,N <= 435`.
