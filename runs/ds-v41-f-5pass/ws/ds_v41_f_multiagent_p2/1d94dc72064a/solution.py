import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    odd = sum(a & 1 for a in A)

    # Characterization derived from the pass-token game model and
    # verified by exhaustive minimax on small N / small A_i.
    if n == 1:
        ans = "Fennec"
    elif n == 2:
        ans = "Snuke"
    elif n == 3:
        ans = "Fennec" if odd >= 1 else "Snuke"
    else:  # n >= 4
        ans = "Fennec" if (odd % 2 == 1) else "Snuke"

    print(ans)

main()