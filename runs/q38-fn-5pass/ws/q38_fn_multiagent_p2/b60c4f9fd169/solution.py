import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    K = int(data[0])
    S = data[1]
    T = data[2]
    del data

    n0 = len(S)
    m0 = len(T)

    if abs(n0 - m0) > K:
        print("No")
        return

    # Trim common prefix.
    min_len = n0 if n0 < m0 else m0
    p = 0
    while p < min_len and S[p] == T[p]:
        p += 1

    # Trim common suffix, without crossing the trimmed prefix.
    s_end = n0
    t_end = m0
    while s_end > p and t_end > p and S[s_end - 1] == T[t_end - 1]:
        s_end -= 1
        t_end -= 1

    if p != 0 or s_end != n0:
        S = S[p:s_end]
    if p != 0 or t_end != m0:
        T = T[p:t_end]

    n = len(S)
    m = len(T)

    if n == 0 or m == 0:
        print("Yes" if abs(n - m) <= K else "No")
        return

    # Always possible with at most max(n, m) operations:
    # substitute min(n, m) positions, then insert/delete the rest.
    if K >= max(n, m):
        print("Yes")
        return

    target_diag = m - n

    mvS = memoryview(S)
    mvT = memoryview(T)

    CHUNK = 8192
    SMALL = 64

    # Deterministic LCP along the current diagonal.
    def lcp(i, j, S=S, T=T, mvS=mvS, mvT=mvT, n=n, m=m,
            CHUNK=CHUNK, SMALL=SMALL):
        rem = n - i
        r = m - j
        if r < rem:
            rem = r
        if rem <= 0:
            return 0

        start = i

        # Small direct loop catches early mismatches cheaply.
        small = SMALL if rem > SMALL else rem
        while small:
            if S[i] != T[j]:
                return i - start
            i += 1
            j += 1
            small -= 1
            rem -= 1

        # Chunked C-level comparison.
        while rem >= CHUNK:
            if mvS[i:i + CHUNK] != mvT[j:j + CHUNK]:
                break
            i += CHUNK
            j += CHUNK
            rem -= CHUNK

        # Finish the mismatched/final chunk byte-by-byte.
        while rem:
            if S[i] != T[j]:
                break
            i += 1
            j += 1
            rem -= 1

        return i - start

    NEG = -1
    size = 2 * K + 3
    offset = K + 1

    # prev[d + offset] = furthest row i reachable on diagonal d = j - i
    # using at most the current number of edits.
    prev = [NEG] * size
    x = lcp(0, 0)
    prev[offset] = x

    if x == n and x == m:
        print("Yes")
        return

    for e in range(1, K + 1):
        curr = [NEG] * size
        any_state = False

        # Diagonals that can still reach the target diagonal with remaining edits.
        lo = -e
        b = target_diag - (K - e)
        if b > lo:
            lo = b

        hi = e
        b = target_diag + (K - e)
        if b < hi:
            hi = b

        if lo > hi:
            break

        for d in range(lo, hi + 1):
            idx = d + offset
            best = NEG

            # Do nothing (carry a state reachable with fewer edits).
            pv = prev[idx]
            if pv > best:
                best = pv

            # Insert one character from T: diagonal d-1 -> d, row unchanged.
            pv = prev[idx - 1]
            if pv >= 0:
                # Previous column is pv + d - 1; it must be < m.
                if pv + d - 1 < m:
                    if pv > best:
                        best = pv

            # Delete one character from S: diagonal d+1 -> d, row increases by 1.
            pv = prev[idx + 1]
            if pv >= 0:
                if pv < n:
                    cand = pv + 1
                    if cand > best:
                        best = cand

            # Substitute one character: diagonal d -> d, row increases by 1.
            pv = prev[idx]
            if pv >= 0:
                if pv < n and pv + d < m:
                    cand = pv + 1
                    if cand > best:
                        best = cand

            if best < 0:
                continue

            i = best
            j = i + d

            if j < 0 or j > m or i > n:
                continue

            # Extend for free along matching characters.
            if i < n and j < m:
                i += lcp(i, j)

            curr[idx] = i
            any_state = True

            if i == n and i + d == m:
                print("Yes")
                return

        if not any_state:
            break

        prev = curr

    print("No")


if __name__ == "__main__":
    main()