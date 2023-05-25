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
from PIL import Image, ImageDraw, ImageFilter

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

base_directory = '../screenshots'

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

    # Create a log file
    log_file = open('website_status.log', 'w')

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
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        website_directory = os.path.join(base_directory, name, timestamp)
        os.makedirs(website_directory, exist_ok=True)
        resized_directory = os.path.join(website_directory, 'resized_screenshots')
        os.makedirs(resized_directory, exist_ok=True)

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
                status_code = 'N/A'

            end_time = datetime.now()
            loading_time = end_time - start_time

            # Capture the screenshot
            screenshot_path = os.path.join(website_directory, 'screenshot.png')
            driver.get(url)
            driver.save_screenshot(screenshot_path)

            # Resize the screenshot
            resized_screenshot_path = os.path.join(resized_directory, 'resized_screenshot.png')
            resize_screenshot(screenshot_path, resized_screenshot_path)

            # Add mockup to the screenshot
            mockup_screenshot_path = os.path.join(website_directory, 'mockup_screenshot.png')
            add_mockup(resized_screenshot_path, mockup_screenshot_path)

            # Log the website status and loading time
            log_file.write(f'{name}\n')
            log_file.write(f'URL: {url}\n')
            log_file.write(f'Status Code: {status_code}\n')
            log_file.write(f'Loading Time: {loading_time}\n')
            log_file.write('\n')

        except Exception as e:
            # Log the exception if an error occurs
            log_file.write(f'{name}\n')
            log_file.write(f'URL: {url}\n')
            log_file.write(f'Error: {str(e)}\n')
            log_file.write('\n')

        finally:
            # Quit the driver to close the browser session
            driver.quit()

    # Close the log file
    log_file.close()

    if report:
        generate_pdf_report()

def load_websites_from_json(json_file):
    with open(json_file) as file:
        data = json.load(file)
        return data

def clear_screenshots_folder():
    click.echo('Clearing screenshots folder...')
    for folder in os.listdir(base_directory):
        folder_path = os.path.join(base_directory, folder)
        if os.path.isdir(folder_path):
            for subfolder in os.listdir(folder_path):
                subfolder_path = os.path.join(folder_path, subfolder)
                if os.path.isdir(subfolder_path) and subfolder == 'resized_screenshots':
                    click.echo(f'Removing {subfolder_path}...')
                    remove_directory(subfolder_path)

def clear_log_file():
    click.echo('Clearing log file...')
    log_file_path = 'website_status.log'
    if os.path.exists(log_file_path):
        os.remove(log_file_path)

def remove_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            remove_directory(file_path)
    os.rmdir(directory)

def resize_screenshot(original_path, resized_path):
    original_image = Image.open(original_path)
    original_width, original_height = original_image.size
    max_dimension = 800
    scale = min(max_dimension / original_width, max_dimension / original_height)
    new_width = math.floor(original_width * scale)
    new_height = math.floor(original_height * scale)
    new_size = (new_width, new_height)
    resized_image = original_image.resize(new_size, Image.LANCZOS)
    resized_image.save(resized_path)

def add_mockup(original_path, mockup_path):
    mockup_folder = os.path.join('mockups', mockup_path)
    original_image = Image.open(original_path)
    mockup_image = Image.open()
    mockup_image = mockup_image.resize(original_image.size)
    mockup_image.paste(original_image, (0, 0), original_image)
    mockup_image.save(mockup_path)

def generate_pdf_report():
    click.echo('Generating PDF report...')
    pdf_name = f'report_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf'
    pdf_path = os.path.join(base_directory, pdf_name)

    html = f'''
    <html>
    <head>
        <title>Website Screenshot Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            h1 {{
                margin-bottom: 30px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>Website Screenshot Report</h1>
        <table>
            <tr>
                <th>Website Name</th>
                <th>URL</th>
                <th>Status Code</th>
                <th>Loading Time</th>
            </tr>
    '''

    log_file_path = 'website_status.log'
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            lines = log_file.readlines()
            for i in range(0, len(lines), 5):
                name = lines[i].strip()
                url = lines[i+1].strip().split(': ')[1]
                status_code = lines[i+2].strip().split(': ')[1]
                loading_time = lines[i+3].strip().split(': ')[1]
                html += f'''
                <tr>
                    <td>{name}</td>
                    <td><a href="{url}">{url}</a></td>
                    <td>{status_code}</td>
                    <td>{loading_time}</td>
                </tr>
                '''

    html += '''
        </table>
    </body>
    </html>
    '''

    pdfkit.from_string(html, pdf_path)
    click.echo(f'PDF report generated: {pdf_path}')

if __name__ == '__main__':
    click.clear()
    click.echo(BANNER)
    capture_screenshots()
