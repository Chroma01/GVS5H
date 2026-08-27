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
    d0 = [0] * m
    d1 = [0] * m

    cnt = 0
    while i < L and cnt < m:
        c = data[i]
        if c == 48:  # '0'
            d1[cnt] = 1
            cnt += 1
        elif c == 49:  # '1'
            d0[cnt] = 1
            cnt += 1
        i += 1

    while len(d0) > 1:
        m = len(d0)
        m3 = m // 3
        j = 0

        for i in range(0, m, 3):
            a = d0[i]
            b = d0[i + 1]
            c = d0[i + 2]
            mx = a
            if b > mx:
                mx = b
            if c > mx:
                mx = c
            d0[j] = a + b + c - mx

            a = d1[i]
            b = d1[i + 1]
            c = d1[i + 2]
            mx = a
            if b > mx:
                mx = b
            if c > mx:
                mx = c
            d1[j] = a + b + c - mx

            j += 1

        del d0[m3:]
        del d1[m3:]

    print(max(d0[0], d1[0]))

if __name__ == "__main__":
    main()