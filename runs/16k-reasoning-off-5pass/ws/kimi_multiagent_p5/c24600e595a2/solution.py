import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    B = list(map(int, data[1 + n:1 + 2 * n]))
    C = list(map(int, data[1 + 2 * n:1 + 3 * n]))

    S = 0
    rem = []  # 1 -> 0 flips
    add = []  # 0 -> 1 flips
    for a, b, c in zip(A, B, C):
        if a == 1:
            S += c
        if a != b:
            if a == 1:
                rem.append(c)
            else:
                add.append(c)

    rem.sort(reverse=True)
    add.sort()

    ans = 0
    for c in rem:
        S -= c
        ans += S
    for c in add:
        S += c
        ans += S

    print(ans)

solve()