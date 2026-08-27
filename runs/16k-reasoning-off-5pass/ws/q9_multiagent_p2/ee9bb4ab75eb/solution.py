from typing import List, Dict
from collections import deque

class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.count = 0

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n < k:
            return [0] * n
        
        root = TrieNode()
        # Build Trie and count frequencies
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
                node.count += 1
        
        # Identify global_base: max depth among nodes with count >= k + 1
        global_base = 0
        
        # Map: depth -> count of nodes at that depth with count == k
        depth_nodes_count: Dict[int, int] = {}
        
        # BFS to collect stats
        queue = deque([(root, 0)])
        while queue:
            node, depth = queue.popleft()
            if node.count >= k + 1:
                if depth > global_base:
                    global_base = depth
            if node.count == k:
                if depth not in depth_nodes_count:
                    depth_nodes_count[depth] = 0
                depth_nodes_count[depth] += 1
            # Add children to queue
            for child in node.children.values():
                queue.append((child, depth + 1))
        
        # Determine M1 and M2 from singleton depths
        # Singletons are depths where depth_nodes_count[d] == 1
        singleton_depths = [d for d, cnt in depth_nodes_count.items() if cnt == 1]
        singleton_depths.sort(reverse=True)
        
        ans = [global_base] * n
        
        # For each word, check if it passes through the specific node at depth m1
        # that has count == k. If so, m1 is blocked for this word.
        # We then check if m2 is blocked, and so on, but optimized by checking counts on the path.
        for i, word in enumerate(words):
            if singleton_depths:
                node = root
                blocked_depths = set()
                
                # Traverse the path of the word
                # We only need to check depths up to m1 because singleton_depths are sorted descending
                # and we want the max valid depth. Any depth > m1 is not a singleton.
                limit = min(len(word), singleton_depths[0])
                
                for j in range(limit):
                    char = word[j]
                    if char not in node.children:
                        break
                    node = node.children[char]
                    depth = j + 1
                    
                    # Check if this depth is a singleton and the current node is the one with count k
                    if depth in depth_nodes_count and depth_nodes_count[depth] == 1:
                        if node.count == k:
                            blocked_depths.add(depth)
                
                # Find the largest singleton depth that is NOT blocked
                best_singleton = 0
                for d in singleton_depths:
                    if d not in blocked_depths:
                        best_singleton = d
                        break
                
                if best_singleton > ans[i]:
                    ans[i] = best_singleton
        
        return ans