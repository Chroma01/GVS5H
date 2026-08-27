import sys

def solve():
    input = sys.stdin.buffer.readline

    N, K = map(int, input().split())
    A = list(map(int, input().split()))

    total_xor = 0
    for value in A:
        total_xor ^= value

    # Enumerate the smaller side of the selection/complement pair.
    if K <= N - K:
        R = K
        base = 0
    else:
        R = N - K
        base = total_xor

    if R == 0:
        print(base)
        return

    best = -1

    def dfs(start, depth, current_xor):
        nonlocal best

        if depth == R:
            candidate = base ^ current_xor
            if candidate > best:
                best = candidate
            return

        # Exactly R-depth positions still need to be selected.
        # i may be at most N - remaining so enough elements remain after i.
        remaining = R - depth
        last = N - remaining

        for i in range(start, last + 1):
            dfs(i + 1, depth + 1, current_xor ^ A[i])

    dfs(0, 0, 0)
    print(best)

if __name__ == "__main__":
    solve()