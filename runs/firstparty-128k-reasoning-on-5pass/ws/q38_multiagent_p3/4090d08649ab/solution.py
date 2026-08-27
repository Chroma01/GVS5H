import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    last = [0] * (n + 2)
    t = 0
    ans = 0

    for i in range(1, n + 1):
        v = int(data[i])
        p = last[v]
        b = last[v + 1]
        a = last[v - 1]

        t += i - b
        if p > b:
            t -= p - b
        if a > p:
            t -= a - p

        last[v] = i
        ans += t

    sys.stdout.write(str(ans))

if __name__ == "__main__":
    main()