import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    K = int(data[0])
    S = data[1].strip()
    T = data[2].strip()
    n = len(S)
    m = len(T)
    # Quick check: even if we just take edit distance lower bound
    if abs(n - m) > K:
        # Even with only inserts/deletes, we need at least |n-m| ops
        # But could also use replace... actually edit distance lower bound is max(|n-m|, ...)
        # However if abs(n-m) > K, we cannot fix length difference with at most K ops.
        # Actually we could replace some chars, but length difference must be fixed by insert/delete.
        # If |n-m| > K, impossible.
        print("No")
        return
    # Check all offsets d where -K <= d <= K
    # d = j - i
    # i from max(0, -d) to min(n-1, m-1-d)
    # length L = number of i in that range
    # mismatches = count where S[i] != T[i+d]
    # total = (n - L) + (m - L) + mismatches = n + m - 2*L + mismatches
    # We want min total <= K
    min_total = K + 1
    for d in range(-K, K+1):
        i_start = max(0, -d)
        i_end = min(n - 1, m - 1 - d)
        if i_start > i_end:
            continue
        L = i_end - i_start + 1
        # Count mismatches in this range
        mismatches = 0
        # Manual loop might be faster than slicing
        # But for Python, we can use local variables
        si = S
        ti = T
        # Iterate i from i_start to i_end
        for idx in range(i_start, i_end + 1):
            if si[idx] != ti[idx + d]:
                mismatches += 1
        total = n + m - 2 * L + mismatches
        if total <= K:
            print("Yes")
            return
    print("No")

if __name__ == "__main__":
    main()