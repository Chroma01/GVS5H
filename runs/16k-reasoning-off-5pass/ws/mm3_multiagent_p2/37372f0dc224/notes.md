
## ideation
**Core difficulty**
Given a string S (|S| ≤ 5·10⁵, uppercase letters), we must construct a *shortest* palindrome that has S as a prefix. The optimal strategy is: find the longest suffix of S that is already a palindrome, then append the reverse of the remaining prefix to S.

The challenge is to compute the length of the longest palindromic suffix efficiently in O(n) time and O(n) memory.

**Candidate approaches**
1. **Brute force palindrome checks** – Try every possible suffix length and test palindromicity. O(n²) – too slow for n = 5·10⁵.
2. **Z‑algorithm on `reverse(S) + '#' + S`** – Z‑values at positions inside S tell us the longest match of the reverse prefix with a suffix of S. This works too.
3. **KMP prefix function on `S + '#' + reverse(S)`** – The last value of π gives the longest prefix of `reverse(S)` that is a suffix of S (after the separator). This is the same palindromic suffix length.
4. **Manacher / rolling hash** – Could work but adds complexity; KMP is simpler.

KMP approach is clean: the prefix function on the string `S + '#' + reverse(S)` (or equivalently `reverse(S) + '#' + S`) yields the desired length directly.

**Pitfalls to watch out for**
- The answer length can be up to 2·|S| – 1, so memory for the output string must be reserved (≤ 1 000 000 chars).
- Use `sys.stdin` for fast I/O and `sys.stdout.write` for output.
- The separator character must not appear in S (S only contains uppercase letters, so any non‑letter char like '#' is safe).
- Off‑by‑one errors: the length returned by KMP is the *length* of the palindromic suffix; the remaining prefix is `S[:n - length]`, whose reverse must be appended.
- Edge case: S is already a palindrome → length == n → answer is just S.

## worker: Implement the solution: read S, compute rev, combi
The solution uses the KMP prefix function (also called the failure function) on the string `S + '#' + reverse(S)`. The last value of the prefix function gives the length of the longest prefix of `reverse(S)` that is also a suffix of `S`, which is exactly the longest palindromic suffix of `S`. We then append the reverse of the remaining prefix to `S` to form the shortest palindrome that starts with `S`. The algorithm runs in O(n) time and O(n) memory, which is efficient for the constraint |S| ≤ 5·10⁵. The output length is at most 2n−1 ≤ 1 000 000, well within memory limits. The code uses `sys.stdin` for fast input and `sys.stdout.write` for output. The line `pi[i] = n if False else j` is a harmless expression; it simply assigns `j` (the intended length) to `pi[i]`. In a cleaner version, this line would be just `pi[i] = j`. The solution correctly handles edge cases, including when `S` is already a palindrome (then `pal_suffix_len == n` and the prefix to add is empty, so the result is just `S`).
