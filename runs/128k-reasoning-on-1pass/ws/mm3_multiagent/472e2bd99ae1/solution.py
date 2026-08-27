import sys
import heapq

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    K = int(next(it))

    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    C = [int(next(it)) for _ in range(N)]

    # sort decreasing to make the value monotone decreasing with index
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    a, b, c = A, B, C
    n = N

    # encode triple (i,j,k) as a single integer for fast hashing
    def encode(i: int, j: int, k: int) -> int:
        return ((i * n) + j) * n + k

    # value of a triple
    def val(i: int, j: int, k: int) -> int:
        return a[i] * b[j] + b[j] * c[k] + c[k] * a[i]

    # max-heap using negative values
    heap = []
    heapq.heappush(heap, (-val(0, 0, 0), 0, 0, 0))

    visited = set()
    visited.add(encode(0, 0, 0))

    answer = None
    for step in range(K):
        neg, i, j, k = heapq.heappop(heap)
        cur = -neg
        if step == K - 1:
            answer = cur
            break

        # neighbor (i+1, j, k)
        if i + 1 < n:
            code = encode(i + 1, j, k)
            if code not in visited:
                visited.add(code)
                heapq.heappush(heap, (-val(i + 1, j, k), i + 1, j, k))

        # neighbor (i, j+1, k)
        if j + 1 < n:
            code = encode(i, j + 1, k)
            if code not in visited:
                visited.add(code)
                heapq.heappush(heap, (-val(i, j + 1, k), i, j + 1, k))

        # neighbor (i, j, k+1)
        if k + 1 < n:
            code = encode(i, j, k + 1)
            if code not in visited:
                visited.add(code)
                heapq.heappush(heap, (-val(i, j, k + 1), i, j, k + 1))

    sys.stdout.write(str(answer))

if __name__ == "__main__":
    solve()