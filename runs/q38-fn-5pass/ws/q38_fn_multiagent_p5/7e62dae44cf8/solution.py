import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    H = int(data[0])
    W = int(data[1])
    X = int(data[2])
    P = int(data[3]) - 1
    Q = int(data[4]) - 1

    N = H * W
    S = [0] * N
    for i in range(N):
        S[i] = int(data[5 + i])
    del data

    start = P * W + Q
    total = S[start]

    # state: 0 = unseen, 1 = in heap, 2 = absorbed
    state = bytearray(N)
    state[start] = 2

    heap = []
    heappush = heapq.heappush
    heappop = heapq.heappop

    # Add initial frontier around the starting cell.
    if start >= W:
        nb = start - W
        state[nb] = 1
        heappush(heap, (S[nb], nb))

    if start < N - W:
        nb = start + W
        state[nb] = 1
        heappush(heap, (S[nb], nb))

    c = start % W
    if c != 0:
        nb = start - 1
        state[nb] = 1
        heappush(heap, (S[nb], nb))

    if c != W - 1:
        nb = start + 1
        state[nb] = 1
        heappush(heap, (S[nb], nb))

    while heap:
        s, idx = heappop(heap)

        # Ignore stale entries if any duplicate ever appears.
        if state[idx] != 1:
            continue

        # Need strictly s < total / X, i.e. s * X < total.
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

        c = idx % W
        if c != 0:
            nb = idx - 1
            if state[nb] == 0:
                state[nb] = 1
                heappush(heap, (S[nb], nb))

        if c != W - 1:
            nb = idx + 1
            if state[nb] == 0:
                state[nb] = 1
                heappush(heap, (S[nb], nb))

    print(total)


if __name__ == "__main__":
    main()