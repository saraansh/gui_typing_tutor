# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 11:59:02 2018

@author: Hopeless
"""

from tkinter import *
from tkinter import messagebox, filedialog
from time import time
import os

root = Tk()
root.geometry('800x500')
root.title('TypeAI')
root.iconbitmap('icons/pypad.ico')

#Initial filepath
filepath = os.getcwd() + "/tutorials/"
textmode = 'static'
loaded_text = StringVar()
count = 1
start_time = 0

#For popup items
def popup(event):
	cmenu.tk_popup(event.x_root, event.y_root, 0)

#Choose theme
def theme():
	global bgc,fgc
	val = themechoice.get()
	clrs = clrschms.get(val)
	fgc, bgc = clrs.split('.')
	fgc, bgc = '#'+fgc, '#'+bgc
	text1.config(bg=bgc, fg=fgc)
	#typingblock.config()

#Status Info Bar
def show_info_bar():
	val = showinbar.get()
	if val:
		infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')
	elif not val:
		infobar.pack_forget()

def display_metrics():
	txt = ''
	#if showln.get():

######################################################################################

#About Message
def about():
    messagebox.showinfo("About", "Typing Specialist by Saraansh and Deepak")

#Help Box
def help_box(event=None):
    messagebox.showinfo("Help", "For help email bsaraansh@gmail.com", icon='question')

#Exit
def exit_tutor():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()
root.protocol('WM_DELETE_WINDOW',exit_tutor)

######################################################################################

def set_tuts():
	global filepath
	global textmode
	textmode = 'static'
	filepath = os.getcwd() + "/tutorials/tut"
	ref_text()

def set_para():
	global filepath
	global textmode
	textmode = 'static'
	filepath = os.getcwd() + "/paragraphs/para"
	ref_text()

def set_gen():
	global textmode
	textmode = 'auto'
	ref_text()

######################################################################################
#Load the text
def load_text(count):
	print('Loading text...')
	s=""
	if (textmode == 'static'):
		path = filepath + str(count) + ".txt"
		s_list = []
		with open(path) as f:
			s = f.read().splitlines()
		for temp in s_list:
			s = s + temp + "\n"
	else:
		print("Do Nothing")#Write code for textmode auto
	#Set timer to zero
	return s

def next_text():
	print('Loading next...')
	global count
	count = count + 1
	try:
		loaded_text.set(load_text(count)[0])
	except:
		print("Loading next failed! Refreshing...")
		count = count - 1
		ref_text()

def prev_text():
	print('Loading previous...')
	global count
	if (count==1):
		print('No previous text found! Refreshing...')
	else:
		count = count - 1
	loaded_text.set(load_text(count)[0])

def ref_text():
	print('Refreshing...')
	loaded_text.set(load_text(count)[0])
"""
#Highlight current text
def highlight():
	#Highlight the current word
"""
#Export mongodb data to csv
def export_csv():
	print("Nothing exported")#Export user csv

######################################################################################

#def record():
	#Record each keypress

def key(event):
    print("pressed", repr(event.char))

######################################################################################
newicon = PhotoImage(file='icons/new_file.gif')
openicon = PhotoImage(file='icons/open_file.gif')
saveicon = PhotoImage(file='icons/Save.gif')
cuticon = PhotoImage(file='icons/Cut.gif')
copyicon = PhotoImage(file='icons/Copy.gif')
pasteicon = PhotoImage(file='icons/Paste.gif')
undoicon = PhotoImage(file='icons/Undo.gif')
redoicon = PhotoImage(file='icons/Redo.gif')

clrschms = {
'1. Default White': '000000.FFFFFF',
'2. Greygarious Grey':'83406A.D1D4D1',
'3. Lovely Lavender':'202B4B.E1E1FF' , 
'4. Aquamarine': '5B8340.D1E7E0',
'5. Bold Beige': '4B4620.FFF0E1',
'6. Cobalt Blue':'ffffBB.3333aa',
'7. Olive Green': 'D1E7E0.5B8340',
}
######################################################################################

menubar = Menu(root)

#File menu
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Previous", accelerator='Ctrl+N', compound=LEFT, image=newicon, underline=0, command=prev_text)
filemenu.add_command(label="Next", accelerator='Ctrl+O', compound=LEFT, underline=0, command=next_text)
filemenu.add_separator()
filemenu.add_command(label="Refresh", accelerator='Ctrl+R', compound=LEFT, underline=0, command=ref_text)
filemenu.add_separator()
filemenu.add_command(label="Exit", accelerator='Alt+F4', command=exit_tutor)
menubar.add_cascade(label="File", menu=filemenu)

#About menu
aboutmenu = Menu(menubar, tearoff=0)
aboutmenu.add_command(label="About", command=about)
aboutmenu.add_command(label="Help", command=help_box)
menubar.add_cascade(label="About", menu=aboutmenu)

root.config(menu=menubar)

#Action bar
actionbar = Frame(root, height=25)
b1 = Button(actionbar,text="Next",command=next_text)
b1.pack(side=RIGHT)
b2 = Button(actionbar,text="Refresh",command=ref_text)
b2.pack(side=RIGHT)
b3 = Button(actionbar,text="Previous",command=prev_text)
b3.pack(side=RIGHT)
actionbar.pack(expand=NO, fill=X)

#Text type list
textlist = Frame(root, width=50)
b1 = Button(textlist, width=20, text="Tutorials",command=set_tuts)
b1.pack(fill=X, side=TOP)
b2 = Button(textlist,text="Paragraphs",command=set_para)
b2.pack(fill=X, side=TOP)
b3 = Button(textlist,text="Generated",command=set_gen)
b3.pack(fill=X, side=TOP)
#metrics_panel = Label(text) 
textlist.pack(side=LEFT, fill=Y)

textframe = Frame(root)
textframe.pack(side=RIGHT, fill=BOTH)
text1 = Label(textframe, bd=10, textvariable=loaded_text, width=100, height=15)
text1.pack(fill=X)
loaded_text.set("Hey! How you doing?")
text2 = Text(textframe, width=100, undo=True)
text2.bind("<Key>", key)
text2.pack(expand=YES, fill=BOTH)

#Info Bar
infobar = Label(text2, text='Line: 1 | Column:0')
infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')

#context popup menu
cmenu = Menu(text2,tearoff=0)
for i in ('export_csv'):
    #cmd = eval(i)
    cmenu.add_command(label=i, compound=LEFT, command=about)  
cmenu.add_separator()
text2.bind("<Button-3>", popup)

text2.tag_configure("active_line", background="ivory2")
root.mainloop()









