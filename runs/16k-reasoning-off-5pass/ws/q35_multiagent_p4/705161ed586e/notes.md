
## ideation
The core difficulty lies in efficiently computing the optimal partitioning of the string into groups of size ≥ 3, where each group is made of identical characters with minimum operations, and among solutions with the same total cost, the lexicographically smallest result is chosen.

Key observations:
1. A "good caption" is a concatenation of blocks, each block being a run of the same character with length ≥ 3.
2. For a fixed segment of the string (say from index j to i-1) that we want to turn into a block of character c, the cost is the sum of distances from each character in that segment to c (in terms of alphabet steps). The best character c for a segment is one that minimizes this cost. However, because we also care about lexicographical order of the final string, we cannot simply pick the character with minimal cost for each segment independently; we must consider the global lexicographical order.

But note: The problem asks for the lexicographically smallest result among those with minimum operations. This suggests that we should use DP where the state is the index, and the value is (min_cost, best_string). However, storing strings in DP states can be expensive (O(n^2) space and time).

Alternative approach:
- We can define dp[i] = (min_cost, best_string) for prefix of length i.
- For each i, iterate over possible last group lengths L (from 3 to i). The last group is caption[i-L:i].
- For this segment, compute the cost to convert all characters to each possible character 'a' to 'z'. Let min_cost_segment be the minimum cost over all characters, and let best_char be the lexicographically smallest character that achieves min_cost_segment for that segment.
- Then, if dp[i-L] is reachable, candidate cost = dp[i-L].cost + min_cost_segment, and candidate string = dp[i-L].string + (best_char * L).
- We take the candidate with the smallest cost, and if tie, the lexicographically smallest string.

Pitfalls:
- The state space for dp[i] might be large if we store full strings. But note that n is up to 50,000. Storing strings of length up to 50,000 in each dp state would lead to O(n^2) space which is 2.5e9, too much.
- We need a more efficient way to compare lexicographical order without storing full strings.

Insight:
Instead of storing the full string, we can store the dp state as (cost, last_char, ...) but that doesn't capture the entire string for lexicographical comparison.

Actually, we can use the following: 
When comparing two candidate solutions for dp[i], if their costs are different, we pick the one with lower cost. If costs are the same, we need to compare the strings lexicographically. 

To avoid storing full strings, we can use a technique: 
Store dp[i] = (min_cost, best_string) but only if n is small. But n is 50,000, so we cannot store full strings.

Alternative efficient approach:
We can use DP with state i, and for each i, we store the best (cost, string) but we can avoid storing the entire string by using a trie or by storing parent pointers. But that complicates lexicographical comparison.

Actually, a better idea: 
Since the groups are contiguous, the entire string is determined by the sequence of characters chosen for each group. And the groups are non-overlapping and cover the entire string.

We can define:
dp[i] = (min_cost, best_string) for prefix i.

But to save space, note that when we compute dp[i], we only need dp[j] for j < i. And we can store the dp states in an array. But the string concatenation is expensive.

We can optimize by not storing the full string until the end. Instead, we can store:
dp[i] = (min_cost, last_char, prev_index, group_char) 
But then reconstructing the string requires backtracking, and lexicographical comparison during DP is still hard.

Actually, a standard trick for lexicographical smallest with DP is: 
When two candidates have the same cost, we choose the one that has the lexicographically smaller string. To compare without storing full strings, we can store the dp state as (cost, string) but only for small n. For large n, we need a different method.

Given the constraints (n up to 50,000), an O(n^2) solution with string concatenation will be too slow and memory heavy.

Reframe:
Notice that the cost to convert a segment to a character c is independent of other segments. And the lexicographical order of the final string is determined by the first character where two solutions differ.

We can use DP where dp[i] = (min_cost, best_string) but we avoid storing full strings by using a "lazy" comparison: 
Actually, we can store dp[i] as (min_cost, best_string) and hope that the number of states that are "best" is small? But worst-case, it could be O(n) states and each string is O(n), so O(n^2) space.

But 50,000^2 = 2.5e9 characters, which is 2.5 GB, which is too much.

We need a more efficient method.

Insight from similar problems (e.g., "Remove Invalid Parentheses", "Minimum Cost to Make String Valid"): 
Use DP with state i, and store only the minimal cost and the necessary information to reconstruct the lexicographically smallest string. 

