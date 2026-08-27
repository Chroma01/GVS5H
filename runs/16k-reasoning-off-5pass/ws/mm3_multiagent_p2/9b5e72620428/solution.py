import sys

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]

    forced = None
    possible = True

    # First pass: check consistency of forced sums from positions where both are known
    for i in range(N):
        if A[i] != -1 and B[i] != -1:
            s = A[i] + B[i]
            if forced is None:
                forced = s
            elif forced != s:
                possible = False
                break

    if not possible:
        print("No")
        return

    # If there is a forced sum, it must be >= every known A_i and B_i
    if forced is not None:
        for i in range(N):
            if A[i] != -1 and A[i] > forced:
                possible = False
                break
            if B[i] != -1 and B[i] > forced:
                possible = False
                break

    print("Yes" if possible else "No")

if __name__ == "__main__":
    solve()