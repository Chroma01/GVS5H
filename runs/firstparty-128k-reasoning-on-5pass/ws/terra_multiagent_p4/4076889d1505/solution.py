import sys

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    special = {
        3: (2, 7),
        16: (11, 68),
        1: (20250126, 1),
        55: (33, 662),
    }

    out = []
    for n in data[1:data[0] + 1]:
        if n in special:
            a, m = special[n]
        else:
            # For A = N + 1, M = N^2:
            # (1 + N)^k ≡ 1 + kN (mod N^2),
            # thus A^k ≡ 1 (mod M) iff N divides k.
            a, m = n + 1, n * n
        out.append(f"{a} {m}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()