# Imports.
import subprocess
import sys

from tkinter import *
import tkinter as tk

from tkinter import ttk
from PIL import Image, ImageTk

import time
import threading

root = Tk()
root.geometry("495x595")

# Create the username variable.
logged_in_username = ""

# Check if a username is provided.
if len(sys.argv) > 1:
    logged_in_username = sys.argv[1]

root.iconbitmap(default="assets\icon.ico")
user_data_file = "db\\user_data.txt"
leaderboard_data_file = "db\\leaderboard_data.txt"

# Function to go to the main window.
def goto_main_window():
    root.destroy()
    subprocess.call(["python", "main.py"])

# Function to go to the hydration calculator window.
def goto_calculator_window():
    root.destroy()
    subprocess.call(["python", "hydration_calculator.py", logged_in_username])

# Function to go to the leaderboard window.
def goto_leaderboard_window():
    root.destroy()
    subprocess.call(["python", "leaderboard.py", logged_in_username])
    
# Function to go to the weather window.
def goto_weather_window():
    root.destroy()
    subprocess.call(["python", "weather.py", logged_in_username])

# Set window properties
root.resizable(width=False, height=False)
root.title("Project Hydrate: Home")

# Function to center the window on the screen.
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

center_window(root)

# Load images.
menu_icon = Image.open("assets\iconmain.png")
waves_bottom = Image.open("assets\wavesfullcropped.png")
title_text_icon = Image.open("assets\\titletext.png")
button_image = Image.open("assets\\buttonimage.png")
user_icon = Image.open("assets\iconuser.png")
waves_top = Image.open("assets\\topwaves.png")
add_button_image = Image.open("assets\plusicon.png")
minus_button_image = Image.open("assets\minusicon.png")
set_button_image = Image.open("assets\seticon.png")
leaderboard_button_image = Image.open("assets\leaderboardicon.png")
weather_button_image = Image.open("assets\weathericon.png")

# Resize images.
menu_icon = menu_icon.resize((108, 141))
waves_bottom = waves_bottom.resize((495, 395))
title_text_icon = title_text_icon.resize((182, 70))
button_image = button_image.resize((200, 30), resample=Image.BICUBIC)
user_icon = user_icon.resize((100, 100))
waves_top = waves_top.resize((495, 595))
add_button_image = add_button_image.resize((20, 20))
minus_button_image = minus_button_image.resize((20, 20))
set_button_image = set_button_image.resize((20, 20))
leaderboard_button_image = leaderboard_button_image.resize((40, 40), resample=Image.BICUBIC)
weather_button_image = weather_button_image.resize((40, 40), resample=Image.BICUBIC)

# Create image objects.
add_button_image_tk = ImageTk.PhotoImage(add_button_image)
minus_button_image_tk = ImageTk.PhotoImage(minus_button_image)
set_button_image_tk = ImageTk.PhotoImage(set_button_image)
leaderboard_button_image_tk = ImageTk.PhotoImage(leaderboard_button_image)
weather_button_image_tk = ImageTk.PhotoImage(weather_button_image)

menu_icon_tk = ImageTk.PhotoImage(menu_icon)
waves_bottom_tk = ImageTk.PhotoImage(waves_bottom)

title_text_icon_tk = ImageTk.PhotoImage(title_text_icon)
button_image_tk = ImageTk.PhotoImage(button_image)

user_icon_tk = ImageTk.PhotoImage(user_icon)
waves_top_tk = ImageTk.PhotoImage(waves_top)

# Create label objects.
menu_icon_label = Label(root, image=menu_icon_tk)
waves_bottom_label = Label(root, image=waves_bottom_tk)

title_text_label = Label(root, image=title_text_icon_tk)
user_icon_label = Label(root, image=user_icon_tk)
waves_top_label = Label(root, image=waves_top_tk)

# Create the username variable and set it as the passed username, and if it doesn"t exist set it to NIL.
username_variable = StringVar()
username_variable.set("")

hydration_progress_variable = StringVar()
hydration_progress_variable.set("")

if not (logged_in_username == ""):
    username_variable.set(str(logged_in_username) + "!")
