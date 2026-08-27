import sys
from bisect import bisect_left, bisect_right

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    Q = data[1]
    A = data[2:2 + N]

    queries_by_r = [[] for _ in range(N + 1)]
    pos = 2 + N
    for idx in range(Q):
        R = data[pos]
        X = data[pos + 1]
        pos += 2
        queries_by_r[R].append((X, idx))

    del data

    ans = [0] * Q
    tails = []

    for i, v in enumerate(A, 1):
        p = bisect_left(tails, v)
        if p == len(tails):
            tails.append(v)
        else:
            tails[p] = v

        if queries_by_r[i]:
            for x, idx in queries_by_r[i]:
                ans[idx] = bisect_right(tails, x)

    sys.stdout.write("\n".join(map(str, ans)))

if __name__ == "__main__":
    main()