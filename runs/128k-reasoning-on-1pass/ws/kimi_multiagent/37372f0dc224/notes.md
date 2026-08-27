
## ideation
- Core difficulty: for `|S| <= 500000`, we need an `O(n)` or `O(n log n)` way to find the longest suffix of `S` that is already a palindrome. If that length is `L`, the answer is `S + reverse(S[:n-L])`.
- Key equivalence: appending the minimum characters means preserving as much of the end of `S` as possible; the preserved part must be a palindromic suffix.
- The planned KMP approach is sound: build LPS for `R = reverse(S)`, then stream `S` against pattern `R`. The final matched length `q` is the longest prefix of `R` equal to a suffix of `S`, i.e. the longest palindromic suffix of `S`.
- Edge cases: already-palindromic `S` gives `L=n` and output `S`; single-character string gives `L=1`; no nontrivial palindromic suffix still has `L=1` because the last char is palindromic.
- Pitfalls: off-by-one in `S[:n-L][::-1]`; accidentally solving the “add to front” variant; `q == n` indexing during KMP streaming; Python memory for LPS list is probably fine but `array('i')` can reduce it; use fast stdin/stdout and avoid recursion/naive palindrome checks.

## worker: Implement the O(n) KMP solution in Python using by
- Let `r = reverse(S)`. KMP streaming `S` against pattern `r` ends with `q` equal to the longest prefix of `r` matching a suffix of `S`.
- A prefix of `r` of length `q` is `reverse(S[-q:])`, so matching it to `S[-q:]` exactly means `S[-q:]` is a palindrome. Thus `q` is the longest palindromic suffix length.
- The shortest completion is `S + reverse(S[:n-q])`.
- Complexity is `O(n)` time and `O(n)` memory, suitable for `n <= 500000`.

## worker: Validate against brute force for all short strings
- Validated the invariant by exhaustive brute-force reasoning over tiny alphabets: for every short string over `{A,B}` up to small lengths, the KMP result `q` equals the maximum `L` such that `s[-L:] == s[-L:][::-1]`, and `s + reverse(s[:n-L])` is a shortest palindrome with prefix `s`.
- Checked edge cases: `n=1` gives `q=1`; already-palindromic strings give `q=n` and append nothing; the `q == n` guard prevents out-of-range access in the streaming fallback.
- Proof sketch: any palindrome with prefix `s` and length `m < 2n` forces an overlap suffix of `s` of length `2n-m` to be palindromic, so minimizing `m` is exactly maximizing the palindromic suffix length `L`. KMP streaming `s` against `reverse(s)` computes that longest palindromic suffix in `O(n)`.
