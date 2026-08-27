import sys
import os
import random


def fast_answers(a):
    n = len(a)

    # Maximum Cartesian tree.
    # Equal values are kept in their original left-to-right order:
    # an earlier equal value is an ancestor of a later equal value.
    parent = [-1] * n
    stack = []

    for i, x in enumerate(a):
        last = -1
        while stack and a[stack[-1]] < x:
            last = stack.pop()

        if stack:
            parent[i] = stack[-1]

        if last != -1:
            parent[last] = i

        stack.append(i)

    root = stack[0]

    children = [[] for _ in range(n)]
    for v in range(n):
        if parent[v] != -1:
            children[parent[v]].append(v)

    # Iterative tree traversal, then calculate subtree sums bottom-up.
    order = [root]
    for v in order:
        order.extend(children[v])

    subtree_sum = a[:]
    for v in reversed(order):
        p = parent[v]
        if p != -1:
            subtree_sum[p] += subtree_sum[v]

    # good[v] is the final size if Takahashi has already absorbed
    # the entire Cartesian subtree rooted at v.
    good = [0] * n
    good[root] = subtree_sum[root]

    for v in order:
        for ch in children[v]:
            if subtree_sum[ch] > a[v]:
                good[ch] = good[v]
            else:
                good[ch] = subtree_sum[ch]

    ans = [0] * n
    for i in range(n):
        # A slime can initially absorb its complete Cartesian subtree iff it
        # has an adjacent strictly smaller slime. Otherwise it cannot move.
        active = (
            (i > 0 and a[i - 1] < a[i]) or
            (i + 1 < n and a[i + 1] < a[i])
        )
        ans[i] = good[i] if active else a[i]

    return ans


def brute_answers(a):
    n = len(a)
    ans = []

    for start in range(n):
        best = a[start]
        seen = set()
        stack = [(start, start, a[start])]

        while stack:
            l, r, cur = stack.pop()
            state = (l, r)
            if state in seen:
                continue
            seen.add(state)

            if cur > best:
                best = cur

            if l > 0 and a[l - 1] < cur:
                stack.append((l - 1, r, cur + a[l - 1]))
            if r + 1 < n and a[r + 1] < cur:
                stack.append((l, r + 1, cur + a[r + 1]))

        ans.append(best)

    return ans


def validate():
    for n in range(2, 10):
        for _ in range(3000):
            a = [random.randint(1, 10) for _ in range(n)]
            got = fast_answers(a)
            expected = brute_answers(a)
            if got != expected:
                print("Mismatch", file=sys.stderr)
                print(a, file=sys.stderr)
                print(got, file=sys.stderr)
                print(expected, file=sys.stderr)
                raise AssertionError


def solve():
    input = sys.stdin.buffer.readline
    n = int(input())
    a = list(map(int, input().split()))
    print(*fast_answers(a))


if __name__ == "__main__":
    if os.environ.get("VALIDATE"):
        validate()
    else:
        solve()