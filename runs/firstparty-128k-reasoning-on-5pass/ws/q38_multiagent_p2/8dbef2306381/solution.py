import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, A, B = data[0], data[1], data[2], data[3]

    intervals = []
    idx = 4
    for _ in range(M):
        L = data[idx]
        R = data[idx + 1]
        idx += 2
        if intervals and L <= intervals[-1][1] + 1:
            if R > intervals[-1][1]:
                intervals[-1] = (intervals[-1][0], R)
        else:
            intervals.append((L, R))

    for L, R in intervals:
        if R - L + 1 >= B:
            print("No")
            return

    mask = (1 << B) - 1

    if A < B:
        G = ((1 << (B - A + 1)) - 1) << (A - 1)
        if A == 1:
            k = 0
        else:
            k = (A - 1 + (B - A) - 1) // (B - A)
        K = B + A * k
    else:
        G = 0
        K = 0

    s = 1
    cur = 1

    def good_gap(length):
        nonlocal s
        if length <= 0 or s == 0 or s == mask:
            return

        if A == B:
            r = length % B
            if r:
                s = ((s << r) | (s >> (B - r))) & mask
        else:
            if length >= K:
                s = mask
            else:
                ss = s
                gg = G
                mm = mask
                for _ in range(length):
                    ss = ((ss << 1) | (1 if ss & gg else 0)) & mm
                s = ss

    for L, R in intervals:
        good_gap(L - 1 - cur)
        if s == 0:
            print("No")
            return

        s = (s << (R - L + 1)) & mask
        cur = R

        if s == 0:
            print("No")
            return

    good_gap(N - cur)
    print("Yes" if (s & 1) else "No")

if __name__ == "__main__":
    solve()