We need to count substrings `s[i..j]` such that the integer value of the substring is divisible by its last non-zero digit (i.e., `s[j]` when `s[j] != '0'`; if `s[j] == '0'`, the substring is automatically excluded because division by zero is undefined). The substring may have leading zeros, so we treat it as a base-10 number with its full digit sequence.

A naive O(n²) check is too slow for n up to 10⁵. We can iterate over all possible ending positions `j` and use modular arithmetic to efficiently test all starting positions `i` that end at `j`. For each `j`, we need to know, for each possible last digit `d ∈ {1..9}`, how many starting positions `i` give a remainder `0 mod d`. Since the last digit `d` is fixed by `j`, we only need counts for that specific `d`.

We can maintain cumulative remainders while expanding the substring leftwards from `j`. For each `j`, we build the substring by extending one character to the left at a time: let `curr` be the value of `s[i..j]` modulo `d`. When we prepend a digit `c = s[i-1]`, the new value is `(c * 10^{len} + curr) mod d`. The power of 10 modulo `d` can be updated iteratively: `pow10 = (pow10 * 10) % d`. We use a dictionary (or array of size `d`) to count frequencies of remainders seen so far while scanning left from `j`, and add the count of remainder 0 to the answer. This yields O(n * average digit length) = O(n * 10) = O(10n) time, since each digit can be the last digit of at most 9 expansions? Actually, each starting position `i` is visited once per ending position `j` it appears in, but we only need to process up to 9 characters to the left because once the prefix becomes longer than 9 digits, the substring's value is guaranteed to be divisible by its last digit? Wait, that's not generally true. Let's reconsider.

Actually, the substring can be arbitrarily long, so we cannot limit to 9. However, we can use a different approach: precompute for each position `i` the cumulative value from `i` to `j` mod `d`? No, because `d` depends on `j`.

Alternative: iterate over all possible starting positions `i` and extend rightwards. For each `i`, we consider substrings starting at `i`. The last digit is `s[j]`. We can maintain the value modulo `s[j]` as we extend. But again, `d` changes with `j`.

Better: iterate over each position `j` as the ending index. For each `j`, the divisor is `d = int(s[j])` (if `d == 0`, skip). We need to count `i` such that `value(s[i..j]) % d == 0`. We can compute `value(s[i..j])` from `value(s[i+1..j])` by prepending `s[i]`. Let `prev = value(s[i+1..j]) % d`. Then `value(s[i..j]) = (s[i] * 10^{j-i} + prev) % d`. We need to know `10^{j-i} % d`. We can maintain this power as we go leftwards.

But we still have O(n²) worst case if we go all the way left from each `j`. However, we can use the fact that for a fixed `d`, we only need to consider substrings where the last digit is `d`. There are at most `n` such ending positions. For each such `j`, we could go left at most 9 steps? Why 9? Because if the substring length > 9, the substring value mod `d` depends on the last 9 digits modulo `d`? Actually, since `10^9` mod `d` cycles? Not necessarily.

Wait, there is a known solution: For each starting index `i`, we extend rightwards but only up to length 9 (or up to the next occurrence of a digit 0 as last digit? No). The key insight: For any integer, if it is divisible by its last digit, the condition is independent of leading parts beyond the last 9 digits? Let's think.

Consider substring `s[i..j]` with last digit `d`. The value is `X`. We want `X % d == 0`. Note that `X = A * 10^k + B`, where `B` is the value of the last 9 digits (or whatever), and `A` is the rest. But `10^k % d` depends on `k`. However, if we consider modulo `d`, we have `X % d == (A * (10^k % d) + B) % d`. This is not necessarily independent of `A` unless `10^k % d` is 0 or we have some periodicity.

Actually, the number of substrings is O(n²), so we need a smarter way. The constraint `n <= 10^5` suggests an O(n * something small) solution, maybe O(n * 9) or O(n log n). 

Let's search for known problems. This is "Count Substrings Divisible By Last Digit" from LeetCode? Actually, there's a LeetCode problem: "Count Substrings Divisible By Last Digit" (Weekly Contest 318 or similar). The solution involves iterating over each starting index `i` and extending rightwards up to 9 characters? Let's recall.

Wait, I remember a problem: "Number of substrings divisible by their last digit" (LeetCode 2951? No). Actually, LeetCode 2951 is "Find the Peaks". Not that.

Maybe it's from Codeforces? There's a Codeforces problem: "Substrings Divisible by Last Digit" or similar.

Let's think about the properties. For a substring ending at `j` with last digit `d`, we want `value(i, j) % d == 0`. Let's denote the substring as `s[i]s[i+1]...s[j]`. The value is `s[i]*10^{j-i} + ... + s[j]`. Modulo `d`, this is a linear combination. We can use a rolling hash approach? Not exactly, because modulus changes per ending position.

But we can fix the last digit `d` and iterate over all `j` where `s[j] == d`. For each such `j`, we want to count `i <= j` such that the value from `i` to `j` is 0 mod `d`. We can preprocess the prefix sums modulo `d`? But `d` varies.

Another approach: For each `i`, we consider substrings starting at `i`. The last digit is `s[j]`. We can compute the value modulo `s[j]` as we extend `j` rightwards. But we need to stop somewhere. The number of distinct last digits is 9. For each `i`, we can consider substrings of length up to 9? Why 9? Because if the substring is longer than 9, the last 9 digits determine divisibility? Let's test: Suppose `d = 3`. `10^k mod 3 = 1` for any `k`. So `X % 3` is just the sum of digits mod 3. So for `d=3`, we only need the last digit? No, we need the whole substring. But sum of digits mod 3 is independent of the order, and the whole number mod 3 is sum of digits mod 3. So we can use prefix sums of digits mod 3. For `d=3`, we can precompute prefix sums of digits mod 3, and for each `j` with `s[j]=3`, the number of `i` such that `(prefix[j+1] - prefix[i]) % 3 == 0` is just the count of `i` with the same prefix sum. That's O(n) for `d=3`.

Similarly for `d=9`: `10^k mod 9 = 1`, so we need the sum of digits mod 9. Prefix sum works.

For `d=1`: any number is divisible by 1. So all substrings ending with 1 count? Wait, the problem says "divisible by their non-zero last digit". So if last digit is 1, all substrings ending with 1 are valid. But we must ensure the substring is non-empty and last digit is non-zero. So for `d=1`, all substrings ending at position `j` with `s[j]=1` are valid: there are `j+1` such substrings. But we can compute using prefix sums: remainder 0 mod 1 is always 0, so all substrings ending with 1 are valid. So we can just add `j+1` for each `j` where `s[j]=1`.

For `d=2`: `10^k mod 2` is 0 for k>=1. So `X % 2` is just `s[j] % 2` if there's at least one digit before? Actually, if the substring length is 1, then `X = s[i]`. If `s[j]=2`, we need `s[i] % 2 == 0`. If length >= 2, then `X = s[i]*10^{...} + ... + s[j]`. Since `10^{k} % 2 = 0` for k>=1, all terms except possibly the first? Wait, `10^{0}=1`. Let's be careful. For a substring `s[i..j]`, the value is `sum_{k=i}^{j} s[k] * 10^{j-k}`. The term `s[j] * 10^0 = s[j]`. For `k < j`, the exponent is >=1, so `10^{j-k}` is even. Thus `X % 2 == s[j] % 2`. Since `s[j]=2` (even), `X` is always even? Not necessarily: if `s[j]=2`, then `s[j]` is even, and all other terms are even, so the sum is even. So any substring ending with 2 is divisible by 2. So for `d=2`, all substrings ending with 2 are valid. Wait, but the example says "5701283": substrings ending with 2? In example 2, they list substrings like "12", "012", "128", "7012", "0128", "70128", "570128", "701283" (ends with 3, not 2). Actually, "12" ends with 2, "012" ends with 2, "128" ends with 8, etc. Let's check: "12" is divisible by 2? 12/2=6 yes. "012" = 12/2=6 yes. "7012"/2=3506 yes. So indeed, for `d=2`, any substring ending with 2 is divisible by 2. Similarly for `d=5`: `10^k % 5 = 0` for k>=1, so `X % 5 == s[j] % 5`. Since `s[j]=5`, it's always divisible. So for `d=5`, all substrings ending with 5 are valid.

For `d=4`: `10^k mod 4` cycles: 10^0=1, 10^1=2, 10^2=0, 10^3=0,... Actually, 10^2=100 ≡ 0 mod 4. So for any exponent >=2, `10^k ≡ 0 mod 4`. So `X % 4` depends only on the last two digits? More precisely: If length >= 3, then the first term has exponent >=2, so it's 0 mod 4. Thus `X % 4` is determined by the last two digits. For length 1, it's just `s[i]`. For length 2, it's `s[i]*10 + s[j]`. So we can handle `d=4` by considering substrings of length up to 2? Actually, any substring of length >= 3 ending with 4 will have `X % 4` equal to the last two digits mod 4. So we only need to check the last two digits. But we need to count all `i`. We can precompute prefix sums of the value mod 4? But the value mod 4 for a long substring depends only on the last two digits. So for each `j` with `s[j]=4`, we need to count `i` such that the value from `i` to `j` is 0 mod 4. For `i` such that `j-i >= 2` (length >=3), the value mod 4 is determined by `s[j-1]*10 + s[j]`. So we can group by the two-digit suffix. For each suffix `(s[j-1], s[j])`, we know if it's divisible by 4. Then we need to count how many `i` have `j-i >= 2` and the suffix is that two-digit number. Actually, for a fixed `j`, the last two digits are fixed: they are `s[j-1]s[j]`. So for any `i <= j-2`, the substring length is at least 3, and the value mod 4 is the same as the two-digit number `s[j-1]s[j]`. So if that two-digit number is divisible by 4, then all substrings starting at `i <= j-2` are valid. The number of such `i` is `j-1` (i from 0 to j-2). Also we need to check substrings of length 1 and 2 starting at `j-1` and `j`. So we can compute for each `j` with `s[j]=4` the number of valid `i` by checking the suffix and adding accordingly. This is O(1) per `j`.

Similarly for `d=8`: `10^k mod 8` for k>=3 is 0. So for length >= 4, the value mod 8 depends only on the last three digits. So we can precompute the last three digits and check if divisible by 8. For each `j` with `s[j]=8`, we can count `i` with `j-i >= 3` (i <= j-3) as all valid if the last three digits are divisible by 8. Then check the three substrings of length 1,2,3 ending at `j`.

