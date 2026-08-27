from collections import Counter
from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n < k:
            return [0] * n
        
        # Step 1: Count all prefixes
        prefix_counts = Counter()
        for word in words:
            for l in range(1, len(word) + 1):
                prefix_counts[word[:l]] += 1
        
        # Step 2: For each length L, find the max count and second max count
        # Also track which prefix achieves the max count (to know if it's affected by removal)
        # We only care about lengths that appear in the words
        max_len = max(len(word) for word in words)
        
        # max_count[L] = maximum frequency of any prefix of length L
        # second_max_count[L] = second maximum frequency of any prefix of length L
        # max_prefix[L] = the prefix string that achieves max_count[L]
        max_count = [0] * (max_len + 1)
        second_max_count = [0] * (max_len + 1)
        max_prefix = [""] * (max_len + 1)
        
        # Group prefixes by length
        prefixes_by_len = [[] for _ in range(max_len + 1)]
        for p, cnt in prefix_counts.items():
            l = len(p)
            prefixes_by_len[l].append((p, cnt))
        
        for l in range(1, max_len + 1):
            if not prefixes_by_len[l]:
                continue
            # Find top 2 counts
            counts = [cnt for _, cnt in prefixes_by_len[l]]
            counts.sort(reverse=True)
            max_count[l] = counts[0]
            second_max_count[l] = counts[1] if len(counts) > 1 else 0
            
            # Find the prefix that achieves max_count[l]
            # There might be multiple, pick any one
            for p, cnt in prefixes_by_len[l]:
                if cnt == max_count[l]:
                    max_prefix[l] = p
                    break
        
        # Step 3: For each index i, compute the answer
        result = [0] * n
        
        for i in range(n):
            word = words[i]
            # We need to find the max L such that there exists a prefix of length L
            # with adjusted count >= k.
            # The adjusted count for a prefix p is:
            #   prefix_counts[p] - 1 if p is a prefix of words[i]
            #   prefix_counts[p] otherwise
            
            # We iterate L from max possible down to 0
            # The maximum possible L is min(len(word), max_len) but actually 
            # the best prefix might not be a prefix of words[i]. 
            # However, if a prefix p of length L is not a prefix of words[i], 
            # its count is unchanged. So we can check lengths from max_len down to 0.
            
            found = False
            for l in range(max_len, 0, -1):
                # Check if there is any prefix of length l with adjusted count >= k
                # Case 1: The prefix that achieves max_count[l] is NOT a prefix of words[i]
                #         Then the adjusted max count is still max_count[l]
                # Case 2: The prefix that achieves max_count[l] IS a prefix of words[i]
                #         Then the adjusted count for that prefix is max_count[l] - 1
                #         And the new max for length l is max(max_count[l]-1, second_max_count[l])
                
                p_max = max_prefix[l]
                is_removed_prefix = (word.startswith(p_max))
                
                if not is_removed_prefix:
                    adj_max = max_count[l]
                else:
                    adj_max = max(max_count[l] - 1, second_max_count[l])
                
                if adj_max >= k:
                    result[i] = l
                    found = True
                    break
            
            # If no l found, result[i] remains 0
            # Note: l=0 always has count n-1 (or n) which is >= k if n-1 >= k, 
            # but we return 0 if not found, which is correct as per problem (empty prefix length 0)
            
        return result