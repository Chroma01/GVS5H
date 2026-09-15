import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    del data

    # Max Cartesian tree.
    # Equal values are not popped, so the earlier equal value becomes the ancestor.
    left = [-1] * n
    right = [-1] * n
    limit = [-1] * n  # parent value; -1 means root

    st = []
    append = st.append
    pop = st.pop

    for i, x in enumerate(A):
        last = -1
        while st and A[st[-1]] < x:
            last = pop()

        if st:
            p = st[-1]
            right[p] = i
            limit[i] = A[p]

        if last != -1:
            left[i] = last
            limit[last] = x

        append(i)

    root = st[0] if st else 0

    # Parent-before-children order, then process reversed.
    order = [root]
    idx = 0
    while idx < len(order):
        v = order[idx]
        idx += 1
        l = left[v]
        if l != -1:
            order.append(l)
        r = right[v]
        if r != -1:
            order.append(r)

    subsum = [0] * n

    # Linked lists of active positions.
    head = [-1] * n
    tail = [-1] * n
    nxt = [-1] * n

    ans = A[:]

    # Local bindings for speed.
    A_loc = A
    left_loc = left
    right_loc = right
    limit_loc = limit
    sub_loc = subsum
    head_loc = head
    tail_loc = tail
    nxt_loc = nxt
    ans_loc = ans

    for v in reversed(order):
        av = A_loc[v]
        l = left_loc[v]
        r = right_loc[v]

        s = av
        hv = -1
        tv = -1

        # Merge left child's active list if it can climb into v.
        if l != -1:
            sl = sub_loc[l]
            s += sl
            if sl > av:
                hv = head_loc[l]
                if hv != -1:
                    tv = tail_loc[l]
                else:
                    tv = -1

        # Merge right child's active list if it can climb into v.
        if r != -1:
            sr = sub_loc[r]
            s += sr
            if sr > av:
                hr = head_loc[r]
                if hr != -1:
                    if hv == -1:
                        hv = hr
                        tv = tail_loc[r]
                    else:
                        nxt_loc[tv] = hr
                        tv = tail_loc[r]

        # v itself is active iff it can make a first move inside its subtree.
        # If it has a child, the adjacent slime inside that child is v-1 or v+1.
        if l == -1 and r == -1:
            if hv == -1:
                hv = v
                tv = v
            else:
                nxt_loc[tv] = v
                tv = v
        elif (l != -1 and A_loc[v - 1] < av) or (r != -1 and A_loc[v + 1] < av):
            if hv == -1:
                hv = v
                tv = v
            else:
                nxt_loc[tv] = v
                tv = v

        sub_loc[v] = s

        # If v cannot climb to its parent, active positions stop here.
        lim = limit_loc[v]
        if lim == -1 or s <= lim:
            cur = hv
            while cur != -1:
                ans_loc[cur] = s
                cur = nxt_loc[cur]
            head_loc[v] = -1
            tail_loc[v] = -1
        else:
            head_loc[v] = hv
            tail_loc[v] = tv

    # Free large structures before constructing the output string.
    del A, left, right, limit, subsum, head, tail, nxt, order
    del A_loc, left_loc, right_loc, limit_loc, sub_loc, head_loc, tail_loc, nxt_loc, ans

    sys.stdout.write(" ".join(map(str, ans_loc)))


if __name__ == "__main__":
    solve()