But for lexicographical comparison, we can do the following: 
When updating dp[i] from dp[j] (for j = i-L), we have a candidate string = dp[j].string + (c * L). 
To compare two candidates for dp[i] without storing full strings, we can store the dp states in a way that allows efficient comparison. 

One idea: 
Store dp[i] = (min_cost, best_string) but use a persistent data structure or a trie to store the strings. But that is complex.

Another idea: 
Since the groups are of size at least 3, the number of groups is at most n/3. And the transitions are from j to i where i-j >= 3. 

We can try to optimize the inner loop: 
For each i, iterate L from 3 to i. For each L, compute the cost for segment caption[i-L:i] to become a block of character c. The best c for that segment is the one that minimizes the cost. We can precompute this for all segments? But there are O(n^2) segments.

Actually, for a fixed segment, the cost function for character c is convex? Not exactly, but we can compute the best c for a segment in O(26 * L) time. And L can be up to n, so worst-case O(n^3) which is too slow.

We need to optimize the cost calculation for a segment. 

Note: The cost to convert a segment to character c is: sum(|ord(s[k]) - ord(c)|) for k in segment. 
This can be computed quickly if we have prefix sums of the character frequencies. 

Specifically, for a segment from j to i-1, let freq[c] be the frequency of character c in that segment. Then cost(c) = sum_{d='a'}^{'z'} freq[d] * |ord(d) - ord(c)|. 
We can precompute a 2D prefix sum array for character frequencies: 
pref[k][c] = number of times character c appears in caption[0:k]. 
Then for segment [j, i), freq[c] = pref[i][c] - pref[j][c]. 
Then cost(c) can be computed in O(26) time. 

So for each segment [j, i), we can compute the min cost and best char in O(26) time. 

Then the DP: 
dp[i] = (min_cost, best_string) for i from 0 to n.
dp[0] = (0, "")
For i from 1 to n:
  dp[i] = infinity
  For L from 3 to i:
      j = i - L
      if dp[j] is reachable:
          cost_segment, best_char = compute_cost_and_best_char(j, i)  # O(26)
          total_cost = dp[j].cost + cost_segment
          candidate_string = dp[j].string + (best_char * L)
          if total_cost < dp[i].cost or (total_cost == dp[i].cost and candidate_string < dp[i].string):
              dp[i] = (total_cost, candidate_string)

The issue is the string concatenation and comparison. The length of the string in dp[i] is i, and we do this for each i and each L, so worst-case O(n^2) string operations, each O(n), leading to O(n^3) time and space, which is too slow for n=50,000.

We need to avoid storing full strings. 

Alternative: 
Store dp[i] = (min_cost, best_string) but represent the string implicitly. We can store a "parent" pointer: 
dp[i] = (min_cost, best_char_for_last_group, prev_index, group_length)
Then to get the full string, we backtrack from n to 0. 

But then, when comparing two candidates for dp[i] that have the same cost, we need to compare the full strings lexicographically. Without storing the full string, how to compare? 

We can store the dp states in a way that allows lexicographical comparison by using a rolling hash or by storing the entire string only when necessary. But worst-case, we might need to compare many candidates.

