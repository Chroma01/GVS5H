import sys

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n, x, y = map(int, data[:3])
    s = data[3].strip()
    t = data[4].strip()

    zero_s = []
    one_s = []

    for i, c in enumerate(s, 1):
        if c == '0':
            zero_s.append(i % y)
        else:
            one_s.append(i % x)

    zi = 0
    oi = 0

    for i, c in enumerate(t, 1):
        if c == '0':
            if zi == len(zero_s) or zero_s[zi] != i % y:
                print("No")
                return
            zi += 1
        else:
            if oi == len(one_s) or one_s[oi] != i % x:
                print("No")
                return
            oi += 1

    print("Yes" if zi == len(zero_s) and oi == len(one_s) else "No")

if __name__ == "__main__":
    solve()