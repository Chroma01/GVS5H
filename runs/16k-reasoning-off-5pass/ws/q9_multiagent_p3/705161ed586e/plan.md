The problem requires transforming a string into a "good caption" (groups of at least 3 identical consecutive characters) with minimum operations, where an operation changes a character to an adjacent alphabet letter. Since we want the lexicographically smallest result, we should aim to convert the entire string to a single character (e.g., 'a') if possible, as this minimizes the cost per character change and guarantees the lexicographically smallest outcome. If converting to a single character is impossible (e.g., the string length is less than 3), we check if it's possible to form a valid group of 3 or more with some characters, but given the constraints and the nature of "groups of at least 3", a single character block of length n >= 3 is the most robust target. We need to check if the target character can be reached from all characters in the string; since we can move up or down, any character can reach any other, so reachability isn't the issue. The main constraint is the length: if n < 3, it's impossible. If n >= 3, the optimal strategy is to convert the whole string to 'a' (cost = sum of distances from each char to 'a') because 'a' is the smallest. Wait, re-reading the definition: "every character appears in groups of at least 3". This means the string can be "aaabbbccc", not necessarily all same. However, to minimize operations and get the lexicographically smallest, converting everything to 'a' (if n >= 3) is usually best. But what if the string is "zzzz"? Converting to 'aaa' costs 3 per 'z' -> 12 ops. Converting to 'zzz' (if n=4, "zzzz" is already good) costs 0. So we must consider the possibility that the original string is already good or can be made good with fewer ops by keeping some characters.
Actually, the optimal strategy for lexicographically smallest is to try to make the string all 'a's if n >= 3. Is there any case where making it all 'a's is worse than making it "aaabbb..."?
Consider "zzzz". All 'a's: cost 4*25 = 100. "zzzz": cost 0. "zzzz" is better.
So we need to find the target character `c` such that converting the entire string to `c` is valid (n >= 3) and the cost is minimized? No, we don't have to convert the *entire* string to one character. We just need *groups* of 3.
However, the problem asks for the *lexicographically smallest* good caption.
The lexicographically smallest string of length n is "aaa...a".
If we can make the string "aaa...a" (which is good if n >= 3), that is the absolute best candidate.
When can we make "aaa...a"? We can change any character to 'a' if it's reachable. Since we can move up/down, any char can become 'a'. The only constraint is the length. If n < 3, we cannot form a group of 3, so return "".
If n >= 3, "aaa...a" is always a valid good caption. Is it always the minimum cost? No, as seen with "zzzz".
But wait, the problem says "minimum number of operations".
So we have two objectives:
1. Minimize operations.
2. Among those with min operations, pick lexicographically smallest.