else:
    logged_in_username = "NIL"
    username_variable.set("NIL!")

user_found = BooleanVar()
user_found.set(False)

user_current_hydration = IntVar()
user_current_hydration.set(0)

user_recommended_hydration = IntVar()
user_recommended_hydration.set(0)

current_time = int(time.time())

'''
currently_updating_timer = BooleanVar()
currently_updating_timer.set(True)

def update_timer():
    while (True):
        time.sleep(10)
        if (currently_updating_timer.get() == True):
            current_time = int(time.time())
            print("Updated")
        else:
            break
    
timer_thread = threading.Thread(target=update_timer)
timer_thread.start()
'''

signin_options_label = Label(root, textvariable=username_variable, fg="black", font=("Simplifica", 20, "bold"))
hello_label = Label(root, text="HELLO", fg="black", font=("Simplifica", 20))
signup_button = ttk.Button(root, text="L O G  O U T", image=button_image_tk, compound="center", command=goto_main_window)

'''
def close_app():
    print("Closed")
    root.destroy()
    currently_updating_timer.set(False)

root.protocol("WM_DELETE_WINDOW", close_app)
'''

# Function to handle subtract canvas click event.
def subtract_click(event):
    subtract_canvas.move(subtract_button, 0, 2)
    subtract_canvas.after(100, lambda: subtract_canvas.move(subtract_button, 0, -2))
    subtract()

# Function to handle add canvas click event.
def add_click(event):
    add_canvas.move(add_button, 0, 2)
    add_canvas.after(100, lambda: add_canvas.move(add_button, 0, -2))
    add()

# Functions to handle adding and subtracting values.
def subtract():
    if (textbox.get() == ""):
        textbox.delete(0, tk.END)
        textbox.insert(tk.END, 0)
        
    current_value = int(textbox.get())
    new_value = current_value - 250
    textbox.delete(0, tk.END)
    textbox.insert(tk.END, str(new_value))

def add():
    if (textbox.get() == ""):
        textbox.delete(0, tk.END)
        textbox.insert(tk.END, 0)
    
    current_value = int(textbox.get())
    new_value = current_value + 250
    textbox.delete(0, tk.END)
    textbox.insert(tk.END, str(new_value))

# Apply changes to their hydration status.
def apply(event):
    if (textbox.get() == ""):
        textbox.delete(0, tk.END)
        textbox.insert(tk.END, 0)
    
    current_value = int(textbox.get())
    set_canvas.move(set_button, 0, 2)
    set_canvas.after(100, lambda: set_canvas.move(set_button, 0, -2))
    
    textbox.delete(0, tk.END)
    textbox.insert(tk.END, 0)

    user_data = open(user_data_file, "r+")
    lines = user_data.readlines()
    user_found.set(False)

    for index, line in enumerate(lines):
        if logged_in_username.upper().strip() in line:
            user_found.set(True)
            line_list = line.split("=")
            
            if (int(line_list[2].strip().replace(".", "")) + current_value >= int(line_list[1].strip().replace(".", ""))):
                print("User has drank more than the recommended amount!")
                                
                if (int(line_list[2].strip().replace(".", "")) + current_value >= int(line_list[1].strip().replace(".", ""))):
                    print("Not the same value")
                    new_line = "{}={}={}={}\n".format(logged_in_username.upper().strip(), str(line_list[1].strip().replace(".", "")), str(line_list[1].strip().replace(".", "")), current_time)
                    hydration_progress_variable.set("HYDRATION PROGRESS: {}ml / {}ml".format(line_list[1].strip().replace(".", ""), line_list[1].strip().replace(".", "")))
                    
                    lines[index] = new_line
                    user_data.seek(0)
            
                    user_data.writelines(lines)
                    user_data.truncate()
                    user_data.close()
                    
                    hydration_canvas.place_forget()
                    leaderboard_user_found = BooleanVar()
                    
                    leaderboard_data = open(leaderboard_data_file, "r+")
                    l_lines = leaderboard_data.readlines()
                    leaderboard_user_found.set(False)
                    
                    for l_index, l_line in enumerate(l_lines):
                        if logged_in_username.upper().strip() in l_line:
                            leaderboard_user_found.set(True)
                            print("Found")
                            leaderboard_line_list = l_line.split("=")
                            leaderboard_new_line = "{}={}\n".format(logged_in_username.upper().strip(), str(int(leaderboard_line_list[1]) + 1))
            
                            l_lines[l_index] = leaderboard_new_line
                            leaderboard_data.seek(0)
            
                            leaderboard_data.writelines(l_lines)
                            leaderboard_data.truncate()
                            return
                        
                    if (leaderboard_user_found.get() == False):
                        leaderboard_line_list = line.split("=")       
                        leaderboard_data.write("{}={}\n".format(logged_in_username.upper().strip(), str(1)))
                        leaderboard_data.close()
                        return
                    
                    break
            
            new_line = "{}={}={}={}".format(logged_in_username.upper().strip(), line_list[1].strip().replace(".", ""), str(max(0, int(line_list[2].strip().replace(".", "")) + current_value)), str(line_list[3]))
            hydration_progress_variable.set("HYDRATION PROGRESS: {}ml / {}ml".format(max(0, int(line_list[2].strip().replace(".", "")) + current_value), line_list[1].strip().replace(".", "")))

            lines[index] = new_line
            user_data.seek(0)
            
            user_data.writelines(lines)
            user_data.truncate()
            user_data.close()
            return

