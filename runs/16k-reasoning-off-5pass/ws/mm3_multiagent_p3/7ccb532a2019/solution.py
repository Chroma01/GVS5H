class Solution:
    def makeStringGood(self, s: str) -> int:
        # Count frequency of each character
        freq = [0] * 26
        for ch in s:
            freq[ord(ch) - ord('a')] += 1
        
        max_freq = max(freq)
        answer = float('inf')
        
        # Try each possible target count k (0 up to max frequency)
        for k in range(0, max_freq + 1):
            surplus = 0   # total extra characters to delete or change
            deficit = 0   # total missing characters to fill
            
            for cnt in freq:
                if cnt > k:
                    surplus += cnt - k
                elif cnt < k:
                    deficit += k - cnt
                # if cnt == k, no action needed
            
            # Each change operation fixes one surplus and one deficit at cost 1.
            # Remaining surplus -> deletes, remaining deficit -> inserts.
            # Total cost = max(surplus, deficit)
            cost = max(surplus, deficit)
            answer = min(answer, cost)
        
        return answer