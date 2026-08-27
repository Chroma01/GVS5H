The problem requires counting substrings divisible by their last non-zero digit. A brute-force approach checking all $O(N^2)$ substrings will be too slow given $N \le 10^5$. Instead, we can iterate through each position in the string as the end of a substring. For each ending position, we only need to check substrings ending with a non-zero digit (since division by zero is undefined and the problem implies divisibility by the *non-zero* last digit; if the last digit is '0', that specific substring ending there doesn't count towards the "divisible by last digit" criteria in the standard sense unless the problem implies skipping '0' endings, but the examples show '0' endings are excluded from the count because they can't be divided by 0). Actually, re-reading the examples: Example 1 says "29", "129", etc. are NOT divisible. Example 2 lists substrings ending in '1', '2', '3', '8' as valid. Substrings ending in '0' are never listed as valid in the explanation because you cannot divide by 0. So, for each index `i`, if `s[i]` is '0', it contributes 0. If `s[i]` is non-zero, we need to count how many starting positions `j` (where $0 \le j \le i$) make the substring `s[j:i+1]` divisible by `int(s[i])`. Since the number of substrings ending at `i` is $i+1$, and checking each one is slow, we need a faster way. However, notice the constraints and the nature of divisibility. For a fixed last digit $d$, we need the number formed by `s[j:i+1]` to be divisible by $d$. This is equivalent to `num % d == 0`. Calculating the number for every substring is $O(N^2)$. Is there a pattern?
Wait, let's re-evaluate the complexity. $N=10^5$. $O(N^2)$ is definitely TLE.
Let's look at the constraints on the last digit. The last digit $d \in \{1, 2, ..., 9\}$.
For a fixed ending position `i` and fixed last digit `d = s[i]`, we need to count `j` such that `val(s[j:i+1]) % d == 0`.
`val(s[j:i+1]) = val(s[j:i]) * 10 + d`.
So we need `(val(s[j:i]) * 10 + d) % d == 0`.
Since `d % d == 0`, this simplifies to `(val(s[j:i]) * 10) % d == 0`.
This means `val(s[j:i]) * 10` must be divisible by `d`.
Let $K = \text{val}(s[j:i])$. We need $10K \equiv 0 \pmod d$.
This depends on $d$.
If $d=1$, always true. Count = $i+1$.
If $d=5$, $10K$ is always divisible by 5. Count = $i+1$.
If $d=2$, $10K$ is always divisible by 2. Count = $i+1$.
If $d=3$, we need $10K \equiv K \equiv 0 \pmod 3$. So $K$ must be divisible by 3.
If $d=4$, we need $10K \equiv 2K \equiv 0 \pmod 4 \implies K \equiv 0 \pmod 2$.
If $d=6$, we need $10K \equiv 4K \equiv 0 \pmod 6 \implies 2K \equiv 0 \pmod 3 \implies K \equiv 0 \pmod 3$.
If $d=7$, we need $10K \equiv 3K \equiv 0 \pmod 7 \implies K \equiv 0 \pmod 7$.
If $d=8$, we need $10K \equiv 2K \equiv 0 \pmod 8 \implies K \equiv 0 \pmod 4$.
If $d=9$, we need $10K \equiv K \equiv 0 \pmod 9 \implies K \equiv 0 \pmod 9$.

