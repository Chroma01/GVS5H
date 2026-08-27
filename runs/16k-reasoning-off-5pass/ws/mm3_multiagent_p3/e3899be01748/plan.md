We need to count substrings whose integer value is divisible by its last (non-zero) digit. For each position `i` (ending index), we consider all starting positions `j <= i` such that the last digit `s[i]` is non-zero, and the substring `s[j..i]` is divisible by `int(s[i])`. A brute-force check is O(n²), too slow for n up to 1e5. The key observation: the divisibility condition only depends on the prefix modulo the last digit. So for each digit `d` from 1 to 9 that appears as `s[i]`, we can maintain the running value of prefixes modulo `d`. For a fixed ending `i` with `s[i] = d`, we need to count how many starting positions `j` (including the empty prefix before index 0) satisfy that the value of `s[j..i]` is divisible by `d`. That value modulo `d` equals `(pref[i+1] - pref[j] * pow10[i-j] mod d) mod d`. We can precompute `pow10[k] mod d` for all `k`. However, recomputing for each digit independently would be O(9·n²). We need a smarter method: for each `d`, process all positions where `s[i] = d` and for each such `i`, iterate over possible substring lengths backwards, but that is still O(n²) in the worst case (e.g., all digits = 1). We need a linear or near-linear solution.

Alternative approach: iterate over starting index `j` and extend to the right, using rolling modulo, but stop when the number becomes too large? Not needed; we can use a two-pointer technique because the condition depends only on the current remainder and the last digit. Actually, we can iterate over each position `i` (as ending) and for each possible `d = s[i]`, we need to count `j` such that the substring value mod `d` == 0. Let’s define `r_j(i) = value(s[j..i]) mod d`. As `j` decreases by 1, we add a new most significant digit `s[j]`. The recurrence is `r_{j-1}(i) = (s[j] * 10^{len} + r_j(i)) mod d`. This depends on `len = i - (j-1)`. So the transformation depends on the length. If we fix `d` and process positions `i` in order, we can maintain a map from remainder to count of starting positions that yield that remainder for the current ending `i`. But the length exponent changes with `i`, so the map is not directly reusable across different `i` unless we also track length.

Observation: For a fixed ending `i` and digit `d = s[i]`, the number of valid `j` is the number of `j` (0 ≤ j ≤ i) such that `(value(s[j..i]) mod d) == 0`. This is similar to counting subarrays where sum modulo d equals zero, but with a weighted sum (digits weighted by powers of 10). The weight factor `10^{len}` mod d depends on `len`. However, we can use the fact that `d` is small (1-9). We can precompute for each `d` an array `pow10_mod_d[k] = 10^k mod d` for k = 0..n. Then for a fixed `i`, we can iterate `j` from `i` downwards and update the remainder using the precomputed powers. This is O(length) per `i`, total O(n²) in worst case.

We need a faster method. Since `d` is at most 9, we can use a different trick: For each `d`, we can process all positions where `s[i] = d` in one pass, using a hashmap that maps the "prefix value" to frequency. Let's think about the number formed by substring `s[j..i]`. If we consider the prefix up to `i` and the prefix up to `j-1`, we have `value(s[j..i]) = (pref[i+1] - pref[j] * 10^{i-j+1}) / 10^{n-(i+1)}? Not simple. Better: treat the string as a number in base 10, and the substring value is `(pref[i+1] - pref[j] * 10^{i-j+1})`. For modulo d, we can multiply by the modular inverse of `10^{i-j+1}` mod d, if it exists. But d is not coprime to 10 in general (e.g., d=2,5). So modular inverse doesn't always exist.

Alternative: Instead of iterating over all j, we can iterate over possible lengths? The number of valid substrings ending at i might be large. For d=1, any substring ending with 1 is valid (since 1 divides everything). That's O(n²) for all substrings ending with 1. So we cannot iterate over each substring individually in the worst case. We need a formula or aggregate counting.

We need to count, for each d, the total number of substrings ending with digit d where the substring value is divisible by d. Since d is small, maybe we can use a different approach: For each d, maintain an array of length d (remainders) and update it as we scan the string. But the catch is that the remainder of a substring depends on its length (due to multiplication by 10). However, if we process the string from left to right, and for each position i (as start), we can extend to the right and compute remainders mod d. But that's O(n^2).

Wait, maybe we can use the fact that d is small to allow O(n * d) or O(n * log n) solutions. For each d, we want to count pairs (j, i) with j ≤ i, s[i] = d, and value(s[j..i]) ≡ 0 mod d. Let's fix d. Consider all positions i where s[i] = d. For each such i, we want to count j ≤ i such that value(s[j..i]) ≡ 0 mod d. This is like: given a set of queries (i, d), answer how many previous starting positions produce a remainder 0. If we process i in order, we can maintain a data structure that for each possible starting position j, stores the value of s[j..i] mod d. As i increments, the values for all j change because the substring length increases. This seems like we need to update all j each time, which is O(n) per i.

But maybe we can reverse the perspective: For each starting position j, we can compute the value of the number starting at j and ending at various positions. The value modulo d changes predictably as we append digits. For a fixed j, as we extend i to i+1, the new value is (old_value * 10 + s[i+1]) mod d. So for each j, we can simulate extending to the right and check divisibility when s[i+1] is non-zero. But that's O(n^2) because for each j we go through all i.

We need a clever combinatorial insight. Let's look at the examples: For s = "1010101010", only substrings ending with 1 are valid, and there are 25 of them. Let's verify: length is 10, number of substrings ending with 1: positions of 1 are at indices 0,2,4,6,8 (5 positions). For each such position i, the number of substrings ending at i is i+1 (since any j from 0 to i). So total = 5+3+1? Wait: i=0: 1 substring (just "1"). i=2: 3 substrings ("1","01","101"). i=4: 5 substrings. i=6: 7. i=8: 9. Sum = 1+3+5+7+9 = 25. Yes, all substrings ending with 1 are divisible by 1 (trivially). So for d=1, the answer is simply the number of substrings that end with '1'. That can be computed easily: for each position i with s[i] = '1', add (i+1) to the answer (since any j from 0 to i works). But wait: does every substring ending with 1 satisfy the condition? The condition says divisible by its non-zero last digit. If last digit is 1, the number is always divisible by 1. So yes. So for d=1, we can just sum (i+1) for all i with s[i] = '1'. That's O(n).

