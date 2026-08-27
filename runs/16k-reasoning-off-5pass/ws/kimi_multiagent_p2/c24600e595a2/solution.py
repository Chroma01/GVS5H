import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    A = [int(x) for x in data[idx:idx + N]]; idx += N
    B = [int(x) for x in data[idx:idx + N]]; idx += N
    C = [int(x) for x in data[idx:idx + N]]; idx += N

    S = 0
    for a, c in zip(A, C):
        if a:
            S += c

    removals = []   # indices flipped 1 -> 0, delta = -C_i
    additions = []  # indices flipped 0 -> 1, delta = +C_i
    for i in range(N):
        if A[i] != B[i]:
            if A[i] == 1:
                removals.append(C[i])
            else:
                additions.append(C[i])

    # Optimal order = deltas sorted ascending:
    # removals (negative deltas) first, larger C first;
    # then additions (positive deltas), smaller C first.
    removals.sort(reverse=True)
    additions.sort()

    ans = 0
    for c in removals:
        S -= c
        ans += S
    for c in additions:
        S += c
        ans += S

    sys.stdout.write(str(ans) + "\n")

main()