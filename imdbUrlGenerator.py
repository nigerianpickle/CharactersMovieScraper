import requests
from bs4 import BeautifulSoup
import urllib.parse

def generate_imdb_url(movie_name):
    # Step 1: URL encode the movie name
    encoded_movie_name = urllib.parse.quote(movie_name)
    
    # Step 2: Create the search URL
    search_url = f'https://www.imdb.com/find?q={encoded_movie_name}'
    
    # Step 3: Send a GET request to the search URL
    response = requests.get(search_url)
    
    # Step 4: Parse the search results page
    soup = BeautifulSoup(response.content, 'lxml')
    
    # Step 5: Find the first movie result
    try:
        # Select the first result from the search results
        first_result = soup.find('td', class_='result_text').find('a')
        movie_page_url = 'https://www.imdb.com' + first_result['href']
        return movie_page_url
    except AttributeError:
        return "Movie not found."

# Example usage
movie_name = input("Enter the movie name: ")
imdb_url = generate_imdb_url(movie_name)
print(f'IMDB URL: {imdb_url}')