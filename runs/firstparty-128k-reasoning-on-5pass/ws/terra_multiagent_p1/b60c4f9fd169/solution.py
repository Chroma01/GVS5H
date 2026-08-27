import sys


def solve():
    input = sys.stdin.buffer.readline
    K = int(input())
    S = input().strip()
    T = input().strip()

    n = len(S)
    m = len(T)

    if abs(n - m) > K:
        print("No")
        return

    # A diagonal is k = x - y, where x is consumed length of S
    # and y is consumed length of T.
    x = 0
    while x < n and x < m and S[x] == T[x]:
        x += 1

    if x == n and x == m:
        print("Yes")
        return

    prev = {0: x}

    for d in range(1, K + 1):
        cur = {}

        for k in range(-d, d + 1):
            best = -1

            # Delete one character from S:
            # (x, y) on diagonal k-1 -> (x+1, y) on diagonal k.
            px = prev.get(k - 1, -1)
            if px >= 0 and px < n:
                best = px + 1

            # Insert one character into S / consume one from T:
            # (x, y) on diagonal k+1 -> (x, y+1) on diagonal k.
            px = prev.get(k + 1, -1)
            if px >= 0:
                py = px - (k + 1)
                if py < m and px > best:
                    best = px

            # Replace one character:
            # (x, y) remains on the same diagonal.
            px = prev.get(k, -1)
            if px >= 0:
                py = px - k
                if px < n and py < m and px + 1 > best:
                    best = px + 1

            if best < 0:
                continue

            y = best - k

            # Greedily extend through all following equal characters.
            while best < n and y < m and S[best] == T[y]:
                best += 1
                y += 1

            cur[k] = best

            if best == n and y == m:
                print("Yes")
                return

        prev = cur

    print("No")


if __name__ == "__main__":
    solve()