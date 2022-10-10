from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


# this automatically validates, and makes these properties as required
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='root',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed: ")
        print("Error: ", error)
        time.sleep(2)

# my_posts = [
#     {"title": "title of the post 1", "content": "content of post 1", "id": 1},
#     {"title": "favorite foods", "content": "some foods names", "id": 2}
# ]
#
#
# def get_post_index(id: int):
#     for index, post in enumerate(my_posts):
#         if post["id"] == id:
#             return index


@app.get("/")
async def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * from posts""")
    posts = cursor.fetchall()

    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit()

    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):  # response: Response
    # post = list(filter(lambda x: x['id'] == int(id), my_posts))
    cursor.execute("""SELECT * from posts WHERE id=%s;""", (id,))
    post = cursor.fetchone()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        #
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # index = get_post_index(int(id))
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *;""", (id,))
    post = cursor.fetchone()
    conn.commit()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    # my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # index = get_post_index(int(id))
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id= %s RETURNING *;""",
                   (post.title, post.content, post.published, id))

    post = cursor.fetchone()
    conn.commit()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exists")

    # my_posts[index] = post.dict()

    return {"message": post}
