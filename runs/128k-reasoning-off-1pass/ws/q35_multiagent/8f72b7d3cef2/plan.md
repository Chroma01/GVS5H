1.  **Analyze the Absorption Process**: Takahashi (slime K) can absorb adjacent slimes strictly smaller than his current size. This process is monotonic: as he absorbs, his size increases, potentially allowing him to absorb larger neighbors. The process stops when both neighbors are $\ge$ his current size.
2.  **Key Insight - Reachable Range**: The set of slimes Takahashi can absorb forms a contiguous segment around his initial position. Specifically, he can absorb a slime if it is "reachable" via a chain of absorptions. A crucial observation is that Takahashi can absorb all slimes in a contiguous range $[L, R]$ containing $K$ if and only if he can "break through" the boundaries. The boundary condition is determined by the nearest slime to the left and right that is $\ge$ Takahashi's final size. However, a more direct approach is to determine the maximal contiguous segment $[L, R]$ such that Takahashi can absorb everything in $[L, R]$ except possibly the endpoints if they are too large. Actually, the standard solution for this type of problem involves finding the nearest greater or equal element to the left and right.
3.  **Nearest Greater or Equal Element (NGE)**: For each slime $i$, let $L_i$ be the index of the nearest slime to the left such that $A_{L_i} \ge A_i$, and $R_i$ be the index of the nearest slime to the right such that $A_{R_i} \ge A_i$. If no such slime exists, $L_i = 0$ and $R_i = N+1$.
4.  **Determining the Absorbed Sum**: Takahashi at position $K$ can absorb all slimes in the range $(L_K, R_K)$ except those that are "blocking". Wait, the condition is strictly smaller. If there is a slime $j$ with $A_j \ge A_K$, he cannot absorb it directly. However, he might absorb other slimes first to grow larger than $A_j$.
    *   Actually, the correct logic is: Takahashi can absorb a contiguous range of slimes $[l, r]$ containing $K$ if and only if for every slime in that range, it can be absorbed. The process is equivalent to: Takahashi can absorb all slimes in the range $(L_K, R_K)$? No.
    *   Let's look at the sample. $A = [4, 13, 2, 3, 2, 6]$. For $K=4$ (value 3):
        *   Left NGE: 13 at index 2. So $L_4 = 2$.
        *   Right NGE: 6 at index 6. So $R_4 = 6$.
        *   Range $(2, 6)$ is indices 3, 4, 5 with values $[2, 3, 2]$. Sum = 7. Initial 3 + 7 = 10. But answer is 13. Why? Because after absorbing 2 (right), size becomes 5. Then absorbs 2 (left), size becomes 7. Then absorbs 6 (right)? No, 6 is not strictly smaller than 7? Wait, $6 < 7$ is true. So he absorbs 6. Size becomes 13. Then he is adjacent to 13. $13 \not< 13$, so stop.
        *   So he absorbed indices 3, 4, 5, 6. The range is effectively up to the first element $\ge$ final size.
    *   Refined Insight: Takahashi can absorb all slimes in the range $(L_K, R_K)$? In the example, $L_4=2$ (val 13), $R_4=6$ (val 6). He absorbed index 6 (val 6). So the range extended past the initial NGE.
    *   Correct Logic: The maximum size Takahashi can achieve is the sum of all slimes in the maximal contiguous segment containing $K$ that he can "clear". A slime $j$ can be absorbed if it is smaller than the current size. This is equivalent to finding the largest range $[l, r]$ containing $K$ such that the minimum value in the range (excluding the boundaries that stop the process) allows propagation.
    *   Actually, there is a known result for this problem: The answer for $K$ is the sum of the subarray $A[l \dots r]$ where $l$ is the first index to the left of $K$ such that $A_l \ge A_K$? No.
    *   Let's use the property of the "Next Greater Element". Let $L_i$ be the index of the previous greater or equal element, and $R_i$ be the index of the next greater or equal element. The slime $i$ can absorb everything between $L_i$ and $R_i$? No.
    *   Alternative View: This is equivalent to finding the sum of the connected component of "smaller" elements that can be merged.
    *   Efficient Approach: Use a stack to find the Previous Greater or Equal Element (PGE) and Next Greater or Equal Element (NGE) for each element. Let $L[i]$ be the index of the PGE of $i$, and $R[i]$ be the index of the NGE of $i$. If no PGE exists, $L[i] = 0$. If no NGE exists, $R[i] = N+1$.
    *   Claim: The maximum size Takahashi (at $K$) can achieve is the sum of $A[j]$ for all $j$ in the range $(L[K], R[K])$?
        *   Sample 1, K=4 (val 3). PGE is 13 at index 2. NGE is 6 at index 6. Range $(2, 6)$ is indices 3,4,5. Sum $2+3+2=7$. Total $3+7=10$. But answer is 13. So this claim is false.
    *   Correction: The process allows Takahashi to grow. Once he grows, he might be able to absorb the NGE.
    *   Actually, the correct interpretation is that Takahashi can absorb all slimes in the range $(L[K], R[K])$ **and potentially more** if the sum allows him to overcome the boundary.
    *   Let's look at Sample 2. K=3 (val 61). PGE? None to left (all smaller? 22, 25 < 61). So $L=0$. NGE? None to right (all smaller? 10,21,37,2,14,5,8,6,24 < 61). So $R=13$. Sum of all is 235. Answer 235.
    *   K=2 (val 25). PGE: None? 22<25. So $L=0$. NGE: 61 at index 3. $R=3$. Range $(0, 3)$ is indices 1,2. Sum $22+25=47$. Answer 47.
    *   K=4 (val 10). PGE: 61 at index 3. $L=3$. NGE: 37 at index 6. $R=6$. Range $(3, 6)$ is indices 4,5. Sum $10+21=31$. Answer 31.
    *   K=5 (val 21). PGE: 61 at index 3. $L=3$. NGE: 37 at index 6. $R=6$. Range $(3, 6)$ is indices 4,5. Sum $10+21=31$. Answer 31.
    *   K=6 (val 37). PGE: 61 at index 3. $L=3$. NGE: None? 2,14,5,8,6,24 are all < 37. So $R=13$. Range $(3, 13)$ is indices 4..12. Sum $10+21+37+2+14+5+8+6+24 = 127$. Initial 37 + 127 = 164? Answer is 235.
    *   Wait, Sample 2 Output for K=6 is 235.
    *   Let's re-read carefully. "Choose a slime adjacent to him that is strictly smaller than him".
    *   For K=6 (val 37), he can absorb 2, 14, 5, 8, 6, 24. Sum of these is $2+14+5+8+6+24 = 59$. Size becomes $37+59=96$. Now he is adjacent to 21 (index 5). $21 < 96$, so he absorbs 21. Size $96+21=117$. Adjacent to 10 (index 4). $10 < 117$, absorbs. Size $127$. Adjacent to 61 (index 3). $61 < 127$, absorbs. Size $188$. Adjacent to 25 (index 2). $25 < 188$, absorbs. Size $213$. Adjacent to 22 (index 1). $22 < 213$, absorbs. Size $235$.
    *   So he absorbed EVERYONE.
    *   Why? Because 37 was large enough to eat the right side, grow big enough to eat the left side's "barrier" (61), and then everything else.
    *   The condition for absorbing the entire array is that the initial element is "large enough" or the sum of one side allows breaking the other side.
    *   This looks like finding the "dominating" element.
    *   Actually, there is a simpler characterization: Takahashi can absorb all slimes in the range $[1, N]$ if the maximum element in the array is Takahashi? No.
    *   Let's go back to the stack-based NGE/PGE idea.
    *   For each $i$, let $L[i]$ be the index of the previous greater or equal element. Let $R[i]$ be the index of the next greater or equal element.
    *   The range $(L[i], R[i])$ consists of elements strictly smaller than $A[i]$.
    *   Takahashi can definitely absorb all elements in $(L[i], R[i])$. His new size will be $S_i = \sum_{j=L[i]+1}^{R[i]-1} A[j]$.
    *   After absorbing this range, he is adjacent to $A[L[i]]$ and $A[R[i]]$.
    *   If $S_i > A[L[i]]$, he can absorb $A[L[i]]$ and continue left.
    *   If $S_i > A[R[i]]$, he can absorb $A[R[i]]$ and continue right.
    *   This suggests a recursive or iterative expansion.
    *   However, $N$ is up to $5 \times 10^5$, so we need an $O(N)$ or $O(N \log N)$ solution.
    *   Observation: The final size is the sum of a contiguous subarray $A[l \dots r]$ containing $K$. Which subarray?
    *   It turns out that the answer for $K$ is the sum of the subarray $A[l \dots r]$ where $l$ is the first index to the left such that $A[l] \ge \text{something}$?
    *   Let's consider the global maximum. If Takahashi is the global maximum, he can absorb everyone? Not necessarily, if there are equal values. But if strictly smaller, he can absorb all strictly smaller. If there are equal values, he cannot absorb them.
    *   In Sample 2, 61 is the unique maximum. K=3 (61) absorbs all.
    *   K=6 (37) absorbs all. Why? Because 37 > sum of right side? No.
    *   Key Insight from similar problems (e.g., AtCoder "Slimes"): The answer for each $K$ is the sum of the range $(L[K], R[K])$ where $L[K]$ and $R[K]$ are defined by the **Next Greater Element** logic, BUT we must account for the fact that absorbing one side might allow absorbing the other.
    *   Actually, the correct efficient solution involves calculating the sum of the range bounded by the nearest greater or equal elements. Let $L[i]$ be the index of the previous greater or equal element, and $R[i]$ be the index of the next greater or equal element.
    *   Let $Sum(i, j)$ be the sum of $A[i \dots j]$.
    *   The candidate answer for $K$ is $Sum(L[K]+1, R[K]-1)$.
    *   Let's test this on Sample 2, K=6 (37).
        *   PGE of 37: 61 at index 3. So $L[6]=3$.
        *   NGE of 37: None. So $R[6]=13$ (N+1).
        *   Range $(3, 13)$ is indices 4 to 12.
        *   Sum $A[4 \dots 12] = 10+21+37+2+14+5+8+6+24 = 127$.
        *   But the answer is 235.
    *   So the simple range sum is insufficient. The "expansion" happens because after absorbing the inner range, the size becomes large enough to eat the boundaries.
    *   Notice that 235 is the sum of the entire array.
    *   When does Takahashi eat the entire array? If he can eat the boundaries.
    *   This problem is equivalent to: For each $K$, find the largest range $[l, r]$ containing $K$ such that $A[K]$ is the "dominant" element? No.
    *   Let's use the property: The answer is the sum of the connected component of elements "smaller than the maximum in the range"?
    *   Actually, there is a known solution using a Disjoint Set Union (DSU) or a stack-based approach that computes the "reach" of each element.
    *   Alternative Idea: Reverse the process. Imagine we start with the largest elements and "remove" them.
    *   Or, consider the "Next Greater Element" tree.
    *   Let's try a different perspective. The process stops when Takahashi is adjacent to two elements $\ge$ his size.
    *   Let $L'[K]$ be the index of the nearest element to the left that is $\ge$ the **final** size.
    *   This is circular.
    *   However, note that the final size is always the sum of a contiguous subarray.
    *   Let's guess: The answer for $K$ is the sum of $A[l \dots r]$ where $l$ is the first index to the left such that $A[l] \ge A[K]$? No, we saw K=6 (37) ate 61 (which is $>37$).
    *   But 61 was eaten because the size grew to 127.
    *   Condition to eat $A[L[K]]$: Sum of $(L[K]+1 \dots R[K]-1) > A[L[K]]$.
    *   If this holds, we expand left. Then we check the new left boundary.
    *   This expansion can be modeled by finding the "effective" boundaries.
    *   We can precompute prefix sums.
    *   For each $K$, we can simulate the expansion? No, $O(N^2)$.
    *   We need to jump boundaries.
    *   Let $NextGreater[i]$ be the index of the next greater or equal element.
    *   Let $PrevGreater[i]$ be the index of the previous greater or equal element.
    *   We can use a DSU to merge intervals.
    *   Sort elements by value. Process from smallest to largest? Or largest to smallest?
    *   If we process from largest to smallest, we can determine which elements are "blocked" by larger elements.
    *   Actually, the standard solution for this specific problem (AtCoder ABC 256 F? No, similar to "Slimes" but with absorption) is:
        1. Compute PGE and NGE for all $i$.
        2. The answer for $i$ is the sum of the range $(PGE[i], NGE[i])$? We proved this wrong for K=6.
        3. Wait, did I calculate PGE/NGE correctly for K=6?
           $A = [22, 25, 61, 10, 21, 37, 2, 14, 5, 8, 6, 24]$
           Index 6 is 37.
           Left: 21, 10, 61. 61 is $\ge 37$. So PGE is index 3.
           Right: 2, 14, 5, 8, 6, 24. All $< 37$. So NGE is None (index 13).
           Range $(3, 13)$ sum is 127.
           Final size 127.
           Is $127 > A[3]=61$? Yes. So he absorbs index 3.
           New size $127+61=188$.
           New Left Boundary: Index 2 (25).
           Is $188 > A[2]=25$? Yes. Absorb index 2.
           New size $188+25=213$.
           New Left Boundary: Index 1 (22).
           Is $213 > A[1]=22$? Yes. Absorb index 1.
           New size $213+22=235$.
           Left Boundary: None.
           Right Boundary: None.
           Stop.
    *   So the algorithm is: Start with range $(L, R)$. Calculate sum $S$. If $S > A[L-1]$, expand left. If $S > A[R+1]$, expand right. Repeat until no expansion.
    *   To do this efficiently for all $K$, we can observe that the expansion is deterministic.
    *   We can precompute the "reach" of each interval.
    *   This looks like we can use a stack to find the "dominant" intervals.
    *   Actually, we can compute the answer for each $K$ by finding the nearest element to the left that is $\ge$ the sum of the range to its right? No.
    *   Let's use the property that the expansion only happens if the current sum exceeds the boundary.
    *   We can model this as: For each $K$, the final range is $[l, r]$.
    *   $l$ is the smallest index such that $\sum_{j=l+1}^{R_{eff}} A[j] > A[l]$?
    *   This is complex.
    *   Simpler approach: Since $N$ is $5 \times 10^5$, maybe we can just run the expansion for each $K$ but optimize the jumps?
    *   The number of expansions is limited by the number of "greater or equal" elements.
    *   We can use the PGE/NGE array to jump.
    *   For a given $K$, let $curr = K$. $L = PGE[K]$, $R = NGE[K]$.
    *   Loop:
        $S = PrefixSum[R-1] - PrefixSum[L]$
        Expanded = False
        If $L > 0$ and $S > A[L]$:
            $L = PGE[L]$
            Expanded = True
        If $R \le N$ and $S > A[R]$:
            $R = NGE[R]$
            Expanded = True
        If not Expanded: Break
    *   Answer is $PrefixSum[R-1] - PrefixSum[L]$.
    *   Complexity: In the worst case, this is $O(N)$ per $K$, leading to $O(N^2)$. We need to optimize.
    *   Optimization: Notice that the expansion path is the same for many $K$.
    *   We can memoize the result for intervals?
    *   Or, we can process queries offline?
    *   Actually, the expansion only moves to "greater or equal" boundaries. The sequence of boundaries is a subsequence of the PGE/NGE chain.
    *   We can use binary lifting (doubling) on the PGE/NGE pointers to speed up the simulation.
    *   Precompute `up_left[i][k]` and `up_right[i][k]`?
    *   But the condition depends on the sum, which changes.
    *   However, note that the sum $S$ is the sum of the current range.
    *   Let's define $L_0 = PGE[K], R_0 = NGE[K]$.
    *   $S_0 = Sum(L_0+1, R_0-1)$.
    *   If $S_0 > A[L_0]$, new $L_1 = PGE[L_0]$.
    *   If $S_0 > A[R_0]$, new $R_1 = NGE[R_0]$.
    *   The new sum $S_1 = S_0 + A[L_0] + A[R_0]$ (if both expanded).
    *   This is still state-dependent.
    *   Given the constraints and problem type, the $O(N \log N)$ or $O(N)$ solution likely involves the stack-based NGE/PGE and then a single pass or DSU.
    *   Let's stick to the simulation with optimization: The number of "greater or equal" elements is small on average? No.
    *   However, we can just implement the simulation. If it TLEs, we optimize. But for the plan, we propose the simulation with PGE/NGE jumps.