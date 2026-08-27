import sys

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N = data[0]
    A = data[1:1 + N]
    B = data[1 + N:1 + 2 * N]
    C = data[1 + 2 * N:1 + 3 * N]

    # Values that need to be removed (1 -> 0) and added (0 -> 1)
    remove = []   # S1: positions where A_i = 1, B_i = 0
    add = []      # S0: positions where A_i = 0, B_i = 1

    # Initial weight = sum of C_i for all positions where A_i = 1
    w0 = 0
    for a, b, c in zip(A, B, C):
        if a == 1:
            w0 += c
        if a == 0 and b == 1:
            add.append(c)
        elif a == 1 and b == 0:
            remove.append(c)

    # Optimal order: removals descending, additions ascending
    remove.sort(reverse=True)
    add.sort()

    cur = w0
    total = 0

    # All removals first
    for c in remove:
        total += cur - c   # weight after the removal
        cur -= c

    # Then all additions
    for c in add:
        total += cur + c   # weight after the addition
        cur += c

    print(total)


if __name__ == "__main__":
    solve()