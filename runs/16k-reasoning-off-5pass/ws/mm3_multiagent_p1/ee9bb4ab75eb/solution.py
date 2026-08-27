from typing import List
import heapq
from collections import defaultdict
import sys

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # If removing any element leaves fewer than k strings, all answers are 0
        if n - 1 < k:
            return [0] * n
        
        # Build trie
        # Each node: index 0 is root
        # children: list of dicts mapping char -> child node index
        # counts: list of ints, count of words passing through this node
        # depths: list of ints, depth of the node (length of prefix)
        children = []
        counts = []
        depths = []
        
        children.append({})
        counts.append(0)
        depths.append(0)
        
        end_nodes = []  # node index where each word ends
        
        # First pass: build trie structure and record end_nodes
        for word in words:
            node = 0
            for ch in word:
                if ch not in children[node]:
                    children.append({})
                    counts.append(0)
                    depths.append(depths[node] + 1)
                    children[node][ch] = len(children) - 1
                node = children[node][ch]
            end_nodes.append(node)
        
        # Second pass: count occurrences at each node (including root for empty prefix)
        for word in words:
            node = 0
            counts[node] += 1
            for ch in word:
                node = children[node][ch]
                counts[node] += 1
        
        # Classify nodes
        # D_high: max depth of always-on nodes (count >= k+1)
        D_high = 0
        fragile_nodes = []  # list of (depth, node_id) for nodes with count == k
        
        for i in range(len(counts)):
            if counts[i] >= k + 1:
                if depths[i] > D_high:
                    D_high = depths[i]
            elif counts[i] == k:
                fragile_nodes.append((depths[i], i))
        
        # If no fragile nodes and D_high is 0, all answers are 0
        if not fragile_nodes and D_high == 0:
            return [0] * n
        
        # Build adjacency list for DFS
        adj = [[] for _ in range(len(counts))]
        for u in range(len(counts)):
            for v in children[u].values():
                adj[u].append(v)
        
        # Initialize max-heap (using negative depths) and active counter
        heap = []
        active = {}  # node_id -> count (1 if available, 0 if on current path)
        
        for depth, node_id in fragile_nodes:
            heapq.heappush(heap, (-depth, node_id))
            active[node_id] = 1
        
        node_depth = depths  # reference for convenience
        
        # Mark root as inactive (on the path)
        if 0 in active:
            active[0] = 0
        
        # Function to get current max depth of available fragile nodes
        def get_current_max():
            while heap:
                d_neg, nid = heap[0]
                if active.get(nid, 0) == 0:
                    heapq.heappop(heap)
                else:
                    return -d_neg
            return 0
        
        # ans_frag[node] = max depth of fragile node not on path to this node
        ans_frag = [0] * len(counts)
        
        # Iterative DFS to avoid recursion limit issues
        # Stack contains tuples: (node, state, child_index)
        # state 0: entering, state 1: leaving
        # But we need to handle the active marking carefully.
        # We'll simulate recursion with a stack.
        
        # Actually, we need to:
        # 1. When entering node u, it is already marked inactive (by parent or initially for root)
        # 2. Record answer for u
        # 3. For each child v: mark v inactive, then process v
        # 4. After all children, mark u active
        
        # Let's use a stack with (node, action)
        # action 'enter' or 'exit'
        # But we need to iterate children. We can push exit after all children.
        # Simpler: use recursion with increased limit.
        
        sys.setrecursionlimit(200000)
        
        def dfs(u):
            # u is on the path, so it's marked inactive before this call
            current_max = get_current_max()
            ans_frag[u] = current_max
            
            for v in adj[u]:
                # Mark child inactive
                if v in active:
                    active[v] -= 1
                dfs(v)
                # Mark child active
                if v in active:
                    active[v] += 1
                    heapq.heappush(heap, (-node_depth[v], v))
        
        dfs(0)
        
        # Compute final answers
        result = []
        for i in range(n):
            node = end_nodes[i]
            best = max(D_high, ans_frag[node])
            result.append(best)
        
        return result