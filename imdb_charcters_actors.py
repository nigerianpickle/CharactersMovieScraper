import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Function to extract movie data
def scrape_movie_data(imdb_url):
    # Extract movie ID from the URL using regex (e.g., tt0468569 from the URL)
    match = re.search(r'tt\d+', imdb_url)
    if not match:
        print("Invalid IMDb URL")
        return
    
    imdb_id = match.group(0)
    full_credits_url = f'https://www.imdb.com/title/{imdb_id}/fullcredits'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    # Request the movie credits page
    response = requests.get(full_credits_url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    # Scrape the cast and characters
    cast_list = soup.find_all('table', class_='cast_list')

    actors = []
    characters = []

    # Iterate over cast members
    for row in cast_list[0].find_all('tr'):
        try:
            # Actor Name
            actor = row.find('td', class_='primary_photo').find_next_sibling('td').get_text(strip=True)
            actors.append(actor)

            # Character Name
            character = row.find('td', class_='character').get_text(strip=True)
            characters.append(character)
        except AttributeError:
            pass

    # Store the data in a DataFrame
    df = pd.DataFrame({
        'Actor': actors,
        'Character': characters
    })

    # Output or save the data
    print(df)
    df.to_csv(f'{imdb_id}_cast.csv', index=False)

# User enters the IMDb URL
user_url = input("Enter IMDb movie URL: ")
scrape_movie_data(user_url)
