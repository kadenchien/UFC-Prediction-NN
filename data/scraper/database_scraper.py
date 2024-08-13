from bs4 import BeautifulSoup
import pandas as pd
import requests

def scrape_fight_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    athlete_profiles = soup.find_all('a', class_='e-button--black')

    all_data = []

    for profile in athlete_profiles:
        relative_url = profile['href']
        full_url = f"https://www.ufc.com{relative_url}"
        athlete_data = scrape_athlete_profile(full_url)
        all_data.append(athlete_data)

    columns = [
        'Name', 'Style', 'Age', 'Height', 'Reach', 
        'Sig. Str. Landed Per Min', 'Sig. Str. Absorbed Per Min', 'Takedown avg Per 15 Min', 'Submission avg Per 15 Min', 'Sig. Str. Defense (%)', 'Takedown Defense (%)', 'Knockdown Avg', 'Average fight time (secs)',
        'Sig. Str. By Position (Standing)', 'Sig. Str. By Position (Clinch)', 'Sig. Str. By Position (Ground)', 'Win by Method (KO/TKO)', 'Win by Method (Decision)', 'Win by Method (Sub)', 'Striking accuracy (%)', 'Takedown Accuracy (%)'
    ]

    df = pd.DataFrame(all_data, columns=columns)

    df.to_csv('mens_fighters_database.csv', index=False)



def scrape_athlete_profile(profile_url):
    response = requests.get(profile_url)
    profile_soup = BeautifulSoup(response.text, 'html.parser')

    name_tag = profile_soup.find('h1', class_='hero-profile__name')
    athlete_name = name_tag.text.strip() if name_tag else 'Unknown Athlete'

    metrics_array = [athlete_name]
    def extract_and_append(label, cast_type=str):
        section = profile_soup.find('div', class_='c-bio__label', string=label)
        if section:
            text_section = section.find_next_sibling('div', class_='c-bio__text')
            if text_section:
                text = text_section.text.strip()
                metrics_array.append(cast_type(text))
            else:
                metrics_array.append(None)
        else:
            metrics_array.append(None)

    # Extract and append each bio detail
    extract_and_append('Fighting style')
    extract_and_append('Age', int)
    extract_and_append('Height', float)
    extract_and_append('Reach', float)

    advanced_metrics = profile_soup.find_all('div', class_='c-stat-compare__number')

    for metric in advanced_metrics:
        metric_text = metric.text.strip()

        if '%' in metric_text:
            metric_text = metric_text.replace('%', '').strip()

        try:
            metric_value = float(metric_text)
        except ValueError:
            if ':' in metric_text:
                minutes, seconds = map(float, metric_text.split(':'))
                metric_value = minutes * 60 + seconds
            else:
                metric_value = 0.0

        metrics_array.append(metric_value)

    sig_strikes_by_pos = profile_soup.find_all('div', class_='c-stat-3bar__value')

    for strike in sig_strikes_by_pos:
        strike_text = strike.text.strip()
        strike_value = strike_text.split()[0]
        try:
            strike_value = float(strike_value)
        except ValueError:
            strike_value = 0.0

        metrics_array.append(strike_value)

    chart_percentages = profile_soup.find_all('text', class_='e-chart-circle__percent')

    for percentage in chart_percentages:
        percentage_text = percentage.text.strip().replace('%', '')
        try:
            percentage_value = int(percentage_text)
        except ValueError:
            percentage_value = 0

        metrics_array.append(percentage_value)
   

    return metrics_array

scrape_fight_page('https://www.ufc.com/athletes/all?filters%5B0%5D=status%3A23&filters%5B1%5D=weight_class%3A8&filters%5B2%5D=weight_class%3A9&filters%5B3%5D=weight_class%3A10&filters%5B4%5D=weight_class%3A11&filters%5B5%5D=weight_class%3A12&filters%5B6%5D=weight_class%3A13&filters%5B7%5D=weight_class%3A14&filters%5B8%5D=weight_class%3A15')

