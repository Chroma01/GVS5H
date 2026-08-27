import sys
from heapq import heappush, heappop

def main():
    vals = list(map(int, sys.stdin.buffer.read().split()))
    if not vals:
        return

    H, W, X, P, Q = vals[:5]
    S = vals[5:]
    del vals

    N = H * W
    start = (P - 1) * W + (Q - 1)
    total = S[start]

    # state: 0 = unseen, 1 = in heap, 2 = absorbed
    state = bytearray(N)
    state[start] = 2

    heap = []
    push = heappush
    pop = heappop

    limit = N - W
    last_col = W - 1

    # Initial frontier: neighbors of the starting cell.
    if start >= W:
        n = start - W
        if state[n] == 0:
            state[n] = 1
            push(heap, (S[n], n))

    if start < limit:
        n = start + W
        if state[n] == 0:
            state[n] = 1
            push(heap, (S[n], n))

    col = start % W
    if col != 0:
        n = start - 1
        if state[n] == 0:
            state[n] = 1
            push(heap, (S[n], n))

    if col != last_col:
        n = start + 1
        if state[n] == 0:
            state[n] = 1
            push(heap, (S[n], n))

    while heap:
        s, v = pop(heap)

        if state[v] == 2:
            continue

        if X * s < total:
            state[v] = 2
            total += s

            if v >= W:
                n = v - W
                if state[n] == 0:
                    state[n] = 1
                    push(heap, (S[n], n))

            if v < limit:
                n = v + W
                if state[n] == 0:
                    state[n] = 1
                    push(heap, (S[n], n))

            col = v % W
            if col != 0:
                n = v - 1
                if state[n] == 0:
                    state[n] = 1
                    push(heap, (S[n], n))

            if col != last_col:
                n = v + 1
                if state[n] == 0:
                    state[n] = 1
                    push(heap, (S[n], n))
        else:
            break

    print(total)

if __name__ == "__main__":
    main()