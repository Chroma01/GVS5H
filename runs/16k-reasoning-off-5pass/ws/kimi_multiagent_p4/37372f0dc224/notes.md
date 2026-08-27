
## ideation
The problem: find the shortest palindrome T such that S is a prefix of T. Since T must start with S, we can only append characters to the end of S. To make T a palindrome with minimal appended characters, we want the longest prefix of S that is already a palindrome (length k). Then the remaining suffix S[k:] must be "mirrored" by appending reverse(S[k:]) at the end. So answer = S + reverse(S[k:]).

Verification with samples:
- S=ABC: longest palindromic prefix is "A" (k=1). Append reverse("BC")="CB" → "ABCCB"? But expected "ABCBA". Hmm — wait: appending reverse(S[k:]) = reverse("BC") = "CB" gives "ABCCB", which is NOT a palindrome. Let me recheck: T = S + X. For T palindrome, T[i] = T[n+m-1-i]. The appended part X of length m must satisfy: X reversed equals S[n-m:] mirrored... Actually correct construction: T = S + reverse(S[:n-k]) where k is the length of the longest palindromic **suffix** of S. Check: S=ABC, longest palindromic suffix = "C" (k=1), append reverse(S[:2]) = reverse("AB") = "BA" → "ABCBA" ✓. S=TREE: longest palindromic suffix = "E" (k=1), append reverse("TRE")="ERT" → "TREEERT"? That's length 7, but expected "TREERT" (length 6). Hmm, longest palindromic suffix of TREE: "EE" is a palindrome of length 2! So k=2, append reverse("TR")="RT" → "TREERT" ✓. S=Z: k=1, append reverse("")="" → "Z" ✓.

So the correct reduction: find the longest palindromic **suffix** of S, then answer = S + reverse(S[:n-k]).

How to compute longest palindromic suffix in O(n):
1. KMP prefix-function approach: compute prefix function of S + '#' + reverse(S). The last value gives the longest prefix of S that equals a suffix of reverse(S), which corresponds to the longest palindromic **prefix** of S. That's the wrong one for appending at the back. Instead, compute prefix function of reverse(S) + '#' + S; the last value = longest prefix of reverse(S) matching a suffix of S = longest suffix of S that equals a prefix of reverse(S) = longest palindromic suffix of S. That works.
2. Manacher's algorithm: compute palindrome radii, then find the longest palindrome ending at position n-1. O(n), also fine.
3. Rolling hash: compare prefix hashes of S with suffix hashes; O(n) with mod hashing (risk of collisions, use double mod or Python's large mod).

Pitfalls:
- n up to 5e5, so O(n^2) is impossible; need linear.
- Recursion limits not relevant; KMP is iterative.
- Memory: building reverse(S) and combined string of length 2n+1 ≈ 1e6+1 chars is fine.
- Off-by-one: answer = S + S[:n-k][::-1].
- Input may have trailing newline; strip it.
- KMP in pure Python over 1e6 characters is fine speed-wise (~1-2s), but should write tight loop. Alternatively use Manacher which is also O(n) but more code. Rolling hash with slicing could be simpler but risk.

Edge cases: S already a palindrome → k=n → answer = S. Single character → answer = S.

## worker: Write the complete Python solution: read S from st
- Reduction: shortest palindrome with S as prefix = S + reverse(S[:n-L]), where L = length of the longest palindromic **suffix** of S. Any palindrome T starting with S must have its last n characters equal to reverse(S); the overlap between S and reverse(S) at the junction is exactly a palindromic suffix of S, so maximizing that overlap (L) minimizes appended characters. Appending reverse(S[:n-L]) is sufficient: the resulting string is a palindrome because the suffix S[n-L:] mirrors the prefix S[:L]... more precisely, T = S + rev(S[:n-L]); T reversed = S[:n-L] + rev(S), and since rev(S) ends with rev(S[n-L:]) = S[:L]... the standard argument: T is a palindrome iff S[n-L:] is a palindrome, which holds by definition of L.
- Computing L: KMP prefix function over `rev(S) + '#' + S`. The final pi value is the longest prefix of rev(S) that is a suffix of S. A prefix of rev(S) of length L equals rev(S[n-L:]); it being a suffix of S means S[n-L:] = rev(S[n-L:]), i.e., S[n-L:] is a palindrome. The separator '#' (not an uppercase letter) prevents matches longer than n.
- Verification:
  - S=ABC: rev=CBA, t=CBA#ABC. Longest prefix of CBA matching suffix of ABC: "A" → L=1. Output ABC + rev("AB") = ABC+BA = ABCBA ✓.
  - S=Z: L=1, output Z + rev("") = Z ✓.
  - S=TREE: rev=EERT, longest prefix of EERT that is a suffix of TREE: "EE" → L=2. Output TREE + rev("TR") = TREE+RT = TREERT ✓.
  - S=ABBA (already palindrome): rev=ABBA, L=4, output ABBA ✓.
- Complexity: O(n) time, O(n) memory (pi array over 2n+1 ≈ 1e6+1 ints). Uses bytes for fast indexing (ints, not 1-char strings), keeping the KMP loop fast in pure Python for n up to 5e5.
- Input read via buffer and split to strip newline; output written as bytes.
