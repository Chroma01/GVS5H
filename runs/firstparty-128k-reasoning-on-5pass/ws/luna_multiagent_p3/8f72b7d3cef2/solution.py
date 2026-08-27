import sys
from array import array


def solve():
    input = sys.stdin.buffer.readline
    n = int(input())
    a = list(map(int, input().split()))

    nxt = [-1] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and a[stack[-1]] < a[i]:
            stack.pop()
        if stack:
            nxt[i] = stack[-1]
        stack.append(i)

    prv = [-1] * n
    stack.clear()
    for i in range(n):
        while stack and a[stack[-1]] < a[i]:
            stack.pop()
        if stack:
            prv[i] = stack[-1]
        stack.append(i)

    levels = n.bit_length()
    rjump = [array("i", nxt)]
    ljump = [array("i", prv)]
    del nxt, prv

    for _ in range(1, levels):
        old_r = rjump[-1]
        old_l = ljump[-1]
        cur_r = array("i", [-1]) * n
        cur_l = array("i", [-1]) * n

        for i in range(n):
            q = old_r[i]
            if q >= 0:
                cur_r[i] = old_r[q]

            q = old_l[i]
            if q >= 0:
                cur_l[i] = old_l[q]

        rjump.append(cur_r)
        ljump.append(cur_l)

    pref = [0] * (n + 1)
    total = 0
    for i, x in enumerate(a):
        total += x
        pref[i + 1] = total

    def first_at_least(pos, value):
        if pos >= n:
            return n
        if a[pos] >= value:
            return pos

        cur = pos
        for k in range(levels - 1, -1, -1):
            q = rjump[k][cur]
            if q >= 0 and a[q] < value:
                cur = q

        q = rjump[0][cur]
        return n if q < 0 else q

    def last_at_least(pos, value):
        if pos < 0:
            return -1
        if a[pos] >= value:
            return pos

        cur = pos
        for k in range(levels - 1, -1, -1):
            q = ljump[k][cur]
            if q >= 0 and a[q] < value:
                cur = q

        q = ljump[0][cur]
        return -1 if q < 0 else q

    ans = [0] * n

    for start in range(n):
        left = start
        right = start
        size = a[start]

        while True:
            changed = False

            if left > 0:
                blocker = last_at_least(left - 1, size)
                if blocker < left - 1:
                    size += pref[left] - pref[blocker + 1]
                    left = blocker + 1
                    changed = True

            if right + 1 < n:
                blocker = first_at_least(right + 1, size)
                if blocker > right + 1:
                    size += pref[blocker] - pref[right + 1]
                    right = blocker - 1
                    changed = True

            if not changed:
                break

        ans[start] = size

    sys.stdout.write(" ".join(map(str, ans)))


if __name__ == "__main__":
    solve()