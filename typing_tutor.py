# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 11:59:02 2018

@author: Hopeless
"""

from tkinter import *
from tkinter import messagebox, filedialog
from pymongo import MongoClient
from time import time
import pandas as pd
import os

#root-window config
root = Tk()
root.geometry('800x500')
root.title('TypeAI')
root.iconbitmap('icons/pypad.ico')

#mongodb config
client = MongoClient('localhost', 27017)
db = client['typeaidata']
collection = db['typist1']

#Program-specefic parameters
filepath = os.getcwd() + "/tutorials/"
textmode = 'static'
count = 1
stats = StringVar()
loaded_text = StringVar()
typed_text = ""
start_time = 0

#Database-specefic parameters
raw_typed_text = []
raw_time = []
corrections = 0
accuracy = 0.0
wpm = 0

# Function to display popup items
def popup(event):
	cmenu.tk_popup(event.x_root, event.y_root, 0)

# Function to change theme
def theme():
	global bgc,fgc
	val = themechoice.get()
	clrs = clrschms.get(val)
	fgc, bgc = clrs.split('.')
	fgc, bgc = '#'+fgc, '#'+bgc
	text1.config(bg=bgc, fg=fgc)
	#typingblock.config()

# Function to diplay status
def show_info_bar():
	val = showinbar.get()
	if val:
		infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')
	elif not val:
		infobar.pack_forget()

######################################################################################

# About Message
def about():
    messagebox.showinfo("About", "TypeAI by Saraansh and Deepak")

# Help Box
def help_box(event=None):
    messagebox.showinfo("Help", "For help email bsaraansh@gmail.com", icon='question')

# Exit
def exit_tutor():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()
root.protocol('WM_DELETE_WINDOW',exit_tutor)

######################################################################################

# Function to switch to tutorials
def set_tuts(event=None):
	global filepath
	global textmode
	global count
	count = 1
	textmode = 'static'
	filepath = os.getcwd() + "/tutorials/tut"
	ref_text()

# Function to switch to text extracts
def set_para(event=None):
	global filepath
	global textmode
	global count
	count = 1
	textmode = 'static'
	filepath = os.getcwd() + "/paragraphs/para"
	ref_text()

# Function to auto-generate text
def set_gen(event=None):
	global textmode
	textmode = 'auto'
	ref_text()

######################################################################################

# Function to load text
def load_text(count):
	print('Loading text...')
	s=""
	if (textmode == 'static'):
		path = filepath + str(count) + ".txt"
		s_list = []
		with open(path) as f:
			s_list = f.read().splitlines()
		for temp in s_list:
			s = s + temp + "\n"
	else:
		print("Do Nothing")#Write code for textmode auto
	#Set timer to zero
	return s.rstrip()

# Function to load next text
def next_text(event=None):
	print('Loading next...')
	global count
	global start_time
	count = count + 1
	start_time = 0
	try:
		ref_text()
	except:
		print("Loading next failed! Refreshing...")
		count = count - 1
		ref_text()

# Function to load previous text
def prev_text(event=None):
	print('Loading previous...')
	global count
	global start_time
	start_time = 0
	if (count==1):
		print('No previous text found! Refreshing...')
	else:
		count = count - 1
	ref_text()

# Function to reload the current text
def ref_text(event=None):
	global start_time
	loaded_text.set(load_text(count))
	start_time=0
	text2.delete('1.0', END)
	text1.config(bg='#000000', fg='#FFFFFF')
"""
# Function to highlight current text
def highlight():
	#Highlight the current word
"""
#####################################################################################

# Function to export csv from mongoDB
def export_csv():
	query = collection.find()
	df =  pd.DataFrame(list(query))
	df.to_csv(os.getcwd() + "/exported.csv", index=None)
	print("Exported CSV!")

# Function to save test data to mongoDB
def save_to_db():
	data = {"text": loaded_text.get(),
			"typedlist": raw_typed_text,
			"timedlist": raw_time,
			"wpm": wpm,
			"corrections": corrections,
			"accuracy": accuracy}
	id = collection.insert_one(data).inserted_id
	print("Saved " + str(id))

######################################################################################
"""
# Function to detect keypresses
def key(event):
    print("Pressed", repr(event.char))
