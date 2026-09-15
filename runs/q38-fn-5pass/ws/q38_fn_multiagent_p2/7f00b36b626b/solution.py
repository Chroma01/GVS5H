from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        limit = threshold + 1

        # Keep only unique relevant values (<= threshold).
        # Values > threshold are isolated because lcm(a, b) >= max(a, b).
        seen = bytearray(limit)
        vals = []
        isolated = 0
        has_one = False

        for x in nums:
            if x <= threshold:
                if not seen[x]:
                    seen[x] = 1
                    if x == 1:
                        has_one = True
                    vals.append(x)
            else:
                isolated += 1

        m = len(vals)
        if m == 0:
            return isolated

        # If 1 is present, it connects to every relevant value.
        # If there is only one unique relevant value, it is one component.
        if has_one or m == 1:
            return isolated + 1

        # DSU with negative sizes.
        parent = [-1] * m

        def find(x: int, par=parent) -> int:
            while par[x] >= 0:
                p = par[x]
                gp = par[p]
                if gp >= 0:
                    par[x] = gp
                    x = gp
                else:
                    x = p
            return x

        # first[m] stores one DSU node among present values that divide m.
        first = [-1] * limit
        comps = m

        par = parent
        fst = first
        find_root = find

        for idx, x in enumerate(vals):
            root = find_root(idx)

            # Every multiple m of x is a possible witness L with x | L.
            for multiple in range(x, limit, x):
                f = fst[multiple]

                if f == -1:
                    fst[multiple] = root
                elif f != root:
                    rf = find_root(f)

                    if rf != root:
                        # Union by size. Keep `root` as the new root.
                        if par[root] > par[rf]:
                            root, rf = rf, root

                        par[root] += par[rf]
                        par[rf] = root
                        comps -= 1

                    # Refresh this bucket entry to the current root.
                    fst[multiple] = root

        return comps + isolated


if __name__ == "__main__":
    sol = Solution()

    tests = [
        ("example1", [2, 4, 8, 3, 9], 5, 4),
        ("example2", [2, 4, 8, 3, 9, 12], 10, 2),

        ("threshold_1_with_one", [1, 2, 3], 1, 3),
        ("threshold_1_without_one", [2, 3], 1, 2),

        ("all_greater_than_threshold", [100, 200, 300], 50, 3),
        ("one_greater_than_threshold", [1, 100], 50, 2),

        ("dense_small_no_one_10", list(range(2, 11)), 10, 2),
        ("dense_small_no_one_100", list(range(2, 101)), 100, 11),
        ("dense_small_with_one", list(range(1, 101)), 100, 1),

        ("lcm_boundary_29", [6, 10, 15], 29, 3),
        ("lcm_boundary_30", [6, 10, 15], 30, 1),

        ("duplicate_relevant", [2, 2], 2, 1),
        ("duplicate_isolated", [100, 100], 50, 2),
    ]

    all_pass = True
    for name, nums, threshold, expected in tests:
        got = sol.countComponents(nums, threshold)
        ok = got == expected
        all_pass = all_pass and ok
        print(f"{'PASS' if ok else 'FAIL'}: {name} expected={expected} got={got}")

    print("ALL PASS" if all_pass else "SOME FAIL")