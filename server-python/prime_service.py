def is_prime(n):
    if n < 2:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True


def factorize(n):
    factors = []
    divisor = 2

    while n > 1:
        if n % divisor == 0:
            factors.append(divisor)
            n = n // divisor
        else:
            divisor += 1

    return factors
