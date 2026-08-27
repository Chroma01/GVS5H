import sys
import heapq


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    H = data[0]
    W = data[1]
    X = data[2]
    P = data[3]
    Q = data[4]

    N = H * W
    S = data[5:5 + N]
    del data

    start = (P - 1) * W + (Q - 1)
    total = S[start]

    visited = bytearray(N)
    in_heap = bytearray(N)
    visited[start] = 1

    heap = []
    push = heapq.heappush
    pop = heapq.heappop

    if P > 1:
        idx = start - W
        in_heap[idx] = 1
        push(heap, (S[idx], idx))
    if P < H:
        idx = start + W
        in_heap[idx] = 1
        push(heap, (S[idx], idx))
    if Q > 1:
        idx = start - 1
        in_heap[idx] = 1
        push(heap, (S[idx], idx))
    if Q < W:
        idx = start + 1
        in_heap[idx] = 1
        push(heap, (S[idx], idx))

    while heap:
        s, idx = pop(heap)
        in_heap[idx] = 0

        if visited[idx]:
            continue

        if X * s >= total:
            break

        visited[idx] = 1
        total += s

        if idx >= W:
            nidx = idx - W
            if not visited[nidx] and not in_heap[nidx]:
                in_heap[nidx] = 1
                push(heap, (S[nidx], nidx))

        if idx < N - W:
            nidx = idx + W
            if not visited[nidx] and not in_heap[nidx]:
                in_heap[nidx] = 1
                push(heap, (S[nidx], nidx))

        col = idx % W

        if col > 0:
            nidx = idx - 1
            if not visited[nidx] and not in_heap[nidx]:
                in_heap[nidx] = 1
                push(heap, (S[nidx], nidx))

        if col + 1 < W:
            nidx = idx + 1
            if not visited[nidx] and not in_heap[nidx]:
                in_heap[nidx] = 1
                push(heap, (S[nidx], nidx))

    print(total)


if __name__ == "__main__":
    main()