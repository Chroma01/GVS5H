import heapq

class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        # Step 1: Parse the string into run lengths
        if not s:
            return 0
        
        runs = []
        current_char = s[0]
        count = 1
        
        for char in s[1:]:
            if char == current_char:
                count += 1
            else:
                runs.append(count)
                current_char = char
                count = 1
        runs.append(count)
        
        # Step 2: Use a max-heap (simulated with negative values)
        # We store negative lengths because Python's heapq is a min-heap
        heap = [-length for length in runs]
        heapq.heapify(heap)
        
        # Step 3: Greedily reduce the largest run using numOps
        while numOps > 0 and heap:
            # Get the largest run (as a positive number)
            largest_neg = heapq.heappop(heap)
            largest = -largest_neg
            
            # If the largest run is 1, we can't reduce it further without potentially
            # merging it with neighbors (which would increase length), so we stop.
            if largest == 1:
                break
            
            # Apply operation: split the run of length L into floor(L/2) and ceil(L/2).
            # The new maximum length for this segment becomes ceil(L/2).
            # ceil(L/2) is equivalent to (L + 1) // 2 using integer division.
            new_len = (largest + 1) // 2
            
            # Push the new length back into the heap
            heapq.heappush(heap, -new_len)
            
            numOps -= 1
        
        # Step 4: The answer is the maximum remaining run length
        if not heap:
            return 0
        
        return -heap[0]