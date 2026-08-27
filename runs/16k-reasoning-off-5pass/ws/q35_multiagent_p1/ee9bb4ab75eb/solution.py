class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n < k:
            return [0] * n
        
        # Build trie
        # Each node is a dict: {char: child_node}
        # We also store count at each node
        # To save memory and time, we use a list of dicts for children and a list for counts
        # root is index 0
        trie_children = [{}]  # list of dicts mapping char to node index
        trie_count = [0]      # count of words passing through this node
        
        def add_word(word: str):
            node = 0
            trie_count[node] += 1
            for char in word:
                if char not in trie_children[node]:
                    trie_children[node][char] = len(trie_children)
                    trie_children.append({})
                    trie_count.append(0)
                node = trie_children[node][char]
                trie_count[node] += 1
        
        for word in words:
            add_word(word)
            
        # Precompute valid_nodes_at_depth and valid_depths set
        # depth of root is 0, but we care about depths 1 to max_depth
        # Actually, the length of LCP is the depth of the node.
        # Root is depth 0, its children are depth 1, etc.
        # We want max depth d such that there exists a node at depth d with count >= k.
        
        # First, compute max depth
        max_depth = 0
        # We can compute depth during trie building or BFS. Let's do BFS.
        # But we can also just track it. Since sum of lengths is 10^5, max depth <= 10^4.
        # We'll use an array for valid_nodes_at_depth, size max_depth+1.
        # Actually, we don't know max_depth exactly, but we can use a dict or a large enough array.
        # Given constraints, max length of a word is 10^4, so max_depth <= 10000.
        
        # Let's do a BFS to assign depths and compute initial valid_nodes_at_depth
        from collections import deque
        depth_of_node = [0] * len(trie_children)
        # depth_of_node[0] = 0
        
        # We'll compute depths in BFS
        queue = deque([0])
        max_d = 0
        # To avoid recursion limit, use iterative BFS
        # We already have trie_children as list of dicts
        
        # Actually, we can compute depths during the initial add_word? No, because nodes are shared.
        # Let's do BFS.
        while queue:
            node = queue.popleft()
            d = depth_of_node[node]
            if d > max_d:
                max_d = d
            for char, child in trie_children[node].items():
                depth_of_node[child] = d + 1
                queue.append(child)
                
        max_depth = max_d
        
        # valid_nodes_at_depth[d] = number of nodes at depth d with count >= k
        valid_nodes_at_depth = [0] * (max_depth + 1)
        for i in range(1, len(trie_children)):  # skip root at depth 0 for LCP length, but root count is n, which is >=k, but depth 0 means LCP length 0? Actually, if no prefix, answer is 0.
            if trie_count[i] >= k:
                d = depth_of_node[i]
                valid_nodes_at_depth[d] += 1
                
        # valid_depths set: depths d where valid_nodes_at_depth[d] > 0
        valid_depths = set()
        for d in range(1, max_depth + 1):
            if valid_nodes_at_depth[d] > 0:
                valid_depths.add(d)
                
        def get_ans():
            if not valid_depths:
                return 0
            return max(valid_depths)
        
        def remove_word(word: str):
            node = 0
            # We need to record changes to revert later
            changes = []
            # Decrement count for root? Actually, root count is not used for LCP length directly, 
            # but it affects nothing for LCP length calculation because we look at depths >=1.
            # But for correctness, we decrement all nodes on path.
            # However, the condition for a node at depth d to be valid is count >= k.
            # Root is at depth 0, we ignore it for answer.
            
            # Process the word's path
            path_nodes = [0]
            for char in word:
                node = trie_children[node][char]
                path_nodes.append(node)
                
            for node in path_nodes:
                old_count = trie_count[node]
                if old_count >= k:
                    # It was valid, now it might become invalid
                    pass
                trie_count[node] -= 1
                new_count = trie_count[node]
                d = depth_of_node[node]
                if d == 0: 
                    continue # skip root for valid_depths tracking
                if old_count >= k and new_count < k:
                    # was valid, now invalid
                    valid_nodes_at_depth[d] -= 1
                    if valid_nodes_at_depth[d] == 0:
                        valid_depths.discard(d)
                # if old_count < k, it was already invalid, no change to valid_nodes_at_depth
                # if old_count >= k and new_count >= k, no change
                
            return path_nodes
            
        def add_word_back(path_nodes):
            for node in reversed(path_nodes):
                old_count = trie_count[node]
                trie_count[node] += 1
                new_count = trie_count[node]
                d = depth_of_node[node]
                if d == 0:
                    continue
                if old_count < k and new_count >= k:
                    # was invalid, now valid
                    valid_nodes_at_depth[d] += 1
                    valid_depths.add(d)
                    
        ans = []
        for i in range(n):
            path_nodes = remove_word(words[i])
            ans.append(get_ans())
            add_word_back(path_nodes)
            
        return ans