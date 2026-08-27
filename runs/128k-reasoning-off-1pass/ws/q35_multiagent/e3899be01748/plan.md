The problem asks us to count substrings divisible by their non-zero last digit. A brute-force approach checking all substrings is O(N^2) which is too slow for N=10^5. We need a more efficient approach.
Key insight: For a substring ending at index `j` with last digit `d` (where `d != 0`), the substring `s[i..j]` represents a number. We need to check if this number is divisible by `d`.
Since `d` is a single digit (1-9), we can iterate over each possible last digit `d` from 1 to 9. For each `d`, we consider only substrings ending at positions where `s[j] == d`.
For a fixed `d`, we want to count indices `i <= j` such that the number formed by `s[i..j]` is divisible by `d`.
The number formed by `s[i..j]` can be computed as: `num(i, j) = num(0, j) - num(0, i-1) * 10^(j-i+1)`. However, a simpler way is to build the number from left to right or right to left.
Actually, a better approach: Iterate `j` from 0 to n-1. If `s[j]` is '0', skip (as last digit is 0, not considered). If `s[j]` is `d` (1-9), we need to count `i` such that `int(s[i..j]) % d == 0`.
We can maintain remainders. But the length of substring varies, so the power of 10 changes.
Alternative: Since `d` is small (1-9), we can use the property that `int(s[i..j]) % d == 0`.
Let's precompute prefix numbers modulo `d`? But `d` changes.
Actually, for each `j` with `s[j]=d`, we can iterate `i` backwards from `j` down to `max(0, j-8)`? No, because the number can be large. But note: `int(s[i..j]) % d` depends on the whole substring.
Wait, if we fix `d`, we can process all `j` where `s[j]==d`. For each such `j`, we want to count `i` such that `int(s[i..j]) % d == 0`.
We can compute the value of `s[i..j]` incrementally as we extend `i` to the left. But doing this for every `j` is still O(N^2) in worst case (e.g., all 1s).
However, note that if the substring length is large, the number is huge. But we only care about modulo `d`.
We can use the fact that `int(s[i..j]) = int(s[i..j-1]) * 10 + int(s[j])`. This doesn't help directly for varying `i`.
Better: `int(s[i..j]) = int(s[0..j]) - int(s[0..i-1]) * 10^(j-i+1)`.
So `int(s[i..j]) % d == 0` iff `int(s[0..j]) % d == (int(s[0..i-1]) * 10^(j-i+1)) % d`.
This seems complex due to the varying power of 10.
Simpler observation: Since `d` is small, we can just iterate `i` from `j` down to `max(0, j-8)`? No, because 10^k mod d cycles with period at most `d` (actually Euler's totient, but for small d, period is small). But the value `int(s[i..j])` depends on all digits.
Actually, the constraints allow O(N * 9) if we can compute the remainder efficiently.
We can precompute prefix sums of digits? No.
Let's try: For each `d` in 1..9, iterate `j` from 0 to n-1. If `s[j] != str(d)`, skip. Else, we need to count `i` such that `int(s[i..j]) % d == 0`.
We can compute `int(s[i..j])` by starting from `i=j` and going left, updating the remainder. But this is O(N) per `j` in worst case, leading to O(N^2).
However, note that if the substring length exceeds a certain bound, the remainders might cycle? Not necessarily for arbitrary digits.
But wait: The maximum length we need to check? Actually, no bound.
Alternative efficient approach: Use the formula `int(s[i..j]) % d`. We can precompute `prefix_val[j] = int(s[0..j]) % d` and `pow10[k] = 10^k % d`. Then `int(s[i..j]) % d = (prefix_val[j] - prefix_val[i-1] * pow10[j-i+1]) % d`. This requires `prefix_val` and `pow10` for each `d`.
For each `d` in 1..9:
  Precompute `prefix_val` array for modulus `d`.
  Precompute `pow10` array for modulus `d`.
  For each `j` where `s[j] == str(d)`:
    For each `i` from 0 to `j`:
       Check if `(prefix_val[j] - prefix_val[i-1] * pow10[j-i+1]) % d == 0`. (Handle i=0 separately).
This is still O(N^2) per `d` in worst case.
But note: We only need to check `i` such that the substring is valid. 
Actually, we can optimize: For a fixed `d`, and fixed `j`, we want to count `i` such that `prefix_val[i-1] * pow10[j-i+1] % d == prefix_val[j] % d`.
This is still hard because `pow10[j-i+1]` depends on `i`.
Given the constraints and typical CP tricks, perhaps the intended solution is O(N * 9) by iterating backwards from `j` for a limited number of steps? No.
Let's reconsider: The number of substrings ending at `j` with last digit `d` is `j+1`. Summing over all `j` is O(N^2).
But note: For `d=1`, every number is divisible by 1. So all substrings ending in '1' are valid. Count = number of '1's * (average length)? No, for each '1' at `j`, all `i` from 0 to `j` are valid. So count += j+1.
For `d=2`, 5, even digits: divisibility by 2 depends on last digit (which is fixed to `d`), so if `d` is even, then any number ending in `d` is divisible by `d` only if the number formed is divisible by `d`. For `d=2`, any number ending in 2 is even, so divisible by 2. Similarly for `d=5`, any number ending in 5 is divisible by 5. For `d=4`, 6, 8, 9: not all numbers ending in `d` are divisible by `d`.
For `d=1, 2, 5`: All substrings ending in `d` are valid.
For `d=3, 6, 9`: Divisibility by 3/9 depends on sum of digits. Divisibility by 6 requires divisible by 2 and 3.
For `d=4, 8`: Divisibility by 4/8 depends on last few digits.
Actually, for `d=4`, a number is divisible by 4 if the number formed by last two digits is divisible by 4. So for `d=4`, we only need to check the last two digits? No, the last digit is fixed to 4. So we check if `int(s[j-1..j]) % 4 == 0`. If yes, then any substring ending at `j` with last digit 4 is divisible by 4? No, that's only for the last two digits of the entire number. The rule "divisible by 4 iff last two digits form a number divisible by 4" applies to the whole number. So yes, for `d=4`, `int(s[i..j]) % 4 == 0` iff `int(s[j-1..j]) % 4 == 0` (if `j-i+1 >= 2`). If length is 1, then `s[j]` itself must be divisible by 4, i.e., `d=4` is divisible by 4, which is true. So for `d=4`, if `int(s[j-1..j]) % 4 == 0` or length is 1, then all substrings ending at `j` are valid? No, the rule is for the entire number. So if the number formed by the last two digits is divisible by 4, then the whole number is divisible by 4. So for `d=4`, if `j>=1` and `int(s[j-1..j]) % 4 == 0`, then all substrings ending at `j` are valid. If `j==0`, then only the single digit substring is valid (and it is, since 4%4==0). If `j>=1` and `int(s[j-1..j]) % 4 != 0`, then no substring of length >=2 is valid, but the single digit substring `s[j]` is valid.
Similarly for `d=8`: Divisible by 8 iff last three digits form a number divisible by 8.
For `d=3, 9`: Divisible by 3/9 iff sum of digits is divisible by 3/9.
For `d=6`: Divisible by 6 iff divisible by 2 and 3. Since last digit is 6 (even), it's always divisible by 2. So just check sum of digits divisible by 3.
For `d=7`: No simple rule. Must check full number. But we can compute remainder incrementally.

So, for `d=1,2,5`: All substrings ending in `d` are valid.
For `d=4,8`: Use last 2/3 digits rule.
For `d=3,6,9`: Use sum of digits rule.
For `d=7`: Must check full number. But we can compute remainder from right to left? Or left to right?
Actually, for `d=7`, we can iterate `i` from `j` down to `max(0, j-8)`? No, the period of 10^k mod 7 is 6. So the remainder pattern repeats every 6 digits? Not exactly, because the digits are arbitrary.
But for `d=7`, we can compute the remainder of `s[i..j]` by building from `i` to `j`. But that's O(N) per `j`.
However, note that for `d=7`, we can precompute prefix remainders? 
`int(s[i..j]) % 7 = (prefix[j] - prefix[i-1] * 10^(j-i+1)) % 7`.
We can store counts of `prefix[i-1] * 10^(- (j-i+1))`? This is getting complicated.
Given the complexity, and that only `d=7` is hard, and `d=7` appears at most N times, and for each we might need to check many `i`, but actually, we can compute the remainder of `s[i..j]` for `i` from `j` down to `0` in O(1) per `i` by maintaining the current remainder. But this is O(N) per `j`, leading to O(N^2).
But note: The constraints are 10^5, so O(N^2) is TLE.
We must find an O(N) or O(N log N) solution.
For `d=7`, we can use the formula with prefix sums and powers of 10. We want to count `i` such that `(prefix[j] - prefix[i-1] * pow10[j-i+1]) % 7 == 0`.
This is `prefix[i-1] * pow10[j-i+1] % 7 == prefix[j] % 7`.
Let `k = j-i+1`, then `i-1 = j-k`. So we need `prefix[j-k] * pow10[k] % 7 == prefix[j] % 7`.
For a fixed `j`, as `k` varies, `pow10[k]` cycles with period 6. So we can group indices `i-1` by `k mod 6` and by `prefix[i-1]`.
This is doable but complex.
Given the time, I'll implement the O(N^2) solution for small cases and hope that the test cases are weak, or use the optimized rules for d=1,2,4,5,8,9 and a simple loop for d=3,6,7.
Actually, for d=3,6,9, we can use prefix sums of digits.
For d=7, we can use the prefix remainder method with a hash map to store counts of `(prefix[i-1] * pow10[-k])` but this is tricky.
I'll implement a solution that handles each d separately with the appropriate rule, and for d=7, I'll use a loop but break early if possible? No.
Let's just implement the straightforward O(N^2) for d=7 and see. But it will TLE.
Better: For d=7, use the formula with prefix remainders and a frequency array for each residue class of `prefix[i-1]` for each `k mod 6`.
This is too complex for this format. I'll provide a solution that uses the rules for d=1,2,4,5,8,9 and for d=3,6,7, I'll use a loop but optimize by noting that for d=3,6,9, we can use prefix sums of digits. For d=7, I'll use the prefix remainder method with a map.