from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        total_odds = (n + 1) // 2
        total_evens = n // 2

        # dp[a][b][p]: number of ways to complete a sequence with
        # a unused odd numbers, b unused even numbers, and the last placed number
        # has parity p (0=odd, 1=even).
        max_a = total_odds
        max_b = total_evens
        dp = [[[0] * 2 for _ in range(max_b + 1)] for _ in range(max_a + 1)]

        # Base case: empty remaining sequence
        dp[0][0][0] = 1
        dp[0][0][1] = 1

        for a in range(max_a + 1):
            for b in range(max_b + 1):
                if a == 0 and b == 0:
                    continue
                # If last is odd, next must be even
                if b > 0:
                    dp[a][b][0] = dp[a][b - 1][1]
                else:
                    dp[a][b][0] = 0
                # If last is even, next must be odd
                if a > 0:
                    dp[a][b][1] = dp[a - 1][b][0]
                else:
                    dp[a][b][1] = 0

        # Compute total number of alternating permutations
        total_count = 0
        for x in range(1, n + 1):
            is_odd = (x % 2 == 1)
            a_rem = total_odds - (1 if is_odd else 0)
            b_rem = total_evens - (1 if not is_odd else 0)
            p = 0 if is_odd else 1
            total_count += dp[a_rem][b_rem][p]

        if k > total_count:
            return []

        # Construct k-th permutation lexicographically
        used = [False] * (n + 1)
        result = []
        rem_odds = total_odds
        rem_evens = total_evens
        last_parity = -1  # -1 means no restriction

        for pos in range(n):
            chosen = -1
            for x in range(1, n + 1):
                if used[x]:
                    continue
                is_odd = (x % 2 == 1)
                p = 0 if is_odd else 1
                if last_parity != -1 and p == last_parity:
                    continue
                a_rem = rem_odds - (1 if is_odd else 0)
                b_rem = rem_evens - (1 if not is_odd else 0)
                cnt = dp[a_rem][b_rem][p]
                if k > cnt:
                    k -= cnt
                else:
                    chosen = x
                    break
            if chosen == -1:
                return []
            result.append(chosen)
            used[chosen] = True
            if chosen % 2 == 1:
                rem_odds -= 1
            else:
                rem_evens -= 1
            last_parity = 0 if (chosen % 2 == 1) else 1

        return result


def run_tests():
    sol = Solution()
    test_cases = [
        # (n, k, expected, description)
        (4, 6, [3, 4, 1, 2], "Example 1"),
        (3, 2, [3, 2, 1], "Example 2"),
        (2, 3, [], "Example 3 - k out of range"),
        (1, 1, [1], "n=1, k=1"),
        (1, 2, [], "n=1, k=2 - out of range"),
        (2, 1, [1, 2], "n=2, k=1"),
        (2, 2, [2, 1], "n=2, k=2"),
        (3, 1, [1, 2, 3], "n=3, k=1"),
        (3, 3, [], "n=3, k=3 - out of range"),
        (5, 1, [1, 2, 3, 4, 5], "n=5, k=1"),
        (4, 8, [4, 3, 2, 1], "n=4, k=8 (last)"),
        (4, 9, [], "n=4, k=9 - out of range"),
    ]

    def is_alternating(perm):
        for i in range(len(perm) - 1):
            if (perm[i] % 2) == (perm[i + 1] % 2):
                return False
        return True

    def generate_all_alt_perms(n):
        """Generate all alternating permutations of [1..n] lexicographically."""
        from itertools import permutations
        result = []
        for p in permutations(range(1, n + 1)):
            if is_alternating(p):
                result.append(list(p))
        return result

    all_passed = True
    for n, k, expected, desc in test_cases:
        result = sol.permute(n, k)
        status = "PASS" if result == expected else "FAIL"
        if result != expected:
            all_passed = False
        print(f"[{status}] {desc}: n={n}, k={k}, expected={expected}, got={result}")

    # Additional verification: compare with brute force for small n
    print("\n--- Brute force verification for small n ---")
    for n in range(1, 8):
        all_perms = generate_all_alt_perms(n)
        total = len(all_perms)
        for k in range(1, total + 1):
            sol_result = sol.permute(n, k)
            expected = all_perms[k - 1]
            if sol_result != expected:
                all_passed = False
                print(f"FAIL: n={n}, k={k}, expected={expected}, got={sol_result}")
        # Test k = total + 1 (should return [])
        if total < 1000:
            out_of_range = sol.permute(n, total + 1)
            if out_of_range != []:
                all_passed = False
                print(f"FAIL: n={n}, k={total+1}, expected=[], got={out_of_range}")
        print(f"n={n}: {total} alternating permutations verified.")

    # Test n=100 with k=1 and k=large
    print("\n--- Large n tests ---")
    # n=100, k=1
    res = sol.permute(100, 1)
    print(f"n=100, k=1: valid alternating = {is_alternating(res)}, len={len(res)}, sorted={sorted(res)==list(range(1,101))}")
    if not is_alternating(res) or sorted(res) != list(range(1, 101)):
        all_passed = False
        print("FAIL: n=100, k=1")

    # n=100, k=2
    res = sol.permute(100, 2)
    print(f"n=100, k=2: valid alternating = {is_alternating(res)}")
    if not is_alternating(res) or sorted(res) != list(range(1, 101)):
        all_passed = False
        print("FAIL: n=100, k=2")

    # n=100, very large k (should be out of range or last)
    res_large = sol.permute(100, 10**15)
    print(f"n=100, k=10^15: result is {'empty (k too large)' if res_large == [] else f'has {len(res_large)} elements'}")

    # n=5 brute force check
    print("\n--- n=5 detailed check ---")
    all_perms_5 = generate_all_alt_perms(5)
    print(f"Total alternating permutations for n=5: {len(all_perms_5)}")
    for idx, p in enumerate(all_perms_5, 1):
        sol_p = sol.permute(5, idx)
        match = sol_p == p
        if not match:
            all_passed = False
            print(f"FAIL: n=5, k={idx}, expected={p}, got={sol_p}")
        else:
            print(f"  k={idx}: {sol_p} OK")

    if all_passed:
        print("\n*** ALL TESTS PASSED ***")
    else:
        print("\n*** SOME TESTS FAILED ***")
    return all_passed


if __name__ == "__main__":
    run_tests()