"""
Log-in page part of Project: Hydrate.

Description:
 - Records user input for username and password,
   then various checks are done to make sure the account
   exists in the user_logins.txt file
   and checks to make sure the credentials match.
"""

# Imports.
import subprocess
import threading

import time
import tkinter as tk

from tkinter import ttk, Tk
from PIL import Image, ImageTk

# File path for storing user logins.
USER_LOGINS_FILE = "db\\user_logins.txt"

# Create the root window for the GUI.
root = Tk()
root.geometry("495x595")
root.iconbitmap(default="assets\\icon.ico")
root.resizable(width=False, height=False)
root.title("Project Hydrate Log-In")

# Function to center the window on the screen.
def center_window(window):
    """
    Center the given window on the screen.
    
    Parameters:
    - window: The Tkinter window to be centered.
    """

    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    width_x = (screen_width - width) // 2
    width_y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{width_x}+{width_y}")

center_window(root)

# Function to navigate to the main window.
def goto_main_window():
    """
    Close the current window and open the main window.
    """

    root.destroy()
    subprocess.Popen(["python", "main.py"])

# Function to handle successful login.
def successful_login(username_returned, real_username):
    """
    Handle successful login by directing to appropriate screens.
    """

    root.destroy()
    if not username_returned == "BADAPPLE":
        subprocess.Popen(["python", "loading_screen.py", real_username])
    else:
        subprocess.Popen(["python", "badapple_easteregg.py"])

# Load and resize the images used in the GUI.
menu_icon = Image.open("assets\\iconmain.png")
waves_bottom = Image.open("assets\\wavesfullcropped.png")
title_text_icon = Image.open("assets\\titletext.png")
button_image = Image.open("assets\\buttonimage.png")
back_button_image = Image.open("assets\\backbutton.png")

menu_icon = menu_icon.resize((108, 141))
waves_bottom = waves_bottom.resize((495, 395))
title_text_icon = title_text_icon.resize((182, 70))
button_image = button_image.resize((200, 30))
back_button_image = back_button_image.resize((30, 30))

# Convert images to Tkinter-compatible format.
menu_icon_tk = ImageTk.PhotoImage(menu_icon)
waves_bottom_tk = ImageTk.PhotoImage(waves_bottom)
title_text_icon_tk = ImageTk.PhotoImage(title_text_icon)
button_image_tk = ImageTk.PhotoImage(button_image)
back_button_image_tk = ImageTk.PhotoImage(back_button_image)

# Create labels and buttons for the GUI.
menu_icon_label = tk.Label(root, image=menu_icon_tk)
waves_bottom_label = tk.Label(root, image=waves_bottom_tk)
title_text_label = tk.Label(root, image=title_text_icon_tk)
back_button = ttk.Button(
    root,
    image=back_button_image_tk,
    compound="center",
    width=0,
    command=goto_main_window
)

# Variables for username and password input fields.
username_variable = tk.StringVar()
username_variable.set("")
verifying_username = tk.StringVar()
verifying_username.set("")
password_variable = tk.StringVar()
password_variable.set("")

# Boolean variables to track changes in username and password fields.
username_changed = tk.BooleanVar()
username_changed.set(False)
password_changed = tk.BooleanVar()
password_changed.set(False)

# Boolean variables to track warnings for username and password.
username_warning_showing = tk.BooleanVar()
username_warning_showing.set(False)
password_warning_showing = tk.BooleanVar()
password_warning_showing.set(False)

# Function to display a warning for non-existent usernames.
def usernamenonexistent_warning():
    """
    Display a warning if the entered username doesn't exist.
    """

    if not username_warning_showing.get():
        username_warning_showing.set(True)
        username_non_existent_label.place(x=170, y=370)

        time.sleep(2)
        username_non_existent_label.place_forget()
        username_warning_showing.set(False)

# Function to display a warning for incorrect passwords.
def wrongpassword_warning():
    """
    Display a warning if the entered password is incorrect.
    """

    if not password_warning_showing.get():
        password_warning_showing.set(True)
        wrong_password_label.place(x=185, y=410)

        time.sleep(2)
        wrong_password_label.place_forget()
        password_warning_showing.set(False)

# Function to display a warning for invalid passwords.
def invalid_password_warning():
    """
    Display a warning for invalid passwords.
    """

    password_warning_label.place(relx=0.5, y=420, anchor=tk.CENTER)

    time.sleep(2)
    password_warning_label.place_forget()

