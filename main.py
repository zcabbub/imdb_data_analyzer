import datetime
import json
import os

from imdb import IMDb
import pandas as pd


def get_ten_previous_movies(person, instance):
    person_id = person.getID()
    person_data = instance.get_person_filmography(person_id)

    try:
        filmography = person_data['data']['filmography']['actor']
    except:
        filmography = person_data['data']['filmography']['writer']

    ten_previous_movies = []
    for movie in filmography:
        if '()' not in movie['title']:
            ten_previous_movies.append(movie)
            if len(ten_previous_movies) == 10:
                break

    return ten_previous_movies


# weekend=True for weekend Box Office revenues
#        =False for worldwide
def get_10_prev_revenues_for(person, instance, weekend):
    ten_previous_movies = get_ten_previous_movies(person, instance)

    data_BOs = {}
    ratios = {}
    suma = 0
    counter = 0

    counter, suma = get_data_BOs(counter, data_BOs, instance, ratios, suma, ten_previous_movies, weekend)

    average = suma/counter

    if weekend:
        return average, ratios, data_BOs
    else:
        return average, data_BOs


def get_data_BOs(counter, data_BOs, instance, ratios, suma, ten_previous_movies, weekend):
    for movie in ten_previous_movies:
        movie_id = movie.getID()
        movie = instance.get_movie(movie_id)
        revenue = movie.get('box office')

        if revenue:
            ratio = get_ratio(revenue)
            ratios[str(movie)] = ratio
            if weekend:
                rev_bo = revenue.get('Opening Weekend United States')
            else:
                rev_bo = revenue.get('Cumulative Worldwide Gross')
        else:
            rev_bo = None
        if rev_bo:
            suma = suma + get_number(rev_bo)
            counter += 1

        data_BOs[str(movie)] = rev_bo
    return counter, suma


def create_movies_by_genre():
    print("Reading TSVs...")
    basics_tsv = pd.read_csv('input_data/data_basics.tsv', sep='\t')
    ratings_tsv = pd.read_csv('input_data/data_ratings.tsv', sep='\t')
    print("Done.")

    print("Merging and sorting the tables...")
    df = pd.merge(ratings_tsv, basics_tsv, on='tconst', how='left')
    sorted_df = df.sort_values(by=['numVotes'], ascending=False).reset_index().drop(axis=1, columns=['index'])
    print("Done.")

    print("Creating the dictionary...")
    movies_by_genre = {}
    for row in sorted_df['genres']:
        try:
            genres = row.split(',')
        except:
            continue
        for genre in genres:
            if genre not in movies_by_genre:
                movies_by_genre[genre] = {}

    # some movies do not have a genre
    movies_by_genre.pop('\\N', None)

    for movie_genre in movies_by_genre:
        genre_df = sorted_df[sorted_df['genres'].str.contains(movie_genre, na=False)]
        genre_dict = dict(zip(genre_df.tconst, genre_df.numVotes))
        movies_by_genre[movie_genre] = genre_dict
    print('Done.')

    print('Writing it in "movies_by_genre.json"...')
    with open('movies_by_genre.json', 'w') as file:
        json.dump(movies_by_genre, file)
    print('Done.')

    return movies_by_genre


def get_top_100_by_genre(genre):
    try:
        # to read if the file exists
        print("Trying to read 'movies_by_genre.json'...")
        with open('movies_by_genre.json', 'r') as file:
            movies_by_genre = json.load(file)
        print('Done.')
    except:
        print("File not found. Starting to create the file...")
        # create the file if not
        movies_by_genre = create_movies_by_genre()
        print("Done.")

    genre_top_100 = {key: movies_by_genre[genre][key] for key in list(movies_by_genre[genre].keys())[:1]}

    return genre_top_100


def get_number(string):
    return int(string.split(' ')[0].replace(',', '')[1:])


def get_ratio(revenue):
    opening = revenue.get('Opening Weekend United States')
    worldwide = revenue.get('Cumulative Worldwide Gross')
    if opening and worldwide:
        ratio = get_number(opening)/get_number(worldwide)
    else:
        ratio = None
    return ratio


