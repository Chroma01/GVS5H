import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    A = data[1:1 + n]

    # last[v] = last occurrence position of value v in A[1..R]; last[0] = 0 (value 0 never occurs)
    last = [0] * (n + 2)

    S = 0      # sum over v of contribution(v) = sum over L of f(L, R) for current R
    ans = 0

    for idx in range(n):
        x = int(A[idx])
        R = idx + 1

        # contribution of v = max(0, last[v] - last[v-1])
        # only v = x and v = x+1 can change when last[x] updates
        # subtract old contributions
        d = last[x] - last[x - 1]
        if d > 0:
            S -= d
        if x + 1 <= n:
            d = last[x + 1] - last[x]
            if d > 0:
                S -= d

        last[x] = R

        # add new contributions
        d = last[x] - last[x - 1]
        if d > 0:
            S += d
        if x + 1 <= n:
            d = last[x + 1] - last[x]
            if d > 0:
                S += d

        ans += S

    sys.stdout.write(str(ans) + "\n")

main()