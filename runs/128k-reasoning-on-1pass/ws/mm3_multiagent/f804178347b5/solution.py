import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    # join all remaining tokens to obtain the binary string
    s = b''.join(data[1:]).decode()
    L = len(s)                # = 3**N

    # leaf level: dp0[i] = flips to make this leaf 0, dp1[i] = flips to make it 1
    dp0 = [0] * L
    dp1 = [0] * L
    for i, ch in enumerate(s):
        if ch == '0':
            dp0[i] = 0
            dp1[i] = 1
        else:                # ch == '1'
            dp0[i] = 1
            dp1[i] = 0

    cur_len = L
    while cur_len > 1:
        new_len = cur_len // 3
        new_dp0 = [0] * new_len
        new_dp1 = [0] * new_len
        # combine triples of children
        for i in range(new_len):
            base = 3 * i
            a0, a1 = dp0[base],     dp1[base]
            b0, b1 = dp0[base + 1], dp1[base + 1]
            c0, c1 = dp0[base + 2], dp1[base + 2]

            # dp0: at least two children must become 0
            best0 = a0 + b0 + c0
            t = a0 + b0 + c1
            if t < best0: best0 = t
            t = a0 + b1 + c0
            if t < best0: best0 = t
            t = a1 + b0 + c0
            if t < best0: best0 = t
            new_dp0[i] = best0

            # dp1: at least two children must become 1
            best1 = a1 + b1 + c1
            t = a1 + b1 + c0
            if t < best1: best1 = t
            t = a1 + b0 + c1
            if t < best1: best1 = t
            t = a0 + b1 + c1
            if t < best1: best1 = t
            new_dp1[i] = best1

        dp0, dp1 = new_dp0, new_dp1
        cur_len = new_len

    root0, root1 = dp0[0], dp1[0]
    # original final bit is 0 iff root0 == 0
    if root0 == 0:
        ans = root1          # change it to 1
    else:
        ans = root0          # change it to 0
    print(ans)


if __name__ == "__main__":
    solve()