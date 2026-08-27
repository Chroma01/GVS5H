
## ideation
The core difficulty lies in determining the target sum $S$ and verifying if the fixed elements can be paired with each other or with the "free" slots (where one or both values are -1) to achieve that sum.

1.  **Case 1: There exists at least one index $i$ where both $A_i \neq -1$ and $B_i \neq -1$.**
    *   In this case, the sum $S$ is strictly determined by these pairs. All such pairs must have the same sum $S = A_i + B_i$. If they don't, the answer is immediately "No".
    *   If they do, we fix $S$ and proceed to check feasibility.

2.  **Case 2: No index has both $A_i$ and $B_i$ non-negative.**
    *   Here, $S$ is not uniquely determined by fixed-fixed pairs. We need to find *if there exists* an $S \ge 0$ such that the conditions are met.
    *   Let $F_A$ be the multiset of fixed values in A, and $F_B$ be the multiset of fixed values in B.
    *   Let $N_A^{fix} = |F_A|$, $N_B^{fix} = |F_B|$.
    *   Let $N_A^{free} = N - N_A^{fix}$ (count of -1 in A), $N_B^{free} = N - N_B^{fix}$ (count of -1 in B).
    *   We need to partition $F_A$ into two subsets: $M_A$ (matched with $F_B$) and $U_A$ (unmatched, will be paired with free B's). Similarly, partition $F_B$ into $M_B$ and $U_B$.
    *   Let $m = |M_A| = |M_B|$. The elements in $M_A$ and $M_B$ must be pairable such that each pair sums to $S$.
    *   The elements in $U_A$ must be $\le S$ (so they can be paired with non-negative free B's).
    *   The elements in $U_B$ must be $\le S$ (so they can be paired with non-negative free A's).
    *   The number of free B's available is $N_B^{free}$. We need $N_B^{free} \ge |U_A| = N_A^{fix} - m$.
    *   The number of free A's available is $N_A^{free}$. We need $N_A^{free} \ge |U_B| = N_B^{fix} - m$.
    *   Crucially, if there are no fixed-fixed pairs, it implies that for every index, at least one is -1. This often simplifies the structure. However, $F_A$ and $F_B$ can still be non-empty.
    *   If $F_A$ and $F_B$ are both empty, any $S \ge 0$ works (just set all to 0 and $S$).
    *   If one is empty (e.g., $F_B$ empty, so all $B_i=-1$), then we just need $S \ge \max(F_A)$. We can always set the free B's to $S - A_i$. Since $A_i$ are fixed, we just need $S \ge \max(A_i)$. We can pick $S = \max(A_i)$ (or 0 if $F_A$ empty).
    *   If both are non-empty, we need to find an $S$ and a matching size $m$.
    *   Observation: If we sort $F_A$ and $F_B$, the "easiest" way to match them to sum to $S$ is not straightforward because we can choose *which* ones to match. However, note that if we decide to match $m$ pairs, we are essentially choosing $m$ elements from $F_A$ and $m$ from $F_B$.
    *   Actually, a simpler necessary and sufficient condition for the existence of *some* $S$ when no fixed-fixed pairs exist:
        *   If $N_A^{fix} == 0$ and $N_B^{fix} == 0$: Yes.
        *   If $N_A^{fix} > 0$ and $N_B^{fix} == 0$: Yes (set $S = \max(F_A)$, fill B's).
        *   If $N_A^{fix} == 0$ and $N_B^{fix} > 0$: Yes.
        *   If $N_A^{fix} > 0$ and $N_B^{fix} > 0$:
            We need to find $S$ such that we can match some subset.
            Consider the constraints on $S$:
            $S \ge \max(U_A)$ and $S \ge \max(U_B)$.
            To maximize our chances, we should try to make $U_A$ and $U_B$ contain the largest elements? No, we want $U_A$ and $U_B$ to have small elements so $S$ can be small? Or large?
            Actually, if we match $m$ pairs, the remaining $N_A^{fix}-m$ elements of $F_A$ must be $\le S$. To allow a smaller $S$, we should put the largest elements of $F_A$ into $M_A$ (matched). Similarly for $F_B$.
            So, for a fixed $m$, the best strategy to minimize the required $S$ is to match the largest $m$ elements of $F_A$ with the largest $m$ elements of $F_B$? Not necessarily. We just need *existence* of a pairing.
            However, there is a simpler check. If we can match *any* $m$ pairs, we just need to ensure that the unmatched elements are small enough.
            
            Let's look at the constraints on $m$:
            $m \le N_A^{fix}$
            $m \le N_B^{fix}$
            $N_A^{fix} - m \le N_B^{free} \implies m \ge N_A^{fix} - N_B^{free}$
            $N_B^{fix} - m \le N_A^{free} \implies m \ge N_B^{fix} - N_A^{free}$
            
            So $m$ must be in $[ \max(0, N_A^{fix} - N_B^{free}, N_B^{fix} - N_A^{free}), \min(N_A^{fix}, N_B^{fix}) ]$.
            
            If this range is empty, return No.
            If it's not empty, we need to check if there exists an $m$ in this range and an $S$ such that we can form $m$ pairs summing to $S$, and the remaining elements are $\le S$.
            
            Actually, if we pick the largest possible $m$, we remove the most elements from the "unmatched" set, potentially lowering the max of the unmatched sets.
            Let's try the maximum possible $m$. Let $m_{max} = \min(N_A^{fix}, N_B^{fix})$.
            Check if $m_{max}$ satisfies the lower bound constraints. If not, try smaller $m$?
            Actually, if we decrease $m$, the sets $U_A$ and $U_B$ grow, so $\max(U_A)$ and $\max(U_B)$ likely increase (or stay same). This requires a larger $S$.
            So, to minimize the required $S$, we should maximize $m$.
            
            Let's test $m = m_{max}$.
            We need to check if there exists an $S$ such that:
            1. We can form $m$ pairs from $F_A$ and $F_B$ summing to $S$.
            2. $S \ge \max(F_A \setminus M_A)$
            3. $S \ge \max(F_B \setminus M_B)$
            
            If we fix the subsets $M_A$ and $M_B$, the sum $S$ is constrained.
            However, we can choose *which* elements go into $M_A$ and $M_B$.
            To make it easy to form pairs summing to $S$, and keep $S$ low, we should probably match the largest elements of $F_A$ with the largest elements of $F_B$?
            
            Let's sort $F_A$ ascending and $F_B$ ascending.
            If we take the largest $m$ elements of $F_A$ and largest $m$ of $F_B$, and try to pair them, what is the minimal $S$?
            Actually, if we just want *any* $S$, we can check if the minimal possible max-sum of a matching of size $m$ is $\ge$ the max of the remaining elements.
            
            This is getting complex. Let's step back.
            If there are NO fixed-fixed pairs, is it always Yes?
            Sample 3:
            A: 1 2 -1
            B: 1 2 4
            Fixed A: {1, 2}. Fixed B: {1, 2, 4}.
            Indices:
            0: A=1, B=1 (Fixed-Fixed! Sum=2).
            1: A=2, B=2 (Fixed-Fixed! Sum=4).
            2: A=-1, B=4 (Fixed B).
            
            Wait, Sample 3 has fixed-fixed pairs!
            Index 0: A0=1, B0=1. Sum=2.
            Index 1: A1=2, B1=2. Sum=4.
            Since $2 \neq 4$, it's impossible. Output No.
            
            So my Case 1 covers Sample 3.
            
            Let's look for a Case 2 example.
            A: -1 -1
            B: 1 2
            Fixed A: {}. Fixed B: {1, 2}.
            $N_A^{fix}=0, N_B^{fix}=2$.
            $N_A^{free}=2, N_B^{free}=0$.
            Range for $m$: $[0, 0]$. So $m=0$.
            $U_A = \emptyset, U_B = \{1, 2\}$.
            Need $S \ge \max(U_B) = 2$.
            Can we form 0 pairs? Yes.
            So $S=2$ works. $A$ becomes $(1, 0)$, $B$ is $(1, 2)$. Sums: $1+1=2, 0+2=2$. Yes.
            
            Another Case 2:
            A: 10 -1
            B: -1 20
            Fixed A: {10}. Fixed B: {20}.
            $N_A^{fix}=1, N_B^{fix}=1$.
            $N_A^{free}=1, N_B^{free}=1$.
            Range for $m$:
            Lower bound: $\max(0, 1-1, 1-1) = 0$.
            Upper bound: $\min(1, 1) = 1$.
            Try $m=1$.
            $M_A=\{10\}, M_B=\{20\}$. Pair sum $S=30$.
            $U_A=\emptyset, U_B=\emptyset$.
            $S=30 \ge 0$. Yes.
            
            Try $m=0$.
            $U_A=\{10\}, U_B=\{20\}$.
            Need $S \ge 10$ and $S \ge 20 \implies S \ge 20$.
            Can we form 0 pairs? Yes.
            So $S=20$ works?
            If $S=20$:
            Index 0: A=10, B=-1. $B_0 = 20-10=10$.
            Index 1: A=-1, B=20. $A_1 = 20-20=0$.
            Pairs: $(10, 10)$ sum 20, $(0, 20)$ sum 20. Yes.
            
            It seems if there are no conflicting fixed-fixed pairs, it's often Yes.
            Is it always Yes if no fixed-fixed pairs?
            Consider:
            A: 100 -1
            B: -1 100
            Fixed A: {100}, Fixed B: {100}.
            $m=1 \implies S=200$. Yes.
            
            What if:
            A: 10 -1 -1
            B: -1 20 -1
            Fixed A: {10}, Fixed B: {20}.
            $m=1 \implies S=30$. Yes.
            
            It seems if there are no fixed-fixed pairs, we can always find a solution?
            Wait, what if the counts don't allow it?
            A: 10 10
            B: -1 -1
            Fixed A: {10, 10}. Fixed B: {}.
            $N_A^{fix}=2, N_B^{fix}=0$.
            $m=0$. $U_A=\{10, 10\}, U_B=\emptyset$.
            Need $S \ge 10$.
            $S=10$. $B$ becomes $(0, 0)$.
            Pairs: $(10,0), (10,0)$. Sums 10. Yes.
            
            It appears that if there are NO fixed-fixed pairs, the answer is always Yes.
            Why? Because we can always set $S = \max(\max(F_A), \max(F_B))$.
            Then for any fixed $A_i$, $B_i$ (if -1) can be set to $S - A_i \ge 0$.
            For any fixed $B_j$, $A_j$ (if -1) can be set to $S - B_j \ge 0$.
            The only issue is if we have fixed A and fixed B at the *same* index, which is excluded in Case 2.
            In Case 2, for every index $i$, at least one is -1.
            So we can independently set the -1s to satisfy the sum $S$.
            The only constraint is $S \ge A_i$ for all fixed $A_i$ (so $B_i \ge 0$) and $S \ge B_j$ for all fixed $B_j$ (so $A_j \ge 0$).
            So $S = \max(\max(F_A \text{ if } F_A \neq \emptyset \text{ else } 0, \max(F_B \text{ if } F_B \neq \emptyset \text{ else } 0))$ works.
            
            So the algorithm is:
            1. Identify all indices where $A_i \neq -1$ and $B_i \neq -1$.
            2. If this set is empty, return "Yes".
            3. If this set is not empty, calculate $S = A_i + B_i$ for the first such index.
            4. Check if all other fixed-fixed indices have sum $S$. If not, return "No".
            5. If all match, we have a fixed $S$. Now we must check if the remaining elements (where at least one is -1) can be filled to sum to $S$ with non-negative integers.
               - For each index $i$:
                 - If $A_i \neq -1$ and $B_i \neq -1$: Already checked sum is $S$.
                 - If $A_i \neq -1$ and $B_i == -1$: Need $B_i = S - A_i \ge 0 \implies S \ge A_i$.
                 - If $A_i == -1$ and $B_i \neq -1$: Need $A_i = S - B_i \ge 0 \implies S \ge B_i$.
                 - If $A_i == -1$ and $B_i == -1$: Can always fill (e.g., $0, S$).
            6. If all these conditions hold, return "Yes", else "No".

## worker: (none)
The problem asks if we can make $A_i + B_i = S$ for all $i$ for some constant $S$, by filling in $-1$s and permuting $A$.
1.  **Fixed-Fixed Pairs**: If there exists any index $i$ where both $A_i$ and $B_i$ are non-negative, the sum $S$ is constrained to be $A_i + B_i$. All such indices must yield the same sum $S$. If they don't, it's impossible ("No").
2.  **No Fixed-Fixed Pairs**: If no index has both values fixed, we have complete freedom to choose $S$. We can simply pick $S = \max(\max(A_{\text{fixed}}), \max(B_{\text{fixed}}), 0)$. Then we can fill in the $-1$s to satisfy the sum $S$ with non-negative integers. For example, if $A_i$ is fixed, set $B_i = S - A_i \ge 0$. If $B_i$ is fixed, set $A_i = S - B_i \ge 0$. If both are $-1$, set $A_i=0, B_i=S$. Thus, the answer is always "Yes".
3.  **Verification for Fixed S**: If $S$ is determined by fixed-fixed pairs, we must check if the remaining indices (where at least one is $-1$) can be filled.
    *   If $A_i$ is fixed and $B_i$ is $-1$, we need $B_i = S - A_i \ge 0 \implies S \ge A_i$.
    *   If $B_i$ is fixed and $A_i$ is $-1$, we need $A_i = S - B_i \ge 0 \implies S \ge B_i$.
    *   If both are $-1$, we can always choose $A_i=0, B_i=S$ (since $S \ge 0$).
    *   If both are fixed, we already verified $A_i + B_i = S$.

The algorithm implements this logic:
- Identify fixed-fixed indices.
- If none, print "Yes".
- If some, determine $S$ from the first one.
- Verify all fixed-fixed indices sum to $S$.
- Verify all partially fixed indices allow non-negative fills for sum $S$.
- If all checks pass, print "Yes", else "No".

Complexity: $O(N)$ time and space, which is well within limits for $N \le 2000$.
