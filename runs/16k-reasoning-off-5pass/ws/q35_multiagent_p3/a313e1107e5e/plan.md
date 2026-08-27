1. **Problem Analysis**: For each query $(R_i, X_i)$, we need the length of the longest strictly increasing subsequence (LIS) of $A[1..R_i]$ such that every element in the subsequence is $\le X_i$. This is equivalent to finding the LIS of the filtered sequence where we only keep elements from $A[1..R_i]$ that are $\le X_i$.

2. **Key Insight**: The standard $O(N \log N)$ LIS algorithm maintains an array `tails` where `tails[k]` is the smallest ending element of an increasing subsequence of length $k+1$. For a fixed prefix $R_i$, if we restrict to elements $\le X_i$, the LIS length is the largest $k$ such that there exists an increasing subsequence of length $k$ with all elements $\le X_i$.

3. **Offline Processing**: Sort queries by $R_i$ (or process them in order of increasing $R_i$). As we increase $R_i$, we add one element $A_{R_i}$ at a time. We need to answer queries about the LIS length with values $\le X_i$ on the current prefix.

4. **Data Structure**: We can maintain the `tails` array of the LIS for the current prefix. However, the constraint $\le X_i$ makes it tricky because the standard `tails` array doesn't directly support value-based queries. Instead, we can use a **Persistent Segment Tree** or **Offline approach with a Fenwick tree/Segment Tree over values**.

5. **Better Approach - Offline with Segment Tree over Values**: 
   - Process queries offline sorted by $R_i$.
   - Maintain a data structure that, for the current prefix $A[1..R]$, can answer: what is the maximum length of an increasing subsequence using only values $\le X$?
   - Actually, a more direct approach: For each position $j$, let $L[j]$ be the length of the LIS ending at position $j$ using only elements from $A[1..j]$. But this doesn't directly handle the $X_i$ constraint.
   
6. **Correct Approach**: Use a **Segment Tree over the value domain** (coordinate compression on $A_i$). The segment tree will store, for each value $v$, the maximum LIS length ending with a value $\le v$ in the current prefix. When we add $A_j$, we compute the LIS length ending at $A_j$ as $1 + \max(\text{query}(1, A_j-1))$ from the segment tree, then update position $A_j$ with this new length. For a query $(R_i, X_i)$, after processing up to $R_i$, the answer is $\text{query}(1, X_i)$ from the segment tree.

7. **Implementation**: 
   - Coordinate compress $A_i$ values.
   - Use a segment tree that supports point update and range maximum query.
   - Process elements $A_1, \dots, A_N$ one by one. After adding $A_j$, answer all queries with $R_i = j$.
   - For each $A_j$: query max in range $[1, A_j-1]$ to get the longest increasing subsequence ending before $A_j$ with value $< A_j$. Let this be $len$. Update position $A_j$ with $\max(\text{current value at } A_j, len + 1)$.
   - For query $(R_i, X_i)$: after processing $A_{R_i}$, query max in range $[1, X_i]$ (clamped to max compressed value).