def get_top_100_revenues_for(genre, instance, weekend):
    top_100 = get_top_100_by_genre(genre)

    ratios = {}
    suma = 0
    counter = 0

    data_BOs = {}

    for movie_id in top_100:
        movie = instance.get_movie(movie_id[2:])
        revenue = movie.get('box office')

        if revenue:
            ratio = get_ratio(revenue)
            ratios[str(movie)] = ratio

            if weekend:
                rev_bo = revenue.get('Opening Weekend United States')
            else:
                rev_bo = revenue.get('Cumulative Worldwide Gross')
        else:
            rev_bo = None

        if rev_bo:
            suma = suma + get_number(rev_bo)
            counter += 1

            data_BOs[str(movie)] = rev_bo

    average = suma/counter

    if weekend:
        return average, ratios, data_BOs
    else:
        return average, data_BOs


def get_data(instance, lead_actor_1, lead_actor_2, director, producer, top_genre, secondary_genre):
    movie_data = {'lead_actor_1': {}, 'lead_actor_2': {}, 'director': {}, 'producer': {}, 'top_genre': {},
                  'secondary_genre': {}}

    categorized_ratios = {}

    averages = {'lead_actor_1': {}, 'lead_actor_2': {}, 'director': {}, 'producer': {}, 'top_genre': {},
                  'secondary_genre': {}}

    # print('Getting data for LEAD ACTOR 1...')
    # print('---opening weekend revenues ...')
    # averages['lead_actor_1']['opening_weekend_revenues'], categorized_ratios['lead_actor_1'], movie_data['lead_actor_1']['opening_weekend_revenues'] = get_10_prev_revenues_for(lead_actor_1, instance, True)
    # print('---worldwide revenues ...')
    # averages['lead_actor_1']['worldwide_revenues'], movie_data['lead_actor_1']['worldwide_revenues'] = get_10_prev_revenues_for(lead_actor_1, instance, False)
    # print('Done.\n')
    #
    # print('Getting data for LEAD ACTOR 2...')
    # print('---opening weekend revenues ...')
    # averages['lead_actor_2']['opening_weekend_revenues'], categorized_ratios['lead_actor_2'], movie_data['lead_actor_2']['opening_weekend_revenues'] = get_10_prev_revenues_for(lead_actor_2, instance, True)
    # print('---worldwide revenues ...')
    # averages['lead_actor_2']['worldwide_revenues'], movie_data['lead_actor_2']['worldwide_revenues'] = get_10_prev_revenues_for(lead_actor_2, instance, False)
    # print('Done.\n')
    #
    # print('Getting data for DIRECTOR...')
    # print('---opening weekend revenues ...')
    # averages['director']['opening_weekend_revenues'], categorized_ratios['director'], movie_data['director']['opening_weekend_revenues'] = get_10_prev_revenues_for(director, instance, True)
    # print('---worldwide revenues ...')
    # averages['director']['worldwide_revenues'], movie_data['director']['worldwide_revenues'] = get_10_prev_revenues_for(director, instance, False)
    # print('Done.\n')
    #
    # print('Getting data for PRODUCER...')
    # print('---opening weekend revenues ...')
    # averages['producer']['opening_weekend_revenues'], categorized_ratios['producer'], movie_data['producer']['opening_weekend_revenues'] = get_10_prev_revenues_for(producer, instance, True)
    # print('---worldwide revenues ...')
    # averages['producer']['worldwide_revenues'], movie_data['producer']['worldwide_revenues'] = get_10_prev_revenues_for(producer, instance, False)
    # print('Done.\n')
    #
    # print('Getting data for TOP GENRE...')
    # print('---opening weekend revenues ...')
    # averages['top_genre']['opening_weekend_revenues'], categorized_ratios['top_genre'], movie_data['top_genre']['opening_weekend_revenues'] = get_top_100_revenues_for(top_genre, instance, True)
    # print('---worldwide revenues ...')
    # averages['top_genre']['worldwide_revenues'], movie_data['top_genre']['worldwide_revenues'] = get_top_100_revenues_for(top_genre, instance, False)
    # print('Done.\n')
    #
    # print('Getting data for SECONDARY GENRE...')
    # print('---opening weekend revenues ...')
    # averages['secondary_genre']['opening_weekend_revenues'], categorized_ratios['secondary_genre'], movie_data['secondary_genre']['opening_weekend_revenues'] = get_top_100_revenues_for(secondary_genre, instance, True)
    # print('---worldwide revenues ...')
    # averages['secondary_genre']['worldwide_revenues'], movie_data['secondary_genre']['worldwide_revenues'] = get_top_100_revenues_for(secondary_genre, instance, False)
    # print('Done.\n')

    return averages, categorized_ratios, movie_data


