from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Precompute factorials up to 100 for combination calculations
        max_n = 100
        fact = [1] * (max_n + 1)
        for i in range(1, max_n + 1):
            fact[i] = fact[i-1] * i
        
        def nCr(n: int, r: int) -> int:
            if r < 0 or r > n:
                return 0
            return fact[n] // (fact[r] * fact[n-r])
        
        def count_completions(e: int, o: int, required_parity: int, L: int) -> int:
            if L <= 0:
                return 1
            # Determine slot counts for the suffix of length L starting with required_parity
            if required_parity == 0:  # even
                even_slots = (L + 1) // 2
                odd_slots = L // 2
            else:  # odd
                odd_slots = (L + 1) // 2
                even_slots = L // 2
            if e < even_slots or o < odd_slots:
                return 0
            return nCr(e, even_slots) * nCr(o, odd_slots)
        
        # Total number of alternating permutations
        e_total = n // 2
        o_total = (n + 1) // 2
        total_even = count_completions(e_total, o_total, 0, n)
        total_odd = count_completions(e_total, o_total, 1, n)
        total = total_even + total_odd
        
        if k > total:
            return []
        
        # Determine starting parity
        if k <= total_odd:
            start_parity = 1  # odd
        else:
            k -= total_odd
            start_parity = 0  # even
        
        # Build the k-th permutation
        unused_evens = list(range(2, n+1, 2))
        unused_odds = list(range(1, n+1, 2))
        result = []
        current_parity = start_parity
        
        for pos in range(n):
            remaining_len = n - pos
            if current_parity == 0:  # need even
                candidates = unused_evens
            else:
                candidates = unused_odds
            
            found = False
            for idx, cand in enumerate(candidates):
                # Compute remaining counts after removing this candidate
                if current_parity == 0:
                    e_rem = len(unused_evens) - 1
                    o_rem = len(unused_odds)
                else:
                    e_rem = len(unused_evens)
                    o_rem = len(unused_odds) - 1
                next_parity = 1 - current_parity
                cnt = count_completions(e_rem, o_rem, next_parity, remaining_len - 1)
                if k > cnt:
                    k -= cnt
                else:
                    result.append(cand)
                    if current_parity == 0:
                        unused_evens.pop(idx)
                    else:
                        unused_odds.pop(idx)
                    current_parity = next_parity
                    found = True
                    break
            if not found:
                return []
        return result

# ---------- Testing ----------
def brute_force_alternating(n, k):
    from itertools import permutations
    valid = []
    for p in permutations(range(1, n+1)):
        ok = True
        for i in range(n-1):
            if (p[i] % 2) == (p[i+1] % 2):
                ok = False
                break
        if ok:
            valid.append(list(p))
    valid.sort()
    if k <= len(valid):
        return valid[k-1]
    else:
        return []

def test():
    sol = Solution()
    # Provided examples
    assert sol.permute(4, 6) == [3, 4, 1, 2], f"n=4,k=6 got {sol.permute(4,6)}"
    assert sol.permute(3, 2) == [3, 2, 1], f"n=3,k=2 got {sol.permute(3,2)}"
    assert sol.permute(2, 3) == [], f"n=2,k=3 got {sol.permute(2,3)}"
    
    # Edge case n=1
    assert sol.permute(1, 1) == [1], f"n=1,k=1 got {sol.permute(1,1)}"
    assert sol.permute(1, 2) == [], f"n=1,k=2 got {sol.permute(1,2)}"
    
    # k = 1 (first lexicographic) for several n
    for n_val in range(1, 11):
        expected = brute_force_alternating(n_val, 1)
        got = sol.permute(n_val, 1)
        assert got == expected, f"n={n_val},k=1 expected {expected} got {got}"
    
    # k = total (last lexicographic) for several n
    for n_val in range(1, 11):
        all_valid = brute_force_alternating(n_val, 10**9)  # get all
        total = len(all_valid)
        if total > 0:
            expected = all_valid[-1]
            got = sol.permute(n_val, total)
            assert got == expected, f"n={n_val},k=total expected {expected} got {got}"
    
    # Test all k for small n against brute force
    for n_val in range(1, 9):
        all_valid = brute_force_alternating(n_val, 10**9)
        total = len(all_valid)
        for k_val in range(1, total+1):
            expected = all_valid[k_val-1]
            got = sol.permute(n_val, k_val)
            if got != expected:
                print(f"Mismatch n={n_val}, k={k_val}: expected {expected}, got {got}")
                return False
        # Test k out of range
        assert sol.permute(n_val, total+1) == [], f"n={n_val}, k=total+1 should be []"
    
    # Test large n and k=1
    n_val = 100
    got = sol.permute(n_val, 1)
    expected = brute_force_alternating(n_val, 1)
    assert got == expected, f"n=100,k=1 expected {expected} got {got}"
    
    # Test large n with k=2 (second permutation)
    got = sol.permute(n_val, 2)
    expected = brute_force_alternating(n_val, 2)
    assert got == expected, f"n=100,k=2 expected {expected} got {got}"
    
    # Test k much larger than total
    got = sol.permute(10, 10**15)
    assert got == [], f"k out of range should return []"
    
    print("All tests passed!")

if __name__ == "__main__":
    test()