from typing import List
from collections import defaultdict

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n < k:
            return [0] * n
        
        # Trie Node structure
        class TrieNode:
            __slots__ = ['children', 'count', 'indices', 'length']
            def __init__(self):
                self.children = {}
                self.count = 0
                self.indices = []
                self.length = 0
        
        root = TrieNode()
        
        # Step 1: Build Trie and count frequencies of all prefixes
        # Also store the list of indices that have this prefix
        for idx, word in enumerate(words):
            node = root
            for i, char in enumerate(word):
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
                node.count += 1
                node.indices.append(idx)
                node.length = i + 1
        
        # Step 2: Identify L_safe (max length of prefix with count >= k+1)
        # And group prefixes with count == k by length.
        safe_len = 0
        critical_by_len = defaultdict(list) # length -> list of index_lists
        
        # Traverse Trie to collect data (Iterative DFS to avoid recursion depth issues)
        stack = [root]
        while stack:
            node = stack.pop()
            if node.count >= k + 1:
                if node.length > safe_len:
                    safe_len = node.length
            elif node.count == k:
                if node.length > 0: # root has length 0, ignore
                    critical_by_len[node.length].append(node.indices)
            
            for child in node.children.values():
                stack.append(child)
        
        # Step 3: Initialize answer array
        ans = [safe_len] * n
        
        # Step 4: Process critical prefixes by length from max down to safe_len + 1
        # We maintain a list of indices that are not yet assigned a value > safe_len.
        assigned = [False] * n
        unassigned = list(range(n))
        
        # Sort lengths descending
        sorted_lengths = sorted(critical_by_len.keys(), reverse=True)
        
        for L in sorted_lengths:
            if L <= safe_len:
                break
            
            index_lists = critical_by_len[L]
            if not index_lists:
                continue
            
            # Compute intersection of all index_lists for this length
            # Optimization: Use the smallest list as the base for intersection
            min_list = min(index_lists, key=len)
            num_lists = len(index_lists)
            
            # Count occurrences of each index across all lists in this batch
            # Using a dictionary to avoid O(N) reset cost
            count_map = defaultdict(int)
            for idx_list in index_lists:
                for idx in idx_list:
                    count_map[idx] += 1
            
            # Determine the intersection
            current_intersection = []
            for idx in min_list:
                if count_map[idx] == num_lists:
                    current_intersection.append(idx)
            
            if not current_intersection:
                # Intersection is empty. This means for every index, there is at least one prefix 
                # of length L (with count k) that does not contain it. So L is valid for all unassigned indices.
                for i in unassigned:
                    ans[i] = L
                unassigned = []
            else:
                # Intersection is not empty.
                # For indices in intersection, L is NOT valid (because ALL critical prefixes of length L contain them).
                # For indices in unassigned but NOT in intersection, L IS valid.
                
                intersect_set = set(current_intersection)
                new_unassigned = []
                for i in unassigned:
                    if i not in intersect_set:
                        ans[i] = L
                    else:
                        new_unassigned.append(i)
                unassigned = new_unassigned
        
        return ans