import sys
import heapq


def solve():
    input = sys.stdin.buffer.readline

    H, W, X = map(int, input().split())
    P, Q = map(int, input().split())

    # Padded grid:
    # state = 0: unseen
    # state = 1: already in heap (frontier)
    # state = 2: absorbed or outside border
    stride = W + 2
    n = (H + 2) * stride

    S = [0] * n
    for r in range(1, H + 1):
        base = r * stride + 1
        S[base:base + W] = list(map(int, input().split()))

    state = bytearray(n)

    # Mark outer border as unavailable.
    bottom = (H + 1) * stride
    for c in range(W + 2):
        state[c] = 2
        state[bottom + c] = 2
    for r in range(1, H + 1):
        left = r * stride
        state[left] = 2
        state[left + W + 1] = 2

    start = P * stride + Q
    strength = S[start]
    state[start] = 2

    heap = []
    heappush = heapq.heappush
    heappop = heapq.heappop

    # Initial frontier.
    nb = start - stride
    if state[nb] == 0:
        state[nb] = 1
        heappush(heap, (S[nb], nb))

    nb = start + stride
    if state[nb] == 0:
        state[nb] = 1
        heappush(heap, (S[nb], nb))

    nb = start - 1
    if state[nb] == 0:
        state[nb] = 1
        heappush(heap, (S[nb], nb))

    nb = start + 1
    if state[nb] == 0:
        state[nb] = 1
        heappush(heap, (S[nb], nb))

    while heap:
        s, idx = heap[0]

        # Normally unnecessary because duplicates are prevented, but safe.
        if state[idx] == 2:
            heappop(heap)
            continue

        # Strict condition: s < strength / X  <=>  s * X < strength.
        if s * X >= strength:
            break

        heappop(heap)
        state[idx] = 2
        strength += s

        nb = idx - stride
        if state[nb] == 0:
            state[nb] = 1
            heappush(heap, (S[nb], nb))

        nb = idx + stride
        if state[nb] == 0:
            state[nb] = 1
            heappush(heap, (S[nb], nb))

        nb = idx - 1
        if state[nb] == 0:
            state[nb] = 1
            heappush(heap, (S[nb], nb))

        nb = idx + 1
        if state[nb] == 0:
            state[nb] = 1
            heappush(heap, (S[nb], nb))

    print(strength)


if __name__ == "__main__":
    solve()