def validate_integers(char):
    # Check if the character is a digit.
    if char.isdigit() or "-" in char or "+" in char:
        return True
    return False

# Create a canvas.
hydration_canvas = tk.Canvas(root, width=50, height=10, bd=0, highlightthickness=0)
hydration_canvas.place(relx=0.25, rely=0.6)

hydration_progress_label = Label(root, textvariable=hydration_progress_variable, fg="black", font=("Simplifica", 15))
calculator_button = ttk.Button(root, text="C A L C U L A T O R", image=button_image_tk, compound="center", command=goto_calculator_window)
leaedrboard_button = ttk.Button(root, image=leaderboard_button_image_tk, command=goto_leaderboard_window)
weather_button = ttk.Button(root, image=weather_button_image_tk, command=goto_weather_window)

# Create the subtract button canvas.
subtract_canvas = tk.Canvas(hydration_canvas, width=50, height=50, bd=0, highlightthickness=0)
subtract_canvas.pack(side=tk.LEFT)

add_label = Label(hydration_canvas, text="ADD (ML):", fg="black", font=("Simplifica", 15))
add_label.pack(side=tk.LEFT, before=subtract_canvas)

subtract_button = subtract_canvas.create_image(25, 25, image=minus_button_image_tk)
subtract_canvas.bind("<Button-1>", subtract_click)
validation = root.register(validate_integers)

# Create the textbox.
textbox = ttk.Entry(hydration_canvas, width=10)
textbox.pack(side=tk.LEFT)

textbox.insert(tk.END, "0")  # Set default value to 0.
textbox.configure(validate="key", validatecommand=(validation, "%S"))

# Create the add button canvas.
add_canvas = tk.Canvas(hydration_canvas, width=50, height=50, bd=0, highlightthickness=0)
add_canvas.pack(side=tk.LEFT)
add_button = add_canvas.create_image(25, 25, image=add_button_image_tk)
add_canvas.bind("<Button-1>", add_click)

# Create the set button canvas.
set_canvas = tk.Canvas(hydration_canvas, width=50, height=50, bd=0, highlightthickness=0)
set_canvas.pack(side=tk.LEFT)
set_button = set_canvas.create_image(15, 25, image=set_button_image_tk)
set_canvas.bind("<Button-1>", apply)

user_data = open(user_data_file, "r+")
lines = user_data.readlines()

