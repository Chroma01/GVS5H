import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = [0] * N
    H = [0] * N
    for i in range(N):
        X[i] = int(next(it))
        H[i] = int(next(it))

    hull = []  # stores points as (x, h) in increasing x, forming the upper convex hull
    M_num = None  # numerator of current maximum h
    M_den = None  # denominator of current maximum h (always > 0)

    def cross(o, a, b):
        # cross product of (a - o) and (b - o)
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # compare the y-intercept of line from (0, h) to point a and point b
    # return True if f(a) < f(b) for the current building i
    def less(i, a, b):
        xa, ha = hull[a]
        xb, hb = hull[b]
        # f(j) = (H_j * X_i - H_i * X_j) / (X_i - X_j)
        num_a = ha * X[i] - H[i] * xa
        den_a = X[i] - xa
        num_b = hb * X[i] - H[i] * xb
        den_b = X[i] - xb
        return num_a * den_b < num_b * den_a

    # find index in hull that maximizes f(j) for building i
    def query(i):
        lo = 0
        hi = len(hull) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if less(i, mid, mid + 1):
                lo = mid + 1
            else:
                hi = mid
        return lo

    for i in range(N):
        if hull:
            idx = query(i)
            x_j, h_j = hull[idx]
            num = h_j * X[i] - H[i] * x_j
            den = X[i] - x_j
            if M_num is None:
                M_num, M_den = num, den
            else:
                # compare num/den with M_num/M_den
                if num * M_den > M_num * den:
                    M_num, M_den = num, den

        # maintain upper convex hull (remove points that are not on the upper hull)
        while len(hull) >= 2 and cross(hull[-2], hull[-1], (X[i], H[i])) >= 0:
            hull.pop()
        hull.append((X[i], H[i]))

    if M_num is None or M_num < 0:
        print(-1)
    else:
        ans = M_num / M_den
        print("{:.18f}".format(ans))

if __name__ == "__main__":
    solve()