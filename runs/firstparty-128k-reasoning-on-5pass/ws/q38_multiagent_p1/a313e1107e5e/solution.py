import sys
from bisect import bisect_left, bisect_right


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, Q = data[0], data[1]
    A = data[2:2 + N]

    queries = []
    p = 2 + N
    for idx in range(Q):
        R = data[p]
        X = data[p + 1]
        p += 2
        queries.append((R, X, idx))

    del data

    queries.sort(key=lambda t: t[0])

    ans = [0] * Q
    tails = []
    ptr = 0

    bl = bisect_left
    br = bisect_right

    for i, x in enumerate(A, 1):
        pos = bl(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x

        while ptr < Q and queries[ptr][0] == i:
            _, X, idx = queries[ptr]
            ans[idx] = br(tails, X)
            ptr += 1

    sys.stdout.write("\n".join(map(str, ans)))


if __name__ == "__main__":
    main()