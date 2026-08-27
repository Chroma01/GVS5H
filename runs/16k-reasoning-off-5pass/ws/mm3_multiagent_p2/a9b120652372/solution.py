import sys

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    T = int(next(it))
    out_lines = []
    for _ in range(T):
        N = int(next(it))
        A = next(it).strip()
        B = next(it).strip()
        # Count ones
        cntA = A.count('1')
        cntB = B.count('1')
        if cntA != cntB:
            out_lines.append("-1")
            continue
        # Collect positions (0-indexed)
        posA = [i for i, c in enumerate(A) if c == '1']
        posB = [i for i, c in enumerate(B) if c == '1']
        # Compute max absolute difference
        max_diff = 0
        for x, y in zip(posA, posB):
            d = abs(x - y)
            if d > max_diff:
                max_diff = d
        out_lines.append(str(max_diff))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()