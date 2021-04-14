# Keypad.py
# written by Roger Woollett

# A simple dialog keypad

from sys import version_info
if version_info[0] < 3:
	import Tkinter as tk
	import tkFont as tkf
else:
	import tkinter as tk
	import tkinter.font as tkf

class Keyx(tk.Button):
	# class for a key based on tk.Button rather than tk.Label
	# This works but the key is bigger in relation to the text
	# I prefer the Label version
	def __init__(self,master,callback,value = None,*args,**kwargs):
		tk.Button.__init__(self,master,takefocus = True,bd = 5
						 ,command = self.on_click,relief = tk.RAISED,*args,**kwargs)
        
		self.value = value
		self.callback = callback
		
	def on_click(self):
		if self.value == None:
			self.callback()
		else:
			self.callback(self.value)
		
class Key(tk.Label):
	# class for a key
	def __init__(self,master,callback,value = None,*args,**kwargs):
		tk.Label.__init__(self,master,takefocus = True,bd = 5
						 ,relief = tk.RAISED,*args,**kwargs)
        
		self.value = value
		self.callback = callback
		
		self.bind("<Button-1>",self.on_over)
		self.bind("<ButtonRelease-1>",self.on_left)
		    
	def on_left(self,x):
		self.configure(relief = tk.RAISED)		
		# left mouse button released over key
		if self.cget("state") == tk.NORMAL:
			if self.value == None:
				self.callback()
			else:
				self.callback(self.value)
						
	def on_over(self,x):
		# left button pressed over key
		if self.cget("state") == tk.NORMAL:
			self.configure(relief = tk.SUNKEN)		
		
class Keypad(tk.Toplevel):
	# Key pad class should be called using wait_window
	# parameters - self,title,reply
	# title is a string that shows on title bar - use as a prompt for
	# the value to be enterred
	# the title bar can be used to drag the window
	# reply is a list [value,reply]
	# value is the initial value, 0 will display blank
	# reply will be set to True if user pressed Return
	# in this case value will contain the entered value
	# reply is False if user pressed Cancel in which case value is unchanged
	# size will change thw size of the keypad, default is 12
	# if sign is False the numbers must be positive
	# if decimal is False then only integers
	
	def __init__(self,master,title,reply,size = 12,sign = True,decimal = True):
		tk.Toplevel.__init__(self,master,bd = 7,relief = tk.RIDGE)
		
		# get rid of standard title bar
		self.overrideredirect(True)
		
		self.reply = reply
		self.decimal = decimal
			
		# this will set size of keypad
		keyfont = tkf.Font(size = size)

		# self.value is a string representing the current value
		self.value = str(reply[0])
		if self.value == "0":
			self.value = ""
		
		# get rid of "." or ".0"
		if self.value[-2 :] == ".0":
			self.value = self.value[: -2]
			
		# see if there is a decimal point		
		self.point = "." in self.value
		
		# valuetext is what is displayed
		self.valuetext = tk.StringVar()		
		self.valuetext.set(self.value)
		
		row = 0
		# create a pseudo titel bar that shows a title and can be use
		# to drag the keypad window
		title_bar = tk.Label(self,text = title,font = keyfont,bg = "grey",fg = "white")
		title_bar.grid(column = 0,row = row,columnspan = 3,sticky = tk.E + tk.W)
		title_bar.bind("<ButtonPress-1>",self.start_move)
		title_bar.bind("<B1-Motion>",self.on_motion)
		title_bar.bind("<ButtonRelease-1>",self.end_move)
		
		row += 1
		# This will display value
		tk.Label(self,textvariable = self.valuetext,font = keyfont)\
				.grid(column = 0,row = row,columnspan = 3,sticky = tk.W)
		     
		row += 1
		# lay out the key buttons
		Key(self,text = "  1  ",value = "1",callback = self.on_digit,font =	keyfont).grid(column = 0,row = row)
		Key(self,text = "  2  ",value = "2",callback = self.on_digit,font = keyfont).grid(column = 1,row = row)
		Key(self,text = "  3  ",value ="3",callback = self.on_digit,font = keyfont).grid(column = 2,row = row)

		row += 1
		Key(self,text = "  4  ",value ="4",callback = self.on_digit,font = keyfont).grid(column = 0,row = row)
		Key(self,text = "  5  ",value ="5",callback = self.on_digit,font = keyfont).grid(column = 1,row = row)
		Key(self,text = "  6  ",value ="6",callback = self.on_digit,font = keyfont).grid(column = 2,row = row)

		row += 1		
		Key(self,text = "  7  ",value ="7",callback = self.on_digit,font = keyfont).grid(column = 0,row = row)
		Key(self,text = "  8  ",value ="8",callback = self.on_digit,font = keyfont).grid(column = 1,row = row)
		Key(self,text = "  9  ",value ="9",callback = self.on_digit,font = keyfont).grid(column = 2,row = row)

		row += 1
		if sign:
			Key(self,text = " +- ",value =0,callback = self.on_sign,font = keyfont).grid(column = 0,row = row)
		Key(self,text = "  0  ",value = "0",callback =  self.on_digit,font = keyfont).grid(column = 1,row = row)			
		if decimal:
			Key(self,text = "  .   ",value =0,callback = self.on_point,font = keyfont).grid(column = 2,row = row)

		row += 1		
		Key(self,text = " <-  ",value =0,callback = self.on_bksp,font = keyfont).grid(column = 0,row = row)
		Key(self,text = " Cancel  ",value =1,callback = self.on_exit,font = keyfont)\
			.grid(column = 1,row = row,columnspan = 2,sticky = tk.E)

		row += 1		
		Key(self,text = "Return",value = 0,callback = self.on_exit,font = keyfont)\
			.grid(column = 0,row = row,columnspan = 3)
		       
	def on_digit(self,value):
		# process a digit button
		self.value = self.value + value
		self.valuetext.set(self.value)
		
	def on_bksp(self,value):
		# backspace
		if self.value != "":
			self.value = self.value[:-1]
			self.point = "." in self.value
			self.valuetext.set(self.value)
			
	def on_point(self,value):
		# decimal point
		if not self.point:
			self.value += "."
			self.point = True
			
	def on_sign(self,value):
		# the + - key toggles the sign
		# handle if it is the first entry
		if self.value == "":
			self.value = "-"
		else:
			if self.value[0] == "-":
				self.value = self.value[1:]
			else:
				self.value = "-" + self.value
		
		self.valuetext.set(self.value)
						
	def on_exit(self,value):
		# user has pressed return or cancel
		if value == 0:
			# return
			if self.value != "":
				if self.decimal:
					self.reply[0] = float(self.value)
				else:
					self.reply[0] = int(self.value)
			else:
				self.reply[0] = 0	
			self.reply[1] = True
		else:
			# cancel
			self.reply[1] = False
		
		self.destroy()
		
	# drag window functions
	def start_move(self,event):
		self.x = event.x
		self.y = event.y
		self.configure(cursor = "diamond_cross")
		
	def on_motion(self,event):
		# called as mouse moves with button down (dragging)
		deltax = event.x - self.x
		deltay = event.y - self.y
		x = self.winfo_x() + deltax
		y = self.winfo_y() + deltay
		self.geometry("+%s+%s" % (x,y))
		
	def end_move(self,event):
		self.configure(cursor = "")
	
