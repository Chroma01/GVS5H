import sys
import random
from itertools import product

class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        
        INF = 10**9
        codes = [ord(c) - ord('a') for c in caption]
        
        # State: ch in 0..25, s in 0..2 (run length 1, 2, >=3)
        STRIDE = 26 * 3  # 78
        
        # Flat list for dp: dp[i * STRIDE + ch * 3 + s]
        dp = [INF] * (n * STRIDE)
        
        # i = 0: each ch can start a run of length 1
        for ch in range(26):
            cost_inc = abs(codes[0] - ch)
            dp[ch * 3 + 0] = cost_inc
        
        # Fill DP for i = 1..n-1
        for i in range(1, n):
            ci = codes[i]
            prev_base = (i - 1) * STRIDE
            curr_base = i * STRIDE
            
            # Find two smallest values among prev[c*3+2] for c in 0..25
            best1_val = INF
            best1_ch = -1
            best2_val = INF
            for c in range(26):
                v = dp[prev_base + c * 3 + 2]
                if v < best1_val:
                    best2_val = best1_val
                    best1_val = v
                    best1_ch = c
                elif v < best2_val:
                    best2_val = v
            
            for ch in range(26):
                cost_inc = abs(ci - ch)
                
                # Continue: s=0 -> s=1
                v = dp[prev_base + ch * 3 + 0]
                nv = v + cost_inc
                idx = curr_base + ch * 3 + 1
                if nv < dp[idx]:
                    dp[idx] = nv
                
                # Continue: s=1 -> s=2
                v = dp[prev_base + ch * 3 + 1]
                nv = v + cost_inc
                idx = curr_base + ch * 3 + 2
                if nv < dp[idx]:
                    dp[idx] = nv
                
                # Continue: s=2 -> s=2
                v = dp[prev_base + ch * 3 + 2]
                nv = v + cost_inc
                idx = curr_base + ch * 3 + 2
                if nv < dp[idx]:
                    dp[idx] = nv
                
                # Start new: from any ch2 != ch with prev state s=2
                if best1_ch != ch:
                    min_excl = best1_val
                else:
                    min_excl = best2_val
                
                nv = min_excl + cost_inc
                idx = curr_base + ch * 3 + 0
                if nv < dp[idx]:
                    dp[idx] = nv
        
        # Find optimal cost at the end (must end with run length >=3, i.e., s=2)
        OPT = INF
        last_base = (n - 1) * STRIDE
        for ch in range(26):
            if dp[last_base + ch * 3 + 2] < OPT:
                OPT = dp[last_base + ch * 3 + 2]
        
        if OPT >= INF:
            return ""
        
        # Reconstruct the lexicographically smallest string
        result = []
        cost_so_far = 0
        current_ch = -1
        current_s = -1
        
        for i in range(n):
            ci = codes[i]
            found = False
            curr_base = i * STRIDE
            for ch in range(26):
                cost_inc = abs(ci - ch)
                target_cost = cost_so_far + cost_inc
                
                if i == 0:
                    if dp[curr_base + ch * 3 + 0] == target_cost:
                        result.append(chr(ord('a') + ch))
                        cost_so_far = target_cost
                        current_ch = ch
                        current_s = 0
                        found = True
                        break
                else:
                    if ch == current_ch:
                        if current_s == 0:
                            new_s = 1
                        elif current_s == 1:
                            new_s = 2
                        else:
                            new_s = 2
                        if dp[curr_base + ch * 3 + new_s] == target_cost:
                            result.append(chr(ord('a') + ch))
                            cost_so_far = target_cost
                            current_s = new_s
                            found = True
                            break
                    if not found and ch != current_ch and current_s == 2:
                        if dp[curr_base + ch * 3 + 0] == target_cost:
                            result.append(chr(ord('a') + ch))
                            cost_so_far = target_cost
                            current_ch = ch
                            current_s = 0
                            found = True
                            break
            
            if not found:
                return ""
        
        return "".join(result)


def is_good(s):
    """Check if string s is a good caption (all runs length >= 3)."""
    if not s:
        return False
    i = 0
    n = len(s)
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        if j - i < 3:
            return False
        i = j
    return True


def compute_cost(orig, target):
    """Compute number of operations: each char changed by +/-1 per unit."""
    return sum(abs(ord(a) - ord(b)) for a, b in zip(orig, target))


def brute_force(caption):
    """Brute force: find min cost good caption, return lex smallest, or ""."""
    n = len(caption)
    if n < 3:
        return ""
    
    best_cost = None
    best_str = None
    
    # For small n, iterate over all possible target strings of length n over 'a'-'z'
    for chars in product(range(26), repeat=n):
        s = ''.join(chr(ord('a') + c) for c in chars)
        if is_good(s):
            cost = compute_cost(caption, s)
            if best_cost is None or cost < best_cost or (cost == best_cost and s < best_str):
                best_cost = cost
                best_str = s
    
    return best_str if best_str is not None else ""


def run_tests():
    sol = Solution()
    
    # Specific test cases from problem
    specific = [
        ("cdcd", "cccc"),
        ("aca", "aaa"),
        ("bc", ""),
        ("aaa", "aaa"),
        ("aaabbb", "aaabbb"),
        ("aabbb", "aaabbb"),
    ]
    
    print("=== Specific test cases ===")
    for caption, expected in specific:
        result = sol.minCostGoodCaption(caption)
        status = "OK" if result == expected else "FAIL"
        print(f"{status}: {caption!r} -> {result!r} (expected {expected!r})")
    
    # Brute force verification for all strings of length 1..6 over small alphabet
    print("\n=== Brute force verification (length 1..6, alphabet 'abc') ===")
    alphabet = 'abc'
    total = 0
    passed = 0
    failed = 0
    
    for n in range(1, 7):
        for chars in product(alphabet, repeat=n):
            caption = ''.join(chars)
            dp_result = sol.minCostGoodCaption(caption)
            bf_result = brute_force(caption)
            total += 1
            if dp_result == bf_result:
                passed += 1
            else:
                failed += 1
                if failed <= 20:
                    print(f"FAIL: {caption!r} -> DP={dp_result!r}, BF={bf_result!r}")
    
    print(f"Total: {total}, Passed: {passed}, Failed: {failed}")
    
    # Random tests with larger alphabet
    print("\n=== Random tests (length 2..7, full alphabet) ===")
    random.seed(42)
    total = 0
    passed = 0
    failed = 0
    
    for _ in range(200):
        n = random.randint(2, 7)
        caption = ''.join(chr(ord('a') + random.randint(0, 25)) for _ in range(n))
        dp_result = sol.minCostGoodCaption(caption)
        bf_result = brute_force(caption)
        total += 1
        if dp_result == bf_result:
            passed += 1
        else:
            failed += 1
            if failed <= 20:
                print(f"FAIL: {caption!r} -> DP={dp_result!r}, BF={bf_result!r}")
    
    print(f"Total: {total}, Passed: {passed}, Failed: {failed}")
    
    if failed == 0:
        print("\n*** ALL TESTS PASSED ***")
    else:
        print(f"\n*** {failed} TESTS FAILED ***")


if __name__ == "__main__":
    run_tests()