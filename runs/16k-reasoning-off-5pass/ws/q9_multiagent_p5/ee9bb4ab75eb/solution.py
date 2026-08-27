from typing import List

class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        # Build the Trie with frequency counts
        root = TrieNode()
        for word in words:
            self._insert(root, word)
        
        n = len(words)
        answer = []
        
        # For each index i, simulate removal of words[i]
        for i in range(n):
            word = words[i]
            curr = root
            
            # Step 1: Decrement counts along the path of the removed word
            # This simulates removing words[i] from the set
            for char in word:
                if char in curr.children:
                    curr = curr.children[char]
                    curr.count -= 1
                else:
                    # Should not happen as the word exists in the Trie
                    break
            
            # Step 2: Find the longest common prefix among any k remaining strings
            # Traverse the Trie to find the deepest node with count >= k
            max_len = 0
            curr = root
            for char in word:
                if char in curr.children:
                    next_node = curr.children[char]
                    if next_node.count >= k:
                        max_len += 1
                        curr = next_node
                    else:
                        # If count < k, no k strings share this prefix
                        break
                else:
                    break
            
            answer.append(max_len)
            
            # Step 3: Restore counts for the next iteration
            # Revert the decrements to maintain the correct state
            curr = root
            for char in word:
                if char in curr.children:
                    curr = curr.children[char]
                    curr.count += 1
                else:
                    break
        
        return answer
    
    def _insert(self, root: TrieNode, word: str) -> None:
        curr = root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
            curr.count += 1

# Test with provided examples
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    words1 = ["jump","run","run","jump","run"]
    k1 = 2
    result1 = sol.longestCommonPrefix(words1, k1)
    expected1 = [3, 4, 4, 3, 4]
    print(f"Example 1 Result: {result1}")
    print(f"Example 1 Expected: {expected1}")
    print(f"Example 1 Match: {result1 == expected1}")
    
    # Example 2
    words2 = ["dog","racer","car"]
    k2 = 2
    result2 = sol.longestCommonPrefix(words2, k2)
    expected2 = [0, 0, 0]
    print(f"Example 2 Result: {result2}")
    print(f"Example 2 Expected: {expected2}")
    print(f"Example 2 Match: {result2 == expected2}")