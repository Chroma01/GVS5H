
## ideation
The core difficulty is finding the longest prefix of `S` that is already a palindrome. Once its length is known, the shortest palindrome beginning with `S` is formed by appending the reverse of the remaining suffix. The input length requires an O(n) time and O(n) memory method; quadratic center expansion or repeated slicing will be too slow.

## worker: Derive and implement the KMP prefix-function metho
The final KMP prefix-function value for `S + "#" + reverse(S)` is the longest prefix of `S` matching a suffix of `reverse(S)`. Such a match means the prefix equals its own reverse, so it is exactly the longest palindromic prefix of `S`.

Appending the reverse of the remaining suffix produces a palindrome while preserving `S` as its prefix. The algorithm runs in `O(n)` time and uses `O(n)` memory.

## worker: Replace the incorrect `S + "#" + reverse(S)` compu
The final KMP prefix-function value for `reverse(S) + "#" + S` is the length of the longest suffix of `S` matching a prefix of `reverse(S)`. This is exactly the longest palindromic suffix of `S`.

If that suffix has length `k`, then appending `reverse(S[:-k])` produces the shortest palindrome with `S` as its prefix. The algorithm runs in `O(n)` time and uses `O(n)` memory.
