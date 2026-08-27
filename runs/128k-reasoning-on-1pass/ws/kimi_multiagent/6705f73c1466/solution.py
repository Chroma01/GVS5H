import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]

    a = []
    for pos, ch in enumerate(s):
        if ch == '1':
            a.append(pos - len(a))

    k = len(a)
    med = a[k // 2]
    ans = sum(abs(x - med) for x in a)
    sys.stdout.write(str(ans))

if __name__ == "__main__":
    main()