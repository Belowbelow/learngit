# try:
# 	print("try...")
# 	r = 10/0
# 	print("result:", r)
# except ZeroDivisionError as e:
# 	print("except:", e)
# finally:
# 	print("finally")

# import logging

# #error
# def foo(s):
# 	return 10 / int(s)

# def bar(s):
# 	return foo(s) * 2

# def main():
# 	try:
# 		bar('0')
# 	except Exception as e:
# 		logging.exception(e)
# print(main())

from functools import reduce

def str2num(s):
   	if '.' in s:
   		return float(s)
   	else:
   		return int(s)

def calc(exp):
    ss = exp.split('+')
    ns = map(str2num, ss)
    return reduce(lambda acc, x: acc + x, ns)

def main():
    r = calc('100 + 200 + 345')
    print('100 + 200 + 345 =', r)
    r = calc('99 + 88 + 7.6')
    print('99 + 88 + 7.6 =', r)

main()