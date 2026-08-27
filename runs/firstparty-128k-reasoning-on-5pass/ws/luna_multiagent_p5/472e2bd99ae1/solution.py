import sys
import heapq


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, k = data[0], data[1]

    a = sorted(data[2:2 + n], reverse=True)
    b = sorted(data[2 + n:2 + 2 * n], reverse=True)
    c = sorted(data[2 + 2 * n:2 + 3 * n], reverse=True)

    n2 = n * n

    def value(i, j, l):
        return a[i] * b[j] + b[j] * c[l] + c[l] * a[i]

    start_score = value(0, 0, 0)
    heap = [(-start_score, 0)]
    seen = {0}

    answer = start_score

    for _ in range(k):
        neg_score, state = heapq.heappop(heap)
        answer = -neg_score

        i = state // n2
        rem = state % n2
        j = rem // n
        l = rem % n

        if i + 1 < n:
            nxt = state + n2
            if nxt not in seen:
                seen.add(nxt)
                heapq.heappush(heap, (-value(i + 1, j, l), nxt))

        if j + 1 < n:
            nxt = state + n
            if nxt not in seen:
                seen.add(nxt)
                heapq.heappush(heap, (-value(i, j + 1, l), nxt))

        if l + 1 < n:
            nxt = state + 1
            if nxt not in seen:
                seen.add(nxt)
                heapq.heappush(heap, (-value(i, j, l + 1), nxt))

    print(answer)


if __name__ == "__main__":
    solve()