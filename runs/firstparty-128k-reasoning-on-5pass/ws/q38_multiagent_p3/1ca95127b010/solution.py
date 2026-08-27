import sys

ONE = 49  # ord('1')


def build_invariants(s, x, y):
    one_res = []
    zero_res = []
    one_bucket = [0] * y
    zero_bucket = [0] * x

    oi = 0
    zi = 0
    one_append = one_res.append
    zero_append = zero_res.append

    for pos, ch in enumerate(s):
        if ch == ONE:
            one_append(pos % x)
            one_bucket[oi % y] += pos // x
            oi += 1
        else:
            zero_append(pos % y)
            zero_bucket[zi % x] += pos // y
            zi += 1

    base = one_bucket[0]
    for i in range(y):
        one_bucket[i] -= base

    base = zero_bucket[0]
    for i in range(x):
        zero_bucket[i] -= base

    return one_res, zero_res, one_bucket, zero_bucket


def matches(s, x, y, one_res, zero_res, one_bucket_s, zero_bucket_s):
    one_bucket_t = [0] * y
    zero_bucket_t = [0] * x

    oi = 0
    zi = 0

    for pos, ch in enumerate(s):
        if ch == ONE:
            if pos % x != one_res[oi]:
                return False
            one_bucket_t[oi % y] += pos // x
            oi += 1
        else:
            if pos % y != zero_res[zi]:
                return False
            zero_bucket_t[zi % x] += pos // y
            zi += 1

    base = one_bucket_t[0]
    for i in range(y):
        one_bucket_t[i] -= base

    base = zero_bucket_t[0]
    for i in range(x):
        zero_bucket_t[i] -= base

    return one_bucket_t == one_bucket_s and zero_bucket_t == zero_bucket_s


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    X = int(data[1])
    Y = int(data[2])
    S = data[3]
    T = data[4]

    if S == T:
        print("Yes")
        return

    M = S.count(b'1')
    if M != T.count(b'1'):
        print("No")
        return

    Z = N - M

    if X + Y > N or M < Y or Z < X:
        print("No")
        return

    one_res, zero_res, one_bucket_s, zero_bucket_s = build_invariants(S, X, Y)

    if matches(T, X, Y, one_res, zero_res, one_bucket_s, zero_bucket_s):
        print("Yes")
    else:
        print("No")


if __name__ == "__main__":
    solve()