The problem requires counting substrings where the numeric value is divisible by the substring's last non-zero digit. A brute-force approach checking all substrings would be O(N^2), which is too slow for N up to 10^5. Instead, we can iterate through each possible ending position of a substring and count how many starting positions satisfy the condition. For a fixed ending index `i` with digit `d` (where `d` is the last non-zero digit of the substring), we need the substring value modulo `d` to be 0. We can maintain the current remainder of the number formed from the start of the current valid segment to the end `i`. However, since the divisor changes with the last digit, a simpler observation is needed: for a substring ending at `i` with last non-zero digit `d`, we only care about substrings ending at `i` where the number formed is divisible by `d`. We can iterate backwards from `i`, maintaining the current number modulo `d`. If we encounter a '0', we skip it for the purpose of forming the number (as per problem note, leading zeros are allowed, but the divisor is the last non-zero digit). Actually, the constraint is simpler: for each ending position `i`, let `d` be the digit `s[i]`. If `d` is 0, this substring cannot be divisible by 0, so we look for the nearest non-zero digit to the right? No, the problem says "divisible by their non-zero last digit". This implies if the last digit is 0, we ignore it for the divisor? Re-reading: "divisible by their non-zero last digit". This phrasing usually means: identify the last digit of the substring. If it is non-zero, check divisibility. If it is zero, the condition is undefined or the substring is invalid for this rule? Looking at Example 2: "01" ends in '1', divisible by 1. "12" ends in '2', 12%2==0. "701" ends in '1', 701%1==0. "012" ends in '2', 12%2==0. "128" ends in '8', 128%8==0. "5701" ends in '1', divisible. "7012" ends in '2', 7012%2==0. "0128" ends in '8', 128%8==0. "57012" ends in '2', divisible. "70128" ends in '8', divisible. "570128" ends in '8', divisible. "701283" ends in '3', 701283%3==0.
Wait, what about substrings ending in '0'? The problem says "divisible by their non-zero last digit". If the last digit is '0', there is no non-zero last digit. Does this mean such substrings are never counted?
Let's check Example 1: "12936". Substrings ending in '0'? None in input.
Example 2: "5701283". Substrings ending in '0': "70", "570", "0".
"70": last digit is '0'. Is it divisible by a non-zero last digit? There isn't one. So likely not counted.
"570": last digit '0'. Not counted.
"0": last digit '0'. Not counted.
So, substrings ending in '0' are never counted.
For substrings ending in `d` (where `d` != 0), we need `num % d == 0`.
Algorithm: Iterate `i` from 0 to n-1. If `s[i] == '0'`, continue. Let `d = int(s[i])`. Iterate `j` from `i` down to 0. Maintain `current_val = (current_val * 10 + int(s[j])) % d`. If `current_val == 0`, increment count. Stop if we hit a '0'? No, leading zeros are allowed. But if we hit a '0' while iterating backwards, say `s[j] == '0'`, then the number formed is `...0...`. The value is still valid. However, if we go far back, the number grows. But we only need to check modulo `d`.
Actually, if we encounter a '0' at `s[j]`, the digit is 0. The number formed from `j` to `i` is `0...` followed by digits. The value is just the value of the suffix.
Wait, if `s[j] == '0'`, then the digit at `j` is 0. The number formed by `s[j...i]` is `0 * 10^k + ...`. This is just the value of `s[j+1...i]`.
So we can just iterate `j` from `i` down to 0. Calculate `val = (val * 10 + int(s[j])) % d`. If `val == 0`, count++.
Is there a case where we can stop early? If `val` becomes 0, it stays 0? No, `(0 * 10 + digit) % d` depends on the digit.
However, if we have a long sequence of zeros before a non-zero digit, say `00012` ending in `2`. `d=2`.
`j=i` ('2'): 2%2=0 -> count.
`j=i-1` ('1'): 12%2=0 -> count.
`j=i-2` ('0'): 120%2=0 -> count.
`j=i-3` ('0'): 1200%2=0 -> count.
`j=i-4` ('0'): 12000%2=0 -> count.
It seems if `d` divides the current number, and we prepend a 0, the new number is `0 * 10^k + old_number`, which is `old_number`. So if `old_number % d == 0`, then `new_number % d == 0`.
So once we find a valid substring ending at `i` starting at `j`, all substrings starting before `j` (as long as they don't introduce a non-zero digit that breaks divisibility? No, prepending 0 doesn't change value).
Wait, if we prepend a non-zero digit `x`, the new value is `x * 10^k + old_val`. This might or might not be divisible.
But if we encounter a '0' at `s[j]`, then for all `k < j`, if `s[k]` is also '0', the value remains the same. If we hit a non-zero digit, the value changes.
Actually, the logic is: iterate `j` from `i` down to 0. Maintain `rem`. If `s[j] == '0'`, `rem` doesn't change (mathematically `rem * 10 + 0 = rem`). If `s[j] != '0'`, `rem = (rem * 10 + int(s[j])) % d`.
If `rem == 0`, we count.
Can we optimize? The constraints are 10^5. O(N^2) is bad.
Is there an O(N) approach?
Notice that for a fixed `i` and `d = s[i]`, we are looking for `j` such that `num(j, i) % d == 0`.
`num(j, i) = num(j, k) * 10^(i-k) + num(k+1, i)`.
This looks like we need to check many `j`.
However, observe the pattern of remainders.
Actually, the number of substrings ending at `i` that are divisible by `d` is not necessarily small.
But wait, if `s[j] == '0'`, then `num(j, i) == num(j+1, i)`. So if `num(j+1, i)` is divisible by `d`, then `num(j, i)` is also divisible.
So if we find the first `j` (closest to `i`) such that `num(j, i) % d == 0`, then all `k < j` such that `s[k...j-1]` are all '0's will also satisfy the condition.
But if we encounter a non-zero digit at `k < j`, the value changes.
Let's re-evaluate the complexity. In worst case, e.g., "111...1", `d=1`. All substrings are divisible. Count is O(N^2). We cannot simulate each one.
We need a mathematical property.
For a fixed `i` and `d`, we want `num(j, i) % d == 0`.
`num(j, i) = (prefix[i] - prefix[j-1] * 10^(i-j+1)) % d == 0`?
Let `P[x]` be the number formed by `s[0...x-1]` modulo `d`.
Then `num(j, i) = (P[i+1] - P[j] * 10^(i+1-j)) % d`.
We need `(P[i+1] - P[j] * 10^(i+1-j)) % d == 0`.
`P[i+1] % d == (P[j] * 10^(i+1-j)) % d`.
This still requires iterating `j`.
Is it possible that the number of such `j` is small? No, for `d=1`, all `j` work.
Wait, if `d=1`, the answer is simply the number of substrings ending at `i` where `s[i] != '0'`. Since `d=1`, any number is divisible. So if `s[i] == '1'`, all substrings ending at `i` are valid. Count = `i+1`.
If `s[i] == '2'`, we need `num(j, i) % 2 == 0`. This means the last digit `s[i]` must be even. But `s[i]` is `2`, so it is even. Any number ending in an even digit is even. So all substrings ending at `i` are divisible by 2. Count = `i+1`.
Generally, if `d` divides 10, then `num(j, i) % d` depends only on the last few digits?
If `d` divides 10 (i.e., `d` is 2 or 5), then `10^k % d == 0` for `k >= 1`.
So `num(j, i) = s[j]*10^(i-j) + ... + s[i]`.
If `i-j >= 1`, then `s[j]*10^(i-j)` is divisible by `d`.
So `num(j, i) % d == (s[i]) % d`.
Since `s[i] = d`, `s[i] % d == 0`.
So for `d=2` or `d=5`, ALL substrings ending at `i` are divisible by `d`.
Count = `i+1`.
What if `d` does not divide 10? i.e., `d` is 1, 3, 7, 9.
If `d=1`: All substrings divisible. Count = `i+1`.
If `d=3, 7, 9`: We need `num(j, i) % d == 0`.
Since `d` is coprime to 10, `10` has an inverse modulo `d`.
`num(j, i) = s[j]*10^(i-j) + ... + s[i]`.
This is a linear recurrence.
Actually, we can just iterate `j` backwards. But we need to stop early?
If `d` is 3, 7, 9, the period of `10^k mod d` is small (order of 10 mod d).
For `d=3`, `10^k mod 3` is always 1.
`num(j, i) % 3 = (sum of digits) % 3`.
So we need sum of digits from `j` to `i` to be divisible by 3.
This can be solved in O(1) per `i` using prefix sums of digits.
For `d=7, 9`: Similar logic, but sum of digits doesn't work directly for 7.
However, notice that for `d=7, 9`, the maximum length of a repeating cycle of `10^k mod d` is small (6 for 7, 6 for 9).
But we need `num(j, i) % d == 0`.
Let's reconsider the constraints and the nature of the problem.
Maybe the number of valid `j` is not always O(N)?
Actually, if `d` is 3, 7, 9, we can compute the prefix remainders.
Let `R[x] = num(0, x-1) % d`.
`num(j, i) = (R[i+1] - R[j] * 10^(i+1-j)) % d`.
We need `R[i+1] == R[j] * 10^(i+1-j) (mod d)`.
Since `d` is small (1, 2, 3, 5, 7, 9), we can precompute powers of 10 mod `d`.
But we still need to count `j`.
Wait, if `d` is 3, 7, 9, the condition `num(j, i) % d == 0` is equivalent to `R[i+1] * inv(10^(i+1-j)) == R[j] (mod d)`.
Let `P[k] = R[k] * inv(10^k) % d`.
Then `R[i+1] * inv(10^(i+1)) * 10^j == R[j]`.
`P[i+1] * 10^j == P[j]`.
This doesn't seem to simplify to a constant time check for all `j`.
However, note that `d` is a single digit.
Is it possible that for `d=7, 9`, the number of solutions is still O(N)? Yes.
But we can't do O(N^2).
Let's re-read the examples.
Example 2: "5701283".
i=0, '5': d=5. 5%5=0. Count=1.
i=1, '7': d=7. 7%7=0. Count=2.
i=2, '0': skip.
i=3, '1': d=1. All substrings ending here. "1", "01", "701", "5701". Count += 4. Total 1+2+4=7.
i=4, '2': d=2. All substrings ending here (since 2 divides 10). "2", "12", "012", "7012", "57012". Count += 5. Total 12.
i=5, '8': d=8. 8 does not divide 10.
Substrings: "8", "28", "128", "0128", "70128", "570128".
8%8=0.
28%8=4 != 0.
128%8=0.
0128%8=0.
70128%8 = 70128 = 70000 + 128. 70000%8=0 (70000/8=8750). 128%8=0. So 0.
570128%8 = 570128 = 560000 + 10128. 560000%8=0. 10128%8 = 10128/8 = 1266. So 0.
So valid: "8", "128", "0128", "70128", "570128". Count = 5.
Total 12+5=17.
i=6, '3': d=3.
Substrings: "3", "83", "283", "1283", "01283", "701283", "5701283".
3%3=0.
83%3=2.
283%3 = (2+8+3)=13%3=1.
1283%3 = (1+2+8+3)=14%3=2.
01283%3 = 14%3=2.
701283%3 = (7+0+1+2+8+3)=21%3=0.
5701283%3 = (5+7+0+1+2+8+3)=26%3=2.
Valid: "3", "701283". Count = 2.
Total 17+2=19?
Example output is 18.
Where is the error?
Ah, "01283" ends in '3'. Last digit is 3. Divisible by 3? 1283%3=2. No.
"701283": 7+0+1+2+8+3 = 21. Divisible. Yes.
"5701283": 5+7+0+1+2+8+3 = 26. No.
So valid: "3", "701283". Count 2.
Wait, my manual count for i=5 was 5.
"8": yes.
"28": 28%8=4. No.
"128": 128%8=0. Yes.
"0128": 128%8=0. Yes.
"70128": 70128%8=0. Yes.
"570128": 570128%8=0. Yes.
Total 5.
i=4: 5 substrings.
i=3: 4 substrings.
i=2: skip.
i=1: 2 substrings.
i=0: 1 substring.
Sum: 1+2+4+5+5+2 = 19.
Why 18?
Maybe "0128" is not counted? "0128" ends in '8'. Last digit is 8. 128%8=0. Should be counted.
Maybe "01283"? 1283%3=2. Not counted.
Maybe "570128"? 5+7+0+1+2+8 = 23. Not div by 8? 570128 / 8 = 71266. Yes.
Wait, let's recheck "570128".
570128 / 8 = 71266. Correct.
Is there any substring I missed or miscounted?
Maybe "0" at i=2? Skipped.
Maybe "70" at i=2? Ends in 0. Skipped.
Maybe "570"? Ends in 0. Skipped.
Maybe "01"? Ends in 1. 1%1=0. Counted in i=3.
Maybe "12"? Ends in 2. 12%2=0. Counted in i=4.
Maybe "701"? Ends in 1. 701%1=0. Counted in i=3.
Maybe "5701"? Ends in 1. Counted in i=3.
Maybe "29" in Ex 1? Ends in 9. 29%9=2. No.
"129": 129%9=3. No.
"293": 293%3=2. No.
"2936": 2936%6=2. No.
Total 15 - 4 = 11. Correct.

