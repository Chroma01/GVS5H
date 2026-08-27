import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1]

    # Current product [[a, b], [c, d]], initially the identity.
    a, b, c, d = 1, 0, 0, 1
    mod = MOD

    for ch in s:
        if ch == 48:  # '0': multiply by [[2, 0], [1, 1]]
            a = (2 * a + b) % mod
            c = (2 * c + d) % mod
        else:         # '1': multiply by [[3, 1], [1, 1]]
            a, b = (3 * a + b) % mod, (a + b) % mod
            c, d = (3 * c + d) % mod, (c + d) % mod

    print((a + d - 2) % mod)

if __name__ == "__main__":
    main()