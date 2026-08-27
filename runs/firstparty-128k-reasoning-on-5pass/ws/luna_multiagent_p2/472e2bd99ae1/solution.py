import sys
import heapq


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, k = data[0], data[1]

    p = 2
    a = sorted(data[p:p + n], reverse=True)
    p += n
    b = sorted(data[p:p + n], reverse=True)
    p += n
    c = sorted(data[p:p + n], reverse=True)

    nn = n * n

    def value(i, j, z):
        x = a[i]
        y = b[j]
        w = c[z]
        return x * y + y * w + w * x

    heap = [(-value(0, 0, 0), 0)]
    visited = {0}

    answer = 0

    for _ in range(k):
        neg_val, code = heapq.heappop(heap)
        answer = -neg_val

        i, rem = divmod(code, nn)
        j, z = divmod(rem, n)

        if i + 1 < n:
            next_code = code + nn
            if next_code not in visited:
                visited.add(next_code)
                x = a[i + 1]
                y = b[j]
                w = c[z]
                heapq.heappush(
                    heap,
                    (-(x * y + y * w + w * x), next_code)
                )

        if j + 1 < n:
            next_code = code + n
            if next_code not in visited:
                visited.add(next_code)
                x = a[i]
                y = b[j + 1]
                w = c[z]
                heapq.heappush(
                    heap,
                    (-(x * y + y * w + w * x), next_code)
                )

        if z + 1 < n:
            next_code = code + 1
            if next_code not in visited:
                visited.add(next_code)
                x = a[i]
                y = b[j]
                w = c[z + 1]
                heapq.heappush(
                    heap,
                    (-(x * y + y * w + w * x), next_code)
                )

    print(answer)


if __name__ == "__main__":
    solve()