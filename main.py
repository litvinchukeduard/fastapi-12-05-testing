from fastapi import FastAPI

from src.route import ingredients, recipes

app = FastAPI()

app.include_router(ingredients.router, prefix='/api')
app.include_router(recipes.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello World"}

# uvicorn main:app --host 0.0.0.0 --port 8080
