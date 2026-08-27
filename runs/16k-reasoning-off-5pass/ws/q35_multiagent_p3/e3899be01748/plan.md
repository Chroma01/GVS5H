1. The problem asks for the count of substrings where the integer value of the substring is divisible by its last non-zero digit.
2. A naive O(N^2) approach checking every substring will be too slow given N up to 10^5. We need a more efficient approach.
3. Key observation: For a substring ending at index `j` with last digit `d` (where `d != 0`), we need to count how many starting indices `i` (0 <= i <= j) make the number `s[i..j]` divisible by `d`.
4. The number `s[i..j]` can be expressed as `prefix[j+1] - prefix[i]` where `prefix[k]` is the integer value of `s[0..k-1]`. However, these numbers can be very large.
5. Instead, we can use modular arithmetic. For a fixed end position `j` and last digit `d`, we need `(value(s[i..j])) % d == 0`.
6. `value(s[i..j]) = (value(s[0..j]) - value(s[0..i-1]) * 10^(j-i+1))` is complex due to varying lengths.
7. Alternative: Iterate over each possible last digit `d` from 1 to 9. For each `d`, iterate through all positions `j` where `s[j] == d`. Then, for each such `j`, we need to count `i` such that the substring `s[i..j]` is divisible by `d`.
8. Since `d` is small (1-9), we can maintain counts of remainders modulo `d` for prefixes. Specifically, let `P[k]` be the number formed by `s[0..k-1]`. Then `s[i..j]` corresponds to `(P[j+1] - P[i] * 10^(j-i+1))`. This is still tricky.
9. Better approach: For each ending position `j`, let `d = int(s[j])`. If `d == 0`, skip. Otherwise, we want to count `i` from `0` to `j` such that `int(s[i..j]) % d == 0`.
10. We can compute `int(s[i..j]) % d` incrementally. But doing this for each `j` is O(N^2) in worst case.
11. Optimization: Note that `int(s[i..j]) = int(s[i..j-1]) * 10 + int(s[j])`. So `val(i, j) = val(i, j-1) * 10 + d`.
12. For a fixed `d`, as we move `j`, we can maintain an array `count[r]` which stores the number of starting positions `i` seen so far such that `int(s[i..j-1]) % d == r`. But the modulus base changes with `d`, and also the power of 10 factor changes.
13. Actually, a simpler O(N * 9) approach: For each end position `j`, and for each `d` in 1..9, if `s[j] == d`, we want to count `i` such that `int(s[i..j]) % d == 0`. We can compute `int(s[i..j]) % d` for all `i` from `j` down to `0`. Since `d` is at most 9, and we do this for each `j`, the total work is O(N * 9 * 9) if we optimize, but actually for each `j`, we only care about `d = int(s[j])`. So for each `j`, we compute remainders for `d = int(s[j])` by iterating `i` from `j` down to `0`. This is O(N^2) worst case.
14. We need a better way. Let's use the fact that `d` is small. For each `d` in 1..9, we can process all positions `j` where `s[j] == d` together.
15. For a fixed `d`, let's define `rem[i] = int(s[i..j]) % d`. As we increase `j`, `rem[i]` for existing `i` becomes `(rem[i] * 10 + d) % d = (rem[i] * 10) % d` since `d % d = 0`. Wait, no: `int(s[i..j]) = int(s[i..j-1]) * 10 + s[j]`. So `rem_new[i] = (rem_old[i] * 10 + d) % d = (rem_old[i] * 10) % d`.
16. So for a fixed `d`, we can maintain an array `cnt[r]` for `r` in `0..d-1`, which counts how many starting positions `i` (processed so far, i.e., `i <= j` and `s[k]` for `k` from `i` to `j` doesn't matter, just `i` is a start) have `int(s[i..current_j]) % d == r`.
17. Algorithm for fixed `d`:
    - Initialize `cnt` array of size `d` to zeros.
    - Iterate `j` from `0` to `n-1`:
        - If `s[j] != d`, continue.
        - Update all existing remainders: for each `r` in `0..d-1`, the new remainder for starts that ended at `j-1` is `(r * 10) % d`. But we need to shift the counts. Let `new_cnt` be a new array. `new_cnt[(r * 10) % d] += cnt[r]`.
        - Add the new substring starting and ending at `j`: `val = d`, so `rem = d % d = 0`. So `new_cnt[0] += 1`.
        - Set `cnt = new_cnt`.
        - Add `cnt[0]` to the total answer.
18. This is O(N * d) for each `d`, so total O(N * 9 * 9) = O(N). This is efficient.