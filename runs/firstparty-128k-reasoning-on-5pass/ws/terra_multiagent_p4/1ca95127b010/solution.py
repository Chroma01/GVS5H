import sys
from array import array


def normal_form(s, x, y):
    # Nodes 0 and 1 are head and tail sentinels.
    prv = array('i', [-1, 0])
    nxt = array('i', [1, -1])
    bit = bytearray([2, 2])
    length = array('i', [0, 0])

    last = 0
    i = 0
    n = len(s)

    while i < n:
        b = 1 if s[i] == '1' else 0
        j = i + 1
        while j < n and s[j] == s[i]:
            j += 1

        v = len(length)
        length.append(j - i)
        bit.append(b)
        prv.append(last)
        nxt.append(1)
        nxt[last] = v
        prv[1] = v
        last = v
        i = j

    def reducible(a):
        b = nxt[a]
        return (
            a != 0
            and a != 1
            and b != 1
            and b != -1
            and bit[a] == 1
            and bit[b] == 0
            and length[a] >= y
            and length[b] >= x
        )

    todo = []
    v = nxt[0]
    while v != 1:
        if reducible(v):
            todo.append(v)
        v = nxt[v]

    def insert_before(right, b, ln):
        left = prv[right]

        if left != 0 and bit[left] == b:
            length[left] += ln
            return left

        v = len(length)
        length.append(ln)
        bit.append(b)
        prv.append(left)
        nxt.append(right)
        nxt[left] = v
        prv[right] = v
        return v

    while todo:
        a = todo.pop()

        if not reducible(a):
            continue

        b = nxt[a]

        p = length[a] // y
        q = length[b] // x
        one_rem = length[a] % y
        zero_rem = length[b] % x

        left = prv[a]
        right = nxt[b]

        # 1^(pY+r) 0^(qX+s) -> 1^r 0^(qX) 1^(pY) 0^s
        nxt[left] = right
        prv[right] = left
        prv[a] = nxt[a] = -1
        prv[b] = nxt[b] = -1

        if one_rem:
            insert_before(right, 1, one_rem)
        insert_before(right, 0, q * x)
        insert_before(right, 1, p * y)
        if zero_rem:
            insert_before(right, 0, zero_rem)

        mid = prv[right]
        if right != 1 and mid != 0 and bit[mid] == bit[right]:
            length[mid] += length[right]
            rr = nxt[right]
            nxt[mid] = rr
            prv[rr] = mid
            prv[right] = nxt[right] = -1

        cur = prv[left] if left != 0 else 0
        for _ in range(14):
            if cur == 1:
                break
            if reducible(cur):
                todo.append(cur)
            cur = nxt[cur]

    out = []
    v = nxt[0]
    while v != 1:
        out.append(('1' if bit[v] else '0') * length[v])
        v = nxt[v]

    return ''.join(out)


def solve():
    input = sys.stdin.readline

    n, x, y = map(int, input().split())
    s = input().strip()
    t = input().strip()

    if x + y > n:
        print("Yes" if s == t else "No")
        return

    print("Yes" if normal_form(s, x, y) == normal_form(t, x, y) else "No")


if __name__ == "__main__":
    solve()