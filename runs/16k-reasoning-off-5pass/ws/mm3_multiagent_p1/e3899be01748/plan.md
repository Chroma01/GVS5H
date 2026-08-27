We need to count substrings `s[i..j]` whose value is divisible by the last digit `d = s[j]` (if `d != '0'`). Since `d` is the last digit of the substring, the substring is fully determined by its start `i` and end `j`. For each position `j` with `d != 0`, we need to count how many `i <= j` make the number `s[i..j]` divisible by `d`.

We can iterate `j` from 0 to n-1. Let `d = int(s[j])`. For this `j`, we consider all substrings ending at `j`. The value of `s[i..j]` can be updated from the previous substring ending at `j-1` as:
`val_i = s[i] * 10^(j-i) + val_{i}^{prev}` (where `val_{i}^{prev}` is the value of `s[i..j-1]`).

However, instead of maintaining all values (which would be O(n^2)), we use modular arithmetic modulo `d`. Since we only care about divisibility by `d`, we maintain `rem[i] = s[i..j] mod d` for each start `i`. The update rule is:
`new_rem[i] = (s[i] * 10^(j-i) + old_rem[i]) mod d`.

Directly computing powers for all `i` is still O(n) per `j`, which is too slow overall (O(n^2)).

The key observation: For a fixed `j` and `d`, the set of `i` where `rem[i] == 0` are those with `s[i..j] mod d == 0`. We can efficiently compute these using a different approach: iterate `i` backwards from `j` to 0, maintaining the current number modulo `d` as we extend the substring to the left. For each `j`, we scan leftwards only while the number of steps is manageable? No, that's still O(n^2) worst case.

Wait, but `d` is at most 9. For each `j`, there are only 9 possible `d` values. We can precompute transitions. Actually, we can do a forward scan for each `j` but only for a limited number of steps? No, the substring length can be up to n.

Alternative: Since `d` is small (1..9), we can afford O(n * 9) or similar. Let's think.

For each `j` and each possible divisor `d` that appears as `s[j]`, we need to count `i <= j` such that `s[i..j] mod d == 0`. Note that `s[i..j] = (prefix[j+1] - prefix[i] * 10^(j-i+1)) / something`? No, standard trick: `s[i..j] mod d` can be computed if we have `prefix mod d` and powers of 10 mod d. But the power `10^(j-i)` depends on the length, which varies with `i`.

But we can precompute `pow10[k] mod d` for all `k` and all `d` (1..9). Then for each `j` and each `d = s[j]`, we iterate `i` from `j` down to 0, maintaining `val = (val * 10 + s[i]) mod d` (building the number from left to right? No, building from right to left: if we extend to the left, the new digit is added at the front, so the number becomes `s[i] * 10^(len) + old_val`). So we can iterate `i` from `j` down to 0, updating `val = (s[i] * pow10[j-i] + val) mod d`. This is O(n) per `j`, total O(n^2).

We need to optimize. Since `d` is only 1..9, we can maintain, for each `d`, an array or hash map of remainders for substrings ending at previous positions? Let's think.

For a fixed `d`, we want to count pairs `(i, j)` with `i <= j`, `s[j] = d` (digit), and `s[i..j] mod d == 0`. This is similar to counting subarrays with sum divisible by k, but with a twist: the modulus depends on the end digit.

Observation: For a fixed end position `j` and fixed `d = s[j]`, we need to count `i` such that `s[i..j] mod d == 0`. The value `s[i..j] mod d` can be expressed as:
`s[i..j] = (prefix[j+1] - prefix[i] * 10^(j-i+1))` in integer arithmetic. Modulo `d`:
`s[i..j] ≡ prefix_mod[j+1] - prefix_mod[i] * 10^(j-i+1) (mod d)`,
where `prefix_mod[k] = number formed by first k digits mod d`.

But `d` changes with `j`. So for each `j`, we need to consider only one `d` (the digit at `j`). So we can iterate `j`, set `d = int(s[j])`, and need to find all `i <= j` with `s[i..j] ≡ 0 (mod d)`.

Now, note that the length `L = j - i + 1` can be up to 10^5. We cannot iterate all `i` for each `j`. But `d` is at most 9. The condition `s[i..j] mod d == 0` depends on `i` and `j`. Let's denote `r_i = prefix[i] mod d`. Then:
`s[i..j] mod d = (r_{j+1} - r_i * pow10[j-i+1] mod d) mod d`.
This is not simply a difference of prefix remainders, because of the multiplier `pow10[...]`.

However, since `d` is small, we can group by the value of `j-i mod something`? Or we can iterate `i` backwards from `j` but stop early? No, we need all.

