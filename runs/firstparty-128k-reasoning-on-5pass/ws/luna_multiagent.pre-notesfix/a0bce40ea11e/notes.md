
## ideation
The core difficulty is that expanding \(B^p\) produces all length-\(p\) walks, while the same replaced entry may occur many times in one walk. Therefore, the choices for different matrix entries cannot be summed independently at the level of individual steps without tracking occurrence counts.

For a replaced entry \(x\in\{1,\ldots,p-1\}\), its contribution to a monomial is \(\sum_x x^t\), which is \(-1\) when \(t\) is divisible by \(p-1\), and \(0\) otherwise. Since every walk has total length \(p\), for \(p>2\) the total number of traversals of replaced entries can only be \(0\) or \(p-1\). Consequently, at most one replaced entry can occur in a surviving walk, and if it occurs, it occurs exactly \(p-1\) times. This is the main structural simplification.

There is also a global sign from entries that do not occur in the walk: each such variable contributes \(p-1\equiv -1\). Care must be taken not to omit this factor. The case \(p=2\) is exceptional because every allowed replacement equals \(1\), so it should be handled separately.

## worker: Derive and validate the complete closed-form contr
For \(p>2\), expand each entry of \(B^p\) as a sum over length-\(p\) walks.

For every zero entry replaced by \(x\in\{1,\dots,p-1\}\),
\[
\sum_x x^t \equiv
\begin{cases}
-1 & (p-1)\mid t,\\
0 & \text{otherwise}.
\end{cases}
\]
Since the total walk length is \(p\), a surviving walk uses either:

1. No zero entries; this contributes \((-1)^K C^p\), where \(C\) is \(A\) with zeros replaced by \(0\).
2. Exactly one zero entry \(p-1\) times and one fixed entry once; every such term has the common factor \((-1)^K\).

For \(p\ge 5\), the repeated zero edge must be a loop. The single fixed edge must be first or last, producing \(CL+LC\), where \(L\) marks zero diagonal entries.

For \(p=3\), there is one additional possibility: a non-loop zero edge \((u,v)\) used twice, separated by the fixed reverse edge \((v,u)\). This contributes \(C_{v,u}\) to output position \((u,v)\).

The case \(p=2\) is handled separately because every replacement is forced to be \(1\).

Matrix exponentiation costs \(O(N^3\log p)\), and the additional corrections cost \(O(N^2)\).

## worker: Fix the \(p=2\) branch by constructing \(B\) from 
Fixed the `p == 2` branch by constructing `B` explicitly, replacing every zero in `A` with `1`, then computing `B^2 mod 2`. The formula for `p > 2` is unchanged.
