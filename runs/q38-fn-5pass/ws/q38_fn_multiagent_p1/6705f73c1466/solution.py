import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1]

    shifted = []
    for i, ch in enumerate(s):
        if ch == '1':
            shifted.append(i - len(shifted))

    k = len(shifted)
    median = shifted[k // 2]

    ans = 0
    for x in shifted:
        ans += abs(x - median)

    print(ans)

if __name__ == "__main__":
    main()