from typing import Optional
from fastapi import FastAPI
from package.routers import blogRouter, userRouter
from package.models import Base
from package.db import engine

# import uvicorn
# Base.metadata.drop_all(engine)
Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(userRouter.router)
app.include_router(blogRouter.router)

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=9000)
