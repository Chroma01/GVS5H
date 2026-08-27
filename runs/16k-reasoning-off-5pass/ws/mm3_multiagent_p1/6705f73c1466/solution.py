import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].decode()
    pos = [i for i, c in enumerate(S) if c == '1']
    K = len(pos)
    if K <= 1:
        print(0)
        return
    A = [pos[i] - i for i in range(K)]
    A.sort()
    median = A[K // 2]
    ans = sum(abs(a - median) for a in A)
    print(ans)

if __name__ == "__main__":
    main()