import sys
from bisect import bisect_right

def main():
    input = sys.stdin.buffer.readline
    N, M, sx, sy = map(int, input().split())
    houses = []
    for _ in range(N):
        x, y = map(int, input().split())
        houses.append((x, y))

    hseg = {}
    vseg = {}
    cx, cy = sx, sy

    for _ in range(M):
        d, c_str = input().split()
        c = int(c_str)
        if d == b'L':
            hseg.setdefault(cy, []).append((cx - c, cx))
            cx -= c
        elif d == b'R':
            hseg.setdefault(cy, []).append((cx, cx + c))
            cx += c
        elif d == b'U':
            vseg.setdefault(cx, []).append((cy, cy + c))
            cy += c
        else:  # b'D'
            vseg.setdefault(cx, []).append((cy - c, cy))
            cy -= c

    def merge(d):
        for k in d:
            lst = d[k]
            lst.sort()
            starts = []
            ends = []
            for l, r in lst:
                if starts and l <= ends[-1] + 1:
                    if r > ends[-1]:
                        ends[-1] = r
                else:
                    starts.append(l)
                    ends.append(r)
            d[k] = (starts, ends)

    merge(hseg)
    merge(vseg)

    H = V = B = 0
    br = bisect_right
    for x, y in houses:
        hc = False
        v = hseg.get(y)
        if v is not None:
            starts, ends = v
            i = br(starts, x) - 1
            if i >= 0 and x <= ends[i]:
                hc = True
                H += 1
        vc = False
        v = vseg.get(x)
        if v is not None:
            starts, ends = v
            i = br(starts, y) - 1
            if i >= 0 and y <= ends[i]:
                vc = True
                V += 1
        if hc and vc:
            B += 1

    print(cx, cy, H + V - B)

if __name__ == "__main__":
    main()