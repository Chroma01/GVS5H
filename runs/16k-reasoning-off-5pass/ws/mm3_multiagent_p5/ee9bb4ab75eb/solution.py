from typing import List
from collections import defaultdict

class TrieNode:
    __slots__ = ('children', 'count', 'id')
    def __init__(self):
        self.children = {}
        self.count = 0
        self.id = -1

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n == k:
            return [0] * n
        
        root = TrieNode()
        for w in words:
            node = root
            for ch in w:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
                node.count += 1
        
        total_eq = defaultdict(int)
        max_depth_gt = 0
        first_id_at_depth = {}
        node_id_counter = 0
        
        def dfs(node, depth):
            nonlocal node_id_counter, max_depth_gt
            node.id = node_id_counter
            node_id_counter += 1
            if node.count > k:
                if depth > max_depth_gt:
                    max_depth_gt = depth
            if node.count == k:
                total_eq[depth] += 1
                if depth not in first_id_at_depth:
                    first_id_at_depth[d] = node.id
            for ch, child in node.children.items():
                dfs(child, depth + 1)
        
        dfs(root, 0)
        
        unique_eq_id = {}
        for d, cnt in total_eq.items():
            if cnt == 1:
                unique_eq_id[d] = first_id_at_depth[d]
        
        M1 = 0
        for d, cnt in total_eq.items():
            if cnt > 1 and d > M1:
                M1 = d
        
        unique_depths_above_M1 = [d for d in total_eq if total_eq[d] == 1 and d > M1]
        unique_depths_above_M1.sort(reverse=True)
        
        ans = []
        for w in words:
            node = root
            blocked = set()
            depth = 0
            for ch in w:
                node = node.children[ch]
                depth += 1
                if total_eq.get(depth, 0) == 1:
                    if unique_eq_id.get(depth) == node.id:
                        blocked.add(depth)
            
            max_unique_not_blocked = 0
            for d in unique_depths_above_M1:
                if d not in blocked:
                    max_unique_not_blocked = d
                    break
            
            D_eq = max(M1, max_unique_not_blocked)
            ans_i = max(max_depth_gt, D_eq)
            ans.append(ans_i)
        
        return ans