def create_CSVs(data):
    columns = list(data.keys())
    weekend_dict = {}
    worldwide_dict = {}

    for column in columns:
        weekend_dict[column] = []
        worldwide_dict[column] = []

    for column in columns:
        weekend_data = data[column].get('opening_weekend_revenues')
        worldwide_data = data[column].get('worldwide_revenues')
        if weekend_data:
            for key in weekend_data:
                pair = key + ':' + str(weekend_data.get(key))
                weekend_dict[column].append(pair)
        if worldwide_data:
            for key in worldwide_data:
                pair = key + ':' + str(worldwide_data.get(key))
                worldwide_dict[column].append(pair)

    for column in columns:
        week_col = weekend_dict[column]
        world_col = worldwide_dict[column]
        if len(week_col) < 100:
            while len(week_col) < 100:
                week_col.append('')
        if len(world_col) < 100:
            while len(world_col) < 100:
                world_col.append('')

    weekend_df = pd.DataFrame(weekend_dict)
    worldwide_df = pd.DataFrame(worldwide_dict)

    return weekend_df, worldwide_df


def get_movie_info(id):
    ia = IMDb()
    movie = ia.get_movie(id)

    lead_actor_1 = movie['cast'][0]
    lead_actor_2 = movie['cast'][1]
    director = movie['director'][0]
    producer = movie['producers'][0]
    top_genre = movie['genres'][0]
    secondary_genre = movie['genres'][1]
    # studio = movie['production companies'][0]

    averages, ratios, movie_data = get_data(ia, lead_actor_1, lead_actor_2, director, producer, top_genre, secondary_genre)

    date = datetime.datetime.now().date()
    filename = str(id) + "_" + str(date)

    try:
        os.makedirs('output_data')
    except:
        # it already exists
        pass

    print("Writing the data in JSON format...")
    with open('output_data/' + filename + '.json', 'w') as f:
        json.dump(movie_data, f)

    print("Creating CSVs...")
    weekend_csv, worldwide_csv = create_CSVs(movie_data)

    print("Writing the data to 2 .CSV files...")
    with open('output_data/' + filename + '_weekend.csv', 'w', newline='\n') as f:
        weekend_csv.to_csv(f, index=False)
    with open('output_data/' + filename + '_worldwide.csv', 'w', newline='\n') as f:
        worldwide_csv.to_csv(f, index=False)

    print("Writing the RATIOS to a JSON file...")
    with open('output_data/' + filename + "_ratios.json", 'w') as f:
        json.dump(ratios, f)

    print("Writing the AVERAGES to a JSON file... ")
    with open('output_data/' + filename + "_averages.json", 'w') as f:
        json.dump(averages, f)

    print('Done.')


import sys

try:
    id = sys.argv[1]
except:
    raise Exception("Argument Error: argument missing.")

if not id.isdecimal():
    raise Exception("Argument Error: it should only contain digits.")

# example id: '0372784'

begin = datetime.datetime.now()

get_movie_info(id)

print("\n\nThe execution time is: {time}".format(time=(datetime.datetime.now() - begin)))