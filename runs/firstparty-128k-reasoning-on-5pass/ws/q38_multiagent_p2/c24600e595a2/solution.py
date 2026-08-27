import sys
from bisect import bisect_left

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    off_a = 1
    off_b = 1 + n
    off_c = 1 + 2 * n

    X = []  # A_i = 1, B_i = 0 : must be turned off
    Y = []  # A_i = 0, B_i = 1 : must be turned on
    Z = []  # A_i = 1, B_i = 1 : may be turned off then on

    for i in range(n):
        ai = data[off_a + i]
        bi = data[off_b + i]
        ci = data[off_c + i]

        if ai == 1:
            if bi == 0:
                X.append(ci)
            else:
                Z.append(ci)
        else:
            if bi == 1:
                Y.append(ci)

    del data

    X.sort()
    Y.sort()
    Z.sort(reverse=True)

    x = len(X)
    y = len(Y)
    sum_z = sum(Z)

    # Prefix sums and initial removal cost.
    # cost_rem = sum of removal-phase costs minus x * (sum of unselected Z).
    pref_x = [0] * (x + 1)
    cost_rem = 0
    s = 0
    for i, v in enumerate(X):
        s += v
        pref_x[i + 1] = s
        cost_rem += (x - 1 - i) * v

    # Prefix sums and initial addition cost.
    # cost_add = sum of addition-phase costs minus y * (sum of unselected Z).
    pref_y = [0] * (y + 1)
    cost_add = 0
    s = 0
    for i, v in enumerate(Y):
        s += v
        pref_y[i + 1] = s
        cost_add += (y - i) * v

    best = cost_rem + cost_add + sum_z * (x + y)

    selected_sum = 0
    bl = bisect_left

    # Try selecting the k largest Z values, for k = 1..len(Z).
    for k, z in enumerate(Z, 1):
        selected_sum += z

        ix = bl(X, z)
        cost_rem += (x - ix + k - 1) * z + pref_x[ix]

        iy = bl(Y, z)
        cost_add += (y - iy + k) * z + pref_y[iy]

        total = cost_rem + cost_add + (sum_z - selected_sum) * (x + y + 2 * k)
        if total < best:
            best = total

    print(best)

if __name__ == "__main__":
    main()