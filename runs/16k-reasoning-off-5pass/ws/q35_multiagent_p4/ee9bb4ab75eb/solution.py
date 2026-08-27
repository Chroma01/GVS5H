class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # If total words less than k, all answers are 0
        if n < k:
            return [0] * n
        
        # Build Trie
        # Each node is a dict: {char: node_index}
        # We also store count at each node index
        # nodes[i] = {'count': int, 'children': {char: next_node_index}}
        # Using lists for performance
        trie_count = [0]
        trie_children = [{}]
        
        def add_word(word):
            node = 0
            trie_count[node] += 1
            for char in word:
                if char not in trie_children[node]:
                    trie_children[node][char] = len(trie_count)
                    trie_count.append(0)
                    trie_children.append({})
                node = trie_children[node][char]
                trie_count[node] += 1
        
        for word in words:
            add_word(word)
            
        # Function to find the deepest node with count >= k
        # We can do a DFS/BFS. To get the deepest, we can just traverse.
        # But doing a full tree traversal for each query is O(nodes) which is too slow.
        # Optimization: The answer is the maximum depth d such that there is a node at depth d with count >= k.
        # We can precompute the global max depth node? No, it changes.
        # However, note that the count is monotonic: if a node has count >= k, its parent has count >= k.
        # So we want the largest depth.
        # We can store for each node, the maximum depth in its subtree that has count >= k?
        # That's complex to update.
        
        # Alternative efficient approach for query:
        # Since we only change counts on one path, the new answer is either:
        # 1. The same as before (if the removed word didn't reduce the count of the best prefix node below k)
        # 2. Or we need to find the next best.
        # But tracking "best" is hard.
        
        # Let's use the sorting + segment tree approach instead, which is proven efficient.
        # But the prompt asks for Trie-based. Let's implement a fast Trie query.
        # Actually, we can optimize the "find deepest node" by noting:
        # We only need to check nodes that are on the paths of the words.
        # And we can pre-sort nodes by depth? 
        # Given constraints (sum of lengths <= 10^5), the total number of nodes is <= 10^5.
        # If we do a BFS/DFS for each query, worst case 10^5 * 10^5 = 10^10, too slow.
        
        # We need a better way. Let's use the fact that we can store the max depth with count >= k for each node's subtree?
        # Or, we can simply iterate over all nodes? No.
        
        # Actually, a simpler observation: The answer for a removal is the maximum depth d such that 
        # there exists a prefix of length d that appears in at least k words (after removal).
        # We can maintain a frequency array of depths? 
        # Let freq[d] = number of nodes at depth d with count >= k.
        # When we decrement counts, we might reduce a node's count below k.
        # We can update freq[d] accordingly.
        # Then the answer is the maximum d such that freq[d] > 0.
        # We can maintain a max-heap or a set of valid depths.
        
        # Steps for Trie with freq array:
        # 1. Build trie, compute counts.
        # 2. Compute initial freq array: for each node, if count >= k, increment freq[depth].
        # 3. Maintain a variable max_valid_depth.
        # 4. For each word removal:
        #    a. Decrement counts on the path. For each node on the path, if count becomes k-1, then this depth is no longer valid from this node. 
        #       But other nodes at the same depth might still be valid. So we need freq[depth] to track how many nodes at that depth have count >= k.
        #    b. After decrementing, check if max_valid_depth is still valid (freq[max_valid_depth] > 0). If not, decrement max_valid_depth until freq[max_valid_depth] > 0.
        #    c. Record answer.
        #    d. Increment counts on the path back. For each node on the path, if count becomes k, then this depth becomes valid again. Increment freq[depth]. Update max_valid_depth if needed.
        
        # This approach is O(L) per word, total O(sum of lengths) which is 10^5. Perfect.
        
        # Rebuild trie with depth tracking
        # We'll store depth for each node
        trie_depth = [0]
        # Reset trie structures
        trie_count = [0]
        trie_children = [{}]
        
        def add_word_with_depth(word):
            node = 0
            trie_count[node] += 1
            # depth of root is 0
            for char in word:
                if char not in trie_children[node]:
                    trie_children[node][char] = len(trie_count)
                    trie_count.append(0)
                    trie_children.append({})
                    trie_depth.append(trie_depth[node] + 1)
                node = trie_children[node][char]
                trie_count[node] += 1
        
        for word in words:
            add_word_with_depth(word)
            
        num_nodes = len(trie_count)
        max_depth = 0
        for d in trie_depth:
            if d > max_depth:
                max_depth = d
                
        # freq[d] = number of nodes at depth d with count >= k
        freq = [0] * (max_depth + 1)
        for i in range(num_nodes):
            if trie_count[i] >= k:
                freq[trie_depth[i]] += 1
                
        # Current max valid depth
        current_max_valid = 0
        for d in range(max_depth, -1, -1):
            if freq[d] > 0:
                current_max_valid = d
                break
                
        ans = []
        
        for word in words:
            # Remove word: decrement counts on path
            node = 0
            # We need to track which nodes were modified to restore later
            path_nodes = []
            for char in word:
                path_nodes.append(node)
                node = trie_children[node][char]
                path_nodes.append(node)
                # Decrement count
                trie_count[node] -= 1
                # If count drops from k to k-1, then this depth loses one valid node
                if trie_count[node] == k - 1:
                    d = trie_depth[node]
                    freq[d] -= 1
                    # If this depth was the current max valid, we might need to lower it
                    if d == current_max_valid:
                        # Find new max valid depth
                        while current_max_valid > 0 and freq[current_max_valid] == 0:
                            current_max_valid -= 1
                        # If current_max_valid becomes 0, check if freq[0] > 0? 
                        # freq[0] is always n (root count), so if n >= k, freq[0] > 0.
                        # But if n < k, we handled that at start. So current_max_valid will be at least 0.
            
            # The answer for this removal is current_max_valid
            # But note: if the remaining number of words is less than k, answer is 0.
            # We already handled n < k at start. Here, after removal, n-1 >= k is guaranteed if n > k.
            # If n == k, then after removal, n-1 = k-1 < k, so answer should be 0.
            # We need to check: if n - 1 < k, then answer is 0.
            if n - 1 < k:
                ans.append(0)
            else:
                ans.append(current_max_valid)
                
            # Restore word: increment counts on path
            # Traverse path in reverse
            for i in range(len(path_nodes) - 1, -1, -1):
                node = path_nodes[i]
                trie_count[node] += 1
                # If count rises from k-1 to k, then this depth gains one valid node
                if trie_count[node] == k:
                    d = trie_depth[node]
                    freq[d] += 1
                    if d > current_max_valid:
                        current_max_valid = d
                        
        return ans