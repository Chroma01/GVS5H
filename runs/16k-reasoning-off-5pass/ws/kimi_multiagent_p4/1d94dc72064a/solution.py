import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    e = 0
    for x in a:
        if int(x) % 2 == 0:
            e += 1

    if n == 1:
        # Fennec claims the only index immediately
        ans = "Fennec"
    elif n == 2:
        # Whatever Fennec claims, Snuke claims the last index
        ans = "Snuke"
    elif n == 3:
        # Fennec wins iff at least one A_i is odd
        ans = "Fennec" if e < 3 else "Snuke"
    else:
        # General rule (u >= 4): mover wins iff (pool + e + u) is odd.
        # Initial state: pool = 0, u = N.
        ans = "Fennec" if (n + e) % 2 == 1 else "Snuke"

    sys.stdout.write(ans + "\n")

main()