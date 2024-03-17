import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser
from PIL import Image
from turtle import *
from math import sqrt, atan, degrees
import sys

sys.setrecursionlimit(5000)

#functions
def tool_changer(n):
    global drawing_tool
    drawing_tool = n
    for btn in btns:
        btn.config(relief='flat')
    btns[n-1].config(relief='sunken')
    pen.color(my_color.cget('background'))

def change_my_color(c):
    my_color.config(bg=c)
    pen_size_changer(pen.width())

def color_changer(c):
    pen.color(c)
    change_my_color(c)

def color_picking():
    color = colorchooser.askcolor()
    if color[1]:
        pen.color(color[1])
    change_my_color(color[1])

def coordinating(event):
    global undo_list
    pen.penup()
    x = event.x - canvas_width // 2
    y = -event.y + canvas_height // 2
    pen.goto(x=x, y=y)
    pen.pendown()
    undo_list += 1

def save_able():
    btn_save.config(state=NORMAL)
    change_title(f'{file_name}*')

def drawing(event, type):
    x = event.x - canvas_width // 2
    y = -event.y + canvas_height // 2
    match type:
        case 1:
            pen.goto(x=x, y=y)
    save_able()
    btn_undo.config(state=DISABLED)

def finishing(event, type):
    global undo_list
    x = event.x - canvas_width // 2
    y = -event.y + canvas_height // 2
    width = x - pen.xcor()
    height = pen.ycor() - y
    match type:
        case 2:
            pen.goto(x=x, y=y)
            undo_list = 1
            undo_able()
        case 3:
            for _ in range(2):
                pen.forward(width)
                pen.right(90)
                pen.forward(height)
                pen.right(90)
            undo_list = 8
            undo_able()
        case 4:
            side = sqrt(pow(width / 2, 2) + pow(height, 2))
            degree = degrees(atan(abs(height) / (width / 2)))
            if width > 0 and height >= 0:
                pen.penup()
                pen.goto(x=pen.xcor(), y=pen.ycor()-height)
                pen.pendown()
                pen.forward(width)
                pen.left(180 - degree)
                pen.forward(side)
                pen.left(180 - (180 - 2 * degree))
                pen.forward(side)
                pen.left(180 - degree)
            elif width < 0 and height < 0:
                pen.forward(width)
                pen.right(degree)
                pen.forward(side)
                pen.left(180 - (180 - 2 * degree))
                pen.forward(side)
                pen.right(degree)
            elif width > 0 and height < 0:
                pen.forward(width)
                pen.left(180-degree)
                pen.forward(side)
                pen.left(180-(180-2*degree))
                pen.forward(side)
                pen.left(180-degree)
            else:
                pen.penup()
                pen.goto(x=pen.xcor(), y=pen.ycor() - height)
                pen.pendown()
                pen.forward(width)
                pen.right(degree)
                pen.forward(side)
                pen.left(2*degree)
                pen.forward(side)
                pen.right(degree)
            undo_list = 6
            undo_able()
        case 5:
            pen.penup()
            pen.goto(x=pen.xcor()+width/2, y = pen.ycor()-width)
            pen.pendown()
            pen.circle(width/2)
            undo_list = 1
            undo_able()
    save_able()

def pen_size_changer(size):
    c_h = int(pen_size_canvas.cget('width')) / 2
    s = round(float(size))
    pen.width(size)
    pen_size_label.config(text=str(s))
    pen_size_canvas.delete('all')
    pen_size_canvas.create_oval(c_h-s/2, c_h-s/2, c_h+s/2, c_h+s/2, fill=my_color.cget('background'), outline=my_color.cget('background'))

def view_pen_size():
    if pen_size_view.cget('text') == 'View pen size':
        pen_size_canvas.place(x=root_width - 110, y=root_height - 110)
        pen_size_view.config(text='Hide pen size')
    else:
        pen_size_canvas.place_forget()
        pen_size_view.config(text='View pen size')

def undo_able():
    btn_undo.config(state=NORMAL)

def undoing():
    for _ in range(undo_list):
        pen.undo()
    btn_undo.config(state=DISABLED)

def eraser():
    global drawing_tool
    drawing_tool = 1
    for btn in btns:
        btn.config(relief='flat')
    btns[-1].config(relief='sunken')
    pen.color('white')

def change_title(s):
    root.title(f'Paint 2.0 {s}')

def save():
    global saved, file_name
    if saved:
        postscript_file = canvas.postscript(file='temp.ps', colormode='color')
        image = Image.open('temp.ps')
        image.save(file_name, format='PNG')
        image.close()
        os.remove('temp.ps')
        btn_save.config(state=DISABLED)
        change_title(file_name)
    else:
        file_name = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_name:
            postscript_file = canvas.postscript(file='temp.ps', colormode='color')
            image = Image.open('temp.ps')
            image.save(file_name, format='PNG')
            image.close()
            os.remove('temp.ps')
            saved = True
            btn_save.config(state=DISABLED)
            change_title(file_name)
        else:
            messagebox.showinfo("Cancelled", "Save operation cancelled.")

def on_closing():
    if btn_save.cget('state') == NORMAL:
        if messagebox.askyesno('Save image', 'Do you want to save your image?'):
            save()
    root.destroy()

def new():
    global saved
    if btn_save.cget('state') == NORMAL:
        if messagebox.askyesno('Save image', 'Do you want to save your image?'):
            save()
    canvas.delete('all')
    saved = False
    btn_save.config(state=DISABLED)
    change_title('')

def keyboard(event):
    if event.keysym == 's':
        save()
    elif event.keysym == 'n':
        new()
    print(event.state, event.keysym)
