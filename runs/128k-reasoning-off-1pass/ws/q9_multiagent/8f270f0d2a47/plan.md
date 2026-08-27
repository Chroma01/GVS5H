The problem requires counting numbers in a range $[l, r]$ where the product of digits is divisible by the sum of digits. Since $r$ can be up to $10^9$, a linear scan is too slow. We will implement a Digit DP approach. The state will track the current position, whether we are restricted by the upper bound, the current sum of digits (which is small, max $9 \times 9 = 81$ for 9 digits, or slightly more for $10^9$), and the current product of digits. To handle the divisibility check efficiently, we can track the product modulo the sum, but since the sum changes, we instead track the product and sum directly in the DP state, noting that the maximum product for 9 digits is $9^9 \approx 3.87 \times 10^8$, which fits in a 64-bit integer. However, storing the full product in the DP state might be too large for memoization. A better approach is to observe that we only need `product % sum == 0`. But `sum` varies. Alternatively, since the maximum number of digits is small (up to 10), we can just store the product and sum in the state. Wait, $9^9$ is too big for a direct array index. Let's reconsider. The maximum sum is $9 \times 10 = 90$. The product can be large. However, we only care about `product % sum == 0`. We can't easily track `product % sum` because `sum` changes. 
Actually, we can just store the product and sum. The maximum product for a 10-digit number (if $r=10^9$, the number is $10^9$, digits 1,0,0... product 0, sum 1) is actually bounded. For numbers up to $10^9$, the max product is for $999,999,999$ which is $9^9 \approx 387,420,489$. This is too large for a standard array dimension. 
However, notice that if the product is 0 (contains a 0), then $0 \% \text{sum} == 0$ is always true (since sum > 0). So any number with a 0 is beautiful. We can count numbers with 0 separately or handle it.
For numbers without 0, the product is non-zero. The maximum product is $9^9$. Is there a way to compress the state? 
Actually, the constraints say $r < 10^9$, so max 9 digits. Max product $9^9$. 
Wait, maybe we don't need to store the full product. We can store the product modulo some large number? No, divisibility depends on the actual value.
Let's re-evaluate the constraints. $r < 10^9$. Max digits = 9.
Is it possible that the number of distinct products is small? No.
Alternative idea: Since the sum is small (max 81), maybe we can iterate on the sum? No, the sum depends on the digits.
Let's look at the "beautiful" condition again: $P \equiv 0 \pmod S$.
If we include 0 in the digits, $P=0$, and $0 \% S = 0$ is always true. So all numbers containing at least one '0' are beautiful.
We can count total numbers in $[l, r]$ minus numbers that do NOT contain '0' AND are NOT beautiful.
Numbers without '0' have digits $1-9$. Max product $9^9$.
This seems hard to optimize with standard DP state if we store product.
Wait, is there a property I'm missing?
Ah, the maximum sum is 81. The product can be large.
But maybe we can just use a dictionary for memoization? The state is `(index, tight, sum, product)`.
Number of states: `index` (10) * `tight` (2) * `sum` (81) * `product` (huge). This is too big.
Let's reconsider the "contains 0" logic.
Total beautiful = (Numbers with at least one 0) + (Numbers with no 0 AND beautiful).
Numbers with at least one 0: We can calculate this as Total - (Numbers with no 0).
Then we just need to count numbers with no 0 (digits 1-9) that satisfy $P \% S == 0$.
For numbers with digits 1-9, max product is $9^9 \approx 3.8 \times 10^8$. Still large.
Is it possible the test cases are weak or there's a mathematical trick?
Or maybe the number of valid products for a given sum is small?
Actually, let's look at the constraints again. $10^9$.
Maybe we can swap the DP? Iterate on the sum $S$ from 1 to 81. For a fixed sum $S$, we want to count numbers with digit sum $S$ and product divisible by $S$.
But generating numbers with fixed sum and checking product is still hard.
Wait, what if we just use recursion with memoization and hope the number of reachable states is small?
State: `(idx, tight, current_sum, current_product)`
`current_sum` max 81.
`current_product` can be up to $9^9$.
However, many products are unreachable or redundant.
Actually, there is a known solution for this problem on LeetCode (Problem 2499? No, similar).
The trick is often that for numbers without 0, the product grows very fast.
Let's try to code the DP with a dictionary for the product part or just rely on the fact that many paths are pruned.
Actually, the maximum sum is 81. The maximum product for sum=81 is $9^9$.
But for small sums, the product is small.
Maybe we can just implement the DP with a `@lru_cache` and see if it passes. The number of states might be manageable because `tight` constraint limits the branching, and `sum` limits the depth.
Wait, if `tight` is false, we have full freedom.
Let's refine the "contains 0" strategy.
1. Count numbers in $[1, N]$ that contain at least one '0'. Let this be $C_0(N)$.
   $C_0(N) = N - (\text{count of numbers in } [1, N] \text{ with no '0'})$.
   Counting numbers with no '0' is easy: Digit DP with digits 1-9.
2. Count numbers in $[1, N]$ with no '0' that are beautiful. Let this be $C_{nb}(N)$.
   Then answer for $[l, r]$ is $(C_0(r) + C_{nb}(r)) - (C_0(l-1) + C_{nb}(l-1))$.
   Note: $C_0(r) + C_{nb}(r)$ is just the total beautiful numbers in $[1, r]$.
   So we need a function `countBeautiful(N)` which returns count of beautiful numbers in $[1, N]$.
   Inside `countBeautiful(N)`:
     - Calculate `total_no_zero(N)`: count of numbers in $[1, N]$ using only digits 1-9.
     - Calculate `beautiful_no_zero(N)`: count of numbers in $[1, N]$ using only digits 1-9 such that product % sum == 0.
     - Result = `(N - total_no_zero(N)) + beautiful_no_zero(N)`.
   
   Now, how to compute `beautiful_no_zero(N)`?
   DP state: `(idx, tight, current_sum, current_product)`
   Since digits are 1-9, `current_sum` max is $9 \times 9 = 81$.
   `current_product` max is $9^9$.
   Is the number of states too big?
   Let's estimate: `idx` (10) * `tight` (2) * `sum` (81) * `product` (many).
   However, for a fixed `idx` and `sum`, the `product` is determined by the specific digits chosen? No, different permutations give same sum but different products.
   But maybe the number of distinct products reachable for a given sum and length is not that huge?
   Actually, for small lengths, it's small. For length 9, sum 45, product could be $3^9$ or $5^9$ etc.
   Wait, if we use `lru_cache`, it will only visit reachable states.
   Given the constraints and typical CP problems, this approach with memoization is likely the intended solution, possibly with the optimization that we don't need to store the full product if we can prove something, but here we probably just need to store it.
   Wait, $9^9$ is too big for an array, but a dictionary key is fine. The number of *reachable* (sum, product) pairs might be much smaller than $81 \times 9^9$.
   Let's proceed with this.