"""
Weather checker part of Project: Hydrate.

Description:
 - This part of the program utilises a free weather API named OpenWeatherMap, 
   utilising an API key and a selected city via a dropdown
   The code will run through the API and report back certain data such as 
   temperature, humidity levels to determine if the user should
   drink more water as well as the weather condition displayed by an icon
"""

# Imports.
import subprocess
import sys

import threading
import tkinter as tk

from tkinter import ttk, Tk
import datetime

import requests
from PIL import Image, ImageTk

# Create the main window.
root = Tk()
root.geometry("495x595")

# Create the username variable.
LOGGED_IN_USERNAME = ""

# Check if a username is provided.
if len(sys.argv) > 1:
    LOGGED_IN_USERNAME = sys.argv[1]

# Set the window icon and title.
root.iconbitmap(default="assets\\icon.ico")
root.resizable(width=False, height=False)
root.title("Project Hydrate: Weather")

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

API_KEY = "c789f0f46b29c603479b296c6608f6f4"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q={city},nz&appid="

# Load images.
button_image = Image.open("assets\\buttonimage.png")
back_button_image = Image.open("assets\\backbutton.png")

waves_bottom = Image.open("assets\\wavesfullcropped.png")
weather_sunny_icon = Image.open("assets\\weathergoodicon.png")
weather_good_night_icon = Image.open("assets\\weathergoodnighticon.png")

weather_rainy_icon = Image.open("assets\\weatherrainyicon.png")
weather_dry_icon = Image.open("assets\\weatherdryicon.png")

weather_hot_icon = Image.open("assets\\weatherhoticon.png")
weather_title = Image.open("assets\\weathertitle.png")

# Resize images.
waves_bottom = waves_bottom.resize((495, 395))
button_image = button_image.resize((200, 30))

back_button_image = back_button_image.resize((30, 30))
weather_title = weather_title.resize((300, 45))

# Create image objects.
waves_bottom_tk = ImageTk.PhotoImage(waves_bottom)
weather_sunny_icon_tk = ImageTk.PhotoImage(weather_sunny_icon)
weather_good_night_icon_tk = ImageTk.PhotoImage(weather_good_night_icon)

weather_rainy_icon_tk = ImageTk.PhotoImage(weather_rainy_icon)
weather_dry_icon_tk = ImageTk.PhotoImage(weather_dry_icon)

weather_hot_icon_tk = ImageTk.PhotoImage(weather_hot_icon)
weather_title_tk = ImageTk.PhotoImage(weather_title)

style_button1 = ttk.Style()
style_button1.configure("Button1.TButton", foreground="black", font=("Arial", 5))

style = ttk.Style()
style.configure("TButton", foreground="gray")
style.configure("TButton", font=("Arial", 12))

# Function to close the current window and open the
# home window with the specified logged-in username
def goto_home_window():
    """
    Close the current window and navigate to the home window.
    """

    root.destroy()  # Close the current window
    subprocess.call(["python", "home.py", LOGGED_IN_USERNAME])  # Open the home window

# Function to retrieve weather data for a given city
def get_weather_data(city):
    """
    Retrieve weather data for a given city using the OpenWeatherMap API.
    """

    url = BASE_URL.format(city=city) + API_KEY
    response = requests.get(url, timeout=30)
    data = response.json()
    return data

# Function to convert Unix time to a formatted timestamp
def unix_time_to_timestamp(unix_time):
    """
    Convert Unix time to a formatted timestamp.
    """

    # Convert Unix time to a datetime object
    dt_object = datetime.datetime.fromtimestamp(unix_time)

    # Format the timestamp as required
    formatted_timestamp = dt_object.strftime("WEATHER INFO LAST UPDATED: %I:%M:%S%p")

    last_updated_variable.set(formatted_timestamp)  # Set the last_updated_variable
    return formatted_timestamp

# Function to check if it's night time based on weather data
def is_night_time(weather_data):
    """
    Check if it's night time based on weather data.
    """

    current_time = weather_data["dt"]

    unix_time_to_timestamp(current_time)  # Convert and set the last updated timestamp
    sunrise_time = weather_data["sys"]["sunrise"]
    sunset_time = weather_data["sys"]["sunset"]

    return current_time > sunset_time or current_time < sunrise_time

