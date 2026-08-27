import sys


def solve():
    input = sys.stdin.buffer.readline
    N, M = map(int, input().split())

    L = [0] * M
    R = [0] * M
    for i in range(M):
        L[i], R[i] = map(int, input().split())

    ans = [0] * M

    def output(cost):
        sys.stdout.write(str(cost) + "\n")
        sys.stdout.write(" ".join(map(str, ans)) + "\n")
        raise SystemExit

    # Cost 1: one interval covers the whole domain.
    for i in range(M):
        if L[i] == 1 and R[i] == N:
            ans[i] = 1
            output(1)

    order_l = sorted(range(M), key=lambda i: L[i])

    # Cost 2: two Operation-2 intervals whose original intervals are disjoint.
    min_r = N + 1
    min_id = -1
    for i in order_l:
        if L[i] > min_r:
            ans[min_id] = 2
            ans[i] = 2
            output(2)
        if R[i] < min_r:
            min_r = R[i]
            min_id = i

    # Cost 2: Operation-2 on an interval and Operation-1 on a distinct
    # interval containing it.
    pos = 0
    best1_r = -1
    best1_id = -1
    best2_r = -1
    best2_id = -1

    while pos < M:
        q = pos
        cur_l = L[order_l[pos]]
        while q < M and L[order_l[q]] == cur_l:
            q += 1

        # Containers with strictly smaller left endpoint.
        for k in range(pos, q):
            i = order_l[k]
            if best1_id != -1 and best1_r >= R[i]:
                ans[i] = 2
                ans[best1_id] = 1
                output(2)

        # Insert this equal-left group, retaining the two largest right ends.
        for k in range(pos, q):
            i = order_l[k]
            if R[i] > best1_r:
                best2_r, best2_id = best1_r, best1_id
                best1_r, best1_id = R[i], i
            elif R[i] > best2_r:
                best2_r, best2_id = R[i], i

        # Containers with equal left endpoint require a different ID.
        for k in range(pos, q):
            i = order_l[k]
            if best1_id != i:
                container_r, container_id = best1_r, best1_id
            else:
                container_r, container_id = best2_r, best2_id

            if container_id != -1 and container_r >= R[i]:
                ans[i] = 2
                ans[container_id] = 1
                output(2)

        pos = q

    # Cost 2: two Operation-1 intervals cover [1, N].
    left_id = -1
    left_r = -1
    right_id = -1
    right_l = N + 1

    for i in range(M):
        if L[i] == 1 and R[i] > left_r:
            left_r = R[i]
            left_id = i
        if R[i] == N and L[i] < right_l:
            right_l = L[i]
            right_id = i

    if left_id != -1 and right_id != -1:
        if left_id != right_id and left_r + 1 >= right_l:
            ans[left_id] = 1
            ans[right_id] = 1
            output(2)

    # Cost 3:
    # Operation-1 on c and Operation-2 on a,b is sufficient when
    # L[a] >= L[c] and R[b] <= R[c].
    #
    # It is enough to try three globally greatest left-endpoint IDs and
    # three globally smallest right-endpoint IDs.  Replacing a candidate by
    # a more extreme endpoint preserves these inequalities; three choices
    # handle excluding c and the other selected Operation-2 ID.
    top_left = order_l[-min(3, M):]
    order_r = sorted(range(M), key=lambda i: R[i])
    top_right = order_r[:min(3, M)]

    for c in range(M):
        for a in top_left:
            if a == c:
                continue
            # top_left guarantees L[a] >= L[c].
            for b in top_right:
                if b == c or b == a:
                    continue
                # top_right guarantees R[b] <= R[c].
                ans[a] = 2
                ans[b] = 2
                ans[c] = 1
                output(3)

    sys.stdout.write("-1\n")


if __name__ == "__main__":
    solve()