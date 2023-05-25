import requests
from datetime import date

# Set device (mobile or desktop), category, and today's date
device = 'mobile'
category = 'performance'
today = date.today().strftime("%Y-%m-%d")

def webcorevitals(url):
    result = {}

    # Making API call for URL
    response = requests.get("https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + url + "&strategy=" + device + "&category=" + category)

    # Saving response as JSON
    data = response.json()

    print('Running URL #', url)

    result['URL'] = url
    result['Date'] = today

    # Getting Metrics
    try:
        data = data['lighthouseResult']
    except KeyError:
        print('No Values')
        data = 'No Values.'

    # First Contentful Paint
    try:
        result['FCP'] = data['audits']['first-contentful-paint']['displayValue']
    except KeyError:
        print('No Values')
        result['FCP'] = 0

    # Largest Contentful Paint
    try:
        result['LCP'] = data['audits']['largest-contentful-paint']['displayValue']
    except KeyError:
        print('No Values')
        result['LCP'] = 0

    # Cumulative Layout Shift
    try:
        result['CLS'] = data['audits']['cumulative-layout-shift']['displayValue']
    except KeyError:
        print('No Values')
        result['CLS'] = 0

    try:
        # Speed Index
        result['SI'] = data['audits']['speed-index']['displayValue']
    except KeyError:
        print('No Values')
        result['SI'] = 0

    try:
        # Time to Interactive
        result['TTI'] = data['audits']['interactive']['displayValue']
    except KeyError:
        print('No Values')
        result['TTI'] = 0

    try:
        # Total Blocking Time
        result['TBT'] = data['audits']['total-blocking-time']['displayValue']
    except KeyError:
        print('No Values')
        result['TBT'] = 0

    try:
        # Score
        result['Score'] = data['categories']['performance']['score']
    except KeyError:
        print('No Values')

    return result
