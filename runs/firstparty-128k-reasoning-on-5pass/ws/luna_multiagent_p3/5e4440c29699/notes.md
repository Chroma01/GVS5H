- **First forbidden point:** Count all unrestricted monotone paths, then subtract paths that visit the forbidden rectangle. Every invalid path has a unique first forbidden point \(p\).
- **Prefix count:** The number of paths from any start point in \([0,x]\times[0,y]\) to \((x,y)\) is
  \[
  T(x,y)=\binom{x+y+2}{y+1}-1.
  \]
- **Suffix count:** The number of paths from \((x,y)\) to any endpoint in \([x,W]\times[y,H]\) is
  \[
  E(x,y)=\binom{W-x+H-y+2}{W-x+1}-1.
  \]
- **First-point prefixes:** For a forbidden point \((x,y)\), the empty prefix contributes one path (the path starts there). Any nonempty valid prefix can enter the rectangle only from below when \(y=D>0\), or from the left when \(x=L>0\). Thus its first-point contribution is
  \[
  1+[y=D,D>0]T(x,D-1)+[x=L,L>0]T(L-1,y).
  \]
- **Invalid paths:** Summing the empty-prefix part gives \(\sum E(x,y)\) over the forbidden rectangle. The two possible entry contributions are handled by linear scans over the bottom and left sides. The corner correctly receives both possible entry contributions.
- **Rectangle sum:** Define
  \[
  P(A,B)=\sum_{0\le x\le A,\;0\le y\le B}E(x,y).
  \]
  By two applications of the hockey-stick identity,
  \[
  P(A,B)=\binom{A+B+4}{B+2}-(B+3)-(A+1)-(A+1)(B+1).
  \]
  Inclusion-exclusion gives the forbidden-rectangle sum in \(O(1)\).
- **Complexity:** Factorials and inverse factorials require \(O(W+H)\) time and memory. The side scans take \(O((R-L+1)+(U-D+1))\), so total complexity is \(O(W+H)\).
