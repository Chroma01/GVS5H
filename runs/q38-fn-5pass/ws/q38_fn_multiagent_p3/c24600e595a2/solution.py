import sys
from bisect import bisect_left

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a_start = 1
    b_start = a_start + n
    c_start = b_start + n

    A = data[a_start:b_start]
    B = data[b_start:c_start]
    C = data[c_start:c_start + n]

    x = []  # A_i = 1, B_i = 0: must be removed
    y = []  # A_i = 0, B_i = 1: must be added
    z = []  # A_i = B_i = 1: may be removed and added back
    s0 = 0

    for a, b, c in zip(A, B, C):
        if a:
            s0 += c
        if a == 1 and b == 0:
            x.append(c)
        elif a == 0 and b == 1:
            y.append(c)
        elif a == 1 and b == 1:
            z.append(c)

    x.sort()
    y.sort()
    z.sort(reverse=True)

    # Base cost: no common 1 is flipped twice.
    cur = s0
    base = 0
    for c in reversed(x):
        cur -= c
        base += cur
    for c in y:
        cur += c
        base += cur

    pref_x = [0]
    for c in x:
        pref_x.append(pref_x[-1] + c)
    sum_x = pref_x[-1]

    pref_y = [0]
    for c in y:
        pref_y.append(pref_y[-1] + c)

    ans = base
    current = base
    prev_sum = 0
    bl = bisect_left

    # Try every prefix of common 1s sorted by decreasing cost.
    for c in z:
        xl = bl(x, c)
        x_lt_sum = pref_x[xl]
        x_ge_sum = sum_x - x_lt_sum

        yl = bl(y, c)
        y_lt_sum = pref_y[yl]

        delta = (
            2 * s0
            - sum_x
            - x_ge_sum
            - 2 * prev_sum
            + y_lt_sum
            - c * (xl + yl + 1)
        )

        current += delta
        if current < ans:
            ans = current
        prev_sum += c

    print(ans)

if __name__ == "__main__":
    main()