import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    out = []

    for i in range(1, t + 1):
        n = int(data[i])
        a = n + 1
        m = n * n
        out.append(f"{a} {m}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()