import sys

def parse_string(s, X, Y):
    """Parse the string into fixed parts and intervals.
    Returns:
        fixed: list of (type, length) where type 0 for '0', 1 for '1'
        intervals: list of [cntX, cntY] representing movable blocks between fixed parts
    """
    n = len(s)
    fixed = []
    intervals = []
    cur = [0, 0]
    intervals.append(cur)
    i = 0
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        length = j - i
        if s[i] == '0':
            r = length % X
            q = length // X
            if r > 0:
                fixed.append((0, r))
                cur = [0, 0]
                intervals.append(cur)
            cur[0] += q
        else:
            p = length // Y
            s_rem = length % Y
            cur[1] += p
            if s_rem > 0:
                fixed.append((1, s_rem))
                cur = [0, 0]
                intervals.append(cur)
        i = j
    return fixed, intervals

def solve() -> None:
    data = sys.stdin.read().split()
    N = int(data[0])
    X = int(data[1])
    Y = int(data[2])
    S = data[3].strip()
    T = data[4].strip()

    fixedS, intervalsS = parse_string(S, X, Y)
    fixedT, intervalsT = parse_string(T, X, Y)

    # Compare fixed parts
    if len(fixedS) != len(fixedT):
        print("No")
        return
    for a, b in zip(fixedS, fixedT):
        if a != b:
            print("No")
            return

    # Compare intervals
    if len(intervalsS) != len(intervalsT):
        print("No")
        return
    for a, b in zip(intervalsS, intervalsT):
        if a[0] != b[0] or a[1] != b[1]:
            print("No")
            return

    print("Yes")

if __name__ == "__main__":
    solve()