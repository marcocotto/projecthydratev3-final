"""
Home page part of Project: Hydrate (biggest file).

Description:
 - Biggest part of the program, this file checks 
   the current logged in user, and checks if they've
   already calculated their hydration.
   If they haven't, they will be prompted to by clicking 
   the Calculator button.
 - This page is the main root of the user's user interface 
   to access all features such as calculator, weather and leaderboard.
 - In this the user is also able to add or subtract amounts in 
   ML to their hydration and track towards their goal via the entry box.
"""

# Imports.
import subprocess
import sys

import tkinter as tk
from tkinter import ttk, Tk

import time
from PIL import Image, ImageTk

root = Tk()
root.geometry("495x595")

# Create the username variable.
LOGGED_IN_USERNAME = ""

# Check if a username is provided.
if len(sys.argv) > 1:
    LOGGED_IN_USERNAME = sys.argv[1]

root.iconbitmap(default="assets\\icon.ico")
USER_DATA_FILE = "db\\user_data.txt"
LEADERBOARD_DATA_FILE = "db\\leaderboard_data.txt"

# Function to go to the main window.
def goto_main_window():
    """
    Destroy the current window and navigate to the main window.
    """

    root.destroy()
    subprocess.Popen(["python", "main.py"])

# Function to go to the hydration calculator window.
def goto_calculator_window():
    """
    Destroy the current window and navigate to the hydration calculator window.
    """

    root.destroy()
    subprocess.Popen(["python", "hydration_calculator.py", LOGGED_IN_USERNAME])

# Function to go to the leaderboard window.
def goto_leaderboard_window():
    """
    Destroy the current window and navigate to the leaderboard window.
    """

    root.destroy()
    subprocess.Popen(["python", "leaderboard.py", LOGGED_IN_USERNAME])
# Function to go to the weather window.
def goto_weather_window():
    """
    Destroy the current window and navigate to the weather window.
    """

    root.destroy()
    subprocess.Popen(["python", "weather.py", LOGGED_IN_USERNAME])

# Set window properties
root.resizable(width=False, height=False)
root.title("Project Hydrate: Home")

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

# Load images.
menu_icon = Image.open("assets\\iconmain.png")
waves_bottom = Image.open("assets\\wavesfullcropped.png")
title_text_icon = Image.open("assets\\titletext.png")
button_image = Image.open("assets\\buttonimage.png")
user_icon = Image.open("assets\\iconuser.png")
waves_top = Image.open("assets\\topwaves.png")
add_button_image = Image.open("assets\\plusicon.png")
minus_button_image = Image.open("assets\\minusicon.png")
set_button_image = Image.open("assets\\seticon.png")
leaderboard_button_image = Image.open("assets\\leaderboardicon.png")
weather_button_image = Image.open("assets\\weathericon.png")

# Resize images.
menu_icon = menu_icon.resize((108, 141))
waves_bottom = waves_bottom.resize((495, 395))
title_text_icon = title_text_icon.resize((182, 70))
button_image = button_image.resize((200, 30))
user_icon = user_icon.resize((100, 100))
waves_top = waves_top.resize((495, 595))
add_button_image = add_button_image.resize((20, 20))
minus_button_image = minus_button_image.resize((20, 20))
set_button_image = set_button_image.resize((20, 20))
leaderboard_button_image = leaderboard_button_image.resize((40, 40))
weather_button_image = weather_button_image.resize((40, 40))

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
menu_icon_label = tk.Label(root, image=menu_icon_tk)
waves_bottom_label = tk.Label(root, image=waves_bottom_tk)

title_text_label = tk.Label(root, image=title_text_icon_tk)
user_icon_label = tk.Label(root, image=user_icon_tk)
waves_top_label = tk.Label(root, image=waves_top_tk)

# Create the username variable and set it as the passed username,
# and if it doesn"t exist set it to NIL.
username_variable = tk.StringVar()
username_variable.set("")

hydration_progress_variable = tk.StringVar()
hydration_progress_variable.set("")

if not LOGGED_IN_USERNAME == "":
    username_variable.set(str(LOGGED_IN_USERNAME) + "!")
else:
    LOGGED_IN_USERNAME = "NIL"
    username_variable.set("NIL!")

user_found = tk.BooleanVar()
user_found.set(False)

user_current_hydration = tk.IntVar()
user_current_hydration.set(0)

user_recommended_hydration = tk.IntVar()
user_recommended_hydration.set(0)

current_time = int(time.time())

signin_options_label = tk.Label(
    root,
    textvariable=username_variable,
    fg="black",
    font=("Simplifica", 20, "bold")
)

hello_label = tk.Label(root, text="HELLO", fg="black", font=("Simplifica", 20))
signup_button = ttk.Button(
    root,
    text="L O G  O U T",
    image=button_image_tk,
    compound="center",
    command=goto_main_window
)

# Function to handle subtract canvas click event.
def subtract_click(event):
    """
    Handle the click event for subtracting.
    """
    event = event or None

    subtract_canvas.move(subtract_button, 0, 2)
    subtract_canvas.after(100, lambda: subtract_canvas.move(subtract_button, 0, -2))
    subtract(event)

