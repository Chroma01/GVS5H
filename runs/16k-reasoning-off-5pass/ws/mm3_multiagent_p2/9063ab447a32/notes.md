
## ideation
The problem is to maximize total units \(K = \sum k_i\) subject to \(\sum P_i k_i^2 \le M\), where \(P_i > 0\), \(M \le 10^{18}\), and \(N \le 2\cdot10^5\).  
Because the cost is convex, the optimal solution is obtained by buying units in increasing order of marginal cost \( (2\ell-1)P_i \) (the \(\ell\)-th unit of product \(i\)).  
Thus the answer is the largest \(K\) such that the sum of the \(K\) smallest numbers in the multiset  
\(\{ (2\ell-1)P_i \mid i=1..N,\ \ell\ge 1 \}\) does not exceed \(M\).

For a threshold \(T\) we can compute:
- \(cnt(T) = \sum_i \left\lfloor \frac{T//P_i + 1}{2} \right\rfloor\) (how many numbers \(\le T\)),
- \(sum(T) = \sum_i P_i \cdot cnt_i(T)^2\) (sum of those numbers),
because the sum of the first \(t\) odd numbers is \(t^2\).

To check a candidate \(K\) we find the smallest \(T\) with \(cnt(T) \ge K\) (binary search on \(T\)), then the minimal sum is  
\(sum(T) - (cnt(T)-K)\cdot T\).  
Binary searching \(K\) itself gives the answer.

A single feasibility check costs \(O(N \log M)\) (\(\log M \approx 60\)).  
Binary searching \(K\) over \([0, \sum \sqrt{M/P_i}]\) needs \(\sim 48\) steps, total \(\sim 5.8\cdot10^8\) operations – too slow in Python.

We need to reduce the constant factor or avoid the inner binary search.  
One idea: compute the sum of the first \(K\) marginal costs directly in \(O(N)\) using the fact that the \(K\)-th smallest value is roughly \(M/K\).  
However, a simpler optimisation is to note that we can combine the two binary searches into a single binary search on the answer \(K\) while reusing the same \(O(N)\) work for the threshold search, but we must cut the number of iterations.

Better: we can binary search the answer \(K\) and for each \(K\) compute the required threshold \(T\) with a *custom* formula.  
Since \(cnt(T) = \sum_i \lfloor (T/P_i+1)/2 \rfloor\) is a step function, we can find the smallest \(T\) with \(cnt(T) \ge K\) in \(O(N)\) by a **parallel** selection? Not obvious.

Alternative: pre‑compute prefix sums of \(P_i\) and treat the problem as merging \(N\) arithmetic progressions.  
We can find the \(K\)-th smallest value by a “selection in sorted matrices” algorithm, but it would still be \(O(N)\) per query.

Given the constraints, the intended solution is likely the \(O(N \log M \log K)\) method, and it passes in C++ but is too slow in Python.  
We need a Python‑friendly optimisation: reduce the inner binary search to \(O(N)\) by **pre‑computing** for each product the number of units needed to reach a given marginal cost? Not possible.

Wait – we can avoid the inner binary search entirely by **directly computing the sum of the first \(K\) marginal costs** using the following trick:

For each product \(i\), the marginal costs are \(P_i, 3P_i, 5P_i, \dots\).  
If we want the first \(K\) values, we can binary search the value \(T\) as before, but we can **batch** the inner loop: the loop computing \(cnt_i\) and \(sum_i\) is the same for all \(T\).  
We can pre‑compute \(1/P_i\) and use integer division. The loop is already very fast in Python (a few integer ops per element).  
The real cost is the outer binary search on \(K\) (48 iterations).  
\(48 \times 2\cdot10^5 \times 60 \approx 5.76\cdot10^8\) integer divisions.  
On PyPy with PyPy 3.10, integer division is cheap but still ~10⁹ ops may be ~30 seconds.

We need a **faster** check.  
Observe that we can compute the answer without binary searching \(K\) at all!  
We can binary search the **threshold value** \(T\): for a given \(T\) we know we can take all items with cost \(<T\) and some of cost \(=T\).  
The total count is \(cnt_{<T} + \min(g(T), \lfloor (M - sum_{<T})/T \rfloor)\).  
This function is monotone in \(T\).  
If we binary search \(T\) we can find the largest \(T\) such that this count is maximal? Actually the count itself is monotone non‑decreasing, and it stabilises at the answer.  
We can find the answer by binary searching \(T\): for each \(T\) compute the count, then the answer is the maximum count we see.  
But we still need to find the exact maximum, which is the count at the threshold just before we cannot afford the next layer.  
However, the number of distinct possible \(T\) is huge (\(10^{18}\)), but we only need to consider \(T\) that are of the form \((2\ell-1)P_i\).  
We can find the smallest \(T\) such that we cannot afford all items with cost \(\le T\).  
Let \(T^*\) be the largest value with \(sum_{\le T^*} \le M\).  
If we take \(T = T^*\), we can take all items with cost \(\le T^*\).  
But maybe we could take some items with cost \(> T^*\) and still stay within budget? No, because if we take any item with cost \(> T^*\), we would have to drop some cheaper item, which would only reduce the count.  
So the optimal is to take all items with cost \(\le T^*\) that we can afford.  
If \(sum_{\le T^*} \le M\), we can take all of them; if \(sum_{\le T^*} > M\), we can only take a subset of the items with cost \(= T^*\).  
Thus the answer is exactly: take all items with cost \(< T^*\) and as many as possible of cost \(= T^*\) within the remaining budget, where \(T^*\) is the **largest value** such that the total cost of all items with cost \(\le T^*\) is \(\le M\)? No, if \(sum_{\le T^*} \le M\) we take all of them, but maybe we could also take some items with cost \(> T^*\) if we have leftover budget? Yes, if \(sum_{\le T^*} < M\) we might be able to take some items with larger cost. So \(T^*\) is not the answer; we need to go further.

But we can binary search the **answer count** \(K\) directly using the feasibility check. The check is the bottleneck.

We can speed up the check by **pre‑computing** the prefix sums of \(P_i\) and using a **divide‑and‑conquer** on the value \(T\)? Not sure.

Another angle: The number of binary search steps on \(K\) can be reduced by using the **continuous** approximation to get a very narrow interval, then doing a linear search? The answer can be up to \(2\cdot10^{14}\), far from the continuous estimate, so the interval would be large.

Wait, we can **invert** the process: we can compute the sum of the first \(K\) marginal costs in \(O(N)\) if we know the **maximum layer** \(L\) we will need. For a given \(K\), the maximum layer \(L\) is at most \(\sqrt{M/\min P_i} \le 10^9\). That's too large.

But we can bound \(L\) by \(K\) because each layer contributes at least one product. Actually the number of layers is at most \(K\) (trivially). Not helpful.

Maybe we can use a **Fenwick tree** or **segment tree** on the values? Not likely.

Given the time, perhaps the intended solution in Python uses the \(O(N \log M \log K)\) with some constant‑factor tricks, and it passes because the constants are small. Let's estimate: 2e5 * 60 * 48 = 576 million. If each iteration of the inner loop is just `q = T // P_i; cnt = (q+1)//2; sum_ += P_i * cnt * cnt`, that's about 5 operations per element. 576M * 5 = 2.88B operations, too many.

We need to cut the number of outer iterations (the binary search on K) drastically.  
Is it possible to compute the answer **directly** without binary search on K?  
Yes, by binary searching on the **value** \(T\): for a given \(T\) we can compute the maximum number of items we can take with cost \(\le T\) and budget \(M\). This is exactly the count we defined earlier: \(C(T) = cnt_{<T} + \min(g(T), \lfloor (M - sum_{<T})/T \rfloor)\).  
\(C(T)\) is monotone non‑decreasing in \(T\). We want the maximum \(C(T)\).  
Since \(C(T)\) increases only at values that appear in the multiset, the maximum is achieved at the largest \(T\) where we can still add at least one item? Actually after we have taken the optimal number of items, increasing \(T\) further will not increase the count because we cannot afford any more items of that larger cost. So the maximum count is achieved at the **threshold** \(T\) equal to the value of the last item taken (the \(K\)-th item).  
Thus we can binary search for the smallest \(T\) such that \(C(T) = C(T+1)\)? Not exactly.

But we can find the answer by a **parametric search** on the value: we want the largest \(K\) such that the sum of the first \(K\) items \(\le M\). This is equivalent to finding the smallest \(T\) such that the sum of all items with value \(\le T\) exceeds \(M\).  
Let \(T^*\) be the smallest value with \(sum_{\le T^*} > M\). Then the optimal number of items is \(cnt_{< T^*} + \max\{ r \le g(T^*) \mid sum_{< T^*} + r \cdot T^* \le M \}\).  
So we can find \(T^*\) by binary searching on the value \(T\) (over the set of possible values) and checking whether \(sum_{\le T} \le M\).  
But we also need to know \(g(T)\) and \(sum_{<T}\).  
The binary search on \(T\) would be over a range of size up to \(M\) (1e18), requiring ~60 iterations.  
In each iteration we need to compute \(sum_{\le T}\) and \(cnt_{\le T}\)? Actually to check \(sum_{\le T} \le M\) we need to compute \(sum(T)\). That's \(O(N)\). So total \(O(N \log M)\).  
Then after we find \(T^*\) (the first value where the sum exceeds \(M\)), we can compute the answer in \(O(N)\).  
So the whole algorithm would be **one** binary search on \(T\) plus a final \(O(N)\) pass.  
That's only \(O(N \log M)\) ≈ 12 million operations!  
This is the key insight.

Let's verify: We want the maximum number of items. Let \(f(T) = \sum_{i} P_i \cdot \left\lfloor \frac{T//P_i + 1}{2} \right\rfloor^2\) = sum of costs of all items with marginal cost \(\le T\).  
We also need \(cnt(T) = \sum_i \lfloor (T//P_i + 1)/2 \rfloor\).  
We know that as we increase the number of items taken, the total cost is \(f(T)\) for some \(T\).  
Specifically, if we take all items with cost \(\le T\), we have taken \(cnt(T)\) items and spent \(f(T)\) yen.  
If we cannot take all items with cost \(\le T\) because \(f(T) > M\), we can only take a subset of the items with cost exactly \(T\).  
Thus the optimal strategy is: find the largest \(T\) such that we can take **all** items with cost \(< T\) and a prefix of items with cost \(=T\) within budget.  
Equivalently, find the smallest \(T\) such that \(f(T) > M\). Let this be \(T_0\).  
Then for \(T = T_0 - 1\) (or the previous value), we can take all items with cost \(\le T_0-1\) and have some remaining budget.  
But we need to be careful: \(T_0\) is not necessarily a value that appears. The set of values is discrete.  
We can binary search for the smallest value \(T\) in the **multiset** of marginal costs such that the sum of all items with value \(\le T\) exceeds \(M\).  
But the multiset values are not contiguous, so we can binary search over integers; the condition \(f(T) \le M\) is monotone (as \(T\) increases, \(f(T)\) increases).  
Let \(T^*\) be the smallest integer such that \(f(T^*) > M\).  
Then for \(T = T^*-1\), we have \(f(T^*-1) \le M\).  
All items with cost \(< T^*\) are fully taken. The items with cost \(= T^*\) may be partially taken.  
The maximum number of items we can take is:
- All items with cost \(< T^*\): count = \(cnt(T^*-1)\), cost = \(f(T^*-1)\).
- Then we can take as many items of cost \(= T^*\) as budget allows: \(r = \min( g(T^*), \lfloor (M - f(T^*-1)) / T^* \rfloor )\), where \(g(T^*)\) is the number of items with cost exactly \(T^*\).
- Total count = \(cnt(T^*-1) + r\).

This is exactly the answer.  
So the algorithm is:
1. Binary search on integer \(T\) to find the smallest \(T\) with \(f(T) > M\).
2. Compute \(cnt_{<T} = cnt(T-1)\), \(sum_{<T} = f(T-1)\), and \(g(T)\) (number of items with cost = T).
3. Compute remaining = M - sum_{<T}, take r = min(g(T), remaining // T).
4. Answer = cnt_{<T} + r.

The binary search on \(T\) runs in \(O(\log M) = 60\) iterations. Each iteration computes \(f(T)\) in \(O(N)\). So total \(O(N \log M)\) ≈ 12 million ops. This is perfectly fast in Python!

We need to be careful with the definitions:
- For a given \(T\), \(cnt(T) = \sum_i \lfloor (T // P_i + 1) // 2 \rfloor\).
- \(sum(T) = \sum_i P_i \cdot cnt_i(T)^2\).
- \(g(T)\) = number of pairs \((i, \ell)\) such that \((2\ell-1)P_i = T\). Equivalently, for each \(i\), if \(T \% P_i == 0\) and \((T // P_i)\) is odd, then there is exactly one \(\ell\) for that product. So \(g(T) = \sum_i [ T \% P_i == 0 \text{ and } (T // P_i) \% 2 == 1 ]\).

In the binary search, we need to compute \(f(T) = sum(T)\). We don't need \(cnt(T)\) during the search, only \(f(T)\). But we can compute both to avoid recomputation? Actually we can compute just \(f(T)\). The binary search condition is \(f(T) > M\).

After finding \(T^*\) (the first \(T\) with \(f(T) > M\)), we need:
- \(cnt_{<T} = cnt(T-1)\)
- \(sum_{<T} = f(T-1)\)
- \(g(T)\)

We can compute these in one more pass over the data.

Edge cases: If for all \(T\) up to some large value \(f(T) \le M\), we might end up with \(T^*\) being beyond the range. But the maximum possible marginal cost we might need to consider is when we have taken all possible items? Actually we can take arbitrarily many items, but cost grows quadratically. For any product, the marginal cost of the \(\ell\)-th unit is \((2\ell-1)P_i\). As \(\ell \to \infty\), cost \(\to \infty\). So for a sufficiently large \(T\) (e.g., \(T = 2 \cdot 10^{18}\) or even larger), \(f(T)\) will exceed \(M\). So the binary search will find a \(T^*\) within the range \([0, \text{high}]\). We can set high to something like \(2 \cdot 10^{18}\) or just \(2 \cdot 10^{18}\) (since M ≤ 1e18, T won't need to be that large? Actually if we take many units, the marginal cost can be larger than M. For example, P_i=1, ℓ=1e9, marginal cost ≈ 2e9, which is > 1e9 but < 1e18. So T can be up to ~2e9 * max P_i? Actually the K-th smallest marginal cost is at most M (if we take K items with total cost ≤ M, the average cost ≤ M/K, but the K-th could be up to M). So T ≤ M is safe. But to be safe, we can set high = 2 * 10^18 (since M ≤ 1e18, and P_i up to 2e9, the marginal cost of a single unit is at most 2e9, but later units can be larger. However, we only need T up to the point where f(T) > M. Since f(T) is monotone, we can set high = 2 * 10^18 (or 4e18) to be safe.

But we need to be careful with overflow in Python? Python handles big integers.

Thus the algorithm is:
- Read N, M, list P.
- Binary search low = 0, high = 2*10**18 (or a larger bound) to find the smallest T such that sum(T) > M.
- In each step, compute sum(T) = sum( P_i * ((T // P_i + 1) // 2)**2 ). If sum(T) > M, set high = T; else low = T+1.
- After loop, T_star = low (the first T with sum > M).
- Compute for T = T_star - 1:
  - cnt_less = sum( (T // P_i + 1) // 2 )
  - sum_less = sum( P_i * ((T // P_i + 1) // 2)**2 )
  - g_T = number of i with T % P_i == 0 and (T // P_i) % 2 == 1.
- remaining = M - sum_less
- take = min(g_T, remaining // T) if T > 0 else 0 (if T=0, no items have cost 0, but T=0 would mean we can't take any items? Actually T=0 is not a marginal cost because P_i ≥ 1, so first marginal cost is at least 1. But binary search may go to T=0. We need to handle T=0 separately: if T_star = 0, that means even with T=0, sum(0) > M? But sum(0) = 0 for all, so sum(0) = 0 ≤ M. So T_star will be at least 1. But to be safe, if T_star = 0, we set answer = 0.)
- answer = cnt_less + take

We also need to consider the case where we can take all items with cost ≤ T_star (i.e., f(T_star) ≤ M). But by definition T_star is the first with f(T_star) > M, so f(T_star-1) ≤ M. So we are good.

But wait: what if we can take some items with cost > T_star as well? For example, f(T_star) > M, but maybe we can take all items with cost < T_star and a few items with cost > T_star, and still stay within budget? That would mean we can take items with cost > T_star without taking all items with cost = T_star. But since T_star is the first value where the **total** sum of all items up to T_star exceeds M, if we skip some items with cost = T_star, we could afford items with larger cost? No, because skipping a cheap item (cost T_star) to take a more expensive item (cost > T_star) would only increase total cost, so we cannot afford it. So the optimal is to take all items with cost < T_star and as many of cost = T_star as possible. Items with cost > T_star are too expensive.

Thus the algorithm is correct.

We need to implement efficiently:
- Pre-store P as a list of integers.
- In the binary search, we compute sum(T) by looping over P. This is O(N) per iteration. With 60 iterations, 2e5*60 = 12M loops. In Python, 12M loops with a few integer ops is fine (< 0.5 sec? Actually 12M loops might be ~0.2-0.3 seconds in PyPy, maybe 1 second in CPython). We also have the final O(N) pass. So total ~15M loops, definitely fine.

We need to be careful with the binary search bounds. Let's determine a safe high.

We need to find a T such that f(T) > M. Since f(T) is monotone, we can start with low = 0, high = 1.
While f(high) ≤ M, double high: high *= 2.
But we need to avoid infinite loop in case f(T) never exceeds M? But for any T, f(T) grows roughly as (T^2) * sum(1/P_i) / 4? Actually for large T, cnt_i ≈ T/(2P_i), sum_i ≈ sum_i P_i * (T/(2P_i))^2 = (T^2/4) * sum_i 1/P_i. So f(T) ~ C * T^2. So for sufficiently large T, f(T) > M. So we can just set a high bound large enough. Since M ≤ 1e18, and sum_i 1/P_i ≥ 1 / max(P_i) ≥ 5e-10? Actually P_i ≤ 2e9, so 1/P_i ≥ 5e-10. With N=2e5, sum_i 1/P_i could be as small as N / max(P) = 2e5 / 2e9 = 1e-4. Then f(T) ~ T^2 * 1e-4 / 4 = 2.5e-5 * T^2. To exceed 1e18, we need T^2 > 4e22, so T > 2e11. So high = 2e12 is safe. To be very safe, we can set high = 2 * 10**18.

But we must ensure that high is large enough so that f(high) > M. Let's compute a guaranteed upper bound. The maximum number of items we can take is K_max = sum_i floor(sqrt(M / P_i)). For each product i, the marginal cost of the (K_max_i)-th unit is (2 K_max_i - 1) P_i ≤ 2 sqrt(M P_i). So the maximum marginal cost we might need to consider is at most 2 sqrt(M * max P_i). With M=1e18, max P_i=2e9, sqrt(M*max P_i) = sqrt(2e27) = sqrt(2)*1e13.5 ≈ 1.4e13. So T ≤ 3e13. So high = 4e13 is enough. But to be safe, we can set high = 10**18 * 2 (since M ≤ 1e18, T cannot exceed M? Actually marginal cost could be larger than M? If we take one item of cost > M, we cannot afford it. The K-th smallest marginal cost for the optimal K is at most M (since total cost ≤ M, each item cost ≤ M). So T ≤ M is safe. So we can set high = M + 1, but careful: if M is the budget, the largest marginal cost of an item we take is ≤ M. So we can set high = M. But M can be 1e18, which is fine.

But wait: what if we have a product with P_i = 1, and we take k units, the marginal cost of the k-th unit is (2k-1). If we take k = sqrt(M) ≈ 1e9, the marginal cost is ≈ 2e9, which is less than M. So T is bounded by M. So we can set high = M. But is it possible that the optimal T is exactly M? For example, if we have only one product with P=1, we can take k = floor(sqrt(M)) units. The last marginal cost is (2k-1) which is about 2 sqrt(M) - 1, which is less than M for M > 4. So T < M. So high = M is safe.

Thus we can set high = M (or M+1). But we need to ensure f(high) > M? If we set high = M, and the optimal T is less than M, then f(high) will be > M because high is larger than the optimal T, and f is monotone. So f(M) > M? Not necessarily: if we set T = M, we are including all items with marginal cost ≤ M. Could it be that the sum of all items with marginal cost ≤ M is still ≤ M? That would mean we can take all items with cost ≤ M and still have budget left. Then the optimal T would be larger than M, but we argued T cannot exceed M because any item with cost > M cannot be taken (since one item cost > M). Actually if we take an item with cost > M, we would exceed budget. So the optimal K cannot include any item with cost > M. Therefore the optimal T is the value of the last item taken, which is ≤ M. So if we set T = M, f(M) is the cost of taking all items with cost ≤ M. Since we cannot take any item with cost > M, f(M) is the cost of taking **all** items that could possibly be taken (i.e., all items with marginal cost ≤ M). But wait, there could be items with marginal cost ≤ M that we cannot take all of because their total cost exceeds M. For example, P_i = 1, M = 10. The marginal costs are 1,3,5,7,9,11,... The items with cost ≤ 10 are 1,3,5,7,9. Their sum is 25 > 10. So f(10) = 25 > M. So f(M) > M. In general, for any M, f(M) is the sum of all items with marginal cost ≤ M. Is it always > M? Not necessarily: if M is very small, say M=1, and P_i are all large (e.g., P_i=10), then no item has cost ≤ 1, so f(1)=0 ≤ M. But then T_star would be 1? Let's see: we need to find smallest T with f(T) > M. If f(1)=0 ≤ M, we need larger T. For P_i=10, the first marginal cost is 10. So f(10) = 10. If M=1, f(10) > 1. So T_star will be somewhere between 1 and 10. So setting high = M might be too small if M is smaller than the first marginal cost. For example, M=5, P_i=10. Then f(5)=0 ≤5, f(10)=10>5, so T_star=10 > M. So we need high to be at least the smallest marginal cost that makes f(T) > M. The smallest marginal cost is min P_i. So we need high ≥ min P_i. Actually we need high to be large enough that f(high) > M. Since f(high) is monotone, we can just set high = 2 * 10^18 (or something huge). To be safe and simple, we can set high = 2 * 10**18. But we must ensure that the binary search doesn't overflow or loop too long. With high = 2e18, log2(high) ≈ 61, which is fine.

Thus we can do:
low = 0
high = 2 * 10**18 + 5  # a safe upper bound
while low < high:
    mid = (low + high) // 2
    if sum_cost(mid) > M:
        high = mid
    else:
        low = mid + 1
# After loop, low = high = smallest T with sum(T) > M
T_star = low

Then compute cnt_less and sum_less for T = T_star - 1 (if T_star > 0; if T_star == 0, answer is 0).
Then compute g_T_star.
Then answer = cnt_less + min(g_T_star, (M - sum_less) // T_star)  (if T_star > 0 else 0).

But we need to be careful: if T_star = 0, that means sum(0) > M? But sum(0) = 0, so impossible. So T_star ≥ 1.

One more nuance: The binary search condition is sum(T) > M. However, sum(T) is the cost of taking **all** items with marginal cost ≤ T. This includes items that we might not be able to afford all of them. The condition sum(T) ≤ M means we can afford all items with cost ≤ T. So the smallest T with sum(T) > M is the threshold where we cannot afford all items with cost ≤ T. This matches our earlier definition.

But is it possible that we can afford all items with cost ≤ T, but cannot afford any item with cost = T? Yes, if sum(T) ≤ M but sum(T+1) > M, then we can afford all items with cost ≤ T, and maybe some with cost = T+1? Actually if sum(T+1) > M, then we cannot afford all items with cost ≤ T+1. However, we might be able to afford a subset of items with cost = T+1. So the optimal T* is the smallest value such that sum(T*) > M? Let's test with an example.

Example: P = [4,1,9], M=9.
Marginal costs:
Product 2 (P=1): 1,3,5,7,9,...
Product 1 (P=4): 4,12,20,...
Product 3 (P=9): 9,27,...

Sorted: 1 (P2), 3 (P2), 4 (P1), 5 (P2), 7 (P2), 9 (P2 or P3), 9 (P3), ...

Compute sum(T):
T=1: items ≤1: only 1 (P2). sum=1 ≤9.
T=2: items ≤2: 1. sum=1 ≤9.
T=3: items ≤3: 1,3. sum=4 ≤9.
T=4: items ≤4: 1,3,4. sum=8 ≤9.
T=5: items ≤5: 1,3,4,5. sum=13 >9. So T_star=5.
Now compute for T=4:
cnt_less = number of items ≤4: 1,3,4 => 3.
sum_less = 8.
g_T_star = number of items with cost =5: only 5 (P2) => 1.
remaining = 9 - 8 = 1. T_star=5, remaining // 5 = 0. So take = 0.
Answer = 3 + 0 = 3. Correct.

Now test a case where we can take a partial layer:
Suppose P = [1, 1], M=4.
Marginal costs: 1,1,3,3,5,5,...
Sorted: 1,1,3,3,5,5,...
sum(T):
T=1: items ≤1: two 1's. sum=2 ≤4.
T=2: items ≤2: two 1's. sum=2 ≤4.
T=3: items ≤3: 1,1,3,3. sum=8 >4. So T_star=3.
Now T=2:
cnt_less = items ≤2: 2.
sum_less = 2.
g_T_star = items with cost=3: two 3's. g=2.
remaining = 4 - 2 = 2. T_star=3, remaining // 3 = 0. So take=0. Answer=2.
But the optimal answer: we can buy two units (cost 1+1=2) or we could buy one unit from each? Actually we have two products, we can buy one from each: cost 1+1=2, count 2. Could we buy three units? To buy three units, we must buy two from one product and one from the other. Cost = 2^2*1 + 1^2*1 = 4+1=5 >4. So max is 2. So answer=2 is correct.

Now test a case where we can take a partial layer:
Suppose P = [1, 10], M=15.
Marginal costs: 1,3,5,7,9,11,13,15,... (P=1)
P=10: 10,30,50,...
Sorted: 1,3,5,7,9,10,11,13,15,...
Compute sum(T):
T=1: items ≤1: 1 (P=1). sum=1.
T=2: same.
T=3: 1,3 sum=4.
T=4: same.
T=5: 1,3,5 sum=9.
T=6: same.
T=7: 1,3,5,7 sum=16 >15. So T_star=7.
Now T=6:
cnt_less: items ≤6: 1,3,5 => 3.
sum_less = 9.
g_T_star: items with cost=7: one (P=1) => 1.
remaining = 15 - 9 = 6. 6 // 7 = 0. So take=0. Answer=3.
But maybe we can do better? Let's see: we can buy 3 units from P=1: cost 1^2+3^2+5^2 = 1+9+25=35 >15. So we can only buy up to 2 units from P=1? Cost 1+9=10. Then we can buy one unit from P=10: cost 10. Total cost 20 >15. So maybe 2 from P=1 and 0 from P=10: cost 10, count 2. Or 1 from P=1 and 1 from P=10: cost 1+10=11, count 2. So max is 2? Wait, the answer from the algorithm is 3? Let's check: sum_less for T=6 includes items with cost 1,3,5. That's three items from P=1. Their cost is 1+9+25=35. But sum_less computed as P_i * cnt_i^2. For P=1, cnt_i = (6//1 + 1)//2 = (6+1)//2 = 3. So sum_i = 1 * 3^2 = 9. That's wrong! Because sum of first 3 odd numbers is 1+3+5=9, not 35. Wait, the sum of marginal costs is not the same as the cost of buying k units. The cost of buying k units is sum of marginal costs, which is indeed sum of odd numbers. For k=3, sum = 1+3+5 = 9. But the actual cost of buying 3 units from product 1 is k^2 * P = 9 * 1 = 9. So it matches! Because sum of first k odd numbers is k^2. So sum_i = P_i * k^2. So for P=1, k=3, sum=9. So sum_less = 9. That is correct. But earlier I thought cost of 3 units is 35, which is wrong. The cost is k^2 P = 9*1 = 9. So we can actually buy 3 units from product 1 for cost 9. Then we have remaining 6 yen. We can buy 0 units from product 10 (cost 10). So total count 3. Is that possible? Let's check: 3 units from P=1: cost 9. Yes, within budget. Can we buy 4 units from P=1? Cost 16 >15. So 3 is the max. So answer=3 is correct. The algorithm gave 3.

Now test a case where we can take a partial layer of a larger value:
Suppose P = [1, 100], M=150.
Marginal costs: P=1: 1,3,5,7,9,11,13,15,17,...
P=100: 100,300,...
Sorted: 1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,... up to some point, then 100.
Compute sum(T):
We want to see if we can take many from P=1. The sum of first k odd numbers is k^2. So we can take k=12 units: sum = 144 ≤150. k=13: sum=169 >150. So we can take 12 units from P=1. The 13th unit would cost 25. So with 144 spent, remaining 6, we cannot take 25. So answer=12.
Let's run the algorithm:
Find smallest T with sum(T) > 150.
We need to compute sum(T) for T values. For T < 25, the only items are from P=1: cnt = (T+1)//2, sum = cnt^2.
We want cnt^2 > 150. The smallest cnt with cnt^2 > 150 is cnt=13 (169). For cnt=13, we need (T+1)//2 = 13 => T+1 >= 26 => T >= 25. So T=25 gives sum=169 >150. T=24 gives cnt=12, sum=144 ≤150. So T_star = 25.
Now T=24:
cnt_less = (24+1)//2 = 12.
sum_less = 12^2 = 144.
g_T_star = items with cost=25: from P=1, since 25 is odd multiple of 1. g=1.
remaining = 150 - 144 = 6. 6 // 25 = 0. So take=0. Answer=12. Correct.

Now test a case where we can take a partial layer from a product with larger P:
Suppose P = [3, 4], M=20.
Marginal costs:
P=3: 3,9,15,21,...
P=4: 4,12,20,28,...
Sorted: 3,4,9,12,15,20,...
Compute sum(T):
T=3: items ≤3: 3 (P=3). sum=3.
T=4: items ≤4: 3,4. sum=7.
T=5: same.
T=6: same.
T=7: same.
T=8: same.
T=9: items ≤9: 3,4,9. sum=16.
T=10: same.
T=11: same.
T=12: items ≤12: 3,4,9,12. sum=28 >20. So T_star=12.
Now T=11:
cnt_less: items ≤11: 3,4,9 => 3.
sum_less = 16.
g_T_star: items with cost=12: from P=4, since 12 = 3*4? Wait 12/4=3, which is odd? 3 is odd, so yes. Also from P=3? 12/3=4, even, so no. So g=1.
remaining = 20 - 16 = 4. 4 // 12 = 0. So take=0. Answer=3.
But is that optimal? Let's see: we can buy 3 units: one from each? Actually we have two products. To get 3 units, we can buy two from P=3 and one from P=4: cost = 2^2*3 + 1^2*4 = 12+4=16 ≤20. Or one from P=3 and two from P=4: cost = 1^2*3 + 2^2*4 = 3+16=19 ≤20. Both give 3 units. Can we get 4 units? To get 4 units, we need to buy at least 2 from each. Cost = 2^2*3 + 2^2*4 = 12+16=28 >20. Or 3 from P=3 and 1 from P=4: cost = 3^2*3 + 1^2*4 = 27+4=31 >20. So max is 3. So answer=3 is correct.

Now test a case where we can take a partial layer from multiple items:
Suppose P = [1, 2, 3], M=10.
Marginal costs:
P=1: 1,3,5,7,9,11,...
P=2: 2,6,10,14,...
P=3: 3,9,15,...
Sorted: 1,2,3,3,5,6,7,9,9,10,11,...
Compute sum(T):
We need to find smallest T with sum(T) > 10.
Let's compute manually:
T=1: sum=1.
T=2: items: 1,2 sum=3.
T=3: items: 1,2,3 (P=1? wait 3 from P=1? 3 is odd multiple of 1, and 3 from P=3? 3 is 1*3? Actually P=3, first unit cost 3. So two items with cost 3? Let's list: P=1: 1,3,5,... P=2: 2,6,... P=3: 3,9,... So items ≤3: 1 (P1), 2 (P2), 3 (P1), 3 (P3). So four items. Their sum = 1+2+3+3 = 9.
T=4: same as T=3.
T=5: items ≤5: add 5 (P1). So items: 1,2,3,3,5. Sum = 14 >10. So T_star=5.
Now T=4:
cnt_less = 4 (items: 1,2,3,3).
sum_less = 9.
g_T_star: items with cost=5: from P1 only. g=1.
remaining = 10 - 9 = 1. 1 // 5 = 0. So take=0. Answer=4.
But can we get 5 units? Let's see: total cost of 5 units? We need to choose k_i. Suppose we take 3 from P1, 1 from P2, 1 from P3: cost = 9 + 2 + 3 = 14 >10. Try 2 from P1, 2 from P2, 1 from P3: cost = 4 + 8 + 3 = 15 >10. Try 2 from P1, 1 from P2, 2 from P3: cost = 4 + 2 + 18 = 24 >10. Try 1 from P1, 3 from P2, 1 from P3: cost = 1 + 12 + 3 = 16 >10. Try 1 from P1, 2 from P2, 2 from P3: cost = 1 + 8 + 18 = 27 >10. Try 1 from P1, 1 from P2, 3 from P3: cost = 1 + 2 + 27 = 30 >10. Try 4 from P1, 1 from P2: cost = 16+2=18 >10. So maybe 4 is the max. But let's try to get 5 units with lower cost: maybe 2 from P1, 1 from P2, 2 from P3? Already computed >10. 1 from P1, 2 from P2, 2 from P3: 1+8+18=27. 3 from P1, 1 from P2, 1 from P3: 9+2+3=14. So 4 seems max. Answer=4 is correct.

Now test a case where we can take a partial layer from multiple items and also from a larger T:
Suppose P = [1, 10], M=100.
We can take many from P=1. The sum of first k odd numbers is k^2. We want k^2 ≤ 100 => k=10 (sum=100). So we can take 10 units from P=1, cost 100. The 11th unit would cost 21, but we have no budget. So answer=10.
Algorithm: find T_star. For T < 21, only P=1 items. sum(T) = ((T+1)//2)^2. We need smallest T with sum > 100. ((T+1)//2)^2 > 100 => (T+1)//2 ≥ 11 => T+1 ≥ 22 => T ≥ 21. So T_star=21.
T=20: cnt_less = 10, sum_less = 100. g_T_star: items with cost=21: from P=1. g=1. remaining=0. take=0. Answer=10. Correct.

Now test a case where we can take a partial layer from a product with larger P, and also some from cheaper:
Suppose P = [2, 3], M=20.
Marginal costs:
P=2: 2,6,10,14,18,22,...
P=3: 3,9,15,21,...
Sorted: 2,3,6,9,10,14,15,18,...
Compute sum(T):
T=2: sum=2.
T=3: items 2,3 sum=5.
T=4: same.
T=5: same.
T=6: items 2,3,6 sum=11.
T=7: same.
T=8: same.
T=9: items 2,3,6,9 sum=20.
T=10: items 2,3,6,9,10 sum=30 >20. So T_star=10.
Now T=9:
cnt_less = 4 (2,3,6,9).
sum_less = 20.
g_T_star: items with cost=10: from P=2 (10/2=5 odd) and maybe from P=3? 10/3 not integer. So g=1.
remaining = 20 - 20 = 0. take=0. Answer=4.
But can we get 5 units? Let's try: 3 from P=2, 2 from P=3: cost = 3^2*2 + 2^2*3 = 18+12=30 >20. 2 from P=2, 3 from P=3: 8+27=35 >20. 4 from P=2, 1 from P=3: 16+3=19 ≤20, count=5. Wait! 4 units from P=2: cost 4^2*2 = 32? No, 4^2=16, 16*2=32 >20. My mistake: 4 units from P=2: cost = (1^2+3^2+5^2+7^2)*2 = (1+9+25+49)*2 = 84*2=168? No, that's wrong. The cost of k units is k^2 * P. So 4 units from P=2: cost = 16*2=32. That's too high. So we cannot take 4 from P=2. So 3 from P=2 (cost 18) and 1 from P=3 (cost 3) gives 21 >20. 2 from P=2 (cost 8) and 2 from P=3 (cost 18) gives 26 >20. 1 from P=2 (cost 2) and 3 from P=3 (cost 27) >20. 3 from P=2 (18) and 0 from P=3: count 3. 2 from P=2 (8) and 1 from P=3 (3): count 3. 1 from P=2 (2) and 2 from P=3 (18): count 3. So max is 3? But algorithm says 4. Let's check: 4 units: 2 from P=2 and 2 from P=3? That cost 8+18=26 >20. 3 from P=2 and 1 from P=3: 18+3=21 >20. 4 from P=2: 32 >20. 1 from P=2 and 3 from P=3: 2+27=29 >20. So 4 units seems impossible. But algorithm gave cnt_less=4, sum_less=20. Those 4 items are: 2 (P=2), 3 (P=3), 6 (P=2), 9 (P=3). Their total cost is 2+3+6+9=20. So we can take those 4 items: that means we take 2 units from P=2 (cost 2 and 6) and 2 units from P=3 (cost 3 and 9). Total cost = (1^2+3^2)*2 + (1^2+3^2)*3 = (1+9)*2 + (1+9)*3 = 20 + 30 = 50? Wait, that's wrong! The cost of buying 2 units from P=2 is 2^2 * 2 = 8. But the sum of marginal costs is 2 + 6 = 8. So that's correct. For P=3, 2 units cost 2^2 * 3 = 12. Sum of marginal costs: 3 + 9 = 12. So total cost = 8 + 12 = 20. Yes! So we can buy 2 units from P=2 and 2 units from P=3, total cost 20, count 4. So answer=4 is correct. I earlier miscalculated the cost of 4 units. So algorithm works.

Thus the algorithm is correct and efficient.

Implementation details:
- sum(T) function: iterate over P, for each p, compute q = T // p, cnt = (q + 1) // 2, add p * cnt * cnt to total. Use Python integers.
- cnt(T) function: same but only count.
- g(T) function: iterate over P, if T % p == 0 and (T // p) % 2 == 1, count++.

We need to be careful with the binary search: the condition is sum(T) > M. We can use a while loop to find the smallest T with sum(T) > M.

Potential overflow: sum(T) can be huge. For T up to 2e18, cnt can be up to T // min(P) ≈ 2e18, cnt^2 up to 4e36, times P up to 2e9 gives 8e45. Python handles big integers, but the loop will be slow if numbers are huge? Actually the operations are just integer multiplications. Python big integers are slower for large numbers, but here the numbers are not that huge: cnt is at most T // min(P). min(P) could be 1, so cnt up to 2e18. cnt^2 is 4e36. Multiplying by P (up to 2e9) gives 8e45. That's a 46-digit number. Python can handle that, but multiplication of large numbers is slower. However, 2e5 such multiplications per iteration, 60 iterations, might be slow due to big integer arithmetic? Let's estimate: 8e45 is a large integer, but Python's Karatsuba or similar can multiply it in maybe a few microseconds. 12 million multiplications of 45-digit numbers might be a few seconds. But we can optimize: we can compute cnt^2 as (cnt * cnt) and multiply by p. Since cnt is up to 2e18, cnt^2 is up to 4e36, which fits in 128 bits? Actually 2e18 squared is 4e36, which is about 120 bits. Python uses arbitrary precision, but it's still fast.

Alternatively, we can avoid the large numbers by noting that sum(T) is monotonic and we only need to compare to M (1e18). We can cap the sum at something > M to avoid huge numbers. Since we only need to know if sum(T) > M, we can stop early if sum exceeds M. That will cut time for large T.

Implementation of sum(T):
def total_cost(T):
    total = 0
    for p in P:
        q = T // p
        cnt = (q + 1) // 2
        total += p * cnt * cnt
        if total > M:  # early exit
            return total
    return total

This early exit will make the binary search fast because for large T, sum(T) quickly exceeds M.

Similarly, for the final pass, we need exact sum_less, which is ≤ M, so it's not huge (≤ 1e18). So that pass is fast.

Thus the algorithm is efficient.

Now we need to implement solve() accordingly.

Edge Cases:
- If T_star = 0? Not possible.
- If T_star is such that T_star - 1 < 0? T_star is at least 1.
- If M = 0, we cannot buy anything, answer 0. The algorithm: binary search for T_star: sum(0) = 0 ≤ 0, sum(1) > 0? Actually sum(1) might be 0 if all P_i > 1. For P_i ≥ 1, sum(1) could be 0. We need to ensure the binary search works. We'll set low=0, high=some large number. We'll find smallest T with sum(T) > M=0. Since sum(0)=0 not >0, we need to find T where sum(T) > 0. The first T with sum(T) > 0 is the smallest P_i. So T_star = min P_i. Then T_star - 1: cnt_less = 0, sum_less = 0. g_T_star = number of i with T_star % p == 0 and (T_star // p) odd. Since T_star = min P_i, for that product, T_star // p = 1 (odd), so g=1. remaining = 0. take = 0. answer = 0. So correct.

- If we can take all items with cost ≤ T_star (i.e., sum(T_star) ≤ M), then T_star would be larger. But by definition T_star is the first with sum > M, so sum(T_star-1) ≤ M. So we are good.

- If sum(T_star-1) = M exactly, then remaining = 0, take = 0, answer = cnt(T_star-1). That is correct.

- If g(T_star) = 0 (i.e., T_star is not a marginal cost), then we cannot take any item of that cost, answer = cnt_less. But T_star is defined as the smallest integer with sum(T) > M. It could be that T_star is not an actual marginal cost. In that case, g(T_star) = 0. But then the answer is just cnt_less. However, is it possible that T_star is not a marginal cost? Let's think: sum(T) is a step function that increases only at values that are marginal costs? Actually sum(T) increases when T crosses a marginal cost. If T_star is not a marginal cost, then sum(T_star) = sum(T_star-1) (since no new items). But sum(T_star) > M and sum(T_star-1) ≤ M. So if T_star is not a marginal cost, then sum(T_star-1) = sum(T_star) > M, contradiction. Therefore T_star must be a marginal cost. So g(T_star) ≥ 1. Good.

Thus the algorithm is sound.

Now we need to implement in Python with fast I/O.

We should read N, M, then list P. Use sys.stdin.buffer.

Binary search range: low = 0, high = 2 * 10**18 + 1? Actually we can set high = 2 * 10**18 (2e18) because M ≤ 1e18, and we argued T ≤ M is enough? But T could be larger than M if the first marginal cost is larger than M. For example, M=1, P_i=10. Then min P_i = 10 > M. T_star will be 10, which is > M. So we need high to be at least max P_i. Since max P_i ≤ 2e9, 2e18 is way larger. So high = 2 * 10**18 is safe. Actually we can set high = 4 * 10**18 to be safe. But 2e18 is enough because the maximum T we need to consider is when we take all possible items? The maximum number of items is sum_i sqrt(M/P_i). The marginal cost of the last item taken is at most M (since total cost ≤ M, the last item cost ≤ M). So T ≤ M. However, if M is very small, say M=1, and P_i=10, then we cannot take any item. The first marginal cost is 10. T_star = 10. 10 > M. So T can be larger than M. But is it possible that T_star > M? Yes, if the cheapest item costs more than M, we cannot buy anything, T_star = min P_i, which could be > M. So we need high to be at least max P_i (or maybe min P_i). Actually we need high such that sum(high) > M. Since sum(high) grows quadratically, for high = max P_i (2e9), sum(high) is at least (high // min P_i + 1)//2 squared times min P_i? Not sure. But we can just set high = 2 * 10**18 to be safe.

We can also compute a high bound: Let max_possible_units = sum_i floor(sqrt(M / P_i)) + N (maybe). The marginal cost of a unit from product i is at most (2 * max_possible_units_i - 1) * P_i. But that's messy. Simpler: set high = 2 * 10**18. 60 iterations is fine.

Now we need to ensure the binary search terminates. We can use:
low = 0
high = 1
while total_cost(high) <= M:
    high *= 2
But this could be slow if high needs to double many times. But we can just set high to a large constant. To be safe, we can set high = 2 * 10**18. Since total_cost(high) will be > M (because for large T, sum(T) ~ T^2 * sum 1/P_i / 4, which grows), we can just set high = 2 * 10**18. However, we need to be sure that total_cost(high) > M. Let's check worst case: sum 1/P_i is minimal when all P_i are large. max P_i = 2e9, N=2e5, sum 1/P_i ≥ N / max P_i = 2e5 / 2e9 = 1e-4. Then sum(T) ~ T^2 * 1e-4 / 4 = 2.5e-5 T^2. For T=2e18, T^2 = 4e36, times 2.5e-5 = 1e32, which is > 1e18. So yes, sum(high) > M. So high = 2e18 is safe.

But we need to be careful with integer overflow in the loop: p * cnt * cnt might be huge (up to 8e45). That's fine for Python.

We can also reduce high by computing an upper bound: The maximum T needed is when we consider all items. The maximum marginal cost for product i is unbounded, but we only need up to the point where sum(T) > M. Since sum(T) is monotone, we can set high = max(1, M) * 2? Not safe.

Thus set high = 2 * 10**18.

Now implement:

def solve():
    import sys
    input_data = sys.stdin.buffer.read().split()
    it = iter(input_data)
    N = int(next(it))
    M = int(next(it))
    P = [int(next(it)) for _ in range(N)]

    # Binary search for smallest T with sum(T) > M
    low = 0
    high = 2 * 10**18  # safe upper bound

    def total_cost(T):
        total = 0
        # local variables for speed
        plist = P
        m = M
        for p in plist:
            q = T // p
            cnt = (q + 1) // 2
            # use Python's big int, but we can compute cnt*cnt
            total += p * cnt * cnt
            if total > m:
                # early exit
                return total
        return total

    # Ensure high is sufficient
    # We can while total_cost(high) <= M: high *= 2
    # but that might be slow. We'll trust 2e18.
    # To be safe, we can do a quick check and expand if needed.
    # However, for simplicity, we can set high = 2e18 and rely on it.
    # But if M is huge and P are huge, maybe high is not enough? Let's test: P_i=2e9, M=1e18. min P_i = 2e9. T_star could be 2e9. high=2e18 is enough. So fine.
    # If P_i are small, sum(T) grows fast, so high is enough.
    # So we can proceed.

    while low < high:
        mid = (low + high) // 2
        if total_cost(mid) > M:
            high = mid
        else:
            low = mid + 1
    T_star = low  # smallest T with sum(T) > M

    # Compute cnt_less, sum_less for T = T_star - 1
    T_less = T_star - 1
    cnt_less = 0
    sum_less = 0
    g_T = 0
    for p in P:
        q = T_less // p
        cnt = (q + 1) // 2
        cnt_less += cnt
        sum_less += p * cnt * cnt
        # compute g(T_star)
        # we can compute in the same loop or separate
    # Now compute g(T_star)
    for p in P:
        if T_star % p == 0:
            if (T_star // p) % 2 == 1:
                g_T += 1

    remaining = M - sum_less
    # remaining // T_star, but careful: if T_star == 0? Not possible.
    # But if T_star is huge and remaining is small, remaining // T_star = 0.
    # If T_star > 0:
    take = 0
    if T_star > 0:
        take = min(g_T, remaining // T_star)
    answer = cnt_less + take

    print(answer)

We need to ensure the early exit in total_cost doesn't break the binary search. It returns a value > M, which is correct. The binary search condition is total_cost(mid) > M. So we can use the early exit.

Potential issue: In the final pass, sum_less might exceed M? No, by definition sum_less = f(T_star-1) ≤ M. So it's fine.

We need to be careful with the case where T_star = 0. But T_star is at least 1 because sum(0) = 0 ≤ M (unless M < 0, impossible). So T_star >= 1.

We also need to consider the case where we can take all items with cost ≤ T_star (i.e., sum(T_star) ≤ M). But by definition T_star is the first with sum > M, so sum(T_star) > M. So we are good.

One more check: What if after taking all items with cost < T_star, we have remaining >= T_star, and g_T > 0, we can take some. That's handled.

What if T_star is such that there are no items with cost < T_star? That is, T_star is the smallest marginal cost. Then T_less = T_star - 1, cnt_less = 0, sum_less = 0. g_T >= 1. remaining = M. take = min(g_T, M // T_star). This is correct: we can buy as many of the cheapest items as possible.

Thus the algorithm is correct.

Complexities: O(N log M) for binary search, plus O(N) for final computation. With N=2e5, log M ≈ 60, total ~12 million loops. Each loop does a few integer divisions and multiplications. This should run in under 1 second in PyPy or CPython? 12 million iterations might be around 0.5-1 second. The final two loops are 2 * 2e5 = 4e5, negligible.

We need to be careful with the early exit in total_cost: it returns early if total > M. In the binary search, we call total_cost(mid) many times. For large mid, the sum quickly exceeds M, so the loop breaks early. This reduces the average number of iterations per call. For small mid, the loop runs fully. But total number of loop iterations across all binary search steps is at most N * log M, but often less.

Thus it's efficient.

Now we need to write the final code with proper structure.

Let's test with the sample inputs.

Sample 1:
N=3, M=9, P=[4,1,9]
Binary search:
T=0: sum=0.
T=1e18: sum huge >9.
We need to find T_star.
Let's compute manually: T_star=5 as before.
Our code will find it.
Then T_less=4, cnt_less=3, sum_less=8, g_T=1, remaining=1, take=0, answer=3. Good.

Sample 2:
N=10, M=1000, P=[2,15,6,5,12,1,7,9,17,2]
We can trust the algorithm.

We should also test edge cases:
- N=1, P=1, M=0. Expect 0.
  total_cost(0)=0 <=0.
  total_cost(1): q=1//1=1, cnt=(1+1)//2=1, total=1*1*1=1 >0. So T_star=1.
  T_less=0, cnt_less=0, sum_less=0. g_T: T_star=1, p=1, 1%1=0, (1//1)=1 odd, g=1. remaining=0. take=0. answer=0. Good.

- N=1, P=1, M=1.
  total_cost(0)=0 <=1.
  total_cost(1)=1 >1? 1 > 1 is False. So T_star > 1.
  total_cost(2): q=2//1=2, cnt=(2+1)//2=1, total=1. 1 <= 1. So T_star > 2.
  total_cost(3): q=3, cnt=(3+1)//2=2, total=1*4=4 >1. So T_star=3.
  T_less=2, cnt_less = (2+1)//2 = 1. sum_less = 1*1^2 = 1. g_T: T_star=3, p=1, 3%1=0, (3//1)=3 odd, g=1. remaining = 1 - 1 = 0. take=0. answer=1. Is that correct? With P=1, M=1, we can buy 1 unit (cost 1). We cannot buy 2 units (cost 4). So answer=1. Good.

- N=1, P=1, M=3.
  total_cost(0)=0.
  total_cost(1)=1 <=3.
  total_cost(2)=1 <=3.
  total_cost(3)=4 >3. So T_star=3.
  T_less=2, cnt_less=1, sum_less=1. g_T=1. remaining=2. 2//3=0. take=0. answer=1. But we can buy 1 unit (cost 1) and have 2 left, but the next unit costs 3, which we cannot afford. So max is 1. Correct.

- N=1, P=1, M=4.
  total_cost(0)=0.
  total_cost(1)=1 <=4.
  total_cost(2)=1 <=4.
  total_cost(3)=4 <=4. So T_star > 3.
  total_cost(4): q=4, cnt=(4+1)//2=2, total=1*4=4 <=4. So T_star > 4.
  total_cost(5): q=5, cnt=3, total=9 >4. So T_star=5.
  T_less=4, cnt_less=2, sum_less=4. g_T=1. remaining=0. take=0. answer=2. We can buy 2 units (cost 1+3=4). Correct.

- N=1, P=2, M=8.
  Marginal costs: 2,6,10,...
  total_cost(0)=0.
  total_cost(1)=0.
  total_cost(2): q=1, cnt=1, total=2*1=2 <=8.
  total_cost(3): same 2.
  total_cost(4): same 2.
  total_cost(5): same 2.
  total_cost(6): q=3, cnt=2, total=2*4=8 <=8.
  total_cost(7): same 8.
  total_cost(8): same 8.
  total_cost(9): same 8.
  total_cost(10): q=5, cnt=3, total=2*9=18 >8. So T_star=10.
  T_less=9, cnt_less = (9//2 + 1)//2 = (4+1)//2 = 2. sum_less = 2*4 = 8. g_T: T_star=10, p=2, 10%2=0, 10//2=5 odd, g=1. remaining=0. take=0. answer=2. We can buy 2 units (cost 2+6=8). Correct.

- N=1, P=2, M=9.
  total_cost(10)=18 >9, so T_star=10.
  T_less=9, cnt_less=2, sum_less=8. remaining=1. 1//10=0. answer=2. We cannot buy 3 units (cost 2+6+10=

## worker: Implement the algorithm in Python: binary search o
We solved the problem by recognizing that the optimal strategy is to buy units in increasing order of marginal cost \((2\ell-1)P_i\). The answer is the largest \(K\) such that the sum of the \(K\) smallest marginal costs does not exceed \(M\).

For a threshold \(T\), the number of marginal costs \(\le T\) is  
\(\displaystyle cnt(T)=\sum_i \left\lfloor \frac{T//P_i+1}{2}\right\rfloor\)  
and their total cost is  
\(\displaystyle sum(T)=\sum_i P_i\cdot cnt_i(T)^2\)  
because the sum of the first \(t\) odd numbers is \(t^2\).

We binary‑search the smallest integer \(T^*\) with \(sum(T^*)>M\).  
Then we can afford all items with cost \(<T^*\) (cost \(sum(T^*-1)\), count \(cnt(T^*-1)\)) and as many items of cost exactly \(T^*\) as the remaining budget allows.  
The number of items with cost \(T^*\) is \(g(T^*)=\sum_i [\,T^*\bmod P_i=0 \text{ and } (T^*/P_i)\text{ odd}\,]\).

The final answer is \(cnt(T^*-1) + \min\bigl(g(T^*),\ \lfloor (M-sum(T^*-1))/T^* \rfloor\bigr)\).

The binary search runs in \(O(N\log M)\) (≈ 60 · 2·10⁵ operations) and the final computation is \(O(N)\), easily fast enough in Python.
