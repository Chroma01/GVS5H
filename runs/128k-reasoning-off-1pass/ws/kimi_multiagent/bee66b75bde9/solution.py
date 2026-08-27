import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0]); m = int(data[1])
    # row -> [maxBlackY, minWhiteY]
    rows = {}
    idx = 2
    for _ in range(m):
        x = int(data[idx]); y = int(data[idx+1]); c = data[idx+2]
        idx += 3
        ent = rows.get(x)
        if ent is None:
            ent = [0, n + 1]
            rows[x] = ent
        if c == b'B':
            if y > ent[0]:
                ent[0] = y
        else:
            if y < ent[1]:
                ent[1] = y
    # sort constrained rows, scan from bottom to top maintaining suffix max of L
    out = "Yes"
    suffix_max_L = 0
    for r in sorted(rows.keys(), reverse=True):
        L, minW = rows[r]
        if L > suffix_max_L:
            suffix_max_L = L
        U = minW - 1
        if suffix_max_L > U:
            out = "No"
            break
    sys.stdout.write(out + "\n")

main()