# Function to handle add canvas click event.
def add_click(event):
    """
    Handle the click event for adding.
    """
    event = event or None

    add_canvas.move(add_button, 0, 2)
    add_canvas.after(100, lambda: add_canvas.move(add_button, 0, -2))
    add(event)

# Functions to handle adding and subtracting values.
def subtract(event):
    """
    Subtract a value from the textbox value.
    """
    event = event or None

    if textbox.get() == "":
        textbox.delete(0, tk.END)
        textbox.insert(tk.END, 0)

    current_value = int(textbox.get())
    new_value = current_value - 250
    textbox.delete(0, tk.END)
    textbox.insert(tk.END, str(new_value))

def add(event):
    """
    Add a value to the textbox value.
    """

    event = event or None

    if textbox.get() == "":
        textbox.delete(0, tk.END)
        textbox.insert(tk.END, 0)

    current_value = int(textbox.get())
    new_value = current_value + 250
    textbox.delete(0, tk.END)
    textbox.insert(tk.END, str(new_value))

# Function to apply changes to user's hydration status based on input event
def apply(event):
    """
    Apply the changes to the user's hydration based on entered value.
    """

    event = event or None

    # Check if the textbox is empty
    if textbox.get() == "":
        textbox.delete(0, tk.END)
        textbox.insert(tk.END, 0)

    # Get the current value from the textbox
    current_value = int(textbox.get())

    # Create a visual effect by temporarily moving the set button
    set_canvas.move(set_button, 0, 2)
    set_canvas.after(100, lambda: set_canvas.move(set_button, 0, -2))

    # Clear the textbox and set it to 0
    textbox.delete(0, tk.END)
    textbox.insert(tk.END, 0)

    # Open the user data file for reading and writing
    user_data_1 = open(USER_DATA_FILE, "r+", encoding="utf-8")
    data_lines = user_data_1.readlines()
    user_found.set(False)  # Initialize a flag to track user presence

    # Loop through lines in the user data
    for data_index, data_line in enumerate(data_lines):
        # Check if the logged-in username is in the current line
        if LOGGED_IN_USERNAME.upper().strip() in data_line:
            user_found.set(True)  # Set the user found flag to True
            data_line_list = data_line.split("=")
            # Check if the user has exceeded the recommended hydration amount
            user_data_value = int(data_line_list[2].strip().replace(".", "")) + current_value
            if user_data_value >= int(data_line_list[1].strip().replace(".", "")):
                print("User has drank more than the recommended amount!")
                # Update the user's hydration data to match the recommended amount
                username_formatted = LOGGED_IN_USERNAME.upper().strip()
                user_goal_hyd= str(data_line_list[1].strip().replace(".", ""))
                user_set_hyd = str(data_line_list[1].strip().replace(".", ""))

                new_data_line = (
        f"{username_formatted}={user_goal_hyd}={user_set_hyd}={current_time}\n"
                )

                print("set 1")

                hydration_progress_variable.set(
                    f"HYDRATION PROGRESS: {user_goal_hyd}ml / {user_set_hyd}ml"
                )

                data_lines[data_index] = new_data_line

                user_data_1.seek(0)  # Move the file pointer to the beginning
                user_data_1.writelines(data_lines)  # Update list back to the file
                user_data_1.truncate()  # Truncate any extra content from the file
                user_data_1.close()

                hydration_canvas.place_forget()  # Hide the hydration canvas

                leaderboard_user_found = tk.BooleanVar()  # Bool

                # Open the leaderboard data file for reading and writing
                leaderboard_data = open(LEADERBOARD_DATA_FILE, "r+", encoding="utf-8")
                l_lines = leaderboard_data.readlines()
                leaderboard_user_found.set(False)  # Initialize the leaderboard user found flag

                # Loop through lines in the leaderboard data
                for l_index, l_line in enumerate(l_lines):
                    # Check if the logged-in username is in the current line
                    if LOGGED_IN_USERNAME.upper().strip() in l_line:
                        leaderboard_user_found.set(True)  # Set to true
                        leaderboard_line_list = l_line.split("=")

                        # Update the leaderboard entry with increased count
                        leaderboard_username = LOGGED_IN_USERNAME.upper().strip()
                        leaderboard_score = str(int(leaderboard_line_list[1]) + 1)
                        leaderboard_new_line = f"{leaderboard_username}={leaderboard_score}\n"

                        l_lines[l_index] = leaderboard_new_line

                        leaderboard_data.seek(0)  # Move the file pointer to the beginning
                        leaderboard_data.writelines(l_lines)  # Update the file
                        leaderboard_data.truncate()  # Truncate any extra content from the file
                        return

                # If leaderboard user not found, create a new entry
                if not leaderboard_user_found.get():
                    leaderboard_line_list = line.split("=")
                    leaderboard_data.write(f"{LOGGED_IN_USERNAME.upper().strip()}={str(1)}\n")
                    leaderboard_data.close()
                    return

                break

            # Update the user's hydration data based on the entered value
            username_stripped = LOGGED_IN_USERNAME.upper().strip()
            goal_hyd = line_list[1].strip().replace(".", "")
            set_hyd_updated = str(
                max(0, int(line_list[2].strip().replace(".", "")) + current_value)
            )

            updated_new_line = (
        f"{username_stripped}={goal_hyd}={set_hyd_updated}={str(line_list[3])}"
            )
            hydration_progress_variable.set(
                f"HYDRATION PROGRESS: {set_hyd_updated}ml / {goal_hyd}ml"
            )

            data_lines[data_index] = updated_new_line

            user_data_1.seek(0)  # Move the file pointer to the beginning
            user_data_1.writelines(data_lines)  # Write the modified 'lines' list back to the file
            user_data_1.truncate()  # Truncate any extra content from the file
            user_data_1.close()

            return

