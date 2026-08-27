1. **Binary Search on Answer**: The key insight is that the function "count how many triples (i,j,k) have value >= X" is monotonic in X. We can binary search for the largest X such that the count of values >= X is at least K.
2. **Counting Efficiently**: For a fixed threshold X, we need to count triples where $A_i B_j + B_j C_k + C_k A_i \ge X$. This can be rewritten as $B_j(A_i + C_k) + C_k A_i \ge X$. However, a more direct approach is to iterate over j and for each j, count pairs (i,k) such that $A_i B_j + B_j C_k + C_k A_i \ge X$.
3. **Optimized Counting per j**: For a fixed j, let $P_i = A_i$ and $Q_k = C_k$. The condition is $B_j P_i + B_j Q_k + Q_k P_i \ge X$. This is still complex. Instead, note that $A_i B_j + B_j C_k + C_k A_i = B_j(A_i + C_k) + A_i C_k$. 
   A better approach: Fix j. Let $b = B_j$. We need $b A_i + b C_k + A_i C_k \ge X$. Rearranging: $A_i(b + C_k) + b C_k \ge X \Rightarrow A_i \ge \frac{X - b C_k}{b + C_k}$ if $b+C_k > 0$. Since all values are positive, $b+C_k > 0$.
   For each k, we can compute the minimum required $A_i$. Then we count how many $A_i$ satisfy this using a sorted array of A and binary search (bisect).
4. **Complexity**: Binary search takes $O(\log(\text{max\_val}))$ steps. Each step iterates over all j and k ($N^2$ iterations), and for each, does a binary search on A ($O(\log N)$). Total: $O(N^2 \log N \log(\text{max\_val}))$. With $N=2 \cdot 10^5$, $N^2$ is too large.
   
   **Revised Approach**: We need a faster counting method. Note that $K \le 5 \cdot 10^5$, which is small. However, the values can be up to $10^{18}$. 
   
   Actually, let's reconsider. $N$ is up to $2 \cdot 10^5$, so $O(N^2)$ is too slow. We need a better way.
   
   Alternative: Sort A, B, C. The maximum value is $A_{max}B_{max} + B_{max}C_{max} + C_{max}A_{max}$. The minimum is similar.
   
   Let's use the fact that we can iterate over j and use two pointers or binary search on sorted A and C? 
   
   For fixed j, let $b = B_j$. We want to count pairs $(i,k)$ such that $b A_i + b C_k + A_i C_k \ge X$.
   Rewrite: $A_i (b + C_k) \ge X - b C_k$.
   If $X - b C_k \le 0$, then all $A_i$ work (since $A_i > 0, b+C_k > 0$). Count = N.
   If $X - b C_k > 0$, we need $A_i \ge \lceil \frac{X - b C_k}{b + C_k} \rceil$. We can find this count using `bisect_left` on sorted A.
   
   This is $O(N^2 \log N)$ per binary search step, which is too slow for $N=2 \cdot 10^5$.
   
   **Key Insight**: Since K is small ($5 \cdot 10^5$), the K-th largest value is likely among the top values. We can use a max-heap to generate the top K values? But $N^3$ is huge.
   
   Actually, there's a known technique for this problem: Binary search on the answer with an $O(N^2)$ check is too slow. But wait, can we do the counting in $O(N \log N)$ or $O(N)$ per binary search step?
   
   Let's sort A and C. For fixed j and fixed k, the condition on $A_i$ is linear. 
   
   Another approach: Iterate over j. For each j, we have a condition on pairs $(A_i, C_k)$. 
   Let $u = A_i, v = C_k$. Condition: $b u + b v + u v \ge X \iff (u+b)(v+b) \ge X + b^2$.
   Let $X' = X + b^2$. We need $(A_i + b)(C_k + b) \ge X'$.
   Let $A'_i = A_i + b$ and $C'_k = C_k + b$. We need $A'_i C'_k \ge X'$.
   Sort $A'$ and $C'$. For each $A'_i$, we need $C'_k \ge \lceil X' / A'_i \rceil$. Use binary search on sorted $C'$.
   This is $O(N \log N)$ per j, so $O(N^2 \log N)$ per binary search step. Still too slow.
   
   **Correct Approach for Large N**: 
   Since K is small, we can use a different strategy. Generate candidate values from the largest elements. 
   Sort A, B, C in descending order. Consider only the top M elements from each array, where M is chosen such that $M^3 \ge K$. Since $K \le 5 \cdot 10^5$, $M \approx 80$. Then we can brute force the top M elements.
   However, this is not rigorous because the K-th largest might involve smaller elements if there are many large elements. But since we take the top M from each, and $M^3 \ge K$, the K-th largest overall must be within the top $M^3$ values formed by these top M elements? Not necessarily, but it's a common heuristic.
   
   Actually, a rigorous approach: 
   1. Sort A, B, C in descending order.
   2. Use a max-heap to extract the top K values from the $N^3$ combinations.
   3. Start with the largest combination $(A_0, B_0, C_0)$. Push neighbors $(i+1,j,k), (i,j+1,k), (i,j,k+1)$ into the heap, keeping track of visited states.
   4. Extract the K-th element.
   
   This works because K is small ($5 \cdot 10^5$). The heap operations are $O(\log K)$ per extraction, and we do K extractions. Total: $O(K \log K)$. This is efficient.