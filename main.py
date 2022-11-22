from typing import Union, Optional

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]



@app.get("/")
async def index():
    return {"msg" : "hi"}

@app.get("/blog")
async def blog(published: Optional[bool] = True, limit: Union[str, None] = 0 ):
    if published is True:
        return f"{limit} published posts from db"
    return fake_items_db[0 : int(limit)]
    return f"{limit} posts from db"

# important ordering of /items
@app.get("/items/text")
async def text(q: Union[str, None] = None):
    return f"text    {q}"

@app.get("/items/{item_id}")
async def get_specific_item(item_id : int):
    return {"item-id" : item_id}

@app.post("/blog")
async def create_blog(blog: Blog):

    return {"data": f"Blog is created with title as {blog.title}!"}



# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=4000)