# Set user progress upon getting to the homepage, if it has been created already.
# Loop through each line in the 'lines' list while keeping track of the index
for index, line in enumerate(lines):
    # Check if the uppercase and stripped logged-in username exists in the current line
    if logged_in_username.upper().strip() in line:
        # Set a flag indicating that the user is found
        user_found.set(True)
        
        # Split the line using '=' as the delimiter
        line_list = line.split("=")
        
        # Print the value from the fourth element in line_list
        print(int(line_list[3]))
        # Print the current time
        
        print(current_time)
        
        # Check if enough time (86400 seconds, or 24 hours) has passed since the last update
        if (current_time > int(line_list[3]) + 86400):            
            # Create a new line with updated values and remove decimals from the second element
            new_line = "{}={}={}={}\n".format(logged_in_username.upper().strip(), str(line_list[1].strip().replace(".", "")), 0, current_time)
            
            # Update the hydration progress variable and format it
            hydration_progress_variable.set("HYDRATION PROGRESS: {}ml / {}ml".format(0, line_list[1].strip().replace(".", "")))
            
            # Update the 'lines' list with the new line
            lines[index] = new_line
            
            # Open the user_data file and prepare to write data
            user_data.seek(0)
            
            # Write the modified 'lines' list back to the file and truncate any extra content
            user_data.writelines(lines)
            user_data.truncate()
            user_data.close()
            
            # Exit the loop since the update is done
            break
        
        # Check if the current hydration is equal to or greater than the recommended hydration
        if (int(line_list[2].strip().replace(".", "")) >= int(line_list[1].strip().replace(".", ""))):
            # Print a message indicating that the values are not the same
            print("Not the same value")
            
            # Create a new line with updated values
            new_line = "{}={}={}={}".format(logged_in_username.upper().strip(), str(line_list[1].strip().replace(".", "")), str(line_list[1].strip().replace(".", "")), str(line_list[3]))
            
            # Update the hydration progress variable and format it
            hydration_progress_variable.set("HYDRATION PROGRESS: {}ml / {}ml".format(line_list[1].strip().replace(".", ""), line_list[1].strip().replace(".", "")))
            
            # Update the 'lines' list with the new line
            lines[index] = new_line
            
            # Open the user_data file and prepare to write data
            user_data.seek(0)
            
            # Write the modified 'lines' list back to the file and truncate any extra content
            user_data.writelines(lines)
            user_data.truncate()
            user_data.close()
            
            # Hide the hydration canvas
            hydration_canvas.place_forget()
            
            # Exit the loop since the update is done
            break
        
        # Update the hydration progress variable and format it based on current and recommended hydration
        hydration_progress_variable.set("HYDRATION PROGRESS: {}ml / {}ml".format(line_list[2].strip().replace(".", ""), line_list[1].strip().replace(".", "")))
        
        # Set the user's current hydration value
        user_current_hydration.set(int(line_list[2].strip().replace(".", "")))
        
        # Set the user's recommended hydration value
        user_recommended_hydration.set(int(line_list[1].strip().replace(".", "")))
        
        # Close the user_data file
        user_data.close()
        
        # Exit the loop since the update is done
        break
    
# Check if the user was not found in the data
if (user_found.get() == False):
    # Set a message indicating that recommended hydration has not been calculated
    hydration_progress_variable.set("Recommended Hydration not yet Calculated")
    
    # Hide the hydration canvas
    hydration_canvas.place_forget()

# Configure the style for Button1
style_button1 = ttk.Style()
style_button1.configure("Button1.TButton", foreground="black", font=("Arial", 5))

# Configure the style for TButton with gray foreground and font size 16
style = ttk.Style()
style.configure("TButton", foreground="gray")
style.configure("TButton", font=("Arial", 16))

# Place labels.
waves_top_label.place(x=-2, y=-100)
waves_bottom_label.place(x=-2, y=210)
title_text_label.place(x=153, y=80)
hello_label.place(relx=0.5, rely=0.5, anchor = tk.CENTER)
signin_options_label.place(relx=0.5, rely=0.55, anchor = tk.CENTER)
hydration_progress_label.place(relx=0.5, rely=0.6, anchor = tk.CENTER)
user_icon_label.place(relx=0.5, y=220, anchor = tk.CENTER)
signup_button.place(x=140, y=450)
calculator_button.place(x=140, y=400)
leaedrboard_button.place(x=100, y=250)
weather_button.place(x=350, y=250)

waves_top_label.lower(waves_bottom_label)
menu_icon_label.lower(title_text_label)
waves_bottom_label.lower(menu_icon_label)

root.mainloop() # Start the main event loop.