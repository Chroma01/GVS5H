
## ideation
The core difficulty is answering $Q$ queries efficiently, where each query asks for the maximum number of pairs $(a, b)$ from a subarray $A[L..R]$ such that $a \le b/2$. A naive $O(N)$ per query solution leads to $O(NQ)$ total time, which is too slow for $N, Q \le 2 \cdot 10^5$.

Key observations:
1. **Greedy Strategy**: For a sorted subarray, the optimal strategy to maximize pairs is to split the subarray into a left half $[L, mid]$ and a right half $[mid+1, R]$ (where $mid = (L+R)//2$). We then greedily match the smallest available elements from the left half with the smallest valid elements from the right half.
2. **Binary Search on Answer**: The maximum number of pairs $K$ is monotonic. If we can form $K$ pairs, we can form $K-1$. We can binary search for the largest $K$ in the range $[0, \min(mid-L+1, R-mid)]$.
3. **Check Function**: To check if $K$ pairs are possible, we need to verify if the $K$ smallest elements from the left half can be matched with the $K$ smallest valid elements from the right half. Due to sorting, this is equivalent to checking if $A[L+i] \le A[mid+1+i]/2$ for all $0 \le i < K$.
4. **Efficient Check**: The condition $A[L+i] \le A[mid+1+i]/2$ for all $i \in [0, K-1]$ is equivalent to finding the first index $i$ where $A[mid+1+i] < 2 A[L+i]$. If no such $i$ exists up to the limit, then $K$ is valid. We can binary search for this first failure index.
5. **Optimization**: Instead of precomputing complex structures, we can use the fact that for a fixed query, the offset $D = mid+1-L$ is constant. We need to find the smallest $j \in [L, mid]$ such that $A[j+D] < 2 A[j]$. This can be done by binary searching for $j$ and checking the condition. However, checking the condition for a range requires scanning or a data structure. Given the constraints and Python's speed, a direct binary search for the answer $K$ with an $O(1)$ check using a precomputed structure is ideal, but hard to implement simply.
   Alternatively, we can observe that the number of pairs is limited by the length of the smaller half. We can binary search $K$ and for each $K$, check the condition $A[L+i] \le A[mid+1+i]/2$ for all $i$. To make the check $O(1)$, we would need a Range Minimum Query on the array $B[i] = A[i+D] - 2A[i]$, but $D$ varies.
   
   A simpler efficient approach in Python:
   Use the two-pointer greedy simulation but optimize with `bisect`. For each element in the left half, find the first valid element in the right half. This is $O(N \log N)$ per query worst case, which might TLE.
   
   However, note that the constraints allow $O(Q \sqrt N)$ or $O(Q \log^2 N)$.
   Let's use the binary search on $K$ approach. For a fixed $K$, we check if $\min_{i=0}^{K-1} (A[mid+1+i] - 2 A[L+i]) \ge 0$.
   We can precompute a Sparse Table for Range Minimum Queries on the array $A$. But the term $A[mid+1+i] - 2 A[L+i]$ is not static.
   
   Given the time constraints of coding, I will implement the $O(N)$ per query solution with a small optimization: since the array is sorted, we can use `bisect` to skip elements. But worst case is still bad.
   
   Actually, there is a known result: the answer is the largest $K$ such that $A[L+K-1] \le A[R-K+1]/2$ is NOT generally true.
   
   Let's stick to the binary search on $K$ with a linear check. In Python, this might be too slow. But let's try to optimize the check.
   The check for $K$ is: for all $i \in [0, K-1]$, $A[mid+1+i] \ge 2 A[L+i]$.
   We can binary search for the first $i$ where this fails.
   Let $f(i) = (A[mid+1+i] \ge 2 A[L+i])$. This is a boolean array that is True for small $i$ and becomes False at some point. We want to find the first False.
   We can binary search for this index $i$ in the range $[0, \min(mid-L+1, R-mid)-1]$.
   The check for a specific $i$ is $O(1)$. So the binary search takes $O(\log N)$.
   Total time per query: $O(\log N)$.
   Total time: $O(Q \log N)$. This is efficient enough.

   Algorithm:
   For each query $(L, R)$:
   1. $mid = (L + R) // 2$
   2. $max\_k = \min(mid - L + 1, R - mid)$
   3. Binary search for the largest $K \in [0, max\_k]$ such that for all $i \in [0, K-1]$, $A[mid+1+i] \ge 2 A[L+i]$.
      This is equivalent to finding the smallest $i \in [0, max\_k-1]$ such that $A[mid+1+i] < 2 A[L+i]$. Let this be $i_{fail}$. Then $K = i_{fail}$. If no such $i$ exists, $K = max\_k$.
   4. To find $i_{fail}$, binary search in $[0, max\_k]$.
      Check if there exists $i \in [0, mid]$ such that $A[mid+1+i] < 2 A[L+i]$.
      We can binary search for the first such $i$.
      Let $low = 0, high = max\_k$.
      While $low < high$:
        $mid\_idx = (low + high) // 2$
        Check if $A[mid+1+mid\_idx] < 2 A[L+mid\_idx]$.
        If true, then the first failure is at or before $mid\_idx$, so $high = mid\_idx$.
        Else, the first failure is after $mid\_idx$, so $low = mid\_idx + 1$.
      Then $K = low$.

   This is $O(\log N)$ per query.

## worker: none
The problem asks for the maximum number of pairs $(a, b)$ from a subarray $A[L..R]$ such that $a \le b/2$. Since the array is sorted, the optimal greedy strategy is to split the subarray into a left half $[L, mid]$ and a right half $[mid+1, R]$ where $mid = (L+R)//2$. We then greedily match the smallest elements from the left half with the smallest valid elements from the right half.

The key insight is that if we want to form $K$ pairs, the best chance is to use the $K$ smallest elements from the left half and the $K$ smallest elements from the right half. Due to the sorted nature of the array, this is equivalent to checking if $A[L+i] \le A[mid+1+i]/2$ for all $0 \le i < K$.

This condition is monotonic: if it holds for $K$, it holds for $K-1$. Therefore, we can binary search for the largest valid $K$. The check for a specific $K$ involves verifying the condition for all $i \in [0, K-1]$. Instead of checking all $i$, we can binary search for the *first* index $i$ where the condition fails ($A[mid+1+i] < 2 A[L+i]$). If the first failure is at index $i_{fail}$, then the maximum number of pairs is $i_{fail}$. If no failure occurs within the valid range, the maximum number of pairs is the size of the smaller half.

This approach results in an $O(\log N)$ time complexity per query, leading to an overall time complexity of $O(Q \log N + N)$, which is efficient enough for the given constraints ($N, Q \le 2 \cdot 10^5$).
