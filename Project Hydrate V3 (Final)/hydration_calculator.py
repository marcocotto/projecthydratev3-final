"""
Hydration calculator page part of Project: Hydrate.

Description:
 - Records user weight via an entry box
 - Records user gender and records user activity level
   then calculates based on their inputs what their recommended hydration should be
"""

# Imports.
import subprocess
import sys

import tkinter as tk
from tkinter import ttk, Tk

import time
import threading
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

root.resizable(width=False, height=False)
root.title("Project Hydrate: Hydration Calculator")

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

# Function to navigate back to the home window.
def goto_home_window():
    """
    Redirect the user back to home page.
    """

    root.destroy()
    subprocess.Popen(["python", "home.py", LOGGED_IN_USERNAME])

canvas = tk.Canvas(root, width=300, height=400)
canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

invalid_weight_label = ttk.Label(
    canvas,
    text="You must input a weight!",
    foreground="red",
    font=("Arial", 10)
)

weight_success_label = ttk.Label(
    canvas,
    text="Weight successfully calculated!",
    foreground="green",
    font=("Arial", 10, "bold")
)

# Function to display a success message when hydration has been calculated.
def weight_success_message():
    """
    Display a success message indicating successful hydration calculation.
    """

    weight_success_label.place(relx=0.5, y=295, anchor=tk.CENTER)
    time.sleep(2)

    weight_success_label.place_forget()


# Function to display a warning if the weight input is left blank.
def invalid_weight_warning():
    """
    Display a warning message for invalid weight input.
    """

    invalid_weight_label.place(relx=0.5, y=295, anchor=tk.CENTER)
    time.sleep(2)

    invalid_weight_label.place_forget()

# Function to calculate hydration.
def calculate_hydration():
    """
    Calculate recommended hydration based on user inputs.
    """

    # Check if weight entry is empty
    if weight_entry.get() == "":
        # Create a thread to display an invalid weight warning
        invalid_weight_thread = threading.Thread(target=invalid_weight_warning)
        invalid_weight_thread.start()
    else:
        # Retrieve weight value from entry field
        weight = int(weight_entry.get())

        # Get selected gender and activity level
        gender = gender_var.get()
        activity_level = activity_var.get()

        # Initialize base hydration and hydration multiplier
        base_hydration = 0
        hydration_multiplier = 1.0

        # Calculate base hydration based on weight
        base_hydration += weight * 0.03

        # Adjust base hydration based on gender
        if gender == "Male":
            base_hydration += 0.2
        elif gender == "Female":
            base_hydration -= 0.1

        # Adjust hydration multiplier based on activity level
        if activity_level == "RARELY ACTIVE":
            hydration_multiplier += 0.1
        elif activity_level == "SOMEWHAT ACTIVE":
            hydration_multiplier += 0.2
        elif activity_level == "QUITE ACTIVE":
            hydration_multiplier += 0.3
        elif activity_level == "EXTREMELY ACTIVE":
            hydration_multiplier += 0.4

        # Create a thread to display a weight success message
        success_thread = threading.Thread(target=weight_success_message)
        success_thread.start()

        # Calculate recommended hydration based on base hydration and multiplier
        recommended_hydration = int(round(base_hydration * hydration_multiplier, 4) * 1000)

        # Update the result label with recommended hydration
        result_label.config(
            text=f"Recommended hydration: {recommended_hydration / 1000} liters"
        )

        # Initialize and set a boolean variable to track user data presence
        user_found = tk.BooleanVar()
        user_found.set(False)

        # Open user data file for reading and writing
        user_data = open(USER_DATA_FILE, "r+", encoding="utf-8")
        lines = user_data.readlines()

        # Loop through lines in the user data
        for index, line in enumerate(lines):
            # Check if the logged-in username is in the current line
            if LOGGED_IN_USERNAME.upper().strip() in line:
                # Set the user found flag to True
                user_found.set(True)

                # Split the line into a list
                line_list = line.split("=")

                # Create a new line with updated recommended hydration and timestamp
                username_stripped = LOGGED_IN_USERNAME.upper().strip()
                goal_hyd = str(recommended_hydration).strip()
                set_hyd = line_list[2]

                new_line = (
            f"{username_stripped}={goal_hyd}={set_hyd}={int(time.time())}\n"
                )

                # Update the line in the 'lines' list
                lines[index] = new_line

                # Move the file pointer to the beginning
                user_data.seek(0)

                # Write the modified 'lines' list back to the file and truncate any extra content
                user_data.writelines(lines)
                user_data.truncate()

                # Return since the update is complete
                return

        # If user data not found, add a new line with recommended hydration and timestamp
        if not user_found.get():
            # Write a new line with the updated information
            username_stripped = LOGGED_IN_USERNAME.upper().strip()
            goal_hyd = str(recommended_hydration).strip()

            new_line = (
            f"{username_stripped}={goal_hyd}={0}={int(time.time())}\n"
            )

            # Close the user data file
            user_data.write(new_line)
            user_data.close()

            # Return since the update is complete
            return

