import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = [0] + data[1:]

    pref = [0] * (n + 1)
    seen = [False] * (n + 1)
    cnt = 0
    for i in range(1, n + 1):
        x = a[i]
        if not seen[x]:
            seen[x] = True
            cnt += 1
        pref[i] = cnt

    suf = [0] * (n + 2)
    seen = [False] * (n + 1)
    cnt = 0
    for i in range(n, 0, -1):
        x = a[i]
        if not seen[x]:
            seen[x] = True
            cnt += 1
        suf[i] = cnt

    m = n - 1
    neg_inf = -10**15
    mx = [neg_inf] * (4 * (m + 1))
    lazy = [0] * (4 * (m + 1))

    def add(node, left, right, ql, qr):
        if ql <= left and right <= qr:
            mx[node] += 1
            lazy[node] += 1
            return

        mid = (left + right) >> 1
        z = lazy[node]
        if z:
            child = node << 1
            mx[child] += z
            lazy[child] += z
            child |= 1
            mx[child] += z
            lazy[child] += z
            lazy[node] = 0

        if ql <= mid:
            add(node << 1, left, mid, ql, qr)
        if mid < qr:
            add(node << 1 | 1, mid + 1, right, ql, qr)

        mx[node] = max(mx[node << 1], mx[node << 1 | 1])

    def activate(node, left, right, pos, value):
        if left == right:
            mx[node] = value
            lazy[node] = 0
            return

        mid = (left + right) >> 1
        z = lazy[node]
        if z:
            child = node << 1
            mx[child] += z
            lazy[child] += z
            child |= 1
            mx[child] += z
            lazy[child] += z
            lazy[node] = 0

        if pos <= mid:
            activate(node << 1, left, mid, pos, value)
        else:
            activate(node << 1 | 1, mid + 1, right, pos, value)

        mx[node] = max(mx[node << 1], mx[node << 1 | 1])

    last = [0] * (n + 1)
    last[a[1]] = 1
    answer = 0

    # j is the second cut: middle segment is A[i+1..j].
    for j in range(2, n):
        # Newly valid first cut i = j - 1 starts with only its prefix score.
        activate(1, 1, m, j - 1, pref[j - 1])

        previous = last[a[j]]
        left_bound = previous if previous > 0 else 1

        # A[j] is a new middle distinct value exactly when i >= previous.
        add(1, 1, m, left_bound, j - 1)

        last[a[j]] = j
        answer = max(answer, mx[1] + suf[j + 1])

    print(answer)

if __name__ == "__main__":
    solve()