import requests
from bs4 import BeautifulSoup

class ApiClient:
    def __init__(self, base_url):
        # Initialize with the given base URL
        self.base_url = base_url

    def check_registration_number(self, registration_number):
        """
        Check the registration number by scraping the website.
        - Constructs the URL using the base URL and the registration number.
        - Sends a GET request to the URL.
        - Parses the response to check for specific text indicating if it's a police vehicle.
        - Returns True if the vehicle is flagged as a police vehicle, otherwise False.
        """
        url = f"{self.base_url}{registration_number}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            if "Nojjigt" in soup.text:
                print("**************************")
                return True  # Indicates it's a police vehicle
            elif "Nepp" in soup.text:
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                return False  # Indicates it's not a police vehicle
        return None  # Indicates an error or unknown result
