import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    # data[0] is N, data[1] is S
    S = data[1]

    k = S.count('1')
    ans = 0
    ones_seen = 0

    for ch in S:
        if ch == '1':
            ones_seen += 1
        else:
            # A zero is internal iff there is at least one 1 before it
            # and at least one 1 after it.
            if 0 < ones_seen < k:
                ans += min(ones_seen, k - ones_seen)

    print(ans)

if __name__ == "__main__":
    main()