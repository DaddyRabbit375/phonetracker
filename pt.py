

import phonenumbers
import folium
import requests
import tkinter as tk
from tkinter import messagebox
from phonenumbers import geocoder, timezone, carrier
from colorama import init
import webbrowser

init()

GOOGLE_API_KEY = "AIzaSyAg3k4niOVEwluNSIX2pHw3sMLKcDhmGoM"

def get_coordinates():
    """ 
    Fetch approximate latitude and longitude using Google's Geolocation API.
    """
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_API_KEY}"
    
    try:
        response = requests.post(url, json={})
        data = response.json()

        if "location" in data:
            lat = data["location"]["lat"]
            lon = data["location"]["lng"]
            return lat, lon
        else:
            return None, None
    except requests.exceptions.RequestException:
        return None, None

def process_number():
    phone_number = entry.get()
    try:
        parsed_number = phonenumbers.parse(phone_number)

        result_text.set("Processing...")

        # Get time zone, region, and carrier
        time_zones = timezone.time_zones_for_number(parsed_number)
        region = geocoder.description_for_number(parsed_number, "en")
        service_provider = carrier.name_for_number(parsed_number, "en")

        # Get coordinates using Google API
        lat, lon = get_coordinates()
        
        result = f"📞 Phone Number: {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}\n"
        result += f"⏰ Time Zone: {time_zones}\n"
        result += f"🌍 Region: {region if region else 'Unknown'}\n"
        result += f"📡 Service Provider: {service_provider if service_provider else 'Unknown'}\n"
        
        if lat and lon:
            result += f"📍 Approximate Location: Latitude {lat}, Longitude {lon}\n"
            
            # Generate Map
            map_location = folium.Map(location=[lat, lon], zoom_start=10)
            folium.Marker([lat, lon], popup=f"Approximate location of {phone_number}").add_to(map_location)
            
            # Save the map to an HTML file
            map_filename = "phone_location_map.html"
            map_location.save(map_filename)

            # Open map in the default web browser
            webbrowser.open(map_filename)
        else:
            result += "❌ Could not fetch precise location."

        # Update result text
        result_text.set(result)

    except phonenumbers.phonenumberutil.NumberParseException:
        messagebox.showerror("Error", "Invalid phone number format. Please enter a valid number with a country code.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create GUI window
root = tk.Tk()
root.title("Phone Number Tracker")

# Set window size and background color
root.geometry("500x400")  # Width x Height
root.configure(bg="#222831")  # Dark background

# Styling
font_main = ("Arial", 14, "bold")
font_result = ("Arial", 12)
button_color = "#00ADB5"
text_color = "#EEEEEE"

# Input Label
label = tk.Label(root, text="Enter Phone Number (e.g., +254718699047):", fg=text_color, bg="#222831", font=font_main)
label.pack(pady=10)

# Input Field
entry = tk.Entry(root, width=30, font=("Arial", 14))
entry.pack(pady=5)

# Submit Button
button = tk.Button(root, text="Track Number", command=process_number, font=font_main, bg=button_color, fg="white", padx=10, pady=5)
button.pack(pady=10)

# Result Display
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left", fg=text_color, bg="#222831", font=font_result, wraplength=450)
result_label.pack(pady=10)

# Run GUI
root.mainloop()
