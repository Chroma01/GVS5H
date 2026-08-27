
## ideation
The core difficulty is that the range can be as large as ~10^9 numbers, so a naive O(r-l) scan with string conversions per number will be too slow in Python. We need a way to count numbers whose digit product is divisible by digit sum faster than iterating every integer, or at least iterate with a very cheap per-number cost.

Observations:
- Digit product and digit sum are relatively small (max sum 9*10=90, max product 9^10 ≈ 3.5e9, but fits in 64-bit).
- For a number with no zero digit, product ≤ 9^k (k = number of digits). Sum ≥ 1.
- The condition product % sum == 0 is the check.
- A number is beautiful iff (digit_product % digit_sum == 0). If a digit is 0, product is 0, and sum>0, so 0 % sum == 0 always, so any number containing a zero is beautiful. This includes numbers like 10, 20, 101, etc.
- Only numbers with all non-zero digits need actual divisibility checking.

Candidate approaches:
1. Direct iterate from l to r with a fast digit extraction loop (no strings). Precompute sums/products incrementally as we increment? Hard because carries.
2. Precompute beautiful numbers up to 10^9 using DP/digit DP that also tracks the GCD or remainder condition. But the condition is product % sum == 0, which is a divisibility relation between two computed values, not a simple modular state. Digit DP state would need to know (sum, product) or (sum, product mod sum). Since sum ≤ 90 and product ≤ 9^10, a DP on (sum, product) is infeasible.
3. Use the fact that any number containing a 0 is beautiful. So we can count numbers with at least one zero in [l, r] via combinatorics, and only iterate over numbers with no zero digits. The count of numbers with no zero digit up to N is manageable (9 * 9^9 ≈ 3.4e8 worst case, still too many).
4. Further restrict: if the number has no zero digit and all digits are 1, then product=1, sum=number of digits. Need 1 % sum == 0, so sum must be 1, i.e., only the number 1. For numbers with digits ≥ 2, product grows much faster than sum, so many are divisible.
5. Brute force with low-level optimization: iterate from l to r, use while-loop digit extract, early exit on zero digit (count immediately). This is the simplest and often passes in Python if test constraints are reasonable (e.g., r-l ≤ 10^7). But the problem allows r up to 10^9 with l=1, so r-l could be 10^9-1. That's too much for Python (would take ~100 seconds at ~10 ns per op, more realistically 1-2 µs per number → 1000+ seconds).

We need a smarter counting method. Let's think about the structure more carefully.

Key insight: A number is NOT beautiful only if it has no zero digit AND digit_product is NOT divisible by digit_sum. Since zero digits make it beautiful, we can count non-beautiful numbers (those with no zero digit and product not divisible by sum) and subtract from total.

Counting numbers with no zero digit in [l, r] is a standard digit DP: count of numbers with digits in {1..9} in a range. That's doable. But we also need to know for which of those product % sum != 0. The DP state would need to track (sum, product_mod_sum) but sum varies, so product_mod_sum depends on sum, making it hard.

Alternative insight: For numbers with no zero digit, can we bound the number of such numbers in [1, 10^9]? There are 9 * 9^9 ≈ 3.4e8 such numbers. Still too many to enumerate.

But wait: the constraint is r < 10^9, and l >= 1. The worst case is l=1, r=10^9-1. We need an algorithm that works for this. The straightforward iteration is O(10^9), which in Python is ~30 seconds at best with C-level loops, but Python per-number overhead is high.

We need a mathematical counting approach. Let's examine the condition more carefully.

Let the digits be d_1, ..., d_k (all in 1..9 since no zero). Let S = sum d_i, P = product d_i. We need S | P.

For k=1 (1..9): S = P = d, so always divides. All 9 are beautiful.
For k=2 (11..99, no zero): S = d1+d2, P = d1*d2. Condition: (d1+d2) | (d1*d2). We can count these.
For k≥3: many will satisfy, but we need exact count.

Actually, for any number with all digits 1, S=k, P=1. Only beautiful if k=1. So 11 is NOT beautiful (sum=2, product=1, 1%2=1). 111 sum=3 product=1, 1%3=1, not beautiful. So numbers like 11, 111, etc. are NOT beautiful.

For numbers with digits all 1 except possibly one digit ≥ 2, product = that digit, sum = k-1 + d. Need (k-1+d) | d. Since d < k-1+d, this requires k-1+d ≤ d, impossible unless d=0 (excluded) or k-1+d = d → k=1. So for k≥2, a number with exactly one digit ≥2 and rest 1s is never beautiful.

Interesting. So 12: sum=3, product=2, 2%3≠0. Not beautiful. 21: sum=3, product=2, not beautiful.

What about numbers with two digits ≥2? e.g., 22: sum=4, product=4, beautiful. 23: sum=5, product=6, 6%5=1, not. 24: sum=6, product=8, 8%6=2, not. 25: sum=7, product=10, 10%7=3, not. 26: sum=8, product=12, 12%8=4, not. 27: sum=9, product=14, 14%9=5, not. 28: sum=10, product=16, 16%10=6, not. 29: sum=11, product=18, 18%11=7, not. 33: sum=6, product=9, 9%6=3, not. 34: sum=7, product=12, 12%7=5, not. 35: sum=8, product=15, 15%8=7, not. 36: sum=9, product=18, 18%9=0, beautiful! 44: sum=8, product=16, 16%8=0, beautiful! 45: sum=9, product=20, 20%9=2, not. 46: sum=10, product=24, 24%10=4, not. 48: sum=12, product=32, 32%12=8, not. 49: sum=13, product=36, 36%13=10, not. 55: sum=10, product=25, 25%10=5, not. 56: sum=11, product=30, 30%11=8, not. 57: sum=12, product=35, 35%12=11, not. 58: sum=13, product=40, 40%13=1, not. 59: sum=14, product=45, 45%14=3, not. 66: sum=12, product=36, 36%12=0, beautiful! 67: sum=13, product=42, 42%13=3, not. 68: sum=14, product=48, 48%14=6, not. 69: sum=15, product=54, 54%15=9, not. 77: sum=14, product=49, 49%14=7, not. 78: sum=15, product=56, 56%15=11, not. 79: sum=16, product=63, 63%16=15, not. 88: sum=16, product=64, 64%16=0, beautiful! 89: sum=17, product=72, 72%17=4, not. 99: sum=18, product=81, 81%18=9, not.

So for 2-digit numbers with no zero, beautiful ones include: 11? No. 12? No. ... from above: 22, 36, 44, 66, 88. Also 24? No. What about 28? No. 32? sum=5, prod=6, no. 42? sum=6, prod=8, no. 48? sum=12, prod=32, no. 64? sum=10, prod=24, no. 72? sum=9, prod=14, no. 84? sum=12, prod=32, no. 96? sum=15, prod=54, 54%15=9, no.

