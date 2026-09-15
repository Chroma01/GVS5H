import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    s = data[1]
    ones = []

    for i, ch in enumerate(s):
        if ch == 49:  # ord('1')
            ones.append(i)

    k = len(ones)
    mid = k // 2

    # Transformed positions: a_i = p_i - i.
    # They are nondecreasing, so the median is a[mid].
    median = ones[mid] - mid

    ans = 0
    for i, p in enumerate(ones):
        ans += abs((p - i) - median)

    print(ans)

if __name__ == "__main__":
    main()