Now for d=2: A number is divisible by 2 iff its last digit is even. But we are already given that the last digit is the digit d. So the condition is automatically satisfied for d=2? Wait, the last digit is d. If d=2, then the number ends with 2, so it is even, so divisible by 2. So any substring ending with '2' is valid! But is that true? Let's check: "12" ends with 2, 12 mod 2 = 0. "32" ends with 2, 32 mod 2 = 0. Any number ending with 2 is even, so divisible by 2. Similarly, any number ending with 4, 6, 8 is divisible by 2? No, divisibility by 2 requires the number to be even. The last digit being 2,4,6,8 means the number is even, so yes. But wait: the condition is divisibility by the last digit itself, not by 2. For d=2, the number ends with 2, so the number mod 2 is 0, so divisible by 2. So any substring ending with 2 is valid. Similarly, for d=4,6,8, the number ends with that digit, but being divisible by 4 requires the last two digits to be divisible by 4, not just the last digit. So for d=2, it's trivial: all substrings ending with '2' are valid. For d=5, the number ends with 5, so it's divisible by 5. So any substring ending with '5' is valid. For d=1, any substring ending with '1' is valid. So for d in {1,2,5}, the answer is simply: for each occurrence of digit d, add the number of substrings ending at that position, which is (position+1). So we can compute these in O(n).

Now for d in {3,4,6,7,8,9}, it's not automatic. For these, we need to count substrings ending with d that are divisible by d.

Let's consider d=3. The sum of digits modulo 3 determines divisibility by 3. So for a substring s[j..i] ending with d, we need the sum of its digits to be divisible by 3. So we can use prefix sums modulo 3. Let prefix sum of digits up to index k be S[k+1] = (S[k] + int(s[k])) mod 3. Then the sum of substring s[j..i] is (S[i+1] - S[j]) mod 3. We need this to be 0. So for each i with s[i] = '3', we need to count j such that S[j] == S[i+1] mod 3. And j can be from 0 to i. Also, note that the substring may have leading zeros, but sum of digits treats zeros as 0, so that's fine. So for d=3, we can maintain a frequency map of prefix sums seen so far. For each i, if s[i] = '3', we add the frequency of the current prefix sum S[i+1] (which corresponds to j=0..i, because S[j] is the prefix sum before including s[j]). Actually, careful: S[i+1] is the sum of s[0..i]. The substring s[j..i] sum mod 3 = (S[i+1] - S[j]) mod 3. We want this = 0, so S[j] = S[i+1]. The possible j are 0 ≤ j ≤ i. The prefix sum S[j] is defined for j from 0 to i. Note: S[0] = 0 (sum of empty prefix). So we need to count how many j in [0, i] have S[j] = S[i+1]. So we can maintain a frequency array of S values for indices 0..i-1, and for each i, we query the frequency of S[i+1]. That gives the number of valid starting positions. So for d=3, we can process the string left to right, maintaining a count of prefix sum frequencies. For each i with s[i] = '3', add freq[S[i+1]] to the answer, then update freq with S[i+1] (since i becomes a potential starting position for future substrings). This is O(n).

Similarly, for d=9: divisibility by 9 depends on sum of digits mod 9. So the same approach: use prefix sums mod 9. For each i with s[i] = '9', we need S[j] = S[i+1] mod 9. So O(n) with frequency array of size 9.

Now for d=4,6,7,8. These are trickier because divisibility by them doesn't have a simple digit sum property. However, note that 4, 6, 8 are powers of 2 times 3, etc. We might use modular arithmetic with base 10. For a fixed d, we want to count substrings ending with d. We can precompute prefix values mod d. Let P[i] be the integer value of s[0..i-1] mod d (i.e., prefix of length i). Then the value of s[j..i] (where i is inclusive) is (P[i+1] - P[j] * 10^{i-j+1}) mod d. This requires knowing the power of 10 modulo d. We can precompute pow10_mod_d[k] = 10^k mod d for k=0..n. Then for each i with s[i]=d, we need to count j such that (P[i+1] - P[j] * pow10_mod_d[i-j+1]) mod d == 0. Rearranging: P[j] * pow10_mod_d[i-j+1] ≡ P[i+1] (mod d). Since d is small (4,6,7,8), we can factor d into prime powers? Actually, we can use the fact that d is small to precompute for each possible length L (from 1 to n) the value of pow10_mod_d[L]. But the exponent depends on i and j, so the product term changes.

Alternatively, we can fix the starting position j and iterate over i, but that's O(n^2). We need a better way.

For d=6: Divisibility by 6 means divisible by 2 and 3. Since the number ends with 6, it's even, so divisible by 2 automatically. So we only need to check divisibility by 3. So for d=6, the condition reduces to: sum of digits mod 3 == 0. So we can use the same prefix sum method as for d=3, but only for positions where s[i] = '6'. Because any number ending with 6 is even, so divisible by 2. So the condition is simply that the number is divisible by 3. So for d=6, we can use prefix sums mod 3. Wait, is that sufficient? For a number to be divisible by 6, it must be divisible by both 2 and 3. Since it ends with 6, it's divisible by 2. So we only need divisibility by 3. And divisibility by 3 is sum of digits mod 3. So yes, for d=6, we can use the same technique as d=3: for each i with s[i]='6', add the count of previous prefix sums equal to current prefix sum mod 3. So O(n).

