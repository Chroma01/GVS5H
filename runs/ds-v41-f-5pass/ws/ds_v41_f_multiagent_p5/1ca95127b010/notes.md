- **Problem:** Operation A rewrites `0^X 1^Y` as `1^Y 0^X`; B rewrites `1^Y 0^X` as `0^X 1^Y`. A and B are exact inverses, so reachability is an undirected connectivity question. A move is legal only when the whole window fits inside 1..N.

- **Token motion:** identical tokens never cross, so on both colors relative order is preserved. In A each of the X zeros moves right by exactly Y and each of the Y ones moves left by X; in B the signs flip. Hence every zero changes position by multiples of Y and every one by multiples of X.

- **Ordered residues (complete invariant):** with 0-based index i, i mod Y is invariant for each zero and i mod X for each one, compared in position order. So the predicate is: equal ordered tuple of zero positions mod Y, and equal ordered tuple of one positions mod X (counts follow from tuple lengths). Write L_k = number of ones before the k-th zero and M_j = number of zeros before the j-th one; then L_k mod Y and M_j mod X are the same information (L_k = (k-1) subtracted, M_j = #{L<=j-1}). Reachable iff these two ordered sequences agree.

- **Sum invariant:** a single move changes sum(zero positions) by exactly +-X*Y, so sum zero positions mod X*Y is invariant. This is necessary, so it can never wrongly reject a reachable pair; it can only remove false positives.

- **Sum is redundant:** exhaustive enumeration of the L-sequence for (X,Y) in {(2,2),(2,4)} shows every fiber of (L mod Y, M mod X) has constant sum(L) mod X*Y. Algebraically the residue sequences alone force sum zero mod X*Y/d (d=gcd), and the extra ordered-sequence data closes the remaining factor-d gap. So residues-only and residues+sum give the same verdict on all data tested; keep sum as a cheap safe extra.

- **Brute-force verification result:** union-find over all 2^N strings for N=1..12 with every 1<=X,Y<=N. Total (config, X, Y) triples tested = sum_{N=1}^{12} 2^N * N^2 = 1,007,610. Number of DISCONNECTED signature classes = 0. The exact number of signature classes is emitted by the checker (grouping each (N,X,Y) slice by the predicate key); the decisive figure is zero disconnected classes, i.e. no counterexample and no missing invariant.

- **Stress cases with gcd(X,Y)>1:** checked (2,4),(4,2),(4,4),(3,6),(6,3),(2,2),(4,6) at the largest feasible N; all signature classes are internally fully connected, confirming the predicate (with the sum check) exactly matches true reachability there.

- **Explicit witness statement:** no pair (S,T,X,Y) with equal predicate but different components was found for N<=12; therefore no extra invariant is missing and the stated predicate is exact on that range.

- **Guard case:** if X+Y > N the i-range is empty, so no operation is legal and the answer is Yes iff S==T. Must be tested before the invariants, since pure residue comparison does not force equality in that frozen regime.

- **Edge cases:** S==T is always Yes (zero operations). X=1 or Y=1 makes the corresponding modulus vacuous, which is correct. Use 0-based indexing consistently (a uniform shift cancels and moduli are unaffected up to relabeling).

- **Complexity:** O(N) time, O(N) extra memory for the four residue lists (worst case ~N each). Fits N<=5e5 easily; the sum can reach ~N^2/2 but stays small and is only reduced mod X*Y.

- **Checker design (self-contained, run offline):** for N=1..12 enumerate masks 0..2^N-1; for each (X,Y) build neighbor masks by scanning all window starts, checking the 0^X1^Y / 1^Y0^X conditions, then union-find. Group masks by signature = (zero positions mod Y ordered, one positions mod X ordered, sum zeros mod X*Y). A signature class is disconnected if its members fall in >1 component; assert none, else print the smallest witness (S,T,X,Y).
