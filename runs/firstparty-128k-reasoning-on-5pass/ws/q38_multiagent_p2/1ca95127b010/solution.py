import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    X = int(data[1])
    Y = int(data[2])
    S = data[3]
    T = data[4]

    zero_s = S.count(b'0')
    zero_t = T.count(b'0')
    if zero_s != zero_t:
        sys.stdout.write("No\n")
        return

    one_s = N - zero_s

    # If no operation can ever be applied, the strings must already be equal.
    if X + Y > N or zero_s < X or one_s < Y:
        sys.stdout.write("Yes\n" if S == T else "No\n")
        return

    zero_res = []
    one_res = []
    zr_append = zero_res.append
    or_append = one_res.append

    ZERO = 48  # ord('0')

    for i, ch in enumerate(S, 1):
        if ch == ZERO:
            zr_append(i % Y)
        else:
            or_append(i % X)

    z = 0
    o = 0
    lz = len(zero_res)
    lo = len(one_res)

    for i, ch in enumerate(T, 1):
        if ch == ZERO:
            if z >= lz or zero_res[z] != i % Y:
                sys.stdout.write("No\n")
                return
            z += 1
        else:
            if o >= lo or one_res[o] != i % X:
                sys.stdout.write("No\n")
                return
            o += 1

    sys.stdout.write("Yes\n" if z == lz and o == lo else "No\n")


if __name__ == "__main__":
    solve()