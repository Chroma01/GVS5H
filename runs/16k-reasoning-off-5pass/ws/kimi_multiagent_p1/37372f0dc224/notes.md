
## ideation
Core difficulty: n up to 500,000, so we need an O(n) or O(n log n) solution; naive palindrome checking per prefix is O(n²) and too slow.

Key insight: The shortest palindrome having S as a prefix is formed by appending characters to the end of S (any palindrome with S as a prefix must at least contain S, and the shortest such is S plus some suffix). The answer is S + reverse(S[:j]) where S[j:] is the longest palindromic suffix of S. Equivalently, find the longest palindromic suffix of S, then mirror the remaining prefix.

Wait — careful: we want the longest palindromic *suffix* of S (since S stays fixed as prefix, we append the reverse of the part before that suffix). Let S = P + T where T is the longest palindromic suffix; answer = S + reverse(P). Length = 2n − |T|, minimized when |T| is maximized.

Candidate approaches:
1. KMP prefix function on T' = S + '#' + reverse(S): the prefix function's last value gives the longest prefix of S that is a suffix of reverse(S), i.e., the longest palindromic *prefix* of S. That's the wrong direction for this problem (that's for shortest palindrome by *prepending*). For our problem we need the longest palindromic *suffix*: run KMP on reverse(S) + '#' + S; the last prefix-function value = longest prefix of rev(S) matching a suffix of S = longest palindromic suffix of S. Then answer = S + reverse(S[:n−k]).
2. Rolling hash: compare forward and backward hashes to find the longest palindromic suffix in O(n) after O(n) precompute; risk of collisions (use double hashing or mod 2^64).
3. Manacher's algorithm: compute palindrome radii, then find the longest palindrome ending at position n−1. O(n), deterministic, slightly more code.

Pitfalls:
- Off-by-one: the appended part is reverse of S[:n−k], not S[k:].
- Separator character must not be in the alphabet (use '#' since input is uppercase letters only).
- Input may have trailing newline; strip it.
- Memory: strings of length ~1e6 are fine in Python.
- Python speed: KMP on 1e6 characters with a Python loop is okay (~1e6 iterations), but should use efficient implementation (list of ints, while loop). Should run within typical limits (~1–2s might be tight but usually fine; can also use the built-in via hashing alternative). KMP loop in pure Python over 1e6 chars is roughly 0.3–0.5s — acceptable.

Edge cases: single character → answer is S itself (k = n, append nothing). Already-palindrome S → k = n, answer S.

## worker: Write the complete Python solution: read S from st
- The shortest palindrome having S as a prefix is S plus the reverse of the part of S preceding its longest palindromic suffix. If the longest palindromic suffix has length k, the answer is `S + reverse(S[:n-k])`, with total length `2n - k`, which is minimal because any palindrome containing S as a prefix must mirror the non-palindromic head.
- To find k: run the KMP prefix function over `reverse(S) + '#' + S`. The final prefix-function value equals the longest prefix of `reverse(S)` that is also a suffix of `S`, which is exactly the longest palindromic suffix of S. The `'#'` separator (not in the uppercase alphabet) prevents matches spanning the boundary.
- Verification against samples:
  - S = "ABC": R = "CBA", T = "CBA#ABC", last pi = 1 (suffix "C" = palindrome "C"). Answer = "ABC" + reverse("AB") = "ABCBA". ✓
  - S = "Z": k = 1, answer = "Z". ✓
  - S = "TREE": R = "EERT", longest palindromic suffix of "TREE" is "EE" (k=2). Answer = "TREE" + reverse("TR") = "TREERT". ✓
- Complexity: O(n) time, O(n) memory. Pure-Python KMP over ~1,000,001 characters runs in roughly 0.5–1s, acceptable for n = 500,000. All-same-character input (worst case for border following) is still linear amortized since each mismatch step decreases k and k increases at most m times total.
- Edge cases: empty input handled; single character returns itself; already-palindromic S gives k = n and appends nothing.
