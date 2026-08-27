class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        # last_nz[i] = index of nearest non-zero digit to the left of i (inclusive), -1 if none
        last_nz = [-1] * n
        for i, ch in enumerate(s):
            if ch != '0':
                last_nz[i] = i
            else:
                last_nz[i] = last_nz[i-1] if i > 0 else -1

        # Precompute prefix values and transformed prefixes for d in {3,6,7,9}
        # For d=6 we will use the same logic as d=3 (mod 3), but only when d=6.
        # We'll store tp[d][k] = pref[k] * inv10_pow[k] mod d
        # We only need tp for the sliding window; we can compute on the fly while scanning.

        # Precompute modular inverses of 10 mod d for d where gcd(10,d)=1
        inv10_mod = {}
        for d in (3, 7, 9):
            # find x such that 10*x % d == 1
            for x in range(1, d):
                if (10 * x) % d == 1:
                    inv10_mod[d] = x
                    break

        # Precompute powers of inv10 for each d
        inv10_pow = {d: [1] * (n + 1) for d in (3, 7, 9)}
        for d in (3, 7, 9):
            inv = inv10_mod[d]
            for k in range(1, n + 1):
                inv10_pow[d][k] = (inv10_pow[d][k-1] * inv) % d

        # Compute prefix values mod d and transformed prefixes tp for d in {3,6,7,9}
        # We'll store pref[d][k] and tp[d][k]
        pref = {d: [0] * (n + 1) for d in (3, 6, 7, 9)}
        tp = {d: [0] * (n + 1) for d in (3, 6, 7, 9)}
        for d in (3, 6, 7, 9):
            for i, ch in enumerate(s):
                digit = ord(ch) - 48
                pref[d][i+1] = (pref[d][i] * 10 + digit) % d
                # transformed prefix only defined when d coprime to 10 (3,7,9). For d=6 we use d=3 logic.
                if d in (3, 7, 9):
                    tp[d][i+1] = (pref[d][i+1] * inv10_pow[d][i+1]) % d
                else:
                    # d==6: we will use pref[3] (mod 3) as the key, same as d=3 transformed.
                    # We'll handle d=6 later using the same key as d=3.
                    pass

        # For d=6 we use the same key as d=3: pref[3][k] (since 10%3==1, transformed prefix equals original).
        # So we can reuse tp[3] for d=6.
        # We'll treat d=6 by using the same array as d=3.

        ans = 0
        # Sliding window pointers and frequency maps for each d we need to query.
        # We'll maintain for each d in (3,6,7,9) a dict of counts of tp values for indices <= current limit.
        # Since d is small, we can use lists of size d.
        limit = -1
        cnt = {d: [0] * d for d in (3, 6, 7, 9)}
        # Note: for d=6 we will use the same key as d=3, so we can store its counts in cnt[6] as well.
        # We'll fill cnt[6] using the same logic as d=3 but only when needed (i.e., when d==6).
        # Actually we can just maintain cnt[6] independently using pref[3] (mod 3) as key.
        # Since d=6's condition is pref[3][i] == pref[3][j+1] (mod 3), we can store the same as d=3.
        # So we can reuse cnt[3] for d=6. We'll just ensure we update cnt[3] for d=6 as well.
        # Simpler: treat d=6 as d=3 for counting, but we must not double count when d=3 itself.
        # So we'll handle d=6 in a separate branch that uses the same key but we must not add to cnt[3] twice.
        # Instead, we can maintain a separate count array for d=6, but since the key is the same, we can reuse cnt[3] for d=6.
        # We'll decide: for d=6, we use the same key as d=3, and we will update cnt[3] for d=6 as well.
        # But to avoid updating cnt[3] for both d=3 and d=6 at the same time, we can just handle d=6 in the same pass.
        # We'll keep a single array cnt3[3] for the key mod 3. We'll update it whenever we need to include a new index,
        # and for both d=3 and d=6 we query it. However we must be careful: for d=3, we need to count i <= p,
        # and for d=6, we also need i <= p (the p for d=6 is the same as for d=6). So we can use the same cnt3 array.
        # So we will maintain cnt3 array for mod 3 keys.
        cnt3 = [0] * 3  # for keys 0,1,2 (mod 3)
        # We will also maintain cnt7 and cnt9 for d=7 and d=9.
        cnt7 = [0] * 7
        cnt9 = [0] * 9

        # We'll also need to know for each j the key for d=3 (pref3[j+1] % 3) and for d=6 (same as d=3).
        # For d=7 and d=9 we have tp[7][j+1] and tp[9][j+1].

        for j in range(n):
            p = last_nz[j]
            if p == -1:
                continue
            d = ord(s[p]) - 48
            # Ensure the sliding window includes all indices up to p
            while limit < p:
                limit += 1
                # Add index limit to the relevant count arrays
                # For d=3 and d=6 (both use key pref3[limit] % 3)
                key3 = pref[3][limit]  # already mod 3
                cnt3[key3] += 1
                # For d=7
                key7 = tp[7][limit] if 7 in tp else 0
                cnt7[key7] += 1
                # For d=9
                key9 = tp[9][limit] if 9 in tp else 0
                cnt9[key9] += 1

            if d == 1 or d == 2 or d == 5:
                ans += p + 1
            elif d == 4:
                # Check divisibility by 4
                # s[j] is either '0' (if p < j) or '4' (if p == j)
                if s[j] == '0':
                    # need tens digit even
                    if j - 1 >= 0 and (ord(s[j-1]) - 48) % 2 == 0:
                        ans += p + 1
                else:  # s[j] == '4'
                    # length 1 substring (i=j) always valid
                    # longer substrings valid if tens digit even
                    if j - 1 >= 0 and (ord(s[j-1]) - 48) % 2 == 0:
                        ans += p  # i from 0 to j-1
                    else:
                        # only i=j is valid
                        ans += 1
            elif d == 8:
                # Compute contributions
                # Case 1: i <= min(p, j-2) -> length >=3
                cnt3_len = 0
                if j >= 2:
                    # three-digit number s[j-2..j]
                    three = (ord(s[j-2]) - 48) * 100 + (ord(s[j-1]) - 48) * 10 + (ord(s[j]) - 48)
                    if three % 8 == 0:
                        # all i <= min(p, j-2) are valid
                        max_i = min(p, j-2)
                        if max_i >= 0:
                            cnt3_len = max_i + 1
                # Case 2: i = j-1 (length 2)
                cnt2_len = 0
                if j >= 1 and p == j-1:
                    two = (ord(s[j-1]) - 48) * 10 + (ord(s[j]) - 48)
                    if two % 8 == 0:
                        cnt2_len = 1
                # Case 3: i = j (length 1)
                cnt1_len = 0
                if p == j and s[j] == '8':
                    cnt1_len = 1
                ans += cnt3_len + cnt2_len + cnt1_len
            elif d == 3:
                # Use transformed prefix for d=3 (which is same as pref mod 3)
                key = pref[3][j+1]  # actually we need tp[3][j+1] but since 10%3=1, tp == pref
                # But we stored tp[3] earlier? We only stored for d in (3,7,9). Let's compute key using tp[3][j+1]
                key = tp[3][j+1]
                ans += cnt3[key]
            elif d == 6:
                # Use same key as d=3
                key = tp[3][j+1]  # since mod 3
                ans += cnt3[key]
            elif d == 7:
                key = tp[7][j+1]
                ans += cnt7[key]
            elif d == 9:
                key = tp[9][j+1]
                ans += cnt9[key]

        return ans