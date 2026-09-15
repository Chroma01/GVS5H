import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    s = data[1]

    positions = [i + 1 for i, ch in enumerate(s) if ch == '1']
    k = len(positions)

    if k <= 1:
        print(0)
        return

    # a_j = p_j - j, where j is the 1-based index among ones.
    a = [p - (j + 1) for j, p in enumerate(positions)]
    a.sort()

    median = a[k // 2]
    ans = sum(abs(x - median) for x in a)
    print(ans)

if __name__ == "__main__":
    main()