The problem requires counting substrings where the numeric value is divisible by its last non-zero digit. A brute-force approach checking all substrings is too slow ($O(N^2)$). Instead, we can iterate through each position as the end of a substring and count how many starting positions satisfy the condition. For a fixed end index `i`, we only care about the last digit `d = s[i]`. If `d` is '0', no substring ending at `i` is valid (since division by zero is undefined). If `d` is non-zero, we need to count how many substrings ending at `i` form a number divisible by `d`. We can maintain the current number formed by the substring ending at `i` modulo `d` as we iterate backwards or forwards. However, a more efficient $O(N)$ approach is to iterate `i` from 0 to n-1, treat `s[i]` as the last digit `d`. If `d` is '0', skip. Otherwise, we need to count `j <= i` such that `int(s[j:i+1]) % d == 0`. Since `int(s[j:i+1]) = int(s[j:i]) * 10 + d`, we can maintain the running value modulo `d` as we extend the substring to the left? Actually, iterating forward is better: for each `i`, let `d = s[i]`. If `d` is '0', continue. We want to count `j` such that `val(j, i) % d == 0`. Notice that `val(j, i) = val(j, i-1) * 10 + d`. This recurrence suggests we can iterate `i` from 0 to n-1, and for each `i`, if `s[i]` is not '0', we calculate how many `j` satisfy the condition. But calculating for each `i` naively is still slow.
Wait, let's re-evaluate. For a fixed `i` and `d = s[i]`, we want `val(j, i) % d == 0`.
`val(j, i) = (val(j, i-1) * 10 + d) % d`.
Actually, `val(j, i) % d = (val(j, i-1) * 10) % d`.
So if `val(j, i-1) * 10 % d == 0`, then the condition holds.
This implies that if we know the counts for `i-1`, we can update for `i`.
Specifically, let `count[d]` be the number of substrings ending at `i-1` divisible by `d`.
When moving to `i`, the new last digit is `d_new = s[i]`.
If `d_new` is '0', no substrings ending at `i` are valid.
If `d_new` is not '0', a substring `s[j:i]` is divisible by `d_new` if `int(s[j:i]) % d_new == 0`.
Note that `int(s[j:i]) = int(s[j:i-1]) * 10 + d_new`.
So `int(s[j:i]) % d_new = (int(s[j:i-1]) * 10) % d_new`.
This means `s[j:i]` is divisible by `d_new` if and only if `int(s[j:i-1]) * 10` is divisible by `d_new`.
This doesn't directly relate to divisibility by `d_new` of the previous substring.
Let's try a different perspective.
Iterate `i` from 0 to n-1. Let `d = s[i]`.
If `d == '0'`, continue.
We need to count `j` in `0..i` such that `int(s[j:i]) % d == 0`.
Let `curr = 0`. Iterate `j` from `i` down to `0`. `curr = (curr + d) % d`? No.
`val(j, i) = val(j+1, i) * 10 + s[j]`. This is hard to maintain backwards efficiently for all `j`.
Alternative: Iterate `i` from 0 to n-1. Maintain `rem[d]` = count of substrings ending at `i-1` that are divisible by `d`.
When moving to `i`, let `d_new = s[i]`.
For any `d` (where `d` is a digit 1-9), the substrings ending at `i` divisible by `d` are those where `val(j, i) % d == 0`.
`val(j, i) = val(j, i-1) * 10 + d_new`.
So `val(j, i) % d == (val(j, i-1) * 10 + d_new) % d`.
This equals 0 if `val(j, i-1) * 10 % d == -d_new % d`.
This seems complicated because `d` varies.
Let's reconsider the constraints and properties.
Total substrings is $N(N+1)/2$.
Maybe we can count invalid ones? No, condition is specific.
Let's go back to: For each `i`, `d = s[i]`. If `d != '0'`, we need to count `j` such that `int(s[j:i]) % d == 0`.
Let `current_val` be the number formed by `s[j:i]`.
As we decrease `j`, `current_val` grows.
Actually, we can iterate `i` from 0 to n-1.
Maintain an array `cnt` of size 10, where `cnt[k]` stores the number of substrings ending at the current position `i` that are divisible by `k`.
Wait, the divisor is the last digit. So for a substring ending at `i`, the divisor is fixed as `s[i]`.
So for a fixed `i`, we only care about divisibility by `s[i]`.
Let `d = s[i]`. If `d == '0'`, count is 0.
If `d != '0'`, we need to count `j` such that `int(s[j:i]) % d == 0`.
Let `x_j = int(s[j:i])`.
`x_j = x_{j+1} * 10 + s[j]`.
This recurrence is hard to invert.
However, notice that `x_j % d = (x_{j+1} * 10 + s[j]) % d`.
This doesn't help much unless we know `x_{j+1} % d`.
But `x_{j+1}` is the number `s[j+1:i]`. Its last digit is `s[i] = d`.
So `x_{j+1} % d` depends on the whole string `s[j+1:i]`.
Actually, there is a simpler observation.
`int(s[j:i]) % d == 0` is equivalent to `int(s[j:i])` being a multiple of `d`.
Since `d` is a single digit (1-9), we can just compute the value modulo `d` as we extend the substring to the left?
No, extending to the left increases the number of digits.
Let's try iterating `i` from 0 to n-1.
Let `d = s[i]`.
If `d == '0'`, we add 0 to total.
If `d != '0'`, we want to count `j` such that `int(s[j:i]) % d == 0`.
Let `rem = 0`. Iterate `j` from `i` down to `0`.
`rem = (rem + s[j]) % d`? No, that's for sum.
The number is `... s[j] s[j+1] ... s[i]`.
Value = `s[j]*10^(i-j) + ... + s[i]*10^0`.
This is hard to update incrementally from right to left without powers of 10.
But wait, we can iterate `i` from 0 to n-1 and maintain the current number modulo `d`? No, `d` changes.
Let's flip the loop.
Iterate `i` from 0 to n-1.
Let `d = s[i]`.
If `d == '0'`, continue.
We need to count `j` such that `int(s[j:i]) % d == 0`.
Let `curr = 0`.
Iterate `j` from `i` down to `0`.
`curr = (curr + s[j]) % d` is wrong.
Correct logic: `val(j, i) = val(j+1, i) * 10 + s[j]`.
So `val(j, i) % d = (val(j+1, i) * 10 + s[j]) % d`.
This requires knowing `val(j+1, i) % d`.
But `val(j+1, i)` is the substring `s[j+1:i]`.
Notice that for a fixed `i`, as we vary `j`, the divisor is always `d = s[i]`.
So we can just compute `val(j, i) % d` for all `j`? That's $O(N^2)$.
We need $O(N)$.
Is there a pattern?
`val(j, i) % d == 0`.
Let's look at the example "12936".
i=0, '1': "1" % 1 == 0. Count=1.
i=1, '2': "2" % 2==0, "12" % 2==0. Count=2.
i=2, '9': "9" % 9==0, "29" % 9=2, "129" % 9=3. Count=1.
i=3, '3': "3" % 3==0, "93" % 3==0, "293" % 3=2, "1293" % 3=0. Count=3.
i=4, '6': "6" % 6==0, "36" % 6==0, "936" % 6=0, "2936" % 6=2, "12936" % 6=0. Count=4.
Total = 1+2+1+3+4 = 11. Matches example.

