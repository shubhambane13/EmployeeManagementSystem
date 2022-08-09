from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import pandas as pd
import requests
import bs4
import matplotlib.pyplot as plt

def f1():						# main window add button
	add_window.deiconify()
	main_window.withdraw()
	

def f3():						# view window back button
	main_window.deiconify()
	view_window.withdraw()

def f4():						# add window save button

	con = None
	try:
		id = int(aw_ent_id.get())
		name = aw_ent_name.get()
		salary = float(aw_ent_salary.get())
		if id < 1:
			showerror("Faliure", "issue enter positive number")
		elif name.isalpha() == False:
			showerror("Faliure","issue name should contain alphabets only")
		elif len(name) == 0 :
			showerror("Failure", "issue name should not be empty")
		elif len(name) < 2:
			showerror("Faliure", "issue enter name should contain min 2 alphabets")
		elif salary < 8000:	
			showerror("Faliure", "issue enter salary should be min of 8k")
		else:
			con = connect("svb.db")
			cursor = con.cursor()
			sql= "insert into employee values('%d', '%s', '%f')"
			cursor.execute(sql % (id, name, salary))

			con.commit()
			showinfo("Success", "record added")
			con.rollback()
	except Error:
		showerror("Faliure", "ID already exists")
	except ValueError:
		showerror("Faliure", "Plz enter integer")
	except Exception as e:
		showerror("Faliure", "issue", e)
	finally:
		aw_ent_id.delete(0, END)
		aw_ent_name.delete(0, END)
		aw_ent_salary.delete(0, END)
		if con is not None:
			con.close()

def f5():						# main window update button
	update_window.deiconify()
	main_window.withdraw()

def f6():						# update window update button
	con = None
	try:
		id = int(uw_ent_id.get())
		name = uw_ent_name.get()
		salary = float(uw_ent_salary.get())
		if id < 1:
			showerror("Faliure", "issue enter positive number")
		elif len(name) == 0 :
			showerror("Failure", "issue name should not be empty")
		elif name.isalpha() == False:
			showerror("Faliure","issue plz enter alphabets")
		elif len(name) < 2:
			showerror("Faliure", "issue enter name should contain min 2 alphabets")
		elif salary < 8000:	
			showerror("Faliure", "issue enter salary should be min of 8k")
		else:
			con = connect("svb.db")
			cursor = con.cursor()
			sql = "update employee set name = '%s', salary = '%d' where id = '%d'"
			cursor.execute(sql % (name, salary, id))
			if cursor.rowcount == 1:
				con.commit()
				showinfo("Success", "record updated")
			else:
				showerror("Faliure", "record does not exists")
	except ValueError:
		showerror("Faliure", "Enter integer")	
	except Exception as e:
		showerror("Faliure", "issue", e)
	finally:
		uw_ent_id.delete(0, END)
		uw_ent_name.delete(0, END)
		uw_ent_salary.delete(0, END)
		if con is not None:
			con.close()


def f7():						# update window back button
	main_window.deiconify()
	update_window.withdraw()	
	
def f8():						# main window delete button
	delete_window.deiconify()
	main_window.withdraw()


def f9():						# delete window delete button
	con = None
	try:
		id = int(dw_ent_id.get())
		if id < 1:
			showerror("Faliure", "Enter positive integer")
		else:
			con = connect("svb.db")
			cursor = con.cursor()
			sql = "delete from employee where id = '%d'"
			id = int(dw_ent_id.get())
			cursor.execute(sql % (id))
			if cursor.rowcount == 1:
				con.commit()
				showinfo("Success", "record deleted")
			else:
				showerror("Faliure", "record does not exists")
	except ValueError:
		showerror("Faliure", "Enter integer")
	except Exception as e:
		showerror("issue", e)
	finally:
		dw_ent_id.delete(0, END)
		if con is not None:
			con.close()
		


def f10():						# delete window back button
	main_window.deiconify()
	delete_window.withdraw()

def f11():						# main window qotd label
	try:
		wa = "https://www.brainyquote.com/quote_of_the_day"
		res = requests.get(wa)
	
		data = bs4.BeautifulSoup(res.content, "html.parser")
		
		info = data.find("img", {"class":"p-qotd"})
		q1 = "Quote Of The Day:\n"
		q2 = info["alt"]
		quo = ""
		for d in q2:
			if d == '-':
				quo += "\n -"
			else:
				quo += d
			q = q1 + quo
		return q
	except Exception as e:
		showerror("issue", e)

def f12():						# add window back button
	main_window.deiconify()
	add_window.withdraw()


def f13():						# main window view button
	view_window.deiconify()
	main_window.withdraw()
	vw_st_data.delete(1.0, END)
	info = ""
	con = None
	try:
		con = connect("svb.db")
		cursor = con.cursor()
		sql = "select * from employee"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info+"id: "+str(d[0])+"  name: "+str(d[1])+"  sal: "+str(d[2])+"\n"
		vw_st_data.insert(INSERT, info)
	except Exception as e:
		showerror("Faliure", e)
	finally:
		if con is not None:
			con.close()

