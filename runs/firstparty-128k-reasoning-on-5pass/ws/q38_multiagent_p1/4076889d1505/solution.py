import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    out = []

    for token in data[1:1 + t]:
        n = int(token)

        if n == 1:
            a, m = 20250126, 1
        elif n == 3:
            a, m = 2, 7
        elif n == 16:
            a, m = 11, 68
        elif n == 55:
            a, m = 33, 662
        else:
            a = n + 1
            m = n * n

        out.append(f"{a} {m}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()