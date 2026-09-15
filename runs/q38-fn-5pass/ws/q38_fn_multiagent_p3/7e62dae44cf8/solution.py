import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    H = int(data[0])
    W = int(data[1])
    X = int(data[2])
    P = int(data[3])
    Q = int(data[4])
    N = H * W

    vals = list(map(int, data[5:5 + N]))
    del data

    # Padded grid: a visited sentinel border avoids boundary checks.
    stride = W + 2
    size = (H + 2) * stride
    S = [0] * size

    k = 0
    for i in range(1, H + 1):
        base = i * stride + 1
        S[base:base + W] = vals[k:k + W]
        k += W
    del vals

    visited = bytearray(size)

    # Mark top and bottom border as visited.
    bottom = (H + 1) * stride
    for j in range(stride):
        visited[j] = 1
        visited[bottom + j] = 1

    # Mark left and right border as visited.
    for i in range(H + 2):
        base = i * stride
        visited[base] = 1
        visited[base + W + 1] = 1

    start = P * stride + Q
    total = S[start]
    visited[start] = 1

    heap = []
    heappush = heapq.heappush
    heappop = heapq.heappop

    # Initial boundary.
    nb = start - 1
    if not visited[nb]:
        visited[nb] = 1
        heappush(heap, (S[nb], nb))

    nb = start + 1
    if not visited[nb]:
        visited[nb] = 1
        heappush(heap, (S[nb], nb))

    nb = start - stride
    if not visited[nb]:
        visited[nb] = 1
        heappush(heap, (S[nb], nb))

    nb = start + stride
    if not visited[nb]:
        visited[nb] = 1
        heappush(heap, (S[nb], nb))

    while heap:
        s, idx = heap[0]

        # Strict condition: s < total / X  <=>  s * X < total.
        if s * X >= total:
            break

        heappop(heap)
        total += s

        nb = idx - 1
        if not visited[nb]:
            visited[nb] = 1
            heappush(heap, (S[nb], nb))

        nb = idx + 1
        if not visited[nb]:
            visited[nb] = 1
            heappush(heap, (S[nb], nb))

        nb = idx - stride
        if not visited[nb]:
            visited[nb] = 1
            heappush(heap, (S[nb], nb))

        nb = idx + stride
        if not visited[nb]:
            visited[nb] = 1
            heappush(heap, (S[nb], nb))

    print(total)


if __name__ == "__main__":
    main()