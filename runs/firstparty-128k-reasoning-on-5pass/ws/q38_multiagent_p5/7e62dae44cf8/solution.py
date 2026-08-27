import sys
import heapq


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    H, W, X = data[0], data[1], data[2]
    P, Q = data[3], data[4]
    S = data[5:]
    del data

    N = H * W
    start = (P - 1) * W + (Q - 1)
    T = S[start]

    seen = bytearray(N)
    absorbed = bytearray(N)
    seen[start] = 1
    absorbed[start] = 1

    heap = []
    push = heapq.heappush
    pop = heapq.heappop

    w = W
    n = N
    x = X
    arr = S
    n_minus_w = n - w
    w_minus_1 = w - 1

    # Initial boundary cells.
    if start >= w:
        nb = start - w
        if not seen[nb]:
            seen[nb] = 1
            push(heap, (arr[nb], nb))
    if start < n_minus_w:
        nb = start + w
        if not seen[nb]:
            seen[nb] = 1
            push(heap, (arr[nb], nb))
    col = start % w
    if col:
        nb = start - 1
        if not seen[nb]:
            seen[nb] = 1
            push(heap, (arr[nb], nb))
    if col != w_minus_1:
        nb = start + 1
        if not seen[nb]:
            seen[nb] = 1
            push(heap, (arr[nb], nb))

    while heap:
        s, idx = pop(heap)
        if absorbed[idx]:
            continue

        # Strictly less than T / X  <=>  X * s < T.
        if x * s >= T:
            break

        absorbed[idx] = 1
        T += s

        if idx >= w:
            nb = idx - w
            if not seen[nb]:
                seen[nb] = 1
                push(heap, (arr[nb], nb))
        if idx < n_minus_w:
            nb = idx + w
            if not seen[nb]:
                seen[nb] = 1
                push(heap, (arr[nb], nb))

        col = idx % w
        if col:
            nb = idx - 1
            if not seen[nb]:
                seen[nb] = 1
                push(heap, (arr[nb], nb))
        if col != w_minus_1:
            nb = idx + 1
            if not seen[nb]:
                seen[nb] = 1
                push(heap, (arr[nb], nb))

    print(T)


if __name__ == "__main__":
    main()