class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Count odds and evens in 1..n
        total_odds = (n + 1) // 2
        total_evens = n // 2
        
        # Memoization for count function
        # count(rem_odd, rem_even, last_parity)
        # last_parity: -1 for start, 0 for even, 1 for odd
        from functools import lru_cache
        
        @lru_cache(maxsize=None)
        def count(rem_odd, rem_even, last_parity):
            if rem_odd == 0 and rem_even == 0:
                return 1
            if last_parity == -1:
                # First element: can choose odd or even
                res = 0
                if rem_odd > 0:
                    res += rem_odd * count(rem_odd - 1, rem_even, 1)
                if rem_even > 0:
                    res += rem_even * count(rem_odd, rem_even - 1, 0)
                return res
            elif last_parity == 0:
                # Last was even, need odd
                if rem_odd == 0:
                    return 0
                return rem_odd * count(rem_odd - 1, rem_even, 1)
            else:  # last_parity == 1
                # Last was odd, need even
                if rem_even == 0:
                    return 0
                return rem_even * count(rem_odd, rem_even - 1, 0)
        
        total = count(total_odds, total_evens, -1)
        if k > total:
            return []
        
        result = []
        rem_odd = total_odds
        rem_even = total_evens
        last_parity = -1  # -1 means no previous element
        
        # Available numbers: we need to track which specific numbers are available
        # But since we only care about parity for counting, and we iterate in order,
        # we can just iterate through 1..n and skip used numbers.
        used = [False] * (n + 1)
        
        for i in range(n):
            # Determine what parity we need at position i
            if last_parity == -1:
                # First position: try all available numbers in order
                for num in range(1, n + 1):
                    if used[num]:
                        continue
                    if num % 2 == 1:  # odd
                        # Number of completions if we pick this odd number
                        completions = count(rem_odd - 1, rem_even, 1)
                    else:  # even
                        completions = count(rem_odd, rem_even - 1, 0)
                    
                    if k <= completions:
                        # Choose this number
                        result.append(num)
                        used[num] = True
                        if num % 2 == 1:
                            rem_odd -= 1
                            last_parity = 1
                        else:
                            rem_even -= 1
                            last_parity = 0
                        break
                    else:
                        k -= completions
            else:
                # Not first position: need opposite parity of last_parity
                needed_parity = 1 - last_parity  # 0 for even, 1 for odd
                for num in range(1, n + 1):
                    if used[num]:
                        continue
                    if num % 2 == needed_parity:
                        # This is the only choice that satisfies the parity constraint
                        # But we still need to check if k is within the count
                        # Actually, since all numbers with the correct parity are equivalent
                        # in terms of future counts (only the count matters, not which specific one),
                        # we just pick the smallest available with the correct parity.
                        # The number of completions is determined by the remaining counts.
                        if needed_parity == 1:  # odd
                            completions = count(rem_odd - 1, rem_even, 0)
                        else:  # even
                            completions = count(rem_odd, rem_even - 1, 1)
                        
                        # Since we're iterating in order, the first available with correct parity
                        # is the lexicographically smallest. And k should be 1 at this point
                        # because all previous branches with smaller numbers were skipped.
                        # But to be safe, we check:
                        if k <= completions:
                            result.append(num)
                            used[num] = True
                            if needed_parity == 1:
                                rem_odd -= 1
                            else:
                                rem_even -= 1
                            last_parity = needed_parity
                            break
                        else:
                            # This shouldn't happen if our counting is correct
                            k -= completions
        
        return result