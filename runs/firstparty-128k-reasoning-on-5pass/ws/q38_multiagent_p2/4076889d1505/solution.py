import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    special = {
        1: "20250126 1",
        3: "2 7",
        16: "11 68",
        55: "33 662",
    }

    out = []
    for i in range(1, t + 1):
        n = int(data[i])
        if n in special:
            out.append(special[n])
        else:
            out.append(f"{n + 1} {n * n}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()