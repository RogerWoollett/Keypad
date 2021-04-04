# Trypad.py

# written by Roger Woollett
# This is a simple test program to try out the Keypad
# put this file (Trypad.py) and Keypad.py in the same directory
# and run with "python3 Trypad.py" 

import tkinter as tk

from Keypad import Keypad

class App(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
					
		self.title('Test Keypad')
		self.geometry("300x100")

		self.value = 0
		# Keypad will show when button is pressed
		tk.Button(self,text = "Pad",command = self.on_pad).pack()
		
		self.mainloop()

	def on_pad(self):
		reply = [self.value,False]
		self.wait_window(Keypad(self,"My data",reply))
		if reply[1]:
			# user pressed Return
			self.value = reply[0]
			
		print(self.value)
                    
App()