# Function to validate integers and allowed characters
def validate_integers(char):
    """
    Validate if the entered character is a digit, plus sign, or minus sign.
    """

    # Check if the character is a digit, plus sign, or minus sign
    if char.isdigit() or "-" in char or "+" in char:
        return True
    return False

# Load images.
waves_bottom = Image.open("assets\\wavesfullcropped.png")
button_image = Image.open("assets\\buttonimage.png")
calculator_title = Image.open("assets\\calculatortitle.png")

# Resize images.
waves_bottom = waves_bottom.resize((495, 395))
button_image = button_image.resize((200, 30))
calculator_title = calculator_title.resize((300, 45))

# Create image objects.
waves_bottom_tk = ImageTk.PhotoImage(waves_bottom)
calculator_title_tk = ImageTk.PhotoImage(calculator_title)

# Create label objects.
waves_bottom_label = tk.Label(root, image=waves_bottom_tk)
calculator_title_label = tk.Label(root, image=calculator_title_tk)

# Creating the back button and its functionality.
back_button_image = Image.open("assets\\backbutton.png")
back_button_image = back_button_image.resize((30, 30))

button_image_tk = ImageTk.PhotoImage(button_image)
back_button_image_tk = ImageTk.PhotoImage(back_button_image)

back_button = ttk.Button(
    root,
    image=back_button_image_tk,
    compound="center",
    width=0,
    command=goto_home_window
)

back_button.place(x=20, y=20)
waves_bottom_label.place(x=-2, y=210)

style_button1 = ttk.Style()
style_button1.configure("Button1.TButton", foreground="black", font=("Arial", 5))

style = ttk.Style()
style.configure("TButton", foreground="gray")
style.configure("TButton", font=("Arial", 16))

# Creating the weight label and entry field.
validation = root.register(validate_integers)
weight_label = ttk.Label(root, text="WEIGHT (IN KG):", font=("Simplifica", 15, "bold"))
weight_entry = ttk.Entry(root)
weight_entry.configure(validate="key", validatecommand=(validation, "%S"))
canvas.create_window(150, 30, window=weight_label)
canvas.create_window(150, 60, window=weight_entry)

#weight_label = ttk.tk.Label(root, text="C A L C U L A T O R", font=("Simplifica", 25, "bold"))
#weight_label.place(relx=0.5, y=70, anchor=tk.CENTER)

calculator_title_label.place(relx=0.5, y=70, anchor=tk.CENTER)

# Creating the gender label and radio buttons.
gender_label = ttk.Label(root, text="GENDER:", font=("Simplifica", 15, "bold"))
canvas.create_window(150, 90, window=gender_label)
gender_var = tk.StringVar()
gender_var.set("MALE")
gender_male_radiobutton = ttk.Radiobutton(root, text="MALE", variable=gender_var, value="MALE")
gender_female_radiobutton = ttk.Radiobutton(
    root,
    text="FEMALE",
    variable=gender_var,
    value="FEMALE"
)

canvas.create_window(110, 120, window=gender_male_radiobutton)
canvas.create_window(190, 120, window=gender_female_radiobutton)

# Creating the activity level label and radio buttons.
activity_label = ttk.Label(root, text="ACTIVITY  LEVEL:", font=("Simplifica", 15, "bold"))
canvas.create_window(150, 150, window=activity_label)
activity_var = tk.StringVar()
activity_var.set("RARELY ACTIVE")
activity_radiobuttons = [
    "RARELY ACTIVE",
    "SOMEWHAT ACTIVE",
    "QUITE ACTIVE",
    "EXTREMELY ACTIVE"
]

Y_POSITION = 180

for activity in activity_radiobuttons:
    activity_radiobutton = ttk.Radiobutton(
        root,
        text=activity,
        variable=activity_var,
        value=activity
    )

    canvas.create_window(150, Y_POSITION, window=activity_radiobutton)
    Y_POSITION += 30

calculate_button = ttk.Button(
    root,
    text="C A L C U L A T E",
    image=button_image_tk,
    compound="center",
    command=calculate_hydration
)

canvas.create_window(150, Y_POSITION + 30, window=calculate_button)

# Creating the result label.
result_label = ttk.Label(root, text="")
canvas.create_window(150, Y_POSITION + 60, window=result_label)

waves_bottom_label.lower(canvas)
waves_bottom_label.lower(invalid_weight_label)

root.mainloop() # Start the main event loop.
