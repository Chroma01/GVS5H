import sys
import heapq


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    k = data[1]

    a = sorted(data[2:2 + n], reverse=True)
    b = sorted(data[2 + n:2 + 2 * n], reverse=True)
    c = sorted(data[2 + 2 * n:2 + 3 * n], reverse=True)

    n2 = n * n

    def value(i, j, z):
        x = a[i]
        y = b[j]
        w = c[z]
        return x * y + y * w + w * x

    # Encode (i, j, z) as i*n^2 + j*n + z.
    initial = value(0, 0, 0)
    heap = [(-initial, 0)]
    seen = {0}

    answer = initial

    for _ in range(k):
        neg_score, code = heapq.heappop(heap)
        answer = -neg_score

        i = code // n2
        rem = code - i * n2
        j = rem // n
        z = rem - j * n

        if i + 1 < n:
            nxt = code + n2
            if nxt not in seen:
                seen.add(nxt)
                heapq.heappush(heap, (-value(i + 1, j, z), nxt))

        if j + 1 < n:
            nxt = code + n
            if nxt not in seen:
                seen.add(nxt)
                heapq.heappush(heap, (-value(i, j + 1, z), nxt))

        if z + 1 < n:
            nxt = code + 1
            if nxt not in seen:
                seen.add(nxt)
                heapq.heappush(heap, (-value(i, j, z + 1), nxt))

    print(answer)


if __name__ == "__main__":
    main()