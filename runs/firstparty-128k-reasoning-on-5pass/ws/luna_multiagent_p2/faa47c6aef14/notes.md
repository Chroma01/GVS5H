- **Color independence:** Red balls follow the permutation \(P\), while blue balls follow \(Q\). Every occupied box must belong to the same permutation cycle as the target box \(X\); otherwise that ball can never reach \(X\).
- **Required route:** Traverse the target cycle from \(X\). If the earliest occupied position is \(c_j\), every box \(c_j,c_{j+1},\ldots\) through the predecessor of \(X\) must be operated. The required operation order is reverse cycle order, from farthest to nearest to \(X\). Balls initially at \(X\) require no operation.
- **Combining colors:** A global operation sequence must contain the red required route and blue required route as subsequences. Therefore the minimum number of operations is the shortest common supersequence length:
  \[
  |R|+|B|-\operatorname{LCS}(R,B).
  \]
  Repeated operations may be necessary when the two route orders conflict.
- **LCS computation:** Each route contains distinct box indices. Map boxes in the red route to their positions, convert the blue route into positions, and compute the longest strictly increasing subsequence in \(O(N\log N)\).
- **Complexity:** The cycle construction, validation, and LIS computation all take \(O(N\log N)\) time overall and \(O(N)\) memory.
