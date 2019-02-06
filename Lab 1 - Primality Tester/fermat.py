import random


def prime_test(n, k):
    # This is the main function connected to the Test button. You don't need to touch it.
    return run_fermat(n, k), run_miller_rabin(n, k)


def mod_exp(x, y, n):  # O(n^3)
    # You will need to implement this function and change the return value.
    if y == 0:  # If you raise anything to the 0 power the answer is 1
        return 1  # O(1)

    z = mod_exp(x, y // 2, n)  # Recursively set z and floor y

    if y % 2 == 0:  # Check if y is even
        return (z ** 2) % n  # O(n^2)
    else:  # y is odd
        return (x * (z ** 2)) % n  # O(n^2)
    

def fprobability(k):
    # You will need to implement this function and change the return value.
    return 1 - (1 / (2 ** k))  # Probability of error algorithm


def mprobability(k):
    # You will need to implement this function and change the return value.
    return 1 - (0.25 ** k)  # Probability we are wrong, subtracted from 100%


def run_fermat(n, k):  # O(n^4)
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likely want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    if n == 1 or n == 0:  # O(1)
        return 'composite'

    for i in range(0, k):  # Here we assume k is equal to n bits
        a = random.randint(1, n - 1)  # O(1)
        mod = mod_exp(a, n - 1, n)  # O(n^3) for one loop
        if mod != 1:  # O(1)
            return 'composite'  # Number is not prime
    return 'prime'  # Number is prime


def run_miller_rabin(n, k):  # O(n^5)
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likely want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    if n == 1 or n == 0:  # O(1)
        return 'composite'
    elif n == 2:  # O(1)
        return 'prime'

    for i in range(0, k):  # Here we assume k is equal to n bits
        a = random.randint(1, n - 1)  # O(1)
        exp = n - 1  # O(n)
        mod = 1  # O(1)

        while mod == 1:
            if exp == 1 or exp == 0:  # If the exponent is 0 or 1 break out of the loop
                break
            mod = mod_exp(a, exp, n)  # O(n^4)
            exp = exp // 2  # Cut the exponent in half and floor it

            if mod != -1 and mod != 1:  # Check the result of modular exponentiation
                mod = mod - n  # Adjust accordingly

            if exp % 2 != 0:  # Check to see if the exponent is even or odd and break accordingly
                break
        if mod != -1 and mod != 1:  # Finally, if our result is not 1 or -1, the number is not prime
            return 'composite'  # Number is not prime
    return 'prime'  # Number is prime
