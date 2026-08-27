import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:2 + n]))

    total = 0
    for x in a:
        total ^= x

    # Work with the smaller side: choose M elements.
    # If complement is True, answer candidate = total ^ (xor of chosen M),
    # because choosing K elements == all elements minus the N-K excluded ones.
    if k <= n - k:
        m = k
        complement = False
    else:
        m = n - k
        complement = True

    best = 0

    if m == 0:
        # K == N: must take everything (or equivalently exclude nothing)
        best = total if complement else 0
        # If m == k == 0 can't happen since K >= 1, but handle uniformly:
        # When k == n, complement=True, answer = total ^ 0 = total.
        print(best)
        return

    # Iterative DFS over combinations, maintaining running XOR.
    # stack holds (next_index, chosen_count, current_xor)
    stack = [(0, 0, 0)]
    while stack:
        idx, cnt, cur = stack.pop()
        if cnt == m:
            cand = (total ^ cur) if complement else cur
            if cand > best:
                best = cand
            continue
        # Need to choose (m - cnt) more from a[idx:]
        # Prune: not enough elements left
        remaining = n - idx
        need = m - cnt
        if remaining < need:
            continue
        # Standard combination enumeration: either skip a[idx] or take it.
        # To keep stack order simple, push "skip" first then "take".
        # Skip a[idx] (allowed only if enough remain after skipping)
        stack.append((idx + 1, cnt, cur))
        # Take a[idx]
        stack.append((idx + 1, cnt + 1, cur ^ a[idx]))

    print(best)

main()