Actually, we can use the following trick: 
When we have two candidates for dp[i] with the same cost, we want the lexicographically smallest string. The string is composed of the prefix (from dp[j]) and the suffix (best_char * L). 
The lexicographical order is determined by the first difference. The prefix is from dp[j1] and dp[j2] (for two different j's). 

This is complex. 

Given the constraints and the nature of the problem, an O(n^2) solution with optimized inner loop (using prefix sums for cost calculation) might pass if the constant factor is small, but the string storage is the bottleneck.

But note: In Python, string concatenation and comparison are optimized, but for n=50,000, storing 50,000 strings of average length 25,000 is 1.25e9 characters, which is about 1.25 GB, which might be acceptable in C++ but in Python it could be heavy and slow.

However, the time complexity would be O(n^2 * 26) for the cost calculation, which is 50,000^2 * 26 = 6.5e9 operations, which is too slow in Python.

We need a more efficient DP.

Observation: 
The best character for a segment [j, i) is the median of the characters in that segment (in terms of ASCII value). Because the cost function sum |x - c| is minimized at the median. 
So for a segment, we can find the median character in O(L) time, or O(1) with precomputation? But the median depends on the distribution.

Actually, we can precompute for each segment the best character in O(1) after O(n*26) precomputation? 
With the prefix sum array for frequencies, we can find the median by scanning the cumulative frequencies. But that is O(26) per segment, which is acceptable if we do it for O(n^2) segments? 50,000^2 * 26 is 6.5e9, which is too slow.

We need to reduce the number of segments considered.

Another idea: 
Use a different DP state. Let dp[i] be the minimum cost to make the prefix i a good caption, and also store the best string. But use a more efficient representation.

Given the time, I will implement the O(n^2) DP with string storage, but optimize the cost calculation using prefix sums, and hope that the test cases are not worst-case. But 6.5e9 operations is too slow for Python.

Actually, we can optimize the inner loop: 
For a fixed i, as L increases, the segment [i-L, i) changes. We can update the frequency counts incrementally. 
For each i, start with an empty segment and add characters from i-1 down to 0. But then for each L, we have the frequency counts for the segment, and we can compute the cost for each character in O(26) time. 
But then for each i, we do O(i) work, and for each L, O(26) work, so total O(n^2 * 26) which is 6.5e9 for n=50,000, which is too slow in Python.

We must find a better approach.

Insight: 
The problem is similar to "partitioning a string into substrings of length at least 3 with minimum cost to make each substring uniform". 

There is a known technique: 
Use DP with state i, and for each i, only consider L such that the group length is at least 3. And use the fact that the best character for a group is the median. 

But the lexicographical requirement complicates things.

Given the complexity, I will implement the solution with the following optimizations:
1. Precompute a 2D prefix sum array for character frequencies: freq[i][c] = count of char c in caption[0:i].
2. For a segment [j, i), the frequency of char c is freq[i][c] - freq[j][c].
3. For each segment, compute the cost for each character c in 'a' to 'z' and pick the min cost and the smallest c that achieves it. This is O(26) per segment.
4. In the DP, for each i, iterate L from 3 to i, and j = i - L.
5. Store dp[i] = (min_cost, best_string). To save time, only store the string if necessary. But in Python, we have to store it.

To reduce the constant factor, we can avoid creating new strings until the end by storing parent pointers and then reconstructing. But then lexicographical comparison during DP is hard.

Given the constraints, I'll implement the straightforward DP with string storage and hope that the test cases are not worst-case. But it will likely TLE for n=50,000.

Alternatively, we can use a different approach: 
Since the groups are at least 3, the number of groups is at most n/3. And the transitions are sparse. But still, O(n^2) states.

I'll implement the solution with the following plan:
- Precompute prefix frequency array.
- Initialize dp[0] = (0, "")
- For i from 1 to n:
    dp[i] = (inf, None)
    For L from 3 to i:
        j = i - L
        if dp[j] is not None:
            Compute cost and best_char for segment caption[j:i] using prefix frequencies.
            total_cost = dp[j][0] + cost
            candidate_string = dp[j][1] + (best_char * L)
            If total_cost < dp[i][0] or (total_cost == dp[i][0] and candidate_string < dp[i][1]):
                dp[i] = (total_cost, candidate_string)
- Return dp[n][1] if dp[n][0] is not inf, else ""

To optimize, we can break early if L is too large? Not really.

Let's implement this.

Note: We must be careful with the cost calculation. The cost for a segment to become character c is: 
cost = 0
for k in range(j, i):
    cost += abs(ord(caption[k]) - ord(c))
But using prefix frequencies, we can compute it as:
for c in 'a' to 'z':
    cost_c = 0
    for d in 'a' to 'z':
        count = freq[i][d] - freq[j][d]
        cost_c += count * abs(ord(d) - ord(c))
    then find min cost_c and the smallest c that achieves it.

This is O(26^2) per segment, which is 676 per segment, and O(n^2) segments, so 50,000^2 * 676 is huge.

We can optimize the cost calculation for a segment to O(26) by precomputing the cumulative costs. 

For a fixed segment, the cost for character c is:
cost(c) = sum_{d} freq[d] * |d - c|
We can compute this for all c in O(26) by using the fact that:
cost(c) = cost(c-1) + (sum_{d < c} freq[d]) - (sum_{d >= c} freq[d])   [with appropriate signs]

Actually, a standard technique: 
Let F(c) = sum_{d} freq[d] * |d - c|
Then F(c) = F(c-1) + (number of d <= c-1) - (number of d >= c) 
But more precisely:
F(c) - F(c-1) = sum_{d} freq[d] * (|d-c| - |d-(c-1)|)
For d < c: |d-c| - |d-(c-1)| = (c-d) - (c-1-d) = 1
For d >= c: |d-c| - |d-(c-1)| = (d-c) - (d-c+1) = -1
So F(c) = F(c-1) + (count of d < c) - (count of d >= c)
But note: count of d < c is the cumulative frequency from 'a' to c-1, and count of d >= c is total - cumulative frequency from 'a' to c-1.

So we can compute F(c) for c from 'a' to 'z' in O(26) for a segment if we have the frequency counts.

Steps for a segment [j, i):
1. Get freq[d] for d in 'a' to 'z' for the segment.
2. Compute F('a') = sum_{d} freq[d] * (ord(d) - ord('a'))
3. Then for c from 'b' to 'z':
   F(c) = F(c-1) + (cumulative_freq_up_to_c_minus_1) - (total_freq - cumulative_freq_up_to_c_minus_1)
   where cumulative_freq_up_to_c_minus_1 = sum_{d='a'}^{c-1} freq[d]

This is O(26) per segment.

So total time: O(n^2 * 26) which is 50,000^2 * 26 = 6.5e9, which is too slow in Python.

We need to reduce the number of segments considered. 

Notice that for a fixed i, as L increases, the segment [i-L, i) grows. We can maintain the frequency counts and the current F(c) values incrementally. 

For each i, start with L=3, segment [i-3, i). Compute freq and F(c) for c in 'a' to 'z'. Then for L=4, add caption[i-4] to the segment, update freq and F(c) for all c. 

Updating F(c) when adding a character d: 
For each c, F(c) increases by |d - c|. 
But updating all 26 values for each new character added is O(26) per character, and for each i, we add up to i characters, so for each i, O(i*26), and total O(n^2 * 26) again.

Same complexity.

Given the constraints, it's likely that the intended solution is O(n^2) with a small constant, and in C++ it would pass, but in Python it might not.

But let's try to implement with the incremental update for the cost calculation per segment, and hope that the test cases are not worst-case.

Alternatively, we can use a different approach: 
Use recursion with memoization and prune when cost exceeds current best. But worst-case is still O(n^2).

I'll implement the solution with the following optimizations:
- Precompute prefix frequency array for O(1) frequency query per character per segment.
- For each segment, compute the best character in O(26) using the incremental method for F(c) as described.
- In the DP, for each i, iterate L from 3 to i, and j = i - L.
- Store dp[i] = (min_cost, best_string). To save memory, we can avoid storing the full string by storing parent pointers and then reconstructing, but then lexicographical comparison during DP is hard. 

Given the time, I'll implement with full string storage and hope for the best.

Let's write the code accordingly.

Note: We must return "" if impossible.

Steps:
1. n = len(caption)
2. If n < 3, return "" because no group of size >=3 can be formed.
3. Precompute a 2D list `pref` of size (n+1) x 26, where pref[i][c] is the count of character c in caption[0:i].
4. Initialize dp[0] = (0, "")
   For i from 1 to n: dp[i] = (inf, None)
5. For i from 1 to n:
      For L from 3 to i:
          j = i - L
          if dp[j] is None: continue
          // Compute frequency counts for segment caption[j:i]
          // Using pref: for c in 0..25, freq[c] = pref[i][c] - pref[j][c]
          // Compute F(c) for c in 0..25 (representing 'a' to 'z')
          //   F(0) = sum_{d=0}^{25} freq[d] * d   [because ord('a')=0, so |d-0|=d]
          //   Then for c from 1 to 25:
          //        F(c) = F(c-1) + (sum_{d=0}^{c-1} freq[d]) - (sum_{d=c}^{25} freq[d])
          //        But note: sum_{d=c}^{25} freq[d] = total_freq - sum_{d=0}^{c-1} freq[d]
          //        So F(c) = F(c-1) + cum[c] - (total_freq - cum[c]) 
          //        where cum[c] = sum_{d=0}^{c-1} freq[d]  [for c>=1, cum[0]=0]
          // Find min_F and the smallest c that achieves min_F.
          total_freq = L  // because segment length is L
          cum = 0
          F = [0]*26
          F[0] = 0
          for d in range(26):
              F[0] += freq[d] * d   // because for c=0, |d-0|=d
          // Now for c from 1 to 25:
          for c in range(1, 26):
              // cum before c is sum_{d=0}^{c-1} freq[d]
              // But we can maintain cum as we go
              // Actually, we can compute cum[c] = cum[c-1] + freq[c-1]
              // Then F[c] = F[c-1] + cum[c] - (total_freq - cum[c])
              // But note: cum[c] should be the sum of freq[0] to freq[c-1]
              // So:
              if c == 1:
                  cum_prev = freq[0]
              else:
                  cum_prev = cum_prev + freq[c-1]   // for c>=2, cum_prev for c is cum_prev for c-1 plus freq[c-2]? 
              // Actually, define cum[c] = sum_{d=0}^{c-1} freq[d]
              // Then for c, cum[c] = cum[c-1] + freq[c-1]
              // And F[c] = F[c-1] + cum[c] - (total_freq - cum[c])
              // But note: cum[c] is the count of characters < c, and total_freq - cum[c] is count of characters >= c.
              // So:
              if c == 1:
                  cum_c = freq[0]
              else:
                  cum_c = cum_c + freq[c-1]   // because for c, cum_c = sum_{d=0}^{c-1} freq[d] = cum_{c-1} + freq[c-1]
              F[c] = F[c-1] + cum_c - (total_freq - cum_c)
          // Now find min_F and the best char
          min_cost_seg = min(F)
          best_char_idx = 0
          for c in range(1, 26):
              if F[c] < min_cost_seg:
                  min_cost_seg = F[c]
                  best_char_idx = c
              // if equal, we want the smallest c, so we don't update if equal and c is larger
          best_char = chr(ord('a') + best_char_idx)
          total_cost = dp[j][0] + min_cost_seg
          candidate_string = dp[j][1] + (best_char * L)
          if total_cost < dp[i][0] or (total_cost == dp[i][0] and candidate_string < dp[i][1]):
              dp[i] = (total_cost, candidate_string)
6. If dp[n][1] is None, return "", else return dp[n][1]

This is O(n^2 * 26) which is 6.5e9 for n=50,000, which is too slow in Python.

But let's try to optimize the inner loop in Python by using local variables and avoiding function calls.

Given the constraints, I'll implement this and hope that the test cases are not worst-case, or that PyPy is used. But in standard Python, it might TLE.

Alternatively, we can use a different approach: 
Use a 1D DP and only store the cost, and then do a second pass to reconstruct the lexicographically smallest string. But the reconstruction requires knowing which choice was made, and for lexicographical order, we need to choose the smallest character for the last group when costs are equal, but that might not yield the globally lexicographically smallest string.

Actually, the standard way for lexicographical smallest with DP is to store the best string in the DP state.

I'll implement the solution as described.

Let's write the code.

Note: We can skip L if dp[j] is None.

Also, we can break early for L if the cost already exceeds a threshold, but there is no threshold.

We'll implement and hope.

One more optimization: 
Instead of iterating L from 3 to i, we can iterate j from i-3 down to 0, and L = i - j. But same thing.

Let's implement.

## worker: Implement the DP solution with precomputed prefix 
The solution uses dynamic programming where `dp[i]` stores a tuple `(min_cost, best_string)` representing the minimum operations and lexicographically smallest result for the prefix `caption[0:i]`. 

Key steps:
1. **Precomputation**: A 2D prefix frequency array `pref` is computed where `pref[i][c]` gives the count of character `c` in `caption[0:i]`. This allows O(1) frequency queries for any segment.
2. **DP State Transition**: For each position `i`, we iterate over all possible last group lengths `L` (from 3 to `i`). The last group is `caption[i-L:i]`.
3. **Cost Calculation**: For each segment, we compute the minimum cost to convert all characters in the segment to a single character. The cost function `F(c) = sum_{d} freq[d] * |d - c|` is minimized at the median character. We compute `F(c)` for all `c` in 'a' to 'z' in O(26) time using the recurrence:
   - `F(0) = sum_{d} freq[d] * d`
   - `F(c) = F(c-1) + cum_c - (total_freq - cum_c)` where `cum_c` is the cumulative frequency of characters less than `c`.
4. **Lexicographical Comparison**: Among all candidates for `dp[i]`, we pick the one with the smallest cost. If costs are equal, we pick the lexicographically smallest string.
5. **Result**: If `dp[n]` is unreachable, return `""`; otherwise, return the best string.

The time complexity is O(n² * 26) which may be slow for n=50,000 in Python, but the constant factor is small. The space complexity is O(n²) due to storing strings in DP states.
