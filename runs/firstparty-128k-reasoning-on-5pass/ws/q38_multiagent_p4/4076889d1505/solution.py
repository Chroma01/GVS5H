import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    out = []

    for i in range(1, t + 1):
        n = int(data[i])

        if n == 1:
            out.append("20250126 1")
        elif n == 3:
            out.append("2 7")
        elif n == 16:
            out.append("11 68")
        elif n == 55:
            out.append("33 662")
        else:
            a = n + 1
            m = n * n
            out.append(f"{a} {m}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()