Let's re-evaluate "zzzz".
Option A: "zzzz" (0 ops). Good? Yes, 'z' appears in group of 4 >= 3.
Option B: "aaaa" (100 ops).
Min ops is 0. So "zzzz" is the answer.
What about "cdcd"?
Target "cccc": 2 ops.
Target "dddd": 2 ops.
Target "aaaa": c->a (2), d->a (3), c->a (2), d->a (3) = 10 ops.
So for "cdcd", "cccc" is better than "aaaa".
But "cccc" is lexicographically larger than "aaaa", but "aaaa" has higher cost. We prioritize cost.
So the strategy is:
Find the character `x` that minimizes the cost to convert the *entire* string to `x`? No, we don't have to convert the entire string to one character. We could have "aaabbb".
But "aaabbb" has cost: a's stay, b's come from somewhere.
Actually, the most efficient way to form groups is usually to pick a character that appears frequently or is close to many characters and expand it.
However, note that if we pick a target character `x`, and we decide to make the *whole* string `x`, the cost is sum(|s[i] - x|).
Is it ever beneficial to have multiple groups?
Suppose we have "ab". Length 2 -> impossible.
Suppose "abc". Length 3.
Target "aaa": cost 0+1+2=3.
Target "bbb": cost 1+0+1=2.
Target "ccc": cost 2+1+0=3.
Target "aaabbb" (length 6) impossible.
So for "abc", "bbb" is best (2 ops).
What if we do "aab"? Not good. "aaa" is good. "bbb" is good.
Is it possible to have a mix? e.g. "aaabb"? Length 5.
If input is "abcde", length 5.
Option 1: All 'b's: cost 1+0+1+2+3 = 7. String "bbbbb".
Option 2: "aaabb": cost to make first 3 'a's, last 2 'b's?
To make "aaabb":
Indices 0,1,2 -> 'a'. Cost: |a-a|+|b-a|+|c-a| = 0+1+2=3.
Indices 3,4 -> 'b'. Cost: |d-b|+|e-b| = 2+3=5. Total 8.
"bbbbb" cost 7.
It seems converting the whole string to a single character is often optimal or close to optimal.
Why? Because splitting the string into two groups means we pay the transition cost or just the distance to two different targets.
Actually, if we split, say into group of 'a's and 'b's, the characters in the 'a' group must be close to 'a', and 'b' group close to 'b'.
But if we just pick the median character of the string and convert everything to it, that minimizes the sum of absolute differences (1D median problem).
Let `x` be the character that minimizes sum(|s[i] - x|). This `x` is the median of the string's characters (mapped to 0-25).
Then the cost is sum(|s[i] - x|).
The resulting string is `x` repeated n times.
Is this always a good caption? Only if n >= 3.
If n < 3, return "".
If n >= 3, is it possible that a mixed string has lower cost?
Example: "a...a" (many a's) and "z...z" (many z's).
If we convert all to 'a', cost is high for z's.
If we convert all to 'z', cost is high for a's.
If we split: keep a's as a, keep z's as z?
But we need groups of 3.
If the string is "aaazzz", it's already good. Cost 0.
Our median approach: characters are [0,0,0,25,25,25]. Median is 25 (or 0, depending on definition, but any between 0 and 25 works).
If we pick 0 ('a'): cost = 0+0+0+25+25+25 = 75.
If we pick 25 ('z'): cost = 75.
If we pick 12 ('m'): cost = 12*6 = 72.
But the original "aaazzz" has cost 0.
So the "convert entire string to one char" strategy fails if the string is already a mix of valid groups.
However, the problem asks for the *lexicographically smallest* among those with *minimum* operations.
If the original string is already good, cost is 0, and we return the original string?
Wait, if there are multiple good captions with 0 ops, we return the lexicographically smallest. But if the input is already good, the only 0-op solution is the input itself.
So if input is "aaazzz", output "aaazzz".
If input is "aaazz", not good. We must change something.
Maybe change one 'z' to 'a'? "aaaaa" -> cost 1. Good.
Or change one 'a' to 'z'? "zzzzz" -> cost 1. Good.
"aaaaa" < "zzzzz". So "aaaaa".
So the strategy is:
1. Check if the string is already good. If yes, return it?
   Wait, is it possible that a non-zero cost transformation yields a lexicographically smaller string than the original (which is good)?
   Example: Input "zzzz". Good. Cost 0.
   Can we get something smaller with cost > 0? "yyyy" (cost 1 per char? no, z->y is 1). "yyyy" cost 4. "zzzz" cost 0.
   We prioritize min cost. So if 0 is possible, we must take 0.
   So if input is already good, return input.
   BUT, what if there are multiple ways to get 0 cost? Only the input itself has 0 cost.
   So if input is good, return input.
   
   What if input is not good?
   We need to find the minimum cost to make it good.
   Candidate 1: Convert entire string to a single character `c`. Cost = sum(|s[i] - c|). Valid if n >= 3.
   Candidate 2: Split into groups?
   Actually, if we split, we are essentially choosing a partition of the string indices into sets, each set converted to a character `c_k`.
   But to minimize cost, each set should be converted to the median of its original characters?
   And the sets must form contiguous groups of size >= 3?
   The problem says "groups of at least 3 consecutive occurrences". It doesn't say the groups must be contiguous blocks in the original string, but the resulting string must have them.
   So we can rearrange? No, we can only change characters, not swap. The positions are fixed.
   So we need to assign a target character `t_i` to each position `i` such that the resulting string `t_0 t_1 ... t_{n-1}` has the property that every character present forms a contiguous block of length >= 3.
   This implies the string looks like `c1...c1 c2...c2 ...` where each block length >= 3.
   To minimize cost, for a fixed partition of indices into blocks, we should pick the target character for each block to be the median of the original characters in that block.
   However, the number of partitions is huge.
   But notice: if we have a block of length >= 3, say from index `l` to `r`, the cost is sum_{i=l}^r |s[i] - c|.
   If we have multiple blocks, say [0, 2] and [4, 6], we solve independently.
   But we need to cover all indices.
   And the blocks must be contiguous segments of the string.
   So we are partitioning the string `s` into segments of length >= 3 (and possibly some segments of length < 3? No, every character must be in a group of >= 3. So every character must belong to some block of identical characters of length >= 3. This implies the entire string must be partitioned into blocks of length >= 3).
   Wait, if n=5, we can have one block of 5, or one block of 3 and one block of 2? No, the block of 2 is invalid.
   So the entire string must be partitioned into blocks of length >= 3.
   This is only possible if n >= 3.
   And if n=5, we can have [0,4] (len 5) or [0,2] and [3,4] (invalid). So only one block of 5.
   If n=6, [0,5] (len 6) or [0,2] and [3,5] (3+3).
   So we need to partition `n` into sums of integers >= 3.
   For each partition, we calculate the cost: sum of costs for each segment (where cost of segment is min_c sum |s[i]-c|).
   Then we pick the partition with minimum total cost.
   If ties, pick the lexicographically smallest resulting string.
   
   However, `n` up to 50,000. We need an efficient DP.
   Let `dp[i]` = (min_cost, lexicographically_smallest_string_suffix) for suffix starting at `i`.
   But storing strings is too expensive.
   We can store the cost and the "best" character choice for the first block.
   Actually, the structure of the optimal solution is likely simple.
   Consider the case where we convert the whole string to one character. Cost = sum |s[i] - c|. Best `c` is median.
   Is it ever better to split?
   Example: "aaazzz". n=6.
   Option 1: Whole string. Median of [0,0,0,25,25,25] is 25 (or 0). Cost 75.
   Option 2: Split into [0,2] and [3,5].
     Block 1: "aaa" -> target 'a', cost 0.
     Block 2: "zzz" -> target 'z', cost 0.
     Total cost 0.
   So splitting is crucial.
   
   Algorithm:
   1. If n < 3, return "".
   2. Check if the string is already good. If yes, return it?
      Wait, if input is "aaazzz", it's good. Cost 0.
      Is there any other good caption with cost 0? No.
      So return input.
      But what if input is "aaabbb"? Good. Return "aaabbb".
      What if input is "aaabb"? Not good.
      We need to fix it.
      
   DP State:
   `dp[i]` = minimum cost to make suffix `s[i:]` good.
   To compute `dp[i]`, we try all possible lengths `L` from 3 to `n-i`.
   The first block would be `s[i:i+L]`. We convert this block to a single character `c` that minimizes sum(|s[k]-c|) for k in `i..i+L-1`.
   Cost for this block = sum(|s[k]-c|).
   Then add `dp[i+L]`.
   We need to handle the lexicographical requirement.
   Since we want the lexicographically smallest string, and we are building from left to right, we should prefer smaller characters for the first block if costs are equal.
   However, the choice of `L` affects the subsequent blocks.
   This looks like a standard DP with tie-breaking.
   Given n=50000, O(n^2) is too slow.
   We need to optimize the transition.
   Notice that for a fixed length `L`, the optimal character `c` is the median of `s[i:i+L]`.
   Also, the cost function is convex.
   Is it possible that we only need to consider specific lengths?
   Actually, maybe the optimal solution always consists of blocks of length exactly 3? Or maybe just one big block?
   In "aaazzz", blocks of 3 are optimal.
   In "aaaaaa", one block of 6 (cost 0) or two blocks of 3 (cost 0).
   Lexicographically: "aaaaaa" vs "aaa" + "aaa" -> "aaaaaa" is the same.
   What if "aaabbb"? "aaabbb" vs "aaa" + "bbb" -> same.
   What if "aaaccc"? Same.
   What if "aaabbc"? Not good.
   Maybe the optimal strategy is to find the best single character `c` for the whole string, and compare with splitting into 3s?
   Actually, consider the cost function.
   Cost of block of length L with median `m`: sum |x - m|.
   If we split a block of length L into two blocks of length L1 and L2, the cost is sum(|x1-m1|) + sum(|x2-m2|).
   Generally, splitting reduces cost if the characters in the two halves are far apart.
   The maximum reduction is when we have distinct clusters.
   
   Given the constraints and the nature of the problem, maybe we can observe that the optimal solution is either:
   1. The entire string converted to the global median.
   2. The string split into blocks of 3s, where each block is converted to its local median.
   
   Let's test this hypothesis.
   Suppose we have a block of 4: "aabb".
   Option 1: Convert to one char. Median of [0,0,1,1] is 0 or 1. Cost 2. Result "aaaa" or "bbbb".
   Option 2: Split into 3+1? No, 1 is invalid.
   So for length 4, must be one block.
   Length 5: "aaabb".
   Option 1: One block. Median 1 ('b'). Cost: |0-1|*2 + |1-1|*3 = 2. Result "bbbbb".
   Option 2: Split 3+2? Invalid.
   So for length 5, must be one block.
   Length 6: "aaabbb".
   Option 1: One block. Median 1. Cost: 3*1 + 3*0 = 3. Result "bbbbbb".
   Option 2: Split 3+3. Block 1 "aaa" -> 'a', cost 0. Block 2 "bbb" -> 'b', cost 0. Total 0.
   So splitting is better.
   
   It seems we only need to consider splits into blocks of size 3?
   What about size 4? "aaab". Must be one block.
   Size 5? "aaabb". Must be one block.
   Size 6? Can be 3+3 or 6.
   Size 7? 3+4 (4 must be one block) or 7.
   So generally, we can have blocks of size >= 3.
   But if we have a block of size 4, 5, etc., can we split it further?
   Size 4: cannot split into >=3.
   Size 5: cannot split.
   Size 6: can split into 3+3.
   Size 7: 3+4? 4 is a block. Or 7.
   So the decomposition is into blocks of size 3 and possibly one larger block at the end?
   Actually, if we have a block of size 4, we can't split it. So it stays as 4.
   But is it ever optimal to have a block of size 4?
   Compare "aaab" (len 4) -> "aaaa" (cost 1) vs "bbbb" (cost 1).
   If we had "aaab" as part of a larger string, say "aaabbb".
   Split: "aaa" (0) + "bbb" (0) = 0.
   If we forced "aaab" as a block, cost 1, then "b" left? No, must cover all.
   So "aaabbb" -> "aaa" + "bbb" is better than "aaabbb" (one block).
   What if "aaabbc"? Len 6.
   Split 3+3: "aaa"->'a' (0), "bbc"-> median 'b' (cost |1-1|+|2-1|+|2-1|=2). Total 2.
   One block: "aaabbc". Median 'b'. Cost: |0-1|*2 + 0 + |2-1|*2 = 2+2=4.
   Split is better.
   
   Hypothesis: The optimal solution partitions the string into blocks of size 3, except possibly the last block which might be larger?
   Actually, if we have a remainder of 4, 5, we can't split it into 3s.
   But maybe we can merge the last 4 into the previous 3? Making a 7?
   Or maybe the optimal is always to use blocks of size 3?
   If n % 3 == 0, all 3s.
   If n % 3 == 1, we have one block of 4? Or one block of 7? Or one block of 10?
   Actually, if we have a block of 4, cost is sum |x-m|.
   If we have a block of 7, cost is sum |x-m|.
   Is it ever better to have a block of 4 than a block of 3 + something?
   If n=4, must be 4.
   If n=7, options: 7, or 4+3, or 3+4.
   Compare 4+3 vs 7.
   Example: "aaabbbccc" (n=9). All 3s -> cost 0.
   Example: "aaabbbcc" (n=8).
   Options: 3+5 (5 must be one block), 4+4, 8.
   3+5: "aaa" (0) + "bbcc" (median 'b' or 'c'). "bbcc" -> 'b': |0|+|1|+|1|+|2| = 4? No, indices: b,b,c,c. Values 1,1,2,2. Median 1 or 2. Cost 2. Total 2.
   4+4: "aaab" -> 'a' (1) + "bbcc" -> 2. Total 3.
   8: "aaabbbcc" -> median 'b'. Cost: 2*1 + 3*0 + 2*1 = 4.
   So 3+5 is best.
   So it seems we should try to maximize the number of 3s.
   The only exception is when n % 3 != 0.
   If n % 3 == 1, we have one block of 4? Or maybe we can have one block of 7?
   Actually, if we have a block of 4, we can't split it.
   But maybe we can shift the boundary?
   Actually, the DP state `dp[i]` = min cost for suffix `i`.
   Transitions: `dp[i] = min_{L=3..n-i} (cost(i, i+L) + dp[i+L])`.
   Since n=50000, we need O(n) or O(n log n).
   Observation: The cost function `cost(i, i+L)` is convex with respect to L? Not necessarily.
   However, note that if we have a block of size L, and L >= 3, we can always split it into 3 and L-3 if L-3 >= 3.
   If L-3 < 3, we can't split.
   So the only "atomic" blocks that cannot be split further are of size 3, 4, 5.
   Wait, if we have a block of 6, we can split into 3+3.
   If we have 7, 3+4 or 4+3.
   If we have 8, 3+5 or 5+3 or 4+4.
   It seems the optimal partition will consist of blocks of size 3, and at most one block of size 4 or 5?
   Actually, if we have a block of 4, can we merge it with a neighbor 3 to make 7?
   Maybe the optimal is to have as many 3s as possible, and the remainder handled by a single block of size 4 or 5?
   Let's check n=4: must be 4.
   n=5: must be 5.
   n=6: 3+3 or 6. 3+3 is better usually.
   n=7: 3+4 or 4+3 or 7.
   n=8: 3+5 or 5+3 or 4+4 or 8.
   n=9: 3+3+3 or 3+6 (6->3+3) -> all 3s.
   
   So the strategy:
   We can iterate over the possible "remainder" block size.
   The remainder block size can be 3, 4, 5.
   Why? Because any block of size >= 6 can be split into 3 + (size-3), and since size-3 >= 3, we can recursively split until we get 3s and a remainder of 3, 4, or 5.
   Wait, is it always better to split?
   Splitting a block of size L into 3 and L-3:
   Cost(L) vs Cost(3) + Cost(L-3).
   Cost(L) = sum |x - m_L|.
   Cost(3) + Cost(L-3) = sum |x1 - m1| + sum |x2 - m2|.
   By triangle inequality / convexity, splitting usually reduces cost if the two halves have different medians.
   If the medians are the same, cost is same.
   If medians are different, splitting reduces cost.
   So we should always split if possible.
   Therefore, the optimal partition will consist of blocks of size 3, and at most one block of size 4 or 5 (if n % 3 == 1 or 2).
   Specifically:
   If n % 3 == 0: All 3s.
   If n % 3 == 1: One block of 4, rest 3s. (Or maybe one block of 7? No, 7 = 3+4, and 3+4 <= 7).
   If n % 3 == 2: One block of 5, rest 3s. (Or 8 = 3+5).
   
   So we only need to consider two cases for the "remainder":
   Case 1: The last block is of size 4 (if n%3==1). The rest are 3s.
   Case 2: The last block is of size 5 (if n%3==2). The rest are 3s.
   Wait, the remainder block could be at the beginning too?
   Yes, "4 + 3 + 3..." or "3 + 3 + ... + 4".
   So we need to check:
   1. All 3s (if n%3==0).
   2. One block of 4, rest 3s. The block of 4 can be at any position `i` such that `i` is multiple of 3? No, the blocks must be contiguous.
      So the partition is: 3, 3, ..., 4, 3, ...
      The position of the 4-block can be anywhere.
      But wait, if we have a 4-block, the previous block must end at `i-1`, so `i` must be such that `i` is a multiple of 3?
      No, the blocks are just segments.
      If we have one 4-block and the rest 3s, then the total length is 3*k + 4 = n.
      The 4-block can start at index `3*j` for some `j` from 0 to `k`.
      So we need to check all possible positions for the 4-block (if n%3==1) and 5-block (if n%3==2).
      And also the "all 3s" case if n%3==0.
      
   Algorithm refined:
   1. If n < 3: return "".
   2. Precompute prefix sums of characters (mapped to 0-25) to quickly calculate sum and median for any range.
      Actually, to find the median and cost for a range in O(1), we can use prefix sums of the values and prefix sums of the counts?
      For a range [l, r], we want `m` that minimizes sum |x - m|. `m` is the median.
      If the range has odd length, median is the middle element.
      If even, any value between the two middle elements works. We pick the smaller one for lexicographical?
      Actually, for cost calculation, any median in the range [mid1, mid2] gives the same cost.
      For lexicographical result, if we have a choice of `m`, we pick the smallest `m`.
      So for even length, `m` = element at index `len//2` (0-based in sorted list)?
      Actually, if sorted values are v0, v1, ..., v_{k-1}.
      If k is odd, median is v_{k//2}.
      If k is even, any value in [v_{k//2 - 1}, v_{k//2}] works. To minimize the resulting character, we pick v_{k//2 - 1}.
      But we need the cost. Cost is sum |x - m|.
      We can compute this using prefix sums.
      Let `P[i]` = sum of s[0..i-1].
      Sum of range [l, r] = P[r+1] - P[l].
      To find median and cost efficiently:
      We need the k-th smallest element in the range. This is hard in O(1).
      However, n=50000. We can precompute the sorted version of each window? No, too slow.
      But notice: the windows we need are mostly length 3.
      Only one window is length 4 or 5.
      So we can just iterate over all possible positions for the special block (4 or 5) and compute the cost in O(L) where L is 4 or 5.
      The rest are length 3. We can precompute the cost for all length 3 blocks in O(n).
      
      Steps:
      1. Precompute `cost3[i]` = cost to convert s[i:i+3] to its median.
         For each i from 0 to n-3:
           chars = s[i], s[i+1], s[i+2]
           median = sorted(chars)[1]
           cost3[i] = abs(s[i]-median) + abs(s[i+1]-median) + abs(s[i+2]-median)
      2. If n % 3 == 0:
         Option A: All 3s. Cost = sum(cost3[i] for i in 0, 3, 6, ...).
         Result string: construct by taking median of each block.
         Since all blocks are 3, we just concatenate the medians.
         This is the only candidate.
      3. If n % 3 == 1:
         We need one block of 4.
         Iterate `j` from 0 to `n-4` with step 3.
           The block of 4 starts at `j`.
           Cost = sum(cost3[k] for k in 0,3,..., j-3) + cost4(j) + sum(cost3[k] for k in j+4, j+7, ...)
           Where `cost4(j)` is cost to convert s[j:j+4] to median.
           Keep track of min cost and the resulting string.
         Also, we need to construct the string for the best option.
         Since we want lexicographically smallest, if costs are equal, pick the one with smaller character at the first difference.
         The first difference will be in the special block or the blocks around it.
         Actually, we can just store the best cost and the starting index of the special block.
         Then reconstruct.
         But wait, if costs are equal, which one is lexicographically smaller?
         The string is determined by the medians of the blocks.
         If we have a block of 4, its median might be different from a block of 3.
         We need to compare the full strings.
         Since n is large, we can't generate all strings.
         But the difference will be localized.
         We can compare the two candidates by finding the first index where they differ.
         The candidates differ only in the region of the special block and possibly the adjacent blocks if the partition shifts?
         No, the partition is fixed: all 3s except one 4.
         The only variable is the position of the 4.
         So we compare the string generated by position `j1` vs `j2`.
         They will be identical except in the range [j1, j1+3] and [j2, j2+3] and the blocks in between?
         Actually, if we shift the 4-block, the 3-blocks shift.
         Example: n=7.
         Pos 0: 4, 3. String: M4 M3.
         Pos 3: 3, 4. String: M3 M4.
         They differ at index 0 vs 3.
         We can compute the cost for each position, find the min cost, then among those with min cost, find the lexicographically smallest.
         To do this efficiently:
         Compute `min_cost`.
         Then iterate again to find the best position.
         Or store the best position during the first pass, but handle ties.
         Since the number of positions is O(n), and comparing two strings takes O(n), total O(n^2) is bad.
         But we only need to compare the best candidates.
         Actually, we can compute the "lexicographical rank" incrementally?
         Simpler: Since we only have one special block, the string is mostly composed of 3-block medians.
         The 3-block medians are fixed except for the ones overlapping the special block.
         Actually, the partition is:
         [0, 3), [3, 6), ..., [j, j+4), ..., [j+4, j+7), ...
         The blocks are fixed in size, just the one block of 4 moves.
         The medians of the 3-blocks are independent of the 4-block position, EXCEPT that the 3-blocks are defined by the partition.
         Wait, if the 4-block is at `j`, then the block before it is `[j-3, j)`, and after is `[j+4, j+7)`.
         If the 4-block is at `j+3`, the block before is `[j, j+3)`, and after is `[j+7, j+10)`.
         So the set of 3-blocks changes.
         However, note that the 3-blocks are just consecutive triplets.
         The only difference is that one triplet is merged into a 4-block.
         So the string is composed of medians of triplets, except one 4-block.
         We can compute the cost for each position `j` in O(1) using precomputed prefix sums of `cost3`?
         Yes, `cost3` array is precomputed.
         `total_cost(j) = prefix_cost3[j] + cost4(j) + suffix_cost3[j+4]`.
         We can compute this in O(1) per `j`.
         Then find `j` with min cost.
         If multiple `j` have min cost, we need to pick the lexicographically smallest string.
         To compare two strings with min cost efficiently:
         The strings differ only in the region around the special block.
         Specifically, if we compare `j1` and `j2`, the blocks before `min(j1, j2)` are identical.
         The blocks after `max(j1, j2) + 4` are identical.
         The difference is in the middle.
         We can compare the medians of the blocks in the range `[min(j1, j2), max(j1, j2) + 4]`.
         Since the range is small (at most 10), we can just generate the substring and compare.
         So:
         1. Find all `j` with min cost.
         2. For each such `j`, generate the string (or just the differing part) and compare.
         Since the number of min-cost positions might be large, but the differing part is small, we can optimize.
         Actually, we can just generate the full string for the first candidate, and for subsequent candidates, compare only the differing part.
         But generating the full string is O(n). If there are many candidates, O(n^2).
         However, the number of candidates with min cost is likely small? Or we can avoid generating.
         We can compare two candidates by finding the first index where they differ.
         The first difference must be within the range of the two special blocks.
         So we can compare in O(1) (constant range) if we know the medians.
         We can precompute the median for every possible 3-block and 4-block.
         Then for two candidates `j1` and `j2`, we compare the sequence of medians.
         The sequence of medians is the same except for the blocks involved in the shift.
         We can implement a custom comparator that checks the range.
         
         Implementation details:
         - Precompute `med3[i]` = median of s[i:i+3].
         - Precompute `cost3[i]`.
         - Precompute `med4[i]` = median of s[i:i+4] and `cost4[i]`.
         - Compute prefix sums of `cost3`.
         - Iterate `j` to find min cost.
         - Collect all `j` with min cost.
         - If only one, done.
         - If multiple, compare them.
           To compare `j1` and `j2` (assume `j1 < j2`):
           The blocks before `j1` are same.
           Blocks from `j1` to `j2+3` might differ.
           Actually, the partition for `j1`: ..., [j1, j1+4), [j1+4, j1+7), ...
           Partition for `j2`: ..., [j1, j1+3), [j1+3, j1+6), ..., [j2, j2+4), ...
           The difference starts at `j1`.
           We can simulate the generation of the string up to `j2+4` and compare.
           Since the range is small (at most 10 blocks), this is O(1).
           Once we find the best `j`, generate the full string.
         
         Special case: n % 3 == 2.
         Similar logic, but block of 5.
         Precompute `med5`, `cost5`.
         Iterate `j` for 5-block.
         
         Edge case: n < 3 -> "".
         Also, check if the original string is already good?
         Our DP approach covers that?
         If the original string is good, then the cost for the optimal partition should be 0.
         And our method will find it (since we check all partitions of 3s and one 4/5).
         Wait, if the string is "aaazzz", n=6.
         Our method checks 3+3.
         Block 1 "aaa" -> 'a', cost 0.
         Block 2 "zzz" -> 'z', cost 0.
         Total 0.
         Result "aaazzz". Correct.
         What if "aaazz"? n=5.
         Check 5-block. "aaazz" -> median 'a' or 'z'?
         Sorted: a,a,a,z,z. Median 'a'.
         Cost: 0+0+0+1+1 = 2.
         Result "aaaaa".
         Is there a better partition? No, only 5-block possible.
         So "aaaaa" is returned.
         But is "aaazz" good? No.
         So we must change.
         Is "aaaaa" the best?
         What about "aaazz" -> change last 'z' to 'a'? "aaaaa". Cost 2.
         Change first 'a' to 'z'? "zzzzz". Cost 2.
         "aaaaa" < "zzzzz". Correct.
         
         One more check: "aaabbb". n=6.
         3+3: "aaa"->'a' (0), "bbb"->'b' (0). Total 0.
         Result "aaabbb". Correct.
         
         So the algorithm seems solid.

```python
class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        
        # Precompute medians and costs for length 3
        med3 = [0] * (n - 2)
        cost3 = [0] * (n - 2)
        for i in range(n - 2):
            chars = [ord(caption[i]), ord(caption[i+1]), ord(caption[i+2])]
            chars.sort()
            m = chars[1]
            med3[i] = chr(m)
            cost3[i] = abs(ord(caption[i]) - m) + abs(ord(caption[i+1]) - m) + abs(ord(caption[i+2]) - m)
        
        # Precompute for length 4
        med4 = [0] * (n - 3)
        cost4 = [0] * (n - 3)
        for i in range(n - 3):
            chars = [ord(caption[i]), ord(caption[i+1]), ord(caption[i+2]), ord(caption[i+3])]
            chars.sort()
            # For even length, pick the smaller median for lexicographical smallest result
            m = chars[1] 
            med4[i] = chr(m)
            cost4[i] = abs(ord(caption[i]) - m) + abs(ord(caption[i+1]) - m) + abs(ord(caption[i+2]) - m) + abs(ord(caption[i+3]) - m)
            
        # Precompute for length 5
        med5 = [0] * (n - 4)
        cost5 = [0] * (n - 4)
        for i in range(n - 4):
            chars = [ord(caption[i]), ord(caption[i+1]), ord(caption[i+2]), ord(caption[i+3]), ord(caption[i+4])]
            chars.sort()
            m = chars[2]
            med5[i] = chr(m)
            cost5[i] = sum(abs(ord(caption[i+k]) - m) for k in range(5))
            
        # Helper to get cost of a block
        def get_cost(start, length):
            if length == 3:
                return cost3[start]
            elif length == 4:
                return cost4[start]
            elif length == 5:
                return cost5[start]
            return 0

        # Helper to get median char of a block
        def get_med(start, length):
            if length == 3:
                return med3[start]
            elif length == 4:
                return med4[start]
            elif length == 5:
                return med5[start]
            return ''

        # Prefix sums for cost3
        pref3 = [0] * (n + 1)
        for i in range(n - 2):
            pref3[i+1] = pref3[i] + cost3[i]
        # pref3[k] = sum of cost3[0..k-1]
        
        min_total_cost = float('inf')
        best_j = -1
        
        if n % 3 == 0:
            # Only all 3s
            total = pref3[n//3] # Wait, pref3 index logic
            # pref3[i] is sum of first i cost3's.
            # We need sum of cost3[0], cost3[3], cost3[6]...
            # My pref3 is contiguous. This is wrong.
            # We need to sum cost3 at indices 0, 3, 6...
            # Let's recompute sum for specific pattern.
            pass
            
        # Correct approach:
        # We need to sum cost3 at indices 0, 3, 6...
        # Let's create a new prefix sum for the sequence of 3-blocks.
        # blocks_3_cost[i] = cost3[i] if i%3==0 else 0? No.
        # The blocks are at 0, 3, 6...
        # So we need sum of cost3[0] + cost3[3] + ...
        # Let's just compute the total cost for the "all 3s" case directly.
        
        # Actually, let's just iterate and compute total cost on the fly for the candidate.
        # Since we only have one special block, we can compute total cost in O(n) once, then O(1) for others?
        # No, O(n) for each candidate is O(n^2).
        # We need O(1) update.
        # Total cost = sum(cost3[0], cost3[3], ...) + cost_special + sum(cost3[...])
        # We can precompute the sum of cost3 at indices 0, 3, 6...
        # Let P3[i] = sum_{k=0}^{i-1} cost3[3*k]
        
        P3 = [0] * (n // 3 + 2)
        for i in range(n // 3):
            P3[i+1] = P3[i] + cost3[3*i]
            
        min_total_cost = float('inf')
        candidates = []
        
        if n % 3 == 0:
            # All 3s
            total = P3[n//3]
            if total < min_total_cost:
                min_total_cost = total
                candidates.append(0) # 0 means no special block
            elif total == min_total_cost:
                candidates.append(0)
                
        if n % 3 == 1:
            # One block of 4
            # Iterate j from 0 to n-4 with step 3
            # The 4-block is at j.
            # Blocks before: 0, 3, ..., j-3. Count = j/3.
            # Blocks after: j+4, j+7, ...
            # Number of 3-blocks before = j // 3
            # Number of 3-blocks after = (n - 4 - j) // 3
            # Total cost = P3[j//3] + cost4[j] + (P3[n//3] - P3[j//3 + 1])? 
            # Wait, P3[k] sums first k blocks (indices 0, 3, ..., 3*(k-1)).
            # We need sum up to index j-3. The index is j-3. The block number is (j-3)//3 = j//3 - 1.
            # So sum before = P3[j//3].
            # Sum after: total blocks = n//3. We used j//3 blocks before. So remaining = n//3 - j//3.
            # But we also have the block at j+4?
            # The blocks after start at j+4. The first block after is at index j+4.
            # The block numbers are j//3 + 1, j//3 + 2, ...
            # The last block number is n//3.
            # So sum after = P3[n//3] - P3[j//3 + 1].
            # Total = P3[j//3] + cost4[j] + (P3[n//3] - P3[j//3 + 1])
            
            total_blocks = n // 3
            for j in range(0, n - 3, 3): # j can be 0, 3, 6...
                # Check if j+4 <= n
                if j + 4 > n:
                    break
                cost_before = P3[j//3]
                cost_after = P3[total_blocks] - P3[j//3 + 1]
                current_cost = cost_before + cost4[j] + cost_after
                if current_cost < min_total_cost:
                    min_total_cost = current_cost
                    candidates = [j]
                elif current_cost == min_total_cost:
                    candidates.append(j)
                    
        if n % 3 == 2:
            # One block of 5
            total_blocks = n // 3
            for j in range(0, n - 4, 3):
                if j + 5 > n:
                    break
                cost_before = P3[j//3]
                cost_after = P3[total_blocks] - P3[j//3 + 1]
                current_cost = cost_before + cost5[j] + cost_after
                if current_cost < min_total_cost:
                    min_total_cost = current_cost
                    candidates = [j]
                elif current_cost == min_total_cost:
                    candidates.append(j)
                    
        # Now find lexicographically smallest among candidates
        if not candidates:
            return "" # Should not happen if n>=3
            
        best_j = candidates[0]
        for j in candidates[1:]:
            # Compare string generated by best_j and j
            # Generate up to the differing point
            # The differing point is around max(best_j, j)
            # We can compare block by block
            # Let's generate the full string for best_j first? No, too slow if many candidates.
            # But number of candidates is at most n/3.
            # Comparing two strings of length n is O(n). Total O(n^2).
            # We need O(1) comparison.
            # The strings differ only in the range [min(best_j, j), max(best_j, j) + 5].
            # We can compare the medians in this range.
            
            # Let's implement a function to compare two candidates
            def compare(j1, j2):
                # Returns True if j1 < j2 lexicographically
                # Find the first index where they differ
                # The blocks before min(j1, j2) are same.
                # The blocks after max(j1, j2) + 5 are same.
                # We need to compare from min(j1, j2) to max(j1, j2) + 5
                start = min(j1, j2)
                end = max(j1, j2) + 5
                # Generate the substring for both in this range and compare
                # But generating is O(end-start) which is small constant (~10)
                # So it's O(1).
                
                # Construct the sequence of characters for j1 and j2 in range [start, end]
                # For a candidate j, the blocks are:
                # ... [start, start+3), [start+3, start+6)...
                # But one block is special.
                # We can simulate the generation.
                
                # Actually, we can just generate the full string for the best candidate found so far,
                # and for each new candidate, compare only the differing part.
                # But we need to store the best_j's string? No, we can regenerate the differing part.
                
                # Let's just generate the full string for the current best_j and compare with new j.
                # Since we only do this for ties, and ties are rare?
                # But worst case all costs equal.
                # We need O(1) comparison.
                
                # Compare block by block
                # The blocks are defined by the partition.
                # For j1: blocks at 0,3,..., j1-3, j1 (size 4/5), j1+4 (size 3), ...
                # For j2: blocks at 0,3,..., j2-3, j2 (size 4/5), ...
                # The first difference is at min(j1, j2).
                # We can compare the characters at each index from min(j1, j2) to max(j1, j2)+5.
                
                # Let's write a helper to get char at index k for candidate j
                def get_char(k, j):
                    # Determine which block k belongs to
                    if j == 0: # No special block (n%3==0 case)
                        block_idx = k // 3
                        if block_idx >= len(med3):
                            return ''
                        return med3[block_idx]
                    else:
                        # Special block at j
                        # Blocks before j: 0, 3, ..., j-3
                        # Block index for k < j: k // 3
                        if k < j:
                            return med3[k//3]
                        elif k < j + (5 if n%3==2 else 4):
                            return med4[j] if n%3==1 else med5[j]
                        else:
                            # After special block
                            # The next block starts at j + (5 if n%3==2 else 4)
                            # Its index in med3 is (j + offset) // 3
                            offset = 5 if n%3==2 else 4
                            return med3[(j + offset + (k - (j + offset))) // 3] # Wait, logic error
                            # The block index after special block:
                            # The special block ends at j+4 (or 5).
                            # The next block starts at j+4.
                            # Its index in med3 is (j+4)//3.
                            # The block index for k is (j+4 + (k - (j+4))) // 3 = (k - 4) // 3? No.
                            # Let's recompute:
                            # Blocks: 0,3,6... j-3 (end j), j (len 4), j+4 (start), j+7...
                            # For k >= j+4:
                            # Block index = (k - (j+4)) // 3 + (j//3 + 1)
                            # = k//3 - (j+4)//3 + j//3 + 1
                            # = k//3 - j//3 - 1 + j//3 + 1 = k//3?
                            # Yes, because j is multiple of 3.
                            # So for k >= j+4, block index is k//3.
                            return med3[k//3]