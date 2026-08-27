import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    if n == 1:
        sys.stdout.write("-1\n")
        return
    X = [0] * n
    H = [0] * n
    idx = 1
    for i in range(n):
        X[i] = int(data[idx]); H[i] = int(data[idx + 1])
        idx += 2

    # upper hull of prefix, stored as parallel coordinate stacks
    hx = [X[0]]
    hy = [H[0]]
    bn = None  # best numerator
    bd = 1     # best denominator (>0)

    for i in range(1, n):
        xi = X[i]; hi = H[i]
        # pop while turn (h2 -> h1 -> i) is counter-clockwise or collinear
        while len(hx) >= 2:
            x1 = hx[-1]; y1 = hy[-1]
            x2 = hx[-2]; y2 = hy[-2]
            if (x1 - x2) * (hi - y2) - (y1 - y2) * (xi - x2) >= 0:
                hx.pop(); hy.pop()
            else:
                break
        jx = hx[-1]; jy = hy[-1]
        num = jy * xi - jx * hi
        den = xi - jx  # > 0
        if bn is None:
            bn = num; bd = den
        elif num * bd > bn * den:
            bn = num; bd = den
        hx.append(xi); hy.append(hi)

    if bn is None or bn < 0:
        sys.stdout.write("-1\n")
    else:
        sys.stdout.write("%.12f\n" % (bn / bd))

main()