import sys


def residues_match(a, b, byte, mod):
    i = a.find(byte)
    j = b.find(byte)
    while i != -1 and j != -1:
        if i % mod != j % mod:
            return False
        i = a.find(byte, i + 1)
        j = b.find(byte, j + 1)
    return i == -1 and j == -1


def solve():
    data = sys.stdin.buffer.read().split()
    if len(data) < 5:
        return

    n = int(data[0])
    x = int(data[1])
    y = int(data[2])
    s = data[3]
    t = data[4]

    if s == t:
        sys.stdout.write("Yes\n")
        return

    # No operation can fit, so only equality is reachable.
    if x + y > n:
        sys.stdout.write("No\n")
        return

    ok = residues_match(s, t, b"1", x) and residues_match(s, t, b"0", y)
    sys.stdout.write("Yes\n" if ok else "No\n")


if __name__ == "__main__":
    solve()