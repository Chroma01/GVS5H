class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n < k:
            return [0] * n
        
        # Build Trie
        # Each node is a dict: {'count': int, 'children': dict}
        root = {'count': 0, 'children': {}}
        
        for word in words:
            node = root
            node['count'] += 1
            for char in word:
                if char not in node['children']:
                    node['children'][char] = {'count': 0, 'children': {}}
                node = node['children'][char]
                node['count'] += 1
        
        # Collect counts per depth
        # depth 0 is root, depth 1 is first char, etc.
        # We'll use a list of lists to store counts at each depth
        max_depth = 0
        for word in words:
            if len(word) > max_depth:
                max_depth = len(word)
        
        # counts_at_depth[d] will be a list of counts of nodes at depth d
        counts_at_depth = [[] for _ in range(max_depth + 1)]
        
        # Traverse the Trie to collect counts at each depth
        # We can do a BFS or DFS. Here we use DFS.
        stack = [(root, 0)]
        while stack:
            node, depth = stack.pop()
            if depth <= max_depth:
                counts_at_depth[depth].append(node['count'])
            for child in node['children'].values():
                stack.append((child, depth + 1))
        
        # Precompute m1, m2, cnt1 for each depth
        m1 = [0] * (max_depth + 1)
        m2 = [0] * (max_depth + 1)
        cnt1 = [0] * (max_depth + 1)
        
        for d in range(max_depth + 1):
            counts = counts_at_depth[d]
            if not counts:
                continue
            # Find top two counts
            c_sorted = sorted(counts, reverse=True)
            m1[d] = c_sorted[0]
            if len(c_sorted) > 1:
                m2[d] = c_sorted[1]
            else:
                m2[d] = 0
            cnt1[d] = sum(1 for c in counts if c == m1[d])
        
        # For each word, compute the answer
        answer = [0] * n
        
        for i, word in enumerate(words):
            # If removing this word leaves fewer than k words, answer is 0
            if n - 1 < k:
                answer[i] = 0
                continue
            
            # Traverse the Trie for the current word to get depths where it passes
            # We want the largest depth d such that adjusted count >= k
            node = root
            best_d = 0
            # Depth 0 always has count n, which is >= k (since n >= k initially, and after removal n-1 might be < k? 
            # But if n-1 < k, we already handled it. So for n-1 >= k, depth 0 is always valid.
            # We check depths from 1 to len(word)
            for j, char in enumerate(word):
                depth = j + 1
                if char not in node['children']:
                    break
                node = node['children'][char]
                # The count at this node (before removal) is node['count']
                # Adjusted count: if this node is the unique max at this depth, then m2, else m1
                if node['count'] == m1[depth] and cnt1[depth] == 1:
                    adj_count = m2[depth]
                else:
                    adj_count = m1[depth]
                
                if adj_count >= k:
                    best_d = depth
                else:
                    # Since we are going in increasing depth order, if at some depth the condition fails,
                    # deeper depths might still satisfy? No, because if a prefix of length d is not shared by k words,
                    # a longer prefix cannot be either. But actually, we are checking per node. 
                    # However, the condition "adj_count >= k" is for the best possible LCP at that depth.
                    # If at depth d, the best adjusted count is < k, then for any deeper depth, the count can only be <= adj_count (since it's a subset).
                    # So we can break early? Actually, no: because we are traversing one specific path. 
                    # But the answer is the maximum depth over ALL nodes at that depth. 
                    # We are checking: for the current word's path, at depth d, what is the max adjusted count achievable at depth d?
                    # And we take the max d for which that is >= k.
                    # It is possible that at depth d, the best adjusted count is < k, but at depth d+1, for a different branch, it might be >= k? 
                    # No, because we are removing word i, and we are checking for the existence of ANY k words. 
                    # The value adj_count at depth d is the maximum number of words (excluding word i if it passes through the max node) that share a prefix of length d.
                    # If adj_count < k, then no prefix of length d is shared by k words (after removal). 
                    # And for any deeper prefix, the count is <= adj_count. So we can break.
                    break
            
            answer[i] = best_d
        
        return answer