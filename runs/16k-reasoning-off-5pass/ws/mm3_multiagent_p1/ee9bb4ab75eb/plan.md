We need for each index i, considering the multiset of words with index i removed, the length of the longest common prefix of any k distinct strings from that multiset. If removing i leaves fewer than k strings, answer is 0.

The key insight: among any set of strings, the longest common prefix of *any* k of them equals the longest common prefix of the k strings that share the longest common prefix overall. So we can think in terms of string frequencies: if we have groups of identical strings, picking k strings from the most frequent group gives the longest possible common prefix (the full length of that string). However, strings that aren't identical can also share a long common prefix. The key observation: the answer for index i is determined by the *most frequent string* in the remaining array. Because if a string S appears at least k times, we can pick k copies of S and get LCP of length |S|. If no string appears k times, the answer is 0. Wait — is that always true? Could strings with different values share a longer common prefix than any single string's length? No, because the LCP of k distinct strings is at most the length of the shortest among them. If no string repeats k times, then any selection of k strings must include at least two different values, so the LCP is at most the LCP of those two distinct strings, which is strictly less than at least one of their full lengths. But could that LCP exceed the length of any single string in the array? No, it cannot exceed the length of the shorter string. So the maximum LCP among k distinct strings is always achieved by picking k copies of the same string (the one with maximum length among those appearing ≥ k times). If no string appears k times, answer is 0.

So the problem reduces to: for each i, after removing word[i], does the most frequent string (by count) have count ≥ k in the remaining array? If yes, answer = length of that string. We want the *maximum* length such string among those with count ≥ k.

Equivalently, we need: after removing index i, the string with the highest frequency that has count ≥ k (in the remaining). Since answer = max length of strings that have count ≥ k after removal.

Strategy:
- Group indices by string value. For each string s, store the list of indices where it occurs and its length.
- Build a segment tree (or similar) over indices tracking: for each index i, when we remove it, we need to know the answer. 
- Actually, let's think of it as: for each string s with count c_s ≥ k originally, it contributes answer = len(s). When we remove an index i, if the removed word belonged to a group that drops below k, we might lose that candidate. We need the maximum len(s) among all s with remaining count ≥ k.

Approach: Sort unique strings by length descending. For each string s, define its "valid" status: it has ≥ k occurrences. Initially, compute which strings are valid. The answer initially (with no removals, or thinking of removal one by one) — but we need answers for each single removal.

Let V = set of strings with count ≥ k. Answer for removal i = max_{s ∈ V, s ≠ words[i] or (s == words[i] and count_s - 1 ≥ k)} len(s), or 0 if empty.

Wait, if words[i] is not in V, removing it doesn't change V. If words[i] is in V:
- If count_s ≥ k+1 after removal, s remains in V.
- If count_s == k after removal, s drops out of V.

So we need to efficiently find, for each index i, the maximum length string in V after possibly removing one occurrence of words[i].

Solution:
1. Compute counts for each string.
2. Let initial valid set = {s : count[s] ≥ k}. 
3. Sort all distinct strings by length descending. Maintain a data structure (e.g., a sorted set by length) of the valid strings' lengths.
4. For each index i (process in some order or compute independently):
   - Determine the new valid set after removing words[i].
   - Answer = max length in new valid set, or 0.

To compute this for all i efficiently:
- We need, for each string s with count[s] == k, the set of indices where s appears. Removing any one of these indices will invalidate s.
- For strings with count[s] > k, they remain valid after any single removal of one of their indices.
- For strings with count[s] < k, they are never valid.

So:
- Group A: strings with count ≥ k+1. Always valid regardless of which single index is removed. They contribute their lengths to every answer.
- Group B: strings with count == k. Valid only if we don't remove an index belonging to them. If we remove one of their indices, they become invalid.

