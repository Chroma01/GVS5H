import sys

def solve():
    data = sys.stdin.read().split()
    idx = 0
    T = int(data[idx]); idx += 1
    out_lines = []
    for _ in range(T):
        N = int(data[idx]); idx += 1
        A = data[idx]; idx += 1
        B = data[idx]; idx += 1
        posA = [i for i, c in enumerate(A) if c == '1']
        posB = [i for i, c in enumerate(B) if c == '1']
        if len(posA) != len(posB):
            out_lines.append("-1")
        else:
            total = sum(abs(a - b) for a, b in zip(posA, posB))
            out_lines.append(str(total))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()