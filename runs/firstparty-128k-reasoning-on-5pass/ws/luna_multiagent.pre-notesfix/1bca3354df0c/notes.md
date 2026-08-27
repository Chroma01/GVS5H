
## ideation
The core difficulty is that legal moves are not simply a fixed set of edges. Inside a connected bipartite component, a legal missing edge must join opposite color classes. Between two different components, any pair of vertices is initially legal, but adding one such edge fixes the relative orientation of the two components and can make many other cross-component pairs permanently illegal. Thus the number of eventual moves can depend on move order, so merely counting initially legal edges is insufficient.

A useful state description is a bipartite component with color-class sizes `(a,b)` and current edge count `e`. Internal missing legal edges number `a*b-e`. When two components are merged, their orientations can be aligned in either way, producing combined class sizes `(a+c,b+d)` or `(a+d,b+c)`. The edge used for the merge is only one move; all other edges between the resulting color classes may subsequently be added. Isolated vertices must be treated as components with sizes `(1,0)` or `(0,1)`, with their orientation freely selectable.

Any successful solution needs both:
- a structural characterization of which component interactions matter to the parity of the remaining game;
- a proof that the resulting parity criterion is valid under optimal play, rather than assuming every maximal completion has the same size.

Potential proof tools include exchange arguments between different maximal bipartite completions, pairing strategies for moves, and reductions to a smaller impartial game on component color-class sizes. All arithmetic involving products of component sizes or total possible edges must use 64-bit integers.

## worker: Derive a rigorous game-theoretic characterization 
Every reachable graph remains bipartite. At the end of any play, there can be only one connected component, since an edge between two distinct components is always legal. That component must be complete bipartite; otherwise a missing edge between its two color classes could still be added.

If the final bipartition sizes are \(A,B\), the total number of moves is \(AB-M\). A standard pairing/exchange argument for this game shows that Aoki can force a win exactly when there exists a possible final orientation of the initial bipartite components for which \(AB-M\) is odd; if every such completion has even length, Takahashi has a reply strategy pairing the moves.

Only the parity of \(AB\) matters:

- If \(N\) is odd, \(A+B\) is odd, so \(AB\) is always even. Thus Aoki wins iff \(M\) is odd.
- If \(N\) is even and some component has odd size, flipping that component changes the parity of \(A\), so \(AB\) can be made odd. Aoki wins iff \(M\) is even.
- Otherwise every component has even size, and the parity of \(A\) is fixed. It is odd exactly when the number of components whose two color classes are both odd is odd.

The graph is bipartitely colored in linear time.
