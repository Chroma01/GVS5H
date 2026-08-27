from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        if k < -total or k > total:
            return -1

        # State index:
        # 2 * (alternating_sum + total) + length_parity
        # Each state stores reachable products as a bitset.
        state_count = (2 * total + 1) * 2
        dp = [0] * state_count
        active = []

        product_mask = (1 << (limit + 1)) - 1
        transform_tables = {}

        def get_transform_table(x: int):
            table = transform_tables.get(x)
            if table is not None:
                return table

            # table[mask] maps every set bit p in a 16-bit mask
            # to the bit representing product p * x.
            table = [0] * 65536
            for mask in range(1, 65536):
                low = mask & -mask
                bit_position = low.bit_length() - 1
                table[mask] = table[mask ^ low] | (1 << (bit_position * x))

            transform_tables[x] = table
            return table

        def add_state(target: int, bits: int, next_dp, next_active) -> None:
            if bits == 0:
                return
            if next_dp[target] == 0:
                next_active.append(target)
            next_dp[target] |= bits

        for x in nums:
            next_dp = dp.copy()
            next_active = active.copy()

            # Start a new singleton only when its product is within limit.
            # This prevents values such as nums=[12], limit=1 from becoming
            # incorrectly reachable.
            if x <= limit:
                singleton = (total + x) * 2 + 1
                add_state(singleton, 1 << x, next_dp, next_active)

            for index in active:
                product_bits = dp[index]
                parity = index & 1

                if parity == 0:
                    target = index + 2 * x + 1
                else:
                    target = index - 2 * x - 1

                if x == 0:
                    transformed = 1
                elif x == 1:
                    transformed = product_bits
                else:
                    source_limit = limit // x
                    bits = product_bits & ((1 << (source_limit + 1)) - 1)
                    if not bits:
                        continue

                    table = get_transform_table(x)
                    transformed = 0
                    chunk_index = 0

                    while bits:
                        chunk = bits & 0xFFFF
                        if chunk:
                            source_base = chunk_index * 16
                            transformed |= table[chunk] << (source_base * x)
                        bits >>= 16
                        chunk_index += 1

                    transformed &= product_mask

                add_state(target, transformed, next_dp, next_active)

            dp = next_dp
            active = next_active

        answer_bits = dp[(total + k) * 2] | dp[(total + k) * 2 + 1]
        if answer_bits == 0:
            return -1

        return answer_bits.bit_length() - 1