The problem requires counting substrings where the numeric value is divisible by the last digit of that substring. Since the last digit determines the divisor, we can iterate through each position in the string treating it as the end of a substring. For each ending position, we only need to check substrings ending there whose last digit is non-zero (since division by zero is undefined). A naive check of all substrings would be O(N^2), which is too slow for N=10^5. We can optimize by observing that for a fixed ending position `i` with digit `d = s[i]`, we only care about substrings `s[j...i]` where `d != 0`. The condition is `(value(s[j...i]) % d == 0)`. Since the value modulo `d` depends on the prefix sum modulo `d` (specifically `(prefix[i+1] - prefix[j]) % d == 0`), we can maintain the count of valid start positions `j` for each ending position `i` by tracking the remainder of the current substring value modulo `d`. However, since `d` changes for every ending position, we cannot precompute a single prefix sum array for all divisors. Instead, for each `i`, we can iterate backwards or use a mathematical insight: actually, iterating backwards for each `i` is still O(N^2) in worst case (e.g., all digits same). 

Let's re-evaluate. The constraints are 10^5. O(N^2) is definitely TLE. Is there an O(N) approach?
Consider the condition: `num % last_digit == 0`.
Let the substring be $S[j..i]$. Let $L = S[i] - '0'$. If $L=0$, skip.
We need $( \sum_{k=j}^i S[k] \cdot 10^{i-k} ) \equiv 0 \pmod L$.
This looks like we need to count $j$ such that the value formed by $S[j..i]$ is divisible by $S[i]$.
Wait, Example 2 says "01" is divisible by 1. "12" is divisible by 2 (12%2==0). "701" by 1 (701%1==0).
Actually, any number ending in 1 is divisible by 1. Any number ending in 5 is divisible by 5 if it ends in 0 or 5? No, divisibility by 5 depends on the last digit being 0 or 5. But here the divisor IS the last digit.
So if last digit is 5, we need the number to be divisible by 5. Since the number ends in 5, it is always divisible by 5.
If last digit is 2, we need the number to be divisible by 2. This means the number must be even. Since the last digit is 2, the number is even. So it's always divisible.
Generally, if a number ends in digit $d$, is it always divisible by $d$?
- $d=1$: Yes.
- $d=2$: Number ends in 2, so even. Yes.
- $d=3$: Not necessarily. e.g., 13 ends in 3, but 13 % 3 != 0.
- $d=4$: Not necessarily. e.g., 14 ends in 4, 14 % 4 = 2.
- $d=5$: Ends in 5, so divisible by 5. Yes.
- $d=6$: Not necessarily. e.g., 16 ends in 6, 16 % 6 = 4.
- $d=7$: Not necessarily.
- $d=8$: Not necessarily.
- $d=9$: Not necessarily.
- $d=0$: Undefined.

