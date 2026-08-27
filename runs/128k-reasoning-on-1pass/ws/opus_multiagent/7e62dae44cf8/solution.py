import sys
from heapq import heappush, heappop

def main():
    data = sys.stdin.buffer.read().split()
    ptr = 0
    H = int(data[ptr]); ptr += 1
    W = int(data[ptr]); ptr += 1
    X = int(data[ptr]); ptr += 1
    P = int(data[ptr]); ptr += 1
    Q = int(data[ptr]); ptr += 1
    n = H * W
    S = [int(x) for x in data[ptr:ptr + n]]

    pi = P - 1
    qi = Q - 1
    start = pi * W + qi
    cur = S[start]

    seen = bytearray(n)
    seen[start] = 1

    heap = []
    # push neighbors of start
    if pi > 0:
        k = start - W
        seen[k] = 1
        heappush(heap, S[k] * n + k)
    if pi < H - 1:
        k = start + W
        seen[k] = 1
        heappush(heap, S[k] * n + k)
    if qi > 0:
        k = start - 1
        seen[k] = 1
        heappush(heap, S[k] * n + k)
    if qi < W - 1:
        k = start + 1
        seen[k] = 1
        heappush(heap, S[k] * n + k)

    while heap:
        top = heap[0]
        idx = top % n
        s = top // n
        if s * X >= cur:
            break
        heappop(heap)
        cur += s
        i, j = divmod(idx, W)
        if i > 0:
            k = idx - W
            if not seen[k]:
                seen[k] = 1
                heappush(heap, S[k] * n + k)
        if i < H - 1:
            k = idx + W
            if not seen[k]:
                seen[k] = 1
                heappush(heap, S[k] * n + k)
        if j > 0:
            k = idx - 1
            if not seen[k]:
                seen[k] = 1
                heappush(heap, S[k] * n + k)
        if j < W - 1:
            k = idx + 1
            if not seen[k]:
                seen[k] = 1
                heappush(heap, S[k] * n + k)

    sys.stdout.write(str(cur) + "\n")

main()