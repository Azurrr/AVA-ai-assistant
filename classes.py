from tkinter import *;

class Fullscreen:
	def __init__(self):
		self.window = Tk();
		self.window.title(v.keyword.capitalize() + ' Personal assistant');
		self.window.attributes('-fullscreen', True);
		self.fullScreenState = False;
		self.window.mainloop();

class Windowed:
	def __init__(self):
		self.window = Tk();
		self.window.title(v.keyword.capitalize() + ' Personal assistant');
		self.window.geometry("300x200+10+20");
		self.window.mainloop();