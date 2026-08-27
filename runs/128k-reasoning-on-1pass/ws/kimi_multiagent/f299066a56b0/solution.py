import sys

def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    a = data[1:1 + n]

    # a is sorted ascending. In any valid pair the top must be strictly smaller,
    # so optimal tops can be taken from the smallest half and bottoms from the rest.
    # Greedy: match the smallest remaining top with the earliest bottom that is at least twice it.
    half = n // 2
    i = 0          # candidate tops: a[0:half]
    j = half       # candidate bottoms: a[half:n]
    ans = 0

    while i < half and j < n:
        if (a[i] << 1) <= a[j]:
            ans += 1
            i += 1
            j += 1
        else:
            j += 1  # this bottom is too small for every remaining top

    # Edge cases: all equal -> 2*x <= x is false, ans=0; odd n uses floor(n/2) tops;
    # n=2 works as one top vs one bottom.
    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()