
from random import choice
import movie_storage
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")


def fetch_movie_details(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching movie details: {response.status_code} {response.reason}")
        return None


def delete_movie():
    """Prompt the user for a movie title to delete from the database."""
    movie_data = movie_storage.read_file(movie_storage.FILE_PATH)
    delete_movie_input = input("Which movie should be deleted? ").strip()

    if not delete_movie_input:
        print("You've entered nothing. Please try again.")
        return

    for movie in movie_data["movies"]:
        if delete_movie_input.lower() == movie["title"].lower():
            movie_storage.delete_movie(movie)
            print(f"Movie '{movie["title"]}' successfully deleted.")
            input("\nPress Enter to return to the menu.")
            return

    print(f"Movie '{delete_movie_input}' not found in the database.")
    input("\nPress Enter to return to the menu.")


def list_movies():
    """Display all movies in the database with their ratings and years."""
    movie_data = movie_storage.read_file(movie_storage.FILE_PATH)
    movies = movie_data["movies"]  # Access the list of movies directly
    print(f"{len(movies)} movies found:\n")

    for movie in movies:
        title = movie["title"]
        rating = movie["rating"]
        year = movie["year"]
        print(f"{title}: {rating} ({year})")

    input("\nPress Enter to return to the menu.")


def mov_sort_by_rate():
    """Sorting and displaying movies by rating."""
    # Read the movie data from the file
    movies_data = movie_storage.read_file(movie_storage.FILE_PATH)

    # Extract the list of movies
    movies = movies_data.get("movies", [])

    if not movies:
        print("No movies found in the database.")
        input("\nPress Enter to return to the menu.")
        return

    # Sort the movies by rating in descending order
    try:
        sorted_movies = sorted(movies, key=lambda movie: float(movie["rating"]), reverse=True)
    except KeyError:
        print("Error: Missing 'rating' in some movie entries.")
        input("\nPress Enter to return to the menu.")
        return
    except ValueError:
        print("Error: Some movies have invalid rating values.")
        input("\nPress Enter to return to the menu.")
        return

    # Display the sorted movies
    print("\nMovies sorted by rating (high to low):")
    for movie in sorted_movies:
        print(f"{movie['rating']}: {movie['title']} ({movie['year']})")

    input("\nPress Enter to return to the menu.")


def add_movie():
    """
    Prompts the user to add a new movie to the database using the OMDb API.
    """
    title = input("Add movie name: ").strip()
    if not title:
        print("You've entered nothing. Try again.")
        return

    movies = movie_storage.read_file(movie_storage.FILE_PATH)

    if title in movies:
        print(f"The movie '{title}' already exists in the database.")
        return

    movie_details = fetch_movie_details(title)
    if movie_details:
        movie_storage.add_movie(
            movie_details['Title'],
            movie_details['Year'],
            movie_details['imdbRating'],
            movie_details['Poster'],
            movie_details['Actors']
        )
        print(f"Added movie: {title}")
    else:
        print(f"Could not fetch details for movie: {title}")


def update_movie():
    """Prompt the user for a movie title and update its rating in the database."""
    movie_data = movie_storage.read_file(movie_storage.FILE_PATH)
    update_movie_input = input("Which movie would you like to update the rating for? ").strip()

    if not update_movie_input:
        print("You've entered nothing. Please try again.")
        return

    # Find the movie to update
    for movie in movie_data["movies"]:
        if update_movie_input.lower() == movie["title"].lower():
            print(f"Updating rating for movie: {movie['title']}")

            # Prompt user for the new rating
            new_rating = input(f"Enter new rating (current: {movie['rating']}): ").strip()

            # Update rating only if a new value is provided
            if new_rating:
                movie["rating"] = new_rating
                movie_storage.write_file(movie_storage.FILE_PATH, movie_data)
                print(f"Rating for movie '{movie['title']}' successfully updated to {new_rating}.")
            else:
                print("No rating entered. Update canceled.")

            input("\nPress Enter to return to the menu.")
            return

    print(f"Movie '{update_movie_input}' not found in the database.")
    input("\nPress Enter to return to the menu.")


def generate_website():
    """Generate an HTML website from movie data."""
    try:
        # Read movie data
        movies = movie_storage.read_file(movie_storage.FILE_PATH)

        if "movies" not in movies:
            print("No movie data found.")
            return

        with open("index_template.html") as file:
            index_template = file.read()

        title = "MOVIE APP"
        movie_grid = ""

        # Create movie grid HTML
        for movie in movies["movies"]:
            movie_grid += (
                f'<li>\n'
                f'    <div class="movie">\n'
                f'        <a href="https://www.imdb.com/title/{movie["imdbID"]}/" target="_blank">\n'
                f'            <img class="movie-poster" src="{movie["poster_url"]}" alt="{movie["title"]}">\n'
                f'        </a>\n'
                f'        <div class="movie-title">{movie["title"]}</div>\n'
                f'        <div class="movie-year">{movie["year"]}</div>\n'
                f'        <div class="rating-bar">\n'
                f'            <div class="movie-rating" style="width: {movie["rating"] * 10}%;">\n'
                f'                <span>{movie["rating"]}/10</span>\n'
                f'            </div>\n'
                f'        </div>\n'
                f'    </div>\n'
                f'</li>\n'
            )

        # Replace placeholders in the template
        output_html = index_template.replace("__TEMPLATE_TITLE__", title).replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

        # Write the output to index.html
        with open("index.html", "w") as file:
            file.write(output_html)

        print("Website generated successfully.")

    except Exception as e:
        print(f"An error occurred while generating the website: {e}")


def search_movie():
    """Search for a movie in the database."""
    movies_data = movie_storage.read_file(movie_storage.FILE_PATH)

    # Get the user input
    movie_name_input = input("Search for a movie (at least 5 characters): ").strip()

    if len(movie_name_input) < 5:
        print("Please enter at least 5 characters to search.")
        input("Press Enter to return.")
        return

    for movie in movies_data["movies"]:
        if movie_name_input.lower() in movie["title"].lower():
            # Movie found
            print(f"Movie found: '{movie['title']}'\nYear: {movie['year']}\nRating: {movie['rating']}")
            input("Press Enter to return.")
            return

    # If the movie is not found
    print(f"'{movie_name_input}' not found in the database.")
    input("Press Enter to return.")


# Define the status function (placeholder)
def status():
    """Display the status of the database."""
    movie_data = movie_storage.read_file(movie_storage.FILE_PATH)  # Read the file and get the dictionary
    movie_list = movie_data.get("movies", [])  # Get the list of movies or an empty list if it doesn't exist

    # Display the number of movies
    print(f"{len(movie_list)} movies in the database.")
    input("Press Enter to return to the menu.")


# Define a random movie function (placeholder)
def random_movie():
    """Display a random movie from the database."""
    movie_data = movie_storage.read_file(movie_storage.FILE_PATH)

    if "movies" in movie_data and movie_data["movies"]:
        movie = choice(movie_data["movies"])  # Choose a random movie from the list
        print(f"Random movie: '{movie['title']}' ({movie.get('year', 'Unknown Year')})")
    else:
        print("No movies in the database.")

    input("Press Enter to return.")
def menu():
    """Display the menu and prompt the user for a command."""
    print("*" * 10, " My Movies Database ", "*" * 10, "\n")

    menu_list = [
        {"description": "Exit", "execute": lambda: print("Bye!")},
        {"description": "List movies", "execute": list_movies},
        {"description": "Add movie", "execute": add_movie},
        {"description": "Delete movie", "execute": delete_movie},
        {"description": "Update movie", "execute": update_movie},  # Ensure you define this function
        {"description": "Status", "execute": status},
        {"description": "Random movie", "execute": random_movie},
        {"description": "Search movie", "execute": search_movie},
        {"description": "Movies sorted by rating", "execute": mov_sort_by_rate},
        {"description": "Generate website", "execute": generate_website},
    ]

    print("Menu:")
    for num, option in enumerate(menu_list):
        print(f"{num}. {option['description']}")

    while True:
        try:
            command_input = int(input(f"\nEnter choice (0-{len(menu_list) - 1}): "))
            if 0 <= command_input < len(menu_list):
                return command_input, menu_list
            print(f"Please choose a number between 0 and {len(menu_list) - 1}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    """Create a while loop so that the program execute the
    function according to users choice"""
    while True:
        print()
        command_input, menu_list = menu()
        menu_list[command_input]["execute"]()
        if command_input == 0:
            break


if __name__ == "__main__":
    main()