# Function to determine the recommended drinking amount based on weather data
def determine_drinking_amount(weather_data):
    """
    Determine the recommended drinking amount based on weather data.
    """

    weather_id = weather_data['weather'][0]['id']
    temp_kelvin = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']

    temp_celsius = temp_kelvin - 273.15  # Convert temperature from Kelvin to Celsius
    temp_celsius_rounded = round(temp_celsius, 2)  # Round temperature to two decimal points
    celsius_character = "°C"

    print(f"The temperature right now is: {temp_celsius_rounded}{celsius_character}")
    temperature_message.set(
        f"The temperature right now is: {temp_celsius_rounded}{celsius_character}"
    )

    is_night = is_night_time(weather_data)  # Check if it's night time

    if weather_id >= 200 and weather_id < 600:
        weather_label.configure(image=weather_rainy_icon_tk)
        return "Drink more water. It's raining today!"
    elif humidity < 30:
        weather_label.configure(image=weather_dry_icon_tk)
        return "Drink more water. It's particularly dry today!"
    elif temp_celsius > 30:
        weather_label.configure(image=weather_hot_icon_tk)
        return "Drink more water. It's hot today!"
    else:
        if not is_night:
            weather_label.configure(image=weather_sunny_icon_tk)
        else:
            weather_label.configure(image=weather_good_night_icon_tk)
        return "Weather is good! You can drink the same amount as usual."

# Function to handle fetching and displaying weather data
def handle_weather():
    """
    Fetch weather data and update the interface with the recommended message.
    """

    selected_city = city_variable.get()
    if selected_city:
        weather_data = get_weather_data(selected_city)
        message = determine_drinking_amount(weather_data)
        weather_message.set(message)

# Function to display weather data and update the interface
def display_weather():
    """
    Display weather data and update the interface with the recommended message.
    """

    temperature_message.set("")
    last_updated_variable.set("")

    if weather_message.get() == "PRESS CHECK WEATHER TO DISPLAY WEATHER INFO":
        weather_message.set("FETCHING WEATHER DATA...")
        print("Fetching")
    else:
        weather_message.set("REFRESHING...")
        print("Refreshing")

    weather_label.configure(image="")  # Clear the weather image

    # Create a thread to handle fetching and displaying weather data
    weather_data_thread = threading.Thread(target=handle_weather)
    weather_data_thread.start()

# Creating the back button and its functionality.
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

weather_label = tk.Label(root, image="")
weather_label.place(relx=0.5, y=160, anchor=tk.CENTER)

weather_title_label = tk.Label(root, image=weather_title_tk)
weather_title_label.place(relx=0.5, y=70, anchor=tk.CENTER)

# Create a dropdown menu for city selection
cities = [
    "Auckland", "Auckland", "Wellington", 
    "Christchurch", "Hamilton", "Tauranga", 
    "Dunedin", "Palmerston North",
    "Napier", "Nelson", "Rotorua", 
    "New Plymouth", "Whangarei", "Invercargill", 
    "Whanganui", "Gisborne", "Lower Hutt",
    "Upper Hutt", "Wanaka", "Queenstown",
    "Taupo"
]

city_variable = tk.StringVar()
city_variable.set("Auckland")  # Default selected city

city_label = ttk.Label(root, text="Select City:", font=("Simplifica", 15, "bold"))
city_label.place(relx=0.5, y=345, anchor=tk.CENTER)

last_updated_variable = tk.StringVar()
last_updated_variable.set("")

last_updated_label = ttk.Label(root, textvariable=last_updated_variable, font=("Simplifica", 10))
last_updated_label.place(relx=0.5, y=450, anchor=tk.CENTER)

city_dropdown = ttk.OptionMenu(root, city_variable, *cities)
city_dropdown.place(relx=0.5, y=375, anchor=tk.CENTER)

waves_bottom_label = tk.Label(root, image=waves_bottom_tk)

# Create a label to display the message
weather_message = tk.StringVar()
weather_message.set("PRESS CHECK WEATHER TO DISPLAY WEATHER INFO")

temperature_message = tk.StringVar()
temperature_message.set("")

message_label = ttk.Label(root, textvariable=weather_message, font=("Simplifica", 16))
message_label.place(relx=0.5, y=250, anchor=tk.CENTER)

temperature_label = ttk.Label(
    root,
    textvariable=temperature_message,
    font=("Simplifica", 16, "bold")
)

temperature_label.place(relx=0.5, y=280, anchor=tk.CENTER)

waves_bottom_label.lower(last_updated_label)
waves_bottom_label.lower(city_dropdown)
waves_bottom_label.lower(city_label)

waves_bottom_label.place(x=-2, y=210)

# Create a button to fetch weather data and display the message
fetch_button = ttk.Button(
    root,
    text="C H E C K  W E A T H E R",
    image=button_image_tk,
    compound="center",
    command=display_weather
)

fetch_button.place(relx=0.5, y=420, anchor=tk.CENTER)

# Run the main event loop.
root.mainloop()
