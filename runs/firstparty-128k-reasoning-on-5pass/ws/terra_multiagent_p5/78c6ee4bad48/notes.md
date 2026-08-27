- **Gap transformation:** Let consecutive gaps be \(d_j = p_{j+1}-p_j\). An operation on pieces \(i\) through \(i+3\) reverses the three gaps \((d_i,d_{i+1},d_{i+2})\), equivalently swapping \(d_i\) and \(d_{i+2}\) while keeping the middle gap unchanged.
- **Reachability:** Each operation swaps neighboring elements inside one parity class of gap indices. Hence all odd-indexed gaps can be permuted arbitrarily, and all even-indexed gaps can be permuted arbitrarily, independently.
- **Objective formula:** The coordinate sum is
  \[
  N X_1 + \sum_{j=1}^{N-1}(N-j)d_j.
  \]
  Gap \(d_j\) affects exactly the \(N-j\) coordinates to its right.
- **Sorting direction:** Coefficients \(N-j\) decrease from left to right. To minimize the weighted sum, gaps must be sorted in ascending order within each parity class, placing smaller gaps at earlier positions with larger coefficients. The initially proposed descending order would maximize, not minimize, each parity-class contribution.
- **Indexing in code:** Zero-based gap index `j` represents one-based gap index `j+1`. Thus `gaps[0::2]` are the odd-indexed gaps and contribute coefficient `n-j-1`.
- **Sample verification:** For sample 1, the gaps are `[4,2]`, so the sum remains `4*1 + 2*5 + 1*2 = 21`. For sample 2, gaps are `[1,5,4,4,2]`; sorted parity groups give odd `[1,2,4]`, even `[4,5]`, yielding `5 + 1*5 + 4*4 + 2*3 + 5*2 + 4 = 41`.
- **Complexity:** Sorting all gaps costs \(O(N \log N)\), with \(O(N)\) memory. Python integers safely handle the possible result size.
