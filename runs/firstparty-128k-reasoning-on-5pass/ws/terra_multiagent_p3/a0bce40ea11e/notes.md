- **Power-sum rule:** For each originally-zero entry, viewed as an independent variable \(x \in \mathbb F_p^\times\), \(\sum_x x^c\) is \(-1\) when \(c\) is divisible by \(p-1\), and \(0\) otherwise. This also applies to exponent \(c=0\), since \(\sum_x 1=p-1=-1\).
- **Global sign:** In every surviving walk monomial, every one of the \(K\) variables contributes \(-1\), whether absent or used a positive multiple of \(p-1\). Therefore the total answer is \((-1)^K\) times the classified surviving-walk sum.
- **Matrices:** Let \(F\) be the matrix containing original nonzero entries and zero elsewhere. Let \(Z\) be the zero-position indicator. Let \(D=\operatorname{diag}(Z_{1,1},\ldots,Z_{N,N})\).
- **Case \(p=2\):** There is only one nonzero field element, so every zero is replaced by 1. Since original nonzero entries are also necessarily 1, the resulting matrix is the all-ones matrix \(J\). The answer is \(J^2=(N\bmod 2)J\).
- **Case \(p=3\):** A used zero variable must occur exactly twice. There can be only one such variable, leaving one fixed edge. The surviving walk sum before the global sign is:
  \[
  F^3 + DF + FD + (Z \odot F^T).
  \]
  The first two extra terms correspond to the two repeated zero edges being consecutive, forcing that zero edge to be a loop. The Hadamard term corresponds to the pattern zero edge, reverse fixed edge, same zero edge.
- **Case \(p\ge5\):** A used zero variable must occur exactly \(p-1\) times, leaving one fixed edge. If the zero edge were non-loop, at most two copies could occur because the one fixed edge can separate the repeated edge sequence into only two runs. Hence it must be a zero loop. The fixed edge can only be before or after all repeated loops, so the surviving sum is:
  \[
  F^p + DF + FD.
  \]
  The apparent interior placement would require the fixed edge to be a fixed loop at the same position as a zero loop, which is impossible.
- **Complexity:** Matrix exponentiation for \(F^p\) costs \(O(N^3\log p)\), with \(N\le100\). The remaining terms cost \(O(N^2)\).
