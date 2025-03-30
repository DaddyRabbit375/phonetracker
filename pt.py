

import phonenumbers
import folium
import sys
import argparse
import os
from phonenumbers import geocoder, timezone, carrier
from colorama import init, Fore

# Initialize colorama
init()

def process_number(number):
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(number)

        print(f"{Fore.GREEN}[+] Attempting to track location of "
              f"{phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}..")

        # Get and display the time zone
        print(f"{Fore.GREEN}[+] Time Zone ID: {timezone.time_zones_for_number(parsed_number)}")

        # Get the geographic location of the phone number
        location = geocoder.description_for_number(parsed_number, "en")
        if location:
            print(f"{Fore.GREEN}[+] Region: {location}")
        else:
            print(f"{Fore.RED}[-] Region: Unknown")

        # Get the service provider (carrier)
        carrier_name = carrier.name_for_number(parsed_number, 'en')
        if carrier_name:
            print(f"{Fore.GREEN}[+] Service Provider: {carrier_name}")

    except phonenumbers.phonenumberutil.NumberParseException:
        print(f"{Fore.RED}[-] Invalid phone number format. Please enter a valid number with a country code.")
        sys.exit()
    except Exception as e:
        print(f"{Fore.RED}[-] An error occurred: {str(e)}")
        sys.exit()

# Ensure this runs only when executed directly
if __name__ == "__main__":
    phone_number = input("Enter phone number with country code (e.g., +14155552671): ")
    process_number(phone_number)
