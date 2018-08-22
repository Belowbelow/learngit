menu_tuple = ("员工信息系统（Python版）", "\t1:添加员工信息", "\t2:打印员工所有信息", "\t3:通过员工编号查找信息", "\t0:退出系统")
emp_tuple = ("ID", "Name", "Title", "Phone")
emp_list = []
emp_dict = {}

judge = 1
while judge != 0:
    for i in menu_tuple:
        print(i)
    choice = input("请输入您想使用的功能序号：")
    if choice == 1:
        print( "添加员工信息")
        emp_add(emp_list,emp_dict)
    elif choice == 2:
        print ("列表打印所有员工信息")
        emp_list_p(emp_list, emp_tuple)
    elif choice == 3:
        print( "通过员工编号查询员工信息")
        emp_find(emp_dict, emp_tuple)
    elif choice == 0:
        print( "退出系统" + "\n" + "您已成功退出系统!")
        judge = 0

def emp_add(list, dict):
	pass

def emp_list_p(list, tuple):
	pass

def emp_find(dict, tuple):
	pass