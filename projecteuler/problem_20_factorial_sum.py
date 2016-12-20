import math

number = 100
fact = math.factorial(number)

digits = []

while fact > 0:
    digit = fact % 10
    digits.append(digit)

    fact = fact / 10

print sum(digits)
