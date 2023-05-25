import click
import os
import json
import base64
import pdfkit
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from PIL import Image, ImageDraw

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

        # Set up the ChromeDriver service
        service = Service(chrome_driver_path)

        # Create a new instance of the ChromeDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.get(url)
            driver.implicitly_wait(10)  # Wait for the page to load completely

            # Capture screenshots for each screen size
            screen_sizes = [(320, 480, "apple-ipad-air-4-medium.png"), (768, 1024, "apple-ipad-air-4-medium.png"), (1440, 900, "apple-ipad-air-4-medium.png"), (1920, 1080, "apple-ipad-air-4-medium.png")]
            
            for index, (width, height, mock) in enumerate(screen_sizes):
                driver.set_window_size(width, height)

                # without mockup
                screenshot_name = f'screenshot_{index}_{width}x{height}_{timestamp}.png'
                screenshot_path = os.path.join(website_directory, screenshot_name)
                driver.save_screenshot(screenshot_path)

                # with mockup
                screenshot_mockup_name = f'screenshot_mockup_{index}_{width}x{height}_{timestamp}.png'
                screenshot_mockup_path = os.path.join(website_directory, screenshot_mockup_name)
                mockup_folder = os.path.join('mockups', mock)
                add_mockup_to_screenshot(screenshot_path, mockup_folder, screenshot_mockup_path)

            click.echo(f"  🗸 Screenshots captured for website: {url}")
        except Exception as e:
            click.echo(f"Error capturing screenshots for website: {url} ({e})")
        finally:
            driver.quit()

    print("\nSelesai... \n")

    if report:
        generate_pdf_report(base_directory)


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


def generate_pdf_report(base_directory):
    screenshot_files = []
    for root, _, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".png"):
                screenshot_files.append(os.path.join(root, file))
    screenshot_files.sort()

    html_content = "<html><body>"
    for screenshot_file in screenshot_files:
        with open(screenshot_file, "rb") as file:
            screenshot_data = base64.b64encode(file.read()).decode("utf-8")
        html_content += f'<img src="data:image/png;base64,{screenshot_data}" /><br><br>'
    html_content += "</body></html>"

    html_file = "report.html"
    with open(html_file, "w") as file:
        file.write(html_content)

    pdf_file = "report.pdf"
    pdfkit.from_file(html_file, pdf_file)

    os.remove(html_file)

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


def main():
    click.echo(BANNER)
    capture_screenshots()
    

if __name__ == '__main__':
    main()
    
