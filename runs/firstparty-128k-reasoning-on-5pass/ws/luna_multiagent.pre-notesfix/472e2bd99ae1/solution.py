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

    nn = n * n

    def value(i, j, z):
        return a[i] * b[j] + b[j] * c[z] + c[z] * a[i]

    initial = value(0, 0, 0)
    heap = [(-initial, 0)]

    for _ in range(k):
        neg_val, state = heapq.heappop(heap)
        current = -neg_val

        if _ == k - 1:
            print(current)
            return

        x, z = divmod(state, n)
        i, j = divmod(x, n)

        # Every state has a unique canonical parent:
        # decrease i if i > 0, otherwise decrease j if j > 0,
        # otherwise decrease k. This avoids duplicate states
        # without requiring a large visited set.

        if i + 1 < n:
            ni = i + 1
            nv = value(ni, j, z)
            heapq.heappush(heap, (-nv, state + nn))

        if i == 0 and j + 1 < n:
            nj = j + 1
            nv = value(i, nj, z)
            heapq.heappush(heap, (-nv, state + n))

        if i == 0 and j == 0 and z + 1 < n:
            nz = z + 1
            nv = value(i, j, nz)
            heapq.heappush(heap, (-nv, state + 1))


if __name__ == "__main__":
    solve()