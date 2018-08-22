# _*_ coding: UTF-8 _*_

year = int(input("year:"))
month = int(input("month:"))
day = int(input("day:"))

months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

result = 0

if year%4 == 0 or year%400 == 0 and year%100 != 0:
	for i in range(0, month-1):
		result += months[i]
	result += day
	result += 1
else:
	for i in range(0, month-1):
		result += months[i]
	result += day

print("Number of days: {}".format(result))

