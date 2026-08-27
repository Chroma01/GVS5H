- **Gap transformation:** For four consecutive sorted coordinates \(a<b<c<d\), the operation reflects \(b\) and \(c\) around \((a+d)/2\), producing \(a,\ a+d-c,\ a+d-b,\ d\). Therefore the three gaps \((b-a,c-b,d-c)\) become \((d-c,c-b,b-a)\), i.e. they are reversed.
- **Parity preservation:** Reversing three consecutive gaps swaps the first and third gaps while leaving the middle gap unchanged. Thus an operation swaps \(g_i\) and \(g_{i+2}\), so odd-indexed gaps never mix with even-indexed gaps.
- **Reachability:** Any two adjacent gaps within the odd-indexed subsequence have indices differing by 2 and can be swapped by choosing the corresponding operation. The same holds for the even-indexed subsequence. Since adjacent transpositions generate all permutations, each parity class can be permuted arbitrarily and independently.
- **Objective:** The leftmost coordinate never changes. If the final gaps are \(g_1,\ldots,g_{N-1}\), the coordinate sum is
  \[
  N X_1+\sum_{i=1}^{N-1}(N-i)g_i.
  \]
  Gap \(g_i\) has weight \(N-i\).
- **Optimal assignment:** Within each parity class, assign the smallest gaps to the largest weights by the rearrangement inequality. Sort each class’s gaps increasingly and its corresponding weights decreasingly, then take the dot product.
- **Complexity:** Constructing the gaps takes \(O(N)\), and sorting the two parity classes takes \(O(N\log N)\) time. Memory usage is \(O(N)\).
