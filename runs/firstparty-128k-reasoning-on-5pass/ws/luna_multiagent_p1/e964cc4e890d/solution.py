import sys

MOD = 998244353
PRIMITIVE_ROOT = 3


def ntt(a, invert):
    n = len(a)

    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        wlen = pow(PRIMITIVE_ROOT, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)

        half = length >> 1
        for start in range(0, n, length):
            w = 1
            for i in range(start, start + half):
                u = a[i]
                v = a[i + half] * w % MOD
                a[i] = (u + v) % MOD
                a[i + half] = (u - v) % MOD
                w = w * wlen % MOD

        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD


def convolution(a, b):
    if not a or not b:
        return []

    result_len = len(a) + len(b) - 1

    if min(len(a), len(b)) <= 32:
        result = [0] * result_len
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    result[i + j] = (result[i + j] + x * y) % MOD
        return result

    size = 1
    while size < result_len:
        size <<= 1

    fa = a + [0] * (size - len(a))
    fb = b + [0] * (size - len(b))

    ntt(fa, False)
    ntt(fb, False)

    for i in range(size):
        fa[i] = fa[i] * fb[i] % MOD

    ntt(fa, True)
    return fa[:result_len]


def solve():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()

    if s[0] == "W":
        print(0)
        return

    length = 2 * n

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (n + 1)
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    black_positions = []
    white_prefix = [0] * (length + 1)
    white_count = 0

    for pos, ch in enumerate(s, 1):
        if ch == "W":
            white_count += 1
        else:
            black_positions.append(pos)
        white_prefix[pos] = white_count

    # Event j: immediately before the (j+1)-th black vertex,
    # all of the first j black vertices are matched to white vertices
    # lying to its left.
    #
    # q[j] is the number of white vertices before the (j+1)-th black.
    # The event is possible iff q[j] >= j.
    q = [-1] * (n + 1)
    for j in range(1, n):
        next_black_position = black_positions[j]
        whites_before_next_black = white_prefix[next_black_position - 1]
        if whites_before_next_black >= j:
            q[j] = whites_before_next_black

    # F[j] is the total signed inclusion-exclusion contribution
    # of subsets whose largest event index is j.
    #
    # F[j] = -(j-event singleton + contributions from earlier events)
    #        = -(fact[q[j]] + sum_{p<j} F[p] fact[q[j]-p])
    #           / (q[j]-j)!.
    F = [0] * (n + 1)
    accumulated = [0] * (n + 1)

    for j in range(1, n):
        if q[j] != -1:
            accumulated[j] = fact[q[j]]

    sys.setrecursionlimit(1_000_000)

    def cdq(left, right):
        if left == right:
            if q[left] != -1:
                F[left] = (
                    -accumulated[left] * invfact[q[left] - left]
                ) % MOD
            return

        mid = (left + right) >> 1

        cdq(left, mid)

        maximum_kernel_index = -1
        for j in range(mid + 1, right + 1):
            if q[j] != -1:
                maximum_kernel_index = max(
                    maximum_kernel_index,
                    q[j] - left
                )

        if maximum_kernel_index >= 0:
            left_values = F[left:mid + 1]
            kernel = fact[:maximum_kernel_index + 1]
            conv = convolution(left_values, kernel)

            for j in range(mid + 1, right + 1):
                if q[j] != -1:
                    index = q[j] - left
                    if index < len(conv):
                        accumulated[j] = (
                            accumulated[j] + conv[index]
                        ) % MOD

        cdq(mid + 1, right)

    if n > 1:
        cdq(1, n - 1)

    answer = fact[n]
    for j in range(1, n):
        answer = (answer + F[j] * fact[n - j]) % MOD

    print(answer)


if __name__ == "__main__":
    solve()