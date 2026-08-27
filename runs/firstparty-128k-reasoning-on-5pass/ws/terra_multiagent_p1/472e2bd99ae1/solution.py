import sys
import heapq

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    kth = data[1]

    a = sorted(data[2:2 + n], reverse=True)
    b = sorted(data[2 + n:2 + 2 * n], reverse=True)
    c = sorted(data[2 + 2 * n:2 + 3 * n], reverse=True)
    del data

    m = min(n, kth)
    a = a[:m]
    b = b[:m]
    c = c[:m]

    m2 = m * m
    bits = (m * m * m - 1).bit_length()
    mask = (1 << bits) - 1

    def score(i, j, k):
        x = a[i]
        y = b[j]
        z = c[k]
        return x * y + y * z + z * x

    initial_score = score(0, 0, 0)
    heap = [-((initial_score << bits) | 0)]
    visited = {0}

    answer = 0

    for _ in range(kth):
        packed = -heapq.heappop(heap)
        answer = packed >> bits
        key = packed & mask

        i = key // m2
        rem = key - i * m2
        j = rem // m
        k = rem - j * m

        if i + 1 < m:
            nxt = key + m2
            if nxt not in visited:
                visited.add(nxt)
                value = score(i + 1, j, k)
                heapq.heappush(heap, -((value << bits) | nxt))

        if j + 1 < m:
            nxt = key + m
            if nxt not in visited:
                visited.add(nxt)
                value = score(i, j + 1, k)
                heapq.heappush(heap, -((value << bits) | nxt))

        if k + 1 < m:
            nxt = key + 1
            if nxt not in visited:
                visited.add(nxt)
                value = score(i, j, k + 1)
                heapq.heappush(heap, -((value << bits) | nxt))

    print(answer)

if __name__ == "__main__":
    main()