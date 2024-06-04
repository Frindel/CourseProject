from recomendedFilm import RecomendedFilm
from fastapi import Body, Request
from fastapi.responses import JSONResponse
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

recomendedFilmApp = None

def init(module_name, app):

    global recomendedFilmApp

    nice_name = "Рекомендации Фильмов"
    description = 'Данная программа поможет вам подобрать интересные фильмы согласно вашему запросу. Для получения списка рекомендаций, вам всего лишь необходимо описать фильм, который вы бы хотели посмотреть'
   
    module = RecomendedFilm(module_name, nice_name, app, description)
    recomendedFilmApp = module

    database = module.database

    # определение маршрутов api и другой бизнес-логики
    app.add_api_route(f"/api/v1/recomended-film/genre-statistics", genreStatistics, methods=['GET'])
    app.add_api_route(f"/api/v1/recomended-film/releaseDate-statistics", releaseDateStatistics, methods=['GET'])
    app.add_api_route(f"/api/v1/recomended-film/reiting-statistics", reitingStatistics, methods=['GET'])
    app.add_api_route(f"/api/v1/recomended-film/search", recomendFilm, methods=['GET'])
    return module
 
def genreStatistics(request: Request):
    _, dataset = recomendedFilmApp.getDataSetByRequest(request)
    genre_counts = dataset['genres'].value_counts().reset_index()
    genre_counts.columns = ['genre', 'count']
    genre_counts = genre_counts.to_dict(orient='records')
    return JSONResponse(genre_counts)
    
def releaseDateStatistics(request: Request):
    _, dataset = recomendedFilmApp.getDataSetByRequest(request)
    film_year = pd.DataFrame(dataset['release_date'].value_counts().reset_index().values, columns=["year", "count"])
    film_year = film_year.sort_values('year', ascending = True)
    film_year = film_year.to_dict(orient='records')
    return JSONResponse(film_year)

def reitingStatistics(request: Request):
    _, dataset = recomendedFilmApp.getDataSetByRequest(request)
    reiting = pd.DataFrame(dataset['vote_average'].value_counts().reset_index().values, columns=["reiting", "count"])
    reiting['count'] = reiting['count'].astype(int)
    reiting = reiting.sort_values('reiting', ascending=True)
    reiting = reiting.to_dict(orient='records')
    return JSONResponse(reiting)
    
def recomendFilm(request: Request, description):
    success, dataset = recomendedFilmApp.getDataSetByRequest(request)
    if not success:
            return JSONResponse({"error": "Не удалось загрузить датасет"}, status_code=500)

    success, vectorizer = recomendedFilmApp.getModelByRequest(request)
    if not success:
       return JSONResponse({"error": "Не удалось загрузить модель"}, status_code=500)
    
    name = description

    dataset['overview_clean'] = dataset['overview_clean'].fillna('')
    movie_vectors = vectorizer.fit_transform(dataset['overview_clean'])  # Используем метод transform

    user_vector = vectorizer.transform([name])

    cosine_similarities = cosine_similarity(user_vector, movie_vectors).flatten()

    recommended_movie_indices = cosine_similarities.argsort()[:-11:-1]

    recommended_movies = dataset.iloc[recommended_movie_indices]
        
    recFilm = pd.DataFrame(recommended_movies[["title", "release_date"]])
    recFilm = recFilm.to_dict(orient='records')
    return JSONResponse(recFilm)