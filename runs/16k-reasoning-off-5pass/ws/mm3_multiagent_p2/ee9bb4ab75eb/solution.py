from typing import List
from collections import defaultdict

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n == 0:
            return []
        
        # Build prefix counts over the whole array
        prefix_counts = defaultdict(int)
        for word in words:
            for i in range(1, len(word) + 1):
                prefix_counts[word[:i]] += 1
        
        # L_global: longest prefix with count >= k+1 (always valid after removal)
        L_global = 0
        for p, cnt in prefix_counts.items():
            if cnt >= k + 1 and len(p) > L_global:
                L_global = len(p)
        
        # Set of prefixes that appear exactly k times
        count_k_prefixes = {p for p, cnt in prefix_counts.items() if cnt == k}
        
        # For each word, store the set of count==k prefixes it contains
        # (only these matter for blocking L_alt)
        word_k_prefixes = []
        for word in words:
            s = set()
            for i in range(1, len(word) + 1):
                p = word[:i]
                if p in count_k_prefixes:
                    s.add(p)
            word_k_prefixes.append(s)
        
        # max word length
        max_len = max((len(w) for w in words), default=0)
        
        # total_count_k_len[L] = number of distinct count==k prefixes of length L
        # unique_prefix_for_len[L] = the only such prefix if total_count_k_len[L] == 1
        total_count_k_len = [0] * (max_len + 1)
        unique_prefix_for_len = [None] * (max_len + 1)
        
        for p in count_k_prefixes:
            L = len(p)
            total_count_k_len[L] += 1
            if total_count_k_len[L] == 1:
                unique_prefix_for_len[L] = p
            # if >1 we don't need the unique prefix
        
        # next_available[L] = largest L' <= L with total_count_k_len[L'] > 0
        next_available = [0] * (max_len + 2)  # extra cell for L+1
        for L in range(max_len, 0, -1):
            if total_count_k_len[L] > 0:
                next_available[L] = L
            else:
                next_available[L] = next_available[L + 1]
        
        global_max_k = next_available[max_len]  # largest L with any count==k prefix
        
        # Compute L_alt[i] for each i
        L_alt = [0] * n
        for i in range(n):
            if global_max_k == 0:
                continue
            word_len = len(words[i])
            L = global_max_k
            # If the longest count==k prefix is longer than this word,
            # the word cannot have it, so it is automatically not blocked.
            if L > word_len:
                L_alt[i] = L
                continue
            # Walk downward through lengths that actually have count==k prefixes
            while L > 0:
                if total_count_k_len[L] > 1:
                    L_alt[i] = L
                    break
                # total_count_k_len[L] == 1
                unique = unique_prefix_for_len[L]
                if unique not in word_k_prefixes[i]:
                    L_alt[i] = L
                    break
                # blocked, jump to next smaller length with a count==k prefix
                L = next_available[L - 1]
        
        # Final answer
        answer = [0] * n
        for i in range(n):
            answer[i] = max(L_global, L_alt[i])
        return answer