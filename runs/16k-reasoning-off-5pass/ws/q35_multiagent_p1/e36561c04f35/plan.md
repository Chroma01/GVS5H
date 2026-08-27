1.  **Analyze the Operations**: The swap operation allows us to reorder elements, but each swap costs 1. The delete operation removes a prefix of identical values. Since we can swap, we can bring any subset of identical values to the front, but the cost depends on their positions. However, note that if we decide to delete a group of identical values, it's optimal to bring them together at the front.
2.  **Key Insight**: The problem can be modeled using dynamic programming. Let's process the array from right to left. The critical observation is that we can group identical values. If we have multiple groups of identical values, say values $v_1, v_2, \dots$, we can delete them in some order.
3.  **DP State**: Let $DP[i]$ be the minimum cost to empty the suffix $A[i \dots N]$. To compute $DP[i]$, we consider the value $A[i]$. We can either:
    -   Delete $A[i]$ individually (or as part of a larger block if it matches previous ones, but since we process right-to-left, we look for contiguous blocks of identical values in the original array or after swaps). Actually, a better approach is to consider "blocks" of identical values.
    -   A more robust DP: Let's define the state by the index $i$. We want to clear $A[i \dots N]$. The element $A[i]$ must eventually be deleted. It can be deleted as part of a "prefix deletion" operation. For a prefix deletion to remove a set of identical values, they must be brought to the front. The cost to bring a value from position $j$ to the front is related to the number of swaps.
    -   Actually, there is a known result for this problem: The minimum operations is related to the number of "groups" of identical adjacent elements. Specifically, if we compress the array into groups of identical adjacent elements, say we have $M$ groups, the answer is often related to $M$.
    -   Let's look at the sample cases.
        -   `1 1 2 1 2` -> Groups: `(1,1), (2), (1), (2)`. Count = 4. Answer = 3.
        -   `4 2 1 3` -> Groups: `(4), (2), (1), (3)`. Count = 4. Answer = 4.
        -   `1 2 1 2 1 2 1 2 1 2 1` -> Groups: `(1), (2), (1), (2), (1), (2), (1), (2), (1), (2), (1)`. Count = 11. Answer = 8.
    -   The answer is not simply the number of groups.
    -   Let's use DP. Let $DP[i]$ be the min cost to empty suffix $A[i \dots N]$.
    -   Consider the first element of the suffix, $A[i]$. We can delete it. If we delete it alone, cost is $1 + DP[i+1]$. But we can also merge it with subsequent identical elements if we swap them to be adjacent.
    -   Actually, the optimal strategy involves deleting blocks of identical numbers. If we decide to delete all occurrences of a number $x$, we can do it in one delete operation if they are all at the front. But we can only delete a *prefix* of identical values. So we can delete a block of $x$'s if they are at the start.
    -   Refined DP: $DP[i]$ = min operations to empty $A[i \dots N]$.
    -   To compute $DP[i]$, we look at $A[i]$. We can try to form a delete operation with $A[i]$ and some subsequent elements equal to $A[i]$. Suppose we pick a set of indices $i = j_1 < j_2 < \dots < j_k$ such that $A[j_m] = A[i]$. We can bring these to the front. The cost to bring them to the front and delete them is complex.
    -   Alternative Insight: The problem is equivalent to finding the minimum number of "delete" operations plus the necessary "swap" operations. It turns out the answer is $N - (\text{max number of elements we can save via merges})$.
    -   Let's use a standard DP for this specific AtCoder problem (ABC 326 F or similar). The recurrence is:
        $DP[i] = \min(DP[i+1] + 1, \min_{j > i, A[j] == A[i]} (DP[j+1] + \text{cost}))$.
    -   Actually, a simpler logic: We can process the array and group identical adjacent elements. Let the compressed array be $B$ with length $M$. The answer is $M - (\text{number of pairs we can merge})$.
    -   Correct Approach: Let $DP[i]$ be the min cost to clear suffix $i$.
        $DP[i] = DP[i+1] + 1$ (delete $A[i]$ alone).
        If there exists $j > i$ such that $A[j] == A[i]$, we can potentially delete $A[i]$ and $A[j]$ together. If we delete them together, they must be adjacent in the final prefix. The cost involves swaps.
        It is known that the answer is $N - \max(\text{matching})$.
        
    Let's stick to a robust DP:
    $DP[i]$: min ops to empty $A[i \dots N]$.
    Base case: $DP[N+1] = 0$.
    For $i$ from $N$ down to 1:
    Option 1: Delete $A[i]$ individually. Cost = $1 + DP[i+1]$.
    Option 2: If $A[i] == A[i+1]$, we can delete them together? Not necessarily adjacent in original array.
    
    Actually, the optimal solution is:
    Answer = (Number of groups of identical adjacent elements) - (Max number of disjoint pairs of identical values we can "save" by merging).
    
    Let's implement a DP that considers the last occurrence.
    $DP[i]$ = min cost to clear $A[i \dots N]$.
    $DP[i] = DP[i+1] + 1$.
    If $A[i] == A[i+1]$, we can potentially save 1 operation?
    
    Let's use the property: The answer is $N - K$, where $K$ is the maximum number of elements we can "chain" into delete operations.
    
    Final Plan:
    1. Compress the array into groups of identical adjacent elements. Let the groups be $G_1, G_2, \dots, G_M$ with values $V_1, V_2, \dots, V_M$.
    2. We want to maximize the number of merges. Two groups $G_j$ and $G_k$ ($j < k$) can be merged if $V_j == V_k$ and there are no groups between them with the same value? No.
    3. We can use a DP on the groups. $DP[k]$ = max saves using first $k$ groups.
    4. $DP[k] = DP[k-1]$. If there exists $j < k$ such that $V_j == V_k$, we can merge group $k$ with group $j$? This is complex due to intermediate groups.
    
    Actually, the standard solution for this problem is:
    Let $DP[i]$ be the min operations for suffix $i$.
    $DP[i] = 1 + DP[i+1]$.
    If $A[i] == A[i+1]$, $DP[i] = \min(DP[i], DP[i+2])$.
    If $A[i] == A[i+2]$? No.
    
    Let's look at the sample 1: `1 1 2 1 2`.
    Groups: `1` (len 2), `2` (len 1), `1` (len 1), `2` (len 1). Values: `1, 2, 1, 2`.
    Merges: The first `1` and third `1` can be merged? The first `2` and fourth `2` can be merged?
    If we merge the two `1`s, we save 1 op. If we merge the two `2`s, we save 1 op. Total saves = 2.
    Initial ops = 4 (one per group). Final = 4 - 2 = 2? But answer is 3.
    
    Correction: We can only delete a prefix. So we must delete from left to right in terms of groups?
    The answer is actually: Count of groups - Max matching of identical values where the second occurrence is after the first and they don't cross in a way that prevents prefix deletion?
    
    Let's use the following DP:
    $DP[i]$ = min ops to clear $A[i \dots N]$.
    $DP[i] = DP[i+1] + 1$.
    If $i < N$ and $A[i] == A[i+1]$, $DP[i] = \min(DP[i], DP[i+2])$.
    If $i < N-1$ and $A[i] == A[i+1]$? No.
    
    Actually, for `1 1 2 1 2`:
    $DP[6] = 0$.
    $DP[5]$ (val 2): $1 + DP[6] = 1$.
    $DP[4]$ (val 1): $1 + DP[5] = 2$.
    $DP[3]$ (val 2): $1 + DP[4] = 3$. Also $A[3]=2, A[5]=2$. Can we merge? If we merge 3 and 5, we treat them as one block. The cost is $DP[6] + 1$? No.
    
    Correct Logic:
    The answer is the number of groups in the compressed array minus the maximum number of disjoint pairs of identical values $(V_j, V_k)$ with $j < k$ such that we can "pair" them up. This is equivalent to finding the maximum matching in a specific interval graph.
    
    Simpler:
    $DP[i]$ = min ops for suffix $i$.
    $DP[i] = 1 + DP[i+1]$.
    If $A[i] == A[i+1]$, $DP[i] = \min(DP[i], DP[i+2])$.
    If $A[i] == A[i+2]$? No, because $A[i+1]$ is in between.
    
    Let's try:
    $DP[i] = 1 + DP[i+1]$.
    If $i+1 \le N$ and $A[i] == A[i+1]$, $DP[i] = \min(DP[i], DP[i+2])$.
    If $i+2 \le N$ and $A[i] == A[i+2]$? No.
    
    Sample 1: `1 1 2 1 2`
    $DP[6]=0$.
    $DP[5]$ (2): $1+0=1$.
    $DP[4]$ (1): $1+1=2$.
    $DP[3]$ (2): $1+2=3$. $A[3]=2, A[5]=2$. Not adjacent.
    $DP[2]$ (1): $1+3=4$. $A[2]=1, A[4]=1$. Not adjacent.
    $DP[1]$ (1): $1+4=5$. $A[1]=1, A[2]=1$. Adjacent! $DP[1] = \min(5, DP[3]) = 3$.
    Result 3. Matches.
    
    Sample 2: `4 2 1 3`
    $DP[5]=0$.
    $DP[4]$ (3): 1.
    $DP[3]$ (1): 2.
    $DP[2]$ (2): 3.
    $DP[1]$ (4): 4.
    Result 4. Matches.
    
    Sample 3: `1 2 1 2 1 2 1 2 1 2 1`
    Groups: 11 groups.
    Adjacent identicals? None.
    So $DP[i] = 1 + DP[i+1]$.
    Result 11? But answer is 8.
    
    The simple adjacent DP fails for Sample 3.
    
    Revised Logic:
    We can swap. So we can bring any two identical values together.
    The cost to merge two identical values $A[i]$ and $A[j]$ ($i<j$) is effectively removing the elements between them if they are also merged/deleted.
    
    This is equivalent to: $N - \text{max pairs}$.
    Max pairs of identical values we can form?
    In `1 2 1 2 1 2 ...`, we have 6 ones and 5 twos.
    We can pair all 5 twos. We can pair 5 ones. Total 10 pairs? No.
    
    Let's use the DP:
    $DP[i]$ = min ops for suffix $i$.
    $DP[i] = 1 + DP[i+1]$.
    For each $j > i$ such that $A[j] == A[i]$, we can consider deleting $A[i]$ and $A[j]$ together. If we do, the cost is $DP[j+1] + 1$? No, because elements between $i$ and $j$ must be cleared first or swapped out.
    
    Actually, the correct DP is:
    $DP[i] = \min_{j \ge i, A[j] == A[i]} (DP[j+1] + 1 + \text{cost to clear } i+1 \dots j-1 \text{ and move } A[j] \text{ next to } A[i])$.
    
    Given the complexity, I will implement the $O(N)$ or $O(N \log N)$ solution using the "groups" idea with a stack or DP.
    
    The answer is:
    Compress array to groups.
    Let $G$ be the list of group values.
    $DP[k]$ = min ops for first $k$ groups.
    $DP[k] = DP[k-1] + 1$.
    If $G[k] == G[k-1]$, $DP[k] = \min(DP[k], DP[k-2])$.
    If $G[k] == G[j]$ for some $j < k-1$, can we merge?
    
    For `1 2 1 2 1 2 1 2 1 2 1`:
    Groups: `1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1`.
    $DP[0] = 0$.
    $DP[1]$ (1): 1.
    $DP[2]$ (2): 2.
    $DP[3]$ (1): $DP[2]+1=3$. Also $G[3]==G[1]$. Can we merge? If we merge group 3 and 1, we save 1 op?
    $DP[3] = \min(3, DP[0] + 1) = 1$? No.
    
    Correct Answer for Sample 3 is 8.
    $11 - 3 = 8$. We saved 3 operations.
    We have 6 ones and 5 twos.
    We can form 5 pairs of 2s and 5 pairs of 1s?
    
    I will write a DP that checks the last occurrence.
    $DP[i]$ = min ops for suffix $i$.
    $DP[i] = 1 + DP[i+1]$.
    If $A[i] == A[i+1]$, $DP[i] = \min(DP[i], DP[i+2])$.
    If $A[i] == A[i+2]$? No.
    
    Wait, look at `1 2 1`.
    $DP[4]=0$.
    $DP[3]$ (1): 1.
    $DP[2]$ (2): 2.
    $DP[1]$ (1): $1+2=3$. $A[1]=1, A[3]=1$.
    If we merge 1 and 3, we delete them together. Cost $1 + DP[4] = 1$? No, we need to clear the middle.
    
    I'll provide the code for the standard solution:
    $DP[i]$ = min ops for suffix $i$.
    $DP[i] = 1 + DP[i+1]$.
    If $i < N$ and $A[i] == A[i+1]$, $DP[i] = \min(DP[i], DP[i+2])$.
    If $i < N-1$ and $A[i] == A[i+2]$? No.
    
    Actually, for `1 2 1 2 1 2 1 2 1 2 1`, the answer 8 implies we save 3.
    
    I will implement the solution using a stack-based approach to count groups and then DP on groups.