So for each `i`, let `d = int(s[i])`. If `d == 0`, skip.
Otherwise, we need to count `j` in `0..i` such that the number formed by `s[j:i]` satisfies a specific modulo condition based on `d`.
The number `val(s[j:i])` is the number formed by the prefix ending at `i-1` minus the prefix ending at `j-1`? No, it's not a simple subtraction because of powers of 10.
`val(s[j:i]) = (val(s[0:i+1]) - val(s[0:j]) * 10^(i-j+1))`? No.
Actually, `val(s[j:i])` is the number formed by digits from `j` to `i-1`.
Let $P[k]$ be the integer value of the prefix $s[0:k]$. Then `val(s[j:i])` is not simply related to $P$ unless we consider modular arithmetic.
We need `val(s[j:i]) % m == 0` where `m` is derived from `d`.
Specifically, we need `(val(s[j:i]) * 10) % d == 0`.
Let $X = \text{val}(s[j:i])$. We need $10X \equiv 0 \pmod d$.
This is equivalent to $X \equiv 0 \pmod {d / \gcd(10, d)}$.
Let $g = \gcd(10, d)$. Then we need $X \equiv 0 \pmod {d/g}$.
So for each `i`, we need to count `j` such that the number formed by `s[j:i]` is divisible by $M = d/g$.
Note that `s[j:i]` is the substring from `j` to `i-1`. If `j=i`, the substring is empty? No, the substring is `s[j:i+1]`.
The condition was: `val(s[j:i+1]) % d == 0`.
`val(s[j:i+1]) = val(s[j:i]) * 10 + d`.
So `(val(s[j:i]) * 10 + d) % d == 0` -> `(val(s[j:i]) * 10) % d == 0`.
Here `val(s[j:i])` is the number formed by `s[j...i-1]`. If `j=i`, this part is 0 (empty prefix before the last digit).
So if `j=i`, `val` is 0, $0 \equiv 0$, so it works.
For `j < i`, `val(s[j:i])` is the number formed by the suffix of the prefix `s[0:i]` starting at `j`.
Let $P[k]$ be the integer value of $s[0:k]$ modulo some large number? No, we need exact divisibility.
Wait, if the substring `s[j:i]` is very long, the number is huge. We cannot compute it directly.
However, we only care about `val(s[j:i]) % M == 0`.
Let $L = i-j$. The value is $\sum_{k=0}^{L-1} s[j+k] \cdot 10^{L-1-k}$.
This looks like we need to count indices `j` such that a suffix of the prefix `s[0:i]` is divisible by `M`.
This seems hard to do in $O(1)$ per `i` without precomputation or a specific property.
Is there a simpler observation?
Look at the constraints again. $N=10^5$.
Maybe the number of valid `j` is not that hard to count?
Actually, let's re-read the problem carefully. "Return the number of substrings of s divisible by their non-zero last digit."
If the last digit is '0', the substring is NOT divisible by its last digit (division by zero). So we ignore substrings ending in '0'.
For substrings ending in `d != 0`, we need `val % d == 0`.
Let's reconsider the condition: `(val(s[j:i]) * 10 + d) % d == 0`.
This is always true if `val(s[j:i]) * 10` is a multiple of `d`.
As derived, this is equivalent to `val(s[j:i])` being a multiple of `d / gcd(10, d)`.
Let $M_d = d / \gcd(10, d)$.
We need to count `j` in `0..i` such that the number formed by `s[j:i]` is divisible by $M_d$.
Note that `s[j:i]` is the substring from `j` to `i-1`.
If `j=i`, the substring is empty (value 0), which is divisible by any $M_d$. So `j=i` is always a solution.
For `j < i`, we need the number formed by `s[j...i-1]` to be divisible by $M_d$.
Let $S = s[0:i]$. We are looking for suffixes of $S$ (excluding the last char which is `d`) that are divisible by $M_d$.
This is equivalent to finding `j` such that `int(s[j:i]) % M_d == 0`.
This still feels like $O(N)$ per `i` in worst case if we scan.
Is it possible that for most `d`, the condition is very loose?
$d=1, 5$: $M_d = 1$. Any number is divisible by 1. So all `j` work. Count = $i+1$.
$d=2$: $M_d = 2/2 = 1$. All `j` work. Count = $i+1$.
$d=4$: $M_d = 4/2 = 2$. We need `int(s[j:i])` even.
$d=6$: $M_d = 6/2 = 3$. We need `int(s[j:i])` divisible by 3.
$d=8$: $M_d = 8/2 = 4$. We need `int(s[j:i])` divisible by 4.
$d=3$: $M_d = 3/1 = 3$. Divisible by 3.
$d=7$: $M_d = 7/1 = 7$. Divisible by 7.
$d=9$: $M_d = 9/1 = 9$. Divisible by 9.

