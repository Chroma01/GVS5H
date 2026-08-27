
## ideation
The problem requires counting substrings of a digit string `s` (length up to 10^5) whose numeric value is divisible by their non-zero last digit. A naive O(n^2) enumeration is too slow.

**Core difficulty:** Efficiently checking divisibility for all substrings without enumerating them explicitly. The last digit `d` is small (1-9), but the substring length can be up to 10^5.

**Key insight:** For a substring `s[i..j]` with last digit `d = s[j]`, the condition `s[i..j] % d == 0` is equivalent to `s[i..j-1] * 10 % d == 0`. Let `g = gcd(10, d)`. This simplifies to `s[i..j-1] % (d/g) == 0`. So for each position `j`, we need to count how many prefixes ending at `j-1` are divisible by `k = d / g`.

**Approach:** Process the string left to right. Maintain, for each relevant modulus `k` (k ∈ {1,2,3,4,7,9}), a frequency array `freq[k][r]` representing the number of substrings ending at the previous position that have remainder `r` modulo `k`. When we encounter a new digit, we can update all `freq` arrays in O(k) time each. Since the sum of `k` is small (1+2+3+4+7+9=26), the total time is O(n). For each position `j` with non-zero digit `d`, the answer increases by `freq[k][0]` (where `k = d/gcd(10,d)`) plus 1 (for the single-digit substring).

**Pitfalls:**
- Must handle `d=0` correctly (skip such positions for the answer, but still update `freq` arrays).
- The `freq` arrays must be updated for every position, even if `d=0`, to maintain correct state for future queries.
- The single-digit substring is always divisible by itself, so add 1 for each non-zero digit.
- Ensure the update formula uses `(r * 10 + digit) % k` for extending substrings to the right.

## worker: Implement the `Solution` class with the `countSubs
The algorithm processes the string in a single pass, maintaining for each small modulus `k ∈ {1,2,3,4,7,9}` a frequency array of remainders of all substrings ending at the previous index. When moving to the next position, these arrays are updated by extending each previous substring to the right and adding the new single-character substring. For each non-zero digit `d`, the number of valid substrings ending at that position is `freq[k][0] + 1`, where `k = d / gcd(10, d)`. This works because `s[i..j] % d == 0` iff `s[i..j-1] * 10 % d == 0` iff `s[i..j-1] % (d/gcd(10,d)) == 0`. The total work per character is `sum(k) = 26`, giving O(n) time and O(1) space. Verified against all three provided examples.
