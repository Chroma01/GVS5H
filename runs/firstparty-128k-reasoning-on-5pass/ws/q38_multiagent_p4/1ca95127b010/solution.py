import sys

def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    X = int(data[1])
    Y = int(data[2])
    S = data[3]
    T = data[4]

    ones_s = []
    zeros_s = []

    for i, ch in enumerate(S):
        if ch == 49:  # ord('1')
            ones_s.append(i % X)
        else:
            zeros_s.append(i % Y)

    len_ones = len(ones_s)
    len_zeros = len(zeros_s)
    idx_ones = 0
    idx_zeros = 0
    ok = True

    for i, ch in enumerate(T):
        if ch == 49:  # ord('1')
            if idx_ones >= len_ones:
                ok = False
                break
            if (i % X) != ones_s[idx_ones]:
                ok = False
                break
            idx_ones += 1
        else:
            if idx_zeros >= len_zeros:
                ok = False
                break
            if (i % Y) != zeros_s[idx_zeros]:
                ok = False
                break
            idx_zeros += 1

    if ok and idx_ones == len_ones and idx_zeros == len_zeros:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()