So for $d \in \{1, 2, 5\}$, the answer for position `i` is simply `i+1`.
For other $d$, we need to count suffixes of `s[0:i]` divisible by $M_d$.
Can we compute this efficiently?
Notice that `int(s[j:i])` is the number formed by digits.
If we maintain the current prefix value modulo $M_d$, say `curr`, then `int(s[j:i])` is not directly `curr`.
`int(s[j:i]) = (int(s[0:i]) - int(s[0:j]) * 10^(i-j))`.
So we need `(P[i] - P[j] * 10^(i-j)) % M_d == 0`.
This depends on `j` in a complex way due to the power of 10.
However, note that if the length of the substring `s[j:i]` is large enough, the number might be divisible by $M_d$ often? No.
Wait, maybe there's a constraint I missed or a property of the test cases?
Or maybe the number of such `j` is small? No, in "11111", all substrings ending in 1 are valid.
Let's re-examine the logic.
Is it possible that the problem implies something else?
"divisible by their non-zero last digit".
If the last digit is 0, we skip.
If the last digit is non-zero, we check divisibility.
The key insight might be that for $d \in \{1, 2, 5\}$, we count all.
For others, maybe we can't do $O(N)$ per `i`.
But wait, if $d=3$, we need `int(s[j:i]) % 3 == 0`.
`int(s[j:i]) % 3` is equal to `sum(digits) % 3`.
So we need the sum of digits from `j` to `i-1` to be divisible by 3.
This can be solved with prefix sums of digits!
Let `pref[k] = sum(s[0:k])`. Then `sum(s[j:i]) = pref[i] - pref[j]`.
We need `pref[i] - pref[j] == 0 mod 3`.
So `pref[j] == pref[i] mod 3`.
We can count frequencies of `pref[j] % 3` as we iterate `i`.
Similarly for $d=9$, divisibility by 9 is also sum of digits mod 9.
What about $d=4$? We need `int(s[j:i]) % 4 == 0`.
A number is divisible by 4 if the number formed by its last 2 digits is divisible by 4.
So we only need to check the last 2 digits of `s[j:i]`.
If `i-j+1 < 2`, i.e., length 1, then `s[j]` must be divisible by 4.
If length >= 2, `int(s[i-2:i])` (the last 2 digits of the substring) must be divisible by 4.
Wait, `s[j:i]` ends at `i-1`. So the last 2 digits are `s[i-2]` and `s[i-1]`.
These are fixed for a given `i`!
So if `i >= 1`, and we consider substrings of length >= 2 ending at `i-1` (which means starting at `j <= i-2`), the divisibility by 4 depends ONLY on `s[i-2]` and `s[i-1]`.
If `int(s[i-2:i]) % 4 == 0`, then ALL `j` such that `i-2 >= j` satisfy the condition.
If not, then NO `j` (with length >= 2) satisfies it.
What about length 1? `j = i-1`. Then we check `s[i-1] % 4 == 0`.
So for $d=4$, we can count in $O(1)$.
Similarly for $d=8$, divisibility by 8 depends on the last 3 digits.
So we check `s[i-3:i]`. If divisible, all `j <= i-3` work. Plus check `j=i-2` (last 2 digits), `j=i-1` (last 1 digit).
For $d=6$, we need `int(s[j:i]) % 3 == 0`. Same as $d=3$, use digit sum.
For $d=7$, divisibility by 7 does not have a simple digit-sum or last-k-digits rule.
However, $d=7$ is the only one left without a simple rule.
Is it possible that for $d=7$, the number of valid substrings is small or there's a trick?
Or maybe the constraints allow $O(N)$ total if we handle $d=7$ specially?
Wait, if $d=7$, we need `int(s[j:i]) % 7 == 0`.
This is `val(s[j:i]) % 7 == 0`.
We can maintain a list of `j` such that `val(s[j:i]) % 7 == 0`?
As we move from `i` to `i+1`, the values change.
`val(s[j:i+1]) = val(s[j:i]) * 10 + s[i+1]`.
This doesn't help directly for the condition `val(s[j:i]) % 7 == 0`.
But wait, the condition is on `s[j:i]` (the part before the last digit `d`).
Let $V_j = \text{val}(s[j:i])$. We need $V_j \equiv 0 \pmod 7$.
When we move from `i` to `i+1`, the new substring ends at `i`. The previous substrings `s[j:i]` become `s[j:i+1]`? No.
The set of substrings ending at `i` is $\{s[j:i+1] \mid 0 \le j \le i\}$.
The condition is on the prefix part $s[j:i]$.
Let $W_j = \text{val}(s[j:i])$.
Then $W_j = \text{val}(s[j:i-1]) * 10 + s[i-1]$.
This recurrence allows us to update $W_j$ for all $j$.
But we need to count how many $W_j \equiv 0 \pmod 7$.
Since we only care about modulo 7, we can maintain an array `count[7]` where `count[r]` is the number of $j$ such that $W_j \equiv r \pmod 7$.
When moving from `i` to `i+1`:
New last digit is $d_{new} = s[i+1]$.
We need to count $j$ such that `val(s[j:i])` satisfies condition for $d_{new}$.
Wait, the condition for $d_{new}$ is `val(s[j:i]) % M_{d_new} == 0`.
So we need the distribution of `val(s[j:i]) % M_{d_new}`.
If $M_{d_new}$ is small (like 1, 2, 3, 4, 6, 8, 9), we can maintain the counts.
For $d=7$, $M=7$. We need `val(s[j:i]) % 7 == 0`.
We can maintain an array `rem_counts` of size 7.
Initially for `i=0`, `s[0:0]` is empty (value 0). `rem_counts[0] = 1`, others 0.
When moving to `i+1`, we update the values:
For each $j$, $W_j^{new} = W_j^{old} * 10 + s[i]$.
So `rem_counts[r]` becomes `rem_counts[(r*10 + s[i]) % 7]`.
This update is $O(1)$ (size of array is constant 7).
So we can handle $d=7$ in $O(1)$ amortized!
Same for $d=9$ ($M=9$), $d=3$ ($M=3$), $d=6$ ($M=3$).
For $d=4, 8$, we used the "last k digits" trick which is also $O(1)$.
For $d=1, 2, 5$, it's $O(1)$ (count = $i+1$).
So the algorithm is:
Iterate `i` from 0 to `n-1`.
Let `d = int(s[i])`.
If `d == 0`, continue.
Calculate `count` for this `i`.
If `d` in {1, 2, 5}: `count = i + 1`.
If `d` in {3, 6, 9}: We need `val(s[j:i]) % (d/gcd(10,d)) == 0`.
  $d=3 \implies M=3$.
  $d=6 \implies M=3$.
  $d=9 \implies M=9$.
  We can maintain `rem_counts` for modulus 3 and 9?
  Actually, we can maintain one `rem_counts` for the current modulus needed?
  No, the modulus changes with `d`.
  But notice:
  For $d=3, 6$, we need mod 3.
  For $d=9$, we need mod 9.
  We can maintain `rem_counts_3` and `rem_counts_9` separately.
  Update rule: `new_rem[r] = old_rem[(r*10 + s[i]) % M]`.
  Wait, the recurrence `W_j = W_{j, prev} * 10 + s[i-1]`?
  Let's trace carefully.
  At step `i` (processing substring ending at `i`), we consider substrings `s[j:i+1]`.
  The condition involves `val(s[j:i])`.
  Let $V_j^{(i)} = \text{val}(s[j:i])$.
  Then $V_j^{(i)} = V_j^{(i-1)} * 10 + s[i-1]$ for $j < i$.
  And $V_i^{(i)} = 0$ (empty).
  So we can maintain the distribution of $V_j^{(i)} \pmod M$.
  We need separate distributions for $M=3$ and $M=9$.
  Let `cnt3` be array of size 3, `cnt9` be array of size 9.
  Initialize `cnt3[0] = 1`, `cnt9[0] = 1` (representing empty prefix).
  Loop `i` from 0 to `n-1`:
    `d = int(s[i])`
    `ans = 0`
    If `d == 0`: continue
    If `d` in {1, 2, 5}: `ans += i + 1`
    Else if `d` in {3, 6}:
       `ans += cnt3[0]`
       Update `cnt3`: `new_cnt3[r] = cnt3[(r*10 + d) % 3]`? No.
       The update happens for the NEXT step.
       Current step uses `cnt3` which represents $V_j^{(i)}$.
       After processing `i`, we need to prepare for `i+1`.
       The new values $V_j^{(i+1)} = V_j^{(i)} * 10 + s[i]$.
       So `cnt3` should be updated using `s[i]`.
       Wait, the condition for `d` at `i` uses $V_j^{(i)}$.
       So we query `cnt3[0]` then update `cnt3` with `s[i]`.
    Else if `d` == 9:
       `ans += cnt9[0]`
       Update `cnt9` with `s[i]`.
    Else if `d` == 4:
       Check last 2 digits of `s[j:i]`.
       If `i >= 1`:
         `val_2 = int(s[i-1:i])` (digits at `i-1` and `i-2`? No, `s[i-2:i]` is indices `i-2, i-1`).
         Actually `s[j:i]` ends at `i-1`.
         So the last 2 digits are `s[i-2]` and `s[i-1]`.
         If `i >= 2`: `val_2 = int(s[i-2:i])`.
         If `val_2 % 4 == 0`: `ans += i - 1` (all `j <= i-2`).
         Else: `ans += 0` for length >= 2.
       Check length 1: `j = i-1`. `val = s[i-1]`.
       If `int(s[i-1]) % 4 == 0`: `ans += 1`.
       (Note: if `i=0`, no length >= 2, check length 1? `j=0`, `s[0:0]` empty, value 0. `0%4==0`. So `j=0` works. `i=0` -> `ans=1`.)
       Wait, for `i=0`, `s[0:0]` is empty. `val=0`. `0%4==0`. So `j=0` works.
       My logic for `i>=2` covers `j <= i-2`.
       For `j = i-1`, check `s[i-1]`.
       For `j = i`, `val=0`, always works.
       So `ans = 1 (for j=i) + (check j=i-1) + (check j<=i-2)`.
    Else if `d` == 8:
       Similar, check last 3 digits.
       `ans = 1 + (check j=i-1) + (check j=i-2) + (check j<=i-3 if last 3 digits divisible)`.
    Else if `d` == 7:
       `ans += cnt7[0]`.
       Update `cnt7` with `s[i]`.

  Wait, I need to maintain `cnt3`, `cnt9`, `cnt7`.
  `cnt3` size 3, `cnt9` size 9, `cnt7` size 7.
  Initialize all with `cnt[0]=1`, others 0.
  In loop `i`:
    `d = int(s[i])`
    `ans = 0`
    If `d == 0`: continue
    If `d` in {1, 2, 5}: `ans += i + 1`
    If `d` in {3, 6}: `ans += cnt3[0]`
    If `d` == 9: `ans += cnt9[0]`
    If `d` == 7: `ans += cnt7[0]`
    If `d` == 4:
       `ans = 1`
       if `i > 0` and `int(s[i-1]) % 4 == 0`: `ans += 1`
       if `i >= 2` and `int(s[i-2:i]) % 4 == 0`: `ans += i - 1`
    If `d` == 8:
       `ans = 1`
       if `i > 0` and `int(s[i-1]) % 8 == 0`: `ans += 1`
       if `i >= 2` and `int(s[i-2:i]) % 8 == 0`: `ans += 1` # Wait, last 2 digits divisible by 8 implies last 3? No.
       # Divisibility by 8 depends on last 3 digits.
       # If last 3 digits divisible, then all j <= i-3 work.
       # If last 2 digits divisible, does it imply last 3? No.
       # We need to check the number formed by s[i-3:i].
       if `i >= 3` and `int(s[i-3:i]) % 8 == 0`: `ans += i - 2`
       # What about j=i-2? That's last 2 digits.
       # If `int(s[i-2:i]) % 8 == 0`, then `j=i-2` works.
       # If `int(s[i-3:i]) % 8 == 0`, then `j <= i-3` work.
       # Note: if `int(s[i-3:i]) % 8 == 0`, then `int(s[i-2:i])` is the last 2 digits of that number.
       # It's possible `int(s[i-3:i])` is divisible but `int(s[i-2:i])` is not?
       # Example: 104. Last 2 digits 04 (div by 8? 4 no). Last 3 digits 104 (div by 8? yes).
       # So we check `j=i-2` separately.
       # Logic:
       # j=i: 1
       # j=i-1: check s[i-1]
       # j=i-2: check s[i-2:i]
       # j<=i-3: check s[i-3:i]
       # So:
       `ans = 1`
       if `i > 0` and `int(s[i-1]) % 8 == 0`: `ans += 1`
       if `i >= 2` and `int(s[i-2:i]) % 8 == 0`: `ans += 1`
       if `i >= 3` and `int(s[i-3:i]) % 8 == 0`: `ans += i - 2`
    
    # Update counts
    # Update cnt3
    if `i > 0`: # Only update if we have a previous digit to append?
       # Actually, the recurrence is for the NEXT step.
       # The current `cnt3` represents $V_j^{(i)}$.
       # We need to compute $V_j^{(i+1)} = V_j^{(i)} * 10 + s[i]$.
       # So update `cnt3` using `s[i]`.
       # But wait, the loop variable is `i`. We are processing `s[i]`.
       # The `cnt` arrays should be updated AFTER we use them for the current `d`.
       # And the update uses `s[i]` to prepare for `i+1`.
       # But `s[i]` is the digit we just processed as the LAST digit.
       # The `cnt` arrays track the prefix part BEFORE the last digit.
       # So for the NEXT iteration (where `s[i]` becomes part of the prefix), we need to update.
       # Yes.
       pass
    # Update logic:
    # new_cnt[r] = sum(cnt[(r - s[i]*10^{-1}) % M])? No.
    # We want `new_rem = (old_rem * 10 + s[i]) % M`.
    # So iterate `r` from 0 to M-1, `new_cnt[(r*10 + s[i]) % M] += cnt[r]`.
    # This is O(M). M is small (3, 7, 9).
    
    # Perform updates
    # Update cnt3
    if `i > 0`: # Actually, even for i=0, we update for i=1.
       # But for i=0, s[0] is the last digit. The prefix part is empty (0).
       # The next step (i=1), the prefix part for j=0 is s[0].
       # So we update.
       # Is there a case where we don't update? No, always update.
       # But wait, the `cnt` arrays are initialized with 1 at 0.
       # After i=0, we update using s[0].
       # Then for i=1, we use the updated cnt.
       # Correct.
       pass
    # Actually, the update should be done regardless of `d`.
    # But we only need to update if we are going to use them later.
    # Since we iterate all i, we always update.
    
    # Wait, for `d=4, 8`, we don't use `cnt`. But we still need to update `cnt3, cnt9, cnt7` if they are needed later.
    # Yes.

    # One detail: `cnt3` and `cnt9` can share updates?
    # `cnt9` is mod 9. `cnt3` is mod 3.
    # We can maintain both.
    # Update `cnt3` using `s[i]`.
    # Update `cnt9` using `s[i]`.
    # Update `cnt7` using `s[i]`.

    # Implementation details:
    # Create arrays `c3 = [0]*3`, `c9 = [0]*9`, `c7 = [0]*7`.
    # `c3[0] = 1`, etc.
    # Loop `i` from 0 to n-1:
    #   d = int(s[i])
    #   if d == 0: continue
    #   ans = 0
    #   if d in {1,2,5}: ans += i+1
    #   elif d in {3,6}: ans += c3[0]
    #   elif d == 9: ans += c9[0]
    #   elif d == 7: ans += c7[0]
    #   elif d == 4:
    #       ans = 1
    #       if i > 0 and int(s[i-1]) % 4 == 0: ans += 1
    #       if i >= 2 and int(s[i-2:i]) % 4 == 0: ans += i - 1
    #   elif d == 8:
    #       ans = 1
    #       if i > 0 and int(s[i-1]) % 8 == 0: ans += 1
    #       if i >= 2 and int(s[i-2:i]) % 8 == 0: ans += 1
    #       if i >= 3 and int(s[i-3:i]) % 8 == 0: ans += i - 2
    #   
    #   # Update counts
    #   digit = int(s[i])
    #   # Update c3
    #   new_c3 = [0]*3
    #   for r in range(3):
    #       new_c3[(r*10 + digit) % 3] = c3[r]
    #   c3 = new_c3
    #   # Similarly for c9, c7
    #   ...
    #   # Wait, the update logic:
    #   # The current `c3` represents $V_j^{(i)}$.
    #   # We need to compute $V_j^{(i+1)} = V_j^{(i)} * 10 + s[i]$.
    #   # So yes, update using `s[i]`.
    #   # But note: for the very first step (i=0), `c3` is [1,0,0].
    #   # After update, `c3` becomes `[(0*10+d)%3]`.
    #   # For i=1, we use this updated `c3`.
    #   # Correct.

    # Wait, for `d=4, 8`, do we need to update `c3` etc?
    # Yes, because later we might encounter `d=3, 6, 7, 9`.
    # So update always.

    # One correction for `d=8`:
    # `ans = 1` (for j=i)
    # `if i>0 and int(s[i-1])%8==0: ans+=1` (j=i-1)
    # `if i>=2 and int(s[i-2:i])%8==0: ans+=1` (j=i-2)
    # `if i>=3 and int(s[i-3:i])%8==0: ans+=i-2` (j<=i-3)
    # This covers all j.

    # Final check on `d=4`:
    # `ans = 1`
    # `if i>0 and int(s[i-1])%4==0: ans+=1`
    # `if i>=2 and int(s[i-2:i])%4==0: ans+=i-1`
    # Correct.

    # Complexity: O(N * max_mod) = O(N).
    
    # Code structure.

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        ans = 0
        # Initialize counts for mod 3, 7, 9
        # c3[r] = count of j such that val(s[j:i]) % 3 == r
        c3 = [0] * 3
        c9 = [0] * 9
        c7 = [0] * 7
        c3[0] = 1
        c9[0] = 1
        c7[0] = 1
        
        for i, ch in enumerate(s):
            d = int(ch)
            if d == 0:
                continue
            
            current_ans = 0
            if d in (1, 2, 5):
                current_ans = i + 1
            elif d in (3, 6):
                current_ans = c3[0]
            elif d == 9:
                current_ans = c9[0]
            elif d == 7:
                current_ans = c7[0]
            elif d == 4:
                current_ans = 1 # j=i
                if i > 0 and int(s[i-1]) % 4 == 0:
                    current_ans += 1 # j=i-1
                if i >= 2 and int(s[i-2:i]) % 4 == 0:
                    current_ans += i - 1 # j<=i-2
            elif d == 8:
                current_ans = 1 # j=i
                if i > 0 and int(s[i-1]) % 8 == 0:
                    current_ans += 1 # j=i-1
                if i >= 2 and int(s[i-2:i]) % 8 == 0:
                    current_ans += 1 # j=i-2
                if i >= 3 and int(s[i-3:i]) % 8 == 0:
                    current_ans += i - 2 # j<=i-3
            
            ans += current_ans
            
            # Update counts for next iteration
            digit = d
            # Update c3
            new_c3 = [0] * 3
            for r in range(3):
                new_c3[(r * 10 + digit) % 3] = c3[r]
            c3 = new_c3
            
            # Update c9
            new_c9 = [0] * 9
            for r in range(9):
                new_c9[(r * 10 + digit) % 9] = c9[r]
            c9 = new_c9
            
            # Update c7
            new_c7 = [0] * 7
            for r in range(7):
                new_c7[(r * 10 + digit) % 7] = c7[r]
            c7 = new_c7
            
        return ans
```