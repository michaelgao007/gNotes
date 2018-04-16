#! /usr/bin/env python3

from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk
import pymysql
import notesConfig

MYSQL_HOST = notesConfig.host
MYSQL_USER = notesConfig.user
MYSQL_PWD = notesConfig.pwd
MYSQL_DATABASE = notesConfig.dbName

class notesSearch(Frame):

	def __init__(self,root,dbHost,dbUser,dbPwd,dbName):

		Frame.__init__(self,root,pady = 10)
		self.grid(row = 0,column = 0)
		self.create_widgets()
		self.dbHost = dbHost
		self.dbUser = dbUser
		self.dbPwd = dbPwd
		self.dbName = dbName
		self.dbConnect = self.db_connect()

	def db_connect(self):

		try:

			db = pymysql.connect(self.dbHost,self.dbUser,self.dbPwd,self.dbName)

			return db

		except:

			messagebox.showwarning("Warning","Database Server Not Connected.")

	def sql_search(self):

		self.msgText.config(state = 'normal')
		self.msgText.delete('1.0',END)
		self.msgText.tag_config('title',foreground='red',font=('Arial', 12,'bold'))
		self.msgText.tag_config('text',foreground='black',font=('Arial', 12,'bold'))
		self.msgText.tag_config('lineSplit',foreground='blue',font=('Arial', 12,'bold'))

		keyWord = self.keyword.get()

		dbCursor = self.dbConnect.cursor()

		sqlCommand = "SELECT * FROM NotesSearch WHERE Title LIKE '%{0}%'".format(keyWord)
		print(sqlCommand)

		dbCursor.execute(sqlCommand)

		data = dbCursor.fetchall()

		for title,text in data:

			titleLine = title + '\n'
			tag = ('title',)
			self.msgText.insert(END,titleLine,tag)

			tag = ('text',)
			self.msgText.insert(END,text,tag)

			tag = ('lineSplit',)
			self.msgText.insert(END,"\n------------------------------------------------------------------------------------------------------------------------------------------------------\n\n",tag)

		self.msgText.config(state = 'disabled')
		self.keyword.set('')

	def sql_update(self):

		dbCursor = self.dbConnect.cursor()

		msg_title = self.title_Entry.get()
		msg_text = self.notesText.get('1.0',END)

		try:

			sqlUpdate = "INSERT INTO NotesSearch (Title,Text) VALUES ('{0}','{1}')".format(msg_title + '\n',msg_text)
			print(sqlUpdate)
			dbCursor.execute(sqlUpdate)
			self.dbConnect.commit()
			messagebox.showwarning("Warning","Database Update Completed.")

		except:

			messagebox.showwarning("Warning","Database Update Failed.")

	def clear_text(self):

		self.title_Entry.delete(0,END)
		self.notesText.delete('1.0',END)



	def new_window(self):

		self.newWindow=Toplevel(self)
		self.newWindow.title("Add New Notes")
		self.newWindow.transient(self)

		self.mainPanel = LabelFrame(self.newWindow,text = 'Notes Title')
		self.mainPanel.pack(fill = 'both',padx = 2)

		self.title_Label = Label(self.mainPanel,width = 12,text = 'Title:',foreground = 'red')
		self.title_Label.grid(row = 0,column = 0,sticky = 'we')

		self.title_Entry = StringVar()
		self.title_Entry = Entry(self.mainPanel,textvariable = self.title_Entry, width = 50)
		self.title_Entry.grid(row = 0,column = 1,pady = 3,sticky='we')
		self.title_Entry.focus()

		self.textPanel = LabelFrame(self.newWindow,text = 'Notes Text')
		self.textPanel.pack(fill = 'both',padx = 2)

		self.notesText = scrolledtext.ScrolledText(self.textPanel,wrap = 'word')
		self.notesText.grid(row = 1,column = 0, columnspan = 2, sticky = 'NEWS')

		self.updateButton = Button(self.textPanel, text = 'Update To Database',command = self.sql_update)
		self.updateButton.grid(row = 2, column = 0 ,sticky = 'we', padx =10,pady = 8)

		self.clrButton = Button(self.textPanel, text = 'Clear Text Area',command = self.clear_text)
		self.clrButton.grid(row = 2, column = 1 ,sticky = 'we', padx =10,pady = 8)

	def exit_program(self):

		self.dbConnect.close()
		root.quit()
		root.destroy()
		exit()

	def create_widgets(self):

		#--------------Status Panel--------------#
		self.statusPanel = LabelFrame(self,text = 'Main Panel')
		self.statusPanel.pack(fill = 'both',padx=2)

		self.keyword_Label = Label(self.statusPanel,width = 12,text = 'Keyword:',foreground = 'red')
		self.keyword_Label.grid(row = 0,column = 0,sticky = 'e')

		self.keyword = StringVar()
		self.keyword_Entry = Entry(self.statusPanel,textvariable = self.keyword)
		self.keyword_Entry.grid(row = 0,column = 1,sticky = 'we')
		self.keyword_Entry.focus()

		self.searchButton = Button(self.statusPanel,text = 'Search',command = self.sql_search)
		self.searchButton.grid(row = 0,column = 2,sticky = 'e',padx = 10,pady = 3)

		self.addButton = Button(self.statusPanel, text = 'Add New Notes',command = self.new_window)
		self.addButton.grid(row = 0, column = 3 ,sticky = 'e', padx =10,pady = 3)

		self.exitButton = Button(self.statusPanel, text = 'Exit',command = self.exit_program)
		self.exitButton.grid(row = 0, column = 4 ,sticky = 'e', padx =10,pady = 3)

		#--------------END of Status Panel--------------#

		#--------------Message Panel--------------#
		self.msgPanel = LabelFrame(self,text = 'Message Panel')
		self.msgPanel.pack(fill='both')

		self.msgText = scrolledtext.ScrolledText(self.msgPanel,wrap = 'word',state = 'disabled')
		self.msgText.grid(row = 0,column = 0,sticky = 'NEWS')

		#--------------End of Message Panel--------------#


if __name__ == "__main__":

	root=Tk()
	root.title("gNotes v1.0")
	notesSearch(root,MYSQL_HOST,MYSQL_USER,MYSQL_PWD,MYSQL_DATABASE)
	root.mainloop()
