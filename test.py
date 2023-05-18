from tkinter import Tk, Canvas

window = Tk()
canvas = Canvas(window, width=400, height=400)
canvas.pack()

x = 200
y = 200

def handle_key(event):
    global x, y
    if event.keysym == 'Up':
        y -= 10
    elif event.keysym == 'Down':
        y += 10
    elif event.keysym == 'Left':
        x -= 10
    elif event.keysym == 'Right':
        x += 10
    canvas.delete('all')
    canvas.create_rectangle(x, y, x + 10, y + 10, fill='red')

window.bind('<Key>', handle_key)
# window.focus_set()

window.mainloop()
