import sys
import heapq


def main():
    input = sys.stdin.buffer.readline

    N, K = map(int, input().split())
    A = sorted(map(int, input().split()), reverse=True)
    B = sorted(map(int, input().split()), reverse=True)
    C = sorted(map(int, input().split()), reverse=True)

    n2 = N * N

    def value(i, j, k):
        a = A[i]
        b = B[j]
        c = C[k]
        return a * b + b * c + c * a

    # Encode (i, j, k) as i*N^2 + j*N + k to reduce memory usage.
    initial = value(0, 0, 0)
    heap = [(-initial, 0)]
    seen = {0}

    answer = initial

    for _ in range(K):
        neg_value, code = heapq.heappop(heap)
        answer = -neg_value

        i, rem = divmod(code, n2)
        j, k = divmod(rem, N)

        if i + 1 < N:
            nxt = code + n2
            if nxt not in seen:
                seen.add(nxt)
                heapq.heappush(heap, (-value(i + 1, j, k), nxt))

        if j + 1 < N:
            nxt = code + N
            if nxt not in seen:
                seen.add(nxt)
                heapq.heappush(heap, (-value(i, j + 1, k), nxt))

        if k + 1 < N:
            nxt = code + 1
            if nxt not in seen:
                seen.add(nxt)
                heapq.heappush(heap, (-value(i, j, k + 1), nxt))

    print(answer)


if __name__ == "__main__":
    main()