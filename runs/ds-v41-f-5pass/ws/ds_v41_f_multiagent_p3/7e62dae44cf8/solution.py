import sys
import heapq


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    H, W, X = data[0], data[1], data[2]
    P, Q = data[3] - 1, data[4] - 1
    vals = data[5:5 + H * W]
    S = [vals[i * W:(i + 1) * W] for i in range(H)]

    occupied = bytearray(H * W)
    start_idx = P * W + Q
    occupied[start_idx] = 1
    cur = S[P][Q]

    heap = []

    if P > 0:
        heapq.heappush(heap, (S[P - 1][Q], P - 1, Q))
    if P + 1 < H:
        heapq.heappush(heap, (S[P + 1][Q], P + 1, Q))
    if Q > 0:
        heapq.heappush(heap, (S[P][Q - 1], P, Q - 1))
    if Q + 1 < W:
        heapq.heappush(heap, (S[P][Q + 1], P, Q + 1))

    while heap:
        val, i, j = heapq.heappop(heap)
        idx = i * W + j

        if occupied[idx]:
            continue

        if X * val < cur:
            occupied[idx] = 1
            cur += val

            if i > 0:
                ni = i - 1
                nidx = ni * W + j
                if not occupied[nidx]:
                    heapq.heappush(heap, (S[ni][j], ni, j))
            if i + 1 < H:
                ni = i + 1
                nidx = ni * W + j
                if not occupied[nidx]:
                    heapq.heappush(heap, (S[ni][j], ni, j))
            if j > 0:
                nj = j - 1
                nidx = i * W + nj
                if not occupied[nidx]:
                    heapq.heappush(heap, (S[i][nj], i, nj))
            if j + 1 < W:
                nj = j + 1
                nidx = i * W + nj
                if not occupied[nidx]:
                    heapq.heappush(heap, (S[i][nj], i, nj))
        else:
            break

    print(cur)


if __name__ == "__main__":
    main()