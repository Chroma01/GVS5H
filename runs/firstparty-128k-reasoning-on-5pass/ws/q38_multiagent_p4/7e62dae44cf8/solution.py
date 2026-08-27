import sys
from heapq import heappush, heappop

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    H = int(next(it))
    W = int(next(it))
    X = int(next(it))
    P = int(next(it))
    Q = int(next(it))

    grid = list(map(int, it))
    del data, it

    N = H * W
    start = (P - 1) * W + (Q - 1)
    total = grid[start]

    # state: 0 = unseen, 1 = in frontier, 2 = absorbed
    state = bytearray(N)
    state[start] = 2

    heap = []
    push = heappush
    pop = heappop

    if P > 1:
        n = start - W
        state[n] = 1
        push(heap, (grid[n], n))
    if P < H:
        n = start + W
        state[n] = 1
        push(heap, (grid[n], n))
    if Q > 1:
        n = start - 1
        state[n] = 1
        push(heap, (grid[n], n))
    if Q < W:
        n = start + 1
        state[n] = 1
        push(heap, (grid[n], n))

    last_col = W - 1
    bottom_limit = N - W

    while heap:
        s, idx = pop(heap)

        if state[idx] != 1:
            continue

        if X * s < total:
            total += s
            state[idx] = 2

            if idx >= W:
                n = idx - W
                if state[n] == 0:
                    state[n] = 1
                    push(heap, (grid[n], n))

            if idx < bottom_limit:
                n = idx + W
                if state[n] == 0:
                    state[n] = 1
                    push(heap, (grid[n], n))

            col = idx % W

            if col:
                n = idx - 1
                if state[n] == 0:
                    state[n] = 1
                    push(heap, (grid[n], n))

            if col != last_col:
                n = idx + 1
                if state[n] == 0:
                    state[n] = 1
                    push(heap, (grid[n], n))
        else:
            break

    print(total)

if __name__ == "__main__":
    main()