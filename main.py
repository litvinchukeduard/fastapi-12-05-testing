from fastapi import FastAPI

from src.route import ingredients, recipes, auth, email

app = FastAPI()

app.include_router(ingredients.router, prefix='/api')
app.include_router(recipes.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(email.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello World"}

# uvicorn main:app --host 0.0.0.0 --port 8080
