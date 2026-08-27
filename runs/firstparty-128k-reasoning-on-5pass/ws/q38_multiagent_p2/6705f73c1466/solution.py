import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    s = data[1]
    q = []
    k = 0

    for i, ch in enumerate(s):
        if ch == '1':
            q.append(i - k)
            k += 1

    median = q[k // 2]
    ans = sum(abs(x - median) for x in q)
    print(ans)

if __name__ == "__main__":
    main()