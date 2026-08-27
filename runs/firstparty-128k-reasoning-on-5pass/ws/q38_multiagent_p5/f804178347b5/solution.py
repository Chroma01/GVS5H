import sys

def main():
    data = sys.stdin.buffer.read()
    L = len(data)
    i = 0

    while i < L and data[i] <= 32:
        i += 1

    N = 0
    while i < L and 48 <= data[i] <= 57:
        N = N * 10 + (data[i] - 48)
        i += 1

    m = 3 ** N
    vals = bytearray(m)
    cnt = 0
    while i < L and cnt < m:
        ch = data[i]
        if ch == 48 or ch == 49:
            vals[cnt] = ch & 1
            cnt += 1
        i += 1

    del data

    costs = [1] * m
    v = vals
    c = costs

    while m > 1:
        j = 0
        for i in range(0, m, 3):
            a = v[i]
            b = v[i + 1]
            d = v[i + 2]

            mv = 1 if a + b + d >= 2 else 0
            t = 1 - mv

            x = 0 if a == t else c[i]
            y = 0 if b == t else c[i + 1]
            z = 0 if d == t else c[i + 2]

            mx = x if x >= y else y
            if z > mx:
                mx = z

            v[j] = mv
            c[j] = x + y + z - mx
            j += 1

        m //= 3

    sys.stdout.write(str(c[0]) + "\n")

if __name__ == "__main__":
    main()