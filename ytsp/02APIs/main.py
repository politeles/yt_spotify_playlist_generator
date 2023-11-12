from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Union

app = FastAPI()

class Video(BaseModel):
    title: str
    id: str
    upload_date: datetime

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/videos/channel/{channel_id}")
async def get_channel_videos(channel_id: str):
    result = list[Video]

    return result


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result