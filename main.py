from fastapi import FastAPI, Depends
from typing import List

app = FastAPI()


def get_db():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]


@app.get("/users")
def get_users(db: List[dict] = Depends(get_db)):
    return db
