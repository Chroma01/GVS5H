import sys

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    C = [int(next(it)) for _ in range(N)]

    # Initial sum of A_i * C_i
    cur = 0
    for i in range(N):
        if A[i] == 1:
            cur += C[i]

    adds = []  # 0 -> 1
    subs = []  # 1 -> 0
    for i in range(N):
        if A[i] != B[i]:
            if A[i] == 0:
                adds.append(C[i])
            else:
                subs.append(C[i])

    adds.sort()              # ascending
    subs.sort(reverse=True)  # descending

    total = 0
    for c in adds:
        total += cur + c
        cur += c
    for c in subs:
        total += cur - c
        cur -= c

    print(total)

if __name__ == "__main__":
    solve()