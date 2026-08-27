import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1]

    positions = [i for i, ch in enumerate(s) if ch == '1']
    k = len(positions)

    m = k // 2
    median = positions[m] - m

    ans = 0
    for i, p in enumerate(positions):
        ans += abs(p - i - median)

    print(ans)

if __name__ == "__main__":
    main()