#OSError: Unable to locate Ghostscript on paths

#window
root = Tk()
root.title('Paint 2.0')
root.iconbitmap('images/logo.ico')
root_width = 1200
root_height = int(root_width * 3 / 5)
root.geometry(f'{root_width}x{root_height}+100+10')
root.resizable(False, False)

#images
pen_image = PhotoImage(file='images/pencil.png').subsample(50, 50)
line_image = PhotoImage(file='images/line.png').subsample(78, 78)
rectangle_image = PhotoImage(file='images/rectangle.png').subsample(48, 48)
triangle_image = PhotoImage(file='images/triangle.png').subsample(117, 117)
eraser_image = PhotoImage(file='images/eraser.png').subsample(39, 39)
circle_image = PhotoImage(file='images/circle.png').subsample(98, 98)
color_picker_image = PhotoImage(file='images/Colors/color-picker.png').subsample(27, 27)
undo_image = PhotoImage(file='images/undo.png').subsample(13, 13)
save_image = PhotoImage(file='images/save.png').subsample(20, 20)
new_image = PhotoImage(file='images/new.png').subsample(11, 11)

#canvas
canvas_width = root_width-50
canvas_height = root_height-70
canvas = Canvas(root, width=canvas_width, height=canvas_height)
canvas.place(x=root_width-canvas_width, y=root_height-canvas_height)
screen = TurtleScreen(canvas)
pen = RawTurtle(screen)
pen.hideturtle()
pen.speed(0)

#variables
drawing_tool = 1
undo_list = 0
saved = False
file_name = ''

#widgets
tools_frame = Frame(root, bg='white', padx=5, pady=5, bd=1, relief=SOLID)
btns = list()
btn_pen = Button(tools_frame, image=pen_image, command=lambda: tool_changer(1), relief='sunken')
btn_pen.grid(row=0, column=0)
btns.append(btn_pen)

btn_line = Button(tools_frame, image=line_image, command=lambda: tool_changer(2), relief='flat')
btn_line.grid(row=1, column=0)
btns.append(btn_line)

btn_rectangle = Button(tools_frame, image=rectangle_image, command=lambda: tool_changer(3), relief='flat')
btn_rectangle.grid(row=0, column=1)
btns.append(btn_rectangle)

btn_triangle = Button(tools_frame, image=triangle_image, command=lambda: tool_changer(4), relief='flat')
btn_triangle.grid(row=1, column=1)
btns.append(btn_triangle)

btn_circle = Button(tools_frame, image=circle_image, command=lambda: tool_changer(5), relief='flat')
btn_circle.grid(row=0, column=2)
btns.append(btn_circle)

btn_eraser = Button(tools_frame, image=eraser_image, command=eraser, relief='flat')
btn_eraser.grid(row=len(btns) % 2, column=len(btns)//2)
btns.append(btn_eraser)

for btn in btns:
    btn.config(width=21, height=21, bg='white')

tools_frame.place(x=root_width-canvas_width, y=2.5)

canvas.bind('<Button-1>', coordinating)
canvas.bind('<B1-Motion>', lambda event: drawing(event, drawing_tool))
canvas.bind('<ButtonRelease-1>', lambda event: finishing(event, drawing_tool))

#color buttons
colors_frame = Frame(root)

color_images = ['black.png', 'red.png', 'green.png', 'blue.png', 'yellow.png', 'orange.png', 'pink.png', 'brown.png']
colors = list()
for name in color_images:
    colors.append(PhotoImage(file=f'images/Colors/{name}').subsample(13, 13))

for i in range(len(color_images)):
    colors_frame.rowconfigure(i, minsize=50)
    Button(colors_frame, image=colors[i], command=lambda c=color_images[i][:-4]: color_changer(c), relief='flat').grid(row=i, column=0)

color_picker = Button(colors_frame, image=color_picker_image, command=color_picking, relief='flat')
color_picker.grid(row=len(color_images)+1, column=0)

my_color = Canvas(colors_frame, width=color_picker_image.width(), height=color_picker_image.height(), bg='black')
my_color.grid(row=len(color_images)+2, column=0)

colors_frame.place(x=2.5, y=root_height-canvas_height+10)

#pen size
pen_size = ttk.Scale(from_=1, to=100, length=200, command=pen_size_changer)
pen_size.place(x=root_width-canvas_width+21*len(btns), y=10)

pen_size_label = Label(text='1', width=15, font=('Arial', 16))
pen_size_label.place(x=root_width-canvas_width+21*len(btns), y=35)

pen_size_view = ttk.Button(text='View pen size', command=view_pen_size)
pen_size_view.place(x=root_width-canvas_width+21*len(btns)+210, y=10)

pen_size_canvas = Canvas(width=110, height=110, bg='#333')
circle = pen_size_canvas.create_oval(54.5, 54.5, 55.5, 55.5, fill=my_color.cget('background'), outline=my_color.cget('background'))

#undo button
btn_undo = Button(image=undo_image, relief='flat', command=undoing, state=DISABLED)
btn_undo.place(x=2.5, y=root_height-undo_image.height()-10)

#save button
btn_save = Button(image=save_image, relief='flat', command=save, state=DISABLED)
btn_save.place(x=root_width-canvas_width+21*len(btns)+300, y=10)

#new button
btn_new = Button(image=new_image, relief='flat', command=new)
btn_new.place(x=root_width-canvas_width+21*len(btns)+360, y=10)

root.bind('<Control-s>', keyboard)
root.bind('<Control-n>', keyboard)
root.protocol('WM_DELETE_WINDOW', on_closing)

root.mainloop()
