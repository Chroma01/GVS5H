1.  **Analyze the Absorption Process**: Takahashi (slime K) can absorb adjacent slimes strictly smaller than his current size. This is equivalent to expanding a "connected component" of slimes that can be merged into Takahashi. The process stops when all adjacent slimes are $\ge$ Takahashi's current size.
2.  **Key Insight**: The final size of Takahashi is the sum of sizes of all slimes in the maximal contiguous segment containing index K that can be "absorbed". A slime $i$ can be absorbed if it is part of a chain of absorptions. Crucially, Takahashi can absorb a neighbor if that neighbor is smaller. After absorbing, his size increases, potentially allowing him to absorb larger neighbors. This looks like finding the range $[L, R]$ around $K$ such that all slimes in $[L, R]$ can be merged into $K$.
3.  **Monotonic Stack / Next Greater Element**: For each slime $i$, we want to find the largest range $[L_i, R_i]$ it can "cover" or be part of. However, the condition is dynamic. A better way to think about it: Takahashi at $K$ can absorb everything in a contiguous block if the "barriers" (slimes larger than the current accumulated size) are pushed out.
4.  **Alternative View**: Consider the structure of the array. The process is similar to merging elements in a segment tree or using a stack to find the "next greater element". Specifically, for a starting position $K$, Takahashi can expand left and right. He can absorb a sequence of slimes to the left if each is smaller than the current total. This is complex because the total grows.
5.  **Efficient Approach**: Notice that the final set of absorbed slimes for position $K$ forms a contiguous interval $[L, R]$ containing $K$. The condition for an interval $[L, R]$ to be fully absorbable by $K$ is that there exists an order of absorption. It turns out that Takahashi can absorb the entire interval $[L, R]$ if and only if for every sub-interval, the maximum element is not a barrier that cannot be crossed. Actually, a known result for this "slime absorption" problem is that the answer for $K$ is the sum of the segment $[L_K, R_K]$ where $L_K$ is the first index to the left of $K$ such that $A_{L_K} > A_K$ (or similar logic involving previous greater elements) and $R_K$ is the first index to the right. Wait, the sample shows $K=2$ (size 13) absorbs everything to sum 30. $13+4+2+3+2+6 = 30$. Why? Because 13 > 4, absorbs 4. Size 17. 17 > 2, absorbs 2. Size 19. 19 > 3, absorbs 3. Size 22. 22 > 2, absorbs 2. Size 24. 24 > 6, absorbs 6. Size 30.
6.  **Refined Insight**: The process allows Takahashi to absorb any adjacent slime smaller than his *current* size. This is equivalent to: Takahashi can absorb the entire connected component of slimes that are "reachable" via a path of strictly smaller slimes, but the threshold increases. This is exactly the problem of finding the range $[L, R]$ such that $A_K$ is the maximum in $[L, R]$? No, in Sample 1, $K=2$ has $A_2=13$. The max in the whole array is 13. So he absorbs everything. For $K=4$ ($A_4=3$), he absorbs right 2 (size 5), then left 2 (size 7), then right 6 (size 13). He stops because left is 13 (not strictly smaller than 13). So he absorbs $[3, 6]$? Indices 3,4,5,6 have values 2,3,2,6. Sum = 13. The boundaries are index 2 (value 13) and end of array. Index 2 is $\ge$ final size? No, the barrier is that he cannot absorb 13 because $13 \ngtr 13$.
7.  **Algorithm**: For each $K$, we want to find the largest interval $[L, R]$ containing $K$ such that $A_K$ can "dominate" the interval. This is equivalent to finding the nearest element to the left $L$ such that $A_L \ge A_K$? No, in Sample 1, $K=4$ ($A_4=3$). Left neighbor is 2 ($A_3=2 < 3$). He absorbs it. Then he faces 13 ($A_2=13$). He cannot absorb 13 immediately. But he might grow larger by absorbing right first. He absorbs right 2, then right 6. Size becomes $3+2+2+6=13$. Now he faces 13. Still cannot absorb. So the left boundary is determined by the first element $\ge$ the *final* size? This is circular.
8.  **Correct Logic**: This problem is equivalent to finding the sum of the "connected component" of $K$ in a graph where edges exist between adjacent slimes if one is smaller than the other? No.
    Let's use the property: The final size is the sum of a contiguous subarray $A[L..R]$ containing $K$. The condition is that $A[K]$ is the maximum in $A[L..R]$? No, $A_4=3$ is not max in $2,3,2,6$. Max is 6.
    Actually, the condition is that there is no "barrier" $B$ in $[L, R]$ such that $B$ is greater than the sum of all other elements in $[L, R]$? No.
    
    Let's look at the structure again. This is a classic problem. The answer for each $K$ is the sum of the segment $[L_K, R_K]$ where $L_K$ is the index of the previous greater or equal element and $R_K$ is the index of the next greater or equal element?
    For $K=4$ ($A_4=3$):
    Prev greater or equal: $A_2=13$ (index 2). So $L=3$?
    Next greater or equal: None? Or $A_?$? $A_6=6 > 3$. So $R=5$?
    Interval $[3, 5]$ is $2, 3, 2$. Sum = 7. But answer is 13.
    
    Let's re-read carefully. "Absorb adjacent strictly smaller".
    The key is that absorption order matters.
    
    **Standard Solution for this Problem**:
    This is equivalent to: For each $i$, find the largest interval $[L, R]$ containing $i$ such that $A_i$ is the **maximum** element in that interval? No.
    
    Actually, consider the "Next Greater Element" (NGE) and "Previous Greater Element" (PGE).
    For each $i$, let $L[i]$ be the index of the first element to the left that is $\ge A[i]$. Let $R[i]$ be the index of the first element to the right that is $\ge A[i]$.
    If we define the range $(L[i], R[i])$, does Takahashi absorb everything in this range?
    For $K=4$ ($A_4=3$):
    Left: $A_3=2 < 3$, $A_2=13 \ge 3$. So $L=2$.
    Right: $A_5=2 < 3$, $A_6=6 \ge 3$. So $R=6$.
    Range $(2, 6)$ is indices $3, 4, 5$. Values $2, 3, 2$. Sum = 7.
    But the answer is 13. The sample explanation says he absorbs index 6 (value 6) as well.
    Why? Because after absorbing 2 and 3, his size is $3+2+2=7$. $7 > 6$, so he absorbs 6.
    So the range expands!
    
    **Revised Insight**:
    The process continues until Takahashi is surrounded by slimes $\ge$ his current size.
    This is equivalent to finding the connected component of slimes that can be merged into $K$.
    This problem is known as "Slimes" on AtCoder (ABC 279 F? No, maybe a different one).
    
    Actually, there is a simpler characterization:
    The final size for $K$ is the sum of $A[j]$ for all $j$ in the range $[L, R]$ where $L$ and $R$ are determined by the "dominance" of $A[K]$.
    
    Let's use a **Stack-based approach** to compute the answer for all $K$ efficiently.
    We can process the array and maintain a stack of "active" segments.
    
    Alternatively, note that the final configuration for any starting point $K$ will result in a size equal to the sum of a contiguous subarray. Which subarray?
    It is the subarray $[L, R]$ such that $A[L-1] \ge \text{Sum}(L, R)$ and $A[R+1] \ge \text{Sum}(L, R)$?
    In Sample 1, $K=4$, Sum=13. Left neighbor $A_2=13 \ge 13$. Right neighbor is end of array.
    $K=2$, Sum=30. Left neighbor none. Right neighbor none.
    $K=1$, Sum=4. Right neighbor $A_2=13 \ge 4$.
    $K=3$, Sum=2. Left $A_2=13 \ge 2$. Right $A_4=3 \ge 2$.
    
    Hypothesis: The answer for $K$ is the sum of the maximal contiguous subarray $[L, R]$ containing $K$ such that for all $j \in [L, R]$, $A[j]$ is "absorbable".
    Actually, the condition is: The sum of the subarray $S = \sum_{j=L}^R A[j]$ must be less than or equal to the neighbors $A[L-1]$ and $A[R+1]$ (if they exist) to stop?
    No, in $K=4$, Sum=13. Left neighbor is 13. $13 \ge 13$ stops absorption.
    
    So, for each $K$, we want to find the largest interval $[L, R]$ containing $K$ such that:
    1. The internal structure allows merging (which is always true if we merge from smallest to largest? No).
    2. The boundaries $A[L-1]$ and $A[R+1]$ are $\ge$ the total sum of the interval.
    
    This looks like we can precompute for each $i$, the range $[L_i, R_i]$ where $A[i]$ is the "bottleneck".
    
    Actually, this problem is solved by computing the **Next Greater Element** and **Previous Greater Element** but with a twist: the value compared against is the **sum** of the segment.
    
    Let's try a different perspective: **Union-Find** or **Stack**.
    We can simulate the process for all $K$ simultaneously?
    
    Correct Algorithm:
    1. Compute `left[i]`: the index of the nearest element to the left of $i$ such that $A[left[i]] \ge A[i]$. If none, 0.
    2. Compute `right[i]`: the index of the nearest element to the right of $i$ such that $A[right[i]] \ge A[i]$. If none, $N+1$.
    3. This defines a range $(left[i], right[i])$ where $A[i]$ is the maximum.
    4. However, as seen, Takahashi can grow beyond $A[i]$.
    
    Let's look at the constraints: $N=5 \times 10^5$. $O(N \log N)$ or $O(N)$ is needed.
    
    **Final Plan**:
    The problem is equivalent to: For each $i$, find the range $[L, R]$ containing $i$ such that $A[i]$ is the **minimum** of the maximums? No.
    
    Actually, there is a known solution using a **Monotonic Stack** to find the "contribution" of each element.
    But here we need the answer for *each* starting position.
    
    Let's use the property: The answer for $K$ is the sum of the segment $[L, R]$ where $L$ is the first index to the left such that $A[L] > \text{Sum}(L+1, K)$? No.
    
    Let's go with the **Next/Previous Greater Element** on the **Prefix Sums**? No.
    
    Let's try this:
    For each $i$, let $L[i]$ be the largest index $< i$ such that $A[L[i]] \ge A[i]$.
    Let $R[i]$ be the smallest index $> i$ such that $A[R[i]] \ge A[i]$.
    The range $(L[i], R[i])$ is the range where $A[i]$ is the maximum.
    If Takahashi starts at $i$, he can absorb everything in $(L[i], R[i])$ IF $A[i]$ is large enough?
    In Sample 1, $K=4$ ($A_4=3$). $L[4]=2$ ($A_2=13$), $R[4]=6$ ($A_6=6$). Range $(2, 6)$ is indices 3,4,5. Sum=7.
    But he absorbs 6 too. Why? Because $7 > 6$ is false. $7 < 6$ is false. $7 > 6$? No.
    Wait, $A_6=6$. Current size 7. $7 > 6$, so he absorbs 6.
    After absorbing 6, size is 13.
    Now he faces $A_2=13$. $13 \ngtr 13$. Stops.
    
    So the range expanded to include 6 because the sum of the inner part was greater than the boundary.
    
    This suggests an iterative expansion.
    
    **Efficient Solution**:
    We can compute the answer for all $K$ using a **Stack** to maintain segments.
    We process the array and merge segments.
    
    Actually, this is equivalent to finding the **Connected Component** in a graph where edges connect $i$ and $j$ if they are adjacent and one is smaller than the other? No.
    
    Let's use the following $O(N)$ approach:
    1. Compute `PGE[i]` (Previous Greater or Equal Element index) and `NGE[i]` (Next Greater or Equal Element index).
    2. This gives a base range $[PGE[i]+1, NGE[i]-1]$ where $A[i]$ is the maximum.
    3. However, if the sum of this range is greater than the boundary values, we can expand.
    
    This is complex. Given the time, I will implement a solution using **Segment Tree** or **Sparse Table** to query range sums and max, and binary search for the range? $O(N \log^2 N)$ might be too slow.
    
    Actually, there is a simpler observation:
    The answer for $K$ is the sum of the segment $[L, R]$ where $L$ and $R$ are determined by the condition that $A[L-1] \ge \text{Sum}(L, R)$ and $A[R+1] \ge \text{Sum}(L, R)$.
    
    We can find this range for each $K$ using a **Two Pointers** or **Stack** method?
    
    Let's try a **Stack-based** approach to compute the "dominant" segment for each element.
    
    Due to complexity, I will write a Python solution that uses a **Monotonic Stack** to compute the Next/Previous Greater Elements, and then uses a **Union-Find** or iterative merging to expand the ranges if the sum exceeds the boundary.
    
    However, a simpler $O(N)$ solution exists:
    The answer for each $i$ is the sum of the segment defined by the **Next Greater Element** and **Previous Greater Element** of the **Prefix Sums**? No.
    
    I will provide a solution that computes `left_bound` and `right_bound` for each element using a stack, assuming the "max in range" logic is the primary driver, and then corrects for the expansion if necessary. Given the constraints and problem type, the "Next Greater Element" range sum is often the answer for "maximal absorption" if we consider the element itself as the seed. But the sample shows expansion.
    
    Let's stick to the most robust $O(N \log N)$ approach:
    For each $K$, binary search for the largest $L$ and $R$ such that the sum of $A[L..R]$ is less than the neighbors? No, the condition is dynamic.
    
    I will implement a solution using **Segment Tree** to support range sum queries and range max queries, and use a recursive function to find the maximal absorbable range for each $K$. This will be $O(N \log N)$ or $O(N)$ depending on implementation.