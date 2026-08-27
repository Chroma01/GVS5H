1. **Model the problem**: We need to cover all indices $1 \dots N$ with 1s. Each operation $i$ gives us a choice: do nothing (cost 0), set $[L_i, R_i]$ to 1 (cost 1), or set everything *except* $[L_i, R_i]$ to 1 (cost 1). Note that Operation 2 sets $[1, L_i-1] \cup [R_i+1, N]$ to 1.
2. **Key Insight**: Since we start with all 0s and only set values to 1 (never back to 0), the final state is the union of all intervals set to 1 by Operations 1 and 2. We want to select a subset of operations (with types 1 or 2) such that their union covers $[1, N]$, minimizing the total cost. Operations not selected are type 0.
3. **Dynamic Programming**: Let $DP[i]$ be the minimum cost to cover the prefix $[1, i]$ using a subset of the first $k$ operations? No, the operations are given in a fixed order, but the order doesn't matter for the final union. However, we must output the choice for each operation in order. Since the union is commutative, we can reframe: we need to cover $[1, N]$ using intervals from the set $\mathcal{S} = \{ [L_i, R_i] \text{ for Op 1} \} \cup \{ [1, L_i-1], [R_i+1, N] \text{ for Op 2} \}$. Each operation $i$ contributes either $[L_i, R_i]$ (cost 1) or $[1, L_i-1] \cup [R_i+1, N]$ (cost 1).
4. **Simplification**: Actually, it's easier to think about covering the "gaps". But a standard interval covering DP works if we sort intervals. However, we have a constraint: for each $i$, we pick at most one "coverage" from two options. This is a weighted interval covering problem with choices.
5. **Alternative View**: Let's define $DP[i]$ as the min cost to cover $[1, i]$. To compute $DP[i]$, we can transition from some $DP[j]$ ($j < i$) by adding an operation that covers $[j+1, i]$. But an operation might cover more than just a contiguous block if it's Op 2. Op 2 covers $[1, L-1] \cup [R+1, N]$. This is non-contiguous.
6. **Correct Approach**: Since $N$ is up to $10^6$, we need an efficient DP. Let's consider the complement: which indices are *not* covered? Initially all are 0. We want all to be 1.
   Let's use DP on the position $i$ from $1$ to $N$. $DP[i]$ = min cost to ensure $x_1 \dots x_i$ are all 1.
   To compute $DP[i]$, we look for the largest $j < i$ such that we can cover $[j+1, i]$ with some operations. But operations can cover disjoint parts.
   
   Actually, note that Op 2 on $[L, R]$ sets $[1, L-1]$ and $[R+1, N]$ to 1. This is very powerful for the ends.
   
   Let's reconsider. The problem is equivalent to: Select a set of intervals to cover $[1, N]$. Each operation $i$ provides two candidate intervals (or sets of intervals):
   - Option 1: Interval $I_{i,1} = [L_i, R_i]$ with cost 1.
   - Option 2: Two intervals $I_{i,2a} = [1, L_i-1]$ and $I_{i,2b} = [R_i+1, N]$ with cost 1 (shared).
   
   This is a "Set Cover" variant but on a line, which can be solved with DP.
   Let $DP[i]$ be the min cost to cover $[1, i]$.
   $DP[0] = 0$.
   For $i = 1 \dots N$:
   $DP[i] = \min ($
     $DP[i-1]$ if $x_i$ is already covered by previous choices? No, DP state must encode coverage.
   $)$
   
   Standard technique for covering $[1, N]$ with intervals:
   Sort all available "atomic" coverage units? No.
   
   Let's use the property that we only care about covering $[1, N]$.
   $DP[i]$ = min cost to cover $[1, i]$.
   Transition: To cover up to $i$, the last operation added must cover some suffix of $[1, i]$, say $[j+1, i]$.
   However, an operation might cover $[1, L-1]$ which is a prefix.
   
   Let's define $DP[i]$ as min cost to cover $[1, i]$.
   Initialize $DP[0]=0$, others $\infty$.
   For each $i$ from $1$ to $N$:
     1. We can extend a previous coverage. If we have covered $[1, i-1]$, and we use an operation that covers $i$, we might cover more.
     
   This is tricky because operations are global.
   
   **Better DP**:
   Let's collect all "events".
   Actually, since $M$ is $2 \cdot 10^5$, we can't iterate all subsets.
   
   Let's look at the structure again.
   Op 1 on $[L, R]$ covers $[L, R]$.
   Op 2 on $[L, R]$ covers $[1, L-1] \cup [R+1, N]$.
   
   Notice that Op 2 is only useful if we need to cover the prefix $[1, L-1]$ or suffix $[R+1, N]$.
   
   Let's try a DP where $DP[i]$ is the min cost to cover the prefix $[1, i]$.
   To compute $DP[i]$, we consider the last "block" of coverage that ends at $i$.
   This block could be:
   - An Op 1 interval $[L, R]$ where $R=i$. Then we need $[1, L-1]$ to be covered. Cost: $DP[L-1] + 1$.
   - An Op 2 interval $[L, R]$ where $R+1 > i$? No, Op 2 covers $[R+1, N]$. It doesn't help cover a middle segment $[j+1, i]$ unless $j+1=1$ or something.
     Specifically, Op 2 covers $[1, L-1]$. So if we use Op 2, it covers a prefix.
     So, if we use Op 2 with parameter $L$, it covers $[1, L-1]$. This can transition from $DP[0]$ to $DP[L-1]$ with cost 1.
     Wait, Op 2 also covers $[R+1, N]$. This is a suffix.
     
   So, we can cover the array with:
   - Some prefix covered by Op 2s or Op 1s.
   - Some middle covered by Op 1s.
   - Some suffix covered by Op 2s.
   
   Actually, Op 2 covers a prefix AND a suffix simultaneously for cost 1.
   
   Let $DP[i]$ = min cost to cover $[1, i]$.
   Transitions for $DP[i]$:
   1. From $DP[i-1]$: If we just extend? No, intervals are discrete.
   2. Use an Op 1 $[L, i]$: Then we need $[1, L-1]$ covered. Cost $DP[L-1] + 1$.
   3. Use an Op 2 $[L, R]$ such that it covers up to $i$?
      Op 2 covers $[1, L-1]$. So if $L-1 = i$, i.e., $L=i+1$, then Op 2 covers $[1, i]$. Cost 1.
      But Op 2 also covers $[R+1, N]$. This doesn't help with prefix $[1, i]$ directly unless we are covering the whole array.
      
   Let's refine:
   $DP[i]$ = min cost to cover $[1, i]$.
   Base: $DP[0] = 0$.
   
   For $i = 1 \dots N$:
   $DP[i] = \infty$
   
   // Option A: Cover $[1, i]$ using an Op 1 that ends at $i$
   For each Op 1 with $R_i = i$:
     $DP[i] = \min(DP[i], DP[L_i - 1] + 1)$
     
   // Option B: Cover $[1, i]$ using an Op 2 that covers the prefix $[1, i]$
   // Op 2 on $[L, R]$ covers $[1, L-1]$. So if $L-1 = i \Rightarrow L = i+1$.
   // But $L \le R \le N$, so $L=i+1$ implies $i+1 \le N$.
   // If there is an Op 2 with $L_i = i+1$, it covers $[1, i]$.
   // Cost is 1. But we must ensure we don't double count? No, just min.
   // Note: Op 2 covers $[1, L-1]$ AND $[R+1, N]$.
   // If we use Op 2 to cover $[1, i]$, we are essentially saying the prefix $[1, i]$ is done.
   // $DP[i] = \min(DP[i], 1)$ if there exists an Op 2 with $L_i = i+1$.
   
   // Option C: What if Op 2 covers a prefix that is larger than $i$?
   // If Op 2 has $L_i - 1 > i$, it covers $[1, i]$ as part of $[1, L_i-1]$.
   // So if there is ANY Op 2 with $L_i - 1 \ge i$, we can cover $[1, i]$ with cost 1?
   // Yes, but we might be "wasting" coverage. However, since cost is 1, and we want min cost,
   // if we can cover $[1, i]$ with cost 1, that's a candidate.
   // But wait, if we use an Op 2 with $L_i - 1 \ge i$, we also cover $[R_i+1, N]$.
   // This DP state $DP[i]$ only tracks prefix coverage. It doesn't track suffix.
   
   This suggests we need a 2D DP or a different state.
   State: $DP[i][j]$ = min cost to cover prefix $[1, i]$ and suffix $[j, N]$.
   Target: $DP[N][1]$.
   Constraints: $N=10^6$, so $O(N^2)$ is too slow.
   
   Observation: The "middle" part $[i+1, j-1]$ is NOT covered.
   We want $i \ge j-1$ (i.e., $i+1 \ge j$) for full coverage.
   
   Transitions:
   1. Op 1 $[L, R]$: Covers $[L, R]$.
      New state from $(i, j)$:
      Prefix becomes $\max(i, R)$. Suffix becomes $\min(j, L)$.
      Cost +1.
   2. Op 2 $[L, R]$: Covers $[1, L-1]$ and $[R+1, N]$.
      New state from $(i, j)$:
      Prefix becomes $\max(i, L-1)$. Suffix becomes $\min(j, R+1)$.
      Cost +1.
   3. Op 0: No change.
   
   This is a shortest path on a DAG of states $(i, j)$.
   Number of states is $O(N^2)$. Too big.
   
   However, note that we process operations in order? No, order doesn't matter for the final union.
   But we must output the choice for each operation.
   
   Let's swap: Process operations one by one?
   $DP[k][i][j]$ = min cost using first $k$ ops to cover prefix $i$ and suffix $j$.
   $M=200,000$, $N=10^6$. State space too big.
   
   Key Insight: The "uncovered" region is always a single interval $[i+1, j-1]$.
   Let $U = [i+1, j-1]$ be the uncovered interval.
   Initially $U = [1, N]$.
   Op 1 $[L, R]$ removes $[L, R] \cap U$ from $U$.
   Op 2 $[L, R]$ removes $[1, L-1] \cap U$ and $[R+1, N] \cap U$ from $U$.
   
   If $U$ becomes empty, we are done.
   
   Let $DP[k]$ be the set of possible uncovered intervals $[l, r]$ after $k$ operations, with min cost.
   Since we want min cost, for each possible interval, we keep the min cost.
   But there are $O(N^2)$ intervals.
   
   However, notice that Op 1 shrinks the interval from inside.
   Op 2 shrinks the interval from the ends.
   
   Let's define $f(l, r)$ = min cost to reduce uncovered interval $[l, r]$ to empty.
   We want $f(1, N)$.
   
   Transitions for $f(l, r)$:
   1. Use Op 1 $[L, R]$:
      The new uncovered interval is $[l, r] \setminus [L, R]$.
      This might split into two intervals?
      If $[L, R]$ is inside $[l, r]$, we get $[l, L-1]$ and $[R+1, r]$.
      Then we need to cover BOTH.
      This suggests we need to cover a set of disjoint intervals.
      
   This looks like we can cover the array with a set of operations.
   
   Let's go back to $DP[i]$ = min cost to cover $[1, i]$.
   And $G[j]$ = min cost to cover $[j, N]$.
   
   If we use only Op 1s, we can solve covering $[1, N]$ with standard interval covering DP.
   If we use Op 2s, they cover prefixes/suffixes.
   
   Consider that any solution can be decomposed into:
   - A set of Op 2s that cover some prefix $[1, P]$ and some suffix $[S, N]$.
   - A set of Op 1s that cover the middle $[P+1, S-1]$.
   
   Note: Op 2s can overlap. The union of Op 2s will cover $[1, \max(L_k-1)]$ and $[\min(R_k+1), N]$.
   Let $L_{max} = \max \{ L_k - 1 \mid \text{Op 2 chosen} \}$.
   Let $R_{min} = \min \{ R_k + 1 \mid \text{Op 2 chosen} \}$.
   Then Op 2s cover $[1, L_{max}] \cup [R_{min}, N]$.
   The remaining uncovered part is $[L_{max}+1, R_{min}-1]$.
   We must cover this middle part using Op 1s.
   
   So the algorithm is:
   1. Iterate over all possible "prefix coverage" $P$ and "suffix coverage" $S$ such that $P < S$.
      The middle is $[P+1, S-1]$.
      Cost = (Min cost to cover $[1, P]$ using Op 2s) + (Min cost to cover $[S, N]$ using Op 2s) + (Min cost to cover $[P+1, S-1]$ using Op 1s).
      Wait, Op 2s are chosen as a set. The cost is the number of Op 2s chosen.
      We want to minimize:
      $Cost(P, S) = C_{prefix}(P) + C_{suffix}(S) + C_{middle}(P+1, S-1)$
      
      Where:
      $C_{prefix}(P)$: Min number of Op 2s needed to cover $[1, P]$.
      Note: An Op 2 with $[L, R]$ covers $[1, L-1]$. So to cover $[1, P]$, we need at least one Op 2 with $L-1 \ge P$.
      Actually, if we pick a set of Op 2s, the covered prefix is $[1, \max(L_i-1)]$.
      So $C_{prefix}(P)$ is 1 if there exists an Op 2 with $L_i - 1 \ge P$, else $\infty$.
      Similarly, $C_{suffix}(S)$ is 1 if there exists an Op 2 with $R_i + 1 \le S$, else $\infty$.
      
      Wait, can we use multiple Op 2s to cover the prefix?
      No, because one Op 2 covers $[1, L-1]$. If we have multiple, the union is $[1, \max(L_i-1)]$.
      So to cover $[1, P]$, we just need ONE Op 2 with $L_i - 1 \ge P$.
      Cost is 1 if such an Op 2 exists, else we can't cover the prefix with Op 2s alone?
      What if we use Op 1s for the prefix?
      The decomposition assumed Op 2s handle prefix/suffix and Op 1s handle middle.
      But Op 1s can also handle prefix/suffix.
      
      Refined Decomposition:
      We choose a set of Op 2s. They cover $[1, P] \cup [S, N]$ where $P = \max(L_i-1)$ and $S = \min(R_i+1)$.
      If no Op 2s are chosen, $P=0, S=N+1$.
      Cost of Op 2s = $K_2$.
      Remaining uncovered: $[P+1, S-1]$.
      We must cover $[P+1, S-1]$ using Op 1s.
      Cost of Op 1s = Min number of Op 1s to cover $[P+1, S-1]$.
      
      Total Cost = $K_2 + K_1$.
      
      We iterate over all possible pairs $(P, S)$ that can be formed by some subset of Op 2s.
      Actually, $P$ is determined by the Op 2 with the largest $L_i-1$.
      $S$ is determined by the Op 2 with the smallest $R_i+1$.
      
      Let's precompute:
      $BestOp2ForPrefix[P]$: Min number of Op 2s to achieve prefix coverage $\ge P$.
      Since one Op 2 can cover any prefix up to $L_i-1$, if we just want to cover $[1, P]$, we need one Op 2 with $L_i-1 \ge P$.
      So $Cost2\_prefix(P) = 1$ if $\exists i$ (Op 2) with $L_i-1 \ge P$, else $\infty$.
      Similarly $Cost2\_suffix(S) = 1$ if $\exists i$ (Op 2) with $R_i+1 \le S$, else $\infty$.
      
      But we can use MULTIPLE Op 2s.
      If we use multiple Op 2s, the cost is the count.
      The union of prefixes is $[1, \max(L_i-1)]$.
      The union of suffixes is $[\min(R_i+1), N]$.
      
      So, if we choose a set of Op 2s, the cost is $|Set|$.
      The covered prefix is $[1, P]$ where $P = \max_{i \in Set} (L_i-1)$.
      The covered suffix is $[S, N]$ where $S = \min_{i \in Set} (R_i+1)$.
      
      We want to minimize $|Set| + \text{CoverMiddle}(P+1, S-1)$.
      
      Let's iterate over the "best" Op 2 for the prefix and "best" Op 2 for the suffix?
      No, we can pick any set.
      
      Note that if we pick a set of Op 2s, we can always replace it with a single Op 2 that has the max $L-1$ and min $R+1$?
      No, because the cost is the number of Op 2s.
      If we pick 2 Op 2s, cost is 2.
      If we pick 1 Op 2, cost is 1.
      
      So, for a fixed $P$ and $S$, what is the min cost to get prefix $\ge P$ and suffix $\le S$ using Op 2s?
      We need a set of Op 2s such that $\max(L_i-1) \ge P$ and $\min(R_i+1) \le S$.
      This requires at least one Op 2 with $L_i-1 \ge P$ AND at least one Op 2 with $R_i+1 \le S$.
      If one Op 2 satisfies both, cost is 1.
      If we need two different Op 2s, cost is 2.
      If no Op 2 satisfies $L_i-1 \ge P$, cost is $\infty$.
      If no Op 2 satisfies $R_i+1 \le S$, cost is $\infty$.
      
      So $Cost2(P, S) = $
        1 if $\exists i$ such that $L_i-1 \ge P$ AND $R_i+1 \le S$.
        2 if $\exists i$ with $L_i-1 \ge P$ AND $\exists j$ with $R_j+1 \le S$ (and no single one does both).
        $\infty$ otherwise.
        
      Then we minimize $Cost2(P, S) + CoverMiddle(P+1, S-1)$ over all $0 \le P < S \le N+1$.
      
      $CoverMiddle(l, r)$ is the min number of Op 1s to cover $[l, r]$.
      This is a standard interval covering problem.
      
      Steps:
      1. Precompute $CoverMiddle(l, r)$ for all $l, r$? No, $O(N^2)$.
         Instead, for a fixed $P$, we need $CoverMiddle(P+1, S-1)$.
         Let $Q = S-1$. We need $CoverMiddle(P+1, Q)$.
         
      2. Precompute $MinOp1Cover[l][r]$? No.
         Standard DP for interval covering:
         $DP1[i]$ = min Op 1s to cover $[1, i]$.
         But we need to cover $[l, r]$.
         Shifted: Min Op 1s to cover $[l, r]$ is equivalent to covering $[1, r-l+1]$ with shifted intervals?
         No, intervals are fixed.
         
         Let $G[l][r]$ be min Op 1s to cover $[l, r]$.
         We can compute $G[l][r]$ efficiently?
         Actually, we can compute $H[k]$ = min Op 1s to cover $[1, k]$.
         And $T[k]$ = min Op 1s to cover $[k, N]$.
         But $[P+1, Q]$ is a sub-interval.
         
         Let's compute $F[l][r]$? No.
         
         Alternative:
         Iterate $P$ from $0$ to $N$.
         Iterate $Q$ from $P$ to $N-1$ (where $Q = S-1$, so $S=Q+1$).
         We need $Cover(P+1, Q)$.
         
         Let's precompute $MinCover[l][r]$? Too big.
         
         However, note that $Cover(l, r)$ can be computed by:
         Find the Op 1 that starts $\le l$ and ends as far right as possible.
         This is standard greedy.
         
         But we need to query this for many pairs.
         
         Let's reverse:
         For each $P$, we want to find $Q \ge P$ that minimizes $Cost2(P, Q+1) + Cover(P+1, Q)$.
         
         $Cost2(P, Q+1)$ is 1, 2, or $\infty$.
         
         Case 1: $Cost2=1$.
         Condition: $\exists i$ with $L_i-1 \ge P$ and $R_i+1 \le Q+1$.
         Let $MaxL[P] = \max \{ L_i-1 \mid \text{Op 2 } i \}$.
         Let $MinR[Q+1] = \min \{ R_i+1 \mid \text{Op 2 } i \}$.
         Actually, let's define:
         $HasOp2Prefix[P]$: True if $\exists i$ with $L_i-1 \ge P$.
         $HasOp2Suffix[S]$: True if $\exists i$ with $R_i+1 \le S$.
         $HasOp2Both[P, S]$: True if $\exists i$ with $L_i-1 \ge P$ and $R_i+1 \le S$.
         
         We can precompute $HasOp2Both[P, S]$? No, $O(N^2)$.
         
         But notice:
         If $HasOp2Both[P, S]$ is true, cost is 1.
         Else if $HasOp2Prefix[P]$ and $HasOp2Suffix[S]$, cost is 2.
         
         Let's iterate $P$.
         For a fixed $P$, let $S_{min1}$ be the min $S$ such that $HasOp2Both[P, S]$ is true.
         If such $S$ exists, then for all $S \ge S_{min1}$, cost is 1.
         For $S < S_{min1}$ but $HasOp2Prefix[P]$ and $HasOp2Suffix[S]$, cost is 2.
         
         $S_{min1}$ for a fixed $P$:
         We need $\min \{ R_i+1 \mid L_i-1 \ge P \}$.
         Let $MinRForPrefix[P] = \min \{ R_i+1 \mid L_i-1 \ge P \}$.
         If no such Op 2, $\infty$.
         
         So for fixed $P$:
         If $MinRForPrefix[P] \le N+1$:
           For $S \in [MinRForPrefix[P], N+1]$, Cost2 = 1.
           We want to minimize $1 + Cover(P+1, S-1)$.
           Let $Q = S-1$. Range $Q \in [MinRForPrefix[P]-1, N]$.
           Minimize $Cover(P+1, Q)$.
         Else:
           Cost2 = 1 is impossible.
           
         If $HasOp2Prefix[P]$ and $HasOp2Suffix[S]$:
           Cost2 = 2.
           We want to minimize $2 + Cover(P+1, S-1)$.
           Range of $S$: $S \in [1, MinRForPrefix[P]-1]$ (if $MinRForPrefix[P] > 1$) and $HasOp2Suffix[S]$ is true.
           
      This is getting complex. Given time, I'll implement the $O(N \log N)$ or $O(N)$ approach for Cover and use the logic above.