def validate_integers(char):
    """
    Check characters upon being registered.
    Check if they are digits.
    """
    # Check if the character is a digit.
    if char.isdigit() or "-" in char or "+" in char:
        return True
    return False

# Create a canvas.
hydration_canvas = tk.Canvas(root, width=50, height=10, bd=0, highlightthickness=0)
hydration_canvas.place(relx=0.25, rely=0.6)

hydration_progress_label = tk.Label(
    root,
    textvariable=hydration_progress_variable,
    fg="black",
    font=("Simplifica", 15)
)

calculator_button = ttk.Button(
    root,
    text="C A L C U L A T O R",
    image=button_image_tk,
    compound="center",
    command=goto_calculator_window
)

leaedrboard_button = ttk.Button(
    root,
    image=leaderboard_button_image_tk,
    command=goto_leaderboard_window
)

weather_button = ttk.Button(root, image=weather_button_image_tk, command=goto_weather_window)

# Create the subtract button canvas.
subtract_canvas = tk.Canvas(hydration_canvas, width=50, height=50, bd=0, highlightthickness=0)
subtract_canvas.pack(side=tk.LEFT)

add_label = tk.Label(hydration_canvas, text="ADD (ML):", fg="black", font=("Simplifica", 15))
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

user_data = open(USER_DATA_FILE, "r+", encoding="utf-8")
lines = user_data.readlines()

# Set user progress upon getting to the homepage, if it has been created already.
# Loop through each line in the 'lines' list while keeping track of the index
for index, line in enumerate(lines):
    # Check if the uppercase and stripped logged-in username exists in the current line
    if LOGGED_IN_USERNAME.upper().strip() in line:
        # Set a flag indicating that the user is found
        user_found.set(True)

        # Split the line using '=' as the delimiter
        line_list = line.split("=")

        # Print the value from the fourth element in line_list
        print(int(line_list[3]))
        # Print the current time

        print(current_time)

        # Check if enough time (86400 seconds, or 24 hours) has passed since the last update
        if current_time > int(line_list[3]) + 86400:
            # Create a new line with updated values and remove decimals from the second element
            USENRAME = LOGGED_IN_USERNAME.upper().strip()
            USER_GOAL_HYDR = str(line_list[1].strip().replace(".", ""))

            new_line = f"{USENRAME}={USER_GOAL_HYDR}={0}={current_time}\n"

            # Update the hydration progress variable and format it
            hydration_progress_variable.set(f"HYDRATION PROGRESS: {0}ml / {USER_GOAL_HYDR}ml")

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
        GOAL_HYDR = int(line_list[2].strip().replace(".", ""))

        if GOAL_HYDR >= int(line_list[1].strip().replace(".", "")):
            # Print a message indicating that the values are not the same
            print("Not the same value")

            # Create a new line with updated values
            CURRENT_USENRAME = LOGGED_IN_USERNAME.upper().strip()
            USER_GOAL_HYD = str(line_list[1].strip().replace(".", ""))

            new_line = (
    f"{CURRENT_USENRAME}={USER_GOAL_HYD}={USER_GOAL_HYD}={str(line_list[3])}"
            )

            # Update the hydration progress variable and format it
            hydration_progress_variable.set(
                f"HYDRATION PROGRESS: {USER_GOAL_HYD}ml / {USER_GOAL_HYD}ml"
            )

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

        # Update the hydration progress variable and
        # format it based on current and recommended hydration
        USER_SET_HYD = str(line_list[2].strip().replace(".", ""))
        USER_GOAL_HYD = str(line_list[1].strip().replace(".", ""))

        hydration_progress_variable.set(
            f"HYDRATION PROGRESS: {USER_SET_HYD}ml / {USER_GOAL_HYD}ml"
        )

        # Set the user's current hydration value
        user_current_hydration.set(int(line_list[2].strip().replace(".", "")))

        # Set the user's recommended hydration value
        user_recommended_hydration.set(int(line_list[1].strip().replace(".", "")))

        # Close the user_data file
        user_data.close()

        # Exit the loop since the update is done
        break

# Check if the user was not found in the data
if not user_found.get():
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