Now for d=8: Divisibility by 8 depends on the last three digits. Specifically, the number formed by the last three digits must be divisible by 8. More generally, for divisibility by 2^k, we only need to look at the last k digits. So for d=8 (2^3), we only need to consider the last up to 3 digits of the substring. But careful: the substring could be shorter than 3 digits. If the substring length is 1, the number is just 8, which is divisible by 8. If length is 2, the number is the two-digit number ending with 8; we need to check if that two-digit number is divisible by 8. If length >= 3, we need to check the last three digits. So for d=8, we can process each position i with s[i]='8', and we need to count j such that the substring s[j..i] is divisible by 8. This can be determined by looking at the last up to 3 digits. So we can iterate backwards from i for up to 3 steps to compute the value of the last up to 3 digits and check divisibility. Since we only go back at most 3 steps per i, the total time is O(n) if we do this for each i. But wait, we also need to consider substrings longer than 3 digits. For a substring of length > 3, its divisibility by 8 depends only on its last 3 digits. So if we know the last 3 digits, we can determine if the whole number is divisible by 8. So for each i, we can compute the number formed by s[i-2..i] (the last 3 digits, or fewer if i<2). Then for any starting position j, the substring s[j..i] will be divisible by 8 if and only if the number formed by its last 3 digits (which is the same as the last 3 digits of s[max(j,i-2)..i] ) is divisible by 8. But careful: if j is more than 2 positions before i, then the last 3 digits of s[j..i] are exactly s[i-2..i]. So the condition only depends on the last 3 digits, regardless of j, as long as j <= i-2. So for j <= i-2, the substring is divisible by 8 iff the 3-digit number (or fewer if i<2) formed by the last three digits (including i) is divisible by 8. But we also need to consider j = i-1 and j = i. So for each i, we can compute the set of j that yield a valid substring. Specifically, we can iterate j backwards from i to max(0, i-2) (or up to i, but for j <= i-2, the condition is the same). So for each i, we can compute the number of j in [0, i-2] such that the last three digits condition holds, plus check the cases j = i-1 and j = i individually. But we can do this efficiently: for each i, compute the number formed by s[i-2..i] (as an integer, or directly check divisibility). If that number is divisible by 8, then all substrings ending at i with starting position j <= i-2 are valid. How many such j? There are (i-2+1) = i-1 if i >= 2? Actually, j from 0 to i-2 inclusive: count = i-1 (since indices 0..i-2). For i=0: no j <= i-2. For i=1: j <= -1 none. For i>=2: count = i-1. So if the last three digits (s[i-2..i]) form a number divisible by 8, then all substrings starting at j=0..i-2 are valid. Then we additionally need to check j = i-1 and j = i. For j = i, substring is "8", which is divisible by 8. For j = i-1, substring is s[i-1] + s[i], i.e., a two-digit number. We need to check if that two-digit number is divisible by 8. So we can compute that on the fly. So for d=8, we can process each i in O(1) time: we need to know the last three digits at i, and also the two-digit number at i-1,i. So we can keep a sliding window of the last three digits as we go. This yields O(n) time.

Similarly, for d=4: Divisibility by 4 depends on the last two digits. So for each i with s[i]='4', we need to count j such that the last two digits of s[j..i] (or the whole number if length < 2) are divisible by 4. For j <= i-1, the last two digits are s[i-1] and s[i]. So if the two-digit number formed by s[i-1]s[i] is divisible by 4, then all substrings with starting position j <= i-1 are valid? Wait, careful: if j = i-1, the substring is exactly s[i-1]s[i], so that's the two-digit number. If j < i-1, the substring is longer, but the last two digits are still s[i-1]s[i]. So for any j <= i-1, the condition is the same: the two-digit number must be divisible by 4. For j = i, the substring is just "4", which is divisible by 4. So for d=4, if the two-digit number (s[i-1]s[i]) is divisible by 4, then all substrings ending at i with j <= i-1 are valid, plus j = i always valid. But wait: what about substrings of length 1? That's j = i, which is always valid. So for d=4, the number of valid substrings ending at i is: (i) if the two-digit number is divisible by 4? Let's count: if the two-digit number is divisible by 4, then for j from 0 to i-1, all are valid (i choices), and j=i is also valid (1 choice), total i+1. If the two-digit number is not divisible by 4, then only j=i (the single digit) is valid, total 1. But we also need to consider the case when i=0: no two-digit number, so only j=0 is valid (the single digit). So we can process d=4 in O(1) per i by looking at s[i-1] and s[i]. We need to be careful for i=0.

Now for d=7: This is the tricky one. Divisibility by 7 doesn't have a simple pattern from last few digits (except last 6 digits, but that's not constant). We need a more general method. Since d=7 is small, we can use modular arithmetic with prefix remainders. Let's think: For d=7, we want to count substrings ending with '7' that are divisible by 7. Let's precompute the prefix values mod 7. Let P[i] be the value of s[0..i-1] mod 7. Then the value of s[j..i] mod 7 is (P[i+1] - P[j] * 10^{i-j+1}) mod 7. We want this to be 0. Rearranging: P[j] * 10^{i-j+1} ≡ P[i+1] (mod 7). Since 10 is invertible modulo 7 (gcd(10,7)=1), we can multiply both sides by the modular inverse of 10^{i-j+1}. Let inv10 = 10^{-1} mod 7. Note that 10 mod 7 = 3, and the inverse of 3 mod 7 is 5 (since 3*5=15≡1 mod 7). So 10^{-1} mod 7 = 5. Then 10^{k} mod 7 is just (3^k) mod 7, and its inverse is 5^k mod 7. So we can write: P[j] ≡ P[i+1] * (10^{-(i-j+1)}) mod 7. But that depends on i-j. So for a fixed i, the required P[j] depends on j through the exponent. We can instead define Q[i] = P[i] * 10^{-i} mod 7. Then the condition becomes: Q[j] = Q[i+1]? Let's check: The value of s[j..i] is (P[i+1] - P[j] * 10^{i-j+1}). Mod 7, we have P[i+1] - P[j] * 10^{i-j+1} ≡ 0. Multiply both sides by 10^{-(i+1)}: P[i+1] * 10^{-(i+1)} - P[j] * 10^{-j} ≡ 0. So Q[i+1] - Q[j] ≡ 0 mod 7, i.e., Q[j] = Q[i+1] mod 7. That's a great simplification! So if we define Q[i] = (P[i] * inv10^i) mod d, for any d coprime to 10, then the condition that substring s[j..i] is divisible by d is equivalent to Q[j] = Q[i+1] mod d. This works because 10 has an inverse modulo d. For d=7, gcd(10,7)=1, so we can do this. For d=3, gcd(10,3)=1, so we could also do this, but we already have the digit sum method. For d=9, gcd(10,9)=1, so we can use this method as well. But for d=4,6,8, gcd(10,d) is not 1 (for d=4, gcd=2; for d=6, gcd=2; for d=8, gcd=2). So the inverse method only works for d coprime to 10. So for d=7, we can use the Q method. For d=3 and d=9, we can also use it, but the digit sum method is simpler. However, we might unify for d=7,3,9 using the Q method. But note: for d=3, the Q method is valid because 10 is invertible mod 3 (10 mod 3 = 1, inverse is 1). So we could use Q method for d=3 as well, but the digit sum method is more intuitive. For d=7, we will use the Q method.

