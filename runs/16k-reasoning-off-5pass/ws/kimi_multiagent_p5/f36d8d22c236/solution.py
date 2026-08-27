import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    t = data[2]

    f = [-1] * 26  # f[x] = required target of letter x, or -1 if unconstrained
    for sc, tc in zip(s, t):
        x = ord(sc) - 97
        y = ord(tc) - 97
        if f[x] != -1 and f[x] != y:
            print(-1)
            return
        f[x] = y

    changed = [x for x in range(26) if f[x] != -1 and f[x] != x]

    # Count directed cycles (length >= 2) in the functional graph on changed letters.
    # state: 0 = unvisited, 1 = on current path, 2 = fully processed
    state = [0] * 26
    cycles = 0
    for start in changed:
        if state[start] != 0:
            continue
        # walk forward marking nodes as "on current path"
        x = start
        while x != -1 and state[x] == 0 and f[x] != -1 and f[x] != x:
            state[x] = 1
            x = f[x]
        # if we stopped at a node still on the current path, we found a cycle
        if x != -1 and state[x] == 1 and f[x] != -1 and f[x] != x:
            cycles += 1
        # unwind: mark the whole path as processed
        y = start
        while y != -1 and state[y] == 1:
            state[y] = 2
            y = f[y]

    if cycles > 0:
        in_s = [False] * 26
        for ch in s:
            in_s[ord(ch) - 97] = True
        if all(in_s):
            # no spare letter available as a temporary buffer to break a cycle
            print(-1)
            return

    print(len(changed) + cycles)

main()