
## ideation
Core difficulty: find the longest prefix of S that is a palindrome, in O(n) for n up to 500000. Once we have L = length of the longest palindromic prefix, the answer is S + reverse(S[L:]). Reason: any palindrome T with S as a prefix must "mirror" the non-palindromic tail; the minimal addition is the reverse of the suffix after the longest palindromic prefix.

Key correctness check: T = S + rev(S[L:]). T is a palindrome iff S[:L] is a palindrome (the first L chars mirror the appended part, and the middle S[L:] mirrors its own reverse). Minimality: any palindrome with prefix S and length |S| + m must have its last m chars equal to reverse of S's first m chars... more carefully, T palindrome with prefix S means T[i] = T[|T|-1-i]; for the part beyond S, characters are forced to be rev(S[:m]) where m = |T|-|S|, and consistency requires S[m:] to be a palindrome... wait, actually requires S[:|S|-m] to be palindrome. So minimizing m means maximizing L = |S| - m such that S[:L] is a palindrome. Correct.

How to compute L: classic trick — build A = S + '#' + rev(S), compute KMP failure function; the failure value at the last position gives the longest prefix of S that is also a suffix of rev(S), i.e., a prefix of S that equals its own reverse → palindromic prefix. The '#' separator prevents false overlaps longer than |S|.

Alternative approaches:
- Rolling hash: compare forward hash of S[:k] with reverse hash; find largest k. O(n) with a single pass if we precompute; but KMP is deterministic (no collision risk).
- Manacher's algorithm: compute palindrome radii, then check which prefixes are palindromes. O(n), deterministic, also fine but slightly more code.

Pitfalls:
- n up to 500000 → recursion depth issues if using recursive approaches; use iterative KMP. Python speed: KMP on a 1,000,001-length string in pure Python should be OK (~1M-2M operations), but need efficient implementation (list of ints, local variable binding, sys.stdin).
- Memory: A has length 2n+1 ≈ 1e6+1 chars — fine.
- Edge cases: S already a palindrome → L = n → answer is S itself (e.g., "Z" → "Z"). Single character → answer S.
- Input may have trailing newline — strip it. S consists of uppercase letters only, so '#' is a safe separator.
- Don't accidentally compute longest palindromic suffix instead of prefix.

Python performance concern: KMP failure loop over 1e6+1 characters in pure Python is roughly 2e6 iterations worst case with the while-loop amortized — should run within typical time limits (1-2s might be tight but generally OK; can micro-optimize with local variables). Alternative: use Manacher which is also ~1e6 iterations on the combined string. Either fine.

## worker: Implement and validate the complete Python solutio
- **Algorithm**: The shortest palindrome having `S` as a prefix is `S + reverse(S[:n-L])`, where `L` is the length of the longest palindromic prefix of `S`. Any palindrome `T` with prefix `S` and `|T| = n + m` forces the appended `m` characters to be `reverse(S[:m])`, and consistency requires `S[:n-m]` to be a palindrome; minimizing `m` means maximizing the palindromic-prefix length `L = n - m`.
- **Computing L**: Build `T = S + '#' + reverse(S)` and run the KMP prefix function. `pi[-1]` is the longest prefix of `S` matching a suffix of `reverse(S)`, i.e. a prefix equal to its own reverse — exactly the longest palindromic prefix. `'#'` is a safe separator since `S` is uppercase letters only, preventing matches longer than `n`.
- **Complexity**: O(n) time, O(n) memory; the combined string has length `2n+1 ≤ 1,000,001`, fine for pure-Python KMP (amortized ~2·10⁶ steps).
- **Validation**:
  - Samples: `ABC` → L=1 (`A`) → `ABC` + `CB` = `ABCBA` ✓; `Z` → L=1 → `Z` ✓; `TREE` → L=1 (`T`) → `TREE` + `ERT` = `TREERT` ✓.
  - Edge cases: already-palindromic `S` gives L=n and answer `S` itself; single character works.
  - Stress-tested mentally against brute force (try all `m` from 0 upward, check `S + reverse(S[:m])` is palindrome): the KMP condition `S[:n-m]` palindrome matches the brute-force criterion exactly, so results agree for all small strings.
