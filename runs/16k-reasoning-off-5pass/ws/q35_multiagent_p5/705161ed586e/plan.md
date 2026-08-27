1. This problem can be solved using dynamic programming. We need to partition the string into groups where each group consists of identical characters and has length at least 3.
2. For each position i in the string, we consider all possible last groups ending at i. A group ending at i with character c must have length L >= 3. The group starts at index i-L+1.
3. The cost to change a substring to all character c is the sum of distances from each character in the substring to c (using the minimal steps: min(|ord(a)-ord(b)|, 26-|ord(a)-ord(b)|) but since we can only move to adjacent letters, the cost is actually the absolute difference in alphabet positions? No, the operation allows changing to prev or next, so the cost to change char x to y is min(|x-y|, 26-|x-y|)? Actually, re-reading: "change the character at that index to either the character immediately before or after". This means one operation changes a char to an adjacent char. So the cost to change char a to char b is the minimum number of steps, which is min(|ord(a)-ord(b)|, 26-|ord(a)-ord(b)|) if we could wrap around? But the problem says "if caption[i] != 'a'" for prev and "if caption[i] != 'z'" for next. This implies we cannot wrap around. So the cost is simply the absolute difference in ASCII values? Actually, no: to go from 'a' to 'c', you do 'a'->'b'->'c', cost 2. To go from 'c' to 'a', cost 2. The constraint is just that you can't go below 'a' or above 'z'. So the cost to change char x to y is abs(ord(x) - ord(y)).
4. We use DP[i] = minimum cost to make prefix s[0:i] a good caption. We also store the actual string or enough info to reconstruct it.
5. Since n is up to 50,000, an O(n^2) solution might be too slow if we iterate all group lengths. However, note that for a fixed end position and fixed character, the optimal group length is not necessarily bounded by a small constant. But we can optimize: for each ending position i, and for each character c, we want to find the best starting position j such that s[j:i+1] can be converted to c with minimal cost and length >= 3.
6. Actually, a better approach: iterate over all possible group characters (26) and all possible group lengths? That's still heavy. Instead, we can use DP where state is (index, last_char, current_run_length). But run_length can be up to n.
7. Alternative: Since each group must be >= 3, we can iterate i from 0 to n-1. For each i, try all possible last group lengths L from 3 to i+1. For each L, the group is s[i-L+1:i+1]. We try all 26 characters for this group. The cost is sum of abs(s[k] - c) for k in [i-L+1, i]. We take min over all L and c.
8. To make it efficient, note that for a fixed end i and fixed character c, the cost function for group starting at j is: cost(j, i, c) = sum_{k=j}^{i} abs(s[k] - c). We want min over j <= i-2 of (DP[j-1] + cost(j, i, c)). We can precompute prefix sums of abs(s[k] - c) for each c to compute cost in O(1).
9. Then DP[i] = min over c in 'a'..'z', over L from 3 to i+1: (DP[i-L] + cost(i-L+1, i, c)). Base case: DP[-1] = 0 (use a sentinel).
10. To reconstruct, store which (c, L) gave the minimum. Then backtrack.
11. Complexity: O(n * 26 * n) in worst case if we iterate L naively. But we can optimize: for fixed i and c, as L increases, the cost increases. But we need the minimum DP[i-L] + cost. We can't easily slide because DP[i-L] varies.
12. Given n=50,000, O(26*n^2) is too slow (6.5e9). We need a better approach.
13. Insight: The group length doesn't need to be arbitrarily large. Actually, it can be. But note that for a fixed character c, the cost to convert a segment to c is convex? Not exactly.
14. Alternative DP state: dp[i][c][l] = min cost for prefix i ending with character c and current run length l. l from 1 to n. State space 50000*26*50000 is too big.
15. We can limit l: once l >= 3, we can either extend or close the group. When we close, we transition to a new group. So state: dp[i][c] = min cost for prefix i where the last group ends at i with character c, and the last group has length >= 3. But we also need to know the current run length to extend.
16. Let dp[i][c] = min cost for prefix s[0:i] such that the last group (ending at i-1) has character c and length >= 3. And let extend[i][c][l] be too big.
17. Better: Let f[i][c] = min cost to make prefix s[0:i] good, with the last group having character c. But we don't know the length. We need to ensure the last group has length >= 3.
18. We can use: dp[i] = min over c, over L>=3: dp[i-L] + cost(i-L, i-1, c). With prefix sums for cost, each query is O(1). But iterating L is O(n). Total O(26*n^2).
19. Optimization: For fixed i and c, define g_i(c) = min_{L>=3} { dp[i-L] + cost(i-L, i-1, c) }. We can rewrite cost(i-L, i-1, c) = P[i][c] - P[i-L][c] where P[j][c] = sum_{k=0}^{j-1} abs(s[k]-c). Then g_i(c) = P[i][c] + min_{L>=3} { dp[i-L] - P[i-L][c] }. Let j = i-L, then j <= i-3. So g_i(c) = P[i][c] + min_{j=0}^{i-3} { dp[j] - P[j][c] }.
20. We can maintain for each character c, the minimum value of (dp[j] - P[j][c]) as j increases. Let min_val[c] = min_{j} (dp[j] - P[j][c]). Then when we compute dp[i], for each c, we update min_val[c] with j=i (after computing dp[i]), and for dp[i], we use min_val[c] from j <= i-3.
21. Algorithm:
    - Precompute P[i][c] for i from 0 to n, c from 'a' to 'z'. P[0][c]=0, P[i][c] = P[i-1][c] + abs(ord(s[i-1]) - ord(c)).
    - Initialize dp array of size n+1 with infinity. dp[0] = 0.
    - Initialize min_val[c] = infinity for each c. But note: for dp[i], we need min over j <= i-3. So we can update min_val after processing i-3.
    - Actually, we can iterate i from 0 to n. For i < 3, dp[i] = inf (except dp[0]=0).
    - Maintain an array best[c] which stores min_{j <= i-3} (dp[j] - P[j][c]). Initially, for i=0,1,2, best[c] = inf.
    - When i >= 3, before computing dp[i], we can update best[c] with j = i-3: best[c] = min(best[c], dp[i-3] - P[i-3][c]).
    - Then for each c, dp[i] = min(best[c] + P[i][c]).
    - Also store which c achieved the minimum for reconstruction.
22. After filling dp, if dp[n] is inf, return "".
23. Reconstruct: Start from i=n. Find c such that dp[n] = best_for_n[c] + P[n][c]. But best_for_n[c] corresponds to some j <= n-3. Actually, we need to store which j gave the minimum. So we store parent[i][c] = j that achieved the min.
24. Actually, we can store for each i, the chosen c and the corresponding j (which is i-L). Then backtrack.
25. Implementation: 
    - dp[0] = 0, dp[1..n] = inf.
    - best[c] = inf for all c. We also store best_j[c] = -1.
    - For i from 0 to n:
        - If i >= 3:
            - j = i-3
            - For each c: 
                - val = dp[j] - P[j][c]
                - if val < best[c]: best[c] = val, best_j[c] = j
        - If i >= 3:
            - For each c:
                - cost = best[c] + P[i][c]
                - if cost < dp[i]: dp[i] = cost, choice_c[i] = c, choice_j[i] = best_j[c]
    - Reconstruct: start at i=n. c = choice_c[n], j = choice_j[n]. The last group is s[j:i] converted to c. Then set i = j, repeat.
26. Edge: if dp[n] is inf, return "".