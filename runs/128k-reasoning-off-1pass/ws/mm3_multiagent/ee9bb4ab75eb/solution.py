from typing import List
from collections import Counter
from sortedcontainers import SortedList

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # If after any removal the remaining array has fewer than k strings, answer is 0.
        if k > n - 1:
            return [0] * n

        # Count occurrences of each distinct word in the original array.
        cnt = Counter(words)

        # Maximum possible word length (bounds the bucket array).
        max_len = max(len(w) for w in words) if words else 0

        # good[l] = number of distinct words with length l whose current count >= k.
        good = [0] * (max_len + 1)
        for w, c in cnt.items():
            if c >= k:
                good[len(w)] += 1

        # Keep a sorted container of all lengths that currently have at least one "good" word.
        good_lengths = SortedList()
        for l in range(max_len + 1):
            if good[l] > 0:
                good_lengths.add(l)

        ans = [0] * n

        # Helper to update structures after removing one occurrence of `word`.
        def process_removal(word: str):
            l = len(word)
            cur = cnt[word]  # count before this removal
            if cur >= k:
                # This word was contributing to good[l]; remove it.
                good[l] -= 1
                if good[l] == 0:
                    good_lengths.remove(l)
            # Decrement the word's count.
            cnt[word] = cur - 1
            # If the new count is still >= k, the word remains good (no change needed).
            # If the old count was < k, the new count is even smaller, still not good.

        # Iterate over each index i, answer for removal i, then remove words[i] for subsequent steps.
        for i, w in enumerate(words):
            ans[i] = good_lengths[-1] if good_lengths else 0
            if i < n - 1:
                process_removal(w)

        return ans