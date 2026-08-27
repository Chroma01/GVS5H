import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] + [int(x) for x in data[1:1 + n]]  # 1-indexed

    # prefix sums
    P = [0] * (n + 1)
    for i in range(1, n + 1):
        P[i] = P[i - 1] + A[i]

    # ---------- compute L[i]: leftmost index of the block ending at i ----------
    # Stack of blocks. Each block: [left, right, sum, need]
    #   need = minimal initial size required to fully absorb this block entering from the right.
    # Blocks on the stack have strictly increasing sums.
    L = [0] * (n + 1)
    st = []  # each entry: [l, r, s, need]
    for i in range(1, n + 1):
        cur_l = i
        cur_s = A[i]
        # absorb blocks to the left while our running sum exceeds their requirement
        while st and cur_s >= st[-1][3]:
            b = st.pop()
            cur_l = b[0]
            cur_s = P[i] - P[cur_l - 1]
        L[i] = cur_l
        # compute need for the new block [cur_l, i]:
        # to absorb it from the right, you must first beat the element just left of it (if any),
        # then recursively beat the inner blocks.
        if cur_l == 1:
            need = 1  # no left neighbor; any positive size absorbs everything eventually
        else:
            need = A[cur_l - 1] + 1
        st.append([cur_l, i, cur_s, need])

    # ---------- compute R[i]: rightmost index of the block starting at i ----------
    R = [0] * (n + 1)
    st = []
    for i in range(n, 0, -1):
        cur_r = i
        cur_s = A[i]
        while st and cur_s >= st[-1][3]:
            b = st.pop()
            cur_r = b[1]
            cur_s = P[cur_r] - P[i - 1]
        R[i] = cur_r
        if cur_r == n:
            need = 1
        else:
            need = A[cur_r + 1] + 1
        st.append([i, cur_r, cur_s, need])

    # ---------- answer each k by simulating with jumps ----------
    out = []
    for k in range(1, n + 1):
        l = k
        r = k
        s = A[k]
        changed = True
        while changed:
            changed = False
            while l > 1 and A[l - 1] < s:
                l = L[l - 1]
                s = P[r] - P[l - 1]
                changed = True
            while r < n and A[r + 1] < s:
                r = R[r + 1]
                s = P[r] - P[l - 1]
                changed = True
        out.append(str(s))

    sys.stdout.write(' '.join(out) + '\n')

main()