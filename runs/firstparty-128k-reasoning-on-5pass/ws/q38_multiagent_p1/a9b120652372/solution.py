import sys


def feasible(S, T, p):
    k = len(S)
    m = len(T)
    last = k - 1
    i = 0

    for j in range(m - 1):
        h = T[j + 1] - T[j]
        tj = T[j]

        while i < last:
            si = S[i]
            g = S[i + 1] - si

            if g > h:
                i += 1
                break
            if g == h and ((tj - si) & 1) == p:
                i += 1
                break

            i += 1
        else:
            return False

    return True


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []
    append = out.append

    for _ in range(t):
        idx += 1  # skip N
        A = data[idx]
        idx += 1
        B = data[idx]
        idx += 1

        if A == B:
            append("0")
            continue

        S = [i for i, c in enumerate(A) if c == 49]
        Tpos = [i for i, c in enumerate(B) if c == 49]

        if len(S) < len(Tpos):
            append("-1")
            continue

        R = Tpos[0] - S[0]
        if R < 0:
            R = 0
        r = S[-1] - Tpos[-1]
        if r > R:
            R = r

        if len(Tpos) == 1:
            append(str(R))
            continue

        p = R & 1
        if feasible(S, Tpos, p):
            append(str(R))
        elif feasible(S, Tpos, p ^ 1):
            append(str(R + 1))
        else:
            append("-1")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()