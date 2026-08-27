
## ideation
The core difficulty is efficiently computing the sum of "division depths" for all numbers in a large range $[l, r]$ where $r$ can be up to $10^9$. A brute-force approach is impossible due to the range size.

The key insight is that the number of divisions by 4 needed to reduce a number $x$ to 0, denoted $d(x)$, is constant for ranges of the form $[4^{k-1}, 4^k - 1]$. Specifically, $d(x) = k$ for $x$ in that range.

We can define a helper function `count_ops(n)` that computes $\sum_{x=1}^{n} d(x)$. This can be done by iterating through powers of 4. For each power $4^k$, we determine how many numbers in $[1, n]$ fall into the bucket where $d(x) = k+1$ (i.e., $[4^k, 4^{k+1}-1]$). The contribution to the sum is the count of such numbers multiplied by $k+1$.

The algorithm for `count_ops(n)`:
1. Initialize `total = 0` and `power = 1` (which is $4^0$).
2. Let `k = 0`.
3. While `power <= n`:
   - The next power is `next_power = power * 4`.
   - The numbers with depth `k+1` are in the range `[power, min(n, next_power - 1)]`.
   - The count of such numbers is `max(0, min(n, next_power - 1) - power + 1)`.
   - Add `count * (k + 1)` to `total`.
   - Update `power = next_power` and `k += 1`.
4. Return `total`.

For each query $[l, r]$, the total depth sum is `count_ops(r) - count_ops(l-1)`. The minimum operations is $\lceil \text{sum} / 2 \rceil$, which can be computed as `(sum + 1) // 2` using integer arithmetic.

Pitfalls to avoid:
- Off-by-one errors in range calculations.
- Integer overflow when computing powers of 4 (though Python handles large integers automatically, the loop condition `power <= n` ensures we don't iterate unnecessarily).
- Forgetting that $d(0)=0$, so `count_ops(0)` should return 0. The logic naturally handles this because if $n=0$, the loop `power <= n` (1 <= 0) is false, returning 0.

## worker: (None)
The solution relies on the observation that for any number $x$, the number of times it needs to be divided by 4 (floor) to become 0 is $d(x) = \lfloor \log_4(x) \rfloor + 1$ for $x \ge 1$. This value $d(x)$ is constant for ranges $[4^{k-1}, 4^k - 1]$ where $d(x) = k$.

To compute the sum of $d(x)$ for $x$ in $[l, r]$ efficiently, we define a helper function `count_ops(n)` that computes $\sum_{x=1}^{n} d(x)$. This is done by iterating through powers of 4. For each power $4^k$, we calculate how many numbers in $[1, n]$ fall into the interval $[4^k, 4^{k+1}-1]$ (which have depth $k+1$) and add `count * (k+1)` to the total.

For each query $[l, r]$, the total depth sum is `count_ops(r) - count_ops(l-1)`. Since one operation reduces two numbers (each by one "depth unit"), the minimum number of operations is $\lceil \text{total\_depth} / 2 \rceil$, which is computed as `(total_depth + 1) // 2` using integer arithmetic.

The time complexity per query is $O(\log_4(\max(r))) = O(\log(\max(r)))$, which is very efficient given $\max(r) \le 10^9$. The overall time complexity is $O(Q \log(\max(r)))$ where $Q$ is the number of queries.
