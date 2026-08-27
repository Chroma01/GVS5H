from typing import List


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        # d(x) = floor(log4 x) + 1 for x >= 1
        # f(n) = sum_{x=1}^{n} d(x)
        # pre[b] = f(4^b - 1) = sum_{j=0}^{b-1} (j+1) * (4^{j+1} - 4^j)
        MAXB = 17
        pows = [1] * (MAXB + 1)
        for k in range(1, MAXB + 1):
            pows[k] = pows[k - 1] * 4
        pre = [0] * (MAXB + 1)
        for b in range(1, MAXB + 1):
            pre[b] = pre[b - 1] + b * (pows[b] - pows[b - 1])

        def f(n: int) -> int:
            if n <= 0:
                return 0
            b = (n.bit_length() - 1) >> 1  # 4^b <= n < 4^(b+1)
            return pre[b] + (b + 1) * (n - pows[b] + 1)

        total = 0
        for l, r in queries:
            S = f(r) - f(l - 1)
            total += (S + 1) >> 1
        return total


if __name__ == "__main__":
    sol = Solution()
    # provided examples
    assert sol.minOperations([[1, 2], [2, 4]]) == 3
    assert sol.minOperations([[2, 6]]) == 4

    # brute force check: greedy pair-the-two-largest simulation
    import heapq

    def d(x):
        c = 0
        while x > 0:
            x //= 4
            c += 1
        return c

    def brute(l, r):
        h = [-d(x) for x in range(l, r + 1)]
        heapq.heapify(h)
        ops = 0
        while True:
            a = -heapq.heappop(h)
            if a == 0:
                break
            b = -heapq.heappop(h) if h else 0
            ops += 1
            heapq.heappush(h, -(a - 1))
            heapq.heappush(h, -max(b - 1, 0))
        return ops

    for l in range(1, 41):
        for r in range(l + 1, 41):
            assert sol.minOperations([[l, r]]) == brute(l, r), (l, r)
    print("all tests passed")