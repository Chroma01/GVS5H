1. The problem asks for the count of substrings where the integer value of the substring is divisible by its last non-zero digit.
2. A brute-force approach checking all O(N^2) substrings would be too slow for N=10^5. We need a more efficient approach.
3. Key observation: For a substring ending at index `j` with last digit `d` (where `d != 0`), the substring value modulo `d` must be 0.
4. Since `d` is a single digit (1-9), we can iterate through each possible last digit `d` from 1 to 9.
5. For a fixed `d`, we only consider substrings ending at indices where `s[j] == d`. For these indices, we need to count how many starting indices `i` (<= j) make the number `s[i..j]` divisible by `d`.
6. We can use modular arithmetic properties: `(value(s[i..j])) % d = 0`. Note that `value(s[i..j]) = value(s[0..j]) - value(s[0..i-1]) * 10^(j-i+1)`. This seems complex due to the power term.
7. Alternative: Iterate `j` from 0 to n-1. If `s[j]` is '0', skip (as last digit must be non-zero). If `s[j]` is `d` (1-9), we need to count `i` such that `int(s[i:j+1]) % d == 0`.
8. To optimize, notice that for a fixed `d`, as we move `j`, the remainder of the prefix number modulo `d` changes. But the substring value depends on the length. 
9. Actually, a simpler observation: Since `d` is small (1-9), we can group indices by the last digit. For each `d` in 1..9, iterate over all positions `j` where `s[j] == d`. For each such `j`, we want to count `i <= j` such that `int(s[i..j]) % d == 0`.
10. We can compute the value of substring `s[i..j]` modulo `d` efficiently if we precompute prefix values modulo `d`. Specifically, let `P[k]` be the integer value of `s[0..k-1]` modulo `d`. Then `int(s[i..j]) % d = (P[j+1] - P[i] * 10^(j-i+1)) % d`. This still has the `10^(j-i+1)` term which depends on `i`, making it hard to use a simple frequency array.
11. However, note that `10^k % d` is periodic. Since `d` is small, the period is at most `d`. We can maintain counts of `P[i] * 10^(j-i+1) % d`? No, the exponent depends on `j-i+1`.
12. Let's reconsider: For a fixed `d`, and fixed `j` (where `s[j]==d`), we need `int(s[i..j]) % d == 0`.
    `int(s[i..j]) = int(s[i..j-1]) * 10 + d`.
    Let `V(i, j)` be the value. `V(i, j) % d = (V(i, j-1) * 10 + d) % d = (V(i, j-1) * 10) % d` since `d % d = 0`.
    So `V(i, j) % d = (V(i, j-1) * 10) % d`.
    This means the remainder for substring `s[i..j]` is determined by the remainder of `s[i..j-1]` multiplied by 10 mod d.
13. We can maintain, for each `d` in 1..9, a frequency array `freq[d][rem]` which stores the count of starting positions `i` (for substrings ending at the previous position) such that `int(s[i..prev_j]) % d == rem`.
14. When moving from `j-1` to `j`:
    - If `s[j] == '0'`, no substrings end with a non-zero digit, so we don't add any. But we still need to update the remainders for future positions? Actually, if `s[j] == '0'`, substrings ending at `j` are ignored. But substrings ending at `j+1` will include `s[j]`. So we must update the state.
    - The new remainder for a substring `s[i..j]` is `(old_rem * 10) % d`.
    - So, for each `d`, we create a new frequency array `new_freq` where `new_freq[(rem * 10) % d] = freq[d][rem]`.
    - If `s[j] == d` (as a character), then for each `i <= j`, the substring `s[i..j]` ends with `d`. The value is `V(i, j)`. We just computed its remainder as `(V(i, j-1) * 10) % d` for `i < j`. For `i == j`, the value is `d`, and `d % d == 0`.
    - So, after updating the frequency array for the shift, if `s[j] == str(d)`, we add `freq[d][0]` to the total count (these are substrings `s[i..j]` with `i < j` that have remainder 0). Also, the substring `s[j..j]` itself has value `d`, which is divisible by `d`, so we add 1 more.
15. Algorithm:
    - Initialize `total = 0`.
    - For each `d` in 1..9:
        - Initialize `freq` as an array of size `d` with zeros.
        - Iterate `j` from 0 to n-1:
            - Update `freq`: `new_freq` where `new_freq[(r * 10) % d] = freq[r]` for all `r`. Set `freq = new_freq`.
            - If `s[j] == str(d)`:
                - Add `freq[0]` to `total`.
                - Add 1 to `total` (for the single digit substring).
    - Return `total`.
16. Complexity: 9 * N * 9 operations, which is O(N). This fits within constraints.