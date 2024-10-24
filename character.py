import csv
from imdb import Cinemagoer
from openpyxl import Workbook

#Initalization
wb = Workbook()
ws = wb.active


def getCharacters(movie_name):
    ia = Cinemagoer()  # Initialize the IMDb instance
    movies = ia.search_movie(movie_name)  # Search for the movie

    if not movies:
        print(f"No movie found with the name '{movie_name}'")
        return

    # Get the first matching movie (you could choose based on year or other attributes)
    movie = ia.get_movie(movies[0].movieID)
    
    # Get the cast of the movie
    cast = movie.get('cast')
    
    if not cast:
        print(f"No cast found for the movie '{movie_name}'")
        return

    print(f"Characters in '{movie_name}':")
    for character in cast:
        # Check if currentRole is available and handle if it's a list
        if character.currentRole:
            # currentRole could be a list of characters (e.g., for actors playing multiple roles)
            if isinstance(character.currentRole, list):
                for role in character.currentRole:
                    print(f"Actor: {character['name']}, Character: {role['name']}")
                    ws.append([character['name'],role['name'],movie_name])
            else:
                print(f"Actor: {character['name']}, Character: {character.currentRole['name']}")
                ws.append([character['name'],character.currentRole['name'],movie_name])
        else:
            #
            print(f"Actor: {character['name']}, Character: N/A")
            ws.append([character['name'],"N/A",movie_name])

# Call the function
#mv = input("Enter a movie: ")





headers=['Actor Name','Role','Movie name']
ws.append(headers)


#Go through CSV file,
#Search for the movie name
# Open the CSV file
with open('movies_dataset copy.csv', mode='r', encoding='UTF-8') as file:
    # Create a DictReader object
    csv_reader = csv.DictReader(file)
    i=0
    # Iterate over the rows as dictionaries

    #test to see if im able to get all the movies names in the file
    # for row in csv_reader:
    #     if (i==8036):
    #         break
    #     i+=1
    #     print(row['title'])  # Each 'row' is an OrderedDict with keys as the column headers

    #TEST PASSED

    #Now
    # for the movie name
    #Search up movie and get cast
    for row in csv_reader:
        #Choose the amount of movies we want
        if (i==8070):
            break
        i+=1
        print("Movie name:"+row['title'])  # Each 'row' is an OrderedDict with keys as the column headers
        getCharacters(row['title'])

    
# Store the actor in a csv file



wb.save('MovieCharacters.csv')
#getCharacters(mv)
