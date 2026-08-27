- **Unrestricted path count:** The number of paths ending at \((x,y)\), with arbitrary starting block and only positive-axis moves, is \(F(x,y)=\binom{x+y+2}{x+1}-1\).
- **Prefix sum:** \(Q(a,b)=\sum_{x\le a,y\le b}F(x,y)\), with
  \(Q(a,b)=\binom{a+b+4}{a+2}-(a+3)-(a+2)(b+1)\), and zero if either argument is negative.
- **Allowed endpoints:** Begin with \(Q(W,H)\), then subtract the unrestricted paths whose endpoint lies in the forbidden rectangle using two-dimensional inclusion-exclusion.
- **First forbidden vertex after an allowed prefix:** It must be on the bottom side or left side. Bottom-side prefix counts are \(F(x,D-1)\), with the additional \(F(L-1,D)\) at the bottom-left corner. Left-side counts for \(y>D\) are \(F(L-1,y)\).
- **Continuation count:** From a forbidden vertex, allowed endpoints are either strictly right of the rectangle or strictly above it. If \(T(a,b)=\sum_{0\le i\le a,0\le j\le b}\binom{i+j}{i}=\binom{a+b+2}{a+1}-1\), continuation counts follow by inclusion-exclusion.
- **Forbidden starting blocks:** A path may start inside the forbidden rectangle, so its zero-length prefix must also be counted. Summing continuation counts over every forbidden starting vertex is done with rectangular sums of \(T\). Since \(Q\) is the double prefix sum of \(T\), this takes constant time after factorial preprocessing and automatically includes one zero-length prefix for every boundary or interior forbidden vertex.
- **Complexity:** Factorial preprocessing is \(O(W+H)\) time and memory. Boundary loops take \(O((R-L+1)+(U-D))\) time. All operations are modulo \(998244353\).
- **Degenerate rectangles:** Width-zero and height-zero cases are handled by the same formulas and negative-index helpers.
