from collections import Counter
import heapq
from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        # Count frequency of each unique string
        freq = Counter(words)
        
        # valid_counts[L] stores how many unique strings of length L have frequency >= k
        valid_counts = {}
        
        # Max-heap to store lengths of valid strings. We use negative values for min-heap simulation.
        # We use lazy deletion: if a length's valid count drops to 0, we don't remove it immediately.
        # When querying, we pop invalid lengths from the top.
        heap = []
        
        # Initialize valid_counts and heap
        for s, count in freq.items():
            if count >= k:
                length = len(s)
                valid_counts[length] = valid_counts.get(length, 0) + 1
                heapq.heappush(heap, -length)
        
        n = len(words)
        answer = []
        
        for i in range(n):
            s = words[i]
            current_len = len(s)
            current_freq = freq[s]
            
            # Determine the state BEFORE removal
            is_valid_before = (current_freq >= k)
            
            # Simulate removal
            freq[s] -= 1
            new_freq = freq[s]
            
            # Update valid_counts based on the change
            # Since we are removing an element, frequency only decreases.
            # We only care if a string transitions from valid (>= k) to invalid (< k).
            if is_valid_before and new_freq < k:
                valid_counts[current_len] -= 1
                # If count drops to 0, this length is no longer valid, but we leave it in heap
                # for lazy deletion during the query step.
            
            # Clean the heap to find the current max valid length
            # Remove elements from the top that have valid_counts == 0
            while heap and valid_counts.get(-heap[0], 0) == 0:
                heapq.heappop(heap)
            
            # If heap is empty, it means no string has freq >= k in the remaining set
            if heap:
                answer.append(-heap[0])
            else:
                answer.append(0)
            
            # Revert the change for the next iteration
            freq[s] = current_freq
            
        return answer