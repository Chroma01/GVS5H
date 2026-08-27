- **Exhaustive oracle testing:** The greedy construction was checked against a brute-force lexicographic oracle on small instances: all `T`/`F` masks for short `str1` lengths, short patterns over a small lowercase alphabet, and all candidate output strings over the corresponding relevant alphabet. The greedy output matched the oracle exactly: it returned `""` precisely for infeasible cases and otherwise returned the lexicographically smallest feasible string.

- **Samples:** All provided samples pass: `("TFTF", "ab") -> "ababa"`, `("TFTF", "abc") -> ""`, and `("F", "d") -> "a"`.

- **Forced T placements:** Construct an output of length `n + m - 1`. For each `T` at index `i`, force `ans[i + j] = str2[j]`. If two forced occurrences require different letters at one output position, the instance is impossible.

- **F-window handling:** Initially, every non-forced position is `'a'`. Scan `F` constraints left to right. If its window already differs from `str2`, it is satisfied. If it equals `str2`, select the rightmost currently usable position in that window and set it to `'b'`.

- **Witness validity:** In a currently equal window, every usable position contains its original `'a'`; therefore its aligned `str2` character is also `'a'`. Replacing it by `'b'` breaks that occurrence.

- **Lexicographic minimality:** A matching forbidden window must receive a mismatch at some non-forced position. Choosing the rightmost available position preserves the smallest possible prefix. At that position, `'b'` is the smallest character different from the required `'a'`.

- **Earlier F constraints:** A selected witness becomes `'b'` permanently. It continues to mismatch the earlier F window, so later actions cannot invalidate that earlier constraint.

- **Complexity:** Applying T constraints, checking F windows, and selecting witnesses each take `O(nm)`. With `n <= 10^4` and `m <= 500`, this is at most a few million character operations. Space usage is `O(n + m)`.
