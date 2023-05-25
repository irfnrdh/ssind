import click
import os
import json
import base64
import pdfkit
import requests
import math
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from PIL import Image, ImageDraw
import lighthouse


# yay -S wkhtmltopdf python-pip

BANNER = """

███████╗███████╗██╗███╗   ██╗██████╗ 
██╔════╝██╔════╝██║████╗  ██║██╔══██╗
███████╗███████╗██║██╔██╗ ██║██║  ██║
╚════██║╚════██║██║██║╚██╗██║██║  ██║
███████║███████║██║██║ ╚████║██████╔╝
╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚═════╝ 

Ambil Unlimited ScreenShoot Sambil Ngopi 
v.0.1.1 - by irfnrdh                      
"""

base_directory = '../export/screenshots'
resized_directory = '../export/resized_screenshots'
report_directory = "../export/report"

@click.command()
@click.option('--clear', is_flag=True, help='Clear screenshots folder')
@click.option('--report', is_flag=True, help='Generate PDF Report')
@click.option('--config', default='websites.json', help='Specify the path to the JSON config list of website file')
def capture_screenshots(clear, config, report):

    if clear:
        click.confirm('Are you sure you want to clear the screenshots folder?', abort=True)
        clear_screenshots_folder()
        clear_log_file()
        return

    # Create base directory to store the screenshots
    os.makedirs(base_directory, exist_ok=True)
    os.makedirs(resized_directory, exist_ok=True)


    # Create a log file
    log_file = open('../export/website_status.log', 'w')

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    # Set up the path to your ChromeDriver executable
    chrome_driver_path = '/usr/bin/chromedriver'

    # Get the absolute path to the 'config' folder
    config_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config'))
    websites = load_websites_from_json(os.path.join(config_folder, config))

    if config == "websites.json":
        click.echo(f'Config menggunakan data : "{config}" \n')

    # Iterate through the websites
    for website in tqdm(websites, desc="Capturing Screenshots"):
        name = website['name']
        url = website['url']
        screenshot = website['screenshot']
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        website_directory = os.path.join(base_directory, name, timestamp)
        os.makedirs(website_directory, exist_ok=True)

        # Set up the ChromeDriver service
        service = Service(chrome_driver_path)

        # Create a new instance of the ChromeDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:

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
            Score = lighthouse.webcorevitals(url)
            log_entry = f"{timestamp} - {name} ({url}): {status_code}, Loading Time: {loading_time}, Score: {Score}"
            # print(log_entry)
            log_file.write(log_entry + '\n')

            

            driver.get(url)
            driver.implicitly_wait(10)  # Wait for the page to load completely

            # Capture screenshots for each screen size on devices data json            
            devices_data = load_devices_from_json(os.path.join('mockups', 'devices.json'))
            screenshot_paths = []

            for index, device in enumerate(devices_data):
                platform = device['platform']
                name = device['name']
                width = int(device['width'])
                height = int(device['height'])
                physical_width = float(device['physical_width'])
                physical_height = float(device['physical_height'])
                mockup_path = device['mockup_path']

                
                # driver.set_window_size(width, height)

                # Calculate the pixel density for the device
                pixel_density = calculate_pixel_density(width, height, physical_width, physical_height)

                # Calculate the effective resolution
                effective_width, effective_height = calculate_effective_resolution(width, height, pixel_density)

                # Set the browser window size with the effective resolution
                driver.set_window_size(width, height)

                # Display the effective resolution in the terminal
                # click.echo(f"Effective Resolution - Width: {effective_width}, Height: {effective_height}, Pixel Density {pixel_density}")

                # Capture the screenshot

                # without mockup
                screenshot_name = f'screenshot_{index}_{platform}_{name}_{width}x{height}_{timestamp}.png'
                screenshot_path = os.path.join(website_directory, screenshot_name)
                driver.save_screenshot(screenshot_path)

                # with mockup
                screenshot_mockup_name = f'screenshot_mockup_{index}_{platform}_{name}_{width}x{height}_{timestamp}.png'
                screenshot_mockup_path = os.path.join(website_directory, screenshot_mockup_name)
                mockup_folder = os.path.join('mockups', mockup_path)
                add_mockup_to_screenshot(screenshot_path, mockup_folder, screenshot_mockup_path)

                # Save the screenshot paths to a list
                screenshot_paths.append(screenshot_mockup_path)

                # Open the screenshot image
                screenshot = Image.open(screenshot_path)
                
                # Resize the captured screenshots
                for screenshot_path in screenshot_paths:
                
                    # Resize the image to the effective resolution
                    resized_screenshot = screenshot.resize((int(effective_width), int(effective_height)))

                    # Save the resized image
                    resized_screenshot.save(f"../export/resized_screenshots/{index}_{platform}_{name}_resized.png")

                

                # screenshot = screenshot_paths[-1] if screenshot_paths else ""  # Update the 'screenshot' field with the last screenshot path or empty string

            # Update the 'screenshot' field in the 'websites' list with the screenshot paths
            website['screenshot'] = screenshot_paths[-1] if screenshot_paths else ""
            
            
            click.echo(f"  🗸 Screenshots captured for website: {url}")

        except Exception as e:
            click.echo(f"Error capturing screenshots for website: {url} ({e})")
        finally:
            driver.quit()
        
    # Update the 'website.json' file
    with open(os.path.join(config_folder, config), 'w') as file:
        json.dump(websites, file, indent=2)

    print("\nSelesai... \n")

    if report:
        generate_pdf_report(base_directory)