So for d=7, we precompute inv10 mod 7 = 5. Then we compute an array Q of length n+1, where Q[0] = 0, and Q[i+1] = (Q[i] * 10 + int(s[i])) * inv10 mod 7? Actually, we want Q[i] = (P[i] * inv10^i) mod 7. So we can compute iteratively: Q[0] = 0. For i from 0 to n-1: P[i+1] = (P[i] * 10 + int(s[i])) mod 7. Then Q[i+1] = P[i+1] * inv10^{i+1} mod 7. But we can compute Q[i+1] directly from Q[i]: Q[i+1] = (P[i+1] * inv10^{i+1}) = ((P[i] * 10 + d_i) * inv10^{i+1}) = (P[i] * 10 * inv10^{i+1} + d_i * inv10^{i+1}) = (P[i] * inv10^i * 10 * inv10 + d_i * inv10^{i+1}) = (Q[i] * 10 * inv10 + d_i * inv10^{i+1}). Since 10 * inv10 ≡ 1 mod 7, this simplifies to Q[i+1] = (Q[i] + d_i * inv10^{i+1}) mod 7. Alternatively, we can compute Q[i+1] = (Q[i] + d_i * pow(inv10, i+1, 7)) mod 7. But we can precompute inv10_pow[i] = (inv10)^i mod 7. So we can compute Q in O(n). Then for each i with s[i] = '7', we need to count j (0 ≤ j ≤ i) such that Q[j] = Q[i+1]. So we can maintain a frequency map of Q values for indices 0..i-1, and for each i, query freq[Q[i+1]] and add to answer. This is O(n) with a frequency array of size 7.

So for d=7, we have an O(n) solution.

Now we have covered all digits 1-9. Let's summarize:

- For d=1: any substring ending with '1' is valid. Count: for each i with s[i]='1', add (i+1).
- For d=2: any substring ending with '2' is valid. Count: for each i with s[i]='2', add (i+1).
- For d=3: use digit sum mod 3. Maintain prefix sum mod 3, frequency array of size 3. For each i with s[i]='3', add freq[prefix_sum] (where prefix_sum is sum up to i mod 3), then update freq.
- For d=4: depends on last two digits. For each i with s[i]='4', if i>=1 and the two-digit number (s[i-1]s[i]) is divisible by 4, then all substrings ending at i with start j ≤ i-1 are valid, plus j=i always valid. So add (i) if i>=1 and two-digit divisible by 4, else add 1. But careful: for i=0, only j=0 is valid, so add 1. For i>=1: if two-digit divisible by 4, add (i) + 1 = i+1? Actually, j from 0 to i-1: that's i choices. Plus j=i: 1 choice. So total i+1. If not divisible, only j=i, so 1. So we can write: if i==0: add 1. else: check two-digit, if divisible by 4, add i+1, else add 1.
- For d=5: any substring ending with '5' is valid. Count: for each i with s[i]='5', add (i+1).
- For d=6: divisible by 2 and 3. Since ends with 6, divisible by 2. So only need divisible by 3. Use digit sum mod 3. Same as d=3 but only for positions with '6'. Maintain prefix sum mod 3 frequency. For each i with s[i]='6', add freq[prefix_sum] (where prefix_sum is sum up to i mod 3), then update freq. Note: we can use the same frequency array as for d=3? But careful: the prefix sum is the same, but we need to update the frequency after processing each i? Actually, for d=3 and d=6, the condition depends on the same prefix sum, but we are processing different positions. We can compute the prefix sum once, and then for each i with s[i] in {3,6}, we query the frequency of the current prefix sum. But we need to update the frequency after processing each character? Because for future positions, the prefix sum includes more digits. So we should update the frequency after considering each character, regardless of whether it's a 3 or 6. So we can maintain a single prefix sum and a frequency array for mod 3. Then for each i, if s[i] is '3' or '6', we add the frequency of the current prefix sum to the answer (before updating? Actually careful: For a given i, the prefix sum up to i is S[i+1]. The substring s[j..i] sum mod 3 = (S[i+1] - S[j]) mod 3. We want this 0, so S[j] = S[i+1]. The j ranges from 0 to i. So the frequency should count how many j in [0, i] have S[j] = S[i+1]. But S[j] for j from 0 to i includes S[0], S[1], ..., S[i]. Note that S[i+1] is the sum up to i, but S[i] is the sum up to i-1. So for substring s[j..i], the starting index j corresponds to prefix sum S[j] (sum of first j digits). So j can be 0, so S[0] is included. So we need to count occurrences of S[i+1] among S[0], S[1], ..., S[i]. That is exactly the frequency of S[i+1] in the set of prefix sums before updating with S[i+1]. So we should query the frequency before adding the current prefix sum to the frequency map. So algorithm: Initialize freq[0] = 1 (for S[0]=0). Set current_sum = 0. For i from 0 to n-1: current_sum = (current_sum + int(s[i])) % 3. If s[i] is '3' or '6': answer += freq[current_sum]. Then freq[current_sum] += 1. This works for both d=3 and d=6 simultaneously. But note: for d=6, we also need to ensure that the number is divisible by 2, but since it ends with 6, it's automatically even. So we don't need to check anything else. So we can combine d=3 and d=6.

- For d=7: use the Q method with mod 7. Compute Q array. Maintain frequency of Q values. For each i with s[i]='7', add freq[Q[i+1]] to answer, then update freq[Q[i+1]].

- For d=8: use last three digits. For each i with s[i]='8', we need to count valid j. We can process as described: if i=0: only j=0, add 1. If i=1: check two-digit number s[0]s[1]. If divisible by 8, then j=0 and j=1 are valid? Actually, for i=1, j can be 0 and 1. If the two-digit number is divisible by 8, then j=0 is valid (since last two digits are the whole number) and j=1 is valid (single digit 8). So both are valid, add 2. If not, only j=1 valid, add 1. For i>=2: we need to consider j from 0 to i-2, j=i-1, j=i. The condition for j <= i-2 depends on the last three digits s[i-2..i]. If that three-digit number is divisible by 8, then all j from 0 to i-2 are valid. Number of such j is i-1 (since 0..i-2 inclusive). Then we also need to check j=i-1 (two-digit number) and j=i (always valid). So we can compute: let three_digit = int(s[i-2:i+1]) if i>=2. If three_digit % 8 == 0, then for j=0..i-2, add (i-1). Then check two-digit: let two_digit = int(s[i-1:i+1]) if i>=1. If two_digit % 8 == 0, then j=i-1 is valid, so add 1. Also j=i is always valid, so add 1. So total if three_digit %8==0 and two_digit %8==0: add (i-1) + 1 + 1 = i+1. If three_digit %8==0 but two_digit %8!=0: add (i-1) + 0 + 1 = i. If three_digit %8!=0: then no j from 0..i-2 are valid. Then we only consider j=i-1 and j=i. So if two_digit %8==0, add 1 (for j=i-1) + 1 (for j=i) = 2. If two_digit %8!=0, add 1 (only j=i). But we also need to consider the case when i<2 separately. So we can write code for d=8 accordingly.

