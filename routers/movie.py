from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from schemas.movie import Movie
from typing import Optional, List
from config.database import  Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService

from fastapi import APIRouter

movie_router = APIRouter()

@movie_router.get('/movies',tags=['movies'],response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.get('/movies/{id}',tags=['movies'],response_model=Movie)
def get_movie(id: int = Path(ge=1,le=2000)) -> Movie:
    # result = list(filter(lambda movie: movie['id']==id,movies))
    # result = [JSONResponse(content=movie) for movie in movies if movie['id']==id]
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})

    # result = [JSONResponse(status_code=404,content=[]) if movie['id'] != id else JSONResponse(content=movie) for movie in movies]
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.get('/movies/',tags=['movies'],response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category)

    if not result:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})
    # result = list(filter(lambda movie: movie['category']==category,movies))
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.post('/movies',tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db= Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201,content={"mensaje": "Se ha registrado la pelicula"})

@movie_router.put('/movies/{id}',tags=['movies'],response_model=dict,status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)

    if not result:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})
    
    MovieService(db).update_movie(id,movie)
    return JSONResponse(status_code=200,content={"mensaje": "Se ha modificado la pelicula"}) 

@movie_router.delete('/movies/{id}',tags=['movies'], response_model=dict,status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)

    if not result:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})
    MovieService(db).delete_movie(id)
    # result = [movies.remove(movie) for movie in movies if movie['id'] == id] 
    return JSONResponse(status_code=200,content={"mensaje": "Se ha removido la pelicula"})