Back to Ex 2. Why 18?
Maybe "0128" is not counted? "0128" -> 128. 128%8=0.
Maybe "70128"? 70128%8=0.
Maybe "570128"? 570128%8=0.
Maybe "83"? 83%3=2. No.
Maybe "283"? 283%3=1. No.
Maybe "1283"? 1283%3=2. No.
Maybe "01283"? 1283%3=2. No.
Maybe "701283"? 21%3=0. Yes.
Maybe "5701283"? 26%3=2. No.
So for i=6, count is 2.
Total 19.
Is it possible that "0128" is not considered a valid substring? "A substring may contain leading zeros." So it is valid.
Is it possible that "0128" is not divisible by 8? 128/8=16. Yes.
Wait, maybe I miscounted i=4?
i=4, '2'. Substrings: "2", "12", "012", "7012", "57012".
"2": 2%2=0.
"12": 12%2=0.
"012": 12%2=0.
"7012": 7012%2=0.
"57012": 57012%2=0.
All 5.
i=3, '1'. Substrings: "1", "01", "701", "5701".
All divisible by 1. 4.
i=5, '8'. Substrings: "8", "28", "128", "0128", "70128", "570128".
"8": yes.
"28": 28%8=4. No.
"128": yes.
"0128": yes.
"70128": yes.
"570128": yes.
Total 5.
i=6, '3'. Substrings: "3", "83", "283", "1283", "01283", "701283", "5701283".
"3": yes.
"83": no.
"283": no.
"1283": no.
"01283": no.
"701283": yes.
"5701283": no.
Total 2.
Sum: 1+2+4+5+5+2 = 19.
The example says 18.
Difference is 1.
Which one is wrong?
Maybe "0128" is not counted? Why?
Maybe "0128" ends in '8', but the substring is "0128". The last digit is '8'. 128 is divisible by 8.
Wait, is "0128" considered to have last digit '8'? Yes.
Is it possible that "0128" is not divisible by 8? 128 = 16 * 8. Yes.
Maybe "570128" is not divisible by 8? 570128 = 560000 + 10128. 560000/8=70000. 10128/8=1266. Yes.
Maybe "70128"? 70128/8=8766. Yes.
Maybe "012"? Ends in 2. 12%2=0. Counted in i=4.
Maybe "701"? Ends in 1. Counted in i=3.
Maybe "5701"? Ends in 1. Counted in i=3.
Maybe "01"? Ends in 1. Counted in i=3.
Maybe "1"? Ends in 1. Counted in i=3.
Maybe "2"? Ends in 2. Counted in i=4.
Maybe "12"? Ends in 2. Counted in i=4.
Maybe "012"? Ends in 2. Counted in i=4.
Maybe "7012"? Ends in 2. Counted in i=4.
Maybe "57012"? Ends in 2. Counted in i=4.
Maybe "8"? Ends in 8. Counted in i=5.
Maybe "28"? Ends in 8. 28%8=4. No.
Maybe "128"? Ends in 8. 128%8=0. Yes.
Maybe "0128"? Ends in 8. 128%8=0. Yes.
Maybe "70128"? Ends in 8. 70128%8=0. Yes.
Maybe "570128"? Ends in 8. 570128%8=0. Yes.
Maybe "3"? Ends in 3. 3%3=0. Yes.
Maybe "83"? Ends in 3. 83%3=2. No.
Maybe "283"? Ends in 3. 283%3=1. No.
Maybe "1283"? Ends in 3. 1283%3=2. No.
Maybe "01283"? Ends in 3. 1283%3=2. No.
Maybe "701283"? Ends in 3. 701283%3=0. Yes.
Maybe "5701283"? Ends in 3. 5701283%3=2. No.

