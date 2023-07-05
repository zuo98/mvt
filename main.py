
from fastapi import FastAPI, Response
from postgresql_connection import get_mvt


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/mvt/{z}/{x}/{y}")
def mvt(z: int, x: int, y: int):
    res = get_mvt(z, x, y)
    print(res)
    headers = {"Access-Control-Allow-Origin": "*", "Content-type": "application/vnd.mapbox-vector-tile"}
    # "application/x-protobuf"  content_type application/vnd.mapbox-vector-tile
    return Response(content=res, headers=headers, media_type="application/x-protobuf")