"""

# Function to display metrics
def display_metrics(elapsed):
	mins = int(elapsed/60)
	seconds = int(elapsed - mins*60)
	s1 = s2 = s3 = ""
	if(mins==0):
		s1 = "\n\nTime elapsed: " + str(seconds) + "s"
	else:
		s1 = "\n\nTime elapsed: " + str(mins) + "m " + str(seconds) + "s"
	s2 = "\n\nAvg WPM: " + str(round(wpm,2))
	s3 = "\n\nAccuracy: " + str(round(accuracy,2))
	stats.set("</>  Metrics  </>" + s1 + s2 + s3 + '\n')
	print(s1 + s2 + s3 + '\n')

# Function to calculate metrics
def calculate(end, begin):
	global wpm, accuracy
	elapsed = (end - begin)
	wpm = (0.2 * (len(typed_text) - 1) * 60) / elapsed
	error_rate = (corrections) / (len(typed_text) + corrections)
	accuracy = (1 - error_rate) * 100
	display_metrics(elapsed)

# Function to record keypress
def record(event):
	global corrections
	global start_time
	global typed_text
	global raw_typed_text
	global raw_time
	#Initializing default values
	if (start_time == 0):
		raw_time = []
		raw_typed_text = []
		typed_text = ""
		corrections = 0
		start_time = time()
	#Storing the raw text & time for future work
	c = event.char
	raw_typed_text.append(c)
	raw_time.append(time())
	#Check for corrections
	if (c=='\x08' or c=='\r' or c=='\x01'):
		corrections += 1
		if(typed_text!=""):
			typed_text = typed_text[:-1]
	else:
		typed_text += str(c)
	#Colour change for incorrect text
	if (loaded_text.get()[0:len(typed_text)] == typed_text):
		text1.config(bg='#000000', fg='#FFFFFF')
	else:
		#text1.tag_add('start', '1.0', text2.index(tk.INSERT))
		text1.config(bg='#000000', fg='#FF00FF')
	#Comparing typed and test strings
	if (loaded_text.get() == typed_text):
		print("Calculating...")
		calculate(time(), start_time)
		save_to_db()
		start_time = 0
		text2.delete('1.0', END)

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
filemenu.add_command(label="Export CSV", accelerator='Ctrl+E', compound=LEFT, underline=0, command=export_csv)
filemenu.add_command(label="Exit", accelerator='Alt+F4', command=exit_tutor)
menubar.add_cascade(label="File", menu=filemenu)

#About menu
aboutmenu = Menu(menubar, tearoff=0)
aboutmenu.add_command(label="Help", accelerator='F1', compound=LEFT, image=newicon, underline=0, command=help_box)
aboutmenu.add_command(label="About", accelerator='F12', compound=LEFT, image=newicon, underline=0, command=about)
menubar.add_cascade(label="About", menu=aboutmenu)

root.config(menu=menubar)

#Action bar
actionbar = Frame(root, height=25)
b1 = Button(actionbar, text="Next", command=next_text)
b1.pack(side=RIGHT)
b2 = Button(actionbar, text="Refresh", command=ref_text)
b2.pack(side=RIGHT)
b3 = Button(actionbar, text="Previous", command=prev_text)
b3.pack(side=RIGHT)
actionbar.pack(expand=NO, fill=X)

#Text type list
textlist = Frame(root, width=50)
b1 = Button(textlist, width=20, text="\nTutorials <F6>\n",command=set_tuts)
b1.pack(fill=X, side=TOP)
b2 = Button(textlist,text="\nParagraphs <F7>\n",command=set_para)
b2.pack(fill=X, side=TOP)
b3 = Button(textlist,text="\nGenerated <F8>\n",command=set_gen)
b3.pack(fill=X, side=TOP)
mpanel = Message(textlist, textvariable=stats, relief=RIDGE)
mpanel.pack(fill=X, side=BOTTOM)
stats.set("</>  Metrics  </>\n\n\n\n\n\n\n")
textlist.pack(side=LEFT, fill=Y)

textframe = Frame(root)
textframe.pack(expand=YES, side=RIGHT, fill=BOTH)
text1 = Message(textframe, textvariable=loaded_text, font=('Verdana',15), aspect=500, anchor='nw', relief=RIDGE)
text1.pack(expand=YES, fill=BOTH)
loaded_text.set("Welcome to TypeAI!\n\nSelect a route and start typing!")
text2 = Text(textframe, height=15, wrap=WORD, undo=True)
text2.pack(expand=YES, fill=BOTH)

#Binding Events
root.bind('<Control-N>', next_text)
root.bind('<Control-n>', next_text)
root.bind('<Control-P>', prev_text)
root.bind('<Control-p>', prev_text)
root.bind('<Control-R>', ref_text)
root.bind('<Control-r>', ref_text)
root.bind('<Prior>', prev_text)
root.bind('<Next>', next_text)
root.bind('<KeyPress-F5>', ref_text)
root.bind('<KeyPress-F6>', set_tuts)
root.bind('<KeyPress-F7>', set_para)
root.bind('<KeyPress-F8>', set_gen)
root.bind('<KeyPress-F1>', help_box)
root.bind('<KeyPress-F12>', about)
text2.bind('<Control-N>', next_text)
text2.bind('<Control-n>', next_text)
text2.bind('<Control-P>', prev_text)
text2.bind('<Control-p>', prev_text)
text2.bind('<Control-R>', ref_text)
text2.bind('<Control-r>', ref_text)
text2.bind('<Prior>', prev_text)
text2.bind('<Next>', next_text)
text2.bind('<KeyPress-F5>', ref_text)
text2.bind('<KeyPress-F6>', set_tuts)
text2.bind('<KeyPress-F7>', set_para)
text2.bind('<KeyPress-F8>', set_gen)
text2.bind('<KeyPress-F1>', help_box)
text2.bind('<KeyPress-F12>', about)
text2.bind("<Key>", record)


#Info Bar
infobar = Label(text2, text='Line: 1 | Column:0')
infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')

#Context popup menu
cmenu = Menu(text2,tearoff=0)
cmenu.add_command(label="Refresh <F5>", accelerator='F5', compound=LEFT, image=newicon, underline=0, command=ref_text)
cmenu.add_separator()
cmenu.add_command(label="Next <PgDn>", accelerator='<Next>', compound=LEFT, image=newicon, underline=0, command=next_text)
cmenu.add_command(label="Prev <PgUp>", accelerator='<Prior>', compound=LEFT, image=newicon, underline=0, command=prev_text)
cmenu.add_separator()
cmenu.add_command(label="Help", accelerator='F1', compound=LEFT, image=newicon, underline=0, command=help_box)  

text2.bind("<Button-3>", popup)
#text2.tag_configure("active_line", background="ivory2")
root.mainloop()









