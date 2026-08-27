class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        total_len = n + m - 1
        
        # DSU class
        class DSU:
            def __init__(self, size):
                self.parent = list(range(size))
                self.rank = [0] * size
                self.forced_char = [None] * size  # The character that this group must be, or None
            
            def find(self, x):
                if self.parent[x] != x:
                    self.parent[x] = self.find(self.parent[x])
                return self.parent[x]
            
            def union(self, x, y):
                rx, ry = self.find(x), self.find(y)
                if rx == ry:
                    return
                if self.rank[rx] < self.rank[ry]:
                    rx, ry = ry, rx
                self.parent[ry] = rx
                if self.rank[rx] == self.rank[ry]:
                    self.rank[rx] += 1
                # Merge forced_char: if one is set, the other must match
                if self.forced_char[rx] is None:
                    self.forced_char[rx] = self.forced_char[ry]
                elif self.forced_char[ry] is not None:
                    if self.forced_char[rx] != self.forced_char[ry]:
                        return False  # Contradiction
                return True
            
            def set_forced(self, x, c):
                r = self.find(x)
                if self.forced_char[r] is None:
                    self.forced_char[r] = c
                elif self.forced_char[r] != c:
                    return False  # Contradiction
                return True
        
        dsu = DSU(total_len)
        
        # Process 'T' constraints
        for i in range(n):
            if str1[i] == 'T':
                # word[i:i+m] must equal str2
                for j in range(m):
                    idx = i + j
                    # Union all positions in the window
                    if j > 0:
                        if not dsu.union(i + j - 1, idx):
                            return ""
                    # Set the character for this position
                    if not dsu.set_forced(idx, str2[j]):
                        return ""
        
        # Build the initial word array based on DSU
        # For each group, if forced_char is set, all members get that char.
        # Otherwise, they are free (initially 'a').
        word = [''] * total_len
        for i in range(total_len):
            r = dsu.find(i)
            if dsu.forced_char[r] is not None:
                word[i] = dsu.forced_char[r]
            else:
                word[i] = 'a'  # Default to smallest
        
        # Now handle 'F' constraints
        # For each i where str1[i] == 'F', we need word[i:i+m] != str2
        # We process from left to right. If a violation is found, we fix it
        # by changing the rightmost unfixed character in the window to the smallest valid char.
        
        for i in range(n):
            if str1[i] == 'F':
                # Check if current word[i:i+m] equals str2
                # Since m is small (<=500), direct comparison is acceptable here
                # But we need to be careful: we are modifying word as we go.
                # We check the current state of word.
                match = True
                for j in range(m):
                    if word[i + j] != str2[j]:
                        match = False
                        break
                if match:
                    # Need to break the match by changing one character in word[i:i+m]
                    # To keep lexicographically smallest, change the rightmost unfixed character
                    # An index k in [i, i+m-1] is "unfixed" if it is not forced by any 'T' constraint.
                    # In our DSU, an index is unfixed if its root's forced_char is None.
                    # But note: we already built the word array. We need to know which positions are fixed.
                    # We can precompute a fixed array.
                    pass
        
        # Precompute which positions are fixed (forced by 'T' constraints)
        fixed = [False] * total_len
        for i in range(total_len):
            r = dsu.find(i)
            if dsu.forced_char[r] is not None:
                fixed[i] = True
        
        # Re-process 'F' constraints with the ability to modify word
        for i in range(n):
            if str1[i] == 'F':
                # Check if current word[i:i+m] equals str2
                match = True
                for j in range(m):
                    if word[i + j] != str2[j]:
                        match = False
                        break
                if match:
                    # Find the rightmost unfixed index in [i, i+m-1]
                    change_idx = -1
                    for j in range(m - 1, -1, -1):
                        if not fixed[i + j]:
                            change_idx = i + j
                            break
                    if change_idx == -1:
                        # All positions in the window are fixed, and they match str2 -> impossible
                        return ""
                    # Change word[change_idx] to the smallest character that doesn't match str2[change_idx - i]
                    target_char = str2[change_idx - i]
                    # Try 'a', 'b', ... until we find one that is not target_char
                    for c in 'abcdefghijklmnopqrstuvwxyz':
                        if c != target_char:
                            word[change_idx] = c
                            break
        
        return "".join(word)