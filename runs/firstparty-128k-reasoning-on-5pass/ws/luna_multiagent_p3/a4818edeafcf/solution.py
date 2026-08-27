import sys

sys.setrecursionlimit(1_000_000)


def solve():
    input = sys.stdin.readline
    n = int(input())
    a = [0] + list(map(int, input().split()))

    # Prefix distinct counts.
    pref = [0] * (n + 1)
    seen = [False] * (n + 1)
    count = 0
    for i in range(1, n + 1):
        if not seen[a[i]]:
            seen[a[i]] = True
            count += 1
        pref[i] = count

    # Suffix distinct counts.
    suff = [0] * (n + 2)
    seen = [False] * (n + 1)
    count = 0
    for i in range(n, 0, -1):
        if not seen[a[i]]:
            seen[a[i]] = True
            count += 1
        suff[i] = count

    # next_pos[i] = next occurrence of a[i], or n+1 if none.
    next_pos = [n + 1] * (n + 1)
    last = [n + 1] * (n + 1)
    for i in range(n, 0, -1):
        next_pos[i] = last[a[i]]
        last[a[i]] = i

    # Segment tree stores:
    # F_i(j) = distinct(A[i+1..j]) + distinct(A[j+1..N])
    # Initially i = 0, for every j in [1, N-1].
    m = n - 1
    initial = [0] * (m + 1)
    for j in range(1, m + 1):
        initial[j] = pref[j] + suff[j + 1]

    size = 4 * (m + 2)
    tree = [0] * size
    lazy = [0] * size

    def build(node, left, right):
        if left == right:
            tree[node] = initial[left]
            return
        mid = (left + right) // 2
        build(node * 2, left, mid)
        build(node * 2 + 1, mid + 1, right)
        tree[node] = max(tree[node * 2], tree[node * 2 + 1])

    def push(node):
        value = lazy[node]
        if value:
            child = node * 2
            tree[child] += value
            lazy[child] += value
            tree[child + 1] += value
            lazy[child + 1] += value
            lazy[node] = 0

    def range_add(node, left, right, ql, qr, value):
        if ql <= left and right <= qr:
            tree[node] += value
            lazy[node] += value
            return

        push(node)
        mid = (left + right) // 2
        if ql <= mid:
            range_add(node * 2, left, mid, ql, qr, value)
        if mid < qr:
            range_add(node * 2 + 1, mid + 1, right, ql, qr, value)
        tree[node] = max(tree[node * 2], tree[node * 2 + 1])

    def range_max(node, left, right, ql, qr):
        if ql <= left and right <= qr:
            return tree[node]

        push(node)
        mid = (left + right) // 2
        result = -10**18
        if ql <= mid:
            result = range_max(node * 2, left, mid, ql, qr)
        if mid < qr:
            result = max(
                result,
                range_max(node * 2 + 1, mid + 1, right, ql, qr)
            )
        return result

    build(1, 1, m)

    answer = 0

    # Transform F_(i-1) into F_i by removing A_i from the middle segment.
    for i in range(1, n - 1):
        endpoint = min(next_pos[i] - 1, n - 1)
        range_add(1, 1, m, i, endpoint, -1)

        # Valid second cuts satisfy j >= i+1 and j <= n-1.
        best_middle_and_suffix = range_max(1, 1, m, i + 1, n - 1)
        answer = max(answer, pref[i] + best_middle_and_suffix)

    print(answer)


if __name__ == "__main__":
    solve()