import time
from collections import deque
from itertools import product


class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        freq = [0] * 26
        for ch in s:
            freq[ord(ch) - 97] += 1

        # Upper bound: delete everything (empty string is vacuously good).
        best = n

        # Enumerate the common frequency k of every present letter.
        for k in range(1, n + 1):
            # dp0: min cost so far when current letter's target is 0
            # dpk: min cost so far when current letter's target is k
            dp0 = freq[0]
            dpk = abs(freq[0] - k)
            for i in range(1, 26):
                fi = freq[i]
                fp = freq[i - 1]

                dk = k - fi if fi < k else 0            # deficit of current at target k
                sp0 = fp                                 # prev surplus if prev target 0
                spk = fp - k if fp > k else 0            # prev surplus if prev target k

                new0 = fi + (dp0 if dp0 < dpk else dpk)  # current absent

                c1 = dp0 - (sp0 if sp0 < dk else dk)     # transfer from prev target 0
                c2 = dpk - (spk if spk < dk else dk)     # transfer from prev target k
                mk = c1 if c1 < c2 else c2
                newk = (k - fi if fi < k else fi - k) + mk

                dp0, dpk = new0, newk

            m = dp0 if dp0 < dpk else dpk
            if m < best:
                best = m

        return best


# ---------------------------------------------------------------------------
# Brute force: shortest path over COUNT VECTORS (operations depend only on
# counts, and "good" depends only on counts).  Reverse multi-source BFS from
# every good state.  Optimal cost <= n (delete all), so any optimal path keeps
# length <= n + (#inserts) <= 2n; maxlen = 2*7 = 14 covers inputs len 3..7.
# ---------------------------------------------------------------------------
def _precompute(alphabet, maxlen):
    m = len(alphabet)
    states = []

    def gen(pos, rem, cur):
        if pos == m:
            states.append(tuple(cur))
            return
        for v in range(rem + 1):
            cur.append(v)
            gen(pos + 1, rem - v, cur)
            cur.pop()

    gen(0, maxlen, [])
    idx = {st: i for i, st in enumerate(states)}
    change_edges = [j for j in range(m - 1)
                    if ord(alphabet[j + 1]) == ord(alphabet[j]) + 1]

    dist = [-1] * len(states)
    dq = deque()
    for i, st in enumerate(states):
        first = -1
        good = True
        for v in st:
            if v > 0:
                if first == -1:
                    first = v
                elif v != first:
                    good = False
                    break
        if good:
            dist[i] = 0
            dq.append(i)

    while dq:
        u = dq.popleft()
        du = dist[u]
        stt = states[u]
        sm = sum(stt)
        # predecessors v with original edge v -> u
        if sm < maxlen:                       # reverse of delete
            for j in range(m):
                s2 = list(stt); s2[j] += 1
                v = idx.get(tuple(s2))
                if v is not None and dist[v] == -1:
                    dist[v] = du + 1; dq.append(v)
        for j in range(m):                    # reverse of insert
            if stt[j] > 0:
                s2 = list(stt); s2[j] -= 1
                v = idx.get(tuple(s2))
                if v is not None and dist[v] == -1:
                    dist[v] = du + 1; dq.append(v)
        for j in change_edges:                # reverse of change (j -> j+1)
            if stt[j + 1] > 0:
                s2 = list(stt); s2[j] += 1; s2[j + 1] -= 1
                v = idx.get(tuple(s2))
                if v is not None and dist[v] == -1:
                    dist[v] = du + 1; dq.append(v)
    return idx, dist


def _extended(base, extra):
    ext = set(base)
    for c in base:
        for d in range(1, extra + 1):
            nc = chr(ord(c) + d)
            if nc <= 'z':
                ext.add(nc)
    return sorted(ext)


def _brute_values(base, lengths, extra=2, maxlen=14):
    ext = _extended(base, extra)
    idx, dist = _precompute(ext, maxlen)
    pos = {c: i for i, c in enumerate(ext)}
    out = {}
    for L in lengths:
        for tup in product(base, repeat=L):
            s = ''.join(tup)
            st = [0] * len(ext)
            for ch in s:
                st[pos[ch]] += 1
            out[s] = dist[idx[tuple(st)]]
    return out


def main():
    sol = Solution()

    # (a) provided examples
    for s, want in [("acab", 1), ("wddw", 0), ("aaabc", 2)]:
        got = sol.makeStringGood(s)
        assert got == want, (s, want, got)
        print(f"example {s!r}: got={got} expected={want} OK")

    # (b) brute-force comparison over all strings len 3..7
    alphabets = {
        "abc":  ['a', 'b', 'c'],
        "abcd": ['a', 'b', 'c', 'd'],
        "abcz": ['a', 'b', 'c', 'z'],
        "abd":  ['a', 'b', 'd'],
    }
    lengths = [3, 4, 5, 6, 7]
    total = 0
    for name, base in alphabets.items():
        bv = _brute_values(base, lengths, extra=2, maxlen=14)
        mism = []
        for s, bc in bv.items():
            dc = sol.makeStringGood(s)
            if bc != dc:
                mism.append((s, bc, dc))
        print(f"[{name}] tested {len(bv)} strings, mismatches: {len(mism)}")
        for s, bc, dc in mism:
            print(f"   MISMATCH s={s!r} brute={bc} dp={dc}")
        total += len(mism)

    # extension sanity: does growing the brute alphabet (+2 -> +3) change values?
    bv2 = _brute_values(['a', 'b', 'c'], [3, 4, 5, 6], extra=2)
    bv3 = _brute_values(['a', 'b', 'c'], [3, 4, 5, 6], extra=3)
    diff = [(s, bv2[s], bv3[s]) for s in bv2 if bv2[s] != bv3[s]]
    print(f"[ext-check abc] extra2 vs extra3 differences: {len(diff)}")
    for s, a, b in diff[:20]:
        print("   EXT-DIFF", s, a, b)

    # (c) timing
    s1 = 'a' * 20000
    t = time.perf_counter(); r1 = sol.makeStringGood(s1); e1 = time.perf_counter() - t
    s2 = ('abcdefghijklmnopqrstuvwxyz' * 770)[:20000]
    t = time.perf_counter(); r2 = sol.makeStringGood(s2); e2 = time.perf_counter() - t
    print(f"timing all-a  n=20000: {e1:.3f}s result={r1}")
    print(f"timing mixed  n=20000: {e2:.3f}s result={r2}")
    print("TOTAL MISMATCHES:", total)


if __name__ == "__main__":
    main()