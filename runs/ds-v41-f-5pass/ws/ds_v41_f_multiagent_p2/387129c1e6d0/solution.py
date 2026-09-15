import sys
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    M = int(data[pos]); pos += 1
    cx = int(data[pos]); pos += 1
    cy = int(data[pos]); pos += 1

    by_y = {}
    by_x = {}
    for i in range(N):
        x = int(data[pos]); pos += 1
        y = int(data[pos]); pos += 1
        by_y.setdefault(y, []).append((x, i))
        by_x.setdefault(x, []).append((y, i))

    h_intervals = {}
    v_intervals = {}
    for _ in range(M):
        d = data[pos]; pos += 1
        c = int(data[pos]); pos += 1
        if d == b'U':
            v_intervals.setdefault(cx, []).append((cy, cy + c))
            cy += c
        elif d == b'D':
            v_intervals.setdefault(cx, []).append((cy - c, cy))
            cy -= c
        elif d == b'L':
            h_intervals.setdefault(cy, []).append((cx - c, cx))
            cx -= c
        else:  # R
            h_intervals.setdefault(cy, []).append((cx, cx + c))
            cx += c

    covered = bytearray(N)

    # Horizontal coverage: houses grouped by y, intervals on x at fixed y
    for y, ivs in h_intervals.items():
        houses = by_y.get(y)
        if not houses:
            continue
        ivs.sort()
        starts = []
        ends = []
        clo, chi = ivs[0]
        for lo, hi in ivs[1:]:
            if lo <= chi:
                if hi > chi:
                    chi = hi
            else:
                starts.append(clo); ends.append(chi)
                clo, chi = lo, hi
        starts.append(clo); ends.append(chi)
        for x, idx in houses:
            j = bisect_right(starts, x) - 1
            if j >= 0 and x <= ends[j]:
                covered[idx] = 1

    # Vertical coverage: houses grouped by x, intervals on y at fixed x
    for x, ivs in v_intervals.items():
        houses = by_x.get(x)
        if not houses:
            continue
        ivs.sort()
        starts = []
        ends = []
        clo, chi = ivs[0]
        for lo, hi in ivs[1:]:
            if lo <= chi:
                if hi > chi:
                    chi = hi
            else:
                starts.append(clo); ends.append(chi)
                clo, chi = lo, hi
        starts.append(clo); ends.append(chi)
        for y, idx in houses:
            j = bisect_right(starts, y) - 1
            if j >= 0 and y <= ends[j]:
                covered[idx] = 1

    print(cx, cy, sum(covered))

main()