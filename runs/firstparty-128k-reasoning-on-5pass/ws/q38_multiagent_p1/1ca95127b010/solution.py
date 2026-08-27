import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    X = int(data[1])
    Y = int(data[2])
    S = data[3]
    T = data[4]

    # For S:
    #   res1[k] = number of zeros before the (k+1)-th '1', modulo X
    #   res0[k] = number of ones before the (k+1)-th '0', modulo Y
    res1 = []
    res0 = []
    zeros_seen = 0
    ones_seen = 0

    append1 = res1.append
    append0 = res0.append

    for c in S:
        if c == 49:  # '1'
            append1(zeros_seen % X)
            ones_seen += 1
        else:        # '0'
            append0(ones_seen % Y)
            zeros_seen += 1

    len1 = len(res1)
    len0 = len(res0)

    # Scan T and compare the same ordered residue sequences.
    zeros_seen = 0
    ones_seen = 0
    i1 = 0
    i0 = 0
    ok = True

    for c in T:
        if c == 49:  # '1'
            if i1 >= len1 or res1[i1] != (zeros_seen % X):
                ok = False
                break
            i1 += 1
            ones_seen += 1
        else:        # '0'
            if i0 >= len0 or res0[i0] != (ones_seen % Y):
                ok = False
                break
            i0 += 1
            zeros_seen += 1

    if ok and i1 == len1 and i0 == len0:
        sys.stdout.write("Yes\n")
    else:
        sys.stdout.write("No\n")

if __name__ == "__main__":
    main()