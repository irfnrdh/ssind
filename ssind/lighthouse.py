import requests
import pandas as pd
from datetime import date

def webcorevitals(url_list, device, category, today):
    df_list = []
    for url in url_list['URL']:
        print(url)

        # Making API call for URL
        response = requests.get("https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + url + "&strategy=" + device + "&category=" + category)

        # Saving response as JSON
        data = response.json()

        print('Running URL #', url)

        test = url
        date = today

        # Getting Metrics
        try:
            data = data['lighthouseResult']
        except KeyError:
            print('No Values')
            data = 'No Values.'

        # First Contentful Paint
        try:
            fcp = data['audits']['first-contentful-paint']['displayValue']
        except KeyError:
            print('No Values')
            fcp = 0

        # Largest Contentful Paint
        try:
            lcp = data['audits']['largest-contentful-paint']['displayValue']
        except KeyError:
            print('No Values')
            lcp = 0

        # Cumulative Layout Shift
        try:
            cls = data['audits']['cumulative-layout-shift']['displayValue']
        except KeyError:
            print('No Values')
            cls = 0

        try:
            # Speed Index
            si = data['audits']['speed-index']['displayValue']
        except KeyError:
            print('No Values')
            si = 0

        try:
            # Time to Interactive
            tti = data['audits']['interactive']['displayValue']
        except KeyError:
            print('No Values')
            tti = 0

        try:
            # Total Blocking Time
            tbt = data['audits']['total-blocking-time']['displayValue']
        except KeyError:
            print('No Values')
            tbt = 0

        try:
            # Score
            score = data['categories']['performance']['score']
        except KeyError:
            print('No Values')

        # List with all values
        values = [test, score, fcp, si, lcp, tti, tbt, cls, date]

        # Create DataFrame using values list
        df_score = pd.DataFrame([values], columns=['URL', 'Score', 'FCP', 'SI', 'LCP', 'TTI', 'TBT', 'CLS', 'Date'])

        # Appending scores to empty df outside for loop
        df_list.append(df_score)

    # Concatenating list of dataframes into one
    df = pd.concat(df_list)

    # Removing 's' from LCP so we can get mean, also transforming it to float
    df['LCP'] = df['LCP'].astype(str).str.replace(r's', '').astype(float)
    df['FCP'] = df['FCP'].astype(str).str.replace(r's', '').astype(float)
    df['SI'] = df['SI'].astype(str).str.replace(r's', '').astype(float)
    df['TTI'] = df['TTI'].astype(str).str.replace(r's', '').astype(float)
    df['TBT'] = df['TBT'].astype(str).str.replace(r'ms', '').str.replace(r',', '').astype(float)
    df['Score'] = df['Score'].astype(float)
    df['CLS'] = df['CLS'].astype(float)

    # Save DataFrame as CSV
    filename = today + '_all_scores.csv'
    df.to_csv(filename)
    print('File was saved in', filename)


# Load URL list from Excel file
url_list = pd.read_excel('urls.xlsx')

# Set device (mobile or desktop), category, and today's date
device = 'mobile'
category = 'performance'
today = date.today().strftime("%Y-%m-%d")

# Call webcorevitals function
webcorevitals(url_list, device, category, today)
