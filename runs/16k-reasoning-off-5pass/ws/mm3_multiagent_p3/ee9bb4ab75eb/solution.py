from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if k > n - 1:
            return [0] * n
        
        # Build trie: each node stores children dict, word count, and prefix depth
        children = [{}]  # node index -> {char: child node index}
        cnt = [0]        # count of words passing through this node
        depth = [0]      # depth = length of prefix
        
        for word in words:
            node = 0
            for ch in word:
                if ch not in children[node]:
                    children[node][ch] = len(children)
                    children.append({})
                    cnt.append(0)
                    depth.append(depth[node] + 1)
                node = children[node][ch]
                cnt[node] += 1
        
        # Map each word to its leaf node
        leaf_nodes = []
        for word in words:
            node = 0
            for ch in word:
                node = children[node][ch]
            leaf_nodes.append(node)
        
        # Post-order traversal to compute subtree_max: deepest node in subtree with cnt == k
        order = []
        stack = [(0, False)]
        while stack:
            node, visited = stack.pop()
            if visited:
                order.append(node)
            else:
                stack.append((node, True))
                for child in children[node].values():
                    stack.append((child, False))
        
        subtree_max = [0] * len(cnt)
        for node in order:
            max_d = depth[node] if cnt[node] == k else 0
            for child in children[node].values():
                if subtree_max[child] > max_d:
                    max_d = subtree_max[child]
            subtree_max[node] = max_d
        
        # sub_max_excl: deepest cnt==k node in subtree excluding self
        sub_max_excl = [0] * len(cnt)
        for node in range(len(cnt)):
            max_d = 0
            for child in children[node].values():
                if subtree_max[child] > max_d:
                    max_d = subtree_max[child]
            sub_max_excl[node] = max_d
        
        # sib_max: deepest cnt==k node among siblings
        sib_max = [0] * len(cnt)
        for v in range(len(cnt)):
            child_list = list(children[v].values())
            if len(child_list) <= 1:
                if child_list:
                    sib_max[child_list[0]] = 0
                continue
            max1, max2 = 0, 0
            for c in child_list:
                sm = subtree_max[c]
                if sm > max1:
                    max2 = max1
                    max1 = sm
                elif sm > max2:
                    max2 = sm
            for c in child_list:
                if subtree_max[c] == max1:
                    sib_max[c] = max2
                else:
                    sib_max[c] = max1
        
        # up_max: top-down, deepest cnt==k node outside the path (from ancestors' other branches and above)
        up_max = [0] * len(cnt)
        stack = [0]
        while stack:
            v = stack.pop()
            for c in children[v].values():
                # The "outside" for child c consists of:
                # 1. The outside for v (up_max[v])
                # 2. The parent v itself if v is cnt==k
                # 3. The sibling subtrees (sib_max[c])
                val = up_max[v]
                if cnt[v] == k and depth[v] > val:
                    val = depth[v]
                if sib_max[c] > val:
                    val = sib_max[c]
                up_max[c] = val
                stack.append(c)
        
        # max_outside_path: deepest cnt==k node not on the path to this node
        # This combines: outside the subtree (up_max), sibling subtrees (sib_max), 
        # and the current subtree excluding self (sub_max_excl)
        max_outside_path = [0] * len(cnt)
        for node in range(len(cnt)):
            m = up_max[node]
            if sib_max[node] > m:
                m = sib_max[node]
            if sub_max_excl[node] > m:
                m = sub_max_excl[node]
            max_outside_path[node] = m
        
        # Global maximum depth for nodes with count >= k+1 (always safe after any removal)
        max_k_plus_1 = 0
        for i in range(1, len(cnt)):
            if cnt[i] >= k + 1 and depth[i] > max_k_plus_1:
                max_k_plus_1 = depth[i]
        
        # Build answer for each word
        ans = []
        for leaf in leaf_nodes:
            res = max_k_plus_1
            if max_outside_path[leaf] > res:
                res = max_outside_path[leaf]
            ans.append(res)
        return ans