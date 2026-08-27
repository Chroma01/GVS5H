from math import factorial
from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Precompute factorials up to n, but cap to avoid huge numbers since k <= 1e15
        # We only need to compare with k, so capping at 1e16 is safe.
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            if fact[i-1] > 10**16:
                fact[i] = fact[i-1]
            else:
                fact[i] = fact[i-1] * i
                if fact[i] > 10**16:
                    fact[i] = 10**16
        
        total_odd = (n + 1) // 2
        total_even = n // 2
        
        # Total alternating permutations
        total = fact[total_odd] * fact[total_even]
        if total_odd > 0 and total_even > 0:
            total *= 2
        
        if k > total:
            return []
        
        used = [False] * (n + 1)
        result = []
        
        def count_rest(odd_left, even_left, need_parity):
            L = odd_left + even_left
            if L == 0:
                return 1
            if need_parity == 1:
                req_odd = (L + 1) // 2
                req_even = L // 2
            else:
                req_odd = L // 2
                req_even = (L + 1) // 2
            if odd_left != req_odd or even_left != req_even:
                return 0
            count = fact[odd_left] * fact[even_left]
            if count > 10**16:
                count = 10**16
            return count
        
        odd_left = total_odd
        even_left = total_even
        need_parity = None
        
        while len(result) < n:
            found = False
            for x in range(1, n + 1):
                if used[x]:
                    continue
                is_odd = (x % 2 == 1)
                if need_parity is not None:
                    if is_odd and need_parity != 1:
                        continue
                    if not is_odd and need_parity != 0:
                        continue
                
                new_odd_left = odd_left - (1 if is_odd else 0)
                new_even_left = even_left - (1 if is_odd else 0)
                
                next_need = 0 if is_odd else 1
                
                completions = count_rest(new_odd_left, new_even_left, next_need)
                
                if completions >= k:
                    result.append(x)
                    used[x] = True
                    odd_left = new_odd_left
                    even_left = new_even_left
                    need_parity = next_need
                    found = True
                    break
                else:
                    k -= completions
            if not found:
                return []
        
        return result