For `d=3` and `d=9`, we can use prefix sums of digit sums mod 3 or mod 9. Since `10 ≡ 1 mod 3` and `10 ≡ 1 mod 9`, the value mod 3 is just the sum of digits mod 3. So we can precompute prefix sums of digits mod 3. For each `j` with `s[j]=3`, we need to count `i` such that `(prefix[j+1] - prefix[i]) % 3 == 0`. This is the count of `i` with the same prefix sum. So we can maintain a frequency array of prefix sums modulo 3 (or 9) as we iterate `j`. This is O(n) for each `d`.

For `d=6`: Note that if a number is divisible by 6, it must be divisible by 2 and 3. But here the divisor is the last digit, which is 6. We want the number to be divisible by 6. Since the last digit is 6, the number is even, so it's divisible by 2 automatically. We also need divisibility by 3. So we need the number to be divisible by 3. Since `10 ≡ 1 mod 3`, again the value mod 3 is the sum of digits mod 3. So we can use the same prefix sum approach for mod 3, but we also need to ensure the number is even? Actually, if the last digit is 6, the number is always even. So the condition reduces to: the number is divisible by 3. So for `d=6`, we just need the number to be divisible by 3. And since the last digit is 6, it's automatically even. But wait, is it always even? Yes, any number ending with 6 is even. So divisibility by 6 is equivalent to divisibility by 3. So we can use the same prefix sum for mod 3, but we must ensure that the substring ends with 6. So for each `j` with `s[j]=6`, we count `i` such that the sum of digits from `i` to `j` is divisible by 3. This is exactly the prefix sum approach for mod 3. So we can reuse the mod 3 counts for `d=6`. However, we must be careful: for `d=3`, we count substrings ending with 3. For `d=6`, we count substrings ending with 6. Both use the same mod 3 condition. So we can process `d=3` and `d=6` together by iterating `j` and if `s[j]` is 3 or 6, we add the count of prefix sum matches.

For `d=7`: `10^k mod 7` cycles with period 6. So the value mod 7 depends on the entire substring. But we can still handle it by iterating over all starting positions? That would be O(n^2). However, we can limit the length of substrings we consider? For a fixed `d`, as we extend leftwards, the value mod `d` depends on the entire prefix. We can use a hash map of remainders while scanning leftwards from `j`. But that is O(n^2) worst case. However, we can limit the length of substrings we consider to at most 9? Why 9? Because for any `d`, the sequence of powers of 10 modulo `d` is periodic with period at most `d-1` (if `gcd(10,d)=1`), but for `d` not coprime to 10, the period might be smaller. Actually, the period of `10^k mod d` divides `λ(d)` (Carmichael function) or `φ(d)`, but for `d` up to 9, we can compute. But the key observation: For any `d`, if the substring length exceeds some bound, the condition might be determined by a suffix? Not necessarily.

