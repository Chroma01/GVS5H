import sys
import heapq

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    H, W, X = data[0], data[1], data[2]
    P = data[3] - 1
    Q = data[4] - 1
    N = H * W
    S = data[5:5 + N]

    start = P * W + Q

    # state: 0 = unseen, 1 = in heap/frontier, 2 = absorbed
    state = bytearray(N)
    state[start] = 2

    current = S[start]
    heap = []

    heappush = heapq.heappush
    heappop = heapq.heappop

    w = W
    n = N
    x = X
    vals = S
    st = state

    # Initialize frontier from the starting cell.
    if start >= w:
        nb = start - w
        st[nb] = 1
        heappush(heap, (vals[nb], nb))

    if start < n - w:
        nb = start + w
        st[nb] = 1
        heappush(heap, (vals[nb], nb))

    col = start % w
    if col > 0:
        nb = start - 1
        st[nb] = 1
        heappush(heap, (vals[nb], nb))

    if col < w - 1:
        nb = start + 1
        st[nb] = 1
        heappush(heap, (vals[nb], nb))

    while heap:
        s, idx = heappop(heap)

        # Should rarely be needed because queued cells are not duplicated,
        # but keeps the logic safe.
        if st[idx] == 2:
            continue

        # Strict condition: s < current / X  <=>  current > X * s.
        if current > x * s:
            st[idx] = 2
            current += s

            if idx >= w:
                nb = idx - w
                if st[nb] == 0:
                    st[nb] = 1
                    heappush(heap, (vals[nb], nb))

            if idx < n - w:
                nb = idx + w
                if st[nb] == 0:
                    st[nb] = 1
                    heappush(heap, (vals[nb], nb))

            col = idx % w

            if col > 0:
                nb = idx - 1
                if st[nb] == 0:
                    st[nb] = 1
                    heappush(heap, (vals[nb], nb))

            if col < w - 1:
                nb = idx + 1
                if st[nb] == 0:
                    st[nb] = 1
                    heappush(heap, (vals[nb], nb))
        else:
            # The weakest frontier cell cannot be absorbed, so no frontier
            # cell can be absorbed.
            break

    print(current)

if __name__ == "__main__":
    solve()