- For d=9: use digit sum mod 9. Similar to d=3 but mod 9. Maintain prefix sum mod 9, frequency array of size 9. For each i with s[i]='9', add freq[prefix_sum] to answer, then update freq.

So overall, we can process the string in one pass, maintaining the necessary data structures for d=3,6,7,9, and handle d=1,2,4,5,8 separately. But note: d=1,2,5 are trivial: for each occurrence, add (i+1). d=4 and d=8 are based on local digits. So we can compute them in the same pass as well, but they are O(1) per character.

Let's verify with examples:

Example 1: s="12936". 
Positions: 0:'1', 1:'2', 2:'9', 3:'3', 4:'6'.
d=1: i=0, add 1. Total=1.
d=2: i=1, add 2 (since i+1=2). Total=3.
d=3: i=3, s[3]='3'. Compute prefix sums mod 3: 
i=0: sum=1 mod3=1. freq[0]=1, freq[1]=1. i=0 not '3'.
i=1: sum=(1+2)=3 mod3=0. freq[0]=2, freq[1]=1. i=1 not '3'.
i=2: sum=(0+9)=9 mod3=0. freq[0]=3, freq[1]=1. i=2 not '3'.
i=3: sum=(0+3)=3 mod3=0. s[3]='3', add freq[0]=3. Then update freq[0]=4. So d=3 adds 3.
d=4: no '4'.
d=5: no '5'.
d=6: i=4, s[4]='6'. At i=4, sum mod3: from previous, sum=0? Actually, after i=3, sum=0. Then i=4: sum=(0+6)=6 mod3=0. s[4]='6', add freq[0] which is 4. Then update freq[0]=5. So d=6 adds 4.
d=7: no '7'.
d=8: no '8'.
d=9: i=2, s[2]='9'. Compute prefix sums mod 9: 
i=0: sum=1, freq[0]=1, freq[1]=1.
i=1: sum=1+2=3, freq[3]=1.
i=2: sum=3+9=12 mod9=3. s[2]='9', add freq[3]=1. Then update freq[3]=2. So d=9 adds 1.
Total = 1+2+3+4+1 = 11. Matches.

Example 2: s="5701283". 
Let's compute quickly:
d=1: no '1'? Actually, there is a '1' at index 2? s="5701283": indices: 0:'5', 1:'7', 2:'0', 3:'1', 4:'2', 5:'8', 6:'3'. So d=1: i=3, add 4. Total=4.
d=2: i=4, add 5. Total=9.
d=3: i=6, s[6]='3'. Compute prefix sums mod3: 
i=0: sum=5 mod3=2. freq[0]=1, freq[2]=1.
i=1: sum=2+7=9 mod3=0. freq[0]=2, freq[2]=1.
i=2: sum=0+0=0. freq[0]=3, freq[2]=1.
i=3: sum=0+1=1. freq[1]=1. s[3] not '3'.
i=4: sum=1+2=3 mod3=0. freq[0]=4, freq[1]=1, freq[2]=1.
i=5: sum=0+8=8 mod3=2. freq[2]=2.
i=6: sum=2+3=5 mod3=2. s[6]='3', add freq[2]=2. Then update freq[2]=3. So d=3 adds 2. Total=11.
d=4: no '4'.
d=5: i=0, add 1. Total=12.
d=6: no '6'.
d=7: i=1, s[1]='7'. For d=7, we need Q method. Let's compute Q for d=7. inv10 mod7=5. Q[0]=0.
i=0: d0=5. Q[1] = (Q[0] + 5 * 5^1) mod7? Actually, we need to compute carefully. We want Q[i+1] = (P[i+1] * inv10^{i+1}) mod7. Alternatively, we can compute P and then Q. Let's compute P mod7:
P[0]=0.
i=0: P[1] = (0*10+5) mod7 = 5.
i=1: P[2] = (5*10+7) mod7 = (50+7)=57 mod7=57-56=1.
i=2: P[3] = (1*10+0)=10 mod7=3.
i=3: P[4] = (3*10+1)=31 mod7=31-28=3.
i=4: P[5] = (3*10+2)=32 mod7=32-28=4.
i=5: P[6] = (4*10+8)=48 mod7=48-42=6.
i=6: P[7] = (6*10+3)=63 mod7=0.
Now compute inv10^k mod7: 5^1=5, 5^2=25 mod7=4, 5^3=20 mod7=6, 5^4=30 mod7=2, 5^5=10 mod7=3, 5^6=15 mod7=1, 5^7=5, etc.
Q[0]=0.
Q[1] = P[1]*5^1 mod7 = 5*5=25 mod7=4.
Q[2] = P[2]*5^2 mod7 = 1*4=4.
Q[3] = P[3]*5^3 mod7 = 3*6=18 mod7=4.
Q[4] = P[4]*5^4 mod7 = 3*2=6.
Q[5] = P[5]*5^5 mod7 = 4*3=12 mod7=5.
Q[6] = P[6]*5^6 mod7 = 6*1=6.
Q[7] = P[7]*5^7 mod7 = 0*5=0.
Now for d=7, we need for each i with s[i]='7' (i=1), count j such that Q[j]=Q[i+1]=Q[2]=4. j can be 0,1. Q[0]=0, Q[1]=4. So only j=1 gives Q[j]=4. But j=1 corresponds to starting at index 1? Actually, j is the starting index, and we need Q[j] = Q[i+1]. Here i=1, so j from 0 to 1. Q[0]=0, Q[1]=4. So only j=1 works. That means substring s[1..1]="7" is valid. But also j=0? That would be s[0..1]="57", which is not divisible by 7? 57/7=8.14, no. So only 1 valid. But the example says there are 12 valid substrings from d=7? Wait, the example says: "Substrings '01', '12', '701', '012', '128', '5701', '7012', '0128', '57012', '70128', '570128', and '701283' are all divisible by their last digit." None of these end with 7. So d=7 might contribute 0? Actually, the example says these substrings are divisible by their last digit. Let's check the last digits: '01' ends with 1, '12' ends with 2, '701' ends with 1, '012' ends with 2, '128' ends with 8, '5701' ends with 1, '7012' ends with 2, '0128' ends with 8, '57012' ends with 2, '70128' ends with 8, '570128' ends with 8, '701283' ends with 3. So none end with 7. So d=7 should contribute 0. Our calculation gave 1, which is wrong. Why? Because for i=1, we considered j=1 gives Q[1]=4 and Q[2]=4, so substring s[1..1] is valid. But is "7" divisible by 7? Yes, 7/7=1. So that is valid. So d=7 should contribute 1 for the single-digit substring "7". But the example explanation says "Since there are 6 such digits" meaning non-zero digits that are alone are divisible by themselves. So "7" is a non-zero digit, and it is divisible by itself. So it should be counted. In the example, they say: "Additionally, all substrings that are just 1 non-zero digit are divisible by themselves. Since there are 6 such digits, the answer is 12 + 6 = 18." So they count 6 single-digit substrings. The non-zero digits in "5701283" are: 5,7,0? Actually non-zero: 5,7,1,2,8,3. That's 6 digits. So each of these single-digit substrings is valid. So d=7 contributes 1 from the single-digit "7". So our count of 1 is correct. But in the total, we have d=1:4, d=2:5, d=3:2, d=5:1, d=7:1, and d=9:0, d=4,6,8:0. Sum=4+5+2+1+1=13, but the example says 18. We are missing some. Let's recalculate d=1: i=3, add 4. But also, there are substrings ending with 1 that are not just single-digit? For example, "01" ends with 1, and it is listed as valid. Does our method count "01"? For i=3 (s[3]='1'), we add (i+1)=4. That includes j=0: "5701", j=1: "701", j=2: "01", j=3: "1". So that includes "01" and "701" and "5701". So that's fine. d=2: i=4, add 5. That includes j=0: "57012", j=1: "7012", j=2: "012", j=3: "12", j=4: "2". So that covers "12", "012", "7012", "57012". So that's fine. d=3: i=6, add 2. That includes j=5: "83"? Wait, i=6, j=5 gives "83", j=6 gives "3". But "83" is not divisible by 3? 83 mod3=2. So that's not valid. So our d=3 count of 2 seems off. Let's recompute d=3 carefully.

