import sys

def main():
    input = sys.stdin.buffer.readline
    INF = 10**30

    N = int(input())
    W = list(map(int, input().split()))

    L = [0] * N
    R = [0] * N
    M = 2 * N

    min_by_r = [INF] * (M + 2)
    min_by_l = [INF] * (M + 2)

    for i in range(N):
        l, r = map(int, input().split())
        L[i] = l
        R[i] = r
        if W[i] < min_by_r[r]:
            min_by_r[r] = W[i]
        if W[i] < min_by_l[l]:
            min_by_l[l] = W[i]

    # left_min[x] = minimum weight among intervals with R < x
    left_min = [INF] * (M + 2)
    cur = INF
    for x in range(1, M + 2):
        if min_by_r[x - 1] < cur:
            cur = min_by_r[x - 1]
        left_min[x] = cur

    # right_min[x] = minimum weight among intervals with L > x
    right_min = [INF] * (M + 2)
    cur = INF
    for x in range(M, -1, -1):
        if min_by_l[x + 1] < cur:
            cur = min_by_l[x + 1]
        right_min[x] = cur

    Q = int(input())
    ans = []

    for _ in range(Q):
        s, t = map(int, input().split())
        s -= 1
        t -= 1

        base = W[s] + W[t]

        # Direct edge.
        if R[s] < L[t] or R[t] < L[s]:
            ans.append(str(base))
            continue

        best_internal = INF

        # One internal interval, left of both endpoints.
        best_internal = min(best_internal, left_min[min(L[s], L[t])])

        # One internal interval, right of both endpoints.
        best_internal = min(best_internal, right_min[max(R[s], R[t])])

        # Two internal intervals: left of s, then right of t.
        a = left_min[L[s]]
        b = right_min[R[t]]
        if a < INF and b < INF:
            best_internal = min(best_internal, a + b)

        # Two internal intervals: right of s, then left of t.
        a = right_min[R[s]]
        b = left_min[L[t]]
        if a < INF and b < INF:
            best_internal = min(best_internal, a + b)

        if best_internal == INF:
            ans.append("-1")
        else:
            ans.append(str(base + best_internal))

    print("\n".join(ans))

if __name__ == "__main__":
    main()