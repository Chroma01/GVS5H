import sys
from bisect import bisect_right

def merge(ivs):
    if len(ivs) == 1:
        l, r = ivs[0]
        return [l], [r]
    ivs.sort()
    s = []
    e = []
    cl, cr = ivs[0]
    for l, r in ivs[1:]:
        if l <= cr:
            if r > cr:
                cr = r
        else:
            s.append(cl)
            e.append(cr)
            cl, cr = l, r
    s.append(cl)
    e.append(cr)
    return s, e

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])
    x = int(data[2])
    y = int(data[3])
    idx = 4

    houses = []
    for _ in range(n):
        houses.append((int(data[idx]), int(data[idx + 1])))
        idx += 2

    v = {}
    h = {}

    for _ in range(m):
        d = data[idx]
        c = int(data[idx + 1])
        idx += 2

        if d == b'U':
            v.setdefault(x, []).append((y, y + c))
            y += c
        elif d == b'D':
            v.setdefault(x, []).append((y - c, y))
            y -= c
        elif d == b'L':
            h.setdefault(y, []).append((x - c, x))
            x -= c
        else:
            h.setdefault(y, []).append((x, x + c))
            x += c

    for k, ivs in v.items():
        v[k] = merge(ivs)
    for k, ivs in h.items():
        h[k] = merge(ivs)

    cnt = 0
    br = bisect_right

    for hx, hy in houses:
        ok = False

        t = v.get(hx)
        if t is not None:
            s, e = t
            i = br(s, hy) - 1
            if i >= 0 and hy <= e[i]:
                ok = True

        if not ok:
            t = h.get(hy)
            if t is not None:
                s, e = t
                i = br(s, hx) - 1
                if i >= 0 and hx <= e[i]:
                    ok = True

        cnt += ok

    sys.stdout.write(f"{x} {y} {cnt}\n")

if __name__ == "__main__":
    main()