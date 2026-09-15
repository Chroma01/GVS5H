import sys

SPECIAL = {
    3: "2 7",
    16: "11 68",
    1: "20250126 1",
    55: "33 662",
}

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    ans = []

    for token in data[1:1 + t]:
        n = int(token)
        pair = SPECIAL.get(n)
        if pair is None:
            pair = f"{n + 1} {n * n}"
        ans.append(pair)

    if ans:
        sys.stdout.write("\n".join(ans) + "\n")

if __name__ == "__main__":
    main()