Therefore:
- Let M = max length among Group A strings. If Group A is empty, M = 0.
- For each index i, let s = words[i].
  - If count[s] ≥ k+1: then even after removal, s is still in Group A. Answer = max(M, len(s)) = M (since len(s) is already considered, but we need max over all valid including s). Actually M already includes s if count[s] ≥ k+1. So answer = M.
  - If count[s] == k: then after removal, s is no longer valid. Answer = M (since s drops out, but M already excluded s... wait, if count[s] ≥ k+1, s is in Group A, so M includes len(s) or larger. If count[s] == k, s is in Group B, not in Group A, so M doesn't include len(s). After removal, s is out. Other Group B strings still valid. So we need max(M, max length of Group B strings excluding s)).
  - If count[s] < k: answer = max(M, max length of all Group B strings).

So we need, for Group B (strings with count == k), to support: max length overall, and for each string s in B, max length of B \ {s}. This is a classic "max excluding one" problem.

We can sort Group B strings by length descending. Let L_1 ≥ L_2 ≥ ... ≥ L_m be the lengths of Group B strings. Then:
- Max over all B = L_1.
- Max over B \ {s} where s is the i-th in this sorted order:
  - If i ≠ 1: answer = L_1 (the max is unchanged).
  - If i == 1: answer = L_2 (or 0 if m == 1).

So the only special case is when we remove an index belonging to the *longest* Group B string, and that string has count == k (so it's the only one or longest one in B).

Let me verify with Example 1:
words = ["jump","run","run","jump","run"], k=2
Counts: "jump": 2, "run": 3.
Group A (count ≥ 3): "run" (len 3). M = 3.
Group B (count == 2): "jump" (len 4). L = [4]. 
- Remove index 0 ("jump"): s="jump", count==k, s is the only/longest in B. After removal, B is empty. Answer = M = 3. ✓
- Remove index 1 ("run"): s="run", count≥k+1. Answer = M = 3? But expected 4. 

Hmm, expected output for index 1 is 4. Let me recheck. Removing index 1 ("run"): remaining = ["jump","run","jump","run"]. "jump" appears 2 times, "run" appears 2 times. Both have count 2. We can pick two "jump"s → LCP "jump" len 4. So answer is 4.

But in my analysis, "jump" has count 2 originally. After removal of a "run", "jump" count is still 2 (k), "run" count becomes 2 (k). So both are in Group B. M (Group A) is empty since no string has count ≥ 3 after removal. So we need to consider Group B after removal.

Ah, I see. My grouping was based on original counts. But after removal, counts change. The initial grouping is:
- Originally count ≥ k+1: always valid after any single removal.
- Originally count == k: valid unless we remove one of its indices.
- Originally count < k: never valid.

In this example, "run" originally has count 3 ≥ k+1=3. So it should be in Group A. M = 3.
"jump" originally has count 2 == k. So Group B = {"jump"}, L = [4].

Now for removal index 1 (a "run"):
- s = "run", count[s] = 3 ≥ k+1, so s stays valid (Group A). M = max length in Group A = len("run") = 3. So answer should be 3. But expected is 4.

Where is the error? The error is that after removal, "jump" becomes a Group B string (count 2, which is k). But originally it was already in Group B. So in my framework, Group B = strings with original count == k. After removing a "run", "jump" still has count 2, so it's still in Group B. So we should consider max(M, max_B_excluding_removed_if_applicable).

In this case, M=3, Group B = {"jump"} len 4. s="run" is not in B, so B remains valid. Answer should be max(3, 4) = 4. ✓

So the correct formula is:
- M_A = max length of strings with original count ≥ k+1.
- M_B_all = max length of strings with original count == k (let's call this the "B-max").
- For removal of index i with word s:
  - If count[s] ≥ k+1: s is in A, remains in A. Answer = max(M_A, M_B_all). [Because A unchanged, B unchanged.]
  - If count[s] == k: s is in B. After removal, s drops from B.
    - Let M_B_excl_s = max length of B \ {s}.
    - Answer = max(M_A, M_B_excl_s).
  - If count[s] < k: s not in A or B. Answer = max(M_A, M_B_all).

For the case count[s] == k, if s is the unique longest in B (or there are ties at top), we need M_B_excl_s = second longest in B, or 0.

In Example 1:
- M_A = len("run") = 3.
- B = {"jump"} len 4. M_B_all = 4. Second longest in B = 0 (only one element).
- Remove index 0 ("jump"): s in B, s is the only/longest. M_B_excl_s = 0. Answer = max(3, 0) = 3. ✓
- Remove index 1 ("run"): s in A. Answer = max(3, 4) = 4. ✓
- Remove index 2 ("run"): same as above, answer 4. ✓
- Remove index 3 ("jump"): same as index 0, answer 3. ✓
- Remove index 4 ("run"): same as index 1, answer 4. ✓

This works. Now the key data structure problem: we need M_A, and for Group B, we need the max length and second max length (or more generally, for each string in B, we need max of B excluding that string). Since we only need the top two, and the set B is static (doesn't change as we iterate i), we can precompute:
- Sort B strings by length descending.
- The answer for removing a string not in B is max(M_A, M_B_all).
- The answer for removing a string s in B is max(M_A, M_B_all if s is not the sole top, else M_B_second).

Specifically, if there are multiple strings in B tied for the maximum length, removing one of them still leaves others, so M_B_excl = M_B_all. Only if s is the *unique* maximum in B (or all max-length strings are exactly s, meaning only one string has that max length), then M_B_excl = M_B_second (the second highest distinct or just the next in sorted order, even if equal length? Wait, if there are two strings with the same max length, removing one leaves the other, so M_B_excl = same max. So we only need to worry if there's exactly one string with the max length in B.

Let sorted B lengths: L_1 ≥ L_2 ≥ ... ≥ L_m.
- If m == 1: M_B_excl for the only string = 0.
- If m ≥ 2 and L_1 > L_2: the unique max string has M_B_excl = L_2. Others have M_B_excl = L_1.
- If m ≥ 2 and L_1 == L_2: removing any of the top strings (there are at least 2) leaves another with same length, so M_B_excl = L_1 for all. For non-top strings, M_B_excl = L_1.

So for each string s in B, we can determine its "value when excluded" = M_B_excl_s.

Implementation:
1. Count frequencies of each string.
2. Let len_map: string -> length.
3. Group A: strings with count ≥ k+1. M_A = max(len(s) for s in A), or 0.
4. Group B: strings with count == k. Collect their lengths. Sort descending to get L_1, L_2, ...
5. For each string s in B, determine excl_value[s]:
   - Find its position in the sorted B. But actually we can just note:
     - If there's only one string in B, or if s is the unique max in B, then excl_value[s] = L_2 (or 0).
     - Otherwise, excl_value[s] = L_1.
   - Actually, if L_1 == L_2, no string is "unique max" because there are ties. So unique max means: the count of strings in B with length L_1 is exactly 1, and s is that string.
   - Let count_at_max = number of strings in B with length L_1.
   - If count_at_max >= 2: for all s in B, excl_value[s] = L_1.
   - If count_at_max == 1: for the unique max string s*, excl_value[s*] = L_2 (or 0 if m==1). For others, excl_value[s] = L_1.

Wait, is that sufficient? What if L_1 == L_2 == L_3 but we have 3 strings all same length. Then any removal leaves at least 2 with length L_1, so M_B_excl = L_1 for all. Good.

What if L_1 > L_2, and we remove a string with length L_2. Then M_B_excl = L_1. Good.

What if L_1 > L_2, and we remove the unique L_1 string. Then M_B_excl = L_2. Good.

So yes, this is correct.

6. For each index i:
   - s = words[i]
   - if count[s] >= k+1: ans[i] = max(M_A, M_B_all) [but M_A already >= len(s), and M_B_all is independent; actually M_A might not include the max of B. So ans = max(M_A, M_B_all).]
   - elif count[s] == k: ans[i] = max(M_A, excl_value[s])
   - else: ans[i] = max(M_A, M_B_all)

This gives O(n + m) where m is number of distinct strings. Since sum of lengths ≤ 10^5, this is efficient.

But wait: is the answer really just the max length of a string with count ≥ k after removal? Yes, because we can always pick k copies of that string, achieving LCP = len(s). And we argued no longer LCP is possible without k copies of some string. But wait — what if we pick k strings that are not all identical but share a long common prefix that is longer than any single string's full length? That's impossible because the LCP of k distinct strings cannot exceed the length of the shortest string among them. If we have k strings that are not all identical, the shortest one has some length L. But we could just pick the string with the longest L among all strings, and if it has count ≥ k, we get that length. If no string has count ≥ k, then any k-selection has at least 2 different strings. The LCP is at most the min of their lengths, which is ≤ max length of all strings. But could it be that a non-unanimous selection gives a prefix longer than the longest individual string? No, prefix length is bounded by the string length. So the max possible LCP is the max length of any string that appears ≥ k times.

This seems correct.

Let me double-check with a case: words = ["a", "ab", "abc"], k=2. Counts: all 1. M_A=0, B empty. All answers = 0. After removing any one, we have 2 strings. LCP of "a" and "ab" is "a" (len 1). But no string appears twice, so answer should be 0. Correct.

Another case: words = ["abc", "abd", "ab"], k=2. Counts: "abc":1, "abd":1, "ab":1. All 1. After removing any, two strings left, LCP could be 2 ("abc","abd" → "ab"). But no string repeats, so answer = 0. Correct.

Another case: words = ["abc", "abc", "ab"], k=2. Counts: "abc":2, "ab":1. B = {"abc"} len 3. M_A=0.
- Remove "abc" (index 0 or 1): s in B, unique max, M_B_excl=0. Answer = 0. Correct (remaining: "abc","ab" or "abc","ab", only one "abc" so can't pick 2 identical; best LCP of "abc" and "ab" is 2, but we claim 0? Wait, this is a problem!)

Wait! If we have "abc", "abc", "ab", k=2. After removing one "abc", remaining is ["abc", "ab"]. We can pick these two. Their LCP is "ab" (length 2). But according to my logic, no string appears twice, so answer is 0. That's wrong! The answer should be 2.

So my logic is flawed. The LCP of k distinct strings is not necessarily achieved by k identical strings. It could be that no string appears k times, but the k strings share a common prefix.

Example: "abc", "abd", k=2. LCP is "ab" length 2, but no string repeats.

So the problem is more subtle. We need the longest common prefix of *any* k strings from the remaining array, not necessarily identical.

This is a much harder problem. Let me think again.

The constraint sum of lengths ≤ 10^5 is key. This suggests we can build a trie.

Let's think. We have an array of strings. We need, for each i, the max LCP of any k strings in words \ {i}.

Observation: The answer is determined by the "k-th most frequent prefix" or something? Actually, the LCP of k strings is the length of the longest prefix P such that at least k strings in the set have P as a prefix.

So the answer for a set S is: max length L such that there exists a prefix P of length L with count_S(P) ≥ k.

This is a classic problem. We can build a trie of all words. Each node represents a prefix. The count of a node is the number of words in S that have that prefix. The answer is the maximum depth of a node with count ≥ k.

Now, S = words \ {i}. We need this for each i.

Since sum of lengths ≤ 10^5, the total number of trie nodes is O(10^5).

We need, for each index i, the max depth of any node whose count in S is ≥ k. The count in S is total_count - (1 if word i has that prefix else 0).

So for each node v (representing prefix P), let total[v] = number of words in the whole array with prefix P. Let leaf_count for word i: for each node on the path from root to leaf(word i), if we remove word i, the count becomes total[v] - 1.

So for each node v, define:
- If total[v] ≥ k+1: even after removing one word that has this prefix, count remains ≥ k. So this node contributes its depth to every answer (for any removal).
- If total[v] == k: then this node is "fragile": it contributes its depth to all answers except when we remove one of the words that has this prefix.
- If total[v] < k: never contributes.

This is analogous to before, but now nodes have depths, and the condition is about prefixes.

We want, for each i, the maximum depth of:
- Nodes v with total[v] ≥ k+1 (always on), plus
- Nodes v with total[v] == k, and word i does NOT have prefix v (i.e., v is not on the path of word i), plus
- Nodes v with total[v] ≥ k+1... wait, already covered.

Actually, let's define:
- Let S_k = set of nodes v with total[v] ≥ k.
- For removal i, the valid nodes are: {v ∈ S_k : total[v] - (1 if v ∈ path(i) else 0) ≥ k}.
- This is: (S_k \ path(i)) ∪ {v ∈ path(i) : total[v] - 1 ≥ k}.

Note that if total[v] ≥ k+1, then v is in S_k and v ∈ path(i) still satisfies total[v]-1 ≥ k, so v is valid.
If total[v] == k, then v ∈ S_k, but v is valid only if v ∉ path(i).

So the valid set for removal i is:
- All nodes with total[v] ≥ k+1 (regardless of path).
- Plus, nodes with total[v] == k that are NOT on path(i).

We need the maximum depth of a valid node.

Let D_high = max depth of nodes with total[v] ≥ k+1. If none, D_high = 0.
Let D_k_all = max depth of nodes with total[v] == k.
For a given i, we need max(D_high, max depth of "k-nodes" not on path(i)).

If path(i) doesn't contain the deepest k-node, then answer = max(D_high, D_k_all).
If path(i) contains the deepest k-node, we might lose it. We need the max depth of k-nodes not on path(i).

This is similar to the earlier problem but on the trie. However, the "k-nodes" are many, and path(i) can contain many k-nodes. We need an efficient way.

Since the trie has O(10^5) nodes, and each path has length O(10^5) in worst case but sum of all path lengths is sum of word lengths ≤ 10^5.

We can think of the k-nodes as having a value (depth). We need, for each i, the max depth of a k-node not in path(i). This is a range/path query.

Observation: If we know the max depth of all k-nodes, and for the specific k-nodes on path(i), we know their depths, we can compute the max excluding them.

Since path(i) has length len(words[i]) ≤ 10^4, and sum is 10^5, we can afford to iterate over path(i) for each i? No, that would be O(sum of lengths) per i in the worst case if we did something naive. But total sum of lengths is 10^5, so if we process each i by looking at its path, and for each node on the path we do O(1) work, total work is O(sum of lengths) = O(10^5). That's good!

So algorithm:
1. Build a trie. For each node, maintain total count.
2. Identify the set of "k-nodes": nodes with total count == k. (We also track D_high = max depth of nodes with count ≥ k+1, and D_k_all = max depth of k-nodes.)
3. For the k-nodes, we need to answer: for a given set of nodes (the path of word i), what is the max depth of a k-node NOT in this set?
   - If the set of k-nodes on the path is empty, answer is D_k_all.
   - Otherwise, we need max over (all k-nodes minus the k-nodes on path).
   - The max over all k-nodes is D_k_all. The only way the answer is different is if the only k-node(s) achieving the max are all on the path. This is similar to the array case: we need to know if the max is unique and on the path.

Specifically, let max_depth_k = D_k_all. Let the set of k-nodes with depth = max_depth_k be called the "max-k-nodes". If no max-k-node is on path(i), then the answer is max_depth_k. If all max-k-nodes are on path(i), we need the second highest depth among k-nodes.

But wait, is it sufficient to only consider the max? What if path(i) contains the max node, but there's another node with same max depth? Then we're fine. Only if ALL nodes with max_depth_k are on path(i) do we need to look at the next depth.

However, a path could contain many k-nodes, some deep, some shallow. If the max_depth_k node is not on the path, great. If it is, and there are other k-nodes with same depth not on the path, great. If it's the unique max or all max are on path, we drop to second max, etc.

But the path could contain the top several max nodes! For example, if the top 5 deepest k-nodes are all on the path of word i. Then we need the 6th deepest.

Is that possible? Yes, if word i is very long and contains many k-nodes along its path.

So we need, for each path, the max depth of a k-node not in the path. This is equivalent to: given a sorted list of k-node depths (descending), and a set of "forbidden" depths (those on the path), find the highest depth not forbidden.

Since each path has at most O(length) nodes, and sum of lengths is 10^5, we can:
- Collect all k-node depths, sort descending: d_1 ≥ d_2 ≥ ... ≥ d_m.
- For each i, we have a set of depths on the path that are in this list. We want the first d_j not in the path's k-node depths.

If we just naively for each i scan the sorted list until finding one not on path, and check membership in path's k-nodes using a hash set of those k-nodes on the path, this could be O(m) per i in the worst case, which is too much (m could be 10^5, n could be 10^5).

But note: the path of word i has at most L_i nodes, and sum L_i ≤ 10^5. The number of k-nodes on path i is at most L_i.

We can precompute for each k-node its depth. Sort k-nodes by depth descending.

For each i, let B_i = set of k-nodes on path of word i. Let their depths be on the path. We want max depth of k-node ∉ B_i.

This is a standard problem. Since the set B_i is small (size ≤ L_i), and we have many queries, we need an efficient way.

Alternative: for each i, we can look at the k-nodes on its path. The answer is max(D_high, max_k_not_in_B_i).

The max_k_not_in_B_i = the highest depth in the global k-node list that is not in B_i.

We can precompute a "next higher not forbidden" or something. But B_i varies per i.

Another approach: process the trie nodes. Each k-node v has a depth. The answer for i is max(D_high, max_{v ∈ k-nodes \ B_i} depth(v)).

We can think of it as: initially, the max is D_k_all. For each i, we "remove" the k-nodes in B_i. The answer is the max of remaining.

Since the total size of all B_i is sum of (number of k-nodes per word). Each node v is a k-node and lies on some paths. Specifically, v lies on the path of each word that has prefix v. Let the set of such words be W_v. Then v is in B_i for all i ∈ W_v.

So the total size of all B_i is sum over k-nodes v of |W_v|. In the worst case, if the root is a k-node (total count ≥ k), then |W_v| = n, so this could be O(n * #k-nodes) which is too big.

But wait, is the root a k-node? The root represents the empty prefix. All words have the empty prefix. So total[root] = n. If n ≥ k, then root is a k-node (in fact, ≥ k+1 if n > k, or == k if n = k). So if n = k, root is a k-node, and it's on every path. Then |W_root| = n. This is fine, we just need to handle it.

But the total number of (i, v) pairs where v is a k-node and v is on path of word i could be large. For example, if every prefix of every word is a k-node. That would require many counts to be exactly k. With n up to 10^5, sum lengths 10^5, this is bounded by the number of trie nodes, which is ≤ 10^5 + 1. But each node v contributes to |W_v| paths. The total sum is sum_v |W_v| = total number of (word, ancestor) pairs where the ancestor is a k-node. This is bounded by sum over words of (number of ancestors that are k-nodes). In the worst case, if all nodes are k-nodes, this is sum of lengths = 10^5. Because each word contributes its length. So total sum is O(10^5). That's manageable!

Wait, is that true? If all trie nodes are k-nodes, then for each word, all its ancestors are k-nodes, so the number of k-nodes on its path is its length. Sum over words of length is 10^5. So total pairs (word, k-node ancestor) is O(10^5). This is great.

But could it be larger? The number of trie nodes is at most 10^5. Each node v has a set of words that pass through it. The sum over v of |W_v| is exactly the sum over words of (number of nodes on path of word). The number of nodes on path of word w is len(w) + 1 (including root). So sum is sum (len(w)+1) = sum len(w) + n ≤ 10^5 + 10^5 = 2*10^5. So indeed, the total number of (word, node on path) pairs is O(10^5).

Therefore, if we iterate over all words and for each word, iterate over its path, the total work is O(10^5).

Now, for each word i, we need to compute max depth of k-node not on its path. We can precompute the k-nodes sorted by depth. But we need to query: given a set of nodes B_i (the k-nodes on path i), find max depth of k-node not in B_i.

We can do this by noting that the max is D_k_all, unless the node(s) achieving D_k_all are all in B_i. In general, we can precompute the k-nodes in a data structure that allows us to query the max depth excluding a given set.

Since B_i has size at most len(words[i])+1, and sum of sizes is O(10^5), we can afford to, for each i, check the top few k-nodes.

Specifically, let the k-nodes sorted by depth descending be v_1, v_2, v_3, ... with depths d_1 ≥ d_2 ≥ ... . We want the first d_j such that v_j ∉ B_i.

We can iterate j = 1, 2, 3, ... and for each j, check if v_j ∈ B_i. If not, return d_j. Since the answer is likely found quickly (usually j=1), and even in the worst case, j could be up to the size of B_i plus one. But could it be large?

Suppose all k-nodes are on the path of word i. Then we need to find a k-node not on path i. If all k-nodes are on path i, and there are m k-nodes, we scan all m. But m ≤ number of k-nodes ≤ number of nodes ≤ 10^5. And this could happen for many i. If we do O(m) per i, and there are n=10^5 words, this is O(n*m) = 10^10. Too slow.

But note: the total work over all i is sum_i (number of k-nodes checked). If for each i we scan from the top until finding one not in B_i, the work is sum_i (position of first valid). This could be large.

We need a better way.

Alternative: for each k-node v, we can precompute "the set of words that contain v on their path". Then the answer for i is max depth of k-node v such that i ∉ W_v (i.e., word i does not have prefix v).

Equivalently, we want max depth of v where total[v] == k and v ∉ path(i).

We can think of each k-node v as "blocking" the words in W_v from using v. But other k-nodes might not block word i.

Another idea: since total[v] is the count, and we only care about v with total[v] == k (fragile nodes) and total[v] ≥ k+1 (always on).

For always-on nodes, D_high is their max depth.

For fragile nodes, we have a set of nodes. For each word i, we want the max depth of a fragile node not on path(i).

This is exactly: given a set of items (fragile nodes) each with a weight (depth), and each word i has a "blocked set" B_i (the fragile nodes on its path). We want for each i the max weight of an item not in B_i.

We can solve this with a segment tree or BIT if we linearize the trie. Or we can use the fact that the trie has small total size.

Let's think differently. The fragile nodes are the nodes with count == k. For each fragile node v, it has depth d_v. It is "available" for word i if v ∉ path(i).

The path(i) is a root-to-leaf path. The set of fragile nodes not on path(i) includes all fragile nodes except those on path(i).

We want the max d_v over v fragile, v ∉ path(i).

If we precompute the max depth of all fragile nodes: max_frag = max d_v.
If the unique max or all max are achieved by nodes not in B_i, then answer is max_frag. Otherwise, we need the next.

This is like: the global sorted list of fragile nodes by depth. For each i, we remove B_i from this list and take the max.

We can precompute the sorted list. The issue is efficient query.

Since sum of |B_i| is O(10^5), we can use a trick: for each i, we mark all nodes in B_i as "removed" for this query, find the max, then unmark. But we have many queries.

We can use a "offline" approach. For each fragile node v, it is removed for exactly the words in W_v. So the "unremoved" set for word i is all fragile nodes minus union of v ∈ B_i = all fragile nodes minus fragile nodes on path(i).

This is equivalent to: for each word i, the available fragile nodes are those not on path(i).

We can compute for each fragile node v, the set of words that "cover" it (i.e., have v on path). Then the answer for i is max over v fragile, i ∉ W_v.

We can think of this as: the answer is the max depth of a fragile node v such that word i is not in W_v.

If we process words in some order, or if we have a data structure...

Another approach: the answer for i is max(D_high, second_best_if_first_blocked).

Actually, note that if a fragile node v is on path(i), then word i has prefix v, and total[v] = k. This means there are exactly k words with prefix v, and word i is one of them.

Consider the deepest fragile node. If it's on path(i), we drop it. The next deepest might also be on path(i), drop it, etc.

Since the path(i) is a chain, the fragile nodes on path(i) are a subset of the nodes on that chain. Their depths are increasing along the chain.

Specifically, along the path from root to leaf for word i, the depths increase. The fragile nodes on this path have some depths. We want the max depth of a fragile node not on this path.

The set of all fragile nodes has depths. The ones not on this path include:
- Fragile nodes with depth greater than some threshold? No, there could be fragile nodes off the path with various depths.
- Fragile nodes with depth less than the min depth on path, or between depths on path but not on the path.

Actually, the set of depths of fragile nodes on path(i) is a set of integers (depths). We want the maximum depth in the global fragile set that is not in this set of depths? No! That's not right. There could be two different fragile nodes with the same depth. If the global max depth is d, and there are multiple nodes with depth d, and only one is on path(i), then the answer is still d. We only lose the max if ALL nodes with max depth are on path(i).

So we need to know, for the global max depth value D, how many fragile nodes have this depth, and are they all on path(i)?

Similarly for the second highest depth, etc.

But the path could block multiple top depths.

This is getting complicated. Let's think of a direct way.

Since the total number of nodes is small (10^5), and the total path length is 10^5, we can do the following:

For each fragile node v, we know its depth d_v. We want, for each i, max {d_v : v fragile, v ∉ path(i)}.

We can compute the global maximum depth among fragile nodes, and the set of nodes achieving it. If any of them is not in path(i), answer is that max. Otherwise, we look at the next level.

But "level" by depth: we can group fragile nodes by depth. Let the distinct depths of fragile nodes in decreasing order be D_1 > D_2 > ... .

For a given i, the answer is the largest D_j such that there exists a fragile node with depth D_j not on path(i).

Equivalently, the answer is the largest D_j such that NOT (all fragile nodes with depth D_j are on path(i)).

So for each depth level, we need to know if all nodes at that level are covered by path(i).

For a depth level D, let S_D = set of fragile nodes with depth D. For word i, if S_D ⊆ path(i), then this level is "blocked". Otherwise, available.

path(i) is a set of nodes (the chain). S_D ⊆ path(i) means every node in S_D is on the chain of word i.

Since S_D is a set of nodes, and the chain is a specific path, this is a containment check.

But the number of depth levels could be large (up to 10^5), and for each i we need to find the first unblocked level. This could be done by scanning levels from top to bottom, but if the top many levels are all blocked, and there are many i, this is slow.

However, note that if S_D is not empty, and the chain has length L, then the number of nodes on the chain is L+1. The set S_D could be large, but to check if S_D ⊆ chain, we need to see if all nodes in S_D are on the chain. Since the chain is a path, and S_D is a set of nodes, we can precompute for each node its "position" on the chain? No, the chain varies per word.

Alternative: for each word i, the set path(i) is fixed. We can precompute for each fragile node v, the set of words that contain v. Then for a given i, S_D ⊆ path(i) iff for all v ∈ S_D, i ∈ W_v (i.e., word i is in the word-set of v).

This is like: a depth level D is blocked for word i if i is in the intersection of W_v for all v ∈ S_D.

If S_D is empty, it's not blocked. If S_D has one node v, it's blocked if i ∈ W_v. If S_D has multiple nodes, it's blocked if i ∈ ∩_{v ∈ S_D} W_v.

We can precompute for each depth level D the set of words that contain ALL nodes in S_D. This is the intersection.

But the intersection of sets, and there are many levels.

Observation: the nodes in S_D are all at depth D. They are siblings or in different subtrees? At depth D, there are multiple possible nodes (different strings of length D). The set S_D is the set of those that have count exactly k.

For a word i, path(i) at depth D contains exactly one node (the prefix of length D of word i), unless len(word i) < D, in which case path(i) doesn't reach depth D. So if len(word i) < D, then path(i) does not contain any node at depth D, so certainly not all of S_D, so the level is unblocked (provided S_D is non-empty).

If len(word i) ≥ D, then path(i) contains exactly one node at depth D, call it v_i(D). Then S_D ⊆ path(i) iff v_i(D) ∈ S_D. Because S_D is a set of nodes at depth D, and path(i) contains exactly one such node, so all of S_D is contained iff that one node is in S_D and... wait, if S_D has multiple nodes, and path(i) contains one node, then S_D ⊆ path(i) requires that the one node is in S_D AND S_D has no other nodes. So S_D ⊆ path(i) iff |S_D| = 1 and that node is v_i(D).

Is that right? path(i) at depth D is exactly one node (if len ≥ D). For S_D to be a subset of path(i), every element of S_D must equal that one node. So yes, S_D must be a singleton, and that node must be the prefix of word i.

Therefore, for word i with length L_i:
- For any depth D > L_i, path(i) has no node at D, so cannot contain S_D (unless S_D empty). So level D is available if S_D nonempty.
- For depth D ≤ L_i, path(i) has node v_i(D) at depth D. S_D ⊆ path(i) iff S_D = {v_i(D)}.

This is a huge simplification!

So the blocked levels for word i are:
- Depths D where S_D = {v} and v = v_i(D) (i.e., the unique node at depth D that has count k is exactly the prefix of word i at depth D).

In other words, a depth level D is blocked for word i if and only if:
- There is exactly one fragile node at depth D, call it v, and
- v is the prefix of word i at depth D (which requires len(word i) ≥ D).

Otherwise, the level is available (has at least one fragile node not on path, or word i is too short to reach D, or there are multiple fragile nodes at D so word i can cover at most one).

Therefore, to find the answer for word i, we look at the fragile nodes sorted by depth descending. The answer is the depth of the first fragile node v such that either:
- v is not on path of word i, OR
- there is another fragile node at the same depth as v (so even if v is on path, the depth is still available because the other node is not).

Wait, we need max depth of fragile node v with v ∉ path(i). This is equivalent to: the largest depth D such that there exists a fragile node at depth D not in path(i).

As argued, at depth D, the set of available nodes is S_D \ path(i).
- If |S_D| ≥ 2, then since path(i) contains at most one node at depth D, S_D \ path(i) is nonempty. So depth D is available.
- If |S_D| = 1, let the node be u. Then depth D is available iff u ∉ path(i).
- If |S_D| = 0, depth D is not a fragile depth, skip.

So the set of available depths is exactly:
- All depths D where |S_D| ≥ 2, PLUS
- Depths D where |S_D| = 1 and the unique node u is not on path(i).

For word i, the unavailable depths are those D where |S_D| = 1 and the unique node is on path(i).

Therefore, the maximum available depth is:
- If there is any depth with |S_D| ≥ 2, then the maximum such depth is the answer. (Because even if word i covers some nodes, the max depth with multiple nodes is always available.)
- Otherwise, all fragile nodes are at distinct depths (|S_D| = 1 for all D that have fragile nodes). Then the available depths are all except those on path(i). The answer is the maximum fragile depth that is not on path(i).

In the case where some depth has |S_D| ≥ 2, the global maximum depth might be one with |S_D| ≥ 2 or not. If the global max has |S_D| ≥ 2, it's always available. If the global max has |S_D| = 1, we might lose it, but we can use the next.

But note: the maximum depth among all fragile nodes is the global max. If this max has count ≥ 2 (|S_D| ≥ 2), then it's always available. If it has |S_D| = 1, we might need the next.

More precisely:
- Let D_max_frag = maximum depth among fragile nodes.
- If |S_{D_max_frag}| ≥ 2, then for any i, this depth is available. Answer = D_max_frag (from fragile side, then max with D_high).
- If |S_{D_max_frag}| = 1, let the node be u. Then for word i, this depth is available iff u ∉ path(i).
  - If u ∉ path(i), answer = D_max_frag.
  - If u ∈ path(i), we need the next highest available depth. This could be another depth with |S_D| ≥ 2, or another |S_D|=1 with node not on path(i), etc.

In the case where all fragile depths have |S_D| = 1, we have a set of depths, each with a unique node. We want the max depth where the node is not on path(i). Since the nodes are unique per depth, and each is on the path of some words. For word i, the nodes on its path are the prefixes. We want the max depth d such that the unique fragile node at depth d is not a prefix of word i.

This is equivalent to: among the fragile nodes, the one with max depth that is not an ancestor of word i (i.e., not a prefix).

We can precompute the fragile nodes. There are at most 10^5 of them. For each word i, we want the max depth fragile node not on its path. Since all fragile nodes are at distinct depths (in this subcase), we can just look at the sorted fragile nodes and find the first not on path(i). But the fragile nodes could be many.

However, note that in this subcase, each fragile node is the only one at its depth. This means the trie is such that no two different strings of the same length both have count exactly k. This is a restriction, but it could still be many.

But we can solve it by noting: for each word i, the fragile nodes on its path are exactly the prefixes of word i that have count k. We want the max depth of a fragile node not on this path.

Since the total number of (word, fragile ancestor) pairs is small (as argued, sum over words of number of fragile ancestors is O(sum lengths) = O(10^5)), we can perhaps do something with the Euler tour.

Another approach: for each fragile node v, we know its depth. We want, for each i, max_{v fragile, v not ancestor of i} depth(v). Equivalently, max depth of v where i is not in the subtree of v? No, ancestor means on the path from root to i. v is ancestor of i iff i is in the subtree of v (where subtree means all words with prefix v). But we are working with words, not nodes in the usual way. Actually, the trie node v corresponds to a prefix. The set of words that have v as prefix is exactly the set of words in the subtree of v (in the trie, rooted at v). So v is on path(i) iff word i is in the subtree of v.

So we want: for each i, max_{v fragile} depth(v) such that i ∉ subtree(v).

If we do an Euler tour of the trie, each node gets an interval [tin, tout]. Word i is a leaf or a path. Actually, each word corresponds to a leaf (or a node if we consider the word as a path, but words can be prefixes of others? The problem says array of strings, they can be duplicates or one prefix of another. In the trie, each word ends at some node. Let's call that node end_i for word i.

Then i ∈ subtree(v) iff end_i is in the subtree of v, which is true iff the path from root to end_i passes through v. This is equivalent to v being a prefix of word i, i.e., v is on the path to end_i. This is true iff tin(v) ≤ tin(end_i) ≤ tout(v) and they are in the same tree? In a trie, the condition for v to be ancestor of end_i in the tree rooted at root is exactly that end_i is in the subtree of v.

But the trie is a tree. The standard condition: v is ancestor of u iff tin(v) ≤ tin(u) ≤ tout(v).

So i ∈ subtree(v) iff v is ancestor of end_i in the trie.

Therefore, v is NOT on path(i) iff v is not an ancestor of end_i, i.e., end_i is not in subtree(v).

We want for each i: max depth of fragile v such that end_i is not in subtree(v).

This is a classic query: given a set of points (end_i) and a set of nodes (fragile v) with weights (depths), for each point, find the max weight of a node whose subtree does not contain the point.

Equivalently, min over v containing i of (max - depth(v))? Not exactly.

Since the trie has 10^5 nodes, and we have n=10^5 queries, we need O((n+N) log N) or similar.

We can process the queries by considering the complement: the nodes that contain i. For each i, the fragile nodes containing i are the fragile ancestors of end_i. Let this set be A_i. We want max over fragile nodes not in A_i.

This is similar to the earlier problem. Since the total size of A_i is small, and we want the global max not in A_i.

We can precompute the fragile nodes sorted by depth. The global max is at the top. If the top node is not in A_i, answer is its depth. If it is, we look at the next, etc.

In the worst case, for a given i, A_i could be large (up to 10^5 in theory, but sum |A_i| is O(10^5)). However, scanning from the top, we might scan many nodes before finding one not in A_i. This could be O(N) per query.

But note: the set of "top" nodes that are in A_i for many i... actually, the top node is in A_i for all i in its subtree. The subtree could be large. So for many i, the top node is in A_i. Then we look at the second node. The second node might also be in A_i for many i, etc. The total work could be large.

We need a smarter way.

Since the answer is max(D_high, max_frag_not_in_A_i), and D_high is easy.

For the fragile part: we want max depth of v fragile, v not ancestor of end_i.

Consider the fragile nodes. They form a subset of the trie. We can build a virtual tree or use segment tree on Euler tour.

Another idea: for each node v, let depth(v) be known. We want, for each leaf end_i, the max depth of a fragile node not on the path to end_i.

This is equivalent to: in the trie, remove the path to end_i, find the max depth fragile node in the remaining forest.

The remaining forest is the trie with the path to end_i removed. The max depth fragile node in this forest.

We can compute for each node the "highest fragile node not in the subtree of this node" or something.

Actually, since the trie is a tree, we can compute DP.

Let frag[v] be a boolean or the depth if v is fragile.

For each node v, define f(v) = max depth of fragile node in the subtree of v? No, we want not in subtree.

Let's define for each node v, g(v) = max depth of fragile node in the trie that is not in the subtree of v. This can be computed with a DP (rerooting).

Specifically:
- Let best[v] = max depth of fragile node in the subtree of v.
- Then for a node u, the max fragile node not in subtree of u is the max of best[child] for all children c of u? No, because there could be fragile nodes in other branches at the same level or higher up.

Standard reroot DP:
- First, compute down[v] = max depth of fragile node in subtree of v.
- Then, compute up[v] = max depth of fragile node not in subtree of v.
  - up[root] = -inf or 0.
  - For child c of v, the max not in subtree of c is max( up[v], best of other children of v, and if v is fragile, depth(v) (but v is not in subtree of c? v is ancestor of c, so v is in the path to c, so v is in the "subtree" of v but not in the subtree of c? Actually, for c, the set of nodes not in subtree(c) includes v and all nodes not in subtree(v). The nodes in subtree(v) but not in subtree(c) are exactly the other children of v and v itself. So we need to consider them.
  - Specifically, for child c, the available nodes for c are: all nodes not in subtree(c). This is: (all nodes not in subtree(v)) ∪ (v and its other children's subtrees).
  - So up[c] = max( up[v], depth(v) if v fragile, and for all siblings s of c, down[s] ).
  - We can precompute for each node v the top two down values among children to compute this efficiently.

Then for each word i, the answer for the fragile part is up[end_i], because the fragile nodes not on path to end_i are exactly the fragile nodes not in the subtree of end_i? Wait, the path to end_i is exactly the set of ancestors of end_i. A node is on the path to end_i iff it is an ancestor of end_i, i.e., in the subtree of the root? No, the ancestors of end_i form the path from root to end_i. A node is an ancestor of end_i iff end_i is in its subtree. So a node is NOT on the path to end_i iff it is NOT an ancestor of end_i, i.e., end_i is NOT in its subtree. This is exactly the nodes whose subtree does not contain end_i.

The set of nodes whose subtree does not contain end_i is: all nodes except the ancestors of end_i. The ancestors of end_i are exactly the nodes on the path from root to end_i. The nodes not in this set are everything else.

Is "up[end_i]" the max depth of fragile node whose subtree does not contain end_i? Let's see: up[end_i] is defined as the max depth of fragile node not in the subtree of end_i. Yes! That's exactly what we want.

Wait, is that correct? A node v is not in the subtree of end_i iff v is not a descendant of end_i? No, subtree of end_i consists of end_i and all its descendants. v is not in subtree(end_i) means v is not a descendant of end_i. But the nodes not on the path to end_i include nodes that are descendants of end_i? No! The path to end_i goes from root to end_i. The descendants of end_i are below end_i. If end_i is a leaf, no descendants. If end_i is an internal node, its descendants are in its subtree. But the path to end_i only goes down to end_i. The nodes below end_i (descendants of end_i) are NOT on the path to end_i. Are they in the subtree of end_i? Yes. So they are not in the set "not in subtree(end_i)".

But are they on the path to end_i? No, they are not. So they should be considered available.

Wait, there's a confusion. The fragile nodes we consider are all nodes in the trie. For word i, the path to word i is the sequence of nodes representing the prefixes of word i. The word i ends at node end_i. The nodes on this path are exactly the ancestors of end_i (including end_i). A node v is on the path iff v is an ancestor of end_i.

A node v is NOT on the path iff v is not an ancestor of end_i. This includes:
- Nodes in other branches at any ancestor.
- Nodes that are descendants of end_i? No! If v is a descendant of end_i, then end_i is an ancestor of v, so v is not an ancestor of end_i (unless v=end_i, but then it is an ancestor). So yes, descendants of end_i are not ancestors of end_i, so they are not on the path.

But wait: in the trie, if end_i has children, then words that are longer and have end_i as prefix exist. But in our array, word i is just one string. The set of words is the array. The trie is built from all words. The path for word i is its prefix path.

A node v is a prefix of word i iff the string represented by v is a prefix of word i. This means v is an ancestor of end_i in the trie.

Now, v is a descendant of end_i. Is v a prefix of word i? Only if v is on the path from root to end_i, which is the ancestors. The descendants of end_i are not ancestors of end_i (they are below). So they are not prefixes of word i. So they are not on the path.

Therefore, the set of available nodes (not on path) includes the descendants of end_i, as well as nodes in other subtrees.

The "not in subtree of end_i" means: v is not in the subtree rooted at end_i. The subtree rooted at end_i includes end_i and all its descendants. So "not in subtree" means v is not end_i and not a descendant. This includes ancestors (which are on the path) and nodes in other subtrees (which are not on the path).

So "not in subtree" is not the same as "not on path". The ancestors are not in the subtree of end_i (except end_i itself), but they are on the path.

Specifically:
- on path: ancestors of end_i (including end_i).
- not in subtree: everyone except end_i and its descendants.
- not on path: everyone except ancestors of end_i.

So "not in subtree" includes ancestors (which are bad, we want to exclude them) and excludes descendants (which are good, we want to include them).

So up[end_i] (max fragile not in subtree of end_i) is NOT what we want. It excludes the descendants of end_i, which are available (not on path). And it includes the ancestors, which are not available (on path).

This is the opposite!

We want the max fragile node that is not an ancestor of end_i.

Let me define:
- We want max depth of fragile v such that v is not an ancestor of end_i.
- Equivalently, min depth? No, max depth.

A node v is not an ancestor of end_i iff end_i is not in the subtree of v, OR v is a descendant of end_i? Let's think: v is ancestor of end_i iff end_i is in subtree(v). So v is NOT ancestor of end_i iff end_i is NOT in subtree(v).

But also, if v is a descendant of end_i, then end_i is ancestor of v, so end_i is in subtree(v) only if v=end_i? No, end_i is in subtree(v) only if v is an ancestor of end_i. If v is a descendant of end_i, then end_i is an ancestor of v, so v is not an ancestor of end_i, and end_i is not in subtree(v) (since subtree(v) is below v, end_i is above v). So yes, v not ancestor of end_i iff end_i not in subtree(v).

Is that true? Let's check:
- v = root: ancestor of everyone, so v is ancestor of end_i. end_i in subtree(root)? Yes. So end_i in subtree(v) => v ancestor.
- v = sibling of end_i: not ancestor. end_i in subtree(v)? No. So end_i not in subtree(v) => v not ancestor.
- v = child of end_i: not ancestor (since child is not ancestor of parent? Actually, child is descendant, not ancestor). end_i in subtree(v)? Subtree(v) is below child, so no. So end_i not in subtree(v) => v not ancestor.
- v = end_i itself: ancestor (trivially). end_i in subtree(v)? Yes, end_i is in its own subtree. So end_i in subtree(v) => v ancestor.

So yes! v is ancestor of end_i iff end_i is in subtree(v).

Therefore, v is NOT on path(i) (not an ancestor of end_i) iff end_i is NOT in subtree(v).

So the available nodes are exactly those v such that end_i ∉ subtree(v).

This is exactly the complement of the set of nodes whose subtree contains end_i.

The set of nodes whose subtree contains end_i is exactly the set of ancestors of end_i.

So the available nodes are the nodes that are not ancestors of end_i.

We want the max depth fragile node that is not an ancestor of end_i.

This is the same as: among all fragile nodes, the max depth of one whose subtree does not contain end_i.

This is what up[end_i] would give if up means "not in subtree", but we need to be careful.

up[v] as defined earlier: max depth of fragile node not in subtree(v). That is exactly: nodes whose subtree does not contain v. This is the same as nodes v' such that v is not in subtree(v'). Wait, "v' not in subtree(v)" means v is not a descendant of v'. That is, v is not in the subtree of v'. The condition "subtree of v' does not contain v" is the same as v' is not an ancestor of v. Because v is in subtree(v') iff v' is ancestor of v.

So "fragile node v' such that v' is not an ancestor of v" is exactly the nodes that are not ancestors of v.

Yes! So up[v] (if defined as max depth of fragile node v' such that v' is not an ancestor of v) is exactly what we want for the word ending at v.

So my earlier definition of up[v] should be: max depth of fragile node in the whole tree that is not an ancestor of v.

Can we compute this?

This is equivalent to: for each node v, find the max depth of a fragile node in the tree, excluding the ancestors of v.

We can compute this with a DP.

Let frag_depth[v] = depth(v) if v is fragile, else -inf.

First, compute down[v] = max depth of fragile node in subtree of v. This includes v itself.

Then, for each node v, we want up[v] = max depth of fragile node not in the "ancestor chain" of v? No, not in the set of ancestors of v. The set of ancestors of v is the path from root to v.

The available nodes for v are: all nodes that are not on the path from root to v. This includes:
- The siblings of nodes on the path to v and their subtrees.
- The descendants of v? No, descendants of v are in subtree(v). Are they on the path? No, path to v is the ancestors. Descendants are not ancestors. So descendants are available? Wait.

Let's clarify: the path to v is the set of ancestors of v. The nodes not on this path are all other nodes. This includes:
- Nodes in other subtrees of the root (i.e., not in subtree(root)??? whole tree is subtree of root).
- Specifically, for each node u on the path to v, the children of u that are not on the path to v, and their subtrees.
- Also, the descendants of v are not on the path to v (since path ends at v). So they are available.

But wait: in the trie, the path to v is the string v. The descendants of v are strings longer that have v as prefix. Are they considered "not on the path"? Yes, because the path to v is exactly the prefixes of v. A longer string is not a prefix of v, so it's not on the path.

So the available set for v is: the whole tree minus the ancestors of v.

This is the complement of the ancestor set.

To compute the max depth of fragile node not an ancestor of v.

We can compute the global max fragile depth, but we need to exclude the ancestors of v.

Since the ancestors of v form a chain, and we have many v, we can use the fact that the total number of (v, ancestor) pairs is small, but we need an efficient query.

We can compute for each node v:
- The max fragile depth in the whole tree excluding the subtree of v? No, that would exclude descendants too, which we want to include.

Actually, the set "not an ancestor of v" is: the whole tree minus the set of ancestors of v.

The set of ancestors of v is a path. We can precompute the fragile nodes. For each v, we need the max depth fragile node not on the path to v.

This is the same problem as before: for each query node v, the forbidden set is the path from root to v. We want the max depth fragile node not in this set.

Since the total number of fragile nodes is at most 10^5, and we have 10^5 queries, we need an efficient batch query.

One way: since the path to v is a set of nodes, and we want the max not in the set. We can use a segment tree on the Euler tour if the forbidden set is a subtree, but here it's a path from root, which is not a contiguous interval in general (it's a chain, which in Euler tour is multiple intervals? Actually, the ancestors of v form a chain, and in Euler tour, the subtree of an ancestor contains v. The set of ancestors is not a single interval, but we can still process.

Alternative: since the total size of all ancestor sets is O(total nodes) = O(10^5), we can process the queries in a specific order.

We can root the tree at root. For each node v, the ancestors of v are the nodes on the path from root to v.

We can compute for each node v:
- The max fragile depth in the tree that is not in the path to v.

This can be computed with a DFS. As we go down, we maintain a data structure of the fragile nodes not on the current path.

Specifically, we can do a DFS. Maintain a max-heap of the fragile nodes in the current "available" set. But when we go down to a child, the path gains the child and loses the root? No, going down, the path becomes longer. The available set loses the nodes on the path? No, the available set is everything not on the current path.

This is tricky because the available set changes as the path changes.

We can think of it as: initially, at root, the path is just [root]. The available set is everything except root. As we go to child c, the path becomes [root, c]. The available set loses c (since c is now on path). It gains nothing? Actually, it was losing root, but root is still on path. The change is: c is added to the path, so c is removed from available set. That's it.

Wait, is that right? At root, available = all nodes except root. At child c, available = all nodes except {root, c}. So we just remove c from the available set.

But what about the descendants? They were available at root (since not root), and at c they are still available (since not root or c). So yes, the only change when moving from parent to child is that the child is removed from the available set.

Is that true? The ancestors of c are the ancestors of parent plus c. So the forbidden set increases by {c}. Therefore, the available set decreases by {c}.

This is a huge insight! The set of nodes not on the path to current node v is simply: the set of all nodes minus the ancestors of v. When we move from parent p to child c, the ancestors of c are ancestors(p) ∪ {c}. So the available set for c is available(p) \ {c}.

Therefore, if we can maintain the max depth fragile node in the available set as we traverse the tree, we can compute the answer for each node in O(1) amortized per step.

We just need a data structure that supports:
- Remove a node (when we go down to it).
- Query max.
- Add a node back (when we go back up).

We can use a max-heap with lazy deletion (a dict of counts), or a sorted set.

Since we have at most 10^5 nodes and 10^5 operations, a heap is fine.

But wait: is the available set really just the previous minus the new node? Yes, because the forbidden set is the ancestors. When we go from p to c, the ancestors of c are ancestors(p) plus c. So available(c) = all nodes \ ancestors(c) = (all nodes \ ancestors(p)) \ {c} = available(p) \ {c}.

This is true for any tree! The ancestors of c are the ancestors of p plus c.

So we can do a DFS from root. Maintain a max-heap of (depth, node_id) for all fragile nodes. Initially, push all fragile nodes. Then root is in the path, so we should remove root if it is fragile? Wait, initially at root, the path is {root}. The available set is all nodes \ {root}. So we need to remove root from the heap.

Then for each child c of current node v:
- The available set for c is available(v) \ {c}. So we remove c from the heap.
- Now the top of the heap is the max depth fragile node in available(c).
- Record for c: this value (or 0 if empty).
- Recurse on c.
- When returning from c, add c back to the heap.

This gives us, for each node c, the max depth of a fragile node not on the path to c.

And this is exactly what we want for word i ending at node end_i!

Is that right? The path to end_i is the ancestors of end_i. The available set is the nodes not on this path. So yes!

And this handles both the descendants and other branches correctly, because the available set is maintained correctly via the simple rule.

Let's verify