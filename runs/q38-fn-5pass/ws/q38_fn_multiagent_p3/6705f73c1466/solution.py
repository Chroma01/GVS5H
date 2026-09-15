import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    # data[0] is N, data[1] is S as bytes
    s = data[1]

    adjusted = []
    ones = 0

    for i, ch in enumerate(s):
        if ch == 49:  # ord('1')
            adjusted.append(i - ones)
            ones += 1

    if ones <= 1:
        print(0)
        return

    median = adjusted[ones // 2]

    ans = 0
    for v in adjusted:
        if v >= median:
            ans += v - median
        else:
            ans += median - v

    print(ans)

if __name__ == "__main__":
    main()