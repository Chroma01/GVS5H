import sys

sys.setrecursionlimit(1_000_000)

data = list(map(int, sys.stdin.buffer.read().split()))
it = iter(data)

N = next(it)
contests = [(next(it), next(it)) for _ in range(N)]
Q = next(it)

M = 500_000
mx = [0] * (4 * M)
lazy = [0] * (4 * M)


def build(node, left, right):
    if right - left == 1:
        mx[node] = right
        return
    mid = (left + right) // 2
    build(node * 2, left, mid)
    build(node * 2 + 1, mid, right)
    mx[node] = mx[node * 2 + 1]


def apply(node, value):
    mx[node] += value
    lazy[node] += value


def push(node):
    value = lazy[node]
    if value:
        apply(node * 2, value)
        apply(node * 2 + 1, value)
        lazy[node] = 0


def range_add(node, left, right, ql, qr):
    if qr <= left or right <= ql:
        return
    if ql <= left and right <= qr:
        apply(node, 1)
        return

    push(node)
    mid = (left + right) // 2
    range_add(node * 2, left, mid, ql, qr)
    range_add(node * 2 + 1, mid, right, ql, qr)
    mx[node] = max(mx[node * 2], mx[node * 2 + 1])


def first_at_least(node, left, right, target):
    if mx[node] < target:
        return M
    if right - left == 1:
        return left

    push(node)
    mid = (left + right) // 2
    result = first_at_least(node * 2, left, mid, target)
    if result != M:
        return result
    return first_at_least(node * 2 + 1, mid, right, target)


def point_get(node, left, right, index):
    if right - left == 1:
        return mx[node]

    push(node)
    mid = (left + right) // 2
    if index < mid:
        return point_get(node * 2, left, mid, index)
    return point_get(node * 2 + 1, mid, right, index)


build(1, 0, M)

for L, R in contests:
    start = first_at_least(1, 0, M, L)
    end = first_at_least(1, 0, M, R + 1)
    if start < end:
        range_add(1, 0, M, start, end)

answers = []
for _ in range(Q):
    x = next(it)
    answers.append(str(point_get(1, 0, M, x - 1)))

sys.stdout.write("\n".join(answers))