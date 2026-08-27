class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        MOD = 10**15 + 7
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = min(fact[i-1] * i, MOD)
        
        odds = (n + 1) // 2
        evens = n // 2
        
        if n % 2 == 0:
            total = fact[n//2] * fact[n//2] * 2
        else:
            total = fact[(n+1)//2] * fact[n//2]
        
        if k > total:
            return []
        
        used = [False] * (n + 1)
        result = []
        rem_o = odds
        rem_e = evens
        
        for pos in range(n):
            if pos == 0:
                for num in range(1, n + 1):
                    if used[num]:
                        continue
                    if num % 2 == 1:  # odd
                        rem_odd_pos = (n - 1) // 2
                        rem_even_pos = (n - 1 + 1) // 2
                        r_o = rem_o - 1
                        r_e = rem_e
                    else:  # even
                        rem_odd_pos = (n - 1 + 1) // 2
                        rem_even_pos = (n - 1) // 2
                        r_o = rem_o
                        r_e = rem_e - 1
                    
                    if r_o == rem_odd_pos and r_e == rem_even_pos:
                        count = fact[r_o] * fact[r_e]
                    else:
                        count = 0
                    
                    if k <= count:
                        result.append(num)
                        used[num] = True
                        if num % 2 == 1:
                            rem_o -= 1
                        else:
                            rem_e -= 1
                        first_parity = num % 2
                        break
                    else:
                        k -= count
            else:
                required_parity = (first_parity + pos) % 2
                remaining = n - 1 - pos
                if remaining == 0:
                    rem_odd_pos = 0
                    rem_even_pos = 0
                else:
                    first_rem_parity = (first_parity + pos + 1) % 2
                    if first_rem_parity == 1:
                        rem_odd_pos = (remaining + 1) // 2
                        rem_even_pos = remaining // 2
                    else:
                        rem_odd_pos = remaining // 2
                        rem_even_pos = (remaining + 1) // 2
                
                for num in range(1, n + 1):
                    if used[num]:
                        continue
                    if num % 2 == required_parity:
                        r_o = rem_o - (1 if num % 2 == 1 else 0)
                        r_e = rem_e - (1 if num % 2 == 0 else 0)
                        
                        if r_o == rem_odd_pos and r_e == rem_even_pos:
                            count = fact[r_o] * fact[r_e]
                        else:
                            count = 0
                        
                        if k <= count:
                            result.append(num)
                            used[num] = True
                            if num % 2 == 1:
                                rem_o -= 1
                            else:
                                rem_e -= 1
                            break
                        else:
                            k -= count
        
        return result