We need to count substrings ending with '3' that are divisible by 3. For d=3, we used prefix sums mod 3. But note: for d=3, the condition is that the sum of digits mod 3 is 0. For substring s[j..i] with i=6 (s[6]='3'), we need sum of digits from j to 6 mod 3 = 0. Let's compute prefix sums of digits (not mod yet): 
Indices: 0:5, 1:7, 2:0, 3:1, 4:2, 5:8, 6:3.
Sums: S0=0, S1=5, S2=12, S3=12, S4=13, S5=15, S6=23, S7=26.
Mod 3: S0=0, S1=2, S2=0, S3=0, S4=1, S5=0, S6=2, S7=2.
At i=6, we need S[j] = S7 mod 3 = 2. j can be 0..6. S0=0, S1=2, S2=0, S3=0, S4=1, S5=0, S6=2. So j=1 and j=6 give S[j]=2. That means substrings: s[1..6] = "701283" and s[6..6]="3". Check: "701283": sum=7+0+1+2+8+3=21, divisible by 3? 21/3=7, yes. "3" is divisible. So that gives 2. So d=3 adds 2. That matches.

d=5: i=0, add 1. So total so far: 4+5+2+1+1=13. But we also have d=8? In the example, there are substrings ending with 8 that are valid. Let's check d=8. In "5701283", there is an '8' at index 5. We need to count substrings ending at index 5 with last digit 8 that are divisible by 8. According to our d=8 method:
i=5, s[5]='8'. i>=2, so compute three_digit: s[3..5] = "128", int=128, 128/8=16, so divisible by 8. So for j=0..3 (i-2=3), all are valid? Wait, j from 0 to i-2 = 3, that's 4 substrings: j=0: "570128", j=1: "70128", j=2: "0128", j=3: "128". Then check two_digit: s[4..5]="28", int=28, 28/8=3.5, not divisible. So j=4 not valid. And j=5: "8" valid. So total valid: 4 (from j=0..3) + 0 (j=4) + 1 (j=5) = 5. So d=8 should add 5. That would give total 18. And indeed the example lists substrings ending with 8: "128", "0128", "70128", "570128" (that's 4) and also "8" is not listed explicitly? They said "all substrings that are just 1 non-zero digit are divisible by themselves", so "8" is included in the 6 single-digit substrings. But in our d=8 count, we already included j=5 as valid. So d=8 adds 5. But wait, in the list of 12 substrings, they have "128", "0128", "70128", "570128" — that's 4. But they also have "8"? They said "Since there are 6 such digits" so "8" is one of them. So total from d=8 is 5. So our d=8 method gives 5. So total answer = d=1:4, d=2:5, d=3:2, d=5:1, d=7:1, d=8:5, d=9:0, d=4,6:0. Sum = 4+5+2+1+1+5 = 18. Perfect.

So our method works.

Now we need to implement all this in one pass. We can compute the answer incrementally as we scan the string from left to right. We'll maintain:

