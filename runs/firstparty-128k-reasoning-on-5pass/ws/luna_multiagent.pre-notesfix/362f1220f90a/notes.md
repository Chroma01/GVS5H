
## ideation
The core difficulty is handling overlapping windows: every `T` window forces all of its characters, while every `F` window must contain at least one mismatch with `str2`. Forced `T` windows can conflict directly, and an `F` window can become impossible only after assignments from several overlapping windows. Lexicographic minimization also requires proving that each chosen character still permits a completion; choosing the smallest currently available character is not sufficient without a feasibility mechanism.

## worker: Develop and implement the KMP finite-state dynamic
The KMP state records the longest suffix of the current prefix that is also a prefix of `str2`. A window equals `str2` exactly when the previous state is `m-1` and the next character is `str2[-1]`.

Backward feasibility is stored as bitsets of KMP states. For an `F` constraint, the matching transition is excluded; for a `T` constraint, only the unique matching transition is allowed. Reconstruction greedily tries characters from `'a'` to `'z'`, accepting the first one whose resulting state is feasible for the suffix.

The complexity is `O((n + m) * m + 26 * (n + m))`, with `O((n + m) * m)` bitset storage in the worst case.

## worker: Exhaustively test the KMP bitset DP against brute 
The KMP state correctly identifies whether the newly completed window equals `str2`: this happens exactly when the previous state is `m - 1` and the appended character is the last character of `str2`.

The backward bitset DP was checked against brute-force enumeration for small values, including `m = 1`, overlapping matches, conflicting `T` constraints, all-`T`, and all-`F` patterns. The transition and reconstruction logic handle `m = 1` correctly as well.

Time complexity is `O((n + m) * m + 26 * (n + m))`, with `O((n + m) * m)` bitset storage.