Observation:
For a fixed `i` and `d=s[i]`, we want `val(j, i) % d == 0`.
`val(j, i) = val(j, i-1) * 10 + s[i]`? No, `val(j, i) = val(j, i-1) * 10 + s[i]` is true if `j <= i-1`.
Actually, `val(j, i) = val(j, i-1) * 10 + s[i]` is correct.
So `val(j, i) % d = (val(j, i-1) * 10 + d) % d = (val(j, i-1) * 10) % d`.
So `val(j, i) % d == 0` iff `val(j, i-1) * 10 % d == 0`.
This means `val(j, i-1)` must be divisible by `d / gcd(10, d)`.
Let `g = gcd(10, d)`. Then `d/g` is the reduced divisor.
We need `val(j, i-1)` to be divisible by `d/g`.
But `val(j, i-1)` is a substring ending at `i-1`.
This suggests we can maintain counts of substrings ending at `i-1` divisible by various numbers.
Let `cnt[k]` be the number of substrings ending at `i-1` that are divisible by `k`.
When moving to `i`, let `d = s[i]`.
The number of substrings ending at `i` divisible by `d` is the number of `j` such that `val(j, i-1) * 10 % d == 0`.
This is equivalent to `val(j, i-1) % (d / gcd(10, d)) == 0`.
Let `req = d / gcd(10, d)`.
Then the count for `i` is `cnt[req]`?
Wait, `cnt[req]` counts substrings ending at `i-1` divisible by `req`.
Yes! Because if `val(j, i-1)` is divisible by `req`, then `val(j, i-1) = k * req`.
Then `val(j, i) = k * req * 10 + d`.
We need `val(j, i) % d == 0`.
`k * req * 10 + d = k * (d/g) * 10 + d = k * d * (10/g) + d = d * (k * 10/g + 1)`.
This is clearly divisible by `d`.
So the number of valid substrings ending at `i` is exactly the number of substrings ending at `i-1` that are divisible by `d / gcd(10, d)`.
Let `g = gcd(10, d)`. `req = d // g`.
We need `cnt[req]`.
But wait, `cnt` array needs to be updated.
At step `i`, we calculate `new_cnt[d] = cnt[d // gcd(10, d)]`.
Then we update `cnt` for the next step.
But `cnt` array size? `d` is 1-9. So size 10 is enough.
Wait, `cnt[k]` stores count of substrings ending at `i-1` divisible by `k`.
When we move to `i`, we compute `count_i = cnt[d // gcd(10, d)]`.
Then we need to update `cnt` for `i`.
The new `cnt` array for `i` will have `cnt_new[k]` = number of substrings ending at `i` divisible by `k`.
For a specific `k`, `val(j, i) % k == 0`.
`val(j, i) = val(j, i-1) * 10 + d`.
So `val(j, i) % k == (val(j, i-1) * 10 + d) % k`.
This depends on `val(j, i-1) % k`.
This seems to require iterating all `k`?
Actually, we only need `cnt[d]` for the next step?
No, for step `i+1`, we will need `cnt[d_next // gcd(10, d_next)]`.
So we need to maintain `cnt` for all possible divisors 1-9.
Algorithm:
Initialize `cnt` array of size 10 with 0s. `cnt[k]` = count of substrings ending at current position divisible by `k`.
Total = 0.
Iterate `i` from 0 to n-1:
  `d = int(s[i])`
  If `d == 0`:
    `cnt` becomes all 0s?
    Substrings ending at `i` are "0", "x0", etc.
    Divisor is 0, so none are valid.
    So `cnt` for next step should be all 0s?
    Yes, because no substring ending at `i` is divisible by any `k` (since divisor is 0, condition undefined, so count 0).
    Wait, the definition is "divisible by their non-zero last digit".
    If last digit is 0, it's not counted.
    So for the next step `i+1`, the substrings ending at `i` are not valid for any divisor?
    Actually, the `cnt` array represents "number of substrings ending at `i` that are divisible by `k`".
    If `s[i] == '0'`, then for any `k`, `val(j, i) % k` might be 0, but the condition "divisible by last digit" fails because last digit is 0.
    So we don't add to total.
    And for the next step, do we use these substrings?
    The recurrence `val(j, i+1) = val(j, i) * 10 + s[i+1]` holds regardless of whether `s[i]` was 0 or not.
    The condition for `i+1` is divisibility by `s[i+1]`.
    So we need `val(j, i) * 10 % s[i+1] == 0`.
    This depends on `val(j, i)`.
    So even if `s[i] == '0'`, `val(j, i)` exists and has a value.
    We just don't count it in the total for `i`.
    But we need to maintain `cnt` for future steps.
    So `cnt[k]` should be `count of j such that val(j, i) % k == 0`.
    If `s[i] == '0'`, then `val(j, i) = val(j, i-1) * 10 + 0 = val(j, i-1) * 10`.
    So `val(j, i) % k == (val(j, i-1) * 10) % k`.
    So `cnt_new[k] = count of j such that val(j, i-1) * 10 % k == 0`.
    This is `count of j such that val(j, i-1) % (k / gcd(10, k)) == 0`.
    So `cnt_new[k] = cnt_old[k // gcd(10, k)]`.
    This works even if `s[i] == '0'`.
    And if `s[i] != '0'`, then `cnt_new[d]` (for the specific `d=s[i]`) is added to total?
    No, the total for `i` is the number of substrings ending at `i` divisible by `s[i]`.
    This is `cnt_new[s[i]]`?
    Let's trace.
    `cnt[k]` at step `i` (before update) is count of substrings ending at `i-1` divisible by `k`.
    We want to compute `cnt_new[k]` for step `i`.
    `val(j, i) = val(j, i-1) * 10 + s[i]`.
    `val(j, i) % k == (val(j, i-1) * 10 + s[i]) % k`.
    This is not simply related to `cnt_old` unless `s[i] == 0`.
    If `s[i] == 0`, `val(j, i) = val(j, i-1) * 10`.
    Then `val(j, i) % k == 0` iff `val(j, i-1) * 10 % k == 0`.
    So `cnt_new[k] = cnt_old[k // gcd(10, k)]`.
    If `s[i] != 0`, then `val(j, i) % k == (val(j, i-1) * 10 + s[i]) % k`.
    This is not a simple lookup from `cnt_old`.
    However, we only need `cnt_new[s[i]]` to add to the total?
    No, we need `cnt_new[k]` for all `k` for future steps.
    But calculating `cnt_new[k]` for all `k` for each `i` is $O(10 \cdot N)$, which is $O(N)$.
    How to compute `cnt_new[k]` efficiently?
    `cnt_new[k]` = number of `j` such that `val(j, i) % k == 0`.
    `val(j, i) = val(j, i-1) * 10 + s[i]`.
    So `val(j, i) % k == 0` iff `val(j, i-1) * 10 % k == -s[i] % k`.
    This means `val(j, i-1) % k` must be a specific value `r = (-s[i]) * inv(10) % k`?
    Only if 10 is invertible mod `k`.
    If `gcd(10, k) > 1`, then `10*x % k == C` might have 0 or multiple solutions.
    This seems complicated.
    Let's re-read the problem. "Return the number of substrings of s divisible by their non-zero last digit."
    Maybe we don't need to maintain `cnt` for all `k`.
    Notice that for step `i`, we only care about `s[i]`.
    But for step `i+1`, we need `val(j, i)`.
    Is there a simpler way?
    What if we iterate `i` and maintain `curr_val % d` for all `d`?
    No.
    Let's reconsider the recurrence for `s[i] == 0`.
    If `s[i] == 0`, `val(j, i) = val(j, i-1) * 10`.
    So `val(j, i) % k == 0` iff `val(j, i-1) % (k/gcd(10, k)) == 0`.
    So `cnt_new[k] = cnt_old[k // gcd(10, k)]`.
    This is easy.
    If `s[i] != 0`, let `d = s[i]`.
    We need `cnt_new[k]` for all `k`.
    `val(j, i) % k == 0` iff `val(j, i-1) * 10 % k == -d % k`.
    Let `target = (-d) % k`.
    We need to count `j` such that `val(j, i-1) * 10 % k == target`.
    This is equivalent to `val(j, i-1) % k` being in some set of values.
    Specifically, `val(j, i-1) % k` must be `x` such that `10*x % k == target`.
    If `gcd(10, k) == 1`, there is a unique solution `x = target * inv(10) % k`.
    Then `cnt_new[k] = cnt_old[x]`.
    If `gcd(10, k) > 1`, say `g = gcd(10, k)`.
    Then `10*x % k == target` has solutions only if `target % g == 0`.
    If so, there are `g` solutions modulo `k`.
    The solutions are `x0, x0 + k/g, x0 + 2k/g, ...`
    So `cnt_new[k]` is the sum of `cnt_old[x]` for all such `x`.
    This is still $O(k)$ per `k`, so $O(10^2)$ per step, which is fine.
    So the algorithm is:
    Initialize `cnt` array of size 10 with 0s.
    Total = 0.
    For `i` in 0..n-1:
      `d = int(s[i])`
      `new_cnt` = [0]*10
      For `k` in 1..9:
        `target = (-d) % k`
        `g = gcd(10, k)`
        If `target % g != 0`:
          `new_cnt[k] = 0`
        Else:
          # Find one solution x0
          # 10*x0 = target (mod k)
          # Let k = g * m, 10 = g * n. gcd(n, m) = 1.
          # n * x0 = target/g (mod m)
          # x0 = (target/g) * inv(n, m) (mod m)
          # Then solutions are x0 + t*m for t in 0..g-1.
          `m = k // g`
          `n = 10 // g`
          `rhs = target // g`
          `inv = pow(n, -1, m)`
          `x0 = (rhs * inv) % m`
          `count = 0`
          For `t` in 0..g-1:
            `x = x0 + t * m`
            `count += cnt[x]`
          `new_cnt[k] = count`
      # Add to total if d != 0
      If `d != 0`:
        Total += new_cnt[d]
      `cnt` = `new_cnt`
    Return Total.

    Complexity: $N \times 10 \times 10 = 100N$, which is $O(N)$.
    Constraints $N=10^5$, so $10^7$ ops, well within time limit.