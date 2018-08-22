# _*_ coding: UTF-8 _*_

def fib(n):
	a, b = 0, 1
	for i in range(n):
		print(b)
		a, b = b, a+b

x = int(input("Numbers of fibonacci list: "))
fib(x)