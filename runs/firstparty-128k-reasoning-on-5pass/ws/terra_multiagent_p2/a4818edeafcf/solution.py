import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = [0] + data[1:]

    prefix = [0] * (n + 1)
    seen = [False] * (n + 1)
    cnt = 0
    for i in range(1, n + 1):
        x = a[i]
        if not seen[x]:
            seen[x] = True
            cnt += 1
        prefix[i] = cnt

    suffix = [0] * (n + 2)
    seen = [False] * (n + 1)
    cnt = 0
    for i in range(n, 0, -1):
        x = a[i]
        if not seen[x]:
            seen[x] = True
            cnt += 1
        suffix[i] = cnt

    size = 4 * n + 5
    neg_inf = -10**9
    mx = [neg_inf] * size
    lazy = [0] * size

    def push(node):
        v = lazy[node]
        if v:
            left = node * 2
            right = left + 1
            mx[left] += v
            mx[right] += v
            lazy[left] += v
            lazy[right] += v
            lazy[node] = 0

    def point_set(node, left, right, pos, value):
        if left == right:
            mx[node] = value
            lazy[node] = 0
            return
        push(node)
        mid = (left + right) // 2
        if pos <= mid:
            point_set(node * 2, left, mid, pos, value)
        else:
            point_set(node * 2 + 1, mid + 1, right, pos, value)
        mx[node] = max(mx[node * 2], mx[node * 2 + 1])

    def range_add(node, left, right, ql, qr):
        if ql <= left and right <= qr:
            mx[node] += 1
            lazy[node] += 1
            return
        push(node)
        mid = (left + right) // 2
        if ql <= mid:
            range_add(node * 2, left, mid, ql, qr)
        if mid < qr:
            range_add(node * 2 + 1, mid + 1, right, ql, qr)
        mx[node] = max(mx[node * 2], mx[node * 2 + 1])

    last = [0] * (n + 1)
    answer = 0

    # Sweep the second cut j. The segment tree stores candidates for first cut i.
    for j in range(2, n):
        # First cut i = j - 1 becomes valid now.
        point_set(1, 1, n, j - 1, prefix[j - 1])

        x = a[j]
        previous = last[x]
        left = previous if previous > 0 else 1

        # A[j] is newly distinct in A[i+1..j] exactly when i >= previous.
        range_add(1, 1, n, left, j - 1)
        last[x] = j

        answer = max(answer, mx[1] + suffix[j + 1])

    print(answer)

if __name__ == "__main__":
    solve()