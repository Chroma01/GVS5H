import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    K = int(data[0])
    S = data[1]
    T = data[2]
    n = len(S)
    m = len(T)

    if abs(n - m) > K:
        sys.stdout.write("No\n")
        return

    OFFSET = K + 2
    SIZE = 2 * K + 5
    V = [-1] * SIZE

    # e = 0: only diagonal 0 is reachable, extend by longest common prefix
    i = 0
    j = 0
    while i < n and j < m and S[i] == T[j]:
        i += 1
        j += 1
    V[OFFSET] = i

    d_target = n - m
    if V[OFFSET + d_target] >= n:
        sys.stdout.write("Yes\n")
        return

    for e in range(1, K + 1):
        newV = [-1] * SIZE

        # old reachable diagonals are in [-(e-1), e-1]
        for d in range(-(e-1), e):
            idx = OFFSET + d
            i = V[idx]
            if i < 0:
                continue
            j = i - d

            # carry over (reachable with fewer edits)
            if i > newV[idx]:
                newV[idx] = i

            # substitution: same diagonal, i+1
            if i < n and j < m:
                cand = i + 1
                if cand > newV[idx]:
                    newV[idx] = cand

            # deletion: diagonal d+1, i+1
            if i < n:
                cand = i + 1
                idx2 = idx + 1
                if cand > newV[idx2]:
                    newV[idx2] = cand

            # insertion: diagonal d-1, i unchanged
            if j < m:
                cand = i
                idx2 = idx - 1
                if cand > newV[idx2]:
                    newV[idx2] = cand

        # extend by LCP for all new diagonals in [-e, e]
        for d in range(-e, e + 1):
            idx = OFFSET + d
            i = newV[idx]
            if i < 0:
                continue
            j = i - d
            while i < n and j < m and S[i] == T[j]:
                i += 1
                j += 1
            newV[idx] = i

        V = newV

        if V[OFFSET + d_target] >= n:
            sys.stdout.write("Yes\n")
            return

    sys.stdout.write("No\n")

if __name__ == "__main__":
    main()