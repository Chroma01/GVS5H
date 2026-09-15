import sys
import heapq


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    H, W, X = data[0], data[1], data[2]
    P, Q = data[3] - 1, data[4] - 1

    S = data[5:]
    del data

    N = H * W
    start = P * W + Q

    total = S[start]

    # state:
    # 0 = not in heap and not absorbed
    # 1 = currently in heap (boundary)
    # 2 = absorbed
    state = bytearray(N)
    state[start] = 2

    heap = []

    if P > 0:
        idx = start - W
        state[idx] = 1
        heap.append((S[idx], idx))
    if P + 1 < H:
        idx = start + W
        state[idx] = 1
        heap.append((S[idx], idx))
    if Q > 0:
        idx = start - 1
        state[idx] = 1
        heap.append((S[idx], idx))
    if Q + 1 < W:
        idx = start + 1
        state[idx] = 1
        heap.append((S[idx], idx))

    heapq.heapify(heap)

    heappop = heapq.heappop
    heappush = heapq.heappush

    while heap:
        s, idx = heappop(heap)

        if state[idx] != 1:
            continue

        # Strict condition: s < total / X  <=>  s * X < total
        if s * X >= total:
            break

        state[idx] = 2
        total += s

        if idx >= W:
            nb = idx - W
            if state[nb] == 0:
                state[nb] = 1
                heappush(heap, (S[nb], nb))

        if idx < N - W:
            nb = idx + W
            if state[nb] == 0:
                state[nb] = 1
                heappush(heap, (S[nb], nb))

        col = idx % W

        if col != 0:
            nb = idx - 1
            if state[nb] == 0:
                state[nb] = 1
                heappush(heap, (S[nb], nb))

        if col != W - 1:
            nb = idx + 1
            if state[nb] == 0:
                state[nb] = 1
                heappush(heap, (S[nb], nb))

    print(total)


if __name__ == "__main__":
    solve()