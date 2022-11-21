from typing import Union, Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    return {"msg" : "hi"}

@app.get("/blog")
async def blog(published: Optional[bool] = True, limit: Union[str, None] = None ):
    if published is True:
        return f"{limit} published posts from db"
    return f"{limit} posts from db"

# important ordering of /items
@app.get("/items/text")
async def text(q: Union[str, None] = None):
    return f"text    {q}"

@app.get("/items/{item_id}")
async def get_specific_item(item_id : int):
    return {"item-id" : item_id}

