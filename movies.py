import requests
import pandas as pd
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog

# Add your OMDB API key 
api_key = 'cbdf5f1e'

def get_movie_data(api_key, movie_title):
    #Send a get request to the OMDB api
    response = requests.get(f'http://www.omdbapi.com/?t={movie_title}&apikey={api_key}')
    data = response.json()

    #Check if "imdbRating" exists
    if 'imdbRating' not in data: 
        return 'NA' #this will add NA when IMDB Score is not found
    
    #Extrat the rating from the response
    imdb_score = data['imdbRating']

    return imdb_score

# Create a Tkinter window and hide it 

root = tk.Tk()
root.withdraw()

# Open a file dialog and ask the user to select a csv file 
# that contains the movie list

csv_file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

#Ask the user to enter the name of the column that contains the movie titles
title_column_name = input("PLease enter the name of the field with movie titles:")

#Load the data from the selected CSV file
data = pd.read_csv(csv_file_path)

#Extract the movie titles
movies = data[title_column_name].tolist()

#Get the IMDb scores for each movie
imdb_scores = [get_movie_data(api_key,movie_title)
                for movie_title in tqdm(movies, desc="Fetching IMDb scores")
               ]
#Add the scores to the DataFrame
data['IMDB_Scores'] = imdb_scores

#Save the DataFrame to the same CSV file we have
data.to_csv(csv_file_path, index=False)

