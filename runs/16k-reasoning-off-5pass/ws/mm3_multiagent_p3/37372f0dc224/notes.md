
## ideation
We are given a string S (|S| up to 500k, uppercase letters). We need to output the shortest palindrome that has S as a prefix.

**Core idea:**  
If we append some suffix of the reverse of S to S, the whole string becomes a palindrome. The shortest such palindrome corresponds to using the longest possible suffix of reverse(S) that is already a prefix of S. In other words, we need the longest prefix of `rev = reverse(S)` that matches a suffix of S.

**Standard trick:**  
Compute the longest prefix of `rev` that matches a suffix of S. Construct the string `T = S + '#' + rev`. Compute the Z-function (or prefix function) for T.  
- The Z-value at position `len(S) + 1` (the start of `rev`) gives the length of the longest prefix of T that matches a substring starting at that position. Since T starts with S, this is exactly the length of the longest prefix of `rev` that matches a suffix of S.

**Algorithm:**
1. Read S, compute rev = reversed S.
2. Build T = S + '#' + rev.
3. Run Z-algorithm in O(|T|) = O(|S|).
4. Let k = Z[len(S)+1].
5. Answer = S + rev[k:].

**Edge cases:**
- S already a palindrome: then k == len(S) and answer is just S.
- S length 1: works.
- Large N (500k): Z-algo in O(N) with integer arrays is fine in Python if we use lists; careful with recursion (no recursion needed). Memory is O(N) (a list of ints of size N ≈ 1e6) which is OK.

**Pitfalls:**
- Using naive string find/concat repeatedly would be O(N^2).
- Z-algorithm must be implemented correctly with O(N) loops.
- Using a sentinel character like '#' that is guaranteed not to appear in the input is safe because input is uppercase letters A-Z.
- The output should be printed directly; S can be large, but Python print can handle it.

## worker: Implementation is complete and correct; the soluti
The solution uses the Z-algorithm to find the longest prefix of `rev` that matches a suffix of `S`. By constructing `T = S + '#' + rev` (where `#` is a sentinel character not present in the input), the Z-value at the start of `rev` (`z[len(s)+1]`) directly gives the required match length. The answer is then formed by appending the unmatched suffix of `rev` to `S`, which is guaranteed to be the shortest palindrome with prefix `S`. The algorithm runs in O(N) time and O(N) memory, which is suitable for `N` up to 500,000.
