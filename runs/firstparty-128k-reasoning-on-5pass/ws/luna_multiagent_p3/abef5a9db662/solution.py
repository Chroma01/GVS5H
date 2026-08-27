import sys

MAX_X = 500000

data = iter(map(int, sys.stdin.buffer.read().split()))
n = next(data)

mx = [0] * (4 * MAX_X + 5)
lazy = [0] * (4 * MAX_X + 5)


def build(node, left, right):
    if left == right:
        mx[node] = left
        return
    mid = (left + right) // 2
    build(node * 2, left, mid)
    build(node * 2 + 1, mid + 1, right)
    mx[node] = right


def push(node):
    value = lazy[node]
    if value:
        left_child = node * 2
        right_child = left_child + 1
        mx[left_child] += value
        lazy[left_child] += value
        mx[right_child] += value
        lazy[right_child] += value
        lazy[node] = 0


def add(node, left, right, ql, qr):
    if ql <= left and right <= qr:
        mx[node] += 1
        lazy[node] += 1
        return

    push(node)
    mid = (left + right) // 2
    if ql <= mid:
        add(node * 2, left, mid, ql, qr)
    if qr > mid:
        add(node * 2 + 1, mid + 1, right, ql, qr)
    mx[node] = max(mx[node * 2], mx[node * 2 + 1])


def first_at_least(node, left, right, value):
    if mx[node] < value:
        return MAX_X + 1
    if left == right:
        return left

    push(node)
    mid = (left + right) // 2
    if mx[node * 2] >= value:
        return first_at_least(node * 2, left, mid, value)
    return first_at_least(node * 2 + 1, mid + 1, right, value)


def get(node, left, right, pos):
    if left == right:
        return mx[node]

    push(node)
    mid = (left + right) // 2
    if pos <= mid:
        return get(node * 2, left, mid, pos)
    return get(node * 2 + 1, mid + 1, right, pos)


build(1, 1, MAX_X)

for _ in range(n):
    low = next(data)
    high = next(data)

    start = first_at_least(1, 1, MAX_X, low)
    end = first_at_least(1, 1, MAX_X, high + 1)

    if start < end:
        add(1, 1, MAX_X, start, end - 1)

q = next(data)
answers = []
for _ in range(q):
    x = next(data)
    answers.append(str(get(1, 1, MAX_X, x)))

sys.stdout.write("\n".join(answers))