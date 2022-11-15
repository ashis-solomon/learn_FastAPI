from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"msg" : "heyy"}

@app.get("/about")
def about():
    return {"msg" : "about page"}