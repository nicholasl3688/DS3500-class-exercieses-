from fastapi import FastAPI, Query
from fastapi import Query
from src import MovieInput
from fastapi import File, UploadFile
from fastapi import HTTPException
from src import MovieResponse
import logging
from src import CSVInfo, DataStorage
import pandas as pd
from pathlib import Path
#main.py
import io


app = FastAPI(title="Movie API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


#a path parameter identifies a resource (movie) to retrieve
@app.get("/demo/movies/{movie_id}")
def demo_get_movie(movie_id: int): #type annotation: it declares the expected type, int
    return {"requested_id": movie_id}



#a query parameter adjusts a request
@app.get("/demo/movies")
def demo_list_movies(limit: int = Query(default=2, ge=1)):
    #The default is 2 when limit is omitted in the query.
    # ge=1 means greater than or equal to one.
    return {"requested_limit": limit}




@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    # movie.title --> "Movie C"
    # movie.release_year --> 2022
    return movie.model_dump() #{"title": "Movie C", "release_year": 2022}




demo_movie_examples = []

@app.post("/demo/movie-examples", response_model=MovieResponse)
def demo_add_movie_example(movie: MovieInput):
    movie_id = len(demo_movie_examples) + 1
    record = movie.model_dump() # {title: "..", "release_year": 2025}
    record["id"] = movie_id

    # updating our list eg, our DB
    demo_movie_examples.append(record)
    return record


#main.py


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

movies = {
    1: {"id": 1, "title": "Movie A", "release_year": 2020},
    2: {"id": 2, "title": "Movie B", "release_year": 2021},
}


#main.py


@app.get("/movies", response_model=list[MovieResponse])
def list_movies(limit: int = Query(default=2, ge=1)):
    result = list(movies.values())[:limit]
    logger.info(f"Returned {len(result)} movies")
    return result



@app.post("/movies", response_model=MovieResponse)
def add_movie(movie: MovieInput):
    record = movie.model_dump()
    new_id = max(movies) + 1
    record["id"] = new_id
    movies[new_id] = record

    logger.info(f"Added movie with id {new_id}")
    return record

# main.py

@app.post("/demo/inspect-csv")
async def demo_inspect_csv(file: UploadFile = File(...)):
    # ... in File(...) means the upload is required.
    contents = await file.read() # reads as bytes e.g. b"title,year\nMovie A,2020\n"
    return {"filename": file.filename,"size_bytes": len(contents)}




@app.get("/demo/movie-lookup/{movie_id}", response_model=MovieResponse)
def demo_lookup_movie(movie_id: int):
    movie = movies.get(movie_id)

    if movie is None:
        logger.warning(f"Movie not found: {movie_id}")
        raise HTTPException( status_code=404, detail="Movie not found")

    return movie



#CSV STORAGE PART DIFJAKSFIAFOAFEA;LWEJREOWQIFDSLKFA

storage = DataStorage()



@app.post("/inspect-csv", response_model=CSVInfo)
async def inspect_csv(file: UploadFile = File(...)):
    # TODO 2: check the filename extension using pathlib.
    # Reject non-CSV files with status 400 and log a WARNING.
    if Path(file.filename).suffix != ".csv":
            logger.warning(f"File not CSV: {file.filename}")
            raise HTTPException( status_code=400, detail="Wrong file type")


    # TODO 3: await the file contents and parse the CSV.
    # Catch expected parsing/decoding errors (e.g. EmptyDataError,ParserError, UnicodeDecodeError) and raise HTTPException
    # with status_code=400.
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except (pd.errors.EmptyDataError,pd.errors.ParserError,UnicodeDecodeError) as error:
        logger.warning(f"Cannot read CSV: {error}")
        raise HTTPException(status_code=400, detail="Cannot read the uploaded CSV")


    # TODO 4: save the DataFrame with storage.save_data().
    # Log the dataset ID, filename at INFO.
    # Return a CSVInfo object with the ID, filename, shape, and column names.
    dataset_id = storage.save_data(df, file.filename)
    logger.info(f"Stored CSV: id={dataset_id}, filename={file.filename}")
    return CSVInfo(
    filename=file.filename,
    rows=df.shape[0],
    columns=df.shape[1],
    column_names=list(df.columns),
    dataset_id=dataset_id,
    )



@app.get("/datasets/{dataset_id}/shape")
def get_dataset_shape(dataset_id: int):
    # TODO 5: get the DataFrame using storage.get_data().
    # If it is missing, log a WARNING and raise HTTPException with status 404.
    # Otherwise, log successful retrieval at INFO.
    # Return a dictionary with dataset_id, rows, and columns.
    data = storage.get_data(dataset_id)
    if data is None:
        logger.warning(f"ID not found: {dataset_id}")
        raise HTTPException( status_code=404, detail="ID not found")
    #missing

    logger.info(f"successfully retrieved dataset with id {dataset_id}")
    return {"dataset_id": dataset_id, "rows": data.shape[0], "columns": data.shape[1]}