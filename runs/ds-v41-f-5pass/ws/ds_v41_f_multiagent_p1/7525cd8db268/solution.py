from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)

        # Bucket pairs by their larger endpoint b (normalize so a < b).
        by_b = [[] for _ in range(n + 1)]
        for i, (x, y) in enumerate(conflictingPairs):
            if x < y:
                a, b = x, y
            else:
                a, b = y, x
            by_b[b].append((a, i))

        # Active set grows monotonically as r increases. Track:
        #   max1   = largest a among pairs with b <= r (0 if none)
        #   max2   = largest a strictly less than max1 (0 if none)
        #   cnt1   = how many active pairs attain max1
        #   owner1 = pair id attaining max1 when it is unique
        max1 = 0
        max2 = 0
        cnt1 = 0
        owner1 = -1

        baseline = 0
        gain = [0] * m

        for r in range(1, n + 1):
            for a, i in by_b[r]:
                if a > max1:
                    max2 = max1
                    max1 = a
                    cnt1 = 1
                    owner1 = i
                elif a == max1:
                    cnt1 += 1
                    owner1 = -1
                elif a > max2:
                    max2 = a

            # Subarray [l, r] is valid iff l > max1; count = r - max1
            baseline += r - max1

            # Removing the unique max pair drops the bound to max2
            if cnt1 == 1:
                gain[owner1] += max1 - max2

        best = 0
        for g in gain:
            if g > best:
                best = g
        return baseline + best


if __name__ == "__main__":
    import random

    def brute(n, pairs):
        m = len(pairs)
        best = 0
        for rem in range(m):
            cnt = 0
            for l in range(1, n + 1):
                for r in range(l, n + 1):
                    ok = True
                    for j, (x, y) in enumerate(pairs):
                        if j == rem:
                            continue
                        a, b = (x, y) if x < y else (y, x)
                        if l <= a and b <= r:
                            ok = False
                            break
                    if ok:
                        cnt += 1
            if cnt > best:
                best = cnt
        return best

    sol = Solution()
    print("ex1:", sol.maxSubarrays(4, [[2, 3], [1, 4]]), "expected 9")
    print("ex2:", sol.maxSubarrays(5, [[1, 2], [2, 5], [3, 5]]), "expected 12")

    random.seed(1)
    mismatches = 0
    for _ in range(20000):
        n = random.randint(2, 7)
        m = random.randint(1, 2 * n)
        pairs = []
        for _ in range(m):
            a = random.randint(1, n)
            b = random.randint(1, n)
            while b == a:
                b = random.randint(1, n)
            pairs.append([a, b])
        got = sol.maxSubarrays(n, pairs)
        exp = brute(n, pairs)
        if got != exp:
            mismatches += 1
            if mismatches <= 5:
                print("MISMATCH", n, pairs, "got", got, "exp", exp)
    print("brute-force mismatches:", mismatches)