# Function to send a login request.
def send_login_request():
    """
    Send a login request and handle the response.
    """

    if (username_changed.get() and password_changed.get()):
        verifying_username.set(username_variable.get().strip().upper())
        user_logins = open(USER_LOGINS_FILE, "r", encoding="utf-8")
        user_logins_lines = user_logins.readlines()

        user_exists = tk.BooleanVar()
        user_exists.set(False)

        for user_login in user_logins_lines:
            if verifying_username.get().strip() in user_login:
                login_info = user_login.split("=")
                user = login_info[1]
                password = login_info[2]

                if user.strip() == verifying_username.get().strip():
                    user_exists.set(True)

                    if password.strip() == password_variable.get().strip():
                        successful_login(user.strip(), login_info[3].strip())
                    else:
                        if not password_warning_showing.get():
                            password_warning_thread = threading.Thread(target=wrongpassword_warning)
                            password_warning_thread.start()

        if not user_exists.get():
            if not username_warning_showing.get():
                username_warning_thread = threading.Thread(target=usernamenonexistent_warning)
                username_warning_thread.start()

            return
    else:
        password_warning_variable.set("Log-in rejected as one or both inputs were left blank")
        password_warning_thread = threading.Thread(target=invalid_password_warning)
        password_warning_thread.start()
        return

# Create login button and labels.
login_button = ttk.Button(
    root,
    text="L O G  I N",
    image=button_image_tk,
    compound="center",
    command=send_login_request
)

login_label = tk.Label(root, text="A C C O U N T  L O G  I N", fg="darkgray", font=("Arial", 14))
wrong_password_label = ttk.Label(
    root,
    text="Incorrect Password",
    foreground="red",
    font=("Arial", 10)
)

username_non_existent_label = ttk.Label(
    root,
    text="Username does not exist",
    foreground="red",
    font=("Arial", 10)
)

# Configure button style.
style = ttk.Style()
style.configure("TButton", foreground="gray")
style.configure("TButton", font=("Arial", 16))

# Place labels, buttons, and entry fields in the GUI.
waves_bottom_label.place(x=-2, y=210)
menu_icon_label.place(x=191, y=40)
title_text_label.place(x=153, y=200)
back_button.place(x=20, y=20)

# Functions to handle focus and leave events for username and password entry fields.
def username_focus(event):
    """
    Remove placeholder text upon clicking the username entry.
    """
    event = event or None

    if username_box.get() == "Username":
        if not username_changed.get():
            username_changed.set(True)
            username_box.delete(0, len(username_box.get()))
            username_box.configure(foreground="black")

def username_leave(event):
    """
    Keep user typed text or put back placeholder text
    upon leaving the username entry.
    """
    event = event or None

    if username_box.get() == "":
        if username_changed.get():
            username_changed.set(False)
            username_box.insert(0, "Username")
            username_box.configure(foreground="gray")

def password_focus(event):
    """
    Remove placeholder text upon clicking the password entry.
    """
    event = event or None

    if password_box.get() == "Password":
        if not password_changed.get():
            password_changed.set(True)
            password_box.delete(0, len(password_box.get()))
            password_box.configure(foreground="black", show="*")

def password_leave(event):
    """
    Keep user typed text or put back placeholder text
    upon leaving the password entry.
    """
    event = event or None

    if password_box.get() == "":
        if password_changed.get():
            password_changed.set(False)
            password_box.insert(0, "Password")
            password_box.configure(foreground="gray", show="")

password_warning_variable = tk.StringVar()
password_warning_variable.set("Log-in rejected as one or both inputs were left blank")
password_warning_label = ttk.Label(
    root,
    textvariable=password_warning_variable,
    foreground="red",
    font=("Arial", 10)
)

username_box = ttk.Entry(root, textvariable=username_variable, width=34, foreground="gray")
password_box = ttk.Entry(root, textvariable=password_variable, width=34, foreground="gray")

username_box.insert(0, "Username")
username_box.bind("<FocusIn>", username_focus)
username_box.bind("<FocusOut>", username_leave)

password_box.insert(0, "Password")
password_box.bind("<FocusIn>", password_focus)
password_box.bind("<FocusOut>", password_leave)

login_label.place(x=130, y=310)
username_box.place(x=140, y=350)
password_box.place(x=140, y=390)
login_button.place(x=140, y=430)

# Set the stacking order of the GUI elements.
title_text_label.lower(login_button)
menu_icon_label.lower(title_text_label)
waves_bottom_label.lower(menu_icon_label)

# Start the main event loop.
root.mainloop()
