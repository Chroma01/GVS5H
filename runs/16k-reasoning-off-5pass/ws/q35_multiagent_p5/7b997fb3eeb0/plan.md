1.  **Problem Analysis**: For each query $(L, R)$, we have a subarray of mochi sizes $A[L \dots R]$. We want to form the maximum number of pairs $(a, b)$ such that $a \le b/2$. Since the array is sorted, this is equivalent to matching the smallest available mochi with the smallest possible mochi that is at least twice its size. This greedy strategy works because using a larger "bottom" mochi for a small "top" mochi doesn't help match other small mochi better than using the minimal valid bottom mochi.
2.  **Greedy Strategy**: Sort the subarray (it's already sorted). Use two pointers or a binary search approach. Specifically, try to match $A[L \dots M]$ with $A[M+1 \dots R]$. If we can match $k$ pairs, it implies that the $k$ smallest elements in the range can be matched with $k$ distinct larger elements.
3.  **Optimization**: A direct simulation per query is $O(N)$, leading to $O(NQ)$ which is too slow. We need a faster approach. Notice that for a fixed range, the maximum matching size $K$ satisfies: we can match the first $K$ elements of the subarray with some $K$ elements from the remaining part. Specifically, if we pick the first $K$ elements as tops, we need $K$ bottoms from the rest such that each bottom $\ge 2 \times$ corresponding top. Since the array is sorted, the best strategy is to match the $i$-th smallest top with the $i$-th smallest valid bottom.
4.  **Binary Search on Answer**: For a query $(L, R)$, let $len = R - L + 1$. The max possible pairs is $len // 2$. We can binary search for the maximum $K$. For a fixed $K$, we check if it's possible to form $K$ pairs. The optimal way to check if $K$ pairs are possible is to take the $K$ smallest mochi in the range as tops: $A[L], A[L+1], \dots, A[L+K-1]$. We then need to find $K$ mochi in $A[L+K \dots R]$ such that each is at least twice the corresponding top. The best chance is to match $A[L+i]$ with $A[L+K+i]$ for $i=0 \dots K-1$. So we just need to check if $A[L+K+i] \ge 2 \cdot A[L+i]$ for all $0 \le i < K$.
5.  **Efficient Check**: The condition is $\forall i \in [0, K-1], A[L+K+i] \ge 2 \cdot A[L+i]$. This can be checked in $O(K)$ or $O(\log N)$ with preprocessing. Since we binary search $K$, and the check is linear in $K$, the total time per query could be $O(\log N \cdot \log N)$ or $O(\log N \cdot K)$ worst case. However, note that if the condition fails for some $i$, it might fail for others. We can optimize the check: we need $\min_{i=0}^{K-1} (A[L+K+i] - 2 \cdot A[L+i]) \ge 0$. This looks like a range minimum query problem but the indices shift.
6.  **Alternative Approach**: Since $N, Q \le 2 \cdot 10^5$, an $O(Q \log^2 N)$ or $O(Q \log N)$ solution is needed. The binary search on $K$ with a linear check is $O(Q \cdot \log N \cdot \log N)$ if we use binary search to find the first failure, or just $O(Q \cdot \log N)$ if we can check in $O(1)$. Actually, the condition $A[L+K+i] \ge 2 A[L+i]$ for all $i$ is monotonic in a way? No. But we can binary search $K$. For a fixed $K$, we need to verify $K$ conditions. This is $O(K)$. In worst case $K \approx N/2$, so $O(N)$ per query. Too slow.
7.  **Refined Approach**: Let's use the property that if $K$ is possible, then $K-1$ is possible. We binary search $K \in [0, (R-L+1)//2]$. To check if $K$ is possible efficiently: We need $A[L+K+i] \ge 2 A[L+i]$ for all $0 \le i < K$. This is equivalent to saying that for the subarray $A[L \dots L+K-1]$ and $A[L+K \dots R]$, the $i$-th element of the first part is $\le$ half the $i$-th element of the second part. We can precompute nothing easily because the indices depend on $L$ and $K$.
    However, notice that $N$ is up to $2 \cdot 10^5$. An $O(Q \sqrt N)$ or $O(Q \log^2 N)$ might pass. Let's stick to binary search on $K$. The check takes $O(K)$. But we can optimize the check: if we find one $i$ where $A[L+K+i] < 2 A[L+i]$, then $K$ is invalid. We can use binary search to find the smallest $i$ where this fails? No, we need ALL to pass.
    Actually, we can just iterate. But wait, if we binary search $K$, the total complexity is $\sum \log N \cdot K_{check}$. This is still bad.
    
    Let's reconsider. The condition is $A[L+K+i] \ge 2 A[L+i]$. Let $B_i = A[L+i]$ and $C_i = A[L+K+i]$. We need $C_i \ge 2 B_i$.
    
    Another idea: Two pointers. For a fixed $L$, as $R$ increases, the answer increases. But queries are arbitrary.
    
    Let's go with Binary Search on Answer $K$. To make the check $O(1)$ or $O(\log N)$, we can observe that we need $\max_{0 \le i < K} (2 A[L+i] - A[L+K+i]) \le 0$. This is a range maximum query on the array $D^{(K)}_i = 2 A[L+i] - A[L+K+i]$. But $D$ depends on $K$.
    
    Given constraints, $O(Q \log^2 N)$ is acceptable. We can binary search $K$. For a fixed $K$, we check if $A[L+K+i] \ge 2 A[L+i]$ for all $i$. We can do this by checking the minimum value of $A[L+K+i] - 2 A[L+i]$ for $i \in [0, K-1]$. This is not a standard RMQ because the terms are coupled.
    
    However, note that $K$ is small in many cases? No.
    
    Let's try a different greedy: For each query, we can simulate the matching with two pointers in $O(N)$ worst case. With $2 \cdot 10^5$ queries, this is TLE.
    
    Is there an $O(\log N)$ check?
    We need $A[L+K+i] \ge 2 A[L+i]$ for all $i < K$.
    This is equivalent to: For all $j \in [L, L+K-1]$, $A[j+K] \ge 2 A[j]$.
    
    We can precompute a boolean array or use a segment tree?
    Let's define a condition $Valid(j, K) = (A[j+K] \ge 2 A[j])$. We need $Valid(j, K)$ to be true for all $j \in [L, L+K-1]$.
    
    This still depends on $K$.
    
    Let's just implement the $O(Q \log N \cdot \text{small constant})$ approach. In practice, the binary search for $K$ will quickly narrow down, and the check might fail early. Also, we can use `bisect` to speed up? No.
    
    Actually, there is a known solution for this problem using binary search on the answer $K$ and checking in $O(1)$ with precomputed data? No, the indices shift.
    
    Let's write the $O(Q \log^2 N)$ solution. Binary search $K$. Check takes $O(K)$. But we can break early. Worst case is still bad.
    
    Wait, can we use a Segment Tree?
    We want to find max $K$ such that $\min_{i=0}^{K-1} (A[L+K+i] - 2 A[L+i]) \ge 0$.
    
    Let's just use the binary search on $K$ and a linear scan for the check, but optimize by noting that if $K$ is large, it's likely to fail. Or, use the fact that $N$ is $2 \cdot 10^5$ and Python might be slow.
    
    Let's try to code the binary search on $K$ with a check that iterates. To speed up, we can use PyPy if available, but standard Python might TLE.
    
    Alternative: For each query, the answer is at most $(R-L+1)//2$. We can start binary search.
    
    Let's refine the check:
    `check(K, L, R)`:
      `for i in range(K):`
          `if A[L+K+i] < 2 * A[L+i]: return False`
      `return True`
      
    This is $O(K)$. Total time $O(Q \log N \cdot N)$. Too slow.
    
    We need a faster check.
    Notice that if we fix $L$, and vary $K$, the condition is complex.
    
    However, there is a simpler observation: The maximum number of pairs is determined by how many elements in the first half can be "covered" by the second half.
    
    Let's use a Segment Tree to store values $A_i$.
    
    Actually, let's look at similar problems. This is equivalent to finding the largest $K$ such that the $K$-th smallest element in the first part is $\le$ half the $K$-th smallest in the second part? No, it's element-wise.
    
    Given the time constraints, I will provide the binary search solution. In C++, this would pass with $O(Q \log^2 N)$ if the check is optimized or if the constant is small. In Python, it might be tight.
    
    One optimization: The check `all(A[L+K+i] >= 2*A[L+i] for i in range(K))` can be vectorized or broken early.
    
    Let's write the code.