Is it possible that "0128" is not counted because the problem says "non-zero last digit"? '8' is non-zero.
Wait, maybe I miscounted the total substrings?
Total substrings of "5701283" is 7*8/2 = 28.
Substrings ending in 0: "70", "570", "0". (3 substrings).
Substrings ending in non-zero: 28 - 3 = 25.
We found 19 valid.
Missing 6?
Example explanation: "Substrings "01", "12", "701", "012", "128", "5701", "7012", "0128", "57012", "70128", "570128", and "701283" are all divisible by their last digit. Additionally, all substrings that are just 1 non-zero digit are divisible by themselves. Since there are 6 such digits, the answer is 12 + 6 = 18."
Let's list the 12 from explanation:
"01" (i=3, j=2)
"12" (i=4, j=3)
"701" (i=3, j=1)
"012" (i=4, j=2)
"128" (i=5, j=3)
"5701" (i=3, j=0)
"7012" (i=4, j=1)
"0128" (i=5, j=2)
"57012" (i=4, j=0)
"70128" (i=5, j=1)
"570128" (i=5, j=0)
"701283" (i=6, j=1)
That's 12.
Plus "all substrings that are just 1 non-zero digit".
Non-zero digits: 5, 7, 1, 2, 8, 3. (6 digits).
Single digit substrings: "5", "7", "1", "2", "8", "3". (6 substrings).
Total 12 + 6 = 18.
Wait, my count included single digits in the "ending at i" counts.
i=0: "5" (1)
i=1: "7" (1)
i=3: "1" (1)
i=4: "2" (1)
i=5: "8" (1)
i=6: "3" (1)
Total 6 single digits.
My count for multi-digit:
i=3: "01", "701", "5701" (3) + "1" (1) = 4.
i=4: "12", "012", "7012", "57012" (4) + "2" (1) = 5.
i=5: "128", "0128", "70128", "570128" (4) + "8" (1) = 5.
i=6: "701283" (1) + "3" (1) = 2.
Total multi-digit: 3+4+4+1 = 12.
Total single: 6.
Sum 18.
Ah, I see. In my previous manual count for i=5, I counted "8" as 1, "128" as 1, "0128" as 1, "70128" as 1, "570128" as 1. Total 5.
In i=6, I counted "3" as 1, "701283" as 1. Total 2.
In i=3, I counted "1", "01", "701", "5701". Total 4.
In i=4, I counted "2", "12", "012", "7012", "57012". Total 5.
In i=0, "5". 1.
In i=1, "7". 1.
Sum: 1+1+4+5+5+2 = 18.
My previous sum was 19. Why?
Ah, I said i=5 count is 5. i=6 count is 2. i=4 is 5. i=3 is 4. i=1 is 2? No, i=1 is "7" only?
i=1, '7'. Substrings: "7". "57"? 57%7=1. No.
So i=1 count is 1.
i=0 count is 1.
So 1+1+4+5+5+2 = 18.
Okay, the logic holds. The issue was my manual counting of i=1.
So the algorithm is:
Iterate `i` from 0 to n-1.
If `s[i] == '0'`, continue.
`d = int(s[i])`.
If `d == 1`: count += `i+1`.
If `d == 2` or `d == 5`: count += `i+1`.
If `d == 3, 7, 9`: We need to count `j` such that `num(j, i) % d == 0`.
Since `d` is small, we can iterate `j` from `i` down to 0.
But we need to optimize.
Actually, for `d=3, 7, 9`, the number of valid `j` might be small? No, could be O(N).
But we can use the property that `num(j, i) % d` can be computed incrementally.
Since `d` is small, we can just iterate. But worst case O(N^2).
Is there a case where we have to iterate O(N) times for each `i`?
If `d=3`, `num(j, i) % 3` is sum of digits mod 3.
We can precompute prefix sums of digits mod 3.
Then `num(j, i) % 3 == (prefix[i+1] - prefix[j]) % 3`.
We need `(prefix[i+1] - prefix[j]) % 3 == 0` => `prefix[j] == prefix[i+1]`.
So for `d=3`, we can count in O(1) using a frequency array of prefix sums.
For `d=7, 9`:
`num(j, i) = (P[i+1] - P[j] * 10^(i+1-j)) % d`.
We need `P[i+1] == P[j] * 10^(i+1-j) (mod d)`.
`P[j] == P[i+1] * inv(10^(i+1-j)) (mod d)`.
Let `Q[k] = P[k] * inv(10^k) % d`.
Then `Q[j] == P[i+1] * inv(10^(i+1)) * 10^j * inv(10^j) * inv(10^j)`? No.
`P[j] * 10^(i+1-j) = P[i+1]`.
`P[j] * 10^(i+1) * inv(10^j) = P[i+1]`.
`P[j] * inv(10^j) = P[i+1] * inv(10^(i+1))`.
Let `Q[k] = P[k] * inv(10^k) % d`.
Then `Q[j] == Q[i+1]`.
So for any `d` coprime to 10 (1, 3, 7, 9), we can compute `Q` array and count frequencies.
For `d=1`, `inv(10)` is 1. `Q[k] = P[k]`. `Q[j] == Q[i+1]`. Always true?
For `d=1`, `num(j, i) % 1 == 0` always. So count `i+1`.
For `d=3, 7, 9`, we can use the `Q` array.
Algorithm:
1. Initialize `count = 0`.
2. For each `i` from 0 to n-1:
   If `s[i] == '0'`, continue.
   `d = int(s[i])`.
   If `d == 1` or `d == 2` or `d == 5`:
      `count += (i + 1)`
   Else:
      Compute `P` array up to `i+1` for this `d`? No, precomputing for all `d` is not feasible.
      But `d` is only 3, 7, 9.
      We can maintain three separate prefix structures for `d=3, 7, 9`.
      Actually, we can just compute on the fly.
      For `d=3`: maintain `freq3[3]` of `prefix_sum % 3`.
      For `d=7`: maintain `freq7[7]` of `Q[k]`.
      For `d=9`: maintain `freq9[9]` of `Q[k]`.
      Wait, `Q[k]` depends on `inv(10^k)`. We can precompute powers of 10 and their inverses for 7 and 9.
      For `d=3`, it's simpler: `prefix_sum % 3`.
      So:
      Precompute `inv10_7` and `inv10_9` arrays.
      Maintain `pref3`, `pref7`, `pref9` (current prefix values).
      Maintain `count3`, `count7`, `count9` (frequency of `Q` values seen so far).
      Actually, we need to update frequencies as we iterate `i`.
      For `d=3`: `current_rem = (current_rem + int(s[i])) % 3`. We need `current_rem == prev_rem`.
      For `d=7, 9`: `Q[i+1] = (P[i+1] * inv(10^(i+1))) % d`.
      We need to count `j <= i` such that `Q[j] == Q[i+1]`.
      So we maintain a frequency map for `Q` values.
      Initialize `freq3 = {0:1}`, `freq7 = {0:1}`, `freq9 = {0:1}`.
      `cur3 = 0`, `cur7 = 0`, `cur9 = 0`.
      `pow10_7 = 1`, `pow10_9 = 1`.
      `inv_pow10_7 = 1`, `inv_pow10_9 = 1`.
      Iterate `i` from 0 to n-1:
        `digit = int(s[i])`
        If `digit == 0`: continue.
        If `digit == 1` or `digit == 2` or `digit == 5`:
           `count += (i+1)`
        Else:
           # Update for d=3
           `cur3 = (cur3 + digit) % 3`
           `count3 = freq3[cur3]`
           `freq3[cur3] += 1`
           # But wait, we need to count j such that num(j, i) % 3 == 0.
           # num(j, i) % 3 == (cur3 - prefix[j]) % 3 == 0 => prefix[j] == cur3.
           # So we add freq3[cur3] to count.
           # But we must include j=i? Yes, prefix[i+1] is cur3. prefix[i+1] matches itself.
           # So count += freq3[cur3].
           # But we haven't added cur3 to freq3 yet?
           # We should add to freq3 first? No, we need j <= i.
           # prefix[j] for j from 0 to i+1?
           # num(j, i) uses prefix[j] and prefix[i+1].
           # j goes from 0 to i. prefix indices 0 to i.
           # So we should have added prefix[0]...prefix[i] to freq.
           # Then for current i, we compute prefix[i+1], and count matches in freq.
           # Then add prefix[i+1] to freq.
           pass
           
      Let's refine the loop structure.
      Initialize `freq3 = {0:1}`, `freq7 = {0:1}`, `freq9 = {0:1}`.
      `cur3 = 0`, `cur7 = 0`, `cur9 = 0`.
      `pow10_7 = 1`, `inv_pow10_7 = 1`.
      `pow10_9 = 1`, `inv_pow10_9 = 1`.
      `total_count = 0`.
      For `i` in 0..n-1:
        `d = int(s[i])`
        If `d == 0`: continue.
        If `d == 1` or `d == 2` or `d == 5`:
           `total_count += (i+1)`
        Else:
           # Update cur3
           `cur3 = (cur3 + d) % 3`
           `total_count += freq3.get(cur3, 0)`
           `freq3[cur3] = freq3.get(cur3, 0) + 1`
           
           # Update cur7
           `cur7 = (cur7 * 10 + d) % 7`
           `Q7 = (cur7 * inv_pow10_7) % 7`
           `total_count += freq7.get(Q7, 0)`
           `freq7[Q7] = freq7.get(Q7, 0) + 1`
           `pow10_7 = (pow10_7 * 10) % 7`
           `inv_pow10_7 = (inv_pow10_7 * inv(10, 7)) % 7` # Precompute inv(10,7)=5
           
           # Update cur9
           `cur9 = (cur9 * 10 + d) % 9`
           `Q9 = (cur9 * inv_pow10_9) % 9`
           `total_count += freq9.get(Q9, 0)`
           `freq9[Q9] = freq9.get(Q9, 0) + 1`
           `pow10_9 = (pow10_9 * 10) % 9`
           `inv_pow10_9 = (inv_pow10_9 * inv(10, 9)) % 9` # Precompute inv(10,9)=4

      Wait, `inv(10, 7)`: 10*5=50=1 mod 7. Yes.
      `inv(10, 9)`: 10*4=40=4 mod 9. No. 10*4=40=4. 10*7=70=7. 10*1=1. 10*4=4.
      10x = 1 mod 9 => x=1. 10*1=10=1. So inv is 1.
      Wait, 10 mod 9 is 1. So inv(10,9)=1.
      So `inv_pow10_9` stays 1.
      `pow10_9` stays 1.
      So for d=9, `Q9 = cur9`.
      And `cur9` is `num(0, i) % 9`.
      Condition: `num(j, i) % 9 == 0` => `prefix[i+1] - prefix[j] == 0 mod 9`.
      So `prefix[j] == prefix[i+1]`.
      Same as d=3.
      So for d=9, we can use same logic as d=3.
      
      Final plan:
      Use frequency maps for d=3 and d=9 (same logic).
      Use frequency map for d=7.
      Handle d=1,2,5 separately.
      Handle d=0 by skipping.