from typing import List
from collections import defaultdict

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n == 0 or k > n:
            return [0] * n
        
        # Step 1: Compute frequency of every prefix
        # Total number of prefixes is bounded by sum of lengths <= 10^5
        prefix_counts = defaultdict(int)
        for word in words:
            for i in range(len(word)):
                prefix = word[:i+1]
                prefix_counts[prefix] += 1
        
        # Step 2: Categorize prefixes by length
        # safe_lengths[L] is True if there exists a prefix of length L with count > k
        # critical_prefixes[L] is a list of prefixes of length L with count == k
        safe_lengths = defaultdict(bool)
        critical_prefixes = defaultdict(list)
        
        for p, count in prefix_counts.items():
            l = len(p)
            if count > k:
                safe_lengths[l] = True
            elif count == k:
                critical_prefixes[l].append(p)
        
        # Determine the maximum length we need to consider
        max_len = 0
        for l in safe_lengths:
            if l > max_len: max_len = l
        for l in critical_prefixes:
            if l > max_len: max_len = l
            
        # If no prefix has count >= k, all answers are 0
        if max_len == 0:
            return [0] * n
            
        ans = [0] * n
        
        # Helper to check if length L is valid for removal of words[i]
        def is_valid(L, idx):
            # If there is a safe prefix of length L, it remains valid after removing any single word
            if safe_lengths[L]:
                return True
            
            # Check critical prefixes of length L
            crit_list = critical_prefixes[L]
            if not crit_list:
                return False
            
            # If there are multiple critical prefixes, removing one word (which has only one prefix of length L)
            # cannot remove all of them. So at least one remains with count >= k.
            if len(crit_list) > 1:
                return True
            
            # If there is exactly one critical prefix, we must check if it is the prefix of words[idx]
            # If words[idx] has this prefix, its count drops to k-1, making it invalid.
            # If words[idx] does not have this prefix, the count remains k, so it is valid.
            word_i = words[idx]
            if len(word_i) < L:
                return False # words[idx] is too short to have a prefix of length L
            
            # Check if the single critical prefix matches the prefix of words[idx]
            # Since crit_list has only one element here
            p = crit_list[0]
            if p == word_i[:L]:
                return False # This is the one being removed
            return True

        for i in range(n):
            # Binary search for the largest valid length in [0, max_len]
            low, high = 0, max_len
            res = 0
            while low <= high:
                mid = (low + high) // 2
                if is_valid(mid, i):
                    res = mid
                    low = mid + 1
                else:
                    high = mid - 1
            ans[i] = res
            
        return ans