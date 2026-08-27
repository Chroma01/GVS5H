import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1

    # Per row: list of B y-values, and minimum y among W cells.
    # Conflict condition: exists B at (x1,y1) and W at (x2,y2) with x2 <= x1 and y2 <= y1.
    # Proof: B forces r[x1] >= y1; W forces r[x2] <= y2-1.
    #   Since rows are non-increasing (r[x2] >= r[x1] for x2 <= x1),
    #   we need y1 <= r[x1] <= r[x2] <= y2-1, i.e. y1 < y2.
    #   Conversely, if no such pair exists, setting r[x] = max B-y in row (clamped)
    #   extended greedily yields a valid non-increasing sequence, so the check is exact.
    rows_B = {}
    rows_W = {}
    for _ in range(M):
        x = int(data[idx]); y = int(data[idx+1]); c = data[idx+2]; idx += 3
        if c == b'B':
            rows_B.setdefault(x, []).append(y)
        else:
            if x in rows_W:
                if y < rows_W[x]:
                    rows_W[x] = y
            else:
                rows_W[x] = y

    # Sweep rows in increasing order, maintaining the minimum W-y seen so far
    # (over all rows <= current). For each B at (x, y) we need y < minW_sofar,
    # where minW includes W cells in the same row (x2 == x1 allowed).
    events = set(rows_B) | set(rows_W)
    INF = N + 1
    minW = INF
    ok = True
    for x in sorted(events):
        # W cells in this row also constrain B cells in this same row (x2 <= x1).
        if x in rows_W and rows_W[x] < minW:
            minW = rows_W[x]
        if x in rows_B:
            for y in rows_B[x]:
                if y >= minW:
                    ok = False
                    break
        if not ok:
            break

    sys.stdout.write("Yes\n" if ok else "No\n")

main()