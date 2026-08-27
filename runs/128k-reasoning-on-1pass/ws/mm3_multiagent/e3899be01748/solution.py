class Solution:
    def countSubstrings(self, s: str) -> int:
        # Precompute for each digit d = 1..9
        p0_arr = [0] * 10
        p_arr = [0] * 10
        factor_arr = [None] * 10
        periodic_factors_arr = [None] * 10
        need_arr = [None] * 10
        pre_arr = [None] * 10
        periodic_arr = [None] * 10
        cur_periodic_arr = [0] * 10
        cur_rem_arr = [0] * 10

        for d in range(1, 10):
            # Compute the sequence of 10^L mod d and find preperiod p0 and period p
            seen = {}
            cur = 10 % d
            flist = []
            L = 1
            while True:
                if cur in seen:
                    p0 = seen[cur]
                    p = L - 1 - seen[cur]
                    break
                seen[cur] = L - 1
                flist.append(cur)
                cur = (cur * 10) % d
                L += 1
            p0_arr[d] = p0
            p_arr[d] = p
            factor_arr[d] = flist
            # Periodic factors (for L > p0)
            if p > 0:
                periodic_factors_arr[d] = flist[p0:]
            else:
                periodic_factors_arr[d] = []

            # Precompute need[d][f][t] = list of a such that (a * f) % d == t
            need = [[[] for _ in range(d)] for _ in range(d)]
            for f in range(d):
                for t in range(d):
                    lst = []
                    for a in range(d):
                        if (a * f) % d == t:
                            lst.append(a)
                    need[f][t] = lst
            need_arr[d] = need

            # Initialize buckets
            if p0 > 0:
                pre_arr[d] = [[0] * d for _ in range(p0)]
            else:
                pre_arr[d] = []
            periodic_arr[d] = [[0] * d for _ in range(p)]
            cur_periodic_arr[d] = 0
            cur_rem_arr[d] = 0
            # Insert the empty prefix (pref[0] = 0)
            if p0 > 0:
                pre_arr[d][0][0] = 1
            else:
                periodic_arr[d][0][0] = 1

        ans = 0
        n = len(s)
        for r in range(n):
            digit = int(s[r])
            if digit != 0:
                d = digit
                # Current prefix remainder pref[r+1] % d
                cur_pref_rem = (cur_rem_arr[d] * 10 + digit) % d

                # Count substrings ending at r using preperiod buckets
                p0 = p0_arr[d]
                for i in range(p0):
                    bucket = pre_arr[d][i]
                    f = factor_arr[d][i]
                    if f == 0:
                        if cur_pref_rem == 0:
                            ans += sum(bucket)
                    else:
                        for a in need_arr[d][f][cur_pref_rem]:
                            ans += bucket[a]

                # Count substrings ending at r using periodic buckets
                p = p_arr[d]
                cur_p = cur_periodic_arr[d]
                per = periodic_arr[d]
                pf = periodic_factors_arr[d]
                for k in range(p):
                    bucket_idx = (cur_p + k) % p
                    bucket = per[bucket_idx]
                    f = pf[k]
                    if f == 0:
                        if cur_pref_rem == 0:
                            ans += sum(bucket)
                    else:
                        for a in need_arr[d][f][cur_pref_rem]:
                            ans += bucket[a]

            # Update cur_rem for all d (pref[r+1] % d)
            for d in range(1, 10):
                cur_rem_arr[d] = (cur_rem_arr[d] * 10 + digit) % d

            # Update buckets for all d to prepare for next position
            for d in range(1, 10):
                p0 = p0_arr[d]
                p = p_arr[d]
                # Rotate periodic buffer (simulate L increase by 1)
                cur_periodic_arr[d] = (cur_periodic_arr[d] - 1) % p
                if p0 > 0:
                    # The bucket that was at L = p0 moves to periodic part (offset 0)
                    moving = pre_arr[d][p0 - 1]
                    # Shift preperiod buckets: L = i becomes L = i+1
                    for i in range(p0 - 1, 0, -1):
                        pre_arr[d][i] = pre_arr[d][i - 1]
                    # Insert new prefix (L = 1) into preperiod[0]
                    pre_arr[d][0] = [0] * d
                    pre_arr[d][0][cur_rem_arr[d]] = 1
                    # Add the moved bucket to periodic buffer at offset 0
                    target = periodic_arr[d][cur_periodic_arr[d]]
                    for a in range(d):
                        target[a] += moving[a]
                else:
                    # p0 == 0: insert new prefix directly into periodic buffer at offset 0
                    periodic_arr[d][cur_periodic_arr[d]][cur_rem_arr[d]] += 1

        return ans