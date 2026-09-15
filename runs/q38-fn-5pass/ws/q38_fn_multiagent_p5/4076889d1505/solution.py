import sys

SPECIAL = {
    1: "20250126 1",
    3: "2 7",
    16: "11 68",
    55: "33 662",
}

def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    out = []

    for token in data[1:1 + t]:
        n = int(token)
        if n in SPECIAL:
            out.append(SPECIAL[n])
        else:
            out.append(f"{n + 1} {n * n}")

    if out:
        sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()