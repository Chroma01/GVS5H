import sys
import heapq


def main():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    n = next(it)
    k_needed = next(it)

    a = [next(it) for _ in range(n)]
    b = [next(it) for _ in range(n)]
    c = [next(it) for _ in range(n)]
    del it

    a.sort(reverse=True)
    b.sort(reverse=True)
    c.sort(reverse=True)

    n2 = n * n

    # Encoded index: i * n^2 + j * n + k
    heap = [(-(a[0] * b[0] + b[0] * c[0] + c[0] * a[0]), 0)]
    visited = {0}

    for count in range(k_needed):
        neg_value, code = heapq.heappop(heap)

        if count + 1 == k_needed:
            print(-neg_value)
            return

        i, rest = divmod(code, n2)
        j, k = divmod(rest, n)

        if i + 1 < n:
            nxt = code + n2
            if nxt not in visited:
                visited.add(nxt)
                ni = i + 1
                value = a[ni] * b[j] + b[j] * c[k] + c[k] * a[ni]
                heapq.heappush(heap, (-value, nxt))

        if j + 1 < n:
            nxt = code + n
            if nxt not in visited:
                visited.add(nxt)
                nj = j + 1
                value = a[i] * b[nj] + b[nj] * c[k] + c[k] * a[i]
                heapq.heappush(heap, (-value, nxt))

        if k + 1 < n:
            nxt = code + 1
            if nxt not in visited:
                visited.add(nxt)
                nk = k + 1
                value = a[i] * b[j] + b[j] * c[nk] + c[nk] * a[i]
                heapq.heappush(heap, (-value, nxt))


if __name__ == "__main__":
    main()