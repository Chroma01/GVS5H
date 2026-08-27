
## ideation
The problem asks for the shortest palindrome string that has the given string `S` as a prefix. The classic solution is to find the longest suffix of `S` that is already a palindrome, then append the reverse of the remaining prefix to the end.

**Core difficulty:** Efficiently finding the longest palindromic suffix of `S` when `|S|` can be up to 500,000. A naive O(n²) check would be too slow.

**Candidate approaches:**
1. **KMP failure function:** Build the string `T = S + '#' + reverse(S)`. Compute the prefix function (failure function) for `T`. The value at the last position gives the length of the longest prefix of `reverse(S)` that matches a suffix of `S`. Since `reverse(S)` reversed is `S`, this length is exactly the length of the longest palindromic suffix of `S`. This runs in O(n) time.
2. **Z-function:** Similar idea using Z-algorithm on `reverse(S) + '#' + S`. Also O(n).
3. **Rolling hash:** Binary search the length of the palindromic suffix and check with hash. O(n log n), acceptable but slightly more complex.

**Pitfalls:**
- Need to handle the case where `S` itself is a palindrome (then answer is just `S`).
- Memory: storing `T` of length ~2n is fine for n=500k.
- Off-by-one errors when slicing `S[:n - l]` to reverse and append.
- The delimiter character `'#'` must not appear in `S` (given uppercase letters, safe).

**Algorithm steps:**
1. Read `S`.
2. Compute `rev = S[::-1]`.
3. Build `combined = S + '#' + rev`.
4. Compute prefix function `pi` for `combined`.
5. Let `l = pi[-1]` (length of longest palindromic suffix).
6. The answer is `S + rev[:len(S) - l]`.
7. Print the answer.

## worker: Write a Python program that reads S, computes the 
The algorithm uses the KMP prefix function on `S + '#' + reverse(S)`. The value of the prefix function at the last position equals the length `l` of the longest suffix of `S` that is also a palindrome (because matching a suffix of `S` with a prefix of `reverse(S)` is equivalent to finding a palindromic suffix). The answer is then `S` plus the reverse of the first `n - l` characters of `S`. This runs in O(n) time and O(n) memory, which easily handles `|S| ≤ 500,000`.
