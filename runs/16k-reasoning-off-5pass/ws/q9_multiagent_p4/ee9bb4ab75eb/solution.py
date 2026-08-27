from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # If removing one element leaves fewer than k strings, the answer is 0 for all i.
        if n - 1 < k:
            return [0] * n
        
        # Trie construction
        # Each node is represented by an index.
        # trie_children[u][char_index] -> index of child node, or -1 if none
        # trie_count[u] -> count of words passing through node u
        trie_children = []
        trie_count = []
        
        def new_node():
            trie_children.append([-1] * 26)
            trie_count.append(0)
            return len(trie_children) - 1
        
        root = new_node()
        
        # Build the Trie
        for word in words:
            node = root
            for char in word:
                idx = ord(char) - ord('a')
                if trie_children[node][idx] == -1:
                    trie_children[node][idx] = new_node()
                node = trie_children[node][idx]
            trie_count[node] += 1
        
        # BFS to assign depths and collect nodes with count == k
        num_nodes = len(trie_children)
        depths = [-1] * num_nodes
        depths[root] = 0
        queue = [root]
        idx = 0
        
        nodes_k = []  # List of (depth, node_index) for nodes with count == k
        
        while idx < len(queue):
            u = queue[idx]
            idx += 1
            d = depths[u]
            
            if trie_count[u] == k:
                nodes_k.append((d, u))
            
            for char_code in range(26):
                v = trie_children[u][char_code]
                if v != -1:
                    depths[v] = d + 1
                    queue.append(v)
        
        # Sort nodes_k by depth descending to quickly find the deepest valid node with count == k
        nodes_k.sort(key=lambda x: x[0], reverse=True)
        
        # Precompute max_depth_greater_k: max depth of any node with count > k
        # Nodes with count > k are always valid after removing any single word because count - 1 >= k.
        max_depth_greater_k = -1
        for i, count in enumerate(trie_count):
            if count > k:
                if depths[i] > max_depth_greater_k:
                    max_depth_greater_k = depths[i]
        
        ans = []
        
        # For each word, simulate removal
        for i, word in enumerate(words):
            # Mark nodes on the path of word[i]
            # We use a set for O(1) lookup.
            path_set = set()
            node = root
            # Traverse the path of the current word
            for char in word:
                idx = ord(char) - ord('a')
                node = trie_children[node][idx]
                path_set.add(node)
            
            # Candidate 1: max_depth_greater_k
            # If max_depth_greater_k is -1, it means no node has count > k.
            # However, since n > k (checked at start), root has count n > k, so max_depth_greater_k >= 0.
            cand1 = max_depth_greater_k
            
            # Candidate 2: max depth of a node with count == k that is NOT on the path
            # We iterate nodes_k (sorted by depth descending) and pick the first one not in path_set.
            cand2 = -1
            for d, u in nodes_k:
                if u not in path_set:
                    cand2 = d
                    break
            
            # The answer is the maximum of the two candidates.
            # Since n > k, at least one candidate will be >= 0.
            ans.append(max(cand1, cand2))
        
        return ans