Also check 2-digit with repeated digit d: sum=2d, product=d^2. d^2 % 2d = d^2 - d*floor(d/2)*2. If d is even, d=2k, d^2=4k^2, 2d=4k, 4k^2 % 4k = 0. So any even repeated digit is beautiful: 22, 44, 66, 88. If d is odd, d^2 % 2d = d^2 - d*(d-1) = d, so remainder d ≠ 0. So odd repeated digits not beautiful: 11, 33, 55, 77, 99. Confirmed.

Now, the number of beautiful numbers seems sparse among no-zero numbers, but we still need to count them. Given the complexity of the divisibility condition, a digit DP that tracks the actual product and sum might be needed, but product can be up to 9^10 ≈ 3.5e9, which is too large for DP state. However, we can track product modulo all possible sums? That's circular.

Alternative: Since any number with a zero digit is beautiful, and the density of numbers with at least one zero digit is 1 - (9/10)^k for k-digit numbers. For large k, this is high. For 9-digit numbers, 1 - 0.9^9 ≈ 0.61. So most numbers are beautiful just because they have a zero. Only the no-zero numbers are problematic, and there are 9^9 ≈ 3.8e8 of them in 9 digits. That's still too many to enumerate.

But wait: 9^9 is the count of 9-digit numbers with no zero (since first digit is 1-9, rest 1-9). Actually, 9-digit numbers: first digit 1-9 (9 choices), remaining 8 digits 1-9 (9^8 choices), total 9^9 = 387,420,489. For all numbers 1 to 10^9-1, total no-zero count is sum_{k=1}^{9} 9^k = (9^10 - 9)/8 ≈ 3.4e8. Still ~340 million, too many for Python iteration.

But maybe we can iterate faster? In C++ this is feasible (340M iterations with simple arithmetic is ~1 second). In Python, 340M iterations is ~100 seconds. Too slow.

We need a counting method that avoids iterating over no-zero numbers. Since the density of beautiful numbers among no-zero numbers is not 100%, we need to count them.

Let's think about the condition for no-zero numbers. For a k-digit number with digits d_1,...,d_k ∈ {1..9}, we need (sum d_i) | (prod d_i).

For k=1: all 9 are beautiful. Count = 9.
For k=2: we enumerated. Let's count systematically. We can write a program to count beautiful 2-digit numbers, but we need up to k=9.

For k=3: digits a,b,c ∈ 1..9. Need (a+b+c) | abc.
This is a constrained problem. The number of such triples is limited? Let's estimate: for each (a,b,c), check. 9^3 = 729. Easy to enumerate. We can precompute all beautiful numbers up to length 9? 9^9 is too many, but maybe we can enumerate all tuples (d_1,...,d_k) with product P and sum S where S|P, and then count how many numbers have that digit multiset. For each valid (S, P) with S|P, the number of digit tuples with that sum and product is finite.

Actually, the number of tuples (d_1,...,d_k) with digits in 1..9 and a given (sum, product) is the coefficient in a generating function. But we can observe that product grows fast. For a fixed sum S, the product P is bounded by 9^S? No, product can be large even for small sum if digits are 9s. But for sum S, the product is maximized when digits are 9, giving 9^S? Wait, if sum is S and we have k digits each ≤9, the max product for given sum S is when we use as many 9s as possible and one remainder digit. But product can be huge: for S=9, one digit 9, product=9. For S=10, digits 9 and 1, product=9. For S=18, two 9s, product=81. For S=27, three 9s, product=729. In general, product ≤ 9^{S/9} roughly. For S up to 9*9=81, product can be up to 9^9 ≈ 4e8. Still too many to enumerate pairs (S,P).

But we need to count numbers, i.e., ordered tuples of digits (with leading digit non-zero, but no zero allowed at all). For each length k, the number of valid digit tuples is 9^k. The number of pairs (sum, product) for length k is at most 9k × 9^k, but many tuples share the same (sum, product). Actually, we can group by (sum, product). For each length k, the number of distinct (sum, product) pairs is at most (9k) × 9^k? No, sum is at most 9k, product varies. But the number of achievable products for a given sum and length is limited. However, the total number of distinct (sum, product) pairs across all lengths is still large.

Alternative approach: Use inclusion-exclusion or Möbius inversion? The condition is S | P. We can write indicator as sum_{d|gcd(S,P)} μ(d)? No, S|P is not a gcd condition.

Wait, S|P is equivalent to P ≡ 0 (mod S). We can write it as sum_{d|S} [P ≡ 0 (mod d)] * something? Actually, by Möbius inversion, for any integer P, the number of divisors d of S that divide P is sum_{d|gcd(S,P)} φ(d)? Not helpful.

Another idea: For each number, compute S and P. We want to count n with S|P. We can iterate over S (the sum) and for each S, count numbers with digit sum S and product divisible by S. For fixed S, the product P must be a multiple of S. The number of k-digit numbers (no zero) with sum S is the coefficient of x^S in (x + x^2 + ... + x^9)^k. The product is harder.

Given the difficulty, maybe the problem expects a brute force with optimizations in Python, and the test cases are not worst-case. But the constraint says r < 10^9, so l=1, r=10^9-1 is possible. In competitive programming, Python solutions for such problems often use PyPy and a simple loop if the number of iterations is at most ~10^7, but 10^9 is too much.

Wait, maybe I misread: "1 <= l <= r < 10^9". So r can be 999,999,999. The difference r-l can be nearly 10^9. No way to iterate in Python.

We need a mathematical formula or a much faster algorithm. Let's think again.

Observation: If a number has a zero digit, it's beautiful. So non-beautiful numbers are exactly those with no zero digit and S ∤ P.

How many such numbers exist? For a k-digit number with no zero, the number of such numbers is 9^k minus the beautiful ones. The beautiful ones among no-zero numbers: we need to count them.

Can we characterize when S|P for no-zero numbers?
- If the number is 1...1 (k ones), S=k, P=1. Only beautiful if k=1. So for k≥2, all 1...1 are NOT beautiful.
- If the number has a digit ≥ 2 and rest are 1s, P = that digit d, S = k-1+d. Need (k-1+d) | d. Since k≥2, k-1+d > d, so impossible. So all such numbers are NOT beautiful.
- So any number with at most one digit ≥ 2 and the rest 1s is NOT beautiful (except the single digit itself).

What about numbers with two digits ≥ 2? Let's see. For 2-digit numbers: beautiful ones are 22, 36, 44, 66, 88. That's 5 out of 81. About 6%.

