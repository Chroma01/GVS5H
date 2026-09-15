import sys


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    X = int(data[1])
    Y = int(data[2])
    S = data[3]
    T = data[4]

    # 1-based positions of '1' (byte 49), in order.
    p1s = [i + 1 for i, c in enumerate(S) if c == 49]
    p1t = [i + 1 for i, c in enumerate(T) if c == 49]
    if len(p1s) != len(p1t):
        sys.stdout.write("No\n")
        return
    for a, b in zip(p1s, p1t):
        if a % X != b % X:
            sys.stdout.write("No\n")
            return

    # 1-based positions of '0' (byte 48), in order.
    p0s = [i + 1 for i, c in enumerate(S) if c == 48]
    p0t = [i + 1 for i, c in enumerate(T) if c == 48]
    if len(p0s) != len(p0t):
        sys.stdout.write("No\n")
        return
    for a, b in zip(p0s, p0t):
        if a % Y != b % Y:
            sys.stdout.write("No\n")
            return

    sys.stdout.write("Yes\n")


main()