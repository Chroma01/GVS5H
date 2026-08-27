
## ideation
- **Goal**: Append the minimal number of characters to the right of `S` so that the resulting string is a palindrome and still starts with `S`.
- **Key observation**: The shortest extension is obtained by finding the longest suffix of `S` that is already a palindrome.  
  Let this suffix length be `L`. Then the required palindrome is  
  `S + reverse( S[0 : n‑L] )` where `n = |S|`.  
  No shorter extension can work because any palindrome with prefix `S` must contain `S[0…n‑L‑1]` mirrored at the end.
- **Finding `L` efficiently**:
  - `L` is the length of the longest string that is simultaneously a suffix of `S` and a prefix of `reverse(S)`.
  - This is a classic “longest border” problem and can be solved in linear time with the KMP prefix‑function (or Z‑function) on the string  
    `reverse(S) + '#' + S`.
  - The separator `#` (any character not in `S`) guarantees that the match cannot cross the boundary, so the final prefix‑function value equals the length of the longest palindromic suffix of `S`.
- **Complexities**:
  - Time `O(n)` (single linear scan for the prefix function).
  - Memory `O(n)` for the combined string and the prefix array (`n ≤ 5·10⁵` fits easily).
- **Pitfalls**:
  - Using a naïve `O(n²)` check for each suffix is far too slow for `n = 5·10⁵`.
  - The separator must be a character not appearing in the input; `'#'` works because the input contains only uppercase letters.
  - Off‑by‑one errors when slicing: `S[:n-L]` must be taken from the original `S`, not from the reversed string.
  - If `L = n` (the whole string is a palindrome) the answer is just `S`; ensure the code handles the empty append case.
- **Alternative approaches** (less suitable):
  - Rolling hash with binary search on `L` – also `O(n log n)` and more code, but still works.
  - Manacher’s algorithm for longest palindromic suffix – also linear but more involved to get the suffix length.
  - The chosen KMP method is the simplest and well‑known for this exact problem.

## worker: Write the Python code that implements the algorith
- The problem asks for the shortest palindrome that has `S` as a prefix, which is achieved by appending characters to the right of `S`.
- Let `L` be the length of the longest suffix of `S` that is already a palindrome. Then the required palindrome is `S + reverse(S[:n-L])`. No shorter extension can work.
- `L` is found as the longest string that is simultaneously a suffix of `S` and a prefix of `reverse(S)`. This is exactly the longest border between `reverse(S)` and `S`.
- Computing this border in linear time is done with the KMP prefix function applied to `reverse(S) + '#' + S`. The separator character (any non‑uppercase‑letter, e.g. `'#'`) prevents matches from crossing the boundary.
- Complexity: time `O(n)`, memory `O(n)`, where `n = |S| ≤ 5·10⁵`. This comfortably fits the limits.
- The implementation handles the edge case where the whole string is a palindrome (`L = n`), resulting in the answer being just `S`.
