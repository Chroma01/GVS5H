
## ideation
The core difficulty: each pair's price is max of three coordinate sums, so it's like each pair "chooses" the best color, but the choice is coupled (max, not free assignment). We need to select 2K cakes and pair them to maximize sum of max(X_a+X_b, Y_a+Y_b, Z_a+Z_b).

Key observations and candidate directions:

1. **Reformulation**: Total = sum over pairs of max over colors. If we assign each pair a color c, the pair contributes at most (coord_c sum), and the max is achieved at the best color. So the answer equals max over assignments of colors to pairs of (sum of coordinate sums), where each pair's contribution is its assigned color's sum — because max >= any fixed assignment, and the optimal assignment achieves max per pair. So answer = max over (partition into K pairs + color per pair) of sum of (color-coordinate sums).

2. **Fixed color counts**: Suppose we decide kx pairs are X-colored, ky Y-colored, kz Z-colored, kx+ky+kz=K. Then we need max total: choose disjoint pairs, each labeled, maximizing sum. This is a weighted matching problem on N nodes with 3 edge-weight types — general matching is too slow (N up to 1e5, but only 3 colors).

3. **Structure for single color**: If all pairs used color X, optimal is to pick top 2K X-values and sum them (pairing doesn't matter for a sum!). Sum of X over chosen 2K cakes — pairing irrelevant. With mixed colors, the pairing matters only in how we allocate cakes to color-groups: each pair has two endpoints both contributing the same color's coordinate. So actually total = sum over cakes selected of (coordinate of its pair's color). So the problem reduces to: choose 2K cakes, partition them into K unordered pairs, assign each pair a color; each cake contributes its coordinate in its pair's color. Since pairing within a color group doesn't affect the sum, the ONLY thing that matters is: how many pairs of each color (kx, ky, kz), and which 2kx cakes are assigned to X-pairs, which 2ky to Y-pairs, which 2kz to Z-pairs (disjoint sets). Total = sum of X over X-set + sum of Y over Y-set + sum of Z over Z-set. Pairing is irrelevant!! 

   Wait — but the max constraint: a pair assigned color X contributes X_a+X_b, but the actual price is max(...), which is >= X_a+X_b. Since we're maximizing and the true price is the max, the total for a given pairing is sum of maxes, which equals max over color-assignments of sum of assigned coords. So the answer = max over pairings and color assignments of sum of assigned coordinates = max over ways to choose disjoint colored groups of size 2 (kx,ky,kz summing to K pairs, i.e., 2kx,2ky,2kz cakes) of (sum X over X-group + sum Y over Y-group + sum Z over Z-group). Because given any such selection, we can pair within groups arbitrarily and assign that color; the actual price (max) is >= the assigned sum... but we need equality in the optimization: the true objective (sum of maxes) >= any assignment sum, and for the optimal pairing, choosing the argmax color per pair achieves equality. So maximizing assignment-sum over all pairings+assignments gives exactly the max sum-of-maxes. And since pairing within color groups doesn't matter, it reduces to a **selection problem**: partition 2K chosen cakes into three labeled groups of even sizes (2kx, 2ky, 2kz), maximize sum of respective coordinates. Even-size constraint per group.

4. **Selection problem**: Choose disjoint sets Sx, Sy, Sz with |Sx|=2kx etc., kx+ky+kz=K. Maximize sum. Without the evenness constraint, for fixed (kx,ky,kz) this is: pick 2K cakes and assign each to one of three labels to maximize sum of label-coordinate, with exact counts — solvable by sorting on differences. The evenness of group sizes is a parity constraint per group.

5. **Simpler view**: Each selected cake contributes max? No — each cake contributes the coordinate of its group's color, and a cake in group X contributes X_i. A cake would ideally contribute max(X_i,Y_i,Z_i), but groups need even sizes and total 2K. Since we can freely choose kx,ky,kz (nonnegative, sum K), the problem: select 2K cakes, color each with one of 3 colors, each color used an even number of times, maximize sum of chosen coordinate per cake. Upper bound: sum of top 2K values of M_i = max(X_i,Y_i,Z_i). If we can achieve parity-feasibility with the top-2K-by-max selection, done. Parity issue: each color count must be even. Among top 2K by M_i, assign each cake its argmax color; if some color has odd count, we need to swap: either change a cake's assigned color (losing M_i - secondbest_i) or replace a cake with an outsider (losing M_i - M_j). This becomes a small parity-fix DP.

6. **Alternative cleaner approach**: DP over cakes sorted by M_i? Not obviously correct since selection isn't simply top-2K after recoloring... Actually the parity-fix only involves constant number of "defect" adjustments? Not exactly — parity is only mod 2, so at most 2 colors are odd; fixing requires at most... each fix changes parity of two colors (recolor one cake X->Y flips both parities). So from any assignment, at most one recolor fixes parity? If colors with odd counts: number of odd counts is even (sum=2K even), so 0 or 2 odd colors. If 2 odd (say X,Y odd), recolor one cake from X to Y (or Y to X): both become even. Or swap one X-cake with an outside cake assigned Y, etc. So the fix is a single "move"! But which cake to recolor might not be in top-2K selection optimally... We should consider: optimal solution = choose 2K cakes + coloring with even counts. Relax to: each cake colored arbitrarily, maximize sum, with parity constraint. 

   Candidate approach: DP where we process cakes and track (count selected mod ... , parities)? Count up to 2K (1e5) and parity 4 states: DP[i][j][p] too slow if done naively per cake (N * K * 4 = 1e10). Need smarter.

7. **Better: reduction to small case analysis.** Take top 2K cakes by M_i (any tie-breaking). Claim: there's an optimal solution differing from this set by at most a few swaps. Because parity constraint only needs parity fixes. Formal approach: compute best = sum of top 2K M_i. Then try all "parity-fix" candidates: for the selected set with argmax coloring, if parities even → answer is best. Else, consider modifications: (a) recolor one selected cake to a different color: new value best - (M_i - alt_i), flipping parity of two colors; (b) replace one selected cake i with one unselected cake j: value best - M_i + (coordinate of j in some color), flipping parities appropriately. Take max over all feasible single modifications that make all parities even. But is one modification always sufficient from the greedy top-2K? The unconstrained optimum (top 2K with argmax colors) has parity vector with 0 or 2 odd colors. Any feasible solution's symmetric difference with this set... The optimal feasible solution can be obtained from the unconstrained optimum by a sequence of moves each of which is "recolor" or "swap"; the parity constraint requires the total parity effect to fix the 2 odd colors. The minimum-cost way might involve 2 swaps (e.g., swap out an X-cake, swap in a Y-cake — that's one swap changing counts: remove X (X parity flips), add j colored Y (Y parity flips)). A single swap = remove i (color c1) add j (color c2): flips parity of c1 and c2. A single recolor of cake i from c1 to c2: flips c1, c2. So any single move flips exactly two color-parities (or same color twice = no change if c1==c2... recolor to same color is nothing; swap where c1==c2 flips twice = no parity change). Since we need to flip exactly the set of odd colors (size 2), one move with c1,c2 = the two odd colors suffices feasibility-wise. So optimal = unconstrained best minus min cost move that flips exactly the two odd colors. Moves: recolor selected cake i from its argmax color c1 to c2: cost M_i - coord_i(c2); or swap: remove selected i (color c1), add unselected j with color c2: cost M_i - coord_j(c2). Take min over i selected with argmax color c1, over c2 != c1 being the other odd color... wait c1 and c2 must be exactly the two odd colors (in some order). So: odd colors are p,q. Options: recolor a selected p-cake to q, or recolor a selected q-cake to p, or swap out a selected p-cake and bring in an unselected cake colored q, or swap out a selected q-cake and bring in unselected cake colored p. Compute min cost among these four categories. Answer = best - mincost.

   But careful: is the unconstrained optimum unique/tie issues? With ties in M_i at the boundary (2K-th value), different top-2K sets may have different parity vectors, and the optimal feasible solution might use a different tie-breaking with zero swap cost in terms of M-sum but fixing parity. The swap category handles this: swapping i (selected, M_i = boundary value) with j (unselected, M_j = same value, colored appropriately) has cost M_i - coord_j(c2) which could be 0 if M_j = coord_j(c2) = boundary. So considering all unselected j (including those tied at boundary) covers it. Also recolor cost could be 0 if cake has two equal max coords. Good.

   However, subtle: what if min-cost move requires swapping where the incoming j's best color c2 is one of the odd colors but we might also consider bringing j in with a non-argmax color — covered since we take coord_j(c2) for the specific needed color c2, using max over j of coord_j(c2). Yes: for swap category "remove p-colored selected cake, add q-colored cake", cost = min over selected i with color p of M_i ... no wait, cost = M_i - coord_j(q), minimized by minimizing M_i over selected p-cakes AND maximizing coord_j(q) over unselected j. These are independent! So cost_swap(p->q) = (min M_i among selected with argmax color p) - (max coord_j(q) among unselected j). Similarly recolor cost(p->q) = min over selected i with argmax p of (M_i - Y_i... coord_i(q)). Answer = best - min over the four directed options (p->q and q->p for both recolor and swap).

   Edge case: what if there are zero selected cakes of color p? Then p count is 0, even — contradiction with p odd. So fine. Also K>=1 ensures... if 2K = N, no unselected cakes; swaps impossible; recolor still possible. Also need: could a double-move ever beat single-move? Single move flips exactly the two odd parities and is feasible, and its cost is <= any multi-move? Not necessarily — multi-move could have negative total? No: any move's cost is >= ... hmm, swap cost could be negative if unselected j has coord_j(q) > M_i? But j unselected means M_j <= M_i for all selected i only if top-2K by M — M_j <= min selected M. coord_j(q) <= M_j <= M_i. So swap cost >= 0. Recolor cost >= 0. Multi-move total cost >= min single move cost? Each move cost >= 0, and we only need parity flip of {p,q}; a combination of moves achieving that has total cost >= cost of the cheapest single move achieving exactly {p,q} flip? Not obviously — two moves each flipping {p,r} and {q,r} combine to flip {p,q} (r flipped twice). Their combined cost could be less than any single {p,q} move? E.g., recolor p->r costs 1, recolor r->q costs 1, total 2, but direct p->q recolor costs 100. But wait — recoloring one cake p->r and another r->q: net counts: p-1, r: +1-1=0, q+1. Parities: p,q flipped. Cost 2 < 100. So multi-move CAN be better! Hmm. But note recolor p->r then the same... no, different cakes. So my single-move claim is wrong.

   Counter-scenario: colors p,q odd, r even. Moves: two recolors (p->r on cake a, r->q on cake b) cost small each. So we need min-cost "flow" on parity graph: this is a min-cost to fix parity = shortest path / T-join on 3 nodes. With 3 colors, the parity fix options: direct edge p-q (one move flipping p,q), or path p-r-q (two moves). Cost of edge = min move cost flipping that pair. Moves flipping pair (u,v): recolor u->v, recolor v->u, swap out u bring v, swap out v bring u. So compute edge costs c(p,q), c(q,r), c(p,r), then answer = best - min( c(p,q), c(p,r)+c(r,q) ). Since only 3 nodes, that's complete. But wait, can two moves interfere (same cake used twice)? Recolor p->r on cake a and r->q on cake b: if a==b, that means cake a recolored p->r then r->q = p->q net, which is just direct recolor p->q possibly with different intermediate cost — cost would be (M_a - coord_a(r)) + (coord_a(r) - coord_a(q)) = M_a - coord_a(q) = direct recolor cost. So using same cake twice degenerates to direct move, no double counting issue if we just take min over independent cakes; but the min-cost for edge (p,r) might be achieved on the same cake as min-cost for edge (r,q). E.g., only one r-cake... Let's think: c(p,r) via recolor p->r uses a p-cake; c(r,q) via recolor r->q uses an r-cake; different color groups so different cakes. Swap-based: c(p,r) via "remove p, add r" uses selected p-cake and unselected cake; c(r,q) via "remove r, add q" uses selected r-cake and unselected cake — could the same unselected cake j be the best "add" for both? Then we'd add j twice — not allowed. Possible conflict. Handle by considering combos? With only 3 colors and small cases, we can afford to be careful: enumerate the path type (direct or via r), and for the two-move path, the moves are: flip(p,r) and flip(r,q). Each move has 4 sub-types. Conflicts arise only when both moves use the same unselected cake as "add". We can handle by trying: for two-swap conflict case, compute best pair of distinct unselected cakes. Alternatively, avoid the issue: note that a two-move path p-r-q can also be seen as: recolor p->r (cake a, selected, color p) and recolor r->q (cake b, selected, color r) — selected cakes are distinct automatically (different color groups). Swap-out-p-add-r + recolor r->q: swap uses unselected j colored r, recolor uses selected r-cake — distinct (selected vs unselected). Swap-out-p-add-r + swap-out-r-add-q: both add unselected cakes — possible same j. In that case, alternative: remove p-cake, remove r-cake, add j colored r, add j' colored q with j' != j. Compute top two candidates for add-r and add-q and take best non-conflicting combination. Since only this one conflict pattern, manageable.

   Hmm wait, also "swap out p, add r" combined with "swap out r, add q": removes one p-cake and one r-cake (distinct groups, fine), adds two unselected cakes (need distinct). Similarly "recolor" moves never touch unselected. So only add-add conflict. Also both moves could be swaps sharing the same removed cake? Remove p-cake and remove r-cake — different groups, distinct. OK.

   Actually, simpler unified approach: since this is essentially a min-cost parity fix with tiny state, maybe just do a cleaner DP: think of it as we choose 2K cakes and 3-color them with even counts. Equivalent reformulation: pair up cakes within same color... Alternative classic approach: since pairing is free within color, the problem is exactly: max sum = max over kx,ky,kz even counts... hmm.

8. **Alternative cleaner formulation via "pair items"**: Another angle: create the answer directly: we need K pairs, each pair monochromatic in assignment, price = max. Equivalent: answer = max over choices. The selection view is solid. Let me reconsider complexity: per test case O(N log N) for sorting by M_i. Fine for 1e5 total.

   But wait — is the reduction "pairing doesn't matter" fully correct? Given groups Sx (2kx cakes), Sy, Sz, pair arbitrarily within groups, assign color X to Sx-pairs. Actual price per Sx-pair = max(X_a+X_b, Y_a+Y_b, Z_a+Z_b) >= X_a+X_b. Total >= sum_{i in Sx} X_i + ... So actual optimum >= selection optimum. Conversely, for the optimal pairing with prices = max, assign each pair its argmax color; then sum of prices = sum over pairs of assigned color sum = sum over cakes of their pair's argmax coordinate, which is a valid selection (even group sizes). So optimum <= selection optimum. Equality holds. 

9. **Now solve selection problem rigorously**: Maximize sum over choice of 2K cakes and coloring (3 colors, each even count) of sum of coord_i(color_i). 

   Approach: unconstrained: pick each cake's best coordinate M_i, take top 2K. Let colors assigned by argmax (ties: choose arbitrarily but maybe tie-breaking matters for parity; handle via considering moves with cost 0 possibilities — the move-based fix explores alternatives including recolors with cost M_i - coord_i(c) = 0 for tied coords, and swaps with tied boundary cakes; but ties at boundary with same M but different argmax: swap cost 0 covers switching). I think the min-cost parity fix (T-join on 3-node graph with edge costs = min move cost, plus handling add-add conflict) gives the exact optimum. Proof sketch: any feasible solution differs from the unconstrained optimum by a set of recolors and swaps; the parity of color-count differences must be even for all colors; the symmetric difference decomposes... Standard exchange argument: consider optimal feasible solution O maximizing sum; among all such, minimize symmetric difference with greedy set G (top 2K by M, argmax coloring). If G is feasible, done. Else G has exactly two odd colors p,q. O has all even. Compare counts: Let d_c = |O_c| - |G_c| (parity: d_p, d_q odd, d_r even). The difference between O and G consists of: cakes in O\G (added), cakes in G\O (removed), cakes in both but different color (recolored). Total sum(O) - sum(G) <= 0 since G is unconstrained max... but O is constrained-optimal so sum(O) <= sum(G), and we want to show sum(O) >= sum(G) - (min fix cost). Take the "difference" and decompose into moves each flipping two color parities (a recolor flips two; a swap = remove c1 + add c2 flips two; also remove c1 + add c1 flips none — possible if O swaps same-color cakes, but then exchanging them doesn't change feasibility and sum(G)>=... such swaps only decrease or keep sum since G took top M; actually add c1 remove c1 with M_add <= M_remove since G is top-2K... unless tie, then equal). The multiset of parity flips needed is {p,q}. Decompose the difference into primitive moves; the total cost (sum(G)-sum(O)) equals sum of move costs (telescoping per cake: each added cake contributes its coord, each removed contributes -M_i... careful with recolored cakes: cost = M_i - newcoord_i >= 0). The moves' parity-flip multiset must combine to {p,q} mod 2. With 3 colors, the multiset of edges (each move = edge between the two flipped colors, or loop for same-color swap which has cost >= 0 and can be dropped) must have odd degree at p,q and even at r. Min-cost such multiset given edge costs = min over T-join: either single edge pq, or pr+rq. Since actual move costs for the decomposition are >= the min edge costs (each move is a specific instance of an edge type), cost(O) >= min T-join cost... wait we need the opposite: we want a lower bound on sum(O), i.e., show there EXISTS feasible solution with cost <= min T-join cost. Construction: apply the min T-join moves to G: direct edge pq = single move (recolor or swap) — feasible, gives solution with sum = sum(G) - c(p,q). Path pr+rq = two moves — feasible if moves don't conflict (distinct cakes); conflicts only in add-add case; handle by second-best. And upper bound: any feasible O has cost(G) - cost(O) >= min T-join cost because its difference decomposes into a valid T-join multiset of moves, each costing >= corresponding min edge cost? Hmm, each move in decomposition is an instance of some edge type, and its cost >= min cost for that edge type. And the multiset contains a T-join (min T-join <= that multiset's cost <= total difference cost). So cost(O) <= cost(G) - minTjoin. Combined with construction: equality. The only gap: construction conflict (same unselected cake added twice, or same selected cake used in two moves — can that happen? Move1 = recolor p->r uses selected p-cake a; move2 = recolor r->q uses selected r-cake b; a != b since different color classes in G. Move1 = swap(remove p-cake a, add j as r); move2 = recolor r->q on selected r-cake b: a,b distinct groups; j unselected, fine. Move1 = swap(remove p, add j_r), move2 = swap(remove r-cake, add j_q): need j_r != j_q. Also could move1 = recolor r->p?? No — edge pr could be "recolor r->p" (selected r-cake recolored to p) and edge rq = "recolor r->q" (selected r-cake): both use selected r-cakes — could be the same cake if only one r-cake or same minimizer! If same cake a (color r) recolored to p and to q — conflict. Net effect of recoloring a from r to ... can't do both. But we could recolor a r->p and need another r->q from a different r-cake. So conflict possible in recolor-recolor when both edges' min uses same selected cake of color r (one as r->p, other as r->q). Similarly swap-remove-r in both moves. So conflicts: the two moves of the path share the middle color r; each move either "uses an r-cake from G" (recolor r->other, or swap removing r-cake) or "adds an unselected cake as r" (swap adding r). If both moves use an r-cake from G, need distinct cakes; if both add unselected cakes, need distinct. So for the path option, compute min over compatible pairs. Simplest: for path p-r-q, enumerate move types: each edge has up to 4 directed move options with associated (cost, used selected cake id or none, used unselected cake id or none). Just compute for each edge the best few moves (say top 2-3 by cost with their cake ids) and try combinations for compatibility. Since only constant combos, fine. Even simpler: compute c1 = min cost move for edge pr with details; c2 for rq; if conflict, try second-best for each. Keep top 3 candidates per edge per direction-type. Constant work.

   Alternatively — much simpler to implement correctly: since only parity matters and moves are cheap to evaluate, do a tiny "DP over parity with min-plus"... Actually here's a cleaner exact method: Lagrangian/greedy might be overkill. Let me think of a totally different, simpler-to-prove approach.

10. **Simpler alternative: DP over count with parity, using selection structure.** Hmm, N*K too big.

11. **Another approach: reduce to weighted matching on small structure?** No.

12. **Reformulate as assignment with evenness = pairing within color.** Note: even count per color = cakes of each color can be paired among themselves. Alternative: think of choosing K pairs directly where each pair has a color and both endpoints contribute that color. Equivalent original. 

13. **Cleanest implementable exact approach**: I think the move-based parity fix is correct but fiddly. Let me consider an alternative: min-cost flow on a graph with O(N) nodes but structure allowing greedy. Actually, here's a classical trick: the problem "select 2K items, 3-color with even classes, maximize sum" can be solved as follows. For each cake, its value if colored c is coord_i(c). WLOG think of choosing counts. Hmm.

    Alternative: sort by M_i. Prefix thinking: the optimal selected set is top-2K by M except possibly a few swaps near the boundary — actually swaps can involve any selected cake (min M_i of color p could be anywhere) and any unselected cake (max coord_j(q) could be a cake with low M but high q-coordinate, anywhere in the unselected range). But both are found by simple min/max scans. So the move approach needs only: for selected set: for each color c, min M_i among argmax-c cakes; for each ordered pair (c1!=c2), min (M_i - coord_i(c2)) among argmax-c1 selected cakes; for unselected: for each color c, max coord_j(c). All O(N). Then combine with tiny case analysis for conflicts. 

    Let me double check the "two odd colors" claim: sum of counts = 2K even, so number of colors with odd count is even: 0 or 2. Yes.

    Also possibility: 2K = N → no unselected → swaps unavailable; only recolors. Fine.

    Also K could be such that 2K < 2? No, K>=1, 2K>=2.

    Edge: what if top-2K selection has 0 odd colors → answer = sum of top 2K M_i. 

    Now the conflict handling for path p-r-q: moves for edge (p,r): types: A: recolor selected p-cake to r (uses selected p-cake); B: recolor selected r-cake to p (uses selected r-cake); C: swap: remove selected p-cake, add unselected cake as r (uses selected p-cake + unselected j); D: swap: remove selected r-cake, add unselected as p (uses selected r-cake + unselected j). Similarly edge (r,q). Conflicts only if both moves use the same selected r-cake (types B or D on both edges) or same unselected cake (types C or D on both). To keep it simple: for each edge, generate the list of ALL candidate moves? That's O(N) per edge — but combining naively is O(N^2). Instead: for each edge keep best and second-best move (with distinct cake identities) per "resource" category... Simpler: since conflict requires sharing a specific cake, and each move uses at most one selected r-cake and at most one unselected cake: compute for edge pr the top 3 moves by cost (overall), similarly for rq, then try all 3x3 combos, pick min cost compatible. Is top-3 enough? If best move of pr conflicts with best of rq, we try second bests; conflicts are on specific cake ids; with 3 candidates each, at least one compatible pair exists among top... hmm, worst case: pr's top3 all use selected r-cake #5 (impossible—each move uses distinct... no: recolor r->p on cake5, swap remove r-cake5 add unselected j1, swap remove cake5 add j2 — three moves all using cake5!). And rq's top3 all use cake5 too. Then need 4th best. To be safe, keep for each edge: best move NOT using any selected r-cake (i.e., types A or C-with... wait C uses selected p-cake not r; for edge pr, types using selected r-cake: B, D; types not: A, C) and best few using r-cakes with distinct cakes, plus for unselected-resource: best move not using unselected cakes (A, B) and top few with distinct unselected js. This is getting complicated but constant-factor. Alternative cleaner: directly compute the path cost via formulas considering resources:

    Path p-r-q total = min over configurations:
    - Both moves don't touch selected-r or unselected: recolor p->r (uses p-cake) + recolor r->q... touches r. Ugh.

    Maybe simpler: brute-force over "which cake is the pivot"? Alternative: compute path cost as min over:
    (i) recolor-based: min over selected p-cake a of (M_a - coord_a(r)) + min over selected r-cake b of (M_b - coord_b(q)) — distinct groups, no conflict. Similarly recolor q->r + recolor r->p. And recolor p->r + swap(remove r-cake b, add unselected j as q): b and j distinct from a automatically; cost = [min over p-cakes a: M_a - coord_a(r)] + [min over r-cakes b, unselected j: M_b - coord_j(q)]. No conflict (a is p-cake, b is r-cake, j unselected). 
    (ii) The only true conflict cases: both moves use a selected r-cake (recolor r->p + recolor r->q; recolor r->p + swap-remove-r-add-q; swap-remove-r-add-p + recolor r->q; swap-remove-r + swap-remove-r): need two distinct r-cakes. And both moves add unselected cakes (swap-add-r + swap-add-q): need two distinct unselected cakes. And mixed: one move uses selected r-cake, other adds unselected — no conflict.
    
    So: precompute for selected r-cakes: two best (min) values of (M_b - coord_b(p)) [for recolor r->p], two best of (M_b - coord_b(q)), two best of M_b [for swap-remove]. For unselected: two best (max) coord_j(p), coord_j(q), coord_j(r). Then enumerate all combinations for path p-r-q with distinct-cake constraints using top-2 lists (top-2 suffices since only one other move competes for one resource). Constant combos (~ a few dozen). Since colors are only 3 and we also take direct edge, total constant work per test case after O(N) scans + O(N log N) sort.

    Honestly, implementing this correctly is error-prone. Let me think if there's a cleaner overall algorithm.

14. **Cleaner alternative: reduce to min-cost flow with 3 color-sinks and solve via sorting?** The selection problem: choose 2K items, color with even classes. Equivalent to: max over even counts. Consider transforming: pair up items within each color class — the pairing is free, so evenness is the only constraint. Trick: duplicate parity handling via considering items sorted by M and doing DP on parity with "exchange" values... 

    Actually here's a clean DP: process cakes in decreasing order of M_i. Decide selection greedily: we select a prefix? No — swaps show selection isn't a prefix (a cake with low M but high specific coordinate could enter). Hmm, but wait: in the optimal solution, is the selected set always "top-2K by M except at most 2 swaps"? From the T-join analysis: optimal = G with at most 2 moves (direct edge = 1 move; path = 2 moves). Each move changes selection by at most one swap. So optimal set differs from top-2K by at most 2 swaps, and recolors. Yes! So the move-based analysis IS the algorithm, and it's exact. Good — so implement carefully.

15. Let me restate the algorithm per test case:
    - Compute M_i = max(X_i,Y_i,Z_i), and argmax color (pick any, say smallest index achieving max; ties fine because recolor moves with cost 0 handle alternative assignments... wait, need care: if X_i=Y_i=M_i and argmax picks X, recolor X->Y cost 0 available. Good.)
    - Sort indices by M_i descending. Selected = top 2K. Compute base = sum of M over selected.
    - For each selected cake, color g_i = argmax. Count parities. If all even → answer = base.
    - Else let odd colors be p,q; third color r.
      - Direct fix edge(p,q): min over moves flipping p,q:
        * recolor p->q: min over selected with g=p of (M_i - coord_i(q))
        * recolor q->p: symmetric
        * swap out p, add q: (min M_i over selected g=p) - (max coord_j(q) over unselected)
        * swap out q, add p: symmetric
        (if a category has no candidates, skip; e.g., no unselected cakes)
      - Path fix via r: cost = min over compatible move pairs, one flipping (p,r), one flipping (r,q). Enumerate move types for edge pr: 
        - recolor p->r (resource: selected p-cake)
        - recolor r->p (resource: selected r-cake)
        - swap remove p add r (resources: selected p-cake [min M], unselected cake [max coord r])
        - swap remove r add p (resources: selected r-cake, unselected cake)
        Similarly edge rq. Conflict only when both moves' resources overlap: shared selected r-cake or shared unselected cake. Since each move uses at most one selected-r cake and at most one unselected cake, and moves using selected p/q cakes never conflict with the other edge's resources (p-cakes and q-cakes are distinct groups from r-cakes and from each other's edge usage — edge pr uses p-cakes and r-cakes; edge rq uses q-cakes and r-cakes; p≠q so only r-cakes and unselected cakes can conflict).
        Implementation: for edge pr compute candidate moves as list of (cost, r_cake_id or -1, unsel_id or -1); keep, for the combination, the best move per category: actually simplest: build list of moves for pr: for recolor types and swap-remove types, the minimizing cake is specific; but for conflict-avoidance we may need second-best r-cake or second-best unselected. So: precompute:
        * best and second-best (value, id) for: selected r-cakes by (M - coord(p)), by (M - coord(q)), by M (for removal); selected p-cakes by M and by (M - coord(r))... p-cakes never conflict so only best needed. Similarly q.
        * unselected: best and second-best (value,id) for coord(p), coord(q), coord(r).
        Then enumerate all type combinations (4 x 4 = 16) for the path, using best or second-best to avoid id collision: for each combo, get move1 candidates (top1, or top2 if top1 collides — but collision depends on move2's id). Simplest: for each of the 16 combos, take top-2 candidates for each move (as (cost,id1,id2) tuples) and check up to 2x2 pairs for compatibility, take min. Constant.
      - answer = base - min(direct, path).
    
    This is correct but implementation-heavy. Given the constraints (sum N 1e5), performance is fine.

16. **Sanity check with examples.**
    Sample1: N=3,K=1. Cakes: (6,3,8) M=8 c=Z; (3,5,0) M=5 c=Y; (2,7,3) M=7 c=Y. 2K=2: select cakes 1,3 (M=8,7). colors Z,Y → counts Z=1,Y=1,X=0: odd = {Z,Y}, r=X. base=15. Direct edge ZY: recolor Z->Y: cake1: 8-3=5. recolor Y->Z: cake3: 7-3=4. swap out Z add Y: min M among Z-selected=8; max Y among unselected (cake2)=5 → 8-5=3. swap out Y add Z: min M among Y-selected: cake3 M=7; max Z unselected: cake2 Z=0 → 7-0=7. direct min=3 (swap out cake1(Z), add cake2 as Y). Path via X: edge(Z,X) moves: recolor Z->X: cake1: 8-6=2; recolor X->Z: none (no X selected); swap remove Z add X: 8 - max X unsel (cake2 X=3) = 5; swap remove X add Z: none. Best ZX move: 2 (recolor cake1 Z->X, uses selected Z-cake). Edge(X,Y): recolor Y->X: cake3: 7-2=5; recolor X->Y: none; swap remove Y add X: 7 - 3 = 4; swap remove X add Y: none. Best=4 (swap remove cake3(Y), add cake2 as X; resources: selected Y-cake3, unselected cake2). Compatible with move1 (uses selected Z-cake1)? Yes distinct. Path cost = 2+4=6. So answer = 15 - 3 = 12. ✓ (matches: pair cakes 2,3 price 12; our solution: remove cake1, add cake2 as Y → selected {3(Y),2(Y)} sum=7+5=12, even counts Y=2. ✓)

    Sample2 first case: 5 cakes: four (1,2,3) M=3 c=Z; one (100,100,200) M=200 c=Z. K=2, 2K=4. Top4 by M: cake5 (200,Z) + three of the (1,2,3) cakes (M=3 each, Z). base=209. Counts: Z=4 even, X=0,Y=0 → all even! Answer=209 ✓. (Pairing: any pairs, assign Z: pair two small: Z-sum 6, pair small+big: 203; total 209 ✓.)

    Second case: compute later; trust.

17. **Pitfalls:**
    - Ties in M at selection boundary: handled naturally because swap moves consider ALL unselected cakes' coordinates, including tied ones; a tied swap has cost M_i - coord_j(c) which may be 0. But subtlety: our "selected" set's argmax coloring might have odd parities while a different tie-broken selection is feasible with same base — the swap move with cost 0 captures it only if the incoming cake's coordinate equals M_j = boundary value and outgoing min-M cake of the needed color has M = boundary. Since tied, min M among selected of color p might be > boundary? No—if there are tied unselected with M = boundary, then selected min M = boundary too (since top-2K includes boundary-valued cakes... actually if ties straddle the boundary, some boundary cakes are in, some out; min selected M = boundary). OK so cost-0 swap found. But what if the needed swap requires removing a specific-color cake whose M is large while a same-M... no, swap cost = min over selected p-cakes of M_i minus max over unselected of coord_j(q); if there's any feasible zero-cost tie exchange it'll be found when min M (p) = boundary and max coord_j(q) = boundary. If the tie exchange requires removing a p-cake with M=boundary — min captures it. Good.
    - The argmax tie-breaking within selected cakes: a cake with X=Y=M assigned to X; the parity fix might need it as Y with cost 0 — recolor move cost M - coord = 0 captures. Good.
    - Overflow: values up to 1e9, sums up to 2e5 * 1e9 = 2e14 — use 64-bit.
    - When 2K = N: no unselected; swap moves invalid; also path moves requiring adds invalid. Recolors still fine. Also is answer always reachable? Yes, some feasible coloring exists (e.g., all pairs... any pairing gives a coloring with even counts — the all-argmax coloring might be odd-odd but recolor path always exists? With all cakes selected and 3 colors, can we always fix parity by recolors? Need to flip p,q: recolor a p-cake to q directly — always possible (any cake can be recolored to any color, cost >= 0). So direct edge always available via recolor. Good.)
    - K=1: 2 cakes selected, both must same color → counts (2,0,0) pattern. Our framework: top-2 by M, fix parity. Works.
    - Make sure "max coord_j(c) over unselected" uses raw coordinate, not M_j.
    - Second-best tracking for r-cakes and unselected cakes for conflict avoidance in path combos. Actually, let me simplify: for the path, note conflicts are rare; implement generically: for each edge (u,v) build a small list of candidate moves: for each of the 4 types, take best and second-best distinct-resource options. Then try all pairs (move from edge pr list) x (move from edge rq list), check resource disjointness (selected-r cake id, unselected cake id), take min total. List sizes: keep maybe up to 4 per type → 16 per edge → 256 pairs: trivial.
    
    Hmm, generating "second best" for swap moves: swap remove-u-add-v cost = M_i - coord_j(v); resources i (selected u-cake) and j. For edge pr, conflicts on i only if u==r. To get alternative candidates, keep top-2 removals (by min M) for color r, top-2 adds (by max coord) for each color for unselected. Then a swap move candidate = (removal option, add option) — but which pairing? Cost is sum of independent parts; for conflict checking we may need different combos: e.g., best removal + best add conflict with other edge's add → try best removal + second add, etc. So treat resources separately: for the path enumeration, a "move" = choice of type + specific resources. Let me just precompute lists:
      For each ordered pair (u,v), u!=v:
        recolor_uv: top-2 selected u-cakes by min (M - coord(v)) → list of (cost, cake_id).
        swap_uv: top-2 selected u-cakes by min M (removal candidates) and top-2 unselected by max coord(v) → candidate moves = up to 4 combos (cost = M_i - coord_j(v), resources i,j).
      Then edge(u,v) move list = recolor_uv entries (as (cost, sel_u_id, -1)) + swap_uv entries (as (cost, sel_u_id, unsel_id)). Keep all (<= 2+4=6 per ordered pair; edge uses both directions: edge(p,r) moves = moves flipping {p,r} = recolor_pr, recolor_rp, swap_pr, swap_rp → up to 12 candidates).
      Path cost = min over m1 in edge(p,r) candidates, m2 in edge(r,q) candidates, compatible (m1.sel_r_id != m2.sel_r_id if both set... more precisely: if both moves use a selected r-cake, ids must differ; if both use unselected cake, ids must differ; also can m1 use selected r-cake and m2 use... m2 uses selected r-cake or selected q-cake; r vs q distinct. Also m1 uses selected p-cake — no conflict with m2. Also: could m1 = swap remove r add p use unselected j, and m2 = swap remove q add r use same unselected j? Yes that's the unselected-unselected conflict, checked.) Also one more subtle conflict: m1 swap removes selected r-cake i; m2 recolors selected r-cake i — same cake, conflict, checked via sel_r id. What about m1 removes selected r-cake i and m2 adds unselected j — fine. What about m1 recolors p-cake a (p->r) and m2 recolors r-cake b (r->q): fine.
      Also direct edge = min over edge(p,q) candidates (no compatibility needed, single move).
    - Also: is it possible that the optimal fix uses path p-r-q where edge(p,r) move is "swap remove p add r" using unselected j, and edge(r,q) move is "recolor r->q" — and j as an r-cake... j is now selected but that doesn't affect m2. Fine.
    - One more subtlety: after swap remove-p-add-r, the added cake j contributes coord_j(r); in path's second move could we recolor j? No—moves are defined on G's coloring; our decomposition covers optimal via T-join on G-difference, and construction just needs existence of A feasible solution with that cost, which applying moves sequentially to G gives (each move maintains 2K selected and flips parities; final coloring feasible). Cost adds up correctly: move costs defined relative to current state? Recolor cost of a cake not touched before: same. Swap then recolor the added cake: not needed. Sequential application: m1 changes G's counts/coloring; m2's cost was defined w.r.t. G but the cakes it touches are untouched by m1 (compatibility ensures distinct cakes; also m2's recolor cake still has original color since m1 didn't touch it). Edge case: m1 = swap remove p add r (cake j added as r). m2 = recolor r->q on selected r-cake b — b is an original r-cake, untouched. Fine. So total cost = c1 + c2, final parities all even. 

    - Also need to double check the lower-bound direction more carefully (that no weird multi-move solution beats min(direct,path)): any feasible solution O; consider difference between G (with its argmax coloring) and O (with its coloring). Define for each cake: if in both, possibly different colors → "recolor" from g_i to o_i (if same color, nothing). If in G only: removal of color g_i. If in O only: addition of color o_i. Net count change per color = 0 total (both have 2K), and parity of (O_c - G_c): O even, G odd at p,q → changes odd at p,q, even at r. Now build multigraph of "flips": each recolor u->v = edge uv; each removal of color u paired with... removals and additions: total removals = total additions (both 2K selected). Pair each removal (color u) with an addition (color v) → edge uv (if u==v, loop = no flip, cost = M_i - coord_j(u) >= M_i - M_j >= 0). Recolor u->v cost = M_i - coord_i(v) >= 0. Each edge uv has cost >= min-move-cost(u,v)?? Recolor u->v cost >= recolor_uv min. Swap edge uv (removal i color u, addition j color v): cost = M_i - coord_j(v) >= min over all removals of u and adds of v = swap_uv min. Yes since M_i >= min M over selected u-cakes and coord_j(v) <= max over unselected. So each edge's cost >= corresponding edge min-cost. The multigraph has odd degree exactly at {p,q} (recolors and swap-edges contribute degree = flip counts; loops contribute degree 2 = even; also pure "recolor u->v" flips u (–1) and v (+1) — degree odd at u,v). Wait also need: number of recolors out of u minus into u etc.—parity of degree at color c = parity of (number of edges incident to c) = parity of net change? Each edge uv contributes 1 to degree of u and v. Total degree parity at c must equal parity of |O_c Δ ...| hmm, standard: parity of degree at c = parity of (changes involving c) = parity of (O_c - G_c) which is odd for p,q. Yes. So the multigraph is a T-join for T={p,q}; min T-join on 3 nodes = min(edge pq, edge pr + edge rq) using min edge costs; our multigraph's total cost >= that. Hence cost(G) - cost(O) = total edge cost >= min T-join cost → cost(O) <= cost(G) - minTjoin. And we construct a feasible solution achieving cost(G) - minTjoin (with compatible moves). Hence optimal. Also loops (u==v swaps) have cost >= 0 and don't help parity; fine. Also possible: addition without removal (if O has 2K = N... no, both have exactly 2K; removals = additions in count). Also recolor where g_i == o_i: nothing. Good. One more: the decomposition pairing of removals with additions is arbitrary — any pairing gives valid edges with cost >= min edge cost; total = sum M_removed - sum coord_added = cost difference contribution. Fine regardless of pairing since bound holds per edge. 

    Wait, one more check on the lower bound: cost(G) - cost(O) = [sum over G\O removals M_i] + [sum over recolored (M_i - coord_i(o_i))] - [sum over O\G additions coord_j(o_j)]... plus for cakes in both with same color: cancel. Yes telescopes correctly.

    Also the min T-join might use edge pr + rq where the SAME physical move minimizes both edges — that's the conflict case; our construction takes min over compatible pairs, which might be slightly more than c(pr)+c(rq) if the minimizers conflict. But then the lower bound would be c(pr)+c(rq) < constructed — is the true optimum maybe between? If min moves conflict, can the true optimum still achieve c(pr)+c(rq) via different decomposition? The lower bound says cost(O) <= base - minTjoin where minTjoin uses min edge costs. If the unique minimizers conflict, no feasible solution achieves base - (c(pr)+c(rq)) with those two moves; but maybe a feasible O achieves it via a different structure (e.g., a single cake recolored r->? ... a recolor r->p and r->q on the same cake is impossible; but what about recolor r->q on cake b plus recolor p->r... those don't conflict). The conflicting case: e.g., only one selected r-cake b, and c(pr) = recolor r->p on b, c(rq) = recolor r->q on b. Any feasible O with cost base - c(pr) - c(rq)? Its difference decomposition must have total cost = c(pr)+c(rq) with each edge >= min edge cost, forcing edges achieving minima — impossible without using b twice. Could use 3+ edges each at min cost... e.g., edges pr, rq, plus a loop? Loops cost >= 0; to achieve the same total, loop must be 0 and edges minimal — still conflict. Or different T-join: pr, rq is the only one with that cost (pq edge presumably more expensive). So optimum = base - (min compatible pair cost). Our algorithm computes exactly that. But hold on — could a 3-move solution with cost < compatible-pair cost exist? Moves costs >= 0, T-join with 3 edges: e.g., pr, rq, plus loop (cost 0 possible? loop = swap remove u add u with M_i = coord_j(u): possible with ties!). Then total = c(pr)+c(rq) with the two edges possibly conflicting — conflict remains. Or T-join {p,q} via edges pr, rq, and pq, pq? That's pr+rq+2pq >= ... more. So no. Also zero-cost loops don't change parity. Hence compatible-pair min is right. Similarly direct edge with a zero-cost loop: same as direct. Fine.

    Hmm, also one more possibility for the path: use edge pr twice? That flips p and r twice = no net — not a T-join for {p,q}. No.

18. **Implementation plan per test case:**
    - Read N,K, arrays X,Y,Z.
    - M_i, g_i (0/1/2).
    - Sort indices by M desc; selected = first 2K (mark boolean).
    - base = sum M of selected.
    - counts per color of selected g_i; find odd colors.
    - If none odd: print base.
    - Else p,q odd, r the remaining.
      Precompute helper structures:
      - For each color c: top-2 (by min M) selected cakes with g==c: list of (M_i, id) — for removals. Actually need min M; keep two smallest.
      - For each ordered pair (u,v): top-2 selected cakes with g==u by min (M_i - coord_i(v)).
      - For each color v: top-2 unselected cakes by max coord_j(v).
      Build edge candidate list L(u,v) (flips u,v):
        for recolor u->v: for each (cost,id) in top2 recolor_uv: add (cost, ('sel',u,id), None)
        for recolor v->u: similarly ('sel',v,id)
        for swap remove u add v: for each (Mi,id) in top2 removals of u, for each (val,j) in top2 adds of v: cost=Mi-val, resources ('sel',u,id), ('unsel',j)
        for swap remove v add u: symmetric.
      direct = min cost in L(p,q).
      path = min over m1 in L(p,r), m2 in L(r,q) with resource compatibility: compatible unless (both have sel resource with same color AND same id) — sel resources: m1's sel is color p or r; m2's is r or q; conflict only if both color r and same id. And unsel resources: conflict if same j. 
      answer = base - min(direct, path).
    - Print answer.

    Note: top-2 lists might have fewer entries (e.g., no unselected, or <2 selected of a color) — handle.
    
    Also: is top-2 enough for compatibility? Conflict involves at most one specific id from the other move. For recolor lists, top-2 distinct ids suffices (if best conflicts, use second). For swap combos 2x2: if (rem1,add1) conflicts with other move's add j* (add1==j*), try (rem1,add2); if rem conflicts (other's sel r id), try rem2. With 2x2 combos all enumerated, at least one avoids a single conflicting id... unless other move conflicts with rem1 AND rem2 (impossible, single id) and... we take min over all compatible pairs across the 2x2 of m1 and 2x2 of m2... wait m2's swap also 2x2. Compatibility checked per pair. Since each side has a conflict-free option against any single id (2 options for the conflicting resource suffice), min compatible will be found. But subtle: what if m1's best is recolor (single resource) and m2's best swap uses same... recolor r->p on cake b conflicts with m2 swap-remove-r on cake b: m1 has second recolor option (top-2). Also m1 could use a different type entirely (recolor p->r instead) — but that's a different candidate in L(p,r) with its own cost; we enumerate ALL candidates in L lists (each up to 2+2+4+4=12), so all types considered. The only approximation is truncation to top-2 per type; argued sufficient because any single conflicting id can be avoided by the second choice within the same type, and if the type's both options conflict... both options conflict means other move uses two ids? Other move has at most one sel-r id and one unsel id. For m1 swap (rem,add) 2x2: other move conflicts via sel-r id (blocks rem1 only) and unsel id (blocks add1 only): options (rem2, add2) survives. Good. For m1 recolor top-2: other blocks at most one id, other survives. So top-2 per resource is sufficient. 

    Also direct edge: single move, no compatibility; min over L(p,q) — but L built with top-2; min is exact.

19. **Verify on sample 2, case 2** (rough): N=6,K=2,2K=4. Cakes:
    1: (21,74,25) M=74 Y
    2: (44,71,80) M=80 Z
    3: (46,28,96) M=96 Z
    4: (1,74,24) M=74 Y
    5: (81,83,16) M=83 Y
    6: (55,31,1) M=55 X
    Top4 by M: cake3(96,Z), cake5(83,Y), cake2(80,Z), cake1(74,Y). (cake4 M=74 Y also tied with cake1! boundary tie.) base=96+83+80+74=333. Counts: Z=2,Y=2,X=0 → all even! Answer 333 ✓. Matches sample (pairs (2,3): max(90,99,176)=176; (4,5): max(82,157,40)=157; total 333; our selection: cakes {3,5,2,1} colored Z,Y,Z,Y sum=333 — pairing: pair Z's (3,2): price max(44+46,71+28,80+96)=176; pair Y's (5,1): max(102,157,41)=157. Total 333 ✓.)

20. **Complexity**: O(N log N) per test case. Sum N <= 1e5. Fine.

21. **Double-check the reduction once more with a tricky case**: Suppose prices' max is achieved by a color different from assignment — we proved equality of optima both directions. Also confirm: selection with even groups always realizable as pairs — yes, pair arbitrarily within group; price = max >= assigned sum; total actual >= selection sum; but for the upper bound direction we need: optimum pairing's sum-of-maxes <= selection optimum — yes since it induces a valid selection. And our constructed selection has sum = base - fix; the corresponding pairing has actual total >= that; and optimum pairing total = some selection value <= base - fix (by lower bound argument, any selection value <= base - minfix). Wait: lower bound showed any feasible selection O has value <= base - minTjoin... but minTjoin vs min compatible pair: value(O) <= base - minTjoin <= base - minCompatible? No: minCompatible >= minTjoin, so base - minCompatible <= base - minTjoin. We have value(O) <= base - minTjoin for ALL feasible O, and we construct O* with value = base - minCompatible. If minCompatible > minTjoin (conflict case), is O* optimal? Need: no feasible O with value in (base - minCompatible, base - minTjoin]. As argued, achieving value > base - minCompatible requires difference-decomposition cost < minCompatible; decomposition is a T-join multigraph with edge costs >= min edge costs; possible multigraphs: single pq edge (cost >= direct min — and direct min is achievable singly, so direct = min over L(p,q) exactly); or pr+rq (cost >= min compatible? NO — cost >= c(pr)+c(rq) but the decomposition's edges are specific moves which are automatically compatible (they come from an actual solution!). So decomposition cost >= min over compatible pairs = minCompatible. Yes! Because an actual solution's difference gives actual compatible moves. So value(O) <= base - min(directExact, minCompatiblePath, ...other T-joins like pr+rq+loops which cost more). Hence O* optimal. 

    Also T-join could be pq + (zero or more loops) — loops add >= 0. Or pr+rq. Or pq+pr+rq+... any T-join on 3 nodes reduces to one of those two minimal options. Good.

22. **One more edge case**: 2K selected but some color has count 0 selected — e.g., odd colors p,q with... odd means count >= 1, fine. For path via r: r has even count, possibly 0 selected r-cakes. Then moves needing selected r-cake unavailable; moves available: recolor p->r, swap remove p add r, etc. Path still possible: recolor p->r + recolor r->q? No r-cakes. recolor p->r + swap remove r... no. recolor p->r (p count decreases, r increases) + swap remove q add r?? That flips q and r: edges pr and qr — yes! swap remove q add r uses selected q-cake and unselected — no r-cake needed. So path = recolor p->r + swap(remove q, add r): counts: p-1 (even now), q-1 (odd→ q was odd, now even), r+2 (even). Feasible if unselected nonempty. If 2K=N and r count 0: path via r needs r-cakes for recolor r->p / r->q or removals — none; swaps adding r increase r to even but need corresponding flips... with 2K=N: moves: recolor p->r (p even, r odd) then need flip r,q: recolor r->q needs an r-cake — now the recolored cake IS an r-cake! Sequential application: recolor cake a from p to r, then recolor cake a from r to q = net p->q direct recolor, cost = (M_a - coord_a(r)) + (coord_a(r) - coord_a(q)) = M_a - coord_a(q) = direct recolor cost, already considered in direct edge. But our path enumeration would treat m1 (recolor p->r on a) and m2 (recolor r->q on ??? needs an r-cake in G — none in G, so not in candidate list). So path unavailable, direct covers it. Fine. But subtle: m2 candidates are built from G's r-cakes; if none, skip. Correct.

    Also: could the optimal two-move solution use the SAME cake sequentially in a non-degenerate way? Recolor p->r on a, then recolor r->q on a = direct p->q, same cost. Swap remove p-cake a add j as r, then recolor j r->q: net = swap remove p add q, cost = (M_a - coord_j(r)) + (coord_j(r) - coord_j(q)) = M_a - coord_j(q) = direct swap cost. Covered by direct. So no loss. 

23. **Now also handle the possibility that direct/path moves have negative cost?** Recolor cost = M_i - coord_i(v) >= 0. Swap cost = M_i - coord_j(v): M_i >= any selected M >= ... wait min over selected u-cakes of M_i could be less than coord_j(v) for unselected j? coord_j(v) <= M_j <= (min selected M) <= M_i? M_j <= min selected M only if j unselected and selection is top-2K by M: yes, M_j <= M_{(2K)} <= M_i for all selected i. So swap cost >= 0. Good, moves non-negative; answer <= base. Also answer >= 0 trivially.

24. **Ties in sorting**: stable or any order fine.

25. Let me also reconsider: is it legitimate that a "swap" move's added cake j gets color v but j's argmax might be different — doesn't matter, we use coord_j(v) directly. And in the constructed solution, j is colored v. Fine.

26. **Final check on problem constraints**: T up to 1000, sum N <= 1e5. Per test overhead constant. Python speed: sorting 1e5 fine. The per-test candidate enumeration: building L lists: for each of 3 edges... we only need edges among (p,q,r) = all three pairs: L(p,q), L(p,r), L(r,q). Each needs top-2 structures for all colors and ordered pairs — compute once per test case (only when needed): 
    - rem_top2[c]: two smallest M among selected with g==c (with ids).
    - rec_top2[u][v]: two smallest (M - coord(v)) among selected g==u.
    - add_top2[v]: two largest coord(v) among unselected.
    All O(N) scans. Then build lists and enumerate. Constant per test.

27. **Potential pitfall**: When 2 odd colors exist, we assumed exactly {p,q}. If 0 odd, done. Can't have 1 or 3 odd (sum even → number of odd counts even; 3 odd would sum to odd+odd+odd=odd... 3 odds sum to odd, but 2K even, impossible; wait odd+odd+odd = odd, yes impossible). Good.

28. **Also handle K pairs where 2K < 2?** K>=1 so 2K>=2. N>=2.

29. **Let me test mentally on a parity-fix example**: N=4,K=1... 2K=2. Cakes: A:(5,0,0) M=5 X; B:(4,0,0) M=4 X; C:(0,3,0) M=3 Y unselected; D:(0,0,2) M=2 Z unselected. Top2: A,B both X → counts X=2 even → answer=9. Pair A,B price = max(9,0,0)=9 ✓. But alternative pair A,C: max(5,3,0)=5 <9. OK.
    Another: A:(5,0,0), B:(0,4,0), C:(0,0,3), K=1, N=3, 2K=2. M:5 X,4 Y,3 Z. Select A,B: counts X=1,Y=1 odd → p=X,q=Y,r=Z. base=9. Direct: recolor X->Y: A: 5-0=5; recolor Y->X: B: 4-0=4; swap remove X add Y: minM_X=5 - max Y unsel (C:0) =5; swap remove Y add X: 4 - max X unsel(C:0)=4. direct=4. Path via Z: edge(X,Z): recolor X->Z: A:5-0=5; swap remove X add Z: 5 - 3(C's Z)=2; recolor Z->X none; swap remove Z none. Edge(Z,Y): recolor Y->Z: B:4-0=4; swap remove Y add Z: 4-3=1. Path options: m1 from {recolor A X->Z (5, selX=A), swap rem A add C as Z (2, selX=A, unsel=C)}; m2 from {recolor B Y->Z (4, selY=B), swap rem B add C as Z (1, selY=B, unsel=C)}. Compatible pairs: (5,4)=9; (5, swap B+C:1)=6; (swap A+C:2, recolor B:4)=6; (swap A+C, swap B+C): conflict on C → invalid. Path min=6. Answer=9-4=5. Check: actual best pair: A,B: max(5,4,0)=5; A,C: max(5,0,3)=5; B,C: max(0,4,3)=4. Best=5 ✓ (direct fix: recolor B Y->X cost 4 → selection A(X),B(X) sum=5+0=5, pair price max(5,4,0)=5 ✓).

30. **Confidence**: The math is sound. Main risk is implementation bugs in the candidate enumeration. Keep it organized.

    Alternative simpler implementation to reduce bug risk: instead of top-2 lists and compatibility logic, note we could also just try, for the path, ALL combinations of "representative" moves but that's what we're doing. Another even simpler but still exact alternative: since moves are cheap, gather for edge(p,r) the list of candidate moves with full resource info but truncated smartly; I'll implement with per-type top-2 as planned.

    Actually, let me simplify further: instead of top-2 per type with ids, I can build candidate move lists as follows and keep them small:
    For edge flip (u,v), candidate moves:
      - recolor u->v: best two (cost, sel_id)
      - recolor v->u: best two (cost, sel_id)
      - swap rem u / add v: best two rem-u (M, sel_id) × best two add-v (val, unsel_id) → 4 (cost, sel_id, unsel_id)
      - swap rem v / add u: 4
    Total ≤ 12 per edge. For direct: min over the ≤12. For path: 12×12=144 pairs, check compatibility: (m1.sel_id != m2.sel_id) and (m1.unsel_id != m2.unsel_id), where missing = -1 (but use unique sentinel: sel ids and unsel ids are cake indices; a move could have sel_id=-1? No—every move has a sel resource? recolor has sel; swap has sel and unsel. So sel_id always present; unsel_id = -1 if none. Compatibility: sel conflict only if m1.sel_color == m2.sel_color and ids equal — since sel colors possible: m1 sel in {p,r}, m2 sel in {r,q}; just compare ids directly: if m1.sel_id == m2.sel_id → conflict (ids unique across colors anyway). And unsel: if both != -1 and equal → conflict. Simple!)
    
    Wait, one more: m1 swap rem p add r uses unsel j; m2 swap rem r add q uses unsel j' — checked. m1 swap rem p add r (unsel j) and m2 recolor r->q (sel b) — no unsel in m2, fine. Also m1 sel = p-cake a; m2 sel = r-cake b; ids differ always. Good: just compare ids.

31. **Edge case: K such that 2K=N** → add lists empty → swap moves absent → direct = min recolor; path = recolor combos. Works.

32. **Also confirm reading input format**: T then per case "N K" then N lines. Output T lines.

33. **Large answer**: up to K * 2e9 ~ 1e5*2e9=2e14 fits in Python int anyway.

Now write the code.

Implementation details:
- coords: store xs, ys, zs lists; M list; g list (0,1,2 with priority to first max — tie-breaking arbitrary).
- order = sorted indices by M desc; selected flag array; first 2K selected.
- counts per g.
- odd colors list.
- If len(odd)==0: ans=base.
- Else p,q = odd; r = 3-p-q... colors are 0,1,2 so r = 3-p-q? 0+1+2=3, yes r=3-p-q.
- Build:
  rem2[c]: list of up to 2 (M_i, i) smallest M among selected with g_i==c. Use heapq.nsmallest or just collect and sort — O(N) collect per color fine; simpler: iterate selected once, append to lists per color, then nsmallest(2).
  Actually simpler: since we iterate all selected for multiple structures, do one pass:
    For each selected i: 
      append (M_i, i) to remlist[g_i]
      for v != g_i: append (M_i - coord_i(v), i) to reclist[(g_i, v)]
    For each unselected j:
      for v in 0..2: append (coord_j(v), j) to addlist[v]
    Then top2 via heapq.nsmallest(2) / nlargest(2). Sizes O(N); fine.
- coord_i(v): use tuple arrays: val[i][v] store as three lists or list of triples. Store triples in arrays X,Y,Z and a helper getc(i,v).
- Build edge moves function edge_moves(u,v):
    moves = []  # each (cost, sel_id, unsel_id)
    for (cost,i) in rec2[(u,v)]: moves.append((cost,i,-1))
    for (cost,i) in rec2[(v,u)]: moves.append((cost,i,-1))
    for (Mi,i) in rem2[u]: for (val,j) in add2[v]: moves.append((Mi-val, i, j))
    for (Mi,i) in rem2[v]: for (val,j) in add2[u]: moves.append((Mi-val, i, j))
    return moves
- direct = min cost in edge_moves(p,q) (must be nonempty: recolor always available since p,q have >=1 selected each).
- path = inf; for m1 in edge_moves(p,r): for m2 in edge_moves(r,q): if m1[1]!=m2[1] and (m1[2]==-1 or m2[2]==-1 or m1[2]!=m2[2]): path=min(path,m1[0]+m2[0]).
  Also need m1[1] != m2[1]: sel ids. But also: could m1 sel_id == m2 sel_id happen only for r-cakes; comparing ids handles all.
  Hmm wait, one more conflict: m1 = swap rem p add r with unsel j; m2 = swap rem r add p?? No, m2 is from edge(r,q): adds r or q. m2 = swap rem q add r with unsel j — conflict checked. What about m1 adds r-cake j and m2 removes... m2 removals are selected r or q cakes — j is unselected, no clash. Good.
- ans = base - min(direct, path).
- Print ans.

Double-check direct edge must exist: recolor p->q needs selected p-cake: count p odd >= 1 ✓.

Also path might be infeasible (inf) — e.g., 2K=N and r count 0: edge(p,r) moves: recolor p->r ✓ exists; edge(r,q): recolor r->q needs r-cakes (none), recolor q->r ✓ exists (q-cakes), swaps none. So path = recolor p->r + recolor q->r: counts: p-1, q-1, r+2 → all even ✓ feasible! Good, path exists. If N=2K and... always some recolor combo exists. Fine, min(direct,path) finite.

Let me also double check the recolor top-2 truncation sufficiency once more for path: m1 recolor p->r top-2 by cost among p-cakes; m2 recolor r->q top-2 among r-cakes; conflict only if same id — impossible (different colors). So for recolor-recolor across the two edges: conflicts only when both are r-recolors (r->p in edge pr, r->q in edge rq): top-2 each, if best ids clash, second-best available — but what if best of both clash and second-best of one is much worse — we take min of compatible among 2x2 — correct optimum? The true min compatible pair: if global best pair (b1,b2) clash (same id), next best compatible is min(b1_second + b2_best, b1_best + b2_second, b1_second+b2_second...) — min over compatible pairs of sum where each from sorted lists; with lists sorted, min compatible pair is among (1st,2nd) and (2nd,1st) — both in 2x2. ✓. For swap moves 4 candidates each from rem2×add2: similar argument: conflicting resource is single id from the other move; the min compatible combo is captured within top-2×top-2? Suppose true optimal m1 swap uses rem-u 3rd best because best two rem-u ids both conflict with m2? m2 has only ONE sel id, so at most one rem-u id conflicts. Top-2 rem-u ensures a non-conflicting one with cost <= 3rd. Similarly add side: m2 has one unsel id. So top-2 suffices. But also m1's swap candidates pair rem×add: we need the min-cost compatible (rem,add) combo for m1 given m2's ids: with rem2 (2 options) and add2 (2 options), at most 1 rem blocked and 1 add blocked → (rem2nd, add2nd) available; min compatible within 2x2 found. Could a cheaper compatible combo use rem1st with add2nd — yes it's in 2x2. ✓.

One more subtle thing: rem2[c] top-2 by M — for swap removal we want min M_i; but note the removed cake's contribution is M_i (its argmax value) — yes since it was colored g_i=c, contributing M_i. ✓. And recolor cost M_i - coord_i(v) ✓.

Also for add2[v]: max coord_j(v) over unselected j — the added cake colored v contributes coord_j(v) ✓.

Now, is there any scenario where the optimal fix is a swap where removed cake's color u is NOT one of p,q,r pattern... covered: direct edge pq swaps remove p or q; path swaps involve p,r,q. All covered by edge candidate generation.

I think the solution is solid. Let me also run through a quick mental test where path beats direct: earlier constructed: recolor p->r cost1, recolor r->q cost1, direct p->q cost100. E.g., cakes: selected: A (p): M=10, coord r=9, coord q=0 → recolor p->r cost1, p->q cost10... make direct 100: coord q such that M-coord_q=100 → M=100, coord_r=99 (cost1), coord_q=0 (cost100). B (r): M=100, coord_p=0, coord_q=99 → r->q cost1, r->p cost100. C (q): whatever. Counts: p=1(A), r=1(B), q=1(C)?? Then odd colors = p,r,q = 3 odds — impossible (sum 3 odd). Need even total: add D (q): M small. Say D (q): M=1. 2K=4, counts p=1,r=1,q=2 → odd={p,r}! Not our scenario. Let me redo: want odd={p,q}: counts p=1,q=1,r=2: cakes A(p), C(q), B1(r),B2(r). Path p-r-q: recolor p->r (A, cost1) + recolor r->q (B1, cost1) = 2; direct recolor p->q = 100, recolor q->p: C: M_C - coord_C(p) say 100. So answer = base-2. Feasible check: after moves: A→r, B1→q: counts p=0,q=2,r=2 ✓. Sum = base-2. Could there be a better pairing-based solution? Trust the proof.

Also verify no off-by-one: 2K selected, K pairs.

Now, code it up with fast IO (sys.stdin.buffer.read, split).

Per test case:
```
def solve_case(N,K,X,Y,Z):
    M=[0]*N; g=[0]*N
    for i in range(N):
        x,y,z=X[i],Y[i],Z[i]
        if x>=y and x>=z: M[i]=x; g[i]=0
        elif y>=z: M[i]=y; g[i]=1
        else: M[i]=z; g[i]=2
    order=sorted(range(N), key=lambda i:-M[i])
    sel=[False]*N
    base=0
    for t in range(2*K):
        i=order[t]; sel[i]=True; base+=M[i]
    cnt=[0,0,0]
    for i in range(N):
        if sel[i]: cnt[g[i]]+=1
    odd=[c for c in range(3) if cnt[c]%2==1]
    if not odd: return base
    p,q=odd; r=3-p-q
    def coord(i,v):
        return X[i] if v==0 else (Y[i] if v==1 else Z[i])
    # build top2 structures
    rem2=[[],[],[]]
    rec2={}  # (u,v) -> list
    add2=[[],[],[]]
    for i in range(N):
        if sel[i]:
            u=g[i]; mi=M[i]
            rem2[u].append((mi,i))
            for v in range(3):
                if v!=u:
                    rec2.setdefault((u,v),[]).append((mi-coord(i,v), i))
        else:
            for v in range(3):
                add2[v].append((coord(i,v), i))
    import heapq
    for c in range(3):
        rem2[c]=heapq.nsmallest(2, rem2[c])
        add2[c]=heapq.nlargest(2, add2[c])
    for key in rec2:
        rec2[key]=heapq.nsmallest(2, rec2[key])
    def edge_moves(u,v):
        mv=[]
        for cost,i in rec2.get((u,v),[]): mv.append((cost,i,-1))
        for cost,i in rec2.get((v,u),[]): mv.append((cost,i,-1))
        for mi,i in rem2[u]:
            for val,j in add2[v]: mv.append((mi-val,i,j))
        for mi,i in rem2[v]:
            for val,j in add2[u]: mv.append((mi-val,i,j))
        return mv
    direct=min(m[0] for m in edge_moves(p,q))
    INF=float('inf')
    path=INF
    E1=edge_moves(p,r); E2=edge_moves(r,q)
    for c1,s1,a1 in E1:
        for c2,s2,a2 in E2:
            if s1!=s2 and (a1==-1 or a2==-1 or a1!=a2):
                if c1+c2<path: path=c1+c2
    return base-min(direct,path)
```
Wait: rec2 lists could be large before nsmallest — total size O(N) across keys, fine.

Note: edge_moves(u,v) includes recolor u->v AND v->u — both flip {u,v} ✓.

Potential issue: direct edge moves include swaps needing add2 nonempty; if empty, those moves absent; recolors remain ✓.

Also note: for the path, E1 might contain a move and E2 the same physical... e.g., recolor r->p appears in edge(p,r) ✓; recolor r->q in edge(r,q) ✓. Distinct.

One more check — the swap move "remove u-cake i, add j as v": after this, counts: u-1, v+1 → flips u,v ✓.

Also should double check the possibility that the optimal solution's difference from G includes a swap where the added cake j is colored v but j is actually in G too?? No—O\G and G\O disjoint by definition.

And what about ties where an unselected cake has M equal to selected but our G choice leads to odd parities while another top-2K choice (same base) is even — covered by zero-cost swap? Swap cost = M_i - coord_j(v) where M_i = boundary, coord_j(v) <= M_j = boundary; zero cost requires coord_j(v) = boundary = M_j, i.e., j's argmax color is v and we remove a u-cake with M=boundary. If the alternative selection that fixes parity swaps a u-cake out for a v-argmax cake — yes cost 0 found. ✓

Edge: N=2, K=1: 2K=2=N. Both selected. If colors same → even → base. If different → odd p,q; direct recolor = min(M_0 - coord_0(g1), M_1 - coord_1(g0)); answer = base - that = max over same-color assignments = pair price = max(X0+X1, Y0+Y1, Z0+Z1) ✓. Path via r: recolor p->r + recolor r->q?? needs r-cake — none; recolor q->r + recolor r->p — none; swaps none. So path=inf... wait E1=edge(p,r): recolor p->r exists (p-cake), recolor r->p none, swaps none → E1 nonempty. E2=edge(r,q): recolor q->r exists. path = recolor p->r + recolor q->r: counts p-1,q-1,r+2: p=0,q=0,r=2 ✓ feasible! cost = (M0 - coord0(r)) + (M1 - coord1(r)). That's a valid alternative (both colored r). min(direct, path) = correct best. ✓

Great.

Performance: sorting O(N log N); scans O(N); heapq on lists total O(N). Fine.

Now also double-check sample 1 with code logic — did above, got 12 ✓.

Let me also test a random small case mentally against brute force... I'll trust the proof but let me do one more: N=5, K=2, 2K=4.
Cakes:
1: X=10,Y=0,Z=0 → M=10,g=X
2: X=9,Y=8,Z=0 → M=9,g=X
3: X=0,Y=7,Z=6 → M=7,g=Y
4: X=0,Y=5,Z=5 → M=5,g=Y (tie Y,Z; pick Y since y>=z)
5: X=1,Y=0,Z=0 → M=1,g=X unselected
Top4: 1,2,3,4. counts X=2,Y=2 → even! base=31. Answer 31? Check pairings: pair within colors: X-pair (1,2): price max(19,8,0)=19; Y-pair (3,4): max(0,12,11)=12; total 31 ✓. Any better? Total max possible = sum of top-4 M =31 is absolute upper bound (each cake contributes <= M... wait each pair price = max over colors of sum <= sum of maxes of the two cakes? max(Xa+Xb,...) <= max(Xa+Xb, ...) hmm price <= M_a + M_b? X_a+X_b <= M_a+M_b etc., so price <= M_a+M_b. Total <= sum of selected M <= top-2K M sum = 31. ✓ achieved.)

Another: force parity fix:
1: (10,9,0) M=10 X
2: (10,9,0) M=10 X
3: (0,9,10) M=10 Z
4: (0,9,10) M=10 Z
5: (0,0,0) M=0 X
N=5,K=2,2K=4: select 1-4: counts X=2,Z=2 even → base=40. Pair X: (1,2) price max(20,18,0)=20; pair Z: (3,4) price max(0,18,20)=20; total 40 ✓.

Parity-odd example:
1: (10,0,0) M=10 X
2: (9,0,0) M=9 X
3: (0,8,0) M=8 Y
4: (0,0,7) M=7 Z
5: (6,6,0) M=6 X (unselected)
N=5,K=2: select 1,2,3,4: counts X=2,Y=1,Z=1 → odd={Y,Z}, r=X. base=34.
Direct YZ: recolor Y->Z: cake3: 8-0=8; recolor Z->Y: cake4: 7-0=7; swap rem Y add Z: minM_Y=8 - max Z unsel (cake5:0)=8; swap rem Z add Y: 7 - max Y unsel (6)=1. direct=1 (remove cake4(Z), add cake5 as Y). → 33.
Path via X: edge(Y,X): recolor Y->X: cake3: 8-0=8; recolor X->Y: min over X-cakes (M-Y): cake1:10, cake2:9 → 9 (cake2); swap rem Y add X: 8 - max X unsel(6)=2 (cake3 out, cake5 in as X); swap rem X add Y: minM_X=9 (cake2) - max Y unsel(6)=3.
 edge(X,Z): recolor X->Z: min(10-0,9-0)=9 (cake2... cake1:10,cake2:9); recolor Z->X: cake4: 7-0=7; swap rem X add Z: 9 - max Z unsel(0)=9; swap rem Z add X: 7 - 6=1 (cake4 out, cake5 as X).
Path combos: best compatible: m1=swap rem Y add X (cost2, sel=3, unsel=5); m2=swap rem Z add X (cost1, sel=4, unsel=5) → conflict unsel 5! Next: m1 cost2 (sel3,u5) + m2 recolor Z->X cost7 (sel4) = 9; m1 recolor Y->X 8 + m2 swap rem Z add X 1 = 9; m1 swap rem X add Y (cost3, sel2, u5) + m2 swap rem Z add X (cost1, sel4, u5) conflict u5; (3, sel2,u5)+(recolor Z->X 7, sel4)=10; m1 swap rem Y add X (2, sel3, u5) + m2 swap rem X add Z (9, sel2, u? add2[Z]: cake5 Z=0 → (0,5); cost 9-0=9, sel=2, unsel=5) conflict. Hmm many conflicts on cake5 (only unselected). Best path = 9? e.g., m1=swap rem Y(cake3) add X(cake5): cost2; m2=recolor Z->X on cake4: cost7 → total 9. Or m1=recolor Y->X cake3 cost8, m2=swap rem Z(cake4) add X(cake5) cost1 → 9. So answer = base - min(1, 9) = 33.
Brute check: selection after direct fix: cakes {1,2,3,5} colors X,X,Y,Y: sum=10+9+8+6=33. Pairing: X-pair (1,2): max(19,0,0)=19; Y-pair (3,5): max(6,14,0)=14; total 33. Can we do better? Upper bound 34 (base) infeasible due parity... other selections: {1,2,3,4} alternative colorings: need even: options: recolor cheapest: cake4 Z->Y (7→0) loss7: sum 27; cake3 Y->Z loss8; cakes {1,2,3,4} as X,X,Y,Y? cake4 as Y: 0. loss 7. Or X,X,Z,Z: cake3 as Z: 0 loss 8. So {1,2,3,4} best feasible = 34-7=27. {1,2,3,5}: colorings: cake5 X: counts X=3,Y=1 → odd X,Y; fix: recolor cake5 X->Y: 6→6 loss0! counts X=2,Y=2: sum=10+9+8+6=33 ✓ (this is what we found). {1,2,4,5}: X,X,Z,X → X=3,Z=1 odd; fix recolor cake5 X->Z: 6-0=6 loss; or cake2 X->Z: 9; best recolor cake5→Z loss6: sum=10+9+7+0=26; or recolor cake5 X->? to make even: X=3,Z=1: odd={X,Z}: recolor X->Z: cake5:6-0=6, cake2:9,cake1:10 → 6; recolor Z->X: cake4: 7-0=7; so 34-... base for this set=10+9+7+6=32-6=26. {1,3,4,5}: 10+8+7+6=31: colors X,Y,Z,X → X=2,Y=1,Z=1 odd Y,Z: fix: recolor cake4 Z->Y: 7; cake3 Y->Z: 8; recolor... also cake5 is X. min 7 → 24. {2,3,4,5}: 9+8+7+6=30: X,Y,Z,X: same → fix 7 → 23. So max=33 ✓. Our answer 33 ✓.

Great, algorithm works on this case including conflict handling (direct won anyway).

Test conflict-heavy: make direct expensive and path with conflict:
Modify: cake5: (6,0,0) M=6 X (no Y). Then direct: swap rem Z add Y: max Y unsel = 0 → 7; recolor Z->Y: 7; recolor Y->Z: 8; swap rem Y add Z: 8. direct=7. Path: edge(Y,X): recolor Y->X: 8; recolor X->Y: 9 (cake2); swap rem Y add X: 8-6=2 (sel3,u5); swap rem X add Y: 9-0=9. edge(X,Z): recolor X->Z: 9; recolor Z->X: 7; swap rem X add Z: 9-0=9; swap rem Z add X: 7-6=1 (sel4,u5). Path: (2,u5)+(1,u5) conflict; (2, sel3,u5)+(recolor Z->X 7, sel4)=9; (recolor Y->X 8)+(swap rem Z add X 1, u5)=9; (swap rem X add Y 9, sel2,u? add2[Y] empty now → swap rem X add Y needs add2[Y]: empty, absent); so path=9. Answer=34-7=27. Brute: {1,2,3,4} best feasible coloring: even colorings: X,X,Y,Y: cake4 as Y=0: sum=10+9+8+0=27; X,X,Z,Z: cake3 as Z=0: 27; X,Y,... cake2 as Y=0? counts X=1,... need even: many options; best 27. {1,2,3,5}: X,X,Y,X → odd X(3),Y(1): fix recolor X->Y: cake5: 6-0=6, cake2: 9-0=9, cake1:10; or recolor Y->X: cake3: 8-0=8; min 6 → sum 31-6=25. {1,2,4,5}: X,X,Z,X: odd X,Z: recolor X->Z: cake5:6, cake2:9; recolor Z->X: cake4:7; min6 → 32-6=26. {1,3,4,5}: X,Y,Z,X: odd Y,Z: recolor Z->Y: 7, Y->Z: 8 → 31-7=24. So answer 27 ✓ matches.

Now a case where path (2 moves) beats direct: need direct recolors/swaps all expensive but two cheap moves via r. 
Cakes selected: A(p): M=100, coord_r=99, coord_q=0. B(r1): M=100, coord_p=0, coord_q=99. C(q): M=100, coord_p=0, coord_r=0... wait C(q) recolor q->p cost 100, q->r cost 100. D(r2): M=1 (to make r count 2). 2K=4: counts p=1,r=2,q=1 → odd={p,q} ✓. Unselected: none useful (say E: M=0 all coords 0).
base=301.
Direct pq: recolor p->q: 100; recolor q->p: 100; swaps: rem p add q: 100 - 0(E's q)=100; rem q add p: 100. direct=100.
Path via r: edge(p,r): recolor p->r: 1 (A); recolor r->p: min(B:100, D: M=1 - coord_p(D)=0 → 1) =1 (D); swap rem p add r: 100-0=100; swap rem r add p: min M_r =1 (D) - 0 =1.
 edge(r,q): recolor r->q: min(B:1, D: 1-0=1)=1; recolor q->r: 100; swap rem r add q: 1-0=1 (D out, E as q); swap rem q add r: 100.
Path best: recolor p->r (A, cost1) + recolor r->q (B, cost1) = 2, compatible (sel A vs sel B) ✓. Answer = 301-2=299.
Verify: coloring: A→r, B→q, C→q, D→r: counts r=2,q=2 ✓. Sum = 99+99+100+1=299. Alternative: A→r, D→? D is r already... Another feasible: A(p→r), and swap D out E in as q? 99+100(B as r? no B must... whatever, trust. Could any solution beat 299? Upper bound base=301; parity forces >=1 loss; single move min loss: direct min 100; but two-move loss 2. Any one-move... no. 299 likely optimal. Brute-ish: selections including E(M=0): replace D: {A,B,C,E}: colors p,r,q,X?E M=0 g=X(say): counts p=1,r=1,q=1,X=1 → 3 odd?? sum=4 even; counts: p=1,r=1,q=1,X=1: four odd counts — impossible? 1+1+1+1=4 even, but number of odd counts = 4? There are only 3 colors! p,r,q are 0,1,2 — E's g must be one of them. E: all coords 0, g=X=0. If p=X... let me set p=X(0), q=Y(1), r=Z(2). Then E g=X=p. counts: p=2(A,E), r=1(B), q=1(C) → odd={r,q}. Different odd pair! Our algorithm selects top-4 = A,B,C,D (M: 100,100,100,1) not E. OK. The fix stands. Other selections: {A,B,C,E}: base=300, odd={r,q}: direct rq: recolor r->q: B:1; → 299. Same. {A,B,D,E}: 201... lower. So 299 optimal ✓. And our algorithm's path found 2. 

The algorithm handles everything. Now also make sure about reading input and writing output efficiently.

Also note: the problem says "Enclose your code within delimiters" — but my role here is FIRST WORKER: only produce NOTES and NEXT. Right! I must NOT solve; just analysis and next steps. The instructions say respond with exactly ### NOTES ... ### NEXT .... So I should condense the above into notes and a next plan.

## worker: Write the full Python solution implementing the se
- **Reduction**: A pair assigned color c contributes the c-coordinate sum; since the true price is the max over colors, the answer equals: choose 2K cakes, 3-color them with **even** per-color counts, maximize sum of each cake's chosen coordinate. (Pairing within a color group is irrelevant; both directions of the inequality hold — optimal pairing induces a valid even coloring via per-pair argmax, and any even coloring yields a pairing whose actual price is ≥ the colored sum.)
- **Unconstrained optimum**: pick each cake's best coordinate M_i, take top 2K by M_i (sum = base). Color counts have either 0 odd colors (done, answer = base) or exactly 2 odd colors p, q (number of odd counts is even since total 2K is even; 3 odds impossible).
- **Parity fix = min T-join on 3 nodes**: any feasible solution differs from the greedy one by recolors (flip 2 parities, cost M_i − coord_i(v) ≥ 0) and swaps (remove selected u-cake i, add unselected j colored v, cost M_i − coord_j(v) ≥ 0 since M_j ≤ min selected M). Each move's cost ≥ the min cost for its edge type, and the parity flips form a T-join for {p,q}, which on 3 nodes is min(edge pq, edge pr + edge rq). Conversely applying the min compatible move(s) to the greedy set achieves it, so the answer is base − min(direct, path).
- **Conflict handling**: the two path moves can conflict only by sharing a selected r-cake or the same unselected cake. Keeping top-2 candidates per resource (removal per color by min M, recolor per ordered pair by min loss, addition per color by max coordinate) suffices, since the other move blocks at most one id of each resource kind. Compatibility check: distinct sel ids and distinct unsel ids.
- Verified against both samples by hand (12, 209, 333) and several custom cases including tie-at-boundary, 2K = N (no swaps), and path-beats-direct scenarios.
- Complexity: O(N log N) per test case, O(N) memory; sum of N ≤ 1e5. Python ints handle values up to ~2e14.

## worker: Validate the implementation against the derivation
I validated the implementation against the derivation and all the targeted edge cases.

**Validation of the reduction and algorithm (from the plan, confirmed correct):**
- The pair price `max(X_a+X_b, Y_a+Y_b, Z_a+Z_b)` means the answer equals: choose 2K cakes, 3-color them with **even** per-color counts, maximize the sum of each cake's chosen coordinate. Pairing within a color group is irrelevant (both inequality directions hold: an optimal pairing induces a valid even coloring via per-pair argmax; any even coloring gives a pairing whose actual price ≥ the colored sum).
- Unconstrained optimum: take top-2K by `M_i = max(X_i,Y_i,Z_i)` (sum = `base`), colored by argmax. The number of odd-count colors is even (total 2K is even), so it's 0 (done) or exactly 2 odd colors `p, q`.
- Any feasible solution differs from the greedy one by recolors (flip 2 parities, cost `M_i − coord_i(v) ≥ 0`) and swaps (remove selected u-cake i, add unselected j colored v, cost `M_i − coord_j(v) ≥ 0` since `M_j ≤ min selected M`). The parity flips form a T-join for `{p,q}`, which on 3 nodes is `min(edge pq, edge pr + edge rq)`. Applying the min compatible move(s) achieves it, so answer = `base − min(direct, path)`.
- Conflict handling: the two path moves can only conflict by sharing a selected r-cake or the same unselected cake. Top-2 per resource suffices because the other move blocks at most one id of each resource kind.

**Hand-run of samples:**
- Sample 1: select cakes 1 (M=8,Z) and 3 (M=7,Y), base=15, odd={Z,Y}, r=X. Direct: swap out Z (cake1, M=8), add cake2 as Y (coord 5) → cost 3. Path via X = 6. Answer = 15−3 = **12** ✓.
- Sample 2 case 1: top-4 = cake5 (200,Z) + three (3,Z) cakes, counts Z=4 all even → **209** ✓.
- Sample 2 case 2: top-4 = cakes 3(96,Z),5(83,Y),2(80,Z),1(74,Y), counts Z=2,Y=2 even → **333** ✓.

**Targeted edge cases (all hand-verified):**
- **2K = N** (no unselected): `add2` lists are empty so swap moves are simply absent; recolor moves always exist for the odd colors (count ≥ 1), so `direct` is always finite. E.g., N=2, K=1 with different argmax colors: direct = min recolor, path = recolor p→r + recolor q→r (both exist, r+2 stays even); min gives exactly the pair price. ✓
- **K = 1**: works; verified with a 3-cake case where the answer 5 came from a recolor fix. ✓
- **Ties at selection boundary**: an unselected cake with `M_j` equal to the boundary value yields a zero-cost swap (`M_i − coord_j(v) = 0` when `coord_j(v) = M_j`), found because swap moves scan all unselected cakes and `rem2` takes min selected M. ✓
- **Tied argmax coordinates**: recolor cost `M_i − coord_i(v) = 0` for the tied coordinate, so zero-cost recolor fixes are found. ✓
- **Path-beats-direct with add-add conflict on the only unselected cake**: constructed a case where the two cheapest path moves both add the same unselected cake (conflict, correctly rejected by `a1 != a2` check), and the next-best compatible pair (cost 9) was correctly chosen over the conflicting pair (cost 3). Direct (cost 1 in one variant, 7 in another) was correctly compared. Answers matched brute-force enumeration over all selections/colorings. ✓

**Bug check on the code:** The `coord` helper closure was inlined into direct `X/Y/Z` accesses in the scan loop (no stale reference). `r = 3 - p - q` is correct since colors are 0,1,2. Compatibility check `s1 != s2` (distinct selected cakes — ids are globally unique so color comparison is subsumed) and `a1 == -1 or a2 == -1 or a1 != a2` (distinct unselected) is exactly right. `min(direct, path)` is always finite (direct recolor always available). Values up to ~2e14 fit Python ints. Complexity O(N log N) per test, sum N ≤ 1e5 — fast enough.

No bugs found; the implementation is correct as written.
