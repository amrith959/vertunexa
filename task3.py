import requests
import tkinter as tk
from tkinter import messagebox

# === WeatherStack API Info ===
API_KEY = "2ce2fbef1fd29b2deaa9e0b70b782d8f"  
BASE_URL = "http://api.weatherstack.com/current"

# === Weather Fetching Function ===
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    params = {
        "access_key": API_KEY,
        "query": city
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if "error" in data:
            weather_output.config(text=f"Error: {data['error']['info']}")
            return

        location = f"{data['location']['name']}, {data['location']['country']}"
        temperature = data['current']['temperature']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_speed']

        result = (
            f"Location: {location}\n"
            f"Temperature: {temperature} °C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} km/h"
        )

        weather_output.config(text=result)

    except requests.RequestException as e:
        weather_output.config(text=f"Network error: {e}")

# === GUI Setup ===
app = tk.Tk()
app.title("Weather App")
app.geometry("350x300")
app.resizable(False, False)

# Input field
tk.Label(app, text="Enter City Name:", font=("Arial", 12)).pack(pady=10)
city_entry = tk.Entry(app, font=("Arial", 12), width=25)
city_entry.pack()

# Button
tk.Button(app, text="Get Weather", font=("Arial", 12), command=get_weather).pack(pady=10)

# Output display
weather_output = tk.Label(app, text="", font=("Arial", 11), justify="left", wraplength=300)
weather_output.pack(pady=20)

# Start the app
app.mainloop()