- For d=1,2,5: just sum (i+1) when s[i] is '1','2','5' respectively.
- For d=3,6: maintain prefix sum mod 3, and a frequency array of size 3. Initially freq[0]=1, freq[1]=freq[2]=0. For each i, update current_sum_mod3 = (current_sum_mod3 + int(s[i])) % 3. If s[i] is '3' or '6', add freq[current_sum_mod3] to answer. Then increment freq[current_sum_mod3].
- For d=4: as described, check two-digit number if i>=1. We can keep track of the last digit to compute the two-digit number. Actually, we need to know s[i-1] to form the two-digit number. So we can store the previous digit. Alternatively, we can compute the two-digit number from s[i-1] and s[i] on the fly. Since we process sequentially, we can keep a variable prev_digit. For i=0, only add 1. For i>=1, let two_digit = int(s[i-1])*10 + int(s[i]). If two_digit % 4 == 0, add (i+1) (since j from 0 to i-1 and j=i), else add 1. But careful: when two_digit is divisible by 4, we said add i+1. That includes j=i. So correct.
- For d=7: we need to maintain Q values mod 7 and their frequencies. We'll precompute inv10_pow[i] = (inv10)^i mod 7. We can compute iteratively. Let inv10 = 5. inv10_pow[0]=1, inv10_pow[1]=5, inv10_pow[2]=4, etc. We'll compute as we go. We'll maintain a frequency array for Q of size 7. Initially, Q[0]=0, so freq[0]=1, others 0. For each i, we need to update Q. We have Q[i+1] = (Q[i] + d_i * inv10_pow[i+1]) mod 7? Actually, from earlier: Q[i+1] = (P[i+1] * inv10^{i+1}) mod 7. And we had recurrence: Q[i+1] = (Q[i] + d_i * inv10^{i+1}) mod 7. Check: Q[i] = P[i] * inv10^i. Then Q[i+1] = P[i+1] * inv10^{i+1} = (P[i]*10 + d_i) * inv10^{i+1} = P[i] * 10 * inv10^{i+1} + d_i * inv10^{i+1} = (P[i] * inv10^i) * (10 * inv10) + d_i * inv10^{i+1} = Q[i] * 1 + d_i * inv10^{i+1} mod 7. Yes, so we can update Q iteratively if we have inv10_pow[i+1]. So we can precompute inv10_pow array of length n+1. Or we can compute inv10_pow on the fly: maintain a variable inv10_pow, multiply by inv10 each step mod 7. So algorithm: Q = 0, inv10_pow = 1 (for i=0? Actually, we need inv10_pow for i+1). Let's define: initially, Q corresponds to index 0, so Q=0. Also, we need freq[0]=1. For i from 0 to n-1: update inv10_pow = (inv10_pow * inv10) % 7. Then Q = (Q + int(s[i]) * inv10_pow) % 7. Now Q is the value for index i+1. So if s[i] is '7', we want to count j such that Q[j] = Q (current Q). But Q[j] for j from 0 to i. We have freq array for Q values of indices 0..i-1. So before updating freq with the current Q, we should query freq[Q]. So: if s[i] == '7': answer += freq[Q]. Then update freq[Q] += 1. But careful: we also need to include Q[0]=0 in the initial freq. So initialize freq[0]=1, Q=0, inv10_pow=1? Actually, for i=0, we need inv10_pow for i+1=1. So we should update inv10_pow first. Let's do: inv10_pow = (inv10_pow * inv10) % 7, starting with inv10_pow=1? If we set inv10_pow=1 initially, then after first multiplication, it becomes inv10. So that's good. So steps: 
Initialize: answer=0, Q=0, inv10_pow=1, freqQ = [0]*7, freqQ[0]=1.
For i in range(n):
    inv10_pow = (inv10_pow * inv10) % 7
    digit = int(s[i])
    Q = (Q + digit * inv10_pow) % 7
    if s[i] == '7':
        answer += freqQ[Q]
    freqQ[Q] += 1
This should work.

- For d=8: as described. We need to know the previous two digits to form the three-digit and two-digit numbers. We can keep track of the last two digits. Let last1 = s[i-1] (if exists), last2 = s[i-2] (if exists). For i=0: add 1. For i=1: let two_digit = int(s[0])*10 + int(s[1]). If two_digit % 8 == 0, add 2, else add 1. For i>=2: let three_digit = int(s[i-2])*100 + int(s[i-1])*10 + int(s[i]). If three_digit % 8 == 0, then count_three = i-1 (number of j from 0 to i-2). Else count_three = 0. Then let two_digit = int(s[i-1])*10 + int(s[i]). If two_digit % 8 == 0, add 1 for j=i-1. Always add 1 for j=i. So total add = count_three + (1 if two_digit%8==0 else 0) + 1. We need to update last1 and last2 as we go.

- For d=9: similar to d=3 but mod 9. Maintain prefix sum mod 9, frequency array of size 9. Initially freq[0]=1, sum_mod9=0. For each i, sum_mod9 = (sum_mod9 + int(s[i])) % 9. If s[i] == '9', add freq[sum_mod9], then increment freq[sum_mod9].

We also need to handle d=4,6,8 carefully. For d=4, we already have a method. For d=6, we already combined with d=3. For d=8, we have method.

Now, we must ensure that we don't double-count or miss. Also, note that for d=3 and d=6, we use the same prefix sum and frequency. So we can update once per i and then check both.

Let's code accordingly.

We'll write a class Solution with method countSubstrings(self, s: str) -> int.

Implementation steps:

1. n = len(s)
2. Initialize ans = 0
3. For d=1,2,5: just loop and add (i+1) if s[i] in {'1','2','5'}.
4. For d=3,6: 
   - sum_mod3 = 0
   - freq3 = [0]*3, freq3[0] = 1
   - For i in range(n):
        sum_mod3 = (sum_mod3 + int(s[i])) % 3
        if s[i] in {'3','6'}:
            ans += freq3[sum_mod3]
        freq3[sum_mod3] += 1
5. For d=4:
   - We'll do in the same loop, but need to keep track of previous digit. We can do a separate loop or integrate. Since we need to access s[i-1], we can do a loop from i=0 to n-1, and for i>=1, compute two_digit. We can also store previous digit as we go. Let's integrate with the main loop? But we have multiple conditions. We can do a single loop that updates everything. However, for d=4, we need to know s[i-1]. We can keep a variable prev_digit. For i=0, prev_digit is None. So in the loop, we can have:
        if i == 0:
            if s[0] == '4': ans += 1
        else:
            two_digit = prev_digit*10 + digit
            if s[i] == '4':
                if two_digit % 4 == 0:
                    ans += i+1
                else:
                    ans += 1
        prev_digit = digit
   But careful: prev_digit should be the digit value (integer), not the character. So we convert to int.
6. For d=7:
   - inv10 = 5
   - Q = 0
   - inv10_pow = 1
   - freqQ = [0]*7, freqQ[0] = 1
   - In the loop, after updating sum_mod3, we can update for d=7 as well. But we need to compute Q. So in the same loop, we do:
        inv10_pow = (inv10_pow * inv10) % 7
        digit_int = int(s[i])
        Q = (Q + digit_int * inv10_pow) % 7
        if s[i] == '7':
            ans += freqQ[Q]
        freqQ[Q] += 1
