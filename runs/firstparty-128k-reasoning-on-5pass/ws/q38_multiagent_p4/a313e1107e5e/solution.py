import sys
from bisect import bisect_left, bisect_right

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    q = data[1]

    a_start = 2
    p = a_start + n

    queries_by_r = [[] for _ in range(n + 1)]
    for idx in range(q):
        r = data[p]
        x = data[p + 1]
        p += 2
        queries_by_r[r].append((x, idx))

    ans = [0] * q
    tails = []

    bl = bisect_left
    br = bisect_right

    for i in range(1, n + 1):
        x = data[a_start + i - 1]

        pos = bl(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x

        if queries_by_r[i]:
            for xq, idx in queries_by_r[i]:
                ans[idx] = br(tails, xq)

    sys.stdout.write("\n".join(map(str, ans)))

if __name__ == "__main__":
    main()