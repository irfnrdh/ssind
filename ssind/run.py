## OLD version 0.1.0

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from datetime import datetime
import os
import requests
import click
import json
import base64

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode

# Set up the path to your ChromeDriver executable
chrome_driver_path = '/usr/bin/chromedriver'

# Create a base directory to store the screenshots
base_directory = 'screenshots'
os.makedirs(base_directory, exist_ok=True)

# Create a log file
log_file = open('website_status.log', 'w')

# Define the screen sizes to capture
screen_sizes = [
    (320, 1920),
    (320, 480),   # Mobile portrait
    (768, 1024),  # Tablet portrait
    (1440, 900),  # Laptop
    (1920, 1080)  # Desktop
]

BANNER = """
SCREENSHOT-IND
"""

@click.command()
@click.option('--clear', is_flag=True, help='Clear screenshots folder and logs')
@click.option('--config', default='websites.json', help='Specify the path to the JSON config list of website file')
def capture_screenshots(clear, config):
    if clear:
        clear_screenshots_folder()
        clear_log_file()
        return

    websites = load_websites_from_json(config)

    # Set up the ChromeDriver service
    service = Service(chrome_driver_path)

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Iterate through the websites, screen sizes, and capture screenshots
    for website in tqdm(websites, desc="Capturing Screenshots"):
        url = website['url']
        name = website['name']

        # Create a directory for the current website
        website_directory = os.path.join(base_directory, name)
        os.makedirs(website_directory, exist_ok=True)

        # Check the website status and measure the loading time
        start_time = datetime.now()
        try:
            response = requests.get(url)
            status_code = response.status_code
        except requests.exceptions.RequestException:
            status_code = "Error"
        end_time = datetime.now()
        loading_time = end_time - start_time

        # Log the website status and loading time in the terminal and log file
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {name} ({url}): {status_code}, Loading Time: {loading_time}"
        # print(log_entry)
        log_file.write(log_entry + '\n')

        driver.get(url)
        # Wait for the page to load completely
        driver.implicitly_wait(10)  # Adjust the waiting time if needed

        # Capture screenshots for each screen size
        for index, (width, height) in enumerate(screen_sizes):
            # Adjust window size to match the current screen size
            driver.set_window_size(width, height)

            # Calculate the total scroll height
            total_height = driver.execute_script("return document.body.scrollHeight")

            # Set the initial scroll position
            scroll_position = 0

            # Create a combined screenshot of the entire page
            fullpage_screenshot = None
            # fullpage_screenshot = ''

            # Scroll and capture screenshots until reaching the bottom of the page
            while scroll_position < total_height:
                # Scroll the page to the current position
                driver.execute_script(f"window.scrollTo(0, {scroll_position});")

                # Capture the current viewport screenshot
                screenshot = driver.get_screenshot_as_base64()

                # Combine the current viewport screenshot with the previous screenshots
                if fullpage_screenshot is None:
                    fullpage_screenshot = screenshot
                else:
                    fullpage_screenshot += screenshot

                # Scroll to the next position
                scroll_position += height

            # Generate a timestamp string
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # Construct the screenshot filename with timestamp and dimensions
            screenshot_name = f'screenshot_{index}_{width}x{height}_{timestamp}.png'
            # Specify the path to save the screenshot
            screenshot_path = os.path.join(website_directory, screenshot_name)
            # Save the full-page screenshot
            with open(screenshot_path, 'wb') as file:
                file.write(base64.b64decode(fullpage_screenshot))

    # Close the log file
    log_file.close()

    # Quit the browser
    driver.quit()

    print("\nSelesai... \n")



def load_websites_from_json(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data['websites']

def clear_screenshots_folder():
    # Remove all files and directories in the screenshots folder
    for root, dirs, files in os.walk(base_directory, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    print("Screenshots folder cleared.")


def clear_log_file():
    # Clear the content of the log file
    open('website_status.log', 'w').close()
    print("Log file cleared.")


if __name__ == '__main__':
    click.echo(BANNER)
    capture_screenshots()
