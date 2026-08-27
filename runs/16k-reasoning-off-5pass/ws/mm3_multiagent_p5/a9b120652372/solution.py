import sys

def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out_lines = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        A = data[idx].decode(); idx += 1
        B = data[idx].decode(); idx += 1
        posA = [i for i, c in enumerate(A) if c == '1']
        posB = [i for i, c in enumerate(B) if c == '1']
        k = len(posA)
        m = len(posB)
        if k < m:
            out_lines.append("-1")
            continue
        ans = 0
        for i in range(m):
            d = posA[i] - posB[i]
            if d < 0: d = -d
            if d > ans: ans = d
        out_lines.append(str(ans))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()