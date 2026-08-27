import sys
import heapq


def solve():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    n = next(it)
    k_limit = next(it)

    a = sorted((next(it) for _ in range(n)), reverse=True)
    b = sorted((next(it) for _ in range(n)), reverse=True)
    c = sorted((next(it) for _ in range(n)), reverse=True)

    nn = n * n

    def value(i, j, k):
        return a[i] * b[j] + b[j] * c[k] + c[k] * a[i]

    heap = [(-value(0, 0, 0), 0)]
    visited = {0}

    for step in range(k_limit):
        neg_score, state = heapq.heappop(heap)

        if step == k_limit - 1:
            print(-neg_score)
            return

        i = state // nn
        rem = state - i * nn
        j = rem // n
        l = rem - j * n

        if i + 1 < n:
            nxt = state + nn
            if nxt not in visited:
                visited.add(nxt)
                score = value(i + 1, j, l)
                heapq.heappush(heap, (-score, nxt))

        if j + 1 < n:
            nxt = state + n
            if nxt not in visited:
                visited.add(nxt)
                score = value(i, j + 1, l)
                heapq.heappush(heap, (-score, nxt))

        if l + 1 < n:
            nxt = state + 1
            if nxt not in visited:
                visited.add(nxt)
                score = value(i, j, l + 1)
                heapq.heappush(heap, (-score, nxt))


if __name__ == "__main__":
    solve()