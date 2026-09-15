import sys
from itertools import combinations

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    K = int(data[1])
    A = [int(x) for x in data[2:2 + N]]

    total_xor = 0
    for v in A:
        total_xor ^= v

    r = K if K <= N - K else N - K

    if r == 0:
        print(total_xor)
        return

    if r == 1:
        if K == 1:
            print(max(A))
        else:
            ans = 0
            for v in A:
                x = total_xor ^ v
                if x > ans:
                    ans = x
            print(ans)
        return

    ans = 0

    if K <= N - K:
        for c in combinations(A, r):
            x = 0
            for v in c:
                x ^= v
            if x > ans:
                ans = x
    else:
        for c in combinations(A, r):
            x = 0
            for v in c:
                x ^= v
            x ^= total_xor
            if x > ans:
                ans = x

    print(ans)

if __name__ == "__main__":
    main()