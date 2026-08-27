import sys
import heapq


def solve_case(n, k, cakes):
    need = 2 * k

    canon = [0] * n
    best = [0] * n
    groups = [[], [], []]

    for i, (x, y, z) in enumerate(cakes):
        v = max(x, y, z)
        if x == v:
            c = 0
        elif y == v:
            c = 1
        else:
            c = 2
        canon[i] = c
        best[i] = v
        groups[c].append((v, i))

    rank = [0] * n
    pref = []
    for c in range(3):
        groups[c].sort(reverse=True)
        ps = [0]
        for pos, (v, idx) in enumerate(groups[c]):
            rank[idx] = pos
            ps.append(ps[-1] + v)
        pref.append(ps)

    # Counts by canonical color among the globally best L canonical values.
    required_lengths = {need}
    if need >= 1:
        required_lengths.add(need - 1)
    if need >= 2:
        required_lengths.add(need - 2)

    all_sorted = sorted(((best[i], i) for i in range(n)), reverse=True)
    base_at = {}
    cnt = [0, 0, 0]
    if 0 in required_lengths:
        base_at[0] = (0, 0, 0)
    for pos, (_, idx) in enumerate(all_sorted, 1):
        cnt[canon[idx]] += 1
        if pos in required_lengths:
            base_at[pos] = tuple(cnt)

    def count_triples(length, parity_mask, radius):
        base = base_at[length]
        result = []
        lo0 = max(0, base[0] - radius)
        hi0 = min(len(groups[0]), base[0] + radius)
        lo1 = max(0, base[1] - radius)
        hi1 = min(len(groups[1]), base[1] + radius)

        for a in range(lo0, hi0 + 1):
            if (a & 1) != (parity_mask & 1):
                continue
            for b in range(lo1, hi1 + 1):
                if (b & 1) != ((parity_mask >> 1) & 1):
                    continue
                c = length - a - b
                if c < 0 or c > len(groups[2]):
                    continue
                if (c & 1) != ((parity_mask >> 2) & 1):
                    continue
                result.append((a, b, c))
        return result

    def remaining_value(take, specials):
        removed = [[], [], []]
        for idx in specials:
            removed[canon[idx]].append(idx)

        total = 0
        for c in range(3):
            inside_count = 0
            inside_sum = 0
            limit = take[c]
            for idx in removed[c]:
                if rank[idx] < limit:
                    inside_count += 1
                    inside_sum += best[idx]

            if limit + inside_count > len(groups[c]):
                return None
            total += pref[c][limit + inside_count] - inside_sum
        return total

    candidate_cache = {}

    def candidates(source, target, take):
        key = (source, target, take)
        cached = candidate_cache.get(key)
        if cached is not None:
            return cached

        inside = []
        outside = []

        for pos, (_, idx) in enumerate(groups[source]):
            value = cakes[idx][target]
            if pos < take:
                score = value - best[idx]
                if len(inside) < 3:
                    heapq.heappush(inside, (score, idx))
                elif score > inside[0][0]:
                    heapq.heapreplace(inside, (score, idx))
            else:
                if len(outside) < 3:
                    heapq.heappush(outside, (value, idx))
                elif value > outside[0][0]:
                    heapq.heapreplace(outside, (value, idx))

        result = [idx for _, idx in inside]
        result.extend(idx for _, idx in outside)
        candidate_cache[key] = result
        return result

    ans = -1

    # No non-canonical assignments.
    for t in count_triples(need, 0, 2):
        value = pref[0][t[0]] + pref[1][t[1]] + pref[2][t[2]]
        if value > ans:
            ans = value

    # One non-canonical assignment.
    length = need - 1
    for target in range(3):
        parity = 1 << target
        for t in count_triples(length, parity, 3):
            cand = []
            for source in range(3):
                if source != target:
                    cand.extend(candidates(source, target, t[source]))

            for idx in cand:
                value = remaining_value(t, (idx,))
                if value is not None:
                    value += cakes[idx][target]
                    if value > ans:
                        ans = value

    # Two non-canonical assignments.
    if need >= 2:
        length = need - 2
        for target1 in range(3):
            for target2 in range(3):
                parity = (1 << target1) ^ (1 << target2)

                for t in count_triples(length, parity, 4):
                    cand1 = []
                    cand2 = []

                    for source in range(3):
                        if source != target1:
                            cand1.extend(candidates(source, target1, t[source]))
                        if source != target2:
                            cand2.extend(candidates(source, target2, t[source]))

                    for i in cand1:
                        vi = cakes[i][target1]
                        for j in cand2:
                            if i == j:
                                continue
                            value = remaining_value(t, (i, j))
                            if value is not None:
                                value += vi + cakes[j][target2]
                                if value > ans:
                                    ans = value

    return ans


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    t = next(it)
    out = []

    for _ in range(t):
        n = next(it)
        k = next(it)
        cakes = [(next(it), next(it), next(it)) for _ in range(n)]
        out.append(str(solve_case(n, k, cakes)))

    print("\n".join(out))


if __name__ == "__main__":
    main()