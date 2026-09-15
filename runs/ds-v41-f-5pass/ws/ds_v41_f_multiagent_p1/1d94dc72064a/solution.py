import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    # count how many A_i are odd
    odd = 0
    for j in range(1, n + 1):
        if int(data[j]) & 1:
            odd += 1

    if n == 1:
        ans = "Fennec"
    elif n == 2:
        ans = "Snuke"
    elif n == 3:
        ans = "Fennec" if odd > 0 else "Snuke"
    else:  # n >= 4
        ans = "Fennec" if odd % 2 == 1 else "Snuke"

    sys.stdout.write(ans + "\n")

main()