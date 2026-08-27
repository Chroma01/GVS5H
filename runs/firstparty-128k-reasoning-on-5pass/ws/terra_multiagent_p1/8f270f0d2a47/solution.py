class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        max_len = len(str(r))

        fact = [1] * 10
        for i in range(1, 10):
            fact[i] = fact[i - 1] * i

        beautiful = [[] for _ in range(max_len + 1)]
        totals = [0] * (max_len + 1)
        counts = [0] * 10

        def no_leading_zero_permutations(cnt, n):
            denom = 1
            for amount in cnt:
                denom *= fact[amount]

            total = fact[n] // denom

            if cnt[0]:
                zero_first_denom = fact[cnt[0] - 1]
                for digit in range(1, 10):
                    zero_first_denom *= fact[cnt[digit]]
                total -= fact[n - 1] // zero_first_denom

            return total

        def generate(digit, left, digit_sum, product, length):
            if digit == 10:
                if left != 0 or digit_sum == 0:
                    return

                # A zero digit makes the digit product zero.
                if counts[0] > 0 or product % digit_sum == 0:
                    vec = tuple(counts)
                    beautiful[length].append(vec)
                    totals[length] += no_leading_zero_permutations(vec, length)
                return

            power = 1
            for take in range(left + 1):
                counts[digit] = take
                generate(
                    digit + 1,
                    left - take,
                    digit_sum + digit * take,
                    product * power,
                    length,
                )
                if digit:
                    power *= digit
            counts[digit] = 0

        for length in range(1, max_len + 1):
            generate(0, length, 0, 1, length)

        def permutations_after_choice(cnt, chosen, remaining):
            denom = 1
            for digit in range(10):
                amount = cnt[digit] - (1 if digit == chosen else 0)
                denom *= fact[amount]
            return fact[remaining] // denom

        def count_up_to(bound):
            if bound <= 0:
                return 0

            digits = list(map(int, str(bound)))
            n = len(digits)

            answer = sum(totals[1:n])

            for vec in beautiful[n]:
                cnt = list(vec)
                valid = True

                for pos, limit in enumerate(digits):
                    remaining = n - pos - 1
                    lower = 1 if pos == 0 else 0

                    for digit in range(lower, limit):
                        if cnt[digit]:
                            answer += permutations_after_choice(
                                cnt, digit, remaining
                            )

                    if cnt[limit] == 0:
                        valid = False
                        break

                    cnt[limit] -= 1

                if valid:
                    answer += 1

            return answer

        return count_up_to(r) - count_up_to(l - 1)