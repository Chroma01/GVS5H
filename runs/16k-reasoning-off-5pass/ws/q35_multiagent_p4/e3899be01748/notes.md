
## ideation
The core difficulty is efficiently counting substrings `s[i..j]` such that the integer value of the substring is divisible by its last digit `d = int(s[j])`, where `d != 0`. A naive $O(N^2)$ approach will time out for $N=10^5$.

The key insight is to process each possible last digit `d` (from 1 to 9) separately. For a fixed `d`, we only care about substrings ending at positions `j` where `s[j] == d`. For such a substring `s[i..j]`, the condition is:
`int(s[i..j]) % d == 0`.

We can express the value of the substring `s[i..j]` as:
`val(i, j) = sum_{k=i}^{j} int(s[k]) * 10^{j-k}`.

This can be rewritten modulo `d` as:
`val(i, j) % d = (10^j % d) * (sum_{k=i}^{j} int(s[k]) * 10^{-k} % d) % d`.

Let `P[j] = sum_{k=0}^{j-1} int(s[k]) * 10^{-k} % d` be a prefix sum array (with `P[0]=0`). Then:
`sum_{k=i}^{j} int(s[k]) * 10^{-k} % d = (P[j+1] - P[i]) % d`.

So the condition becomes:
`(10^j % d) * (P[j+1] - P[i]) % d == 0`.

Since `d` is coprime to 10 (as `d` is 1-9, and we handle 0 separately by skipping), `10^j % d` is invertible modulo `d` (unless `d=1`, in which case everything is divisible, but 1 is coprime to 10 too). Actually, for `d=1`, every substring ending in '1' is divisible by 1, so we just count all such substrings. For `d` in {2,3,4,5,6,7,8,9}, we need to check if `(P[j+1] - P[i]) % d == 0`, which means `P[i] == P[j+1] % d`.

Therefore, for each `d` from 1 to 9:
1. Precompute powers of 10 mod `d` and their modular inverses (or just compute the prefix sums directly using the formula with modular inverse of 10 mod `d`).
2. Iterate through the string, maintaining a frequency array of prefix sums mod `d`.
3. For each position `j` where `s[j] == d`, the number of valid starting positions `i` is the frequency of `P[j+1] % d` in the prefix sums seen so far (including `P[0]`).

Special case: `d=1`. Since every number is divisible by 1, we just count all substrings ending in '1'. This fits the general framework if we note that `P[j+1] - P[i]` mod 1 is always 0, so we just add the count of all previous prefixes (which is `j+1` if we include `P[0]`... actually, we need to be careful with indices).

Actually, a simpler approach for each `d`:
- Initialize `count = 0`.
- Initialize a frequency map `freq` for remainders mod `d`, starting with `freq[0] = 1` (for the empty prefix before index 0).
- Maintain a running prefix sum `current_prefix` mod `d`.
- Iterate `j` from 0 to n-1:
  - Update `current_prefix` by adding `int(s[j]) * inv(10)^j`? No, it's easier to build the prefix sum as: `current_prefix = (current_prefix + int(s[j]) * pow(10, -j, d)) % d`. But computing modular inverse for each step is costly.
  
Alternative: Use the property that `val(i, j) = val(i, j-1)*10 + s[j]`. But this depends on `i`. 

Better approach: For each `d`, iterate `j` from 0 to n-1. If `s[j] == d`, then we want to count `i` such that `int(s[i..j]) % d == 0`. We can compute `int(s[i..j]) % d` incrementally from right to left? No, that's $O(N)$ per `j`, leading to $O(N^2)$.

The prefix sum with modular inverse approach is $O(N)$ per `d`, total $O(9N) = O(N)$.
Steps for each `d` in 1..9:
1. Compute `inv10 = pow(10, -1, d)` if `gcd(10,d)==1`. For `d=1`, `inv10=0` or handle separately. For `d=5`, `gcd(10,5)=5!=1`, so 10 is not invertible mod 5. Similarly for 2,4,6,8.
   - For `d` coprime to 10 (1,3,7,9), use the prefix sum method with modular inverse.
   - For `d` not coprime to 10 (2,4,5,6,8), we need a different approach. Note that for these `d`, the divisibility rule depends on the last few digits. Specifically:
     - `d=2,5`: A number is divisible by 2 (or 5) if its last digit is 0 (or 0,5). But here the last digit is fixed to `d`. So for `d=2`, last digit is 2, which is even, so any number ending in 2 is divisible by 2? No, e.g., 12 is divisible by 2, 22 is, but 32 is. Actually, a number is divisible by 2 if its last digit is even. Since the last digit is 2, which is even, EVERY number ending in 2 is divisible by 2. So for `d=2`, all substrings ending in '2' are valid.
     - Similarly, for `d=5`, every number ending in 5 is divisible by 5.
     - For `d=4`: A number is divisible by 4 if the number formed by its last two digits is divisible by 4. So we need `int(s[j-1..j]) % 4 == 0`. We can check this for each `j` where `s[j]=='4'`.
     - For `d=6`: A number is divisible by 6 if it is divisible by 2 and 3. Divisible by 2: last digit even (4 is even, so ok). Divisible by 3: sum of digits divisible by 3. So for `d=6`, we need sum of digits of `s[i..j]` divisible by 3. We can use prefix sums of digits mod 3.
     - For `d=8`: A number is divisible by 8 if the number formed by its last three digits is divisible by 8. So we check `int(s[j-2..j]) % 8 == 0`.

So the plan:
- For `d` in {1,3,7,9}: Use prefix sums with modular inverse of 10 mod `d`.
- For `d` in {2,5}: All substrings ending in `d` are valid. Count them.
- For `d` in {4}: Check if the last two digits form a number divisible by 4.
- For `d` in {6}: Check if sum of digits is divisible by 3 (since last digit is even, divisibility by 2 is automatic).
- For `d` in {8}: Check if the last three digits form a number divisible by 8.

This handles all cases in $O(N)$ time.

## worker: Implement the solution in Python using the categor
The solution handles each digit `d` from 1 to 9 separately with optimized logic:
1. **d=1**: Every substring ending in '1' is valid. Count is `i+1` for each occurrence at index `i`.
2. **d=2,5**: Any number ending in 2 is even (divisible by 2), and any number ending in 5 is divisible by 5. Count is `i+1` for each occurrence at index `i`.
3. **d=4**: A number is divisible by 4 if the number formed by its last two digits is divisible by 4. For each `j` where `s[j]=='4'`, if `j==0`, only one substring ("4") is valid. If `j>=1`, check if `int(s[j-1..j]) % 4 == 0`. If true, all `j+1` substrings ending at `j` are valid.
4. **d=8**: A number is divisible by 8 if the number formed by its last three digits is divisible by 8. For `j<2`, handle specially (check 1-digit or 2-digit numbers). For `j>=2`, check last three digits. If valid, all `j+1` substrings ending at `j` are valid.
5. **d=6**: Divisible by 6 iff divisible by 2 and 3. Last digit 6 ensures divisibility by 2. For divisibility by 3, use prefix sums of digits mod 3. For each `j` where `s[j]=='6'`, count previous indices `i` such that `prefix_sum[i] == prefix_sum[j+1] % 3`.
6. **d=3,7,9**: Use the prefix sum method with modular inverse of 10 mod `d`. Since `gcd(10,d)=1` for these `d`, 10 is invertible. Maintain a running prefix sum of `digits[k] * inv10^k mod d`. For each `j` where `s[j]==d`, the number of valid starting positions is the frequency of `current_prefix` in the frequency array.

All cases are handled in $O(N)$ time per digit, leading to an overall $O(N)$ solution.
