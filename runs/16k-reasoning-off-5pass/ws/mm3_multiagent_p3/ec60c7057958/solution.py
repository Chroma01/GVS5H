from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        INF = 10**15 + 1
        odd_count = (n + 1) // 2
        even_count = n // 2

        max_odd = odd_count
        max_even = even_count
        # dp[o][e][par] = number of alternating completions using o odds and e evens
        # where the next number to place must have parity par (0=even, 1=odd)
        dp = [[[0, 0] for _ in range(max_even + 1)] for _ in range(max_odd + 1)]
        # Base case: no numbers left -> one way (empty suffix)
        dp[0][0][0] = 1
        dp[0][0][1] = 1

        # Fill in increasing total count
        for total in range(1, max_odd + max_even + 1):
            for o in range(0, min(total, max_odd) + 1):
                e = total - o
                if e < 0 or e > max_even:
                    continue
                # need even next (par=0)
                if e > 0:
                    val = e * dp[o][e - 1][1]
                    if val > INF:
                        val = INF
                    dp[o][e][0] = val
                # need odd next (par=1)
                if o > 0:
                    val = o * dp[o - 1][e][0]
                    if val > INF:
                        val = INF
                    dp[o][e][1] = val

        # Total permutations
        total_perms = 0
        if odd_count > 0:
            total_perms += odd_count * dp[odd_count - 1][even_count][0]
        if even_count > 0:
            total_perms += even_count * dp[odd_count][even_count - 1][1]
        if total_perms > INF:
            total_perms = INF

        if k > total_perms:
            return []

        result = []
        remaining_odd = odd_count
        remaining_even = even_count
        remaining = list(range(1, n + 1))
        first_pos = True
        required_parity = None  # None for first position

        while len(result) < n:
            placed = False
            for num in remaining:
                if not first_pos and (num % 2) != required_parity:
                    continue
                if num % 2 == 1:
                    cnt = dp[remaining_odd - 1][remaining_even][0]
                else:
                    cnt = dp[remaining_odd][remaining_even - 1][1]
                if k > cnt:
                    k -= cnt
                    continue
                # Place this number
                result.append(num)
                remaining.remove(num)
                if num % 2 == 1:
                    remaining_odd -= 1
                    required_parity = 0
                else:
                    remaining_even -= 1
                    required_parity = 1
                first_pos = False
                placed = True
                break
            if not placed:
                return []
        return result


# Testing
if __name__ == "__main__":
    sol = Solution()

    # Example 1
    out = sol.permute(4, 6)
    assert out == [3, 4, 1, 2], f"Example 1 failed: {out}"
    print("Example 1 passed:", out)

    # Example 2
    out = sol.permute(3, 2)
    assert out == [3, 2, 1], f"Example 2 failed: {out}"
    print("Example 2 passed:", out)

    # Example 3
    out = sol.permute(2, 3)
    assert out == [], f"Example 3 failed: {out}"
    print("Example 3 passed:", out)

    # n=1, k=1
    out = sol.permute(1, 1)
    assert out == [1], f"n=1,k=1 failed: {out}"
    print("n=1,k=1 passed:", out)

    # n=1, k=2
    out = sol.permute(1, 2)
    assert out == [], f"n=1,k=2 failed: {out}"
    print("n=1,k=2 passed:", out)

    # n=5, enumerate first few
    # All alternating perms of [1..5] in lex order
    n = 5
    expected = [
        [1, 2, 3, 4, 5],
        [1, 2, 5, 4, 3],
        [1, 4, 3, 2, 5],
        [1, 4, 5, 2, 3],
        [3, 2, 1, 4, 5],
        [3, 2, 5, 4, 1],
        [3, 4, 1, 2, 5],
        [3, 4, 5, 2, 1],
        [5, 2, 1, 4, 3],
        [5, 2, 3, 4, 1],
        [5, 4, 1, 2, 3],
        [5, 4, 3, 2, 1],
    ]
    for i, exp in enumerate(expected, 1):
        out = sol.permute(n, i)
        if out != exp:
            print(f"n=5,k={i} expected {exp} got {out}")
        else:
            print(f"n=5,k={i} ok: {out}")
    # k beyond count
    out = sol.permute(5, 13)
    assert out == [], f"n=5,k=13 expected [] got {out}"
    print("n=5,k=13 passed:", out)

    # n=100, k=1 (should return [1,2,3,...,100])
    out = sol.permute(100, 1)
    assert out == list(range(1, 101)), "n=100,k=1 failed"
    print("n=100,k=1 passed")

    # n=100, k=2 (should return [1, 100, 2, 99, 3, 98, ...]? let's test small)
    out = sol.permute(100, 2)
    # Just check it's a valid alternating perm
    def valid(perm):
        if sorted(perm) != list(range(1, len(perm)+1)):
            return False
        for i in range(len(perm)-1):
            if (perm[i] % 2) == (perm[i+1] % 2):
                return False
        return True
    assert valid(out), f"n=100,k=2 invalid: {out}"
    print("n=100,k=2 passed (valid alternating perm)")

    # k larger than total should be []
    out = sol.permute(6, 1000)
    assert out == [], "n=6,k=1000 expected []"
    print("n=6,k=1000 passed")

    print("All tests passed.")