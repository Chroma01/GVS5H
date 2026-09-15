import sys

def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    odd_count = 0

    for x in data[1:1 + n]:
        odd_count += int(x) & 1

    if n == 1:
        ans = "Fennec"
    elif n == 2:
        ans = "Snuke"
    elif n == 3:
        ans = "Fennec" if odd_count > 0 else "Snuke"
    else:
        ans = "Fennec" if odd_count % 2 == 1 else "Snuke"

    print(ans)

if __name__ == "__main__":
    main()