import sys
import heapq


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, k = data[0], data[1]

    a = data[2:2 + n]
    b = data[2 + n:2 + 2 * n]
    c = data[2 + 2 * n:2 + 3 * n]

    a.sort(reverse=True)
    b.sort(reverse=True)
    c.sort(reverse=True)

    initial = a[0] * b[0] + b[0] * c[0] + c[0] * a[0]
    heap = [(-initial, 0, 0, 0)]
    visited = {(0, 0, 0)}

    for step in range(k):
        neg_value, i, j, l = heapq.heappop(heap)

        if step == k - 1:
            print(-neg_value)
            return

        if i + 1 < n:
            state = (i + 1, j, l)
            if state not in visited:
                visited.add(state)
                ai = a[i + 1]
                bj = b[j]
                ck = c[l]
                value = ai * bj + bj * ck + ck * ai
                heapq.heappush(heap, (-value, i + 1, j, l))

        if j + 1 < n:
            state = (i, j + 1, l)
            if state not in visited:
                visited.add(state)
                ai = a[i]
                bj = b[j + 1]
                ck = c[l]
                value = ai * bj + bj * ck + ck * ai
                heapq.heappush(heap, (-value, i, j + 1, l))

        if l + 1 < n:
            state = (i, j, l + 1)
            if state not in visited:
                visited.add(state)
                ai = a[i]
                bj = b[j]
                ck = c[l + 1]
                value = ai * bj + bj * ck + ck * ai
                heapq.heappush(heap, (-value, i, j, l + 1))


if __name__ == "__main__":
    solve()