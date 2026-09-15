from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        OFF = total
        target_pos = k + OFF
        target_bit = (1 << target_pos) if target_pos >= 0 else 0

        # ---------------- Positive-product DP ----------------
        # even[p] / odd[p] = bitset of alternating sums of NON-EMPTY, zero-free
        # subsequences whose element-count parity is even / odd and product is p.
        # Sum s is stored at bit (s + OFF).  Taking value x at even parity adds x
        # (left shift), at odd parity subtracts x (right shift).
        even = {}
        odd = {}
        for x in nums:
            if x == 0 or x > limit:
                # zero handled by the second DP; x>limit can never fit a positive product
                continue
            add_e = {}
            add_o = {}
            # take x after an even-length subsequence -> odd length, sum += x
            for p, b in even.items():
                np = p * x
                if np <= limit:
                    nb = b << x
                    if np in add_o:
                        add_o[np] |= nb
                    else:
                        add_o[np] = nb
            # take x after an odd-length subsequence -> even length, sum -= x
            for p, b in odd.items():
                np = p * x
                if np <= limit:
                    nb = b >> x
                    if nb:
                        if np in add_e:
                            add_e[np] |= nb
                        else:
                            add_e[np] = nb
            # start a fresh subsequence with x (count 1 -> odd parity, product x, sum x)
            sb = 1 << (x + OFF)
            if x in add_o:
                add_o[x] |= sb
            else:
                add_o[x] = sb
            for np, b in add_e.items():
                if np in even:
                    even[np] |= b
                else:
                    even[np] = b
            for np, b in add_o.items():
                if np in odd:
                    odd[np] |= b
                else:
                    odd[np] = b

        if target_bit:
            best = -1
            for p, b in odd.items():
                if p > best and (b & target_bit):
                    best = p
            for p, b in even.items():
                if p > best and (b & target_bit):
                    best = p
            if best != -1:
                return best

        # ---------------- Zero-product reachability ----------------
        # Any subsequence containing a zero has product 0 <= limit, so no cap applies.
        # E0/E1: zero-free subsequences with even/odd count; Z0/Z1: contain >=1 zero.
        E0 = E1 = Z0 = Z1 = 0
        for x in nums:
            nE0, nE1 = E0, E1
            nZ0, nZ1 = Z0, Z1
            if x == 0:
                nZ1 |= E0          # even, zero-free + zero -> odd, has zero, sum+0
                nZ0 |= E1          # odd, zero-free + zero -> even, has zero, sum-0
                nZ1 |= Z0
                nZ0 |= Z1
                nZ1 |= (1 << OFF)  # start with the single element 0
            else:
                nE1 |= E0 << x
                nE0 |= E1 >> x
                nZ1 |= Z0 << x
                nZ0 |= Z1 >> x
                nE1 |= (1 << (x + OFF))  # start with x (zero-free)
            E0, E1, Z0, Z1 = nE0, nE1, nZ0, nZ1

        if target_bit and ((Z0 | Z1) & target_bit):
            return 0
        return -1