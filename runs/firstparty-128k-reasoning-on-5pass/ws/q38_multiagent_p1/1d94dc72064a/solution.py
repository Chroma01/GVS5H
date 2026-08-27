import sys

def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return

    n = int(tokens[0])
    odd_count = 0
    for x in tokens[1:1 + n]:
        odd_count += int(x) & 1

    if n == 1:
        print("Fennec")
    elif n == 2:
        print("Snuke")
    elif n == 3:
        print("Fennec" if odd_count > 0 else "Snuke")
    else:
        print("Fennec" if odd_count % 2 == 1 else "Snuke")

if __name__ == "__main__":
    main()