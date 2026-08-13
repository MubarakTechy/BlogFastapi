from fastapi import FastAPI

from app.auth.router import router as auth_router


app = FastAPI(
    title="Blog API"
)


app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Blog API"
    }