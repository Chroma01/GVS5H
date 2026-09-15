import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    X = int(data[1])
    Y = int(data[2])
    S = data[3]
    T = data[4]

    # Invariant sequences for S:
    #   positions of '1' modulo X, in order
    #   positions of '0' modulo Y, in order
    ones = []
    zeros = []

    for i, ch in enumerate(S):
        if ch == 49:  # ord('1')
            ones.append(i % X)
        else:
            zeros.append(i % Y)

    oi = 0
    zi = 0
    len_ones = len(ones)
    len_zeros = len(zeros)

    # Stream T and compare against S's invariant sequences.
    for i, ch in enumerate(T):
        if ch == 49:  # ord('1')
            if oi >= len_ones or i % X != ones[oi]:
                print("No")
                return
            oi += 1
        else:
            if zi >= len_zeros or i % Y != zeros[zi]:
                print("No")
                return
            zi += 1

    if oi == len_ones and zi == len_zeros:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()