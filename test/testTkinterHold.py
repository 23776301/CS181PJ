import tkinter as tk

key_states = {}

def handle_key_press(event):
    if event.keysym not in key_states:
        print("Key pressed:", event.keysym)
        key_states[event.keysym] = True

def handle_key_release(event):
    if event.keysym in key_states:
        print("Key released:", event.keysym)
        del key_states[event.keysym]

root = tk.Tk()

# Bind the key press and release events to their respective functions
root.bind('<KeyPress>', handle_key_press)
root.bind('<KeyRelease>', handle_key_release)

root.mainloop()
