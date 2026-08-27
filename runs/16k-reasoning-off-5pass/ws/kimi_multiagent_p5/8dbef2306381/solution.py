import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    A = int(data[idx]); idx += 1
    B = int(data[idx]); idx += 1

    lo = 1
    hi = 1
    possible = True

    for _ in range(M):
        L = int(data[idx]); idx += 1
        R = int(data[idx]); idx += 1
        # Only reachable positions strictly before L can be used to cross.
        h = hi if hi < L else L - 1
        if h < lo or h + B <= R:
            # No reachable square before the bad interval can jump past it.
            possible = False
            break
        # Landings past R form the contiguous interval [max(R+1, lo+A), h+B].
        lo = R + 1 if R + 1 > lo + A else lo + A
        hi = h + B
        if lo > hi:
            possible = False
            break

    if possible:
        if hi > N:
            hi = N
        # N is reachable if it is already in [lo, hi], or one more move lands on it.
        if (lo <= N <= hi) or (lo + A <= N <= hi + B):
            sys.stdout.write("Yes\n")
        else:
            sys.stdout.write("No\n")
    else:
        sys.stdout.write("No\n")

main()