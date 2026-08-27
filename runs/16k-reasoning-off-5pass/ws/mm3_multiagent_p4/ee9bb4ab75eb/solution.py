import sys
sys.setrecursionlimit(200000)
from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        class Node:
            __slots__ = ('children', 'count', 'depth', 'tin', 'tout')
            def __init__(self):
                self.children = {}
                self.count = 0
                self.depth = 0
                self.tin = 0
                self.tout = 0

        root = Node()
        all_nodes = [root]
        terminal = []  # terminal node for each word

        for word in words:
            curr = root
            curr.count += 1
            for ch in word:
                if ch not in curr.children:
                    new_node = Node()
                    new_node.depth = curr.depth + 1
                    curr.children[ch] = new_node
                    all_nodes.append(new_node)
                curr = curr.children[ch]
                curr.count += 1
            terminal.append(curr)

        # DFS for tin/tout (Euler tour)
        time = 0
        def dfs(u):
            nonlocal time
            u.tin = time
            time += 1
            for v in u.children.values():
                dfs(v)
            u.tout = time - 1
        dfs(root)

        # Candidates: nodes with count >= k
        candidates = [node for node in all_nodes if node.count >= k]
        # Sort by depth descending so we can find the deepest non-ancestor quickly
        candidates.sort(key=lambda x: x.depth, reverse=True)

        n = len(words)
        ans = [0] * n

        for i in range(n):
            # Compute on_path_max: deepest node on the path of words[i] with count >= k+1
            on_path = 0
            curr = root
            for ch in words[i]:
                curr = curr.children[ch]
                if curr.count >= k + 1:
                    if curr.depth > on_path:
                        on_path = curr.depth

            # Compute off_path_max: deepest candidate node that is NOT an ancestor of terminal[i]
            off_path = 0
            target = terminal[i]
            for cand in candidates:
                # cand is an ancestor of target iff tin[cand] <= tin[target] and tout[cand] >= tout[target]
                if not (cand.tin <= target.tin and cand.tout >= target.tout):
                    off_path = cand.depth
                    break

            ans[i] = max(on_path, off_path)

        return ans