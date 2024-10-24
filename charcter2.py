import csv
from imdb import Cinemagoer
from openpyxl import Workbook

# Initialization
wb = Workbook()
ws = wb.active


def getCharacters(movie_name):
    ia = Cinemagoer()  # Initialize the IMDb instance
    try:
        movies = ia.search_movie(movie_name)  # Search for the movie
    except Exception as e:
        print(f"Error searching for movie '{movie_name}': {e}")
        return

    if not movies:
        print(f"No movie found with the name '{movie_name}'")
        return

    # Get the first matching movie (you could choose based on year or other attributes)
    try:
        movie = ia.get_movie(movies[0].movieID)
    except Exception as e:
        print(f"Error retrieving movie details for '{movie_name}': {e}")
        return
    
    # Get the cast of the movie
    cast = movie.get('cast', [])
    
    if not cast:
        print(f"No cast found for the movie '{movie_name}'")
        return

    print(f"Characters in '{movie_name}':")
    for character in cast:
        try:
            actor_name = character.get('name', '??')
            if character.currentRole:
                # currentRole could be a list of characters (e.g., for actors playing multiple roles)
                if isinstance(character.currentRole, list):
                    for role in character.currentRole:
                        character_name = role.get('name', '??')
                        print(f"Actor: {actor_name}, Character: {character_name}")
                        ws.append([actor_name, character_name, movie_name])
                else:
                    character_name = character.currentRole.get('name', '??')
                    print(f"Actor: {actor_name}, Character: {character_name}")
                    ws.append([actor_name, character_name, movie_name])
            else:
                print(f"Actor: {actor_name}, Character: N/A")
                ws.append([actor_name, "N/A", movie_name])
        except Exception as e:
            print(f"Error processing character data for '{movie_name}': {e}")
            ws.append(['??', '??', movie_name])  # Adding placeholder for corrupt data


# Call the function
# mv = input("Enter a movie: ")

headers = ['Actor Name', 'Role', 'Movie name']
ws.append(headers)

# Go through CSV file,
# Search for the movie name
try:
    with open('movies_dataset copy.csv', mode='r', encoding='UTF-8') as file:
        # Create a DictReader object
        csv_reader = csv.DictReader(file)
        i = 0
        # Iterate over the rows as dictionaries
        for row in csv_reader:
            # Choose the amount of movies we want
            if i == 0:
                break
            i += 1
            print("Movie name: " + row.get('title', '??'))  # Using '??' if title is missing
            getCharacters(row.get('title', '??'))

except FileNotFoundError:
    print("The file 'movies_dataset copy.csv' was not found.")
except Exception as e:
    print(f"An error occurred while reading the CSV file: {e}")

# Store the actor in a CSV file
wb.save('MovieCharacters.csv')