def f14():						# main window chart button
	try:
		con = connect("svb.db")
		sql = "select name, salary from employee order by [salary] desc"
		df = pd.read_sql_query(sql, con)

		data = df.head()

		name = data["name"].tolist()
		sal = data["salary"].tolist()
	
		plt.bar(name, sal, width=0.25, label="salary")
		plt.xlabel("Names")
		plt.ylabel("Salary")
		plt.legend(shadow=True)
		plt.title("Employee Management System")
		plt.grid()
		plt.show()
	except Exception as e:
		showerror("issue ", e)
	finally:
		if con is not None:
			con.close()


#****************************************************************************


f = ("Arial", 20, "bold")
f2 = ("Arial", 15, "bold")


# ---------------------Main window------------------------------


main_window = Tk()
main_window.title("E. M. S.")
main_window.geometry("1000x500+200+100")

mw_btn_add = Button(main_window, text="Add", font=f, width=10, bd=3, command=f1)
mw_btn_view = Button(main_window, text="View", font=f, width=10, bd=3, command=f13)
mw_btn_update = Button(main_window, text="Update", font=f, width=10, bd=3, command=f5)
mw_btn_delete = Button(main_window, text="Delete", font=f, width=10, bd=3, command=f8)
mw_btn_charts = Button(main_window, text="Charts", font=f, width=10, bd=3, command=f14)
mw_lbl_qotd = Label(main_window, text=f11(), font=f, bd=3,)

mw_btn_add.pack(pady=5)
mw_btn_view.pack(pady=5)
mw_btn_update.pack(pady=5)
mw_btn_delete.pack(pady=5)
mw_btn_charts.pack(pady=5)
mw_lbl_qotd.pack(pady=15)


#------------------Add window-------------------------


add_window = Toplevel(main_window)
add_window.title("Add Employee")
add_window.geometry("1000x500+200+100")
add_window.withdraw()

aw_lb_id = Label(add_window, text="Enter id:", font=f)
aw_ent_id = Entry(add_window, font=f)
aw_lb_name = Label(add_window, text="Enter name:", font=f)
aw_ent_name = Entry(add_window, font=f)
aw_lb_salary = Label(add_window, text="Enter salary:", font=f)
aw_ent_salary = Entry(add_window, font=f)
aw_btn_save = Button(add_window, text="Save", font=f, bd=3, command=f4)
aw_btn_back = Button(add_window, text="Back", font=f, bd=3, command=f12)

aw_lb_id.pack(pady=5)
aw_ent_id.pack(pady=5)
aw_lb_name.pack(pady=5)
aw_ent_name.pack(pady=5)
aw_lb_salary.pack(pady=5)
aw_ent_salary.pack(pady=5)
aw_btn_save.pack(pady=5)
aw_btn_back.pack(pady=5)


#---------------------view window------------------------------


view_window = Toplevel(main_window)
view_window.title("View Employee")
view_window.geometry("1000x500+200+100")
view_window.withdraw()

vw_st_data = ScrolledText(view_window, width=40, height=10, font=f)
vw_btn_back = Button(view_window, text="Back", font=f, bd=3, command=f3)

vw_st_data.pack(pady=5)
vw_btn_back.pack(pady=5)


#--------------------update window---------------------------


update_window = Toplevel(main_window)
update_window.title("Update Employee")
update_window.geometry("1000x500+200+100")
update_window.withdraw()

uw_lb_id = Label(update_window, text="Enter id:", font=f)
uw_ent_id = Entry(update_window, font=f)
uw_lb_name = Label(update_window, text="Enter name:", font=f)
uw_ent_name = Entry(update_window, font=f)
uw_lb_salary = Label(update_window, text="Enter salary:", font=f)
uw_ent_salary = Entry(update_window, font=f)
uw_btn_update = Button(update_window, text="Update", font=f, bd=3, command=f6)
uw_btn_back = Button(update_window, text="Back", font=f, bd=3, command=f7)

uw_lb_id.pack(pady=5)
uw_ent_id.pack(pady=5)
uw_lb_name.pack(pady=5)
uw_ent_name.pack(pady=5)
uw_lb_salary.pack(pady=5)
uw_ent_salary.pack(pady=5)
uw_btn_update.pack(pady=5)
uw_btn_back.pack(pady=5)


#----------------------delete window--------------------------


delete_window = Toplevel(main_window)
delete_window.title("Delete student")
delete_window.geometry("1000x500+200+100")
delete_window.withdraw()

dw_lb_id = Label(delete_window, text="Enter id to be deleted", font=f)
dw_ent_id = Entry(delete_window, font=f)
dw_button_delete = Button(delete_window, text="Delete", font=f, command=f9)
dw_button_back = Button(delete_window, text="Back", font=f, bd=3, command=f10)

dw_lb_id.pack(pady=5)
dw_ent_id.pack(pady=5)
dw_button_delete.pack(pady=5)
dw_button_back.pack(pady=5)


main_window.mainloop()