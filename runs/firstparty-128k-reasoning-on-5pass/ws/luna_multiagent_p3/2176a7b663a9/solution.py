import sys


def solve():
    input = sys.stdin.buffer.readline

    n = int(input())
    w = [0] + list(map(int, input().split()))

    L = [0] * (n + 1)
    R = [0] * (n + 1)
    max_coord = 2 * n

    for i in range(1, n + 1):
        L[i], R[i] = map(int, input().split())

    inf = 10**30

    best_end = [inf] * (max_coord + 2)
    best_start = [inf] * (max_coord + 2)

    for i in range(1, n + 1):
        if w[i] < best_end[R[i]]:
            best_end[R[i]] = w[i]
        if w[i] < best_start[L[i]]:
            best_start[L[i]] = w[i]

    for x in range(1, max_coord + 2):
        if best_end[x - 1] < best_end[x]:
            best_end[x] = best_end[x - 1]

    for x in range(max_coord, 0, -1):
        if best_start[x + 1] < best_start[x]:
            best_start[x] = best_start[x + 1]

    q = int(input())
    ans = []

    for _ in range(q):
        s, t = map(int, input().split())

        ls, rs = L[s], R[s]
        lt, rt = L[t], R[t]

        # Disjoint intervals are adjacent, hence this is always optimal.
        if rs < lt or rt < ls:
            ans.append(str(w[s] + w[t]))
            continue

        # The two queried intervals overlap.
        base = w[s] + w[t]
        best = inf

        # One intermediate vertex disjoint from both.
        x = best_end[min(ls, lt) - 1]
        if x < inf:
            best = min(best, base + x)

        x = best_start[max(rs, rt) + 1]
        if x < inf:
            best = min(best, base + x)

        # Two intermediate vertices on the outer sides.
        left_s = best_end[ls - 1]
        right_s = best_start[rs + 1]
        left_t = best_end[lt - 1]
        right_t = best_start[rt + 1]

        if left_s < inf and right_t < inf:
            best = min(best, base + left_s + right_t)
        if right_s < inf and left_t < inf:
            best = min(best, base + right_s + left_t)

        ans.append(str(best if best < inf else -1))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    solve()