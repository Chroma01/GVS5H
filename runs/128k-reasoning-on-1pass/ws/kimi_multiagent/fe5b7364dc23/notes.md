
## ideation
Core difficulty: summing over all O(N^2) subarrays directly is impossible for N up to 2e5, but K is tiny (<=10), so expand subarray sums using prefix sums. Let P_0=0, P_i=P_{i-1}+A_i mod MOD. A subarray sum is P_r-P_{l-1}. The required sum is over ordered prefix pairs j<r of (P_r-P_j)^K. Binomial expansion turns each new prefix P_r into an O(K) update if we maintain aggregate power sums S_m = sum_{previous prefixes j} P_j^m for m=0..K:

sum_{j<r}(P_r-P_j)^K = sum_{t=0}^K C(K,t) P_r^t (-1)^{K-t} S_{K-t}.

Then add P_r^m into S_m and continue. Including the empty prefix is essential; iterating i=0..N with P_0 handled first naturally counts all l<=r. All arithmetic can be done mod 998244353 because the expression is polynomial in A_i.

Pitfalls: sign of (-1)^{K-t} must be mapped to MOD-1 when odd; binomial coefficients should be reduced mod MOD; prefix sums must be reduced before powering; powers should be built incrementally to avoid repeated pow; do not use O(NK^2) convolution per prefix unnecessarily; watch Python speed but O(NK) with K<=10 is fine; handle A_i=0 and N=1; ensure the previous-prefix sums are updated only after answering for current prefix to enforce j<r.

## worker: Implement the O(NK) prefix-power solution in Pytho
Let `P_0 = 0` and `P_r = A_1 + ... + A_r`. Every subarray sum is `P_r - P_{l-1}`, so the answer is  
`sum_{0 <= j < r <= N} (P_r - P_j)^K`.

Using binomial expansion:

`(P_r - P_j)^K = sum_{t=0}^K C(K,t) (-1)^(K-t) P_r^t P_j^(K-t)`.

While scanning prefixes increasingly, maintain `S_m = sum_{j<r} P_j^m`. Then each new prefix contributes  
`sum_t C(K,t)(-1)^(K-t) P_r^t S_{K-t}`, after which `P_r` is inserted into `S_m`. This is `O(NK)` time and `O(K)` memory, easily fast enough for `N <= 2e5`, `K <= 10`. All operations are modulo `998244353`, valid because the whole expression is polynomial in the `A_i`.
