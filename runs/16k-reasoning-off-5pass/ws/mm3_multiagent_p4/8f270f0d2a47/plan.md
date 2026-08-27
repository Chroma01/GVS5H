We need to count numbers in [l, r] where the product of digits is divisible by the sum of digits. Since r < 10^9 (max 9 digits), we can precompute all "beautiful" numbers up to 10^9-1 once, then answer queries with binary search. Approach: iterate over all numbers from 1 to 10^9-1 by generating all digit combinations (0-9) for each length, compute product and sum, check divisibility (skip if sum=0, i.e., number contains all zeros). However, iterating all 10^9 numbers is infeasible. Better: brute-force over all numbers up to 10^6 (since most interesting behavior is in lower digits) and just iterate directly in O(N) per query? No, we need multiple queries possibly. We can iterate all numbers from 1 to r (max ~10^9) — still too slow.

Alternative: Since the condition only depends on digit multiset, we can use DP over digit positions (digit DP) to count numbers ≤ X. DP state: position, tight flag, current sum, current product, and a flag "has_nonzero" (to avoid sum=0). But product can be huge (9^9 ~ 387M) — still manageable as a factor. We can store product directly. DP complexity ~ positions * sum_max * product_states. Sum max for 9 digits = 81. Product max = 9^9 = 387,420,489. That's too large for product dimension.

Insight: product divisible by sum. Equivalent: sum | product. Sum ranges 1..81. We can iterate over possible sums s, and for each s, count numbers where product % s == 0. We can DP over positions tracking (sum_so_far, product_mod_s) where s is fixed. For each s from 1..81, do DP to count numbers ≤ X with sum=s and product% s ==0. Total complexity: 81 * (positions * 81 * s) ≈ 81 * 10 * 81 * 81 ≈ 5M — feasible. This yields an O(81 * 10 * 81 * max_s) DP per X, which is fine. We'll compute count(X) = sum over s of DP. Then answer = count(r) - count(l-1).

DP design: memoize (pos, sum, prod_mod, tight, started). 'started' indicates if we've placed a non-leading digit yet (to handle leading zeros). If not started, sum=0, prod=1 (but we'll ignore). When we place a digit d (0..max_digit):
- If not started and d==0: keep started=False, sum=0, prod=1 (unused).
- Else: new_started=True, new_sum = sum + d, new_prod = (prod * d) % s (but if d==0, product becomes 0, which means actual product 0; we need to treat 0 specially: if any digit is 0, product=0, divisible by any sum, so number is beautiful unless sum=0 (which would mean all digits zero, not a valid positive number). So we can short-circuit: if d==0 and started==True, then product becomes 0 -> always divisible. So we can have a flag "product_is_zero". Simpler: when we encounter d==0 after started, set product_mod=0 (any s divides 0, so always true). In DP we need to know if product is exactly 0. Since we only care mod s, product_mod=0 is equivalent to "product is multiple of s", which is sufficient. But if we later multiply by more digits, 0 remains 0. So we can just set prod_mod=0 and keep it. Good.

Thus DP per s:
- State: (pos, sum, prod_mod, tight, started). sum ranges 0..s (since we only need sum == s at end). Actually sum can exceed s, but we can cap at s+1 (invalid) to prune.
- At the end (pos == n), if started and sum==s and prod_mod==0 -> count this number.

Complexities: positions up to 10 (for 10^9 has 10 digits? Actually 10^9-1 = 999,999,999 has 9 digits; r < 10^9 so max 9 digits). Use 10 to be safe.

We'll write a function count_upto(X) that returns count of beautiful numbers in [1, X]. If X < 1, return 0.

Implementation details:
- For each s in 1..81:
  - Build DP with memoization (lru_cache) for (pos, sum, prod_mod, tight, started).
  - pos from 0 to len(digits) of X.
  - digits = list(map(int, str(X))).
  - In recursion, at pos==len: return 1 if started and sum==s and prod_mod==0 else 0.
  - For each d in 0..max_digit:
    - new_started = started or (d != 0)
    - If not new_started: new_sum=0, new_prod_mod=1 (unused). But careful: if started=False and d==0, we are still not started, sum stays 0, prod stays 1.
    - Else: new_sum = sum + d. If new_sum > s: continue (prune). new_prod_mod = (prod_mod * d) % s if d != 0 else 0 (since product contains zero).
      - But careful: if started was True and d==0, then product becomes 0, new_prod_mod=0. If started was False and d!=0, then new_prod_mod = d % s.
    - Then proceed.

Edge case: number 0? Input l>=1, so we don't count 0.

This DP counts numbers of exactly len(digits) digits (allowing leading zeros) with the condition. But numbers with leading zeros correspond to shorter numbers. That's fine because we count them as long as they are valid (started becomes True at first non-zero digit). However, we must ensure we don't count the number 0 (all digits zero) — started will be False at end, so excluded.

Complexity: For each s, states ~ pos * (s+1) * s * 2 * 2 ≈ 10 * 82 * 82 * 4 ≈ 270k. Times 81 = ~22M, feasible.

We can further optimize by noting product_mod=0 is absorbing, but fine.

We'll implement Solution.beautifulNumbers(l, r) returning count(r) - count(l-1).