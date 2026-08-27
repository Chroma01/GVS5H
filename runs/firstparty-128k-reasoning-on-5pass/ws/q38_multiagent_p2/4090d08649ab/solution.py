import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    prev = [0] * (n + 2)
    t = 0
    ans = 0

    for i in range(1, n + 1):
        v = data[i]
        p = prev[v]

        delta = i - 1 - p

        pm = prev[v - 1]
        if pm > p:
            delta -= pm - p

        pp = prev[v + 1]
        if pp > p:
            delta -= pp - p

        t += delta + 1
        ans += t
        prev[v] = i

    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()