from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def feasible(T):
            c = [(T + p - 1) // p for p in points]
            G0 = [0] * (n + 1)
            G1 = [0] * (n + 1)
            for i in range(n - 1, -1, -1):
                bi = c[i]
                r0 = G0[i + 1]
                r1 = G1[i + 1]
                G1[i] = r0 + bi
                G0[i] = r0 if r0 > r1 else r1

            F0 = 0
            F1 = 0
            for E in range(n):
                ai = c[E] - 1
                if ai < 0:
                    ai = 0
                oldF0 = F0
                oldF1 = F1
                F1 = oldF0 + ai
                F0 = oldF0 if oldF0 > oldF1 else oldF1

                g0 = G0[E + 1]
                g1 = G1[E + 1]
                suf = g0 if g0 > g1 else g1
                cand1 = F0 + suf
                cand2 = F1 + g0
                mw = cand1 if cand1 > cand2 else cand2

                if 2 * mw + E + 1 <= m:
                    return True
            return False

        lo = 0
        hi = min(points) * ((m + 1) // 2)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo


def brute(points, m):
    n = len(points)
    best = 0
    def dfs(idx, moves, scores):
        nonlocal best
        cur = min(scores)
        if cur > best:
            best = cur
        if moves == m:
            return
        if idx + 1 < n:
            scores[idx + 1] += points[idx + 1]
            dfs(idx + 1, moves + 1, scores)
            scores[idx + 1] -= points[idx + 1]
        if idx - 1 >= 0:
            scores[idx - 1] += points[idx - 1]
            dfs(idx - 1, moves + 1, scores)
            scores[idx - 1] -= points[idx - 1]
    if n > 0:
        scores = [0] * n
        scores[0] += points[0]
        dfs(0, 1, scores)
    return best


if __name__ == '__main__':
    import random
    sol = Solution()
    assert sol.maxScore([2, 4], 3) == 4, "Sample 1 failed"
    assert sol.maxScore([1, 2, 3], 5) == 2, "Sample 2 failed"
    print("Sample tests passed: Example1=4, Example2=2")
    for _ in range(200):
        n = random.randint(2, 6)
        m = random.randint(1, 12)
        points = [random.randint(1, 6) for _ in range(n)]
        expected = brute(points, m)
        got = sol.maxScore(points, m)
        if expected != got:
            print(f"Mismatch: points={points}, m={m}, expected={expected}, got={got}")
            break
    else:
        print("Random cross-check passed (200 cases)")