Wait, there is a known solution for this problem (LeetCode 2955? No, that's different. This is LeetCode 2954? Actually "Number of Substrings Divisible by Their Last Digit" might be a problem). The typical solution is to iterate `j` and for each `j`, iterate `i` backwards but only up to a certain length? No, that would miss some.

Let's think differently. For each `j`, `d` is fixed. We need to count `i` such that `s[i..j] mod d == 0`. The number of such `i` can be counted if we maintain a map from remainders to counts for the prefix values modulo `d`, but we need to account for the power of 10.

Let `len = j - i + 1`. The value is `A = s[i..j]`. We can write `A = B * 10 + s[j]` where `B = s[i..j-1]`. Then `A mod d = (B * 10 + s[j]) mod d = (B mod d) * 10 + s[j] mod d`. So if we know `B mod d`, we can compute `A mod d`. This is a backward recurrence: if we know the remainder of the substring ending at `j-1`, we can get the remainder of the substring ending at `j` by multiplying by 10 and adding the new last digit. But we are extending to the left, not the right. Wait, we are fixing the end `j` and varying the start `i`. For a fixed `j`, the substrings ending at `j` are built by starting from the empty string (or just `s[j]`) and prepending digits to the left. So if we let `R_i` be the remainder of `s[i..j] mod d`, then `R_{i-1} = (s[i-1] * 10^{j-i+1} + R_i) mod d`. The power depends on the distance.

But we can precompute `pow10[k] mod d` for all `k`. Then updating `R` for each step leftwards is O(1). So for each `j`, we can iterate `i` from `j` down to 0 in O(j) time. Total O(n^2). We need to do better.

Notice that for a fixed `d`, the recurrence `R_{i-1} = (s[i-1] * pow10[j-i+1] + R_i) mod d` can be rewritten. Let `k = j - i`. Then `R_{i-1} = (s[i-1] * pow10[k+1] + R_i) mod d`. This is still O(1) per step.

Is there a way to use the fact that `d` is small to batch process? For each `j`, we only care about `d = s[j]`. We can process all `j` together by grouping by `d`. For a fixed `d`, we have a set of positions `j` where `s[j] = d`. For each such `j`, we need to count `i <= j` with `s[i..j] mod d == 0`.

Let's fix `d` and consider all `j` where `s[j] = d`. For each such `j`, we need to count `i` such that `s[i..j] mod d == 0`. If we could answer this for all `j` in a fixed `d` group efficiently.

Consider the reverse: for each `i`, the substrings starting at `i` and ending at `j` (where `s[j]=d`) have values that are built by appending digits to the right. The remainder update is: `R_{new} = (R_old * 10 + s[j]) mod d`. This is independent of the starting position! Wait, that's true: if we have a substring `s[i..j-1]` with remainder `r`, then `s[i..j] = s[i..j-1] * 10 + s[j]`. So modulo `d`, the new remainder is `(r * 10 + s[j]) mod d`. This recurrence does not depend on `i` in terms of the multiplier? It does: the multiplier is 10, which is constant. So if we iterate `j` from left to right, for each start `i`, the remainder evolves as we add more digits. But we are fixing `j` and varying `i`.

What if we iterate `i` from right to left, and for each `i`, we consider all `j >= i`? That is still O(n^2).

But wait: for a fixed `d`, the number of possible remainders is at most `d` (0 to d-1). Since `d <= 9`, there are at most 9 possible remainders. Can we use this to speed up?

For a fixed `d`, we want to count pairs `(i, j)` with `i <= j`, `s[j] = d`, and `s[i..j] mod d == 0`. Let's define for each `i` a "state" as we extend `j`. But we need to know when the condition holds.

Alternatively, think about the condition `s[i..j] mod d == 0`. Since `d` is small, we can precompute for each position `i` the value of `s[i..j] mod d` for all `j`? No.

Another angle: Since `d` is at most 9, we can afford O(n * 9) memory. For each `d`, we can maintain an array `cnt_d[rem]` of counts of remainders of substrings ending at the current position? Let's define for each position `j`, and for each possible divisor `d` (1..9), we want to know, among all `i <= j`, the remainders `s[i..j] mod d`. But `d` is determined by `s[j]`, so we only need to query for `d = s[j]`.

Suppose we process `j` from left to right. For each `j`, we need to count how many `i <= j` give remainder 0 mod `d`. If we could maintain, for each `d`, a map from remainders to counts, updated as we move `j`. How does the set of remainders change when we move from `j-1` to `j`? The new substrings ending at `j` are formed by taking each substring ending at `j-1` and appending `s[j]`. So if we have a remainder `r` for a substring ending at `j-1` modulo `d`, the new remainder is `(r * 10 + s[j]) mod d`. But this holds only if the divisor `d` is the same. However, `d` is the last digit of the substring. For substrings ending at `j-1`, their last digit is `s[j-1]`, which may be different from `s[j]`. So we cannot simply maintain a single map per `d` across different `j` because the divisor changes.

Thus, for each `j`, the divisor is `s[j]`. The substrings ending at `j` have varying divisors depending on where they end. So we need to group by the end position.

This suggests that for each `j`, we need to count `i` such that `s[i..j] mod s[j] == 0`. This is exactly what we had.

Maybe we can use the fact that `s[j]` is small to iterate `i` backwards but stop when the number becomes too large? No, the number can be large and we only care about modulo.

Wait, there is a known trick: For each `j`, we can iterate `i` backwards but only up to 10 or 100 steps? No, the string length is 10^5, and the answer can be O(n^2). But we need to count them efficiently.

Let's reconsider the recurrence. For a fixed `j` and `d = s[j]`, we have:
`s[i..j] mod d = 0` iff `(s[i..j-1] * 10 + d) mod d == 0` iff `(s[i..j-1] * 10) mod d == 0`.
Since `d` divides `d`, we need `s[i..j-1] * 10 ≡ 0 (mod d)`.
So the condition `s[i..j] mod d == 0` is equivalent to `s[i..j-1] * 10 ≡ 0 (mod d)`.
If `gcd(10, d) = g`, then this is equivalent to `s[i..j-1] ≡ 0 (mod d/g)`.
This is a crucial simplification!

Let's verify: We want `s[i..j] = s[i..j-1] * 10 + d` to be divisible by `d`.
So `s[i..j-1] * 10 + d ≡ 0 (mod d)` => `s[i..j-1] * 10 ≡ 0 (mod d)`.
Let `g = gcd(10, d)`. Then `10/g` and `d/g` are coprime. The condition `10 * x ≡ 0 (mod d)` is equivalent to `(d/g) | x`. So `x ≡ 0 (mod d/g)`.
Thus, `s[i..j-1] ≡ 0 (mod d/g)`.

So the problem reduces to: For each position `j` with `d = s[j] > 0`, let `k = d / gcd(10, d)`. Count the number of `i <= j-1` such that `s[i..j-1] ≡ 0 (mod k)`. Also, we must include the substring consisting of just the digit `d` itself (when `i == j`). That substring is always divisible by `d` (since `d` divides itself). So the answer is the number of `i < j` with `s[i..j-1] mod k == 0`, plus 1 (for the single digit substring).

This is great! Now we need to efficiently count, for each `j`, the number of `i < j` such that `s[i..j-1] ≡ 0 (mod k)`, where `k` is determined by `d = s[j]`. Note that `k` is a divisor of `d`, and `d` is the digit at `j`. Since `d` is 1..9, `k` is small (1, 2, 5, etc. Let's list:
- d=1: gcd(10,1)=1, k=1. Condition: s[i..j-1] mod 1 == 0 (always true). So all i < j work. Plus the single digit '1'.
- d=2: gcd(10,2)=2, k=1. Condition: always true. All i < j work.
- d=3: gcd(10,3)=1, k=3. Condition: s[i..j-1] mod 3 == 0.
- d=4: gcd(10,4)=2, k=2. Condition: s[i..j-1] mod 2 == 0 (i.e., even).
- d=5: gcd(10,5)=5, k=1. Condition: always true.
- d=6: gcd(10,6)=2, k=3. Condition: s[i..j-1] mod 3 == 0.
- d=7: gcd(10,7)=1, k=7. Condition: s[i..j-1] mod 7 == 0.
- d=8: gcd(10,8)=2, k=4. Condition: s[i..j-1] mod 4 == 0.
- d=9: gcd(10,9)=1, k=9. Condition: s[i..j-1] mod 9 == 0.

So for each `j`, we need to count, among positions `i < j`, how many have `s[i..j-1] mod k == 0`. This is a range query: for a fixed `j` and a modulus `k`, count `i` in `[0, j-1]` such that the number formed by `s[i..j-1]` is divisible by `k`.

Now, we can precompute for each `k` (which are 1,2,3,4,7,9) the remainders of all suffixes? Or we can process from left to right and maintain, for each `k`, a map from remainders of prefixes to counts.

Let's define `pref_mod[k][i]` = the number formed by the first `i` digits modulo `k`. Then `s[i..j-1] = (pref[j] - pref[i] * 10^(j-i))`? Actually, if we have `pref[t] = value of s[0..t-1] mod k`, then `s[i..j-1] = (pref[j] - pref[i] * 10^(j-i)) mod k`. This is not simply a difference of two prefix values because of the multiplier `10^(j-i)`.

However, we can process from right to left. For a fixed `k`, we can precompute for each `i` the value of `s[i..] mod k`? That would be suffixes. But we need `s[i..j-1]` for all `j`. If we fix `j` and vary `i`, the suffix starting at `i` and ending at `j-1` is a prefix of the suffix starting at `i`. Specifically, if we define `suffix_val[i][len] = s[i..i+len-1] mod k`. We want `suffix_val[i][j-i]`. This still depends on `i` and `j`.

But note: We only need to support queries of the form: count `i` in `[0, j-1]` such that `s[i..j-1] mod k == 0`. This is exactly asking: among all substrings ending at `j-1`, how many have remainder 0 mod `k`? Because the substring `s[i..j-1]` ends at `j-1`. So if we process `j` from left to right, at step `j` we want to know, for the current position `j-1` (as the end), how many substrings ending at `j-1` are divisible by `k`. Wait, we need the count for each possible `k` at each position.

So let's process the string from left to right. At each position `p` (which will serve as `j-1`), we want to know, for each modulus `k` (1,2,3,4,7,9), the number of substrings ending at `p` that are divisible by `k`. Let's denote `count[k][p]` = number of `i` such that `s[i..p] mod k == 0`.

We can compute `count[k][p]` from `count[k][p-1]`? For substrings ending at `p`, they are either just the single digit `s[p]`, or they are `s[i..p-1] * 10 + s[p]`. So the remainder of `s[i..p]` modulo `k` is `(remainder_of_s[i..p-1] * 10 + s[p]) mod k`. So if we know, for each `i <= p-1`, the remainder of `s[i..p-1]`, we can compute the new remainder. But we don't need to know each individually; we just need the count of those with remainder 0 after the transformation.

Specifically, for a fixed `k`, a substring `s[i..p]` is divisible by `k` iff `(r * 10 + s[p]) mod k == 0`, where `r = s[i..p-1] mod k`. So we need to count, among the remainders `r` of substrings ending at `p-1`, how many satisfy `r ≡ (-s[p]) * 10^{-1} (mod k)`, provided `10` is invertible mod `k`. If `gcd(10, k) != 1`, then we need to count `r` such that `(r * 10 + s[p]) mod k == 0`.

This is a standard technique: we maintain a frequency map of remainders for each `k`. For each `k`, we have an array `freq[k][r]` = number of substrings ending at the previous position (or starting at each position?) with remainder `r`. Let's formalize.

Let `end_freq[k][r]` be the number of substrings ending at the current position (say `p`) that have remainder `r` modulo `k`. When we move to the next position `p+1`, the new substrings ending at `p+1` are:
1. The single character `s[p+1]` with remainder `s[p+1] mod k`.
2. For each substring ending at `p` with remainder `r`, the extended substring has remainder `(r * 10 + s[p+1]) mod k`.

So we can update `end_freq` for the next position as:
`new_end_freq[k][(r * 10 + digit) mod k] += end_freq[k][r] for all r`.
This is O(k) per `k` per position. Since `k` is at most 9, and we have a few `k`s, this is O(n * sum_k k) = O(n * 30) = O(n). That is efficient!

But wait, we need to answer queries for each `j` (which corresponds to `p+1` in this notation). For a given `j`, we need `count[k][j-1]` where `k` depends on `s[j]`. Specifically, we need the number of substrings ending at `j-1` that are divisible by `k`. That is exactly `end_freq[k][0]` at position `j-1`. So if we process from left to right, and at each step we have `end_freq` for the substrings ending at the current position, then for the next position `j` (where `j = p+1`), we need `end_freq[k][0]` from the previous position `p = j-1`. So we can compute the answer for `j` using the `end_freq` from the previous index.

Let's outline the algorithm:

Initialize `ans = 0`.
Initialize `end_freq` for position `-1` (i.e., before any characters). At this point, there are no substrings. So `end_freq[k][r] = 0` for all `k, r`.
For each position `j` from 0 to n-1:
  - Let `d = int(s[j])`.
  - If `d != 0`:
      - Determine `k` as above: `g = gcd(10, d); k = d // g`.
      - The number of valid `i < j` is `end_freq[k][0]` (since these are substrings ending at `j-1` with remainder 0 mod `k`).
      - Add this to `ans`.
      - Also add 1 for the single digit substring `s[j]`.
  - Now, we need to update `end_freq` to include substrings ending at `j`. This is for future queries.
  - For each `k` in our set (1,2,3,4,7,9):
      - Compute `new_end_freq` based on current `end_freq` and `s[j]`.
      - The new remainder for a previous remainder `r` is `(r * 10 + digit) mod k`.
      - Also, add the single digit: `new_end_freq[digit mod k] += 1`.
      - Replace `end_freq` with `new_end_freq`.

At the end, return `ans`.

Wait, we need to be careful: the `end_freq` for position `j` will be used when processing `j+1` to answer the query for `j+1` (where `j+1` acts as the new end). So the order is:
- Before processing `j`, `end_freq` contains the remainders of substrings ending at `j-1`.
- We use `end_freq[k][0]` to answer for `j`.
- Then we update `end_freq` to contain remainders of substrings ending at `j`.

This works perfectly.

Now, what are the moduli `k` we need to support? From the analysis:
- d=1: k=1
- d=2: k=1
- d=3: k=3
- d=4: k=2
- d=5: k=1
- d=6: k=3
- d=7: k=7
- d=8: k=4
- d=9: k=9

So the set of `k` is {1,2,3,4,7,9}. (k=1 is trivial, but we can include it.)
For k=1, all numbers are divisible by 1, so `end_freq[1][0]` is just the total number of substrings ending at `j-1`, which is `j`. But we can also compute it via the same method.

The number of states is small: for each k, we need an array of size k. Total size = 1+2+3+4+7+9 = 26. Very small.

The update for each `k` takes O(k) time per character. So total time per character is O(sum k) = O(26) = O(1). Total time O(n). Space O(1).

Let's verify with examples.

Example 1: s = "12936"
j=0: d=1, k=1. end_freq from j=-1 is all zeros. end_freq[1][0] = 0. ans += 0 + 1 = 1. Update end_freq for substrings ending at 0: "1". For k=1: new[ (0*10+1)%1 ] += 0 + 1? Wait, we need to be careful with the update.

Let's write the update step clearly.

We have `freq[k][r]` for substrings ending at previous position.
We want `new_freq[k][r']` for substrings ending at current position.
For each `r` from 0 to k-1:
  `new_r = (r * 10 + digit) mod k`
  `new_freq[k][new_r] += freq[k][r]`
Also, the single character substring:
  `new_freq[k][digit mod k] += 1`

Initialize `new_freq` to zeros.

Let's test with "12936".

Initialize all freq arrays to zero.

j=0, digit=1.
d=1, k=1.
end_freq[1][0] = 0. ans += 0 + 1 = 1. (substring "1" is valid)
Update:
k=1: new_freq[1][ (0*10+1)%1 ] += freq[1][0] = 0. Then new_freq[1][1%1] += 1. So new_freq[1][0] = 1. (Only substring "1" ends at 0)
k=2: new_freq[2][ (0*10+1)%2 ] += freq[2][0] = 0. new_freq[2][1%2] += 1. So new_freq[2][1] = 1.
k=3: new_freq[3][ (0*10+1)%3 ] += 0. new_freq[3][1] = 1.
k=4: new_freq[4][1] = 1.
k=7: new_freq[7][1] = 1.
k=9: new_freq[9][1] = 1.

j=1, digit=2.
d=2, k=1 (since gcd(10,2)=2, k=1).
end_freq[1][0] = 1 (substring "1" ending at 0). So count of i<1 with s[i..0] mod 1 == 0 is 1.
ans += 1 + 1 = 2. Total ans=3.
Check: substrings ending at 1: "2", "12". "2" is valid. "12": last digit 2, 12%2=0, valid. So 2 valid. But we are counting i<j: i=0 gives "1" which is s[0..0] and we require s[0..0] mod 1 == 0, which is true. So we add 1 for i=0, plus 1 for the single digit "2". That gives 2. Total 3 so far. But wait, are there any others? "1" and "2" and "12". All valid. So 3 is correct.

Update with digit=2:
For k=1: freq[1] currently has new_freq[1][0]=1.
new_freq[1][ (0*10+2)%1 ] += 1 => new_freq[1][0] += 1.
plus single digit: new_freq[1][2%1] += 1 => new_freq[1][0] += 1.
So new_freq[1][0] = 1 (from prev) + 1 (single) = 2? Wait, careful: we need to initialize new_freq to zero, then for each r, add freq[r] to new_freq[new_r], then add 1 to new_freq[digit%k].
So for k=1: freq[1][0]=1.
r=0: new_r = (0*10+2)%1 = 0. new_freq[1][0] += 1.
Then single: new_freq[1][0] += 1.
Total new_freq[1][0] = 2.
k=2: freq[2][1]=1.
r=1: new_r = (1*10+2)%2 = 0. new_freq[2][0] += 1.
single: new_freq[2][2%2] = new_freq[2][0] += 1.
So new_freq[2][0] = 2.
k=3: freq[3][1]=1.
r=1: new_r = (1*10+2)%3 = 0. new_freq[3][0] += 1.
single: new_freq[3][2%3] = new_freq[3][2] += 1.
So new_freq[3][0]=1, new_freq[3][2]=1.
k=4: freq[4][1]=1.
r=1: new_r = (1*10+2)%4 = 0. new_freq[4][0] += 1.
single: new_freq[4][2] += 1.
k=7: freq[7][1]=1.
r=1: new_r = (1*10+2)%7 = 5? 12%7=5. new_freq[7][5] += 1.
single: new_freq[7][2] += 1.
k=9: freq[9][1]=1.
r=1: new_r = (1*10+2)%9 = 3. new_freq[9][3] += 1.
single: new_freq[9][2] += 1.

j=2, digit=9.
d=9, k=9 (gcd(10,9)=1, k=9).
end_freq[9][0] = 0. So count of i<2 with s[i..1] mod 9 == 0 is 0.
ans += 0 + 1 = 1. Total ans=4.
Check substrings ending at 2: "9", "29", "129". Last digit 9. "9": 9%9=0 valid. "29": 29%9=2 invalid. "129": 129%9=3 invalid. So only 1 valid. Good.

Update with digit=9:
We need to update all k. This is getting long but seems correct.

Let's test the final answer for "12936" manually with code later.

The algorithm seems solid and efficient: O(n * sum(k)) = O(n * 26) = O(n).

We must be careful to handle the case when d=0: the last digit is zero, so we skip (no valid substrings end with 0, as per problem statement "non-zero last digit").

Also, note that the problem says "divisible by their non-zero last digit". So we only consider substrings whose last digit is not zero. If a substring ends with 0, it's invalid. Our algorithm naturally skips d=0.

Now, we need to implement this in the `Solution` class.

Implementation details:
- We need to maintain `freq` for k in {1,2,3,4,7,9}. We can use a dictionary or fixed-size lists.
- Since k values are small, we can use lists of size k.
- We'll have a list `freq = [ [0]*k for k in [1,2,3,4,7,9] ]`. But the indices are different sizes. We can map k to index: idx = {1:0, 2:1, 3:2, 4:3, 7:4, 9:5}.
- Or we can just have separate variables for each k to avoid indexing confusion. Since the number of k is small, separate variables are fine and maybe faster.

Let's define:
`freq1 = [0]`  # size 1
`freq2 = [0,0]` # size 2
`freq3 = [0,0,0]` # size 3
`freq4 = [0,0,0,0]` # size 4
`freq7 = [0]*7`
`freq9 = [0]*9`

When updating for a digit `d`:
- For each k, we compute `new_freq` by initializing a zero list of size k, then for each r in 0..k-1, compute `nr = (r*10 + d) % k` and add `freq[r]` to `new_freq[nr]`. Then add 1 to `new_freq[d % k]`.
- Then replace the old list with the new one.

Since k is small, this is fast.

The total answer: for each j, if d != 0:
  g = gcd(10, d)
  k = d // g
  ans += count of substrings ending at j-1 that are divisible by k.
  This count is exactly the number of substrings ending at j-1 with remainder 0 mod k, which is `freq_k[0]` before updating for j (i.e., the state for position j-1).
  ans += 1 (for the single digit d).

Wait, is there any overlap? The single digit substring is `s[j..j]`. The condition for i=j is always satisfied because `d % d == 0`. So we add 1. The other valid substrings are those with i < j. Our count of `freq_k[0]` gives the number of i < j such that `s[i..j-1] mod k == 0`, which corresponds to `s[i..j] mod d == 0`. So no overlap and no missing.

Let's double-check with example 2: "5701283"
We'll trust the logic.

One more check: What about substrings that consist of a single non-zero digit? They are counted by the `+1` for each j. Are they also counted in `freq_k[0]`? No, because `freq_k` contains substrings ending at previous positions (j-1), not the current one. So no double counting.

Edge case: empty string? Constraints say length >= 1.

What about leading zeros? The problem says substrings may contain leading zeros. Our algorithm handles that naturally because we treat them as numbers with leading zeros (value is just the integer). The modulo operation works fine.

Let's test with "1010101010" from example 3.
Only substrings ending with '1' are valid. Our algorithm: d=1 => k=1. For d=1, we always add `freq1[0] + 1`. Since k=1, `freq1[0]` is just the total number of substrings ending at previous position, which is j (since there are j substrings ending at j-1, all divisible by 1). So for each '1', we add j + 1. Let's compute:
j=0: '1', d=1, k=1. freq1[0]=0. ans += 0+1=1.
j=1: '0', skip.
j=2: '1', d=1. freq1[0] should be the number of substrings ending at j-1=1. At j=1 (digit 0), we updated freq1: all previous remainders become 0, plus single digit 0. So freq1[0] becomes the total number of substrings ending at 1, which is 2 ( "0" and "10"). So ans += 2+1=3. Total 4.
j=3: '0', skip.
j=4: '1', d=1. freq1[0] is number of substrings ending at 3, which is 4. ans += 4+1=5. Total 9.
j=5: '0', skip.
j=6: '1', freq1[0]=6, ans += 7 => 16.
j=7: '0', skip.
j=8: '1', freq1[0]=8, ans += 9 => 25.
j=9: '0', skip.
Total ans = 25. Matches example 3.

Great!

Now, we need to implement this efficiently.

Code structure:
```python
from math import gcd

class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        # Frequency arrays for remainders of substrings ending at previous position
        # k=1,2,3,4,7,9
        freq = {
            1: [0],
            2: [0, 0],
            3: [0, 0, 0],
            4: [0, 0, 0, 0],
            7: [0] * 7,
            9: [0] * 9
        }
        ans = 0
        for j, ch in enumerate(s):
            d = int(ch)
            if d != 0:
                g = gcd(10, d)
                k = d // g
                # Number of i < j such that s[i..j-1] mod k == 0
                ans += freq[k][0]
                # The single digit substring
                ans += 1
            # Update frequency for substrings ending at current position
            for k in [1, 2, 3, 4, 7, 9]:
                old = freq[k]
                new = [0] * k
                digit = d
                for r in range(k):
                    new_r = (r * 10 + digit) % k
                    new[new_r] += old[r]
                # Add the single character substring
                new[digit % k] += 1
                freq[k] = new
        return ans
```

But wait, the update loop runs for all k, even if d=0. That's fine, but we can optimize by not updating when d=0? No, we need to update for all j to maintain the correct frequencies for future j. Even if d=0, the substrings ending at j still have remainders, and we need them for future queries. So we must update for every j.

However, we can note that when d=0, the update is still needed. So the loop is correct.

Complexity: For each j, we iterate over 6 values of k, and for each k, we iterate over k elements. Total operations per j: 1+2+3+4+7+9 = 26. So O(n) time.

Space: O(1).

We should double-check the update for the single character: `new[digit % k] += 1`. This is correct because the substring consisting of just `s[j]` has remainder `s[j] mod k`.

One subtle point: The `freq` initially (for j=0) should represent substrings ending at position -1, i.e., no substrings. So all zeros. That's what we have.

After processing j=0, `freq` contains substrings ending at position 0. So when j=1, `freq` is correct for j-1=0.

Everything seems correct.

Let's test with a small example manually in Python mentally.
s = "5701283"
j=0: '5', d=5, g=5, k=1. ans += freq[1][0] (0) + 1 = 1.
Update:
k=1: old=[0], new: r=0: new[0] += 0; single: new[0] += 1 => [1]
k=2: old=[0,0], new: r=0: new[0] += 0; r=1: new[ (10+5)%2=1 ] += 0; single: new[5%2=1] += 1 => [0,1]
k=3: old=[0,0,0], new: r=0: new[0]+=0; r=1: new[ (10+5)%3=0 ]+=0; r=2: new[ (20+5)%3=1 ]+=0; single: new[5%3=2] +=1 => [0,0,1]
k=4: old=[0,0,0,0], new: r=0: new[0]+=0; r=1: new[ (10+5)%4=3 ]+=0; r=2: new[ (20+5)%4=1 ]+=0; r=3: new[ (30+5)%4=3 ]+=0; single: new[5%4=1] +=1 => [0,1,0,1]? Wait, careful: (r*10 + d) % 4. For r=1: (10+5)%4=15%4=3. So new[3]+=0. For r=2: (20+5)%4=25%4=1. So new[1]+=0. For r=3: (30+5)%4=35%4=3. So new[3]+=0. Then single: new[1] += 1. So new = [0,1,0,0]? Actually, let's compute properly:
k=4:
r=0: nr = (0+5)%4=1. new[1] += 0.
r=1: nr = (10+5)%4=3. new[3] += 0.
r=2: nr = (20+5)%4=1. new[1] += 0.
r=3: nr = (30+5)%4=3. new[3] += 0.
single: new[1] += 1.
So new = [0,1,0,0]. Correct.
k=7: old=[0]*7, new: single: new[5%7=5] = 1. Others 0.
k=9: old=[0]*9, new: single: new[5%9=5] = 1.

j=1: '7', d=7, g=1, k=7. ans += freq[7][0] (0) + 1 = 1. Total ans=2.
Update with d=7:
k=1: old=[1], new: r=0: nr=(0+7)%1=0, new[0]+=1; single: new[0]+=1 => [2]
k=2: old=[0,1], new: r=0: nr=(0+7)%2=1, new[1]+=0; r=1: nr=(10+7)%2=1, new[1]+=1; single: new[7%2=1] +=1 => new[1]=2. So [0,2]
k=3: old=[0,0,1], new: r=0: nr=1, new[1]+=0; r=1: nr= (10+7)%3=2, new[2]+=0; r=2: nr= (20+7)%3=0, new[0]+=1; single: new[7%3=1] +=1 => new: [1,1,0]
k=4: old=[0,1,0,0], new: r=0: nr=3, new[3]+=0; r=1: nr= (10+7)%4=1, new[1]+=1; r=2: nr= (20+7)%4=3, new[3]+=0; r=3: nr= (30+7)%4=1, new[1]+=0; single: new[7%4=3] +=1 => new: [0,1,0,2]
k=7: old=[0,0,0,0,0,1,0], new: r=0: nr=0, new[0]+=0; r=1: nr= (10+7)%7=3, new[3]+=0; r=2: nr= (20+7)%7=6, new[6]+=0; r=3: nr= (30+7)%7=2, new[2]+=0; r=4: nr= (40+7)%7=5, new[5]+=0; r=5: nr= (50+7)%7=0, new[0]+=1; r=6: nr= (60+7)%7=4, new[4]+=0; single: new[0] +=1 => new: [2,0,0,0,0,0,0]
k=9: old=[0]*9 with [5]=1. new: r=5: nr= (50+7)%9=57%9=3, new[3]+=1; single: new[7%9=7] +=1 => new: [0,0,0,1,0,0,0,1,0]

j=2: '0', d=0. Skip ans.
Update with d=0:
k=1: old=[2], new: r=0: nr=0, new[0]+=2; single: new[0]+=1 => [3]
k=2: old=[0,2], new: r=0: nr=0, new[0]+=0; r=1: nr= (10+0)%2=0, new[0]+=2; single: new[0] +=1 => [3,0]
k=3: old=[1,1,0], new: r=0: nr=0, new[0]+=1; r=1: nr= (10+0)%3=1, new[1]+=1; r=2: nr= (20+0)%3=2, new[2]+=0; single: new[0] +=1 => [2,1,0]
k=4: old=[0,1,0,2], new: r=0: nr=0, new[0]+=0; r=1: nr= (10+0)%4=2, new[2]+=1; r=2: nr= (20+0)%4=0, new[0]+=0; r=3: nr= (30+0)%4=2, new[2]+=2; single: new[0] +=1 => [1,0,3,0]
k=7: old=[2,0,0,0,0,0,0], new: r=0: nr=0, new[0]+=2; r=1: nr=3, new[3]+=0; r=2: nr=6, new[6]+=0; r=3: nr=2, new[2]+=0; r=4: nr=5, new[5]+=0; r=5: nr=0, new[0]+=0; r=6: nr=4, new[4]+=0; single: new[0] +=1 => [3,0,0,0,0,0,0]
k=9: old=[0,0,0,1,0,0,0,1,0], new: r=3: nr= (30+0)%9=3, new[3]+=1; r=7: nr= (70+0)%9=7, new[7]+=1; single: new[0] +=1 => [1,0,0,1,0,0,0,1,0]

j=3: '1', d=1, g=1, k=1. ans += freq[1][0] (3) + 1 = 4. Total ans=6.
Update with d=1:
k=1: old=[3], new: r=0: nr=1%1=0, new[0]+=3; single: new[1%1=0] +=1 => [4]
k=2: old=[3,0], new: r=0: nr=1, new[1]+=3; r=1: nr= (10+1)%2=1, new[1]+=0; single: new[1%2=1] +=1 => [0,4]
k=3: old=[2,1,0], new: r=0: nr=1, new[1]+=2; r=1: nr= (10+1)%3=2, new[2]+=1; r=2: nr= (20+1)%3=0, new[0]+=0; single: new[1%3=1] +=1 => [0,3,1]
k=4: old=[1,0,3,0], new: r=0: nr=1, new[1]+=1; r=1: nr= (10+1)%4=3, new[3]+=0; r=2: nr= (20+1)%4=1, new[1]+=3; r=3: nr= (30+1)%4=3, new[3]+=0; single: new[1%4=1] +=1 => [0,5,0,0]
k=7: old=[3,0,0,0,0,0,0], new: r=0: nr=1, new[1]+=3; single: new[1%7=1] +=1 => [0,4,0,0,0,0,0]
k=9: old=[1,0,0,1,0,0,0,1,0], new: r=0: nr=1, new[1]+=1; r=3: nr= (30+1)%9=4, new[4]+=1; r=7: nr= (70+1)%9=8, new[8]+=1; single: new[1%9=1] +=1 => [0,2,0,0,1,0,0,0,1]

j=4: '2', d=2, g=2, k=1. ans += freq[1][0] (4) + 1 = 5. Total ans=11.
Update with d=2:
k=1: old=[4], new: [4+1]= [5]
k=2: old=[0,4], new: r=0: nr=0, new[0]+=0; r=1: nr= (10+2)%2=0, new[0]+=4; single: new[2%2=0] +=1 => [5,0]
k=3: old=[0,3,1], new: r=0: nr=2, new[2]+=0; r=1: nr= (10+2)%3=0, new[0]+=3; r=2: nr= (20+2)%3=1, new[1]+=1; single: new[2%3=2] +=1 => [3,1,1]
k=4: old=[0,5,0,0], new: r=0: nr=2, new[2]+=0; r=1: nr= (10+2)%4=0, new[0]+=5; r=2: nr= (20+2)%4=2, new[2]+=0; r=3: nr= (30+2)%4=0, new[0]+=0; single: new[2%4=2] +=1 => [5,0,1,0]
k=7: old=[0,4,0,0,0,0,0], new: r=1: nr= (10+2)%7=5, new[5]+=4; single: new[2%7=2] +=1 => [0,0,1,0,0,4,0]
k=9: old=[0,2,0,0,1,0,0,0,1], new: r=1: nr= (10+2)%9=3, new[3]+=2; r=4: nr= (40+2)%9=6, new[6]+=1; r=8: nr= (80+2)%9=1, new[1]+=1; single: new[2%9=2] +=1 => [0,1,1,2,0,0,1,0,0]

j=5: '8', d=8, g=2, k=4. ans += freq[4][0] (5) + 1 = 6. Total ans=17.
Update with d=8:
k=1: old=[5], new: [6]
k=2: old=[5,0], new: r=0: nr=0, new[0]+=5; r=1: nr= (10+8)%2=0, new[0]+=0; single: new[8%2=0] +=1 => [6,0]
k=3: old=[3,1,1], new: r=0: nr=2, new[2]+=3; r=1: nr= (10+8)%3=0, new[0]+=1; r=2: nr= (20+8)%3=1, new[1]+=1; single: new[8%3=2] +=1 => [1,1,4]
k=4: old=[5,0,1,0], new: r=0: nr=0, new[0]+=5; r=1: nr= (10+8)%4=2, new[2]+=0; r=2: nr= (20+8)%4=0, new[0]+=1; r=3: nr= (30+8)%4=2, new[2]+=0; single: new[8%4=0] +=1 => [7,0,0,0]
k=7: old=[0,0,1,0,0,4,0], new: r=0: nr=1, new[1]+=0; r=1: nr= (10+8)%7=4, new[4]+=0; r=2: nr= (20+8)%7=0, new[0]+=1; r=3: nr= (30+8)%7=3, new[3]+=0; r=4: nr= (40+8)%7=6, new[6]+=0; r=5: nr= (50+8)%7=2, new[2]+=4; r=6: nr= (60+8)%7=5, new[5]+=0; single: new[8%7=1] +=1 => [1,1,4,0,0,0,0]
k=9: old=[0,1,1,2,0,0,1,0,0], new: r=1: nr= (10+8)%9=0, new[0]+=1; r=2: nr= (20+8)%9=1, new[1]+=1; r=3: nr= (30+8)%9=2, new[2]+=2; r=6: nr= (60+8)%9=5, new[5]+=1; single: new[8%9=8] +=1 => [1,1,2,0,0,1,0,0,1]

j=6: '3', d=3, g=1, k=3. ans += freq[3][0] (1) + 1 = 2. Total ans=19? But expected answer for "5701283" is 18. Wait, let's check the example. Example 2 says output 18. My manual count gave 19? Let's trace carefully.

Wait, I must have made a mistake. Let's list all substrings for "5701283" that are valid.
String: 5 7 0 1 2 8 3
Indices: 0 1 2 3 4 5 6

Valid substrings (last digit non-zero and divisible):
- Single digits: '5', '7', '1', '2', '8', '3' (6 substrings)
- Substrings ending at 1 ('7'): need s[i..0] mod 1 == 0. All substrings ending at 0 are valid. Substrings ending at 0: '5' (i=0). So i=0 gives '57'. '57' last digit 7, 57%7=1? 57=7*8+1, not divisible. Wait, condition is s[i..j] mod d == 0. For j=1, d=7. s[0..1]='57'. 57%7=1, not 0. But my condition said: s[i..j-1] mod k == 0, where k = d/gcd(10,d). For d=7, gcd=1, k=7. So we need s[0..0]='5' mod 7 == 0? 5%7=5 != 0. So it's not valid. So i=0 does not work. My algorithm said ans += freq[7][0] for j=1. At j=1, freq[7][0] was 0, so it correctly added 0. But in my manual trace, I said ans += 0+1=1 for j=1. That was correct. Then for j=2 ('0'), skip. j=3 ('1'): d=1, k=1. ans += freq[1][0] (3) + 1 = 4. So substrings ending at 3: '1', '01', '701', '5701'? Wait, substrings ending at 3: i=3: '1' (counted as +1). i=2: '01' (last digit 1, 1%1=0, valid). i=1: '701' (701%1=0, valid). i=0: '5701' (5701%1=0, valid). So 4 substrings. Total so far: j=0:1, j=1:1, j=3:4 => 6. j=4 ('2'): d=2, k=1. ans += freq[1][0] (4) + 1 = 5. Substrings ending at 4: '2', '12', '012', '7012', '57012'. All valid because mod 1. That's 5. Total 11. j=5 ('8'): d=8, g=2, k=4. ans += freq[4][0] (5) + 1 = 6. Substrings ending at 5: '8', '28', '128', '0128', '70128', '570128'. Check divisibility by 8: '8' ok, '28' 28%8=4 no, '128' 128%8=0 ok, '0128' ok, '70128' 70128/8=8766 ok? 8*8766=70128, yes. '570128' 570128/8=71266? 8*71266=570128, yes. So among these, which are valid? Condition: s[i..4] mod 4 == 0. For i=5: '8' mod 4=0 ok. i=4: '28' mod 4=0? 28%4=0, yes! Wait, '28' is divisible by 4. But my manual check said 28%8=4, not 0. The last digit is 8, so we check 28%8=4, not 0. So '28' is NOT valid because 28 is not divisible by 8. But my condition using k=4: s[i..4] mod 4 == 0. For i=4, s[4..4]='2', 2%4=2 != 0. So the condition says it's not valid. Good. For i=3: '128' mod 4 = 0, and 128%8=0, valid. i=2: '0128' mod 4 = 0, valid. i=1: '70128' mod 4 = 0? 70128 % 4 = 0 (since 28%4=0), valid. i=0: '570128' mod 4 = 0? 128%4=0, valid. So valid substrings ending at 5: i=5,3,2,1,0. That's 5. But we also have the single digit '8'? i=5 is the single digit, already counted. So total 5. My ans added freq[4][0] (5) + 1 = 6. So 6 substrings? But I only found 5. Let's list: '8', '128', '0128', '70128', '570128'. That's 5. Why did freq[4][0] give 5? Because there are 5 substrings ending at j-1=4 that are divisible by 4. Let's check substrings ending at 4: '2', '12', '012', '7012', '57012'. Mod 4: 2%4=2, 12%4=0, 012%4=0, 7012%4=0 (12%4=0), 57012%4=0. So 4 of them are divisible by 4. Wait, '2' is not. So freq[4][0] should be 4, not 5. Let's check my manual update for freq[4] at j=4.

At j=3 ('1'), freq[4] was updated. I had old=[0,5,0,0]? Let's re-evaluate j=3 update.
Before j=3, freq[4] was from j=2: [1,0,3,0] (as I had after j=2).
j=3 digit=1.
Update: r=0: nr=(0+1)%4=1, new[1]+=1.
r=1: nr=(10+1)%4=3, new[3]+=0.
r=2: nr=(20+1)%4=1, new[1]+=3.
r=3: nr=(30+1)%4=3, new[3]+=0.
single: new[1] += 1 (since 1%4=1).
So new = [0, 1+3+1=5, 0, 0]. So freq[4] = [0,5,0,0]. This is for substrings ending at j=3.
Now at j=4, we use this freq. So freq[4][0] = 0. Wait, it's 0, not 5! I mistakenly wrote freq[4][0] = 5 in my ans calculation for j=4. I said "ans += freq[4][0] (5) + 1 = 6". But actually freq[4][0] was 0. So ans added 0+1=1 for j=4? But j=4 is '2', and we need to count substrings ending at 3 that are mod 4 == 0. freq[4][0] is the number of substrings ending at j-1=3 with remainder 0 mod 4. After j=3, freq[4][0] is indeed 0. So the count is 0. But earlier I thought substrings ending at 3: '1', '01', '701', '5701'. Mod 4: 1%4=1, 01%4=1, 701%4=1, 5701%4=1. So none are divisible by 4. So freq[4][0]=0 is correct. So for j=4, ans += 0 + 1 = 1 (for the single '2'). But wait, we also need to count substrings ending at 4 with last digit 2. d=2, k=1. So we need freq[1][0], not freq[4][0]. So for j=4, we use k=1, not k=4. I made a mistake in the manual trace by mixing k values. Let's re-do the ans calculation properly for each j:

j=0: d=5, k=1. ans += freq[1][0] (0) + 1 = 1.
j=1: d=7, k=7. ans += freq[7][0] (0) + 1 = 1. Total 2.
j=2: d=0, skip.
j=3: d=1, k=1. ans += freq[1][0] (3) + 1 = 4. Total 6.
j=4: d=2, k=1. ans += freq[1][0] (4) + 1 = 5. Total 11.
j=5: d=8, k=4. ans += freq[4][0] (0) + 1 = 1. Total 12.
j=6: d=3, k=3. ans += freq[3][0] (1) + 1 = 2. Total 14.

But expected is 18. I got 14. So there is a discrepancy. Let's list all valid substrings for "5701283" according to the problem statement and my count.

The example says:
Substrings "01", "12", "701", "012", "128", "5701", "7012", "0128", "57012", "70128", "570128", and "701283" are all divisible by their last digit. Additionally, all substrings that are just 1 non-zero digit are divisible by themselves. Since there are 6 such digits, the answer is 12 + 6 = 18.

Wait, they list "12" as divisible by its last digit 2. 12%2=0, yes.
"012" divisible by 2? 12%2=0, yes.
"7012" divisible by 2? 12%2=0, yes.
"57012" divisible by 2? 12%2=0, yes.
So these are the ones ending with 2 (except the single '2'). That's 4 substrings ending with 2 (i=4,3,2,1,0? Actually, substrings ending at 4: '2', '12', '012', '7012', '57012'. That's 5 substrings ending with 2. But the example says 4? "01", "12", "701", "012", "128", "5701", "7012", "0128", "57012", "70128", "570128", and "701283". That's 12. Let's parse them:
"01" ends with 1, i=2..3? Wait, "01" is indices 2-3.
"12" is 3-4.
"701" is 1-3.
"012" is 2-4.
"128" is 3-5.
"5701" is 0-3.
"7012" is 1-4.
"0128" is 2-5.
"57012" is 0-4.
"70128" is 1-5.
"570128" is 0-5.
"701283" is 1-6.

Now, substrings ending with 2 (digit 2): these are substrings that end at index 4. The possible start indices: 4 ('2'), 3 ('12'), 2 ('012'), 1 ('7012'), 0 ('57012'). That's 5 substrings. But the example only mentions "12", "012", "7012", "57012" — that's 4. It omits the single "2" because they say "additionally, all substrings that are just 1 non-zero digit are divisible by themselves. Since there are 6 such digits". The 6 single digits are '5','7','1','2','8','3'. So '2' is counted in the 6. So the 12 listed are the multi-digit ones. The 4 ending with 2 are "12", "012", "7012", "57012". The single "2" is separate. So total ending with 2: 4 + 1 = 5. In my count, I added for j=4 (d=2, k=1): freq[1][0] + 1. freq[1][0] is the number of substrings ending at 3 (j-1) that are divisible by 1. Since all are divisible by 1, freq[1][0] should be the number of substrings ending at 3, which is 4 (i=0,1,2,3: "5701", "