So for $d \in \{1, 2, 5\}$, ALL substrings ending in $d$ are valid.
For $d \in \{0\}$, skip.
For $d \in \{3, 4, 6, 7, 8, 9\}$, we must check divisibility.
This suggests we can iterate through the string. For positions where $s[i] \in \{1, 2, 5\}$, we add $(i - start\_index + 1)$ to the count (all substrings ending here are valid).
For other digits, we need to count how many $j \le i$ satisfy the condition.
Can we do this faster than O(N) per such $i$?
Notice that for a fixed $i$ and fixed $d = s[i]$, we are looking for $j$ such that $Val(j, i) \equiv 0 \pmod d$.
$Val(j, i) = (Prefix[i+1] - Prefix[j]) \pmod d$? No, standard prefix sums work for addition, but here we have powers of 10.
$Val(j, i) = \sum_{k=j}^i s[k] \cdot 10^{i-k}$.
Modulo $d$: $\sum_{k=j}^i s[k] \cdot 10^{i-k} \equiv 0 \pmod d$.
This is equivalent to: $( \sum_{k=j}^i s[k] \cdot 10^{i-k} ) \% d == 0$.
Since $d$ is small (1 to 9), maybe we can maintain the state?
Actually, for a fixed $i$, as we decrease $j$, the value changes.
Is there a pattern?
Let's reconsider the "always divisible" cases.
If $d=1$, always true.
If $d=2$, always true (ends in 2).
If $d=5$, always true (ends in 5).
So for these, we just count all substrings ending at $i$.
For $d \in \{3, 4, 6, 7, 8, 9\}$, we need to check.
Since $d$ is small, maybe we can just iterate? Worst case: string is all 3s. Then for each $i$, we iterate $j$ from $i$ down to 0. That's O(N^2).
Is there a constraint I missed? No.
Wait, maybe the number of such "hard" digits is small enough or there's a property?
Actually, let's look at the constraints again. $10^5$. O(N^2) is bad.
Is it possible that for $d \in \{3, 4, 6, 7, 8, 9\}$, the condition simplifies?
No.
Maybe we can use the fact that we only care about the last digit?
Wait, if $d=3$, we need the number to be divisible by 3. A number is divisible by 3 if the sum of its digits is divisible by 3.
So for $d=3$, we need $\sum_{k=j}^i s[k] \equiv 0 \pmod 3$.
This can be solved in O(1) with prefix sums of digits!
Let $P[x] = \sum_{k=0}^{x-1} s[k]$. Then sum of $s[j..i]$ is $P[i+1] - P[j]$.
We need $(P[i+1] - P[j]) \equiv 0 \pmod 3 \implies P[j] \equiv P[i+1] \pmod 3$.
We can count frequencies of remainders of prefix sums modulo 3.
Similarly for $d=9$, same logic (divisibility by 9 depends on sum of digits).
What about $d=6$? Divisible by 6 means divisible by 2 and 3.
Since the number ends in 6, it is even (divisible by 2). So we only need to check divisibility by 3. Same as $d=3$.
What about $d=4$? Divisible by 4 depends on the last two digits.
The number $N$ is divisible by 4 iff $N \pmod{100} < 4$? No, iff the number formed by last two digits is divisible by 4.
So for $d=4$, we need the number formed by $s[i-1..i]$ (if $i>0$) or just $s[i]$ (if $i=0$) to be divisible by 4?
Wait, the divisor is $d=4$. The number is $S[j..i]$.
$S[j..i] \pmod 4$ depends only on the last two digits of $S[j..i]$, which are $s[i-1]$ and $s[i]$ (if $j \le i-1$). If $j=i$, it's just $s[i]$.
So for $d=4$, the condition $S[j..i] \% 4 == 0$ depends only on $j$ being close to $i$.
Specifically, if $j=i$, check $s[i] \% 4 == 0$.
If $j=i-1$, check $(10*s[i-1] + s[i]) \% 4 == 0$.
If $j \le i-2$, the last two digits are still $s[i-1]$ and $s[i]$, so the value modulo 4 is constant for all $j \le i-1$.
So for $d=4$, we can check the last two digits. If they form a number divisible by 4, then all $j \le i-1$ (where $j \ge 0$) are valid, plus check $j=i$ separately.
Similarly for $d=8$: depends on last 3 digits.
For $d=7, 3, 9$:
- $d=3, 9$: Sum of digits.
- $d=7$: No simple digit sum rule. But $d=7$ is small.
Wait, if $d=7$, we need $S[j..i] \% 7 == 0$.
This is $( \sum_{k=j}^i s[k] 10^{i-k} ) \% 7 == 0$.
This looks like we need to track the value modulo 7.
But notice: for a fixed $i$, as we vary $j$, the value changes.
However, we can precompute the prefix values modulo $d$?
Let $V[x] = \text{value of } s[0..x-1] \pmod d$.
Then value of $s[j..i]$ is $(V[i+1] - V[j] \cdot 10^{i+1-j}) \pmod d$?
Actually, $Val(j, i) = (Val(0, i) - Val(0, j-1) \cdot 10^{i-(j-1)}) \pmod d$.
Let $P[x]$ be the number formed by $s[0..x-1]$ modulo $d$.
Then $Val(j, i) = (P[i+1] - P[j] \cdot 10^{i+1-j}) \pmod d$.
We need $P[i+1] - P[j] \cdot 10^{i+1-j} \equiv 0 \pmod d$.
This equation involves $10^{i+1-j}$, which varies with $j$. So we can't just count $P[j]$ remainders.
However, $d$ is small (up to 9).
Maybe we can iterate $j$ for the "hard" cases?
How many hard cases? $d \in \{4, 7, 8\}$. (3, 6, 9 are easy).
Is it possible that the test cases are weak or the number of such digits is small?
Or is there a property I'm missing?
Wait, for $d=4$, we established it depends on last 2 digits. So we only need to check $j=i$ and $j=i-1$. All $j \le i-1$ are either valid or invalid based on last 2 digits.
Actually, if the last 2 digits form a number divisible by 4, then for all $j \le i-1$, the last 2 digits are the same, so the number is divisible by 4.
So for $d=4$:
- Check $j=i$: if $s[i] \% 4 == 0$, count 1.
- Check $j=i-1$: if $i>0$ and $(10*s[i-1] + s[i]) \% 4 == 0$, then all $j \in [0, i-1]$ are valid. Count $i$.
- If not, count 0 for $j \le i-1$.
Similarly for $d=8$: depends on last 3 digits.
- Check $j=i$: if $s[i] \% 8 == 0$, count 1.
- Check $j=i-1$: if $i>0$, check last 2 digits? No, for 8 we need last 3.
- If $i < 2$, just check $j=i$ and maybe $j=i-1$ if exists.
- If $i \ge 2$, check the number formed by $s[i-2..i]$. If divisible by 8, then all $j \le i-2$ are valid. Also check $j=i-1$ and $j=i$ separately.
For $d=7$: Depends on the whole number? No, $10^k \pmod 7$ cycles.
$10^0 \equiv 1, 10^1 \equiv 3, 10^2 \equiv 2, 10^3 \equiv 6, 10^4 \equiv 4, 10^5 \equiv 5, 10^6 \equiv 1$. Cycle length 6.
So $Val(j, i) = \sum_{k=0}^{i-j} s[i-k] 10^k$.
This is a convolution?
Actually, for $d=7$, we can maintain the current value modulo 7 as we iterate $i$.
But we need to count $j$ such that $Val(j, i) \equiv 0$.
This is equivalent to: current value $V_i = (V_{i-1} \cdot 10 + s[i]) \pmod 7$.
We want to find $j$ such that the substring $s[j..i]$ is divisible by 7.
This is not directly solvable by a simple prefix sum because of the shifting powers of 10.
However, note that $d=7$ is the only one without a short dependency (like last 2 or 3 digits) or digit sum property.
But wait, is it possible that for $d=7$, the number of valid $j$ is small? No.
Maybe the intended solution is O(N) for easy cases and O(N) for hard cases by realizing that for $d=7$, we can just iterate?
Wait, if the string is all 7s, and we have to check every $j$, it's O(N^2).
Is there a constraint on the number of non-zero digits? No.
Let's re-read the problem carefully. "Return the number of substrings...".
Maybe I am overthinking $d=7$.
Is it possible that for $d=7$, we can use the fact that $10^k \pmod 7$ is periodic?
Yes, period 6.
So $Val(j, i) = \sum_{k=0}^{L} s[i-k] 10^k \pmod 7$.
This is a linear recurrence.
Actually, maybe the test cases don't hit the worst case for $d=7$? Or maybe there's a trick.
Wait, let's look at the constraints again. $10^5$.
If the solution is O(N), then for $d=7$ there must be a way.
What if we maintain a list of indices $j$ where $Val(j, i) \equiv 0$?
As we move from $i$ to $i+1$, the new value is $Val(j, i+1) = (Val(j, i) \cdot 10 + s[i+1]) \pmod 7$.
If $Val(j, i) \equiv 0$, then $Val(j, i+1) = s[i+1] \pmod 7$.
This doesn't help directly to find new zeros.
However, we can maintain the set of $j$'s that satisfy the condition for the current $i$.
But the set can be large.
Wait, maybe the "hard" digits are rare? No.
Let's reconsider the "easy" digits.
$d=1, 2, 5$: All substrings ending in $d$ are valid.
$d=3, 6, 9$: Divisibility by 3 or 9 depends on sum of digits.
$d=4$: Depends on last 2 digits.
$d=8$: Depends on last 3 digits.
$d=7$: The only one left.
Is it possible that $d=7$ is also solvable in O(N)?
Actually, for $d=7$, we can compute the prefix values modulo 7, but we need to handle the $10^k$ factor.
Let $P[i] = \text{value of } s[0..i-1] \pmod 7$.
Then $Val(j, i) = (P[i+1] - P[j] \cdot 10^{i+1-j}) \pmod 7$.
We need $P[i+1] \equiv P[j] \cdot 10^{i+1-j} \pmod 7$.
Let $k = i+1-j$. Then $j = i+1-k$.
We need $P[i+1] \equiv P[i+1-k] \cdot 10^k \pmod 7$.
For a fixed $i$, we need to count $k \ge 1$ such that this holds.
Since $10^k \pmod 7$ has period 6, we can group $k$ by $k \pmod 6$.
Let $cnt[r][rem]$ be the count of indices $x$ such that $x \equiv r \pmod 6$ and $P[x] \equiv rem \pmod 7$.
Then for a fixed $i$, and for each $r \in \{0..5\}$, we want to count $x = i+1-k$ such that $k \equiv r \pmod 6$ (so $i+1-x \equiv r \implies x \equiv i+1-r \pmod 6$) and $P[x] \cdot 10^r \equiv P[i+1] \pmod 7$.
So $P[x] \equiv P[i+1] \cdot (10^r)^{-1} \pmod 7$.
Since 10 is coprime to 7, $10^r$ has an inverse.
So for each $i$, we can iterate $r \in \{0..5\}$, calculate the required remainder for $P[x]$, and add the count of such $x$ from our precomputed table.
This gives an O(N) solution for $d=7$ as well!
Great. So the plan is:
1. Initialize total count = 0.
2. Iterate $i$ from 0 to $n-1$. Let $d = s[i] - '0'$.
3. If $d == 0$, continue.
4. If $d \in \{1, 2, 5\}$: add $(i+1)$ to total.
5. If $d \in \{3, 6, 9\}$:
   - Calculate prefix sum of digits modulo $d$.
   - Count $j \le i$ such that $(P[i+1] - P[j]) \equiv 0 \pmod d$.
   - This is equivalent to $P[j] \equiv P[i+1] \pmod d$.
   - We can maintain a frequency array of $P[j]$ for current $i$.
6. If $d \in \{4, 8\}$:
   - Check last 2 digits (for 4) or last 3 (for 8).
   - If the suffix of length $L$ (where $L=2$ for 4, $L=3$ for 8) is divisible by $d$, then all $j \le i-L+1$ are valid.
   - Check $j=i, i-1, ..., i-L+2$ individually.
   - Add valid count.
7. If $d == 7$:
   - Precompute $P[x] = \text{value}(s[0..x-1]) \pmod 7$.
   - Maintain a 2D array `count[6][7]` where `count[r][rem]` stores number of $x$ such that $x \equiv r \pmod 6$ and $P[x] \equiv rem \pmod 7$.
   - For current $i$, iterate $r \in 0..5$. Calculate target remainder $target = (P[i+1] \cdot \text{inv}(10^r)) \pmod 7$.
   - Add `count[(i+1-r)%6][target]` to total.
   - Update the `count` table with $x=i+1$.

This covers all cases in O(N).