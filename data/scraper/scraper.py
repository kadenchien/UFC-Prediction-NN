import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to scrape a single fight page
def scrape_fight_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting fight data
    fight_data = {}
    fight_data['event'] = soup.find('h2', class_='b-content__title').text.strip()
    
    fighters = soup.find_all('a', class_='b-link b-fight-details__person-link')
    fight_data['fighter_1'] = fighters[0].text.strip()
    fight_data['fighter_2'] = fighters[1].text.strip()
    
    result = soup.find_all('i', class_='b-fight-details__person-status')
    fight_data['fighter_1_result'] = result[0].text.strip()
    fight_data['fighter_2_result'] = result[1].text.strip()
    
    # Extracting statistics
    stats_tables = soup.find_all('tbody')
    if len(stats_tables) >= 2:
        # Totals table
        totals = stats_tables[0].find_all('td')
        knockdowns = totals[1].text.strip().split()

        fight_data['fighter_1_knockdowns'] = knockdowns[0]
        fight_data['fighter_2_knockdowns'] = knockdowns[1]
        sig_str = totals[2].text.strip().split()

        fight_data['fighter_1_ss'] = sig_str[0]+" of "+sig_str[2]
        fight_data['fighter_2_ss'] = sig_str[3]+" of "+sig_str[5]
        sig_str_pct = totals[3].text.strip().split()

        fight_data['fighter_1_ss_pct'] = sig_str_pct[0]
        fight_data['fighter_2_ss_pct'] = sig_str_pct[1]
        total_strikes = totals[4].text.strip().split()

        fight_data['fighter_1_total_strikes'] = total_strikes[0] + " of " + total_strikes[2]
        fight_data['fighter_2_total_strikes'] = total_strikes[3] + " of " + total_strikes[5]
        takedown_pct = totals[6].text.strip().split()
        takedowns = totals[5].text.strip().split()

        fight_data['fighter_1_takedowns'] = takedowns[0] + " of " + takedowns[2]
        fight_data['fighter_2_takedowns'] = takedowns[3] + " of " + takedowns[5]
        takedown_pct = totals[6].text.strip().split()
        
        fight_data['fighter_1_takedown_pct'] = takedown_pct[0]
        fight_data['fighter_2_takedown_pct'] = takedown_pct[1]

        submission_attempts = totals[7].text.strip().split()
        fight_data['fighter_1_submission_attempts'] = submission_attempts[0]
        fight_data['fighter_2_submission_attempts'] = submission_attempts[1]

        reverses = totals[8].text.strip().split()
        fight_data['fighter_1_reverses'] = reverses[0]
        fight_data['fighter_2_reverses'] = reverses[1]

        control = totals[9].text.strip().split()
        fight_data['fighter_1_control'] = control[0]
        fight_data['fighter_2_control'] = control[1]

        # Significant Strikes table
        significant_strikes = stats_tables[int(len(stats_tables)/2)].find_all('td')
        head_ss = significant_strikes[3].text.strip().split()
        fight_data['fighter_1_head_ss'] = head_ss[0] + " of " + head_ss[2]
        fight_data['fighter_2_head_ss'] = head_ss[3] + " of " + head_ss[5]

        body_ss = significant_strikes[4].text.strip().split()
        fight_data['fighter_1_body_ss'] = body_ss[0] + " of " + body_ss[2]
        fight_data['fighter_2_body_ss'] = body_ss[3] + " of " + body_ss[5]

        leg_ss = significant_strikes[5].text.strip().split()
        fight_data['fighter_1_leg_ss'] = leg_ss[0] + " of " + leg_ss[2]
        fight_data['fighter_2_leg_ss'] = leg_ss[3] + " of " + leg_ss[5]

        distance_ss = significant_strikes[6].text.strip().split()
        fight_data['fighter_1_distance_ss'] = distance_ss[0] + " of " + distance_ss[2]
        fight_data['fighter_2_distance_ss'] = distance_ss[3] + " of " + distance_ss[5]

        clinch_ss = significant_strikes[7].text.strip().split()
        fight_data['fighter_1_clinch_ss'] = clinch_ss[0] + " of " + clinch_ss[2]
        fight_data['fighter_2_clinch_ss'] = clinch_ss[3] + " of " + clinch_ss[5]

        ground_ss = significant_strikes[8].text.strip().split()
        fight_data['fighter_1_ground_ss'] = ground_ss[0] + " of " + ground_ss[2]
        fight_data['fighter_2_ground_ss'] = ground_ss[3] + " of " + ground_ss[5]

    return fight_data

# Function to scrape individual fight URLs from a fight night page
def scrape_individual_fights(event_url):
    response = requests.get(event_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    fights = soup.find_all('tr', class_='b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click')
    
    fight_links = []
    for fight in fights:
        onclick_attr = fight.get('onclick')
        if onclick_attr:
            link = onclick_attr.split("'")[1]  # Extract the URL from the onclick attribute
            fight_links.append(link)
    return fight_links

# Main function to scrape multiple UFC event pages
def scrape_ufc_events(url, num_events):
    all_fight_data = []
    
    for page in range(num_events):
        newURL = f'{url}?page={page+1}'
        response = requests.get(newURL)
        soup = BeautifulSoup(response.text, 'html.parser')
        fightnights = soup.find_all('a', class_='b-link b-link_style_black')

        # Loop over the specified number of events
        for i in range(len(fightnights)):
            if "Fight Night" not in fightnights[i].text.strip():
                event_url = fightnights[i]['href']
                fight_links = scrape_individual_fights(event_url)
                
                for link in fight_links:
                    fight_data = scrape_fight_page(link)
                    all_fight_data.append(fight_data)
                    time.sleep(1)  # To avoid overwhelming the server
    
    return all_fight_data

# Base URL
url = 'http://ufcstats.com/statistics/events/completed'

# Scraping data from UFCStats
ufc_data = scrape_ufc_events(url, num_events=10)  # Adjust num_events for more data

# Converting to DataFrame and saving to CSV
df = pd.DataFrame(ufc_data)
df.to_csv('data/raw/ufc_fight_data.csv', index=False)

print('Data scraping completed and saved to ufc_fight_data.csv')