def load_websites_from_json(file_path):       
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data

def load_devices_from_json(json_path):
    with open(json_path) as json_file:
        data = json.load(json_file)
        devices_data = data['devices']

        devices = []
        for platform, platform_devices in devices_data.items():
            for device in platform_devices:
                name = device['name']
                width = int(device['width'])
                height = int(device['height'])
                physical_width = float(device['physical_width']) if device['physical_width'] is not None else 0.0
                physical_height = float(device['physical_height']) if device['physical_height'] is not None else 0.0
                mockup_path = device['mockup_path']

                devices.append({
                    'platform': platform,
                    'name': name,
                    'width': width,
                    'height': height,
                    'physical_width': physical_width,
                    'physical_height': physical_height,
                    'mockup_path': mockup_path
                })

        return devices

def clear_screenshots_folder():
    # Remove all files and directories in the screenshots folder
    for root, dirs, files in os.walk(base_directory, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))

    # Remove all files and directories in the resize folder
    for root, dirs, files in os.walk(resized_directory, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    print("Resized folder cleared.")

    # Remove all files and directories in the report folder
    for root, dirs, files in os.walk(report_directory, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    print("Report folder cleared.")

def clear_log_file():
    # Clear the content of the log file
    # open('../export/website_status.log', 'w').close()
    print("Log file deative to clear.")

def generate_pdf_report(base_directory):

    pdfkit_options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
    }

    click.echo('Generating PDF report...')
    screenshot_files = []
    for root, _, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".png"):
                screenshot_files.append(os.path.join(root, file))
    screenshot_files.sort()

    html_content = """
        <html>
        <head>
            <style>
                .report-image {
                    max-width: 100%;
                    margin-bottom: 20px;
                }
                body {
                    font-family: Arial, sans-serif;
                    font-size: 12px;
                    color: #333;
                    padding: 20px;
                }
            </style>
        </head>
        <body>
    """

    for screenshot_file in screenshot_files:
        with open(screenshot_file, "rb") as file:
            screenshot_data = base64.b64encode(file.read()).decode("utf-8")
        html_content += f'<img class="report-image" src="data:image/png;base64,{screenshot_data}" /><br><br>'
    html_content += """
        </body>
        </html>
    """

    os.makedirs(report_directory, exist_ok=True)
    html_file = os.path.join(report_directory, f'report_{datetime.now().strftime("%Y%m%d%H%M%S")}.html')
    with open(html_file, "w") as file:
        file.write(html_content)

    pdf_file = os.path.join(report_directory, f'report_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf')
    pdfkit.from_file(html_file, pdf_file, options=pdfkit_options)


    # os.remove(html_file)

    click.echo(f"PDF report generated: {pdf_file}")

def add_mockup_to_screenshot(screenshot_path, mockup_path, output_path):
    # Load the screenshot image
    screenshot = Image.open(screenshot_path)

    # Load the mockup image
    mockup = Image.open(mockup_path)

    # Resize the mockup image to match the size of the screenshot
    mockup = mockup.resize(screenshot.size)

    
    # Create a mask with rounded corners
    mask = Image.new('L', screenshot.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), screenshot.size], radius=20, fill=255)

    # Apply the mask to the mockup image
    mockup_with_rounded_corners = Image.new('RGBA', screenshot.size)
    mockup_with_rounded_corners.paste(mockup, mask=mask)

    # Overlay the mockup image on top of the screenshot
    merged_image = Image.alpha_composite(screenshot.convert('RGBA'), mockup_with_rounded_corners.convert('RGBA'))

    # Save the final image
    merged_image.save(output_path)

def calculate_effective_resolution(width, height, pixel_density):
    
    # Calculate the effective width and height based on the pixel density
    effective_width = int(width) / pixel_density
    effective_height = int(height) / pixel_density

    return effective_width, effective_height

def calculate_pixel_density(screen_width, screen_height, physical_width, physical_height):
    if physical_width != 0 and physical_height != 0:
        # Calculate the pixel density based on the screen and physical dimensions
        pixel_density = screen_width / physical_width
    else:
        # Handle the case where physical_width or physical_height is zero
        pixel_density = 1.0

    return pixel_density

def main():
    click.echo(BANNER)
    capture_screenshots()
    
if __name__ == '__main__':
    main()
    

