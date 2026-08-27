
## ideation
The core difficulty is that the LCS value depends on the entire interaction between the processed prefix of the unknown string and all prefixes of \(S\), so counting strings by LCS length cannot be done using only the current length or the last character. The useful fact is that \(N\le 10\): an LCS DP row has adjacent differences only in \(\{0,1\}\), so its relevant information can be compressed into at most \(2^N\) states. Every appended character induces a deterministic transition between such states and increases the final LCS by either zero or one. Letter multiplicities must be aggregated carefully, since different lowercase letters can induce the same transition.

Important pitfalls include using the correct initial row, distinguishing the updated row from its final component, handling repeated letters in \(S\), and counting all 26 choices with multiplicity rather than merely counting distinct transitions. The total counts should be reduced modulo \(998244353\).

## worker: Derive and implement a correct compact LCS-row aut
The LCS DP row for prefixes of `S` has adjacent differences only in `{0, 1}`. Thus it is represented by an `N`-bit mask, whose popcount equals the current LCS length.

For a character with occurrence mask `A`, the standard bit-parallel LCS update is:
`X = D | A`, `Y = ((D << 1) | 1)`, and `D' = X & ~(X - Y)`, restricted to the lowest `N` bits. The popcount changes by exactly the LCS increment caused by appending that character.

The DP iterates over all `26` letters, so repeated transition results still receive the correct multiplicity. The complexity is `O(M * 26 * 2^N)` and memory usage is `O(26 * 2^N)`.
