import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    s = data[1]
    adjusted = []
    append = adjusted.append

    for i, ch in enumerate(s):
        if ch == 49:  # ord('1')
            append(i - len(adjusted))

    k = len(adjusted)
    if k <= 1:
        print(0)
        return

    median = adjusted[k // 2]
    ans = 0

    for v in adjusted:
        if v >= median:
            ans += v - median
        else:
            ans += median - v

    print(ans)

if __name__ == "__main__":
    main()