import sys


class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.mx = [-10**15] * (4 * n + 5)
        self.lazy = [0] * (4 * n + 5)

    def _push(self, node):
        value = self.lazy[node]
        if value:
            left = node * 2
            right = left + 1
            self.mx[left] += value
            self.lazy[left] += value
            self.mx[right] += value
            self.lazy[right] += value
            self.lazy[node] = 0

    def add(self, ql, qr, value, node=1, left=1, right=None):
        if right is None:
            right = self.n

        if ql > right or qr < left:
            return

        if ql <= left and right <= qr:
            self.mx[node] += value
            self.lazy[node] += value
            return

        self._push(node)
        mid = (left + right) // 2
        self.add(ql, qr, value, node * 2, left, mid)
        self.add(ql, qr, value, node * 2 + 1, mid + 1, right)
        self.mx[node] = max(self.mx[node * 2], self.mx[node * 2 + 1])

    def set_value(self, index, value, node=1, left=1, right=None):
        if right is None:
            right = self.n

        if left == right:
            self.mx[node] = value
            self.lazy[node] = 0
            return

        self._push(node)
        mid = (left + right) // 2
        if index <= mid:
            self.set_value(index, value, node * 2, left, mid)
        else:
            self.set_value(index, value, node * 2 + 1, mid + 1, right)

        self.mx[node] = max(self.mx[node * 2], self.mx[node * 2 + 1])

    def maximum(self):
        return self.mx[1]


def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    prefix = [0] * (n + 1)
    seen = [False] * (n + 1)
    distinct = 0

    for i in range(1, n + 1):
        x = a[i - 1]
        if not seen[x]:
            seen[x] = True
            distinct += 1
        prefix[i] = distinct

    suffix = [0] * (n + 2)
    seen = [False] * (n + 1)
    distinct = 0

    for i in range(n, 0, -1):
        x = a[i - 1]
        if not seen[x]:
            seen[x] = True
            distinct += 1
        suffix[i] = distinct

    tree = SegmentTree(n)

    # A[1] is already present before the sweep starts.
    last = [0] * (n + 1)
    last[a[0]] = 1

    answer = 0

    for j in range(2, n):
        x = a[j - 1]
        previous = last[x]

        # For cuts i >= previous, A[j] is new in A[i+1..j].
        left = max(1, previous)
        right = j - 2
        if left <= right:
            tree.add(left, right, 1)

        last[x] = j

        # Activate the new first cut i = j-1.
        first_cut = j - 1
        tree.set_value(first_cut, prefix[first_cut] + 1)

        answer = max(answer, tree.maximum() + suffix[j + 1])

    print(answer)


if __name__ == "__main__":
    solve()