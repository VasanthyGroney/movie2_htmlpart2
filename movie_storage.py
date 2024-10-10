import json
import os

FILE_PATH = 'data.json'
TEMPLATE_PATH = 'index_template.html'
OUTPUT_PATH = 'index.html'

def read_file(file):
    """Reads a JSON file and returns it as a Python object."""
    with open(file, "r") as json_data:
        movie_data = json.load(json_data)
    return movie_data

def write_file(file, python_obj):
    """Converts a Python object to a JSON string and writes a file."""
    with open(file, "w") as json_data:
        json.dump(python_obj, json_data)

def add_movie(title, year, rating, poster, actors):
    """Adds a movie to the movies database."""
    movie_data = read_file(FILE_PATH)
    movie_data["movies"].append({
        "title": title,
        "year": year,
        "rating": rating,
        "poster": poster,
        "actors": actors
    })
    write_file(FILE_PATH, movie_data)

def delete_movie(title):
    """Deletes a movie from the movies database."""
    movie_data = read_file(FILE_PATH)
    for movie in movie_data["movies"]:
        if movie["title"] == title:
            movie_data["movies"].pop(movie)
    write_file(FILE_PATH, movie_data)


def update_movie(title, new_rating):
    """Updates a movie rating in the movies database."""
    movie_data = read_file(FILE_PATH)

    for movie in movie_data["movies"]:
        if movie["title"] == title:
            movie["rating"] = new_rating
            write_file(FILE_PATH, movie_data)
            print(f"Movie '{title}' successfully updated to rating {new_rating}.")
            return  # Exit after updating

    print(f"Movie '{title}' not found in the database.")