For 3-digit numbers, we can try to enumerate by reasoning. But maybe there is a pattern: the condition S|P is quite restrictive when digits are small and sum is large. Actually, for no-zero numbers, product is at most 9^k, sum is at most 9k. For k≥3, 9^k grows much faster than 9k, so often S|P. But not always.

Wait, for k=3, digits a,b,c. S = a+b+c ≤ 27, P = abc ≤ 729. The probability that a random number up to 729 is divisible by a random number up to 27 is roughly sum_{s=1}^{27} 1/s ≈ 4 (divisor sum). Actually, the expected number of divisors of a number is ~log n. So P has about log(729) ≈ 6.6 divisors on average. So the chance that S is one of them is about 6.6/27 ≈ 0.24. So about 24% of 3-digit no-zero numbers are beautiful? But we need to check.

Actually, the number of (a,b,c) with S|P is the number of triples where abc is a multiple of a+b+c. This is a Diophantine condition. We can compute it by brute force for small k, but for k up to 9, the number of no-zero numbers is 9^9 ≈ 3.8e8, still too many.

But maybe we can use a DP that tracks the remainder of product modulo sum? The problem is that sum is not fixed. However, we can fix the sum S and do DP for that S, counting numbers with sum S and product divisible by S. Then sum over S.

For a fixed sum S (1 ≤ S ≤ 81), we want to count k-digit numbers (k from 1 to 9, but actually up to 9 digits, but also numbers with fewer digits have leading zeros? No, we can handle each length separately, or allow leading zeros in DP and subtract the all-zero case. But since we only consider no-zero numbers, leading zeros are not allowed, so for a k-digit number, the first digit is 1-9, others 1-9. This is a constrained composition.

For a fixed S, the product P must be a multiple of S. The product of digits is at most 9^9 ≈ 3.8e8. For each S, we could in principle enumerate all products that are multiples of S and achievable as product of digits in 1..9 with sum S, and count the number of ways. But the number of such products might be large.

Alternatively, for fixed S, we can do a DP over positions, tracking the product modulo S. The state would be (position, product_mod_S). The number of states is 9 * S, and S ≤ 81, so at most 9*81=729 states. Transitions: for each next digit d in 1..9, new remainder = (old_rem * d) % S, but we also need to track the sum. So we need to track sum as well, but sum is fixed to S, so we just need to ensure that after k digits, the sum is S. So we can do a DP that builds the number digit by digit, tracking the current sum and product modulo S.

DP state: dp[pos][rem][sum] = number of ways to fill pos digits with sum 'sum' and product mod S = 'rem'. But sum is at most 81, pos at most 9, rem at most S-1 ≤ 80. So state size is 9 * 81 * 81 ≈ 59000. For each S, we do this DP. There are 81 values of S, so total states ~ 81 * 59000 ≈ 4.8e6, which is fine. Transitions: for each digit d, new_sum = sum + d, new_rem = (rem * d) % S. We only allow if new_sum ≤ 81 (or ≤ S if we want to end exactly at S). Actually, we want to count numbers with exact sum S. So we can do DP that counts all numbers (with length up to 9) with sum ≤ S and track product mod S, and then for each S, we look at the count where sum = S. But we also need to handle different lengths and the fact that for each length, the first digit cannot be zero (but since we only consider no-zero numbers, all digits 1-9 anyway, so no leading zero issue if we consider all lengths from 1 to 9, but we need to ensure that numbers with fewer than 9 digits are counted. We can do DP over exactly 9 positions, allowing leading zeros? But we cannot allow zero digits at all. So we need to consider numbers of different lengths separately, or we can allow leading zeros in the DP but then exclude the zero digit entirely? No, because leading zeros are not actual digits. A number like 00123 is just 123, and 123 has no zero. So we can do a DP over exactly 9 positions, where the first non-zero digit starts the number, and all subsequent digits (including after the number ends? No, once we start, we continue until 9 digits? That would count numbers with more than 9 digits or pad with zeros, but zeros are not allowed. So we cannot pad with zeros.

Better: For each length L from 1 to 9, do a DP for that length. For length L, the state is dp[pos][rem] where pos is the number of digits placed, and rem is the product modulo S. We also need to track the sum. So dp[pos][sum][rem]. We want to count assignments of L digits from {1..9} such that sum = S and product % S = 0. We can do this for each L and S.

Number of states: L up to 9, sum up to 9L ≤ 81, rem up to S-1 ≤ 80. For each S, we run DP for all L from 1 to 9. Complexity: O(81 * 9 * 81 * 9 * 10) = O(81 * 9 * 81 * 9 * 10) ≈ 5e6 operations. Very fast.

But wait, this counts the number of digit sequences (ordered) of length L with digits 1-9, sum S, and product divisible by S. This is exactly the count of beautiful no-zero numbers of length L. Then we sum over L and S? No, for a fixed number, its sum S is fixed, and product P is fixed. We just need to count for each S, the number of length-L sequences with sum S and product % S == 0. Then total beautiful no-zero numbers up to 9 digits is sum_{S=1}^{81} sum_{L=1}^{9} count(L, S). But this counts numbers with exactly L digits and no zero. However, we need to count numbers in [l, r], not all numbers up to 10^9. The DP counts all numbers of length L with no zero. But we need a range query [l, r].

We can do a digit DP that counts beautiful numbers up to N (i.e., in [1, N]). Then answer is f(r) - f(l-1). The DP would need to know the sum so far and the product modulo the sum? But the sum is not known until the end. In a standard digit DP, we process digits from most significant to least. We need to track the sum S and the product P. At the end, we check if S|P. But S is not known in advance. We could track the pair (S, P mod S)? But S varies, so P mod S is not well-defined in a state-independent way. However, we can track S and P explicitly? P can be up to 9^9 ≈ 3.8e8, too large for a state.

Alternative: Since we only care about S|P, and S is at most 81, we can do a DP that for each possible sum S, counts numbers with that sum and product divisible by S. But in a prefix DP, the sum is built incrementally. We can have a state that tracks the current sum S, and the product P modulo something? The condition S|P depends on the final S. We could track P modulo all possible divisors? Not feasible.

But wait, we can do a DP that tracks the actual product P (as a 64-bit integer) and the sum S. The number of states is the number of distinct (S, P) pairs achievable as prefix. For a prefix of length at most 9, the number of distinct pairs might be large. Let's estimate: for length 9, the number of distinct (sum, product) pairs is at most 81 * 9^9? No, product varies. But maybe the number of distinct products for a given sum is limited? For a fixed sum S, the number of distinct products of digits in 1..9 that sum to S is the number of partitions of S into parts 1-9, weighted by product. The number of such products is the number of distinct values of ∏ d_i. This could be large. For S=9, only product 9 (one 9) or 3*3*3? 3+3+3=9, product=27. So at least 2. For larger S, more combinations. In the worst case, the number of distinct products for a given sum S is the number of integer partitions of S into parts 1-9, which is exponential in S. For S=81, the number of partitions is huge. So tracking (S, P) as state is not feasible.

So the simple DP with state (S, P) won't work. We need a different insight.

Let's go back to the fact that the number of no-zero numbers is 9^9 ≈ 3.8e8, which is large but maybe enumerable in C++ but not Python. However, the problem might be from a platform where the time limit is generous, or the test cases are not worst-case. But the constraints explicitly say r < 10^9. In many coding challenges, a Python solution with a simple loop from l to r might pass if the test cases have small ranges, but here the constraint is explicit.

Wait, maybe I can use numpy or something? No, that's not allowed in standard competitive programming.

Another thought: The condition S|P for no-zero numbers. Note that P is a multiple of S. Let g = gcd(S, P). Then S/g divides P/g, but S|P means P is a multiple of S. We can write P = kS. Since P is product of digits in 1..9, and S is sum, we can think about the ratio P/S. For the number to be beautiful, P/S must be integer.

Is there a way to count numbers where S divides P by grouping by the multiset of digits? The number of ways to arrange a multiset of digits into a number is multinomial. But we need to count all numbers in a range, not just up to 10^9.

Maybe we can use the fact that the total number of no-zero numbers is 9^9, and we can iterate over them by generating them? In Python, generating 3.8e8 numbers is too slow.

Wait, what about using PyPy and a simple loop? In PyPy, a loop of 10^8 iterations with simple arithmetic takes about 30-60 seconds. Still too slow.

Perhaps the problem expects a digit DP with a clever state. Let's think about the condition again. We want to count numbers with S|P. We can think of it as: for each number, compute S and P, check if P % S == 0. In a digit DP, we can track the product modulo all possible sums? No.

Alternative: We can count the complement: numbers with S ∤ P. Or we can count numbers with a zero digit (easy) and subtract from total, then count beautiful no-zero numbers. The count of no-zero numbers up to N is a standard digit DP (count numbers with no zero digit). Let's call that NZ(N). The total numbers in [1, N] is N. So numbers with at least one zero = N - NZ(N). These are all beautiful. So beautiful count = N - NZ(N) + (beautiful no-zero numbers).

So we need to count beautiful no-zero numbers up to N. Let's denote BN(N). Then answer = (r - NZ(r) + BN(r)) - (l-1 - NZ(l-1) + BN(l-1)) = (r - l + 1) - (NZ(r) - NZ(l-1)) + (BN(r) - BN(l-1)).

But BN(N) is the number of no-zero numbers ≤ N with S|P. This is a digit DP where we track the sum S and the product P modulo... something. Since S is not fixed, we can track the actual product P and sum S, but as we saw, the state space might be large. However, note that for a prefix, the number of distinct (S, P) pairs is limited by the number of prefixes, which is 9^9 = 3.8e8, but we are building a DP, so we need to compress states. The number of distinct (S, P) for prefixes of length up to 9: for each length, there are 9^L prefixes. For L=9, 3.8e8 prefixes, but many share the same (S, P). The number of distinct P for a given S is the number of distinct products of digits in 1..9 with sum S. Is that number small? For S=9, possible products: 9, 3*3*3=27, 1*...*8 etc. Actually, the number of distinct products of a multiset of digits summing to S is the number of ways to partition S into 1-9 and multiply. This is not necessarily small. For S=45 (five 9s), product=9^5=59049. But there are many ways to sum to 45 with digits 1-9, e.g., 9,9,9,9,9 or 8,9,9,9,10? No 10. 8+9+9+9+10 no. Actually, with five digits, max sum is 45. The partitions of 45 into five parts from 1-9: the only way is 9,9,9,9,9. So product is unique. For S=44, five digits sum to 44: 9,9,9,9,8. Product=9^4*8=52488. Also 9,9,9,8,9 same. So product is unique. In general, for a given number of digits, the product is determined by the multiset? No, different multisets can have same product? For example, 2*3=6, 1*6=6, but 6 is not a digit? Digits are 1-9, so 6 is a digit. Sum of {2,3} is 5, product 6. Sum of {1,6} is 7, product 6. So different sums, different products. But could two different multisets of digits have same sum and same product? Yes: {2,2} sum=4 product=4, {4} sum=4 product=4. But they have different lengths. For a fixed length, can two different multisets have same sum and product? For length 2: {2,8} sum=10 prod=16, {4,4} sum=8 prod=16. Different sums. {3,3} sum=6 prod=9, {9} sum=9 prod=9. Different length. For length 3: {1,2,3} sum=6 prod=6, {1,1,6} sum=8 prod=6, {2,2,2} sum=6 prod=8. Not same sum and product. {1,3,3} sum=7 prod=9, {1,1,9} sum=11 prod=9. So maybe for a fixed length, the pair (sum, product) is unique? Let's test: length 4, sum=10, product=12. Possibilities: 1,1,1,7 sum=10 prod=7; 1,1,2,6 sum=10 prod=12; 1,1,3,5 sum=10 prod=15; 1,2,2,5 sum=10 prod=20; 1,2,3,4 sum=10 prod=24; 2,2,2,4 sum=10 prod=32; 2,2,3,3 sum=10 prod=36; 1,3,3,3 sum=10 prod=27. So product 12 comes from {1,1,2,6}. Is there another multiset with sum 10 and product 12? Need product 12. Factorizations: 12=12*1*1*1, but 12 is not a digit. 12=6*2*1*1, that's the one. 12=3*2*2*1, sum=3+2+2+1=8. 12=3*4*1*1, sum=3+4+1+1=9. So only {1,1,2,6}. What about product 16? 16=8*2*1*1 sum=12; 16=4*4*1*1 sum=10! So {1,1,4,4} has sum 10, product 16. And {2,2,2,2} has sum 8, product 16. But for sum 10, {1,1,4,4} and {2,2,2,4}? 2*2*2*4=32, no. {2,2,2,4} sum=10, product 32. So for sum 10, products are 7,12,15,20,24,32,36,27. All distinct? 7,12,15,20,24,32,36,27. Yes, all distinct. What about sum 12, length 3: {1,2,9} sum=12 prod=18; {1,3,8} sum=12 prod=24; {1,4,7} sum=12 prod=28; {1,5,6} sum=12 prod=30; {2,2,8} sum=12 prod=32; {2,3,7} sum=12 prod=42; {2,4,6} sum=12 prod=48; {2,5,5} sum=12 prod=50; {3,3,6} sum=12 prod=54; {3,4,5} sum=12 prod=60; {4,4,4} sum=12 prod=64. All distinct products. This suggests that for a fixed length L, the mapping from multiset of digits to (sum, product) might be injective. Is it always injective? That is, can two different multisets of digits from {1..9} of the same size L have the same sum and same product? This is a known problem: "Are the sum and product of a multiset of integers from 1..9 unique?" I recall that for {1..9}, the pair (sum, product) is not always unique. For example, for two numbers: {1,8} sum=9 prod=8, {2,7} sum=9 prod=14, {3,6} sum=9 prod=18, {4,5} sum=9 prod=20. All different. For three numbers: sum=10, product=24: {1,1,8}? 1+1+8=10, 1*1*8=8. {1,2,7} sum=10 prod=14. {1,3,6} sum=10 prod=18. {1,4,5} sum=10 prod=20. {2,2,6} sum=10 prod=24. {2,3,5} sum=10 prod=30. {2,4,4} sum=10 prod=32. {3,3,4} sum=10 prod=36. So {2,2,6} gives sum 10 prod 24. Is there another multiset with sum 10 and product 24? {1,1,8} no. {1,2,7} no. {1,3,6} no. {3,3,4} no. {1,4,5} no. {2,3,5} no. So unique. But what about sum=12, product=36: {2,2,3}? 2+2+3=7, no. {1,2,9}? 1+2+9=12 prod=18. {1,5,6} sum=12 prod=30. {2,2,8} sum=12 prod=32. {2,3,7} sum=12 prod=42. {2,4,6} sum=12 prod=48. {3,3,6} sum=12 prod=54. {3,4,5} sum=12 prod=60. {4,4,4} sum=12 prod=64. {1,3,8} sum=12 prod=24. {1,4,7} sum=12 prod=28. {1,2,3,6}? That's 4 numbers. So for length 3, sum=12, product=36? Is there a triple with sum 12 and product 36? Need a*b*c=36, a+b+c=12. Factorizations of 36 into three numbers 1-9: 1*6*6=36, sum=13. 2*2*9=36, sum=13. 2*3*6=36, sum=11. 3*3*4=36, sum=10. 1*4*9=36, sum=14. 1*3*12 no. 1*2*18 no. So no triple has sum 12 and product 36. So indeed, for length 3, each (sum, product) seems unique.

Is it always true that for a fixed length, the pair (sum, product) uniquely determines the multiset? This is related to the fact that the polynomial ∏ (1 + x^i y^i) has distinct terms? Not exactly. But if it's true, then for each length, the number of beautiful no-zero numbers is just the count of multisets with S|P, and then we multiply by the number of permutations (accounting for leading digit non-zero). But we need to count numbers in a range, not all numbers. So we still need a DP over the range.

However, if (sum, product) uniquely determines the multiset for a given length, then in a digit DP, we can track the multiset state? But we don't know the length in advance. Alternatively, we can track the product P and sum S, and since for a given length, the pair is unique, we can use it as a state. But the number of distinct (S, P) pairs for a given length L is the number of multisets, which is the number of partitions of S into L parts of size 1-9. This is a combinatorial number. For L=9, the number of such partitions is large. Let's estimate: the number of ways to choose 9 digits from 1-9 with repetition allowed is 9^9 = 3.8e8, which is the number of ordered tuples. The number of multisets is the number of combinations with repetition: C(9+9-1, 9) = C(17,9) = 24310. So there are at most 24310 multisets of size 9. For each, we have a sum and product. Many will be unique pairs, but some might collide? The number of multisets is 24310, which is small! So for a fixed length L, the number of distinct (S, P) pairs is at most the number of multisets, which is C(L+9-1, L) = C(L+8, L). For L=9, that's 24310. For L=1, 9. For L=2, C(10,2)=45. For L=3, C(11,3)=165. For L=4, C(12,4)=495. For L=5, C(13,5)=1287. For L=6, C(14,6)=3003. For L=7, C(15,7)=6435. For L=8, C(16,8)=12870. For L=9, 24310. Sum over L=1 to 9 is about 48620. So the total number of distinct (S, P) pairs across all lengths is at most around 50,000. This is small!

Therefore, in a digit DP, we can track the state as (length, multiset signature)? But the DP builds the number digit by digit from most significant to least. We need to know the multiset of digits chosen so far. The number of possible multisets of a prefix of length up to 9 is the sum of C(L+8, L) for L=1 to 9, which is ~48,620. So we can do a DP where the state is the multiset of digits chosen so far. But how to represent the multiset? A 9-element array of counts (counts of digits 1-9). The number of such count vectors with total count ≤ 9 is exactly the number of multisets of size ≤ 9 from 9 types, which is C(9+9, 9) = C(18,9) = 48620. So the state space is about 48k. That's very manageable.

In a digit DP for counting numbers ≤ N, we process digits. At each step, we have a prefix. We need to track the multiset of digits in the prefix. The number of states is ~48k. For each state, we have transitions by appending a digit. But we also need to know if the number is tight. So the DP would be: dp[pos][state][tight] = count. pos from 0 to len(N). state is the multiset of digits so far. At the end, we need to check if the full number is beautiful. But we don't know the full number's sum and product until the end. However, we can compute the sum and product from the multiset: sum = sum(d * count[d]), product = product(d^count[d]). So at the end, we can look up the sum and product for the state and check if product % sum == 0. This is feasible.

The number of states is ~48k. The number of transitions: from a state with total count k, we can add a digit d (1-9), leading to a new state with count[d] incremented. For the tight case, the digit is constrained by the bound. The DP would have a dimension for the current position in the number (up to 9 or 10), and tight (0/1). So total states ~ 10 * 48k * 2 = 960k. Transitions: for each state, up to 9 next digits. So total operations ~ 10 * 48k * 9 = 4.3 million. Very fast in Python!

But we also need to handle numbers with zero digits. In the DP, we can include zero as a possible digit. The state would track counts of digits 0-9, total 10 types. The number of multisets of size ≤ 9 from 10 types is C(10+9, 9) = C(19,9) = 92378. Still small. So we can include zero. But wait, if a number has a zero digit, it's automatically beautiful, so we don't need to check the product. We can just count them.

But the DP for range [1, N] counts all numbers up to N. We can do a digit DP that tracks the multiset of digits. At the end, we check if the number is beautiful. The condition is: if any digit is 0, it's beautiful. Else, compute sum and product from the multiset, check product % sum == 0.

This DP is very clean and efficient. The state can be represented as a tuple of counts of digits 0-9, but the total number of such tuples with sum ≤ 9 is 92378. We can map each state to an integer index. The DP can be done with memoization or iteratively.

Let's design the DP:
Function count_beautiful(N):
- Convert N to string of digits.
- Use recursion with memoization: dfs(pos, state, tight, leading_zero).
- pos: current position (0 to len).
- state: a tuple of 10 counts of digits used so far. But to make it hashable and efficient, we can use a string or a tuple.
- tight: bool, whether prefix is equal to N's prefix.
- leading_zero: bool, whether we are still placing leading zeros (i.e., number hasn't started). But since we are counting numbers from 1 to N, we need to handle leading zeros. Alternatively, we can start with the first non-zero digit. But it's easier to allow leading zeros and treat them as actual digits. However, if we allow leading zeros, then a number like 00123 is just 123, and the multiset of digits in the 5-digit representation includes two zeros and 1,2,3. But the actual number 123 has digits 1,2,3. So we need to ensure that leading zeros are not counted as part of the number's digits. This complicates the state: we need to know which zeros are leading and which are not. Actually, if we treat the number as exactly len(N) digits with leading zeros allowed, then a number like 00123 is represented with digits [0,0,1,2,3]. The sum of digits is 0+0+1+2+3=6, product is 0. Since product is 0, it would be considered beautiful (as 0 % sum == 0). But the actual number 123 has no zero, so its product is 6, sum 6, beautiful. Both are beautiful, so the answer might still be correct? But the condition for the actual number depends on its actual digits, not the padded representation. If we pad with leading zeros, the product becomes 0, which is divisible by any sum, so a number that is not beautiful (e.g., 12: sum=3, product=2, 2%3=1) becomes beautiful in the padded representation because product=0. So we cannot simply pad with leading zeros; the product would be wrong.

Therefore, we must not count leading zeros as part of the number. We need to handle the start of the number. A standard way: keep a flag started. When started is False, we can place a zero and remain not started, or place a non-zero to start. Once started, zeros are real zeros and affect the product (making it 0). So the state must include the started flag. The state is then: counts of digits placed so far (for the digits that are part of the number), plus the started flag. But the counts of digits 0-9: for digits before started, we don't count them. So we can have a state that is the tuple of counts of digits 0-9 for the number so far (excluding leading zeros). When started is False, the state is all zeros. When we place a non-zero, we start and set count of that digit to 1. When we place a zero after started, we increment count[0]. So the state space is the number of possible count vectors for a number of length up to 9 (since N < 10^9, max length 9). Actually, N can be up to 999,999,999 which is 9 digits. So the number of digits is at most 9. The state space is the number of count vectors for digits 0-9 with total count ≤ 9. That is C(10+9, 9) = C(19,9) = 92378. This is small.

We can implement the DP with memoization: dfs(pos, counts, tight, started). counts is a tuple of 10 integers. We can use a dictionary for memoization. Since the state space is ~92k, and we have up to 9 positions, the total number of states is 9 * 92k * 2 = ~1.6M, which is fine. Each state has up to 10 transitions (digits 0-9). So total operations ~16M, which is fast in Python (maybe 1-2 seconds).

At the end of the recursion (pos == len(N)), we need to check if the number is beautiful. If not started (i.e., the number is 0), we return 0 (since we count from 1). If started, we check: if count[0] > 0: return 1 (beautiful). Else, compute sum = sum(i * count[i] for i=1..9), product = product(i**count[i] for i=1..9). Then return 1 if product % sum == 0 else 0.

We also need to handle the tight condition: if tight, the max digit is the corresponding digit of N. Else, max digit is 9.

This DP counts beautiful numbers from 1 to N. Then answer = count_beautiful(r) - count_beautiful(l-1).

This approach is clean, efficient, and handles the range query properly. It avoids the pitfalls of iterating over all numbers or incorrect padding.

Let's verify with the examples:
Example 1: l=10, r=20. Beautiful numbers in [10,20]: 10, 11?, 12? Let's check:
10: has zero -> beautiful.
11: sum=2, prod=1, 1%2=1 -> not beautiful.
12: sum=3, prod=2, 2%3=2 -> not.
13: sum=4, prod=3, 3%4=3 -> not.
14: sum=5, prod=4, 4%5=4 -> not.
15: sum=6, prod=5, 5%6=5 -> not.
16: sum=7, prod=6, 6%7=6 -> not.
17: sum=8, prod=7, 7%8=7 -> not.
18: sum=9, prod=8, 8%9=8 -> not.
19: sum=10, prod=9, 9%10=9 -> not.
20: has zero -> beautiful.
So beautiful: 10, 20. Count=2. Matches.

Example 2: l=1, r=15. Beautiful: 1,2,3,4,5,6,7,8,9 (all 1-digit), 10 (zero), 11? no, 12? no, 13? no, 14? no, 15? no. So total 10. Matches.

So the DP approach works.

Implementation details:
- We need to represent the counts tuple efficiently. Since the total count is at most 9, each count is a small integer. We can use a tuple of 10 integers. But creating new tuples for each transition might be slow. We can use a dictionary with tuple keys, or we can use a list and convert to tuple for hashing. Since the number of states is ~92k, it's fine.
- We can precompute all possible count vectors and map them to indices to make it faster, but not necessary.
- Use lru_cache on the DFS function with arguments (pos, counts, tight, started). But tight is bool, started is bool. counts is tuple. Python's lru_cache with tuple arguments works. However, the state space is large but manageable. We need to be careful with recursion depth: max depth 9, so fine.
- We can also implement iteratively, but recursion is easier.
- For the product, we need to compute it for the final counts. Since counts are small, we can compute it on the fly. But we need to be careful with large products: 9^9 = 387,420,489, which fits in 64-bit. Python handles big integers anyway.
- Edge case: l=1, l-1=0. We need to handle count_beautiful(0) returning 0.

Let's estimate the time. For N=999,999,999 (9 digits). The DP will explore states. The number of states is bounded by 9 * 92378 * 2 ≈ 1.66M. Each state explores up to 10 digits. So about 16M operations. In Python, with function call overhead, this might take a few seconds, but should be within typical time limits (2-5 seconds). We can optimize by converting the counts tuple to a single integer using a mixed-radix encoding: each count is from 0 to 9, but the sum of counts is at most 9. Actually, the state space is exactly the number of weak compositions of at most 9 into 10 parts. The number is 92378. We can map each composition to an integer ID for faster dictionary lookups. But Python's tuple hashing is quite fast. We can also use a manual dictionary with a string key, but tuple is fine.

We need to be careful with the tight condition: if tight, we only allow digits up to the bound. If not tight, we allow 0-9. But we also need to consider the started flag. When started is False, we can place 0 and remain not started, or place 1-9 and start. The counts are only updated when we start. So the state counts remain all zeros until started. This means that for any prefix before starting, the counts are all zeros. So the state (pos, (0,...,0), tight, False) is shared. This is good.

At the end, when pos == len(N), if started is False, the number is 0, we return 0. If started is True, we evaluate the counts.

One potential issue: The counts tuple is of length 10. We need to update it when a digit is placed. We can do counts = list(counts) then append, but creating new lists is slow. We can use a tuple and addition: new_counts = counts[:digit] + (counts[digit]+1,) + counts[digit+1:]. This creates a new tuple. For 10 elements, it's fast enough. Or we can use a mutable array and backtrack, but recursion with tuple is simpler.

Given the state space is ~92k, and we have at most 9 positions, the total number of distinct (pos, counts, tight, started) is small. Actually, for a given pos, the counts have sum at most pos (since each step we add at most one digit to the number). So the number of states per pos is the number of compositions of at most pos into 10 parts. Summing over pos=0..9 gives 92378 total compositions. So the number of states is at most 9 * 92378 * 2 = 1.66M. Each state is computed once due to memoization. So it's fast.

We should also consider that for the tight=False case, the number of states is less because tight is False and started can be True or False. But it's fine.

Let's write the code.

```python
class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_upto(N):
            if N <= 0:
                return 0
            s = str(N)
            n = len(s)
            from functools import lru_cache

            @lru_cache(maxsize=None)
            def dfs(pos, tight, started, c0, c1, c2, c3, c4, c5, c6, c7, c8, c9):
                # pos: current index in s (0 to n)
                # tight: whether prefix is equal to N's prefix
                # started: whether we have placed a non-leading-zero digit
                # c0..c9: counts of digits placed so far (only after started)
                if pos == n:
                    if not started:
                        return 0
                    # Check if beautiful
                    if c0 > 0:
                        return 1
                    # Compute sum and product
                    total = 0
                    prod = 1
                    for i in range(1, 10):
                        cnt = locals()[f'c{i}']
                        total += i * cnt
                        prod *= i ** cnt
                    if total == 0: # should not happen since started and no zero
                        return 0
                    return 1 if prod % total == 0 else 0
                
                limit = int(s[pos]) if tight else 9
                total = 0
                for d in range(0, limit + 1):
                    ntight = tight and (d == limit)
                    nstarted = started or (d != 0)
                    if not nstarted:
                        # still leading zeros, counts unchanged
                        total += dfs(pos+1, ntight, False, 0,0,0,0,0,0,0,0,0,0)
                    else:
                        # we are in the number
                        if not started:
                            # first non-zero digit
                            new_counts = [0]*10
                            new_counts[d] = 1
                        else:
                            new_counts = [c0,c1,c2,c3,c4,c5,c6,c7,c8,c9]
                            new_counts[d] += 1
                        total += dfs(pos+1, ntight, True, *new_counts)
                return total

            return dfs(0, True, False, 0,0,0,0,0,0,0,0,0,0)

        return count_upto(r) - count_upto(l-1)
```

This should work. The number of arguments to dfs is large (13), but lru_cache can handle it. The use of locals() for fetching counts is slow. Better to pass the counts as a tuple. Let's use a tuple for counts.

```python
def dfs(pos, tight, started, counts):
    if pos == n:
        if not started:
            return 0
        if counts[0] > 0:
            return 1
        s = 0
        p = 1
        for i in range(1, 10):
            cnt = counts[i]
            s += i * cnt
            p *= i ** cnt
        return 1 if p % s == 0 else 0
    limit = int(s[pos]) if tight else 9
    total = 0
    for d in range(0, limit+1):
        ntight = tight and (d == limit)
        nstarted = started or (d != 0)
        if not nstarted:
            total += dfs(pos+1, ntight, False, (0,)*10)
        else:
            if started:
                lst = list(counts)
                lst[d] += 1
                new_counts = tuple(lst)
            else:
                lst = [0]*10
                lst[d] = 1
                new_counts = tuple(lst)
            total += dfs(pos+1, ntight, True, new_counts)
    return total
```

But creating a new tuple for each transition is okay given the state space is small. However, we can optimize by using a custom encoding of the counts into a single integer to speed up hashing. Since the sum of counts is at most 9, we can use a mixed-radix number where each count is a digit in base 10? But the max count for a digit is 9. So we can encode the tuple as a string of 10 characters, or as an integer where each count is a digit in base 10 (since max count is 9). For example, encode as c0*10^9 + c1*10^8 + ... + c9. Since each count is 0..9, this is a unique integer up to 10^10 - 1, which fits in Python int easily. This will make dictionary lookups much faster. Let's do that.

```python
def encode(counts):
    # counts is a tuple of 10 integers each 0..9
    res = 0
    for c in counts:
        res = res * 10 + c
    return res
```

Then the state is (pos, tight, started, encoded_counts). We need to decode when we need to modify. Or we can keep counts as tuple but use the encoded version as key. Actually, we can just use the tuple as key; Python's tuple hashing is efficient. But to reduce overhead, we can use the encoded integer. Let's stick with tuple for simplicity, but we can also use the encoded integer to avoid tuple creation overhead. However, we need to create a new tuple for each transition. Using an integer encoding might be faster.

Let's think about the maximum number of states. For pos=0, started=False, counts=(0,...,0). For pos=1, started can be False (if first digit 0) or True with one digit. So the number of states is small. The total number of states visited is exactly the number of possible (pos, started, counts) combinations that are reachable, times 2 for tight. Since the number of possible counts is 92378, and pos up to 9, started 2, tight 2, total ~1.6M. Each state is visited once. The overhead of tuple creation for each transition is 10 list element assignments and a tuple() call. For 1.6M states, each with up to 10 transitions, that's up to 16M tuple creations. This might be slow in Python (16M * overhead ~ 0.5 seconds? Actually, creating a tuple from a list is relatively fast, but 16M might be a few seconds). We can optimize by passing the counts as a mutable list and backtracking, but then we lose memoization. Alternatively, we can use the integer encoding and pass the integer, then decode to a list of digits (each digit 0-9) to modify, and re-encode. Since the base is 10, we can extract digits using divmod. But we need to increment one digit. We can precompute powers of 10. Let's do that for speed.

Let's implement with integer encoding:

```python
class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_upto(N):
            if N <= 0:
                return 0
            s = str(N)
            n = len(s)
            from functools import lru_cache

            # encode counts as integer: c0*10^9 + c1*10^8 + ... + c9
            # we will use a list of counts for modification, but store as int for memo key
            # Actually, we can store the tuple for simplicity.
            
            @lru_cache(maxsize=None)
            def dfs(pos, tight, started, c0, c1, c2, c3, c4, c5, c6, c7, c8, c9):
                if pos == n:
                    if not started:
                        return 0
                    if c0 > 0:
                        return 1
                    total = 0
                    prod = 1
                    counts = [c1,c2,c3,c4,c5,c6,c7,c8,c9]
                    for i in range(1, 10):
                        cnt = counts[i-1]
                        total += i * cnt
                        prod *= i ** cnt
                    if total == 0:
                        return 0
                    return 1 if prod % total == 0 else 0
                
                limit = int(s[pos]) if tight else 9
                res = 0
                for d in range(0, limit+1):
                    ntight = tight and (d == limit)
                    nstarted = started or (d != 0)
                    if not nstarted:
                        res += dfs(pos+1, ntight, False, 0,0,0,0,0,0,0,0,0,0)
                    else:
                        if d == 0:
                            nc0 = c0 + 1
                            nc = (c1,c2,c3,c4,c5,c6,c7,c8,c9)
                        elif d == 1:
                            nc0 = c0
                            nc = (c1+1,c2,c3,c4,c5,c6,c7,c8,c9)
                        # ... this is tedious
```

This is too many arguments. Better to use a tuple. But the function with 10 arguments might hit the recursion limit or be slow. Actually, lru_cache can handle many arguments, but the function call overhead is high. We can pack the counts into a single tuple and pass that. The tuple hashing is O(10). That's fine.

Let's write the final code with tuple counts.

```python
class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_upto(N):
            if N <= 0:
                return 0
            s = str(N)
            n = len(s)
            from functools import lru_cache

            @lru_cache(maxsize=None)
            def dfs(pos, tight, started, counts):
                # counts is a tuple of 10 ints
                if pos == n:
                    if not started:
                        return 0
                    if counts[0] > 0:
                        return 1
                    total = 0
                    prod = 1
                    for i in range(1, 10):
                        cnt = counts[i]
                        total += i * cnt
                        prod *= i ** cnt
                    if total == 0:
                        return 0
                    return 1 if prod % total == 0 else 0
                limit = int(s[pos]) if tight else 9
                res = 0
                for d in range(0, limit + 1):
                    ntight = tight and (d == limit)
                    nstarted = started or (d != 0)
                    if not nstarted:
                        res += dfs(pos + 1, ntight, False, (0,)*10)
                    else:
                        lst = list(counts) if started else [0]*10
                        lst[d] += 1
                        res += dfs(pos + 1, ntight, True, tuple(lst))
                return res

            return dfs(0, True, False, (0,)*10)

        return count_upto(r) - count_upto(l - 1)
```

This should be correct. Let's test with small values.

Test l=1, r=15:
count_upto(15): numbers 1..15.
Let's simulate mentally: 1..9: all beautiful (9). 10: beautiful (zero). 11: sum=2, prod=1, not. 12: not. 13: not. 14: not. 15: not. So 10. count_upto(15) should be 10. count_upto(0)=0. So answer 10.

Test l=10, r=20:
count_upto(20): 1..20.
1..9: 9. 10: 1. 11:0. 12:0. 13:0. 14:0. 15:0. 16:0. 17:0. 18:0. 19:0. 20:1 (zero). Total = 11.
count_upto(9) = 9. So answer = 11 - 9 = 2. Correct.

The DP seems correct. The only potential issue is performance. Let's analyze the number of states. For N up to 10^9, n=9 or 10? 10^9 is 1000000000, which is 10 digits. But the constraint says r < 10^9, so r <= 999,999,999, which is 9 digits. So n <= 9. Good.

The number of possible counts tuples with sum of counts <= 9 is C(9+10, 9) = C(19,9) = 92378. For each pos (0..9), started (0/1), tight (0/1), we have states. But tight=0 and tight=1 are separate. The number of states with tight=0 is roughly the number of (pos, started, counts) reachable without tight constraint. That is the number of ways to choose a prefix of length pos with digits 0-9, but respecting that if started is False, counts are all zero. Actually, for tight=0, the DP is counting all numbers of length exactly n (with leading zeros allowed) that are ≤ something? No, tight=0 means we are not bounded by N, so we are counting all completions. The number of states for tight=0 is the number of (pos, started, counts) that can occur in a full enumeration of all length-n sequences of digits. This is exactly the number of compositions of at most pos into 10 parts, for each pos. Summing over pos=0..n gives the total number of compositions of at most n into 10 parts, which is C(n+10, n) = C(19,9) = 92378. So there are at most 92378 states with tight=0 for a given started? Actually, started is part of the state. For started=False, the counts are always (0,...,0). So there is only 1 such state per pos. For started=True, the counts have sum = pos (since each step we add one digit, and we started at some point). The number of counts with sum exactly k is C(k+9, 9). Summing over k=1..pos gives C(pos+10, pos) - 1. For pos=9, that's C(19,9) - 1 = 92377. So the total number of (pos, started=True, counts) states with tight=0 is 92377. With started=False, it's 10 (one per pos). So total states with tight=0 is about 92387. With tight=1, it's at most the same, because tight=1 states are subsets of the full tree. So total states across both tight values is at most 2 * 92387 = 184774. This is very small! My previous estimate of 1.6M was off because I assumed started is part of the state, but the number of possible counts is only 92k total, not per pos? Wait, the counts tuple is for the entire number built so far. The sum of counts in the tuple is equal to the number of digits placed so far (after started). So for a given pos, the sum of counts is at most pos. The number of possible count tuples with sum exactly k is C(k+9, 9). So the total number of possible count tuples across all pos is sum_{k=0}^{9} C(k+9,9) = C(19,10) = 92378. So indeed, the total number of distinct count tuples is 92378. So the state (pos, started, counts) has at most 10 * 92378 = 923780 states. With tight, it's at most double: 1.8M. But since lru_cache memoizes, each state is computed once. The number of states is around 1.8M. This is fine.

The transitions: for each state

## worker: Implement the digit DP solution with memoization t
The solution uses a digit DP with memoization. The state tracks the current position, whether the prefix is tight to N, whether the number has started (to handle leading zeros correctly), and a tuple of counts for digits 0-9 used so far. The total number of distinct count tuples for numbers up to 9 digits is C(19,9) = 92,378, making the state space small (~1.8M states). At the end of the recursion, we check if the number is beautiful: if it contains a zero, it's automatically beautiful; otherwise we compute the digit sum and product and check divisibility. The answer is computed as count_upto(r) - count_upto(l-1). This approach efficiently handles the range up to 10^9 without iterating over every number.
