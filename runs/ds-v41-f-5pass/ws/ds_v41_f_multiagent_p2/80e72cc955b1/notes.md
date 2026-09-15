- **Problem model:** For each query [l, r], the array is all integers from l to r inclusive. One operation selects two elements and replaces each by floor(x / 4). Model each element x by its cost c(x), the number of floor-divisions by 4 needed to become 0.

- **Cost function:** c(0)=0. For x>=1, c(x)=k exactly when 4^(k-1) <= x <= 4^k - 1. Thus c(x) equals the number of base-4 digits of x, computed as bisect_right(pow4, x) with pow4=[1,4,16,...]. Examples: c(1)=c(2)=c(3)=1, c(4)=...=c(15)=2, c(16)=...=c(63)=3. Since x<=1e9, maximum cost is 15.

- **Per-query answer:** Let S = sum_{x=l}^{r} c(x) and M = c(r) (cost is nondecreasing, so c(r) is the maximum). The minimum number of operations is max(M, ceil(S/2)). Lower bounds: each operation can reduce the total remaining cost by at most 2, and an element of cost M needs M separate operations. The bound is achievable: greedily pair the two largest remaining positive costs; when only one positive cost remains, pair it with a zero element.

- **Prefix sum closed form:** P(n) = sum_{x=1}^{n} c(x), with P(0)=0. If L=c(n), then P(n) = pref[L-1] + L*(n - 4^(L-1) + 1), where pref[k] = sum_{i=1}^{k} i*3*4^(i-1). Precompute pow4 and pref once. Then S = P(r) - P(l-1).

- **Implementation details:** For every query compute total = prefix_cost(r) - prefix_cost(l-1) and add max(cost(r), (total+1)//2). Python integers avoid overflow; the summed answer can exceed 32-bit range (roughly up to 7.5e14).

- **Complexity:** Precomputation is O(log maxR) ~ O(16). Each query is O(log maxR) for bisect calls. Total O(Q * 16), memory O(log maxR).

- **Edge cases:** Use c(r), not c(l), for the maximum. Exact powers of 4 must map to the higher bucket: bisect_right gives c(4)=2, c(16)=3. Handle l-1=0 via prefix_cost(0)=0. Ensure pref has enough entries for L up to 15 (we build up to 16).

- **Validation:** [[1,2],[2,4]] gives 1 + 2 = 3. [[2,6]] gives total costs 1+1+2+2+2=8, max=2, max(2,4)=4.
