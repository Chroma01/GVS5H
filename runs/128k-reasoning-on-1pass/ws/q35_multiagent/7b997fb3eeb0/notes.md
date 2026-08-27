
## ideation
The problem asks for the maximum number of pairs $(a, b)$ that can be formed from a subarray $A[L \dots R]$ such that $a \le b/2$. Since the array $A$ is sorted, the optimal strategy to maximize the number of pairs is to pick the smallest available elements as the tops ($a$) and the largest available elements as the bottoms ($b$). Specifically, for a target number of pairs $K$, we should pair the $K$ smallest elements in the range with the $K$ largest elements in the range.

Let the range be indices $[L, R]$ (1-based). The $K$ smallest elements are at indices $L, L+1, \dots, L+K-1$. The $K$ largest elements are at indices $R-K+1, \dots, R$. We pair the $i$-th smallest with the $i$-th largest (sorted order), i.e., $A[L+i-1]$ with $A[R-K+i]$. The condition is $2 A[L+i-1] \le A[R-K+i]$ for all $1 \le i \le K$.

This condition can be rewritten in terms of the shift $S = (R-L+1) - K$. We need $2 A[p] \le A[p+S]$ for all $p \in [L, L+K-1]$. This is equivalent to finding the smallest index $j > p$ such that $A[j] \ge 2 A[p]$, let's call it $next[p]$. The condition becomes $next[p] \le p+S$, or $next[p] - p \le S$. Let $val[p] = next[p] - p$. We need $\max_{p \in [L, L+K-1]} val[p] \le S$. Substituting $S$, we get $K + \max_{p \in [L, L+K-1]} val[p] \le R - L + 1$.

We can precompute $val[p]$ for all $p$ using a two-pointer approach in $O(N)$ since $A$ is sorted. Then, for each query, we can binary search for the maximum $K$. The check involves a range maximum query on the $val$ array, which can be done in $O(1)$ using a Sparse Table. The total complexity will be $O(N \log N + Q \log N)$.

## worker: (none)
The problem asks for the maximum number of pairs $(a, b)$ such that $a \le b/2$ from a subarray $A[L \dots R]$. Since $A$ is sorted, the optimal strategy to maximize pairs is to pair the smallest available elements with the largest available elements. Specifically, for a target number of pairs $K$, we pair the $K$ smallest elements in the range with the $K$ largest elements.

Let the range be indices $[l, r]$ (0-indexed). The $K$ smallest elements are at indices $l, l+1, \dots, l+K-1$. The $K$ largest elements are at indices $r-K+1, \dots, r$. We pair $A[l+i]$ with $A[r-K+i]$ for $i=0, \dots, K-1$. The condition is $2 A[l+i] \le A[r-K+i]$.

Let $p = l+i$. Then $p$ ranges from $l$ to $l+K-1$. The condition becomes $2 A[p] \le A[p + (r-l+1) - K]$. Let $S = r-l+1$ and $shift = S - K$. The condition is $2 A[p] \le A[p+shift]$, which is equivalent to $p+shift \ge next[p]$, where $next[p]$ is the smallest index $j$ such that $A[j] \ge 2 A[p]$. This gives $shift \ge next[p] - p$. Let $val[p] = next[p] - p$. We need $shift \ge \max_{p \in [l, l+K-1]} val[p]$. Substituting $shift = S - K$, we get $S - K \ge \max val$, or $K + \max val \le S$.

We precompute $val[p]$ for all $p$ using a two-pointer approach in $O(N)$. Then we build a Sparse Table for range maximum queries on $val$ in $O(N \log N)$. For each query, we binary search for the maximum $K$ in $[0, S//2]$ and check the condition in $O(1)$ using the Sparse Table. The total complexity is $O(N \log N + Q \log N)$.
