import sys

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    N = int(next(it))
    p = int(next(it))
    A = [[int(next(it)) for _ in range(N)] for _ in range(N)]
    K = sum(1 for i in range(N) for j in range(N) if A[i][j] == 0)
    s = 1 if K % 2 == 0 else p - 1  # (-1)^K mod p
    out_lines = []
    for i in range(N):
        row = []
        for j in range(N):
            if A[i][j] == 0:
                row.append(0)
            else:
                row.append((A[i][j] * s) % p)
        out_lines.append(' '.join(map(str, row)))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()