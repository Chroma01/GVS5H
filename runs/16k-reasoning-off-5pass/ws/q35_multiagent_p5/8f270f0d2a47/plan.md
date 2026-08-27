The constraints allow r up to 10^9, so we cannot iterate through all numbers. We use digit dynamic programming (digit DP) to count beautiful numbers up to a given number n, then compute the answer as count(r) - count(l-1). The key insight is that the sum of digits S and the product of digits P are bounded: S <= 9*9=81 for numbers up to 10^9, and P can be large but we only care if P % S == 0. However, tracking the exact product is infeasible. Instead, we note that for numbers with many digits, the product grows very fast. We can use memoization with state (position, tight constraint, current sum, current product modulo some value?). Actually, since S is small (<=81), we can track the product exactly only if it's not too large. But product can be up to 9^9 which is huge. 

Better approach: Since S is small (at most 81 for 9-digit numbers), we can iterate over all possible sums S from 1 to 81. For each S, we count numbers where sum of digits is S and product of digits is divisible by S. But this is still complex.

Alternative: Use digit DP with state (pos, tight, sum, product). But product can be large. However, note that if the product becomes very large, we can still track it. But 9^9 is about 387 million, which is too large for a DP state.

Insight: We can use the fact that the number of distinct products that are divisors of some S (where S <= 81) is limited. Actually, we don't need the exact product; we need product % S == 0. But S varies.

Standard solution for this problem: Use digit DP where state is (pos, tight, sum, product). To handle large products, we can use memoization with a dictionary or note that many products will be the same. But worst-case product is 9^9 which is too big.

Actually, a known trick: Since the sum of digits is at most 81, we can precompute for each possible sum s, the set of products that are divisible by s. But generating all products is hard.

Another known approach: Iterate over all possible sums s from 1 to 81. For each s, use digit DP to count numbers with digit sum s and digit product divisible by s. The state for inner DP: (pos, tight, current_sum, current_product). But current_product can be large. However, we can use memoization with a map for product. Since for a fixed s, we only care if product % s == 0, and s is small, we can track product modulo s? No, because we need exact divisibility.

Actually, we can observe that for numbers with more than 9 digits, but r < 10^9, so at most 9 digits. The maximum product is 9^9 = 387,420,489. This is too large for an array but can be used as a key in a dictionary in memoization. The number of states: pos (10) * tight (2) * sum (82) * product (up to 387 million) is too many.

Better: Use recursion with memoization and a dictionary for the product. In practice, many products will not be reached or will be the same. We can try this.

Steps:
1. Define a helper function count(n) that returns the number of beautiful numbers in [1, n].
2. In count(n), convert n to digits.
3. Use DFS with state (index, tight, current_sum, current_product).
4. Base case: if index == len(digits), return 1 if current_sum > 0 and current_product % current_sum == 0 else 0.
5. Memoize states. Use a dictionary for memoization keyed by (index, tight, current_sum, current_product).
6. In the DFS, iterate over possible digits (0 to limit if tight, else 0-9), update tight, sum, and product.
7. Return count(r) - count(l-1).

This should work because the number of distinct products encountered in practice for numbers up to 10^9 is not too large due to the constraints of digit sums and the structure of the DP.