Wait, the known solution for this problem (I think it's LeetCode 2955? No, 2955 is "Number of Subarrays With XOR Equals K"). Let's search memory: There is a LeetCode problem called "Count Substrings Divisible By Last Digit" (Weekly Contest 324? Problem 2951? Actually, LeetCode 2951 is "Find the Peaks". 2952 is "Number of Subarrays With XOR Equals K". 2953 is "Count Complete Substrings". Not that.

Maybe it's from a different platform. I recall a problem: "Substrings Divisible by Last Digit" on LeetCode? Let me think: LeetCode 2316? No. 2414? No.

Wait, I remember a problem: "Count Substrings Divisible By Last Digit" from LeetCode Weekly Contest 318? Let's check: Weekly Contest 318 was in November 2022. Problem 1: "2373. Largest Local Values in Grid". Problem 2: "2374. Node With Highest Edge Score". Problem 3: "2375. Construct Smallest Number From DI String". Problem 4: "2376. Count Special Integers". Not that.

Maybe it's from Codeforces: Round 1792? Not sure.

Let's think differently. Since `n` is up to 10^5, and the last digit is at most 9, we can group by the last digit. For each last digit `d`, we want to count substrings ending with `d` that are divisible by `d`. For `d=1,2,3,4,5,6,7,8,9`. We already have O(n) or O(n*9) solutions for `d=1,2,3,4,5,6,8,9`. The problematic one is `d=7`. For `d=7`, `10^k mod 7` cycles: 10^0=1, 10^1=3, 10^2=2, 10^3=6, 10^4=4, 10^5=5, 10^6=1, period 6. So if we consider substrings ending with 7, the value mod 7 depends on the last `L` digits where `L` is the length. But we can use the fact that the number of substrings is O(n^2), but we can limit the length we consider? For `d=7`, if the substring is very long, the value mod 7 might be determined by the last 6 digits? Actually, since `10^6 ≡ 1 mod 7`, we can write the number as `A * 10^6 + B`, where `B` is the last 6 digits. Then `X mod 7 = (A + B) mod 7`. This means that the value mod 7 depends on the sum of blocks of 6 digits. But the number of digits can be up to 10^5. So we can use a sliding window of size 6? Not exactly.

Alternatively, we can use a different approach: for each starting position `i`, we extend rightwards up to a certain length (like 9 or 10) and check the condition. Why would that work? Let's test: Suppose we have a substring of length 100 ending with 7. We want to know if it's divisible by 7. Does it depend on the whole 100 digits? Yes, but we can compute the value mod 7 incrementally. We can just iterate `i` from 0 to n-1, and for each `i`, we extend `j` from `i` to `i+9` (or more) and maintain the value mod `d` where `d = int(s[j])`. But the divisor `d` changes with `j`. So for a fixed `i`, as we increase `j`, the divisor is the new last digit. We can compute the value mod that divisor. Since the divisor is at most 9, we can compute `value(i,j) mod d` for each `j`. But we need to do this for all `i`. If we limit the length to 9, then the total number of substrings considered is O(9n) = O(n). Why 9? Because for any integer, the value modulo `d` (for d<=9) is determined by the last 9 digits? No, that's not generally true. For example, 1000000007 mod 7? Actually, 10^9 mod 7 =? 10^6 ≡ 1, so 10^9 = 10^6 * 10^3 ≡ 1 * 10^3 ≡ 6 mod 7. So the value mod 7 depends on the last 6 digits? Actually, since 10^6 ≡ 1, any number X can be split into blocks of 6 digits: X = A * 10^6 + B, where B is the last 6 digits. Then X mod 7 = (A mod 7 + B mod 7) mod 7. So the value mod 7 depends on the sum of the 6-digit blocks. But if we only take the last 9 digits, that includes at most two blocks of 6 digits. For a number of length 10^5, the value mod 7 is not determined by the last 9 digits alone; the higher blocks matter. However, we can use the fact that we are iterating over all starting positions. For a fixed starting position `i`, as we extend `j`, we are building the number from left to right. We can maintain the value modulo the current last digit `d`. But we need to check for each `j` if the current value is divisible by `d`. Since we are building incrementally, we can keep the value mod `d` for the current `d`. But when we move to the next `j`, the divisor changes. So we would need to recompute? That seems messy.

Wait, there is a known trick: For each starting position `i`, we only need to consider substrings up to length 9 (or 10) because the number of digits beyond that doesn't affect divisibility? Let's verify with an example. Take `d=7`. Suppose we have a number X with many digits. Is it true that if X is divisible by 7, then the number formed by the last 9 digits is also divisible by 7? Not necessarily. For example, 1000000007 is divisible by 7? 1000000007 / 7 = 142857143.857... Actually 7*142857143 = 999999001? Let's compute: 7*142857143 = 999999001. 1000000007 - 999999001 = 1006. 1006/7 = 143.714... No. 1000000007 mod 7: 10^9 mod 7 = 6, so 1000000007 = 1*10^9 + 7 ≡ 1*6 + 0 = 6 mod 7. So not divisible. But 1000000007 is not divisible by 7 anyway. What about 1000000006? That's 1000000006 = 1*10^9 + 6 ≡ 6+6=12≡5 mod 7. Not divisible.

But consider a number like 1000000009 (last digit 9, not 7). Not relevant.

Maybe the property is: For any d, if a number is divisible by d, then the number formed by the last k digits is also divisible by d for sufficiently large k? No, that's false. For example, 21 is divisible by 3, but 1 is not. So it's the opposite: the whole number is divisible by d iff the last k digits (for appropriate k) plus the rest times something is divisible.

Actually, there is a known rule for divisibility by 7: 1001 is divisible by 7, so 10^3 ≡ -1 mod 7. More generally, 10^6 ≡ 1 mod 7. So for any number, X mod 7 can be computed by splitting into 6-digit blocks. But this doesn't limit the number of blocks we need to consider. However, if we iterate over all starting positions and extend rightwards, we can stop after length 9 because for length > 9, the number of substrings ending with 7 that are divisible by 7 is rare? No, that's not a proof.

Let's search for the problem statement. I recall a problem: "Count Substrings Divisible By Last Digit" on LeetCode with difficulty Hard. The solution involves iterating over each starting index and extending up to 9 characters to the right, because for any integer, if it is divisible by its last digit, the last digit is at most 9, and the value modulo that digit can be determined by the last 9 digits? Wait, that doesn't sound right.

Let's think about modular arithmetic. For a fixed last digit `d`, the value of a substring `s[i..j]` modulo `d` is what we care about. We can precompute prefix sums modulo `d`? But `d` changes. However, we can precompute for each position `i` and each `d` the value of `s[i..i+len] mod d` for `len` up to some bound. But that's too much.

Another angle: The total number of substrings is O(n^2). We need O(n) or O(n log n). The only way is to use the fact that the divisor is at most 9. For each divisor `d`, we need to count pairs `(i, j)` with `i <= j`, `s[j] = d`, and `value(i,j) % d == 0`. We can treat each `d` separately. For `d=1,2,3,4,5,6,8,9`, we have O(n) solutions. For `d=7`, we need a different approach. For `d=7`, the modulus is coprime to 10, so the powers of 10 modulo 7 are periodic with period 6. We can use a hash map of remainders for substrings ending at each position? But we need to consider all starting positions. For a fixed ending position `j`, we want to count `i` such that `value(i,j) % 7 == 0`. We can express `value(i,j) = s[i]*10^{j-i} + s[i+1]*10^{j-i-1} + ... + s[j]`. This is a sum of terms. If we define a new array where each element is weighted by powers of 10, we might use a prefix sum. But the power depends on the length. However, we can use the periodicity. Since `10^6 ≡ 1 mod 7`, we can write `10^k = 10^{k mod 6} * (10^6)^{floor(k/6)} ≡ 10^{k mod 6}`. So the value modulo 7 is actually a linear combination where the coefficient of `s[t]` is `10^{j-t} mod 7`. This coefficient depends on `j-t`. So it's not a simple prefix sum with constant weights. But we can still use a rolling hash? Actually, we can maintain a running value modulo 7 as we extend the substring. For a fixed starting position `i`, we can compute the value mod 7 for all substrings starting at `i` by iteratively appending digits. But we need to do this for all `i`. That's O(n^2) if we go to the end. However, we can limit the length of substrings we consider? For a fixed `i`, as we increase `j`, the value mod 7 changes. We can compute it in O(1) per step. But we would need to do this for all `i`, leading to O(n^2). But maybe we can stop after a certain length because the number of substrings of length > L is small? No, n is 10^5, so substrings of length > 9 are many.

Wait, the example with n=10^5, if we consider all substrings ending with 7, there are O(n^2) possible. But we only need to count those divisible by 7. The number of such substrings could be O(n^2) as well? For example, if the string is all 7's, then every substring ending with 7 is divisible by 7? Actually, a number like 77 is divisible by 7? 77/7=11. 777/7=111. So yes, a string of all 7's has O(n^2) substrings divisible by 7. So we need a way to count them efficiently.

For a string of all 7's, the number of substrings ending with 7 is O(n^2), and all of them are divisible by 7. How can we count them efficiently? The answer would be the total number of substrings, which is n(n+1)/2. But our algorithm must compute that. If we iterate over ending positions `j`, for each `j` we need to count the number of starting positions `i`. For a string of all 7's, for a fixed `j`, all `i` from 0 to j are valid. So we need to add `j+1` for each `j`. So we need a way to quickly determine that for this specific `d=7` and this specific string, all `i` are valid. But in general, we need a method that works for any string.

So for `d=7`, we need to count for each `j` the number of `i <= j` such that `value(i,j) % 7 == 0`. Let's denote `f(j) = value(0,j) % 7`. Then `value(i,j) = value(0,j) - value(0,i-1) * 10^{j-i+1}`. So `value(i,j) % 7 == 0` iff `f(j) ≡ f(i-1) * 10^{j-i+1} mod 7`. This is not a simple equation because of the power of 10. However, we can use the fact that `10^6 ≡ 1 mod 7`. So the power of 10 modulo 7 depends only on the exponent modulo 6. So `10^{j-i+1} mod 7 = 10^{(j-i+1) mod 6} mod 7`. This means that for a fixed `j`, as we vary `i`, the multiplier `10^{j-i+1} mod 7` cycles with period 6 in the difference `j-i`. So we can group starting positions `i` by the value of `(j-i+1) mod 6`. For each group, the multiplier is constant. Then the condition becomes: for `i` in that group, `f(i-1) * c ≡ f(j) mod 7`, where `c = 10^{(j-i+1) mod 6} mod 7`. So we need to know, for each possible multiplier `c` and each residue `r`, how many `i` have `(j-i+1) mod 6 = k` and `f(i-1) = r`. Since there are only 6 groups (k=0..5) and 7 residues (r=0..6), we can maintain a 2D array `cnt[k][r]` as we scan `j` from left to right. At each `j`, we first add `i=j` (i.e., the substring of length 1) to the appropriate `cnt`. Then for the current `j`, we look at the 6 groups: for each `k`, the required residue is `r = f(j) * inv(c) mod 7`. Then the number of valid `i` in that group is `cnt[k][r]`. We sum over k. This is O(6) per `j`, so O(6n) = O(n). This is a known technique for divisibility by 7 (and other moduli coprime to 10).

Let's verify: For `d=7`, we maintain `cnt[k][r]` for `k` from 0 to 5 (representing the length mod 6, i.e., `j-i+1 mod 6`), and `r` from 0 to 6 (the value of `f(i-1) mod 7`). Actually, `f(i-1)` is the value of the prefix up to `i-1` modulo 7. As we increase `j`, we add the new `i=j+1`? Wait, careful with indices.

Let's define: Let `pref[j]` be the value of the substring `s[0..j-1]` modulo 7 (i.e., the first j digits). So `pref[0] = 0`. Then `pref[j] = (pref[j-1] * 10 + int(s[j-1])) % 7`. The value of substring `s[i..j]` is `value(i, j) = (pref[j+1] - pref[i] * 10^{j-i+1}) % 7`? Actually, careful: `pref[j+1]` is the value of the first `j+1` digits. The value of the first `i` digits is `pref[i]`. So the substring from `i` to `j` (inclusive) is `value = (pref[j+1] - pref[i] * 10^{j-i+1}) mod 7`. Because the first `i` digits form the number `pref[i]`, and they are shifted left by `j-i+1` positions. So `value(i, j) = (pref[j+1] - pref[i] * pow10(j-i+1)) mod 7`. We want this to be 0 mod 7. So `pref[j+1] ≡ pref[i] * pow10(j-i+1) mod 7`. Here `pow10(k) = 10^k mod 7`. Let `len = j-i+1`. So `pref[j+1] ≡ pref[i] * pow10(len) mod 7`. Since `pow10(len)` depends only on `len mod 6`, we can let `c = pow10(len mod 6)`. Then the condition is `pref[i] ≡ pref[j+1] * inv(c) mod 7`. For a fixed `j`, we know `pref[j+1]`. For each possible `len mod 6` (which corresponds to a specific `i`), the required `pref[i]` is fixed. But `i` is not determined by `len mod 6` alone; we need to count all `i <= j` such that `(j-i+1) mod 6 = k` (so `len mod 6 = k`) and `pref[i] = required`. As we iterate `j` from 0 to n-1, we can maintain a 2D array `cnt[k][r]` where `k = (j - i + 1) mod 6`? Actually, for a given `i`, when we are at ending position `j`, the `len = j-i+1`. So `k` is determined by `j` and `i`. If we fix `j`, then for each `i`, `k = (j - i + 1) mod 6 = (j+1 - i) mod 6`. So if we maintain `cnt` indexed by `i mod 6` and `pref[i]`, we can query. Specifically, for a given `j`, we want to sum over `i` from 0 to j: `cnt[(j+1 - i) mod 6][pref[i]]` where the required `pref[i]` is `pref[j+1] * inv(pow10((j+1 - i) mod 6)) mod 7`. So we can maintain an array `cnt[6][7]` where `cnt[k][r]` is the number of indices `i` such that `i mod 6 = k` and `pref[i] = r`. As we iterate `j` from 0 to n-1, before processing `j`, we have added `i=0`? Actually, we need to add `i` as we go. Let's step through.

Initialize `cnt` to zeros. For `j` from 0 to n-1:
- First, we need to add the current `i`? Actually, the condition is for `i <= j`. The substring ends at `j`. So the starting index `i` can be 0,1,...,j. For a given `j`, we want to count all `i` in that range. So we should first query using the current `cnt` (which contains information about `i` from previous iterations? No, `i` can be equal to `j` as well (substring of length 1). So we need to include `i=j`. But at the moment of processing `j`, we haven't yet added `pref[j]` to `cnt`? Actually, `pref[i]` is defined for all `i` from 0 to n. For the substring `s[i..j]`, the starting index is `i`, and the prefix value is `pref[i]`. So we need to have `cnt` containing all `i` from 0 to j. So we should first add the current `i=j` to `cnt`? But `i` ranges from 0 to j. So before querying for `j`, we should have added `i=j`? No, for the substring starting at `i=j`, the length is 1. The condition is: `value(j, j) = int(s[j])` is divisible by `d=7`. So we need to check that separately? Or we can include it in the formula. The formula `pref[j+1] ≡ pref[i] * pow10(j-i+1) mod 7` holds for `i <= j`. For `i=j`, `len=1`, so `pow10(1) = 10 mod 7 = 3`. So the condition is `pref[j+1] ≡ pref[j] * 3 mod 7`. But `pref[j+1] = (pref[j] * 10 + s[j]) mod 7`. So `pref[j+1] - pref[j] * 3 = pref[j] * (10-3) + s[j] = pref[j] * 7 + s[j] ≡ s[j] mod 7`. So the condition becomes `s[j] ≡ 0 mod 7`. So it's consistent. So we can include `i=j` in the count. But to include `i=j`, we need to have `pref[i]` in `cnt`. So we should add `pref[i]` to `cnt` for `i=0,...,j`. But wait, `pref[i]` depends on `i` itself. So we can process as follows: iterate `i` from 0 to n. For each `i`, we consider `j` such that the substring ends at `j` with `s[j]=d`. But that seems messy.

Alternatively, we can iterate over ending positions `j`. For each `j`, we want to count all `i` from 0 to j. So we can maintain `cnt` that is updated after processing `j` for the next `j+1`. But for the current `j`, we need `cnt` to contain all `i` from 0 to j. So we should first add the current `i=j` to `cnt`? Actually, the starting index `i` can be `j`. So yes, we need to include `i=j` in the count for `j`. So we should first update `cnt` with `i=j` and then query? But if we update with `i=j` first, then when we query, we are including `i=j`. That's correct. So the order: for each `j` from 0 to n-1:
- If `s[j] == '7'`, then we compute the number of valid `i` in [0, j] using current `cnt` (which already includes `i` from previous iterations, but not `i=j` yet? Wait, we need to include `i=j`. So we should first add `i=j` to `cnt`? But `i=j` is not a prefix; we need to add `pref[i]` where `i=j`. But `pref[j]` is the value of the first j digits. For `i=j`, the condition uses `pref[i] = pref[j]`. So we should add `pref[j]` to `cnt` before querying. But `pref[j]` is known as we iterate `j` because we can compute `pref[j]` on the fly. So we can do:
```
pref = 0
cnt = [[0]*7 for _ in range(6)]  # cnt[k][r] where k = i % 6? Actually, k = (j+1 - i) % 6? Let's be consistent.
```
Wait, the key is: for a given `j` and `i`, the length `len = j - i + 1`. We want to group by `len mod 6`. So `k = len mod 6 = (j - i + 1) mod 6`. So if we maintain `cnt` where the key is `len mod 6`? That depends on `j` and `i`. It's easier to maintain by `i mod 6` and then compute `k = (j+1 - i) mod 6`. So we can maintain `cnt[i mod 6][pref[i]]`. Then for a given `j`, we iterate over all possible `i mod 6` (which is `i0`), then for each `i0`, the corresponding `k` is `(j+1 - i0) mod 6`. But we need to sum over all `i` with that `i0`, but the condition also depends on `pref[i]`. Actually, if we fix `i0`, then `i` runs over all indices with `i ≡ i0 (mod 6)`. For each such `i`, `k = (j+1 - i) mod 6 = (j+1 - i0) mod 6` (since `i ≡ i0`). So for a fixed `j`, all `i` with the same `i0` have the same `k`. So we can group by `i0`. For each `i0`, we need to count how many `i` with `i ≡ i0 (mod 6)` have `pref[i] = required`, where `required = pref[j+1] * inv(pow10(k)) mod 7`, and `k = (j+1 - i0) mod 6`. So we can maintain `cnt[i0][r]` where `i0` is from 0 to 5, and `r` is from 0 to 6. As we iterate `j` from 0 to n-1, we first add the current `i=j` to `cnt`? Actually, the prefix index `i` goes from 0 to n. For `i=0`, `pref[0]=0`. For `i=1`, `pref[1]` is the first digit, etc. So we can compute `pref` iteratively. For each `j`, we have `pref[j]` (the value of the first j digits) and `pref[j+1]` (the value of the first j+1 digits). We want to count `i` from 0 to j. So we should have `cnt` containing all `i` from 0 to j. That means before querying for `j`, we need to have added `i=j` to `cnt`. So we can do: at the start of the loop for `j`, we first add `i=j` to `cnt` using `pref[j]`. But wait, `i=j` corresponds to `pref[i] = pref[j]`. So we compute `pref[j]` and add it to `cnt[j % 6][pref[j]]`. Then we query for the current `j` if `s[j] == '7'`. The query uses `pref[j+1]`. So we need to compute `pref[j+1]` as well. We can compute it: `pref[j+1] = (pref[j] * 10 + int(s[j])) % 7`. So the order:
1. Initialize `pref = 0`, `cnt = [[0]*7 for _ in range(6)]`.
2. Add `i=0` to `cnt`: `cnt[0 % 6][pref] += 1` (since `i=0`, `pref[0]=0`).
3. Iterate `j` from 0 to n-1:
   a. If `s[j] == '7'`:
      - We want to count `i` from 0 to j such that `value(i,j) % 7 == 0`.
      - We have `pref[j+1]` available? We can compute it now: `pref_next = (pref * 10 + int(s[j])) % 7`. But we need to be careful: we already added `i=j`? No, at this point, we have added `i=0` and maybe previous `i`? Actually, we need to add `i=j` before querying. So we should first add `i=j` using the current `pref` (which is `pref[j]`). Then compute `pref_next` and use it to query. But wait, the condition for `i=j` uses `pref[i] = pref[j]` and `len=1`. So if we add `i=j` before querying, it will be included. So:
   - Add current `i=j`: `cnt[j % 6][pref] += 1`.
   - Compute `pref_next = (pref * 10 + int(s[j])) % 7`.
   - Now query: for each `i0` from 0 to 5, we need to find the number of `i` with `i ≡ i0 (mod 6)` and `pref[i] = required`. But note: the set of `i` we have in `cnt` includes `i=0` and all previous `i` that we added in previous iterations. But in the previous iterations, we added `i` equal to the current `j` of that iteration. So after step 3a for a given `j`, we have added `i=j` to `cnt`. So for the next `j+1`, `cnt` will include all `i` from 0 to `j`. So the query for `j` should use `cnt` that includes `i` up to `j`. That means we should add `i=j` to `cnt` before the query. So the order is:
   - Add `i=j` to `cnt`.
   - Compute `pref_next`.
   - If `s[j] == '7'`, do the query using `pref_next` and current `cnt`.
   - Then update `pref = pref_next` for the next iteration.

Let's test this with a simple string: s = "7". n=1.
- Initialize pref=0, cnt all zeros.
- Add i=0: cnt[0][0] = 1.
- j=0: s[0]='7'.
  - Add i=0? Wait, i=0 is already added. But we need to add i=j=0. That's the same as i=0. So we should add it. But it's already there. So we can just add again, but careful: we don't want to double count. Actually, the first add was for i=0 before the loop. For j=0, i=j=0, so we are adding the same i again. That's wrong because for the substring starting at i=0 and ending at j=0, we should only count it once. So we should not add i=0 again. We should add i=j only if j > 0. More precisely, the set of i to consider for ending j is i in [0, j]. So at the start of the loop for j, we need to have cnt contain i from 0 to j. For j=0, that's i=0 only. So before the loop, we added i=0. For j=1, we need i=0 and i=1. So we should add i=1 at the start of j=1. So the pattern: at the start of iteration for j, we add i=j to cnt. So for j=0, we add i=0? But we already added i=0 before the loop. So we should not pre-add i=0. Instead, we start with cnt empty, and at the beginning of each j, we add i=j. Then for j=0, we add i=0, then query. For j=1, we add i=1, then query (which will consider i=0 and i=1). So the initial state: cnt is empty. For j from 0 to n-1:
- Add i=j to cnt: `cnt[j % 6][pref] += 1`. But what is `pref`? For i=j, we need `pref[i] = pref[j]`. So we need to have `pref[j]` computed. But we are updating `pref` as we go. So we need to compute `pref` iteratively. Let's define: before the loop, `pref = 0` (this is `pref[0]`). For j=0: we want to add i=0. `pref[0] = 0`. So we do `cnt[0 % 6][pref] += 1`. Then we compute `pref_next = (pref * 10 + int(s[0])) % 7`. Then if s[0]=='7', we query using `pref_next`. Then set `pref = pref_next` for the next iteration.
For j=1: now `pref` is `pref[1]` (value of first digit). We add i=1: `cnt[1 % 6][pref] += 1`. Then compute `pref_next = (pref * 10 + int(s[1])) % 7`. Query if s[1]=='7'. Then set `pref = pref_next`.
This way, for j=0, cnt contains i=0. For j=1, cnt contains i=0 and i=1. So the query for j=0 uses cnt with i=0 only. That's correct.
Now, the query: for a given j, we have `pref_next` which is `pref[j+1]`. We need to count i in [0, j] such that `pref[i] * pow10(j-i+1) ≡ pref_next mod 7`. Let `k = (j - i + 1) mod 6`. We can group by `i mod 6`. Let `i0 = i mod 6`. Then `k = (j - i + 1) mod 6 = (j+1 - i) mod 6 = (j+1 - i0) mod 6`. So for each `i0` from 0 to 5, we compute `k = (j+1 - i0) % 6`. Then the required `pref[i]` is `pref_next * inv(pow10(k)) mod 7`. Let `r = (pref_next * inv_pow10[k]) % 7`. Then the number of valid i with `i ≡ i0 (mod 6)` and `pref[i] = r` is `cnt[i0][r]`. We sum over i0. Note: `pow10` is a precomputed array of length 6: `pow10[k] = 10^k % 7` for k=0..5. Actually, we need `pow10(k)` for k from 0 to 5. But `len = j-i+1`, so `k` is `len mod 6`. So we can precompute `pow10_mod7 = [1, 3, 2, 6, 4, 5]` (since 10^0=1, 10^1=3, 10^2=2, 10^3=6, 10^4=4, 10^5=5, 10^6=1). And we need the multiplicative inverse of these modulo 7. Since 7 is prime, we can precompute inv for each. Or we can compute on the fly: inv(c) = c^(5) mod 7. But we can also precompute a table.
But note: `k` depends on `i0` and `j`. For a fixed `j`, as we vary `i0`, `k` cycles through all 6 values? Actually, `k = (j+1 - i0) mod 6`. Since `i0` runs 0..5, `k` runs 0..5 in some order. So we can just iterate over `i0`.
So the query loop:
```
ans = 0
for i0 in range(6):
    k = (j+1 - i0) % 6
    r = (pref_next * inv_pow10[k]) % 7
    ans += cnt[i0][r]
```
This counts all i in [0, j] with the condition. Note that this includes i=j? Let's check: when i=j, then i0 = j % 6. Then k = (j+1 - j) % 6 = 1. So we need pref[j] * pow10(1) ≡ pref_next mod 7. But pref_next = (pref[j] * 10 + s[j]) mod 7. So pref[j] * 3 ≡ pref[j] * 10 + s[j] mod 7 => pref[j] * 7 + s[j] ≡ 0 => s[j] ≡ 0 mod 7. So it correctly checks if the single digit is divisible by 7. So it's correct.
Now, for each j with s[j]=='7', we compute this sum and add to the total answer. Also, we need to add the substrings of length 1 that are just a non-zero digit? Wait, the problem says "divisible by their non-zero last digit". For a substring of length 1 with digit d (non-zero), the value is d, and we need d % d == 0, which is always true. So all single-digit substrings with non-zero digit are valid. Do we count them in the above? For d=7, a single digit '7' is counted when i=j. So yes, it's included. But what about d=1,2,3,4,5,6,8,9? For those, we have separate logic. For d=7, the above logic handles all substrings ending with 7. So we can just use this for d=7.
But wait, the problem includes all last digits 1-9. For d=1,2,3,4,5,6,8,9, we can use simpler methods. For d=7, we use the above.
Now, we need to ensure that we don't double count. The total answer is the sum over all d of the counts for substrings ending with d. Since each substring has exactly one last digit, we can process each d independently and sum.
Let's outline the solution:
1. Initialize ans = 0.
2. For d in [1,2,3,4,5,6,8,9], count substrings ending with d using specific O(n) methods.
3. For d=7, use the 2D array method.
4. Return ans.

Now, let's derive the methods for each d:

- d=1: Any number is divisible by 1. So all substrings ending with 1 are valid. For each j with s[j]='1', there are j+1 substrings ending at j (starting at any i from 0 to j). So we can just add j+1 for each such j. Or we can compute using prefix sums: for each j with s[j]='1', ans += j+1.

- d=2: As argued, for any substring ending with 2, the value mod 2 is s[j] mod 2 = 0. So all substrings ending with 2 are valid. So for each j with s[j]='2', ans += j+1.

- d=3: The value mod 3 is the sum of digits mod 3. We need the sum of digits from i to j to be divisible by 3. We can precompute prefix sums of digits mod 3. Let pref3[0]=0, pref3[i+1] = (pref3[i] + int(s[i])) % 3. Then for a substring from i to j, sum mod 3 = (pref3[j+1] - pref3[i]) % 3. We want this to be 0. So we need pref3[i] = pref3[j+1]. So for each j with s[j]='3', we need to count i in [0, j] with pref3[i] = pref3[j+1]. We can maintain a frequency array of pref3 values as we iterate j. Since we need to count for each j, we can process: iterate i from 0 to n-1? Actually, we can iterate over all positions and update the frequency of the prefix sum. For each j with s[j]='3', we add the current frequency of pref3[j+1] to ans. Then we update the frequency of pref3[j+1] for future j. But careful: we need to include i=j? For i=j, the sum is just s[j], and we need s[j] % 3 == 0. So if s[j]='3', then 3%3=0, so it should be counted. In the prefix sum method, for i=j, pref3[i] = pref3[j], and pref3[j+1] = pref3[j] + 3 mod 3 = pref3[j]. So it matches. So we can do: initialize freq3 = [0,0,0], freq3[0]=1 (for i=0). Iterate j from 0 to n-1:
   - Update pref3 = (pref3 + int(s[j])) % 3.
   - If s[j]=='3', ans += freq3[pref3] (because we want i such that pref3[i] = pref3[j+1]).
   - Then freq3[pref3] += 1.
This works.

- d=4: As argued, for substrings of length >= 3, the value mod 4 depends only on the last two digits. Specifically, for a substring from i to j with j-i+1 >= 3, the value mod 4 is (s[j-1]*10 + s[j]) % 4. So if that two-digit number is divisible by 4, then all substrings starting at i <= j-2 are valid. The number of such i is j-1 (i from 0 to j-2). Also we need to check the substrings of length 1 and 2: length 1: i=j, value = s[j], need s[j] % 4 == 0. Since s[j]='4', 4%4=0, so valid. Length 2: i=j-1, value = s[j-1]*10 + s[j], need that % 4 == 0. So for each j with s[j]='4', we can compute:
   - Check length 2: if j>=1, let two = s[j-1]*10 + int(s[j]); if two % 4 == 0, add 1.
   - Check length 1: always valid (since s[j]='4'), add 1.
   - For length >=3: if j>=2, let two = s[j-1]*10 + int(s[j]); if two % 4 == 0, then add (j-1) because i can be 0 to j-2.
   Note: The length >=3 condition requires the two-digit number to be divisible by 4. But wait, is that sufficient? For any i <= j-2, the value mod 4 is indeed the two-digit number mod 4. So if two % 4 == 0, then all those are valid. So we add j-1. If two % 4 != 0, then none of them are valid. So we can do this in O(1) per j.

- d=5: Similar to d=2, all substrings ending with 5 are divisible by 5. So for each j with s[j]='5', ans += j+1.

- d=6: A number ending with 6 is even, so divisible by 2. We also need divisibility by 3. So we need the sum of digits to be divisible by 3. So we can use the same prefix sum mod 3 as for d=3. For each j with s[j]='6', we need to count i in [0, j] such that (pref3[j+1] - pref3[i]) % 3 == 0. So we can maintain a separate frequency for d=6, or reuse the same freq3. But careful: we need to count substrings ending with 6, not 3. So we can iterate j, and if s[j]=='6', add freq3[pref3]. Then we update freq3. But we also need to count the single digit '6': 6%3=0, so it's included. So we can do the same loop: for each j, update pref3, then if s[j] in ['3','6'], add freq3[pref3] to ans. But wait, for d=3, we need to add for s[j]='3'. For d=6, we need to add for s[j]='6'. So we can just check: if s[j] == '3' or s[j] == '6', then ans += freq3[pref3]. But we must ensure we don't double count? Actually, the same substring cannot end with both 3 and 6, so we can just add for both. However, we need to maintain freq3 correctly. The frequency of prefix sums is the same regardless of the last digit. So we can do: iterate j from 0 to n-1:
   - Update pref3 = (pref3 + int(s[j])) % 3.
   - If s[j] == '3' or s[j] == '6', ans += freq3[pref3].
   - freq3[pref3] += 1.
This counts substrings ending with 3 or 6 that are divisible by their last digit. But wait: for d=3, we need divisibility by 3. For d=6, we need divisibility by 6. We argued that divisibility by 6 is equivalent to divisibility by 3 given the last digit is 6. But is that always true? A number ending with 6 is always even, so it's divisible by 2. So divisibility by 6 is equivalent to divisibility by 2 and 3. Since 2 is guaranteed, we only need 3. So yes. So the condition is exactly the same as for d=3. So we can use the same frequency array. But we need to be careful: the condition for d=3 is that the number is divisible by 3. The condition for d=6 is that the number is divisible by 6. But the number is automatically even, so it's divisible by 6 iff it's divisible by 3. So the count is the same. So we can combine them.

- d=8: Similar to d=4, but for length >= 4, the value mod 8 depends on the last three digits. For each j with s[j]='8':
   - Length 1: always valid (8%8=0).
   - Length 2: i=j-1, value = s[j-1]*10 + 8. Check if divisible by 8.
   - Length 3: i=j-2, value = s[j-2]*100 + s[j-1]*10 + 8. Check if divisible by 8.
   - Length >=4: i <= j-3. The value mod 8 is the last three digits mod 8. So if the three-digit number is divisible by 8, then all substrings starting at i <= j-3 are valid. Number of such i is j-2 (i from 0 to j-3). So we can compute:
        if j>=2: three = s[j-2]*100 + s[j-1]*10 + int(s[j]); if three % 8 == 0, add j-2.
        Also add the individual checks for length 2 and 3. And length 1.
   But wait, for length >=4, we need the three-digit number to be divisible by 8. But is that sufficient? For any i <= j-3, the value mod 8 is indeed the three-digit number mod 8? Let's verify: For a substring from i to j, the value is sum_{k=i}^{j} s[k] * 10^{j-k}. The terms with k <= j-3 have exponent >=3, so 10^{j-k} is divisible by 1000. 1000 mod 8 = 0. So those terms are 0 mod 8. The remaining terms are for k = j-2, j-1, j. So the value mod 8 is (s[j-2]*10^2 + s[j-1]*10 + s[j]) % 8. So yes, it depends only on the last three digits. So if that is divisible by 8, then all i <= j-3 yield a valid substring. So we can add j-2. But we must also check the substrings of length 2 and 3 separately, because they might be valid even if the three-digit number is not? Actually, if the three-digit number is divisible by 8, then length 3 is valid. But if it's not, length 3 might still be valid? No, length 3 is exactly the three-digit number, so it's valid iff the three-digit number is divisible by 8. So we can just check the three-digit number for length 3, and for length >=4, we add j-2 if the three-digit number is divisible by 8. But wait, for length 2, it's a two-digit number, which might be divisible by 8 even if the three-digit number is not. So we need to check length 2 separately. Also length 1 is always valid. So the total for a given j is: 1 (length 1) + (1 if length 2 valid) + (1 if length 3 valid) + (j-2 if length 3 valid). But careful: if length 3 is valid, then we add j-2 for length >=4, plus the 1 for length 3. So we can combine: if three % 8 == 0, then add (j-2) + 1 = j-1? Actually, j-2 is for i from 0 to j-3, which is j-2 values. And length 3 is one more. So total from length 3 and >=4 is (j-2) + 1 = j-1. Then add length 2 if valid, and length 1. So we can do:
        add 1 for length 1.
        if j>=1: two = s[j-1]*10 + 8; if two % 8 == 0: add 1.
        if j>=2: three = s[j-2]*100 + s[j-1]*10 + 8; if three % 8 == 0: add (j-1) (which includes length 3 and all longer ones? Wait: if three is valid, then for i <= j-3, the value is the same as the three-digit number, so all those j-2 substrings are valid. Plus the length 3 substring itself. So total j-1. But we also have length 2 and length 1. So we add them separately. So we can do: if three % 8 == 0: ans += (j-1) (for i <= j-2). Then we also need to check length 2 separately. But note: if three % 8 == 0, then the two-digit number s[j-1]*10+8 might not be divisible by 8. So we check length 2 independently. So the total for j is: 1 + (1 if two%8==0) + (j-1 if three%8==0). But wait, what if j<2? Then we can't compute three. We need to handle edge cases.

- d=9: Similar to d=3, using prefix sums mod 9. For each j with s[j]='9', we need the sum of digits from i to j to be divisible by 9. So we can precompute prefix sums mod 9 and maintain a frequency array. For each j, update pref9 = (pref9 + int(s[j])) % 9. If s[j]=='9', add freq9[pref9]. Then update freq9[pref9]++. This is O(n).

Now, for d=7, we use the 2D array method described earlier.

Let's verify the methods with the examples.

Example 1: s = "12936"
- d=1: s[j]='1' at j=0. j+1=1. So ans +=1.
- d=2: s[j]='2' at j=0. j+1=1. So ans +=1.
- d=3: s[j]='3' at j=3? Wait, s="12936": indices 0:1, 1:2, 2:9, 3:3, 4:6. So s[3]='3'. For d=3, we use prefix sums mod 3.
  pref3: start 0.
  j=0: s[0]=1, pref3=1. s[0]!='3', so no add. freq3[1]++.
  j=1: s[1]=2, pref3=(1+2)%3=0. s[1]!='3'. freq3[0]++.
  j=2: s[2]=9, pref3=(0+9)%3=0. s[2]!='3'. freq3[0]++.
  j=3: s[3]=3, pref3=(0+3)%3=0. s[3]=='3', so add freq3[0]. freq3[0] is currently 2 (from j=1 and j=2? Actually, after j=2, freq3[0] was incremented twice? Let's track: initially freq3[0]=1 (for i=0). After j=0: freq3[1]=1. After j=1: freq3[0]=2. After j=2: freq3[0]=3. So at j=3, pref3=0, so add 3. Then update freq3[0]++ -> 4.
  j=4: s[4]=6, pref3=(0+6)%3=0. s[4]!='3'. freq3[0]++.
  So for d=3, we added 3. But the example says substrings ending with 3 that are divisible by 3: "1293"? Actually, "1293" ends with 3, value 1293/3=431. "293" ends with 3, 293/3=97.666 no. "93" ends with 3, 93/3=31. "3" ends with 3, 3/3=1. Also "12936" ends with 6, not 3. So substrings ending with 3: i=3,j=3 ("3"), i=2,j=3 ("93"), i=1,j=3 ("293"), i=0,j=3 ("1293"). That's 4 substrings. But we added 3? Why? Because our condition for d=3 is that the number is divisible by 3. "293" is 293, 293 mod 3 = 2+9+3=14 mod 3=2, not divisible. So it should not be counted. But our method using prefix sums would count it if the sum of digits mod 3 is 0. For i=1, the sum from i=1 to j=3 is 2+9+3=14 mod 3=2, not 0. So why did we count it? Let's check: At j=3, pref3[j+1] = pref3[4] = sum of first 4 digits: 1+2+9+3=15 mod 3=0. For i=1, pref3[i] = pref3[1] = 1 mod 3=1. So pref3[i] != pref3[j+1]. So it should not be counted. But we added freq3[pref3[j+1]] = freq3[0]. That count is the number of i with pref3[i]=0. Which i have pref3[i]=0? i=0: pref3[0]=0. i=1: pref3[1]=1. i=2: pref3[2]=(1+2)%3=0. i=3: pref3[3]=(0+9)%3=0. So i=0,2,3. That's 3. So we counted i=0,2,3. That gives substrings: i=0,j=3: "1293" (divisible by 3? 1293/3=431 yes), i=2,j=3: "93" (93/3=31 yes), i=3,j=3: "3" (yes). So we correctly did not count i=1. So the count is 3. But wait, the example says there are 15 substrings total, and 4 are not divisible by their last digit: "29", "129", "293", "2936". So the valid substrings are 11. The substrings ending with 3: "3", "93", "1293". That's 3. So our method gave 3. Good.

- d=6: s[j]='6' at j=4. We need to count substrings ending with 6 that are divisible by 6. We use the same prefix sum mod 3. At j=4, pref3[5] = sum of first 5 digits: 1+2+9+3+6=21 mod 3=0. We need i such that pref3[i]=0. freq3[0] at that point: after j=3, freq3[0] was 4 (i=0,2,3, and also the update for j=3 itself? Actually, after j=3, we did freq3[0]++ from 3 to 4. Then j=4: we first compute pref3=0, then if s[4]=='6', add freq3[0] (which is 4), then update freq3[0]++ to 5. So we add 4. That means substrings ending at j=4 with pref3[i]=0: i=0,1? Wait, pref3[i] for i=0,1,2,3,4? We need to check which i have pref3[i]=0. i=0:0, i=1:1, i=2:0, i=3:0, i=4: pref3[4] is sum of first 4 digits? Actually, pref3[4] is the value before processing j=4? Let's be careful: pref3 is updated after processing each j. In our loop, we first update pref3 with s[j], then query. So at the moment of query for j=4, pref3 is the sum of first 5 digits? Wait, the loop: we start with pref3=0. For j=0: pref3 = (0+1)%3=1. Then if s[0]=='3' or '6', add freq3[1]. Then freq3[1]++.
For j=1: pref3 = (1+2)%3=0. Then query, then freq3[0]++.
For j=2: pref3 = (0+9)%3=0. Query, then freq3[0]++.
For j=3: pref3 = (0+3)%3=0. Query (s[3]='3'), so add freq3[0] (which is 2? Actually, after j=1: freq3[0]=1? Let's track freq3 carefully:
Initial: freq3 = [1,0,0] (for i=0, pref3=0).
j=0: s[0]=1, pref3=1. s[0] not 3/6. freq3[1]++ -> [1,1,0].
j=1: s[1]=2, pref3=0. s[1] not 3/6. freq3[0]++ -> [2,1,0].
j=2: s[2]=9, pref3=0. s[2] not 3/6. freq3[0]++ -> [3,1,0].
j=3: s[3]=3, pref3=0. s[3] is 3, so add freq3[0] = 3. ans_d3 += 3. Then freq3[0]++ -> [4,1,0].
j=4: s[4]=6, pref3 = (0+6)%3=0. s[4] is 6, so add freq3[0] = 4. ans_d6 += 4. Then freq3[0]++ -> [5,1,0].
So the substrings counted for d=6 are those with i such that pref3[i]=0 at the time of j=4. Which i have pref3[i]=0? i=0:0, i=1:1, i=2:0, i=3:0, i=4:0? Wait, pref3[i] is the value before adding s[i]? Actually, pref3 is updated after each j. So pref3 at the end of iteration j is the sum of first j+1 digits. So pref3[0] is 0 (before any digits). pref3[1] is 1. pref3[2] is 0. pref3[3] is 0. pref3[4] is 0. pref3[5] is 0 (after j=4). But in the query for j=4, we use pref3 (which is the sum of first 5 digits, i.e., pref3[5]=0). And we look at freq3[0]. freq3[0] contains the counts of pref3 values that have been seen and added to freq. We add to freq after each j. So before processing j=4, freq3[0] includes the counts for i=0 (initial), and after j=1, j=2, j=3. So i=0,1,2,3. Their pref3 values: i=0:0, i=1:1, i=2:0, i=3:0. So freq3[0] = 1 (i=0) + 1 (i=2) + 1 (i=3) = 3? Wait, we also had i=1? No, i=1 has pref3=1. So freq3[0] should be 1 (initial) + 1 (after j=1? Actually, after j=1, pref3=0, so we increment freq3[0] from 1 to 2. After j=2, pref3=0, so increment to 3. After j=3, we add freq3[0] (which is 3) to ans, then increment to 4. So before j=4, freq3[0]=4. That means we have counted i=0,2,3, and also i=4? No, i=4 has not been processed yet. So the 4 comes from i=0,2,3, and the initial? Actually, initial freq3[0]=1 (i=0). After j=1: freq3[0]=2 (i=0 and i=1? No, i=1 has pref3=1, so it didn't increment freq3[0]. Wait, after j=1, we updated pref3 to 0, and then we do freq3[0]++. So that corresponds to i=1? No, the update freq3[0]++ is after processing j=1, so it corresponds to the prefix value at i=2? Let's be systematic.

We have a loop: for j in range(n):
   pref3 = (pref3 + int(s[j])) % 3
   if s[j] in ['3','6']:
       ans += freq3[pref3]
   freq3[pref3] += 1

So for each j, we first update pref3 to be the value including s[j]. This pref3 corresponds to the prefix ending at j, i.e., pref3[j+1]. Then we query freq3[pref3]. The freq3 array currently contains counts of pref3 values for all previous i from 0 to j-1? Actually, at the start, before the loop, we should initialize freq3 with the value for i=0: pref3=0, so freq3[0]=1. Then for j=0: we update pref3 to include s[0], so now pref3 is the value for i=1 (prefix of length 1). Then we query freq3[pref3]. The freq3 contains the value for i=0. So it checks if the prefix of length 0 and prefix of length 1 have the same value mod 3. That corresponds to the substring s[0..0] (length 1). That's correct: we want to count i=0 for j=0. Then we increment freq3[pref3] to include the new prefix (i=1). So for the next j=1, freq3 contains prefixes for i=0 and i=1. So the query for j=1 will use pref3 (prefix of length 2) and freq3 contains prefixes for i=0 and i=1. So it counts i such that prefix i matches prefix j+1. That's exactly what we want: for each j, we want to count i in [0, j] such that pref3[i] = pref3[j+1]. So the loop is correct.

Now, back to example 1. For j=4, s[4]='6'. We update pref3 from previous value (after j=3, pref3=0) to (0+6)%3=0. So pref3=0. Then we query freq3[0]. At this point, freq3 has been updated for j=0,1,2,3. Let's list the updates:
- Initially: freq3[0]=1 (i=0).
- j=0: s[0]=1, pref3 becomes 1. s[0] not 3/6. freq3[1] becomes 1.
- j=1: s[1]=2, pref3 becomes (1+2)%3=0. s[1] not 3/6. freq3[0] becomes 2.
- j=2: s[2]=9, pref3 becomes (0+9)%3=0. s[2] not 3/6. freq3[0] becomes 3.
- j=3: s[3]=3, pref3 becomes (0+3)%3=0. s[3] is 3, so ans += freq3[0] = 3. Then freq3[0] becomes 4.
- j=4: s[4]=6, pref3 becomes (0+6)%3=0. s[4] is 6, so ans += freq3[0] = 4. Then freq3[0] becomes 5.
So for j=4, we add 4. The substrings counted are those with i such that pref3[i] = pref3[5] = 0. Which i? i=0: pref3[0]=0, i=1: pref3[1]=1, i=2: pref3[2]=0, i=3: pref3[3]=0, i=4: pref3[4]=0. So i=0,2,3,4. That's 4 substrings: s[0..4]="12936", s[2..4]="936", s[3..4]="36", s[4..4]="6". Check divisibility by 6:
- "12936": 12936/6=2156, yes.
- "936": 936/6=156, yes.
- "36": 36/6=6, yes.
- "6": 6/6=1, yes.
So all 4 are valid. So our method gives 4 for d=6.

Now, what about d=4,5,7,8,9? In this example, there are no 4,5,7,8,9. So total ans = 1 (d=1) + 1 (d=2) + 3 (d=3) + 4 (d=6) = 9? But the expected answer is 11. So we missed something. Let's check the substrings that are valid in example 1. The invalid ones are "29", "129", "293", "2936". So the valid ones are all others: total 15 - 4 = 11. Let's list all substrings and check:
Indices:
0:1
1:2
2:9
3:3
4:6
Substrings:
i=0: "1" (1/1=1), "12" (12/2=6), "129" (129/9=14.333 no), "1293" (1293/3=431), "12936" (12936/6=2156). So valid: "1", "12", "1293", "12936". (4)
i=1: "2" (2/2=1), "29" (29/9=3.22 no), "293" (293/3=97.66 no), "2936" (2936/6=489.33 no). So valid: "2". (1)
i=2: "9" (9/9=1), "93" (93/3=31), "936" (936/6=156). So valid: "9", "93", "936". (3)
i=3: "3" (3/3=1), "36" (36/6=6). So valid: "3", "36". (2)
i=4: "6" (6/6=1). So valid: "6". (1)
Total valid: 4+1+3+2+1 = 11.
Now, let's see what our method counts:
d=1: s[0]='1' -> j+1=1. So adds 1. (covers "1")
d=2: s[1]='2' -> j+1=2? Wait, j=1, so j+1=2. But we only have one substring ending with 2 starting at i=0 or i=1? Actually, substrings ending with 2: i=0,j=1 ("12") and i=1,j=1 ("2"). That's 2. So ans +=2. (covers "12" and "2")
d=3: s[3]='3' -> we added 3. Those are: i=0,j=3 ("1293"), i=2,j=3 ("93"), i=3,j=3 ("3"). That's 3. (covers "1293", "93", "3")
d=6: s[4]='6' -> we added 4. Those are: i=0,j=4 ("12936"), i=2,j=4 ("936"), i=3,j=4 ("36"), i=4,j=4 ("6"). That's 4. (covers "12936", "936", "36", "6")
d=9: s[2]='9' -> we need to count substrings ending with 9. s[2]='9' at j=2. Substrings ending with 9: i=0,j=2 ("129"), i=1,j=2 ("29"), i=2,j=2 ("9"). But "129" and "29" are not divisible by 9. Only "9" is. So we should count 1. Our method for d=9: use prefix sums mod 9. Let's compute:
pref9 start 0.
j=0: s[0]=1, pref9=1. s[0]!='9'. freq9[1]++.
j=1: s[1]=2, pref9=(1+2)%9=3. s[1]!='9'. freq9[3]++.
j=2: s[2]=9, pref9=(3+9)%9=3. s[2]=='9', so add freq9[3]. freq9[3] is currently 1 (from j=1). So add 1. Then freq9[3]++.
So we get 1. That's correct. So we need to include d=9.
d=4,5,7,8: none.
So total ans = 1 (d=1) + 2 (d=2) + 3 (d=3) + 4 (d=6) + 1 (d=9) = 11. Perfect.

So our method works for example 1.

Now, let's test example 2: s = "5701283"
Expected ans = 18.
We need to compute each d.
d=1: s[3]='1' at j=3? Actually, s="5 7 0 1 2 8 3". Indices: 0:5, 1:7, 2:0, 3:1, 4:2, 5:8, 6:3.
d=1: s[3]='1', j=3, j+1=4. So ans +=4.
d=2: s[4]='2', j=4, j+1=5. So ans +=5.
d=3: s[6]='3', j=6, j+1=7. So ans +=7? But wait, not all substrings ending with 3 are divisible by 3. So our method for d=3 uses prefix sums mod 3. Let's compute:
pref3 start 0.
j=0: s[0]=5, pref3=5%3=2. s[0]!='3'. freq3[2]++.
j=1: s[1]=7, pref3=(2+7)%3=0. s[1]!='3'. freq3[0]++.
j=2: s[2]=0, pref3=(0+0)%3=0. s[2]!='3'. freq3[0]++.
j=3: s[3]=1, pref3=(0+1)%3=1. s[3]!='3'. freq3[1]++.
j=4: s[4]=2, pref3=(1+2)%3=0. s[4]!='3'. freq3[0]++.
j=5: s[5]=8, pref3=(0+8)%3=2. s[5]!='3'. freq3[2]++.
j=6: s[6]=3, pref3=(2+3)%3=2. s[6]=='3', so add freq3[2]. freq3[2] currently: after j=0:1, after j=5:2? Let's track freq3:
Initial: freq3[0]=1.
j=0: pref3=2, freq3[2]=1.
j=1: pref3=0, freq3[0]=2.
j=2: pref3=0, freq3[0]=3.
j=3: pref3=1, freq3[1]=1.
j=4: pref3=0, freq3[0]=4.
j=5: pref3=2, freq3[2]=2.
j=6: pref3=2, add freq3[2]=2. Then freq3[2]=3.
So for d=3, we add 2. That means substrings ending with 3 that are divisible by 3: there are 2. Which ones? Let's find all substrings ending with 3: i=6,j=6 ("3"), i=5,j=6 ("83"), i=4,j=6 ("283"), i=3,j=6 ("1283"), i=2,j=6 ("01283"), i=1,j=6 ("701283"), i=0,j=6 ("5701283"). We need those divisible by 3. The sum of digits mod 3: "3":3%3=0, "83":8+3=11%3=2, "283":2+8+3=13%3=1, "1283":1+2+8+3=14%3=2, "01283": same 14%3=2, "701283":7+0+1+2+8+3=21%3=0, "5701283":5+7+0+1+2+8+3=26%3=2. So only "3" and "701283" are divisible by 3. That's 2. So our method gives 2.
d=4: no '4' in string.
d=5: s[0]='5', j=0, j+1=1. So ans +=1. But wait, is that correct? Substrings ending with 5: only "5". And 5%5=0, so valid. So 1.
d=6: no '6' in string.
d=7: s[1]='7', j=1. We need to count substrings ending with 7. We use the 2D array method. Let's compute manually: substrings ending with 7: i=1,j=1 ("7"), i=0,j=1 ("57"). We need to check divisibility by 7: 7%7=0, 57%7=1? 7*8=56, so 57%7=1. So only "7" is valid. So count=1. Our method should give 1.
d=8: s[5]='8', j=5. Substrings ending with 8: i=5,j=5 ("8"), i=4,j=5 ("28"), i=3,j=5 ("128"), i=2,j=5 ("0128"), i=1,j=5 ("70128"), i=0,j=5 ("570128"). Check divisibility by 8: 8%8=0, 28%8=4, 128%8=0, 0128=128%8=0, 70128%8: 128/8=16, so 70128%8=0? 70000/8=8750, 128/8=16, so yes 0. 570128%8: 128%8=0, so yes. So valid: "8", "128", "0128", "70128", "570128". That's 5. But our method for d=8: for j=5, we compute:
Length 1: always valid -> +1.
Length 2: two = s[4]*10+8 = 2*10+8=28. 28%8=4, not valid.
Length 3: three = s[3]*100 + s[4]*10 + 8 = 1*100+2*10+8=128. 128%8=0, valid. Then we add j-1 = 4? Wait, j=5, j-1=4. That would add 4. But we also have length 1 already added. So total from length >=3: 4 (i<=2) plus length 3? Actually, our formula: if three%8==0, add j-1. That includes length 3 and all longer. So we add 4. Then we also added length 1 (1) and length 2 (0). So total = 1 + 0 + 4 = 5. But wait, the substrings of length >=3 that are valid: i=0,1,2,3? Actually, i=3 is length 3 ("128"), i=2 is length 4 ("0128"), i=1 is length 5 ("70128"), i=0 is length 6 ("570128"). That's 4 substrings. Plus length 1 ("8") gives 5. So our method gives 5. Correct.
d=9: no '9' in string.
Now sum: d=1:4, d=2:5, d=3:2, d=5:1, d=7:1, d=8:5. Total = 4+5+2+1+1+5 = 18. Correct.

Example 3: s = "1010101010"
Expected ans = 25.
Only substrings ending with '1' are divisible. There are 25 such substrings. Our d=1 method: for each j with s[j]='1', add j+1. Let's list j positions: s="1 0 1 0 1 0 1 0 1 0". j=0,2,4,6,8. j+1: 1,3,5,7,9. Sum = 1+3+5+7+9 = 25. Correct. Other d's: d=2,3,4,5,6,7,8,9: none, because no such digits. So total 25.

So the methods work for the examples.

Now, we need to implement all these methods in the `countSubstrings` function. The overall complexity: O(n) for d=1,2,3,5,6,9 (using prefix sums and simple counts), O(n) for d=4 and d=8 (constant per j), and O(6n) for d=7. So total O(n). Space: O(n) for the frequency arrays (size at most 9 or 7*6=42). So it's efficient.

Let's write the solution step by step.

Algorithm:
Input: s (string of digits), n = len(s).
Initialize ans = 0.

1. Process d=1: 
   For each j where s[j]=='1', ans += j+1.
2. Process d=2:
   For each j where s[j]=='2', ans += j+1.
3. Process d=5:
   For each j where s[j]=='5', ans += j+1.
4. Process d=3 and d=6 together using prefix sums mod 3:
   pref3 = 0, freq3 = [0,0,0], freq3[0]=1.
   For j from 0 to n-1:
       pref3 = (pref3 + int(s[j])) % 3
       if s[j] == '3' or s[j] == '6':
           ans += freq3[pref3]
       freq3[pref3] += 1
5. Process d=9:
   pref9 = 0, freq9 = [0]*9, freq9[0]=1.
   For j from 0 to n-1:
       pref9 = (pref9 + int(s[j])) % 9
       if s[j] == '9':
           ans += freq9[pref9]
       freq9[pref9] += 1
6. Process d=4:
   For each j where s[j]=='4':
       ans += 1  # length 1
       if j >= 1:
           two = int(s[j-1])*10 + 4
           if two % 4 == 0:
               ans += 1
       if j >= 2:
           two = int(s[j-1])*10 + 4  # last two digits
           if two % 4 == 0:
               ans += (j-1)  # all substrings starting at i <= j-2
7. Process d=8:
   For each j where s[j]=='8':
       ans += 1  # length 1
       if j >= 1:
           two = int(s[j-1])*10 + 8
           if two % 8 == 0:
               ans += 1
       if j >= 2:
           three = int(s[j-2])*100 + int(s[j-1])*10 + 8
           if three % 8 == 0:
               ans += (j-1)  # length 3 and all longer (i <= j-2)
8. Process d=7:
   Use the 2D array method.
   Precompute pow10_mod7 = [1, 3, 2, 6, 4, 5] for k=0..5.
   Precompute inv_pow10_mod7: since 7 is prime, we can compute inverse of each.
   inv_pow10_mod7 = [1, 5, 4, 6, 2, 3] (since 1*1=1, 3*5=15≡1, 2*4=8≡1, 6*6=36≡1, 4*2=8≡1, 5*3=15≡1). Check: 3*5=15 mod 7=1, 2*4=8 mod 7=1, 6*6=36 mod 7=1, 4*2=8 mod 7=1, 5*3=15 mod 7=1. So yes.
   Initialize cnt = [[0]*7 for _ in range(6)].
   pref7 = 0.  # This is the value of the prefix modulo 7.
   For j from 0 to n-1:
       # Add current i=j to cnt? Actually, we need to add i=j for the next j. But for the query, we need i up to j. So we should first add the current pref7 (which corresponds to i=j) to cnt? But careful: for j=0, we want to include i=0. So we should add i=0 before querying for j=0. So we can do:
       # Actually, we can process as: at the start, we have pref7 = 0 (for i=0). We add cnt[0][0] = 1.
       # Then for each j, we first query? But we need to include i=j. So we should add i=j to cnt before querying for that j. So we can do:
       # For j=0: add i=0: cnt[0 % 6][pref7] += 1. But pref7 is still 0. So cnt[0][0] = 1.
       # Then compute pref7_next = (pref7 * 10 + int(s[0])) % 7.
       # Then if s[0]=='7', query using pref7_next and cnt.
       # Then set pref7 = pref7_next.
       # For j=1: now pref7 is the value of the first digit. We add i=1: cnt[1 % 6][pref7] += 1.
       # Then compute pref7_next, query, etc.
   So the code:
   ```
   cnt = [[0]*7 for _ in range(6)]
   pref7 = 0
   # Add i=0
   cnt[0 % 6][pref7] = 1
   for j in range(n):
       # Add i=j? Actually, for j=0, i=0 is already added. For j=1, we need to add i=1. So we should add i=j at the beginning of the loop? But for j=0, i=0 is already there. So we can do:
       # For j=0, we don't add again. For j>=1, we add i=j. So we can check if j>0: add i=j. But it's easier to just add at the end? Let's think.
       # We want for each j, the cnt to contain all i in [0, j]. So at the start of iteration j, cnt should contain i=0,...,j-1. For j=0, that means only i=0. So we pre-add i=0.
       # Then for j>=1, we need to add i=j. So we can do: at the beginning of the loop, if j>0, we add i=j using the current pref7 (which is the prefix value up to j). But pref7 is updated from the previous iteration. So for j=1, pref7 is the value of the first digit (i=1). So we can add cnt[j % 6][pref7] += 1.
       # But careful: the order should be: first add the new i, then compute pref7_next, then query. Because the query should use the updated pref7_next and the cnt that includes all i up to j.
       # So:
       if j > 0:
           cnt[j % 6][pref7] += 1
       pref7_next = (pref7 * 10 + int(s[j])) % 7
       if s[j] == '7':
           for i0 in range(6):
               k = (j+1 - i0) % 6
               r = (pref7_next * inv_pow10_mod7[k]) % 7
               ans += cnt[i0][r]
       pref7 = pref7_next
   ```
   Let's test with s="7": n=1.
   Initialize cnt all zeros, pref7=0.
   Pre-add i=0: cnt[0][0] = 1.
   j=0: j>0? No, so skip the add. Compute pref7_next = (0*10+7)%7=0. s[0]=='7', so query:
       for i0 in range(6):
           k = (0+1 - i0) % 6 = (1 - i0) % 6.
           i0=0: k=1, r = (0 * inv[1]) %7 = 0. cnt[0][0]=1. ans+=1.
           i0=1: k=0, r = 0*inv[0]=0. cnt[1][0]=0.
           i0=2: k=5, r=0. cnt[2][0]=0.
           i0=3: k=4, r=0. cnt[3][0]=0.
           i0=4: k=3, r=0. cnt[4][0]=0.
           i0=5: k=2, r=0. cnt[5][0]=0.
       So ans becomes 1. Then pref7=0.
   So we get 1. That's correct: "7" is divisible by 7.
   Test with s="57": n=2.
   Pre-add i=0: cnt[0][0]=1.
   j=0: j>0? No. pref7_next = (0*10+5)%7=5. s[0]='5', not '7'. pref7=5.
   j=1: j>0, so add i=1: cnt[1 % 6][pref7] = cnt[1][5] += 1. Now cnt[1][5]=1.
   pref7_next = (5*10+7)%7 = (50+7)%7=57%7=1 (since 56 is multiple). s[1]='7', so query:
       i0=0: k = (1+1 - 0)%6 = 2%6=2. r = 1 * inv[2] = 1*4=4. cnt[0][4]=0.
       i0=1: k = (2 - 1)%6 = 1. r = 1 * inv[1] = 1*5=5. cnt[1][5]=1. ans+=1.
       i0=2: k = (2-2)%6=0. r=1*inv[0]=1. cnt[2][1]=0.
       i0=3: k = (2-3)%6=5. r=1*inv[5]=1*3=3. cnt[3][3]=0.
       i0=4: k = (2-4)%6=4. r=1*inv[4]=1*2=2. cnt[4][2]=0.
       i0=5: k = (2-5)%6=3. r=1*inv[3]=1*6=6. cnt[5][6]=0.
   So ans +=1. Then pref7=1.
   Total ans=1. That means we counted one substring ending with 7 that is divisible by 7. Which one? i=1,j=1: "7" (value 7%7=0). i=0,j=1: "57" (57%7=1). So only "7" is valid. So ans=1 is correct.
   So the method works.

We need to be careful with the index for k. In the query, we used `k = (j+1 - i0) % 6`. This is because `len = j - i + 1`, and `i = i0 + 6*m`. So `len mod 6 = (j - i0 - 6*m + 1) mod 6 = (j+1 - i0) mod 6`. So yes.

Now, we also need to consider that for d=7, the substring can be of any length. The method handles all lengths because we consider all i from 0 to j. The only potential issue is if the number becomes very large, but we are working modulo 7, so it's fine.

Now, let's double-check d=4 and d=8 methods.

For d=4:
We argued: for length >=3, value mod 4 = (s[j-1]*10 + s[j]) % 4. So if that two-digit number is divisible by 4, then all substrings of length >=3 are valid. So for a given j with s[j]='4':
- Always add 1 for length 1.
- If j>=1, check two-digit number. If valid, add 1 for length 2.
- If j>=2, check the two-digit number again (same as length 2). If valid, add (j-1) for all substrings starting at i <= j-2 (which have length >=3). Note: we don't need to check the three-digit number because for length >=3, the value mod 4 is determined by the last two digits. So if the last two digits are divisible by 4, then all longer substrings are valid. So we add (j-1) for i from 0 to j-2. But wait, is it always true that for any i <= j-2, the value mod 4 is exactly the two-digit number? Let's test with an example: s = "104". j=2, s[2]='4'. s[0]='1', s[1]='0', s[2]='4'. The two-digit number is "04" = 4. 4%4=0. So for i=0, substring "104" = 104. 104%4=0. Yes. For i=1, substring "04" = 4. 4%4=0. So both are valid. So adding (j-1) for j=2 gives 1, which is for i=0. And we also add length 2? But we already added length 2 separately. Wait, our addition: ans += 1 (length 1). If j>=1, check two-digit: for j=2, s[1]='0', s[2]='4', two=4, divisible, so add 1 for length 2. Then if j>=2, we check two-digit again and add (j-1)=1 for i <= j-2 (i=0). So total added: 1+1+1=3. But the actual valid substrings ending at j=2: "4" (length 1), "04" (length 2), "104" (length 3). That's 3. So correct.
What if the two-digit number is not divisible by 4? Example: s = "124". j=2, s[2]='4'. s[1]='2', s[2]='4', two=24%4=0. Actually 24 is divisible by 4. So it's valid. What about s = "134": two=34%4=2, not divisible. Then we add 1 for length 1, and length 2 is not valid. For i<=j-2, we add 0. So total 1. But is that correct? Substrings: "4" (valid), "34" (34%4=2 no), "134" (134%4=2 no). So only 1. Correct.
What about length 3 exactly? If j=2, i=1 is length 2, not 3. So for length 3, we need j>=3. So if j=3, s[3]='4', s[2]='3', s[1]='1', s[0]='1'. Then two-digit is "34"=34%4=2, not divisible. So for i<=1 (j-2=1), we add 0. But what about i=2,j=3: substring "34" is length 2, already checked. i=1,j=3: "134", length 3. Its value mod 4 is determined by "34" mod 4 = 2, so not valid. So correct.
So the method works.

For d=8:
Similarly, for length >=4, value mod 8 = (s[j-2]*100 + s[j-1]*10 + s[j]) % 8. So if that three-digit number is divisible by 8, then all substrings of length >=4 are valid. So for a given j with s[j]='8':
- Always add 1 for length 1.
- If j>=1, check two-digit number. If valid, add 1 for length 2.
- If j>=2, check three-digit number. If valid, add 1 for length 3.
- Also, if j>=3, we need to add for all substrings of length >=4. But wait, our condition for length >=4 is that the three-digit number is divisible by 8. So if it is divisible, then for all i <= j-3, the substring is valid. The number of such i is j-2 (i from 0 to j-3). So we can add (j-2) if three-digit is divisible. But careful: we already added for length 3 (i=j-2). So total for length >=3 is (j-2) + 1 = j-1. So we can do: if three%8==0, add (j-1) (which covers i <= j-2). Then we also have length 2 and 1. So the code: ans += 1; if j>=1 and two%8==0: ans+=1; if j>=2 and three%8==0: ans += (j-1). But wait, if j=2, j-1=1, that adds 1 for i<=0, which is length 3? Actually, for j=2, length 3 means i=0, j=2. So that's correct. For j=2, three-digit is the whole string of length 3. So we add 1 for length 3, and that's it. For j>2, j-1 includes length 3 and longer. So it's correct.
But we must be careful: if j<2, we can't compute three. So the condition j>=2.
Let's test with s = "5701283" at j=5 (s[5]='8'). j=5.
ans +=1 (length 1).
j>=1: two = s[4]*10+8 = 2*10+8=28. 28%8=4, so no add.
j>=2: three = s[3]*100 + s[4]*10 + 8 = 1*100+2*10+8=128. 128%8=0, so add j-1=4. So total added: 1+4=5. That's what we had earlier.
Test with j=2 (if s had an 8 at index 2). Suppose s="128", j=2. 
ans +=1.
j>=1: two = s[1]*10+8 = 2*10+8=28, 28%8=4, no.
j>=2: three = s[0]*100 + s[1]*10 + 8 = 1*100+2*10+8=128, divisible, add j-1=1. So total 2. Substrings: "8" (valid), "28" (28%8=4 no), "128" (128%8=0 valid). So valid: "8" and "128" = 2. Correct.
So the method works.

Now, we need to combine all these into one function.

One more thing: For d=3 and d=6, we used the same prefix sum mod 3. But we must ensure that the frequency array is updated correctly. In the loop, we update freq3 after the query. So for j=0, we first update pref3, then if s[0] is 3 or 6, we add freq3[pref3], then increment freq3. But note: at the very start, we need to have freq3 include the prefix value for i=0 (which is 0). So we initialize freq3[0]=1. Then for j=0, after updating pref3, freq3[0] is still 1, so if s[0] is 3, we add 1 (for i=0). That's correct. Then we increment freq3. So it's fine.

Similarly for d=9.

For d=7, we already handled the initialization.

Now, let's write the code.

We'll implement the `Solution` class with the `countSubstrings` method.

We need to be careful with integer conversions. Since s consists of digits, we can use int(s[j]) or ord(s[j])-48.

Complexity: O(n) time, O(1) extra space (since frequency arrays are of fixed size, and the 2D array is 6x7=42). So it's efficient.

Let's code accordingly.</mm:think>### PLAN
We need to count substrings `s[i..j]` where the integer value is divisible by its non-zero last digit `d = s[j]`. Since `d ∈ {1,…,9}`, we handle each digit separately. For `d=1,2,5`, all substrings ending with `d` are valid (O(n) by summing `j+1`). For `d=3,6,9`, we use digit-sum prefix sums modulo `d` (O(n) with a frequency array). For `d=4,8`, only the last two/three digits determine divisibility for long substrings (O(1) per ending position). For `d=7`, we use a 2D frequency array indexed by `i mod 6` and prefix value mod 7, exploiting `10^6 ≡ 1 (mod 7)` to keep the per-position cost constant. Overall O(n) time and O(1) extra space.