7. For d=8:
   - We need last two digits. We can keep two variables: prev1 and prev2 (integers). Initialize prev2 = None, prev1 = None.
   - In the loop, at index i, digit = int(s[i]).
   - If s[i] == '8':
        if i == 0:
            ans += 1
        elif i == 1:
            two_digit = prev1*10 + digit
            if two_digit % 8 == 0:
                ans += 2
            else:
                ans += 1
        else: # i >= 2
            three_digit = prev2*100 + prev1*10 + digit
            count = 0
            if three_digit % 8 == 0:
                count += (i-1)  # j=0..i-2
            two_digit = prev1*10 + digit
            if two_digit % 8 == 0:
                count += 1
            count += 1  # j=i
            ans += count
   - Then update: prev2 = prev1, prev1 = digit.
8. For d=9:
   - sum_mod9 = 0
   - freq9 = [0]*9, freq9[0] = 1
   - In the loop, after sum_mod3, we also update sum_mod9:
        sum_mod9 = (sum_mod9 + digit) % 9
        if s[i] == '9':
            ans += freq9[sum_mod9]
        freq9[sum_mod9] += 1

We can combine all updates in one loop for efficiency. But we need to be careful about the order of updates: for d=3 and d=6, we need to query the frequency before updating it. Similarly for d=7 and d=9. So the loop structure should be: for each i, first compute digit, then update the various sums and Q, then check conditions and add to ans, then update frequencies. But for d=4 and d=8, we need to use previous digits, which are already stored.

Let's write a single loop that does all.

We need to initialize all variables before the loop.

Let's code step by step.

Note: For d=1,2,5, we can simply add (i+1) when the digit matches. That can be done inside the loop as well.

So the loop:

n = len(s)
ans = 0
sum_mod3 = 0
freq3 = [0]*3
freq3[0] = 1
Q = 0
inv10 = 5
inv10_pow = 1
freqQ = [0]*7
freqQ[0] = 1
sum_mod9 = 0
freq9 = [0]*9
freq9[0] = 1
prev_digit = None  # for d=4 and d=8
prev1 = None  # for d=8
prev2 = None  # for d=8

for i in range(n):
    digit_char = s[i]
    digit = int(digit_char)
    
    # d=1,2,5
    if digit_char in ('1','2','5'):
        ans += (i+1)
    
    # d=3 and d=6
    sum_mod3 = (sum_mod3 + digit) % 3
    if digit_char in ('3','6'):
        ans += freq3[sum_mod3]
    freq3[sum_mod3] += 1
    
    # d=4
    if digit_char == '4':
        if i == 0:
            ans += 1
        else:
            two_digit = prev_digit*10 + digit
            if two_digit % 4 == 0:
                ans += i+1
            else:
                ans += 1
    
    # d=7
    inv10_pow = (inv10_pow * inv10) % 7
    Q = (Q + digit * inv10_pow) % 7
    if digit_char == '7':
        ans += freqQ[Q]
    freqQ[Q] += 1
    
    # d=8
    if digit_char == '8':
        if i == 0:
            ans += 1
        elif i == 1:
            two_digit = prev1*10 + digit
            if two_digit % 8 == 0:
                ans += 2
            else:
                ans += 1
        else:
            three_digit = prev2*100 + prev1*10 + digit
            count = 0
            if three_digit % 8 == 0:
                count += (i-1)
            two_digit = prev1*10 + digit
            if two_digit % 8 == 0:
                count += 1
            count += 1
            ans += count
    
    # d=9
    sum_mod9 = (sum_mod9 + digit) % 9
    if digit_char == '9':
        ans += freq9[sum_mod9]
    freq9[sum_mod9] += 1
    
    # Update prev digits for next iteration
    prev2 = prev1
    prev1 = digit
    prev_digit = digit

But wait: for d=4, we used prev_digit, but we also have prev1 from d=8. They are the same: the previous digit. So we can use prev1 for d=4 as well. So we can remove prev_digit and use prev1. But careful: for d=4, we need the previous digit, which is prev1. But at i=0, prev1 is None. So we need to check i==0 first. So we can use prev1 for d=4.

Also, for d=8, we need prev2 and prev1. So we update prev2 and prev1 at the end.

Let's adjust: use prev1 as the previous digit (integer). For d=4, we can use prev1.

Now, check d=7: We need to ensure that the Q update and query are correct. We have Q corresponding to index i+1. Initially, Q for index 0 is 0, and freqQ[0]=1. For i=0, we update inv10_pow to inv10, then Q = (0 + digit * inv10) % 7. Then if s[0] is '7', we add freqQ[Q]. But note: freqQ contains frequencies for indices 0..i-1. For i=0, freqQ only has index 0. So we are checking if Q[0] equals Q[1]. That's correct. Then we update freqQ[Q] for index 1. So it's fine.

Now, we need to test with examples.

Example 1: s="12936"
i=0: digit=1. d1: ans+=1 -> ans=1.
sum_mod3: 1%3=1, freq3[1]? s[0] not 3 or 6, so skip. freq3[1] becomes 1.
d4: not 4.
d7: inv10_pow=5, Q=1*5=5 mod7=5. s[0] not 7, skip. freqQ[5] becomes 1.
d8: not 8.
d9: sum_mod9=1, freq9[1] becomes 1.
prev1=1.

i=1: digit=2. d1: not 1,2,5? Actually 2 is in, so ans+=2 -> ans=3.
sum_mod3: (1+2)=3%3=0. s[1]='2', not 3 or 6. freq3[0] becomes 1.
d4: not 4.
d7: inv10_pow=5*5=25%7=4, Q=(5+2*4)=5+8=13%7=6. s[1] not 7. freqQ[6] becomes 1.
d8: not 8.
d9: sum_mod9=1+2=3, freq9[3] becomes 1.
prev1=2, prev2=1.

i=2: digit=9. d1: not. ans=3.
sum_mod3: 0+9=9%3=0. s[2]='9', not 3 or 6. freq3[0] becomes 2.
d4: not.
d7: inv10_pow=4*5=20%7=6, Q=(6+9*6)=6+54=60%7=4 (since 56 is multiple, 60-56=4). s[2] not 7. freqQ[4] becomes 1.
d8: not.
d9: sum_mod9=3+9=12%9=3. s[2]='9', so add freq9[3]=1 -> ans=4. Then freq9[3] becomes 2.
prev1=9, prev2=2.

i=3: digit=3. d1: not. ans=4.
sum_mod3: 0+3=3%3=0. s[3]='3', so add freq3[0]=2 -> ans=6. Then freq3[0] becomes 3.
d4: not.
d7: inv10_pow=6*5=30%7=2, Q=(4+3*2)=4+6=10%7=3. s[3] not 7. freqQ[3] becomes 1.
d8: not.
d9: sum_mod9=