from enum import Enum, unique

Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

for name, member in Month.__members__.items():
	print(name, '=>', member, ',', member.value)

print(Month)
print(Month.__members__)
print(Month.__members__.items())

@unique
class Week(Enum):
	Sun = 0
	Mon = 1
	Tue = 2
	Wed = 3
	Thu = 4
	Fri = 5
	Sat = 6

day1 = Week.Mon
print(day1)
print(Week.Tue)
print(Week['Sun'])

for name, memeber in Week.__members__.items():
	print(name, '=>', member)

