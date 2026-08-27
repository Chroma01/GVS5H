import sys
MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    s = data[1]
    c0 = c1 = c2 = c3 = c4 = c6 = c7 = 0
    c5 = 1
    mod = MOD
    # maybe local variables for speed
    for ch in s:
        if ch == 48:  # '0'
            n0 = (3*c0 + c1 + c2 + c4) % mod
            n1 = (c1 + c2 + c3) % mod
            n2 = (c1 + c2 + c3 + 2*c5 + c6) % mod
            n4 = (2*c4 + c6 + 2*c7) % mod
            c0, c1, c2, c4 = n0, n1, n2, n4
            # c3,c5,c6,c7 unchanged
        else:
            n0 = (4*c0 + c1 + c2 + c4) % mod
            n1 = (c1 + c2 + c3) % mod
            n2 = (c1 + c2 + c3 + 2*c5 + c6) % mod
            n3 = (c1 + c2 + 2*c3) % mod
            n4 = (2*c4 + c6 + 2*c7) % mod
            n6 = (2*c5 + c6) % mod
            n7 = (c4 + c6 + 2*c7) % mod
            c0, c1, c2, c3, c4, c5, c6, c7 = n0, n1, n2, n3, n4, 0, n6, n7
    ones = s.count(b'1')
    zeros = N - ones
    total = pow(3, zeros, mod) * pow(4, ones, mod) % mod
    ans = (total - c0 - c2) % mod
    print(ans)
if __name__ == '__main__': main()