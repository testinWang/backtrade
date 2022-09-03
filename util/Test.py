import math
rate = 0.25*(0.15 * 2 + 0.12 * 2 + 0.08 * 3 + 0.06 * 1) - 0.25 * (0.06 * 6)
rate = round(rate, 3)
print('月收益率:{}'.format(rate))

first_year = [round(math.pow(1+rate, i), 2) for i in range(1, 11)]
second_year = [round(math.pow(1+rate, i), 2) for i in range(11, 21)]
print('首年复利:', first_year)
print('次年复利:', second_year)